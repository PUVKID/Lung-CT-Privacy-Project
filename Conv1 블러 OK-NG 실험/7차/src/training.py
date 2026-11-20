"""σ0 모델을100회 새 학습하고 선정 가중치를 고정해10개 블러를 평가합니다."""

import csv
import gc
import hashlib
import json
import math
import os
from pathlib import Path
import random
import shutil
import time

import numpy as np
from sklearn.metrics import accuracy_score, average_precision_score, confusion_matrix, f1_score, roc_auc_score
import torch
from torch import nn
from torch.utils.data import DataLoader

from .data import CTDataset, prepare_dataset
from .model import SplitResNet50
from .state import atomic_json, now_kst


def binary_metrics(labels, probabilities, logits=None):
    y = np.asarray(labels, dtype=int)
    p = np.asarray(probabilities, dtype=float)
    if len(y) == 0 or len(y) != len(p) or not np.isfinite(p).all():
        raise ValueError("평가 라벨·예측 확률이 유효하지 않습니다.")
    if not set(y).issubset({0, 1}) or np.any((p < 0) | (p > 1)):
        raise ValueError("이진 라벨/확률 범위가 유효하지 않습니다.")
    score = p if logits is None else np.asarray(logits, dtype=np.float64)
    if len(score) != len(y) or not np.isfinite(score).all():
        raise ValueError("평가 로짓의 수 또는 유한성이 유효하지 않습니다.")
    predicted = (p >= 0.5).astype(int) if logits is None else (score >= 0).astype(int)
    consistent = bool(np.array_equal(predicted, (p >= 0.5).astype(int)))
    matrix = confusion_matrix(y, predicted, labels=[0, 1])
    tn, fp, fn, tp = matrix.ravel()
    return {"accuracy": float(accuracy_score(y, predicted)),
            "auc": float(roc_auc_score(y, score)) if len(set(y)) == 2 else None,
            "pr_auc": float(average_precision_score(y, score)) if len(set(y)) == 2 else None,
            "sensitivity": float(tp / (tp + fn)) if tp + fn else None,
            "specificity": float(tn / (tn + fp)) if tn + fp else None,
            "f1": float(f1_score(y, predicted, zero_division=0)),
            "confusion_matrix": matrix.tolist(), "threshold": 0.5, "n_images": len(y),
            "unit": "image", "patient_id_available": False, "threshold_consistent": consistent,
            "threshold_rounding_differences": int(np.count_nonzero(predicted != (p >= 0.5).astype(int))),
            "ranking_score": "raw_logits" if logits is not None else "probability",
            "ng_probability_mean": float(p.mean()), "brier_score": float(np.mean((p-y)**2)),
            "false_positive_rate": float(fp/(tn+fp)) if tn+fp else None}


def stable_binary_loss(logits, targets, dtype=torch.float32, reduction="mean"):
    # 확신한 음성의 input-logsigmoid 상쇄를 피하는 동일한 이진 교차 엔트로피입니다.
    signed = logits.to(dtype) * (targets.to(dtype) * 2 - 1)
    values = torch.nn.functional.softplus(-signed)
    if reduction == "sum":
        return values.sum()
    if reduction == "none":
        return values
    if reduction != "mean":
        raise ValueError("지원하지 않는 손실 집계 방식입니다.")
    return values.mean()


class TrainingControl:
    def __init__(self, min_delta=1e-4, patience=15, enabled=True):
        if min_delta < 0 or not math.isfinite(min_delta) or patience < 1 or type(enabled) is not bool:
            raise ValueError("조기 종료 정책이 유효하지 않습니다.")
        self.min_delta, self.patience = float(min_delta), int(patience)
        self.enabled = enabled
        self.best_raw_loss, self.best_raw_epoch = math.inf, 0
        self.meaningful_best_loss, self.stale_epochs = math.inf, 0
        self.optimizer_steps = 0
        self.shadow_stop_epoch, self.shadow_best_raw_epoch = 0, 0

    def observe(self, loss, epoch):
        if not math.isfinite(loss) or loss < 0:
            raise ValueError("검증 손실은 유한한 0 이상이어야 합니다.")
        raw = loss < self.best_raw_loss
        meaningful = loss < self.meaningful_best_loss - self.min_delta
        if raw:
            self.best_raw_loss, self.best_raw_epoch = float(loss), int(epoch)
        if meaningful:
            self.meaningful_best_loss, self.stale_epochs = float(loss), 0
        else:
            self.stale_epochs += 1
        would_stop = self.stale_epochs >= self.patience
        if would_stop and not self.shadow_stop_epoch:
            self.shadow_stop_epoch, self.shadow_best_raw_epoch = int(epoch), self.best_raw_epoch
        return {"raw_improved": raw, "meaningful_improved": meaningful,
                "would_stop": would_stop, "should_stop": self.enabled and would_stop}

    def state_dict(self):
        return {key: getattr(self, key) for key in ["min_delta", "patience", "best_raw_loss", "best_raw_epoch",
                                                    "meaningful_best_loss", "stale_epochs", "optimizer_steps",
                                                    "enabled", "shadow_stop_epoch", "shadow_best_raw_epoch"]}

    def load_state_dict(self, values):
        if (values["min_delta"] != self.min_delta or values["patience"] != self.patience
                or values.get("enabled", True) is not self.enabled):
            raise ValueError("재개 조기 종료 정책이 현재 설정과 다릅니다.")
        for key in ["best_raw_loss", "best_raw_epoch", "meaningful_best_loss", "stale_epochs", "optimizer_steps"]:
            setattr(self, key, values[key])
        self.shadow_stop_epoch = values.get("shadow_stop_epoch", 0)
        self.shadow_best_raw_epoch = values.get("shadow_best_raw_epoch", 0)


def build_optimizer_scheduler(parameters, config):
    optimizer = torch.optim.AdamW(parameters, lr=config["learning_rate"], weight_decay=config["weight_decay"])
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode="min", factor=config["scheduler_factor"], patience=config["scheduler_patience"],
        threshold=config["min_delta"], threshold_mode="abs", min_lr=config["min_learning_rate"])
    return optimizer, scheduler


def per_source_metrics(records, labels, probabilities, logits):
    result = {}
    for source in sorted({row["source_class"] for row in records}):
        indices = [index for index, row in enumerate(records) if row["source_class"] == source]
        result[source] = binary_metrics([labels[i] for i in indices], [probabilities[i] for i in indices],
                                        logits=[logits[i] for i in indices])
        result[source]["auc_note"] = "단일 라벨 원본 클래스는 AUC/AP를 계산하지 않습니다." if result[source]["auc"] is None else None
    return result


def seed_everything(seed, cpu_threads=4):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.set_num_threads(cpu_threads)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True
    torch.use_deterministic_algorithms(True)


def precision_policy(name, device_type, bf16_supported=None):
    if name not in {"fp32", "fp16", "bf16"}:
        raise ValueError(f"지원하지 않는 정밀도 설정입니다: {name}")
    if name != "fp32" and device_type != "cuda":
        raise ValueError("이 실험의 FP16/BF16은 CUDA 전용입니다. CPU 실행은 precision=fp32를 명시하세요.")
    if name == "bf16":
        supported = torch.cuda.is_bf16_supported() if bf16_supported is None else bf16_supported
        if not supported:
            raise RuntimeError("요청한 BF16을 현재 CUDA 기기가 지원하지 않습니다. FP16으로 자동 대체하지 않았습니다.")
    return {"name": name, "dtype": {"fp32": torch.float32, "fp16": torch.float16, "bf16": torch.bfloat16}[name],
            "autocast_enabled": name != "fp32", "use_grad_scaler": name == "fp16"}


def restore_rng_state(checkpoint, device):
    # CUDA map_location으로 읽어도 생성기 상태는 CPU ByteTensor로 복구해야 합니다.
    torch.set_rng_state(checkpoint["torch_rng_state"].cpu())
    if device.type == "cuda":
        torch.cuda.set_rng_state_all([state.cpu() for state in checkpoint["cuda_rng_state"]])


def device_information(device):
    result = {"type": device.type, "name": "CPU", "torch_version": torch.__version__,
              "cuda_version": torch.version.cuda, "deterministic_algorithms": True}
    if device.type == "cuda":
        info = torch.cuda.get_device_properties(device)
        free, total = torch.cuda.mem_get_info(device)
        result.update(name=info.name, total_memory_gb=round(total / 2 ** 30, 2),
                      free_memory_gb=round(free / 2 ** 30, 2), capability=list(torch.cuda.get_device_capability(device)),
                      bf16_supported=torch.cuda.is_bf16_supported())
    return result


def _loader(dataset, config, device):
    return DataLoader(dataset, batch_size=config["batch_size"], shuffle=False,
                      num_workers=config.get("num_workers", 0), pin_memory=device.type == "cuda")


def evaluate(model, loader, device, precision, state=None, stage="validation", return_logits=False):
    model.eval()
    labels, probabilities, raw_logits = [], [], []
    total_loss = 0.0
    count = 0
    with torch.inference_mode():
        for batch_index, (images, target) in enumerate(loader, 1):
            images, target = images.to(device, non_blocking=True), target.to(device, non_blocking=True)
            # 평가는 학습 AMP와 분리하여 FP32 정방향과 FP64 손실/확률 계산을 사용합니다.
            with torch.autocast(device_type=device.type, enabled=False):
                logits = model(images.float())
            logits64 = logits.double()
            loss = stable_binary_loss(logits64, target, dtype=torch.float64, reduction="sum")
            if not torch.isfinite(loss):
                raise FloatingPointError("평가 손실에 NaN/Inf가 발생했습니다.")
            total_loss += loss.item()
            count += len(target)
            labels.extend(target.cpu().int().tolist())
            probabilities.extend(logits64.sigmoid().cpu().tolist())
            raw_logits.extend(logits64.cpu().tolist())
            if state and (batch_index == 1 or batch_index % 10 == 0 or batch_index == len(loader)):
                state.update(stage=stage, batch=batch_index, batches=len(loader),
                             message=f"{'시험' if stage == 'testing' else '검증'} 원본 영상 {count}개 평가 중")
    metrics = binary_metrics(labels, probabilities, logits=raw_logits)
    metrics["loss"] = total_loss / count
    metrics.update(forward_precision="fp32", loss_precision="fp64_signed_softplus",
                   logit_min=min(raw_logits), logit_max=max(raw_logits))
    records = getattr(loader.dataset, "records", None)
    if records is not None:
        if len(records) != count:
            raise ValueError("원본 클래스별 평가 목록과 예측 수가 다릅니다.")
        metrics["per_source"] = per_source_metrics(records, labels, probabilities, raw_logits)
    return (metrics, labels, probabilities, raw_logits) if return_logits else (metrics, labels, probabilities)


def _save_predictions(path, rows, labels, probabilities):
    with Path(path).open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["relative_path", "label", "ng_probability"])
        for row, label, probability in zip(rows, labels, probabilities):
            writer.writerow([row["relative_path"], label, probability])


def _save_checkpoint(path, payload):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    torch.save(payload, temporary)
    os.replace(temporary, path)


def _freeze_prefix_checkpoint(source, destination):
    """기존 최저 검증 손실 파일을 RNG 사용 없이 한 번 고정하고 복사 해시를 확인합니다."""
    source, destination = Path(source), Path(destination)
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    if destination.exists():
        if hashlib.sha256(destination.read_bytes()).hexdigest() != digest:
            raise ValueError("이미 고정된 관찰용 체크포인트를 교체할 수 없습니다.")
        return digest
    temporary = destination.with_suffix(".tmp")
    try:
        shutil.copyfile(source, temporary)
        if hashlib.sha256(temporary.read_bytes()).hexdigest() != digest:
            raise ValueError("관찰용 체크포인트 복사 해시가 다릅니다.")
        os.replace(temporary, destination)
    finally:
        if temporary.exists():
            temporary.unlink()
    return digest


def _check_prefix_hash(path, expected):
    if (not isinstance(expected, str) or len(expected) != 64
            or hashlib.sha256(Path(path).read_bytes()).hexdigest() != expected):
        raise ValueError("고정된 관찰용 체크포인트 해시가 재개 기록과 다릅니다.")


from .identity import (PROTOCOL, SIGMAS, _run_identity, file_sha256, validate_config,
                       validate_run, validate_fixed_result, load_selection)
from .model import GaussianDCTBlur


def tensor_state_digest(state):
    """이름·dtype·shape·모든 tensor 바이트를 결합하며 BN buffer도 포함합니다."""
    value = hashlib.sha256()
    for name, tensor in sorted(state.items()):
        item = tensor.detach().cpu().contiguous()
        value.update(json.dumps([name, str(item.dtype), list(item.shape)], ensure_ascii=False).encode("utf-8"))
        value.update(item.reshape(-1).view(torch.uint8).numpy().tobytes())
    return value.hexdigest()


def checkpoint_load(path, run_id):
    # 본 실행이 만든, 고정 폴더 안의 로컬 파일만 읽습니다.
    saved = torch.load(path, map_location="cpu", weights_only=True)
    if (saved.get("run_id") != run_id or saved.get("protocol") != PROTOCOL
            or saved.get("protocol_fixed_model") is not True or saved.get("training_sigma") != 0
            or saved.get("sigma") != 0 or type(saved.get("epoch")) is not int or not 1 <= saved["epoch"] <= 100):
        raise ValueError("체크포인트의 단일 σ0 학습·실행 식별자가 다릅니다.")
    return saved


def checkpoint_base(run_id, epoch, model, control, policy):
    return {"run_id": run_id, "protocol": PROTOCOL, "protocol_fixed_model": True,
            "training_sigma": 0, "sigma": 0, "epoch": epoch, "model": model.state_dict(),
            "training_control": control.state_dict(), "training_policy": policy}


def numpy_rng_state():
    name, values, position, gaussian, cached = np.random.get_state()
    return {"name": name, "values": values.tolist(), "position": position, "gaussian": gaussian, "cached": cached}


def restore_all_rng(saved, device):
    restore_rng_state(saved, device)
    random.setstate(saved["python_rng_state"])
    item = saved["numpy_rng_state"]
    np.random.set_state((item["name"], np.asarray(item["values"], dtype=np.uint32), item["position"], item["gaussian"], item["cached"]))


def _save_fixed_predictions(path, records, labels, probabilities, logits, identity, sigma):
    with Path(path).open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["relative_path", "label", "ng_probability", "logit", "run_id", "training_sigma", "evaluation_sigma",
                         "checkpoint_sha256", "model_state_sha256", "protocol_fixed_model"])
        for row, label, probability, logit in zip(records, labels, probabilities, logits):
            writer.writerow([row["relative_path"], label, probability, logit, identity["run_id"], 0, sigma,
                             identity["checkpoint_sha256"], identity["model_state_sha256"], True])


def evaluate_frozen_sigmas(model, splits, loaders, device, root, run_id, selection, state, optimizer_steps):
    """optimizer를 받거나 만들지 않고 하나의 선정 모델을10개의 입력 블러로 평가합니다."""
    root = Path(root)
    destination = root / "work/results" / ("run_" + run_id)
    model.eval().requires_grad_(False)
    expected_digest = selection["model_state_sha256"]
    if tensor_state_digest(model.state_dict()) != expected_digest:
        raise ValueError("평가 시작 모델이 동결 state와 다릅니다.")
    values = []
    for index, sigma in enumerate(SIGMAS):
        path = destination / f"sigma_{sigma}_metrics.json"
        entry = state.data["sigma_queue"][index]
        if path.exists():
            value = validate_fixed_result(root, json.loads(path.read_text(encoding="utf-8")), run_id)
            entry.update(status="completed", result=path.relative_to(root).as_posix())
            values.append(value)
            continue
        # sigma 속성만 변경하면 transfer 캐시가 남으므로 새 모듈로 교체합니다.
        model.blur = GaussianDCTBlur(sigma).to(device)
        if tensor_state_digest(model.state_dict()) != expected_digest or file_sha256(root / selection["selected_checkpoint"]) != selection["checkpoint_sha256"]:
            raise ValueError("평가 조건 시작 전 고정 가중치 또는 체크포인트가 변경됐습니다.")
        entry.update(status="running")
        state.update(phase="evaluation", training_status="completed", stage="validation", status="running",
                     sigma=sigma, sigma_index=index + 1, evaluation_current_sigma=sigma, eval_optimizer_steps=0,
                     message=f"학습 완료 모델 고정 · 블러 σ={sigma} 평가 중")
        validation, y_val, p_val, z_val = evaluate(model, loaders[0], device, None, state, return_logits=True)
        test, y_test, p_test, z_test = evaluate(model, loaders[1], device, None, state, stage="testing", return_logits=True)
        if (any(module.training for module in model.modules()) or any(p.grad is not None for p in model.parameters())
                or tensor_state_digest(model.state_dict()) != expected_digest
                or file_sha256(root / selection["selected_checkpoint"]) != selection["checkpoint_sha256"]):
            raise ValueError("고정 평가에서 학습 상태·기울기·가중치 또는 BN buffer가 변했습니다.")
        prediction_files = {}
        for name, labels, probabilities, logits in [("validation", y_val, p_val, z_val), ("test", y_test, p_test, z_test)]:
            output = destination / f"sigma_{sigma}_{name}_predictions_private.csv"
            _save_fixed_predictions(output, splits[name], labels, probabilities, logits, selection, sigma)
            prediction_files[name] = {"relative_path": output.relative_to(root).as_posix(), "sha256": file_sha256(output)}
        value = {**selection, "sigma": sigma, "evaluation_sigma": sigma, "eval_optimizer_steps": 0,
                 "optimizer_steps": optimizer_steps, "validation": validation, "test": test,
                 "prediction_files": prediction_files, "completed_at": now_kst(), "selected_checkpoint_policy": "σ0 검증 원시 손실 최저 모델",
                 "test_use": "동일 시험셋 탐색적 비교; 시험 결과로 모델·σ·임계값을 선택하지 않습니다.",
                 "state_digest_before": expected_digest, "state_digest_after": tensor_state_digest(model.state_dict()),
                 "checkpoint_sha256_before": selection["checkpoint_sha256"], "checkpoint_sha256_after": file_sha256(root / selection["selected_checkpoint"])}
        atomic_json(path, value)
        validate_fixed_result(root, value, run_id)
        entry.update(status="completed", result=path.relative_to(root).as_posix())
        state.update(evaluation=value, message=f"고정 모델 σ={sigma} 평가 완료")
        state.event("고정 모델 평가 완료", {"sigma": sigma, "checkpoint_sha256": selection["checkpoint_sha256"], "eval_optimizer_steps": 0})
        values.append(value)
    return values


def run_training(config, root, state, device_name="cuda"):
    root = Path(root)
    validate_config(config)
    from .model import block_weight_downloads
    block_weight_downloads()
    started = time.monotonic()
    seed_everything(config["seed"], config.get("cpu_threads", 4))
    if device_name == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA를 사용할 수 없습니다. 과학 조건을 바꿔 CPU로 대체하지 않습니다.")
    device = torch.device(device_name)
    precision = precision_policy(config["precision"], device.type)
    manifest = prepare_dataset(config, root)
    run_id, settings = _run_identity(root, config, manifest["manifest_sha256"])
    result_dir = root / "work/results" / ("run_" + run_id)
    checkpoint_dir = root / "work/checkpoints" / ("run_" + run_id)
    result_dir.mkdir(parents=True, exist_ok=True)
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    policy = {"max_epochs": 100, "patience": config["early_stopping_patience"], "early_stopping_enabled": False,
              "min_delta": config["min_delta"], "min_delta_mode": "absolute", "batch_size": config["batch_size"],
              "optimizer": "AdamW", "initial_learning_rate": config["learning_rate"], "weight_decay": config["weight_decay"],
              "scheduler_patience": config["scheduler_patience"], "scheduler_factor": config["scheduler_factor"],
              "min_learning_rate": config["min_learning_rate"], "evaluation_forward": "fp32", "evaluation_loss": "fp64_signed_softplus"}
    metadata = {**settings, "run_id": run_id, "protocol": PROTOCOL, "protocol_fixed_model": True,
                "training_sigma": 0, "started_at": now_kst(), "device": device_information(device), "training_policy": policy}
    atomic_json(result_dir / "run_metadata.json", metadata)
    state.update(run_id=run_id, phase="training", training_status="running", stage="loading_model", sigma=0,
                 device=metadata["device"], training_policy=policy, precision={k: v for k, v in precision.items() if k != "dtype"},
                 dataset=manifest["summary"], result_directory=result_dir.relative_to(root).as_posix(), optimizer_steps=0,
                 checkpoint_sha256=None, model_state_sha256=None, selected_checkpoint=None,
                 message="σ0에서 새 모델 학습 준비 · 블러10조건은 학습 완료 후 평가")
    splits = manifest["splits"]
    training = CTDataset(splits["train"], config["image_size"], training=True, samples_per_class=config["samples_per_class"], seed=config["seed"])
    validation = CTDataset(splits["validation"], config["image_size"], training=False)
    test = CTDataset(splits["test"], config["image_size"], training=False)
    train_loader, val_loader, test_loader = [_loader(dataset, config, device) for dataset in [training, validation, test]]
    weights = Path(config["initial_weights_path"])
    weights = weights if weights.is_absolute() else root / weights
    model = SplitResNet50(sigma=0, pretrained=True, weights_path=weights, expected_weights_sha256=config["initial_weights_sha256"]).to(device)
    optimizer, scheduler = build_optimizer_scheduler([p for p in model.parameters() if p.requires_grad], config)
    scaler = torch.amp.GradScaler("cuda", enabled=precision["use_grad_scaler"])
    control = TrainingControl(config["min_delta"], config["early_stopping_patience"], enabled=False)
    best_path = checkpoint_dir / "sigma_0_best.pt"
    last_path = checkpoint_dir / "sigma_0_last.pt"
    history = []
    start_epoch = 1
    if last_path.exists():
        saved = checkpoint_load(last_path, run_id)
        history = saved["history"]
        if (len(history) != saved["epoch"] or [row["epoch"] for row in history] != list(range(1, saved["epoch"] + 1))
                or any(row["sigma"] != 0 for row in history) or saved["training_policy"] != policy):
            raise ValueError("마지막 완료 epoch·이력·학습 정책이 서로 다릅니다.")
        model.load_state_dict(saved["model"], strict=True)
        optimizer.load_state_dict(saved["optimizer"])
        scheduler.load_state_dict(saved["scheduler"])
        scaler.load_state_dict(saved["scaler"])
        control.load_state_dict(saved["training_control"])
        if control.optimizer_steps != saved["epoch"] * len(train_loader):
            raise ValueError("완료 epoch와 실제 optimizer 업데이트 수가 다릅니다.")
        restore_all_rng(saved, device)
        start_epoch = saved["epoch"] + 1
        if not best_path.exists() or checkpoint_load(best_path, run_id)["epoch"] != control.best_raw_epoch:
            raise ValueError("재개에 필요한 현재 run의 최저 검증 손실 모델이 없습니다.")
        state.event("σ0 마지막 완료 회차 재개", {"next_epoch": start_epoch, "optimizer_steps": control.optimizer_steps})
    elif best_path.exists() or list(result_dir.glob("sigma_*_metrics.json")) or (result_dir / "fixed_model_selection.json").exists():
        raise ValueError("last 없이 남은 모델·결과가 있어 새 학습으로 덮어쓰지 않습니다.")
    state.data["history"] = list(history)
    for epoch in range(start_epoch, 101):
        if (result_dir / "fixed_model_selection.json").exists() or list(result_dir.glob("sigma_*_metrics.json")):
            raise ValueError("선정·평가 뒤 추가 학습을 허용하지 않습니다.")
        training.set_epoch(epoch - 1)
        model.train()
        total_loss, seen = 0.0, {"OK": 0, "NG": 0}
        tick = time.monotonic()
        state.update(phase="training", stage="training", epoch=epoch, batch=0, batches=len(train_loader), sigma=0,
                     seen_per_class=seen.copy(), message=f"블러 없는 모델 학습 {epoch}/100회")
        for batch_index, (images, target) in enumerate(train_loader, 1):
            state.data["attempted_batch"] = batch_index
            images, target = images.to(device, non_blocking=True), target.to(device, non_blocking=True)
            optimizer.zero_grad(set_to_none=True)
            with torch.autocast(device_type=device.type, dtype=precision["dtype"], enabled=precision["autocast_enabled"]):
                logits = model(images)
                loss = stable_binary_loss(logits, target, dtype=torch.float32)
            if not torch.isfinite(loss):
                raise FloatingPointError(f"σ0 epoch={epoch} batch={batch_index}: 비유한 학습 손실")
            scaler.scale(loss).backward()
            scaler.unscale_(optimizer)
            gradient_norm = nn.utils.clip_grad_norm_(model.parameters(), 1.0, error_if_nonfinite=True)
            scaler.step(optimizer)
            scaler.update()
            control.optimizer_steps += 1
            total_loss += loss.item() * len(target)
            ng = int(target.sum().item())
            seen["NG"] += ng
            seen["OK"] += len(target) - ng
            if batch_index == 1 or batch_index % config["status_every_batches"] == 0 or batch_index == len(train_loader):
                state.update(batch=batch_index, seen_per_class=seen.copy(), train_loss=total_loss / sum(seen.values()),
                             optimizer_steps=control.optimizer_steps, run_optimizer_steps=control.optimizer_steps,
                             learning_rate=optimizer.param_groups[0]["lr"], last_gradient_norm=gradient_norm.item(),
                             epoch_elapsed_seconds=time.monotonic() - tick, elapsed_seconds=time.monotonic() - started)
        if seen != {"OK": config["samples_per_class"], "NG": config["samples_per_class"]}:
            raise AssertionError("클래스별 온라인 학습 표본 수가 명세와 다릅니다.")
        state.update(stage="validation", batch=0, batches=len(val_loader), message="σ0 검증 손실로만 모델 선정 중")
        val_metrics, _, _ = evaluate(model, val_loader, device, precision, state)
        lr_before = optimizer.param_groups[0]["lr"]
        decision = control.observe(val_metrics["loss"], epoch)
        scheduler.step(val_metrics["loss"])
        row = {"sigma": 0, "epoch": epoch, "train_loss": total_loss / len(training), "val_loss": val_metrics["loss"],
               "val_accuracy": val_metrics["accuracy"], "val_auc": val_metrics["auc"], "seen_per_class": seen.copy(),
               "seconds": time.monotonic() - tick, "learning_rate": lr_before, "next_learning_rate": optimizer.param_groups[0]["lr"],
               "optimizer_steps": control.optimizer_steps, "best_raw_epoch": control.best_raw_epoch,
               "meaningful_best_loss": control.meaningful_best_loss, "early_stopping_wait": control.stale_epochs}
        history.append(row)
        state.data["history"] = list(history)
        base = checkpoint_base(run_id, epoch, model, control, policy)
        if decision["raw_improved"]:
            _save_checkpoint(best_path, {**base, "validation": val_metrics})
        _save_checkpoint(last_path, {**base, "optimizer": optimizer.state_dict(), "scheduler": scheduler.state_dict(),
                                   "scaler": scaler.state_dict(), "history": list(history), "torch_rng_state": torch.get_rng_state(),
                                   "cuda_rng_state": torch.cuda.get_rng_state_all() if device.type == "cuda" else [],
                                   "python_rng_state": random.getstate(), "numpy_rng_state": numpy_rng_state()})
        atomic_json(result_dir / "sigma_0_history.json", history)
        state.update(best_epoch=control.best_raw_epoch, best_raw_epoch=control.best_raw_epoch, best_raw_loss=control.best_raw_loss,
                     learning_rate=optimizer.param_groups[0]["lr"], early_stopping_wait=control.stale_epochs)
        state.event("σ0 학습 회차 완료", row)
        print(json.dumps(row, ensure_ascii=False), flush=True)
    if len(history) != 100 or control.optimizer_steps != 100 * len(train_loader):
        raise ValueError("σ0 학습100회를 모두 마치지 않아 블러 평가를 시작하지 않습니다.")
    best = checkpoint_load(best_path, run_id)
    if best["epoch"] != control.best_raw_epoch:
        raise ValueError("선정 best epoch와 전체 검증 이력이 다릅니다.")
    # 평가 모델을 새로 만들며 학습의 gradient·optimizer를 넘기지 않습니다.
    evaluation_model = SplitResNet50(sigma=0, pretrained=False).to(device).eval().requires_grad_(False)
    evaluation_model.load_state_dict(best["model"], strict=True)
    selection = {"run_id": run_id, "protocol": PROTOCOL, "protocol_fixed_model": True, "training_sigma": 0,
                 "best_epoch": best["epoch"], "checkpoint_epoch": best["epoch"], "epochs_ran": 100,
                 "selected_checkpoint": best_path.relative_to(root).as_posix(), "checkpoint_sha256": file_sha256(best_path),
                 "model_state_sha256": tensor_state_digest(evaluation_model.state_dict())}
    selection_path = result_dir / "fixed_model_selection.json"
    if selection_path.exists():
        if json.loads(selection_path.read_text(encoding="utf-8")) != selection:
            raise ValueError("이미 동결한 모델 identity를 교체할 수 없습니다.")
    else:
        atomic_json(selection_path, selection)
    state.update(**{key: selection[key] for key in ["best_epoch", "checkpoint_sha256", "model_state_sha256", "selected_checkpoint"]},
                 phase="evaluation", training_status="completed", epoch=100, eval_optimizer_steps=0)
    evaluate_frozen_sigmas(evaluation_model, splits, [val_loader, test_loader], device, root, run_id,
                          selection, state, control.optimizer_steps)
    state.update(phase="completed", stage="completed", status="completed", training_status="completed", pid=None,
                 evaluation_current_sigma=None, elapsed_seconds=time.monotonic() - started,
                 message="σ0 모델100회 학습과 동일 가중치 블러10단계 평가 완료")
    return state.data

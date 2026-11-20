"""강도마다 새100회 독립 학습 뒤 해당 모델의 분류·후보 복원 점수를 계산합니다."""

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
            "n_correct": int(np.count_nonzero(predicted == y)),
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


from .identity import (PROTOCOL, SIGMAS, _run_identity, file_sha256, readonly_input,
                       validate_config, validate_run, validate_result, validate_privacy_result, load_selection, result_binding)
from .privacy import run_privacy


def tensor_state_digest(state):
    """이름·dtype·shape와 BN buffer를 포함한 전체 tensor 바이트를 결합합니다."""
    value = hashlib.sha256()
    for name, tensor in sorted(state.items()):
        item = tensor.detach().cpu().contiguous()
        value.update(json.dumps([name, str(item.dtype), list(item.shape)], ensure_ascii=False).encode())
        value.update(item.reshape(-1).view(torch.uint8).numpy().tobytes())
    return value.hexdigest()


def checkpoint_load(path, run_id, sigma):
    # 현재 실행이 만든 알려진 로컬 파일만 weights_only로 읽습니다.
    saved = torch.load(path, map_location="cpu", weights_only=True)
    if (saved.get("run_id") != run_id or saved.get("protocol") != PROTOCOL
            or saved.get("protocol_fixed_model") is not False or type(saved.get("sigma")) is not int
            or saved.get("sigma") != sigma or type(saved.get("training_sigma")) is not int or saved["training_sigma"] != sigma
            or type(saved.get("epoch")) is not int or not 1 <= saved["epoch"] <= 100):
        raise ValueError("체크포인트의 독립 학습 강도·실행 식별자가 다릅니다.")
    return saved


def numpy_rng_state():
    name, values, position, gaussian, cached = np.random.get_state()
    return {"name": name, "values": values.tolist(), "position": position, "gaussian": gaussian, "cached": cached}


def restore_all_rng(saved, device):
    restore_rng_state(saved, device)
    random.setstate(saved["python_rng_state"])
    item = saved["numpy_rng_state"]
    np.random.set_state((item["name"], np.asarray(item["values"], dtype=np.uint32), item["position"], item["gaussian"], item["cached"]))


def checkpoint_base(run_id, sigma, epoch, model, control, policy):
    return {"run_id": run_id, "protocol": PROTOCOL, "protocol_fixed_model": False,
            "training_sigma": sigma, "sigma": sigma, "epoch": epoch, "model": model.state_dict(),
            "training_control": control.state_dict(), "training_policy": policy}


def _save_bound_predictions(path, records, labels, probabilities, logits, selection):
    with Path(path).open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        keys = ["run_id", "sigma", "training_sigma", "checkpoint_sha256", "model_state_sha256", "protocol_fixed_model"]
        writer.writerow(["relative_path", "label", "ng_probability", "logit", *keys])
        for row, label, probability, logit in zip(records, labels, probabilities, logits):
            writer.writerow([row["relative_path"], label, probability, logit, *[selection[key] for key in keys]])


def classify(model, splits, loaders, device, root, selection, state, optimizer_steps):
    """학습이 완료된 해당 강도 best만 eval 상태로 평가하며 추가 갱신하지 않습니다."""
    sigma, run_id = selection["sigma"], selection["run_id"]
    directory = root / "work/results" / ("run_" + run_id)
    path = directory / f"sigma_{sigma}_metrics.json"
    if path.exists():
        return validate_result(root, json.loads(path.read_text(encoding="utf-8")), run_id)
    before = tensor_state_digest(model.state_dict())
    if before != selection["model_state_sha256"]:
        raise ValueError("분류 평가 시작 state가 선정 모델과 다릅니다.")
    values, files = {}, {}
    for name, loader in zip(["validation", "test"], loaders):
        metrics, labels, probabilities, logits = evaluate(model, loader, device, None, state,
                                                        stage="testing" if name == "test" else "validation", return_logits=True)
        output = directory / f"sigma_{sigma}_{name}_predictions_private.csv"
        _save_bound_predictions(output, splits[name], labels, probabilities, logits, selection)
        files[name] = {"relative_path": output.relative_to(root).as_posix(), "sha256": file_sha256(output)}
        values[name] = metrics
    after = tensor_state_digest(model.state_dict())
    if (before != after or any(m.training for m in model.modules()) or any(p.grad is not None for p in model.parameters())
            or file_sha256(root / selection["selected_checkpoint"]) != selection["checkpoint_sha256"]):
        raise ValueError("분류 평가에서 모델 state·BN·gradient·체크포인트가 변했습니다.")
    value = {**selection, **values, "evaluation_sigma": sigma, "eval_optimizer_steps": 0,
             "optimizer_steps": optimizer_steps, "prediction_files": files, "completed_at": now_kst(),
             "state_digest_before": before, "state_digest_after": after,
             "selected_checkpoint_policy": "해당 강도100회 학습 중 raw 검증 손실 최저 모델",
             "test_use": "기존 시험셋의 탐색적 재사용; 시험 결과로 모델·강도·임계값을 선택하지 않음"}
    atomic_json(path, value)
    return validate_result(root, value, run_id)


def run_training(config, root, state, device_name="cuda"):
    root = Path(root)
    validate_config(config)
    from .model import block_weight_downloads
    block_weight_downloads()
    started = time.monotonic()
    if device_name == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA를 사용할 수 없습니다. 과학 조건을 자동 대체하지 않습니다.")
    device = torch.device(device_name)
    precision = precision_policy(config["precision"], device.type)
    manifest = prepare_dataset(config, root)
    run_id, settings = _run_identity(root, config, manifest["manifest_sha256"])
    result_dir = root / "work/results" / ("run_" + run_id)
    checkpoint_dir = root / "work/checkpoints" / ("run_" + run_id)
    result_dir.mkdir(parents=True, exist_ok=True)
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    policy = {"max_epochs": 100, "early_stopping_enabled": False, "batch_size": config["batch_size"],
              "optimizer": "AdamW", "initial_learning_rate": config["learning_rate"], "weight_decay": config["weight_decay"],
              "scheduler_patience": config["scheduler_patience"], "scheduler_factor": config["scheduler_factor"],
              "min_learning_rate": config["min_learning_rate"], "min_delta": config["min_delta"],
              "evaluation_forward": "fp32", "evaluation_loss": "fp64_signed_softplus"}
    metadata = {**settings, "run_id": run_id, "protocol": PROTOCOL, "protocol_fixed_model": False,
                "started_at": now_kst(), "device": device_information(device), "training_policy": policy}
    existing_metadata = result_dir / "run_metadata.json"
    if existing_metadata.exists():
        old = json.loads(existing_metadata.read_text(encoding="utf-8"))
        if any(old.get(key) != value for key, value in settings.items()) or old.get("run_id") != run_id:
            raise ValueError("기존 실행 metadata를 다른 소스로 덮어쓰지 않습니다.")
    atomic_json(existing_metadata, metadata)
    splits = manifest["splits"]
    training = CTDataset(splits["train"], config["image_size"], training=True, samples_per_class=config["samples_per_class"], seed=config["seed"])
    validation = CTDataset(splits["validation"], config["image_size"], training=False)
    test = CTDataset(splits["test"], config["image_size"], training=False)
    train_loader, val_loader, test_loader = [_loader(dataset, config, device) for dataset in [training, validation, test]]
    state.update(run_id=run_id, dataset=manifest["summary"], device=metadata["device"], training_policy=policy,
                 precision={k:v for k,v in precision.items() if k != "dtype"}, status="running")
    completed_steps = 0
    for index, sigma in enumerate(SIGMAS):
        entry = state.data["sigma_queue"][index]
        metrics_path = result_dir / f"sigma_{sigma}_metrics.json"
        privacy_path = result_dir / f"sigma_{sigma}_privacy.json"
        state.update(sigma=sigma, sigma_index=index+1, training_sigma=sigma, epoch=0, history=[], evaluation=None, privacy=None,
                     checkpoint_sha256=None, model_state_sha256=None, selected_checkpoint=None,
                     classification_status="pending", privacy_status="pending", training_status="pending")
        if metrics_path.exists() and privacy_path.exists():
            result = validate_result(root, json.loads(metrics_path.read_text(encoding="utf-8")), run_id)
            private = validate_privacy_result(root, json.loads(privacy_path.read_text(encoding="utf-8")), run_id)
            entry.update(status="completed", training_status="completed", classification_status="completed", privacy_status="completed",
                         result=metrics_path.relative_to(root).as_posix(), privacy_result=privacy_path.relative_to(root).as_posix())
            completed_steps += result["optimizer_steps"]
            state.update(evaluation=result, privacy=private, epoch=100, training_status="completed",
                         classification_status="completed", privacy_status="completed", run_optimizer_steps=completed_steps)
            continue
        entry.update(status="running", training_status="running")
        seed_everything(config["seed"], config.get("cpu_threads", 4))
        model = SplitResNet50(sigma=sigma, pretrained=True,
                             weights_path=readonly_input(root, config, "initial_weights_path"),
                             expected_weights_sha256=config["initial_weights_sha256"]).to(device)
        initialization = {"initial_model_state_sha256": tensor_state_digest(model.state_dict()),
                          "initial_weights_sha256": config["initial_weights_sha256"], "seed": config["seed"],
                          "optimizer_initial_steps": 0, "training_sigma": sigma}
        initial_path = result_dir / f"sigma_{sigma}_initialization.json"
        if initial_path.exists() and json.loads(initial_path.read_text(encoding="utf-8")) != initialization:
            raise ValueError("새 강도의 초기 모델·옵티마이저0 조건이 최초 기록과 다릅니다.")
        atomic_json(initial_path, initialization)
        optimizer, scheduler = build_optimizer_scheduler([p for p in model.parameters() if p.requires_grad], config)
        scaler = torch.amp.GradScaler("cuda", enabled=precision["use_grad_scaler"])
        control = TrainingControl(config["min_delta"], config["early_stopping_patience"], enabled=False)
        best_path, last_path = [checkpoint_dir / f"sigma_{sigma}_{kind}.pt" for kind in ["best", "last"]]
        history, start_epoch = [], 1
        if last_path.exists():
            saved = checkpoint_load(last_path, run_id, sigma)
            history = saved["history"]
            if (len(history) != saved["epoch"] or [r["epoch"] for r in history] != list(range(1, saved["epoch"]+1))
                    or any(r["sigma"] != sigma for r in history) or saved["training_policy"] != policy):
                raise ValueError("재개 마지막 회차·이력·학습 정책이 다릅니다.")
            model.load_state_dict(saved["model"], strict=True)
            optimizer.load_state_dict(saved["optimizer"])
            scheduler.load_state_dict(saved["scheduler"])
            scaler.load_state_dict(saved["scaler"])
            control.load_state_dict(saved["training_control"])
            restore_all_rng(saved, device)
            start_epoch = saved["epoch"] + 1
            if control.optimizer_steps != saved["epoch"] * len(train_loader) or checkpoint_load(best_path, run_id, sigma)["epoch"] != control.best_raw_epoch:
                raise ValueError("재개 optimizer 단계·best 회차가 다릅니다.")
        elif best_path.exists() or metrics_path.exists() or privacy_path.exists():
            raise ValueError("마지막 완료 회차 없이 남은 결과·모델을 덮어쓰지 않습니다.")
        state.update(phase="training", stage="training", training_status="running", history=list(history),
                     optimizer_steps=control.optimizer_steps, run_optimizer_steps=completed_steps+control.optimizer_steps)
        for epoch in range(start_epoch, 101):
            if metrics_path.exists() or (result_dir / f"sigma_{sigma}_selection.json").exists():
                raise ValueError("모델 선정·분류 뒤 추가 학습을 거부합니다.")
            training.set_epoch(epoch-1)
            model.train()
            total_loss, seen, tick = 0., {"OK": 0, "NG": 0}, time.monotonic()
            state.update(epoch=epoch, stage="training", batch=0, batches=len(train_loader), seen_per_class=seen.copy(),
                         message=f"σ={sigma}: 새 모델 학습 {epoch}/100회")
            for batch_index, (images, target) in enumerate(train_loader, 1):
                state.data["attempted_batch"] = batch_index
                images, target = images.to(device), target.to(device)
                optimizer.zero_grad(set_to_none=True)
                with torch.autocast(device_type=device.type, dtype=precision["dtype"], enabled=precision["autocast_enabled"]):
                    loss = stable_binary_loss(model(images), target, dtype=torch.float32)
                if not torch.isfinite(loss):
                    raise FloatingPointError(f"σ={sigma} epoch={epoch} batch={batch_index}: 비유한 학습 손실")
                scaler.scale(loss).backward()
                scaler.unscale_(optimizer)
                norm = nn.utils.clip_grad_norm_(model.parameters(), 1., error_if_nonfinite=True)
                scaler.step(optimizer)
                scaler.update()
                control.optimizer_steps += 1
                total_loss += loss.item()*len(target)
                ng = int(target.sum().item())
                seen["NG"] += ng
                seen["OK"] += len(target)-ng
                if batch_index == 1 or batch_index % config["status_every_batches"] == 0 or batch_index == len(train_loader):
                    state.update(batch=batch_index, seen_per_class=seen.copy(), train_loss=total_loss/sum(seen.values()),
                                 optimizer_steps=control.optimizer_steps, run_optimizer_steps=completed_steps+control.optimizer_steps,
                                 learning_rate=optimizer.param_groups[0]["lr"], last_gradient_norm=norm.item(),
                                 epoch_elapsed_seconds=time.monotonic()-tick, elapsed_seconds=time.monotonic()-started)
            if seen != {"OK": config["samples_per_class"], "NG": config["samples_per_class"]}:
                raise AssertionError("실제 클래스별 온라인 학습 표본 수가 다릅니다.")
            val, _, _ = evaluate(model, val_loader, device, precision, state)
            lr = optimizer.param_groups[0]["lr"]
            decision = control.observe(val["loss"], epoch)
            scheduler.step(val["loss"])
            history.append({"sigma": sigma, "epoch": epoch, "train_loss": total_loss/len(training), "val_loss": val["loss"],
                            "val_accuracy": val["accuracy"], "val_auc": val["auc"], "seen_per_class": seen,
                            "seconds": time.monotonic()-tick, "learning_rate": lr, "next_learning_rate": optimizer.param_groups[0]["lr"],
                            "optimizer_steps": control.optimizer_steps, "best_raw_epoch": control.best_raw_epoch})
            base = checkpoint_base(run_id, sigma, epoch, model, control, policy)
            if decision["raw_improved"]:
                _save_checkpoint(best_path, {**base, "validation": val})
            _save_checkpoint(last_path, {**base, "optimizer": optimizer.state_dict(), "scheduler": scheduler.state_dict(),
                                       "scaler": scaler.state_dict(), "history": list(history), "torch_rng_state": torch.get_rng_state(),
                                       "cuda_rng_state": torch.cuda.get_rng_state_all() if device.type == "cuda" else [],
                                       "python_rng_state": random.getstate(), "numpy_rng_state": numpy_rng_state()})
            atomic_json(result_dir / f"sigma_{sigma}_history.json", history)
            state.update(history=list(history), best_epoch=control.best_raw_epoch, best_raw_epoch=control.best_raw_epoch,
                         best_raw_loss=control.best_raw_loss, learning_rate=optimizer.param_groups[0]["lr"])
            state.event("독립 학습 회차 완료", history[-1])
            print(json.dumps(history[-1], ensure_ascii=False), flush=True)
        if len(history) != 100 or control.optimizer_steps != 100*len(train_loader):
            raise ValueError("100회 학습 미완료 상태에서 분류·점수를 시작하지 않습니다.")
        best = checkpoint_load(best_path, run_id, sigma)
        if best["epoch"] != control.best_raw_epoch:
            raise ValueError("선정 best 회차와 전체 검증 이력이 다릅니다.")
        del model, optimizer, scheduler, scaler
        gc.collect()
        if device.type == "cuda":
            torch.cuda.empty_cache()
        evaluation_model = SplitResNet50(sigma=sigma, pretrained=False).to(device).eval().requires_grad_(False)
        evaluation_model.load_state_dict(best["model"], strict=True)
        selection = {"run_id": run_id, "protocol": PROTOCOL, "protocol_fixed_model": False, "sigma": sigma, "training_sigma": sigma,
                     "best_epoch": best["epoch"], "checkpoint_epoch": best["epoch"], "epochs_ran": 100,
                     "selected_checkpoint": best_path.relative_to(root).as_posix(), "checkpoint_sha256": file_sha256(best_path),
                     "model_state_sha256": tensor_state_digest(evaluation_model.state_dict()), **result_binding(root, metadata)}
        selection_path = result_dir / f"sigma_{sigma}_selection.json"
        if selection_path.exists() and json.loads(selection_path.read_text(encoding="utf-8")) != selection:
            raise ValueError("이미 선정한 강도별 모델 식별자를 교체할 수 없습니다.")
        atomic_json(selection_path, selection)
        entry.update(training_status="completed", classification_status="running")
        state.update(phase="classification", training_status="completed", classification_status="running", epoch=100,
                     **{k:selection[k] for k in ["best_epoch", "checkpoint_sha256", "model_state_sha256", "selected_checkpoint"]})
        result = classify(evaluation_model, splits, [val_loader, test_loader], device, root, selection, state, control.optimizer_steps)
        entry.update(classification_status="completed", result=metrics_path.relative_to(root).as_posix(), privacy_status="running")
        state.update(phase="privacy", stage="privacy", evaluation=result, classification_status="completed", privacy_status="running")
        private = (validate_privacy_result(root, json.loads(privacy_path.read_text(encoding="utf-8")), run_id) if privacy_path.exists()
                   else run_privacy(evaluation_model, splits["test"], root, run_id, selection, state))
        validate_privacy_result(root, private, run_id)
        entry.update(status="completed", privacy_status="completed", privacy_result=privacy_path.relative_to(root).as_posix())
        completed_steps += control.optimizer_steps
        state.update(privacy=private, privacy_status="completed", run_optimizer_steps=completed_steps,
                     message=f"σ={sigma}: 독립100회 학습·분류·실측 점수 완료")
        state.event("독립 강도 완료", {"sigma": sigma, "score": private["score"]})
        del evaluation_model, best
        gc.collect()
        if device.type == "cuda":
            torch.cuda.empty_cache()
    state.update(phase="completed", stage="completed", status="completed", pid=None,
                 elapsed_seconds=time.monotonic()-started, message="10강도 독립 학습·분류·조건부 프라이버시 점수 계산 완료")
    return state.data



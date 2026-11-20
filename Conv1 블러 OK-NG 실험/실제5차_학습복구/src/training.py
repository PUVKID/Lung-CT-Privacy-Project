"""고정 Conv1·온라인 균형 증강·검증 손실 조기 종료를 실제 실행합니다."""

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


def evaluate(model, loader, device, precision, state=None, stage="validation"):
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
    return metrics, labels, probabilities


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


def _run_identity(root, config, manifest_sha256):
    root = Path(root)
    sources = [root / "run_training.py", root / "config.json", *sorted((root / "src").glob("*.py"))]
    source_hashes = {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    settings = {"config": config, "manifest_sha256": manifest_sha256, "source_hashes": source_hashes}
    digest = hashlib.sha256(json.dumps(settings, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()[:16]
    return digest, settings


def run_training(config, root, state, device_name="cuda"):
    root = Path(root)
    started = time.monotonic()
    seed_everything(config["seed"], config.get("cpu_threads", 4))
    if device_name == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA GPU를 요청했지만 사용할 수 없습니다. CPU로 자동 대체하지 않았습니다.")
    device = torch.device("cuda" if device_name == "auto" and torch.cuda.is_available() else "cpu" if device_name == "auto" else device_name)
    precision = precision_policy(config["precision"], device.type)
    precision_info = {key: value for key, value in precision.items() if key != "dtype"}
    policy = {"max_epochs": config["epochs"], "patience": config["early_stopping_patience"],
              "early_stopping_enabled": config.get("early_stopping_enabled", True),
              "min_delta": config["min_delta"], "min_delta_mode": "absolute", "batch_size": config["batch_size"],
              "optimizer": "AdamW", "initial_learning_rate": config["learning_rate"], "weight_decay": config["weight_decay"],
              "scheduler_patience": config["scheduler_patience"], "scheduler_factor": config["scheduler_factor"],
              "min_learning_rate": config["min_learning_rate"], "evaluation_forward": "fp32", "evaluation_loss": "fp64_signed_softplus"}
    state.update(device=device_information(device), precision=precision_info, training_policy=policy,
                 learning_rate=config["learning_rate"], optimizer_steps=0, best_epoch=0, best_raw_epoch=0,
                 early_stopping_wait=0, stage="preparing", message="원본 해시와 유사 그룹 분할을 확인하는 중")
    manifest = prepare_dataset(config, root)
    run_id, settings = _run_identity(root, config, manifest["manifest_sha256"])
    result_dir = root / "work/results" / f"run_{run_id}"
    checkpoint_dir = root / "work/checkpoints" / f"run_{run_id}"
    result_dir.mkdir(parents=True, exist_ok=True)
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    atomic_json(result_dir / "run_metadata.json", {**settings, "run_id": run_id, "started_at": now_kst(),
                                                  "device": state.data["device"], "training_policy": policy,
                                                  "protocol": "similarity-group preliminary holdout"})
    state.update(dataset=manifest["summary"], run_id=run_id, result_directory=result_dir.relative_to(root).as_posix())
    state.event("자료 검증 완료", {"run_id": run_id, "summary": manifest["summary"]})
    splits = manifest["splits"]
    training = CTDataset(splits["train"], config["image_size"], training=True,
                         samples_per_class=config["samples_per_class"], seed=config["seed"])
    validation = CTDataset(splits["validation"], config["image_size"], training=False)
    test = CTDataset(splits["test"], config["image_size"], training=False)
    train_loader, val_loader, test_loader = [_loader(dataset, config, device) for dataset in [training, validation, test]]
    completed_steps = 0
    for sigma_index, sigma in enumerate(config["sigmas"], 1):
        entry = state.data["sigma_queue"][sigma_index - 1]
        metrics_file = result_dir / f"sigma_{sigma}_metrics.json"
        if metrics_file.exists():
            # 완료된 결과는 동일한 소스·설정·자료 해시에 한해서만 재사용합니다.
            result = json.loads(metrics_file.read_text(encoding="utf-8"))
            entry.update(status="completed", result=metrics_file.relative_to(root).as_posix())
            history_file = result_dir / f"sigma_{sigma}_history.json"
            if history_file.exists():
                state.data["history"].extend(json.loads(history_file.read_text(encoding="utf-8")))
            completed_steps += result["optimizer_steps"]
            state.update(evaluation=result, run_optimizer_steps=completed_steps)
            state.event("완료 조건 재사용", {"sigma": sigma, "run_id": run_id})
            continue
        entry["status"] = "running"
        seed_everything(config["seed"], config.get("cpu_threads", 4))
        state.update(stage="loading_model", status="running", sigma=sigma, sigma_index=sigma_index,
                     epoch=0, batch=0, batches=len(train_loader), seen_per_class={"OK": 0, "NG": 0},
                     best_epoch=0, best_raw_epoch=0, best_raw_loss=None, meaningful_best_loss=None,
                     early_stopping_wait=0, optimizer_steps=0, learning_rate=config["learning_rate"],
                     train_loss=None, attempted_batch=0,
                     evaluation=None, message=f"σ={sigma}: 동일 ImageNet 초기값 모델 구성 중")
        model = SplitResNet50(sigma=sigma, pretrained=True).to(device)
        optimizer, scheduler = build_optimizer_scheduler([p for p in model.parameters() if p.requires_grad], config)
        scaler = torch.amp.GradScaler("cuda", enabled=precision["use_grad_scaler"])
        control = TrainingControl(config["min_delta"], config["early_stopping_patience"],
                                  enabled=policy["early_stopping_enabled"])
        checkpoint = checkpoint_dir / f"sigma_{sigma}_best.pt"
        latest_checkpoint = checkpoint_dir / f"sigma_{sigma}_last.pt"
        prefix_checkpoint = checkpoint_dir / f"sigma_{sigma}_shadow_prefix_best.pt"
        prefix_sha256 = None
        sigma_history = []
        start_epoch = 1
        stopping_reason = "max_epochs"
        if latest_checkpoint.exists():
            saved = torch.load(latest_checkpoint, map_location=device, weights_only=False)
            if saved["run_id"] != run_id or saved["sigma"] != sigma:
                raise ValueError("재개 체크포인트의 자료·설정 식별자가 일치하지 않습니다.")
            model.load_state_dict(saved["model"])
            optimizer.load_state_dict(saved["optimizer"])
            scheduler.load_state_dict(saved["scheduler"])
            scaler.load_state_dict(saved["scaler"])
            control.load_state_dict(saved["training_control"])
            prefix_sha256 = saved.get("shadow_prefix_sha256")
            if not control.enabled and control.shadow_stop_epoch:
                _check_prefix_hash(prefix_checkpoint, prefix_sha256)
            sigma_history = saved["history"]
            start_epoch = saved["epoch"] + 1
            restore_rng_state(saved, device)
            state.data["history"].extend(sigma_history)
            state.event("체크포인트 재개", {"sigma": sigma, "epoch": start_epoch, "run_id": run_id,
                                              "optimizer_steps": control.optimizer_steps,
                                              "learning_rate": optimizer.param_groups[0]["lr"],
                                              "meaningful_best_loss": control.meaningful_best_loss})
        state.update(learning_rate=optimizer.param_groups[0]["lr"], optimizer_steps=control.optimizer_steps,
                     early_stopping_wait=control.stale_epochs, best_epoch=control.best_raw_epoch,
                     best_raw_epoch=control.best_raw_epoch, run_optimizer_steps=completed_steps + control.optimizer_steps)
        state.event("학습 조건 시작", {"sigma": sigma, "epochs": config["epochs"], "batches": len(train_loader),
                                        "samples_per_class": config["samples_per_class"], "image_size": config["image_size"]})
        for epoch in range(start_epoch, config["epochs"] + 1):
            if control.enabled and control.stale_epochs >= control.patience:
                stopping_reason = "meaningful_validation_plateau"
                break
            training.set_epoch(epoch - 1)
            model.train()
            total_loss = 0.0
            seen = {"OK": 0, "NG": 0}
            epoch_started = time.monotonic()
            state.update(stage="training", epoch=epoch, batch=0, batches=len(train_loader), seen_per_class=seen.copy(),
                         message=f"σ={sigma}: {epoch}/{config['epochs']} epoch 학습 중")
            for batch_index, (images, target) in enumerate(train_loader, 1):
                state.data["attempted_batch"] = batch_index
                images, target = images.to(device, non_blocking=True), target.to(device, non_blocking=True)
                optimizer.zero_grad(set_to_none=True)
                with torch.autocast(device_type=device.type, dtype=precision["dtype"], enabled=precision["autocast_enabled"]):
                    logits = model(images)
                    loss = stable_binary_loss(logits, target, dtype=torch.float32)
                if not torch.isfinite(loss):
                    raise FloatingPointError(f"σ={sigma}, epoch={epoch}, batch={batch_index}: 학습 손실 NaN/Inf")
                scaler.scale(loss).backward()
                scaler.unscale_(optimizer)
                gradient_norm = nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0, error_if_nonfinite=True)
                scaler.step(optimizer)
                scaler.update()
                control.optimizer_steps += 1
                total_loss += loss.item() * len(target)
                ng = int(target.sum().item())
                seen["NG"] += ng
                seen["OK"] += len(target) - ng
                if batch_index == 1 or batch_index % config["status_every_batches"] == 0 or batch_index == len(train_loader):
                    state.update(stage="training", batch=batch_index, batches=len(train_loader), seen_per_class=seen.copy(),
                                 train_loss=total_loss / sum(seen.values()), elapsed_seconds=round(time.monotonic() - started, 1),
                                 last_gradient_norm=gradient_norm.item(),
                                 learning_rate=optimizer.param_groups[0]["lr"], optimizer_steps=control.optimizer_steps,
                                 run_optimizer_steps=completed_steps + control.optimizer_steps,
                                 epoch_elapsed_seconds=round(time.monotonic() - epoch_started, 1),
                                 message=f"σ={sigma}: epoch {epoch}, 실제 학습 {sum(seen.values())}/{len(training)} 표본")
                if batch_index == 1:
                    state.event("실제 학습 배치 완료", {"sigma": sigma, "epoch": epoch, "batch": 1,
                                                         "loss": loss.item(), "device": device.type})
            if seen != {"OK": config["samples_per_class"], "NG": config["samples_per_class"]}:
                raise AssertionError(f"클래스별 실제 학습 표본 수가 다릅니다: {seen}")
            state.update(stage="validation", batch=0, batches=len(val_loader), message=f"σ={sigma}: 원본 검증셋 평가 중")
            val_metrics, _, _ = evaluate(model, val_loader, device, precision, state)
            learning_rate_before = optimizer.param_groups[0]["lr"]
            decision = control.observe(val_metrics["loss"], epoch)
            scheduler.step(val_metrics["loss"])
            row = {"sigma": sigma, "epoch": epoch, "train_loss": total_loss / len(training),
                   "val_loss": val_metrics["loss"], "val_accuracy": val_metrics["accuracy"], "val_auc": val_metrics["auc"],
                   "seen_per_class": seen.copy(), "seconds": round(time.monotonic() - epoch_started, 2),
                   "learning_rate": learning_rate_before, "next_learning_rate": optimizer.param_groups[0]["lr"],
                   "optimizer_steps": control.optimizer_steps, "best_raw_epoch": control.best_raw_epoch,
                   "meaningful_best_loss": control.meaningful_best_loss, "early_stopping_wait": control.stale_epochs,
                   "shadow_stop_epoch": control.shadow_stop_epoch,
                   "per_source_validation": val_metrics.get("per_source", {}),
                   "val_logit_min": val_metrics["logit_min"], "val_logit_max": val_metrics["logit_max"]}
            sigma_history.append(row)
            state.data["history"].append(row)
            if decision["raw_improved"]:
                _save_checkpoint(checkpoint, {"run_id": run_id, "sigma": sigma, "epoch": epoch,
                                              "model": model.state_dict(), "validation": val_metrics,
                                              "training_control": control.state_dict(), "training_policy": policy})
            if not control.enabled and control.shadow_stop_epoch == epoch and prefix_sha256 is None:
                prefix_sha256 = _freeze_prefix_checkpoint(checkpoint, prefix_checkpoint)
                state.event("관찰용 종료 모델 고정", {"sigma": sigma, "shadow_stop_epoch": epoch,
                                                      "best_epoch": control.shadow_best_raw_epoch,
                                                      "checkpoint_sha256": prefix_sha256})
            _save_checkpoint(latest_checkpoint, {"run_id": run_id, "sigma": sigma, "epoch": epoch,
                                                  "model": model.state_dict(), "optimizer": optimizer.state_dict(),
                                                  "scheduler": scheduler.state_dict(), "scaler": scaler.state_dict(),
                                                  "training_control": control.state_dict(), "training_policy": policy,
                                                  "shadow_prefix_sha256": prefix_sha256,
                                                  "learning_rate": optimizer.param_groups[0]["lr"], "history": sigma_history,
                                                  "torch_rng_state": torch.get_rng_state(),
                                                  "cuda_rng_state": torch.cuda.get_rng_state_all() if device.type == "cuda" else []})
            atomic_json(result_dir / f"sigma_{sigma}_history.json", sigma_history)
            state.update(message=f"σ={sigma}: epoch {epoch} 완료, 검증 손실 {val_metrics['loss']:.6g}",
                         best_epoch=control.best_raw_epoch, best_raw_epoch=control.best_raw_epoch,
                         best_raw_loss=control.best_raw_loss, meaningful_best_loss=control.meaningful_best_loss,
                         shadow_stop_epoch=control.shadow_stop_epoch,
                         early_stopping_wait=control.stale_epochs, learning_rate=optimizer.param_groups[0]["lr"])
            state.event("epoch 완료", row)
            print(json.dumps(row, ensure_ascii=False), flush=True)
            if decision["should_stop"]:
                stopping_reason = "meaningful_validation_plateau"
                state.event("조기 종료", {"sigma": sigma, "epoch": epoch, "stale_epochs": control.stale_epochs,
                                             "min_delta": control.min_delta, "best_raw_epoch": control.best_raw_epoch})
                break
        if not checkpoint.exists():
            raise RuntimeError("검증을 거친 최적 체크포인트가 없어 시험 평가를 중단합니다.")
        if not control.enabled and len(sigma_history) != config["epochs"]:
            raise RuntimeError("고정 학습 회차를 모두 완료하지 않아 시험 평가를 중단합니다.")
        best = torch.load(checkpoint, map_location=device, weights_only=False)
        if best["run_id"] != run_id or best["sigma"] != sigma or best["epoch"] != control.best_raw_epoch:
            raise ValueError("전체 학습 최적 체크포인트 식별자가 다릅니다.")
        model.load_state_dict(best["model"])
        del best
        val_metrics, val_y, val_p = evaluate(model, val_loader, device, precision, state)
        state.update(stage="testing", batch=0, batches=len(test_loader), message=f"σ={sigma}: 전체 학습 최적 모델의 시험 평가 중")
        test_metrics, test_y, test_p = evaluate(model, test_loader, device, precision, state, stage="testing")
        _save_predictions(result_dir / f"sigma_{sigma}_validation_predictions_private.csv", splits["validation"], val_y, val_p)
        _save_predictions(result_dir / f"sigma_{sigma}_test_predictions_private.csv", splits["test"], test_y, test_p)
        comparison = {"available": False, "shadow_stop_epoch": control.shadow_stop_epoch or None,
                      "selection": "최초 가상 종료 시점까지의 최저 검증 손실; 시험 지표로 선택하지 않음"}
        if not control.enabled and control.shadow_stop_epoch:
            _check_prefix_hash(prefix_checkpoint, prefix_sha256)
            prefix = torch.load(prefix_checkpoint, map_location=device, weights_only=False)
            if (prefix["run_id"] != run_id or prefix["sigma"] != sigma
                    or prefix["epoch"] != control.shadow_best_raw_epoch
                    or not 1 <= prefix["epoch"] <= control.shadow_stop_epoch <= len(sigma_history)):
                raise ValueError("관찰용 최적 체크포인트 식별자가 다릅니다.")
            model.load_state_dict(prefix["model"])
            del prefix
            prefix_val, prefix_y, prefix_p = evaluate(model, val_loader, device, precision, state)
            prefix_test, prefix_test_y, prefix_test_p = evaluate(model, test_loader, device, precision, state, stage="testing")
            _save_predictions(result_dir / f"sigma_{sigma}_shadow_validation_predictions_private.csv", splits["validation"], prefix_y, prefix_p)
            _save_predictions(result_dir / f"sigma_{sigma}_shadow_test_predictions_private.csv", splits["test"], prefix_test_y, prefix_test_p)
            comparison.update(available=True, best_epoch=control.shadow_best_raw_epoch,
                              checkpoint_sha256=prefix_sha256, validation=prefix_val, test=prefix_test)
        result = {"run_id": run_id, "sigma": sigma, "best_epoch": control.best_raw_epoch,
                  "best_raw_epoch": control.best_raw_epoch, "epochs_ran": len(sigma_history),
                  "optimizer_steps": control.optimizer_steps, "training_policy": policy, "stopping_reason": stopping_reason,
                  "validation": val_metrics, "test": test_metrics, "completed_at": now_kst(),
                  "selected_checkpoint": "전체 학습 중 최저 검증 손실 모델",
                  "early_stopping_comparison": comparison,
                  "test_use": "이미 사용한 동일 시험셋의 탐색적 비교입니다. 두 모델은 검증 손실로만 선정하며 시험 결과로 모델·sigma·임계값을 선택하지 않습니다.",
                  "protocol": "환자 ID 없는 유사 영상 그룹 예비실험; 7-fold/매칭/복원 공격 미실행"}
        atomic_json(metrics_file, result)
        entry.update(status="completed", result=metrics_file.relative_to(root).as_posix())
        state.update(evaluation=result, message=f"σ={sigma}: 학습·검증·시험 평가 완료")
        state.event("조건 완료", result)
        completed_steps += control.optimizer_steps
        del model, optimizer, scheduler, scaler
        gc.collect()
        if device.type == "cuda":
            torch.cuda.empty_cache()
    state.update(stage="completed", status="completed", pid=None,
                 message="10단계 영상 단위 분류 실험 완료. 환자 교차검증·매칭·복원 공격은 미실행입니다.",
                 elapsed_seconds=round(time.monotonic() - started, 1))
    state.event("분류 큐 완료", {"run_id": run_id, "sigmas": config["sigmas"]})
    return state.data

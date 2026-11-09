"""고정 Conv1·온라인 균형 증강·검증 손실 조기 종료를 실제 실행합니다."""

import csv
import gc
import hashlib
import json
import math
import os
from pathlib import Path
import random
import time

import numpy as np
from sklearn.metrics import accuracy_score, average_precision_score, confusion_matrix, f1_score, roc_auc_score
import torch
from torch import nn
from torch.utils.data import DataLoader

from .data import CTDataset, prepare_dataset
from .model import SplitResNet50
from .state import atomic_json, now_kst


def binary_metrics(labels, probabilities):
    y = np.asarray(labels, dtype=int)
    p = np.asarray(probabilities, dtype=float)
    if len(y) == 0 or len(y) != len(p) or not np.isfinite(p).all():
        raise ValueError("평가 라벨·예측 확률이 유효하지 않습니다.")
    if not set(y).issubset({0, 1}) or np.any((p < 0) | (p > 1)):
        raise ValueError("이진 라벨/확률 범위가 유효하지 않습니다.")
    predicted = (p >= 0.5).astype(int)
    matrix = confusion_matrix(y, predicted, labels=[0, 1])
    tn, fp, fn, tp = matrix.ravel()
    return {"accuracy": float(accuracy_score(y, predicted)),
            "auc": float(roc_auc_score(y, p)) if len(set(y)) == 2 else None,
            "pr_auc": float(average_precision_score(y, p)) if len(set(y)) == 2 else None,
            "sensitivity": float(tp / (tp + fn)) if tp + fn else None,
            "specificity": float(tn / (tn + fp)) if tn + fp else None,
            "f1": float(f1_score(y, predicted, zero_division=0)),
            "confusion_matrix": matrix.tolist(), "threshold": 0.5, "n_images": len(y),
            "unit": "image", "patient_id_available": False}


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
    labels, probabilities = [], []
    total_loss = 0.0
    count = 0
    criterion = nn.BCEWithLogitsLoss(reduction="sum")
    with torch.inference_mode():
        for batch_index, (images, target) in enumerate(loader, 1):
            images, target = images.to(device, non_blocking=True), target.to(device, non_blocking=True)
            with torch.autocast(device_type=device.type, dtype=precision["dtype"], enabled=precision["autocast_enabled"]):
                logits = model(images)
                loss = criterion(logits, target)
            if not torch.isfinite(loss):
                raise FloatingPointError("평가 손실에 NaN/Inf가 발생했습니다.")
            total_loss += loss.item()
            count += len(target)
            labels.extend(target.cpu().int().tolist())
            probabilities.extend(logits.sigmoid().float().cpu().tolist())
            if state and (batch_index == 1 or batch_index % 10 == 0 or batch_index == len(loader)):
                state.update(stage=stage, batch=batch_index, batches=len(loader),
                             message=f"{'시험' if stage == 'testing' else '검증'} 원본 영상 {count}개 평가 중")
    metrics = binary_metrics(labels, probabilities)
    metrics["loss"] = total_loss / count
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
    state.update(device=device_information(device), precision=precision_info, stage="preparing", message="원본 해시와 분할을 확인하는 중")
    manifest = prepare_dataset(config, root)
    run_id, settings = _run_identity(root, config, manifest["manifest_sha256"])
    result_dir = root / "work/results" / f"run_{run_id}"
    checkpoint_dir = root / "work/checkpoints" / f"run_{run_id}"
    result_dir.mkdir(parents=True, exist_ok=True)
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    atomic_json(result_dir / "run_metadata.json", {**settings, "run_id": run_id, "started_at": now_kst(),
                                                  "device": state.data["device"], "protocol": "image-level preliminary holdout"})
    state.update(dataset=manifest["summary"], run_id=run_id, result_directory=result_dir.relative_to(root).as_posix())
    state.event("자료 검증 완료", {"run_id": run_id, "summary": manifest["summary"]})
    splits = manifest["splits"]
    training = CTDataset(splits["train"], config["image_size"], training=True,
                         samples_per_class=config["samples_per_class"], seed=config["seed"])
    validation = CTDataset(splits["validation"], config["image_size"], training=False)
    test = CTDataset(splits["test"], config["image_size"], training=False)
    train_loader, val_loader, test_loader = [_loader(dataset, config, device) for dataset in [training, validation, test]]
    for sigma_index, sigma in enumerate(config["sigmas"], 1):
        entry = state.data["sigma_queue"][sigma_index - 1]
        metrics_file = result_dir / f"sigma_{sigma}_metrics.json"
        if metrics_file.exists():
            # 완료된 결과는 동일한 소스·설정·자료 해시에 한해서만 재사용합니다.
            result = json.loads(metrics_file.read_text(encoding="utf-8"))
            entry.update(status="completed", result=metrics_file.relative_to(root).as_posix())
            state.event("완료 조건 재사용", {"sigma": sigma, "run_id": run_id})
            continue
        entry["status"] = "running"
        seed_everything(config["seed"], config.get("cpu_threads", 4))
        state.update(stage="loading_model", status="running", sigma=sigma, sigma_index=sigma_index,
                     epoch=0, batch=0, batches=len(train_loader), seen_per_class={"OK": 0, "NG": 0},
                     evaluation=None, message=f"σ={sigma}: 동일 ImageNet 초기값 모델 구성 중")
        model = SplitResNet50(sigma=sigma, pretrained=True).to(device)
        optimizer = torch.optim.Adam([p for p in model.parameters() if p.requires_grad], lr=config["learning_rate"])
        scaler = torch.amp.GradScaler("cuda", enabled=precision["use_grad_scaler"])
        criterion = nn.BCEWithLogitsLoss()
        best_loss, stale_epochs, best_epoch = math.inf, 0, 0
        checkpoint = checkpoint_dir / f"sigma_{sigma}_best.pt"
        latest_checkpoint = checkpoint_dir / f"sigma_{sigma}_last.pt"
        sigma_history = []
        start_epoch = 1
        if latest_checkpoint.exists():
            saved = torch.load(latest_checkpoint, map_location=device, weights_only=False)
            if saved["run_id"] != run_id or saved["sigma"] != sigma:
                raise ValueError("재개 체크포인트의 자료·설정 식별자가 일치하지 않습니다.")
            model.load_state_dict(saved["model"])
            optimizer.load_state_dict(saved["optimizer"])
            scaler.load_state_dict(saved["scaler"])
            best_loss, best_epoch, stale_epochs = saved["best_loss"], saved["best_epoch"], saved["stale_epochs"]
            sigma_history = saved["history"]
            start_epoch = saved["epoch"] + 1
            restore_rng_state(saved, device)
            state.data["history"].extend(sigma_history)
            state.event("체크포인트 재개", {"sigma": sigma, "epoch": start_epoch, "run_id": run_id})
        state.event("학습 조건 시작", {"sigma": sigma, "epochs": config["epochs"], "batches": len(train_loader),
                                        "samples_per_class": config["samples_per_class"], "image_size": config["image_size"]})
        for epoch in range(start_epoch, config["epochs"] + 1):
            if stale_epochs >= config["early_stopping_patience"]:
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
                    loss = criterion(logits, target)
                if not torch.isfinite(loss):
                    raise FloatingPointError(f"σ={sigma}, epoch={epoch}, batch={batch_index}: 학습 손실 NaN/Inf")
                scaler.scale(loss).backward()
                scaler.unscale_(optimizer)
                gradient_norm = nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0, error_if_nonfinite=True)
                scaler.step(optimizer)
                scaler.update()
                total_loss += loss.item() * len(target)
                ng = int(target.sum().item())
                seen["NG"] += ng
                seen["OK"] += len(target) - ng
                if batch_index == 1 or batch_index % config["status_every_batches"] == 0 or batch_index == len(train_loader):
                    state.update(stage="training", batch=batch_index, batches=len(train_loader), seen_per_class=seen.copy(),
                                 train_loss=total_loss / sum(seen.values()), elapsed_seconds=round(time.monotonic() - started, 1),
                                 last_gradient_norm=gradient_norm.item(),
                                 epoch_elapsed_seconds=round(time.monotonic() - epoch_started, 1),
                                 message=f"σ={sigma}: epoch {epoch}, 실제 학습 {sum(seen.values())}/{len(training)} 표본")
                if batch_index == 1:
                    state.event("실제 학습 배치 완료", {"sigma": sigma, "epoch": epoch, "batch": 1,
                                                         "loss": loss.item(), "device": device.type})
            if seen != {"OK": config["samples_per_class"], "NG": config["samples_per_class"]}:
                raise AssertionError(f"클래스별 실제 학습 표본 수가 다릅니다: {seen}")
            state.update(stage="validation", batch=0, batches=len(val_loader), message=f"σ={sigma}: 원본 검증셋 평가 중")
            val_metrics, _, _ = evaluate(model, val_loader, device, precision, state)
            row = {"sigma": sigma, "epoch": epoch, "train_loss": total_loss / len(training),
                   "val_loss": val_metrics["loss"], "val_accuracy": val_metrics["accuracy"], "val_auc": val_metrics["auc"],
                   "seen_per_class": seen.copy(), "seconds": round(time.monotonic() - epoch_started, 2)}
            sigma_history.append(row)
            state.data["history"].append(row)
            improved = val_metrics["loss"] < best_loss
            if improved:
                best_loss, best_epoch, stale_epochs = val_metrics["loss"], epoch, 0
                _save_checkpoint(checkpoint, {"run_id": run_id, "sigma": sigma, "epoch": epoch,
                                              "model": model.state_dict(), "validation": val_metrics})
            else:
                stale_epochs += 1
            _save_checkpoint(latest_checkpoint, {"run_id": run_id, "sigma": sigma, "epoch": epoch,
                                                  "model": model.state_dict(), "optimizer": optimizer.state_dict(),
                                                  "scaler": scaler.state_dict(), "best_loss": best_loss, "best_epoch": best_epoch,
                                                  "stale_epochs": stale_epochs, "history": sigma_history,
                                                  "torch_rng_state": torch.get_rng_state(),
                                                  "cuda_rng_state": torch.cuda.get_rng_state_all() if device.type == "cuda" else []})
            atomic_json(result_dir / f"sigma_{sigma}_history.json", sigma_history)
            state.update(message=f"σ={sigma}: epoch {epoch} 완료, 검증 손실 {val_metrics['loss']:.5f}",
                         best_epoch=best_epoch, early_stopping_wait=stale_epochs)
            state.event("epoch 완료", row)
            print(json.dumps(row, ensure_ascii=False), flush=True)
        if not checkpoint.exists():
            raise RuntimeError("검증을 거친 최적 체크포인트가 없어 시험 평가를 중단합니다.")
        best = torch.load(checkpoint, map_location=device, weights_only=False)
        model.load_state_dict(best["model"])
        val_metrics, val_y, val_p = evaluate(model, val_loader, device, precision, state)
        state.update(stage="testing", batch=0, batches=len(test_loader), message=f"σ={sigma}: 최적 검증 모델의 독립 시험 평가 중")
        test_metrics, test_y, test_p = evaluate(model, test_loader, device, precision, state, stage="testing")
        _save_predictions(result_dir / f"sigma_{sigma}_validation_predictions_private.csv", splits["validation"], val_y, val_p)
        _save_predictions(result_dir / f"sigma_{sigma}_test_predictions_private.csv", splits["test"], test_y, test_p)
        result = {"run_id": run_id, "sigma": sigma, "best_epoch": best_epoch, "epochs_ran": len(sigma_history),
                  "validation": val_metrics, "test": test_metrics, "completed_at": now_kst(),
                  "test_use": "모든 sigma 시험 성능은 탐색적 기술 결과이며 sigma·임계값 선택에 사용하지 않습니다.",
                  "protocol": "환자 ID 없는 영상 단위 예비실험; 7-fold/매칭/복원 공격 미실행"}
        atomic_json(metrics_file, result)
        entry.update(status="completed", result=metrics_file.relative_to(root).as_posix())
        state.update(evaluation=result, message=f"σ={sigma}: 학습·검증·시험 평가 완료")
        state.event("조건 완료", result)
        del model, optimizer, scaler
        gc.collect()
        if device.type == "cuda":
            torch.cuda.empty_cache()
    state.update(stage="completed", status="completed", pid=None,
                 message="10단계 영상 단위 분류 실험 완료. 환자 교차검증·매칭·복원 공격은 미실행입니다.",
                 elapsed_seconds=round(time.monotonic() - started, 1))
    state.event("분류 큐 완료", {"run_id": run_id, "sigmas": config["sigmas"]})
    return state.data

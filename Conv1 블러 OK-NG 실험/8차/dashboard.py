"""실제 학습 상태만 읽는 루프백 전용 대시보드 서버."""
from __future__ import annotations

import argparse
import ctypes
import hashlib
import json
import math
import mimetypes
import os
from pathlib import Path
import secrets
import time
from datetime import datetime, timezone
from http import HTTPStatus
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit

from src.identity import validate_run, validate_result, validate_privacy_result, load_selection, file_sha256, safe_path

ROOT = Path(__file__).resolve().parent
ASSETS = {
    "/": "index.html", "/style.css": "style.css", "/app.js": "app.js",
    "/scene.js": "scene.js", "/theme.js": "theme.js", "/fonts/NanumGothic-Bold.ttf": "fonts/NanumGothic-Bold.ttf",
    "/fonts/OFL.txt": "fonts/OFL.txt", "/vendor/three.module.js": "vendor/three.module.js",
    "/vendor/three.core.js": "vendor/three.core.js", "/vendor/LICENSE": "vendor/LICENSE",
}


def process_alive(pid):
    """PID가 있을 때만 운영체제에서 생존 여부를 확인합니다."""
    if not isinstance(pid, int) or isinstance(pid, bool) or pid <= 0:
        return None
    if os.name == "nt":
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel.OpenProcess.restype = ctypes.c_void_p
        handle = kernel.OpenProcess(0x1000, False, pid)
        if not handle:
            return None if ctypes.get_last_error() == 5 else False
        try:
            code = ctypes.c_ulong()
            if not kernel.GetExitCodeProcess(ctypes.c_void_p(handle), ctypes.byref(code)):
                return None
            return code.value == 259
        finally:
            kernel.CloseHandle(ctypes.c_void_p(handle))
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return None


MAX_STATUS_BYTES = 4 * 1024 * 1024
PREVIEW_SIGMAS = (1, 2, 4, 8, 16, 32, 64, 128, 256)


def feature_preview_path(sigma, class_key, stage):
    """사용자가 지정한 참고 자료와 같은 고정 폴더·파일 구성을 사용합니다."""
    folder = "원본 파일 생성" if sigma == 0 else f"sigma{sigma} 블러 파일 생성"
    label = "원본" if sigma == 0 else f"sigma{sigma}_블러"
    stage_names = ("stage0_원본", "stage1_Stage-1_에지클라우드_전송", "stage2_Stage-2",
                   "stage3_Stage-3", "stage4_Stage-4", "stage5_Stage-5")
    return Path("블러 피쳐맵 저장 파일") / folder / "피쳐맵" / class_key / f"{stage_names[stage]}_{label}_{class_key}.png"


def feature_previews(root, requested_id=None):
    """평가와 18장 묶음 생성이 모두 완료된 강도만 인증된 화면에 제공합니다."""
    status = read_status(root)
    run_id = status.get("run_id")
    sigmas = (0,) + PREVIEW_SIGMAS
    classes = {"Bengin_cases": "양성", "Malignant_cases": "악성", "Normal_cases": "정상"}
    result = {"run_id": run_id, "items": [], "completed_sigmas": [],
              "pending": list(sigmas), "expected_total": 180}
    folder = root.parent / "블러 강도별 대표 특징맵" / "8차"
    try:
        if not run_id:
            result["message"] = "현재 실행에서 강도별 독립 학습·분류 평가·점수 계산을 기다리고 있습니다."
            return result
        metadata = validate_run(root, run_id)
        folder = safe_path(root.parent, folder)
        if folder.is_symlink() or not folder.resolve().is_relative_to(root.parent.resolve()):
            raise ValueError("이미지 폴더 경계 오류")
        manifest_path = safe_path(folder, "export_index_private.json")
        if manifest_path.is_symlink() or manifest_path.stat().st_size > 4 * 1024 * 1024:
            raise ValueError("특징맵 목록 형식 오류")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"), parse_constant=reject_nonfinite)
        if not isinstance(run_id, str) or len(run_id) != 16 or any(c not in "0123456789abcdef" for c in run_id) or manifest.get("run_id") != run_id:
            raise ValueError("실행 식별자 불일치")
        identities = {"protocol": "independent-sigma-privacy-v1", "protocol_fixed_model": False,
                      "manifest_records_sha256": metadata["manifest_sha256"],
                      "source_manifest_sha256": file_sha256(root / "work/results/dataset_manifest_private.json"),
                      "model_source_sha256": file_sha256(root / "src/model.py"),
                      "data_source_sha256": file_sha256(root / "src/data.py"),
                      "generator_sha256": file_sha256(root / "tools/feature_generator.py")}
        if manifest.get("schema_version") != 3 or any(manifest.get(key) != value or type(manifest.get(key)) is not type(value) for key, value in identities.items()):
            raise ValueError("특징맵 실행·소스·고정 모델 불일치")
        completed = {entry.get("sigma") for entry in status.get("sigma_queue", [])
                     if entry.get("status") == "completed" and entry.get("classification_status")=="completed" and entry.get("privacy_status")=="completed"}
        raw_items = manifest.get("items", [])
        if not isinstance(raw_items, list) or len(raw_items) > 180:
            raise ValueError("특징맵 목록 개수 오류")
        # 이미지 한 장 요청은 공통 경계와 해당 강도의 18장만 대조합니다.
        # 목록 요청은 모든 완료 강도의 180장을 그대로 검증합니다. 요청 간 캐시는 사용하지 않습니다.
        requested_sigma=None
        if requested_id is not None:
            registered={f"{sigma}-{class_key}-{stage}":sigma for sigma in sigmas for class_key in classes for stage in range(6)}
            if requested_id not in registered:
                raise ValueError("등록되지 않은 이미지 식별자")
            requested_sigma=registered[requested_id]
        for sigma in sigmas:
            if requested_sigma is not None and sigma != requested_sigma:
                continue
            if sigma not in completed or sigma not in manifest.get("completed_sigmas", []):
                continue
            metrics_path = root / "work" / "results" / f"run_{run_id}" / f"sigma_{sigma}_metrics.json"
            if metrics_path.is_symlink() or not metrics_path.resolve().is_relative_to(root.resolve()):
                raise ValueError("결과 파일 경계 오류")
            metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
            validate_result(root, metrics, expected_run=run_id)
            privacy_path=safe_path(root, f"work/results/run_{run_id}/sigma_{sigma}_privacy.json")
            privacy=json.loads(privacy_path.read_text(encoding="utf-8"),parse_constant=reject_nonfinite)
            validate_privacy_result(root,privacy,expected_run=run_id)
            if privacy.get("sigma")!=sigma or type(privacy.get("sigma"))is not int:
                raise ValueError("특징 그림 점수 강도 불일치")
            selection=load_selection(root,run_id,sigma)
            item_identity={key:selection[key]for key in ("protocol","protocol_fixed_model","training_sigma","checkpoint_sha256","model_state_sha256","checkpoint_epoch","selected_checkpoint")}

            if metrics.get("run_id") != run_id or metrics.get("sigma") != sigma or not metrics.get("test") or not metrics.get("completed_at"):
                continue
            bundle = []
            for class_key, class_label in classes.items():
                for stage in range(6):
                    item_id = f"{sigma}-{class_key}-{stage}"
                    matches = [item for item in raw_items if item.get("id") == item_id]
                    if len(matches) != 1:
                        raise ValueError("18장 묶음 누락 또는 중복")
                    entry = matches[0]
                    if entry.get("run_id") != run_id:
                        raise ValueError("특징맵 개별 실행 불일치")
                    for key in ("protocol", "protocol_fixed_model", "training_sigma", "checkpoint_sha256", "model_state_sha256", "checkpoint_epoch", "selected_checkpoint"):
                        if entry.get(key) != item_identity[key] or type(entry.get(key)) is not type(item_identity[key]):
                            raise ValueError("특징맵 개별 고정 모델 불일치")
                    relative = feature_preview_path(sigma, class_key, stage)
                    if entry.get("relative_path", "").replace("\\", "/") != relative.as_posix():
                        raise ValueError("등록되지 않은 이미지 경로")
                    path = safe_path(folder, relative)
                    if path.is_symlink() or not path.resolve().is_relative_to(folder.resolve()) or path.stat().st_size > 8 * 1024 * 1024:
                        raise ValueError("이미지 경계 또는 크기 오류")
                    item = {"id": item_id, "sigma": sigma, "class_key": class_key, "class_label": class_label,
                            "stage": stage, "image_url": f"/api/feature-previews/image/{item_id}",
                            "caption": str(entry.get("caption", "")), "width": entry.get("width"), "height": entry.get("height")}
                    # 사진 이해에 필요한 생성 조건만 전달하고 원본 경로·해시는 노출하지 않습니다.
                    policy = metrics.get("training_policy", {})
                    item["settings"] = {
                        "layer": str(entry.get("layer", "")), "shape": entry.get("shape", []),
                        "panel_indices": entry.get("panel_indices", []),
                        "panel_count": entry.get("panel_count", 1),
                        "panel_minmax": entry.get("panel_minmax", []),
                        "checkpoint_epoch": entry.get("checkpoint_epoch"),
                        "training_sigma": sigma, "checkpoint_sha256": selection["checkpoint_sha256"],
                        "eval_optimizer_steps": 0,
                        "precision": "CPU FP32 평가 추론",
                        "preprocessing": "512×512 회색조를 3채널에 복제한 뒤 RGB 평균·표준편차로 정규화합니다.",
                        "normalization": "입력 CT의 회색조 표시" if stage == 0 else "각 패널의 최솟값·최댓값으로 개별 정규화",
                        "training_policy": {key: policy[key] for key in
                            ("optimizer", "batch_size", "initial_learning_rate", "weight_decay", "max_epochs", "patience", "min_delta", "early_stopping_enabled")
                            if key in policy},
                    }
                    # 목록 조회는 이미지를 모두 읽지 않습니다. 전송할 한 파일만 읽어 해시를 확인합니다.
                    if requested_id == item_id:
                        payload = path.read_bytes()
                        if not payload.startswith(b"\x89PNG\r\n\x1a\n") or hashlib.sha256(payload).hexdigest() != entry.get("sha256"):
                            raise ValueError("이미지 무결성 오류")
                        item["_payload"] = payload
                    bundle.append(item)
            result["items"].extend(bundle)
            result["completed_sigmas"].append(sigma)
            result["pending"].remove(sigma)
    except FileNotFoundError:
        result["message"] = "완료된 모델의 전체 특징 맵 생성을 기다리고 있습니다."
    except (OSError, ValueError, TypeError, KeyError, AttributeError):
        # 원본 경로를 노출하지 않고 준비 오류를 화면에서 구분할 수 있게 합니다.
        result.update(items=[], completed_sigmas=[], pending=list(sigmas))
        result["error"] = "특징 맵의 실행·소스·고정 모델 또는 이미지 무결성을 확인할 수 없습니다."
    return result


def open_status_file(path: Path):
    """원자적 교체를 막지 않는 읽기 전용 바이너리 파일을 엽니다."""
    if os.name != "nt":
        return path.open("rb")
    import msvcrt
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.CreateFileW.argtypes = [ctypes.c_wchar_p, ctypes.c_uint32, ctypes.c_uint32,
                                  ctypes.c_void_p, ctypes.c_uint32, ctypes.c_uint32,
                                  ctypes.c_void_p]
    kernel.CreateFileW.restype = ctypes.c_void_p
    kernel.CloseHandle.argtypes = [ctypes.c_void_p]
    kernel.CloseHandle.restype = ctypes.c_int
    # 삭제 공유는 쓰기 권한을 부여하지 않으며 읽는 동안 이름 교체를 허용합니다.
    for delay in (0.01, 0.02, 0.04, 0.08, None):
        handle = kernel.CreateFileW(str(path), 0x80000000, 0x00000007, None, 3, 0x80, None)
        if handle != ctypes.c_void_p(-1).value:
            break
        error_code = ctypes.get_last_error()
        # 이름 교체 순간의 파일/경로 부재와 공유 위반만 짧게 재시도합니다.
        if error_code not in (2, 3, 32) or delay is None:
            raise ctypes.WinError(error_code)
        time.sleep(delay)
    try:
        descriptor = msvcrt.open_osfhandle(handle, os.O_RDONLY | os.O_BINARY)
    except BaseException:
        kernel.CloseHandle(handle)
        raise
    try:
        # 여기부터 파일 객체가 descriptor와 원래 Windows 핸들의 닫기를 소유합니다.
        return os.fdopen(descriptor, "rb")
    except BaseException:
        os.close(descriptor)
        raise


def reject_nonfinite(value):
    """상태 JSON의 NaN 및 무한대를 손상된 관측으로 처리합니다."""
    raise ValueError("유한하지 않은 JSON 수치: " + value)


STATUS_FIELDS = {"schema_version", "protocol_fixed_model", "protocol", "phase", "training_status", "training_sigma",
                 "stage", "status", "updated_at", "pid", "run_id", "sigma", "sigma_index", "sigmas", "epochs", "epoch",
                 "batch", "batches", "learning_rate", "optimizer_steps", "best_epoch", "best_raw_epoch", "early_stopping_wait",
                 "classification_status", "privacy_status", "score_version", "evaluation_current_sigma", "checkpoint_sha256", "model_state_sha256", "eval_optimizer_steps"}
HISTORY_FIELDS = {"sigma", "epoch", "train_loss", "val_loss", "val_accuracy", "val_auc", "learning_rate",
                  "next_learning_rate", "optimizer_steps", "early_stopping_wait"}

def public_status(data):
    """화면이 사용하는 등록된 필드만 반환합니다."""
    # 상태 원문에 진단 경로가 추가되어도 인증된 화면에 자동 노출하지 않습니다.
    scalar = lambda value: value is None or isinstance(value, (str, bool)) or type(value) in (int, float)
    output = {key: value for key, value in data.items() if key in STATUS_FIELDS and scalar(value)}
    output["sigmas"] = list(SIGMA_VALUES)
    for key, fields in {"training_policy": {"max_epochs", "patience", "early_stopping_enabled", "min_delta", "batch_size", "optimizer", "initial_learning_rate", "weight_decay"},
                        "device": {"type", "name", "torch_version"}, "seen_per_class": {"OK", "NG"}}.items():
        value = data.get(key)
        if isinstance(value, dict):
            output[key] = {k: v for k, v in value.items() if k in fields and scalar(v)}
        elif key == "device" and isinstance(value, str):
            output[key] = value
    output["history"] = [{key: value for key, value in row.items() if key in HISTORY_FIELDS and scalar(value)}
                         for row in data.get("history", []) if isinstance(row, dict)] if isinstance(data.get("history", []), list) else None
    output["sigma_queue"] = [{key: value for key, value in row.items() if key in {"sigma", "status", "training_status", "classification_status", "privacy_status"} and scalar(value)}
                             for row in data.get("sigma_queue", []) if isinstance(row, dict)] if isinstance(data.get("sigma_queue", []), list) else None
    dataset = data.get("dataset")
    if isinstance(dataset, dict):
        output["dataset"] = {"original_total": dataset.get("original_total") if type(dataset.get("original_total")) is int else None,
                             "splits": {}}
        splits = dataset.get("splits", {})
        for split in ("train", "validation", "test"):
            row = splits.get(split, {}) if isinstance(splits, dict) else {}
            output["dataset"]["splits"][split] = {key: value for key, value in row.items() if key in {"OK", "NG", "total"} and type(value) is int} if isinstance(row, dict) else {}
    if data.get("error"):
        output["error"] = {"error_type": "실행 오류"}
    return output


def read_status(root: Path):
    meta = {"observed_at": datetime.now(timezone.utc).isoformat(), "stale": True,
            "age_seconds": None, "process_alive": None, "read_error": None}
    try:
        path = safe_path(root, "work/runtime/status.json")
        # 상태 파일이 다른 위치로 연결되면 읽지 않습니다.
        if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
            raise ValueError("상태 파일 경계 위반")
        with open_status_file(path) as stream:
            payload = stream.read(MAX_STATUS_BYTES + 1)
        if len(payload) > MAX_STATUS_BYTES:
            raise ValueError("상태 파일이 허용 크기를 초과했습니다")
        data = json.loads(payload.decode("utf-8"), parse_constant=reject_nonfinite)
        if not isinstance(data, dict):
            raise ValueError("상태 원문은 JSON 객체여야 합니다")
        stamp = datetime.fromisoformat(str(data.get("updated_at", "")).replace("Z", "+00:00"))
        if stamp.tzinfo is None:
            raise ValueError("상태 갱신 시각에 시간대가 없습니다")
        if data.get("run_id") is not None:
            validate_run(root, data["run_id"])
            if data.get("training_status") == "completed":
                selection = load_selection(root, data["run_id"], data.get("sigma"))
                if type(data.get("epoch")) is not int or data["epoch"] != 100:
                    raise ValueError("고정 완료 상태의 학습 회차 불일치")
                for key in ("training_sigma", "best_epoch", "checkpoint_sha256", "model_state_sha256"):
                    if data.get(key) != selection[key] or type(data.get(key)) is not type(selection[key]):
                        raise ValueError("현재 완료 상태와 선정 모델 불일치")
        data = public_status(data)
        age = max(0, (datetime.now(timezone.utc) - stamp).total_seconds())
        meta.update(age_seconds=round(age, 1), stale=data.get("status") == "running" and age > 60,
                    process_alive=process_alive(data.get("pid")))
    except FileNotFoundError:
        data = {"stage": "ready", "status": "waiting", "message": "학습 상태가 아직 기록되지 않았습니다", "history": []}
        meta["read_error"] = "상태 파일 대기"
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as error:
        data = {"stage": "error", "status": "failed", "message": "상태 파일을 읽을 수 없습니다", "history": []}
        # 로컬 파일의 절대 경로와 의료 원문은 응답에 포함하지 않습니다.
        meta["read_error"] = "상태 파일 형식 또는 읽기 오류: " + type(error).__name__
    data["_dashboard"] = meta
    return data


SIGMA_VALUES = (0,) + PREVIEW_SIGMAS


def sigma_results(root, sigma):
    """현재 실행에서 해당 강도가 독립 학습·평가한 결과만 제공합니다."""
    state = read_status(root)
    run_id = state.get("run_id")
    valid_run = isinstance(run_id, str) and len(run_id) == 16 and all(c in "0123456789abcdef" for c in run_id)
    valid_sigma = type(sigma) is int and sigma in SIGMA_VALUES
    result = {"run_id": run_id if valid_run else None, "sigma": sigma if valid_sigma else None,
              "history": [], "evaluation_history": [], "metrics": None, "privacy": None, "privacy_status": "pending", "status": "unavailable",
              "message": "현재 실행의 결과 기록을 기다리고 있습니다."}
    if not valid_sigma or not valid_run:
        return result
    folder = root / "work" / "results" / f"run_{run_id}"
    try:
        validate_run(root, run_id)
        if state.get("protocol_fixed_model") is not False or state.get("protocol") != "independent-sigma-privacy-v1":
            raise ValueError("강도별 독립 모델 프로토콜 불일치")
        queue = state.get("sigma_queue", [])
        if not isinstance(queue, list) or any(not isinstance(item, dict) or type(item.get("sigma")) is not int
                                              or item["sigma"] not in SIGMA_VALUES for item in queue):
            raise ValueError("강도 대기열 형식 오류")
        entries = [item for item in queue if item["sigma"] == sigma]
        if len(entries) > 1:
            raise ValueError("강도 대기열 중복")
        entry = entries[0] if entries else {}
        status = entry.get("status", "pending")
        privacy_status = entry.get("privacy_status", "pending")
        if privacy_status not in ("pending", "running", "completed", "error"):
            raise ValueError("점수 상태 형식 오류")
        result["privacy_status"] = privacy_status
        if status not in ("completed", "pending", "running", "interrupted", "failed", "error") or not isinstance(status, str):
            raise ValueError("강도 상태 형식 오류")
        def number(value, minimum=0, maximum=None, nullable=False, integer=False):
            # bool과 숫자 모양 문자열은 수치가 아닙니다. 정수는 화면의 정확한 표현 범위도 지킵니다.
            if nullable and value is None:
                return None
            if type(value) not in (int, float) or (integer and type(value) is not int):
                raise ValueError("결과 수치 형식 오류")
            if (type(value) is int and abs(value) > 2**53 - 1) or not math.isfinite(value):
                raise ValueError("결과 수치 범위 오류")
            if value < minimum or (maximum is not None and value > maximum):
                raise ValueError("결과 수치 범위 오류")
            return value

        def public_history(history):
            if not isinstance(history, list):
                raise ValueError("곡선 목록 형식 오류")
            selected = []
            for row in history:
                if not isinstance(row, dict) or type(row.get("sigma")) is not int or row["sigma"] not in SIGMA_VALUES:
                    raise ValueError("곡선 강도 오류")
                if row["sigma"] != sigma:
                    raise ValueError("곡선 강도 불일치")
                if "run_id" in row and row["run_id"] != run_id:
                    raise ValueError("곡선 실행 불일치")
                epoch = number(row.get("epoch"), minimum=1, integer=True)
                if epoch != len(selected) + 1:
                    raise ValueError("곡선 회차 불일치")
                public = {"sigma": sigma, "epoch": epoch}
                for key in ("train_loss", "val_loss", "learning_rate", "next_learning_rate"):
                    public[key] = number(row.get(key))
                public["val_accuracy"] = number(row.get("val_accuracy"), maximum=1)
                public["val_auc"] = number(row.get("val_auc"), maximum=1, nullable=True)
                public["optimizer_steps"] = number(row.get("optimizer_steps"), integer=True)
                if "early_stopping_wait" in row:
                    public["early_stopping_wait"] = number(row["early_stopping_wait"], maximum=epoch, integer=True)
                if selected and public["optimizer_steps"] < selected[-1]["optimizer_steps"]:
                    raise ValueError("곡선 갱신 횟수 불일치")
                selected.append(public)
            return selected

        for part in (root / "work", root / "work" / "results", folder):
            if part.is_symlink() or not part.resolve().is_relative_to(root.resolve()):
                raise ValueError("결과 경계 오류")
        def read_json(name):
            path = safe_path(root, folder / name)
            if path.is_symlink() or not path.resolve().is_relative_to(folder.resolve()):
                raise ValueError("결과 경계 오류")
            with open_status_file(path) as stream:
                payload = stream.read(MAX_STATUS_BYTES + 1)
            if len(payload) > MAX_STATUS_BYTES:
                raise ValueError("결과 크기 오류")
            return json.loads(payload.decode("utf-8"), parse_constant=reject_nonfinite)

        training_complete = entry.get("training_status") == "completed"
        classification_complete = entry.get("classification_status") == "completed"
        if not training_complete:
            history = public_history(state.get("history", [])) if state.get("sigma") == sigma else []
            result.update(history=history, status="running" if entry.get("training_status")=="running" else "pending",
                          message="선택한 강도의 독립 학습 기록입니다. 분류 성적과 점수는 각각 계산이 끝난 뒤 표시합니다.")
            return result
        if classification_complete:
            metrics = read_json(f"sigma_{sigma}_metrics.json")
            validate_result(root, metrics, expected_run=run_id)
            selection = metrics
            if type(metrics.get("sigma")) is not int or metrics["sigma"] != sigma:
                raise ValueError("결과 강도 불일치")
            stamp = metrics.get("completed_at")
            if not isinstance(stamp, str) or not 20 <= len(stamp) <= 40 or stamp[10] != "T" or any(c not in "0123456789-T:+.Z" for c in stamp):
                raise ValueError("결과 완료 시각 형식 오류")
            if datetime.fromisoformat(stamp.replace("Z", "+00:00")).tzinfo is None:
                raise ValueError("결과 완료 시각 시간대 누락")
            selected = {"best_epoch": number(metrics.get("best_epoch"), minimum=1, maximum=100, integer=True),
                        "epochs_ran": number(metrics.get("epochs_ran"), minimum=100, maximum=100, integer=True),
                        "optimizer_steps": number(metrics.get("optimizer_steps"), integer=True),
                        "eval_optimizer_steps": number(metrics.get("eval_optimizer_steps"), minimum=0, maximum=0, integer=True),
                        "training_sigma": sigma, "checkpoint_sha256": selection["checkpoint_sha256"],
                        "model_state_sha256": selection["model_state_sha256"], "completed_at": stamp}
            history = public_history(read_json(f"sigma_{sigma}_history.json"))
            if len(history) != 100 or history[-1]["optimizer_steps"] != selected["optimizer_steps"]:
                raise ValueError("완료 결과와 학습 곡선 불일치")
            test = metrics.get("test")
            if not isinstance(test, dict):
                raise ValueError("시험 결과 형식 오류")
            selected["test"] = {"accuracy": number(test.get("accuracy"), maximum=1),
                                "auc": number(test.get("auc"), maximum=1, nullable=True),
                                "loss": number(test.get("loss")),
                                "n_images": number(test.get("n_images"), minimum=1, integer=True)}
            if "confusion_matrix" in test:
                matrix = test["confusion_matrix"]
                if not isinstance(matrix, list) or len(matrix) != 2 or any(not isinstance(row, list) or len(row) != 2 for row in matrix):
                    raise ValueError("시험 혼동 행렬 형식 오류")
                checked = [[number(value, integer=True) for value in row] for row in matrix]
                if sum(sum(row) for row in checked) != selected["test"]["n_images"]:
                    raise ValueError("시험 혼동 행렬 표본 수 불일치")
                correct_count = checked[0][0] + checked[1][1]
                # 표시 반올림 전의 저장 원비율과 행렬의 실제 정답 비율을 대조합니다.
                if correct_count / selected["test"]["n_images"] != selected["test"]["accuracy"]:
                    raise ValueError("시험 혼동 행렬과 정확도 원비율 불일치")
                selected["test"]["correct_count"] = correct_count

            validation = metrics.get("validation")
            if not isinstance(validation, dict):
                raise ValueError("검증 평가 결과 누락")
            selected["validation"] = {"accuracy": number(validation.get("accuracy"), maximum=1),
                                      "loss": number(validation.get("loss")),
                                      "auc": number(validation.get("auc"), maximum=1, nullable=True),
                                      "n_images": number(validation.get("n_images"), minimum=1, integer=True)}
            result.update(history=history, metrics=selected, status="running",
                          message="이 강도의 100회 독립 학습과 분류 평가를 마쳤습니다. 원본 찾기·복원 저항 점수 계산 상태를 확인하세요.")
            if privacy_status == "completed":
                try:
                    privacy = read_json(f"sigma_{sigma}_privacy.json")
                    validate_privacy_result(root, privacy, expected_run=run_id)
                    if type(privacy.get("sigma")) is not int or privacy["sigma"] != sigma:
                        raise ValueError("점수 강도 불일치")
                    public = {"score_version": "gallery-residual-v1"}
                    for key, maximum in (("score",100),("T_attack",1),("T_prior",1),("fractional_top1",1),("raw_ratio",None)):
                        public[key] = number(privacy.get(key), maximum=maximum)
                    for key in ("G", "n_queries", "original_test_images", "exact_return_groups", "target_in_tie_groups"):
                        public[key] = number(privacy.get(key), integer=True, minimum=2 if key=="G" else 0)
                    if public["n_queries"] != public["G"] or public["exact_return_groups"] > public["G"] or public["target_in_tie_groups"] > public["G"]:
                        raise ValueError("점수 그룹 분모 불일치")
                    for key in ("residual_quantiles", "tie_histogram"):
                        values=privacy.get(key)
                        if not isinstance(values,dict) or len(values)>10000:
                            raise ValueError("점수 분포 형식 오류")
                        allowed={"0","0.25","0.5","0.75","1"} if key=="residual_quantiles" else {str(i)for i in range(1,public["G"]+1)}
                        if any(k not in allowed for k in values):
                            raise ValueError("점수 분포 항목 오류")
                        public[key]={k:number(v,maximum=1 if key=="residual_quantiles" else public["G"],integer=key=="tie_histogram")for k,v in values.items()}
                    controls=privacy.get("controls")
                    if not isinstance(controls,dict) or controls.get("original_score")!=0 or controls.get("constant_score")!=100:
                        raise ValueError("점수 대조군 오류")
                    public["controls"]={"original_score":0,"constant_score":100}
                    result.update(privacy=public, status="completed", message="선택한 강도의 분류 성적과 실제 원본 후보 공격 점수 계산을 마쳤습니다.")
                except (FileNotFoundError,OSError,ValueError,TypeError,KeyError,AttributeError):
                    result.update(privacy=None,privacy_status="error",status="error",message="분류 결과는 확인했지만 점수 파일의 실행·모델·원값 연결을 확인할 수 없습니다. 오류 원문을 보존하고 복구를 기다립니다.")
            elif privacy_status == "error":
                result.update(status="error",message="이 강도의 분류 결과는 보존됐습니다. 점수 계산 오류를 복구한 뒤 다시 계산합니다.")
        else:
            load_selection(root, run_id, sigma)
            history=public_history(read_json(f"sigma_{sigma}_history.json"))
            if len(history)!=100:
                raise ValueError("완료 학습 회차 누락")
            result.update(history=history,status="running",message="이 강도의 독립 학습을 마쳤습니다. 분류 평가와 점수 계산을 기다립니다.")
    except FileNotFoundError:
        result.update(history=[], evaluation_history=[], metrics=None, message="현재 실행의 해당 강도 모델 또는 평가 파일을 기다리고 있습니다.")
    except (OSError, ValueError, TypeError, AttributeError, KeyError):
        result.update(history=[], evaluation_history=[], metrics=None, status="unavailable", message="실행·소스·해당 강도 모델과 결과 기록의 일치를 확인할 수 없습니다.")
    return result


def make_server(root=ROOT, port=8766, token=None):
    root = Path(root).resolve()
    session_token = token or secrets.token_urlsafe(32)

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_args):
            pass

        def send_content(self, status, body, content_type="text/plain; charset=utf-8", headers=None):
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self'; font-src 'self'; connect-src 'self'; img-src 'self' data:; object-src 'none'; base-uri 'none'; frame-ancestors 'none'")
            for key, value in (headers or {}).items():
                self.send_header(key, value)
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            # DNS 재바인딩 및 다른 사이트의 교차 출처 조회를 차단합니다.
            expected_host = f"127.0.0.1:{self.server.server_port}"
            if self.headers.get("Host") != expected_host:
                self.send_content(HTTPStatus.FORBIDDEN, "허용되지 않은 호스트".encode())
                return
            parts = urlsplit(self.path)
            supplied = parse_qs(parts.query).get("token", [""])[0]
            if parts.path == "/" and supplied and secrets.compare_digest(supplied, session_token):
                self.send_content(HTTPStatus.SEE_OTHER, b"", headers={
                    "Location": "/", "Set-Cookie": f"dashboard_session={session_token}; HttpOnly; SameSite=Strict; Path=/"})
                return
            cookies = SimpleCookie()
            try:
                cookies.load(self.headers.get("Cookie", ""))
                value = cookies["dashboard_session"].value if "dashboard_session" in cookies else ""
            except Exception:
                value = ""
            if not secrets.compare_digest(value, session_token):
                self.send_content(HTTPStatus.UNAUTHORIZED, "세션 URL로 접속해 주세요".encode())
                return
            if parts.path == "/api/status" and not parts.query:
                payload = json.dumps(read_status(root), ensure_ascii=False, allow_nan=False).encode("utf-8")
                self.send_content(HTTPStatus.OK, payload, "application/json; charset=utf-8")
                return
            if parts.path.startswith("/api/sigma-results/"):
                suffix = parts.path.removeprefix("/api/sigma-results/")
                if parts.query or suffix not in {str(value) for value in SIGMA_VALUES}:
                    self.send_content(HTTPStatus.BAD_REQUEST, "등록된 블러 강도가 아닙니다".encode())
                    return
                payload = json.dumps(sigma_results(root, int(suffix)), ensure_ascii=False, allow_nan=False).encode("utf-8")
                self.send_content(HTTPStatus.OK, payload, "application/json; charset=utf-8")
                return
            if parts.path == "/api/feature-previews" and not parts.query:
                payload = json.dumps(feature_previews(root), ensure_ascii=False, allow_nan=False).encode("utf-8")
                self.send_content(HTTPStatus.OK, payload, "application/json; charset=utf-8")
                return
            if parts.path.startswith("/api/feature-previews/image/") and not parts.query:
                suffix = parts.path.removeprefix("/api/feature-previews/image/")
                available = feature_previews(root, requested_id=suffix)
                if not any(item["id"] == suffix and "_payload" in item for item in available["items"]):
                    self.send_content(HTTPStatus.NOT_FOUND, "완료된 대표 특징맵이 없습니다".encode())
                    return
                # 해시 검증한 동일 바이트를 보내고 파일을 다시 열지 않습니다.
                payload = next(item["_payload"] for item in available["items"] if item["id"] == suffix)
                self.send_content(HTTPStatus.OK, payload, "image/png")
                return
            if parts.path not in ASSETS or parts.query:
                self.send_content(HTTPStatus.NOT_FOUND, "등록되지 않은 경로".encode())
                return
            web = (root / "web").resolve()
            path = web / ASSETS[parts.path]
            if not web.is_relative_to(root) or path.is_symlink() or not path.resolve().is_relative_to(web):
                self.send_content(HTTPStatus.FORBIDDEN, b"Forbidden")
                return
            try:
                content = path.read_bytes()
            except OSError:
                self.send_content(HTTPStatus.NOT_FOUND, b"Not found")
                return
            mime = "text/javascript" if path.suffix == ".js" else mimetypes.guess_type(path.name)[0] or "application/octet-stream"
            self.send_content(HTTPStatus.OK, content, mime)

    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    server.session_token = session_token
    return server


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8766)
    args = parser.parse_args()
    server = make_server(port=args.port)
    record = {"url": f"http://127.0.0.1:{server.server_port}/?token={server.session_token}",
              "pid": os.getpid(), "port": server.server_port,
              "started_at": datetime.now(timezone.utc).isoformat()}
    work = ROOT / "work"
    work.mkdir(exist_ok=True)
    temporary = work / "server.json.tmp"
    temporary.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.replace(work / "server.json")
    try:
        server.serve_forever(poll_interval=0.5)
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()

"""대시보드 상태는 원자적으로 갱신하고 실제 사건만 추가 기록합니다."""

from datetime import datetime, timedelta, timezone
import ctypes
import json
import os
from pathlib import Path
import tempfile
import time


def now_kst():
    return datetime.now(timezone(timedelta(hours=9))).isoformat(timespec="seconds")


def replace_file(source, destination):
    source, destination = Path(source), Path(destination)
    if os.name != "nt" or not destination.exists():
        os.replace(source, destination)
        return
    # MoveFileEx 기반 os.replace는 삭제 공유 reader가 있어도 기존 대상 교체를 거부합니다.
    # ReplaceFileW는 기존 ACL을 유지하고 열린 reader에는 이전 버전을 보존합니다.
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    replace = kernel.ReplaceFileW
    replace.argtypes = [ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_wchar_p,
                        ctypes.c_uint32, ctypes.c_void_p, ctypes.c_void_p]
    replace.restype = ctypes.c_int
    if not replace(str(destination), str(source), None, 0, None, None):
        raise ctypes.WinError(ctypes.get_last_error())


def atomic_json(path, payload):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary = tempfile.mkstemp(prefix=path.stem + "-", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(handle, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(payload, stream, ensure_ascii=False, indent=2, allow_nan=False)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        # Windows 읽기 핸들의 짧은 삭제/이름변경 잠금만 최대 0.63초 동안 재시도합니다.
        # 권한 문제가 지속되거나 다른 오류이면 원래 예외를 그대로 반환합니다.
        delays = (0.01, 0.02, 0.04, 0.08, 0.16, 0.32)
        for attempt in range(len(delays) + 1):
            try:
                replace_file(temporary, path)
                break
            except PermissionError as error:
                if getattr(error, "winerror", None) not in {5, 32} or attempt == len(delays):
                    raise
                time.sleep(delays[attempt])
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


class StatusWriter:
    def __init__(self, root, config):
        self.root = Path(root)
        self.folder = self.root / "work/runtime"
        self.folder.mkdir(parents=True, exist_ok=True)
        self.data = {"schema_version": 1, "stage": "preparing", "status": "running", "message": "원본 자료 확인 중",
                     "training_policy": {"max_epochs": config.get("epochs", 100),
                                         "patience": config.get("early_stopping_patience", 15),
                                         "min_delta": config.get("min_delta", 1e-4),
                                         "scheduler_patience": config.get("scheduler_patience", 4),
                                         "batch_size": config.get("batch_size", 8)},
                     "pid": os.getpid(), "epoch": 0, "epochs": config.get("epochs", 35),
                     "batch": 0, "batches": 0, "seen_per_class": {"OK": 0, "NG": 0},
                     "history": [], "dataset": None, "evaluation": None, "device": None, "error": None,
                     "sigma": 0, "sigma_index": 1, "sigmas": config.get("sigmas", [0]),
                     "sigma_queue": [{"sigma": sigma, "status": "pending", "result": None} for sigma in config.get("sigmas", [0])],
                     "limitations": ["환자 ID 없는 영상 단위 예비실험이며 임상 성능으로 해석할 수 없습니다.",
                                     "원본의 7-fold 환자 교차검증·복원 공격·동일 영상 매칭은 이번 실행에 포함되지 않습니다."]}

    def update(self, **values):
        self.data.update(values)
        self.data["updated_at"] = now_kst()
        atomic_json(self.folder / "status.json", self.data)

    def event(self, name, details=None):
        item = {"time": now_kst(), "pid": os.getpid(), "event": name, "details": details or {}}
        with (self.folder / "events.jsonl").open("a", encoding="utf-8", newline="\n") as stream:
            stream.write(json.dumps(item, ensure_ascii=False, allow_nan=False) + "\n")

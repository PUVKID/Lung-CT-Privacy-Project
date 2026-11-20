"""동일 학습 코드 앞에 공간·중복 확인과 독립 오류 보존 경계만 둡니다."""

from __future__ import annotations

import argparse
import ctypes
from datetime import datetime, timezone, timedelta
import json
import ntpath
import os
from pathlib import Path
import shutil
import subprocess
import sys
import threading
import traceback

ROOT = Path(__file__).resolve().parents[1]
MIN_TRAIN_FREE = 8 * 1024 ** 3
MIN_LOG_FREE = 256 * 1024 ** 2


def exception_payload(error):
    observed = {}
    try:
        for path in (ROOT / ".codex/routing-state").glob("*.json"):
            if len(path.stem) == 24 and all(c in "0123456789abcdef" for c in path.stem):
                saved = json.loads(path.read_text(encoding="utf-8-sig"))
                observed = {key: saved[key] for key in ["repair_used", "input_fix_used", "stop_failures", "verification_failures"]}
                break
    except Exception as secondary:
        # 누적 상태 읽기 실패가 이미 발생한 원오류를 덮지 않도록 별도 표시합니다.
        observed = {"counter_read_error": repr(secondary)}
    return {"time_kst": datetime.now(timezone(timedelta(hours=9))).isoformat(),
            "session": os.environ.get("CT_EXPERIMENT_SESSION", "local-session"), "task": os.environ.get("CT_EXPERIMENT_TASK", "local-experiment"), **observed,
            "error_type": type(error).__name__, "error": str(error),
            "errno": getattr(error, "errno", None), "winerror": getattr(error, "winerror", None),
            "traceback": "".join(traceback.format_exception(type(error), error, error.__traceback__)),
            "argv": [sys.executable, *sys.orig_argv[1:]], "cwd": os.getcwd(), "pid": os.getpid(), "exit_code": 1,
            "changes_at_failure": "8차 상태·checkpoint의 마지막 완료epoch와 함께 확인; 기존1~7차 입력은 읽기 전용"}


def write_independent_logs(folders, filename, payload):
    """한 볼륨의 오류가 다른 볼륨의 원오류 기록을 막지 않게 각각 저장합니다."""
    failures, good = [], []
    for folder in map(Path, folders):
        try:
            folder.mkdir(parents=True, exist_ok=True)
            path = folder / filename
            with path.open("w", encoding="utf-8", newline="\n") as stream:
                json.dump({**payload, "secondary_log_errors": failures}, stream, ensure_ascii=False, indent=2, allow_nan=False)
                stream.write("\n"); stream.flush(); os.fsync(stream.fileno())
            good.append(path)
        except Exception as error:
            failures.append({"folder": str(folder), **exception_payload(error)})
    # 성공한 볼륨에도 먼저/나중에 생긴 secondary 오류를 함께 남깁니다.
    if failures:
        for path in good:
            try:
                with path.open("w", encoding="utf-8", newline="\n") as stream:
                    json.dump({**payload, "secondary_log_errors": failures}, stream, ensure_ascii=False, indent=2, allow_nan=False)
                    stream.write("\n"); stream.flush(); os.fsync(stream.fileno())
            except Exception as error:
                print(json.dumps({"secondary_log_error": exception_payload(error)}, ensure_ascii=False), file=sys.stderr, flush=True)
    return failures


def require_free_space(path, minimum):
    probe = Path(path).resolve()
    while not probe.exists():
        probe = probe.parent
    free = shutil.disk_usage(probe).free
    if free < minimum:
        raise OSError(28, f"저장 여유 공간이 기준보다 작습니다: free={free}, required={minimum}, volume={probe.anchor}")
    return free


def reject_duplicates(processes):
    if processes:
        raise RuntimeError("같은 프로젝트의 학습 프로세스가 있어 중복 실행하지 않습니다: " +
                           ", ".join(str(item["pid"]) for item in processes))


def windows_process(pid):
    """숫자로 확인한 단일 PID의 부모와 실행파일만 읽습니다."""
    if type(pid) is not int or pid <= 0:
        raise ValueError("유효한 프로세스 PID가 필요합니다.")
    command = ("$ErrorActionPreference='Stop'; [Console]::OutputEncoding=[System.Text.UTF8Encoding]::new($false); "
               f"Get-CimInstance Win32_Process -Filter 'ProcessId = {pid}' | "
               "Select-Object ProcessId,ParentProcessId,ExecutablePath | ConvertTo-Json -Compress")
    result = subprocess.run(["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", command],
                            capture_output=True, text=True, encoding="utf-8", errors="strict", timeout=20,
                            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    if result.returncode:
        raise RuntimeError("worker 감독 연결 조회 실패: " + result.stderr)
    return json.loads(result.stdout) if result.stdout.strip() else None


def worker_parent_authorized(supervisor_pid):
    """직접 감독 또는 그 감독이 만든 동일 venv launcher 한 단계만 허용합니다."""
    if (not isinstance(supervisor_pid, str) or not supervisor_pid.isascii()
            or not supervisor_pid.isdecimal() or int(supervisor_pid) <= 0):
        return False
    supervisor_pid = int(supervisor_pid)
    parent_pid = os.getppid()
    if parent_pid == supervisor_pid:
        return True
    if os.name != "nt":
        return False
    launcher = windows_process(parent_pid)
    if (not isinstance(launcher, dict) or launcher.get("ProcessId") != parent_pid
            or launcher.get("ParentProcessId") != supervisor_pid
            or not isinstance(launcher.get("ExecutablePath"), str)):
        return False
    normalize = lambda path: os.path.normcase(os.path.abspath(path))
    return normalize(launcher["ExecutablePath"]) == normalize(sys.executable)


def windows_arguments(command_line):
    """Windows의 실제 따옴표 규칙으로 명령행을 분리하며 작업 폴더는 추측하지 않습니다."""
    from ctypes import wintypes
    count = ctypes.c_int()
    parse = ctypes.WinDLL("shell32", use_last_error=True).CommandLineToArgvW
    parse.argtypes = [wintypes.LPCWSTR, ctypes.POINTER(ctypes.c_int)]
    parse.restype = ctypes.POINTER(wintypes.LPWSTR)
    arguments = parse(command_line, ctypes.byref(count))
    if not arguments:
        raise ctypes.WinError(ctypes.get_last_error())
    release = ctypes.WinDLL("kernel32", use_last_error=True).LocalFree
    release.argtypes = [ctypes.c_void_p]
    release.restype = ctypes.c_void_p
    try:
        return [arguments[index] for index in range(count.value)]
    finally:
        release(ctypes.cast(arguments, ctypes.c_void_p))


def training_processes(project_root):
    if os.name != "nt":
        raise RuntimeError("이 복구 실행의 중복 확인은 Windows CIM에서만 지원합니다.")
    command = "$ErrorActionPreference='Stop'; [Console]::OutputEncoding=[System.Text.UTF8Encoding]::new($false); Get-CimInstance Win32_Process | Where-Object { $_.Name -match '^python(w)?(.exe)?$' } | Select-Object ProcessId,ParentProcessId,ExecutablePath,CommandLine | ConvertTo-Json -Compress"
    result = subprocess.run(["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", command],
                            capture_output=True, text=True, encoding="utf-8", errors="strict", timeout=20,
                            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    if result.returncode:
        raise RuntimeError("학습 중복 조회 실패: " + result.stderr)
    rows = json.loads(result.stdout) if result.stdout.strip() else []
    if isinstance(rows, dict):
        rows = [rows]
    own_pid, parent_pid = os.getpid(), os.getppid()
    own = [row for row in rows if row.get("ProcessId") == own_pid]
    if len(own) != 1 or own[0].get("ParentProcessId") != parent_pid:
        raise RuntimeError("CIM에서 자기 프로세스와 실제 부모 관계를 확인하지 못했습니다.")
    suffix = str(Path(project_root)).replace("\\", "/").lower()
    if len(suffix) > 2 and suffix[1] == ":":
        suffix = suffix[2:]
    found = []
    for row in rows:
        command_line = row.get("CommandLine") or ""
        if row["ProcessId"] == own_pid or not command_line:
            continue
        executable = row.get("ExecutablePath")
        # 실제 부모 관계가 확인된 동일 venv launcher만 자기 실행 체인으로 제외합니다.
        if (row["ProcessId"] == parent_pid and isinstance(executable, str)
                and os.path.normcase(os.path.abspath(executable)) == os.path.normcase(os.path.abspath(sys.executable))):
            continue
        arguments = windows_arguments(command_line)
        scripts = [argument for argument in arguments[1:]
                   if ntpath.basename(argument).lower() in {"run_training.py", "복구_학습.py", "안전_학습.py"}]
        module_call = any(value == "-m" and index + 1 < len(arguments)
                          and arguments[index + 1] in {"run_training", "복구_학습", "안전_학습", "tools.safe_training"}
                          for index, value in enumerate(arguments))
        ambiguous = module_call or any(not ntpath.isabs(script) for script in scripts)
        same_project = any(ntpath.splitdrive(script)[1].replace("\\", "/").lower().startswith(suffix.rstrip("/") + "/")
                           for script in scripts if ntpath.isabs(script))
        if ambiguous or same_project:
            found.append({"pid": row["ProcessId"], "command": command_line,
                          "reason": "상대 호출의 작업 폴더를 확인할 수 없습니다." if ambiguous else "같은 프로젝트의 학습입니다."})
    return found


def log_folders(root):
    local = Path(os.environ.get("LOCALAPPDATA", str(Path.home() / "AppData/Local")))
    return [Path(root) / "work/recovery_logs", local / "폐CT_학습복구" / "8차"]


def worker(root, device, folders):
    """기존 run_training.py의 오류 처리 전에 원오류를 먼저 잡는 별도 진입점입니다."""
    os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")
    os.environ.setdefault("TORCH_HOME", str(Path(root) / "work/torch-cache"))
    from src.state import StatusWriter, atomic_json
    from src.training import run_training
    state = None
    try:
        config = json.loads((Path(root) / "config.json").read_text(encoding="utf-8"))
        state = StatusWriter(root, config)
        state.update()
        run_training(config, root, state, device)
        return 0
    except BaseException as error:
        # 원오류를 상태 갱신·추가 오류 기록보다 먼저 고정합니다.
        details = exception_payload(error)
        details.update(sigma=state.data.get("sigma") if state else None,
                       epoch=state.data.get("epoch") if state else None,
                       attempted_batch=state.data.get("attempted_batch") if state else None)
        name = "원오류_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f") + ".json"
        failures = write_independent_logs(folders, name, details)
        secondary = []
        try:
            atomic_json(Path(root) / "work/runtime/last_error.json", details)
        except Exception as followup:
            secondary.append(exception_payload(followup))
        if state:
            try:
                interrupted = isinstance(error, KeyboardInterrupt)
                for entry in state.data["sigma_queue"]:
                    if entry["status"] == "running":
                        entry["status"] = "error"
                        for field in ["training_status", "classification_status", "privacy_status"]:
                            if entry.get(field) == "running":
                                entry[field] = "error"
                                state.data[field] = "error"
                state.update(stage="interrupted" if interrupted else "error", status="interrupted" if interrupted else "failed",
                             pid=None, error=details, message=f"학습 중단: {type(error).__name__}: {error}")
                state.event("복구 실행 중단", details)
            except Exception as followup:
                secondary.append(exception_payload(followup))
        if failures or secondary:
            write_independent_logs(folders, name, {**details, "secondary_status_errors": secondary,
                                                   "initial_log_errors": failures})
        print(details["traceback"], file=sys.stderr, flush=True)
        return 130 if isinstance(error, KeyboardInterrupt) else 1


def supervise(root, device, baseline_sha256):
    root = Path(root).resolve()
    folders = log_folders(root)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    lock = root / "work/runtime/recovery.lock"
    child = None
    locked = False
    try:
        storage = {"training_free": require_free_space(root, MIN_TRAIN_FREE),
                   "independent_log_free": require_free_space(folders[1], MIN_LOG_FREE)}
        if root.anchor.lower() == folders[1].anchor.lower():
            raise ValueError("독립 오류 로그는 학습과 다른 볼륨이어야 합니다.")
        reject_duplicates(training_processes(root.parent))
        from tools.inputs import verify_training_inputs
        recovery = verify_training_inputs(root, baseline_sha256)
        lock.parent.mkdir(parents=True, exist_ok=True)
        descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        locked = True
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump({"pid": os.getpid(), "time": stamp, **storage, **recovery}, stream, ensure_ascii=False)
        argv = [sys.executable, "-B", "-X", "utf8", "-u", str(root / "안전_학습.py"), "--worker", "--device", device]
        errors = write_independent_logs(folders, f"실행_{stamp}.json", {"argv": argv, "cwd": str(root), **storage, **recovery})
        if errors:
            raise OSError("학습 시작 전 두 볼륨의 독립 로그를 모두 만들지 못했습니다.")
        environment = dict(os.environ, CT_RECOVERY_SUPERVISOR_PID=str(os.getpid()))
        child = subprocess.Popen(argv, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=environment,
                                 creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        log_errors = []

        def pump(pipe, kind):
            streams = []
            for folder in folders:
                try:
                    folder.mkdir(parents=True, exist_ok=True)
                    streams.append((folder, (folder / f"학습_{stamp}.{kind}.log").open("xb")))
                except Exception as error:
                    log_errors.append(exception_payload(error))
            try:
                for block in iter(lambda: pipe.read1(4096), b""):
                    for folder, stream in list(streams):
                        try:
                            stream.write(block); stream.flush()
                        except Exception as error:
                            log_errors.append({"folder": str(folder), **exception_payload(error)})
                            streams.remove((folder, stream)); stream.close()
                    target = sys.stderr if kind == "stderr" else sys.stdout
                    try:
                        target.buffer.write(block); target.buffer.flush()
                    except (OSError, AttributeError):
                        pass
            finally:
                pipe.close()
                for _folder, stream in streams:
                    stream.close()

        pumps = [threading.Thread(target=pump, args=(child.stdout, "stdout")),
                 threading.Thread(target=pump, args=(child.stderr, "stderr"))]
        for thread in pumps:
            thread.start()
        code = child.wait()
        for thread in pumps:
            thread.join()
        write_independent_logs(folders, f"종료_{stamp}.json", {"exit_code": code, "child_pid": child.pid,
                                                           "time_kst": datetime.now().astimezone().isoformat(), "secondary_stream_errors": log_errors})
        return code
    except BaseException as error:
        details = exception_payload(error)
        write_independent_logs(folders, f"실행경계오류_{stamp}.json", details)
        print(details["traceback"], file=sys.stderr, flush=True)
        if child is not None and child.poll() is None:
            child.terminate(); child.wait()
        return 130 if isinstance(error, KeyboardInterrupt) else 1
    finally:
        if locked:
            try:
                lock.unlink()
            except OSError as error:
                write_independent_logs(folders, f"잠금정리오류_{stamp}.json", exception_payload(error))


def main():
    parser = argparse.ArgumentParser(description="8차 강도별 독립 학습과 분류·프라이버시 점수를 시작하거나 마지막 완료 회차에서 재개합니다.")
    parser.add_argument("--device", choices=("cuda", "cpu"), default="cuda")
    parser.add_argument("--baseline-sha256", help="사전에 고정·검토한 비공개 원본 기준의 SHA256")
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.worker:
        try:
            authorized = worker_parent_authorized(os.environ.get("CT_RECOVERY_SUPERVISOR_PID"))
        except Exception as error:
            parser.error("worker 감독 연결을 확인하지 못했습니다: " + str(error))
        if not authorized:
            parser.error("worker는 사전 검사를 통과한 감독 프로세스에서만 시작합니다.")
    if not args.worker and (not args.baseline_sha256 or len(args.baseline_sha256) != 64
                            or any(c not in "0123456789abcdef" for c in args.baseline_sha256)):
        parser.error("사전에 고정한 소문자 SHA256 64자리를 명시해야 합니다.")
    return worker(ROOT, args.device, log_folders(ROOT)) if args.worker else supervise(ROOT, args.device, args.baseline_sha256)

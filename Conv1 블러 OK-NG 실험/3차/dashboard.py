"""실제 학습 상태만 읽는 루프백 전용 대시보드 서버."""
from __future__ import annotations

import argparse
import ctypes
import hashlib
import json
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
    folder = root.parent / "블러 강도별 대표 특징맵" / "2차"
    try:
        if folder.is_symlink() or not folder.resolve().is_relative_to(root.parent.resolve()):
            raise ValueError("이미지 폴더 경계 오류")
        manifest_path = folder / "export_index_private.json"
        if manifest_path.is_symlink() or manifest_path.stat().st_size > 4 * 1024 * 1024:
            raise ValueError("특징맵 목록 형식 오류")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"), parse_constant=reject_nonfinite)
        if not isinstance(run_id, str) or len(run_id) != 16 or any(c not in "0123456789abcdef" for c in run_id) or manifest.get("run_id") != run_id:
            raise ValueError("실행 식별자 불일치")
        completed = {entry.get("sigma") for entry in status.get("sigma_queue", [])
                     if entry.get("status") == "completed"}
        raw_items = manifest.get("items", [])
        if not isinstance(raw_items, list) or len(raw_items) > 180:
            raise ValueError("특징맵 목록 개수 오류")
        for sigma in sigmas:
            if sigma not in completed or sigma not in manifest.get("completed_sigmas", []):
                continue
            metrics_path = root / "work" / "results" / f"run_{run_id}" / f"sigma_{sigma}_metrics.json"
            if metrics_path.is_symlink() or not metrics_path.resolve().is_relative_to(root.resolve()):
                raise ValueError("결과 파일 경계 오류")
            metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
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
                    relative = feature_preview_path(sigma, class_key, stage)
                    if entry.get("relative_path", "").replace("\\", "/") != relative.as_posix():
                        raise ValueError("등록되지 않은 이미지 경로")
                    path = folder / relative
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
                        "precision": "CPU FP32 평가 추론",
                        "preprocessing": "512×512 회색조를 3채널에 복제한 뒤 RGB 평균·표준편차로 정규화합니다.",
                        "normalization": "입력 CT의 회색조 표시" if stage == 0 else "각 패널의 최솟값·최댓값으로 개별 정규화",
                        "training_policy": {key: policy[key] for key in
                            ("optimizer", "batch_size", "initial_learning_rate", "weight_decay", "max_epochs", "patience", "min_delta")
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
        result["error"] = "특징 맵 목록 또는 이미지 무결성을 확인할 수 없습니다."
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


def read_status(root: Path):
    meta = {"observed_at": datetime.now(timezone.utc).isoformat(), "stale": True,
            "age_seconds": None, "process_alive": None, "read_error": None}
    try:
        path = root / "work" / "runtime" / "status.json"
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
        age = max(0, (datetime.now(timezone.utc) - stamp).total_seconds())
        meta.update(age_seconds=round(age, 1), stale=data.get("status") == "running" and age > 60,
                    process_alive=process_alive(data.get("pid")))
    except FileNotFoundError:
        data = {"stage": "ready", "status": "waiting", "message": "학습 상태가 아직 기록되지 않았습니다", "history": []}
        meta["read_error"] = "상태 파일 대기"
    except (OSError, ValueError, TypeError) as error:
        data = {"stage": "error", "status": "failed", "message": "상태 파일을 읽을 수 없습니다", "history": []}
        # 로컬 파일의 절대 경로와 의료 원문은 응답에 포함하지 않습니다.
        meta["read_error"] = "상태 파일 형식 또는 읽기 오류: " + type(error).__name__
    data["_dashboard"] = meta
    return data


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

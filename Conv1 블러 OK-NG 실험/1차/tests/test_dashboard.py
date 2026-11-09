"""대시보드의 상태 읽기 및 HTTP 경계를 검증합니다."""
import http.client
import ctypes
import json
import os
from pathlib import Path
import tempfile
import threading
import unittest
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest import mock

from dashboard import MAX_STATUS_BYTES, make_server, open_status_file, read_status
from src.state import atomic_json


class DashboardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "work" / "runtime").mkdir(parents=True)
        (self.root / "web").mkdir()
        (self.root / "web" / "index.html").write_text("실험 현황", encoding="utf-8")
        self.server = make_server(self.root, port=0, token="test-session-token")
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=3)
        self.temp.cleanup()

    def status(self, **changes):
        data = {"updated_at": datetime.now(timezone.utc).isoformat(), "pid": os.getpid(),
                "stage": "training", "status": "running", "history": [], "message": "학습 중"}
        data.update(changes)
        path = self.root / "work" / "runtime" / "status.json"
        path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        return path

    def get(self, path, authenticated=True, host=None):
        connection = http.client.HTTPConnection("127.0.0.1", self.server.server_port, timeout=3)
        headers = {"Host": host or f"127.0.0.1:{self.server.server_port}"}
        if authenticated:
            headers["Cookie"] = "dashboard_session=test-session-token"
        connection.request("GET", path, headers=headers)
        response = connection.getresponse()
        result = response.status, dict(response.getheaders()), response.read()
        connection.close()
        return result

    @unittest.skipUnless(os.name == "nt", "Windows 삭제 공유 핸들 검사")
    def test_open_reader_allows_replace_and_preserves_complete_versions(self):
        path = self.status(epoch=1)
        old = json.loads(path.read_text(encoding="utf-8"))
        new = dict(old, epoch=2, message="다음 학습 상태")
        with open_status_file(path) as old_reader:
            atomic_json(path, new)
            self.assertEqual(json.loads(old_reader.read().decode("utf-8")), old)
            with open_status_file(path) as new_reader:
                self.assertEqual(json.loads(new_reader.read().decode("utf-8")), new)
        self.assertEqual(read_status(self.root)["epoch"], 2)

    @unittest.skipUnless(os.name == "nt", "Windows 일시적 파일 부재 재시도 검사")
    def test_transient_missing_open_retries_then_reads_complete_json(self):
        path = self.status(epoch=7)
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel.CreateFileW.argtypes = [ctypes.c_wchar_p, ctypes.c_uint32, ctypes.c_uint32,
                                      ctypes.c_void_p, ctypes.c_uint32, ctypes.c_uint32,
                                      ctypes.c_void_p]
        kernel.CreateFileW.restype = ctypes.c_void_p
        attempts = []

        def controlled_open(*args):
            attempts.append(args)
            if len(attempts) <= 2:
                ctypes.set_last_error(2)
                return ctypes.c_void_p(-1).value
            return kernel.CreateFileW(*args)

        controlled_kernel = SimpleNamespace(CreateFileW=mock.Mock(side_effect=controlled_open),
                                            CloseHandle=kernel.CloseHandle)
        with mock.patch("dashboard.ctypes.WinDLL", return_value=controlled_kernel), \
                mock.patch("dashboard.time.sleep") as sleep:
            with open_status_file(path) as stream:
                self.assertEqual(json.loads(stream.read().decode("utf-8"))["epoch"], 7)
        self.assertEqual(len(attempts), 3)
        self.assertEqual(sleep.call_args_list, [mock.call(0.01), mock.call(0.02)])

    @unittest.skipUnless(os.name == "nt", "Windows 영구 파일 부재 한계 검사")
    def test_permanent_missing_open_raises_after_bounded_attempts(self):
        def missing_open(*_args):
            ctypes.set_last_error(3)
            return ctypes.c_void_p(-1).value

        controlled_open = mock.Mock(side_effect=missing_open)
        controlled_kernel = SimpleNamespace(CreateFileW=controlled_open, CloseHandle=mock.Mock())
        with mock.patch("dashboard.ctypes.WinDLL", return_value=controlled_kernel), \
                mock.patch("dashboard.time.sleep") as sleep:
            with self.assertRaises(FileNotFoundError) as raised:
                open_status_file(self.root / "missing.json")
        self.assertEqual(raised.exception.winerror, 3)
        self.assertEqual(controlled_open.call_count, 5)
        self.assertEqual(sleep.call_args_list,
                         [mock.call(0.01), mock.call(0.02), mock.call(0.04), mock.call(0.08)])
        controlled_kernel.CloseHandle.assert_not_called()

    @unittest.skipUnless(os.name == "nt", "Windows 일시적 공유 위반 재시도 검사")
    def test_transient_sharing_violation_retries_then_reads_complete_json(self):
        path = self.status(epoch=8)
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel.CreateFileW.argtypes = [ctypes.c_wchar_p, ctypes.c_uint32, ctypes.c_uint32,
                                      ctypes.c_void_p, ctypes.c_uint32, ctypes.c_uint32,
                                      ctypes.c_void_p]
        kernel.CreateFileW.restype = ctypes.c_void_p
        attempts = []

        def controlled_open(*args):
            attempts.append(args)
            if len(attempts) <= 2:
                ctypes.set_last_error(32)
                return ctypes.c_void_p(-1).value
            return kernel.CreateFileW(*args)

        controlled_kernel = SimpleNamespace(CreateFileW=mock.Mock(side_effect=controlled_open),
                                            CloseHandle=kernel.CloseHandle)
        with mock.patch("dashboard.ctypes.WinDLL", return_value=controlled_kernel), \
                mock.patch("dashboard.time.sleep") as sleep:
            with open_status_file(path) as stream:
                self.assertEqual(json.loads(stream.read().decode("utf-8"))["epoch"], 8)
        self.assertEqual(len(attempts), 3)
        self.assertEqual(sleep.call_args_list, [mock.call(0.01), mock.call(0.02)])

    @unittest.skipUnless(os.name == "nt", "Windows 영구 공유 위반 한계 검사")
    def test_permanent_sharing_violation_raises_after_bounded_attempts(self):
        def locked_open(*_args):
            ctypes.set_last_error(32)
            return ctypes.c_void_p(-1).value

        controlled_open = mock.Mock(side_effect=locked_open)
        controlled_kernel = SimpleNamespace(CreateFileW=controlled_open, CloseHandle=mock.Mock())
        with mock.patch("dashboard.ctypes.WinDLL", return_value=controlled_kernel), \
                mock.patch("dashboard.time.sleep") as sleep:
            with self.assertRaises(PermissionError) as raised:
                open_status_file(self.root / "locked.json")
        self.assertEqual(raised.exception.winerror, 32)
        self.assertEqual(controlled_open.call_count, 5)
        self.assertEqual(sleep.call_args_list,
                         [mock.call(0.01), mock.call(0.02), mock.call(0.04), mock.call(0.08)])
        controlled_kernel.CloseHandle.assert_not_called()

    def test_status_size_limit_remains_enforced(self):
        path = self.status()
        path.write_bytes(b" " * (MAX_STATUS_BYTES + 1))
        state = read_status(self.root)
        self.assertEqual(state["status"], "failed")
        self.assertIsNotNone(state["_dashboard"]["read_error"])

    def test_state_is_read_only_and_process_is_observed(self):
        path = self.status(epoch=2, seen_per_class={"OK": 5000, "NG": 5000})
        before = path.read_bytes()
        code, headers, body = self.get("/api/status")
        data = json.loads(body)
        self.assertEqual(code, 200)
        self.assertEqual(data["epoch"], 2)
        self.assertEqual(data["seen_per_class"], {"OK": 5000, "NG": 5000})
        self.assertFalse(data["_dashboard"]["stale"])
        self.assertTrue(data["_dashboard"]["process_alive"])
        self.assertEqual(path.read_bytes(), before)
        self.assertNotIn("Access-Control-Allow-Origin", headers)
        self.assertEqual(headers["Cache-Control"], "no-store")

    def test_missing_and_malformed_status_are_explicit(self):
        state = read_status(self.root)
        self.assertEqual(state["history"], [])
        self.assertEqual(state["_dashboard"]["read_error"], "상태 파일 대기")
        path = self.root / "work" / "runtime" / "status.json"
        path.write_text('{"private":"D:/medical/', encoding="utf-8")
        code, _, body = self.get("/api/status")
        self.assertEqual(code, 200)
        self.assertEqual(json.loads(body)["status"], "failed")
        self.assertNotIn(b"medical", body)

    def test_nonfinite_status_is_reported_as_read_error(self):
        path = self.status()
        path.write_text('{"updated_at":"2026-11-10T00:00:00+09:00","loss":NaN}', encoding="utf-8")
        code, _, body = self.get("/api/status")
        self.assertEqual(code, 200)
        self.assertEqual(json.loads(body)["status"], "failed")

    def test_stale_and_dead_process_are_observable(self):
        self.status(updated_at=(datetime.now(timezone.utc)-timedelta(minutes=3)).isoformat(), pid=2147483647)
        state = read_status(self.root)
        self.assertTrue(state["_dashboard"]["stale"])
        self.assertGreaterEqual(state["_dashboard"]["age_seconds"], 179)
        self.assertFalse(state["_dashboard"]["process_alive"])

    def test_token_redirect_then_cookie_and_no_token_echo(self):
        code, headers, body = self.get("/?token=test-session-token", authenticated=False)
        self.assertEqual(code, 303)
        self.assertEqual(headers["Location"], "/")
        self.assertIn("HttpOnly", headers["Set-Cookie"])
        self.assertIn("SameSite=Strict", headers["Set-Cookie"])
        self.assertEqual(body, b"")
        self.assertEqual(self.get("/", authenticated=False)[0], 401)
        self.assertEqual(self.get("/?token=wrong", authenticated=False)[0], 401)
        self.assertEqual(self.get("/")[0], 200)

    def test_unlisted_and_traversal_paths_never_expose_files(self):
        secret = self.root / "private.json"
        secret.write_text("private-secret", encoding="utf-8")
        for route in ("/../private.json", "/%2e%2e/private.json", "/work/runtime/status.json", "/private.json", "/api/status?file=private.json", "/web/index.html"):
            with self.subTest(route=route):
                code, _, body = self.get(route)
                self.assertEqual(code, 404)
                self.assertNotIn(b"private-secret", body)

    def test_invalid_host_and_write_method_are_rejected(self):
        self.assertEqual(self.get("/api/status", host="example.com")[0], 403)
        connection = http.client.HTTPConnection("127.0.0.1", self.server.server_port, timeout=3)
        connection.request("POST", "/api/status", body=b"{}", headers={"Cookie": "dashboard_session=test-session-token"})
        response = connection.getresponse()
        self.assertEqual(response.status, 501)
        response.read()
        connection.close()

    def test_status_requires_timezone_and_object(self):
        self.status(updated_at="2026-11-10T01:00:00")
        self.assertEqual(read_status(self.root)["status"], "failed")
        (self.root / "work" / "runtime" / "status.json").write_text("[]", encoding="utf-8")
        self.assertEqual(read_status(self.root)["status"], "failed")


if __name__ == "__main__":
    unittest.main()

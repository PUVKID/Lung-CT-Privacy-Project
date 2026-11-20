"""대시보드의 상태 읽기 및 HTTP 경계를 검증합니다."""
import hashlib
import http.client
import ctypes
import copy
import io
import json
import os
import shutil
import subprocess
from pathlib import Path
import tempfile
import threading
import unittest
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest import mock

from dashboard import MAX_STATUS_BYTES, make_server, open_status_file, read_status, sigma_results, feature_previews, feature_preview_path, SIGMA_VALUES
from src.state import atomic_json


class DashboardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "experiment"
        self.root.mkdir()
        (self.root / "work" / "runtime").mkdir(parents=True)
        (self.root / "web").mkdir()
        (self.root / "web" / "index.html").write_text("실험 현황", encoding="utf-8")
        self.server = make_server(self.root, port=0, token="test-session-token")
        self.thread = threading.Thread(target=lambda: self.server.serve_forever(poll_interval=0.01), daemon=True)
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

    def test_deliberately_idle_states_are_not_stale(self):
        old_stamp = (datetime.now(timezone.utc) - timedelta(minutes=3)).isoformat()
        for status in ("ready", "interrupted", "completed"):
            with self.subTest(status=status):
                self.status(updated_at=old_stamp, stage=status, status=status, pid=None)
                state = read_status(self.root)
                self.assertGreaterEqual(state["_dashboard"]["age_seconds"], 179)
                self.assertFalse(state["_dashboard"]["stale"])
                self.assertIsNone(state["_dashboard"]["read_error"])

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


    def fixed_fixture(self, sigma=0, completed=True):
        # CT나 실제 모델을 읽지 않는 합성 자료입니다. 저장 경계와 SHA만 실제 파일로 검사합니다.
        from src.identity import _run_identity, PROTOCOL
        (self.root / "src").mkdir(exist_ok=True)
        (self.root / "tools").mkdir(exist_ok=True)
        for relative in ("run_training.py", "src/model.py", "src/data.py", "tools/feature_generator.py"):
            (self.root / relative).write_text("# 합성 검사 자료\n", encoding="utf-8")
        reference = self.root / "work/reference.json"
        records = [{"id": "synthetic", "source_class": "Normal cases"}]
        digest = hashlib.sha256(json.dumps(records, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
        manifest = {"records": records, "splits": {"train": records, "validation": [], "test": []}, "manifest_sha256": digest}
        reference.write_text(json.dumps(manifest), encoding="utf-8")
        config = {"protocol": PROTOCOL, "protocol_fixed_model": True, "training_sigma": 0,
                  "sigmas": list(SIGMA_VALUES), "epochs": 100, "early_stopping_enabled": False,
                  "image_size": 512, "batch_size": 8, "samples_per_class": 5000, "seed": 42, "precision": "bf16",
                  "expected_reference_manifest": "work/reference.json",
                  "expected_reference_manifest_sha256": hashlib.sha256(reference.read_bytes()).hexdigest(),
                  "expected_reference_records_sha256": digest}
        (self.root / "config.json").write_text(json.dumps(config), encoding="utf-8")
        results = self.root / "work/results"
        results.mkdir(exist_ok=True)
        (results / "dataset_manifest_private.json").write_text(json.dumps(manifest), encoding="utf-8")
        run_id, settings = _run_identity(self.root, config, digest)
        self.run_id = run_id
        folder = results / f"run_{run_id}"
        folder.mkdir(exist_ok=True)
        (folder / "run_metadata.json").write_text(json.dumps(dict(settings, run_id=run_id, protocol=PROTOCOL, protocol_fixed_model=True, training_sigma=0)), encoding="utf-8")
        checkpoint = self.root / f"work/checkpoints/run_{run_id}/sigma_0_best.pt"
        checkpoint.parent.mkdir(parents=True, exist_ok=True)
        checkpoint.write_bytes(b"synthetic-selected-checkpoint")
        selection = {"run_id": run_id, "protocol": PROTOCOL, "protocol_fixed_model": True, "training_sigma": 0,
                     "best_epoch": 2, "checkpoint_epoch": 2, "epochs_ran": 100,
                     "checkpoint_sha256": hashlib.sha256(checkpoint.read_bytes()).hexdigest(), "model_state_sha256": "a"*64,
                     "selected_checkpoint": checkpoint.relative_to(self.root).as_posix()}
        (folder / "fixed_model_selection.json").write_text(json.dumps(selection), encoding="utf-8")
        history = [{"sigma": 0, "epoch": epoch, "train_loss": 0, "val_loss": 1/epoch,
                    "val_accuracy": 1, "val_auc": None, "learning_rate": 0, "next_learning_rate": 0,
                    "optimizer_steps": epoch*1250, "early_stopping_wait": 0} for epoch in range(1,101)]
        (folder / "sigma_0_history.json").write_text(json.dumps(history), encoding="utf-8")
        metrics = dict(selection, sigma=sigma, evaluation_sigma=sigma, eval_optimizer_steps=0, optimizer_steps=125000,
                       completed_at="2026-11-20T01:00:00+09:00", validation={"accuracy": 1, "auc": None, "loss": 0, "n_images": 4},
                       test={"accuracy": 0.75, "auc": 0.8, "loss": 0, "n_images": 4, "confusion_matrix": [[2,0],[1,1]]}, prediction_files={})
        for split in ("validation", "test"):
            relative = f"work/results/run_{run_id}/sigma_{sigma}_{split}_predictions_private.csv"
            target = self.root / relative
            target.write_text("id,label,prediction\nsynthetic,0,0\n", encoding="utf-8")
            metrics["prediction_files"][split] = {"relative_path": relative, "sha256": hashlib.sha256(target.read_bytes()).hexdigest()}
        (folder / f"sigma_{sigma}_metrics.json").write_text(json.dumps(metrics), encoding="utf-8")
        self.status(run_id=run_id, schema_version=2, protocol=PROTOCOL, protocol_fixed_model=True, training_sigma=0,
                    training_status="completed" if completed else "running", epoch=100 if completed else 47, epochs=100,
                    checkpoint_sha256=selection["checkpoint_sha256"] if completed else None,
                    model_state_sha256=selection["model_state_sha256"] if completed else None, best_epoch=2,
                    history=history if completed else history[:47],
                    sigma_queue=[{"sigma": n, "status": "completed" if completed and n==sigma else "pending"} for n in SIGMA_VALUES])
        return folder, metrics

    def test_training_keeps_all_evaluations_pending_even_when_old_metrics_exist(self):
        self.fixed_fixture(completed=False)
        for sigma in SIGMA_VALUES:
            result = sigma_results(self.root, sigma)
            self.assertEqual(result["status"], "pending")
            self.assertIsNone(result["metrics"])
            self.assertEqual(result["evaluation_history"], [])
            self.assertEqual(len(result["history"]), 47 if sigma == 0 else 0)

    def test_all_ten_evaluations_share_one_checkpoint_and_no_extra_steps(self):
        hashes = set()
        for sigma in SIGMA_VALUES:
            self.fixed_fixture(sigma)
            code, _, body = self.get(f"/api/sigma-results/{sigma}")
            self.assertEqual(code, 200)
            result = json.loads(body)
            self.assertEqual(result["status"], "completed", result)
            self.assertEqual(result["metrics"]["eval_optimizer_steps"], 0)
            self.assertEqual(result["metrics"]["test"]["correct_count"], 3)
            self.assertEqual(result["metrics"]["test"]["accuracy"], 0.75)
            self.assertEqual(len(result["history"]), 100 if sigma == 0 else 0)
            self.assertEqual(result["evaluation_history"][0]["sigma"], sigma)
            hashes.add(result["metrics"]["checkpoint_sha256"])
            self.assertNotIn("selected_checkpoint", body.decode())
            self.assertNotIn("synthetic", body.decode())
        self.assertEqual(len(hashes), 1)
        self.assertEqual(self.get("/api/sigma-results/0", authenticated=False)[0], 401)
        self.assertEqual(self.get("/api/sigma-results/0", host="example.com")[0], 403)
        for suffix in ("-1", "3", "00", "0?file=private.json", "../status", "%30"):
            self.assertEqual(self.get("/api/sigma-results/"+suffix)[0], 400)

    def test_wrong_model_run_source_prediction_or_training_contract_is_rejected(self):
        folder, original = self.fixed_fixture(8)
        path = folder / "sigma_8_metrics.json"
        for changes in ({"training_sigma": 8}, {"eval_optimizer_steps": 1}, {"checkpoint_sha256": "b"*64},
                        {"model_state_sha256": "b"*64}, {"best_epoch": 3}, {"epochs_ran": 99},
                        {"run_id": "f"*16}, {"sigma": 0}, {"evaluation_sigma": 4}, {"protocol_fixed_model": False}):
            with self.subTest(changes=changes):
                path.write_text(json.dumps(dict(original, **changes)), encoding="utf-8")
                self.assertIsNone(sigma_results(self.root, 8)["metrics"])
        path.write_text(json.dumps(original), encoding="utf-8")
        prediction = self.root / original["prediction_files"]["test"]["relative_path"]
        prediction.write_text("changed", encoding="utf-8")
        self.assertIsNone(sigma_results(self.root, 8)["metrics"])
        self.fixed_fixture(8)
        (self.root / "src/model.py").write_text("# 변경된 소스\n", encoding="utf-8")
        self.assertEqual(read_status(self.root)["status"], "failed")
        self.assertIsNone(sigma_results(self.root, 8)["metrics"])

    def test_selected_checkpoint_bytes_and_missing_selection_fail_closed(self):
        folder, metrics = self.fixed_fixture()
        (self.root / metrics["selected_checkpoint"]).write_bytes(b"changed")
        self.assertIsNone(sigma_results(self.root, 0)["metrics"])
        self.fixed_fixture()
        (folder / "fixed_model_selection.json").unlink()
        self.assertIsNone(sigma_results(self.root, 0)["metrics"])

    def test_numeric_results_are_strict_and_preserve_zero_and_undefined_auc(self):
        folder, original = self.fixed_fixture()
        path = folder / "sigma_0_metrics.json"
        for field in ("accuracy", "loss", "auc", "n_images"):
            for value in ({"private_path": "D:/medical/secret"}, [], "secret", True, float("nan"), float("inf"), -1):
                changed = copy.deepcopy(original)
                changed["test"][field] = value
                path.write_text(json.dumps(changed), encoding="utf-8")
                result = sigma_results(self.root, 0)
                self.assertIsNone(result["metrics"], (field, value))
                self.assertNotIn("secret", json.dumps(result))
        changed = copy.deepcopy(original)
        changed["test"].update(accuracy=0, auc=None, loss=0, confusion_matrix=[[0,2],[2,0]])
        path.write_text(json.dumps(changed), encoding="utf-8")
        result = sigma_results(self.root, 0)
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["metrics"]["test"]["accuracy"], 0)
        self.assertEqual(result["metrics"]["test"]["loss"], 0)
        self.assertIsNone(result["metrics"]["test"]["auc"])
        changed["test"]["accuracy"] = 0.75
        path.write_text(json.dumps(changed), encoding="utf-8")
        self.assertIsNone(sigma_results(self.root, 0)["metrics"])

    def test_history_never_relabels_sigma0_as_another_training_curve(self):
        folder, _ = self.fixed_fixture()
        path = folder / "sigma_0_history.json"
        rows = json.loads(path.read_text(encoding="utf-8"))
        for bad in ([], rows[:99], rows[::-1], [dict(rows[0], sigma=8)]+rows[1:], [dict(rows[0], train_loss=-1)]+rows[1:]):
            path.write_text(json.dumps(bad), encoding="utf-8")
            self.assertIsNone(sigma_results(self.root, 0)["metrics"])
        self.fixed_fixture(8)
        (folder / "sigma_0_history.json").write_text("invalid", encoding="utf-8")
        result = sigma_results(self.root, 8)
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["history"], [])

    def test_result_symlink_and_status_private_fields_do_not_escape(self):
        folder, _ = self.fixed_fixture()
        path = folder / "sigma_0_metrics.json"
        original = Path.is_symlink
        with mock.patch.object(Path, "is_symlink", lambda target: target == path or original(target)):
            self.assertIsNone(sigma_results(self.root, 0)["metrics"])
        self.status(private_path="D:/medical/secret", device={"name": "CPU", "source_path": "D:/secret"},
                    dataset={"splits": {}, "records": [{"private": "secret"}]})
        _, _, body = self.get("/api/status")
        self.assertNotIn(b"secret", body)
        self.assertNotIn(b"private_path", body)

    def test_feature_previews_wait_until_single_training_is_complete(self):
        self.fixed_fixture(completed=False)
        result = feature_previews(self.root)
        self.assertEqual(result["items"], [])
        self.assertEqual(result["pending"], list(SIGMA_VALUES))


    def test_damaged_manifest_returns_explicit_status_error_without_exception(self):
        self.fixed_fixture()
        path = self.root / "work/results/dataset_manifest_private.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        del manifest["splits"]
        path.write_text(json.dumps(manifest), encoding="utf-8")
        code, _, body = self.get("/api/status")
        self.assertEqual(code, 200)
        result = json.loads(body)
        self.assertEqual(result["status"], "failed")
        self.assertIn("KeyError", result["_dashboard"]["read_error"])
        self.assertEqual(result["history"], [])

    def test_status_completed_identity_matches_selected_file_and_epoch(self):
        self.fixed_fixture()
        path = self.root / "work/runtime/status.json"
        original = json.loads(path.read_text(encoding="utf-8"))
        for change in ({"checkpoint_sha256": "f"*64}, {"model_state_sha256": "f"*64}, {"best_epoch": 3}, {"epoch": 99}):
            path.write_text(json.dumps(dict(original, **change)), encoding="utf-8")
            self.assertEqual(read_status(self.root)["status"], "failed", change)

    def test_feature_180_bundle_identity_hash_and_current_source(self):
        import base64
        from src.identity import file_sha256
        for sigma in SIGMA_VALUES:
            folder, metrics = self.fixed_fixture(sigma)
        self.status(run_id=self.run_id, protocol="fixed-model-sigma0-v1", protocol_fixed_model=True,
                    training_sigma=0, training_status="completed", epoch=100,
                    checkpoint_sha256=metrics["checkpoint_sha256"], model_state_sha256=metrics["model_state_sha256"], best_epoch=2,
                    sigma_queue=[{"sigma": n, "status": "completed"} for n in SIGMA_VALUES])
        target = self.root.parent / "블러 강도별 대표 특징맵/7차"
        target.mkdir(parents=True)
        selection = json.loads((folder / "fixed_model_selection.json").read_text(encoding="utf-8"))
        keys = ("protocol", "protocol_fixed_model", "training_sigma", "checkpoint_sha256", "model_state_sha256", "checkpoint_epoch", "selected_checkpoint")
        identity = {key: selection[key] for key in keys}
        index = dict(identity, schema_version=2, run_id=self.run_id, completed_sigmas=list(SIGMA_VALUES), items=[],
                     source_manifest_sha256=file_sha256(self.root / "work/results/dataset_manifest_private.json"),
                     manifest_records_sha256=json.loads((folder / "run_metadata.json").read_text(encoding="utf-8"))["manifest_sha256"],
                     model_source_sha256=file_sha256(self.root / "src/model.py"), data_source_sha256=file_sha256(self.root / "src/data.py"),
                     generator_sha256=file_sha256(self.root / "tools/feature_generator.py"))
        png = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jRZkAAAAASUVORK5CYII=")
        for sigma in SIGMA_VALUES:
            for class_key in ("Bengin_cases", "Malignant_cases", "Normal_cases"):
                for stage in range(6):
                    relative = feature_preview_path(sigma, class_key, stage)
                    image = target / relative
                    image.parent.mkdir(parents=True, exist_ok=True)
                    image.write_bytes(png)
                    index["items"].append(dict(identity, run_id=self.run_id, id=f"{sigma}-{class_key}-{stage}", relative_path=relative.as_posix(),
                                               sha256=hashlib.sha256(png).hexdigest(), width=1, height=1))
        path = target / "export_index_private.json"
        path.write_text(json.dumps(index), encoding="utf-8")
        result = feature_previews(self.root)
        self.assertEqual(len(result["items"]), 180, result.get("error"))
        self.assertEqual(result["pending"], [])
        code, _, body = self.get("/api/feature-previews/image/8-Normal_cases-4")
        self.assertEqual(code, 200)
        self.assertEqual(body, png)
        for key in ("checkpoint_sha256", "model_source_sha256", "data_source_sha256", "source_manifest_sha256", "manifest_records_sha256", "generator_sha256"):
            changed = dict(index, **{key: "f"*64})
            path.write_text(json.dumps(changed), encoding="utf-8")
            result = feature_previews(self.root)
            self.assertEqual(result["items"], [], key)
            self.assertIn("error", result)
        index["items"][0]["run_id"] = "f"*16
        path.write_text(json.dumps(index), encoding="utf-8")
        self.assertEqual(feature_previews(self.root)["items"], [])
        index["items"][0]["run_id"] = self.run_id
        index["items"][0]["checkpoint_sha256"] = "f"*64
        path.write_text(json.dumps(index), encoding="utf-8")
        self.assertEqual(feature_previews(self.root)["items"], [])

    def test_javascript_syntax_and_real_ui_state_selection(self):
        node = shutil.which("node")
        self.assertIsNotNone(node, "Node.js 실행 파일이 필요합니다")
        root = Path(__file__).resolve().parents[1]
        for name in ("app.js", "scene.js", "theme.js"):
            checked = subprocess.run([node, "--check", "--input-type=module"], input=(root / "web" / name).read_text(encoding="utf-8"),
                                     text=True, encoding="utf-8", capture_output=True, timeout=10)
            self.assertEqual(checked.returncode, 0, checked.stderr)
        script = r"""
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
(async()=>{
const html=fs.readFileSync('web/index.html','utf8');
const ids=[...html.matchAll(/id="([^"]+)"/g)].map(x=>x[1]);
const plot=[];const context={scale(){},beginPath(){},moveTo(){},lineTo(){},stroke(){},fillText(){},arc(...v){plot.push(v);},fill(){}};
function element(){return {textContent:'',children:[],dataset:{},attributes:{},querySelector(selector){if(selector==='small')return this.children[1];return this.children.find(x=>String(x.dataset.sigma)===selector.match(/"(\d+)"/)?.[1]);},parentElement:{},addEventListener(){},setAttribute(k,v){this.attributes[k]=v;},replaceChildren(...v){this.children=v;},append(...v){this.children.push(...v);},getBoundingClientRect(){return {width:600,height:210};},getContext(){return context;}};}
const nodes=Object.fromEntries(ids.map(id=>[id,element()])),selected=[];
let fetchCount=0;
const sandbox={console,AbortController,setTimeout,clearTimeout,fetch:async url=>{fetchCount++;const sigma=Number(url.split('/').at(-1));return {ok:true,json:async()=>({run_id:state.run_id,sigma,history:sigma===0?state.history:[],evaluation_history:[{sigma,validation_loss:0,test_loss:0.25,validation_accuracy:1,test_accuracy:sigma===8?0.5:0.9878048780487805}],metrics:{training_sigma:0,best_epoch:2,epochs_ran:100,eval_optimizer_steps:0,checkpoint_sha256:'a'.repeat(64),test:{accuracy:sigma===8?0.5:0.9878048780487805,auc:0,loss:0,correct_count:162,n_images:164}}})};},
createPipeline(){return {setSelectedSigma(...v){selected.push(v);},setStatus(){},setPaused(){},setTheme(){}};},document:{getElementById(id){return nodes[id]||null;},createElement:element,querySelectorAll(){return [];},fonts:{ready:Promise.resolve()}},window:{matchMedia(){return {matches:false,addEventListener(){}};},addEventListener(){},ctTheme:{current(){return 'light';}},devicePixelRatio:1},setInterval(){}};
let code=fs.readFileSync('web/app.js','utf8').replace(/^import[^\n]*\n/,'').replace('await document.fonts.ready;','').replace('refresh();setInterval(refresh,3000);','');
vm.runInNewContext(code+'\nglobalThis.testAPI={render,selectSigma,percent};',sandbox);
const state={run_id:'0123456789abcdef',stage:'training',status:'running',training_status:'running',training_sigma:0,sigma:0,epoch:47,epochs:100,training_policy:{max_epochs:100,early_stopping_enabled:false},learning_rate:0,best_epoch:2,optimizer_steps:58750,history:[{sigma:0,epoch:1,train_loss:0,val_loss:1e-16,val_accuracy:1}],sigma_queue:[{sigma:0,status:'completed'}],_dashboard:{stale:false,process_alive:true},updated_at:'2026-11-20T00:00:00+09:00'};
const tick=()=>new Promise(resolve=>setImmediate(resolve));
sandbox.testAPI.render(state);await tick();
assert.equal(nodes.testAccuracy.textContent,'미측정');assert.equal(nodes.queueCount.textContent,'0 / 10 평가 완료');
assert.match(nodes.sigmaLabel.textContent,/한 번의 학습/);assert.match(nodes.latestLoss.textContent,/학습 손실 0/);
sandbox.testAPI.selectSigma(8);await tick();assert.equal(nodes.testAccuracy.textContent,'미측정');assert.equal(nodes.latestLoss.textContent,'최근 손실 미측정');assert.equal(nodes.chartTitle.textContent,'선택 강도의 고정 모델 평가');
state.training_status='completed';state.stage='testing';state.checkpoint_sha256='a'.repeat(64);state.evaluation_current_sigma=8;
sandbox.testAPI.render(state);await tick();assert.equal(nodes.testAccuracy.textContent,'50.0%');assert.equal(nodes.selectedSteps.textContent,'0');assert.equal(nodes.selectedCheckpoint.textContent,'a'.repeat(64));assert.match(nodes.latestLoss.textContent,/시험 손실 0.25/);assert.equal(selected.at(-1)[0],8);
sandbox.testAPI.selectSigma(0);await tick();assert.equal(nodes.testAccuracy.textContent,'98.8%');assert.equal(nodes.testAccuracyRaw.textContent,'0.9878048780487805');assert.equal(nodes.testAuc.textContent,'0');assert.match(nodes.testCorrectCount.textContent,/162 \/ 164/);assert.match(nodes.chartTitle.textContent,/블러 0/);
assert.equal(sandbox.testAPI.percent(0),'0.0%');assert.equal(sandbox.testAPI.percent(1),'100.0%');assert.equal(sandbox.testAPI.percent(0.99999),'100.0%');
state.run_id='fedcba9876543210';sandbox.testAPI.render(state);assert.equal(nodes.testAccuracy.textContent,'미측정');assert.equal(nodes.selectedCheckpoint.textContent,'고정 모델 평가 대기');
state.status='interrupted';state.stage='interrupted';sandbox.testAPI.render(state);assert.equal(nodes.motion.disabled,true);assert.equal(nodes.badge.textContent,'중단');
console.log('강도 선택·학습 중 대기·추가 갱신0·동일 모델·원값/반올림·실행 전환·중단 상태 통과');
})().catch(error=>{console.error(error);process.exitCode=1;});
"""
        checked = subprocess.run([node, "-"], input=script, text=True, encoding="utf-8", capture_output=True, timeout=20, cwd=root)
        self.assertEqual(checked.returncode, 0, checked.stdout+checked.stderr)


if __name__ == "__main__":
    unittest.main()

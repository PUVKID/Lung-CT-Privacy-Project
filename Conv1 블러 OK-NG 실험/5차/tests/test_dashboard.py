"""대시보드의 상태 읽기 및 HTTP 경계를 검증합니다."""
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

from dashboard import MAX_STATUS_BYTES, make_server, open_status_file, read_status, sigma_results, SIGMA_VALUES
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

    @unittest.skipUnless(shutil.which("node"), "화면 상태 검사에 Node.js가 필요합니다")
    def test_ui_policy_zero_missing_interrupted_and_zero_loss(self):
        script = r"""
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
(async()=>{
const html=fs.readFileSync('web/index.html','utf8');
const ids=[...html.matchAll(/id="([^"]+)"/g)].map(x=>x[1]);
const plot=[];
const context={scale(){},beginPath(){},moveTo(){},lineTo(){},stroke(){},fillText(){},arc(...args){plot.push(args);},fill(){}};
function element(){return {textContent:'',className:'',children:[],dataset:{},attributes:{},querySelector(selector){if(selector==='small')return this.children[1];return this.children.find(x=>String(x.dataset.sigma)===selector.match(/"(\d+)"/)?.[1]);},parentElement:{},addEventListener(){},setAttribute(k,v){this.attributes[k]=v;},replaceChildren(){this.children=[];},append(...items){this.children.push(...items);},getBoundingClientRect(){return {width:600,height:210};},getContext(){return context;}};}
const nodes=Object.fromEntries(ids.map(id=>[id,element()]));
const motion=[];
const pipeline={setSelectedSigma(){},setStatus(...args){motion.push(args);},setPaused(){},setTheme(){}};
const sandbox={console,AbortController,setTimeout,clearTimeout,fetch:async()=>({ok:true,json:async()=>({run_id:state.run_id,sigma:state.sigma,history:state.history,metrics:{best_epoch:2,epochs_ran:3,test:{accuracy:1,auc:1}}})}),createPipeline(){return pipeline;},document:{getElementById(id){return nodes[id];},createElement:element,querySelectorAll(){return [];},querySelector(){return null;},fonts:{ready:Promise.resolve()}},window:{matchMedia(){return {matches:false,addEventListener(){}};},addEventListener(){},ctTheme:{current(){return 'light';}},devicePixelRatio:1},setInterval(){}};
let code=fs.readFileSync('web/app.js','utf8').replace(/^import[^\n]*\n/,'').replace('await document.fonts.ready;','').replace('refresh();setInterval(refresh,3000);','');
vm.runInNewContext(code+'\nglobalThis.testAPI={render};',sandbox);
const state={run_id:'0123456789abcdef',stage:'training',status:'running',sigma:0,epoch:0,epochs:35,training_policy:{max_epochs:20,patience:7},learning_rate:0,early_stopping_wait:0,best_epoch:0,optimizer_steps:0,history:[{sigma:0,epoch:1,train_loss:0,val_loss:1e-16,val_accuracy:1}],_dashboard:{stale:false,process_alive:true},updated_at:'2026-11-10T00:00:00+09:00'};
const original=JSON.stringify(state.history);
sandbox.testAPI.render(state);
await new Promise(resolve=>setImmediate(resolve));
assert.match(html,/<title>폐 CT 특징 블러 실험 · 4차<\/title>/);
assert.equal(nodes.epoch.textContent,'0회 / 최대 20회');
assert.equal(nodes.learningRate.textContent,'0');
assert.equal(nodes.earlyStopping.textContent,'0 / 7회');
assert.equal(nodes.bestEpoch.textContent,'0회');
assert.equal(nodes.optimizerSteps.textContent,'0');
assert.match(nodes.latestLoss.textContent,/학습 손실 0 · 검증 손실 1e-16/);
assert.equal(JSON.stringify(state.history),original);
assert.ok(plot.some(point=>point[1]===180));
sandbox.testAPI.render({...state,learning_rate:null,early_stopping_wait:null,best_epoch:null,optimizer_steps:null,training_policy:{}});
assert.equal(nodes.learningRate.textContent,'미측정');
assert.equal(nodes.earlyStopping.textContent,'미측정');
assert.equal(nodes.bestEpoch.textContent,'미측정');
assert.equal(nodes.optimizerSteps.textContent,'미측정');
assert.equal(nodes.epoch.textContent,'0회 / 최대 35회');
sandbox.testAPI.render({...state,early_stopping_wait:0,training_policy:{max_epochs:100,patience:15}});
assert.equal(nodes.earlyStopping.textContent,'0 / 15회');
sandbox.testAPI.render({...state,training_policy:{max_epochs:100,patience:15,early_stopping_enabled:false}});
assert.equal(nodes.earlyStopping.textContent,'조기 종료 끔 · 강도마다 100회');
assert.equal(nodes.epoch.textContent,'0회 / 목표 100회');
assert.match(nodes.trainingPolicyNote.textContent,/조기 종료를 끄고/);
sandbox.testAPI.render({...state,stage:'interrupted',status:'interrupted'});
assert.equal(nodes.currentTitle.textContent,'학습을 중단했습니다');
assert.equal(nodes.badge.textContent,'중단');
assert.equal(nodes.motion.disabled,true);
assert.equal(nodes.motion.attributes['aria-pressed'],'true');
assert.equal(motion.at(-1)[2],false);
assert.match(nodes.alert.textContent,/중단/);
assert.equal(nodes.step0.textContent,'중단');
assert.equal(nodes.testAccuracy.textContent,'100.0%');
assert.equal(nodes.testAuc.textContent,'1');
sandbox.testAPI.render({...state,run_id:'fedcba9876543210',sigma:256});
assert.equal(nodes.testAccuracy.textContent,'미측정');
assert.equal(nodes.testAuc.textContent,'미측정');
assert.equal(nodes.latestLoss.textContent,'최근 손실 미측정');
assert.match(nodes.selectionNote.textContent,/새 실험/);
await new Promise(resolve=>setImmediate(resolve));
assert.equal(nodes.testAccuracy.textContent,'미측정');
assert.equal(nodes.testAuc.textContent,'미측정');
assert.equal(nodes.latestLoss.textContent,'최근 손실 미측정');
console.log('화면 상태 0/미측정/상한/중단/선형0손실 및 새 실행 응답 전 잔상 제거 검증 통과');
})().catch(error=>{console.error(error);process.exitCode=1;});
"""
        result = subprocess.run([shutil.which("node"), "-"], input=script, text=True,
                                encoding="utf-8", capture_output=True, timeout=20,
                                cwd=Path(__file__).resolve().parents[1])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

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

    def result_fixture(self, sigma=0):
        run_id = "0123456789abcdef"
        self.status(run_id=run_id, sigma_queue=[{"sigma": n, "status": "completed"} for n in SIGMA_VALUES])
        folder = self.root / "work" / "results" / f"run_{run_id}"
        folder.mkdir(parents=True, exist_ok=True)
        metrics = {"run_id": run_id, "sigma": sigma, "best_epoch": 2, "epochs_ran": 3,
                   "optimizer_steps": 30, "completed_at": "2026-11-10T01:00:00+09:00",
                   "test": {"accuracy": 1-sigma/512, "auc": 1-sigma/1024, "loss": 0, "n_images": 164},
                   "source_path": "PRIVATE", "hash": "PRIVATE"}
        (folder / f"sigma_{sigma}_metrics.json").write_text(json.dumps(metrics), encoding="utf-8")
        (folder / f"sigma_{sigma}_history.json").write_text(json.dumps([
            {"sigma": sigma, "epoch": epoch, "train_loss": 0, "val_loss": 0, "val_accuracy": 1,
             "val_auc": 1, "learning_rate": 0, "next_learning_rate": 0, "optimizer_steps": 10*epoch,
             "early_stopping_wait": 0, "source_path": "PRIVATE"} for epoch in (1, 2, 3)]), encoding="utf-8")
        return folder, metrics

    def test_all_sigma_results_and_endpoint_auth(self):
        for sigma in SIGMA_VALUES:
            self.result_fixture(sigma)
            result = sigma_results(self.root, sigma)
            self.assertEqual(result["sigma"], sigma)
            self.assertEqual(result["status"], "completed")
            self.assertEqual(result["history"][0]["sigma"], sigma)
            self.assertEqual(result["history"][0]["train_loss"], 0)
            self.assertEqual(result["metrics"]["test"]["accuracy"], 1-sigma/512)
            self.assertNotIn("PRIVATE", json.dumps(result))
        self.assertEqual(self.get("/api/sigma-results/0", authenticated=False)[0], 401)
        self.assertEqual(self.get("/api/sigma-results/0", host="example.com")[0], 403)
        for suffix in ("-1", "3", "00", "0?file=private.json", "../status", "%30"):
            self.assertEqual(self.get("/api/sigma-results/"+suffix)[0], 400)
        code, _, payload = self.get("/api/sigma-results/256")
        self.assertEqual(code, 200)
        self.assertEqual(json.loads(payload)["sigma"], 256)

    def test_result_missing_wrong_run_nonfinite_and_history_sigma_fail_closed(self):
        folder, metrics = self.result_fixture()
        path = folder / "sigma_0_metrics.json"
        original = path.read_bytes()
        for change in ({"run_id": "fedcba9876543210"}, {"sigma": 1}, {"test": {"auc": float("nan")}}):
            path.write_text(json.dumps(dict(metrics, **change)), encoding="utf-8")
            result = sigma_results(self.root, 0)
            self.assertEqual(result["history"], [])
            self.assertIsNone(result["metrics"])
            self.assertEqual(result["status"], "unavailable")
        path.write_bytes(original)
        (folder / "sigma_0_history.json").write_text('[{"sigma":1}]', encoding="utf-8")
        self.assertIsNone(sigma_results(self.root, 0)["metrics"])
        path.unlink()
        self.assertEqual(sigma_results(self.root, 0)["history"], [])
        self.assertIsNone(sigma_results(self.root, 3)["metrics"])
        self.assertIsNone(sigma_results(self.root, True)["metrics"])

    def test_pending_result_does_not_reuse_last_test_metrics(self):
        self.status(run_id="0123456789abcdef", sigma=256,
                    sigma_queue=[{"sigma": 0, "status": "pending"}],
                    history=[{"sigma": 256, "epoch": 1}], evaluation={"test": {"auc": 1}})
        result = sigma_results(self.root, 0)
        self.assertEqual(result["status"], "pending")
        self.assertEqual(result["history"], [])
        self.assertIsNone(result["metrics"])

    def test_result_symlink_escape_is_rejected(self):
        folder, _ = self.result_fixture()
        path = folder / "sigma_0_metrics.json"
        path.unlink()
        outside = self.root / "outside.json"
        outside.write_text('{"secret":"PRIVATE"}', encoding="utf-8")
        # 권한에 의존하지 않고 실제 경계 분기를 고정해 검사합니다.
        original = Path.is_symlink
        with mock.patch.object(Path, "is_symlink", lambda target: target == path or original(target)):
            result = sigma_results(self.root, 0)
        self.assertIsNone(result["metrics"])
        self.assertNotIn("PRIVATE", json.dumps(result))

    def test_result_nested_metric_value_is_not_returned(self):
        folder, metrics = self.result_fixture()
        metrics["test"]["accuracy"] = {"source_path": "D:/medical/private-example"}
        payload = json.dumps(metrics).encode("utf-8")
        original_open = open_status_file

        def memory_open(path):
            if path == folder / "sigma_0_metrics.json":
                return io.BytesIO(payload)
            return original_open(path)

        # 측정 파일을 바꾸지 않고 HTTP 응답 경계에 오염된 값만 주입합니다.
        with mock.patch("dashboard.open_status_file", side_effect=memory_open):
            code, _, body = self.get("/api/sigma-results/0")
        self.assertEqual(code, 200)
        result = json.loads(body)
        self.assertEqual(result["status"], "unavailable")
        self.assertEqual(result["history"], [])
        self.assertIsNone(result["metrics"])
        self.assertNotIn(b"private-example", body)
        self.assertNotIn(b"source_path", body)

    def result_memory_response(self, folder, metrics, history):
        records = {folder / "sigma_0_metrics.json": metrics, folder / "sigma_0_history.json": history}
        original_open = open_status_file

        def memory_open(path):
            if path in records:
                return io.BytesIO(json.dumps(records[path]).encode("utf-8"))
            return original_open(path)

        with mock.patch("dashboard.open_status_file", side_effect=memory_open):
            code, _, body = self.get("/api/sigma-results/0")
        self.assertEqual(code, 200)
        return json.loads(body), body

    def test_result_public_fields_reject_invalid_types_and_nonfinite_values(self):
        folder, original_metrics = self.result_fixture()
        original_history = json.loads((folder / "sigma_0_history.json").read_text(encoding="utf-8"))
        fields = [("test", key) for key in ("accuracy", "auc", "loss", "n_images")]
        fields += [("metrics", key) for key in ("best_epoch", "epochs_ran", "optimizer_steps", "completed_at", "run_id", "sigma")]
        fields += [("history", key) for key in ("sigma", "epoch", "train_loss", "val_loss", "val_accuracy", "val_auc",
                                                "learning_rate", "next_learning_rate", "optimizer_steps", "early_stopping_wait")]
        invalid = ({"source_path": "D:/medical/private-example"}, ["D:/medical/private-example"],
                   "D:/medical/private-example", True, False, float("nan"), float("inf"), float("-inf"), None)
        before = {path: path.read_bytes() for path in (folder / "sigma_0_metrics.json", folder / "sigma_0_history.json")}
        for group, key in fields:
            for value in invalid:
                if value is None and key in ("auc", "val_auc"):
                    continue
                with self.subTest(group=group, key=key, value=value):
                    metrics, history = copy.deepcopy(original_metrics), copy.deepcopy(original_history)
                    target = metrics["test"] if group == "test" else metrics if group == "metrics" else history[0]
                    target[key] = value
                    result, body = self.result_memory_response(folder, metrics, history)
                    self.assertEqual(result["status"], "unavailable")
                    self.assertEqual(result["history"], [])
                    self.assertIsNone(result["metrics"])
                    self.assertNotIn(b"private-example", body)
                    self.assertNotIn(b"source_path", body)
        for path, payload in before.items():
            self.assertEqual(path.read_bytes(), payload)

    def test_result_numeric_ranges_epoch_alignment_and_timestamp_are_checked(self):
        folder, original_metrics = self.result_fixture()
        original_history = json.loads((folder / "sigma_0_history.json").read_text(encoding="utf-8"))
        cases = [("test", "accuracy", -0.1), ("test", "accuracy", 1.1), ("test", "auc", -0.1),
                 ("test", "auc", 1.1), ("test", "loss", -1), ("test", "n_images", 0),
                 ("test", "n_images", 1.5), ("test", "n_images", 2**53),
                 ("metrics", "best_epoch", 0), ("metrics", "best_epoch", 4),
                 ("metrics", "epochs_ran", 2), ("metrics", "optimizer_steps", 29),
                 ("metrics", "completed_at", "2026-11-10T01:00:00"),
                 ("metrics", "completed_at", "2026-99-10T01:00:00+09:00"),
                 ("metrics", "completed_at", "2026-11-10T01:00:00+09:00" + "0"*50),
                 ("history", "epoch", 2), ("history", "epoch", 1.0), ("history", "sigma", 0.0),
                 ("history", "train_loss", -1), ("history", "val_loss", -1),
                 ("history", "val_accuracy", 2), ("history", "val_auc", -1),
                 ("history", "learning_rate", -1), ("history", "next_learning_rate", -1),
                 ("history", "optimizer_steps", -1), ("history", "early_stopping_wait", 2),
                 ("history", "early_stopping_wait", 0.5), ("history", "run_id", "fedcba9876543210")]
        for group, key, value in cases:
            with self.subTest(group=group, key=key, value=value):
                metrics, history = copy.deepcopy(original_metrics), copy.deepcopy(original_history)
                target = metrics["test"] if group == "test" else metrics if group == "metrics" else history[0]
                target[key] = value
                result, _ = self.result_memory_response(folder, metrics, history)
                self.assertEqual(result["status"], "unavailable")
                self.assertEqual(result["history"], [])
                self.assertIsNone(result["metrics"])
        for history in ([], original_history[:2], original_history[::-1],
                        [original_history[0], original_history[0], original_history[2]]):
            result, _ = self.result_memory_response(folder, original_metrics, history)
            self.assertEqual(result["status"], "unavailable")
        history = copy.deepcopy(original_history)
        history[1]["optimizer_steps"] = 1
        self.assertEqual(self.result_memory_response(folder, original_metrics, history)[0]["status"], "unavailable")

    def test_result_zero_and_undefined_auc_keep_valid_values(self):
        folder, metrics = self.result_fixture()
        history = json.loads((folder / "sigma_0_history.json").read_text(encoding="utf-8"))
        metrics["test"].update(accuracy=0, auc=None, loss=0)
        history[0].update(val_accuracy=0, val_auc=None, optimizer_steps=0)
        result, body = self.result_memory_response(folder, metrics, history)
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["metrics"]["test"], {"accuracy": 0, "auc": None, "loss": 0, "n_images": 164})
        self.assertEqual(result["history"][0]["val_accuracy"], 0)
        self.assertIsNone(result["history"][0]["val_auc"])
        self.assertEqual(result["history"][0]["learning_rate"], 0)
        self.assertEqual(result["history"][0]["optimizer_steps"], 0)
        self.assertNotIn(b"PRIVATE", body)

    def test_result_container_and_pending_state_values_fail_closed(self):
        folder, metrics = self.result_fixture()
        history = json.loads((folder / "sigma_0_history.json").read_text(encoding="utf-8"))
        for bad in (None, [], "D:/medical/private-example", True):
            with self.subTest(container="test", value=bad):
                changed = dict(metrics, test=bad)
                result, body = self.result_memory_response(folder, changed, history)
                self.assertEqual(result["status"], "unavailable")
                self.assertNotIn(b"private-example", body)
            for bad_metrics, bad_history in ((bad, history), (metrics, bad)):
                result, body = self.result_memory_response(folder, bad_metrics, bad_history)
                self.assertEqual(result["status"], "unavailable")
                self.assertNotIn(b"private-example", body)
        state = {"run_id": "0123456789abcdef", "sigma_queue": [{"sigma": 0, "status": "running"}], "history": history}
        with mock.patch("dashboard.read_status", return_value=state):
            self.assertEqual(self.get("/api/sigma-results/0")[0], 200)
            self.assertEqual(sigma_results(self.root, 0)["status"], "running")
        for change in ({"run_id": {"source_path": "D:/medical/private-example"}},
                       {"sigma_queue": [{"sigma": 0, "status": {"source_path": "D:/medical/private-example"}}]},
                       {"sigma_queue": [{"sigma": False, "status": "completed"}]},
                       {"sigma_queue": [{"sigma": 0, "status": "running"}]*2},
                       {"sigma_queue": {}}, {"history": None},
                       {"history": [dict(history[0], val_loss={"source_path": "D:/medical/private-example"})]}):
            with self.subTest(change=change), mock.patch("dashboard.read_status", return_value=dict(state, **change)):
                code, _, body = self.get("/api/sigma-results/0")
                result = json.loads(body)
                self.assertEqual(code, 200)
                self.assertEqual(result["status"], "unavailable")
                self.assertEqual(result["history"], [])
                self.assertIsNone(result["metrics"])
                self.assertNotIn(b"private-example", body)


if __name__ == "__main__":
    unittest.main()

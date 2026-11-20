"""경로 이관과 명시적 상태 복구가 과학 설정·가중치를 바꾸지 않는지 검사합니다."""

import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock
import io
from contextlib import redirect_stdout

import torch
import numpy as np
from PIL import Image

from tools import recovery, safe_training
from src import training
from src.state import StatusWriter


class RecoveryTests(unittest.TestCase):
    def manifest(self):
        row = {"path": "D:/원본/Normal/a.png", "relative_path": "Normal/a.png",
               "label": 0, "byte_sha256": "a" * 64, "similarity_group": "g"}
        rows = [row]
        return {"records": rows, "splits": {"train": copy.deepcopy(rows), "validation": [], "test": []},
                "summary": {"original_total": 1}, "manifest_sha256": recovery.records_digest(rows)}

    def test_manifest_changes_only_path_and_derived_hash(self):
        source = self.manifest()
        target = recovery.relocate_manifest(source, "D:/원본", "E:/원본")
        self.assertEqual(target["records"][0]["path"], "E:/원본/Normal/a.png")
        self.assertEqual(target["splits"]["train"][0]["path"], "E:/원본/Normal/a.png")
        self.assertEqual(target["summary"], source["summary"])
        self.assertEqual(source["records"][0]["path"], "D:/원본/Normal/a.png")
        reversed_target = recovery.relocate_manifest(target, "E:/원본", "D:/원본")
        self.assertEqual(reversed_target, source)

    def test_manifest_rejects_foreign_and_parent_paths(self):
        for bad in ["D:/원본외부/a.png", "D:/원본/../비밀/a.png"]:
            value = self.manifest()
            value["records"][0]["path"] = bad
            with self.assertRaises(ValueError):
                recovery.relocate_manifest(value, "D:/원본", "E:/원본")

    def test_config_allows_only_exact_relocation_fields(self):
        old = {"dataset_root": "D:/원본", "epochs": 100, "seed": 42,
               "expected_reference_manifest": "../2차/manifest.json",
               "expected_reference_manifest_sha256": "a" * 64,
               "expected_reference_records_sha256": "b" * 64}
        new = recovery.relocated_config(old, "E:/원본", self.manifest())
        recovery.assert_config_compatible(old, new, "E:/원본", self.manifest())
        for key, value in [("epochs", 99), ("seed", 43), ("precision", "fp16")]:
            changed = {**new, key: value}
            with self.assertRaises(ValueError):
                recovery.assert_config_compatible(old, changed, "E:/원본", self.manifest())

    def test_baseline_and_source_tamper_fail_closed(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            path = root / "기준.json"
            path.write_text('{"source_files": {"file": "wrong"}}', encoding="utf-8")
            digest = recovery.file_digest(path)
            baseline = recovery.read_baseline(path, digest)
            (root / "file").write_text("원본", encoding="utf-8")
            with self.assertRaises(ValueError):
                recovery.verify_files(root, baseline["source_files"])
            path.write_text("{}", encoding="utf-8")
            with self.assertRaises(ValueError):
                recovery.read_baseline(path, digest)

    def test_checkpoint_rebinding_preserves_all_tensor_and_control_values(self):
        original = {"run_id": "a" * 16, "sigma": 1, "epoch": 65,
                    "model": {"weight": torch.tensor([1.0, 2.0])},
                    "optimizer": {"state": {0: {"exp_avg": torch.tensor([.2])}}},
                    "scheduler": {"last_epoch": 65}, "torch_rng_state": torch.get_rng_state(),
                    "training_control": {"best_raw_epoch": 62}, "shadow_prefix_sha256": "c" * 64}
        changed = recovery.rebind_checkpoint(original, "a" * 16, "b" * 16, 1, "d" * 64)
        self.assertEqual(changed["run_id"], "b" * 16)
        self.assertEqual(changed["shadow_prefix_sha256"], "d" * 64)
        self.assertEqual(original["run_id"], "a" * 16)
        recovery.assert_state_equal({k: v for k, v in original.items() if k not in {"run_id", "shadow_prefix_sha256"}},
                                    {k: v for k, v in changed.items() if k not in {"run_id", "shadow_prefix_sha256"}})
        with self.assertRaises(ValueError):
            recovery.rebind_checkpoint(original, "e" * 16, "b" * 16, 1, "d" * 64)

    def test_serialized_prefix_hash_links_last_and_completed_metric(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / "old.pt"
            torch.save({"run_id": "a" * 16, "sigma": 0, "epoch": 1,
                        "model": {"weight": torch.ones(2)}}, source)
            result = recovery.convert_checkpoint(source, root / "new.pt", "a" * 16, "b" * 16, 0)
            self.assertEqual(result["new_sha256"], recovery.file_digest(root / "new.pt"))
            metric = {"run_id": "a" * 16, "sigma": 0, "epochs_ran": 100,
                      "test": {"accuracy": 1.0, "n_images": 4, "confusion_matrix": [[2, 0], [0, 2]]},
                      "early_stopping_comparison": {"available": True, "checkpoint_sha256": "old"}}
            changed = recovery.rebind_metric(metric, "a" * 16, "b" * 16, 0, result["new_sha256"])
            self.assertEqual(changed["test"], metric["test"])
            self.assertEqual(changed["early_stopping_comparison"]["checkpoint_sha256"], result["new_sha256"])
            invalid = copy.deepcopy(metric)
            invalid["test"]["accuracy"] = .75
            with self.assertRaises(ValueError):
                recovery.rebind_metric(invalid, "a" * 16, "b" * 16, 0, result["new_sha256"])

    def test_resume_requires_complete_history_and_frozen_prefix(self):
        last = {"epoch": 2, "history": [{"epoch": 1}, {"epoch": 2}],
                "training_control": {"optimizer_steps": 4, "best_raw_epoch": 1,
                                     "best_raw_loss": .1, "meaningful_best_loss": .1, "stale_epochs": 1,
                                     "shadow_stop_epoch": 2, "shadow_best_raw_epoch": 1,
                                     "enabled": False, "patience": 15, "min_delta": .0001}}
        config = {"epochs": 100, "batch_size": 1, "samples_per_class": 1,
                  "early_stopping_enabled": False, "early_stopping_patience": 15, "min_delta": .0001}
        self.assertEqual(recovery.validate_resume(last, config, 2), 3)
        last["history"].pop()
        with self.assertRaises(ValueError):
            recovery.validate_resume(last, config, 2)

    def test_low_space_and_duplicate_process_block_before_training(self):
        with mock.patch.object(safe_training.shutil, "disk_usage", return_value=mock.Mock(free=10)):
            with self.assertRaises(OSError):
                safe_training.require_free_space(Path.cwd(), 100)
        with self.assertRaises(RuntimeError):
            safe_training.reject_duplicates([{"pid": 12, "command": "run_training.py"}])
        safe_training.reject_duplicates([])

    def test_primary_and_secondary_error_survive_one_failed_log_sink(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            broken = root / "blocked"
            broken.write_text("폴더 아님", encoding="utf-8")
            good = root / "good"
            try:
                raise OSError(28, "원래 저장 오류")
            except OSError as error:
                payload = safe_training.exception_payload(error)
            failures = safe_training.write_independent_logs([broken, good], "오류.json", payload)
            self.assertEqual(len(failures), 1)
            saved = json.loads((good / "오류.json").read_text(encoding="utf-8"))
            self.assertEqual(saved["errno"], 28)
            self.assertIn("원래 저장 오류", saved["traceback"])
            self.assertEqual(len(saved["secondary_log_errors"]), 1)

    def test_worker_preserves_primary_before_failing_status_error_handler(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "config.json").write_text("{}", encoding="utf-8")
            state = mock.Mock()
            state.data = {"sigma": 1, "epoch": 66, "attempted_batch": 470,
                          "sigma_queue": [{"status": "running"}]}
            state.update.side_effect = [None, PermissionError("상태 오류 기록도 실패")]
            folders = [root / "first", root / "second"]
            with mock.patch("src.state.StatusWriter", return_value=state), \
                    mock.patch("src.state.atomic_json", side_effect=OSError("오류 파일 기록 실패")), \
                    mock.patch("src.training.run_training", side_effect=OSError(28, "원래 학습 저장 오류")), \
                    mock.patch.object(safe_training.sys, "stderr", io.StringIO()):
                code = safe_training.worker(root, "cpu", folders)
            self.assertEqual(code, 1)
            for path in folders:
                record = json.loads(next(path.glob("*.json")).read_text(encoding="utf-8"))
                self.assertEqual(record["errno"], 28)
                self.assertIn("원래 학습 저장 오류", record["traceback"])
                self.assertEqual(len(record["secondary_status_errors"]), 2)

    def test_import_then_actual_cpu_loop_skips_completed_and_resumes_epoch66(self):
        # 임상 자료와 GPU 없이 같은 저장·재개 함수의 실제 경계를 검사합니다.
        class TinyModel(torch.nn.Module):
            def __init__(self, **kwargs):
                super().__init__()
                self.weight = torch.nn.Parameter(torch.tensor(1.0))

            def forward(self, images):
                return (images.mean((1, 2, 3)) - .5) * self.weight

        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder)
            source, target = base / "old", base / "new"
            old_data, new_data = base / "old_data", base / "new_data"
            for root in (source, target):
                (root / "src").mkdir(parents=True)
                for name in recovery.SCIENTIFIC:
                    (root / name).write_text("# 합성 검사 원본\n", encoding="utf-8")
            records, splits = [], {}
            for split in ("train", "validation", "test"):
                splits[split] = []
                for label in (0, 1):
                    relative = f"{split}_{label}.png"
                    for data_root in (old_data, new_data):
                        data_root.mkdir(exist_ok=True)
                        Image.fromarray(np.full((8, 8), 40 + 160 * label, dtype=np.uint8)).save(data_root / relative)
                    row = {"path": str(old_data / relative), "relative_path": relative, "label": label,
                           "source_class": "Normal cases" if label == 0 else "Malignant cases",
                           "byte_sha256": recovery.file_digest(old_data / relative)}
                    records.append(row); splits[split].append(copy.deepcopy(row))
            manifest = {"records": records, "splits": splits, "summary": {},
                        "manifest_sha256": recovery.records_digest(records)}
            config = {"dataset_root": str(old_data), "seed": 42, "cpu_threads": 1, "precision": "fp32",
                      "epochs": 100, "early_stopping_enabled": False, "early_stopping_patience": 15,
                      "min_delta": .0001, "batch_size": 1, "samples_per_class": 1, "image_size": 8,
                      "learning_rate": .00003, "weight_decay": .0001, "scheduler_patience": 4,
                      "scheduler_factor": .5, "min_learning_rate": .000001, "num_workers": 0,
                      "sigmas": [0, 1], "status_every_batches": 1,
                      "expected_reference_manifest": "reference.json",
                      "expected_reference_manifest_sha256": hashlib.sha256(recovery.json_bytes(manifest)).hexdigest(),
                      "expected_reference_records_sha256": manifest["manifest_sha256"]}
            (source / "work/results").mkdir(parents=True)
            (source / "config.json").write_bytes(recovery.json_bytes(config))
            (source / "reference.json").write_bytes(recovery.json_bytes(manifest))
            (source / "work/results/dataset_manifest_private.json").write_bytes(recovery.json_bytes(manifest))
            old_run, old_settings = training._run_identity(source, config, manifest["manifest_sha256"])
            result_dir = source / f"work/results/run_{old_run}"
            checkpoint_dir = source / f"work/checkpoints/run_{old_run}"
            result_dir.mkdir(parents=True); checkpoint_dir.mkdir(parents=True)
            (result_dir / "run_metadata.json").write_bytes(recovery.json_bytes({**old_settings, "run_id": old_run,
                                                                               "started_at": "2026-11-13T00:00:00+09:00"}))
            for sigma, epoch in [(0, 100), (1, 65)]:
                control = training.TrainingControl(enabled=False)
                control.best_raw_loss = control.meaningful_best_loss = .5
                control.best_raw_epoch = control.shadow_best_raw_epoch = 1
                control.shadow_stop_epoch, control.stale_epochs = 16, epoch - 1
                control.optimizer_steps = epoch * 2
                model = TinyModel()
                optimizer, scheduler = training.build_optimizer_scheduler(model.parameters(), config)
                history = [{"sigma": sigma, "epoch": i} for i in range(1, epoch + 1)]
                basic = {"run_id": old_run, "sigma": sigma, "epoch": 1, "model": model.state_dict()}
                prefix_path = checkpoint_dir / f"sigma_{sigma}_shadow_prefix_best.pt"
                torch.save(basic, prefix_path)
                torch.save(basic, checkpoint_dir / f"sigma_{sigma}_best.pt")
                last = {**basic, "epoch": epoch, "optimizer": optimizer.state_dict(), "scheduler": scheduler.state_dict(),
                        "scaler": {}, "training_control": control.state_dict(), "torch_rng_state": torch.get_rng_state(),
                        "cuda_rng_state": [], "shadow_prefix_sha256": recovery.file_digest(prefix_path), "history": history}
                torch.save(last, checkpoint_dir / f"sigma_{sigma}_last.pt")
                (result_dir / f"sigma_{sigma}_history.json").write_bytes(recovery.json_bytes(history))
                if sigma == 0:
                    metric = {"run_id": old_run, "sigma": 0, "epochs_ran": 100, "optimizer_steps": 200,
                              "completed_at": "원본 완료", "test": {"accuracy": 1.0, "n_images": 2, "confusion_matrix": [[1, 0], [0, 1]]},
                              "early_stopping_comparison": {"available": True, "checkpoint_sha256": recovery.file_digest(prefix_path)}}
                    (result_dir / "sigma_0_metrics.json").write_bytes(recovery.json_bytes(metric))
            files = {p.relative_to(source).as_posix(): recovery.file_digest(p) for p in source.rglob("*") if p.is_file()}
            baseline = {"source_files": files, "source_run_id": old_run, "source_config": config,
                        "reference_relative_path": "reference.json", "reference_file_sha256": config["expected_reference_manifest_sha256"],
                        "reference_records_sha256": manifest["manifest_sha256"], "source_dataset_prefix": str(old_data),
                        "target_dataset_prefix": str(new_data), "transfer": {"0": {"epoch": 100, "completed": True},
                                                                               "1": {"epoch": 65, "completed": False}}}
            baseline_path = base / "baseline.json"
            baseline_path.write_bytes(recovery.json_bytes(baseline))
            new_manifest = recovery.relocate_manifest(manifest, str(old_data), str(new_data))
            new_config = recovery.relocated_config(config, str(new_data), new_manifest)
            (target / "config.json").write_bytes(recovery.json_bytes(new_config))
            with mock.patch.object(recovery, "prepare_dataset", return_value=new_manifest):
                lineage = recovery.import_recovery(target, source, baseline_path, recovery.file_digest(baseline_path))
            self.assertNotEqual(lineage["run_id"], old_run)
            self.assertEqual(lineage["transfer"]["1"]["next_epoch"], 66)
            recovery.verify_files(source, files)
            state = StatusWriter(target, new_config)
            epochs, tested = [], []
            actual_update, actual_evaluate = state.update, training.evaluate

            def update(**values):
                if values.get("stage") == "training" and values.get("batch") == 0:
                    epochs.append((state.data["sigma"], values["epoch"]))
                return actual_update(**values)

            def evaluate(*args, **kwargs):
                if kwargs.get("stage") == "testing":
                    tested.append((state.data["sigma"], state.data["epoch"]))
                return actual_evaluate(*args, **kwargs)

            with mock.patch.object(training, "prepare_dataset", return_value=new_manifest), \
                    mock.patch.object(training, "SplitResNet50", TinyModel), \
                    mock.patch.object(training, "evaluate", side_effect=evaluate), \
                    mock.patch.object(state, "update", side_effect=update), redirect_stdout(io.StringIO()):
                training.run_training(new_config, target, state, "cpu")
            self.assertEqual(epochs[0], (1, 66))
            self.assertEqual(epochs[-1], (1, 100))
            self.assertEqual(len(epochs), 35)
            self.assertEqual(tested, [(1, 100), (1, 100)])
            self.assertEqual(state.data["stage"], "completed")
            recovery.verify_import(target, initial=False)
            # prefix 변조는 다음 실행 경계에서 차단됩니다.
            frozen = target / f"work/checkpoints/run_{lineage['run_id']}/sigma_1_shadow_prefix_best.pt"
            frozen.write_bytes("변조".encode("utf-8"))
            with self.assertRaises(ValueError):
                recovery.verify_import(target, initial=False)


class WorkerParentTests(unittest.TestCase):
    def test_direct_supervisor_parent_is_accepted(self):
        with mock.patch.object(safe_training.os, "getppid", return_value=42):
            self.assertTrue(safe_training.worker_parent_authorized("42"))

    def test_exact_venv_launcher_between_supervisor_and_worker_is_accepted(self):
        row = {"ProcessId": 50, "ParentProcessId": 42, "ExecutablePath": safe_training.sys.executable}
        with mock.patch.object(safe_training.os, "getppid", return_value=50), \
                mock.patch.object(safe_training, "windows_process", return_value=row):
            self.assertTrue(safe_training.worker_parent_authorized("42"))

    def test_wrong_launcher_parent_pid_and_executable_are_rejected(self):
        valid = {"ProcessId": 50, "ParentProcessId": 42, "ExecutablePath": safe_training.sys.executable}
        for changes in ({"ProcessId": 51}, {"ParentProcessId": 43},
                        {"ExecutablePath": "C:/다른환경/python.exe"}, {"ExecutablePath": None}):
            with self.subTest(changes=changes), \
                    mock.patch.object(safe_training.os, "getppid", return_value=50), \
                    mock.patch.object(safe_training, "windows_process", return_value={**valid, **changes}):
                self.assertFalse(safe_training.worker_parent_authorized("42"))

    def test_missing_or_malformed_supervisor_id_is_rejected(self):
        for value in (None, "", "0", "-1", "42;exit", "４２"):
            with self.subTest(value=value):
                self.assertFalse(safe_training.worker_parent_authorized(value))

    def test_launcher_query_failure_does_not_authorize_worker(self):
        with mock.patch.object(safe_training.os, "getppid", return_value=50), \
                mock.patch.object(safe_training, "windows_process", side_effect=RuntimeError("CIM 조회 실패")):
            with self.assertRaises(RuntimeError):
                safe_training.worker_parent_authorized("42")


class DuplicateCommandTests(unittest.TestCase):
    def processes(self, command):
        rows = [{"ProcessId": 900000001, "ParentProcessId": 900000002,
                 "ExecutablePath": "C:/Python/python.exe", "CommandLine": command},
                {"ProcessId": safe_training.os.getpid(), "ParentProcessId": safe_training.os.getppid(),
                 "ExecutablePath": "C:/Python/python.exe", "CommandLine": "자기 프로세스"}]
        response = mock.Mock(returncode=0, stdout=json.dumps(rows), stderr="")
        with mock.patch.object(safe_training.subprocess, "run", return_value=response):
            return safe_training.training_processes(Path("E:/가상/실험"))

    def test_relative_training_entry_is_ambiguous_and_blocks_start(self):
        for script in ("run_training.py", '"run_training.py"', ".\\run_training.py",
                       "../5차/복구_학습.py", '"상대 폴더/run_training.py"', "-m run_training"):
            with self.subTest(script=script):
                found = self.processes('"C:/Python/python.exe" ' + script + " train --device cuda")
                self.assertEqual([row["pid"] for row in found], [900000001])
                with self.assertRaises(RuntimeError):
                    safe_training.reject_duplicates(found)

    def test_explicit_other_project_is_excluded_and_same_project_both_drives_block(self):
        self.assertEqual(self.processes('"C:/Python/python.exe" "E:/다른 프로젝트/run_training.py" train'), [])
        for drive in ("D", "E"):
            with self.subTest(drive=drive):
                found = self.processes(f'"C:/Python/python.exe" "{drive}:/가상/실험/4차/run_training.py" train')
                self.assertEqual([row["pid"] for row in found], [900000001])

    def test_cim_query_failure_blocks_instead_of_returning_no_conflicts(self):
        response = mock.Mock(returncode=1, stdout="", stderr="CIM 조회 실패")
        with mock.patch.object(safe_training.subprocess, "run", return_value=response):
            with self.assertRaises(RuntimeError):
                safe_training.training_processes(Path("E:/가상/실험"))

    def test_only_cim_confirmed_own_venv_launcher_is_excluded(self):
        own = {"ProcessId": 42, "ParentProcessId": 50, "ExecutablePath": "C:/Python/python.exe", "CommandLine": "자기 프로세스"}
        for launcher_pid, executable, expected in ((50, safe_training.sys.executable, []),
                                                   (50, "C:/다른환경/python.exe", [50]),
                                                   (51, safe_training.sys.executable, [51])):
            rows = [own, {"ProcessId": launcher_pid, "ParentProcessId": 10, "ExecutablePath": executable,
                          "CommandLine": '"C:/Python/python.exe" "E:/가상/실험/5차/복구_학습.py"'}]
            response = mock.Mock(returncode=0, stdout=json.dumps(rows), stderr="")
            with self.subTest(pid=launcher_pid, executable=executable), \
                    mock.patch.object(safe_training.os, "getpid", return_value=42), \
                    mock.patch.object(safe_training.os, "getppid", return_value=50), \
                    mock.patch.object(safe_training.subprocess, "run", return_value=response):
                self.assertEqual([row["pid"] for row in safe_training.training_processes(Path("E:/가상/실험"))], expected)

    def test_unconfirmed_own_cim_parent_relation_blocks_start(self):
        rows = [{"ProcessId": 42, "ParentProcessId": 51, "CommandLine": "자기 프로세스"}]
        response = mock.Mock(returncode=0, stdout=json.dumps(rows), stderr="")
        with mock.patch.object(safe_training.os, "getpid", return_value=42), \
                mock.patch.object(safe_training.os, "getppid", return_value=50), \
                mock.patch.object(safe_training.subprocess, "run", return_value=response):
            with self.assertRaises(RuntimeError):
                safe_training.training_processes(Path("E:/가상/실험"))


if __name__ == "__main__":
    unittest.main()

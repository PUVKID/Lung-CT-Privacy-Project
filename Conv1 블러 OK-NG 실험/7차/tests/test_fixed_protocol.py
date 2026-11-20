"""단일 σ0 학습과 동결 평가의 경계 및 실패 경로를 합성 CPU 입력으로 검사합니다."""

import copy
import hashlib
import importlib
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


class FixedProtocolTests(unittest.TestCase):
    def test_prepare_and_smoke_refuse_active_lock_without_changing_files(self):
        import run_training
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            runtime = root / "work/runtime"
            runtime.mkdir(parents=True)
            status = runtime / "status.json"
            lock = runtime / "recovery.lock"
            status.write_text(json.dumps({"phase": "training", "epoch": 47, "pid": 123}), encoding="utf-8")
            lock.write_text("이미 있는 잠금", encoding="utf-8")
            before = {path: path.read_bytes() for path in [status, lock]}
            with mock.patch.object(run_training, "ROOT", root):
                for operation in [lambda: run_training.prepare({}), lambda: run_training.smoke({}, "cuda")]:
                    with self.assertRaisesRegex(RuntimeError, "잠금"):
                        operation()
                    self.assertEqual({path: path.read_bytes() for path in before}, before)

    def test_unstarted_guard_refuses_progress_and_accepts_only_empty_ready(self):
        import run_training
        from src.state import StatusWriter
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            status = StatusWriter(root, {"epochs": 100, "sigmas": [0, 1]})
            status.update(phase="preparing", stage="ready", status="ready", pid=None)
            run_training.require_unstarted(root)
            path = root / "work/runtime/status.json"
            for changes in [{"phase": "training", "epoch": 47, "pid": 123}, {"history": [{"epoch": 1}]}, {"training_status": "completed"}]:
                altered = {**status.data, **changes}
                path.write_text(json.dumps(altered), encoding="utf-8")
                before = path.read_bytes()
                with self.assertRaises(RuntimeError):
                    run_training.require_unstarted(root)
                self.assertEqual(before, path.read_bytes())

    def test_status_marks_all_sigmas_as_evaluation_pending(self):
        from src.state import StatusWriter
        with tempfile.TemporaryDirectory() as directory:
            status = StatusWriter(directory, {"epochs": 100, "sigmas": [0, 1, 4], "training_sigma": 0})
            self.assertTrue(status.data.get("protocol_fixed_model"), "고정 모델 프로토콜 상태가 없습니다.")
            self.assertEqual(status.data["training_sigma"], 0)
            self.assertEqual(status.data["training_status"], "pending")
            self.assertTrue(all(row["status"] == "pending" for row in status.data["sigma_queue"]))

    def test_frozen_state_digest_includes_batch_norm_buffers(self):
        import torch
        from src import training
        self.assertTrue(hasattr(training, "tensor_state_digest"), "전체 state 동결 검사가 없습니다.")
        model = torch.nn.BatchNorm2d(2)
        before = training.tensor_state_digest(model.state_dict())
        model.running_mean[0] += 1
        self.assertNotEqual(before, training.tensor_state_digest(model.state_dict()))

    def test_immutable_model_eval_replaces_blur_for_every_sigma(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = SyntheticRun(Path(directory))
            state, models = fixture.execute()
            self.assertEqual(len(models), 2, "학습 모델 하나와 동결 평가 모델 하나만 만듭니다.")
            self.assertEqual(models[0].training_sigmas, [0] * 100)
            self.assertEqual(state["epoch"], 100)
            self.assertTrue(all(row["status"] == "completed" for row in state["sigma_queue"]))
            self.assertEqual(len(models[1].blur_objects), 10)
            self.assertEqual(len({id(value) for value in models[1].blur_objects}), 10)
            from src.identity import validate_fixed_result, SIGMAS
            values = [json.loads((fixture.result_dir / f"sigma_{sigma}_metrics.json").read_text(encoding="utf-8")) for sigma in SIGMAS]
            for value in values:
                validate_fixed_result(fixture.root, value)
                self.assertEqual(value["eval_optimizer_steps"], 0)
                self.assertEqual(value["state_digest_before"], value["state_digest_after"])
            self.assertEqual(len({value["checkpoint_sha256"] for value in values}), 1)
            self.assertEqual(len({value["model_state_sha256"] for value in values}), 1)
            self.assertEqual(fixture.val_training_sigmas, [0] * 100)
            for key, invalid in [("training_sigma", False), ("epochs_ran", 100.0), ("eval_optimizer_steps", 1), ("checkpoint_sha256", "0" * 64)]:
                with self.subTest(tamper=key), self.assertRaises(ValueError):
                    validate_fixed_result(fixture.root, {**values[0], key: invalid})
            prediction = fixture.root / values[0]["prediction_files"]["test"]["relative_path"]
            original = prediction.read_bytes()
            prediction.write_bytes(original + b"tampered")
            with self.assertRaises(ValueError):
                validate_fixed_result(fixture.root, values[0])
            prediction.write_bytes(original)
            checkpoint = fixture.root / values[0]["selected_checkpoint"]
            checkpoint.write_bytes(checkpoint.read_bytes() + b"tampered")
            with self.assertRaises(ValueError):
                validate_fixed_result(fixture.root, values[0])

    def test_identity_is_standard_library_and_refuses_other_protocol(self):
        from src.identity import validate_config
        config = json.loads((Path(__file__).resolve().parents[1] / "config.json").read_text(encoding="utf-8"))
        for key, value in [("training_sigma", False), ("epochs", 100.0), ("training_sigma", 4), ("early_stopping_enabled", True), ("protocol", "adaptive")]:
            invalid = {**config, key: value}
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                validate_config(invalid)
        # stdlib helper가 Torch를 import하지 않는지 새 프로세스로 확인합니다.
        import subprocess
        import sys
        result = subprocess.run([sys.executable, "-B", "-c", "import src.identity,sys; assert 'torch' not in sys.modules"],
                                cwd=Path(__file__).resolve().parents[1], capture_output=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_resume_preserves_rng_optimizer_and_completed_epoch(self):
        from src import training
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            full = SyntheticRun(Path(a))
            full_state, _ = full.execute()
            resumed = SyntheticRun(Path(b))
            original_save = training._save_checkpoint
            def interrupt_after_complete_epoch(path, payload):
                original_save(path, payload)
                if Path(path).name == "sigma_0_last.pt" and payload["epoch"] == 3:
                    raise RuntimeError("제어된 완료 회차 중단")
            with mock.patch.object(training, "_save_checkpoint", side_effect=interrupt_after_complete_epoch):
                with self.assertRaisesRegex(RuntimeError, "제어된"):
                    resumed.execute()
            self.assertFalse(list(resumed.result_dir.glob("sigma_*_metrics.json")))
            state, models = resumed.execute()
            self.assertEqual(len(models[0].training_sigmas), 97)
            self.assertEqual(state["optimizer_steps"], full_state["optimizer_steps"])
            first = training.checkpoint_load(full.checkpoint_dir / "sigma_0_last.pt", full.run_id)
            second = training.checkpoint_load(resumed.checkpoint_dir / "sigma_0_last.pt", resumed.run_id)
            self.assertEqual(training.tensor_state_digest(first["model"]), training.tensor_state_digest(second["model"]))
            self.assertEqual(first["scheduler"], second["scheduler"])
            self.assertEqual(first["training_control"], second["training_control"])

    def test_eval_rejects_batch_norm_buffer_mutation(self):
        from src import training
        real_evaluate = training.evaluate
        def corrupt_buffer(model, *args, **kwargs):
            result = real_evaluate(model, *args, **kwargs)
            if not any(p.requires_grad for p in model.parameters()):
                model.cloud[0].running_mean.add_(1)
            return result
        with tempfile.TemporaryDirectory() as directory:
            fixture = SyntheticRun(Path(directory))
            with mock.patch.object(training, "evaluate", side_effect=corrupt_buffer), self.assertRaisesRegex(ValueError, "BN"):
                fixture.execute()
            self.assertFalse(list(fixture.result_dir.glob("sigma_*_metrics.json")))

    def test_safe_path_rejects_outside_and_checkpoint_symlink(self):
        from src.identity import safe_path
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaises(ValueError):
                safe_path(root, "../outside")
            target = root / "target"
            target.write_text("합성", encoding="utf-8")
            link = root / "linked"
            try:
                link.symlink_to(target)
            except OSError:
                self.skipTest("이 Windows 세션은 심볼릭 링크 생성 권한이 없습니다.")
            with self.assertRaises(ValueError):
                safe_path(root, "linked")


class SyntheticRun:
    """실제 CT·GPU 없이 같은 생산 학습 루프를100회 통과시키는 합성 fixture입니다."""
    def __init__(self, root):
        from src.identity import _run_identity
        self.root = root
        self.config = json.loads((Path(__file__).resolve().parents[1] / "config.json").read_text(encoding="utf-8"))
        self.config["cpu_threads"] = 1
        rows = [{"path": "synthetic0", "relative_path": "합성0", "label": 0, "source_class": "OK"},
                {"path": "synthetic1", "relative_path": "합성1", "label": 1, "source_class": "NG"}]
        records_sha = hashlib.sha256(json.dumps(rows, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()
        self.manifest = {"records": rows, "splits": {name: copy.deepcopy(rows) for name in ["train", "validation", "test"]},
                         "summary": {"patient_id_available": False}, "manifest_sha256": records_sha}
        reference = root / self.config["expected_reference_manifest"]
        reference.parent.mkdir(parents=True)
        reference.write_text(json.dumps(self.manifest, ensure_ascii=False), encoding="utf-8")
        self.config["expected_reference_manifest_sha256"] = hashlib.sha256(reference.read_bytes()).hexdigest()
        self.config["expected_reference_records_sha256"] = records_sha
        (root / "config.json").write_text(json.dumps(self.config, ensure_ascii=False), encoding="utf-8")
        (root / "run_training.py").write_text("# 합성 검사\n", encoding="utf-8")
        (root / "src").mkdir()
        (root / "src/fixture.py").write_text("# 합성 검사\n", encoding="utf-8")
        self.run_id, _ = _run_identity(root, self.config, records_sha)
        self.result_dir = root / "work/results" / ("run_" + self.run_id)
        self.result_dir.mkdir(parents=True)
        (root / "work/results/dataset_manifest_private.json").write_text(json.dumps(self.manifest, ensure_ascii=False), encoding="utf-8")
        self.checkpoint_dir = root / "work/checkpoints" / ("run_" + self.run_id)
        self.val_training_sigmas = []

    def execute(self):
        import torch
        from src import training
        from src.model import GaussianDCTBlur
        from src.state import StatusWriter
        models = []
        class TinyModel(torch.nn.Module):
            def __init__(self, sigma=0, **kwargs):
                super().__init__()
                self.edge = torch.nn.Conv2d(3, 2, 1, bias=False).requires_grad_(False)
                self.blur = GaussianDCTBlur(sigma)
                self.cloud = torch.nn.Sequential(torch.nn.BatchNorm2d(2), torch.nn.ReLU(), torch.nn.AdaptiveAvgPool2d(1), torch.nn.Flatten(), torch.nn.Linear(2, 1))
                self.register_buffer("rgb_mean", torch.zeros(1, 3, 1, 1))
                self.register_buffer("rgb_std", torch.ones(1, 3, 1, 1))
                self.training_sigmas, self.blur_objects = [], []
                models.append(self)
            def train(self, mode=True):
                super().train(mode)
                self.cloud[0].eval()
                return self
            def forward(self, images):
                if self.training:
                    self.training_sigmas.append(self.blur.sigma)
                elif not any(p.requires_grad for p in self.parameters()) and self.blur not in self.blur_objects:
                    self.blur_objects.append(self.blur)
                return self.cloud(self.blur(self.edge(images))).squeeze(1)
        class TinyDataset:
            def __init__(self, records, image_size, training=False, **kwargs):
                self.records = records
                self.training = training
            def __len__(self):
                return 10000 if self.training else 2
            def set_epoch(self, epoch):
                self.epoch = epoch
        def loader(dataset, config, device):
            target = torch.tensor([0., 1.]).repeat(5000 if dataset.training else 1)
            class TinyLoader(list):
                pass
            result = TinyLoader([(target[:, None, None, None].expand(-1, 3, 2, 2).clone(), target)])
            result.dataset = dataset
            return result
        real_evaluate = training.evaluate
        def record_evaluate(model, *args, **kwargs):
            if any(p.requires_grad for p in model.parameters()):
                self.val_training_sigmas.append(model.blur.sigma)
            return real_evaluate(model, *args, **kwargs)
        with mock.patch.object(training, "prepare_dataset", return_value=self.manifest), \
             mock.patch.object(training, "CTDataset", TinyDataset), mock.patch.object(training, "_loader", side_effect=loader), \
             mock.patch.object(training, "SplitResNet50", TinyModel), \
             mock.patch.object(training, "precision_policy", return_value={"name": "fp32", "dtype": torch.float32, "autocast_enabled": False, "use_grad_scaler": False}), \
             mock.patch.object(training, "evaluate", side_effect=record_evaluate):
            state = StatusWriter(self.root, self.config)
            result = training.run_training(self.config, self.root, state, "cpu")
        return result, models


if __name__ == "__main__":
    unittest.main()

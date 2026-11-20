"""100회 고정 학습·가상 조기 종료·분할 고정과 정확한 정답수를 검증합니다."""

import copy
import hashlib
import inspect
import io
import json
from pathlib import Path
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest import mock

import numpy as np
from PIL import Image
import torch
from torch import nn

import dashboard
from src import data, training
from src.state import StatusWriter, atomic_json


class TinyClassifier(nn.Module):
    """실제 optimizer·손실·저장 경로를 빠르게 검사하는 작은 CPU 분류기입니다."""
    def __init__(self, **_kwargs):
        super().__init__()
        self.weight = nn.Parameter(torch.tensor(0.0))

    def forward(self, images):
        return (images.mean((1, 2, 3)) - 0.5) * self.weight


class FixedEpochTests(unittest.TestCase):
    def make_fixture(self, root, enabled=False):
        # 기존 검사와 같은 실제 파일 경계를 사용하며 외부 자료·모델만 대체합니다.
        (root / "src").mkdir()
        (root / "src" / "__init__.py").write_text("", encoding="utf-8")
        (root / "run_training.py").write_text("", encoding="utf-8")
        config = {"seed": 42, "cpu_threads": 1, "precision": "fp32", "epochs": 100,
                  "early_stopping_patience": 2, "min_delta": 100.0, "batch_size": 2,
                  "learning_rate": 0.1, "weight_decay": 0.0, "scheduler_patience": 4,
                  "scheduler_factor": 0.5, "min_learning_rate": 0.01, "image_size": 8,
                  "samples_per_class": 1, "num_workers": 0, "sigmas": [0],
                  "status_every_batches": 1, "early_stopping_enabled": enabled}
        (root / "config.json").write_text(json.dumps(config), encoding="utf-8")
        splits = {}
        for split in ["train", "validation", "test"]:
            rows = []
            for label, value in [(0, 60), (1, 195)]:
                path = root / f"{split}_{label}.png"
                Image.fromarray(np.full((8, 8), value, dtype=np.uint8)).save(path)
                rows.append({"path": str(path), "relative_path": path.name, "label": label,
                             "source_class": "Normal cases" if label == 0 else "Malignant cases"})
            splits[split] = rows
        return config, {"manifest_sha256": "a" * 64, "summary": {}, "splits": splits}

    def run_fixture(self, root, config, manifest, state=None):
        state = state or StatusWriter(root, config)
        real_evaluate = training.evaluate
        test_epochs = []

        def observed_evaluate(*args, **kwargs):
            if kwargs.get("stage") == "testing":
                test_epochs.append(state.data["epoch"])
            return real_evaluate(*args, **kwargs)

        with mock.patch.object(training, "prepare_dataset", return_value=manifest), \
                mock.patch.object(training, "SplitResNet50", TinyClassifier), \
                mock.patch.object(training, "evaluate", side_effect=observed_evaluate), redirect_stdout(io.StringIO()):
            training.run_training(config, root, state, "cpu")
        folder = root / state.data["result_directory"]
        result = json.loads((folder / "sigma_0_metrics.json").read_text(encoding="utf-8"))
        result["observed_test_epochs"] = test_epochs
        return result, folder

    def test_disabled_control_records_first_stop_once_and_continues_to_100(self):
        self.assertIn("enabled", inspect.signature(training.TrainingControl).parameters)
        control = training.TrainingControl(min_delta=100, patience=2, enabled=False)
        for epoch in range(1, 101):
            decision = control.observe(0.01 / epoch, epoch)
            self.assertFalse(decision["should_stop"])
        self.assertEqual(control.shadow_stop_epoch, 3)
        self.assertEqual(control.shadow_best_raw_epoch, 3)
        self.assertEqual(control.best_raw_epoch, 100)

    def test_control_resume_keeps_disabled_mode_and_frozen_prefix_epoch(self):
        self.assertIn("enabled", inspect.signature(training.TrainingControl).parameters)
        control = training.TrainingControl(min_delta=100, patience=2, enabled=False)
        for epoch in range(1, 5):
            control.observe(1 / epoch, epoch)
        restored = training.TrainingControl(min_delta=100, patience=2, enabled=False)
        restored.load_state_dict(control.state_dict())
        restored.observe(0.001, 5)
        self.assertEqual(restored.shadow_stop_epoch, 3)
        self.assertEqual(restored.shadow_best_raw_epoch, 3)
        self.assertEqual(restored.best_raw_epoch, 5)
        with self.assertRaises(ValueError):
            training.TrainingControl(min_delta=100, patience=2).load_state_dict(control.state_dict())

    def test_100_epochs_keep_prefix_checkpoint_and_main_test_selects_full_best(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config, manifest = self.make_fixture(root)
            result, folder = self.run_fixture(root, config, manifest)
            self.assertEqual(result["epochs_ran"], 100)
            self.assertFalse(result["training_policy"]["early_stopping_enabled"])
            self.assertEqual(result["optimizer_steps"], 100)
            comparison = result["early_stopping_comparison"]
            self.assertEqual(comparison["shadow_stop_epoch"], 3)
            self.assertEqual(comparison["best_epoch"], 3)
            self.assertEqual(result["best_epoch"], 100)
            self.assertEqual(result["observed_test_epochs"], [100, 100])
            self.assertLess(result["validation"]["loss"], comparison["validation"]["loss"])
            history = json.loads((folder / "sigma_0_history.json").read_text(encoding="utf-8"))
            self.assertEqual(len(history), 100)
            self.assertEqual([row["epoch"] for row in history], list(range(1, 101)))

    def test_interrupted_resume_keeps_prefix_hash_and_does_not_stop_at_shadow_epoch(self):
        class InterruptAfterFour(StatusWriter):
            def event(self, name, details=None):
                super().event(name, details)
                if name == "epoch 완료" and details["epoch"] == 4:
                    raise KeyboardInterrupt()

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config, manifest = self.make_fixture(root)
            state = InterruptAfterFour(root, config)
            with self.assertRaises(KeyboardInterrupt):
                self.run_fixture(root, config, manifest, state)
            prefix = next((root / "work/checkpoints").glob("*/sigma_0_shadow_prefix_best.pt"), None)
            self.assertIsNotNone(prefix)
            initial_hash = hashlib.sha256(prefix.read_bytes()).hexdigest()
            result, _ = self.run_fixture(root, config, manifest)
            self.assertEqual(result["epochs_ran"], 100)
            self.assertEqual(result["early_stopping_comparison"]["shadow_stop_epoch"], 3)
            self.assertEqual(hashlib.sha256(prefix.read_bytes()).hexdigest(), initial_hash)

    def test_default_true_keeps_original_early_stopping(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config, manifest = self.make_fixture(root, enabled=True)
            del config["early_stopping_enabled"]
            result, _ = self.run_fixture(root, config, manifest)
            self.assertEqual(result["epochs_ran"], 3)
            self.assertEqual(result["stopping_reason"], "meaningful_validation_plateau")

    def test_ready_state_exposes_disabled_policy_before_training(self):
        with tempfile.TemporaryDirectory() as directory:
            state = StatusWriter(Path(directory), {"early_stopping_enabled": False})
            self.assertIs(state.data["training_policy"].get("early_stopping_enabled"), False)


class ReferencePinTests(unittest.TestCase):
    def test_reference_pin_rejects_changed_file_records_or_split(self):
        self.assertTrue(hasattr(data, "validate_reference_manifest"))
        records = [{"relative_path": "a", "label": 0}, {"relative_path": "b", "label": 1}]
        digest = hashlib.sha256(json.dumps(records, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()
        payload = {"records": records, "manifest_sha256": digest,
                   "splits": {"train": [records[0]], "validation": [records[1]], "test": []}}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            reference = root / "reference.json"
            raw = json.dumps(payload).encode()
            reference.write_bytes(raw)
            config = {"expected_reference_manifest": str(reference),
                      "expected_reference_manifest_sha256": hashlib.sha256(raw).hexdigest(),
                      "expected_reference_records_sha256": digest}
            data.validate_reference_manifest(config, root, payload)
            changed = copy.deepcopy(payload)
            changed["splits"]["train"], changed["splits"]["validation"] = changed["splits"]["validation"], changed["splits"]["train"]
            with self.assertRaises(ValueError):
                data.validate_reference_manifest(config, root, changed)
            changed = copy.deepcopy(payload)
            changed["records"][0]["label"] = 1
            with self.assertRaises(ValueError):
                data.validate_reference_manifest(config, root, changed)
            reference.write_bytes(raw + b" ")
            with self.assertRaises(ValueError):
                data.validate_reference_manifest(config, root, payload)


class ResultCountTests(unittest.TestCase):
    def write_result(self, root, matrix):
        run_id = "a" * 16
        atomic_json(root / "work/runtime/status.json", {"status": "completed", "stage": "completed",
                    "updated_at": "2026-11-10T11:00:00+09:00",
                    "run_id": run_id, "sigma_queue": [{"sigma": 0, "status": "completed"}]})
        folder = root / "work/results" / f"run_{run_id}"
        row = {"sigma": 0, "epoch": 1, "train_loss": 0.1, "val_loss": 0.1,
               "val_accuracy": 0.75, "val_auc": 0.9, "learning_rate": 0.001,
               "next_learning_rate": 0.001, "optimizer_steps": 1, "early_stopping_wait": 0}
        atomic_json(folder / "sigma_0_history.json", [row])
        test = {"accuracy": 0.75, "auc": 0.9, "loss": 0.1, "n_images": 4}
        if matrix is not None:
            test["confusion_matrix"] = matrix
        atomic_json(folder / "sigma_0_metrics.json", {"run_id": run_id, "sigma": 0,
                    "best_epoch": 1, "epochs_ran": 1, "optimizer_steps": 1,
                    "completed_at": "2026-11-10T11:00:00+09:00", "test": test})

    def test_correct_count_only_comes_from_validated_integer_matrix(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_result(root, [[1, 1], [0, 2]])
            result = dashboard.sigma_results(root, 0)
            self.assertEqual(result["metrics"]["test"].get("correct_count"), 3)
            self.write_result(root, None)
            self.assertNotIn("correct_count", dashboard.sigma_results(root, 0)["metrics"]["test"])
            for matrix in [[[True, 1], [0, 2]], [[1.0, 1], [0, 2]], [[1, 0], [0, 2]], [[1, {"private": "secret"}], [0, 2]]]:
                self.write_result(root, matrix)
                result = dashboard.sigma_results(root, 0)
                self.assertIsNone(result["metrics"])
                self.assertNotIn("secret", json.dumps(result))

    def test_accuracy_inconsistent_with_matrix_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for matrix in [[[2, 0], [0, 2]], [[0, 2], [2, 0]]]:
                with self.subTest(matrix=matrix):
                    # 저장된 정확도 0.75와 대각합의 실제 원비율 1 또는 0은 모순입니다.
                    self.write_result(root, matrix)
                    result = dashboard.sigma_results(root, 0)
                    self.assertEqual(result["status"], "unavailable")
                    self.assertIsNone(result["metrics"])
                    self.assertEqual(result["history"], [])
                    self.assertEqual(result["message"], "이 강도의 결과 기록을 확인할 수 없어요.")


if __name__ == "__main__":
    unittest.main()

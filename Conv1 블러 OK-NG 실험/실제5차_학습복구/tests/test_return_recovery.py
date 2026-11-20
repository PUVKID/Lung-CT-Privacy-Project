"""관찰용 종료 전의 부분 상태와 E 원본이 없는 D 재개를 합성 CPU 자료로 검사합니다."""

import copy
import hashlib
import io
import json
from contextlib import redirect_stdout
from pathlib import Path
import tempfile
import unittest
from unittest import mock

import numpy as np
from PIL import Image
import torch

from tools import recovery
from src import training
from src.state import StatusWriter


class TinyReturnModel(torch.nn.Module):
    def __init__(self, **kwargs):
        super().__init__()
        self.weight = torch.nn.Parameter(torch.tensor(1.0))

    def forward(self, images):
        return (images.mean((1, 2, 3)) - .5) * self.weight


class UnfrozenReturnTests(unittest.TestCase):
    def fixture(self, folder):
        base = Path(folder)
        source, target = base / "이전_실행", base / "D_복귀"
        old_data, new_data = base / "이전_영상", base / "D_영상"
        for root in (source, target):
            (root / "src").mkdir(parents=True)
            for name in recovery.SCIENTIFIC:
                (root / name).write_text("# 합성 고정 학습 소스\n", encoding="utf-8")
        records, splits = [], {}
        for split in ("train", "validation", "test"):
            splits[split] = []
            for label in (0, 1):
                relative = f"{split}_{label}.png"
                for root in (old_data, new_data):
                    root.mkdir(exist_ok=True)
                    Image.fromarray(np.full((8, 8), 40 + 160 * label, dtype=np.uint8)).save(root / relative)
                row = {"path": str(old_data / relative), "relative_path": relative, "label": label,
                       "source_class": "Normal cases" if label == 0 else "Malignant cases",
                       "byte_sha256": recovery.file_digest(old_data / relative)}
                records.append(row)
                splits[split].append(copy.deepcopy(row))
        manifest = {"records": records, "splits": splits, "summary": {},
                    "manifest_sha256": recovery.records_digest(records)}
        config = {"dataset_root": str(old_data), "seed": 42, "cpu_threads": 1, "precision": "fp32",
                  "epochs": 4, "early_stopping_enabled": False, "early_stopping_patience": 2,
                  "min_delta": .0001, "batch_size": 1, "samples_per_class": 1, "image_size": 8,
                  "learning_rate": .00003, "weight_decay": .0001, "scheduler_patience": 4,
                  "scheduler_factor": .5, "min_learning_rate": .000001, "num_workers": 0,
                  "sigmas": [0, 2], "status_every_batches": 1,
                  "expected_reference_manifest": "reference.json",
                  "expected_reference_manifest_sha256": hashlib.sha256(recovery.json_bytes(manifest)).hexdigest(),
                  "expected_reference_records_sha256": manifest["manifest_sha256"]}
        (source / "work/results").mkdir(parents=True)
        (source / "config.json").write_bytes(recovery.json_bytes(config))
        (source / "reference.json").write_bytes(recovery.json_bytes(manifest))
        (source / "work/results/dataset_manifest_private.json").write_bytes(recovery.json_bytes(manifest))
        old_run, settings = training._run_identity(source, config, manifest["manifest_sha256"])
        results = source / f"work/results/run_{old_run}"
        checkpoints = source / f"work/checkpoints/run_{old_run}"
        results.mkdir(parents=True)
        checkpoints.mkdir(parents=True)
        (results / "run_metadata.json").write_bytes(recovery.json_bytes({**settings, "run_id": old_run,
                                                                          "started_at": "합성 원본 시각"}))
        for sigma, epoch in ((0, 4), (2, 1)):
            control = training.TrainingControl(.0001, 2, enabled=False)
            control.best_raw_loss = control.meaningful_best_loss = .00001
            control.best_raw_epoch = 1
            control.optimizer_steps = epoch * 2
            model = TinyReturnModel()
            optimizer, scheduler = training.build_optimizer_scheduler(model.parameters(), config)
            basic = {"run_id": old_run, "sigma": sigma, "epoch": 1, "model": model.state_dict()}
            prefix_hash = None
            if sigma == 0:
                control.shadow_stop_epoch, control.shadow_best_raw_epoch, control.stale_epochs = 3, 1, 3
                prefix = checkpoints / "sigma_0_shadow_prefix_best.pt"
                torch.save(basic, prefix)
                prefix_hash = recovery.file_digest(prefix)
            history = [{"sigma": sigma, "epoch": i} for i in range(1, epoch + 1)]
            torch.save(basic, checkpoints / f"sigma_{sigma}_best.pt")
            torch.save({**basic, "epoch": epoch, "optimizer": optimizer.state_dict(),
                        "scheduler": scheduler.state_dict(), "scaler": {},
                        "training_control": control.state_dict(), "torch_rng_state": torch.get_rng_state(),
                        "cuda_rng_state": [], "shadow_prefix_sha256": prefix_hash, "history": history},
                       checkpoints / f"sigma_{sigma}_last.pt")
            (results / f"sigma_{sigma}_history.json").write_bytes(recovery.json_bytes(history))
            if sigma == 0:
                metric = {"run_id": old_run, "sigma": 0, "epochs_ran": 4, "optimizer_steps": 8,
                          "completed_at": "합성 완료", "test": {"accuracy": 1.0, "n_images": 2,
                                                                     "confusion_matrix": [[1, 0], [0, 1]]},
                          "early_stopping_comparison": {"available": True, "checkpoint_sha256": prefix_hash}}
                (results / "sigma_0_metrics.json").write_bytes(recovery.json_bytes(metric))
        baseline = {"source_files": {}, "source_run_id": old_run, "source_config": config,
                    "reference_relative_path": "reference.json",
                    "reference_file_sha256": config["expected_reference_manifest_sha256"],
                    "reference_records_sha256": manifest["manifest_sha256"],
                    "source_dataset_prefix": str(old_data), "target_dataset_prefix": str(new_data),
                    "transfer": {"0": {"epoch": 4, "completed": True}, "2": {"epoch": 1, "completed": False}}}
        baseline_path = target / "work/recovery/복귀_기준.json"
        baseline_path.parent.mkdir(parents=True)
        new_manifest = recovery.relocate_manifest(manifest, str(old_data), str(new_data))
        new_config = recovery.relocated_config(config, str(new_data), new_manifest)
        (target / "config.json").write_bytes(recovery.json_bytes(new_config))
        return {"source": source, "target": target, "old_run": old_run, "checkpoints": checkpoints,
                "baseline": baseline, "baseline_path": baseline_path, "manifest": new_manifest,
                "config": new_config}

    def import_fixture(self, value):
        source = value["source"]
        value["baseline"]["source_files"] = {p.relative_to(source).as_posix(): recovery.file_digest(p)
                                                for p in source.rglob("*") if p.is_file()}
        value["baseline_path"].write_bytes(recovery.json_bytes(value["baseline"]))
        with mock.patch.object(recovery, "prepare_dataset", return_value=value["manifest"]):
            return recovery.import_recovery(value["target"], source, value["baseline_path"],
                                             recovery.file_digest(value["baseline_path"]))

    def test_none_prefix_hash_is_preserved_without_fabricating_a_checkpoint(self):
        source = {"run_id": "a" * 16, "sigma": 2, "epoch": 20, "shadow_prefix_sha256": None,
                  "model": {"weight": torch.tensor([2.0])}, "training_control": {"shadow_stop_epoch": 0}}
        restored = recovery.rebind_checkpoint(source, "a" * 16, "b" * 16, 2)
        self.assertIsNone(restored["shadow_prefix_sha256"])
        recovery.assert_state_equal(source["model"], restored["model"])
        self.assertEqual(restored["training_control"]["shadow_stop_epoch"], 0)

    def test_partial_before_shadow_stop_imports_without_a_prefix_and_source_access(self):
        with tempfile.TemporaryDirectory() as folder:
            value = self.fixture(folder)
            lineage = self.import_fixture(value)
            self.assertEqual(lineage["transfer"]["2"]["next_epoch"], 2)
            self.assertNotIn("sigma_2_shadow_prefix_best.pt", lineage["converted_checkpoints"])
            checkpoint_dir = value["target"] / f"work/checkpoints/run_{lineage['run_id']}"
            self.assertFalse((checkpoint_dir / "sigma_2_shadow_prefix_best.pt").exists())
            old_last = torch.load(value["checkpoints"] / "sigma_2_last.pt", map_location="cpu", weights_only=False)
            new_last = torch.load(checkpoint_dir / "sigma_2_last.pt", map_location="cpu", weights_only=False)
            recovery.assert_state_equal({k: v for k, v in old_last.items() if k != "run_id"},
                                        {k: v for k, v in new_last.items() if k != "run_id"})
            value["source"].rename(Path(folder) / "접근불가_이전_실행")
            result = recovery.verify_import(value["target"], initial=True)
            self.assertTrue(result["verified"])

    def test_missing_frozen_prefix_and_orphan_prefix_states_are_rejected(self):
        for corruption in ("종료만기록", "해시만기록", "고아파일", "최적시점만기록"):
            with self.subTest(corruption=corruption), tempfile.TemporaryDirectory() as folder:
                value = self.fixture(folder)
                path = value["checkpoints"] / "sigma_2_last.pt"
                last = torch.load(path, map_location="cpu", weights_only=False)
                if corruption == "종료만기록":
                    last["training_control"].update(shadow_stop_epoch=1, shadow_best_raw_epoch=1)
                elif corruption == "해시만기록":
                    last["shadow_prefix_sha256"] = "f" * 64
                elif corruption == "최적시점만기록":
                    last["training_control"]["shadow_best_raw_epoch"] = 1
                else:
                    torch.save({"run_id": value["old_run"], "sigma": 2, "epoch": 1},
                               value["checkpoints"] / "sigma_2_shadow_prefix_best.pt")
                torch.save(last, path)
                with self.assertRaises(ValueError):
                    self.import_fixture(value)

    def test_existing_frozen_prefix_requires_original_hash_before_rebinding(self):
        with tempfile.TemporaryDirectory() as folder:
            value = self.fixture(folder)
            path = value["checkpoints"] / "sigma_0_last.pt"
            last = torch.load(path, map_location="cpu", weights_only=False)
            last["shadow_prefix_sha256"] = "f" * 64
            torch.save(last, path)
            with self.assertRaises(ValueError):
                self.import_fixture(value)

    def test_real_cpu_resume_creates_future_prefix_and_preserves_completed_result(self):
        with tempfile.TemporaryDirectory() as folder:
            value = self.fixture(folder)
            lineage = self.import_fixture(value)
            value["source"].rename(Path(folder) / "접근불가_이전_실행")
            root, config = value["target"], value["config"]
            result_dir = root / f"work/results/run_{lineage['run_id']}"
            saved_metric = (result_dir / "sigma_0_metrics.json").read_bytes()
            state = StatusWriter(root, config)
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

            with mock.patch.object(training, "prepare_dataset", return_value=value["manifest"]), \
                    mock.patch.object(training, "SplitResNet50", TinyReturnModel), \
                    mock.patch.object(training, "evaluate", side_effect=evaluate), \
                    mock.patch.object(state, "update", side_effect=update), redirect_stdout(io.StringIO()):
                training.run_training(config, root, state, "cpu")
            self.assertEqual(epochs, [(2, 2), (2, 3), (2, 4)])
            self.assertEqual(tested, [(2, 4), (2, 4)])
            self.assertEqual((result_dir / "sigma_0_metrics.json").read_bytes(), saved_metric)
            self.assertTrue(recovery.verify_import(root, initial=False)["verified"])
            prefix = root / f"work/checkpoints/run_{lineage['run_id']}/sigma_2_shadow_prefix_best.pt"
            self.assertTrue(prefix.is_file())
            prefix.write_bytes(b"tampered-prefix")
            with self.assertRaises(ValueError):
                recovery.verify_import(root, initial=False)


if __name__ == "__main__":
    unittest.main()

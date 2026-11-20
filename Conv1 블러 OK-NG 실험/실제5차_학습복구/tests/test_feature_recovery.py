"""특징맵 감시의 일시 읽기 잠금과 실제 실패를 구분합니다."""

from pathlib import Path
import copy
import hashlib
import json
import tempfile
import unittest
from unittest import mock

from tools import feature_generator as generator
from src.training import _run_identity
import dashboard


def sharing_error():
    error = PermissionError("일시적인 공유 잠금")
    error.winerror = 32
    return error


class FeatureReadTests(unittest.TestCase):
    def test_transient_windows_read_lock_retries_then_succeeds(self):
        with mock.patch.object(Path, "read_text", side_effect=[sharing_error(), '{"run_id":"new"}']) as read, \
                mock.patch.object(generator.time, "sleep") as pause:
            self.assertEqual(generator.read_json(Path("status.json")), {"run_id": "new"})
            self.assertEqual(read.call_count, 2)
            pause.assert_called_once()

    def test_persistent_windows_lock_stops_after_bound(self):
        with mock.patch.object(Path, "read_text", side_effect=sharing_error()) as read, \
                mock.patch.object(generator.time, "sleep"):
            with self.assertRaises(PermissionError):
                generator.read_json(Path("status.json"))
            self.assertEqual(read.call_count, 7)

    def test_other_error_or_invalid_json_is_not_hidden_or_retried(self):
        for value in [OSError(28, "공간 부족"), PermissionError(13, "지속 권한 오류"), '{"broken":']:
            with mock.patch.object(Path, "read_text", side_effect=value if isinstance(value, Exception) else None,
                                   return_value=value) as read, mock.patch.object(generator.time, "sleep") as pause:
                with self.assertRaises((OSError, ValueError)):
                    generator.read_json(Path("status.json"))
                self.assertEqual(read.call_count, 1)
                pause.assert_not_called()

    def test_old_run_lineage_is_rejected_before_any_inference(self):
        with mock.patch.object(generator, "RUN", "b" * 16), \
                mock.patch.object(generator, "read_json", return_value={"run_id": "a" * 16, "source_run_id": "a" * 16}):
            with self.assertRaises(ValueError):
                generator.run_once([])

    def test_http_preview_uses_only_round5_and_current_run(self):
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder)
            root = base / "experiment"
            result_dir = root / ("work/results/run_" + "b" * 16)
            result_dir.mkdir(parents=True)
            (result_dir / "sigma_0_metrics.json").write_text(json.dumps({"run_id": "b" * 16, "sigma": 0,
                "completed_at": "완료", "test": {"accuracy": 1}, "training_policy": {"early_stopping_enabled": False}}), encoding="utf-8")
            output = base / "블러 강도별 대표 특징맵" / "5차"
            output.mkdir(parents=True)
            items = []
            raw = b"\x89PNG\r\n\x1a\n" + b"synthetic"
            for key in ("Bengin_cases", "Malignant_cases", "Normal_cases"):
                for stage in range(6):
                    relative = dashboard.feature_preview_path(0, key, stage)
                    path = output / relative
                    path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(raw)
                    items.append({"id": f"0-{key}-{stage}", "sigma": 0, "class_key": key, "stage": stage,
                                  "relative_path": relative.as_posix(), "sha256": hashlib.sha256(raw).hexdigest()})
            index = output / "export_index_private.json"
            payload = {"run_id": "b" * 16, "completed_sigmas": [0], "items": items}
            index.write_text(json.dumps(payload), encoding="utf-8")
            with mock.patch.object(dashboard, "read_status", return_value={"run_id": "b" * 16,
                    "sigma_queue": [{"sigma": 0, "status": "completed"}]}):
                result = dashboard.feature_previews(root, "0-Normal_cases-0")
                self.assertEqual(result["completed_sigmas"], [0])
                self.assertEqual(len(result["items"]), 18)
                self.assertEqual(next(i for i in result["items"] if i["id"] == "0-Normal_cases-0")["_payload"], raw)
                payload["run_id"] = "a" * 16
                index.write_text(json.dumps(payload), encoding="utf-8")
                rejected = dashboard.feature_previews(root)
                self.assertEqual(rejected["items"], [])
                self.assertIn("error", rejected)


class FeatureIdentityTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.train = Path(self.temporary.name) / "실험"
        self.output = Path(self.temporary.name) / "그림"
        (self.train / "src").mkdir(parents=True)
        self.output.mkdir()
        for relative in ("run_training.py", "src/data.py", "src/model.py"):
            (self.train / relative).write_text("# 합성 고정 소스\n", encoding="utf-8")
        rows = [{"source_class": source, "relative_path": f"{index}.png", "label": int(index == 1),
                 "path": str(self.train / f"{index}.png"), "byte_sha256": "a" * 64}
                for index, (_key, source, _label) in enumerate(generator.CLASSES)]
        records_sha = hashlib.sha256(json.dumps(rows, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()
        self.manifest = {"records": rows, "splits": {"train": copy.deepcopy(rows), "validation": [], "test": []},
                         "manifest_sha256": records_sha}
        reference = self.train / "기준.json"
        self.write_json(reference, self.manifest)
        config = {"expected_reference_manifest": "기준.json",
                  "expected_reference_manifest_sha256": hashlib.sha256(reference.read_bytes()).hexdigest(),
                  "expected_reference_records_sha256": records_sha}
        self.write_json(self.train / "config.json", config)
        self.run_id, settings = _run_identity(self.train, config, records_sha)
        self.write_json(self.train / "work/recovery/복구_계보_비공개.json",
                        {"run_id": self.run_id, "source_run_id": "f" * 16, "settings": settings})
        self.write_json(self.train / "work/runtime/status.json", {"run_id": self.run_id, "sigma_queue": []})
        self.manifest_path = self.train / "work/results/dataset_manifest_private.json"
        self.write_json(self.manifest_path, self.manifest)
        patches = mock.patch.multiple(generator, TRAIN=self.train, HERE=self.output, RUN=self.run_id)
        patches.start()
        self.addCleanup(patches.stop)

    @staticmethod
    def write_json(path, value):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def test_verified_pending_run_has_no_images_and_waits(self):
        self.assertFalse(generator.run_once([]))
        saved = json.loads((self.output / "export_index_private.json").read_text(encoding="utf-8"))
        self.assertEqual(saved["items"], [])
        self.assertEqual(saved["pending_sigmas"], [0, 1, 2, 4, 8, 16, 32, 64, 128, 256])

    def test_manifest_record_tamper_with_unchanged_claimed_sha_is_rejected(self):
        self.manifest["records"][0]["label"] = 1
        self.write_json(self.manifest_path, self.manifest)
        with self.assertRaises(ValueError):
            generator.run_once([])
        self.assertFalse((self.output / "export_index_private.json").exists())

    def test_split_tamper_with_unchanged_records_is_rejected(self):
        self.manifest["splits"]["train"].reverse()
        self.write_json(self.manifest_path, self.manifest)
        with self.assertRaises(ValueError):
            generator.run_once([])

    def test_source_changes_and_unexpected_source_file_are_rejected(self):
        for change in ("바뀐원본", "추가소스"):
            path = self.train / ("run_training.py" if change == "바뀐원본" else "src/추가.py")
            original = path.read_bytes() if path.exists() else None
            path.write_text("# 변조\n", encoding="utf-8")
            with self.subTest(change=change), self.assertRaises(ValueError):
                generator.run_once([])
            if original is None:
                path.unlink()
            else:
                path.write_bytes(original)

    def test_existing_output_from_different_generator_is_rejected(self):
        self.assertFalse(generator.run_once([]))
        index_path = self.output / "export_index_private.json"
        payload = json.loads(index_path.read_text(encoding="utf-8"))
        payload["generator_sha256"] = "0" * 64
        self.write_json(index_path, payload)
        with self.assertRaises(ValueError):
            generator.run_once([])


if __name__ == "__main__":
    unittest.main()

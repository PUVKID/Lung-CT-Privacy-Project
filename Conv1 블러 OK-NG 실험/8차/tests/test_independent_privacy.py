"""실제 CT·GPU 없이 새 독립학습과 조건부 점수의 경계를 검사합니다."""

import copy
import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


class IndependentPrivacyTests(unittest.TestCase):
    def test_score_controls_ties_and_expectation_order(self):
        import numpy as np
        from src.privacy import score_gallery
        d = np.array([[0., 1., 4.], [1., 0., 1.], [4., 1., 0.]])
        exact = score_gallery(d, [[0], [1], [2]])
        self.assertEqual(exact["score"], 0.)
        self.assertEqual(exact["fractional_top1"], 1.)
        constant = score_gallery(d, [[0, 1, 2]] * 3)
        self.assertAlmostEqual(constant["score"], 100.)
        self.assertAlmostEqual(constant["fractional_top1"], 1/3)
        # 첫 행 clip(1/(5/3))=.6, clip(4/(5/3))=1: 먼저 clip한 평균은.8입니다.
        tied = score_gallery(d, [[1, 2], [1], [2]])
        self.assertAlmostEqual(tied["per_group"][0]["attack_residual"], .8)
        self.assertAlmostEqual(tied["T_attack"], .8/3)
        self.assertAlmostEqual(tied["T_prior"], (1.6+2+1.6)/9)

    def test_invalid_gallery_and_unmatched_query_are_errors(self):
        import numpy as np
        from src.privacy import score_gallery, match_hashes
        for d in [np.zeros((1, 1)), np.zeros((2, 2)), np.array([[0., np.nan], [np.nan, 0.]])]:
            with self.assertRaises(ValueError):
                score_gallery(d, [[0]] * len(d))
        with self.assertRaises(ValueError):
            match_hashes(["a", "b"], ["a", "missing"])
        self.assertEqual(match_hashes(["a", "a", "b"], ["a", "b"]), [[0, 1], [2]])

    def test_same_candidate_and_monotonic_score(self):
        import numpy as np
        from src.privacy import score_gallery
        d = np.array([[0., 1., 4.], [1., 0., 1.], [4., 1., 0.]])
        weak = score_gallery(d, [[2], [0], [0]])
        strong = score_gallery(d, [[1], [1], [2]])
        self.assertLess(strong["score"], weak["score"])
        self.assertEqual(strong["exact_return_groups"], 2)

    def test_preprocessing_groups_and_feature_hash_header(self):
        import numpy as np
        import torch
        from src.privacy import group_pixels, feature_hash, pairwise_mse
        x = np.array([[[0., 1.]], [[0., 1.]], [[1., 0.]]], dtype=np.float32)
        representatives, groups = group_pixels(x)
        self.assertEqual(representatives, [0, 2])
        self.assertEqual(groups, [[0, 1], [2]])
        np.testing.assert_array_equal(pairwise_mse(x[representatives]), [[0., 1.], [1., 0.]])
        a = torch.zeros(1, 2, 2, dtype=torch.float32)
        self.assertNotEqual(feature_hash(a, "pipeline-a"), feature_hash(a, "pipeline-b"))
        self.assertNotEqual(feature_hash(a, "pipeline-a"), feature_hash(a.reshape(2, 1, 2), "pipeline-a"))

    def test_prepare_guard_is_non_mutating(self):
        import run_training
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "work/runtime/status.json"
            path.parent.mkdir(parents=True)
            path.write_text('{"stage":"training","epoch":77,"pid":123}', encoding="utf-8")
            before = path.read_bytes()
            with mock.patch.object(run_training, "ROOT", root):
                with self.assertRaises(RuntimeError):
                    run_training.prepare({})
            self.assertEqual(path.read_bytes(), before)
            lock = path.parent / "recovery.lock"
            lock.write_text("오래된 잠금도 보존", encoding="utf-8")
            with self.assertRaises(RuntimeError):
                run_training.require_unstarted(root)
            self.assertTrue(lock.exists())

    def test_real_status_storage_and_source_metrics(self):
        from src.state import StatusWriter
        from src.training import per_source_metrics, binary_metrics
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            state = StatusWriter(root, {"epochs":100, "sigmas":[0,1]})
            state.update(stage="training", epoch=3, sigma=1, message="실제 한글 상태 저장")
            self.assertEqual(json.loads((root / "work/runtime/status.json").read_text(encoding="utf-8")), state.data)
            state.event("실제 회차 기록", {"epoch":3})
            raw = (root / "work/runtime/events.jsonl").read_bytes()
            self.assertTrue(raw.endswith(b"\n"))
            self.assertEqual(json.loads(raw.decode())['details'], {"epoch":3})
        rows = [{"source_class":"A"},{"source_class":"A"},{"source_class":"B"},{"source_class":"B"}]
        values = per_source_metrics(rows, [0,1,0,1], [.1,.8,.7,.9], [-2.,1.,1.,2.])
        self.assertEqual(values["A"]["confusion_matrix"], [[1,0],[0,1]])
        self.assertEqual(values["B"]["confusion_matrix"], [[0,1],[0,1]])
        self.assertEqual(binary_metrics([0,1,0,1], [.1,.8,.7,.9])["n_correct"], 3)

    def test_independent_models_100_epochs_and_identity(self):
        from src.identity import SIGMAS, validate_result, validate_privacy_result
        with tempfile.TemporaryDirectory() as directory:
            fixture = SyntheticRun(Path(directory))
            state, models = fixture.execute()
            trained = [m for m in models if m.training_sigmas]
            self.assertEqual(len(trained), 10)
            self.assertEqual([m.training_sigmas for m in trained], [[s] * 100 for s in SIGMAS])
            self.assertEqual(len({m.initial_digest for m in trained}), 1)
            self.assertEqual([r["status"] for r in state["sigma_queue"]], ["completed"] * 10)
            self.assertEqual(fixture.privacy_order, SIGMAS)
            for sigma in SIGMAS:
                result = json.loads((fixture.result_dir / f"sigma_{sigma}_metrics.json").read_text(encoding="utf-8"))
                validate_result(fixture.root, result)
                self.assertEqual(result["training_sigma"], sigma)
                self.assertEqual(result["epochs_ran"], 100)
                self.assertEqual(result["best_epoch"], 1)
                self.assertEqual(fixture.checkpoint_writes.count((f"sigma_{sigma}_best.pt", 1)), 1)
                self.assertEqual(sum(name == f"sigma_{sigma}_best.pt" for name, _ in fixture.checkpoint_writes), 1)
                self.assertEqual([epoch for name, epoch in fixture.checkpoint_writes if name == f"sigma_{sigma}_last.pt"], list(range(1,101)))
                history = json.loads((fixture.result_dir / f"sigma_{sigma}_history.json").read_text(encoding="utf-8"))
                self.assertEqual(result["best_epoch"], min(history, key=lambda row: row["val_loss"])["epoch"])
                self.assertEqual(result["eval_optimizer_steps"], 0)
                private = json.loads((fixture.result_dir / f"sigma_{sigma}_privacy.json").read_text(encoding="utf-8"))
                validate_privacy_result(fixture.root, private)
                if sigma in [0,256]:
                    for key, invalid in [("privacy_source_sha256", "f" * 64), ("packet_batch_size", 8), ("score", 100.)]:
                        with self.assertRaises(ValueError):
                            validate_privacy_result(fixture.root, {**private, key: invalid})
                    for key, invalid in [("training_sigma", False), ("checkpoint_sha256", "0" * 64)]:
                        with self.assertRaises(ValueError):
                            validate_result(fixture.root, {**result, key: invalid})
            again, new_models = fixture.execute()
            self.assertFalse(any(m.training_sigmas for m in new_models))
            self.assertEqual(again["status"], "completed")
            result = json.loads((fixture.result_dir / "sigma_0_metrics.json").read_text(encoding="utf-8"))
            checkpoint = fixture.root / result["selected_checkpoint"]
            checkpoint.write_bytes(checkpoint.read_bytes() + b"tampered")
            with self.assertRaises(ValueError):
                validate_result(fixture.root, result)

    def test_resume_completed_epoch_and_privacy_failure(self):
        from src import training
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            full = SyntheticRun(Path(a))
            full.execute(sigmas=[0])
            resumed = SyntheticRun(Path(b))
            original = training._save_checkpoint
            def stop(path, value):
                original(path, value)
                if Path(path).name == "sigma_0_last.pt" and value["epoch"] == 3:
                    raise RuntimeError("제어된 회차 완료 중단")
            with mock.patch.object(training, "_save_checkpoint", side_effect=stop):
                with self.assertRaisesRegex(RuntimeError, "제어된"):
                    resumed.execute(sigmas=[0])
            _, models = resumed.execute(sigmas=[0])
            self.assertEqual(len(models[0].training_sigmas), 97)
            x = training.checkpoint_load(full.checkpoint_dir / "sigma_0_last.pt", full.run_id, 0)
            y = training.checkpoint_load(resumed.checkpoint_dir / "sigma_0_last.pt", resumed.run_id, 0)
            self.assertEqual(training.tensor_state_digest(x["model"]), training.tensor_state_digest(y["model"]))
            self.assertEqual(x["scheduler"], y["scheduler"])
            self.assertEqual(x["training_control"], y["training_control"])
        with tempfile.TemporaryDirectory() as directory:
            fixture = SyntheticRun(Path(directory))
            with mock.patch.object(training, "run_privacy", side_effect=RuntimeError("제어된 공격 실패")):
                with self.assertRaisesRegex(RuntimeError, "공격 실패"):
                    fixture.execute(patch_privacy=False, sigmas=[0, 1])
            self.assertTrue((fixture.result_dir / "sigma_0_metrics.json").exists())
            self.assertFalse((fixture.checkpoint_dir / "sigma_1_last.pt").exists())
            _, models = fixture.execute(sigmas=[0, 1])
            self.assertFalse(any(m.training_sigmas and m.blur.sigma == 0 for m in models))

    def test_restore_all_rng_next_cpu_samples(self):
        import random
        import numpy as np
        import torch
        from src.training import numpy_rng_state, restore_all_rng
        random.seed(314)
        np.random.seed(314)
        torch.manual_seed(314)
        saved = {"python_rng_state":random.getstate(), "numpy_rng_state":numpy_rng_state(),
                 "torch_rng_state":torch.get_rng_state().clone(), "cuda_rng_state":[]}
        expected = (random.random(), np.random.random(4), torch.rand(4))
        for _ in range(17):
            random.random()
            np.random.random()
            torch.rand(1)
        restore_all_rng(saved, torch.device("cpu"))
        actual = (random.random(), np.random.random(4), torch.rand(4))
        self.assertEqual(actual[0], expected[0])
        np.testing.assert_array_equal(actual[1], expected[1])
        self.assertTrue(torch.equal(actual[2], expected[2]))

    def test_identity_stdlib_and_protocol_validation(self):
        import subprocess
        import sys
        from src.identity import validate_config, safe_path
        root = Path(__file__).resolve().parents[1]
        config = json.loads((root / "config.json").read_text(encoding="utf-8"))
        validate_config(config)
        for key, invalid in [("protocol_fixed_model", True), ("epochs", 100.), ("early_stopping_enabled", True)]:
            with self.assertRaises(ValueError):
                validate_config({**config, key: invalid})
        with self.assertRaises(ValueError):
            safe_path(root, "../outside")
        result = subprocess.run([sys.executable, "-B", "-c", "import src.identity,sys; assert 'torch' not in sys.modules"], cwd=root, capture_output=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_actual_cpu_model_shared_feature_path_and_frozen_bn(self):
        import torch
        from src.model import SplitResNet50, GaussianDCTBlur
        from src.training import seed_everything, tensor_state_digest, build_optimizer_scheduler
        root = Path(__file__).resolve().parents[1]
        config = json.loads((root / "config.json").read_text(encoding="utf-8"))
        seed_everything(42, 1)
        first = SplitResNet50(sigma=4, pretrained=True, weights_path=config["initial_weights_path"], expected_weights_sha256=config["initial_weights_sha256"])
        first.train()
        self.assertFalse(first.edge.training)
        self.assertTrue(all(not m.training for m in first.modules() if isinstance(m, torch.nn.BatchNorm2d)))
        self.assertTrue(all(not p.requires_grad for p in first.edge.parameters()))
        optimizer, _ = build_optimizer_scheduler([p for p in first.parameters() if p.requires_grad], config)
        self.assertEqual(len(optimizer.state), 0)
        x = torch.rand(1, 3, 16, 16)
        with torch.inference_mode():
            actual = first.transmitted_features(x)
            expected = GaussianDCTBlur(4)(first.edge((x-first.rgb_mean)/first.rgb_std))
        self.assertTrue(torch.equal(actual, expected))
        before = tensor_state_digest(first.state_dict())
        seed_everything(42, 1)
        second = SplitResNet50(sigma=256, pretrained=True, weights_path=config["initial_weights_path"], expected_weights_sha256=config["initial_weights_sha256"])
        self.assertEqual(before, tensor_state_digest(second.state_dict()))

    def test_actual_privacy_file_pipeline_and_constant_feature_control(self):
        import torch
        from src.privacy import run_privacy
        from src.model import GaussianDCTBlur
        from src.training import tensor_state_digest
        from src.identity import PROTOCOL, _run_identity, result_binding, validate_privacy_result
        from src.state import atomic_json
        class TinyTransmitter(torch.nn.Module):
            def __init__(self):
                super().__init__()
                self.edge = torch.nn.Conv2d(3, 1, 1, bias=False)
                with torch.no_grad():
                    self.edge.weight.fill_(1/3)
                self.blur = GaussianDCTBlur(4)
                self.calls = 0
            def transmitted_features(self, x):
                self.calls += 1
                return self.blur(self.edge(x)[..., ::256, ::256])
        for constant in [False, True]:
            with self.subTest(constant=constant), tempfile.TemporaryDirectory() as directory:
                fixture = SyntheticRun(Path(directory), real_images=True)
                run_id, settings = _run_identity(fixture.root, fixture.config, fixture.manifest["manifest_sha256"])
                metadata = {**settings, "run_id":run_id, "protocol":PROTOCOL, "protocol_fixed_model":False}
                atomic_json(fixture.result_dir / "run_metadata.json", metadata)
                model = TinyTransmitter().eval().requires_grad_(False)
                if constant:
                    with torch.no_grad():
                        model.edge.weight.zero_()
                before = tensor_state_digest(model.state_dict())
                fixture.checkpoint_dir.mkdir(parents=True)
                checkpoint = fixture.checkpoint_dir / "sigma_4_best.pt"
                checkpoint.write_bytes(b"known-synthetic-only")
                selection = {"run_id":run_id, "protocol":PROTOCOL, "protocol_fixed_model":False, "sigma":4, "training_sigma":4,
                             "epochs_ran":100, "best_epoch":1, "checkpoint_epoch":1,
                             "selected_checkpoint":checkpoint.relative_to(fixture.root).as_posix(),
                             "checkpoint_sha256":hashlib.sha256(checkpoint.read_bytes()).hexdigest(),
                             "model_state_sha256":before, **result_binding(fixture.root,metadata)}
                atomic_json(fixture.result_dir / "sigma_4_selection.json", selection)
                value = run_privacy(model, fixture.manifest["splits"]["test"], fixture.root, run_id, selection)
                validate_privacy_result(fixture.root, value)
                self.assertEqual(value["score"], 100. if constant else 0.)
                self.assertEqual(model.calls, 4, "후보2개와 별도 쿼리2개를 각각 계산해야 합니다.")
                self.assertFalse(any(m.training for m in model.modules()))
                self.assertEqual(before, tensor_state_digest(model.state_dict()))
                raw = json.loads((fixture.root / value["raw_file"]["relative_path"]).read_text(encoding="utf-8"))
                self.assertEqual(raw["per_group"][0]["candidates"], [0,1] if constant else [0])
                if not constant:
                    from src import privacy
                    before_file = (fixture.root / value["raw_file"]["relative_path"]).read_bytes()
                    original_hash, count = privacy.feature_hash, [0]
                    def mismatch(tensor, pipeline):
                        count[0] += 1
                        result = original_hash(tensor, pipeline)
                        return result if count[0] <= 2 else "재현불일치" + result
                    with mock.patch.object(privacy, "feature_hash", side_effect=mismatch), self.assertRaisesRegex(ValueError, "사전"):
                        run_privacy(model, fixture.manifest["splits"]["test"], fixture.root, run_id, selection)
                    self.assertEqual(before_file, (fixture.root / value["raw_file"]["relative_path"]).read_bytes())


class SyntheticRun:
    """실제 생산 루프·저장·재개는 유지하고 대형 모델과 원영상만 합성으로 대체합니다."""
    def __init__(self, root, real_images=False):
        from src.identity import _run_identity
        self.root = root
        self.config = json.loads((Path(__file__).resolve().parents[1] / "config.json").read_text(encoding="utf-8"))
        self.config["cpu_threads"] = 1
        self.config["initial_weights_path"] = "work/reference/합성초기값.bin"
        self.config["expected_reference_manifest"] = "work/reference/dataset_manifest_private.json"
        rows = [{"path": "synthetic0", "relative_path": "합성0", "label": 0, "source_class": "OK"}, {"path": "synthetic1", "relative_path": "합성1", "label": 1, "source_class": "NG"}]
        if real_images:
            from PIL import Image
            folder = root / "합성원본"
            folder.mkdir()
            for i, row in enumerate(rows):
                path = folder / f"합성{i}.png"
                Image.new("L", (4,4), 255*i).save(path)
                row.update(path=str(path), relative_path=path.name, byte_sha256=hashlib.sha256(path.read_bytes()).hexdigest())
        records_sha = hashlib.sha256(json.dumps(rows, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
        self.manifest = {"records": rows, "splits": {n: copy.deepcopy(rows) for n in ["train", "validation", "test"]}, "summary": {}, "manifest_sha256": records_sha}
        reference = root / self.config["expected_reference_manifest"]
        reference.parent.mkdir(parents=True)
        (root / self.config["initial_weights_path"]).write_bytes(b"synthetic-only")
        self.config["initial_weights_sha256"] = hashlib.sha256(b"synthetic-only").hexdigest()
        reference.write_text(json.dumps(self.manifest, ensure_ascii=False), encoding="utf-8")
        self.config["expected_reference_manifest_sha256"] = hashlib.sha256(reference.read_bytes()).hexdigest()
        self.config["expected_reference_records_sha256"] = records_sha
        # 실제 외부 원본 경로가 합성 fixture의 어느 출력에도 섞이지 않게 고정합니다.
        self.config["dataset_root"] = str(root / "합성원본")
        (root / "config.json").write_text(json.dumps(self.config, ensure_ascii=False), encoding="utf-8")
        (root / "run_training.py").write_text("# 합성\n", encoding="utf-8")
        (root / "src").mkdir()
        for source in (Path(__file__).resolve().parents[1] / "src").glob("*.py"):
            (root / "src" / source.name).write_bytes(source.read_bytes())
        self.run_id, _ = _run_identity(root, self.config, records_sha)
        self.result_dir = root / "work/results" / ("run_" + self.run_id)
        self.result_dir.mkdir(parents=True)
        (root / "work/results/dataset_manifest_private.json").write_text(json.dumps(self.manifest, ensure_ascii=False), encoding="utf-8")
        self.checkpoint_dir = root / "work/checkpoints" / ("run_" + self.run_id)
        self.privacy_order = []
        self.checkpoint_writes = []

    def execute(self, patch_privacy=True, sigmas=None):
        import torch
        from src import training
        from src.model import GaussianDCTBlur
        from src.state import StatusWriter
        models = []
        class TinyModel(torch.nn.Module):
            def __init__(self, sigma=0, **kwargs):
                super().__init__()
                self.blur = GaussianDCTBlur(sigma)
                self.head = torch.nn.Linear(1, 1)
                self.training_sigmas = []
                self.initial_digest = training.tensor_state_digest(self.state_dict())
                models.append(self)
            def forward(self, images):
                if self.training:
                    self.training_sigmas.append(self.blur.sigma)
                return self.head(images[:, :1, 0, 0]).squeeze(1)
        class TinyDataset:
            def __init__(self, records, image_size, training=False, **kwargs):
                # 선택적인 원본 클래스 진단은 위 실제 literal 회귀로 검사합니다.
                self.records, self.training = None, training
            def __len__(self):
                return 10000 if self.training else 2
            def set_epoch(self, epoch):
                self.epoch = epoch
        def loader(dataset, config, device):
            target = torch.tensor([0., 1.]).repeat(5000 if dataset.training else 1)
            # 학습 관계와 반대인 검증 입력으로 실제 검증 손실이 악화하는 합성 문제입니다.
            inputs = target*2-1 if dataset.training else 1-target*2
            class TinyLoader(list):
                pass
            value = TinyLoader([(inputs[:, None, None, None], target)])
            value.dataset = dataset
            return value
        def privacy(model, records, root, run_id, selection, state=None):
            from src.identity import SCORE_VERSION, validate_run
            from src.state import atomic_json
            from src.privacy import score_gallery
            import numpy as np
            sigma = selection["sigma"]
            self.privacy_order.append(sigma)
            raw_path = self.result_dir / f"sigma_{sigma}_privacy_groups_private.json"
            raw = score_gallery(np.array([[0., 1.], [1., 0.]]), [[0], [1]])
            metadata = validate_run(root, run_id)
            pipeline = {"protocol": selection["protocol"], "sigma": sigma, "checkpoint_sha256": selection["checkpoint_sha256"],
                        "model_state_sha256": selection["model_state_sha256"], "source_hashes": metadata["source_hashes"],
                        "precision": "fp32", "packet_batch_size": 1, "device": "cpu", "torch_version": "합성",
                        "shape_dtype_byteorder_in_hash": True, "manifest_sha256": metadata["manifest_sha256"], "encoder_state_sha256": "0"*64}
            atomic_json(raw_path, {"per_group": raw["per_group"], "distance_matrix": [[0., 1.], [1., 0.]],
                                   "pipeline": pipeline, "gallery_feature_hashes": ["0"*64, "1"*64], "query_feature_hashes": ["0"*64, "1"*64]})
            value = {**selection, **{k:v for k,v in raw.items() if k != "per_group"}, "score_version": SCORE_VERSION, "completed_at": "합성",
                     "privacy_source_sha256": metadata["source_hashes"]["src/privacy.py"], "attack_protocol": "known-encoder-closed-gallery-full-feature-bytehash-v1",
                     "precision": "fp32", "packet_batch_size": 1, "device": "cpu", "encoder_state_sha256": "0"*64,
                     "pipeline_sha256": hashlib.sha256(json.dumps(pipeline, sort_keys=True).encode()).hexdigest(),
                     "controls": {"original_score": 0., "constant_score": 100.},
                     "raw_file": {"relative_path": raw_path.relative_to(root).as_posix(), "sha256": hashlib.sha256(raw_path.read_bytes()).hexdigest()}}
            atomic_json(self.result_dir / f"sigma_{sigma}_privacy.json", value)
            return value
        import contextlib
        original_save = training._save_checkpoint
        def record_save(path, payload):
            self.checkpoint_writes.append((Path(path).name, payload["epoch"]))
            return original_save(path, payload)
        class MemoryStatus(StatusWriter):
            """1000회 통합에서는 상태값을 유지하고 반복 디스크 fsync만 분리합니다."""
            def update(self, **values):
                from src.state import now_kst
                self.data.update(values)
                self.data["updated_at"] = now_kst()
            def event(self, name, details=None):
                pass
        with contextlib.ExitStack() as stack:
            stack.enter_context(mock.patch.object(training, "_save_checkpoint", record_save))
            if sigmas is not None:
                stack.enter_context(mock.patch.object(training, "SIGMAS", sigmas))
            for name, replacement in [("prepare_dataset", lambda *a: self.manifest), ("CTDataset", TinyDataset), ("_loader", loader), ("SplitResNet50", TinyModel), ("precision_policy", lambda *a: {"name":"fp32", "dtype":torch.float32, "autocast_enabled":False, "use_grad_scaler":False})]:
                stack.enter_context(mock.patch.object(training, name, replacement))
            if patch_privacy:
                stack.enter_context(mock.patch.object(training, "run_privacy", privacy))
            state = MemoryStatus(self.root, self.config)
            result = training.run_training(self.config, self.root, state, "cpu")
        return result, models


if __name__ == "__main__":
    unittest.main()

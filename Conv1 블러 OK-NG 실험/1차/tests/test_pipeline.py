"""자료 누수·균형 표본·모델 절단·블러의 실제 동작을 검사합니다."""

import importlib
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock


def load_module(name):
    try:
        return importlib.import_module(name)
    except ModuleNotFoundError as exc:
        if exc.name in {"src", name}:
            raise AssertionError(f"아직 구현되지 않은 학습 모듈: {name}") from exc
        raise


def legacy_read_lock(path):
    """제품에서 쓰지 않는 삭제 공유 없는 Windows 핸들을 검사 목적으로 엽니다."""
    import ctypes
    from ctypes import wintypes
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    create_file = kernel.CreateFileW
    create_file.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, ctypes.c_void_p,
                            wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE]
    create_file.restype = wintypes.HANDLE
    close_handle = kernel.CloseHandle
    close_handle.argtypes = [wintypes.HANDLE]
    close_handle.restype = wintypes.BOOL
    handle = create_file(str(path), 0x80000000, 3, None, 3, 128, None)
    if handle == ctypes.c_void_p(-1).value:
        raise ctypes.WinError(ctypes.get_last_error())
    return lambda: close_handle(handle)


class DataTests(unittest.TestCase):
    def test_labels_map_benign_normal_to_ok(self):
        data = load_module("src.data")
        self.assertEqual([data.binary_label(x) for x in ["Bengin cases", "Normal cases", "Malignant cases"]], [0, 0, 1])
        with self.assertRaises(ValueError):
            data.binary_label("unconfirmed")

    def make_images(self, root, conflict=False):
        import numpy as np
        from PIL import Image
        for name, offset in [("Bengin cases", 0), ("Normal cases", 40), ("Malignant cases", 80)]:
            folder = root / name
            folder.mkdir()
            for i in range(20):
                pixels = np.full((16, 16), offset + i, dtype=np.uint8)
                pixels[0, 0] = 250
                Image.fromarray(pixels).save(folder / f"case ({i}).png")
        original = root / "Bengin cases" / "case (0).png"
        same_class = root / "Normal cases" / "same_pixels.bmp"
        with Image.open(original) as image:
            image.save(same_class)
        (root / "Normal cases" / "same_bytes.png").write_bytes(original.read_bytes())
        if conflict:
            (root / "Malignant cases" / "conflict.png").write_bytes(original.read_bytes())

    def test_bytes_and_decoded_pixels_never_cross_splits(self):
        data = load_module("src.data")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_images(root)
            manifest = data.discover_images(root)
            split = data.split_records(manifest, seed=42, validation_ratio=0.15, test_ratio=0.15)
            self.assertEqual(len(manifest), 62)
            self.assertEqual(sum(len(x) for x in split.values()), 62)
            for hash_name in ["byte_sha256", "pixel_sha256", "duplicate_group"]:
                owners = {}
                for part, rows in split.items():
                    for row in rows:
                        owners.setdefault(row[hash_name], set()).add(part)
                self.assertTrue(all(len(parts) == 1 for parts in owners.values()), hash_name)
            self.assertEqual(split, data.split_records(manifest, seed=42, validation_ratio=0.15, test_ratio=0.15))
            self.assertTrue(all({r["label"] for r in rows} == {0, 1} for rows in split.values()))

    def test_duplicate_label_conflict_fails_closed(self):
        data = load_module("src.data")
        with tempfile.TemporaryDirectory() as directory:
            self.make_images(Path(directory), conflict=True)
            with self.assertRaisesRegex(ValueError, "라벨"):
                data.discover_images(Path(directory))

    def test_balanced_epoch_is_exact_and_deterministic(self):
        data = load_module("src.data")
        rows = [{"label": 0, "path": f"ok{i}"} for i in range(3)] + [{"label": 1, "path": f"ng{i}"} for i in range(5)]
        plan = data.balanced_epoch_plan(rows, 5000, seed=42, epoch=0)
        self.assertEqual(len(plan), 10000)
        self.assertEqual(sum(rows[i]["label"] == 0 for i, _ in plan), 5000)
        self.assertEqual(sum(rows[i]["label"] == 1 for i, _ in plan), 5000)
        self.assertEqual(plan, data.balanced_epoch_plan(rows, 5000, seed=42, epoch=0))
        self.assertNotEqual(plan, data.balanced_epoch_plan(rows, 5000, seed=42, epoch=1))

    def test_validation_pixels_are_untouched_and_train_is_repeatable(self):
        import numpy as np
        import torch
        from PIL import Image
        data = load_module("src.data")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "ct.png"
            gray = np.arange(256, dtype=np.uint8).reshape(16, 16)
            Image.fromarray(gray).save(path)
            rows = [{"path": str(path), "label": 0}, {"path": str(path), "label": 1}]
            validation = data.CTDataset(rows, image_size=16, training=False)
            x1, y1 = validation[0]
            x2, _ = validation[0]
            self.assertTrue(torch.equal(x1, x2))
            self.assertTrue(np.array_equal(x1[0].numpy(), gray / np.float32(255)))
            self.assertEqual(y1.item(), 0)
            training = data.CTDataset(rows, image_size=16, training=True, samples_per_class=5, seed=42)
            training.set_epoch(3)
            a, _ = training[2]
            b, _ = training[2]
            self.assertTrue(torch.equal(a, b))

    def test_invalid_or_empty_data_is_rejected(self):
        data = load_module("src.data")
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                data.discover_images(Path(directory))
        with self.assertRaises(ValueError):
            data.balanced_epoch_plan([{"label": 0}], 5000, 42, 0)


class ModelTests(unittest.TestCase):
    def test_edge_contains_only_conv1_and_cloud_owns_bn(self):
        import torch
        model = load_module("src.model").SplitResNet50(sigma=0, pretrained=False)
        self.assertEqual(sum(isinstance(x, torch.nn.Conv2d) for x in model.edge.modules()), 1)
        self.assertFalse(any(isinstance(x, torch.nn.BatchNorm2d) for x in model.edge.modules()))
        self.assertTrue(any(isinstance(x, torch.nn.BatchNorm2d) for x in model.cloud.modules()))
        self.assertFalse(any(p.requires_grad for p in model.edge.parameters()))
        model.train()
        self.assertFalse(any(x.training for x in model.modules() if isinstance(x, torch.nn.BatchNorm2d)))
        trainable = [name for name, p in model.named_parameters() if p.requires_grad]
        self.assertTrue(trainable)
        self.assertTrue(all(name.startswith(("cloud.layer4.", "cloud.head.")) for name in trainable))

    def test_smoke_forward_has_only_cloud_gradients(self):
        import torch
        torch.set_num_threads(2)
        model = load_module("src.model").SplitResNet50(sigma=1, pretrained=False)
        model.train()
        output = model(torch.rand(2, 3, 64, 64))
        self.assertEqual(tuple(output.shape), (2,))
        torch.nn.functional.binary_cross_entropy_with_logits(output, torch.tensor([0.0, 1.0])).backward()
        self.assertTrue(all(p.grad is None for p in model.edge.parameters()))
        self.assertTrue(any(p.grad is not None for p in model.cloud.head.parameters()))

    def test_dct_blur_matches_independent_scipy_reference(self):
        import numpy as np
        import torch
        from scipy.fft import dctn, idctn
        blur = load_module("src.model").GaussianDCTBlur(2)
        rng = np.random.default_rng(9)
        original = rng.normal(size=(2, 3, 12, 16)).astype(np.float32)
        yy = np.pi * np.arange(12) / 12
        xx = np.pi * np.arange(16) / 16
        attenuation = np.exp(-2 * (yy[:, None] ** 2 + xx[None, :] ** 2))
        expected = idctn(dctn(original, type=2, norm="ortho", axes=(-2, -1)) * attenuation, type=2, norm="ortho", axes=(-2, -1))
        actual = blur(torch.from_numpy(original)).numpy()
        np.testing.assert_allclose(actual, expected, atol=2e-6, rtol=2e-5)

    def test_blur_identity_mean_and_sigma_strength(self):
        import torch
        GaussianDCTBlur = load_module("src.model").GaussianDCTBlur
        original = torch.arange(2 * 3 * 16 * 16).reshape(2, 3, 16, 16).float() / 100
        self.assertTrue(torch.equal(GaussianDCTBlur(0)(original), original))
        weak = GaussianDCTBlur(1)(original)
        strong = GaussianDCTBlur(8)(original)
        torch.testing.assert_close(weak.mean((-2, -1)), original.mean((-2, -1)), atol=2e-5, rtol=1e-5)
        self.assertLess(strong.var((-2, -1)).mean().item(), weak.var((-2, -1)).mean().item())
        for sigma in [-1, float("nan"), float("inf")]:
            with self.assertRaises(ValueError):
                GaussianDCTBlur(sigma)


class RuntimeTests(unittest.TestCase):
    def test_atomic_status_retries_only_transient_windows_lock(self):
        state_module = load_module("src.state")
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "status.json"
            state_module.atomic_json(destination, {"sequence": 0})
            replace = state_module.replace_file
            attempts = []

            def locked_then_available(source, target):
                attempts.append((source, target))
                if len(attempts) <= 2:
                    error = PermissionError("일시적인 Windows 읽기 잠금")
                    error.winerror = [5, 32][len(attempts) - 1]
                    raise error
                return replace(source, target)

            with mock.patch.object(state_module, "replace_file", side_effect=locked_then_available):
                state_module.atomic_json(destination, {"sequence": 1, "message": "완전한 상태"})
            self.assertEqual(len(attempts), 3)
            self.assertEqual(json.loads(destination.read_text(encoding="utf-8")), {"sequence": 1, "message": "완전한 상태"})
            self.assertFalse(list(Path(directory).glob("*.tmp")))

    def test_atomic_status_permanent_or_unrelated_error_is_not_hidden(self):
        state_module = load_module("src.state")
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "status.json"
            state_module.atomic_json(destination, {"sequence": 0})
            for code, expected_attempts in [(5, 7), (13, 1), (112, 1)]:
                with self.subTest(winerror=code):
                    error = PermissionError("영구 권한 또는 다른 오류") if code != 112 else OSError("디스크 공간 오류")
                    error.winerror = code
                    with mock.patch.object(state_module, "replace_file", side_effect=error) as replacement:
                        with self.assertRaises(type(error)) as caught:
                            state_module.atomic_json(destination, {"sequence": 99})
                    self.assertIs(caught.exception, error)
                    self.assertEqual(replacement.call_count, expected_attempts)
                    self.assertEqual(json.loads(destination.read_text(encoding="utf-8")), {"sequence": 0})
                    self.assertFalse(list(Path(directory).glob("*.tmp")))

    @unittest.skipUnless(os.name == "nt", "Windows 공유 삭제 제한 동시 읽기·쓰기 검사")
    def test_atomic_status_windows_reader_writer_500_updates(self):
        import threading
        import time
        import dashboard
        state_module = load_module("src.state")
        ready, stop = threading.Event(), threading.Event()
        failures, read_sequences, lock_conflicts = [], [], []
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "status.json"
            state_module.atomic_json(destination, {"sequence": 0, "data": "x" * 2048})

            def read_while_writing():
                first = True
                while not stop.is_set():
                    try:
                        # 실제 제품의 삭제 공유 reader로 500회 원자교체와 공존하는지 검사합니다.
                        with dashboard.open_status_file(destination) as stream:
                            payload = json.loads(stream.read().decode("utf-8"))
                            if len(payload["data"]) != 2048 or not isinstance(payload["sequence"], int):
                                failures.append("부분 상태 또는 잘못된 내용")
                            read_sequences.append(payload["sequence"])
                            ready.set()
                            time.sleep(0.03 if first else 0.0002)
                            first = False
                    except Exception as error:
                        failures.append(repr(error))
                        ready.set()
                        return
                    stop.wait(0.0005)

            reader = threading.Thread(target=read_while_writing, daemon=True)
            real_replace = state_module.replace_file

            def observed_replace(source, target):
                try:
                    return real_replace(source, target)
                except PermissionError as error:
                    lock_conflicts.append(getattr(error, "winerror", None))
                    raise

            reader.start()
            self.assertTrue(ready.wait(3), "동시 읽기 작업이 시작되지 않았습니다.")
            try:
                with mock.patch.object(state_module, "replace_file", side_effect=observed_replace):
                    for sequence in range(1, 501):
                        state_module.atomic_json(destination, {"sequence": sequence, "data": "x" * 2048})
            finally:
                stop.set()
                reader.join(timeout=3)
            self.assertFalse(reader.is_alive())
            self.assertFalse(failures, failures)
            self.assertGreater(len(read_sequences), 0)
            self.assertEqual(lock_conflicts, [], "제품 reader는 원자교체를 잠그지 않아야 합니다.")
            self.assertEqual(json.loads(destination.read_text(encoding="utf-8"))["sequence"], 500)
            self.assertFalse(list(Path(directory).glob("*.tmp")))

    @unittest.skipUnless(os.name == "nt", "Windows 기존 reader의 짧은 잠금 회복 검사")
    def test_atomic_status_legacy_read_lock_released_after_30ms_recovers(self):
        import threading
        state_module = load_module("src.state")
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "status.json"
            state_module.atomic_json(destination, {"sequence": 0})
            release = legacy_read_lock(destination)
            timer = threading.Timer(0.03, release)
            real_replace = state_module.replace_file
            conflicts = []

            def observed_replace(source, target):
                try:
                    return real_replace(source, target)
                except PermissionError as error:
                    conflicts.append(error.winerror)
                    raise

            timer.start()
            try:
                with mock.patch.object(state_module, "replace_file", side_effect=observed_replace):
                    state_module.atomic_json(destination, {"sequence": 1})
            finally:
                timer.join(timeout=2)
            self.assertFalse(timer.is_alive())
            self.assertGreater(len(conflicts), 0)
            self.assertEqual(json.loads(destination.read_text(encoding="utf-8")), {"sequence": 1})
            self.assertFalse(list(Path(directory).glob("*.tmp")))

    @unittest.skipUnless(os.name == "nt", "Windows 기존 reader의 영구 잠금 한계 검사")
    def test_atomic_status_legacy_permanent_read_lock_raises_at_retry_limit(self):
        state_module = load_module("src.state")
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "status.json"
            state_module.atomic_json(destination, {"sequence": 0})
            release = legacy_read_lock(destination)
            try:
                with self.assertRaises(PermissionError) as caught:
                    state_module.atomic_json(destination, {"sequence": 1})
            finally:
                release()
            self.assertIn(caught.exception.winerror, {5, 32})
            self.assertEqual(json.loads(destination.read_text(encoding="utf-8")), {"sequence": 0})
            self.assertFalse(list(Path(directory).glob("*.tmp")))

    def test_precision_dispatch_never_applies_fp16_scaling_to_bf16(self):
        import torch
        training = load_module("src.training")
        self.assertTrue(hasattr(training, "precision_policy"), "정밀도별 autocast/scaler 정책이 아직 없습니다.")
        bf16 = training.precision_policy("bf16", "cuda", bf16_supported=True)
        self.assertEqual(bf16["dtype"], torch.bfloat16)
        self.assertTrue(bf16["autocast_enabled"])
        self.assertFalse(bf16["use_grad_scaler"])
        fp16 = training.precision_policy("fp16", "cuda")
        self.assertEqual(fp16["dtype"], torch.float16)
        self.assertTrue(fp16["use_grad_scaler"])
        fp32 = training.precision_policy("fp32", "cpu")
        self.assertEqual(fp32["dtype"], torch.float32)
        self.assertFalse(fp32["autocast_enabled"])
        self.assertFalse(fp32["use_grad_scaler"])
        with self.assertRaises(RuntimeError):
            training.precision_policy("bf16", "cuda", bf16_supported=False)
        with self.assertRaises(ValueError):
            training.precision_policy("bf16", "cpu")
        with self.assertRaises(ValueError):
            training.precision_policy("unknown", "cuda")

    @unittest.skipUnless(__import__("torch").cuda.is_available(), "CUDA 전용 체크포인트 RNG 회귀 검사")
    def test_cuda_rng_resume_accepts_cuda_mapped_checkpoint(self):
        import torch
        training = load_module("src.training")
        self.assertTrue(hasattr(training, "restore_rng_state"), "RNG 장치 보정 재개 함수가 아직 없습니다.")
        original_cpu = torch.get_rng_state()
        original_cuda = torch.cuda.get_rng_state_all()
        try:
            torch.manual_seed(321)
            saved = {"torch_rng_state": torch.get_rng_state().cuda(),
                     "cuda_rng_state": [state.cuda() for state in torch.cuda.get_rng_state_all()]}
            expected = torch.rand(8, device="cuda")
            training.restore_rng_state(saved, torch.device("cuda"))
            actual = torch.rand(8, device="cuda")
            self.assertTrue(torch.equal(actual, expected))
        finally:
            torch.set_rng_state(original_cpu)
            torch.cuda.set_rng_state_all(original_cuda)

    def test_status_writes_valid_utf8_and_events(self):
        state_module = load_module("src.state")
        with tempfile.TemporaryDirectory() as directory:
            state = state_module.StatusWriter(Path(directory), {"epochs": 35, "sigmas": [0, 1]})
            state.update(stage="training", status="running", message="학습 중", epoch=1, batch=2)
            payload = json.loads((Path(directory) / "work/runtime/status.json").read_bytes().decode("utf-8"))
            self.assertEqual(payload["stage"], "training")
            self.assertEqual(payload["message"], "학습 중")
            self.assertEqual(payload["epoch"], 1)
            self.assertIn("updated_at", payload)
            self.assertEqual(payload["seen_per_class"], {"OK": 0, "NG": 0})
            state.event("학습상태", {"sigma": 0})
            events = (Path(directory) / "work/runtime/events.jsonl").read_text(encoding="utf-8").split("\n")
            self.assertEqual(json.loads(events[-2])["event"], "학습상태")
            self.assertFalse(list((Path(directory) / "work/runtime").glob("*.tmp")))

    def test_metrics_use_fixed_threshold_and_ng_positive_class(self):
        metrics = load_module("src.training").binary_metrics([0, 0, 1, 1], [0.1, 0.6, 0.7, 0.8])
        self.assertEqual(metrics["confusion_matrix"], [[1, 1], [0, 2]])
        self.assertEqual(metrics["accuracy"], 0.75)
        self.assertEqual(metrics["sensitivity"], 1.0)
        self.assertEqual(metrics["specificity"], 0.5)
        self.assertEqual(metrics["auc"], 1.0)


if __name__ == "__main__":
    unittest.main()

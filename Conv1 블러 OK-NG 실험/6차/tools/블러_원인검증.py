"""기존 원본을 읽기만 하여 블러 수식·재추론·고정 모델·DC 정보를 검증합니다."""

import argparse
import csv
from datetime import datetime, timedelta, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import sys
import time
import traceback
import warnings


ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get("CT_AUDIT_SOURCE_ROOT", str(ROOT.parent / "실제5차_학습복구")))
RUN_ID = os.environ.get("CT_AUDIT_RUN_ID", "")
RESULTS = SOURCE / "work/results" / ("run_" + RUN_ID)
CHECKPOINTS = SOURCE / "work/checkpoints" / ("run_" + RUN_ID)
WORK = ROOT / "work"
BASELINE = WORK / "초기_읽기전용_기준_비공개.json"
COMPLETE = WORK / "실험완료_비공개.json"
SIGMAS = [0, 4, 16, 64, 256]
REPRO_SIGMAS = [0, 4, 16, 256]
SIZES = {"train": 769, "validation": 164, "test": 164}
SESSION = os.environ.get("CT_AUDIT_SESSION", "local-audit")
TASK = "blur-validity-audit"
os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")
sys.path.insert(0, str(SOURCE))


def now():
    return datetime.now(timezone(timedelta(hours=9))).isoformat(timespec="seconds")


def digest(path):
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(4 * 1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def save_json(path, value):
    path = Path(path)
    if not path.resolve().is_relative_to(ROOT.resolve()):
        raise ValueError("6차 밖으로 결과를 저장할 수 없습니다.")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n")


def csv_rows(path):
    with Path(path).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def save_csv(path, rows):
    if not rows:
        raise ValueError("빈 결과 CSV는 저장하지 않습니다.")
    with Path(path).open("x", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def counters():
    for path in sorted((ROOT / ".codex/routing-state").glob("*.json")):
        value = read_json(path)
        if value.get("session_id") == SESSION and value.get("task_id") == TASK:
            if "repair_used" in value:
                return {key: value[key] for key in ("repair_used", "input_fix_used", "stop_failures", "verification_failures")}
    return {"repair_used": 0, "input_fix_used": 0, "stop_failures": 0, "verification_failures": 0}


def progress(stage, **values):
    print(json.dumps({"time_kst": now(), "stage": stage, **values}, ensure_ascii=False, allow_nan=False), flush=True)


def dependencies():
    global np, torch, dctn, idctn, expit, roc_auc_score, StandardScaler, LogisticRegression
    global GaussianDCTBlur, SplitResNet50, CTDataset, seed_everything
    import numpy as np
    import torch
    from scipy.fft import dctn, idctn
    from scipy.special import expit
    from sklearn.metrics import roc_auc_score
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LogisticRegression
    from src.model import GaussianDCTBlur, SplitResNet50
    from src.data import CTDataset
    from src.training import seed_everything


def get_manifest():
    manifest = read_json(SOURCE / "work/results/dataset_manifest_private.json")
    if {name: len(rows) for name, rows in manifest["splits"].items()} != SIZES:
        raise ValueError("사전 명세의 train769/validation164/test164와 다릅니다.")
    return manifest


def required_files():
    relative = ["run_training.py", "config.json", "src/__init__.py", "src/model.py", "src/data.py", "src/training.py", "src/state.py",
                "tools/feature_generator.py", "work/results/dataset_manifest_private.json",
                "work/results/run_" + RUN_ID + "/run_metadata.json"]
    config = read_json(SOURCE / "config.json")
    relative.append(config["expected_reference_manifest"])
    for sigma in REPRO_SIGMAS:
        relative += [f"work/checkpoints/run_{RUN_ID}/sigma_{sigma}_best.pt",
                     f"work/results/run_{RUN_ID}/sigma_{sigma}_metrics.json",
                     f"work/results/run_{RUN_ID}/sigma_{sigma}_test_predictions_private.csv"]
    return [SOURCE / name for name in relative]


def preflight():
    if BASELINE.exists():
        return check_baseline()
    if not (ROOT / ".codex/routing-project.json").is_file():
        raise ValueError("부모의 6차 프로젝트 활성화가 필요합니다.")
    manifest = get_manifest()
    meta = read_json(RESULTS / "run_metadata.json")
    config = read_json(SOURCE / "config.json")
    if meta["run_id"] != RUN_ID or meta["config"] != config:
        raise ValueError("기존 실행 metadata·설정이 일치하지 않습니다.")
    from src.training import _run_identity
    actual_id, settings = _run_identity(SOURCE, config, manifest["manifest_sha256"])
    if actual_id != RUN_ID or any(meta[key] != value for key, value in settings.items()):
        raise ValueError("기존 소스·설정·manifest의 실행 식별자와 다릅니다.")
    originals = []
    # 분할을 재설계하지 않고, 읽을 원본과 저장된 byte SHA만 대조합니다.
    data_root = Path(config["dataset_root"]).resolve()
    for row in manifest["records"]:
        path = Path(row["path"])
        if not path.resolve().is_relative_to(data_root) or path.is_symlink():
            raise ValueError("원본 경로가 확인한 자료 폴더 경계를 벗어났습니다.")
        if digest(path) != row["byte_sha256"]:
            raise ValueError("실험 전 원본 byte SHA가 저장 manifest와 다릅니다.")
        originals.append({"path": str(path), "sha256": row["byte_sha256"], "bytes": path.stat().st_size})
    value = {"created_at": now(), "session": SESSION, "task": TASK, "source_root": str(SOURCE), "run_id": RUN_ID,
             "source_files": [{"path": str(path), "sha256": digest(path), "bytes": path.stat().st_size} for path in required_files()],
             "original_files": originals, "split_sizes": SIZES, "settings": settings,
             "plan_sha256": digest(ROOT / "docs/추가실험_계획.md"), "counters": counters(),
             "baseline_policy": "최초 고정값이며 현재 파일로 교체하지 않습니다."}
    save_json(BASELINE, value)
    progress("baseline_frozen", source_files=len(value["source_files"]), original_files=len(originals), sha256=digest(BASELINE))
    return value


def check_baseline(originals=False):
    baseline = read_json(BASELINE)
    if baseline["session"] != SESSION or baseline["task"] != TASK or baseline["run_id"] != RUN_ID:
        raise ValueError("초기 기준의 session/task/run이 다릅니다.")
    for item in baseline["source_files"] + (baseline["original_files"] if originals else []):
        if digest(item["path"]) != item["sha256"]:
            raise ValueError("고정한 기존 입력 파일이 변경됐습니다: " + item["path"])
    if digest(ROOT / "docs/추가실험_계획.md") != baseline["plan_sha256"]:
        raise ValueError("결과 확인 전 고정한 계획이 변경됐습니다.")
    return baseline


def reference_blur(array, sigma):
    # 기존 Torch FFT 구현을 호출하지 않는 독립 SciPy 식입니다.
    value = np.asarray(array, dtype=np.float64)
    height, width = value.shape[-2:]
    y = np.arange(height, dtype=np.float64) * np.pi / height
    x = np.arange(width, dtype=np.float64) * np.pi / width
    transfer = np.exp(-0.5 * float(sigma) ** 2 * (y[:, None] ** 2 + x[None, :] ** 2))
    return idctn(dctn(value, type=2, axes=(-2, -1), norm="ortho") * transfer,
                 type=2, axes=(-2, -1), norm="ortho")


def math_checks(device="cpu"):
    rng = np.random.default_rng(42)
    rows = []
    for height, width in [(17, 19), (256, 256)]:
        impulse = np.zeros((height, width), dtype=np.float32)
        impulse[height // 2, width // 2] = 1
        signals = [("constant", np.full((height, width), 2.5, np.float32), None),
                   ("impulse", impulse, None),
                   ("random", rng.normal(size=(height, width)).astype(np.float32), None)]
        for ky, kx in [(1, 0), (0, 1), (3, 4), (height // 2, 0)]:
            mode = (np.cos(np.pi * (np.arange(height)[:, None] + 0.5) * ky / height)
                    * np.cos(np.pi * (np.arange(width)[None, :] + 0.5) * kx / width)).astype(np.float32)
            signals.append((f"cosine_{ky}_{kx}", mode, (ky, kx)))
        for name, signal, mode in signals:
            tensor = torch.tensor(signal[None, None], device=device)
            for sigma in SIGMAS:
                with torch.inference_mode():
                    actual = GaussianDCTBlur(sigma).to(device)(tensor).cpu().numpy()[0, 0].astype(np.float64)
                reference = reference_blur(signal, sigma)
                maximum_error = float(np.max(np.abs(actual - reference)))
                mean_error = abs(float(actual.mean() - signal.astype(np.float64).mean()))
                tolerance = 3e-5 * max(1.0, float(np.abs(signal).max()))
                if maximum_error > tolerance or mean_error > tolerance:
                    raise AssertionError(f"독립 DCT 대조 실패: {device}/{height}x{width}/{name}/{sigma}, {maximum_error}, {mean_error}")
                expected_gain = actual_gain = gain_error = None
                if mode is not None:
                    ky, kx = mode
                    expected_gain = math.exp(-0.5 * sigma ** 2 * math.pi ** 2 * ((ky / height) ** 2 + (kx / width) ** 2))
                    signal64 = signal.astype(np.float64)
                    actual_gain = float(np.sum(actual * signal64) / np.sum(signal64 ** 2))
                    gain_error = abs(actual_gain - expected_gain)
                    if gain_error > 3e-5:
                        raise AssertionError("코사인 주파수 이득이 사전 명세와 다릅니다.")
                rows.append({"device": device, "height": height, "width": width, "signal": name, "sigma": sigma,
                             "max_abs_error": maximum_error, "mean_abs_error": mean_error, "tolerance": tolerance,
                             "expected_gain": expected_gain, "actual_gain": actual_gain, "gain_abs_error": gain_error})
    if len(rows) != 70:
        raise AssertionError("수학 검사 조건 수가70이 아닙니다.")
    return {"n_cases": len(rows), "device": device, "max_abs_error": max(row["max_abs_error"] for row in rows),
            "max_mean_abs_error": max(row["mean_abs_error"] for row in rows), "cases": rows}


def metric_values(labels, logits, probabilities=None):
    y = np.asarray(labels, dtype=np.int64)
    z = np.asarray(logits, dtype=np.float64)
    p = expit(z) if probabilities is None else np.asarray(probabilities, dtype=np.float64)
    if not np.isfinite(z).all() or not np.isfinite(p).all() or y.shape != z.shape or y.shape != p.shape:
        raise ValueError("라벨·로짓·확률의 shape 또는 유한성이 잘못됐습니다.")
    predicted = (z >= 0).astype(np.int64)
    matrix = [[int(np.sum((y == a) & (predicted == b))) for b in (0, 1)] for a in (0, 1)]
    correct = int(np.sum(y == predicted))
    return {"correct": correct, "n_images": len(y), "accuracy": correct / len(y),
            "auc": float(roc_auc_score(y, z)), "confusion_matrix": matrix,
            "loss": float(np.logaddexp(0, -(2 * y - 1) * z).mean()),
            "logit_min": float(z.min()), "logit_max": float(z.max()),
            "threshold": 0.5, "logit_threshold": 0.0,
            "threshold_rounding_differences": int(np.sum(predicted != (p >= 0.5).astype(np.int64)))}


def prediction_rows(records, logits, probabilities):
    if len(records) != len(logits) or len(records) != len(probabilities):
        raise ValueError("예측 CSV의 원본 목록·값 수가 다릅니다.")
    return [{"relative_path": row["relative_path"], "label": row["label"], "logit": float(logit),
             "ng_probability": float(probability), "prediction": int(logit >= 0),
             "probability_prediction": int(probability >= 0.5)}
            for row, logit, probability in zip(records, logits, probabilities)]


def load_model(sigma, device):
    path = CHECKPOINTS / f"sigma_{sigma}_best.pt"
    baseline = read_json(BASELINE)
    known = {item["path"]: item["sha256"] for item in baseline["source_files"]}
    if str(path) not in known or digest(path) != known[str(path)]:
        raise ValueError("알려진 최초 SHA의 로컬 체크포인트만 읽을 수 있습니다.")
    saved = torch.load(path, map_location="cpu", weights_only=True)
    metrics = read_json(RESULTS / f"sigma_{sigma}_metrics.json")
    if saved["run_id"] != RUN_ID or saved["sigma"] != sigma or saved["epoch"] != metrics["best_epoch"]:
        raise ValueError("체크포인트의 실행·강도·선정 epoch가 기존 지표와 다릅니다.")
    model = SplitResNet50(sigma=sigma, pretrained=False).eval()
    model.load_state_dict(saved["model"], strict=True)
    return model.to(device), {"sigma": sigma, "epoch": saved["epoch"], "sha256": known[str(path)], "weights_only": True}


def infer(model, records, device):
    dataset = CTDataset(records, image_size=512, training=False)
    loader = torch.utils.data.DataLoader(dataset, batch_size=8, shuffle=False, num_workers=0)
    logits, probabilities = [], []
    with torch.inference_mode():
        for images, _ in loader:
            values = model(images.to(device).float()).double()
            logits.extend(values.cpu().tolist())
            probabilities.extend(values.sigmoid().cpu().tolist())
    return logits, probabilities


def compare_original(sigma, records, logits, probabilities):
    original = csv_rows(RESULTS / f"sigma_{sigma}_test_predictions_private.csv")
    if len(original) != len(records):
        raise AssertionError("원 CSV와 재추론 표본 수가 다릅니다.")
    if any(a["relative_path"] != b["relative_path"] or int(a["label"]) != b["label"] for a, b in zip(original, records)):
        raise AssertionError("원 CSV와 재추론 순서·라벨이 다릅니다.")
    old = np.asarray([float(row["ng_probability"]) for row in original])
    new = np.asarray(probabilities)
    prediction_mismatches = int(np.sum((old >= .5) != (np.asarray(logits) >= 0)))
    result = {"max_probability_abs_difference": float(np.max(np.abs(old - new))),
              "probabilities_within_prespecified_tolerance": bool(np.allclose(old, new, atol=2e-7, rtol=2e-5)),
              "prediction_mismatches": prediction_mismatches,
              "original_correct": int(np.sum((old >= .5) == np.asarray([row["label"] for row in records]))),
              "original_csv_has_logits": False}
    if prediction_mismatches or not result["probabilities_within_prespecified_tolerance"]:
        raise AssertionError("기존 CSV 확률·정답 재현이 사전 허용 범위를 벗어났습니다: " + json.dumps(result))
    return result


def cross_sigma(model, records, device, destination):
    # 각 모듈을 새로 만들어 강도 변경 때 기존 transfer 캐시를 재사용하지 않습니다.
    blurs = {sigma: GaussianDCTBlur(sigma).to(device) for sigma in SIGMAS}
    predictions = {sigma: {"logits": [], "probabilities": []} for sigma in SIGMAS}
    statistics = []
    dataset = CTDataset(records, image_size=512, training=False)
    loader = torch.utils.data.DataLoader(dataset, batch_size=8, shuffle=False, num_workers=0)
    offset = 0
    with torch.inference_mode():
        for images, _ in loader:
            images = images.to(device).float()
            features = model.edge((images - model.rgb_mean) / model.rgb_std)
            source64 = features.double()
            means = source64.mean(dim=(-2, -1), keepdim=True)
            base_ac = ((source64 - means) ** 2).mean(dim=(1, 2, 3))
            base_total = (source64 ** 2).mean(dim=(1, 2, 3))
            for sigma, blur in blurs.items():
                transmitted = blur(features)
                logits64 = model.cloud(transmitted).double()
                predictions[sigma]["logits"].extend(logits64.cpu().tolist())
                predictions[sigma]["probabilities"].extend(logits64.sigmoid().cpu().tolist())
                value64 = transmitted.double()
                new_means = value64.mean(dim=(-2, -1), keepdim=True)
                ac = ((value64 - new_means) ** 2).mean(dim=(1, 2, 3))
                mse = ((value64 - source64) ** 2).mean(dim=(1, 2, 3))
                arrays = {"base_ac_energy": base_ac, "ac_energy": ac,
                          "ac_retention_ratio": ac / base_ac,
                          "dc_energy": (new_means ** 2).mean(dim=(1, 2, 3)),
                          "total_energy": (value64 ** 2).mean(dim=(1, 2, 3)),
                          "relative_squared_change": mse / base_total,
                          "mse_from_unblurred": mse,
                          "max_channel_mean_abs_difference": (new_means - means).abs().amax(dim=(1, 2, 3))}
                arrays = {name: values.cpu().tolist() for name, values in arrays.items()}
                for index in range(len(images)):
                    row = records[offset + index]
                    statistics.append({"relative_path": row["relative_path"], "label": row["label"], "sigma": sigma,
                                       **{name: values[index] for name, values in arrays.items()}})
            offset += len(images)
            if offset == 8 or offset % 40 == 0 or offset == len(records):
                progress("cross_sigma", completed_images=offset, total_images=len(records))
    summary = {}
    for sigma in SIGMAS:
        selected = [row for row in statistics if row["sigma"] == sigma]
        summary[str(sigma)] = {key: float(np.mean([row[key] for row in selected])) for key in selected[0]
                               if key not in {"relative_path", "label", "sigma"}}
        summary[str(sigma)]["maximum_channel_mean_error"] = max(row["max_channel_mean_abs_difference"] for row in selected)
    save_csv(destination / "CT특징_공간통계_비공개.csv", statistics)
    return predictions, summary


def dc_experiment(model, splits, device, destination):
    descriptors, labels = {}, {}
    for name in ["train", "validation", "test"]:
        loader = torch.utils.data.DataLoader(CTDataset(splits[name], image_size=512, training=False),
                                             batch_size=8, shuffle=False, num_workers=0)
        values, targets = [], []
        with torch.inference_mode():
            for images, target in loader:
                features = model.edge((images.to(device).float() - model.rgb_mean) / model.rgb_std)
                values.append(features.double().mean(dim=(-2, -1)).cpu().numpy())
                targets.extend(target.int().tolist())
        descriptors[name] = np.concatenate(values, axis=0)
        labels[name] = np.asarray(targets, dtype=np.int64)
        progress("dc_extraction", split=name, n_images=len(targets), n_features=64)
    scaler = StandardScaler()
    scaled_train = scaler.fit_transform(descriptors["train"])
    classifier = LogisticRegression(C=1.0, solver="lbfgs", max_iter=2000, tol=1e-4, random_state=42)
    # validation/test 정보는 fit·표준화 추정·설정 선택에 사용하지 않습니다.
    with warnings.catch_warnings(record=True) as captured:
        warnings.simplefilter("always")
        classifier.fit(scaled_train, labels["train"])
    if captured or int(classifier.n_iter_.max()) >= 2000:
        diagnostic = {"n_iter": classifier.n_iter_.tolist(), "warnings": [str(item.message) for item in captured]}
        save_json(destination / "DC분류기_수렴진단_비공개.json", diagnostic)
        raise RuntimeError("DC 분류기의 수렴 경고 또는 반복 상한 도달: " + json.dumps(diagnostic, ensure_ascii=False))
    reports = {}
    for name in ["train", "validation", "test"]:
        transformed = scaler.transform(descriptors[name])
        logits = classifier.decision_function(transformed)
        probabilities = classifier.predict_proba(transformed)[:, 1]
        reports[name] = metric_values(labels[name], logits, probabilities)
        save_csv(destination / f"DC평균64_{name}_예측_비공개.csv",
                 prediction_rows(splits[name], logits, probabilities))
        save_csv(destination / f"DC평균64_{name}_특징_비공개.csv",
                 [{"relative_path": row["relative_path"], "label": row["label"],
                   **{f"channel_{channel}": float(value) for channel, value in enumerate(vector)}}
                  for row, vector in zip(splits[name], descriptors[name])])
    reports.update(n_features=64, fit_split="train", scaler_fit_split="train", n_fit=769,
                   parameters={"C": 1.0, "solver": "lbfgs", "max_iter": 2000, "tol": 1e-4, "seed": 42},
                   n_iter=classifier.n_iter_.tolist(), warnings=[str(item.message) for item in captured],
                   scaler_mean=scaler.mean_.tolist(), scaler_scale=scaler.scale_.tolist(),
                   coefficients=classifier.coef_.tolist(), intercept=classifier.intercept_.tolist())
    return reports


def experiment():
    baseline = check_baseline(originals=True)
    if COMPLETE.exists():
        raise FileExistsError("완료 결과는 덮어쓰지 않습니다. 검증 모드를 사용하세요.")
    if not torch.cuda.is_available():
        raise RuntimeError("확인한 CUDA 장치를 사용할 수 없습니다. CPU로 자동 대체하지 않습니다.")
    seed_everything(42, 4)
    started = time.monotonic()
    attempt = WORK / ("추가실험_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
    attempt.mkdir()
    save_json(attempt / "실행시작_비공개.json", {"time_kst": now(), "argv": [sys.executable, *sys.orig_argv[1:]],
              "cwd": os.getcwd(), "session": SESSION, "task": TASK, "counters": counters(),
              "runner_sha256": digest(__file__), "baseline_sha256": digest(BASELINE)})
    import scipy
    import sklearn
    download_calls = []
    def deny_download(*args, **kwargs):
        download_calls.append({"args": repr(args), "kwargs": repr(kwargs)})
        raise RuntimeError("이 실험은 외부 가중치 다운로드를 허용하지 않습니다.")
    torch.hub.download_url_to_file = deny_download
    environment = {"python": sys.version, "torch": torch.__version__, "scipy": scipy.__version__, "sklearn": sklearn.__version__,
                   "cuda": torch.version.cuda, "device": torch.cuda.get_device_name(0), "CPU_threads": torch.get_num_threads(),
                   "batch_size": 8, "forward_precision": "fp32", "probability_precision": "fp64", "seed": 42,
                   "deterministic": torch.are_deterministic_algorithms_enabled(), "CUBLAS_WORKSPACE_CONFIG": os.environ.get("CUBLAS_WORKSPACE_CONFIG"),
                   "CUDA_VISIBLE_DEVICES": os.environ.get("CUDA_VISIBLE_DEVICES")}
    progress("math_started")
    math_cpu = math_checks("cpu")
    math_cuda = math_checks("cuda")
    save_json(attempt / "독립_DCT_대조_비공개.json", {"cpu": math_cpu, "cuda": math_cuda})
    manifest = get_manifest()
    splits = manifest["splits"]
    device = torch.device("cuda")
    reproduction = {}
    timings = {}
    fixed = None
    for sigma in REPRO_SIGMAS:
        tick = time.monotonic()
        model, checkpoint = load_model(sigma, device)
        logits, probabilities = infer(model, splits["test"], device)
        metric = metric_values([row["label"] for row in splits["test"]], logits, probabilities)
        original_comparison = compare_original(sigma, splits["test"], logits, probabilities)
        saved = read_json(RESULTS / f"sigma_{sigma}_metrics.json")["test"]
        if metric["accuracy"] != saved["accuracy"] or metric["auc"] != saved["auc"]:
            raise AssertionError("원 지표와 추가 추론의 정확도/AUC가 다릅니다.")
        reproduction[str(sigma)] = {"checkpoint": checkpoint, "metrics": metric, "original_comparison": original_comparison,
                                    "loss_difference_from_saved": metric["loss"] - saved["loss"]}
        save_csv(attempt / f"재현_sigma{sigma}_test_예측_비공개.csv", prediction_rows(splits["test"], logits, probabilities))
        timings["reproduction_sigma" + str(sigma)] = time.monotonic() - tick
        progress("reproduction", sigma=sigma, correct=metric["correct"], n_images=164,
                 max_probability_difference=original_comparison["max_probability_abs_difference"], seconds=timings["reproduction_sigma" + str(sigma)])
        if sigma == 0:
            fixed = model
        else:
            del model
            torch.cuda.empty_cache()
    tick = time.monotonic()
    cross_predictions, feature_statistics = cross_sigma(fixed, splits["test"], device, attempt)
    cross = {}
    for sigma in SIGMAS:
        values = cross_predictions[sigma]
        cross[str(sigma)] = metric_values([row["label"] for row in splits["test"]], values["logits"], values["probabilities"])
        save_csv(attempt / f"고정sigma0_입력블러{sigma}_test_예측_비공개.csv",
                 prediction_rows(splits["test"], values["logits"], values["probabilities"]))
    timings["fixed_model_cross_sigma"] = time.monotonic() - tick
    # 분해 정방향이 원모델 정방향과 같은지 σ0 결과를 다시 대조합니다.
    zero_rows = csv_rows(attempt / "재현_sigma0_test_예측_비공개.csv")
    if not np.array_equal(np.asarray([float(row["logit"]) for row in zero_rows]), np.asarray(cross_predictions[0]["logits"])):
        raise AssertionError("고정 모델의 σ0 분해 정방향이 재현 정방향과 다릅니다.")
    tick = time.monotonic()
    dc = dc_experiment(fixed, splits, device, attempt)
    timings["dc_experiment"] = time.monotonic() - tick
    check_baseline(originals=True)
    report = {"schema_version": 1, "completed_at": now(), "session": SESSION, "task": TASK, "run_id": RUN_ID,
              "runner_sha256": digest(__file__), "baseline_sha256": digest(BASELINE), "environment": environment,
              "reproduction": reproduction, "fixed_sigma0_cross_sigma": cross, "feature_statistics": feature_statistics,
              "dc_only": dc, "math": {"cpu_cases": math_cpu["n_cases"], "cuda_cases": math_cuda["n_cases"],
                                        "cpu_max_abs_error": math_cpu["max_abs_error"], "cuda_max_abs_error": math_cuda["max_abs_error"]},
              "download_calls": len(download_calls), "timings_seconds": timings, "elapsed_seconds": time.monotonic() - started,
              "counters_at_run": counters(), "source_file_count": len(baseline["source_files"]), "original_file_count": len(baseline["original_files"]),
              "limitations": ["같은 기존 시험셋의 재사용 탐색적 진단; 결과를 본 튜닝 없음", "환자 ID 없어 환자 독립·임상·프라이버시 달성 미검증",
                              "DC 단서의 예측력은 원모델의 유일한 인과 사용 증명이 아님", "클래스당5000은 온라인 반복 표본"]}
    save_json(attempt / "실측결과_비공개.json", report)
    products = [{"relative_path": path.relative_to(ROOT).as_posix(), "sha256": digest(path), "bytes": path.stat().st_size}
                for path in sorted(attempt.iterdir()) if path.is_file()]
    save_json(COMPLETE, {"completed_at": now(), "session": SESSION, "task": TASK, "run_id": RUN_ID,
                        "baseline_sha256": digest(BASELINE), "runner_sha256": digest(__file__),
                        "report": (attempt / "실측결과_비공개.json").relative_to(ROOT).as_posix(), "products": products})
    progress("experiment_complete", elapsed_seconds=report["elapsed_seconds"], products=len(products), download_calls=len(download_calls))


def verify_results():
    tick = time.monotonic()
    baseline = check_baseline(originals=True)
    complete = read_json(COMPLETE)
    if complete["session"] != SESSION or complete["task"] != TASK or complete["run_id"] != RUN_ID:
        raise AssertionError("완료 결과의 session/task/run이 다릅니다.")
    if complete["runner_sha256"] != digest(__file__) or complete["baseline_sha256"] != digest(BASELINE):
        raise AssertionError("완료 결과의 최종 소스 또는 최초 기준 SHA가 다릅니다.")
    for item in complete["products"]:
        path = (ROOT / item["relative_path"]).resolve()
        if not path.is_relative_to(WORK.resolve()) or digest(path) != item["sha256"] or path.stat().st_size != item["bytes"]:
            raise AssertionError("완료 산출물의 경계·SHA·크기가 다릅니다.")
    report = read_json(ROOT / complete["report"])
    attempt = (ROOT / complete["report"]).parent
    if report["download_calls"] != 0 or report["runner_sha256"] != digest(__file__) or report["baseline_sha256"] != digest(BASELINE):
        raise AssertionError("다운로드0·최종 소스·초기 기준 조건이 다릅니다.")
    manifest = get_manifest()
    checked = 0
    for prefix, sigmas, key in [("재현_sigma", REPRO_SIGMAS, "reproduction"), ("고정sigma0_입력블러", SIGMAS, "fixed_sigma0_cross_sigma")]:
        for sigma in sigmas:
            rows = csv_rows(attempt / f"{prefix}{sigma}_test_예측_비공개.csv")
            if len(rows) != 164 or any(row["relative_path"] != source["relative_path"] or int(row["label"]) != source["label"]
                                       for row, source in zip(rows, manifest["splits"]["test"])):
                raise AssertionError("시험 CSV 행수·순서·라벨이 다릅니다.")
            metrics = metric_values([int(row["label"]) for row in rows], [float(row["logit"]) for row in rows], [float(row["ng_probability"]) for row in rows])
            expected = report[key][str(sigma)]["metrics"] if key == "reproduction" else report[key][str(sigma)]
            if metrics != expected:
                raise AssertionError("CSV 재계산 지표와 저장 JSON이 다릅니다.")
            if key == "reproduction":
                compare_original(sigma, manifest["splits"]["test"], [float(row["logit"]) for row in rows], [float(row["ng_probability"]) for row in rows])
            checked += len(rows)
    for name, size in SIZES.items():
        rows = csv_rows(attempt / f"DC평균64_{name}_예측_비공개.csv")
        features = csv_rows(attempt / f"DC평균64_{name}_특징_비공개.csv")
        if len(rows) != size or len(features) != size:
            raise AssertionError("DC 예측 또는 특징 행수가 다릅니다.")
        if any(row["relative_path"] != original["relative_path"] or int(row["label"]) != original["label"] for row, original in zip(rows, manifest["splits"][name])):
            raise AssertionError("DC 예측 순서·라벨이 원분할과 다릅니다.")
        if any(len(row) != 66 for row in features):
            raise AssertionError("DC 특징이64개가 아닙니다.")
        metrics = metric_values([int(row["label"]) for row in rows], [float(row["logit"]) for row in rows], [float(row["ng_probability"]) for row in rows])
        if metrics != report["dc_only"][name]:
            raise AssertionError("DC CSV 재계산 지표와 JSON이 다릅니다.")
        checked += size
    stats = csv_rows(attempt / "CT특징_공간통계_비공개.csv")
    if len(stats) != 820 or {int(row["sigma"]) for row in stats} != set(SIGMAS):
        raise AssertionError("실제 CT 공간 통계의 조건/행수가 다릅니다.")
    independent = math_checks("cpu")
    saved_math = read_json(attempt / "독립_DCT_대조_비공개.json")
    if independent != saved_math["cpu"] or saved_math["cuda"]["n_cases"] != 70:
        raise AssertionError("독립 CPU 수학 재실행이 저장 결과와 다릅니다.")
    # 별도 검증자가 이 명령과 구현·설계를 대조하며 자기 승인 영수증은 만들지 않습니다.
    progress("verify_results_pass", prediction_rows=checked, feature_stat_rows=len(stats), math_cases=independent["n_cases"],
             baseline_files=len(baseline["source_files"]), originals=len(baseline["original_files"]), elapsed_seconds=time.monotonic() - tick)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--preflight", action="store_true")
    modes.add_argument("--run", action="store_true")
    modes.add_argument("--math-only", action="store_true")
    modes.add_argument("--verify-results", action="store_true")
    args = parser.parse_args()
    dependencies()
    if args.preflight:
        preflight()
    elif args.math_only:
        seed_everything(42, 4)
        value = math_checks("cpu")
        progress("math_pass", n_cases=value["n_cases"], max_abs_error=value["max_abs_error"])
    elif args.verify_results:
        seed_everything(42, 4)
        verify_results()
    else:
        experiment()
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception:
        failure = {"time_kst": now(), "session": SESSION, "task": TASK,
                   "argv": [sys.executable, *sys.orig_argv[1:]], "cwd": os.getcwd(), "exit_code": 1,
                   "error": traceback.format_exc(), "changes_at_failure": "6차 추가 runner/계획만 변경; 기존5차 읽기 전용",
                   **counters()}
        WORK.mkdir(exist_ok=True)
        with (WORK / "실험실패_비공개.jsonl").open("a", encoding="utf-8", newline="\n") as stream:
            stream.write(json.dumps(failure, ensure_ascii=False) + "\n")
        traceback.print_exc()
        raise SystemExit(1)

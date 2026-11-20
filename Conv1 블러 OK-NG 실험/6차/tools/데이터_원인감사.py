"""보존한 원영상·분할을 읽어 저차원 단서와 중복 경계를 탐색합니다."""

import argparse
from collections import Counter
from datetime import datetime, timedelta, timezone
import hashlib
import io
import json
import math
import os
from pathlib import Path
import sys
import time
import traceback
import warnings

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

import numpy as np
import PIL
from PIL import Image
import scipy
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components
from scipy.spatial.distance import cdist
import sklearn
from sklearn.exceptions import ConvergenceWarning
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from threadpoolctl import threadpool_limits


PERCENTILES = [1, 5, 10, 25, 50, 75, 90, 95, 99]
FEATURE_NAMES = ["mean", "std_ddof0", "min", "max"] + [f"p{x}" for x in PERCENTILES] + [f"hist_{x:02d}" for x in range(32)]
SPLITS = ["train", "validation", "test"]


def kst():
    return datetime.now(timezone(timedelta(hours=9))).isoformat()


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(path, report):
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8", newline="\n")


def statistics(pixels):
    """촬영 크기·파일명·폴더 라벨을 입력하지 않고 픽셀 분포만 요약합니다."""
    x = np.asarray(pixels, dtype=np.uint8).reshape(-1)
    histogram = np.histogram(x, bins=32, range=(0, 256))[0].astype(np.float64) / len(x)
    summary = np.array([x.mean(), x.std(ddof=0), x.min(), x.max()], dtype=np.float64) / 255.0
    percentiles = np.percentile(x, PERCENTILES, method="linear") / 255.0
    return np.concatenate([summary, percentiles, histogram])


def border_pixels(pixels):
    """원해상도 가로·세로 각각 바깥쪽 5%를 모서리 중복 없이 사용합니다."""
    height, width = pixels.shape
    by, bx = max(1, math.ceil(height * 0.05)), max(1, math.ceil(width * 0.05))
    mask = np.ones((height, width), dtype=bool)
    mask[by:height - by, bx:width - bx] = False
    return pixels[mask]


def metrics(y, predicted, scores):
    matrix = confusion_matrix(y, predicted, labels=[0, 1])
    tn, fp, fn, tp = [int(x) for x in matrix.ravel()]
    correct = tn + tp
    total = len(y)
    return {"correct": correct, "total": total, "accuracy": correct / total,
            "accuracy_percent_rounded": f"{100 * correct / total:.1f}%", "auc": float(roc_auc_score(y, scores)),
            "confusion_matrix": matrix.tolist(), "sensitivity": tp / (tp + fn), "specificity": tn / (tn + fp)}


def fit_experiment(features, labels, indices, fit_labels):
    """표준화와 분류기 학습 모두 train 원본에만 적합합니다."""
    pipe = Pipeline([("scale", StandardScaler()), ("logreg", LogisticRegression(C=1.0, random_state=42, max_iter=2000,
                                                                                 solver="lbfgs", tol=1e-4, class_weight=None))])
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always", ConvergenceWarning)
        pipe.fit(features[indices["train"]], fit_labels)
    warnings_text = [str(x.message) for x in caught]
    result = {"feature_count": features.shape[1], "fit_count": int(pipe.named_steps["scale"].n_samples_seen_),
              "fit_n_iter": pipe.named_steps["logreg"].n_iter_.tolist(), "warnings": warnings_text,
              "converged": not any(issubclass(x.category, ConvergenceWarning) for x in caught),
              "scaler_mean_sha256": sha(pipe.named_steps["scale"].mean_.astype("<f8").tobytes()),
              "scaler_var_sha256": sha(pipe.named_steps["scale"].var_.astype("<f8").tobytes()),
              "train_only_scaler_mean_matches": bool(np.allclose(pipe.named_steps["scale"].mean_, features[indices["train"]].mean(axis=0), rtol=1e-12, atol=1e-15)),
              "evaluation": {}}
    for split in SPLITS:
        ix = indices[split]
        scores = pipe.decision_function(features[ix])
        predicted = (scores > 0.0).astype(int)
        result["evaluation"][split] = metrics(labels[ix], predicted, scores)
    return result


def self_check():
    image = np.zeros((100, 100), dtype=np.uint8)
    image[5:95, 5:95] = 255
    assert len(border_pixels(image)) == 1900 and np.max(border_pixels(image)) == 0
    stats = statistics(np.array([0, 255], dtype=np.uint8))
    assert len(stats) == 45 and stats[0] == 0.5 and np.isclose(stats[13:].sum(), 1)
    result = metrics(np.array([0, 0, 1, 1]), np.array([0, 1, 0, 1]), np.array([-2., 1., -1., 2.]))
    assert result["confusion_matrix"] == [[1, 1], [1, 1]] and result["correct"] == 2 and result["auc"] == 0.75
    print(json.dumps({"self_check": "PASS", "checks": 3}, ensure_ascii=False), flush=True)


def execute(args, report, output):
    started = time.monotonic()
    source = Path(args.source_root).resolve()
    manifest_path = source / "work/results/dataset_manifest_private.json"
    raw_manifest = manifest_path.read_bytes()
    manifest = json.loads(raw_manifest.decode("utf-8", errors="strict"))
    rows = manifest["records"]
    required = {"path", "relative_path", "source_class", "label", "byte_sha256", "pixel_sha256", "width", "height", "similarity_descriptor_sha256", "exact_duplicate_group", "similarity_group"}
    assert all(required <= set(row) for row in rows), "원본 manifest 스키마 누락"
    assert len(rows) == 1097 and set(manifest["splits"]) == set(SPLITS), "원본 수·분할이 승인 범위와 다름"
    guard_paths = [source / "config.json", source / "run_training.py", *sorted((source / "src").glob("*.py")), source / "work/runtime/status.json", manifest_path]
    guard_before = {str(p.relative_to(source)): sha(p.read_bytes()) for p in guard_paths}
    report.update(status="실행중", started_at_kst=kst(), actual_argv=sys.orig_argv, cwd=str(Path.cwd()),
                  executor_role="새 감사실행기 구현자; 자기 독립검증·중앙영수증 아님", source_root=str(source),
                  source_manifest={"bytes": len(raw_manifest), "file_sha256": sha(raw_manifest), "manifest_sha256": manifest["manifest_sha256"]},
                  schema={"root_fields": list(manifest), "record_fields": sorted(required)},
                  script_sha256=sha(Path(__file__).read_bytes()), package_versions={"python": sys.version, "numpy": np.__version__, "Pillow": PIL.__version__, "scipy": scipy.__version__, "scikit_learn": sklearn.__version__},
                  fixed_conditions={"feature_names": FEATURE_NAMES, "feature_count": len(FEATURE_NAMES), "intensity": "Pillow.convert('L'), native resolution, no augmentation", "statistics": "mean/std(ddof0)/min/max/percentiles(linear)/normalized32bins[0,256)", "border": "outer5% width+height using ceil/min1; corner pixels once", "scaler": "StandardScaler fit only train769", "logreg": {"C": 1, "solver": "lbfgs", "random_state": 42, "max_iter": 2000, "tol": 1e-4, "class_weight": None, "default_penalty": "l2"}, "prediction_threshold": "decision_function>0 (probability>0.5); exact zero→class0, sklearn binary predict rule", "shuffle_seeds": list(range(42, 52)), "grouping": "64x64 Pillow BILINEAR uint8; direct squared Euclidean float64; RMSE<=5; connected components", "tuning": "none; no validation/test fitting or parameter selection", "cpu_threads": 1},
                  official_references=["https://scikit-learn.org/stable/common_pitfalls.html", "https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html"])
    save(output, report)
    print("원영상 무결성·통계 읽기 시작", flush=True)
    descriptors, whole, border = [], [], []
    actual_rows = []
    source_sha_hasher = hashlib.sha256()
    for index, row in enumerate(rows):
        path = Path(row["path"])
        raw = path.read_bytes()
        assert sha(raw) == row["byte_sha256"], "원영상 byte SHA 불일치"
        with Image.open(io.BytesIO(raw)) as image:
            gray = image.convert("L")
            width, height = gray.size
            pixels = np.asarray(gray, dtype=np.uint8)
            pixel_sha = sha(f"L:{width}:{height}:".encode() + gray.tobytes())
            thumb = np.asarray(gray.resize((64, 64), Image.Resampling.BILINEAR), dtype=np.uint8)
        assert pixel_sha == row["pixel_sha256"] and (width, height) == (row["width"], row["height"]), "픽셀 SHA·크기 불일치"
        assert sha(thumb.tobytes()) == row["similarity_descriptor_sha256"], "유사 descriptor SHA 불일치"
        source_sha_hasher.update(row["relative_path"].encode("utf-8") + b"\0" + bytes.fromhex(sha(raw)))
        descriptors.append(thumb.reshape(-1).astype(np.float64))
        whole.append(statistics(pixels))
        border.append(statistics(border_pixels(pixels)))
        actual_rows.append({"relative_path": row["relative_path"], "byte_sha256": sha(raw), "pixel_sha256": pixel_sha})
        if (index + 1) % 200 == 0 or index + 1 == len(rows):
            print(f"원영상 {index + 1}/{len(rows)} 읽기 완료", flush=True)
    names = [r["relative_path"] for r in rows]
    assert len(set(names)) == len(names), "manifest 원본 상대경로 중복"
    name_to_index = {name: i for i, name in enumerate(names)}
    labels = np.array([r["label"] for r in rows], dtype=int)
    assert set(labels) == {0, 1}, "이진 라벨 이외 값"
    indices = {split: np.array([name_to_index[r["relative_path"]] for r in sorted(manifest["splits"][split], key=lambda r: r["relative_path"])], dtype=int) for split in SPLITS}
    all_indices = [int(i) for values in indices.values() for i in values]
    assert len(all_indices) == len(rows) and len(set(all_indices)) == len(rows), "분할 누락·중복"
    for split in SPLITS:
        assert all(r == rows[name_to_index[r["relative_path"]]] for r in manifest["splits"][split]), "분할 행과 원본 행 불일치"
    assert [len(indices[s]) for s in SPLITS] == [769, 164, 164], "분할 수 불일치"
    split_summary = {}
    for split in SPLITS:
        split_rows = [rows[i] for i in indices[split]]
        counts = Counter(r["label"] for r in split_rows)
        split_summary[split] = {"total": len(split_rows), "OK": counts[0], "NG": counts[1], "source_class": dict(Counter(r["source_class"] for r in split_rows))}
    print("64픽셀 직접 거리와 연결성분 계산", flush=True)
    descriptors = np.asarray(descriptors)
    distance_squared = cdist(descriptors, descriptors, metric="sqeuclidean")
    n_components, components = connected_components(csr_matrix(distance_squared <= 25 * 4096), directed=False)
    group_id = {int(c): min(rows[i]["pixel_sha256"] for i in np.flatnonzero(components == c)) for c in np.unique(components)}
    actual_groups = [group_id[int(c)] for c in components]
    group_match = all(g == row["similarity_group"] for g, row in zip(actual_groups, rows))
    assert group_match, "독립 연결성분과 manifest 유사그룹 불일치"
    assert all(len(set(labels[components == c])) == 1 for c in np.unique(components)), "유사그룹 라벨 충돌"
    cross_overlap = {}
    for left, right in [("train", "validation"), ("train", "test"), ("validation", "test")]:
        values = {}
        for key in ["relative_path", "byte_sha256", "pixel_sha256", "exact_duplicate_group", "similarity_group"]:
            values[key] = len({rows[i][key] for i in indices[left]} & {rows[i][key] for i in indices[right]})
        values["independent_similarity_components"] = len({actual_groups[i] for i in indices[left]} & {actual_groups[i] for i in indices[right]})
        cross_overlap[left + "__" + right] = values
    assert all(value == 0 for pair in cross_overlap.values() for value in pair.values()), "분할간 교차 겹침 발견"
    nearest = {}
    for split in ["validation", "test"]:
        distances = distance_squared[np.ix_(indices[split], indices["train"])]
        closest = distances.argmin(axis=1)
        nearest_sq = distances[np.arange(len(closest)), closest]
        rmse = np.sqrt(nearest_sq / 4096)
        predicted = labels[indices["train"]][closest]
        nearest[split] = {"rmse_min": float(rmse.min()), "rmse_median": float(np.median(rmse)), "rmse_max": float(rmse.max()),
                          "count_le_5": int((rmse <= 5).sum()), "count_le_10": int((rmse <= 10).sum()), "count_le_15": int((rmse <= 15).sum()),
                          "ties_for_nearest_count": int(np.sum(np.sum(distances == nearest_sq[:, None], axis=1) > 1)),
                          "tie_break": "lexicographically first train relative_path; fixed before evaluation",
                          "one_nn": metrics(labels[indices[split]], predicted, predicted), "auc_score": "binary nearest-train label; no calibrated probability"}
    global_features, border_features = np.asarray(whole), np.asarray(border)
    assert global_features.shape == border_features.shape == (1097, 45) and np.isfinite(global_features).all() and np.isfinite(border_features).all(), "특징 수·유한성 불일치"
    report.update(integrity={"all_images_byte_pixel_descriptor_verified": 1097, "aggregate_ordered_path_and_bytes_sha256": source_sha_hasher.hexdigest(),
                             "source_counts": dict(Counter(r["source_class"] for r in rows)), "split_summary": split_summary, "cross_overlap": cross_overlap,
                             "independent_similarity_group_count": int(n_components), "similarity_group_matches_manifest": group_match,
                             "unique_pixel_sha256": len({r["pixel_sha256"] for r in rows}), "unique_byte_sha256": len({r["byte_sha256"] for r in rows}),
                             "largest_similarity_group": int(np.bincount(components).max())}, nearest_train=nearest,
                  feature_matrix_sha256={"global_intensity": sha(global_features.astype("<f8").tobytes()), "border_intensity": sha(border_features.astype("<f8").tobytes())})
    save(output, report)
    print("고정 로지스틱 회귀: 전체통계·테두리통계·label shuffle10회", flush=True)
    train_labels = labels[indices["train"]]
    with threadpool_limits(limits=1):
        global_result = fit_experiment(global_features, labels, indices, train_labels)
        border_result = fit_experiment(border_features, labels, indices, train_labels)
        shuffled = []
        for seed in range(42, 52):
            permuted = np.random.default_rng(seed).permutation(train_labels)
            assert Counter(permuted) == Counter(train_labels), "shuffle 라벨 수 변경"
            result = fit_experiment(global_features, labels, indices, permuted)
            result.update(seed=seed, train_label_equal_original_count=int(np.sum(permuted == train_labels)),
                          shuffled_train_labels_sha256=sha(permuted.astype("<i8").tobytes()),
                          train_evaluation_target="original true labels, not shuffled labels; val/test original unchanged")
            shuffled.append(result)
            print(f"shuffle seed{seed}: test {result['evaluation']['test']['accuracy_percent_rounded']}", flush=True)
    shuffle_summary = {}
    for split in SPLITS:
        accuracies = np.array([r["evaluation"][split]["accuracy"] for r in shuffled])
        aucs = np.array([r["evaluation"][split]["auc"] for r in shuffled])
        shuffle_summary[split] = {"runs": 10, "accuracy_mean": float(accuracies.mean()), "accuracy_std_ddof0": float(accuracies.std()), "accuracy_min": float(accuracies.min()), "accuracy_max": float(accuracies.max()), "auc_mean": float(aucs.mean()), "auc_std_ddof0": float(aucs.std()), "correct_sum_across10_correlated_runs": sum(r["evaluation"][split]["correct"] for r in shuffled), "total_sum_across10_correlated_runs": 10 * len(indices[split]), "note": "동일 평가영상 반복으로 독립 표본 증가·통계적 유의성 검정 아님"}
    assert all(r["converged"] and r["fit_count"] == 769 and r["train_only_scaler_mean_matches"] for r in [global_result, border_result, *shuffled]), "수렴·학습전용 scaler 검증 실패"
    print("기존 입력·소스 바이트 재확인", flush=True)
    guard_after = {str(p.relative_to(source)): sha(p.read_bytes()) for p in guard_paths}
    assert guard_before == guard_after, "실행 중 기존 소스·설정·manifest·상태 변경"
    unchanged_images = sum(sha(Path(row["path"]).read_bytes()) == row["byte_sha256"] for row in rows)
    assert unchanged_images == 1097, "실행 후 원영상 바이트 변경"
    report.update(status="완료", outcome="PASS", completed_at_kst=kst(), elapsed_seconds=time.monotonic() - started,
                  experiments={"global_intensity_logreg": global_result, "border_only_logreg": border_result,
                               "global_intensity_train_label_shuffle": shuffled, "shuffle_summary": shuffle_summary},
                  preservation={"source_settings_manifest_state_before": guard_before, "source_settings_manifest_state_after": guard_after, "unchanged_original_images": unchanged_images, "existing5_root_write_calls": 0},
                  majority_baseline={split: {"accuracy": max(Counter(labels[indices[split]]).values()) / len(indices[split]), "note": "분할 내 다수 라벨 비율을 설명하는 참고값; 시험으로 모델 선택 없음"} for split in SPLITS},
                  limitations=["환자 ID·기관·스캐너 정보가 없습니다. 중복·유사그룹 교차0은 환자 독립성을 보장하지 않습니다.",
                               "전체 밝기 통계와 테두리 단서로 분류돼도 촬영기관 원인 또는 기존 ResNet의 인과적 사용을 확정하지 못합니다.",
                               "테두리에도 인체 조직이 포함될 수 있어 비의학 정보만의 실험이라고 단정하지 않습니다.",
                               "같은 validation/test의 추가 탐색 재사용입니다. 독립 외부검증·임상성능·프라이버시효과 검증이 아닙니다.",
                               "shuffle10회는 낮은 차원의 고정모델 음성대조입니다. 낮은 결과는 모든 종류의 누수 부재를 증명하지 못합니다.",
                               "서로 다른 shuffle 모델은 같은 평가영상을 사용합니다. 10회 합산을1640개의 독립 시험영상으로 해석하지 않습니다.",
                               "영상 원본해상도의 통계이며 기존 ResNet의512픽셀 입력·채널별 DC 특징과는 다른 실험입니다.",
                               "원본을 바꾸거나 새 분할을 만들지 않았습니다. 그룹 threshold·특징·초매개변수·임계값을 평가결과로 튜닝하지 않았습니다.",
                               "새 실행기 구현자의 직접 실행 결과입니다. 별도 verifier의 독립검증·중앙영수증은 부모가 별도 조율합니다."],
                  expected_exit_code=0)
    save(output, report)
    print(json.dumps({"outcome": "PASS", "images": len(rows), "group_count": int(n_components), "splits": split_summary, "global": global_result["evaluation"], "border": border_result["evaluation"], "nearest": nearest, "shuffle_summary": shuffle_summary, "elapsed_seconds": report["elapsed_seconds"], "output": str(output)}, ensure_ascii=False), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", required=False)
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    if args.self_check:
        self_check()
        return
    if not args.source_root:
        parser.error("--source-root 필요")
    output = Path(__file__).resolve().with_name("데이터원인_독립감사_비공개.json")
    report = json.loads(output.read_text(encoding="utf-8", errors="strict")) if output.exists() else {"schema_version": 1, "failures": []}
    try:
        execute(args, report, output)
    except Exception:
        error = traceback.format_exc()
        report["status"] = "실패"
        report["outcome"] = "FAIL"
        report.setdefault("failures", []).append({"observed_at_kst": kst(), "task": "데이터 원인 감사", "actual_argv": sys.orig_argv,
                                                    "cwd": str(Path.cwd()), "exit_code": 1, "error": error, "source_modified": False,
                                                    "repair_used_local": report.get("repair_used_local", 0), "input_fix_used_local": report.get("input_fix_used_local", 0)})
        save(output, report)
        raise


if __name__ == "__main__":
    main()

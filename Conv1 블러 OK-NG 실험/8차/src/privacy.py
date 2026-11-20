"""원본 후보가 있는 알려진 encoder 공격과 조건부 복원 저항 점수를 계산합니다."""

from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

import numpy as np
import torch

from .data import CTDataset
from .identity import SCORE_VERSION, file_sha256, safe_path, validate_run
from .model import GaussianDCTBlur
from .state import atomic_json, now_kst


def group_pixels(pixels):
    """거리 계산에 실제 쓰는 float32 회색조 표현의 동일 바이트만 묶습니다."""
    x = np.asarray(pixels)
    if x.ndim < 2 or x.dtype != np.float32 or not np.isfinite(x).all():
        raise ValueError("그룹 입력은 유한한 float32 영상 집합이어야 합니다.")
    known, representatives, groups = {}, [], []
    for index, image in enumerate(x):
        key = hashlib.sha256(json.dumps(list(image.shape)).encode() + np.ascontiguousarray(image).tobytes()).hexdigest()
        if key not in known:
            known[key] = len(groups)
            representatives.append(index)
            groups.append([])
        groups[known[key]].append(index)
    return representatives, groups


def pairwise_mse(pixels):
    """float64 직접 차이로 계산하며 Gram 차분의 상쇄를 피합니다."""
    x = np.asarray(pixels, dtype=np.float64).reshape(len(pixels), -1)
    if x.shape[1] == 0 or not np.isfinite(x).all():
        raise ValueError("거리 입력에 빈 영상 또는 비유한 값이 있습니다.")
    result = np.zeros((len(x), len(x)), dtype=np.float64)
    for i in range(len(x)):
        for start in range(i + 1, len(x), 8):
            end = min(len(x), start + 8)
            delta = x[start:end] - x[i]
            values = np.einsum("ij,ij->i", delta, delta) / x.shape[1]
            result[i, start:end] = values
            result[start:end, i] = values
    return result


def match_hashes(gallery_hashes, query_hashes):
    dictionary = {}
    for index, value in enumerate(gallery_hashes):
        dictionary.setdefault(value, []).append(index)
    matches = []
    for value in query_hashes:
        if value not in dictionary:
            raise ValueError("별도 쿼리 특징 바이트가 후보 사전에 없습니다. 재현 실패를 전체 동점으로 대체하지 않습니다.")
        matches.append(list(dictionary[value]))
    return matches


def feature_hash(tensor, pipeline_identity):
    item = tensor.detach().cpu().contiguous()
    if item.dtype != torch.float32 or not torch.isfinite(item).all():
        raise ValueError("전송 특징은 유한한 FP32여야 합니다.")
    header = {"shape": list(item.shape), "dtype": "float32", "byteorder": sys.byteorder,
              "pipeline_identity": pipeline_identity}
    return hashlib.sha256(json.dumps(header, sort_keys=True).encode() + item.numpy().tobytes()).hexdigest()


def score_gallery(distances, candidates):
    """같은 반환 후보의 잔여를 먼저 계산한 뒤 균등 동점·그룹 평균을 냅니다."""
    d = np.asarray(distances, dtype=np.float64)
    if (d.ndim != 2 or d.shape[0] != d.shape[1] or len(d) < 2 or not np.isfinite(d).all()
            or np.any(d < 0) or not np.array_equal(d, d.T) or np.any(np.diag(d) != 0)):
        raise ValueError("후보 거리 행렬의 크기·대칭·유한성·자기 거리가 유효하지 않습니다.")
    g = len(d)
    if np.any(d[~np.eye(g, dtype=bool)] <= 0):
        raise ValueError("거리 표현에서 서로 다른 후보 그룹의 MSE가 양수여야 합니다.")
    if len(candidates) != g:
        raise ValueError("쿼리와 후보 반환 집합 수가 다릅니다.")
    baseline = d.mean(axis=1)
    if not np.isfinite(baseline).all() or np.any(baseline <= 0):
        raise ValueError("특징 없는 균등 후보 반환의 기준 오차가 양수여야 합니다.")
    t = np.clip(d / baseline[:, None], 0, 1)
    np.fill_diagonal(t, 0)
    rows = []
    for i, choices in enumerate(candidates):
        if (not choices or any(type(j) is not int or not 0 <= j < g for j in choices)
                or len(choices) != len(set(choices))):
            raise ValueError("공격 동점 후보가 비었거나 중복·범위 오류가 있습니다.")
        rows.append({"group_index": i, "weight": 1/g, "candidates": choices, "tie_count": len(choices),
                     "b_i": float(baseline[i]), "expected_mse": float(d[i, choices].mean()),
                     "candidate_mse": d[i, choices].tolist(), "candidate_residual": t[i, choices].tolist(),
                     "attack_residual": float(t[i, choices].mean()), "prior_residual": float(t[i].mean()),
                     "fractional_top1": 1/len(choices) if i in choices else 0.,
                     "target_in_tie": i in choices})
    attack = float(np.mean([r["attack_residual"] for r in rows]))
    prior = float(np.mean([r["prior_residual"] for r in rows]))
    if not 1/g - 1e-14 <= prior <= (g-1)/g + 1e-14:
        raise ValueError("특징 없는 기준 잔여의 증명된 범위를 벗어났습니다.")
    residuals = np.array([r["attack_residual"] for r in rows])
    ratio = attack/prior
    # 고정 후보 집합에 대한 그룹 재표집 CI이며 환자·모집단 보안 보장이 아닙니다.
    rng = np.random.default_rng(20261120)
    indices = rng.integers(0, g, size=(2000, g))
    priors = np.array([r["prior_residual"] for r in rows])
    boot = 100 * np.clip(residuals[indices].mean(1)/priors[indices].mean(1), 0, 1)
    return {"score_version": SCORE_VERSION, "score": float(100 * np.clip(ratio, 0, 1)),
            "G": g, "n_queries": g, "T_attack": attack, "T_prior": prior, "raw_ratio": ratio,
            "fractional_top1": float(np.mean([r["fractional_top1"] for r in rows])),
            "fractional_correct_sum": float(sum(r["fractional_top1"] for r in rows)),
            "exact_return_groups": sum(r["candidates"] == [r["group_index"]] for r in rows),
            "target_in_tie_groups": sum(r["target_in_tie"] for r in rows),
            "tie_histogram": dict(Counter(str(r["tie_count"]) for r in rows)),
            "residual_quantiles": {str(q): float(np.quantile(residuals, q)) for q in [0, .25, .5, .75, 1]},
            "score_ci95": np.quantile(boot, [.025, .975]).tolist(),
            "ci_method": "고정 후보 집합의 영상 그룹 균등 bootstrap2000·seed20261120; 환자 CI 아님",
            "per_group": rows}


def run_privacy(model, records, root, run_id, selection, state=None):
    """쿼리와 후보를 실제로 각각 정방향 계산하고 그 바이트 사전만 공격에 씁니다."""
    from .training import tensor_state_digest
    root = Path(root)
    metadata = validate_run(root, run_id)
    sigma = selection["sigma"]
    device = next(model.parameters()).device
    before = tensor_state_digest(model.state_dict())
    if before != selection["model_state_sha256"] or any(m.training for m in model.modules()) or any(p.requires_grad for p in model.parameters()):
        raise ValueError("공격 평가 모델이 선정 state·전체 eval·동결 조건과 다릅니다.")
    dataset = CTDataset(records, image_size=512, training=False)
    pixels = np.stack([dataset[i][0][0].numpy() for i in range(len(dataset))])
    representatives, groups = group_pixels(pixels)
    if len(groups) < 2:
        raise ValueError("실제512픽셀 표현의 서로 다른 후보 그룹이2개 미만입니다.")
    distances = pairwise_mse(pixels[representatives])
    for row in records:
        if file_sha256(row["path"]) != row["byte_sha256"]:
            raise ValueError("공격 입력 원영상의 고정 바이트 SHA가 다릅니다.")
    pipeline = {"protocol": selection["protocol"], "sigma": sigma, "checkpoint_sha256": selection["checkpoint_sha256"],
                "model_state_sha256": before, "source_hashes": metadata["source_hashes"], "precision": "fp32",
                "packet_batch_size": 1, "device": str(device), "torch_version": str(torch.__version__),
                "shape_dtype_byteorder_in_hash": True, "manifest_sha256": metadata["manifest_sha256"]}
    pipeline["encoder_state_sha256"] = tensor_state_digest(model.edge.state_dict())
    pipeline_sha = hashlib.sha256(json.dumps(pipeline, sort_keys=True).encode()).hexdigest()
    hashes = []
    model.blur = GaussianDCTBlur(sigma).to(device).eval()
    for pass_index in range(2):
        current = []
        with torch.inference_mode(), torch.autocast(device.type, enabled=False):
            for group_index, original_index in enumerate(representatives):
                image, _ = dataset[original_index]
                transmitted = model.transmitted_features(image[None].to(device).float())
                current.append(feature_hash(transmitted[0], pipeline_sha))
                if state and (group_index == 0 or (group_index + 1) % 10 == 0):
                    state.update(batch=group_index+1, batches=len(groups),
                                 message=f"σ={sigma}: {'후보' if pass_index == 0 else '별도 쿼리'} 전송 특징 계산 {group_index+1}/{len(groups)}")
        hashes.append(current)
    matches = match_hashes(hashes[0], hashes[1])
    measured = score_gallery(distances, matches)
    positive = score_gallery(distances, [[i] for i in range(len(groups))])
    negative = score_gallery(distances, [list(range(len(groups)))] * len(groups))
    if positive["score"] != 0 or abs(negative["score"] - 100) > 1e-10:
        raise ValueError("원본 반환·상수 특징 대조군의 점수 검사가 실패했습니다.")
    if (tensor_state_digest(model.state_dict()) != before or any(m.training for m in model.modules())
            or any(p.grad is not None for p in model.parameters())
            or file_sha256(safe_path(root, selection["selected_checkpoint"])) != selection["checkpoint_sha256"]):
        raise ValueError("공격 평가에서 선정 가중치·BN·기울기·체크포인트가 변했습니다.")
    raw_path = root / f"work/results/run_{run_id}/sigma_{sigma}_privacy_groups_private.json"
    raw = {"per_group": measured.pop("per_group"), "distance_matrix": distances.tolist(),
           "representatives": representatives, "groups_original_indices": groups,
           "group_member_relative_paths": [[records[j]["relative_path"] for j in group] for group in groups],
           "gallery_feature_hashes": hashes[0], "query_feature_hashes": hashes[1], "pipeline": pipeline}
    atomic_json(raw_path, raw)
    value = {**selection, **measured, "completed_at": now_kst(), "original_test_images": len(records),
             "controls": {"original_score": positive["score"], "constant_score": negative["score"]},
             "controls_kind": "후보 집합을 주입한 산식 대조; 실제 특징 매칭 대조는 별도 회귀검사",
             "raw_file": {"relative_path": raw_path.relative_to(root).as_posix(), "sha256": file_sha256(raw_path)},
             "attack_protocol": "known-encoder-closed-gallery-full-feature-bytehash-v1",
             "precision": "fp32", "packet_batch_size": 1, "device": str(device), "pipeline_sha256": pipeline_sha,
             "grouping_rule": "gray512-bilinear-float32-div255-exact-bytes-uniform-representatives-v1",
             "threat_model": "원영상 후보와 encoder·블러를 아는 공격자의 후보 반환 복원",
             "source_manifest_sha256": file_sha256(root / "work/results/dataset_manifest_private.json"),
             "manifest_records_sha256": metadata["manifest_sha256"],
             "privacy_source_sha256": file_sha256(root / "src/privacy.py"),
             "encoder_state_sha256": tensor_state_digest(model.edge.state_dict()),
             "limitations": ["후보 원본이 있는 조건부 실험이며 후보 없는 복원 점수가 아닙니다.",
                             "분류 FP32 batch8 패킷과 별개인 FP32 batch1 공격 패킷입니다.",
                             "제안식의 독창성·표준성·DP·안전 확률·환자 재식별 방어는 미검증입니다.",
                             "고정 conv1 특징은 후단 분류기 독립 학습으로 바뀌지 않습니다."]}
    atomic_json(root / f"work/results/run_{run_id}/sigma_{sigma}_privacy.json", value)
    return value

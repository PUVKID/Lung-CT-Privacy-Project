"""Torch를 import하지 않고 현재 실행·고정 분할·선정 모델의 연결을 대조합니다."""

import hashlib
import json
from pathlib import Path

PROTOCOL = "independent-sigma-privacy-v1"
SCORE_VERSION = "gallery-residual-v1"
SIGMAS = [0, 1, 2, 4, 8, 16, 32, 64, 128, 256]


def safe_path(root, value):
    """프로젝트 안의 실제 경로만 허용하며 중간 폴더 연결도 따라가지 않습니다."""
    base = Path(root).absolute()
    candidate = Path(value)
    candidate = candidate if candidate.is_absolute() else base / candidate
    if not candidate.resolve().is_relative_to(base.resolve()):
        raise ValueError("프로젝트 경계를 벗어난 파일 경로입니다.")
    for part in [candidate, *candidate.parents]:
        if part.is_symlink() or (hasattr(part, "is_junction") and part.is_junction()):
            raise ValueError("프로젝트 자료의 폴더 연결은 따라가지 않습니다.")
        if part == base:
            break
    return candidate


def file_sha256(path):
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(4 * 1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def validate_config(config):
    if (config.get("protocol") != PROTOCOL or config.get("protocol_fixed_model") is not False
            or config.get("sigmas") != SIGMAS or type(config.get("epochs")) is not int or config["epochs"] != 100
            or config.get("early_stopping_enabled") is not False):
        raise ValueError("강도별 독립100회 학습·프라이버시 평가 프로토콜과 다릅니다.")
    if config.get("score_version") != SCORE_VERSION:
        raise ValueError("고정한 프라이버시 산식 버전과 다릅니다.")
    for key, expected in [("image_size", 512), ("batch_size", 8), ("samples_per_class", 5000), ("seed", 42)]:
        if type(config.get(key)) is not int or config[key] != expected:
            raise ValueError("고정한 실험 조건과 다릅니다: " + key)
    if config.get("precision") != "bf16":
        raise ValueError("본 학습의 BF16 조건을 유지해야 합니다.")


def _run_identity(root, config, manifest_sha256):
    root = Path(root)
    sources = [safe_path(root, "run_training.py"), safe_path(root, "config.json"), *sorted(safe_path(root, "src").glob("*.py"))]
    sources = [safe_path(root, path) for path in sources]
    hashes = {path.relative_to(root).as_posix(): file_sha256(path) for path in sources}
    settings = {"config": config, "manifest_sha256": manifest_sha256, "source_hashes": hashes}
    run_id = hashlib.sha256(json.dumps(settings, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()[:16]
    return run_id, settings


def readonly_input(root, config, key):
    """명시적으로 고정한 두 개의 외부 읽기 전용 입력만 허용합니다."""
    path = Path(config[key])
    if not path.is_absolute():
        return safe_path(root, path)
    allowed = {"expected_reference_manifest": Path(root).parent / "7차/work/reference/dataset_manifest_private.json",
               "initial_weights_path": Path(root).parent / "7차/work/torch-cache/hub/checkpoints/resnet50-0676ba61.pth"}
    expected = allowed.get(key)
    if expected is None or path.absolute() != expected.absolute():
        raise ValueError("명시한 읽기 전용 이전 차수 입력 경로가 아닙니다.")
    for part in [path, *path.parents]:
        if part.is_symlink() or (hasattr(part, "is_junction") and part.is_junction()):
            raise ValueError("읽기 전용 입력의 폴더 연결은 허용하지 않습니다.")
    return path


def validate_manifest(root, config, manifest):
    path = readonly_input(root, config, "expected_reference_manifest")
    if path.is_symlink() or file_sha256(path) != config["expected_reference_manifest_sha256"]:
        raise ValueError("최초 참조 manifest 파일 SHA와 다릅니다.")
    reference = read_json(path)
    for candidate in [manifest, reference]:
        actual = hashlib.sha256(json.dumps(candidate["records"], ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()
        if actual != config["expected_reference_records_sha256"] or candidate["manifest_sha256"] != actual:
            raise ValueError("고정 원본 목록의 실제 records SHA가 다릅니다.")
    if manifest["records"] != reference["records"] or manifest["splits"] != reference["splits"]:
        raise ValueError("기존 원본 목록 또는 정확한 분할이 달라졌습니다.")


def validate_run(root, run_id):
    root = Path(root)
    if not isinstance(run_id, str) or len(run_id) != 16 or any(c not in "0123456789abcdef" for c in run_id):
        raise ValueError("현재 실행 ID 형식이 유효하지 않습니다.")
    config = read_json(safe_path(root, "config.json"))
    validate_config(config)
    manifest = read_json(safe_path(root, "work/results/dataset_manifest_private.json"))
    validate_manifest(root, config, manifest)
    actual, settings = _run_identity(root, config, manifest["manifest_sha256"])
    metadata = read_json(safe_path(root, Path("work/results") / ("run_" + run_id) / "run_metadata.json"))
    if actual != run_id or metadata.get("run_id") != run_id or any(metadata.get(key) != value for key, value in settings.items()):
        raise ValueError("현재 소스·설정·분할·metadata의 실행 식별자가 다릅니다.")
    if metadata.get("protocol") != PROTOCOL or metadata.get("protocol_fixed_model") is not False:
        raise ValueError("현재 metadata가 강도별 독립 모델 실험이 아닙니다.")
    return metadata


def load_selection(root, run_id, sigma):
    root = Path(root).resolve()
    metadata = validate_run(root, run_id)
    if type(sigma) is not int or sigma not in SIGMAS:
        raise ValueError("선정 모델의 강도가 유효하지 않습니다.")
    selection = read_json(safe_path(root, Path("work/results") / ("run_" + run_id) / f"sigma_{sigma}_selection.json"))
    if (selection.get("run_id") != run_id or selection.get("protocol") != PROTOCOL
            or selection.get("protocol_fixed_model") is not False or type(selection.get("training_sigma")) is not int or selection.get("training_sigma") != sigma
            or type(selection.get("sigma")) is not int or selection.get("sigma") != sigma
            or type(selection.get("epochs_ran")) is not int or selection.get("epochs_ran") != 100 or type(selection.get("best_epoch")) is not int
            or not 1 <= selection["best_epoch"] <= 100 or type(selection.get("checkpoint_epoch")) is not int
            or selection.get("checkpoint_epoch") != selection["best_epoch"]):
        raise ValueError("100회 완료 뒤 강도별 선정 모델 식별자가 유효하지 않습니다.")
    expected_path = f"work/checkpoints/run_{run_id}/sigma_{sigma}_best.pt"
    if selection.get("selected_checkpoint") != expected_path:
        raise ValueError("선정 체크포인트가 현재 실행의 σ0 best가 아닙니다.")
    for key in ["checkpoint_sha256", "model_state_sha256"]:
        value = selection.get(key)
        if not isinstance(value, str) or len(value) != 64 or any(c not in "0123456789abcdef" for c in value):
            raise ValueError("고정 모델 SHA 형식이 유효하지 않습니다.")
    if file_sha256(safe_path(root, expected_path)) != selection["checkpoint_sha256"]:
        raise ValueError("선정 후 best 체크포인트 파일이 변경됐습니다.")
    for key, value in result_binding(root, metadata).items():
        if selection.get(key) != value:
            raise ValueError("선정 모델의 소스·원본 분할 결합이 다릅니다: " + key)
    return selection


def result_binding(root, metadata):
    return {"source_manifest_sha256": file_sha256(safe_path(root, "work/results/dataset_manifest_private.json")),
            "manifest_records_sha256": metadata["manifest_sha256"],
            "source_hashes_sha256": hashlib.sha256(json.dumps(metadata["source_hashes"], sort_keys=True).encode()).hexdigest()}


def _result_identity(root, result, expected_run=None):
    run_id = result.get("run_id")
    if expected_run is not None and expected_run != run_id:
        raise ValueError("평가 결과가 현재 실행과 다릅니다.")
    selection = load_selection(root, run_id, result.get("sigma"))
    for key in ["run_id", "protocol", "protocol_fixed_model", "training_sigma", "best_epoch", "checkpoint_epoch",
                "checkpoint_sha256", "model_state_sha256", "selected_checkpoint", "epochs_ran",
                "source_manifest_sha256", "manifest_records_sha256", "source_hashes_sha256"]:
        if type(result.get(key)) is not type(selection[key]) or result.get(key) != selection[key]:
            raise ValueError("평가가 동일한 선정 모델을 사용하지 않았습니다: " + key)
    if (type(result.get("sigma")) is not int or result["sigma"] not in SIGMAS
            or type(result.get("evaluation_sigma")) is not int or result.get("evaluation_sigma") != result["sigma"] or type(result.get("eval_optimizer_steps")) is not int
            or result["eval_optimizer_steps"] != 0 or not result.get("completed_at")):
        raise ValueError("고정 모델의 블러 평가 조건·완료 근거가 유효하지 않습니다.")
    for name in ["validation", "test"]:
        expected = f"work/results/run_{run_id}/sigma_{result['sigma']}_{name}_predictions_private.csv"
        item = result.get("prediction_files", {}).get(name)
        if not isinstance(item, dict) or item.get("relative_path") != expected or file_sha256(safe_path(root, expected)) != item.get("sha256"):
            raise ValueError("고정 평가의 예측 CSV 연결 또는 SHA가 다릅니다.")
    return selection


def validate_result(root, result, expected_run=None):
    _result_identity(root, result, expected_run)
    return result


def validate_privacy_result(root, result, expected_run=None):
    import math
    selection = load_selection(root, result.get("run_id"), result.get("sigma"))
    if expected_run is not None and result.get("run_id") != expected_run:
        raise ValueError("점수 실행 식별자가 다릅니다.")
    for key, value in selection.items():
        if type(result.get(key)) is not type(value) or result.get(key) != value:
            raise ValueError("점수와 강도별 선정 모델 연결이 다릅니다: " + key)
    for key in ["score", "T_attack", "T_prior", "fractional_top1"]:
        if type(result.get(key)) not in {int, float} or not math.isfinite(result[key]):
            raise ValueError("점수 집계가 유한한 숫자가 아닙니다.")
    if (result.get("score_version") != SCORE_VERSION or not 0 <= result["score"] <= 100
            or type(result.get("G")) is not int or result["G"] < 2 or result.get("n_queries") != result["G"]
            or not 0 < result["T_prior"] < 1 or not 0 <= result["T_attack"] <= 1
            or not 0 <= result["fractional_top1"] <= 1 or not result.get("completed_at")
            or abs(result["score"] - 100 * min(1, max(0, result["T_attack"] / result["T_prior"]))) > 1e-10):
        raise ValueError("점수의 범위·분모·수식·완료 근거가 다릅니다.")
    expected = f"work/results/run_{result['run_id']}/sigma_{result['sigma']}_privacy_groups_private.json"
    item = result.get("raw_file", {})
    if item.get("relative_path") != expected or file_sha256(safe_path(root, expected)) != item.get("sha256"):
        raise ValueError("점수 그룹별 원값 파일 연결 또는 SHA가 다릅니다.")
    raw = read_json(safe_path(root, expected))
    metadata = validate_run(root, result["run_id"])
    pipeline = raw.get("pipeline", {})
    for key, value in {"protocol": PROTOCOL, "sigma": result["sigma"], "checkpoint_sha256": result["checkpoint_sha256"],
                       "model_state_sha256": result["model_state_sha256"], "source_hashes": metadata["source_hashes"],
                       "manifest_sha256": metadata["manifest_sha256"], "precision": "fp32", "packet_batch_size": 1,
                       "shape_dtype_byteorder_in_hash": True, "encoder_state_sha256": result.get("encoder_state_sha256")}.items():
        if type(pipeline.get(key)) is not type(value) or pipeline.get(key) != value:
            raise ValueError("공격 파이프라인의 실제 입력·소스 연결이 다릅니다: " + key)
    if (result.get("privacy_source_sha256") != metadata["source_hashes"].get("src/privacy.py")
            or result.get("attack_protocol") != "known-encoder-closed-gallery-full-feature-bytehash-v1"
            or result.get("precision") != "fp32" or type(result.get("packet_batch_size")) is not int or result["packet_batch_size"] != 1
            or result.get("device") != pipeline.get("device")
            or result.get("pipeline_sha256") != hashlib.sha256(json.dumps(pipeline, sort_keys=True).encode()).hexdigest()
            or result.get("controls") != {"original_score": 0., "constant_score": 100.}):
        raise ValueError("공격 설정·정밀도·소스·대조군 연결이 다릅니다.")
    encoder = result.get("encoder_state_sha256")
    if not isinstance(encoder, str) or len(encoder) != 64 or any(c not in "0123456789abcdef" for c in encoder):
        raise ValueError("전송 encoder state SHA가 유효하지 않습니다.")
    d, rows, g = raw.get("distance_matrix"), raw.get("per_group"), result["G"]
    gallery, query = raw.get("gallery_feature_hashes"), raw.get("query_feature_hashes")
    if (not isinstance(d, list) or len(d) != g or not isinstance(rows, list) or len(rows) != g
            or not isinstance(gallery, list) or len(gallery) != g or not isinstance(query, list) or len(query) != g):
        raise ValueError("점수 원값의 후보·쿼리·거리 개수가 다릅니다.")
    attack_values, prior_values, correct = [], [], []
    for i in range(g):
        if (not isinstance(d[i], list) or len(d[i]) != g
                or any(type(v) not in {int, float} or not math.isfinite(v) or v < 0 for v in d[i])
                or d[i][i] != 0 or any(d[i][j] <= 0 for j in range(g) if j != i)):
            raise ValueError("점수 원값의 실제 거리·자기 거리·그룹 구분이 다릅니다.")
        choices = [j for j, h in enumerate(gallery) if h == query[i]]
        if not choices or rows[i].get("candidates") != choices:
            raise ValueError("점수 원값의 별도 쿼리와 사전 후보가 일치하지 않습니다.")
        b = sum(d[i])/g
        t = [min(1., max(0., v/b)) for v in d[i]]
        a, p = sum(t[j] for j in choices)/len(choices), sum(t)/g
        for key, expected_value in {"b_i": b, "attack_residual": a, "prior_residual": p}.items():
            if not math.isclose(rows[i].get(key, -1), expected_value, rel_tol=1e-12, abs_tol=1e-14):
                raise ValueError("그룹별 점수 원값 재집계가 다릅니다: " + key)
        attack_values.append(a)
        prior_values.append(p)
        correct.append(1/len(choices) if i in choices else 0.)
    for key, expected_value in {"T_attack": sum(attack_values)/g, "T_prior": sum(prior_values)/g,
                                "fractional_top1": sum(correct)/g}.items():
        if not math.isclose(result[key], expected_value, rel_tol=1e-12, abs_tol=1e-14):
            raise ValueError("점수 집계와 원값 재계산이 다릅니다: " + key)
    return result

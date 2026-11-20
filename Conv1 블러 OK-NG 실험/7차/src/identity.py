"""Torch를 import하지 않고 현재 실행·고정 분할·선정 모델의 연결을 대조합니다."""

import hashlib
import json
from pathlib import Path

PROTOCOL = "fixed-model-sigma0-v1"
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
    if (config.get("protocol") != PROTOCOL or config.get("protocol_fixed_model") is not True
            or type(config.get("training_sigma")) is not int or config["training_sigma"] != 0
            or config.get("sigmas") != SIGMAS or type(config.get("epochs")) is not int or config["epochs"] != 100
            or config.get("early_stopping_enabled") is not False):
        raise ValueError("σ0 단일 학습·100회·고정 모델10평가 프로토콜과 다릅니다.")
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


def validate_manifest(root, config, manifest):
    path = Path(config["expected_reference_manifest"])
    path = safe_path(root, path)
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
    if (metadata.get("protocol") != PROTOCOL or type(metadata.get("training_sigma")) is not int
            or metadata.get("training_sigma") != 0 or metadata.get("protocol_fixed_model") is not True):
        raise ValueError("현재 metadata가 단일 고정 모델 실험이 아닙니다.")
    return metadata


def load_selection(root, run_id):
    root = Path(root).resolve()
    validate_run(root, run_id)
    selection = read_json(safe_path(root, Path("work/results") / ("run_" + run_id) / "fixed_model_selection.json"))
    if (selection.get("run_id") != run_id or selection.get("protocol") != PROTOCOL
            or selection.get("protocol_fixed_model") is not True or type(selection.get("training_sigma")) is not int or selection.get("training_sigma") != 0
            or type(selection.get("epochs_ran")) is not int or selection.get("epochs_ran") != 100 or type(selection.get("best_epoch")) is not int
            or not 1 <= selection["best_epoch"] <= 100 or type(selection.get("checkpoint_epoch")) is not int
            or selection.get("checkpoint_epoch") != selection["best_epoch"]):
        raise ValueError("100회 완료 뒤의 단일 선정 모델 identity가 유효하지 않습니다.")
    expected_path = f"work/checkpoints/run_{run_id}/sigma_0_best.pt"
    if selection.get("selected_checkpoint") != expected_path:
        raise ValueError("선정 체크포인트가 현재 실행의 σ0 best가 아닙니다.")
    for key in ["checkpoint_sha256", "model_state_sha256"]:
        value = selection.get(key)
        if not isinstance(value, str) or len(value) != 64 or any(c not in "0123456789abcdef" for c in value):
            raise ValueError("고정 모델 SHA 형식이 유효하지 않습니다.")
    if file_sha256(safe_path(root, expected_path)) != selection["checkpoint_sha256"]:
        raise ValueError("선정 후 best 체크포인트 파일이 변경됐습니다.")
    return selection


def validate_fixed_result(root, result, expected_run=None):
    run_id = result.get("run_id")
    if expected_run is not None and expected_run != run_id:
        raise ValueError("평가 결과가 현재 실행과 다릅니다.")
    selection = load_selection(root, run_id)
    for key in ["run_id", "protocol", "protocol_fixed_model", "training_sigma", "best_epoch", "checkpoint_epoch",
                "checkpoint_sha256", "model_state_sha256", "selected_checkpoint", "epochs_ran"]:
        if type(result.get(key)) is not type(selection[key]) or result.get(key) != selection[key]:
            raise ValueError("평가가 동일한 선정 모델을 사용하지 않았습니다: " + key)
    if (type(result.get("sigma")) not in {int, float} or result["sigma"] not in SIGMAS
            or result.get("evaluation_sigma") != result["sigma"] or type(result.get("eval_optimizer_steps")) is not int
            or result["eval_optimizer_steps"] != 0 or not result.get("completed_at")):
        raise ValueError("고정 모델의 블러 평가 조건·완료 근거가 유효하지 않습니다.")
    for name in ["validation", "test"]:
        expected = f"work/results/run_{run_id}/sigma_{result['sigma']}_{name}_predictions_private.csv"
        item = result.get("prediction_files", {}).get(name)
        if not isinstance(item, dict) or item.get("relative_path") != expected or file_sha256(safe_path(root, expected)) != item.get("sha256"):
            raise ValueError("고정 평가의 예측 CSV 연결 또는 SHA가 다릅니다.")
    return result

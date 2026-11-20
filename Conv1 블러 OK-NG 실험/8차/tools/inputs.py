"""새 실험의 최초 입력 기준과 실제 원본을 검사하며 이전 학습 상태는 가져오지 않습니다."""

from pathlib import Path
from src.identity import (_run_identity, file_sha256, read_json, safe_path, readonly_input, validate_config, validate_manifest, validate_run)
from src.state import atomic_json


def operational_hashes(root):
    root = Path(root)
    paths = [safe_path(root, "안전_학습.py"), *sorted(safe_path(root, "tools").glob("*.py"))]
    return {path.relative_to(root).as_posix(): file_sha256(safe_path(root, path)) for path in paths}


def baseline_path(root, run_id):
    return safe_path(root, f"work/reference/run_{run_id}_입력기준_비공개.json")


def freeze_inputs(root, run_id):
    root = Path(root)
    metadata = validate_run(root, run_id)
    config = metadata["config"]
    value = {"run_id": run_id, "settings": {key: metadata[key] for key in ["config", "manifest_sha256", "source_hashes"]},
             "operational_hashes": operational_hashes(root),
             "manifest_file_sha256": file_sha256(safe_path(root, "work/results/dataset_manifest_private.json")),
             "initial_weights_sha256": file_sha256(readonly_input(root, config, "initial_weights_path"))}
    if value["initial_weights_sha256"] != config["initial_weights_sha256"]:
        raise ValueError("초기 ImageNet 파일이 고정 SHA와 다릅니다.")
    path = baseline_path(root, run_id)
    if path.exists():
        if read_json(path) != value:
            raise ValueError("최초 입력 기준을 현재 값으로 교체할 수 없습니다.")
    else:
        atomic_json(path, value)
    return {"run_id": run_id, "baseline_path": path.relative_to(root).as_posix(), "baseline_sha256": file_sha256(path)}


def verify_training_inputs(root, expected_baseline_sha256):
    root = Path(root)
    config = read_json(safe_path(root, "config.json"))
    validate_config(config)
    manifest = read_json(safe_path(root, "work/results/dataset_manifest_private.json"))
    validate_manifest(root, config, manifest)
    run_id, settings = _run_identity(root, config, manifest["manifest_sha256"])
    path = baseline_path(root, run_id)
    if file_sha256(path) != expected_baseline_sha256:
        raise ValueError("부모가 명시한 최초 입력 기준 SHA와 다릅니다.")
    baseline = read_json(path)
    if (baseline["run_id"] != run_id or baseline["settings"] != settings
            or baseline["operational_hashes"] != operational_hashes(root)
            or baseline["manifest_file_sha256"] != file_sha256(safe_path(root, "work/results/dataset_manifest_private.json"))
            or baseline["initial_weights_sha256"] != config["initial_weights_sha256"]
            or file_sha256(readonly_input(root, config, "initial_weights_path")) != config["initial_weights_sha256"]):
        raise ValueError("새 학습의 입력·소스·초기 가중치가 최초 기준과 다릅니다.")
    validate_run(root, run_id)
    data_root = Path(config["dataset_root"]).resolve()
    for row in manifest["records"]:
        path = Path(row["path"])
        if path.is_symlink() or not path.resolve().is_relative_to(data_root) or file_sha256(path) != row["byte_sha256"]:
            raise ValueError("실제 원본 영상이 고정 목록과 다릅니다.")
    return {"run_id": run_id, "baseline_sha256": expected_baseline_sha256, "original_files": len(manifest["records"]),
            "split_sizes": {name: len(rows) for name, rows in manifest["splits"].items()}}

"""고정된 원본 SHA를 확인한 뒤 경로와 실행 식별자만 명시적으로 변환합니다."""

from __future__ import annotations

import argparse
import copy
import gc
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import torch

from src.data import prepare_dataset, validate_reference_manifest
from src.state import atomic_json, now_kst
from src.training import TrainingControl, _run_identity

REFERENCE = "work/recovery/이관_기준목록_비공개.json"
LINEAGE = "work/recovery/복구_계보_비공개.json"
SCIENTIFIC = ("run_training.py", "src/__init__.py", "src/data.py", "src/model.py",
              "src/state.py", "src/training.py")


def file_digest(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def records_digest(rows):
    return hashlib.sha256(json.dumps(rows, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def json_bytes(payload):
    return (json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")


def safe_path(root, relative):
    root = Path(root).resolve()
    value = PurePosixPath(str(relative).replace("\\", "/"))
    if value.is_absolute() or any(part in {"..", "."} or ":" in part for part in value.parts):
        raise ValueError("허용한 폴더 밖의 경로입니다.")
    path = root.joinpath(*value.parts)
    if not path.resolve().is_relative_to(root):
        raise ValueError("폴더 경계를 벗어나는 파일입니다.")
    for item in [path, *path.parents]:
        if item == root:
            break
        if item.is_symlink() or (hasattr(item, "is_junction") and item.is_junction()):
            raise ValueError("복구 파일에서 폴더 연결을 따라가지 않습니다.")
    return path


def read_baseline(path, expected_sha256):
    if file_digest(path) != expected_sha256:
        raise ValueError("복구 기준 파일의 외부 고정 SHA와 다릅니다.")
    return json.loads(Path(path).read_text(encoding="utf-8"))


def verify_files(root, files):
    for relative, expected in files.items():
        if file_digest(safe_path(root, relative)) != expected:
            raise ValueError(f"원본 SHA가 다릅니다: {relative}")


def relocate_manifest(source, old_prefix, new_prefix):
    if source.get("manifest_sha256") != records_digest(source.get("records")):
        raise ValueError("원본 목록의 파생 SHA가 다릅니다.")
    target = copy.deepcopy(source)
    old_prefix, new_prefix = old_prefix.replace("\\", "/").rstrip("/"), new_prefix.replace("\\", "/").rstrip("/")
    for rows in [target["records"], *target["splits"].values()]:
        for row in rows:
            relative = row["relative_path"]
            pieces = PurePosixPath(relative).parts
            if PurePosixPath(relative).is_absolute() or any(p in {"..", "."} or ":" in p or "\\" in p for p in pieces):
                raise ValueError("원본 목록의 상대 경로가 유효하지 않습니다.")
            expected = old_prefix + "/" + relative
            if row["path"].replace("\\", "/") != expected:
                raise ValueError("명시한 원본 접두와 상대 경로가 일치하지 않습니다.")
            # 원본 경로의 구분자 표기도 보존하고 드라이브 접두만 바꿉니다.
            separator = "\\" if "\\" in row["path"] else "/"
            row["path"] = (new_prefix + "/" + relative).replace("/", separator)
    target["manifest_sha256"] = records_digest(target["records"])
    return target


def relocated_config(source, new_dataset, target_manifest):
    result = copy.deepcopy(source)
    result.update(dataset_root=new_dataset, expected_reference_manifest=REFERENCE,
                  expected_reference_manifest_sha256=hashlib.sha256(json_bytes(target_manifest)).hexdigest(),
                  expected_reference_records_sha256=target_manifest["manifest_sha256"])
    return result


def assert_config_compatible(source, target, new_dataset, target_manifest):
    if target != relocated_config(source, new_dataset, target_manifest):
        raise ValueError("자료·기준 목록 경로와 파생 SHA 외의 설정이 변경됐습니다.")


def assert_state_equal(before, after):
    if isinstance(before, torch.Tensor):
        if not isinstance(after, torch.Tensor) or before.dtype != after.dtype or before.shape != after.shape or not torch.equal(before.cpu(), after.cpu()):
            raise ValueError("복구 변환에서 tensor 값·형식이 변경됐습니다.")
    elif type(before) is not type(after):
        raise ValueError("복구 변환에서 상태의 자료형이 변경됐습니다.")
    elif isinstance(before, dict):
        if before.keys() != after.keys():
            raise ValueError("복구 변환에서 상태 키가 변경됐습니다.")
        for key in before:
            assert_state_equal(before[key], after[key])
    elif isinstance(before, (list, tuple)):
        if len(before) != len(after):
            raise ValueError("복구 변환에서 상태 길이가 변경됐습니다.")
        for left, right in zip(before, after):
            assert_state_equal(left, right)
    elif before != after:
        raise ValueError("허용한 식별자 이외의 상태가 변경됐습니다.")


def rebind_checkpoint(source, old_run_id, new_run_id, sigma, prefix_sha256=None):
    if source.get("run_id") != old_run_id or source.get("sigma") != sigma:
        raise ValueError("가져올 체크포인트 실행·강도가 다릅니다.")
    # tensor는 수정하지 않고 새 mapping만 만듭니다. 저장 후 재로딩으로 내용도 대조합니다.
    target = dict(source, run_id=new_run_id)
    if source.get("shadow_prefix_sha256") is not None:
        if not prefix_sha256:
            raise ValueError("변환한 prefix SHA가 필요합니다.")
        target["shadow_prefix_sha256"] = prefix_sha256
    return target


def convert_checkpoint(source_path, target_path, old_run_id, new_run_id, sigma, prefix_sha256=None):
    source = torch.load(source_path, map_location="cpu", weights_only=False)
    target = rebind_checkpoint(source, old_run_id, new_run_id, sigma, prefix_sha256)
    Path(target_path).parent.mkdir(parents=True, exist_ok=True)
    torch.save(target, target_path)
    restored = torch.load(target_path, map_location="cpu", weights_only=False)
    assert_state_equal(target, restored)
    result = {"source_sha256": file_digest(source_path), "new_sha256": file_digest(target_path),
              "epoch": source["epoch"], "tensor_and_state_equal": True}
    del source, target, restored
    gc.collect()
    return result


def validate_metric(metric):
    for key in ("validation", "test"):
        if key not in metric:
            continue
        value = metric[key]
        matrix, count = value["confusion_matrix"], value["n_images"]
        if (len(matrix) != 2 or any(len(row) != 2 for row in matrix)
                or any(type(n) is not int or n < 0 for row in matrix for n in row)
                or type(count) is not int or count <= 0 or sum(map(sum, matrix)) != count
                or abs(value["accuracy"] - (matrix[0][0] + matrix[1][1]) / count) > 1e-12):
            raise ValueError("원본 결과의 혼동행렬·분모·정확도가 모순됩니다.")


def rebind_metric(source, old_run_id, new_run_id, sigma, prefix_sha256):
    if source.get("run_id") != old_run_id or source.get("sigma") != sigma:
        raise ValueError("완료 결과의 실행·강도가 다릅니다.")
    validate_metric(source)
    target = copy.deepcopy(source)
    target["run_id"] = new_run_id
    comparison = target.get("early_stopping_comparison", {})
    if comparison.get("available"):
        if not prefix_sha256:
            raise ValueError("완료 비교의 prefix SHA가 필요합니다.")
        validate_metric(comparison)
        comparison["checkpoint_sha256"] = prefix_sha256
    return target


def validate_resume(last, config, expected_epoch):
    history = last["history"]
    epoch = last["epoch"]
    if (epoch != expected_epoch or len(history) != epoch or [r["epoch"] for r in history] != list(range(1, epoch + 1))):
        raise ValueError("완료 epoch와 학습 이력이 일치하지 않습니다.")
    control = TrainingControl(config["min_delta"], config["early_stopping_patience"],
                              enabled=config.get("early_stopping_enabled", True))
    control.load_state_dict(last["training_control"])
    expected_steps = epoch * ((2 * config["samples_per_class"] + config["batch_size"] - 1) // config["batch_size"])
    if control.optimizer_steps != expected_steps or not 1 <= control.best_raw_epoch <= epoch:
        raise ValueError("완료 epoch의 업데이트 수·최적 epoch가 다릅니다.")
    if not control.enabled and control.shadow_stop_epoch and not 1 <= control.shadow_best_raw_epoch <= control.shadow_stop_epoch <= epoch:
        raise ValueError("고정한 가상 종료 상태가 유효하지 않습니다.")
    return epoch + 1


def validate_prefix_state(last, prefix_path, run_id, sigma, expected_sha256=None):
    """아직 생성 전인 정상 상태와 생성된 뒤 반드시 보존할 prefix를 구분합니다."""
    prefix_path = Path(prefix_path)
    control = last["training_control"]
    stop_epoch = control.get("shadow_stop_epoch", 0)
    best_epoch = control.get("shadow_best_raw_epoch", 0)
    stored_hash = last.get("shadow_prefix_sha256")
    if stop_epoch == 0:
        if best_epoch != 0 or stored_hash is not None or prefix_path.exists() or expected_sha256 is not None:
            raise ValueError("관찰용 종료 전 상태에 prefix 파일·해시·최적 시점이 남아 있습니다.")
        return None
    if (type(stop_epoch) is not int or type(best_epoch) is not int
            or not 1 <= best_epoch <= stop_epoch <= last["epoch"]
            or not isinstance(stored_hash, str) or len(stored_hash) != 64
            or any(c not in "0123456789abcdef" for c in stored_hash)
            or not prefix_path.is_file()):
        raise ValueError("관찰용 종료 상태에 유효한 prefix 파일·해시·시점이 필요합니다.")
    if file_digest(prefix_path) != stored_hash or (expected_sha256 is not None and stored_hash != expected_sha256):
        raise ValueError("고정한 prefix SHA와 마지막 완료 상태가 다릅니다.")
    frozen = torch.load(prefix_path, map_location="cpu", weights_only=False)
    if frozen.get("run_id") != run_id or frozen.get("sigma") != sigma or frozen.get("epoch") != best_epoch:
        raise ValueError("고정한 prefix의 실행·강도·최적 시점이 다릅니다.")
    del frozen
    return stored_hash


def build_target_config(source_root, target_root, baseline):
    reference = Path(source_root) / baseline["reference_relative_path"]
    if file_digest(reference) != baseline["reference_file_sha256"]:
        raise ValueError("보존한 원본 기준 목록 SHA가 다릅니다.")
    source = json.loads(reference.read_text(encoding="utf-8"))
    if records_digest(source["records"]) != baseline["reference_records_sha256"]:
        raise ValueError("보존한 원본 목록 SHA가 다릅니다.")
    actual = json.loads((Path(source_root) / "work/results/dataset_manifest_private.json").read_text(encoding="utf-8"))
    if source["records"] != actual["records"] or source["splits"] != actual["splits"]:
        raise ValueError("원본 실행과 기준 목록의 원본·정확한 분할이 다릅니다.")
    target = relocate_manifest(source, baseline["source_dataset_prefix"], baseline["target_dataset_prefix"])
    config = relocated_config(baseline["source_config"], baseline["target_dataset_prefix"], target)
    return config, target


def import_recovery(target_root, source_root, baseline_path, baseline_sha256):
    root, source_root = Path(target_root).resolve(), Path(source_root).resolve()
    baseline = read_baseline(baseline_path, baseline_sha256)
    verify_files(source_root, baseline["source_files"])
    source_manifest = json.loads((source_root / "work/results/dataset_manifest_private.json").read_text(encoding="utf-8"))
    old_run, source_settings = _run_identity(source_root, baseline["source_config"], source_manifest["manifest_sha256"])
    source_metadata = json.loads((source_root / f"work/results/run_{baseline['source_run_id']}/run_metadata.json").read_text(encoding="utf-8"))
    if (old_run != baseline["source_run_id"] or source_metadata.get("run_id") != old_run
            or any(source_metadata.get(key) != value for key, value in source_settings.items())):
        raise ValueError("원본 실행 metadata·소스·설정·자료의 식별자가 다릅니다.")
    for name in SCIENTIFIC:
        if file_digest(root / name) != baseline["source_files"][name]:
            raise ValueError(f"학습 소스가 원본과 다릅니다: {name}")
    config, manifest = build_target_config(source_root, root, baseline)
    assert_config_compatible(baseline["source_config"], json.loads((root / "config.json").read_text(encoding="utf-8")),
                             baseline["target_dataset_prefix"], manifest)
    for row in manifest["records"]:
        image = safe_path(Path(config["dataset_root"]), row["relative_path"])
        if file_digest(image) != row["byte_sha256"]:
            raise ValueError("이동한 원영상의 byte SHA가 다릅니다.")
    # 기준 파일을 먼저 고정하고 기존 자료 준비 함수의 전체 재계산·분할 핀 검사를 통과합니다.
    reference = root / REFERENCE
    if reference.exists() and reference.read_bytes() != json_bytes(manifest):
        raise ValueError("기존 이관 기준 목록을 다른 내용으로 덮어쓰지 않습니다.")
    reference.parent.mkdir(parents=True, exist_ok=True)
    if not reference.exists():
        reference.write_bytes(json_bytes(manifest))
    validate_reference_manifest(config, root, manifest)
    prepared = prepare_dataset(config, root)
    if prepared["records"] != manifest["records"] or prepared["splits"] != manifest["splits"]:
        raise ValueError("실제 대상 영상 재계산이 이관 기준과 다릅니다.")
    new_run, settings = _run_identity(root, config, prepared["manifest_sha256"])
    old_run = baseline["source_run_id"]
    if new_run == old_run:
        raise ValueError("경로가 변경된 복구 실행은 새 식별자가 필요합니다.")
    result_dir, checkpoint_dir = root / f"work/results/run_{new_run}", root / f"work/checkpoints/run_{new_run}"
    if result_dir.exists() or checkpoint_dir.exists() or (root / LINEAGE).exists():
        raise FileExistsError("가져올 실행 폴더가 이미 있습니다. 덮어쓰지 않습니다.")
    from tools.safe_training import require_free_space
    checkpoint_sizes = [(source_root / name).stat().st_size for name in baseline["source_files"] if name.endswith(".pt")]
    require_free_space(root, sum(checkpoint_sizes) + max(checkpoint_sizes, default=0) + 64 * 1024 ** 2)
    stage = root / f"work/recovery/가져오기_진행_{new_run}"
    stage.mkdir(parents=True, exist_ok=False)
    output_result, output_ckpt = stage / "results", stage / "checkpoints"
    output_result.mkdir(); output_ckpt.mkdir()
    lineage = {"schema_version": 1, "time": now_kst(), "source_run_id": old_run, "run_id": new_run,
               "baseline_sha256": baseline_sha256, "baseline_path": str(Path(baseline_path).resolve()),
               "source_root": str(source_root), "source_files": baseline["source_files"], "settings": settings,
               "manifest_path_changes_only": True, "original_images_byte_verified": len(manifest["records"]),
               "scientific_sources_unchanged": list(SCIENTIFIC), "converted_checkpoints": {}, "imported_files": {},
               "transfer": baseline["transfer"], "completed_results_reevaluated": False,
               "resume_note": "마지막 완료 epoch 다음 회차부터 다시 수행하며 중단 회차의 배치는 재사용하지 않습니다."}
    source_results = source_root / f"work/results/run_{old_run}"
    source_checkpoints = source_root / f"work/checkpoints/run_{old_run}"
    for sigma_text, spec in baseline["transfer"].items():
        sigma = int(sigma_text)
        prefix_name = f"sigma_{sigma}_shadow_prefix_best.pt"
        source_last = torch.load(source_checkpoints / f"sigma_{sigma}_last.pt", map_location="cpu", weights_only=False)
        validate_resume(source_last, config, spec["epoch"])
        source_prefix_hash = validate_prefix_state(source_last, source_checkpoints / prefix_name, old_run, sigma)
        del source_last
        prefix_hash = None
        if source_prefix_hash is not None:
            prefix = convert_checkpoint(source_checkpoints / prefix_name, output_ckpt / prefix_name, old_run, new_run, sigma)
            prefix_hash = prefix["new_sha256"]
            lineage["converted_checkpoints"][prefix_name] = prefix
        for kind in ("best", "last"):
            name = f"sigma_{sigma}_{kind}.pt"
            lineage["converted_checkpoints"][name] = convert_checkpoint(source_checkpoints / name, output_ckpt / name,
                                                                         old_run, new_run, sigma, prefix_hash)
        last = torch.load(output_ckpt / f"sigma_{sigma}_last.pt", map_location="cpu", weights_only=False)
        next_epoch = validate_resume(last, config, spec["epoch"])
        history = json.loads((source_results / f"sigma_{sigma}_history.json").read_text(encoding="utf-8"))
        assert_state_equal(last["history"], history)
        best = torch.load(output_ckpt / f"sigma_{sigma}_best.pt", map_location="cpu", weights_only=False)
        if best["epoch"] != last["training_control"]["best_raw_epoch"]:
            raise ValueError("최적 모델 epoch가 마지막 상태와 다릅니다.")
        validate_prefix_state(last, output_ckpt / prefix_name, new_run, sigma, prefix_hash)
        shutil.copyfile(source_results / f"sigma_{sigma}_history.json", output_result / f"sigma_{sigma}_history.json")
        if spec["completed"]:
            metric_path = source_results / f"sigma_{sigma}_metrics.json"
            metric = json.loads(metric_path.read_text(encoding="utf-8"))
            if metric.get("epochs_ran") != config["epochs"] or metric.get("optimizer_steps") != last["training_control"]["optimizer_steps"]:
                raise ValueError("완료 조건의 회차·업데이트 수가 마지막 상태와 다릅니다.")
            rebound = rebind_metric(metric, old_run, new_run, sigma, prefix_hash)
            atomic_json(output_result / metric_path.name, rebound)
            for prediction in source_results.glob(f"sigma_{sigma}_*predictions_private.csv"):
                shutil.copyfile(prediction, output_result / prediction.name)
        elif (source_results / f"sigma_{sigma}_metrics.json").exists() or next_epoch > config["epochs"]:
            raise ValueError("중단 조건의 완료/재개 구분이 다릅니다.")
        lineage["transfer"][sigma_text] = {**spec, "next_epoch": next_epoch,
                                          "shadow_prefix_at_import": prefix_hash is not None}
        del last, best
        gc.collect()
    source_meta = json.loads((source_results / "run_metadata.json").read_text(encoding="utf-8"))
    metadata = {**source_meta, **settings, "run_id": new_run, "started_at": now_kst(),
                "recovery": {"source_run_id": old_run, "source_started_at": source_meta["started_at"],
                             "source_metadata_sha256": baseline["source_files"][f"work/results/run_{old_run}/run_metadata.json"],
                             "lineage": LINEAGE, "conversion": "경로·실행 식별자와 연결 SHA만 변환한 상태 이관"}}
    atomic_json(output_result / "run_metadata.json", metadata)
    for kind, folder in (("results", output_result), ("checkpoints", output_ckpt)):
        for path in folder.iterdir():
            lineage["imported_files"][f"work/{kind}/run_{new_run}/{path.name}"] = file_digest(path)
    result_dir.parent.mkdir(parents=True, exist_ok=True); checkpoint_dir.parent.mkdir(parents=True, exist_ok=True)
    os.replace(output_ckpt, checkpoint_dir); os.replace(output_result, result_dir)
    atomic_json(root / LINEAGE, lineage)
    verify_import(root)
    return lineage


def verify_import(root, initial=True, expected_baseline_sha256=None):
    root = Path(root)
    lineage = json.loads((root / LINEAGE).read_text(encoding="utf-8"))
    if expected_baseline_sha256 is not None and lineage["baseline_sha256"] != expected_baseline_sha256:
        raise ValueError("복구 계보의 기준 SHA가 명시한 외부 승인값과 다릅니다.")
    baseline = read_baseline(lineage["baseline_path"], lineage["baseline_sha256"])
    for name in SCIENTIFIC:
        if file_digest(root / name) != baseline["source_files"][name]:
            raise ValueError("복구 후 학습 소스가 변경됐습니다.")
    config = json.loads((root / "config.json").read_text(encoding="utf-8"))
    manifest = json.loads((root / REFERENCE).read_text(encoding="utf-8"))
    assert_config_compatible(baseline["source_config"], config, baseline["target_dataset_prefix"], manifest)
    validate_reference_manifest(config, root, manifest)
    run_id, settings = _run_identity(root, config, manifest["manifest_sha256"])
    if run_id != lineage["run_id"] or settings != lineage["settings"]:
        raise ValueError("복구 실행 식별자·설정이 계보와 다릅니다.")
    if initial:
        verify_files(root, lineage["imported_files"])
    for sigma_text, spec in lineage["transfer"].items():
        folder = root / f"work/checkpoints/run_{run_id}"
        prefix = folder / f"sigma_{sigma_text}_shadow_prefix_best.pt"
        imported_prefix = lineage["converted_checkpoints"].get(prefix.name)
        expected = imported_prefix["new_sha256"] if imported_prefix else None
        last = torch.load(folder / f"sigma_{sigma_text}_last.pt", map_location="cpu", weights_only=False)
        if last["run_id"] != run_id or last["sigma"] != int(sigma_text):
            raise ValueError("재개 상태의 실행·강도가 다릅니다.")
        validate_resume(last, config, spec["epoch"] if initial else last["epoch"])
        # 가져올 때 미생성이었던 prefix는 기존 학습 루프가 나중에 고정할 수 있습니다.
        # 기존에 가져온 prefix는 새 last가 생겨도 처음 변환한 SHA를 계속 고정합니다.
        validate_prefix_state(last, prefix, run_id, int(sigma_text), expected)
        del last
    return {"run_id": run_id, "verified": True, "initial_import": initial, "transfer": lineage["transfer"]}


def main():
    parser = argparse.ArgumentParser(description="보존한 체크포인트의 명시적 경로 복구")
    parser.add_argument("command", choices=("configure", "import", "verify"))
    parser.add_argument("--source-root", type=Path, default=ROOT.parent / "4차")
    parser.add_argument("--baseline", type=Path, default=ROOT / "work/recovery/원본_복구기준_비공개.json")
    parser.add_argument("--baseline-sha256", required=True)
    args = parser.parse_args()
    if args.command == "verify":
        # verify도 외부 기준을 다시 확인합니다.
        read_baseline(args.baseline, args.baseline_sha256)
        result = verify_import(ROOT, expected_baseline_sha256=args.baseline_sha256)
    elif args.command == "configure":
        baseline = read_baseline(args.baseline, args.baseline_sha256)
        verify_files(args.source_root, baseline["source_files"])
        config, _manifest = build_target_config(args.source_root, ROOT, baseline)
        atomic_json(ROOT / "config.json", config)
        result = {"configured": True, "scientific_settings_unchanged": True}
    else:
        result = import_recovery(ROOT, args.source_root, args.baseline, args.baseline_sha256)
        result = {key: result[key] for key in ("source_run_id", "run_id", "original_images_byte_verified", "transfer")}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

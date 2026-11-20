"""강도별 독립 학습 실험을 준비하고 비연구 GPU 연결 검사를 수행합니다."""

import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import sys
import traceback

ROOT = Path(__file__).resolve().parent
os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")
os.environ.setdefault("TORCH_HOME", str(ROOT / "work/torch-cache"))


def require_unstarted(root):
    """준비·연결 검사가 이미 진행된 학습 상태를 덮어쓰지 못하게 합니다."""
    root = Path(root)
    lock = root / "work/runtime/recovery.lock"
    if lock.exists() or lock.is_symlink():
        raise RuntimeError("학습 잠금이 있어 준비·연결 검사를 거부합니다. 오래된 잠금도 이 명령이 삭제하지 않습니다.")
    status_path = root / "work/runtime/status.json"
    if status_path.exists():
        status = json.loads(status_path.read_text(encoding="utf-8-sig"))
        pristine = (status.get("stage") == "ready" and status.get("status") == "ready"
                    and status.get("phase") == "preparing" and status.get("training_status") == "pending"
                    and type(status.get("epoch")) is int and status["epoch"] == 0
                    and status.get("history") == [] and status.get("pid") is None
                    and status.get("checkpoint_sha256") is None
                    and all(row.get("status") == "pending" for row in status.get("sigma_queue", [])))
        if not pristine:
            raise RuntimeError("현재 실행이 이미 진행됐거나 준비 대기 상태가 아니어서 준비·연결 검사를 거부합니다.")
    if list((root / "work/checkpoints").glob("run_*/*.pt")):
            raise RuntimeError("8차 학습 체크포인트가 있어 준비·연결 검사를 거부합니다.")
    for directory in (root / "work/results").glob("run_*"):
        if list(directory.glob("sigma_*_metrics.json")) or list(directory.glob("sigma_*_selection.json")) or list(directory.glob("sigma_*_privacy.json")):
            raise RuntimeError("8차 선정·평가 이력이 있어 준비·연결 검사를 거부합니다.")
        for path in directory.glob("sigma_*_history.json"):
            if json.loads(path.read_text(encoding="utf-8-sig")):
                raise RuntimeError("8차 학습 이력이 있어 준비·연결 검사를 거부합니다.")


def prepare(config):
    require_unstarted(ROOT)
    from src.data import prepare_dataset
    from src.identity import PROTOCOL, _run_identity, validate_config
    from src.state import StatusWriter, atomic_json, now_kst
    from tools.inputs import freeze_inputs
    validate_config(config)
    manifest = prepare_dataset(config, ROOT)
    run_id, settings = _run_identity(ROOT, config, manifest["manifest_sha256"])
    metadata = {**settings, "run_id": run_id, "protocol": PROTOCOL, "protocol_fixed_model": False,
                "prepared_at": now_kst(), "started_at": None}
    path = ROOT / "work/results" / ("run_" + run_id) / "run_metadata.json"
    if not path.exists():
        atomic_json(path, metadata)
    state = StatusWriter(ROOT, config)
    state.update(run_id=run_id, phase="preparing", stage="ready", status="ready", pid=None,
                 dataset=manifest["summary"], message="강도별 새100회 독립 학습 준비 완료 · 분류·점수 모두 대기")
    frozen = freeze_inputs(ROOT, run_id)
    print(json.dumps({"command": "prepare", **frozen, "split_sizes": {k: len(v) for k, v in manifest["splits"].items()}}, ensure_ascii=False), flush=True)


def smoke(config, device_name):
    require_unstarted(ROOT)
    import torch
    from src.model import SplitResNet50, block_weight_downloads, DOWNLOAD_ATTEMPTS
    from src.training import seed_everything, precision_policy, stable_binary_loss, build_optimizer_scheduler
    from src.state import atomic_json, now_kst
    seed_everything(42, 4)
    block_weight_downloads()
    if device_name != "cuda" or not torch.cuda.is_available():
        raise RuntimeError("512×512·batch8·BF16 연결 검사는 확인한 CUDA 장치가 필요합니다.")
    device = torch.device("cuda")
    precision = precision_policy("bf16", "cuda")
    torch.cuda.reset_peak_memory_stats(device)
    free_before, total = torch.cuda.mem_get_info(device)
    # 난수 초기값과 합성 입력만 사용하는 비연구 검사이며 실제 체크포인트를 만들지 않습니다.
    model = SplitResNet50(sigma=0, pretrained=False).to(device).train()
    optimizer, _ = build_optimizer_scheduler([p for p in model.parameters() if p.requires_grad], config)
    x = torch.rand(8, 3, 512, 512, device=device)
    y = torch.tensor([0., 1.] * 4, device=device)
    optimizer.zero_grad(set_to_none=True)
    with torch.autocast("cuda", dtype=precision["dtype"]):
        loss = stable_binary_loss(model(x), y)
    if not torch.isfinite(loss):
        raise FloatingPointError("합성 BF16 검사 손실이 비유한 값입니다.")
    loss.backward()
    norm = torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0, error_if_nonfinite=True)
    optimizer.step()
    torch.cuda.synchronize(device)
    result = {"command": "smoke", "time_kst": now_kst(), "research_result": False, "synthetic_inputs": True,
              "input_shape": [8, 3, 512, 512], "precision": "bf16", "optimizer_steps": 1,
              "finite_loss": bool(torch.isfinite(loss)), "loss": loss.item(), "gradient_norm": norm.item(),
              "edge_gradients": any(p.grad is not None for p in model.edge.parameters()),
              "peak_allocated_bytes": torch.cuda.max_memory_allocated(device), "peak_reserved_bytes": torch.cuda.max_memory_reserved(device),
              "free_before_bytes": free_before, "free_after_bytes": torch.cuda.mem_get_info(device)[0], "total_bytes": total,
              "device": torch.cuda.get_device_name(device), "download_calls": len(DOWNLOAD_ATTEMPTS)}
    if result["edge_gradients"]:
        raise AssertionError("고정 conv1에 gradient가 생겼습니다.")
    atomic_json(ROOT / "work/results/smoke_private.json", result)
    print(json.dumps(result, ensure_ascii=False), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["prepare", "smoke", "train"])
    parser.add_argument("--device", choices=["cuda", "cpu"], default="cuda")
    args = parser.parse_args()
    try:
        config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
        if args.command == "prepare":
            prepare(config)
        elif args.command == "smoke":
            smoke(config, args.device)
        else:
            raise RuntimeError("본 학습은 입력 기준 SHA를 검증하는 안전_학습.py 감독으로 실행해야 합니다.")
        return 0
    except Exception:
        details = {"argv": [sys.executable, *sys.orig_argv[1:]], "cwd": os.getcwd(), "exit_code": 1, "error": traceback.format_exc()}
        from tools.safe_training import exception_payload, write_independent_logs, log_folders
        write_independent_logs(log_folders(ROOT), "준비_검사_실패_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f") + ".json", details)
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

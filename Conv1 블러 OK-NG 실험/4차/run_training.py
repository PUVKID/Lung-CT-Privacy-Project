"""prepare / smoke / train 명령으로 실제 로컬 실험을 실행합니다."""

import argparse
import json
import os
from pathlib import Path
import sys
import traceback


ROOT = Path(__file__).resolve().parent
os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")
os.environ.setdefault("TORCH_HOME", str(ROOT / "work/torch-cache"))


def main():
    parser = argparse.ArgumentParser(description="Conv1 블러 OK/NG 영상 단위 예비실험")
    parser.add_argument("command", choices=["prepare", "smoke", "train"])
    parser.add_argument("--config", type=Path, default=ROOT / "config.json")
    parser.add_argument("--device", choices=["cuda", "cpu", "auto"], default="cuda")
    args = parser.parse_args()
    from src.state import StatusWriter, atomic_json, now_kst
    config = json.loads(args.config.read_text(encoding="utf-8-sig"))
    state = StatusWriter(ROOT, config)
    state.update()
    try:
        if args.command == "prepare":
            from src.data import prepare_dataset
            payload = prepare_dataset(config, ROOT)
            state.update(stage="ready", status="ready", pid=None, dataset=payload["summary"],
                         message="자료 검증과 원본 분할 완료. 학습 시작 대기 중")
            state.event("자료 준비 완료", payload["summary"])
            print(json.dumps(payload["summary"], ensure_ascii=False, indent=2))
        elif args.command == "smoke":
            import torch
            from src.model import SplitResNet50
            from src.training import device_information, precision_policy, seed_everything
            seed_everything(config["seed"], config.get("cpu_threads", 4))
            if args.device == "cuda" and not torch.cuda.is_available():
                raise RuntimeError("CUDA GPU 연결 검사에 실패했습니다.")
            device = torch.device("cuda" if args.device == "auto" and torch.cuda.is_available() else "cpu" if args.device == "auto" else args.device)
            precision = precision_policy(config["precision"] if device.type == "cuda" else "fp32", device.type)
            # 연결 검사에는 미학습 난수 모델을 사용하고 연구 결과로 저장하지 않습니다.
            model = SplitResNet50(sigma=1, pretrained=False).to(device).train()
            x = torch.rand(2, 3, 64, 64, device=device)
            y = torch.tensor([0.0, 1.0], device=device)
            with torch.autocast(device_type=device.type, dtype=precision["dtype"], enabled=precision["autocast_enabled"]):
                loss = torch.nn.functional.binary_cross_entropy_with_logits(model(x), y)
            loss.backward()
            assert torch.isfinite(loss)
            assert all(p.grad is None for p in model.edge.parameters())
            assert any(p.grad is not None for p in model.cloud.head.parameters())
            result = {"command": "smoke", "device": device_information(device), "loss": loss.item(),
                      "research_result": False, "input_size": 64, "edge_conv_count": 1,
                      "precision": precision["name"]}
            atomic_json(ROOT / "work/results/smoke.json", result)
            state.update(stage="ready", status="ready", pid=None, device=result["device"],
                         message="모델 정방향·Cloud 역전파 연결 검사 완료. 실제 학습 결과는 아닙니다.")
            state.event("연결 검사 완료", result)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            from src.training import run_training
            run_training(config, ROOT, state, args.device)
        return 0
    except KeyboardInterrupt:
        state.update(stage="interrupted", status="interrupted", pid=None, message="사용자 중단으로 실험을 멈췄습니다.")
        state.event("사용자 중단")
        return 130
    except Exception as exc:
        details = {"time": now_kst(), "argv": sys.argv, "cwd": os.getcwd(), "error_type": type(exc).__name__,
                   "error": str(exc), "traceback": traceback.format_exc(), "exit_code": 1,
                   "sigma": state.data.get("sigma"), "epoch": state.data.get("epoch"),
                   "attempted_batch": state.data.get("attempted_batch"), "precision": state.data.get("precision")}
        atomic_json(ROOT / "work/runtime/last_error.json", details)
        for entry in state.data["sigma_queue"]:
            if entry["status"] == "running":
                entry["status"] = "failed"
        state.update(stage="error", status="failed", pid=None, error=details,
                     message=f"실험 오류: {type(exc).__name__}: {exc}")
        state.event("실험 오류", details)
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

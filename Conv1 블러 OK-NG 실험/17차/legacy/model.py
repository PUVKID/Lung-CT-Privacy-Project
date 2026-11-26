"""입력 사진 블러 → 명시적 ResNet 분할점 → 기울기 반환으로 앞뒤 공동 학습."""

import math
from pathlib import Path
import torch
from torch import nn
from torchvision.models import resnet50
from .identity import PIPELINE_IDENTITY, file_sha256, REGIMES

DOWNLOAD_ATTEMPTS = []


def block_weight_downloads():
    """명시적으로 금지한 외부 가중치 다운로드 시도는 실행 전에 오류로 기록합니다."""
    def reject(*args, **kwargs):
        DOWNLOAD_ATTEMPTS.append({"args": repr(args), "kwargs": repr(kwargs)})
        raise RuntimeError("이 실험은 로컬 고정 초기 가중치만 허용합니다.")
    torch.hub.download_url_to_file = reject


def _dct(x):
    n = x.shape[-1]
    extension = torch.cat((x, x.flip(-1)), dim=-1)
    spectrum = torch.fft.rfft(extension, dim=-1)[..., :n]
    angle = torch.arange(n, device=x.device, dtype=x.dtype) * (-math.pi / (2 * n))
    raw = (spectrum * torch.polar(torch.ones_like(angle), angle)).real
    scale = torch.full((n,), math.sqrt(1 / (2 * n)), device=x.device, dtype=x.dtype)
    scale[0] = math.sqrt(1 / (4 * n))
    return raw * scale


def _idct(x):
    n = x.shape[-1]
    scale = torch.full((n,), math.sqrt(2 * n), device=x.device, dtype=x.dtype)
    scale[0] = math.sqrt(4 * n)
    angle = torch.arange(n, device=x.device, dtype=x.dtype) * (math.pi / (2 * n))
    spectrum = (x * scale) * torch.polar(torch.ones_like(angle), angle)
    spectrum = torch.cat((spectrum, torch.zeros_like(spectrum[..., :1])), dim=-1)
    return torch.fft.irfft(spectrum, n=2 * n, dim=-1)[..., :n]


class GaussianDCTBlur(nn.Module):
    def __init__(self, sigma):
        super().__init__()
        if not math.isfinite(float(sigma)) or sigma < 0:
            raise ValueError("sigma는 유한한 0 이상이어야 합니다.")
        self.sigma = float(sigma)
        self.register_buffer("transfer", torch.empty(0), persistent=False)

    def forward(self, inputs):
        if inputs.ndim != 4 or min(inputs.shape[-2:]) < 2:
            raise ValueError("블러 입력은 N×C×H×W이며 H,W는 2 이상이어야 합니다.")
        if self.sigma == 0:
            return inputs
        original_dtype = inputs.dtype
        x = inputs.float()
        height, width = x.shape[-2:]
        if self.transfer.shape != (height, width) or self.transfer.device != x.device:
            yy = torch.arange(height, device=x.device, dtype=torch.float32) * (math.pi / height)
            xx = torch.arange(width, device=x.device, dtype=torch.float32) * (math.pi / width)
            self.transfer = torch.exp(-0.5 * self.sigma ** 2 * (yy[:, None].square() + xx[None, :].square()))
        # DCT-II 반사/Neumann 경계. sigma는 크기 조정한 입력 영상 픽셀 단위입니다.
        coefficients = _dct(_dct(x).transpose(-1, -2)).transpose(-1, -2)
        coefficients = coefficients * self.transfer
        result = _idct(_idct(coefficients).transpose(-1, -2)).transpose(-1, -2)
        return result.to(original_dtype)


class EdgeStage(nn.Module):
    """선택한 분할점까지의 ResNet 앞단. 모듈은 앞단/후단 중 한 곳에만 등록합니다."""
    def __init__(self, backbone, split_boundary):
        super().__init__()
        self.split_boundary = split_boundary
        names = {"conv1": ("conv1",), "stem": ("conv1", "bn1", "relu", "maxpool"),
                 "layer1": ("conv1", "bn1", "relu", "maxpool", "layer1")}[split_boundary]
        for name in names:
            setattr(self, name, getattr(backbone, name))

    def forward(self, images):
        x = self.conv1(images)
        if self.split_boundary != "conv1":
            x = self.maxpool(self.relu(self.bn1(x)))
        if self.split_boundary == "layer1":
            x = self.layer1(x)
        return x



def deterministic_spatial_summary(x):
    """Per-channel spatial mean and standard deviation, avoiding adaptive pooling autograd.

    Both reductions use ordinary mean so strict CUDA deterministic mode remains enabled.
    Input [N,2048,H,W] -> [N,4096]. It replaces 11th-stage avg/max pooling;
    the new 12th-stage must therefore be trained from scratch, not resumed.
    """
    pool_input = x.float()
    spatial_mean = pool_input.mean(dim=(-2, -1))
    centered = pool_input - spatial_mean[..., None, None]
    spatial_std = (centered.square().mean(dim=(-2, -1)) + 1e-8).sqrt()
    return torch.cat([spatial_mean, spatial_std], dim=1)

class CloudResNet(nn.Module):
    """선택한 분할점 다음의 분류기. 앞단과 함께 모든 파라미터를 학습합니다."""
    def __init__(self, backbone, split_boundary):
        super().__init__()
        self.split_boundary = split_boundary
        names = []
        if split_boundary == "conv1":
            names += ["bn1", "relu", "maxpool"]
        if split_boundary != "layer1":
            names += ["layer1"]
        for name in [*names, "layer2", "layer3", "layer4"]:
            setattr(self, name, getattr(backbone, name))
        self.head = nn.Sequential(nn.Linear(4096, 256), nn.LayerNorm(256), nn.GELU(),
                                  nn.Dropout(0.3), nn.Linear(256, 1))

    def forward(self, features):
        x = features
        if self.split_boundary == "conv1":
            x = self.maxpool(self.relu(self.bn1(x)))
        if self.split_boundary != "layer1":
            x = self.layer1(x)
        x = self.layer4(self.layer3(self.layer2(x)))
        pooled = deterministic_spatial_summary(x)
        return self.head(pooled).squeeze(1)


class SplitResNet50(nn.Module):
    def __init__(self, sigma=0, pretrained=True, weights_path=None, expected_weights_sha256=None,
                 regime="split_trainable", split_boundary="conv1"):
        super().__init__()
        if regime not in REGIMES:
            raise ValueError("알 수 없는 학습 정책입니다.")
        self.regime = regime
        if split_boundary not in {"conv1", "stem", "layer1"}:
            raise ValueError("분할점은 conv1, stem, layer1 중 하나여야 합니다.")
        self.split_boundary = split_boundary
        self.split_point = split_boundary
        backbone = resnet50(weights=None)
        if pretrained:
            if weights_path is None or expected_weights_sha256 is None:
                raise ValueError("새 학습은 고정한 로컬 ImageNet 가중치 경로와 SHA가 필요합니다.")
            path = Path(weights_path)
            if path.is_symlink() or file_sha256(path) != expected_weights_sha256:
                raise ValueError("초기 ImageNet 가중치 파일이 최초 고정 SHA와 다릅니다.")
            backbone.load_state_dict(torch.load(path, map_location="cpu", weights_only=True), strict=True)
        self.front = EdgeStage(backbone, split_boundary)
        self.cloud = CloudResNet(backbone, split_boundary)
        self.blur = GaussianDCTBlur(sigma)
        for key, value in PIPELINE_IDENTITY.items():
            setattr(self, key, value)
        self.register_buffer("rgb_mean", torch.tensor([0.485, 0.456, 0.406]).view(1, 3, 1, 1))
        self.register_buffer("rgb_std", torch.tensor([0.229, 0.224, 0.225]).view(1, 3, 1, 1))

    @property
    def edge(self):
        """Conv1 중간 그림용 별칭. 실제 전송 앞단 전체는 front입니다."""
        return self.front.conv1

    def encoder_state_dict(self):
        return self.front.state_dict()

    def stage_module(self, name):
        """시각화에서 분할 위치와 무관하게 원래 ResNet 모듈을 찾습니다."""
        if hasattr(self.front, name):
            return getattr(self.front, name)
        return getattr(self.cloud, name)

    @property
    def sigma(self):
        return self.blur.sigma

    @property
    def tail(self):
        return self.cloud

    def encode_from_blurred(self, images):
        """학습 입력은 디스크의 실제 PNG입니다. 이 경로는 블러를 다시 하지 않습니다."""
        if images.ndim != 4 or images.shape[1] != 3:
            raise ValueError("입력은 N×3×H×W 영상이어야 합니다.")
        with torch.autocast(device_type=images.device.type, enabled=False):
            normalized = (images.float() - self.rgb_mean) / self.rgb_std
            return self.front(normalized)

    def transmitted_features_from_blurred(self, images):
        return self.encode_from_blurred(images)

    def forward_from_blurred(self, images):
        return self.cloud(self.encode_from_blurred(images))

    def split_forward_from_blurred(self, images):
        packet = self.encode_from_blurred(images)
        wire = packet.detach().requires_grad_(torch.is_grad_enabled())
        return self.cloud(wire), packet, wire

    def encode_differentiable(self, images):
        """사진 블러 → 정규화 → 선택한 앞단. FP32, 입력/가중치 기울기 보존."""
        if images.ndim != 4 or images.shape[1] != 3:
            raise ValueError("입력은 N×3×H×W 영상이어야 합니다.")
        with torch.autocast(device_type=images.device.type, enabled=False):
            blurred = self.blur(images.float())
            normalized = (blurred - self.rgb_mean) / self.rgb_std
            return self.front(normalized)

    def transmitted_features(self, images):
        """평가/공격 시 공개되는 선택 분할점의 FP32 출력. 실제 학습에는 split_forward를 사용합니다."""
        with torch.no_grad():
            return self.encode_differentiable(images)

    def split_forward(self, images):
        """전송 텐서의 그래프를 끊고, 후단이 돌려줄 기울기를 받는 leaf를 만듭니다."""
        front_packet = self.encode_differentiable(images)
        wire_packet = front_packet.detach().requires_grad_(torch.is_grad_enabled())
        logits = self.cloud(wire_packet)
        return logits, front_packet, wire_packet

    def forward(self, images):
        # 평가 및 일반 단일 모델 비교. split 학습은 training.backward_loss의 명시적 반환 경로입니다.
        return self.cloud(self.encode_differentiable(images))

    def monolithic_forward(self, images):
        """동일 가중치를 분리 객체 인터페이스 없이 한 흐름으로 계산하는 대조."""
        with torch.autocast(device_type=images.device.type, enabled=False):
            x = self.edge((self.blur(images.float()) - self.rgb_mean) / self.rgb_std)
            if self.split_boundary != "conv1":
                x = self.stage_module("maxpool")(self.stage_module("relu")(self.stage_module("bn1")(x)))
            if self.split_boundary == "layer1":
                x = self.stage_module("layer1")(x)
        if self.split_boundary == "conv1":
            x = self.stage_module("maxpool")(self.stage_module("relu")(self.stage_module("bn1")(x)))
        if self.split_boundary != "layer1":
            x = self.stage_module("layer1")(x)
        for name in ("layer2", "layer3", "layer4"):
            x = self.stage_module(name)(x)
        return self.cloud.head(deterministic_spatial_summary(x)).squeeze(1)


def audit_forward_order(model, images):
    """실제 분류 훅으로 사진 선블러와 선택 분할점, 단일 모델 출력 동등성을 검증합니다."""
    if any(module.training for module in model.modules()):
        raise ValueError("연결 검사는 eval 상태에서 수행해야 합니다.")
    calls, seen = [], {}
    def blur_hook(_module, _inputs, output):
        calls.append("input_image_blur")
        seen["blurred"] = output.detach().clone()
    def conv_hook(_module, inputs):
        calls.append("conv1")
        seen["conv1_input"] = inputs[0].detach().clone()
    def front_hook(_module, _inputs, output):
        calls.append("front_output")
        seen["front_packet"] = output.detach().clone()
    def cloud_hook(_module, inputs):
        calls.append("cloud_input")
        seen["cloud_input"] = inputs[0].detach().clone()
    hooks = [model.blur.register_forward_hook(blur_hook), model.edge.register_forward_pre_hook(conv_hook),
             model.front.register_forward_hook(front_hook), model.cloud.register_forward_pre_hook(cloud_hook)]
    try:
        with torch.no_grad(), torch.autocast(device_type=images.device.type, enabled=False):
            logits = model.split_forward(images)[0] if model.regime == "split_trainable" else model(images)
    finally:
        for hook in hooks:
            hook.remove()
    expected = (seen["blurred"] - model.rgb_mean) / model.rgb_std
    if calls != ["input_image_blur", "conv1", "front_output", "cloud_input"] or not torch.equal(expected, seen["conv1_input"]):
        raise AssertionError("실제 분류의 입력 사진 블러 → 정규화 → 선택 ResNet 앞단 순서 검증 실패")
    if not torch.equal(seen["front_packet"], seen["cloud_input"]):
        raise AssertionError("후단이 실제 선택 앞단의 출력을 받지 않았습니다.")
    with torch.no_grad(), torch.autocast(device_type=images.device.type, enabled=False):
        direct = model.monolithic_forward(images)
    error = float((logits - direct).abs().max().item())
    if not torch.equal(logits, direct):
        raise AssertionError("같은 모델의 분할/단일 호출 출력이 다릅니다.")
    return {"actual_forward_calls": calls, "conv1_input_equals_normalized_blur": True,
            "cloud_input_equals_selected_front_output": True,
            "split_vs_monolithic_bitwise_equal": True, "max_abs_logit_difference": error,
            "regime": model.regime, "bn_policy": "all_trainable_during_training_eval_for_measurement",
            "front_packet_shape": list(seen["front_packet"].shape), "front_packet_dtype": str(seen["front_packet"].dtype),
            "forward_precision": "fp32", "split_boundary": model.split_boundary}


def audit_materialized_forward(model, saved_png_images):
    """이미 저장된 블러 PNG가 그대로 Conv1에 전달되고 재블러되지 않는지 실제 훅으로 확인."""
    if any(module.training for module in model.modules()):
        raise ValueError("저장 PNG 연결 검사는 eval 상태여야 합니다.")
    calls, observed = [], {}
    def forbidden_blur(*_):
        raise AssertionError("실제 PNG를 읽은 다음 다시 블러를 적용했습니다.")
    def conv_hook(_module, inputs):
        calls.append('conv1')
        observed['conv1_input'] = inputs[0].detach().clone()
    def front_hook(_module, _inputs, result):
        calls.append('front_output')
        observed['front_output'] = result.detach().clone()
    def tail_hook(_module, inputs):
        calls.append('tail_input')
        observed['tail_input'] = inputs[0].detach().clone()
    hooks = [model.blur.register_forward_pre_hook(forbidden_blur),
             model.front.conv1.register_forward_pre_hook(conv_hook),
             model.front.register_forward_hook(front_hook), model.tail.register_forward_pre_hook(tail_hook)]
    try:
        with torch.no_grad(), torch.autocast(saved_png_images.device.type, enabled=False):
            if model.regime == 'split_trainable':
                logits = model.split_forward_from_blurred(saved_png_images)[0]
            else:
                logits = model.forward_from_blurred(saved_png_images)
    finally:
        for hook in hooks:
            hook.remove()
    normalized = (saved_png_images.float() - model.rgb_mean) / model.rgb_std
    if calls != ['conv1', 'front_output', 'tail_input']:
        raise AssertionError('저장 PNG → Conv1 → 후단의 실제 호출 순서가 다릅니다.')
    if not torch.equal(normalized, observed['conv1_input']):
        raise AssertionError('Conv1이 저장된 PNG와 다른 영상을 받았습니다.')
    if not torch.equal(observed['front_output'], observed['tail_input']):
        raise AssertionError('후단에 전송한 피처맵이 Conv1 출력과 다릅니다.')
    with torch.no_grad(), torch.autocast(saved_png_images.device.type, enabled=False):
        monolithic = model.forward_from_blurred(saved_png_images)
    if not torch.equal(logits, monolithic):
        raise AssertionError('같은 가중치의 분할 호출과 연속 호출 출력이 다릅니다.')
    return {'input': 'actual_saved_png8', 'actual_forward_calls': calls, 'blurred_again': False,
            'conv1_input_equals_normalized_saved_png': True, 'tail_received_actual_conv1_features': True,
            'split_and_continuous_logits_identical': True, 'split_boundary': model.split_boundary,
            'packet_shape': list(observed['front_output'].shape), 'packet_dtype': str(observed['front_output'].dtype)}

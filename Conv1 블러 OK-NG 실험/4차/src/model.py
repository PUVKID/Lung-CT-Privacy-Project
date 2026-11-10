"""PyTorch CUDA 이식: Edge conv1 한 층과 Cloud 나머지 계층을 구분합니다."""

import math
import torch
from torch import nn
from torchvision.models import ResNet50_Weights, resnet50


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
        # DCT-II의 반사/Neumann 경계를 사용하며 sigma는 특징맵 픽셀 단위입니다.
        coefficients = _dct(_dct(x).transpose(-1, -2)).transpose(-1, -2)
        coefficients = coefficients * self.transfer
        result = _idct(_idct(coefficients).transpose(-1, -2)).transpose(-1, -2)
        return result.to(original_dtype)


class CloudResNet(nn.Module):
    def __init__(self, backbone):
        super().__init__()
        for name in ["bn1", "relu", "maxpool", "layer1", "layer2", "layer3", "layer4", "avgpool"]:
            setattr(self, name, getattr(backbone, name))
        self.head = nn.Sequential(nn.Linear(2048, 128), nn.ReLU(), nn.Dropout(0.3), nn.Linear(128, 1))
        for parameter in self.parameters():
            parameter.requires_grad_(False)
        for parameter in self.layer4.parameters():
            parameter.requires_grad_(True)
        for module in self.modules():
            if isinstance(module, nn.BatchNorm2d):
                for parameter in module.parameters():
                    parameter.requires_grad_(False)
        for parameter in self.head.parameters():
            parameter.requires_grad_(True)

    def forward(self, x):
        # 고정된 앞부분에는 역전파 그래프가 필요하지 않습니다.
        with torch.no_grad():
            x = self.maxpool(self.relu(self.bn1(x)))
            x = self.layer3(self.layer2(self.layer1(x)))
        x = self.layer4(x)
        x = self.avgpool(x).flatten(1)
        return self.head(x).squeeze(1)


class SplitResNet50(nn.Module):
    def __init__(self, sigma=0, pretrained=True):
        super().__init__()
        # 가중치가 없으면 실제 학습을 임의 난수 초기값으로 대체하지 않습니다.
        backbone = resnet50(weights=ResNet50_Weights.IMAGENET1K_V1 if pretrained else None, progress=True)
        self.edge = backbone.conv1
        self.edge.requires_grad_(False)
        self.blur = GaussianDCTBlur(sigma)
        self.cloud = CloudResNet(backbone)
        self.register_buffer("rgb_mean", torch.tensor([0.485, 0.456, 0.406]).view(1, 3, 1, 1))
        self.register_buffer("rgb_std", torch.tensor([0.229, 0.224, 0.225]).view(1, 3, 1, 1))

    def train(self, mode=True):
        super().train(mode)
        self.edge.eval()
        for module in self.modules():
            if isinstance(module, nn.BatchNorm2d):
                module.eval()
        return self

    def forward(self, images):
        with torch.no_grad():
            normalized = (images - self.rgb_mean) / self.rgb_std
            features = self.edge(normalized)
            transmitted = self.blur(features)
        return self.cloud(transmitted)

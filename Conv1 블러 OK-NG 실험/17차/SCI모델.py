"""표준 ResNet 평균풀링·FC와 실제 detach 기울기 반환 분할 모델입니다."""
import hashlib
from pathlib import Path
import torch
from torch import nn
from torchvision.models import resnet50,resnet18
from legacy.model import GaussianDCTBlur

LAYERS=('conv1','stem','layer1','layer2','layer3','layer4')

def sha256(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''): h.update(block)
    return h.hexdigest()

class SCIResNet(nn.Module):
    def __init__(self,name='resnet50',sigma=0,boundary='conv1',weights_path=None,weights_sha256=None,pretrained=True):
        super().__init__()
        if name not in ('resnet50','resnet18') or boundary not in ('conv1','stem','layer1'):
            raise ValueError('지원하는 ResNet·분할 경계가 아닙니다.')
        self.name,self.boundary=name,boundary
        self.backbone=(resnet50 if name=='resnet50' else resnet18)(weights=None)
        if pretrained:
            if weights_path is None or weights_sha256 is None or sha256(weights_path)!=weights_sha256:
                raise ValueError('고정 초기 가중치 경로·SHA가 필요합니다.')
            self.backbone.load_state_dict(torch.load(weights_path,map_location='cpu',weights_only=True),strict=True)
        self.backbone.fc=nn.Linear(self.backbone.fc.in_features,1)
        self.blur=GaussianDCTBlur(sigma)
        self.register_buffer('rgb_mean',torch.tensor([.485,.456,.406]).reshape(1,3,1,1))
        self.register_buffer('rgb_std',torch.tensor([.229,.224,.225]).reshape(1,3,1,1))

    def observed(self,raw):
        if raw.ndim!=4 or raw.shape[1]!=1 or not torch.isfinite(raw).all():
            raise ValueError('입력은 유한한 N×1×H×W 원본 ROI이어야 합니다.')
        with torch.autocast(device_type=raw.device.type,enabled=False):
            return self.blur(raw.float())

    def features_from_observed(self,observed,layer):
        if layer not in LAYERS: raise ValueError('알 수 없는 특징 층')
        b=self.backbone
        with torch.autocast(device_type=observed.device.type,enabled=False):
            x=b.conv1((observed.float().repeat(1,3,1,1)-self.rgb_mean)/self.rgb_std)
            if layer=='conv1': return x
            x=b.maxpool(b.relu(b.bn1(x)))
            if layer=='stem': return x
            for name in ('layer1','layer2','layer3','layer4'):
                x=getattr(b,name)(x)
                if name==layer: return x

    def front(self,raw):
        return self.features_from_observed(self.observed(raw),self.boundary)

    def back(self,x):
        return self.logits_from_layer(x,self.boundary)

    def logits_from_layer(self,x,layer):
        b=self.backbone
        if layer not in LAYERS: raise ValueError('알 수 없는 후단 시작 층')
        if layer=='conv1': x=b.maxpool(b.relu(b.bn1(x)))
        start=0 if layer in ('conv1','stem') else int(layer[-1])
        for number in range(start+1,5): x=getattr(b,'layer'+str(number))(x)
        return b.fc(torch.flatten(b.avgpool(x),1)).squeeze(1)

    def forward(self,raw):
        return self.back(self.front(raw))

    def split_loss_backward(self,raw,labels,divisor=1):
        front=self.front(raw)
        wire=front.detach().requires_grad_(True)
        logits=self.back(wire)
        loss=nn.functional.binary_cross_entropy_with_logits(logits.float(),labels)
        (loss/divisor).backward()
        if wire.grad is None or not torch.isfinite(wire.grad).all():
            raise RuntimeError('분할 경계의 반환 기울기가 없거나 비유한 값입니다.')
        front.backward(wire.grad)
        return logits.detach(),loss.detach(),{'detached':wire.is_leaf,'returned_gradient_norm':float(wire.grad.float().norm())}

def freeze_running_stats(model):
    for module in model.modules():
        if isinstance(module,nn.modules.batchnorm._BatchNorm): module.eval()

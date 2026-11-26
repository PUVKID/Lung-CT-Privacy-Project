"""알려진 best Conv1의 실제 FP32 특징 노출을 가정한 선형 패치 역복원입니다."""
from pathlib import Path
import hashlib
import torch
import torch.nn.functional as F
import numpy as np

LAMBDA_RATIOS=(0.,1e-8,1e-6)

def sha256(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda:stream.read(1024*1024),b''):
            h.update(chunk)
    return h.hexdigest()

class FeatureExposure:
    def __init__(self,checkpoint,expected_sha256,device='cpu',rcond=1e-7):
        self.path=Path(checkpoint)
        self.expected_sha256=expected_sha256
        self.verify_checkpoint()
        state=torch.load(self.path,map_location='cpu',weights_only=False)['model']
        self.weight=state['front.conv1.weight'].detach().float().to(device)
        self.mean=state['rgb_mean'].detach().float().to(device)
        self.std=state['rgb_std'].detach().float().to(device)
        if self.weight.shape!=(64,3,7,7) or self.mean.numel()!=3 or self.std.numel()!=3 or (self.std<=0).any():
            raise ValueError('특징 노출은 실제 ResNet Conv1 64×3×7×7과 RGB 정규화가 필요합니다.')
        if not all(torch.isfinite(x).all() for x in (self.weight,self.mean,self.std)):
            raise ValueError('Conv1 가중치·정규화에 비유한 값이 있습니다.')
        self.device=device
        self.rcond=float(rcond)
        if not np.isfinite(self.rcond) or not 0<self.rcond<1:
            raise ValueError('SVD cutoff 범위 오류')
        self.kernel=(self.weight.double()/self.std.double().reshape(1,3,1,1)).sum(1).reshape(64,49)
        u,s,vh=torch.linalg.svd(self.kernel,full_matrices=False)
        cutoff=self.rcond*float(s[0])
        active=s>cutoff
        self.rank=int(active.sum())
        self.condition=float(s[0]/s[-1]) if self.rank==49 else None
        self.smax=float(s[0])
        self.inverses={}
        for ratio in LAMBDA_RATIOS:
            regularization=ratio*self.smax**2
            multiplier=torch.zeros_like(s)
            if ratio==0:
                multiplier[active]=1/s[active]
            elif regularization>0:
                multiplier=s/(s.square()+regularization)
            self.inverses[ratio]=(vh.T*multiplier)@u.T
        self.phase='unspecified'
        self.stats={}
        self.geometry={}

    def verify_checkpoint(self):
        if sha256(self.path)!=self.expected_sha256:
            raise ValueError('특징 노출 best 체크포인트 SHA 불일치')

    def expose(self,x):
        normalized=(x.repeat(1,3,1,1)-self.mean)/self.std
        return F.conv2d(normalized,self.weight,stride=2,padding=3)

    def transform(self,pixels):
        pixels=np.asarray(pixels,dtype=np.float32)
        if pixels.ndim!=2 or min(pixels.shape)<7 or not np.isfinite(pixels).all() or pixels.min()<0 or pixels.max()>1:
            raise ValueError('특징 노출 입력은 유한한 [0,1] 2차원 영상이어야 합니다.')
        with torch.no_grad(),torch.autocast(device_type=self.device,enabled=False):
            x=torch.from_numpy(pixels.copy())[None,None].to(self.device)
            feature=self.expose(x)
            h,w=pixels.shape
            key=(h,w)
            if key not in self.geometry:
                offset=self.expose(torch.zeros_like(x))
                count=F.fold(torch.ones(1,49,feature.shape[-2]*feature.shape[-1],device=self.device,dtype=torch.float64),
                             output_size=(h,w),kernel_size=7,stride=2,padding=3)
                if float(count.min())<=0:
                    raise ValueError('Conv1 역복원 겹침 분모가0입니다.')
                self.geometry[key]=(offset,count)
            offset,count=self.geometry[key]
            centered=(feature-offset).double().reshape(1,64,-1)
            actual_linear=self.kernel@F.unfold(x.double(),kernel_size=7,stride=2,padding=3)
            representation_residual=float((actual_linear-centered).square().mean())
            result={}
            for ratio,inverse in self.inverses.items():
                patches=inverse@centered
                raw=F.fold(patches,output_size=(h,w),kernel_size=7,stride=2,padding=3)/count
                clipped=raw.clamp(0,1).float()
                forwarded=self.expose(clipped)
                fwd_mse=float((forwarded-feature).square().mean())
                energy=float(feature.square().mean())
                record={'raw_input_mse':float((raw-x.double()).square().mean()),'raw_input_max_abs':float((raw-x.double()).abs().max()),
                        'clipped_input_mse':float((clipped-x).square().mean()),'clipped_fraction':float(((raw<0)|(raw>1)).double().mean()),
                        'forward_mse':fwd_mse,'forward_relative_mse':fwd_mse/max(energy,1e-30),
                        'actual_forward_linear_mse':representation_residual,'overlap_min':float(count.min())}
                if not all(np.isfinite(value) for value in record.values()):
                    raise ValueError('특징 역복원 진단에 비유한 값이 있습니다.')
                phase=self.stats.setdefault(self.phase,{})
                aggregate=phase.setdefault(str(ratio),{'count':0,'sums':{name:0. for name in record},'maxima':{name:0. for name in record}})
                aggregate['count']+=1
                for name,value in record.items():
                    aggregate['sums'][name]+=value
                    aggregate['maxima'][name]=max(aggregate['maxima'][name],value)
                result[ratio]=clipped[0,0].cpu().numpy()
        return result

    def metadata(self):
        self.verify_checkpoint()
        summaries={phase:{ratio:{'count':r['count'],'means':{k:v/r['count'] for k,v in r['sums'].items()},'maxima':r['maxima']} for ratio,r in data.items()} for phase,data in self.stats.items()}
        return {'threat_model':'알려진 best Conv1 whitebox; 서버 내부 FP32 beforeReLU 특징 노출 가정',
                'checkpoint_sha256':self.expected_sha256,'layer':'front.conv1','feature_precision':'fp32','kernel_shape':[64,49],
                'rank':self.rank,'condition_number':self.condition,'rank_reason':None if self.rank==49 else '고정 cutoff에서49차원 패치 정보를 모두 식별할 수 없음',
                'pinv_rcond':self.rcond,'absolute_svd_cutoff':self.rcond*self.smax,'cutoff_note':'FP64 기본 epsilon 대신 사전 고정한 상대 cutoff',
                'lambda_ratios':list(LAMBDA_RATIOS),'lambda_absolute':[r*self.smax**2 for r in LAMBDA_RATIOS],
                'fold':{'kernel_size':7,'stride':2,'padding':3,'division':'실제 겹침 횟수'},'offset':'zero image의 실제 RGB 정규화 Conv1; padding 경계 포함',
                'output':'float01 clipping만 적용; uint8 재양자화 없음','decoder':'이미 학습한 사진 입력 디코더를 선형 역복원 뒤 재사용; 독립64채널 학습 디코더 아님',
                'diagnostics':summaries,'full_feature_files_saved':False,
                'observed_geometry':[{'input_size':list(size),'feature_shape':list(offset.shape),
                                      'overlap_min':float(count.min()),'overlap_max':float(count.max())}
                                     for size,(offset,count) in self.geometry.items()]}

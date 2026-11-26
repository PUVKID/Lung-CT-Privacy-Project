"""조건별 train/validation만으로 복원 공격을 선정하고 시험 원본은 마지막에 평가합니다."""
from pathlib import Path
import math
import numpy as np
from scipy.fft import dctn, idctn
from scipy.ndimage import gaussian_filter

def metrics(target, prediction):
    """[0,1] 범위 영상의 MSE·PSNR·11px Gaussian SSIM입니다."""
    x,y = target.astype(np.float64), np.clip(prediction.astype(np.float64),0,1)
    mse=float(np.mean((x-y)**2))
    ux,uy=gaussian_filter(x,1.5,truncate=3.5),gaussian_filter(y,1.5,truncate=3.5)
    vx=gaussian_filter(x*x,1.5,truncate=3.5)-ux*ux
    vy=gaussian_filter(y*y,1.5,truncate=3.5)-uy*uy
    cov=gaussian_filter(x*y,1.5,truncate=3.5)-ux*uy
    ssim=((2*ux*uy+.01**2)*(2*cov+.03**2))/((ux*ux+uy*uy+.01**2)*(vx+vy+.03**2))
    # 경계의 반사 확장 효과를 제외한 11×11 유효 영역 평균입니다.
    return {'mse':mse,'ssim':float(ssim[5:-5,5:-5].mean()),'psnr':None if mse==0 else float(-10*math.log10(mse)),
            'psnr_infinite':mse==0}

def deblur(image,sigma,alpha):
    h,w=image.shape
    yy=np.arange(h,dtype=np.float64)*np.pi/h
    xx=np.arange(w,dtype=np.float64)*np.pi/w
    transfer=np.exp(-.5*sigma*sigma*(yy[:,None]**2+xx[None,:]**2))
    result=idctn(dctn(image,type=2,norm='ortho')*transfer/(transfer*transfer+alpha),type=2,norm='ortho')
    return np.clip(result,0,1).astype(np.float32)

def decoder_model():
    import torch
    # 5단 다중 해상도와 skip 연결로 큰 블러까지 다루며 매 조건 새 초기화합니다.
    class Decoder(torch.nn.Module):
        def __init__(self):
            super().__init__()
            channels=[8,16,32,64,96,128]
            def block(a,b):
                return torch.nn.Sequential(torch.nn.Conv2d(a,b,3,padding=1),torch.nn.GroupNorm(4,b),torch.nn.ReLU(),
                                           torch.nn.Conv2d(b,b,3,padding=1),torch.nn.GroupNorm(4,b),torch.nn.ReLU())
            self.enc=torch.nn.ModuleList([block(1,8)]+[block(channels[i-1],channels[i]) for i in range(1,6)])
            self.dec=torch.nn.ModuleList([block(channels[i+1]+channels[i],channels[i]) for i in range(4,-1,-1)])
            self.out=torch.nn.Conv2d(8,1,1)
            torch.nn.init.zeros_(self.out.weight)
            torch.nn.init.zeros_(self.out.bias)
        def forward(self,x):
            original=x
            skips=[]
            for i,layer in enumerate(self.enc):
                if i:
                    x=torch.nn.functional.avg_pool2d(x,2,ceil_mode=True)
                x=layer(x)
                skips.append(x)
            for layer,skip in zip(self.dec,reversed(skips[:-1])):
                x=x.repeat_interleave(2,-2).repeat_interleave(2,-1)
                x=x[...,:skip.shape[-2],:skip.shape[-1]]
                x=layer(torch.cat((x,skip),1))
            return (original+self.out(x)).clamp(0,1)
    return Decoder()

def fit_decoder(config,folder,rows,device,resume,run_id):
    import torch
    from 실행 import PacketDataset, seed_all, rng_state, restore_rng, save_torch, save_json, disk_guard
    rc=config['reconstruction']
    seed_all(rc['seed'],device=='cuda')
    model=decoder_model().to(device)
    optimizer=torch.optim.AdamW(model.parameters(),lr=rc['learning_rate'],weight_decay=rc['weight_decay'])
    scheduler=torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer,patience=5,factor=.5)
    best,last=folder/'decoder_best.pth',folder/'decoder_last.pth'
    start,best_loss,bad,history=0,float('inf'),0,[]
    if (folder/'decoder_training.json').exists():
        model.load_state_dict(torch.load(best,map_location='cpu',weights_only=False)['model'])
        return model.eval()
    if last.exists():
        if not resume:
            raise RuntimeError('복원 디코더 체크포인트가 있습니다. --resume 필요')
        ckpt=torch.load(last,map_location='cpu',weights_only=False)
        if ckpt['run_id']!=run_id:
            raise ValueError('복원 디코더 run_id 불일치')
        model.load_state_dict(ckpt['model'])
        optimizer.load_state_dict(ckpt['optimizer'])
        scheduler.load_state_dict(ckpt['scheduler'])
        start,best_loss,bad,history=[ckpt[k] for k in ('epoch','best','bad','history')]
        restore_rng(ckpt['rng'])
    for epoch in range(start,rc['epochs']):
        if epoch>=rc['min_epochs'] and bad>=rc['patience']:
            break
        disk_guard(folder,int(config['reserve_gib']*1024**3))
        model.train()
        loader=torch.utils.data.DataLoader(PacketDataset(rows['train'],target=True),batch_size=2,shuffle=True,num_workers=0)
        train_sum=0.
        for x,y in loader:
            x,y=x.to(device),y.to(device)
            optimizer.zero_grad(set_to_none=True)
            loss=(model(x)-y).square().mean()
            loss.backward()
            optimizer.step()
            train_sum+=loss.item()*len(x)
        model.eval()
        val_sum=0.
        with torch.no_grad():
            for x,y in torch.utils.data.DataLoader(PacketDataset(rows['validation'],target=True),batch_size=2,num_workers=0):
                x,y=x.to(device),y.to(device)
                val_sum+=(model(x)-y).square().flatten(1).mean(1).sum().item()
        val_loss=val_sum/len(rows['validation'])
        scheduler.step(val_loss)
        if val_loss<best_loss:
            best_loss,bad=val_loss,0
            save_torch(best,{'run_id':run_id,'model':model.state_dict(),'epoch':epoch+1})
        else:
            bad+=1
        history.append({'epoch':epoch+1,'training_mse':train_sum/len(rows['train']),'validation_mse':val_loss})
        save_torch(last,{'run_id':run_id,'model':model.state_dict(),'optimizer':optimizer.state_dict(),'scheduler':scheduler.state_dict(),
                        'epoch':epoch+1,'best':best_loss,'bad':bad,'history':history,'rng':rng_state(device=='cuda')})
        save_json(folder/'decoder_history.json',history)
    save_json(folder/'decoder_training.json',{'history':history,'best_validation_mse':best_loss,'precision':'fp32'})
    model.load_state_dict(torch.load(best,map_location='cpu',weights_only=False)['model'])
    return model.eval()

def run_attack(config,folder,data,device,resume,run_id,exposure=None):
    import torch
    from 실행 import PacketDataset, original, read_json, save_json
    from 전송 import decode
    photo_folder=Path(folder)
    runtime_root=photo_folder.parent.parent
    folder=photo_folder if exposure is None else photo_folder/'feature_exposure'
    result_path=folder/'attack.json'
    if result_path.exists():
        cached=read_json(result_path)
        if exposure is not None and cached['exposure']['checkpoint_sha256']!=exposure.expected_sha256:
            raise ValueError('특징 공격 결과의 best 체크포인트가 다릅니다.')
        return cached
    rows=data['splits']
    model=fit_decoder(config,photo_folder,rows,device,resume,run_id)
    mean=np.zeros((512,512),dtype=np.float64)
    for row in rows['train']:
        mean+=original(row).astype(np.float64)/255
    mean=(mean/len(rows['train'])).astype(np.float32)
    families=['copy_decoded','mean_train','learned_decoder']+['dct_'+str(a) for a in config['reconstruction']['deblur_alphas']]
    if exposure is not None:
        from 특징노출 import LAMBDA_RATIOS
        families=[f'lambda_{ratio}:{family}' for ratio in LAMBDA_RATIOS for family in families]
    input_cache={'source':None,'values':None}
    def reconstruct(family,x):
        if exposure is not None:
            ratio_text,family=family.split(':',1)
            if input_cache['source'] is not x:
                input_cache['source']=x
                input_cache['values']=exposure.transform(x)
            x=input_cache['values'][float(ratio_text[len('lambda_'):])]
        if family=='copy_decoded':
            return x
        if family=='mean_train':
            return mean
        if family=='learned_decoder':
            with torch.no_grad():
                return model(torch.from_numpy(x.copy())[None,None].to(device))[0,0].cpu().numpy()
        return deblur(x,data['sigma'],float(family[4:]))
    # 모든 후보는 동일 검증 원본으로 선정하며 시험 입력·목표는 이 루프에 사용하지 않습니다.
    val={family:0. for family in families}
    validation_metrics={family:[] for family in families}
    validation_prior=[]
    if exposure is not None:
        exposure.phase='validation'
    for x,y in PacketDataset(rows['validation'],target=True):
        x,y=x[0].numpy(),y[0].numpy()
        validation_prior.append(float(np.mean((mean-y)**2)))
        for family in families:
            measurement=metrics(y,reconstruct(family,x))
            validation_metrics[family].append(measurement)
            val[family]+=measurement['mse']
    val={family:value/len(rows['validation']) for family,value in val.items()}
    selected=min(families,key=lambda family:val[family])
    save_json(folder/'attack_selection.json',{'selected_family':selected,'validation_mse_by_family':val,'selection_split':'validation','run_id':run_id})
    measured=[]
    test_metrics={family:[] for family in families}
    mean_errors=[]
    if exposure is not None:
        exposure.phase='test'
    for x,y in PacketDataset(rows['test'],target=True):
        x,y=x[0].numpy(),y[0].numpy()
        for family in families:
            test_metrics[family].append(metrics(y,reconstruct(family,x)))
        measured.append(test_metrics[selected][-1])
        mean_errors.append(float(np.mean((mean-y)**2)))
    aggregate={key:float(np.mean([m[key] for m in measured])) if all(m[key] is not None for m in measured) else None for key in ('mse','ssim','psnr')}
    aggregate.update(count=len(measured),psnr_infinite_count=sum(m['psnr_infinite'] for m in measured),psnr_aggregation='원본별 PSNR 산술평균; 무한값 포함 시 null')
    baseline=float(np.mean(mean_errors))
    ratio=None if baseline==0 else aggregate['mse']/baseline
    clipped=None if ratio is None else float(np.clip(ratio,0,1))
    by_class={}
    for label in (0,1):
        indices=[i for i,r in enumerate(rows['test']) if r['label']==label]
        error=float(np.mean([measured[i]['mse'] for i in indices]))
        base=float(np.mean([mean_errors[i] for i in indices]))
        raw=None if base==0 else error/base
        by_class['OK' if label==0 else 'NG']={'mse':error,'mean_baseline_mse':base,'count':len(indices),
             'privacy_ratio_raw':raw,'privacy_ratio_clipped':None if raw is None else float(np.clip(raw,0,1)),
             'privacy_score':None if raw is None else 100*float(np.clip(raw,0,1)),'undefined_reason':'기준 평균영상 MSE가 0' if raw is None else None}
    examples=[]
    from PIL import Image
    from 실행 import atomic
    if exposure is not None:
        exposure.phase='examples_validation'
    for label in (0,1):
        row=next(r for r in rows['validation'] if r['label']==label)
        y=original(row)
        x=decode(Path(row['packet_path']).read_bytes())
        name='OK' if label==0 else 'NG'
        images={'original':y,'transmitted':x,'reconstructed':np.rint(reconstruct(selected,x.astype(np.float32)/255)*255).astype(np.uint8)}
        example={'label':name,'source':'validation','settings':{'sigma':data['sigma'],'profile':data['profile'],'selected_family':selected,'selected_attack':selected}}
        for kind,pixels in images.items():
            image_path=folder/'examples'/f'{name}_{kind}.png'
            image_path.parent.mkdir(parents=True,exist_ok=True)
            atomic(image_path,lambda p,pixels=pixels:Image.fromarray(pixels).save(p,format='PNG'))
            example[kind]=image_path.relative_to(runtime_root).as_posix()
        examples.append(example)
    def aggregate_family(records,prior,indices):
        chosen=[records[i] for i in indices]
        report={key:float(np.mean([r[key] for r in chosen])) if all(r[key] is not None for r in chosen) else None for key in ('mse','ssim','psnr')}
        prior_error=float(np.mean([prior[i] for i in indices]))
        error_raw=None if prior_error==0 else report['mse']/prior_error
        structure_raw=1-report['ssim']
        report.update(count=len(chosen),mean_baseline_mse=prior_error,privacy_error_ratio_raw=error_raw,
            privacy_error_ratio_clipped=None if error_raw is None else float(np.clip(error_raw,0,1)),
            privacy_error_score=None if error_raw is None else 100*float(np.clip(error_raw,0,1)),
            privacy_error_clipping_applied=error_raw is not None and error_raw!=float(np.clip(error_raw,0,1)),
            privacy_structure_ratio_raw=structure_raw,privacy_structure_ratio_clipped=float(np.clip(structure_raw,0,1)),
            privacy_structure_score=100*float(np.clip(structure_raw,0,1)),privacy_structure_clipping_applied=structure_raw!=float(np.clip(structure_raw,0,1)),
            undefined_reason='대상 집합의 학습 평균영상 MSE가0' if error_raw is None else None,
            psnr_infinite_count=sum(r['psnr_infinite'] for r in chosen))
        return report
    candidates={}
    for family in families:
        candidate={}
        for split,all_metrics,prior in [('validation',validation_metrics,validation_prior),('test',test_metrics,mean_errors)]:
            indices=list(range(len(rows[split])))
            candidate[split]=aggregate_family(all_metrics[family],prior,indices)
            candidate[split+'_by_class']={name:aggregate_family(all_metrics[family],prior,[i for i,r in enumerate(rows[split]) if r['label']==label]) for label,name in [(0,'OK'),(1,'NG')]}
            candidate[split+'_per_source']=all_metrics[family]
        candidate['interpretation']='학습 평균영상 비교기준: 정의상 상대오차 점수100이며 방어 성공이 아님' if family.endswith('mean_train') else '실제 패킷 입력 또는 실제 특징 노출에 적용한 복원 공격의 관측값'
        candidates[family]=candidate
    if 'test_generated' in rows:
        generated_metrics={family:[] for family in families}
        generated_prior=[]
        if exposure is not None:
            exposure.phase='test_generated'
        for x,y in PacketDataset(rows['test_generated'],target=True):
            x,y=x[0].numpy(),y[0].numpy()
            generated_prior.append(float(np.mean((mean-y)**2)))
            for family in families:
                generated_metrics[family].append(metrics(y,reconstruct(family,x)))
        for family in families:
            candidates[family]['test_generated']=aggregate_family(generated_metrics[family],generated_prior,list(range(len(rows['test_generated']))))
            candidates[family]['test_generated_by_class']={name:aggregate_family(generated_metrics[family],generated_prior,[i for i,r in enumerate(rows['test_generated']) if r['label']==label]) for label,name in [(0,'OK'),(1,'NG')]}
            candidates[family]['test_generated_per_source']=generated_metrics[family]
    posthoc={}
    for group in ('overall','OK','NG'):
        reports={family:(candidates[family]['test'] if group=='overall' else candidates[family]['test_by_class'][group]) for family in families}
        valid={family:r for family,r in reports.items() if r['privacy_error_score'] is not None}
        strongest=min(valid,key=lambda f:valid[f]['privacy_error_score']) if valid else None
        posthoc[group]={'family':strongest,'privacy_error_score':None if strongest is None else valid[strongest]['privacy_error_score'],
                        'interpretation':'시험 후 관측한 최소 상대오차 점수 탐색; 검증 선정 공격을 대체하지 않음'}
    result={'selected_family':selected,'validation_mse':val[selected],'validation_mse_by_family':val,'test':aggregate,
            'mean_baseline_test_mse':baseline,'privacy_ratio_raw':ratio,'privacy_ratio_clipped':clipped,
            'privacy_score':None if clipped is None else 100*clipped,'privacy_score_defined':ratio is not None,
            'privacy_interpretation':'평균영상 공격 대비 상대 복원 MSE 탐색지표; 성공확률·보호 보장 아님',
            'test_per_source_metrics':measured,'attack_input':'실제 Rust 패킷 복호화 512px',
            'deblur_limitation':'축소·양자화 손실을 역으로 복구한다는 보장 없음; 복호화 확대 영상에 정규화 DCT 역필터 적용',
            'missing_families':[],'examples':examples,'candidate_metrics':candidates,'privacy_by_class':by_class,
            'undefined_reason':'기준 평균영상 MSE가 0' if ratio is None else None,'clipping_applied':ratio is not None and ratio!=clipped,
            'selected_scores':{'validation':candidates[selected]['validation'],'test':candidates[selected]['test'],
                               'validation_by_class':candidates[selected]['validation_by_class'],'test_by_class':candidates[selected]['test_by_class']},
            'posthoc_strongest_observed':posthoc,'score_interpretation':'공격 기반 상대오차·구조 차이 탐색지표; 복원 성공률·확률·보호 보장이 아님'}
    if 'test_generated' in rows:
        result['test_generated']=candidates[selected]['test_generated']
        result['selected_scores']['test_generated']=candidates[selected]['test_generated']
        result['selected_scores']['test_generated_by_class']=candidates[selected]['test_generated_by_class']
        result['test_generated_interpretation']='같은 시험 원본 계보의 보조 증강평가; 공격 학습·선정에 사용하지 않음'
    if exposure is not None:
        result['exposure']=exposure.metadata()
        result['attack_input']='실제 best Conv1 FP32 beforeReLU 특징 → 선형 패치 역복원 float01 → 사진 공격 합성'
        result['photo_decoder_reused']=True
    save_json(result_path,result)
    return result

"""SCI 사진·다층 특징·실제 직렬화·연결·멤버십의 분리 평가입니다."""
from __future__ import annotations
import hashlib,json,math,subprocess
from pathlib import Path
import numpy as np
import torch
from torch import nn
import torch.nn.functional as F
from PIL import Image
from 공격 import metrics,deblur,decoder_model
from 실행 import read_json,save_json,save_torch,digest,seed_all,rng_state,restore_rng,disk_guard,atomic
from SCI모델 import LAYERS

ENGINE=Path(__file__).parent/'rust'/'전송엔진.exe'

class FeatureCodec:
    def __init__(self,dtype):
        if dtype not in ('f32','f16','i8'): raise ValueError('특징 dtype 오류')
        self.dtype=dtype;self.count=0;self.packet_bytes=0;self.sidecar_bytes=0;self.error=0.;self.metadata_hash=hashlib.sha256()
    def transfer(self,value,actual=True):
        array=value.detach().float().cpu().numpy()
        if not np.isfinite(array).all() or array.size>32_000_000: raise ValueError('특징 원소 수·유한값 오류')
        scale=float(np.max(np.abs(array))/127) if self.dtype=='i8' and np.max(np.abs(array))>0 else 1.
        packed=(np.rint(array/scale).clip(-127,127).astype('i1') if self.dtype=='i8' else array.astype('<f4' if self.dtype=='f32' else '<f2'))
        if not np.isfinite(packed).all(): raise ValueError('특징 정밀도 변환에서 비유한 값 발생')
        raw=packed.tobytes()
        metadata=json.dumps({'shape':list(array.shape),'dtype':self.dtype,'scale':scale,'quantization':'symmetric127' if self.dtype=='i8' else 'IEEE754'},sort_keys=True,separators=(',',':')).encode('utf-8')
        if actual:
            packet=subprocess.run([str(ENGINE),'feature-encode',self.dtype,str(array.size)],input=raw,capture_output=True,check=True,timeout=60).stdout
            if packet[:4]!=b'FTR1' or len(packet)!=len(raw)+9: raise ValueError('Rust 특징 패킷 머리글·길이 오류')
            decoded=subprocess.run([str(ENGINE),'feature-decode'],input=packet,capture_output=True,check=True,timeout=60).stdout
            if decoded!=raw: raise ValueError('Rust 특징 전송 rawpayload 불일치')
            raw=decoded
            self.count+=1;self.packet_bytes+=len(packet);self.sidecar_bytes+=len(metadata);self.metadata_hash.update(metadata)
        reconstructed=np.frombuffer(raw,dtype='i1' if self.dtype=='i8' else '<f4' if self.dtype=='f32' else '<f2').reshape(array.shape).astype(np.float32)
        if self.dtype=='i8': reconstructed*=np.float32(scale)
        if actual: self.error+=float(np.mean((reconstructed-array)**2))
        return torch.from_numpy(reconstructed.copy()).to(value.device)
    def report(self):
        return {'dtype':self.dtype,'packet_bytes':self.packet_bytes,'sidecar_bytes':self.sidecar_bytes,'total_bytes':self.packet_bytes+self.sidecar_bytes,
                'count':self.count,'mean_total_bytes':None if not self.count else (self.packet_bytes+self.sidecar_bytes)/self.count,
                'quantization_mse':None if not self.count else self.error/self.count,'metadata_sha256':self.metadata_hash.hexdigest(),
                'scope':'평가 입력의 실제 Rust 헤더+payload와 실제 UTF-8 shape/scale sidecar 바이트. 네트워크 지연 실측 아님',
                'training_note':'공격 학습은 같은 dtype cast·scale 연산, 평가 입력은 실제 Rust 직렬화·복호화를 경유'}

class FeatureDecoder(nn.Module):
    def __init__(self,channels,size,output_size=512):
        super().__init__();self.output_size=output_size
        self.first=nn.Sequential(nn.Conv2d(channels,64,1),nn.GroupNorm(4,64),nn.GELU(),nn.Conv2d(64,64,3,padding=1),nn.GELU())
        blocks=[];current=64
        while size<output_size:
            following=max(8,current//2)
            blocks.append(nn.Sequential(nn.Conv2d(current,following,3,padding=1),nn.GroupNorm(4,following),nn.GELU()))
            current=following;size*=2
        self.blocks=nn.ModuleList(blocks);self.last=nn.Conv2d(current,1,1)
    def forward(self,x):
        x=self.first(x)
        for block in self.blocks: x=block(x.repeat_interleave(2,-2).repeat_interleave(2,-1))
        if x.shape[-2:]!=(self.output_size,self.output_size): raise ValueError('특징 디코더 출력 크기 오류')
        return torch.sigmoid(self.last(x))

def _source(row,model,layer,codec,actual):
    from SCI실행 import image
    from SCI고정표본 import read_raw
    device=next(model.parameters()).device
    target=torch.from_numpy(read_raw(row) if row.get('materialized') else image(row))[None,None].to(device)
    with torch.no_grad():
        observed=torch.from_numpy(image(row))[None,None].to(device) if row.get('preblurred') else model.observed(target)
        source=observed if layer=='photo' else codec.transfer(model.features_from_observed(observed,layer),actual=actual)
    return source,target,observed

def _fit(model,rows,layer,codec,config,folder,run_id,resume,progress=None):
    rc=config['reconstruction'];seed_all(rc['seed'],next(model.parameters()).device.type=='cuda')
    source,_,_=_source(rows['train'][0],model,layer,codec,False)
    decoder=(decoder_model() if layer=='photo' else FeatureDecoder(source.shape[1],source.shape[-1],config['image_size'])).to(source.device)
    optimizer=torch.optim.AdamW(decoder.parameters(),lr=rc['learning_rate'],weight_decay=1e-5)
    scheduler=torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer,patience=5,factor=.5)
    start,best,bad,history=0,float('inf'),0,[]
    last=folder/'last.json'
    if last.exists():
        if not resume: raise ValueError('공격 epoch 보존본 재개는 --resume 필요')
        ref=read_json(last);path=folder/ref['path']
        if digest(path)!=ref['sha256']: raise ValueError('공격 epoch SHA 불일치')
        state=torch.load(path,map_location='cpu',weights_only=False)
        if state['run_id']!=run_id: raise ValueError('공격 run_id 불일치')
        decoder.load_state_dict(state['model']);optimizer.load_state_dict(state['optimizer']);scheduler.load_state_dict(state['scheduler'])
        start,best,bad,history=[state[k] for k in ('epoch','best','bad','history')];restore_rng(state['rng'])
        from SCI실행 import reconcile_best_reference
        reconcile_best_reference(folder,ref,state,'validation_mse')
    if not (folder/'training_complete.json').exists():
        for epoch in range(start,rc['epochs']):
            if epoch>=rc['min_epochs'] and bad>=rc['patience']: break
            disk_guard(folder,int(config['reserve_gib']*1024**3)+sum(p.numel()*p.element_size() for p in decoder.parameters())*4)
            decoder.train();train_loss=0.
            order=list(rows['train']);random_order=np.random.default_rng(rc['seed']+epoch).permutation(len(order))
            for processed,index in enumerate(random_order,1):
                source,target,_=_source(order[index],model,layer,codec,False)
                optimizer.zero_grad(set_to_none=True);loss=(decoder(source)-target).square().mean();loss.backward();optimizer.step();train_loss+=float(loss)
                if progress and (processed==1 or processed%20==0 or processed==len(order)): progress({"phase":"decoder_train","epoch":epoch+1,"processed":processed,"total":len(order)})
            decoder.eval();validation=0.
            with torch.no_grad():
                for processed,row in enumerate(rows['validation'],1):
                    source,target,_=_source(row,model,layer,codec,False);validation+=float((decoder(source)-target).square().mean())
                    if progress and (processed==1 or processed%20==0 or processed==len(rows['validation'])): progress({'phase':'decoder_validation','epoch':epoch+1,'processed':processed,'total':len(rows['validation'])})
            validation/=len(rows['validation']);scheduler.step(validation)
            improved=validation<best
            if improved: best,bad=validation,0
            else: bad+=1
            history.append({'run_id':run_id,'epoch':epoch+1,'training_mse':train_loss/len(order),'validation_mse':validation})
            path=folder/'epochs'/f'epoch_{epoch+1:04d}.pth'
            save_torch(path,{'run_id':run_id,'epoch':epoch+1,'model':decoder.state_dict(),'optimizer':optimizer.state_dict(),'scheduler':scheduler.state_dict(),
                'rng':rng_state(source.device.type=='cuda'),'best':best,'bad':bad,'history':history})
            ref={'path':path.relative_to(folder).as_posix(),'sha256':digest(path),'epoch':epoch+1}
            save_json(last,ref)
            if improved: save_json(folder/'best.json',ref)
        save_json(folder/'training_complete.json',{'run_id':run_id,'history':history,'best_validation_mse':best})
    reference=read_json(folder/'best.json');path=folder/reference['path']
    if digest(path)!=reference['sha256']: raise ValueError('공격 best SHA 불일치')
    decoder.load_state_dict(torch.load(path,map_location='cpu',weights_only=False)['model']);decoder.eval()
    return decoder

def _score(records,prior):
    if not records: return {'state':'blocked','reason':'평가 원본 없음','mse':None,'mae':None,'psnr':None,'ssim':None,'count':0}
    report={key:float(np.mean([r[key] for r in records])) if all(r[key] is not None for r in records) else None for key in ('mse','mae','psnr','ssim')}
    denominator=float(np.mean(prior));raw=None if denominator==0 else report['mse']/denominator
    structural=1-report['ssim'];clip=None if raw is None else float(np.clip(raw,0,1))
    return {**report,'count':len(records),'mean_baseline_mse':denominator,'privacy_error_ratio_raw':raw,'privacy_error_ratio_clipped':clip,
        'privacy_error_score':None if clip is None else 100*clip,'privacy_error_clipping_applied':raw is not None and raw!=clip,
        'privacy_structure_ratio_raw':structural,'privacy_structure_ratio_clipped':float(np.clip(structural,0,1)),
        'privacy_structure_score':100*float(np.clip(structural,0,1)),'privacy_structure_clipping_applied':structural!=float(np.clip(structural,0,1)),
        'undefined_reason':'같은 평가 집합의 학습 평균영상 오차가0' if raw is None else None,'psnr_infinite_count':sum(r['psnr_infinite'] for r in records)}

def _measure(target,prediction):
    report=metrics(target,prediction);report['mae']=float(np.mean(np.abs(target-np.clip(prediction,0,1))));return report

def _gradient_inverse(model,target_feature,layer,mean,steps,tv):
    guess=torch.tensor(mean,device=target_feature.device)[None,None].requires_grad_(True)
    optimizer=torch.optim.Adam([guess],lr=.03)
    for _ in range(steps):
        optimizer.zero_grad(set_to_none=True)
        feature=model.features_from_observed(guess,layer)
        variation=(guess[...,1:,:]-guess[...,:-1,:]).abs().mean()+(guess[...,:,1:]-guess[...,:,:-1]).abs().mean()
        loss=(feature-target_feature).square().mean()+tv*variation
        loss.backward();optimizer.step()
        with torch.no_grad(): guess.clamp_(0,1)
    return guess.detach()[0,0].cpu().numpy()

def _feature_forward_ste(feature,dtype):
    """전달 정밀도의 실제 forward 값, 양자화 미분 대신 항등 STE 근사입니다."""
    packed=FeatureCodec(dtype).transfer(feature,actual=False)
    return packed+(feature-feature.detach())


def _raw_gradient_inverse(model,target_feature,layer,mean,steps,tv,dtype,initializations):
    """시험 원본 없이 전달 특징과 TV만으로 원본공간 후보를 선택합니다."""
    if any(parameter.requires_grad for parameter in model.parameters()):
        raise ValueError('원본공격의 source 파라미터는 frozen이어야 합니다.')
    if not initializations or len(set(initializations))!=len(initializations):
        raise ValueError('고정 초기값 목록 오류')
    target_feature=target_feature.detach();candidates=[];best=None;best_image=None
    for name in initializations:
        if name=='train_mean': initial=np.asarray(mean,dtype=np.float32)
        elif name=='flat_0.5': initial=np.full_like(mean,.5,dtype=np.float32)
        else: raise ValueError('지원하지 않는 고정 초기값')
        guess=torch.tensor(initial,device=target_feature.device)[None,None].requires_grad_(True)
        optimizer=torch.optim.Adam([guess],lr=.03);local_best=None;local_image=None
        # 마지막 갱신까지 포함해 관측 목적이 가장 작은 iterate를 보존합니다.
        for iteration in range(steps+1):
            optimizer.zero_grad(set_to_none=True)
            feature=_feature_forward_ste(model.features_from_observed(model.blur(guess),layer),dtype)
            mismatch=(feature-target_feature).square().mean()
            variation=(guess[...,1:,:]-guess[...,:-1,:]).abs().mean()+(guess[...,:,1:]-guess[...,:,:-1]).abs().mean()
            loss=mismatch+tv*variation;objective=float(loss.detach())
            if not math.isfinite(objective): raise ValueError('원본공격 목적 비유한 값')
            if local_best is None or objective<local_best['objective']:
                local_best={'initialization':name,'objective':objective,'feature_mse':float(mismatch.detach()),'tv':float(variation.detach()),'iteration':iteration}
                local_image=guess.detach()[0,0].cpu().numpy().copy()
            if iteration<steps:
                loss.backward();optimizer.step()
                with torch.no_grad(): guess.clamp_(0,1)
        candidates.append(local_best)
        if best is None or local_best['objective']<best['objective']: best=local_best;best_image=local_image
    return best_image,{'selected_initialization':best['initialization'],'selected_objective':best['objective'],'candidates':candidates,
        'selection':'전달 dtype 특징 MSE + TV 가중치×원본 후보 TV만 사용; 시험 원본 접근 없음',
        'forward':'features_from_observed(model.blur(raw_guess), layer), preblurred 우회 금지',
        'dtype':dtype,'gradient':'dtype cast/동적 symmetric127의 forward는 FeatureCodec와 동일; backward는 항등 STE 근사이며 정확 양자화 미분 아님'}


def _shuffle_source_labels(rows,seed):
    """원본 단위 라벨 순열을 고정 사본에 전파하고 실제 분포를 반환합니다."""
    originals={}
    for row in rows:
        source=row['source_id'];label=int(row['label'])
        if label not in (0,1): raise ValueError('셔플 원본 이진 라벨 오류')
        if source in originals and originals[source]!=label: raise ValueError('동일 source_id 원본 라벨 불일치')
        originals[source]=label
    sources=sorted(originals);labels=[originals[source] for source in sources]
    shuffled=np.random.default_rng(seed).permutation(labels).tolist();mapping=dict(zip(sources,shuffled))
    output=[{**row,'label':int(mapping[row['source_id']])} for row in rows]
    counts=lambda values:{str(label):sum(value==label for value in values) for label in (0,1)}
    return output,{'seed':seed,'source_order':'source_id 정렬','mapping':[{'source_id':source,'original_label':originals[source],'shuffled_label':mapping[source]} for source in sources],
        'source_counts_before':counts(labels),'source_counts_after':counts(shuffled),
        'row_counts_before':counts([row['label'] for row in rows]),'row_counts_after':counts([row['label'] for row in output]),
        'main_training_labels_changed':0,'validation_test_labels_changed':0,
        'scope':'source_id별 원본 라벨 고정 순열; 모든 사본 동일배정. 원본단위 분포 보존, 증강후 행 50/50 보장 없음'}


def _linear_inverse(model,value,shape,ratio):
    weights=model.backbone.conv1.weight.detach().double();std=model.rgb_std.double()
    kernel=(weights/std.reshape(1,3,1,1)).sum(1).reshape(64,49)
    u,s,vh=torch.linalg.svd(kernel,full_matrices=False);cutoff=1e-7*float(s[0])
    if ratio==0:
        multiplier=torch.zeros_like(s);active=s>cutoff;multiplier[active]=1/s[active]
    else: multiplier=s/(s.square()+ratio*s[0].square())
    inverse=(vh.T*multiplier)@u.T
    with torch.no_grad():
        offset=model.features_from_observed(torch.zeros(1,1,*shape,device=value.device),'conv1')
        patches=inverse@(value-offset).double().flatten(2)
        count=F.fold(torch.ones_like(patches),output_size=shape,kernel_size=7,stride=2,padding=3)
        if float(count.min())<=0: raise ValueError('선형 역복원 겹침 횟수 오류')
        raw=F.fold(patches,output_size=shape,kernel_size=7,stride=2,padding=3)/count
        reconstruction=raw.clamp(0,1).float()
        residual=float((model.features_from_observed(reconstruction,'conv1')-value).square().mean())
    if not torch.isfinite(raw).all(): raise ValueError('선형 역복원 비유한 값')
    return reconstruction[0,0].cpu().numpy(),{'rank':int((s>cutoff).sum()),'condition':float(s[0]/s[-1]) if s[-1]>cutoff else None,
        'rcond':1e-7,'lambda_ratio':ratio,'raw_min':float(raw.min()),'raw_max':float(raw.max()),'clipped_fraction':float(((raw<0)|(raw>1)).double().mean()),'feature_forward_mse':residual}

def attack_exposure(model,rows,config,folder,run_id,layer='photo',dtype='f32',resume=False,progress=None):
    from SCI실행 import image
    folder.mkdir(parents=True,exist_ok=True)
    if (folder/'result.json').exists():
        cached=read_json(folder/'result.json')
        if not run_id or cached.get('run_id')!=run_id: raise ValueError('공격 완료캐시 run_id 불일치')
        if progress: progress({'phase':'cached_complete','layer':layer,'dtype':dtype})
        return cached
    codec=FeatureCodec(dtype);decoder=_fit(model,rows,layer,codec,config,folder/'decoder',run_id,resume,progress)
    mean=np.zeros((config['image_size'],config['image_size']),dtype=np.float64)
    from SCI고정표본 import read_raw
    for row in rows['train']: mean+=read_raw(row) if row.get('materialized') else image(row)
    mean=(mean/len(rows['train'])).astype(np.float32)
    photo_names=['copy_observed','mean_train','learned_decoder']+['dct_'+str(a) for a in config['reconstruction']['deblur_alphas']]
    names=photo_names if layer=='photo' else ['mean_train','learned_decoder']+[f'gradient_tv_{tv}' for tv in config['reconstruction']['tv_alphas']]
    if layer=='conv1': names += [f'linear_{ratio}:{name}' for ratio in (0.,1e-8,1e-6) for name in photo_names]
    if layer!='photo': names += [f'raw_blur_aware_tv_{tv}' for tv in config['reconstruction']['tv_alphas']]
    diagnostics=[];raw_diagnostics=[]
    def candidates(row):
        source,target,observed=_source(row,model,layer,codec,True)
        target_array=target[0,0].cpu().numpy();observed_array=observed[0,0].cpu().numpy()
        with torch.no_grad(): learned=decoder(source)[0,0].cpu().numpy()
        result={'mean_train':mean,'learned_decoder':learned}
        if layer=='photo':
            result['copy_observed']=observed_array
            for alpha in config['reconstruction']['deblur_alphas']: result['dct_'+str(alpha)]=deblur(observed_array,model.blur.sigma,alpha)
        else:
            for tv in config['reconstruction']['tv_alphas']:
                result[f'gradient_tv_{tv}']=_gradient_inverse(model,source,layer,mean,config['reconstruction']['inverse_steps'],tv)
                result[f'raw_blur_aware_tv_{tv}'],audit=_raw_gradient_inverse(model,source,layer,mean,config['reconstruction']['inverse_steps'],tv,dtype,config['reconstruction'].get('raw_initializations',['train_mean','flat_0.5']))
                raw_diagnostics.append({'row_id':row['id'],'tv_weight':tv,**audit})
        if layer=='conv1':
            for ratio in (0.,1e-8,1e-6):
                inverse,audit=_linear_inverse(model,source,observed_array.shape,ratio);audit['observed_input_mse']=float(np.mean((inverse-observed_array)**2));diagnostics.append(audit)
                with torch.no_grad(): refined=photo_decoder(torch.tensor(inverse,device=source.device)[None,None])[0,0].cpu().numpy()
                for name in photo_names:
                    result[f'linear_{ratio}:{name}']=inverse if name=='copy_observed' else mean if name=='mean_train' else refined if name=='learned_decoder' else deblur(inverse,model.blur.sigma,float(name[4:]))
        with torch.no_grad(): transmitted_logit=None if layer=='photo' else float(model.logits_from_layer(source,layer)[0])
        return target_array,result,transmitted_logit
    photo_decoder=decoder
    if layer=='conv1':
        photo_decoder=_fit(model,rows,'photo',FeatureCodec('f32'),config,folder.parents[1]/'photo'/'decoder',run_id,True,progress)
    measurements={};prior_errors={};selections={};classification={}
    datasets={key:rows[key] for key in ('validation','test','test_generated','validation_original') if key in rows}
    for cohort,external in rows.get('external',{}).items():
        external=external.get('rows',[]) if isinstance(external,dict) else external
        if external: datasets['external_'+cohort]=external
    for split,records in datasets.items():
        measurements[split]={name:[] for name in names};prior_errors[split]=[]
        classified=[]
        for processed,row in enumerate(records,1):
            if progress: progress({'phase':'reconstruction','split':split,'processed':processed-1,'total':len(records)})
            target,outputs,logit=candidates(row);prior_errors[split].append(float(np.mean((mean-target)**2)))
            if logit is not None: classified.append(logit)
            for name in names: measurements[split][name].append(_measure(target,outputs[name]))
            if progress: progress({'phase':'reconstruction','split':split,'processed':processed,'total':len(records)})
        if classified:
            from 지표 import binary_report
            classification[split]=binary_report([row['label'] for row in records],classified)
        if split=='validation':
            for group in ('overall','OK','NG'):
                indices=[i for i,r in enumerate(records) if group=='overall' or r['label']==(0 if group=='OK' else 1)]
                selections[group]={metric:(None if not indices else min(names,key=lambda n:np.mean([measurements[split][n][i][metric] for i in indices])) if metric in ('mse','mae') else max(names,key=lambda n:np.mean([measurements[split][n][i][metric] if measurements[split][n][i][metric] is not None else float('inf') for i in indices]))) for metric in ('mse','mae','ssim','psnr')}
            save_json(folder/'selection.json',{'run_id':run_id,'split':'validation','selections':selections,'unit':'각 전체·클래스·지표별 검증 평균; 시험은 선정에 사용하지 않음'})
    reports={}
    for name in names:
        item={'interpretation':'학습 평균영상 비교기준; 상대오차100은 방어 성공 아님' if name.endswith('mean_train') else '사전 정의한 실제 복원 공격'}
        for split,records in datasets.items():
            item[split]=_score(measurements[split][name],prior_errors[split]);item[split+'_per_source']=measurements[split][name]
            item[split+'_by_class']={group:_score([measurements[split][name][i] for i,r in enumerate(records) if r['label']==label],
                [prior_errors[split][i] for i,r in enumerate(records) if r['label']==label]) for label,group in ((0,'OK'),(1,'NG'))}
        reports[name]=item
    selected=selections['overall']['mse'];selected_report=reports[selected]
    examples=[]
    for label,group in ((0,'OK'),(1,'NG')):
        row=next((r for r in rows['validation'] if r['label']==label),None)
        if row is None: continue
        target,outputs,_=candidates(row)
        output=folder/'examples'/f'{group}_reconstructed.png'
        atomic(output,lambda p:Image.fromarray(np.rint(np.clip(outputs[selected],0,1)*255).astype(np.uint8)).save(p,format='PNG'))
        examples.append({'label':group,'row_id':row['id'],'patient_id':row['patient_id'],'source':'validation',
            'reconstructed':output.relative_to(folder.parents[3] if layer=='photo' else folder.parents[4]).as_posix(),
            'settings':{'layer':layer,'dtype':dtype,'selected_attack':selected,'selection_split':'validation'}})
    result={'run_id':run_id,'selected_family':selected,'selection_unit':'전체 검증 평균 MSE',
        'validation_selection_by_class_metric':selections,'candidate_metrics':reports,'selected_scores':{key:selected_report[key] for key in selected_report if not key.endswith('_per_source')},
        'test':selected_report['test'],'privacy_score':selected_report['test']['privacy_error_score'],'examples':examples,'transmission':codec.report(),
        'raw_inverse_diagnostics_per_source':raw_diagnostics,
        'raw_inverse_summary':{'count':len(raw_diagnostics),'initializations':config['reconstruction'].get('raw_initializations',['train_mean','flat_0.5']),
            'forward_evaluations_per_source':0 if layer=='photo' else len(config['reconstruction'].get('raw_initializations',['train_mean','flat_0.5']))*(config['reconstruction']['inverse_steps']+1)*len(config['reconstruction']['tv_alphas']),
            'scope':'초기값별 iterate 및 초기값 선택은 전달 특징 MSE+TV만 사용; 공격군 선정은 validation만 사용. 실제 전체 실행시간 미측정'},
        'attack_target_spaces':{'gradient_tv':'관측공간 특징 역복원, 최종 원본과 평가','raw_blur_aware_tv':'명시적 블러를 통과하는 원본공간 최적화, 최종 원본과 평가'},
        'linear_inverse_diagnostics_per_source':diagnostics,'linear_inverse_summary':{'count':len(diagnostics),'detail_location':'동일 result.json의 linear_inverse_diagnostics_per_source'},'classification_from_transmitted_features':classification,
        'score_interpretation':'복원 상대오차·구조 차이 탐색 점수이며 재식별 성공확률·안전 보장 아님','external':{}}
    for cohort in ('CSTL','Histo'):
        key='external_'+cohort
        if key not in selected_report: result['external'][cohort]={'state':'blocked','reason':rows.get('external_status',{}).get(cohort,{}).get('reason','확인한 외부 결절·환자·양성악성 주석 없음'),'mse':None};continue
        result['external'][cohort]={'selected_family':selected,'selection_source':'LUNA25 validation','test':selected_report[key],
            'privacy_score':selected_report[key]['privacy_error_score'],
            'candidate_metrics':{name:{'test':reports[name][key],'test_by_class':reports[name][key+'_by_class']} for name in names},
            'selected_scores':{'test':selected_report[key],'test_by_class':selected_report[key+'_by_class']}}
    if 'test_generated' in selected_report: result['test_generated']=selected_report['test_generated']
    save_json(folder/'result.json',result);return result

def membership(model,rows,folder,test_key='test',progress=None):
    from sklearn.metrics import roc_auc_score
    from SCI실행 import image
    device=next(model.parameters()).device
    patients=sorted({r['patient_id'] for r in rows['train']});np.random.default_rng(42).shuffle(patients)
    first=set(patients[:len(patients)//2]);second=set(patients[len(patients)//2:])
    if not first or not second: return {'state':'blocked','test_auc':None,'reason':'선정용·최종용 멤버 환자를 분리할 수 없음'}
    def scores(records):
        result=[]
        with torch.no_grad():
            for processed,row in enumerate(records,1):
                logit=float(model(torch.tensor(image(row),device=device)[None,None])[0]);p=1/(1+math.exp(-max(-700,min(700,logit))))
                loss=float(np.logaddexp(0,logit)-row['label']*logit)
                result.append({'patient_id':row['patient_id'],'label':row['label'],'confidence':max(p,1-p),'negative_loss':-loss})
                if progress and (processed==1 or processed%20==0 or processed==len(records)): progress({'phase':'membership','split':test_key,'processed':processed,'total':len(records)})
        return result
    member_val=scores([r for r in rows['train'] if r['patient_id'] in first]);member_test=scores([r for r in rows['train'] if r['patient_id'] in second])
    nonmember_val=scores(rows['validation']);nonmember_test=scores(rows[test_key])
    if ({r['patient_id'] for r in member_val+nonmember_val}&{r['patient_id'] for r in member_test+nonmember_test}): raise ValueError('멤버십 선정·최종 환자 중복')
    def auc(members,nonmembers,name,one_class=False):
        values=members+nonmembers
        if not members or not nonmembers: return None
        labels=sorted({r['label'] for r in values})
        if not one_class and labels!=[0,1]: return None
        weights=[]
        for member,records in ((1,members),(0,nonmembers)):
            for label in labels:
                if not any(r['label']==label for r in records): return None
            for row in records:
                patients={r['patient_id'] for r in records if r['label']==row['label']}
                patient_nodules=sum(r['patient_id']==row['patient_id'] and r['label']==row['label'] for r in records)
                weights.append(1/(len(patients)*patient_nodules))
        return float(roc_auc_score([1]*len(members)+[0]*len(nonmembers),[r[name] for r in values],sample_weight=weights))
    validation={name:auc(member_val,nonmember_val,name) for name in ('confidence','negative_loss')}
    valid={name:value for name,value in validation.items() if value is not None}
    selected=max(valid,key=valid.get) if valid else None
    test_auc=None if selected is None else auc(member_test,nonmember_test,selected)
    save_json(folder/'membership_raw.json',{'member_selection':member_val,'nonmember_selection':nonmember_val,'member_test':member_test,'nonmember_test':nonmember_test})
    external={}
    for cohort in ('CSTL','Histo'):
        records=rows.get('external',{}).get(cohort,[]);records=records.get('rows',[]) if isinstance(records,dict) else records
        if not records or selected is None: external[cohort]={'auc':None,'reason':'외부 주석·환자계보 미확보 또는 선정 점수 미정의'};continue
        external[cohort]={'auc':auc(member_test,scores(records),selected),'reason':None,
            'interpretation':'외부 cohort 비멤버 비교는 분포 차이와 중복 환자 가능성의 영향을 받음; namespace만으로 환자 독립성 보장하지 않음'}
    return {'selected_score':selected,'validation_auc':validation,'test_auc':test_auc,'external':external,
        'by_class':{group:None if selected is None else auc([r for r in member_test if r['label']==label],[r for r in nonmember_test if r['label']==label],selected,True) for label,group in ((0,'OK'),(1,'NG'))},
        'member_count':len(member_test),'nonmember_count':len(nonmember_test),'selection_final_patient_overlap':0,
        'reason':None if selected is not None else '환자 분리 후 모든 멤버·비멤버 클래스가 있어야 함',
        'weighting':'멤버 여부×건강라벨 셀 동일 가중치, 각 셀의 환자 동일 가중치, 환자내 결절 분산',
        'interpretation':'라벨·환자 가중치의 알려진 점수 공격; 높은 AUC를 cohort 차이와 분리 해석해야 하며 개인정보 유출 확률 아님'}

def linking(model,records,layer,topk,progress=None):
    from SCI실행 import image
    from SCI고정표본 import read_raw
    if not records: return {'state':'blocked','reason':'연결 평가 원본 없음'}
    # 원본별 gallery 하나. 증강 query는 그대로 평가하되 행 번호가 아닌 source_id로 판정합니다.
    sources={}
    source_id=lambda row:row.get('source_id',row['id'])
    for row in records:
        key=source_id(row)
        if key in sources and sources[key]['patient_id']!=row['patient_id']: raise ValueError('연결 source_id 환자 불일치')
        if key not in sources or row.get('canonical'): sources[key]=row
    gallery_rows=list(sources.values());device=next(model.parameters()).device;gallery=[];query=[]
    def vector(x):
        values=F.adaptive_avg_pool2d(model.features_from_observed(x,layer),(2,2)).flatten().float().cpu().numpy()
        return values/max(float(np.linalg.norm(values)),1e-20)
    with torch.no_grad():
        for row in gallery_rows:
            raw=torch.tensor(read_raw(row) if row.get('materialized') else image(row),device=device)[None,None]
            gallery.append(vector(raw))
        for processed,row in enumerate(records,1):
            raw=torch.tensor(read_raw(row) if row.get('materialized') else image(row),device=device)[None,None]
            observed=torch.tensor(image(row),device=device)[None,None] if row.get('preblurred') else model.observed(raw)
            query.append(vector(observed))
            if progress and (processed==1 or processed%20==0 or processed==len(records)): progress({'phase':'linking','processed':processed,'total':len(records)})
    gallery=np.stack(gallery);query=np.stack(query);source_counts={};patient_counts={}
    for k in topk:
        source_correct,patient_correct=0,0
        for index,query_vector in enumerate(query):
            positions=np.argsort(-(gallery@query_vector),kind='stable')[:min(k,len(gallery_rows))]
            source_correct+=int(any(source_id(gallery_rows[p])==source_id(records[index]) for p in positions))
            patient_correct+=int(any(gallery_rows[p]['patient_id']==records[index]['patient_id'] for p in positions))
        source_counts[str(k)]={'correct':source_correct,'total':len(records),'accuracy':source_correct/len(records)}
        patient_counts[str(k)]={'correct':patient_correct,'total':len(records),'accuracy':patient_correct/len(records)}
    return {'topk_source':source_counts,'topk_patient':patient_counts,'count':len(records),'gallery_size':len(gallery_rows),
            'gallery_unit':'고유 source_id별 원본 대표 1개; canonical 우선',
            'query_unit':'선택 집합의 모든 행; 증강 보조는 독립 원본 수 아님',
            'assumption':'정답 결절·환자 목록을 가진 닫힌 집합 원본 ROI gallery와 같은 출처 블러 query. 독립 현실 재식별 성능 아님'}


def run_protection(model,rows,config,folder,run_id,checkpoint,device,resume,progress=None):
    for parameter in model.parameters(): parameter.requires_grad_(False)
    model.eval();attacks=folder/'attacks'
    def reporter(layer,dtype):
        return (lambda info:progress({**info,'layer':layer,'dtype':dtype})) if progress else None
    photo=attack_exposure(model,rows,config,attacks/'photo',run_id,resume=resume,progress=reporter('photo','f32'))
    features={};connections={}
    for layer in config['feature_layers']:
        features[layer]={'precisions':{}}
        for dtype in config['feature_dtypes']:
            features[layer]['precisions'][dtype]=attack_exposure(model,rows,config,attacks/layer/dtype,run_id,layer,dtype,resume,reporter(layer,dtype))
        connections[layer]={'test':linking(model,rows['test'],layer,config['connection_topk'],reporter(layer,'f32')),
            'test_generated':linking(model,rows.get('test_generated',[]),layer,config['connection_topk'],reporter(layer,'f32')),'external':{}}
        for cohort in ('CSTL','Histo'):
            external=rows.get('external',{}).get(cohort,[]);external=external.get('rows',[]) if isinstance(external,dict) else external
            connections[layer]['external'][cohort]=linking(model,external,layer,config['connection_topk'],reporter(layer,'f32'))
    examples=[]
    from SCI실행 import image
    for label,group in ((0,'OK'),(1,'NG')):
        row=next(r for r in rows['validation'] if r['label']==label)
        _,source,observed=_source(row,model,'photo',FeatureCodec('f32'),False)
        with torch.no_grad(): feature=model.features_from_observed(observed,'conv1').abs().mean(1)[0].cpu().numpy()
        low,high=float(feature.min()),float(feature.max());feature=(feature-low)/(high-low) if high>low else np.zeros_like(feature)
        entry={'label':group,'source':'validation','row_id':row['id'],'patient_id':row['patient_id'],'settings':{'sigma':model.blur.sigma,'model':model.name,'cohort':row['cohort'],
            'source_metadata':row['metadata'],'feature_map':{'layer':'conv1','aggregation':'mean_absolute_channels','normalization':'per_image_min_max','raw_min':low,'raw_max':high},
            'feature_reconstruction':{'layer':'conv1','dtype':'f32','selected_attack':features['conv1']['precisions']['f32']['selected_family'],'checkpoint_sha256':checkpoint['sha256'],'threat_model':'서버 내부 특징 노출 가정: 같은 선정 모델과 Conv1 FP32 전달 특징을 알고 원본을 복원하는 공격'}}}
        arrays={'original':source[0,0].cpu().numpy(),'transmitted':observed[0,0].cpu().numpy(),'feature_map':feature}
        for kind,array in arrays.items():
            path=folder/'examples'/f'{group}_{kind}.png';atomic(path,lambda p,array=array:Image.fromarray(np.rint(np.clip(array,0,1)*255).astype(np.uint8)).save(p,format='PNG'))
            entry[kind]=path.relative_to(folder.parent.parent).as_posix()
        entry['reconstructed']=next(e for e in photo['examples'] if e['label']==group)['reconstructed']
        entry['feature_reconstructed']=next(e for e in features['conv1']['precisions']['f32']['examples'] if e['label']==group)['reconstructed']
        examples.append(entry)
    return {'attack':photo,'feature_attacks':features,'feature_attack':features['conv1']['precisions']['f32'],'linking':connections,
            'membership':membership(model,rows,folder,progress=progress),
            'membership_generated':membership(model,rows,folder/'generated','test_generated',progress) if 'test_generated' in rows else None,'examples':examples,'packet':{'count':0,'mean_bytes':None,'reason':'사진 float 블러는 별도 네트워크 전송 실측 없음; 특징 실제 전송은 층·정밀도별 transmission 참조'},
            'metric_inheritance':{'P0_M1_to_M15':None,'reason':'원래 정의를 확인하지 못해 승계 완료로 주장하지 않음; 실제 raw/상대오차/구조 점수만 보고'}}

def run_diagnostics(manifest,config,run_id,device,resume,progress=None):
    """주실험 선정과 분리한 고정 train-only 진단을 한 실행에서 한 번 수행합니다."""
    from SCI실행 import image,Dataset,evaluate
    from SCI모델 import SCIResNet,freeze_running_stats
    from SCI고정표본 import prepare_fixed,original_rows,epoch_rows
    from 지표 import binary_report
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LogisticRegression
    folder=Path(config['runtime'])/'diagnostics'
    if (folder/'result.json').exists():
        result=read_json(folder/'result.json')
        if result['run_id']!=run_id: raise ValueError('진단 run_id 불일치')
        return result
    fixed=prepare_fixed(manifest,config)['splits']
    rows={'train':fixed['train'],'validation':fixed['validation'],'test':original_rows(fixed['test'])};data={}
    for split in ('train','validation','test'):
        data[split]=(np.stack([np.asarray(Image.fromarray(np.rint(image(row)*255).astype(np.uint8)).resize((16,16),Image.Resampling.BOX),dtype=float).ravel()/255 for row in rows[split]]),np.asarray([r['label'] for r in rows[split]]))
    center=np.zeros((16,16),dtype=bool);center[4:12,4:12]=True
    coarse={}
    for name,mask in [('coarse_full',np.ones(256,dtype=bool)),('coarse_center',center.ravel()),('coarse_outer',~center.ravel())]:
        estimator=make_pipeline(StandardScaler(),LogisticRegression(C=1,class_weight='balanced',max_iter=2000,random_state=42))
        estimator.fit(data['train'][0][:,mask],data['train'][1])
        coarse[name]={split:binary_report(data[split][1],estimator.decision_function(data[split][0][:,mask])) for split in ('validation','test')}
    seed_all(config['diagnostics']['shuffle_seed'],device=='cuda')
    shuffled,shuffle_audit=_shuffle_source_labels(rows['train'],config['diagnostics']['shuffle_seed'])
    labels=[row['label'] for row in shuffled]
    save_json(folder/'label_shuffle_mapping.json',{'run_id':run_id,**shuffle_audit})
    weights=config['weights']['resnet50'];model=SCIResNet('resnet50',0,'conv1',weights['path'],weights['sha256']).to(device)
    optimizer=torch.optim.AdamW(model.parameters(),lr=config['learning_rate'],weight_decay=config['weight_decay'])
    scheduler=torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer,patience=3,factor=.5)
    start=0;history=[]
    if (folder/'shuffle_last.json').exists():
        if not resume: raise ValueError('라벨 셔플 진단 재개는 --resume 필요')
        reference=read_json(folder/'shuffle_last.json');path=folder/reference['path']
        if digest(path)!=reference['sha256']: raise ValueError('셔플 진단 보존본 SHA 불일치')
        state=torch.load(path,map_location='cpu',weights_only=False)
        if state['run_id']!=run_id: raise ValueError('셔플 진단 run_id 불일치')
        model.load_state_dict(state['model']);optimizer.load_state_dict(state['optimizer']);scheduler.load_state_dict(state['scheduler']);restore_rng(state['rng'])
        start,history=state['epoch'],state['history']
    for epoch in range(start,config['diagnostics']['shuffle_epochs']):
        disk_guard(folder,int(config['reserve_gib']*1024**3)+sum(t.numel()*t.element_size() for t in model.state_dict().values())*4)
        model.train();freeze_running_stats(model);loss_sum=0.;count=0
        selected=epoch_rows(shuffled,config['seed']+epoch)
        loader=torch.utils.data.DataLoader(Dataset(selected,True),batch_size=config['batch_size'],num_workers=0)
        optimizer.zero_grad(set_to_none=True)
        for batch,(x,y) in enumerate(loader):
            x,y=x.to(device),y.to(device)
            with torch.autocast(device_type=device,dtype=torch.bfloat16,enabled=device=='cuda'):
                logits=model(x);loss=F.binary_cross_entropy_with_logits(logits.float(),y)
            divisor=min(config['accumulation'],len(loader)-(batch//config['accumulation'])*config['accumulation'])
            (loss/divisor).backward()
            if (batch+1)%config['accumulation']==0 or batch+1==len(loader): optimizer.step();optimizer.zero_grad(set_to_none=True)
            loss_sum+=float(loss)*len(y);count+=len(y)
            if progress and (batch==0 or (batch+1)%20==0 or batch+1==len(loader)): progress({'phase':'label_shuffle','epoch':epoch+1,'processed':count,'total':len(selected)})
        scheduler.step(loss_sum/count);history.append({'epoch':epoch+1,'training_shuffled_loss':loss_sum/count,'run_id':run_id})
        path=folder/'shuffle_epochs'/f'epoch_{epoch+1:04d}.pth'
        save_torch(path,{'run_id':run_id,'epoch':epoch+1,'model':model.state_dict(),'optimizer':optimizer.state_dict(),'scheduler':scheduler.state_dict(),
                         'rng':rng_state(device=='cuda'),'history':history,'label_permutation_sha256':hashlib.sha256(json.dumps(labels).encode()).hexdigest()})
        save_json(folder/'shuffle_last.json',{'path':path.relative_to(folder).as_posix(),'sha256':digest(path)})
    precision='cuda_bf16' if device=='cuda' else 'cpu_fp32'
    shuffled_report={split:evaluate(model,rows[split],device,precision) for split in ('validation','test')}
    result={'run_id':run_id,'coarse':coarse,'label_shuffle':{'epochs':config['diagnostics']['shuffle_epochs'],'reports':shuffled_report,
        'permutation_scope':shuffle_audit['scope'],'label_permutation_sha256':hashlib.sha256(json.dumps(labels).encode()).hexdigest(),
        'source_label_shuffle':{key:value for key,value in shuffle_audit.items() if key!='mapping'},
        'mapping_file':'label_shuffle_mapping.json','mapping_sha256':digest(folder/'label_shuffle_mapping.json'),'mapping_count':len(shuffle_audit['mapping']),
        'note':'고정 짧은 진단이며 주200epoch 학습과 동등한 성능 비교 아님; 결과로 강도·분할·정답을 수정하지 않음'},
        'used_for_model_or_attack_selection':False,'coarse_note':'중앙 사각형은 결절·폐 마스크가 아니며 바깥에도 결절·신체 정보가 있을 수 있음'}
    save_json(folder/'result.json',result);return result

"""환자 계보가 확인된 SCI v2 자료만 소비하는 독립 실행기입니다."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import random
import sys
import uuid
import numpy as np
from PIL import Image
from 실행 import atomic,save_json,read_json,digest,save_torch,lock,cuda_guard,runtime_context,seed_all,rng_state,restore_rng,disk_guard,validation_progress,save_dashboard,now

ROOT=Path(__file__).resolve().parent
PROTOCOL='stage17-luna25-2d-patient-v2'

def experiment_plan(config):
    main=[{'model':'resnet50','regime':regime,'split_boundary':'conv1','sigma':sigma,'kind':'main'}
          for regime in ('split_trainable','full_finetune') for sigma in config['sigmas']]
    auxiliary=[{'model':'resnet18','regime':'full_finetune','split_boundary':'conv1','sigma':0,'kind':'auxiliary'}]
    auxiliary += [{'model':'resnet50','regime':'split_trainable','split_boundary':layer,'sigma':sigma,'kind':'auxiliary'}
                  for layer in ('stem','layer1') for sigma in (0,32)]
    for item in main+auxiliary:
        item['id']=f"{item['model']}_{item['regime']}_{item['split_boundary']}_sigma_{item['sigma']:03d}"
        item['cohort']='LUNA25'
        item['sigma_mm']=item['sigma']*config['roi_pixel_spacing_mm']
    return main+auxiliary

def load_manifest(config):
    path=Path(config['manifest'])
    if not path.exists(): raise FileNotFoundError('공식 결절 영상·주석 준비 manifest가 없습니다: '+str(path))
    manifest=read_json(path)
    if manifest.get('protocol')!=PROTOCOL:
        raise ValueError('기존12차 또는 다른 프로토콜 manifest는 SCI v2에서 사용하지 않습니다.')
    from SCI데이터 import validate_manifest
    validate_manifest(manifest,verify_files=True)
    validate_patient_separation(manifest)
    return manifest

def validate_patient_separation(manifest):
    seen=set()
    for split in ('train','validation','test'):
        rows=manifest['splits'][split]
        if not rows: raise ValueError('SCI 환자 분할이 비어 있습니다: '+split)
        patients={row['patient_id'] for row in rows}
        if not patients or patients&seen: raise ValueError('SCI 환자 분할 간 중복')
        if any(row['label'] not in (0,1) or row['cohort']!='LUNA25' for row in rows): raise ValueError('LUNA25 주실험 라벨·cohort 오류')
        seen|=patients
    return {'patient_overlap':0,'method':'같은 환자의 혼합 라벨 결절도 같은 분할'}

def image(row):
    path=Path(row['image_path'])
    if digest(path)!=row['image_sha256']: raise ValueError('결절 ROI SHA 불일치: '+row['id'])
    with Image.open(path) as source:
        pixels=np.asarray(source.convert('L'),dtype=np.uint8).copy()
    if pixels.shape!=(512,512): raise ValueError('정식 결절 ROI는512×512이어야 합니다.')
    transform=row.get('augmentation')
    if transform:
        if transform['hflip']: pixels=pixels[:,::-1].copy()
        values=pixels.astype(np.float64)
        values=(values-values.mean())*transform['contrast']+values.mean()+transform['brightness']
        pixels=np.rint(np.clip(values,0,255)).astype(np.uint8)
    return pixels.astype(np.float32)/255

class Dataset:
    def __init__(self,rows,training=False): self.rows,self.training=rows,training
    def __len__(self): return len(self.rows)
    def __getitem__(self,index):
        import torch
        row=self.rows[index]
        pixels=image(row)
        if self.training and random.random()<.25: pixels=pixels[:,::-1].copy()
        return torch.from_numpy(pixels)[None],torch.tensor(row['label'],dtype=torch.float32)

def fixed_test_plan(manifest,config):
    rows=[]
    for label in (0,1):
        pool=[r for r in manifest['splits']['test'] if r['label']==label]
        if not pool: raise ValueError('주시험에 두 클래스 모두 필요합니다.')
        if len(pool)>config['test_samples_per_class']: raise ValueError('고정 보조시험 크기보다 원본이 많아 모든 첫 사본을 보존할 수 없습니다.')
        rng=random.Random(config['test_augmentation_seed']+label)
        for index in range(config['test_samples_per_class']):
            source=dict(pool[index%len(pool)])
            original=index<len(pool)
            source.update(id=f"aug_{label}_{index:04d}",source_id=source['id'],canonical=original,
                augmentation={'hflip':False if original else rng.random()<.5,'contrast':1. if original else rng.uniform(.94,1.06),
                              'brightness':0. if original else rng.uniform(-6,6)})
            rows.append(source)
    return {'protocol':PROTOCOL,'seed':config['test_augmentation_seed'],'rows':rows,
            'note':'동일 시험 환자·결절 계보의 보조 증강이며 독립 표본 증가가 아님'}

def bind(config,manifest,runtime,device):
    files=['SCI실행.py','SCI모델.py','SCI공격.py','SCI데이터.py','SCIconfig.json','실행.py','공격.py','특징노출.py','지표.py','전송.py','rust/전송엔진.exe','legacy/model.py','legacy/identity.py','legacy/__init__.py']
    binding={'protocol':PROTOCOL,'config':config,'manifest_sha256':digest(config['manifest']),
             'sources':{name:digest(ROOT/name) for name in files},'execution_context':runtime_context(device)}
    plan=fixed_test_plan(manifest,config)
    plan_path=runtime/'test_plan.json'
    if plan_path.exists() and read_json(plan_path)!=plan: raise ValueError('기존 고정 시험 증강 계획 변경')
    if not plan_path.exists(): save_json(plan_path,plan)
    binding['test_plan_sha256']=digest(plan_path)
    path=runtime/'run.json'
    if path.exists():
        record=read_json(path)
        if record['binding']!=binding: raise ValueError('소스·자료·문맥 변경: 기존 SCI run 재개 거부')
        return record['run_id']
    run_id=uuid.uuid4().hex
    save_json(path,{'run_id':run_id,'created_at':now(),'binding':binding})
    return run_id

def update_status(config,run_id,state,reason=None,current=None):
    runtime=Path(config['runtime'])
    items=[]
    for condition in experiment_plan(config):
        folder=runtime/'conditions'/condition['id']
        item={**condition,'state':'not_started','epoch':0}
        if (folder/'current.json').exists():
            value=read_json(folder/'current.json')
            if value.get('run_id')==run_id:
                item.update({k:value[k] for k in ('state','epoch','best_validation_loss') if k in value})
                for split in ('training','validation'):
                    if split in value: item[split+'_accuracy']=value[split]['accuracy']
        if (folder/'dashboard.json').exists():
            value=read_json(folder/'dashboard.json')
            if value.get('run_id')==run_id:
                item.update(state='completed',test_accuracy=value['classifier']['test']['accuracy'],privacy_score=value['attack']['privacy_score'],
                            result_path=str(folder/'dashboard.json'))
        items.append(item)
    save_json(runtime/'status.json',{'schema':'stage17-sci-v2','protocol':PROTOCOL,'state':state,'reason':reason,'reasons':[] if reason is None else [reason],
        'run_id':run_id,'updated_at':now(),'current_condition':current,'main_conditions':40,'auxiliary_conditions':5,'total_conditions':len(items),
        'completed_conditions':sum(item['state']=='completed' for item in items),'conditions':items,
        'auxiliary_references':[{'model':'resnet50','split_boundary':'conv1','sigma':s,'reference':f'resnet50_split_trainable_conv1_sigma_{s:03d}'} for s in (0,32)],
        'data_status_path':config['data_status'],'limitations':['결절 중심이 제공된 분류 과제이며 결절 탐지 성능이 아님','원본 주시험과 고정 증강 보조시험은 독립적으로 표시']})

def evaluate(model,rows,device,precision,path=None,context=None):
    import torch
    from 지표 import binary_report,grouped_accuracy_interval
    model.eval()
    labels,logits=[],[]
    with torch.no_grad():
        for x,y in torch.utils.data.DataLoader(Dataset(rows),batch_size=2,num_workers=0):
            with torch.autocast(device_type=device,dtype=torch.bfloat16,enabled=precision=='cuda_bf16'):
                predicted=model(x.to(device)).float().cpu()
            labels.extend(y.tolist());logits.extend(predicted.tolist())
    result=binary_report(labels,logits)
    if path is not None:
        from scipy.special import expit
        result.update(grouped_accuracy_interval(labels,logits,[row['patient_id'] for row in rows]))
        result['n_patients']=len({row['patient_id'] for row in rows})
        result.pop('n_similarity_groups',None)
        result['patient_ci95']=result.pop('accuracy_ci95_group')
        result['interval_note']='환자 단위 군집 재표집95% 구간; 환자 내 복수 결절·증강을 함께 재표집'
        if result['n_patients']<2: result['interval_reason']='환자2명 미만으로 군집 구간 미정의'
        records=[{'row_id':row['id'],'source_id':row.get('source_id',row['id']),'patient_id':row['patient_id'],'cohort':row['cohort'],
                  'label':int(label),'rawlogit':float(logit),'probability':float(expit(logit)),'predicted':int(logit>=0)} for row,label,logit in zip(rows,labels,logits)]
        save_json(path,{'protocol':PROTOCOL,**(context or {}),'rows':records})
        result['predictions']={'path':path.relative_to(path.parents[3]).as_posix(),'sha256':digest(path),'rows':len(records)}
    return result

def train_condition(config,manifest,condition,run_id,device,resume=False):
    import torch
    from SCI모델 import SCIResNet,freeze_running_stats
    from 지표 import binary_report
    from 실행 import train_rows
    from SCI공격 import run_protection,run_diagnostics
    folder=Path(config['runtime'])/'conditions'/condition['id']
    if (folder/'result.json').exists():
        if not (folder/'dashboard.json').exists(): save_dashboard(folder,read_json(folder/'result.json'))
        return
    folder.mkdir(parents=True,exist_ok=True)
    seed_all(config['seed'],device=='cuda')
    weights=config['weights'][condition['model']]
    model=SCIResNet(condition['model'],condition['sigma'],condition['split_boundary'],weights['path'],weights['sha256']).to(device)
    precision='cuda_bf16' if device=='cuda' else 'cpu_fp32'
    if device=='cuda' and not torch.cuda.is_bf16_supported(): raise RuntimeError('CUDA BF16 지원 필요')
    optimizer=torch.optim.AdamW(model.parameters(),lr=config['learning_rate'],weight_decay=config['weight_decay'])
    scheduler=torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer,patience=8,factor=.5,min_lr=1e-6)
    start,best,patience_best,bad,best_epoch,history=0,float('inf'),float('inf'),0,0,[]
    pointer=folder/'last.json'
    if pointer.exists():
        if not resume: raise ValueError('기존 epoch 보존본이 있습니다. --resume 필요')
        reference=read_json(pointer);path=folder/reference['path']
        if digest(path)!=reference['sha256']: raise ValueError('epoch 체크포인트 SHA 오류')
        checkpoint=torch.load(path,map_location='cpu',weights_only=False)
        if checkpoint['run_id']!=run_id or checkpoint['condition']!=condition: raise ValueError('체크포인트 실행·조건 불일치')
        model.load_state_dict(checkpoint['model']);optimizer.load_state_dict(checkpoint['optimizer']);scheduler.load_state_dict(checkpoint['scheduler'])
        start,best,patience_best,bad,best_epoch,history=[checkpoint[k] for k in ('epoch','best','patience_best','bad','best_epoch','history')]
        restore_rng(checkpoint['rng'])
    rows=manifest['splits']
    for epoch in range(start,config['epochs']):
        if epoch>=config['min_epochs'] and bad>=config['patience']: break
        estimate=sum(t.numel()*t.element_size() for t in model.state_dict().values())*4
        disk_guard(folder,int(config['reserve_gib']*1024**3)+estimate)
        loader=torch.utils.data.DataLoader(Dataset(train_rows(rows['train'],config['samples_per_class'],config['seed']+epoch),True),batch_size=config['batch_size'],num_workers=0)
        model.train();freeze_running_stats(model);optimizer.zero_grad(set_to_none=True)
        labels,logits=[],[];gradient_evidence=None
        for batch,(x,y) in enumerate(loader):
            x,y=x.to(device),y.to(device)
            group_start=batch//config['accumulation']*config['accumulation']
            divisor=min(config['accumulation'],len(loader)-group_start)
            with torch.autocast(device_type=device,dtype=torch.bfloat16,enabled=precision=='cuda_bf16'):
                if condition['regime']=='split_trainable':
                    prediction,loss,gradient_evidence=model.split_loss_backward(x,y,divisor)
                else:
                    prediction=model(x)
                    loss=torch.nn.functional.binary_cross_entropy_with_logits(prediction.float(),y)
                    (loss/divisor).backward()
            if (batch+1)%config['accumulation']==0 or batch+1==len(loader):
                torch.nn.utils.clip_grad_norm_(model.parameters(),1.);optimizer.step();optimizer.zero_grad(set_to_none=True)
            labels.extend(y.cpu().tolist());logits.extend(prediction.detach().float().cpu().tolist())
        validation=evaluate(model,rows['validation'],device,precision)
        scheduler.step(validation['loss'])
        progress=validation_progress(validation['loss'],best,patience_best,bad,config['min_delta'])
        if progress['is_best']: best,best_epoch=validation['loss'],epoch+1
        patience_best,bad=progress['patience_best'],progress['bad']
        item={**condition,'protocol':PROTOCOL,'run_id':run_id,'state':'classifying','epoch':epoch+1,'training':binary_report(labels,logits),
              'validation':validation,'best_validation_loss':best,'precision':precision,'gradient_return':gradient_evidence}
        history.append(item)
        path=folder/'epochs'/f'epoch_{epoch+1:04d}.pth'
        save_torch(path,{'protocol':PROTOCOL,'run_id':run_id,'condition':condition,'epoch':epoch+1,'model':model.state_dict(),
                        'optimizer':optimizer.state_dict(),'scheduler':scheduler.state_dict(),'rng':rng_state(device=='cuda'),
                        'best':best,'patience_best':patience_best,'bad':bad,'best_epoch':best_epoch,'history':history})
        reference={'path':path.relative_to(folder).as_posix(),'sha256':digest(path),'epoch':epoch+1,'run_id':run_id}
        save_json(pointer,reference)
        if best_epoch==epoch+1: save_json(folder/'best.json',reference)
        save_json(folder/'history.json',history);save_json(folder/'current.json',item)
        update_status(config,run_id,'running',current=condition['id'])
    reference=read_json(folder/'best.json');best_path=folder/reference['path']
    if digest(best_path)!=reference['sha256']: raise ValueError('best 보존본 SHA 불일치')
    model.load_state_dict(torch.load(best_path,map_location='cpu',weights_only=False)['model']);model.eval()
    context={'run_id':run_id,'condition':condition,'checkpoint_sha256':reference['sha256']}
    classifier={'best_epoch':best_epoch,'checkpoint':reference,'test':evaluate(model,rows['test'],device,precision,folder/'predictions'/'test.json',context)}
    generated=read_json(Path(config['runtime'])/'test_plan.json')['rows']
    classifier['test_generated']=evaluate(model,generated,device,precision,folder/'predictions'/'test_generated.json',context)
    external={}
    for cohort in ('CSTL','Histo'):
        external_rows=manifest.get('external',{}).get(cohort,[])
        if isinstance(external_rows,dict): external_rows=external_rows.get('rows',[])
        external[cohort]=evaluate(model,external_rows,device,precision,folder/'predictions'/f'external_{cohort}.json',context) if external_rows else {'state':'blocked','reason':manifest.get('external_status',{}).get(cohort,{}).get('reason','외부 영상·환자계보·양성악성 주석 미확보')}
    protection=run_protection(model,{**rows,'test_generated':generated,'external':manifest.get('external',{}),'external_status':manifest.get('external_status',{})},config,folder,run_id,reference,device,resume)
    diagnostic=run_diagnostics(manifest,config,run_id,device,resume)
    result={**condition,'condition':condition['id'],'protocol':PROTOCOL,'run_id':run_id,'classifier':classifier,'external':external,
            **protection,'diagnostics':diagnostic,'dataset':{split:{'images':len(records),'patients':len({r['patient_id'] for r in records})} for split,records in rows.items()},
            'limitations':['결절 중심이 제공된 분류이며 탐지 성능 아님','증강은 독립 환자 증가 아님','외부 고정시험은 학습·선정에 사용하지 않음']}
    save_json(folder/'result.json',result);save_dashboard(folder,result)
    save_json(folder/'current.json',{**history[-1],'state':'completed'})

def require_previous_experiment_complete(root=Path('D:/2026/폐암 논문/Conv1 블러 OK-NG 실험/12차')):
    """이전 실험의 현재 실행 전체 완료를 읽기 전용으로 확인합니다."""
    try:
        root=Path(root).resolve();config_path=root/'config.json'
        config=read_json(config_path);status=read_json(root/'work'/'runtime'/'status.json')
        if not status.get('run_id') or not status.get('experiment_instance_id'): raise ValueError('현재 실행 식별자 누락')
        if status.get('config_sha256')!=digest(config_path): raise ValueError('현재 상태와 계획 설정 SHA 불일치')
        planned={(regime,sigma) for regime in config['regimes'] for sigma in config['sigmas']}
        conditions=status['conditions'];actual={(r['regime'],r['sigma']) for r in conditions}
        if actual!=planned or len(conditions)!=len(planned): raise ValueError('전체 계획 조건 목록 누락·중복')
        if any(row.get('status')!='completed' for row in conditions): raise ValueError('이전 실험의 미완료 조건이 있음')
        for row in conditions:
            path=(root/row['result_path']).resolve()
            if not path.is_relative_to(root): raise ValueError('이전 결과 경로가 프로젝트 밖임')
            result=read_json(path)
            if any(result.get(key)!=status[key] for key in ('run_id','experiment_instance_id')): raise ValueError('이전 최종 결과 실행 식별자 불일치')
            if result.get('sigma')!=row['sigma'] or result.get('regime')!=row['regime'] or not result.get('completed_at'): raise ValueError('이전 최종 결과 조건·완료 기록 누락')
        return {'run_id':status['run_id'],'conditions':len(conditions),'state':'completed','read_only':True}
    except (OSError,ValueError,KeyError,TypeError) as error:
        raise RuntimeError('12차 현재 실행의 모든 조건 완료를 확인하지 못해 새 CUDA 실행을 거부합니다: '+str(error)) from error


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    action=parser.add_mutually_exclusive_group();action.add_argument('--prepare',action='store_true');action.add_argument('--run',action='store_true');action.add_argument('--resume',action='store_true')
    parser.add_argument('--device',choices=['cpu','cuda'],default='cuda');parser.add_argument('--condition')
    args=parser.parse_args(argv);config=read_json(ROOT/'SCIconfig.json');runtime=Path(config['runtime'])
    try: manifest=load_manifest(config)
    except (FileNotFoundError,ValueError,ImportError) as error:
        update_status(config,None,'blocked',str(error));print(json.dumps({'state':'blocked','reason':str(error),'protocol':PROTOCOL},ensure_ascii=False));return
    selected=experiment_plan(config)
    if args.condition:
        selected=[item for item in selected if item['id']==args.condition]
        if not selected: parser.error('정의되지 않은 SCI 조건 ID')
    if not (args.prepare or args.run or args.resume):
        print(json.dumps(read_json(runtime/'status.json') if (runtime/'status.json').exists() else {'state':'ready','protocol':PROTOCOL},ensure_ascii=False,indent=2));return
    os.environ.setdefault('CUBLAS_WORKSPACE_CONFIG',':4096:8')
    with lock(runtime):
        if (args.run or args.resume) and args.device=='cuda':
            previous=require_previous_experiment_complete()
            save_json(runtime/'previous_experiment_gate.json',previous)
            cuda_guard(runtime/'cuda_guard.json')
        run_id=bind(config,manifest,runtime,args.device)
        update_status(config,run_id,'prepared')
        if args.run or args.resume:
            import torch
            torch.set_num_threads(config['cpu_threads'])
            for condition in selected: train_condition(config,manifest,condition,run_id,args.device,args.resume)
            update_status(config,run_id,'idle')

if __name__=='__main__': main()

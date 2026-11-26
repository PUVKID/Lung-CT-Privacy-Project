"""환자 분할 뒤 한 번 생성하는 고정 PNG와 CPU DCT float32 TIFF 사본입니다."""
from __future__ import annotations
import copy
import hashlib
import io
import json
import random
from pathlib import Path
import numpy as np
from PIL import Image
from 실행 import atomic,digest,lock,read_json,save_json

POLICY='fixed-copies-v1'
ROOT=Path(__file__).resolve().parent

def _sha(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode('utf-8')).hexdigest()

def _sources():
    return {name:digest(ROOT/name) for name in ('SCI고정표본.py','SCI실행.py','SCI모델.py','SCI공격.py','legacy/model.py')}

def _check(path,sha):
    path=Path(path)
    if path.is_symlink() or not path.is_file() or path.stat().st_nlink!=1 or digest(path)!=sha:
        raise ValueError('고정 사본 변경·링크·누락: '+str(path))

def _start(folder,binding):
    folder.mkdir(parents=True,exist_ok=True)
    path=folder/'binding.json'
    if path.exists():
        if read_json(path)!=binding: raise ValueError('고정 표본 입력·설정·소스 변경: '+str(folder))
    else:
        if any(p.name not in ('실행.guard','실행.lock') for p in folder.iterdir()): raise ValueError('결합 기록 없는 고정 표본 폴더')
        save_json(path,binding)

def _write(folder,key,data):
    """완료된 사본은 검증만 하며, 중간 중단은 사전 SHA와 대조해 이어갑니다."""
    path=folder/key;receipt=path.with_name(path.name+'.sha.json')
    expected=hashlib.sha256(data).hexdigest()
    if receipt.exists() and read_json(receipt)!= {'sha256':expected}: raise ValueError('부분 사본 생성 결과 변경')
    if path.exists():
        _check(path,expected)
    else:
        if not receipt.exists(): save_json(receipt,{'sha256':expected})
        atomic(path,lambda p:p.write_bytes(data))
    if not receipt.exists(): save_json(receipt,{'sha256':expected})
    return str(path),expected

def _verify(result):
    for records in result.values():
        for row in records:
            _check(row['image_path'],row['image_sha256'])
            if 'observed_path' in row: _check(row['observed_path'],row['observed_sha256'])

def _completed(folder):
    path=folder/'complete.json'
    receipt=folder/'complete.sha256.json'
    if not receipt.exists(): raise ValueError('완료 index의 SHA 기록 누락')
    _check(path,read_json(receipt)['sha256'])
    return read_json(path)

def _finish(folder,result):
    data=json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2).encode('utf-8')
    # SHA를 먼저 보존하므로 index 저장 중 중단되어도 동일 결과만 이어갈 수 있습니다.
    receipt=folder/'complete.sha256.json';expected={'sha256':hashlib.sha256(data).hexdigest()}
    if receipt.exists() and read_json(receipt)!=expected: raise ValueError('중단된 완료 index 결과 변경')
    if not receipt.exists(): save_json(receipt,expected)
    atomic(folder/'complete.json',lambda p:p.write_bytes(data))

def read_raw(row):
    _check(row['image_path'],row['image_sha256'])
    with Image.open(row['image_path']) as source:
        if source.mode!='L': raise ValueError('고정 원본은 회색 PNG이어야 합니다.')
        return np.asarray(source,dtype=np.float32).copy()/255

def read_observed(row):
    if 'observed_path' not in row: return read_raw(row)
    _check(row['observed_path'],row['observed_sha256'])
    with Image.open(row['observed_path']) as source: result=np.asarray(source).copy()
    if result.dtype!=np.float32 or not np.isfinite(result).all(): raise ValueError('관측 사본은 유한한 float32 TIFF이어야 합니다.')
    return result

def epoch_rows(rows,seed):
    result=list(rows);random.Random(seed).shuffle(result);return result

def prepare_fixed(manifest,config):
    if config.get('input_policy')!=POLICY: raise ValueError('고정 입력 정책 명시 필요')
    # 운영 경로에는 공식 준비기의 전체 검사를 통과한 자료만 생성합니다.
    if Path(config['fixed_samples_root']).resolve()==(ROOT/'work/data/fixed_samples').resolve():
        from SCI데이터 import validate_manifest
        validate_manifest(manifest,verify_files=True)
    counts={'train':config['samples_per_class'],'validation':config['validation_samples_per_class'],'test':config['test_samples_per_class']}
    if any(type(n) is not int or n<=0 for n in counts.values()): raise ValueError('분할별 클래스 수는 양의 정수 필요')
    seen={}
    for split,records in manifest['splits'].items():
        for row in records:
            patient=row.get('global_patient_id',row['patient_id'])
            if patient in seen and seen[patient]!=split: raise ValueError('환자 분할 중복')
            seen[patient]=split;_check(row['image_path'],row['image_sha256'])
    binding={'policy':POLICY,'manifest':manifest,'counts':counts,'seed':config['seed'],'image_size':config['image_size'],'sources':_sources()}
    folder=Path(config['fixed_samples_root'])/'base'
    with lock(folder):
        _start(folder,binding)
        if (folder/'complete.json').exists():
            result=_completed(folder)
            if result['binding_sha256']!=_sha(binding): raise ValueError('완료 표본 결합 변경')
            _verify(result['splits']);return result
        splits={}
        for split,count in counts.items():
            rows=[]
            for label in (0,1):
                pool=[r for r in manifest['splits'][split] if r['label']==label]
                if not pool or len(pool)>count: raise ValueError('모든 원본 첫 사본을 보존할 수 없는 클래스 크기: '+split)
                rng=random.Random(config['seed']+100*list(counts).index(split)+label)
                for index in range(count):
                    original=pool[index%len(pool)];row=copy.deepcopy(original)
                    transform={'hflip':False,'contrast':1.,'brightness':0.}
                    if index>=len(pool): transform={'hflip':rng.random()<.5,'contrast':rng.uniform(.94,1.06),'brightness':rng.uniform(-6,6)}
                    data=Path(original['image_path']).read_bytes()
                    if index>=len(pool):
                        with Image.open(io.BytesIO(data)) as source: values=np.asarray(source,dtype=np.float64).copy()
                        if transform['hflip']: values=values[:,::-1].copy()
                        values=(values-values.mean())*transform['contrast']+values.mean()+transform['brightness']
                        buffer=io.BytesIO();Image.fromarray(np.rint(np.clip(values,0,255)).astype(np.uint8)).save(buffer,format='PNG');data=buffer.getvalue()
                    path,sha=_write(folder,f'{split}/{label}/{index:05d}.png',data)
                    row.update(id=f'fixed_{split}_{label}_{index:05d}',source_id=original['id'],canonical=index<len(pool),
                        original_image_path=original['image_path'],original_image_sha256=original['image_sha256'],
                        image_path=path,image_sha256=sha,materialized=True,input_policy=POLICY,fixed_transform=transform)
                    row.pop('augmentation',None);rows.append(row)
            splits[split]=rows
        result={'policy':POLICY,'binding_sha256':_sha(binding),'splits':splits}
        _finish(folder,result);return result

def prepare_sigma(base,config,sigma,manifest=None):
    """동일 강도의 두 학습 조건은 같은 완료 폴더를 사용합니다. GPU는 호출하지 않습니다."""
    import torch
    from legacy.model import GaussianDCTBlur
    batch_size=config.get('fixed_blur_batch_size',4)
    if type(batch_size) is not int or batch_size<1: raise ValueError('CPU 블러 batch 크기 오류')
    datasets=copy.deepcopy(base['splits'])
    if manifest:
        for cohort,external in manifest.get('external',{}).items():
            records=external.get('rows',[]) if isinstance(external,dict) else external
            if records: datasets['external_'+cohort]=[dict(r,materialized=True,input_policy=POLICY) for r in records]
    binding={'policy':POLICY,'base_sha256':_sha(base),'sigma':float(sigma),'sources':_sources(),'datasets_sha256':_sha(datasets),
        'torch':torch.__version__,'numpy':np.__version__,'backend':'GaussianDCTBlur-cpu-float32','batch_size':batch_size}
    folder=Path(config['fixed_samples_root'])/'sigmas'/('sigma_'+format(float(sigma),'.12g'))
    with lock(folder):
        _start(folder,binding)
        if (folder/'complete.json').exists():
            completed=_completed(folder)
            if completed['binding_sha256']!=_sha(binding): raise ValueError('완료 블러 결합 변경')
            _verify(completed['rows']);return completed['rows']
        blur=GaussianDCTBlur(sigma).cpu()
        for split,rows in datasets.items():
            for start in range(0,len(rows),batch_size):
                batch=rows[start:start+batch_size]
                arrays=[]
                for index,row in enumerate(batch,start):
                    data=Path(row['image_path']).read_bytes()
                    _check(row['image_path'],row['image_sha256'])
                    path,sha=_write(folder,f'{split}/raw/{index:05d}.png',data)
                    row.update(image_path=path,image_sha256=sha);arrays.append(read_raw(row))
                with torch.no_grad(): observed=blur(torch.from_numpy(np.stack(arrays))[:,None])[:,0]
                for index,(row,array) in enumerate(zip(batch,observed.numpy()),start):
                    buffer=io.BytesIO();Image.fromarray(array.astype(np.float32)).save(buffer,format='TIFF')
                    path,sha=_write(folder,f'{split}/observed/{index:05d}.tiff',buffer.getvalue())
                    row.update(observed_path=path,observed_sha256=sha,observed_sigma=float(sigma),preblurred=True)
        _finish(folder,{'binding_sha256':_sha(binding),'rows':datasets});return datasets

def original_rows(cached):
    result=[]
    for row in cached:
        if row.get('canonical'):
            item=dict(row);item['id']=item['source_id'];result.append(item)
    return result

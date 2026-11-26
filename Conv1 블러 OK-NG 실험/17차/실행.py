"""60개 독립 조건의 실제 패킷 준비·분류·복원 실험. 기본 실행은 상태 조회입니다."""
from __future__ import annotations
import argparse
import contextlib
import hashlib
import json
import os
from pathlib import Path
import random
import shutil
import subprocess
import time
import uuid
import sys
import importlib.metadata
import ntpath
import re
from datetime import datetime, timezone, timedelta
import numpy as np
from PIL import Image
from 전송 import PROFILES, encode, decode

ROOT = Path(__file__).resolve().parent

def now():
    return datetime.now(timezone(timedelta(hours=9))).isoformat()

def digest(path):
    h = hashlib.sha256()
    with open(path, 'rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def atomic(path, writer):
    """고유 임시본은 실패 시 보존하며 일시적인 공유 위반만 제한 재시도합니다."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + '.' + uuid.uuid4().hex + '.tmp')
    writer(temp)
    for attempt in range(5):
        try:
            os.replace(temp, path)
            return
        except PermissionError:
            if attempt == 4:
                raise
            time.sleep(0.1 * (attempt + 1))

def save_json(path, data):
    atomic(path, lambda p: p.write_text(json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False), encoding='utf-8'))

def save_torch(path, data):
    import torch
    atomic(path, lambda p: torch.save(data, p))

def dashboard_projection(value):
    """전체 지표는 보존하고 대용량 원본별 배열만 별도 원본 파일에 둡니다."""
    if isinstance(value,dict):
        return {key:dashboard_projection(item) for key,item in value.items()
                if key!='test_per_source_metrics' and not key.endswith('_per_source')}
    if isinstance(value,list):
        return [dashboard_projection(item) for item in value]
    return value

def save_dashboard(folder,result):
    source=folder/'result.json'
    compact=dashboard_projection(result)
    compact['full_result']={'path':source.relative_to(folder.parent.parent).as_posix(),'sha256':digest(source),'bytes':source.stat().st_size}
    save_json(folder/'dashboard.json',compact)

def condition_id(sigma, profile):
    return f'sigma_{int(sigma):03d}_{profile}'

def conditions(config):
    return [(s, p) for s in config['sigmas'] for p in config['profiles']]

def source_binding(config):
    files = [ROOT / n for n in ('실행.py', '공격.py', '특징노출.py', '전송.py', '지표.py', '단서진단.py', 'config.json')]
    files += sorted((ROOT / 'legacy').glob('*.py'))
    files += sorted((ROOT / 'rust').rglob('*.rs'))
    files += [ROOT / '빌드.py']
    files += [ROOT / 'rust' / '전송엔진.exe', Path(config['canonical_manifest'])]
    return {str(p): digest(p) for p in files}

def installed_cudnn_files(torch):
    """cuDNN을 로드하지 않고 Windows PE 파일의 버전 자원만 읽습니다."""
    import ctypes
    from ctypes import wintypes
    version=ctypes.WinDLL('version',use_last_error=True)
    version.GetFileVersionInfoSizeW.argtypes=[wintypes.LPCWSTR,ctypes.POINTER(wintypes.DWORD)]
    version.GetFileVersionInfoSizeW.restype=wintypes.DWORD
    version.GetFileVersionInfoW.argtypes=[wintypes.LPCWSTR,wintypes.DWORD,wintypes.DWORD,ctypes.c_void_p]
    version.GetFileVersionInfoW.restype=wintypes.BOOL
    version.VerQueryValueW.argtypes=[ctypes.c_void_p,wintypes.LPCWSTR,ctypes.POINTER(ctypes.c_void_p),ctypes.POINTER(wintypes.UINT)]
    version.VerQueryValueW.restype=wintypes.BOOL
    files=[]
    for path in sorted((Path(torch.__file__).parent/'lib').glob('cudnn*.dll')):
        size=version.GetFileVersionInfoSizeW(str(path),None)
        file_version=None
        if size:
            buffer=ctypes.create_string_buffer(size)
            pointer=ctypes.c_void_p()
            length=wintypes.UINT()
            if version.GetFileVersionInfoW(str(path),0,size,buffer) and version.VerQueryValueW(buffer,'\\',ctypes.byref(pointer),ctypes.byref(length)) and length.value>=52:
                values=ctypes.cast(pointer,ctypes.POINTER(wintypes.DWORD))
                if values[0]==0xFEEF04BD:
                    file_version='.'.join(str(n) for n in (values[2]>>16,values[2]&65535,values[3]>>16,values[3]&65535))
        stat=path.stat()
        files.append({'path':str(path),'bytes':stat.st_size,'mtime_ns':stat.st_mtime_ns,'pe_file_version':file_version,
                      'version_reason':None if file_version is not None else 'Windows PE 버전 자원을 확인하지 못함'})
    return files

def runtime_context(device):
    """버전 조회는 CUDA 텐서·컨텍스트 생성 없이 수행합니다."""
    import torch
    packages=['torch','torchvision','numpy','scipy','Pillow','scikit-learn','psutil']
    return {'device':device,'precision':'cuda_bf16' if device=='cuda' else 'cpu_fp32',
            'python_executable':sys.executable,'python_version':sys.version,
            'packages':{name:importlib.metadata.version(name) for name in packages},
            'torch_cuda_build':torch.version.cuda,'cudnn_installed_files':installed_cudnn_files(torch),
            'cudnn_runtime_version':None,'cudnn_runtime_note':'CUDA 초기화를 피하기 위해 런타임 조회 미수행; PE 파일 메타데이터이며 전체 파일 SHA 증명 아님',
            'environment':{name:{'present':name in os.environ,'value':os.environ.get(name)}
                           for name in ('CUDA_VISIBLE_DEVICES','CUBLAS_WORKSPACE_CONFIG')}}

def bind(config, runtime, device='cpu'):
    plan=fixed_test_plan(config)
    plan_path=runtime/'test_plan.json'
    if plan_path.exists() and read_json(plan_path)!=plan:
        raise ValueError('고정 시험 증강 계획이 기존 계획과 다릅니다.')
    if not plan_path.exists():
        save_json(plan_path,plan)
    current = {'config': config, 'sources': source_binding(config),'test_plan_sha256':digest(plan_path),'execution_context':runtime_context(device)}
    path = runtime / 'run.json'
    if path.exists():
        record = read_json(path)
        if record['binding'] != current:
            raise ValueError('설정·소스·분할이 기존 run_id와 다릅니다. 기존 결과를 덮어쓸 수 없습니다.')
        return record['run_id']
    run_id = uuid.uuid4().hex
    save_json(path, {'run_id': run_id, 'binding': current, 'created_at': now()})
    return run_id

def canonical(config):
    manifest = read_json(config['canonical_manifest'])
    if manifest['sigma'] != 0:
        raise ValueError('원본 sigma0 manifest가 필요합니다.')
    result = {split: [dict(r) for r in manifest['splits'][split] if r['canonical']] for split in ('train', 'validation', 'test')}
    groups = set()
    for split, expected in [('train', 769), ('validation', 164), ('test', 164)]:
        rows = result[split]
        if len(rows) != expected or len({r['source_id'] for r in rows}) != expected:
            raise ValueError(f'{split} 독립 원본 수 오류')
        split_groups = {r['source_group'] for r in rows}
        if groups & split_groups:
            raise ValueError('분할 간 원본 그룹 중복')
        groups.update(split_groups)
    return result

def original(row):
    path = Path(row['unblurred_path'])
    if digest(path) != row['unblurred_sha256']:
        raise ValueError('sigma0 원본 파일 SHA 불일치: ' + str(path))
    with Image.open(path) as image:
        pixels = np.asarray(image.convert('L'), dtype=np.uint8).copy()
    if pixels.shape != (512, 512):
        raise ValueError('원본은 512×512여야 합니다.')
    if 'fixed_transform' in row:
        transform=row['fixed_transform']
        if transform['hflip']:
            pixels=pixels[:,::-1].copy()
        values=pixels.astype(np.float64)
        values=(values-values.mean())*transform['contrast']+values.mean()+transform['brightness']
        pixels=np.rint(np.clip(values,0,255)).astype(np.uint8)
    return pixels

def validate_generated(records, canonical_test):
    """보조 시험 영상의 계보는 주평가 시험 원본에만 속해야 합니다."""
    ancestors={r['source_id']:r['source_group'] for r in canonical_test}
    if len({r['id'] for r in records})!=len(records):
        raise ValueError('시험 증강 행 ID 중복')
    for row in records:
        if row['source_id'] not in ancestors or ancestors[row['source_id']]!=row['source_group'] or row['split']!='test':
            raise ValueError('시험 증강 영상이 주시험 원본 계보와 다릅니다.')
    return [dict(r) for r in records]

def all_rows(config):
    rows=canonical(config)
    generated=validate_generated(fixed_test_plan(config)['rows'],rows['test'])
    if len(generated)!=2*config['test_samples_per_class']:
        raise ValueError('고정 시험 증강 계획 개수 오류')
    rows['test_generated']=generated
    return rows

def fixed_test_plan(config):
    """같은 시험 원본만 균등 순회하며 모든 조건에서 동일한 고정 변환을 사용합니다."""
    base=canonical(config)['test']
    records=[]
    for label in (0,1):
        pool=[row for row in base if row['label']==label]
        rng=random.Random(config['test_augmentation_seed']+label)
        for index in range(config['test_samples_per_class']):
            row=dict(pool[index%len(pool)])
            identity=index<len(pool)
            row.update(id=f'test_fixed_{label}_{index:04d}',canonical=identity,copy_index=index//len(pool),
                       fixed_transform={'hflip':False if identity else rng.random()<.5,
                                        'contrast':1. if identity else rng.uniform(.94,1.06),
                                        'brightness':0. if identity else rng.uniform(-6,6)})
            records.append(row)
    return {'schema':'stage17-fixed-test-plan-v1','seed':config['test_augmentation_seed'],'samples_per_class':config['test_samples_per_class'],
            'source_manifest_sha256':digest(config['canonical_manifest']),'rows':records,
            'interpretation':'고정 증강 시험2000장; 원본 시험164개 계보이며 환자수·독립원본2000개 아님'}

def dataset_summary(rows):
    return {split:{'images':len(records),'unique_source_ids':len({r['source_id'] for r in records}),
                   'similarity_groups':len({r['source_group'] for r in records}),
                   'canonical_images':sum(bool(r.get('canonical',False)) for r in records),
                   'generated_images':sum(not r.get('canonical',False) for r in records),
                   'counts':{'OK':sum(r['label']==0 for r in records),'NG':sum(r['label']==1 for r in records)},
                   'unit_note':'영상·유사 그룹은 환자 수가 아닙니다.'} for split,records in rows.items()}

def disk_guard(runtime, needed):
    runtime.mkdir(parents=True, exist_ok=True)
    if shutil.disk_usage(runtime).free < needed:
        raise OSError(f'디스크 여유 부족: 최소 {needed} 바이트 필요')

@contextlib.contextmanager
def lock(runtime):
    import psutil
    import msvcrt
    runtime.mkdir(parents=True, exist_ok=True)
    path = runtime / '실행.lock'
    # guard 파일은 삭제하지 않으며 OS byte-lock이 죽은 프로세스의 점유를 해제합니다.
    with (runtime/'실행.guard').open('a+b') as guard:
        if guard.seek(0,2)==0:
            guard.write(b'0')
            guard.flush()
        guard.seek(0)
        try:
            msvcrt.locking(guard.fileno(),msvcrt.LK_NBLCK,1)
        except OSError as error:
            raise RuntimeError('다른 프로세스가 실행 guard를 점유하고 있습니다.') from error
        try:
            if path.exists():
                reason='종료된 PID 또는 재사용된 PID'
                try:
                    old=read_json(path)
                    if type(old['pid']) is not int or old['pid']<=0 or not isinstance(old['created'],(int,float)) or not np.isfinite(old['created']):
                        raise ValueError('PID 기록의 값 범위 오류')
                except (json.JSONDecodeError,UnicodeDecodeError,KeyError,TypeError,ValueError) as error:
                    old=None
                    reason='빈 값 또는 부분 PID 기록: '+str(error)
                if old is not None:
                    try:
                        proc=psutil.Process(old['pid'])
                        if abs(proc.create_time()-old['created'])<.01:
                            raise RuntimeError(f"동일 실행 잠금 PID {old['pid']}가 살아 있습니다.")
                    except psutil.NoSuchProcess:
                        pass
                stale=runtime/('실행.stale.'+uuid.uuid4().hex+'.json')
                os.replace(path,stale)
                save_json(stale.with_name(stale.name+'.reason.txt'),{'reason':reason,'preserved_sha256':digest(stale),'observed_at':now()})
            save_json(path,{'pid':os.getpid(),'created':psutil.Process().create_time()})
            try:
                yield
            finally:
                path.unlink(missing_ok=True)
        finally:
            guard.seek(0)
            msvcrt.locking(guard.fileno(),msvcrt.LK_UNLCK,1)

def gui_process_reason(executable):
    """관측한 Windows 화면 프로세스의 정확한 설치 위치만 좁게 허용합니다."""
    path=ntpath.normcase(ntpath.abspath(executable))
    windows=ntpath.normcase(os.environ.get('SystemRoot',r'C:\Windows'))
    program=ntpath.normcase(os.environ.get('ProgramFiles',r'C:\Program Files'))
    program86=ntpath.normcase(os.environ.get('ProgramFiles(x86)',r'C:\Program Files (x86)'))
    if path in {windows+r'\explorer.exe',windows+r'\system32\shellhost.exe'}:
        return '확인한 Windows 셸 실행 경로'
    systemapps=ntpath.join(windows,'systemapps')+chr(92)
    if path.startswith(systemapps):
        relative=path[len(systemapps):]
        patterns=[r'microsoftwindows\.client\.cbs_[^\\]+\\(?:searchhost|crossdeviceresume|textinputhost)\.exe',
                  r'microsoft\.windows\.startmenuexperiencehost_[^\\]+\\startmenuexperiencehost\.exe',
                  r'shellexperiencehost_[^\\]+\\shellexperiencehost\.exe']
        if any(re.fullmatch(pattern,relative) for pattern in patterns):
            return '확인한 Windows SystemApps 화면 프로세스'
    browsers=[program+r'\google\chrome\application\chrome.exe',program86+r'\google\chrome\application\chrome.exe',
              program86+r'\microsoft\edge\application\msedge.exe',program+r'\microsoft\edge\application\msedge.exe']
    local=os.environ.get('LOCALAPPDATA')
    if local:
        browsers.append(ntpath.normcase(local)+r'\google\chrome\application\chrome.exe')
    if path in browsers:
        return '확인한 Chrome/Edge 브라우저 설치 경로'
    for base in (program,program86):
        prefix=ntpath.join(base,'microsoft','edgewebview','application')+chr(92)
        if path.startswith(prefix) and re.fullmatch(r'[0-9.]+\\msedgewebview2\.exe',path[len(prefix):]):
            return '확인한 Edge WebView 버전 디렉터리'
    prefix=ntpath.join(program,'windowsapps')+chr(92)
    if path.startswith(prefix):
        relative=path[len(prefix):]
        patterns=[r'openai\.codex_[0-9.]+_x64__2p2nqsd0c76g0\\app\\chatgpt\.exe',
                  r'microsoft\.windowsnotepad_[0-9.]+_x64__8wekyb3d8bbwe\\notepad\\notepad\.exe',
                  r'microsoft\.windowsterminal_[0-9.]+_x64__8wekyb3d8bbwe\\windowsterminal\.exe',
                  r'microsoft\.yourphone_[0-9.]+_x64__8wekyb3d8bbwe\\phoneexperiencehost\.exe']
        if any(re.fullmatch(pattern,relative) for pattern in patterns):
            return '확인한 Codex 또는 Windows 화면 앱 패키지 경로'
    return None

def cuda_guard(audit_path=None,status_path=None):
    """기존 학습·계산·미확인 작업은 차단하고 확인한 GUI 경로만 허용합니다."""
    import psutil
    status_path=Path(status_path) if status_path is not None else Path('D:/2026/폐암 논문/Conv1 블러 OK-NG 실험/12차/work/runtime/status.json')
    audit={'checked_at':now(),'policy':'현재 학습 PID와 계산 프로세스 거부; 경로 확인한 GUI만 좁게 허용; 기타 failclosed','processes':[]}
    def reject(reason):
        audit['decision']='blocked'
        audit['reason']=reason
        if audit_path is not None:
            save_json(audit_path,audit)
        raise RuntimeError(reason)
    if status_path.exists():
        owner=read_json(status_path)
        try:
            known=psutil.Process(owner['pid'])
            if abs(known.create_time()-owner['process_created'])<.01:
                reject(f"기존12차 학습 PID {owner['pid']}가 살아 있어 새 CUDA 학습을 거부합니다.")
            audit['prior_owner']='PID 재사용: 생성시각 불일치'
        except psutil.NoSuchProcess:
            audit['prior_owner']='기존 기록 PID는 종료됨'
        except psutil.AccessDenied:
            reject('기존12차 PID의 생존 확인 권한이 없어 CUDA 실행을 거부합니다.')
    proc=subprocess.run(['nvidia-smi','--query-compute-apps=pid,process_name','--format=csv,noheader'],capture_output=True,text=True,check=True,timeout=15)
    for line in proc.stdout.splitlines():
        if not line.strip():
            continue
        parts=line.split(',',1)
        if len(parts)!=2 or not parts[0].strip().isdigit():
            reject('nvidia-smi PID 응답을 해석할 수 없어 CUDA 실행을 거부합니다.')
        pid=int(parts[0].strip())
        requested=parts[1].strip()
        if pid==os.getpid():
            continue
        record={'pid':pid,'reported_executable':requested}
        audit['processes'].append(record)
        try:
            process=psutil.Process(pid)
            created=process.create_time()
            executable=process.exe()
            command=process.cmdline()
            if abs(psutil.Process(pid).create_time()-created)>.001:
                reject(f'GPU 조회 중 PID {pid}가 재사용되어 실행을 거부합니다.')
            record.update(executable=executable,created=created,command_argc=len(command),
                          command_sha256=hashlib.sha256(json.dumps(command,ensure_ascii=False).encode('utf-8')).hexdigest())
        except psutil.NoSuchProcess:
            record['decision']='조회 중 종료: 현재 계산 점유로 판단하지 않음'
            continue
        except psutil.AccessDenied:
            reject(f'GPU PID {pid}의 실행 경로·명령을 확인할 수 없어 실행을 거부합니다.')
        actual=ntpath.normcase(ntpath.abspath(executable))
        reported=ntpath.normcase(requested)
        if (ntpath.isabs(reported) and reported!=actual) or (not ntpath.isabs(reported) and ntpath.basename(actual)!=reported):
            reject(f'GPU PID {pid}의 조회 경로와 실제 실행 경로가 달라 실행을 거부합니다.')
        basename=ntpath.basename(actual)
        if re.fullmatch(r'python(?:w|[0-9.]*)?\.exe',basename) or basename in {'torchrun.exe','accelerate.exe','deepspeed.exe','jupyter.exe'}:
            reject(f'다른 Python/계산 프로세스 PID {pid}가 GPU 목록에 있어 새 학습을 거부합니다.')
        reason=gui_process_reason(executable)
        if reason is None:
            reject(f'GPU PID {pid}의 작업 종류가 확인한 GUI 허용목록에 없어 실행을 거부합니다: {executable}')
        record.update(decision='allowed_gui',reason=reason)
    audit['decision']='allowed'
    audit['limitation']='관측 시점의 계산 충돌 방어이며 모든 GPU 사용이 없다는 보장·GUI 서명 인증은 아님'
    if audit_path is not None:
        save_json(audit_path,audit)
    return audit

def required_packet_bytes(rows,runtime,selected,run_id):
    """해시까지 맞는 기존 패킷은 추가 공간으로 다시 계산하지 않습니다."""
    needed=0
    for sigma,profile in selected:
        folder=runtime/'conditions'/condition_id(sigma,profile)
        if (folder/'data.json').exists() and read_json(folder/'data.json')['run_id']!=run_id:
            raise ValueError('기존 패킷 자료 run_id 불일치')
        size,bits=PROFILES[profile]
        packet_size=9+(size*size*bits+7)//8
        for split,records in rows.items():
            for row in records:
                path=folder/'packets'/split/(row['id']+'.ctb')
                meta_path=path.with_suffix('.json')
                if path.exists() and meta_path.exists():
                    meta=read_json(meta_path)
                    if meta['sha256']!=digest(path) or meta['source_sha256']!=row['unblurred_sha256'] or path.stat().st_size!=packet_size:
                        raise ValueError('기존 패킷 공간 산정 중 무결성 오류')
                    decode(path.read_bytes())
                else:
                    needed+=packet_size
    return needed

def prepare(config, runtime, selected, run_id):
    rows = all_rows(config)
    reserve = int(config['reserve_gib'] * 1024**3)
    estimate = required_packet_bytes(rows,runtime,selected,run_id)
    disk_guard(runtime, int(estimate) + reserve)
    for sigma, profile in selected:
        folder = runtime / 'conditions' / condition_id(sigma, profile)
        output = {}
        byte_count, elapsed, count = 0, 0., 0
        for split, records in rows.items():
            output[split] = []
            for row in records:
                pixels = original(row)
                packet_path = folder / 'packets' / split / (row['id'] + '.ctb')
                metadata_path = packet_path.with_suffix('.json')
                if packet_path.exists() and metadata_path.exists():
                    metadata = read_json(metadata_path)
                    if metadata['sha256'] != digest(packet_path) or metadata['source_sha256'] != row['unblurred_sha256']:
                        raise ValueError('저장 패킷 무결성 오류')
                    packet = packet_path.read_bytes()
                    seconds = metadata['encode_seconds']
                else:
                    start = time.perf_counter()
                    packet = encode(pixels, sigma, profile)
                    seconds = time.perf_counter() - start
                    atomic(packet_path, lambda p: p.write_bytes(packet))
                    metadata = {'sha256': digest(packet_path), 'source_sha256': row['unblurred_sha256'], 'encode_seconds': seconds}
                    save_json(metadata_path, metadata)
                decode(packet)
                output[split].append({**row, 'packet_path': str(packet_path), 'packet_sha256': metadata['sha256']})
                byte_count += len(packet)
                elapsed += seconds
                count += 1
        save_json(folder / 'data.json', {'run_id': run_id, 'sigma': sigma, 'profile': profile, 'splits': output,'test_plan_sha256':digest(runtime/'test_plan.json'),
                  'packet': {'count': count, 'total_bytes': byte_count, 'mean_bytes': byte_count/count, 'encode_seconds': elapsed,
                             'timing_scope': '블러+축소+Rust 프로세스 인코딩, 로컬이며 네트워크 시간 아님'}})
        if not (folder / 'current.json').exists():
            save_json(folder / 'current.json', {'run_id':run_id,'state': 'prepared', 'epoch': 0})
        write_status(config, runtime, run_id, 'prepared')

def write_status(config, runtime, run_id, state, current=None):
    summaries = []
    for sigma, profile in conditions(config):
        cid = condition_id(sigma, profile)
        folder = runtime / 'conditions' / cid
        item = {'id': cid, 'sigma': sigma, 'profile': profile, 'state': 'not_started', 'epoch': 0}
        if (folder / 'current.json').exists():
            info = read_json(folder / 'current.json')
            item.update({k: info[k] for k in ('state', 'epoch', 'best_validation_loss') if k in info})
            for split in ('training', 'validation'):
                if split in info:
                    item[split + '_accuracy'] = info[split]['accuracy']
        if (folder / 'dashboard.json').exists():
            result = read_json(folder / 'dashboard.json')
            item.update(state='completed', test_accuracy=result['classifier']['test']['accuracy'],
                        privacy_score=result['attack']['privacy_score'], result_path=str(folder / 'result.json'))
        summaries.append(item)
    save_json(runtime / 'status.json', {'schema': 'stage17-v1', 'run_id': run_id, 'state': state, 'updated_at': now(),
              'current_condition': current, 'completed_conditions': sum(x['state']=='completed' for x in summaries),
              'total_conditions': len(summaries), 'conditions': summaries})

def seed_all(seed, include_cuda=False):
    import torch
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if include_cuda:
        torch.cuda.manual_seed_all(seed)
    torch.use_deterministic_algorithms(True)

def rng_state(include_cuda=False):
    import torch
    return {'python': random.getstate(), 'numpy': np.random.get_state(), 'torch': torch.get_rng_state(),
            'cuda': torch.cuda.get_rng_state_all() if include_cuda else None}

def restore_rng(state):
    import torch
    random.setstate(state['python'])
    np.random.set_state(state['numpy'])
    torch.set_rng_state(state['torch'])
    if state['cuda'] is not None:
        torch.cuda.set_rng_state_all(state['cuda'])

class PacketDataset:
    def __init__(self, rows, flip=False, target=False):
        self.rows, self.flip, self.target = rows, flip, target
    def __len__(self):
        return len(self.rows)
    def __getitem__(self, index):
        import torch
        row = self.rows[index]
        path = Path(row['packet_path'])
        if digest(path) != row['packet_sha256']:
            raise ValueError('학습 입력 패킷 해시 불일치')
        pixels = decode(path.read_bytes())
        if self.target:
            target = original(row).astype(np.float32)/255
            return torch.from_numpy(pixels.astype(np.float32)/255)[None], torch.from_numpy(target)[None]
        if self.flip and random.random() < .25:
            pixels = pixels[:, ::-1].copy()
        x = torch.from_numpy(pixels.astype(np.float32)/255)[None].repeat(3, 1, 1)
        return x, torch.tensor(row['label'], dtype=torch.float32)

def train_rows(rows, count, seed):
    rng = random.Random(seed)
    selected = []
    for label in (0, 1):
        pool = [r for r in rows if r['label'] == label]
        if not pool:
            raise ValueError('학습 클래스가 비었습니다.')
        selected.extend(rng.choices(pool, k=count))
    rng.shuffle(selected)
    return selected

def evaluate(model, rows, device, precision, group_ci=False, prediction_path=None, prediction_root=None, prediction_context=None):
    import torch
    from 지표 import binary_report
    loader = torch.utils.data.DataLoader(PacketDataset(rows), batch_size=2, shuffle=False, num_workers=0)
    model.eval()
    labels, predictions = [], []
    with torch.no_grad():
        for x, y in loader:
            x, y = x.to(device), y.to(device)
            with torch.autocast(device_type=device, dtype=torch.bfloat16, enabled=precision=='cuda_bf16'):
                logits = model.forward_from_blurred(x)
            labels.extend(y.cpu().tolist())
            predictions.extend(logits.float().cpu().tolist())
    report=binary_report(labels,predictions)
    if group_ci:
        from 지표 import grouped_accuracy_interval
        report.update(grouped_accuracy_interval(labels,predictions,[r['source_group'] for r in rows]))
    if prediction_path is not None:
        from scipy.special import expit
        if prediction_root is None or len(rows)!=len(predictions):
            raise ValueError('최종 예측 저장 경로·행수 오류')
        records=[{'row_id':row['id'],'source_id':row['source_id'],'source_group':row['source_group'],
                  'label':int(label),'rawlogit':float(logit),'probability':float(expit(logit)),'predicted':int(logit>=0)}
                 for row,label,logit in zip(rows,labels,predictions)]
        artifact={'schema':'stage17-final-predictions-v1','split':Path(prediction_path).stem,
                  **(prediction_context or {}),'rows':records}
        save_json(prediction_path,artifact)
        report['predictions']={'path':Path(prediction_path).relative_to(prediction_root).as_posix(),
                               'sha256':digest(prediction_path),'rows':len(records),'schema':artifact['schema']}
    return report

def validation_progress(loss,best,patience_best,bad,min_delta):
    """최저 손실 모델 선정과 patience의 유의미 개선 기준을 분리합니다."""
    meaningful=loss<patience_best-min_delta
    return {'is_best':loss<best,'best':min(best,loss),'patience_best':loss if meaningful else patience_best,
            'bad':0 if meaningful else bad+1,'meaningful_improvement':meaningful}

def export_feature_maps(model,rows,folder,device,best_epoch):
    """최종 best 모델의 실제 순전파에서 Conv1 출력만 관측합니다."""
    import torch
    model.eval()
    reports={}
    for label,name in [(0,'OK'),(1,'NG')]:
        row=next(r for r in rows if r['label']==label)
        image,_=PacketDataset([row])[0]
        observed=[]
        hook=model.front.conv1.register_forward_hook(lambda module,args,result:observed.append(result.detach().float().cpu()))
        try:
            with torch.no_grad():
                model.forward_from_blurred(image[None].to(device))
        finally:
            hook.remove()
        if len(observed)!=1:
            raise ValueError('대표사진 Conv1 출력 관측 횟수 오류')
        activation=observed[0]
        summary=activation[0].abs().mean(0).numpy()
        low,high=float(summary.min()),float(summary.max())
        scaled=np.zeros_like(summary) if high==low else (summary-low)/(high-low)
        pixels=np.rint(scaled*255).astype(np.uint8)
        path=folder/'examples'/f'{name}_feature_map.png'
        atomic(path,lambda p:Image.fromarray(pixels).save(p,format='PNG'))
        reports[name]={'path':path.relative_to(folder.parent.parent).as_posix(),
            'settings':{'layer':'front.conv1','aggregation':'mean_absolute_channels','normalization':'per_image_min_max',
                        'raw_min':low,'raw_max':high,'activation_shape':list(activation.shape),'checkpoint':'best.pth','best_epoch':best_epoch,
                        'interpretation':'분류기 내부 실제 Conv1의 채널 절댓값 평균; 전송한 특징맵이 아님'}}
    return reports

def classify(config, folder, data, device, resume, run_id):
    import torch
    from 지표 import binary_report
    from legacy.model import SplitResNet50, block_weight_downloads
    block_weight_downloads()
    seed_all(config['seed'],device=='cuda')
    model = SplitResNet50(sigma=data['sigma'], pretrained=True, weights_path=config['initial_weights_path'],
                         expected_weights_sha256=config['initial_weights_sha256'], regime='full_finetune').to(device)
    precision = 'cuda_bf16' if device=='cuda' else 'cpu_fp32'
    if device=='cuda' and not torch.cuda.is_bf16_supported():
        raise RuntimeError('CUDA BF16 지원이 필요합니다.')
    optimizer = torch.optim.AdamW(model.parameters(), lr=config['learning_rate'], weight_decay=config['weight_decay'])
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=8, factor=.5, min_lr=1e-6)
    start, best, bad, best_epoch, history = 0, float('inf'), 0, 0, []
    patience_best=float('inf')
    last, best_path = folder / 'last.pth', folder / 'best.pth'
    if (folder / 'classifier.json').exists():
        return read_json(folder / 'classifier.json')
    if last.exists():
        if not resume:
            raise RuntimeError('기존 체크포인트가 있습니다. --resume으로 epoch 경계에서 재개하세요.')
        ckpt = torch.load(last, map_location='cpu', weights_only=False)
        if ckpt['run_id'] != run_id:
            raise ValueError('체크포인트 run_id 불일치')
        model.load_state_dict(ckpt['model'])
        optimizer.load_state_dict(ckpt['optimizer'])
        scheduler.load_state_dict(ckpt['scheduler'])
        start,best,bad,best_epoch,history = [ckpt[k] for k in ('epoch','best','bad','best_epoch','history')]
        patience_best=ckpt['patience_best']
        restore_rng(ckpt['rng'])
    rows = data['splits']
    for epoch in range(start, config['epochs']):
        if epoch >= config['min_epochs'] and bad >= config['patience']:
            break
        disk_guard(folder, int(config['reserve_gib'] * 1024**3))
        selected = train_rows(rows['train'], config['samples_per_class'], config['seed'] + epoch)
        loader = torch.utils.data.DataLoader(PacketDataset(selected, flip=True), batch_size=config['batch_size'], num_workers=0, shuffle=False)
        model.train()
        for module in model.modules():
            if isinstance(module, torch.nn.modules.batchnorm._BatchNorm):
                module.eval()
        optimizer.zero_grad(set_to_none=True)
        loss_sum, correct, total = 0., 0, 0
        train_labels,train_logits=[],[]
        for batch, (x,y) in enumerate(loader):
            x,y = x.to(device),y.to(device)
            with torch.autocast(device_type=device, dtype=torch.bfloat16, enabled=precision=='cuda_bf16'):
                logits = model.forward_from_blurred(x)
                targets = y * .98 + .01
                loss = torch.nn.functional.binary_cross_entropy_with_logits(logits.float(), targets)
            # 각 누적 묶음의 마지막 불완전 묶음도 올바르게 정규화합니다.
            group_start = (batch // config['accumulation']) * config['accumulation']
            group_size = min(config['accumulation'], len(loader)-group_start)
            (loss/group_size).backward()
            if (batch+1)%config['accumulation']==0 or batch+1==len(loader):
                torch.nn.utils.clip_grad_norm_(model.parameters(), 1.)
                optimizer.step()
                optimizer.zero_grad(set_to_none=True)
            loss_sum += loss.item()*len(y)
            correct += int(((logits >= 0)==(y >= .5)).sum())
            total += len(y)
            train_labels.extend(y.cpu().tolist())
            train_logits.extend(logits.detach().float().cpu().tolist())
        validation = evaluate(model, rows['validation'], device, precision)
        scheduler.step(validation['loss'])
        progress=validation_progress(validation['loss'],best,patience_best,bad,config['min_delta'])
        if progress['is_best']:
            best,best_epoch = validation['loss'],epoch+1
            save_torch(best_path, {'run_id': run_id, 'model': model.state_dict(), 'epoch': best_epoch})
        bad,patience_best=progress['bad'],progress['patience_best']
        training_report=binary_report(train_labels,train_logits)
        training_report['optimization_smoothed_loss']=loss_sum/total
        item = {'run_id':run_id,'state': 'classifying', 'epoch': epoch+1, 'training': training_report,
                'validation': validation, 'best_validation_loss':best, 'patience_validation_loss':patience_best,'learning_rate':optimizer.param_groups[0]['lr'], 'precision':precision}
        history.append(item)
        save_torch(last, {'run_id':run_id,'model':model.state_dict(),'optimizer':optimizer.state_dict(),'scheduler':scheduler.state_dict(),
                         'epoch':epoch+1,'best':best,'patience_best':patience_best,'bad':bad,'best_epoch':best_epoch,'history':history,'rng':rng_state(device=='cuda')})
        save_json(folder/'history.json',history)
        save_json(folder/'current.json',item)
        write_status(config, folder.parent.parent, run_id, 'running', folder.name)
    model.load_state_dict(torch.load(best_path,map_location='cpu',weights_only=False)['model'])
    prediction_context={'run_id':run_id,'checkpoint_sha256':digest(best_path)}
    result = {'test':evaluate(model,rows['test'],device,precision,group_ci=True,prediction_path=folder/'predictions'/'test.json',
                              prediction_root=folder.parent.parent,prediction_context=prediction_context),'best_epoch':best_epoch,'best_validation_loss':best,
              'precision':precision,'training_samples_per_epoch':2*config['samples_per_class'],'independent_training_sources':769}
    if 'test_generated' in rows:
        result['test_generated']=evaluate(model,rows['test_generated'],device,precision,group_ci=True,
                     prediction_path=folder/'predictions'/'test_generated.json',prediction_root=folder.parent.parent,prediction_context=prediction_context)
        result['test_generated']['interpretation']='같은 시험 원본164개 계보의2000장 고정 증강평가; 독립2000원본 아님'
    result['feature_maps']=export_feature_maps(model,rows['validation'],folder,device,best_epoch)
    result['checkpoint_sha256']=prediction_context['checkpoint_sha256']
    save_json(folder/'classifier.json',result)
    return result

def run_condition(config, runtime, sigma, profile, device, resume, run_id):
    from 공격 import run_attack
    folder = runtime/'conditions'/condition_id(sigma,profile)
    if (folder/'result.json').exists():
        if not (folder/'dashboard.json').exists():
            save_dashboard(folder,read_json(folder/'result.json'))
        return
    data = read_json(folder/'data.json')
    if data['run_id'] != run_id:
        raise ValueError('준비 데이터 run_id 불일치')
    classifier = classify(config,folder,data,device,resume,run_id)
    current = read_json(folder/'current.json')
    current['state'] = 'attacking'
    save_json(folder/'current.json',current)
    write_status(config,runtime,run_id,'running',folder.name)
    attack = run_attack(config,folder,data,device,resume,run_id)
    from 특징노출 import FeatureExposure
    feature_exposure=FeatureExposure(folder/'best.pth',classifier['checkpoint_sha256'],device=device)
    feature_attack=run_attack(config,folder,data,device,resume,run_id,exposure=feature_exposure)
    feature_examples={example['label']:example for example in feature_attack['examples']}
    for example in attack['examples']:
        feature=classifier['feature_maps'][example['label']]
        example['feature_map']=feature['path']
        example['settings']['feature_map']=feature['settings']
        feature_example=feature_examples[example['label']]
        example['feature_reconstructed']=feature_example['reconstructed']
        example['settings']['feature_reconstruction']={'selected_attack':feature_attack['selected_family'],
                    'checkpoint_sha256':feature_exposure.expected_sha256,'exposure_layer':'front.conv1','precision':'fp32',
                    'photo_decoder_reused':True,'threat_model':'알려진 best Conv1 whitebox; 서버 내부 특징 노출 가정'}
    diagnostics_path=folder/'diagnostics.json'
    if not diagnostics_path.exists():
        from 단서진단 import diagnose
        save_json(diagnostics_path,diagnose(data['splits']))
    result = {'condition':folder.name,'sigma':sigma,'profile':profile,'run_id':run_id,'classifier':classifier,'attack':attack,'feature_attack':feature_attack,'packet':data['packet'],'examples':attack['examples'],'diagnostics':read_json(diagnostics_path),'dataset':dataset_summary(data['splits']),'test_plan_sha256':data['test_plan_sha256'],
              'limitations':['환자ID 없음: 영상 원본 그룹 분할','12차에서 이미 사용한 시험셋의 탐색 비교','로컬 패킷 모의 전송: 네트워크 실측 아님','복원오차 점수는 성공확률·프라이버시 보장이 아님']}
    save_json(folder/'result.json',result)
    save_dashboard(folder,result)
    current['state'] = 'completed'
    save_json(folder/'current.json',current)
    (folder/'last.pth').unlink(missing_ok=True)
    (folder/'decoder_last.pth').unlink(missing_ok=True)

def smoke(runtime):
    """GPU·원본·분류 모델을 사용하지 않는 작은 CPU 최적화 및 패킷 왕복 검사입니다."""
    import torch
    torch.set_num_threads(2)
    seed_all(42)
    results=[]
    image = np.arange(512*512,dtype=np.uint8).reshape(512,512)
    for profile in PROFILES:
        packet=encode(image,2,profile)
        pixels=decode(packet)
        assert pixels.shape==(512,512) and pixels.dtype==np.uint8
        results.append({'profile':profile,'bytes':len(packet)})
    tiny=torch.nn.Conv2d(1,1,1)
    optimizer=torch.optim.AdamW(tiny.parameters())
    x=torch.from_numpy(pixels[:8,:8].astype(np.float32)/255)[None,None]
    loss=(tiny(x)-x).square().mean()
    loss.backward()
    optimizer.step()
    checkpoint=runtime/'smoke_checkpoint.pth'
    save_torch(checkpoint,{'model':tiny.state_dict(),'optimizer':optimizer.state_dict(),'rng':rng_state(),'epoch':1})
    restored=torch.nn.Conv2d(1,1,1)
    restored_optimizer=torch.optim.AdamW(restored.parameters())
    saved=torch.load(checkpoint,map_location='cpu',weights_only=False)
    restored.load_state_dict(saved['model'])
    restored_optimizer.load_state_dict(saved['optimizer'])
    restore_rng(saved['rng'])
    assert torch.equal(tiny(x),restored(x))
    restored_optimizer.zero_grad(set_to_none=True)
    second=(restored(x)-x).square().mean()
    second.backward()
    restored_optimizer.step()
    from 공격 import decoder_model, metrics, deblur
    decoder=decoder_model()
    decoder_optimizer=torch.optim.AdamW(decoder.parameters())
    decoder_loss=(decoder(x)-x).square().mean()
    decoder_loss.backward()
    decoder_optimizer.step()
    reconstructed=deblur(pixels.astype(np.float32)/255,2,.1)
    measured=metrics(image.astype(np.float32)/255,reconstructed)
    save_json(runtime/'smoke.json',{'kind':'CPU 합성 패킷·작은 모델·복원·epoch 체크포인트 재개 검사; 정식 학습 아님',
              'profiles':results,'tiny_loss':loss.item(),'resumed_loss':second.item(),'decoder_loss':decoder_loss.item(),
              'resume_equal':True,'reconstruction':measured})

def main(argv=None):
    from SCI실행 import main as sci_main
    return sci_main(argv)
    parser=argparse.ArgumentParser(description=__doc__)
    actions=parser.add_mutually_exclusive_group()
    actions.add_argument('--prepare',action='store_true')
    actions.add_argument('--run',action='store_true')
    actions.add_argument('--resume',action='store_true')
    actions.add_argument('--smoke',action='store_true')
    parser.add_argument('--condition',help='예: 2:블러_축소128; 미지정이면 전체60조건')
    parser.add_argument('--device',choices=['cpu','cuda'],default='cuda')
    args=parser.parse_args(argv)
    config=read_json(ROOT/'config.json')
    runtime=Path(config['runtime'])
    if not any((args.prepare,args.run,args.resume,args.smoke)):
        print(json.dumps(read_json(runtime/'status.json') if (runtime/'status.json').exists() else {'state':'not_started','total_conditions':len(conditions(config))},ensure_ascii=False,indent=2))
        return
    selected=conditions(config)
    if args.condition:
        sigma,profile=args.condition.split(':',1)
        candidate=(int(sigma),profile)
        if candidate not in selected:
            parser.error('정의되지 않은 조건')
        selected=[candidate]
    os.environ.setdefault('CUBLAS_WORKSPACE_CONFIG',':4096:8')
    with lock(runtime):
        if args.smoke:
            smoke(runtime)
            return
        if args.run or args.resume:
            if args.device=='cuda':
                cuda_guard(runtime/'cuda_guard.json')
        run_id=bind(config,runtime,args.device)
        prepare(config,runtime,selected,run_id)
        if args.run or args.resume:
            import torch
            torch.set_num_threads(config['cpu_threads'])
            for sigma,profile in selected:
                run_condition(config,runtime,sigma,profile,args.device,args.resume,run_id)
            write_status(config,runtime,run_id,'idle')

if __name__=='__main__':
    main()

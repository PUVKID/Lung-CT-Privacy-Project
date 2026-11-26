"""이전 엔진 회귀 검사 전용 설정·합성 계보. 현 SCI 설정과 실제 자료는 변경하지 않습니다."""
from contextlib import contextmanager
from pathlib import Path
import tempfile,json
ROOT=Path(__file__).resolve().parents[2]
def legacy_config():
    config=json.loads((ROOT/'SCIconfig.json').read_text(encoding='utf-8'))
    weights=config['weights']['resnet50']
    config.update(initial_weights_path=weights['path'],initial_weights_sha256=weights['sha256'],
                  profiles=['블러만','블러_축소128_8비트','블러_축소64_4비트'])
    config['reconstruction']['weight_decay']=1e-5
    from 전송 import PROFILES
    config['profiles']=list(PROFILES)
    return config
@contextmanager
def legacy_manifest_config():
    with tempfile.TemporaryDirectory() as temporary:
        splits={split:[{'id':f'{split}_{i}','source_id':f'{split}_{i}','source_group':f'{split}_group_{i}',
                        'label':i%2,'canonical':True,'split':split} for i in range(count)]
                for split,count in [('train',769),('validation',164),('test',164)]}
        p=Path(temporary)/'합성_이전계보.json';p.write_text(json.dumps({'sigma':0,'splits':splits}),encoding='utf-8')
        yield {**legacy_config(),'canonical_manifest':str(p)}

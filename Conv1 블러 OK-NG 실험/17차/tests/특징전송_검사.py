"""실제 Rust 프로세스의 특징 직렬화·복호화와 손상 거부를 확인합니다."""
import struct
import subprocess
from pathlib import Path
import numpy as np

ENGINE = Path(__file__).resolve().parents[1] / 'rust' / '전송엔진.exe'

def call(args, payload):
    return subprocess.run([str(ENGINE), *args], input=payload, capture_output=True, timeout=20)

def main():
    for dtype, code, values in [('f32',1,np.array([-1.25,0,2.5],dtype='<f4')),
                                ('f16',2,np.array([-1.25,0,2.5],dtype='<f2')),
                                ('i8',3,np.array([-127,0,127],dtype='i1'))]:
        raw=values.tobytes()
        encoded=call(['feature-encode',dtype,'3'],raw)
        assert encoded.returncode==0, encoded.stderr
        packet=encoded.stdout
        assert packet[:9]==b'FTR1'+bytes([code])+struct.pack('<I',3)
        assert len(packet)==9+len(raw)
        decoded=call(['feature-decode'],packet)
        assert decoded.returncode==0 and decoded.stdout==raw
        for corrupt in (packet[:-1],packet+b'X',b'FTR1'+bytes([9])+packet[5:],b'FTR1'+bytes([code])+struct.pack('<I',0)+raw):
            assert call(['feature-decode'],corrupt).returncode==2
    for dtype,raw in [('f32',np.array([np.nan],dtype='<f4').tobytes()),('f16',np.array([np.inf],dtype='<f2').tobytes())]:
        assert call(['feature-encode',dtype,'1'],raw).returncode==2
    assert call(['feature-encode','f32','32000001'],b'').returncode==2
    print('PASS: Rust 실제 FP32/FP16/INT8 바이트 왕복·길이·손상·비유한값·상한 거부')

if __name__=='__main__':
    main()

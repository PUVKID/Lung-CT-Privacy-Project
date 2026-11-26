"""실제 Rust 송수신의 바이트·양자화·잘못된 입력을 검사합니다."""
import sys, subprocess, struct
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from 전송 import ENGINE, encode, decode, blur, PROFILES

def main():
    pixels = np.tile(np.arange(256, dtype=np.uint8), (512, 2))
    for profile, (size, bits) in PROFILES.items():
        packet = encode(pixels, 0, profile)
        assert len(packet) == 9 + size*size*bits//8
        py = decode(packet, upsample=False)
        native = subprocess.run([str(ENGINE), 'decode'], input=packet, capture_output=True, check=True).stdout
        assert native == py.tobytes()
        if bits == 4:
            assert np.all(py % 17 == 0)
        if size == 512:
            assert np.array_equal(py, pixels)
        for broken in [packet[:-1], packet+b'X', b'bad', b'CTB1'+struct.pack('<HHB',0,size,bits)]:
            try:
                decode(broken)
            except ValueError:
                pass
            else:
                raise AssertionError('손상패킷을수락했습니다.')
            assert subprocess.run([str(ENGINE), 'decode'], input=broken, capture_output=True).returncode == 2
    for sigma in [-1, float('nan'), float('inf')]:
        try:
            blur(pixels, sigma)
        except ValueError:
            pass
        else:
            raise AssertionError('잘못된블러강도를수락했습니다.')
    odd = subprocess.run([str(ENGINE),'encode','3','1','4'],input=bytes([0,128,255]),capture_output=True,check=True).stdout
    assert decode(odd,False).tolist() == [[0,136,255]]
    constant = np.full((512,512),127,dtype=np.uint8)
    assert np.max(np.abs(blur(constant,16).astype(int)-127)) == 0
    assert not np.array_equal(blur(pixels,16),pixels)
    print('PASS:3전송조건,실제Rust복호화일치,바이트길이,4bit,홀수패딩,손상/비정상입력,블러항등/평탄영상')

if __name__ == '__main__':
    main()

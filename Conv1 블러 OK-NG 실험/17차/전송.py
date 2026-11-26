"""블러를 먼저 적용한 뒤 실제 Rust 패킷을 만들고 서버 입력을 복호화합니다."""
import struct
import subprocess
import math
from pathlib import Path
import numpy as np
from PIL import Image
from scipy.fft import dctn, idctn

PROFILES = {"블러만": (512, 8), "블러_축소128": (128, 8), "블러_축소64_4비트": (64, 4)}
ENGINE = Path(__file__).parent / "rust" / "전송엔진.exe"

def blur(pixels, sigma):
    if (not isinstance(pixels, np.ndarray) or pixels.dtype != np.uint8
            or pixels.shape != (512, 512) or not math.isfinite(float(sigma)) or sigma < 0):
        raise ValueError("원본은512×512 uint8, 블러는유한한0이상이어야합니다.")
    if sigma == 0:
        return pixels.copy()
    x = pixels.astype(np.float32) / np.float32(255)
    h, w = x.shape
    yy = np.arange(h, dtype=np.float32) * (np.float32(np.pi) / h)
    xx = np.arange(w, dtype=np.float32) * (np.float32(np.pi) / w)
    transfer = np.exp(np.float32(-.5 * sigma * sigma) * (yy[:, None]**2 + xx[None, :]**2))
    y = idctn(dctn(x, type=2, norm="ortho", workers=1) * transfer, type=2, norm="ortho", workers=1)
    return np.rint(np.clip(y, 0, 1) * 255).astype(np.uint8)

def encode(pixels, sigma, profile):
    if profile not in PROFILES:
        raise ValueError("알수없는전송조건입니다.")
    size, bits = PROFILES[profile]
    transformed = Image.fromarray(blur(pixels, sigma)).resize((size, size), Image.Resampling.BOX)
    proc = subprocess.run([str(ENGINE), "encode", str(size), str(size), str(bits)],
                          input=transformed.tobytes(), capture_output=True, check=True, timeout=20)
    return proc.stdout

def decode(packet, upsample=True):
    if len(packet) < 9 or packet[:4] != b"CTB1":
        raise ValueError("패킷 머리글 오류")
    w, h, bits = struct.unpack("<HHB", packet[4:9])
    if not (0 < w <= 512 and 0 < h <= 512 and bits in (4, 8)):
        raise ValueError("패킷 크기/비트수 오류")
    n = w*h
    if len(packet) != 9 + (n if bits == 8 else (n+1)//2):
        raise ValueError("패킷 길이 오류")
    values = np.frombuffer(packet[9:], dtype=np.uint8)
    if bits == 4:
        if n % 2 and values[-1] & 15:
            raise ValueError("패킷 패딩 오류")
        expanded = np.empty(len(values)*2, dtype=np.uint8)
        expanded[::2] = (values >> 4)*17
        expanded[1::2] = (values & 15)*17
        values = expanded[:n]
    image = Image.fromarray(values.reshape(h, w))
    if upsample:
        image = image.resize((512, 512), Image.Resampling.BILINEAR)
    return np.asarray(image, dtype=np.uint8).copy()

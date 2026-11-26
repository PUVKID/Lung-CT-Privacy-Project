"""17차 공식 CT 자료 확보와 환자 단위 2D 준비. GPU와 과거 실험을 호출하지 않는다."""
from __future__ import annotations

import argparse
import bisect
import collections
import contextlib
import csv
import hashlib
import io
import json
import math
import os
import pickle
import random
import re
import shutil
import stat
import sys
import time
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path, PurePosixPath

import numpy as np
from PIL import Image
from scipy.ndimage import map_coordinates

ROOT = Path(__file__).resolve().parent
PROTOCOL = "stage17-luna25-2d-patient-v2"
DATA = ROOT / "work" / "data"
MANIFEST = DATA / "SCI_manifest.json"
STATUS = DATA / "SCI_준비상태.json"
CATALOG = ROOT / "공식자료.json"
LABELS = {"0": 0, "1": 1}
COHORTS = {"LUNA25", "CSTL", "Histo"}
LUNA_COLUMNS = {"PatientID", "SeriesInstanceUID", "StudyDate", "CoordX", "CoordY", "CoordZ", "LesionID", "AnnotationID", "NoduleID", "label"}


class DataBlocked(ValueError):
    """필수 근거가 없거나 계보가 충돌하면 자료 준비를 중단한다."""


class GeometryRejected(DataBlocked):
    """성능 관측 전 고정한 물리 입력 적격성에서 제외할 행이다."""


ELIGIBILITY_POLICY = "fixed-50mm-geometry-qc-before-patient-split-v1"
ELIGIBILITY_SPEC = {"id": ELIGIBILITY_POLICY, "fov_mm": 50, "output_size": 512,
    "excluded_geometry": ["invalid-coordinate-matrix-or-center", "center-outside-source", "fixed-fov-outside-source"],
    "checksum_or_missing_file": "block-entire-preparation", "selection_uses_labels_or_predictions": False,
    "order": "geometry-qc-then-patient-split"}
ELIGIBILITY_SHA256 = hashlib.sha256(json.dumps(ELIGIBILITY_SPEC, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def digest(path: Path, algorithm="sha256") -> str:
    h = hashlib.new(algorithm)
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def atomic_json(path: Path, value) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + f".{os.getpid()}.tmp")
    try:
        with temp.open("w", encoding="utf-8", newline="\n") as f:
            json.dump(value, f, ensure_ascii=False, indent=2, allow_nan=False)
            f.write("\n")
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp, path)
    finally:
        temp.unlink(missing_ok=True)


def load_json(path: Path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def _inside(path: Path, root: Path) -> Path:
    path = path.resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError as exc:
        raise DataBlocked("허용한 자료 폴더 밖 경로") from exc
    return path


def _no_links(path: Path) -> None:
    for p in (path, *path.parents):
        if p.exists():
            s = p.lstat()
            if p.is_symlink() or getattr(s, "st_file_attributes", 0) & 0x400:
                raise DataBlocked("자료 경로의 심볼릭 링크/정션을 허용하지 않습니다")


def catalog_entries(group: str):
    cat = load_json(CATALOG)["records"]
    selected = {
        "annotations": [("14673658", None), ("8422229", {"all_anno_3D.csv", "anno_WorldCoord.csv"}),
                        ("12582356", {"5mm_3D_detection_mhd3.zip", "1.25mm_3D_detection_mhd_3.zip"})],
        "nodule-blocks": [("14223624", {"luna25_nodule_blocks.zip.001", "luna25_nodule_blocks.zip.002"})],
        "external-classification": [("12582356", {"class_dataset.zip"}), ("8422229", {"BMP_classification.zip"})],
        "full-ct": [("14223624", "full")],
    }
    if group not in selected:
        raise DataBlocked("알 수 없는 다운로드 그룹")
    rows = []
    for record, names in selected[group]:
        for f in cat[record]["files"]:
            if names is None or (names == "full" and f["name"].startswith("luna25_images.zip.")) or (isinstance(names, set) and f["name"] in names):
                rows.append({"record_id": record, **f})
    return sorted(rows, key=lambda r: (r["record_id"], r["name"]))


def verify_download(path: Path, entry: dict) -> dict:
    path = Path(path)
    _no_links(path)
    algo, expected = entry["checksum"].split(":", 1)
    if algo not in {"md5", "sha256"} or path.stat().st_size != entry["bytes"] or digest(path, algo) != expected:
        raise DataBlocked(f"공식 파일의 크기/체크섬 불일치: {path.name}")
    return {"name": path.name, "bytes": path.stat().st_size, "sha256": digest(path), "official_checksum": entry["checksum"], "record_id": entry["record_id"]}


@contextlib.contextmanager
def _download_guard(path: Path):
    """같은 부분 파일을 두 작업이 동시에 이어 쓰지 않도록 OS 잠금을 유지한다."""
    path.parent.mkdir(parents=True, exist_ok=True)
    _no_links(path)
    f = path.open("a+b")
    try:
        if path.stat().st_size == 0:
            f.write(b"0")
            f.flush()
        f.seek(0)
        try:
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            raise DataBlocked("같은 공식 파일의 다운로드가 이미 실행 중입니다") from exc
        try:
            yield
        finally:
            f.seek(0)
            if os.name == "nt":
                msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
    finally:
        f.close()


def download_entry(entry: dict, destination: Path, status_path=STATUS) -> dict:
    name = entry["name"]
    if Path(name).name != name or ":" in name or "\\" in name:
        raise DataBlocked("공식 목록 파일 이름이 안전하지 않습니다")
    with _download_guard(Path(destination) / (name + ".download.lock")):
        return _download_entry_unlocked(entry, destination, status_path)


def _download_entry_unlocked(entry: dict, destination: Path, status_path=STATUS) -> dict:
    name = entry["name"]
    if Path(name).name != name or ":" in name or "\\" in name:
        raise DataBlocked("공식 목록 파일 이름이 안전하지 않습니다")
    u = urllib.parse.urlparse(entry["url"])
    if u.scheme != "https" or u.hostname != "zenodo.org":
        raise DataBlocked("공식 Zenodo HTTPS만 다운로드합니다")
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    _no_links(destination)
    out = destination / name
    if out.exists():
        return verify_download(out, entry)
    part = out.with_name(out.name + ".part")
    _no_links(part)
    offset = part.stat().st_size if part.exists() else 0
    if offset > entry["bytes"]:
        raise DataBlocked("기존 부분 파일이 예상 크기보다 큽니다")
    need = entry["bytes"] - offset
    if shutil.disk_usage(destination).free < need + 2 * 1024 ** 3:
        raise DataBlocked("다운로드 용량과 2GiB 여유 공간 부족")
    headers = {"User-Agent": "Stage17-Research-Data/1.0"}
    if offset:
        headers["Range"] = f"bytes={offset}-"
    req = urllib.request.Request(entry["url"], headers=headers)
    written = offset
    last = 0.0
    if offset < entry["bytes"]:
        with urllib.request.urlopen(req, timeout=90) as r:
            if urllib.parse.urlparse(r.geturl()).scheme != "https":
                raise DataBlocked("HTTPS가 아닌 리디렉션")
            if offset and (r.status != 206 or not r.headers.get("Content-Range", "").startswith(f"bytes {offset}-")):
                raise DataBlocked("이어받기 범위를 서버가 확인하지 않았습니다. 부분 파일은 보존합니다")
            with part.open("ab" if offset else "xb") as f:
                for block in iter(lambda: r.read(1024 * 1024), b""):
                    written += len(block)
                    if written > entry["bytes"]:
                        raise DataBlocked("다운로드가 공식 예상 크기를 초과했습니다")
                    f.write(block)
                    if time.monotonic() - last > 5:
                        atomic_json(status_path, {"protocol": PROTOCOL, "status": "downloading", "file": name,
                            "bytes": written, "expected_bytes": entry["bytes"], "pid": os.getpid(), "updated_at": time.time()})
                        last = time.monotonic()
                f.flush()
                os.fsync(f.fileno())
    verify_download(part, entry)
    os.replace(part, out)
    return verify_download(out, entry)


class JoinedFiles(io.RawIOBase):
    """공식 분할 ZIP을 디스크에 다시 합치지 않고 읽는다."""
    def __init__(self, paths):
        self.files = [Path(p).open("rb") for p in paths]
        self.ends = []
        total = 0
        for f in self.files:
            total += os.fstat(f.fileno()).st_size
            self.ends.append(total)
        self.pos = 0
        self.total = total

    def seekable(self):
        return True

    def readable(self):
        return True

    def tell(self):
        return self.pos

    def seek(self, offset, whence=0):
        target = offset if whence == 0 else self.pos + offset if whence == 1 else self.total + offset
        if target < 0:
            raise ValueError("음수 읽기 위치")
        self.pos = target
        return target

    def read(self, size=-1):
        size = max(0, self.total - self.pos) if size < 0 else min(size, max(0, self.total - self.pos))
        blocks = []
        while size:
            idx = bisect.bisect_right(self.ends, self.pos)
            start = 0 if idx == 0 else self.ends[idx - 1]
            f = self.files[idx]
            f.seek(self.pos - start)
            b = f.read(min(size, self.ends[idx] - self.pos))
            if not b:
                raise DataBlocked("분할 ZIP 조기 종료")
            blocks.append(b)
            self.pos += len(b)
            size -= len(b)
        return b"".join(blocks)

    def close(self):
        for f in self.files:
            f.close()
        super().close()


def safe_extract(paths, destination: Path, *, max_bytes=100 * 1024 ** 3, max_files=100000) -> dict:
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    _no_links(destination)
    files = []
    with JoinedFiles(paths) as joined, zipfile.ZipFile(joined) as z:
        infos = z.infolist()
        if len(infos) > max_files or sum(i.file_size for i in infos) > max_bytes:
            raise DataBlocked("압축 해제의 파일 수/크기 한도 초과")
        if shutil.disk_usage(destination).free < sum(i.file_size for i in infos) + 2 * 1024 ** 3:
            raise DataBlocked("압축 해제 여유 공간 부족")
        seen = set()
        for i in infos:
            name = i.filename
            pp = PurePosixPath(name)
            if not name or pp.is_absolute() or any(p in {"..", "."} for p in pp.parts) or "\\" in name or ":" in name:
                raise DataBlocked("안전하지 않은 ZIP 경로")
            if stat.S_ISLNK(i.external_attr >> 16) or i.flag_bits & 1:
                raise DataBlocked("ZIP 연결/암호화 항목 거부")
            key = name.rstrip("/").casefold()
            if key in seen:
                raise DataBlocked("ZIP 중복/대소문자 경로 충돌")
            seen.add(key)
            target = _inside(destination / name, destination)
            _no_links(target)
            if i.is_dir():
                target.mkdir(parents=True, exist_ok=True)
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            temp = target.with_name(target.name + ".extracting")
            h = hashlib.sha256()
            try:
                with z.open(i) as src, temp.open("xb") as dst:
                    copied = 0
                    for block in iter(lambda: src.read(1024 * 1024), b""):
                        copied += len(block)
                        if copied > i.file_size:
                            raise DataBlocked("ZIP 선언 크기 초과")
                        h.update(block)
                        dst.write(block)
                    dst.flush()
                    os.fsync(dst.fileno())
                if copied != i.file_size:
                    raise DataBlocked("ZIP 크기 불일치")
                sha = h.hexdigest()
                if target.exists():
                    if digest(target) != sha:
                        raise DataBlocked("압축 해제 대상의 기존 다른 파일 보존")
                    temp.unlink()
                else:
                    os.replace(temp, target)
                files.append({"path": name, "bytes": copied, "sha256": sha})
            finally:
                temp.unlink(missing_ok=True)
    return {"files": files, "total_bytes": sum(f["bytes"] for f in files), "archives": [{"name": Path(p).name, "sha256": digest(Path(p))} for p in paths]}


class _MetadataUnpickler(pickle.Unpickler):
    """공식 NumPy 숫자 헤더만 허용한다. 임의 Python 함수 복원은 거부한다."""
    def find_class(self, module, name):
        allowed = {("numpy", "ndarray"): np.ndarray, ("numpy", "dtype"): np.dtype,
            ("numpy.core.multiarray", "_reconstruct"): np.core.multiarray._reconstruct,
            ("numpy._core.multiarray", "_reconstruct"): np.core.multiarray._reconstruct,
            ("numpy.core.multiarray", "scalar"): np.core.multiarray.scalar,
            ("numpy._core.multiarray", "scalar"): np.core.multiarray.scalar}
        if (module, name) not in allowed:
            raise DataBlocked(f"메타데이터의 허용하지 않은 pickle 전역: {module}.{name}")
        return allowed[module, name]


def load_block_metadata(path: Path) -> dict:
    if Path(path).stat().st_size > 65536:
        raise DataBlocked("메타데이터 파일 크기 초과")
    with Path(path).open("rb") as f:
        version = np.lib.format.read_magic(f)
        if version == (1, 0):
            shape, _, dtype = np.lib.format.read_array_header_1_0(f)
        elif version == (2, 0):
            shape, _, dtype = np.lib.format.read_array_header_2_0(f)
        else:
            raise DataBlocked("지원하지 않는 공식 NPY 메타데이터 버전")
        if not dtype.hasobject or shape != ():
            raise DataBlocked("공식 메타데이터의 0차원 dict 형식 불일치")
        value = _MetadataUnpickler(f).load()
        if not isinstance(value, np.ndarray) or value.shape != ():
            raise DataBlocked("메타데이터 형식 불일치")
        value = value.item()
    if not isinstance(value, dict) or set(value) != {"origin", "spacing", "transform"}:
        raise DataBlocked("공식 메타데이터 필수 키 불일치")
    m = {k: np.asarray(value[k], dtype=float) for k in value}
    if m["origin"].shape != (3,) or m["spacing"].shape != (3,) or m["transform"].shape != (3, 3):
        raise DataBlocked("메타데이터 좌표 차원 불일치")
    if not all(np.isfinite(a).all() for a in m.values()) or (m["spacing"] <= 0).any():
        raise DataBlocked("메타데이터 비유한 좌표/간격")
    return m


def extract_physical_patch(volume, *, origin_xyz, index_to_world_xyz, center_xyz, fov_mm=50.0, output_size=512):
    """원본 z,y,x 배열에서 환자 물리 x,y 평면의 단일 단면을 선형 보간한다."""
    if volume.ndim != 3 or not np.issubdtype(volume.dtype, np.number):
        raise DataBlocked("수치형 3D 원본 필요")
    a = np.asarray(index_to_world_xyz, dtype=float)
    center = np.asarray(center_xyz, dtype=float)
    origin = np.asarray(origin_xyz, dtype=float)
    if a.shape != (3, 3) or not np.isfinite(a).all() or abs(np.linalg.det(a)) < 1e-10 or center.shape != (3,) or not np.isfinite(center).all() or origin.shape != (3,) or not np.isfinite(origin).all():
        raise GeometryRejected("물리좌표 행렬/결절 중심 불량")
    if not (0 < fov_mm <= 256 and 1 <= output_size <= 1024):
        raise DataBlocked("잘못된 패치 시야/크기")
    inv = np.linalg.inv(a)
    center_idx = inv @ (center - origin)
    if np.any(center_idx < 0) or np.any(center_idx > np.asarray(volume.shape[::-1]) - 1):
        raise GeometryRejected("공식 결절 중심이 원본 범위 밖")
    axis = (np.arange(output_size) - (output_size - 1) / 2) * fov_mm / output_size
    xx, yy = np.meshgrid(axis, axis)
    world = np.stack((xx + center[0], yy + center[1], np.full_like(xx, center[2])), axis=0)
    indices = inv @ (world.reshape(3, -1) - origin[:, None])
    shape_xyz = np.asarray(volume.shape[::-1])[:, None]
    inside = np.logical_and(indices >= 0, indices <= shape_xyz - 1).all(axis=0)
    # 원본 block이 물리 시야보다 작으면 빈 패딩을 임의 학습 단서로 허용하지 않는다.
    if not inside.all():
        raise GeometryRejected(f"고정 {fov_mm:g}mm 시야가 제공 block 밖입니다. 패딩으로 포함하지 않습니다")
    patch = map_coordinates(volume, indices[::-1], order=1, output=np.float32, mode="constant", cval=-1000.0, prefilter=False).reshape(output_size, output_size)
    if not np.isfinite(patch).all():
        raise DataBlocked("원본 HU의 비유한 수치")
    return patch.astype(np.float32), {"fov_mm": float(fov_mm), "pixel_spacing_mm": fov_mm / output_size,
        "output_size": output_size, "center_world_xyz_mm": center.tolist(), "plane": "patient-axial-xy", "interpolation": "linear", "outside_fraction": 0.0,
        "sigma_units": "output-pixel", "sigma_mm_per_pixel": fov_mm / output_size,
        "task": "fixed-FOV nodule classification; full lesion containment not guaranteed"}


def block_geometry(metadata: dict):
    # 공식 preprocessing/utils.py는 z,y,x 축의 방향 성분을 행으로 쌓고 열별 간격으로 나눈다.
    # 해당 정의를 역으로 적용해 인덱스→물리좌표 행렬을 복원한다. 일반 direction 행렬로 오해하지 않는다.
    a_zyx = np.diag(metadata["spacing"]) @ metadata["transform"].T
    return metadata["origin"][::-1], a_zyx[::-1, ::-1]


def patient_split(rows: list[dict], seed=42) -> dict[str, list[dict]]:
    groups = collections.defaultdict(list)
    for row in rows:
        groups[row["patient_id"]].append(row)
    if len(groups) < 7:
        raise DataBlocked("환자 분할을 위해 최소 7명의 실제 환자가 필요합니다")
    strata = collections.defaultdict(list)
    for p, rs in groups.items():
        strata[max(r["label"] for r in rs)].append(p)
    rng = random.Random(seed)
    out = {s: [] for s in ("train", "validation", "test")}
    for label in sorted(strata):
        patients = sorted(strata[label])
        rng.shuffle(patients)
        n = len(patients)
        n_val, n_test = max(1, round(n * .15)), max(1, round(n * .15))
        if n - n_val - n_test < 1:
            raise DataBlocked("라벨별 환자 수가 70/15/15 분할에 부족합니다")
        assignments = (("validation", patients[:n_val]), ("test", patients[n_val:n_val+n_test]), ("train", patients[n_val+n_test:]))
        for split, ids in assignments:
            for p in ids:
                out[split].extend({**r, "split": split} for r in groups[p])
    for split, rs in out.items():
        out[split] = sorted(rs, key=lambda r: r["id"])
        if {r["label"] for r in rs} != {0, 1}:
            raise DataBlocked(f"{split}에 두 결절 라벨이 모두 없습니다")
    return out


def _valid_hash(value):
    return isinstance(value, str) and bool(re.fullmatch(r"[0-9a-f]{64}", value))


def validate_manifest(manifest: dict, *, verify_files=True) -> dict:
    if not isinstance(manifest, dict) or manifest.get("protocol") != PROTOCOL:
        raise DataBlocked("17차 LUNA25 SCI 프로토콜이 아닙니다. 12차 자료 재사용 금지")
    if manifest.get("status") != "ready" or set(manifest.get("splits", {})) != {"train", "validation", "test"}:
        raise DataBlocked("환자 분할/자료 준비 미완료")
    if set(manifest.get("external", {})) != {"CSTL", "Histo"}:
        raise DataBlocked("외부 코호트 계약 누락")
    if any(manifest["external"].values()) and manifest.get("cross_cohort_review", {}).get("reviewed") is not True:
        raise DataBlocked("기관/환자 중복 검토 근거 부재")
    patient_owner, image_owner, source_owner, ids, summary = {}, {}, {}, set(), {}
    required = {"id", "patient_id", "cohort", "label", "image_path", "image_sha256", "source_sha256", "split", "metadata"}
    collections_rows = [(k, v) for k, v in manifest["splits"].items()] + [(k, v) for k, v in manifest["external"].items()]
    for split, rows in collections_rows:
        if not isinstance(rows, list):
            raise DataBlocked(f"{split} 실제 자료가 없습니다")
        if not rows and split in {"CSTL", "Histo"}:
            state = manifest.get("external_status", {}).get(split, {})
            if state.get("status") != "blocked" or not state.get("reason"):
                raise DataBlocked("미준비 외부 코호트의 상태/사유 누락")
            summary[split] = {"nodules": 0, "patients": 0, "status": "blocked", "reason": state["reason"]}
            continue
        if not rows:
            raise DataBlocked(f"{split} 실제 자료가 없습니다")
        labels = collections.Counter()
        patients = set()
        for r in rows:
            if not required <= r.keys() or type(r["label"]) is not int or r["label"] not in {0, 1}:
                raise DataBlocked("manifest 필수 행/양성악성 라벨 불일치")
            cohort = "LUNA25" if split in manifest["splits"] else split
            if r["cohort"] != cohort or r["split"] != (split if cohort == "LUNA25" else "external"):
                raise DataBlocked("코호트/분할 태그 불일치")
            if not isinstance(r["patient_id"], str) or not r["patient_id"] or not isinstance(r["id"], str) or not r["id"] or r["id"] in ids:
                raise DataBlocked("환자 ID/결절 ID 누락 또는 중복")
            ids.add(r["id"])
            # 동일한 번호가 다른 기관에서 독립 부여될 수 있으므로 검토된 전역 ID를 필수로 한다.
            p = r["metadata"].get("global_patient_id")
            if not p or not r["metadata"].get("label_evidence"):
                raise DataBlocked("전역 환자 대응/공식 라벨 근거 부재")
            if p in patient_owner and patient_owner[p] != split:
                raise DataBlocked("분할/외부 코호트 사이 환자 중복")
            patient_owner[p] = split
            for key, registry in (("image_sha256", image_owner), ("source_sha256", source_owner)):
                sha = r[key]
                if not _valid_hash(sha):
                    raise DataBlocked("영상 SHA 형식 불일치")
                if sha in registry and registry[sha] != split:
                    raise DataBlocked("분할/외부 코호트 사이 동일 영상/원본 중복")
                registry[sha] = split
            pix = r["metadata"].get("pixel_sha256")
            if not _valid_hash(pix):
                raise DataBlocked("픽셀 SHA 부재")
            if pix in image_owner and image_owner[pix] != split:
                raise DataBlocked("다른 파일명의 동일 픽셀이 분할 사이 중복")
            image_owner[pix] = split
            image = Path(r["image_path"])
            if not image.is_absolute():
                raise DataBlocked("준비 영상은 절대 경로여야 합니다")
            if verify_files:
                _no_links(image)
                if not image.is_file() or digest(image) != r["image_sha256"]:
                    raise DataBlocked("준비 영상 무결성 불일치")
                with Image.open(image) as im:
                    if im.mode != "L" or im.size != (512, 512):
                        raise DataBlocked("512x512 8bit 단일 단면 계약 불일치")
                    if hashlib.sha256(np.asarray(im).tobytes()).hexdigest() != pix:
                        raise DataBlocked("준비 영상 픽셀 SHA 불일치")
            labels[r["label"]] += 1
            patients.add(p)
        if set(labels) != {0, 1}:
            raise DataBlocked(f"{split} 두 라벨이 없어서 이진 분류 전체 지표를 계산할 수 없습니다")
        summary[split] = {"nodules": len(rows), "patients": len(patients), "labels": dict(labels)}
    return summary


def read_luna_annotations(path: Path, *, require_official=True):
    path = Path(path)
    if require_official:
        entry = next(e for e in catalog_entries("annotations") if e["record_id"] == "14673658")
        verify_download(path, entry)
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if not LUNA_COLUMNS <= set(reader.fieldnames or []):
            raise DataBlocked("공식 LUNA25 CSV 열 불일치")
        rows = list(reader)
    seen = set()
    for r in rows:
        if r["label"] not in LABELS or not r["PatientID"].isdigit() or not re.fullmatch(r"[0-9_]+", r["AnnotationID"]):
            raise DataBlocked("LUNA25 라벨/환자/결절 형식 불일치")
        if r["AnnotationID"] != f'{r["PatientID"]}_{r["LesionID"]}_{r["StudyDate"]}' or r["AnnotationID"] in seen:
            raise DataBlocked("공식 환자/시점/결절 키 중복 또는 불일치")
        if not all(math.isfinite(float(r[k])) for k in ("CoordX", "CoordY", "CoordZ")):
            raise DataBlocked("공식 결절 좌표 비유한 수치")
        seen.add(r["AnnotationID"])
    return rows


def _save_png(array: np.ndarray, path: Path):
    pixels = np.rint(np.clip((array + 1000) / 1400, 0, 1) * 255).astype(np.uint8)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + f".{os.getpid()}.tmp")
    try:
        Image.fromarray(pixels).save(temp, format="PNG")
        if path.exists():
            if digest(temp) != digest(path):
                raise DataBlocked("기존 준비 이미지가 달라 덮어쓰지 않습니다")
        else:
            os.replace(temp, path)
    finally:
        temp.unlink(missing_ok=True)
    return hashlib.sha256(pixels.tobytes()).hexdigest()


def prepare_luna(blocks_root: Path, annotation: Path, output_root: Path, *, fov_mm=50):
    if fov_mm != 50:
        raise DataBlocked("이 프로토콜의 물리 시야는 성능 관측 전에 고정한 50mm입니다")
    ann = read_luna_annotations(annotation)
    blocks_root = Path(blocks_root).resolve()
    extraction_receipt = blocks_root / "압축해제_무결성.json"
    if not extraction_receipt.is_file():
        raise DataBlocked("공식 체크섬 확인 후 생성한 압축 해제 영수증 필요")
    receipt = load_json(extraction_receipt)
    allowed = {r["path"]: r["sha256"] for r in receipt["files"]}
    matching = {}
    for p in blocks_root.rglob("*.npy"):
        if p.parent.name == "image":
            if p.stem in matching:
                raise DataBlocked("결절 block 파일명이 여러 폴더에서 중복")
            matching[p.stem] = p
    out = []
    rejected = []
    csv_sha = digest(annotation)
    for r in ann:
        key = r["AnnotationID"]
        if key not in matching:
            raise DataBlocked(f"공식 주석에 대응하는 block 없음: {key}")
        image = matching[key]
        meta_file = image.parent.parent / "metadata" / image.name
        source_sha = digest(image)
        if source_sha != allowed.get(image.relative_to(blocks_root).as_posix()) or digest(meta_file) != allowed.get(meta_file.relative_to(blocks_root).as_posix()):
            raise DataBlocked("압축 해제 후 block/메타데이터 변경")
        meta = load_block_metadata(meta_file)
        volume = np.load(image, mmap_mode="r", allow_pickle=False)
        origin, a = block_geometry(meta)
        coords = [float(r[k]) for k in ("CoordX", "CoordY", "CoordZ")]
        try:
            patch, geometry = extract_physical_patch(volume, origin_xyz=origin, index_to_world_xyz=a, center_xyz=coords, fov_mm=fov_mm)
        except GeometryRejected as exc:
            rejected.append({"annotation_id": key, "patient_id": r["PatientID"], "label": r["label"], "reason": str(exc)})
            continue
        target = Path(output_root).resolve() / "LUNA25" / f"{key}.png"
        pixel_sha = _save_png(patch, target)
        out.append({"id": "LUNA25:" + key, "patient_id": r["PatientID"], "cohort": "LUNA25", "label": LABELS[r["label"]],
            "image_path": str(target), "image_sha256": digest(target), "source_sha256": source_sha, "split": "unassigned",
            "metadata": {"global_patient_id": "LUNA25:" + r["PatientID"], "pixel_sha256": pixel_sha,
                "source_image": str(image), "source_metadata_sha256": digest(meta_file), "annotation_csv_sha256": csv_sha,
                "series_uid": r["SeriesInstanceUID"], "nodule_id": r["NoduleID"], "annotation_id": key,
                "label_original": r["label"], "label_evidence": "Zenodo14673658 CSV label; official baseline train.py: malignant=label.sum()",
                "hu_window": [-1000, 400], "eligibility_policy": ELIGIBILITY_POLICY,
                "source_geometry": {k: v.tolist() for k, v in meta.items()}, **geometry}})
    report = {"policy": ELIGIBILITY_POLICY, "policy_spec": ELIGIBILITY_SPEC, "policy_sha256": ELIGIBILITY_SHA256,
        "fov_mm": fov_mm, "annotation_csv_sha256": csv_sha,
        "source_annotations": len(ann), "source_patients": len({r["PatientID"] for r in ann}),
        "source_labels": dict(collections.Counter(r["label"] for r in ann)),
        "accepted_annotations": len(out), "accepted_patients": len({r["patient_id"] for r in out}),
        "accepted_labels": dict(collections.Counter(str(r["label"]) for r in out)),
        "rejected_annotations": len(rejected), "rejected_patients": len({r["patient_id"] for r in rejected}),
        "rejected_labels": dict(collections.Counter(r["label"] for r in rejected)), "rejected": rejected,
        "selection_basis": "성능 관측 전 고정한 물리 입력 QC만 사용. 라벨·예측·시험점수는 제외 판단에 사용하지 않음",
        "limitation": "적격성에 따른 제외가 발생한 경우 공식 전체 코호트 성능과 같다고 주장하지 않음"}
    report_path = Path(output_root) / "LUNA25_입력적격성_비공개.json"
    atomic_json(report_path, report)
    report_sha = digest(report_path)
    for row in out:
        row["metadata"]["eligibility_report_sha256"] = report_sha
        row["metadata"]["eligibility_policy_sha256"] = ELIGIBILITY_SHA256
    if not out or {r["label"] for r in out} != {0, 1}:
        raise DataBlocked("고정 물리 입력 QC 후 두 클래스가 모두 남지 않았습니다")
    return out


def prepare_external(mapping_path: Path, output_root: Path):
    """공식 주석/환자 대응을 직접 검토한 JSON만 외부 시험으로 받는다."""
    m = load_json(mapping_path)
    if m.get("reviewed") is not True or m.get("cohort") not in {"CSTL", "Histo"} or not m.get("patient_identity_evidence") or not m.get("institution_overlap_review"):
        raise DataBlocked("외부 환자/기관/라벨 대응 검토 미완료")
    for key in ("annotation_file", "annotation_sha256", "label_definition_url"):
        if not m.get(key):
            raise DataBlocked("외부 공식 주석/라벨 정의 근거 부재")
    if digest(Path(m["annotation_file"])) != m["annotation_sha256"]:
        raise DataBlocked("외부 검토 대상 주석 변경")
    cohort = m["cohort"]
    out = []
    for r in m.get("rows", []):
        if type(r.get("label")) is not int or r["label"] not in {0, 1} or not all(r.get(k) for k in ("id", "patient_id", "global_patient_id", "label_evidence", "source_path", "source_sha256")):
            raise DataBlocked("외부 행의 공식 이진라벨/환자 대응 부재")
        source = Path(r["source_path"])
        _no_links(source)
        if digest(source) != r["source_sha256"]:
            raise DataBlocked("외부 원본 영상 변경")
        policy = r.get("policy")
        geom = {}
        source_identity = r["source_sha256"]
        if policy == "physical-volume":
            if source.suffix.lower() == ".mhd":
                fields = {}
                for line in source.read_text(encoding="ascii").splitlines():
                    if "=" in line:
                        k, v = line.split("=", 1)
                        fields[k.strip()] = v.strip()
                companion = fields.get("ElementDataFile", "")
                if not companion or Path(companion).name != companion or any(c in companion for c in (":", "\\", "/", " ")):
                    raise DataBlocked("MHD의 외부/복수 RAW 참조는 허용하지 않습니다")
                raw = source.parent / companion
                _no_links(raw)
                expected = r.get("source_companions_sha256", {}).get(companion)
                if not expected or digest(raw) != expected:
                    raise DataBlocked("MHD와 연결된 RAW 원본 SHA 근거 불일치")
                source_identity = hashlib.sha256(json.dumps({"header": source_identity, "raw": expected}, sort_keys=True).encode()).hexdigest()
            try:
                import SimpleITK as sitk
            except ImportError as exc:
                raise DataBlocked("외부 MHD/NIfTI 물리 처리에는 별도 SimpleITK 설치가 필요합니다") from exc
            im = sitk.ReadImage(str(source))
            volume = sitk.GetArrayFromImage(im)
            a = np.asarray(im.GetDirection()).reshape(3, 3) @ np.diag(im.GetSpacing())
            patch, geom = extract_physical_patch(volume, origin_xyz=im.GetOrigin(), index_to_world_xyz=a, center_xyz=r["center_xyz_mm"])
            pix = np.rint(np.clip((patch + 1000) / 1400, 0, 1) * 255).astype(np.uint8)
        elif policy == "legacy-2d-intensity":
            if not r.get("physical_geometry_unavailable") or not r.get("nodule_center_evidence"):
                raise DataBlocked("외부 2D의 좌표/시야 한계와 결절 중심 근거를 기록해야 합니다")
            with Image.open(source) as im:
                if im.mode not in {"L", "RGB"}:
                    raise DataBlocked("외부 2D 영상 모드 불일치")
                im = im.convert("L")
                if r.get("source_is_nodule_roi") is True:
                    roi = im
                elif "center_xy_px" in r:
                    center = np.asarray(r["center_xy_px"], dtype=float)
                    size = r.get("fixed_crop_size_px", 128)
                    if center.shape != (2,) or not np.isfinite(center).all() or type(size) is not int or not 16 <= size <= 512:
                        raise DataBlocked("외부 2D 고정 ROI 좌표/크기 오류")
                    left, top = np.rint(center - size / 2).astype(int)
                    if left < 0 or top < 0 or left + size > im.width or top + size > im.height:
                        raise DataBlocked("외부 2D 고정 ROI가 원본 범위 밖")
                    roi = im.crop((left, top, left + size, top + size))
                    geom["center_xy_px"] = center.tolist()
                    geom["fixed_crop_size_px"] = size
                else:
                    raise DataBlocked("외부 전체 흉부 BMP를 결절 ROI로 자동 간주하지 않습니다")
                pix = np.asarray(roi.resize((512, 512), Image.Resampling.BILINEAR))
            geom.update({"fov_mm": None, "hu_window": None, "geometry_unavailable": True, "domain_shift": "공식 BMP의 물리 간격/HU가 없어 50mm LUNA25와 동일 입력이라고 볼 수 없음"})
        else:
            raise DataBlocked("외부 처리 정책 미지정")
        sid = hashlib.sha256(str(r["id"]).encode()).hexdigest()[:24]
        target = Path(output_root).resolve() / cohort / (sid + ".png")
        target.parent.mkdir(parents=True, exist_ok=True)
        stream = io.BytesIO()
        Image.fromarray(pix).save(stream, format="PNG")
        data = stream.getvalue()
        if target.exists() and target.read_bytes() != data:
            raise DataBlocked("외부 준비 영상 충돌")
        if not target.exists():
            temp = target.with_suffix(".tmp")
            temp.write_bytes(data)
            os.replace(temp, target)
        out.append({"id": f'{cohort}:{r["id"]}', "patient_id": str(r["patient_id"]), "cohort": cohort, "label": r["label"],
            "image_path": str(target), "image_sha256": digest(target), "source_sha256": source_identity, "split": "external",
            "metadata": {"global_patient_id": r["global_patient_id"], "pixel_sha256": hashlib.sha256(pix.tobytes()).hexdigest(),
                "label_evidence": r["label_evidence"], "mapping_sha256": digest(mapping_path), "primary_source_sha256": r["source_sha256"], "policy": policy, **geom}})
    if not out:
        raise DataBlocked("외부 검토된 행 없음")
    return out


def build_manifest(luna_rows, cstl_rows=None, histo_rows=None, review=None, *, seed=42):
    cstl_rows, histo_rows = cstl_rows or [], histo_rows or []
    review = review or {"reviewed": False, "evidence": "외부 환자·기관·물리 입력 대응 준비 중. LUNA25 주학습과 구분"}
    if (cstl_rows or histo_rows) and (review.get("reviewed") is not True or not review.get("evidence")):
        raise DataBlocked("CSTL/Histo 기관·환자 중복 검토 미완료")
    result = {"protocol": PROTOCOL, "status": "ready", "label_names": {"0": "OK 양성 결절", "1": "NG 악성 결절"},
        "split_policy": {"unit": "patient", "seed": seed, "ratios": [.7, .15, .15], "stratification": "patient-any-malignant"},
        "preprocessing": {"fov_mm": 50, "output_size": 512, "hu_window": [-1000, 400], "eligibility_policy": ELIGIBILITY_POLICY},
        "splits": patient_split(luna_rows, seed), "external": {"CSTL": cstl_rows, "Histo": histo_rows},
        "external_status": {c: {"status": "ready" if rs else "blocked", "reason": None if rs else "공식 분류 라벨은 확인했으나 환자·결절 중심·물리 입력 대응 검토 미완료"}
            for c, rs in (("CSTL", cstl_rows), ("Histo", histo_rows))},
        "cross_cohort_review": review, "created_at": time.time()}
    result["summary"] = validate_manifest(result)
    return result


def inspect_external_archives(downloads: Path, destination: Path):
    """공식 분류 폴더를 실제 읽어 라벨을 연결하되 미확인 환자·ROI는 완료로 꾸미지 않는다."""
    summaries = {}
    for entry in catalog_entries("external-classification"):
        verify_download(Path(downloads) / entry["name"], entry)
        cohort = "CSTL" if entry["record_id"] == "12582356" else "Histo"
        dest = Path(destination) / cohort
        receipt_path = dest / "압축해제_무결성.json"
        if receipt_path.exists():
            receipt = load_json(receipt_path)
            if receipt["archives"] != [{"name": entry["name"], "sha256": digest(Path(downloads) / entry["name"])}]:
                raise DataBlocked("외부 추출 영수증의 공식 원본 변경")
            for r in receipt["files"]:
                if digest(dest / r["path"]) != r["sha256"]:
                    raise DataBlocked("외부 원본 추출 후 변경")
        else:
            receipt = safe_extract([Path(downloads) / entry["name"]], dest)
            atomic_json(receipt_path, receipt)
        mapping = {"1": 1, "2": 1, "3": 1, "4": 1, "5": 0, "6": 0} if cohort == "CSTL" else {"0": 0, "1": 1, "2": 1}
        reference = "https://www.nature.com/articles/s41597-024-03851-7" if cohort == "CSTL" else "https://www.nature.com/articles/s41597-024-03658-6"
        if cohort == "CSTL":
            readme = dest / "class_dataset" / "READ_ME.txt"
            text = readme.read_text(encoding="utf-8-sig")
            for term in ("invasive adenocarcinoma", "minimally invasive adenocarcinoma", "adenocarcinoma in situ", "malignant other subtypes", "inflammation", "benign other subtypes"):
                if term not in text:
                    raise DataBlocked("CSTL 공식 README의 병리 하위형 변경")
        pixel_annotations = collections.defaultdict(list)
        histo_ann = Path(downloads) / "all_anno_3D.csv"
        if cohort == "Histo" and histo_ann.exists():
            annotation_entry = next(e for e in catalog_entries("annotations") if e["name"] == "all_anno_3D.csv")
            verify_download(histo_ann, annotation_entry)
            with histo_ann.open(encoding="utf-8-sig", newline="") as f:
                for r in csv.DictReader(f):
                    pixel_annotations[r["image"]].append(r)
        rows = []
        for image in sorted(dest.rglob("*.bmp")):
            raw_label = image.parent.name
            if raw_label not in mapping:
                raise DataBlocked("공식 외부 분류 폴더에 미정의 라벨")
            tokens = image.stem.split("_")
            if not tokens or not all(t.isdigit() for t in tokens):
                raise DataBlocked("외부 파일의 사례/시점 이름 형식 변경")
            rows.append({"source_path": str(image.resolve()), "source_sha256": digest(image), "original_label": raw_label,
                "label": mapping[raw_label], "label_evidence": reference, "source_case_id_candidate": tokens[0],
                "patient_id_verified": False, "roi_verified": False,
                "annotation_candidates": pixel_annotations.get(image.name, []),
                "blocked_reason": "공식 라벨 연결 완료. 파일명 사례→환자 대응·결절 ROI·HU/물리 간격 검토 미완료"})
        payload = {"cohort": cohort, "reviewed": False, "status": "blocked", "label_mapping_reviewed": True,
            "source_archive": entry, "label_definition_url": reference, "rows": rows,
            "institution_evidence": "Second Hospital of Shandong University" if cohort == "CSTL" else "Linyi Central Hospital",
            "institution_evidence_level": "공식 논문 기술. 개별 환자의 병원간 이동/중복은 미확인",
            "patient_identity_evidence": None, "physical_geometry_verified": False}
        atomic_json(dest / "공식라벨_자동대응_환자ROI검토대기_비공개.json", payload)
        summaries[cohort] = {"images": len(rows), "raw_labels": dict(collections.Counter(r["original_label"] for r in rows)),
            "binary_labels": dict(collections.Counter(r["label"] for r in rows)),
            "candidate_case_ids": len({r["source_case_id_candidate"] for r in rows}),
            "exact_pixel_annotation_image_matches": sum(bool(r["annotation_candidates"]) for r in rows),
            "status": "blocked", "label_mapping_reviewed": True, "patient_roi_verified": False}
    atomic_json(Path(destination) / "외부자료_실제대응_요약.json", summaries)
    return summaries


def prepare_status(path=STATUS):
    state = {"protocol": PROTOCOL, "status": "blocked", "reasons": [], "updated_at": time.time(), "manifest": str(MANIFEST)}
    if MANIFEST.exists():
        try:
            state["summary"] = validate_manifest(load_json(MANIFEST))
            state["status"] = "ready"
        except (ValueError, OSError) as exc:
            state["reasons"].append(str(exc))
    else:
        state["reasons"].append("LUNA25 공식 결절 block의 전체 체크섬·물리 시야·환자 분할 준비 필요. 외부 코호트는 별도 준비대기이며 내부 주학습의 필수 완료 조건과 구분합니다")
    state["external_status"] = {c: {"status": "blocked", "reason": "공식 분류 라벨 연결은 확인했으나 환자·결절 중심·물리 입력 검토 미완료"} for c in ("CSTL", "Histo")}
    if MANIFEST.exists() and state["status"] == "ready":
        state["external_status"] = load_json(MANIFEST).get("external_status", state["external_status"])
    state["available_downloads"] = {g: {"files": len(catalog_entries(g)), "bytes": sum(e["bytes"] for e in catalog_entries(g))} for g in ("annotations", "nodule-blocks", "external-classification", "full-ct")}
    atomic_json(path, state)
    return state


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("status")
    inspect = sub.add_parser("inspect-external")
    inspect.add_argument("--downloads", type=Path, default=DATA / "official")
    inspect.add_argument("--destination", type=Path, default=DATA / "external_original")
    ls = sub.add_parser("list")
    ls.add_argument("--group", choices=("annotations", "nodule-blocks", "external-classification", "full-ct"), default="annotations")
    dl = sub.add_parser("download")
    dl.add_argument("--group", choices=("annotations", "nodule-blocks", "external-classification", "full-ct"), required=True)
    dl.add_argument("--destination", type=Path, default=DATA / "official")
    ex = sub.add_parser("extract")
    ex.add_argument("--group", choices=("nodule-blocks", "external-classification"), required=True)
    ex.add_argument("--downloads", type=Path, default=DATA / "official")
    ex.add_argument("--destination", type=Path, required=True)
    prep = sub.add_parser("prepare")
    prep.add_argument("--blocks", type=Path, required=True)
    prep.add_argument("--annotation", type=Path, default=DATA / "official" / "LUNA25_Public_Training_Development_Data.csv")
    prep.add_argument("--cstl-mapping", type=Path)
    prep.add_argument("--histo-mapping", type=Path)
    prep.add_argument("--cross-review", type=Path)
    prep.add_argument("--output-root", type=Path, default=DATA / "prepared")
    prep.add_argument("--manifest", type=Path, default=MANIFEST)
    args = parser.parse_args(argv)
    try:
        if args.command == "status":
            print(json.dumps(prepare_status(), ensure_ascii=False))
        elif args.command == "list":
            es = catalog_entries(args.group)
            print(json.dumps({"group": args.group, "bytes": sum(e["bytes"] for e in es), "files": es}, ensure_ascii=False, indent=2))
        elif args.command == "download":
            receipts = [download_entry(e, args.destination) for e in catalog_entries(args.group)]
            atomic_json(args.destination / (args.group + "_다운로드_무결성.json"), {"group": args.group, "files": receipts})
            atomic_json(STATUS, {"protocol": PROTOCOL, "status": "blocked", "download_completed": args.group, "reasons": ["다운로드 체크섬 확인은 전처리/환자·라벨 대응 완료가 아닙니다"], "updated_at": time.time()})
            print(json.dumps({"downloaded": len(receipts), "group": args.group}, ensure_ascii=False))
        elif args.command == "extract":
            entries = catalog_entries(args.group)
            for e in entries:
                verify_download(args.downloads / e["name"], e)
            if args.group == "nodule-blocks":
                receipt = safe_extract([args.downloads / e["name"] for e in entries], args.destination)
                atomic_json(args.destination / "압축해제_무결성.json", receipt)
            else:
                for e in entries:
                    dst = args.destination / e["record_id"]
                    atomic_json(dst / "압축해제_무결성.json", safe_extract([args.downloads / e["name"]], dst))
            print("공식 체크섬·ZIP CRC와 파일 SHA 확인 후 압축 해제했습니다")
        elif args.command == "inspect-external":
            print(json.dumps(inspect_external_archives(args.downloads, args.destination), ensure_ascii=False))
        elif args.command == "prepare":
            cstl = prepare_external(args.cstl_mapping, args.output_root) if args.cstl_mapping else []
            histo = prepare_external(args.histo_mapping, args.output_root) if args.histo_mapping else []
            luna = prepare_luna(args.blocks, args.annotation, args.output_root)
            manifest = build_manifest(luna, cstl, histo, load_json(args.cross_review) if args.cross_review else None)
            atomic_json(args.manifest, manifest)
            atomic_json(STATUS, {"protocol": PROTOCOL, "status": "ready", "manifest": str(args.manifest.resolve()), "manifest_sha256": digest(args.manifest), "summary": manifest["summary"]})
            print(json.dumps(manifest["summary"], ensure_ascii=False))
        return 0
    except Exception as exc:
        atomic_json(STATUS, {"protocol": PROTOCOL, "status": "blocked", "reasons": [str(exc)], "error_type": type(exc).__name__, "command": args.command, "updated_at": time.time()})
        print(f"자료 준비 중단: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

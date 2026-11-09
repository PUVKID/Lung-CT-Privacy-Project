"""원본을 바꾸지 않고 중복 단위 분할과 학습 전용 증강을 수행합니다."""

from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance
import torch
from torch.utils.data import Dataset


IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"}


def binary_label(value):
    key = str(value).lower().strip().replace(" ", "").replace("_", "").replace("-", "")
    if key in {"0", "ok", "bengin", "bengincases", "benign", "benigncases", "normal", "normalcases"}:
        return 0
    if key in {"1", "ng", "malignant", "malignantcases"}:
        return 1
    raise ValueError(f"확인되지 않은 원본 라벨: {value!r}")


def discover_images(dataset_root):
    root = Path(dataset_root).resolve()
    if not root.is_dir():
        raise FileNotFoundError(f"원본 자료 폴더가 없습니다: {root}")
    rows = []
    for folder in sorted(root.iterdir()):
        if not folder.is_dir():
            continue
        try:
            label = binary_label(folder.name)
        except ValueError:
            continue
        for path in sorted(folder.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in IMAGE_SUFFIXES:
                continue
            raw = path.read_bytes()
            with Image.open(path) as image:
                image.load()
                gray = image.convert("L")
                width, height = gray.size
                # 실제 학습에 읽히는 회색조 픽셀과 크기를 함께 해시합니다.
                pixel_digest = hashlib.sha256(f"L:{width}:{height}:".encode() + gray.tobytes()).hexdigest()
            rows.append({"path": str(path.resolve()), "relative_path": path.relative_to(root).as_posix(),
                         "source_class": folder.name, "label": label,
                         "byte_sha256": hashlib.sha256(raw).hexdigest(), "pixel_sha256": pixel_digest,
                         "width": width, "height": height})
    if not rows:
        raise ValueError("분류 가능한 원본 영상이 0개입니다.")
    parents = list(range(len(rows)))

    def find(index):
        while parents[index] != index:
            parents[index] = parents[parents[index]]
            index = parents[index]
        return index

    known = {}
    for index, row in enumerate(rows):
        for kind in ["byte_sha256", "pixel_sha256"]:
            key = (kind, row[kind])
            if key in known:
                parents[find(index)] = find(known[key])
            else:
                known[key] = index
    members = defaultdict(list)
    for index in range(len(rows)):
        members[find(index)].append(index)
    for indices in members.values():
        if len({rows[i]["label"] for i in indices}) > 1:
            raise ValueError("동일 바이트/픽셀 영상에 OK와 NG 라벨 충돌이 있습니다. 원본 확인이 필요합니다.")
        group = min(rows[i]["pixel_sha256"] for i in indices)
        for index in indices:
            rows[index]["duplicate_group"] = group
    return rows


def split_records(records, seed=42, validation_ratio=0.15, test_ratio=0.15):
    if not (0 < validation_ratio < 1 and 0 < test_ratio < 1 and validation_ratio + test_ratio < 1):
        raise ValueError("학습·검증·시험 비율이 유효하지 않습니다.")
    by_class = defaultdict(dict)
    for row in records:
        by_class[row["label"]].setdefault(row["duplicate_group"], []).append(row)
    if set(by_class) != {0, 1}:
        raise ValueError("OK와 NG 두 클래스가 모두 필요합니다.")
    result = {"train": [], "validation": [], "test": []}
    rng = np.random.default_rng(seed)
    for label in [0, 1]:
        groups = sorted(by_class[label])
        if len(groups) < 7:
            raise ValueError("각 클래스에 서로 다른 영상 중복 그룹이 7개 이상 필요합니다.")
        groups = [groups[i] for i in rng.permutation(len(groups))]
        n_test = max(1, round(len(groups) * test_ratio))
        n_val = max(1, round(len(groups) * validation_ratio))
        n_train = len(groups) - n_test - n_val
        if n_train < 1:
            raise ValueError("원본 학습 그룹이 남지 않는 분할입니다.")
        for name, selected in [("test", groups[:n_test]), ("validation", groups[n_test:n_test + n_val]),
                               ("train", groups[n_test + n_val:])]:
            for group in selected:
                result[name].extend(by_class[label][group])
    for name in result:
        result[name].sort(key=lambda row: row["relative_path"])
    assert_disjoint(result)
    return result


def assert_disjoint(splits):
    for key in ["path", "byte_sha256", "pixel_sha256", "duplicate_group"]:
        owners = {}
        for name, rows in splits.items():
            for row in rows:
                previous = owners.setdefault(row[key], name)
                if previous != name:
                    raise ValueError(f"분할 사이 {key} 누수가 있습니다.")


def balanced_epoch_plan(records, samples_per_class, seed, epoch):
    if isinstance(samples_per_class, bool) or int(samples_per_class) != samples_per_class or samples_per_class < 1:
        raise ValueError("클래스별 표본 수는 양의 정수여야 합니다.")
    rng = np.random.default_rng(np.random.SeedSequence([int(seed), int(epoch)]))
    plan = []
    for label in [0, 1]:
        indices = [i for i, row in enumerate(records) if row["label"] == label]
        if not indices:
            raise ValueError("학습에 OK와 NG가 모두 필요합니다.")
        selected = []
        while len(selected) < samples_per_class:
            selected.extend(rng.permutation(indices).tolist())
        for index in selected[:samples_per_class]:
            plan.append((int(index), int(rng.integers(0, 2 ** 63 - 1))))
    return [plan[i] for i in rng.permutation(len(plan))]


class CTDataset(Dataset):
    def __init__(self, records, image_size=512, training=False, samples_per_class=5000, seed=42):
        self.records = list(records)
        self.image_size = image_size
        self.training = training
        self.samples_per_class = samples_per_class
        self.seed = seed
        self.cache = {}
        self.set_epoch(0)

    def set_epoch(self, epoch):
        self.plan = balanced_epoch_plan(self.records, self.samples_per_class, self.seed, epoch) if self.training else [(i, 0) for i in range(len(self.records))]

    def __len__(self):
        return len(self.plan)

    def __getitem__(self, item):
        index, sample_seed = self.plan[item]
        row = self.records[index]
        path = row["path"]
        if path not in self.cache:
            with Image.open(path) as image:
                gray = image.convert("L")
                if gray.size != (self.image_size, self.image_size):
                    gray = gray.resize((self.image_size, self.image_size), Image.Resampling.BILINEAR)
                self.cache[path] = np.asarray(gray, dtype=np.uint8).copy()
        pixels = self.cache[path]
        if self.training:
            rng = np.random.default_rng(sample_seed)
            image = Image.fromarray(pixels)
            if rng.random() < 0.5:
                image = image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            image = ImageEnhance.Contrast(image).enhance(float(rng.uniform(0.94, 1.06)))
            pixels = np.clip(np.asarray(image, dtype=np.float32) + rng.uniform(-6, 6), 0, 255)
        tensor = torch.from_numpy(np.asarray(pixels, dtype=np.float32).copy()).unsqueeze(0).repeat(3, 1, 1) / 255.0
        return tensor, torch.tensor(float(row["label"]), dtype=torch.float32)


def dataset_summary(records, splits, samples_per_class):
    def count(rows):
        labels = Counter(row["label"] for row in rows)
        return {"OK": labels[0], "NG": labels[1], "total": len(rows)}
    return {"source_counts": dict(Counter(row["source_class"] for row in records)),
            "class_counts": count(records), "splits": {name: count(rows) for name, rows in splits.items()},
            "original_total": len(records), "unique_duplicate_groups": len({r["duplicate_group"] for r in records}),
            "duplicate_extra_files": len(records) - len({r["duplicate_group"] for r in records}),
            "epoch_target_per_class": samples_per_class, "split_unit": "image_duplicate_group",
            "patient_id_available": False, "leakage_checked": True,
            "limitations": ["실제 환자 ID가 없어 이미지 단위 예비실험입니다. 환자 간 독립성을 검증하지 못했습니다.",
                            "바이트·회색조 픽셀의 완전 중복만 차단하며 유사 영상·같은 환자의 다른 절편은 식별할 수 없습니다.",
                            "온라인 증강 5000개/클래스는 원본 환자나 독립 영상 5000개를 의미하지 않습니다."]}


def prepare_dataset(config, root):
    records = discover_images(config["dataset_root"])
    actual = dict(Counter(row["source_class"] for row in records))
    expected = config.get("expected_source_counts")
    if expected and actual != expected:
        raise ValueError(f"원본 클래스별 수가 확인된 명세와 다릅니다: 실제={actual}, 예상={expected}")
    splits = split_records(records, config["seed"], config["validation_ratio"], config["test_ratio"])
    summary = dataset_summary(records, splits, config["samples_per_class"])
    destination = Path(root) / "work/results"
    destination.mkdir(parents=True, exist_ok=True)
    payload = {"records": records, "splits": splits, "summary": summary,
               "manifest_sha256": hashlib.sha256(json.dumps(records, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()}
    path = destination / "dataset_manifest_private.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    return payload

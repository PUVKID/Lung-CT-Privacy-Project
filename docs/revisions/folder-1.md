<div align="center">

# 📓 자료 1차 · ResNet50 비교 노트북의 설정 정리

**블록·블러의 rebuilt·same_settings·metric_matched 변형과 노트북 수정 보조 스크립트를 함께 읽는 코드 자료 차수입니다.**

**기술 분류:** 실험 코드 › ResNet50 단독 변환 › 설정 정렬·유사도 매칭

[목적](#purpose) · [기능](#features) · [입출력](#flow) · [구성](#files) · [준비](#setup) · [사용법](#usage) · [결과](#results) · [제약](#limits) · [변경](#changes)

</div>

<a name="purpose"></a>

## 🎯 이 단계에서 하는 일

같은 설정을 맞추는 비교와 영상 유사도 지표를 맞추는 비교는 목적이 다릅니다. 파일별 batch·블러 강도 결정·경로·콜백의 차이를 먼저 확인해 실행할 노트북을 선택합니다.

<a name="features"></a>

## 🧩 주요 기능과 처리 방식

| 구성 | 실제 역할 |
| --- | --- |
| 여섯 노트북 | 블록·블러 각각 rebuilt·same_settings·metric_matched로 나누어 보관합니다. |
| 강도 매칭 | metric_matched 블러는 블록 변환의 평균 SSIM/PSNR에 맞는 sigma를 보정하는 함수를 포함합니다. |
| 학습 설정 | 변형별 batch4/8과 단계별 epoch·SWA 시작값이 다르므로 설정 셀을 확인합니다. |
| 수정 도구 | 노트북 생성·콜백·반복 학습·과적합 제어를 수정하는 보조 스크립트가 있습니다. |

<a name="flow"></a>

## 🔄 입력 → 처리 → 출력

| 입력 | 처리 | 출력·읽을 결과 |
| --- | --- | --- |
| 블록·블러 노트북 | 설정과 변환 강도 비교 | 실행할 변형 선택 |
| 보정용 영상 | SSIM/PSNR 기반 sigma 탐색 | 블록과 비교할 블러 강도 |
| 노트북 원본 | 지정 셀·문자열 수정 | 다른 설정의 노트북 |

<a name="files"></a>

## 📁 파일과 핵심 처리

| 파일 | 이용 방법 |
| --- | --- |
| [1차/block_encryption_resnet50_metric_matched_seq.ipynb](../../1%EC%B0%A8/block_encryption_resnet50_metric_matched_seq.ipynb) | 설정·함수·실행 셀 |
| [1차/blur_resnet50_metric_matched_seq.ipynb](../../1%EC%B0%A8/blur_resnet50_metric_matched_seq.ipynb) | 설정·함수·실행 셀 |
| [자료차수/1차/create_metric_matched_notebooks.js](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/1%EC%B0%A8/create_metric_matched_notebooks.js) | 해당 단계의 자료 |
| [자료차수/1차/fix_training_repeat_overfit.py](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/1%EC%B0%A8/fix_training_repeat_overfit.py) | 처리 함수와 실행 조건 |

### 🔎 함수·셀로 찾아가기

아래 이름은 해당 파일의 실제 정의입니다. 위 처리 설명과 함께 설정·호출 순서·출력 경로를 따라 읽습니다.

| 파일 | 핵심 정의 |
| --- | --- |
| [1차/block_encryption_resnet50_metric_matched_seq.ipynb](../../1%EC%B0%A8/block_encryption_resnet50_metric_matched_seq.ipynb) | 셀 6: `gpu_status` · `GPUMonitorCallback` · `__init__` · `on_epoch_end`<br>셀 8: `set_reproducible` · `list_class_dirs` · `list_image_files`<br>셀 10: `block_scramble` · `generate_block_dataset`<br>셀 12: `oversample_dir`<br>셀 14: `prepare_split`<br>셀 16: `_deterministic` · `get_paths_labels` · `load_image` · `augment_train` · `mixup_batch` · `cutmix_batch` · `apply_mixup` · `apply_cutmix`<br>셀 18: `focal_loss` · `loss_fn` · `CosineAnnealingWarmRestart` · `__init__` · `on_epoch_begin` · `SWACallback` · `__init__` · `on_epoch_end` |
| [1차/blur_resnet50_metric_matched_seq.ipynb](../../1%EC%B0%A8/blur_resnet50_metric_matched_seq.ipynb) | 셀 6: `gpu_status` · `GPUMonitorCallback` · `__init__` · `on_epoch_end`<br>셀 8: `set_reproducible` · `list_class_dirs` · `list_image_files`<br>셀 10: `apply_gaussian_blur` · `block_scramble_for_calibration` · `generate_blur_dataset` · `calibration_image_paths` · `load_metric_image` · `average_similarity_metrics` · `choose_sigma_for_target` · `distance`<br>셀 12: `oversample_dir`<br>셀 14: `prepare_split`<br>셀 16: `_deterministic` · `get_paths_labels` · `load_image` · `augment_train` · `mixup_batch` · `cutmix_batch` · `apply_mixup` · `apply_cutmix`<br>셀 18: `focal_loss` · `loss_fn` · `CosineAnnealingWarmRestart` · `__init__` · `on_epoch_begin` · `SWACallback` · `__init__` · `on_epoch_end` |
| [자료차수/1차/create_metric_matched_notebooks.js](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/1%EC%B0%A8/create_metric_matched_notebooks.js) | 소스: `asText` · `asSourceArray` · `setCell` · `set_reproducible` · `list_class_dirs` · `list_image_files` · `set_reproducible` · `list_class_dirs` |
| [자료차수/1차/fix_training_repeat_overfit.py](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/1%EC%B0%A8/fix_training_repeat_overfit.py) | 소스: `cell_text` · `set_cell_text` · `replace_once` · `patch_notebook` · `OverfitControlCallback` · `__init__` · `on_epoch_end` |

<a name="setup"></a>

## ⚙️ 환경과 설정

| 항목 | 조건·기본값 |
| --- | --- |
| 입력 크기 | 512 |
| 변환 | 블록 512~1·블러 조건별 sigma |
| 비교 목적 | same_settings와 metric_matched 구분 |
| 수정 도구 | Python 및 Node.js·실제 notebook 경로 |

<a name="usage"></a>

## 🚀 준비와 사용 순서

1. 여섯 노트북의 설정 셀에서 비교 목적·batch·변환 강도를 확인합니다.
2. metric_matched의 보정 영상 선택과 목표 SSIM/PSNR을 읽습니다.
3. 실험 입력·저장 경로와 분할·증강 순서를 확인합니다.
4. 수정 스크립트는 대상 파일을 다시 쓰므로 별도 사본에서 입력·치환 대상을 확인한 뒤 사용합니다.

<a name="results"></a>

## 📊 결과를 읽는 방법

노트북 변형은 실험 조건을 정리한 코드입니다. 설정이 달라졌다고 새 성능 결과가 이미 확보된 것으로 보지 않습니다.

영상 유사도를 맞추는 보정은 분류 성능이나 프라이버시가 동등하다는 보장이 아닙니다. 보정에 사용하는 자료와 시험 자료의 관계도 확인해야 합니다.

<a name="limits"></a>

## 🛠️ 알려진 제약과 확인 지점

| 상황 | 확인할 내용 |
| --- | --- |
| 이름과 역할 | rebuilt·same_settings·metric_matched가 같은 실행이라는 뜻은 아닙니다. |
| 파일 쓰기 | 보조 도구는 지정 노트북을 덮어쓸 수 있으므로 사본과 경로를 준비합니다. |
| 평가 기준 | 유사도 매칭과 독립 분류 시험을 구분합니다. |

<a name="changes"></a>

## 🔀 이전 단계와의 변화

블록·블러 실험 노트북의 조건과 보조 도구를 정리한 자료 1차입니다. 논문의 연구 1 번호와 다른 코드 자료 구분입니다.

[🔎 직전 단계 전체 비교·구성](../revision-diffs/folder-1.diff) · [📋 전체 파일 크기·해시](../revision-manifests/folder-1.json)

<details>
<summary>📎 이 단계의 파일 기록과 전체 해시</summary>

아래 표는 해당 단계가 기록될 당시의 파일 정보입니다. 현재 첨부는 [프로젝트 자료 안내](../PAPERS.md)에서 확인할 수 있습니다.

| 파일 | 종류 | 바이트 | SHA-256 |
|---|---|---:|---|
| [자료차수/1차/block_encryption_resnet50_metric_matched_seq.ipynb](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/1%EC%B0%A8/block_encryption_resnet50_metric_matched_seq.ipynb) | .ipynb | 60093 | `066b6f71ee4c438ea16e481f2182166ef777cf77b0759439945aeb7cdc12d5c1` |
| [자료차수/1차/block_encryption_resnet50_rebuilt_KO.ipynb](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/1%EC%B0%A8/block_encryption_resnet50_rebuilt_KO.ipynb) | .ipynb | 93336 | `e4526e11284c362e99634a7f3a7cd2ee3e96c79b25a8e1970d57eba31669de89` |
| [자료차수/1차/block_encryption_resnet50_same_settings_seq.ipynb](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/1%EC%B0%A8/block_encryption_resnet50_same_settings_seq.ipynb) | .ipynb | 60070 | `e7ee462efd677bce07208fb329a0b16add22b58598dc2e7dff71698c4b5887d6` |
| [자료차수/1차/blur_resnet50_metric_matched_seq.ipynb](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/1%EC%B0%A8/blur_resnet50_metric_matched_seq.ipynb) | .ipynb | 72937 | `ca47cc04346b01931e768101723d2e5c7f9a8d6fc878c53bfba0178331d2dfdc` |
| [자료차수/1차/blur_resnet50_rebuilt_KO.ipynb](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/1%EC%B0%A8/blur_resnet50_rebuilt_KO.ipynb) | .ipynb | 106507 | `2667478acda4fd06ecd4dfb1126540af313490a24dd5b57bc05d670c4cd19819` |
| [자료차수/1차/blur_resnet50_same_settings_seq.ipynb](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/1%EC%B0%A8/blur_resnet50_same_settings_seq.ipynb) | .ipynb | 63986 | `847de605b3686cbaf559cd7c95402b2cded9a2be7b8b536339ddb8ca93acfaa6` |
| [자료차수/1차/create_metric_matched_notebooks.js](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/1%EC%B0%A8/create_metric_matched_notebooks.js) | .js | 18124 | `f40132eda3c769d267c036941a23db74c2b4fab28e9fbb3cc3c57354b3f68973` |
| [자료차수/1차/fix_pseudo_callbacks.py](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/1%EC%B0%A8/fix_pseudo_callbacks.py) | .py | 1725 | `b12fd56841636cc008ee9baecc3d8b237731c2cc4af12802b2487cb3c94a968d` |
| [자료차수/1차/fix_training_repeat_overfit.py](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/1%EC%B0%A8/fix_training_repeat_overfit.py) | .py | 6714 | `a8e3cfd2fc9e97297f213c60e5d006dd731edda15f05785ab46c607f90353510` |
| [자료차수/1차/patch_blur_block_notebooks.js](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/1%EC%B0%A8/patch_blur_block_notebooks.js) | .js | 36556 | `700d96b1a98589cc1e8254660463a77755cf54ab521dff6f7aa7e280a98fad48` |
| [자료차수/1차/rebuild_blur_ko_notebook.py](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/1%EC%B0%A8/rebuild_blur_ko_notebook.py) | .py | 45698 | `47761fbbefedbb8524b8e97d2527d55f82c51fc9e47f88a7a26275822f0bef6a` |

</details>

---

[🏠 프로젝트](../../README.md) · [🗂️ 전체 차수](../REVISION_INDEX.md) · [📁 자료 폴더](../../1%EC%B0%A8) · [➡️ 폴더 2차](folder-2.md)

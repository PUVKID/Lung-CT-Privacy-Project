<a id="️-조합기본--입력-blockblur100조건"></a>

# 조합기본 · 입력 Block→Blur100조건

블록 10개와 블러 10개의 100조합을 비교합니다. 입력 영상을 블록 재배열한 뒤 Gaussian Blur를 적용합니다.

분야: 의료 영상 실험 코드 › TensorFlow·ResNet50 › 입력 Block→Blur

[목적](#purpose) · [기능](#features) · [입출력](#flow) · [구성](#files) · [준비](#setup) · [사용법](#usage) · [결과](#results) · [제약](#limits) · [변경](#changes)

<a name="purpose"></a>

<a id="-이-단계에서-하는-일"></a>

## 연구 목적

이 단계의 핵심은 입력 Block→Blur입니다. 변환 원본에서 train/test를 먼저 나누고 학습 쪽을 증강합니다. 같은 블러 강도에서 블록 크기를 바꾸거나 같은 블록 크기에서 블러 강도를 바꿔 읽습니다.

<a name="features"></a>

<a id="-주요-기능과-처리-방식"></a>

## 방법과 구현

| 구성 | 실제 역할 |
| --- | --- |
| 변환 위치 | 블록 10개와 블러 10개의 100조합을 비교합니다. 입력 영상을 블록 재배열한 뒤 Gaussian Blur를 적용합니다. |
| 모델 연결 | 일반 ResNet50 분류 모델을 사용합니다. |
| 분할·증강 | 변환 원본에서 train/test를 먼저 나누고 학습 쪽을 증강합니다. |
| 입력과 증강 | JPEG 3채널을 512×512 float32로 읽습니다. 학습에서는 좌우·상하 반전, 밝기·대비·잡음을 적용하며 평가 입력과 구분합니다. |
| 분류 헤드 | GAP와 GMP를 연결하고 Dense512→BatchNorm·ReLU·Dropout0.35→Dense256→BatchNorm·ReLU·Dropout0.25→softmax로 분류합니다. |
| 평가·저장 | 조건별 정확도·ROC-AUC·클래스별 Recall·혼동행렬과 모델·그래프 출력을 구분합니다. |
| 테스트 의사 라벨 | 테스트 예측의 최대 확률이 0.88 이상인 영상을 예측 라벨로 학습 자료에 추가하는 후속 경로가 있습니다. |

<a name="flow"></a>

<a id="-입력--처리--출력"></a>

## 입력·처리·출력

| 입력 | 처리 | 출력 |
| --- | --- | --- |
| CT 원본과 클래스 | 분할·학습 자료 준비 | 학습·검증·시험 입력 |
| 입력 또는 특징 | 설정한 변환과 모델 학습 | 조건별 예측 |
| 예측·특징·자원 기록 | 분류 지표·그림·모델 저장 | 조건 비교 결과 |

<a name="files"></a>

<a id="-파일과-핵심-처리"></a>

## 파일별 역할

| 파일 | 이용 방법 |
| --- | --- |
| [블록+블러/block_blur_resnet50_v4_KO.ipynb](../../%EB%B8%94%EB%A1%9D%2B%EB%B8%94%EB%9F%AC/block_blur_resnet50_v4_KO.ipynb) | 설정·함수·실행 셀 |

<a id="-함수셀로-찾아가기"></a>

### 관련 함수와 셀

관련 함수와 셀을 파일별로 정리했습니다. 실행 전 설정과 호출 순서, 출력 경로를 확인하세요.

| 파일 | 핵심 정의 |
| --- | --- |
| [블록+블러/block_blur_resnet50_v4_KO.ipynb](../../%EB%B8%94%EB%A1%9D%2B%EB%B8%94%EB%9F%AC/block_blur_resnet50_v4_KO.ipynb) | 셀 6: `gpu_status` · `GPUMonitorCallback` · `__init__` · `on_epoch_end`<br>셀 8: `condition_key` · `condition_label` · `condition_short_label` · `condition_label_from_key` · `set_reproducible` · `list_class_dirs` · `list_image_files`<br>셀 10: `block_scramble` · `generate_block_dataset` · `apply_gaussian_blur` · `generate_blur_dataset` · `generate_combined_dataset`<br>셀 12: `oversample_train`<br>셀 14: `prepare_split`<br>셀 16: `_deterministic` · `get_paths_labels` · `load_image` · `augment_train` · `mixup_batch` · `cutmix_batch` · `apply_mixup` · `apply_cutmix`<br>셀 18: `focal_loss` · `loss_fn` · `CosineAnnealingWarmRestart` · `__init__` · `on_epoch_begin` · `SWACallback` · `__init__` · `on_epoch_end` |

<a name="setup"></a>

<a id="️-환경과-설정"></a>

## 실행 환경과 설정

| 항목 | 조건·기본값 |
| --- | --- |
| 이미지·배치 | 512×512·batch8 |
| 재현 설정 | seed42·7fold·test 비율 0.10 |
| 학습 설정 | 설정 셀의 단계별 epoch·SWA 시작 40·TTA20 |
| 입력 | 별도 CT 데이터와 클래스 폴더 |
| 변환 조건 | 입력 100조합 |
| 최대 epoch | EPOCHS_S1=80·EPOCHS_S2=200 |
| 학습 증강 | 밝기 최대 0.25×255·대비 0.75~1.25·Gaussian 잡음 표준편차 5 |
| TTA 증강 | 좌우 반전·밝기 최대 0.15×255·대비 0.85~1.15 |
| fold | StratifiedKFold·shuffle·seed42·클래스 가중치 |
| 손실 | focal_loss: gamma2·학습 label smoothing0.02 |
| 최적화 | AdamW·weight decay1e-4·학습률 1e-3→1e-4 |
| 후속 재학습 | 학습률 3e-5·label smoothing0.05 |
| 중단·체크포인트 | val_loss 조기 중단·최선 가중치·과적합 제어·SWA/TTA 경로 |

<a name="usage"></a>

<a id="-준비와-사용-순서"></a>

## 실행 순서

1. 설정 셀에서 입력·작업·결과 경로와 변환 조건을 확인합니다.
2. 분할·증강 함수의 호출 순서와 시험 자료가 분리되는 지점을 읽습니다.
3. GPU·TensorFlow·학습 자료를 준비하고 설치·모니터·학습·출력 셀을 구분해 순서대로 읽습니다.
4. 기존 결과의 재사용 조건을 확인한 뒤 필요한 조건을 선택합니다.
5. 조건별 JSON과 혼동행렬·ROC-AUC·Recall을 같은 분모와 클래스 순서로 비교합니다.

<a name="results"></a>

<a id="-결과를-읽는-방법"></a>

## 결과와 해석

같은 블러 강도에서 블록 크기를 바꾸거나 같은 블록 크기에서 블러 강도를 바꿔 읽습니다.

원고 보고값과 이 코드의 조건별 저장 결과를 구분합니다. 변환 위치·분할·시드와 실제 결과 파일이 같은지 확인합니다.

<a name="limits"></a>

<a id="️-알려진-제약과-확인-지점"></a>

## 제약과 확인 사항

| 상황 | 확인할 내용 |
| --- | --- |
| 변환의 의미 | 블록 재배열·블러 강도만으로 환자 재식별 저항성이나 암호학적 안전성을 보증하지 않습니다. |
| 결과 재사용 | 조건별 데이터·가중치·결과를 만들거나 재사용하므로 입력·출력 폴더와 기존 결과를 구분합니다. |
| 분할 | 변환 원본에서 train/test를 먼저 나누고 학습 쪽을 증강합니다. |
| 평가 방식 | 테스트 의사 라벨 추가 학습 후의 수치는 transductive 평가입니다. 테스트 자료를 전혀 이용하지 않은 독립 평가와 구분합니다. |
| 예시 그래프 | 실제 결과·학습 이력이 없으면 _dummy_results 또는 _dummy_histories 계열로 예시 값을 만드는 그래프 셀이 있습니다. 그래프가 그려졌다는 사실만으로 학습 결과로 인용하지 않습니다. |
| 입력 스케일 | load_image는 float32 변환으로 0~255 입력을 유지합니다. ImageNet 사전학습과 연결할 때 전처리 가정을 확인합니다. |

<a name="changes"></a>

<a id="-이전-단계와의-변화"></a>

## 직전 단계와 비교

입력 Block→Blur의 구현과 평가 경로를 다루는 단계입니다. 변환 위치·모델 연결·분할 순서는 위 구성과 같으며, 기존 전체 비교에서 설정·함수·주석을 포함한 차이를 읽을 수 있습니다.

[직전 단계 전체 비교·구성](../revision-diffs/experiment-8.diff) · [전체 파일 크기·해시](../revision-manifests/experiment-8.json)

<details>
<summary>이 단계의 파일 기록과 전체 해시</summary>

아래 표는 해당 단계가 기록될 당시의 파일 정보입니다. 현재 첨부는 [프로젝트 자료 안내](../PAPERS.md)에서 확인할 수 있습니다.

| 파일 | 종류 | 바이트 | SHA-256 |
|---|---|---:|---|
| [블록+블러/block_blur_resnet50_v4_KO.ipynb](../../%EB%B8%94%EB%A1%9D%2B%EB%B8%94%EB%9F%AC/block_blur_resnet50_v4_KO.ipynb) | .ipynb | 123969 | `42d6c2bcdf41bcff53ab1d99f6687a3fb75f0bd1bf8071565ac66952111b634a` |
| [원본자료/블록+블러/block_blur_resnet50_v4_KO.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EB%B8%94%EB%A1%9D%2B%EB%B8%94%EB%9F%AC/block_blur_resnet50_v4_KO.ipynb) | .ipynb | 124546 | `5eede93c16dcfb25d0fb60e1e3900ba0c883d3c4bb503ebb398343ec9709964d` |
| [원본자료/블록+블러/실험 완료/all_block_blur_results_resnet50_block_blur_all_combinations_v1.json](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EB%B8%94%EB%A1%9D%2B%EB%B8%94%EB%9F%AC/%EC%8B%A4%ED%97%98%20%EC%99%84%EB%A3%8C/all_block_blur_results_resnet50_block_blur_all_combinations_v1.json) | .json | 57221 | `7f3cb8aa58b2aba0ac843629ea14fbe52f35ab365ee5975e27d2127165f544b2` |

</details>

---

[프로젝트](../../README.md) · [전체 차수](../REVISION_INDEX.md) · [자료 폴더](../../%EB%B8%94%EB%A1%9D%2B%EB%B8%94%EB%9F%AC)

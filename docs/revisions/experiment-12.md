<div align="center">

# 🧠 Stage1엣지 · 특징맵 자체에 블러

**ResNet50의 pool1_pool 특징에 채널별 고정 Gaussian 커널을 depthwise_conv2d로 적용합니다.**

**기술 분류:** 의료 영상 실험 코드 › TensorFlow·ResNet50 › pool1_pool 특징 블러

[목적](#purpose) · [기능](#features) · [입출력](#flow) · [구성](#files) · [준비](#setup) · [사용법](#usage) · [결과](#results) · [제약](#limits) · [변경](#changes)

</div>

<a name="purpose"></a>

## 🎯 이 단계에서 하는 일

이 단계의 핵심은 pool1_pool 특징 블러입니다. 원본 test를 먼저 분리하고 학습 쪽을 증강합니다. σ32·64·128·256은 전역 평균 분기로 처리됩니다. REUSE_COLLAPSED_RESULTS를 켜면 같은 분기의 결과를 재사용합니다.

<a name="features"></a>

## 🧩 주요 기능과 처리 방식

| 구성 | 실제 역할 |
| --- | --- |
| 변환 위치 | ResNet50의 pool1_pool 특징에 채널별 고정 Gaussian 커널을 depthwise_conv2d로 적용합니다. |
| 모델 연결 | edge→FeatureGaussianBlur→cloud 순서로 연결합니다. |
| 분할·증강 | 원본 test를 먼저 분리하고 학습 쪽을 증강합니다. |
| 입력과 증강 | JPEG 3채널을 512×512 float32로 읽습니다. 학습에서는 좌우·상하 반전, 밝기·대비·잡음을 적용하며 평가 입력과 구분합니다. |
| 분류 헤드 | GAP와 GMP를 연결하고 Dense512→BatchNorm·ReLU·Dropout0.35→Dense256→BatchNorm·ReLU·Dropout0.25→softmax로 분류합니다. |
| 평가·저장 | 조건별 정확도·ROC-AUC·클래스별 Recall·혼동행렬과 모델·그래프 출력을 구분합니다. |
| 테스트 의사 라벨 | 테스트 예측의 최대 확률이 0.88 이상인 영상을 예측 라벨로 학습 자료에 추가하는 후속 경로가 있습니다. |
| 추가 분석 | 특징 SSIM·cosine과 선택적 디코더 복원의 PSNR/SSIM 경로를 제공합니다. 설정과 저장된 결과를 구분합니다. |

<a name="flow"></a>

## 🔄 입력 → 처리 → 출력

| 입력 | 처리 | 출력·읽을 결과 |
| --- | --- | --- |
| CT 원본과 클래스 | 분할·학습 자료 준비 | 학습·검증·시험 입력 |
| 입력 또는 특징 | 설정한 변환과 모델 학습 | 조건별 예측 |
| 예측·특징·자원 기록 | 분류 지표·그림·모델 저장 | 조건 비교 결과 |

<a name="files"></a>

## 📁 파일과 핵심 처리

| 파일 | 이용 방법 |
| --- | --- |
| [블러 스테이지 1 엣지/stage1_edge_feature_blur_resnet50.ipynb](../../%EB%B8%94%EB%9F%AC%20%EC%8A%A4%ED%85%8C%EC%9D%B4%EC%A7%80%201%20%EC%97%A3%EC%A7%80/stage1_edge_feature_blur_resnet50.ipynb) | 설정·함수·실행 셀 |

### 🔎 함수·셀로 찾아가기

아래 이름은 해당 파일의 실제 정의입니다. 위 처리 설명과 함께 설정·호출 순서·출력 경로를 따라 읽습니다.

| 파일 | 핵심 정의 |
| --- | --- |
| [블러 스테이지 1 엣지/stage1_edge_feature_blur_resnet50.ipynb](../../%EB%B8%94%EB%9F%AC%20%EC%8A%A4%ED%85%8C%EC%9D%B4%EC%A7%80%201%20%EC%97%A3%EC%A7%80/stage1_edge_feature_blur_resnet50.ipynb) | 셀 6: `gpu_status` · `GPUMonitorCallback` · `__init__` · `on_epoch_end`<br>셀 8: `condition_key` · `condition_label` · `condition_label_from_key` · `set_reproducible` · `list_class_dirs` · `list_image_files` · `_box_line`<br>셀 10: `prepare_split` · `oversample_train`<br>셀 12: `_deterministic` · `get_paths_labels` · `load_image` · `augment_train` · `mixup_batch` · `cutmix_batch` · `apply_mixup_cutmix` · `_apply`<br>셀 14: `focal_loss` · `loss_fn` · `CosineAnnealingWarmRestart` · `__init__` · `on_epoch_begin` · `SWACallback` · `__init__` · `on_epoch_end`<br>셀 16: `_gaussian_kernel_2d` · `FeatureGaussianBlur` · `__init__` · `call` · `get_config` · `is_collapse_sigma` · `build_edge_model` · `build_cloud_model`<br>셀 18: `diagnose_fit` · `print_fold_result` · `AdvancedMonitorCallback` · `__init__` · `on_epoch_end` · `OverfitControlCallback` · `__init__` · `on_epoch_end` |

<a name="setup"></a>

## ⚙️ 환경과 설정

| 항목 | 조건·기본값 |
| --- | --- |
| 이미지·배치 | 512×512·batch8 |
| 재현 설정 | seed42·7fold·test 비율 0.10 |
| 학습 설정 | 설정 셀의 단계별 epoch·SWA 시작 40·TTA20 |
| 입력 | 별도 CT 데이터와 클래스 폴더 |
| 변환 조건 | 특징 σ 10개 |
| 최대 epoch | EPOCHS_S1=80·EPOCHS_S2=200 |
| 학습 증강 | 밝기 최대 0.25×255·대비 0.75~1.25·Gaussian 잡음 표준편차 5 |
| TTA 증강 | 좌우 반전·밝기 최대 0.15×255·대비 0.85~1.15 |
| fold | StratifiedKFold·shuffle·seed42·클래스 가중치 |
| 손실 | focal_loss: gamma2·학습 label smoothing0.02 |
| 최적화 | AdamW·weight decay1e-4·학습률 1e-4 |
| 후속 재학습 | 학습률 3e-5·label smoothing0.05 |
| 중단·체크포인트 | val_loss 조기 중단·최선 가중치·과적합 제어·SWA/TTA 경로 |
| 분리 모델의 fit | 최대 EPOCHS_S1+EPOCHS_S2=280epoch로 연결 학습 |
| 선택적 복원 디코더 | AdamW 학습률 5e-4·weight decay1e-5·MAE 손실 |

<a name="usage"></a>

## 🚀 준비와 사용 순서

1. 설정 셀에서 입력·작업·결과 경로와 변환 조건을 확인합니다.
2. 분할·증강 함수의 호출 순서와 시험 자료가 분리되는 지점을 읽습니다.
3. GPU·TensorFlow·학습 자료를 준비하고 설치·모니터·학습·출력 셀을 구분해 순서대로 읽습니다.
4. 기존 결과의 재사용 조건을 확인한 뒤 필요한 조건을 선택합니다.
5. 조건별 JSON과 혼동행렬·ROC-AUC·Recall을 같은 분모와 클래스 순서로 비교합니다.

<a name="results"></a>

## 📊 결과를 읽는 방법

σ32·64·128·256은 전역 평균 분기로 처리됩니다. REUSE_COLLAPSED_RESULTS를 켜면 같은 분기의 결과를 재사용합니다.

원고 보고값과 이 코드의 조건별 저장 결과를 구분합니다. 변환 위치·분할·시드와 실제 결과 파일이 같은지 확인합니다.

<a name="limits"></a>

## 🛠️ 알려진 제약과 확인 지점

| 상황 | 확인할 내용 |
| --- | --- |
| 변환의 의미 | 블록 재배열·블러 강도만으로 환자 재식별 저항성이나 암호학적 안전성을 보증하지 않습니다. |
| 결과 재사용 | 조건별 데이터·가중치·결과를 만들거나 재사용하므로 입력·출력 폴더와 기존 결과를 구분합니다. |
| 분할 | 원본 test를 먼저 분리하고 학습 쪽을 증강합니다. |
| 평가 방식 | 테스트 의사 라벨 추가 학습 후의 수치는 transductive 평가입니다. 테스트 자료를 전혀 이용하지 않은 독립 평가와 구분합니다. |
| 배치 구조 | edge/cloud는 코드의 모듈 분리입니다. 이 노트북은 같은 프로세스에서 연결합니다. |
| 전역 평균 분기 | 같은 분기의 재사용 결과를 조건마다 독립 재학습한 값으로 세지 않습니다. |
| 예시 그래프 | 실제 결과·학습 이력이 없으면 _dummy_results 또는 _dummy_histories 계열로 예시 값을 만드는 그래프 셀이 있습니다. 그래프가 그려졌다는 사실만으로 학습 결과로 인용하지 않습니다. |
| 입력 스케일 | load_image는 float32 변환으로 0~255 입력을 유지합니다. ImageNet 사전학습과 연결할 때 전처리 가정을 확인합니다. |
| 복원 코드 의존성 | 선택적 디코더는 Conv2D를 사용하지만 해당 이름의 import/정의가 필요합니다. 공격 실험을 실행하기 전에 의존성을 확인합니다. |

<a name="changes"></a>

## 🔀 이전 단계와의 변화

pool1_pool 특징 블러의 구현과 평가 경로를 다루는 단계입니다. 변환 위치·모델 연결·분할 순서는 위 구성과 같으며, 기존 전체 비교에서 설정·함수·주석을 포함한 차이를 읽을 수 있습니다.

[🔎 직전 단계 전체 비교·구성](../revision-diffs/experiment-12.diff) · [📋 전체 파일 크기·해시](../revision-manifests/experiment-12.json)

<details>
<summary>📎 이 단계의 파일 기록과 전체 해시</summary>

아래 표는 해당 단계가 기록될 당시의 파일 정보입니다. 현재 첨부는 [프로젝트 자료 안내](../PAPERS.md)에서 확인할 수 있습니다.

| 파일 | 종류 | 바이트 | SHA-256 |
|---|---|---:|---|
| [블러 스테이지 1 엣지/stage1_edge_feature_blur_resnet50.ipynb](../../%EB%B8%94%EB%9F%AC%20%EC%8A%A4%ED%85%8C%EC%9D%B4%EC%A7%80%201%20%EC%97%A3%EC%A7%80/stage1_edge_feature_blur_resnet50.ipynb) | .ipynb | 136775 | `069080fa81d3e1f740d9cb0f9433b3a6cb1184a3af6a626956bc4b948cc87caa` |
| [원본자료/블러 스테이지 1 엣지/stage1_edge_feature_blur_resnet50.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EB%B8%94%EB%9F%AC%20%EC%8A%A4%ED%85%8C%EC%9D%B4%EC%A7%80%201%20%EC%97%A3%EC%A7%80/stage1_edge_feature_blur_resnet50.ipynb) | .ipynb | 136774 | `31f78836099ec69365232e8a30071e8b6f4ed0bb70491b29f2b08a6dcfcb51e1` |
| [원본자료/블러 스테이지 1 엣지/stage1_feature_blur_resnet50_outputs/results/all_stage1_feature_blur_results_resnet50_stage1_feature_blur_resnet50_v1.json](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EB%B8%94%EB%9F%AC%20%EC%8A%A4%ED%85%8C%EC%9D%B4%EC%A7%80%201%20%EC%97%A3%EC%A7%80/stage1_feature_blur_resnet50_outputs/results/all_stage1_feature_blur_results_resnet50_stage1_feature_blur_resnet50_v1.json) | .json | 7731 | `74122d318190860fb214e01725ce4bc8d81e1abe533c67be64beb5224dd7f802` |

</details>

---

[🏠 프로젝트](../../README.md) · [🗂️ 전체 차수](../REVISION_INDEX.md) · [📁 자료 폴더](../../%EB%B8%94%EB%9F%AC%20%EC%8A%A4%ED%85%8C%EC%9D%B4%EC%A7%80%201%20%EC%97%A3%EC%A7%80)

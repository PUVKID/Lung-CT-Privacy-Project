<a id="-블록-2차--위치-재배열과-resnet50"></a>

# 블록 2차·위치 재배열과 ResNet50

<!-- reading-levels17:start -->
읽기 수준 · [LEVEL 1](#reading-level-1) · [LEVEL 2](#reading-level-2) · [LEVEL 3](#reading-level-3) · [LEVEL 4](#reading-level-4) · [LEVEL 5](#reading-level-5)

<details open>
<summary>LEVEL 1 · Beginner — 목적과 동작부터</summary>

<a id="reading-level-1"></a>

## LEVEL 1 - Beginner

<a id="semantic-lung-training-level-1"></a>

| 항목 | 이 차수의 내용 |
| --- | --- |
| 목적 | 시드로 정한 순열에 따라 입력 블록의 위치를 바꾸며 블록 내부 픽셀 배열은 유지합니다.<br>영상보다 작지 않은 블록은 원본을 복사합니다. |
| 변경 | 입력 블록 재배열의 구현과 평가 경로를 다루는 단계입니다.<br>변환 위치·모델 연결·분할 순서는 위 구성과 같으며, 기존 전체 비교에서 설정·함수·주석을 포함한 차이를 읽을 수 있습니다. |
| 조건 | **이미지·배치**: 512×512·batch8<br>**재현 설정**: seed42·7fold·test 비율 0.10<br>**학습 설정**: 설정 셀의 단계별 epoch·SWA 시작 40·TTA20<br>**입력**: 별도 CT 데이터와 클래스 폴더<br>**변환 조건**: 입력 10 조건<br>**최대 epoch**: EPOCHS_S1=80·EPOCHS_S2=200<br>**학습 증강**: 밝기 최대 0.25×255·대비 0.75~1.25·Gaussian 잡음 표준편차 5<br>**TTA 증강**: 좌우 반전·밝기 최대 0.15×255·대비 0.85~1.15<br>**fold**: StratifiedKFold·shuffle·seed42·클래스 가중치<br>**손실**: focal_loss: gamma2·학습 label smoothing0.02<br>**최적화**: AdamW·weight decay1e-4·학습률 1e-3→1e-4<br>**후속 재학습**: 학습률 3e-5·label smoothing0.05<br>**중단·체크포인트**: val_loss 조기 중단·최선 가중치·과적합 제어·SWA/TTA 경로 |
| 동작 | 1.<br>설정 셀에서 입력·작업·결과 경로와 변환 조건을 확인합니다. |
| 결과 | 원고 보고값과 이 코드의 조건별 저장 결과를 구분합니다.<br>변환 위치·분할·시드와 실제 결과 파일이 같은지 확인합니다. |

### LEVEL 1 · 노트북 학습·평가의 연결과 실패 조건

**블록 2차·위치 재배열과 ResNet50**의 범위에서 설명합니다. 먼저 이 자료가 무엇을 바꾸고 무엇을 보여 주는지 살펴봅니다. 아래 조건은 이 문서에 연결된 파일의 내용이며 다른 차수의 결과를 함께 센 값이 아닙니다.

| 항목 | 이 차수의 내용 |
| --- | --- |
| <a id="layout18-table-1-row-1"></a> **목적** | 이 단계의 핵심은 입력 블록 재배열입니다. 이 사본은 oversample_dir 뒤 prepare_split을 호출해 증강 후 train/test를 나눕니다. 블록 크기 512~1의 분류 결과를 비교합니다. |
| <a id="layout18-table-1-row-2"></a> **구현** | **변환 위치**: 시드로 정한 순열에 따라 입력 블록의 위치를 바꾸며 블록 내부 픽셀 배열은 유지합니다.<br>영상보다 작지 않은 블록은 원본을 복사합니다.<br>**모델 연결**: 일반 ResNet50 분류 모델을 사용합니다.<br>**분할·증강**: 이 사본은 oversample_dir 뒤 prepare_split을 호출해 증강 후 train/test를 나눕니다.<br>**입력과 증강**: JPEG 3 채널을 512×512 float32로 읽습니다.<br>학습에서는 좌우·상하 반전, 밝기·대비·잡음을 적용하며 평가 입력과 구분합니다.<br>**분류 헤드**: GAP와 GMP를 연결하고 Dense512 →BatchNorm·ReLU·Dropout0.35 →Dense256 →BatchNorm·ReLU·Dropout0.25 →softmax로 분류합니다.<br>**평가·저장**: 조건별 정확도·ROC-AUC·클래스별 Recall·혼동행렬과 모델·그래프 출력을 구분합니다.<br>**테스트 의사 라벨**: 테스트 예측의 최대 확률이 0.88 이상인 영상을 예측 라벨로 학습 자료에 추가하는 후속 경로가 있습니다. |
| <a id="layout18-table-1-row-3"></a> **조건** | **이미지·배치**: 512×512·batch8<br>**재현 설정**: seed42·7fold·test 비율 0.10<br>**학습 설정**: 설정 셀의 단계별 epoch·SWA 시작 40·TTA20<br>**입력**: 별도 CT 데이터와 클래스 폴더<br>**변환 조건**: 입력 10 조건<br>**최대 epoch**: EPOCHS_S1=80·EPOCHS_S2=200<br>**학습 증강**: 밝기 최대 0.25×255·대비 0.75~1.25·Gaussian 잡음 표준편차 5<br>**TTA 증강**: 좌우 반전·밝기 최대 0.15×255·대비 0.85~1.15<br>**fold**: StratifiedKFold·shuffle·seed42·클래스 가중치<br>**손실**: focal_loss: gamma2·학습 label smoothing0.02<br>**최적화**: AdamW·weight decay1e-4·학습률 1e-3→1e-4<br>**후속 재학습**: 학습률 3e-5·label smoothing0.05<br>**중단·체크포인트**: val_loss 조기 중단·최선 가중치·과적합 제어·SWA/TTA 경로 |
| <a id="layout18-table-1-row-4"></a> **관측과 해석** | 블록 크기 512~1의 분류 결과를 비교합니다.<br>원고 보고값과 이 코드의 조건별 저장 결과를 구분합니다. 변환 위치·분할·시드와 실제 결과 파일이 같은지 확인합니다. |
| <a id="layout18-table-1-row-5"></a> **한계** | **변환의 의미**: 블록 재배열·블러 강도만으로 환자 재식별 저항성이나 암호학적 안전성을 보증하지 않습니다.<br>**결과 재사용**: 조건별 데이터·가중치·결과를 만들거나 재사용하므로 입력·출력 폴더와 기존 결과를 구분합니다.<br>**분할**: 이 사본은 oversample_dir 뒤 prepare_split을 호출해 증강 후 train/test를 나눕니다.<br>**평가 방식**: 테스트 의사 라벨 추가 학습 후의 수치는 transductive 평가입니다.<br>테스트 자료를 전혀 이용하지 않은 독립 평가와 구분합니다.<br>**자료 중복**: 증강 후 분할하는 이 사본에서는 같은 원영상에서 파생한 자료가 학습·시험 양쪽에 들어갈 위험을 확인해야 합니다.<br>**예시 그래프**: 실제 결과·학습 이력이 없으면 _dummy_results 또는 _dummy_histories 계열로 예시 값을 만드는 그래프 셀이 있습니다.<br>그래프가 그려졌다는 사실만으로 학습 결과로 인용하지 않습니다.<br>**입력 스케일**: load_image는 float32 변환으로 0~255 입력을 유지합니다.<br>ImageNet 사전 학습과 연결할 때 전처리 가정을 확인합니다. |
| <a id="layout18-table-1-row-6"></a> **자료 연결** | [이 차수 전체 상세](#purpose) · [실행 순서](#usage) · [결과와 해석](#results) · [프로젝트 공통 안내](../../README.md)<br>다른 입력 변환·모델 구성과 원고 보고값은 [공통 프로젝트 안내](../../README.md)에서 해당 자료로 이동합니다. |
| <a id="layout18-table-1-row-7"></a> **읽기 범위** | 이 차수의 [전체 상세](#purpose)와 [파일 구성](#files)을 확인합니다. 다른 차수의 사실은 공통 안내 링크에서 별도로 읽습니다. |


<a id="semantic-lung-feature-level-1"></a>

### LEVEL 1 · 입력 변환·분리 모델·특징 블러의 차이

<a id="layout18-table-2-row-1"></a><a id="layout18-table-2-row-2"></a><a id="layout18-table-2-row-3"></a><a id="layout18-table-2-row-4"></a>

이 차수의 목적·구현·조건·관측과 한계는 [위의 같은 차수 표](#layout18-table-1-row-1)에서 함께 비교합니다. 다른 변환 방식과 자료 차수의 설명은 [프로젝트 공통 안내](../../README.md)에서 해당 문서로 이동합니다.


[동일 수준 프로젝트 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A81.md)


</details>

<details>
<summary>LEVEL 2 · Explorer — 구성과 연결 원리</summary>

<a id="reading-level-2"></a>

## LEVEL 2 - Explorer

<a id="semantic-lung-training-level-2"></a>

| 항목 | 이 차수의 내용 |
| --- | --- |
| 목적 | 시드로 정한 순열에 따라 입력 블록의 위치를 바꾸며 블록 내부 픽셀 배열은 유지합니다.<br>영상보다 작지 않은 블록은 원본을 복사합니다. |
| 변경 | 입력 블록 재배열의 구현과 평가 경로를 다루는 단계입니다.<br>변환 위치·모델 연결·분할 순서는 위 구성과 같으며, 기존 전체 비교에서 설정·함수·주석을 포함한 차이를 읽을 수 있습니다. |
| 조건 | **이미지·배치**: 512×512·batch8<br>**재현 설정**: seed42·7fold·test 비율 0.10<br>**학습 설정**: 설정 셀의 단계별 epoch·SWA 시작 40·TTA20<br>**입력**: 별도 CT 데이터와 클래스 폴더<br>**변환 조건**: 입력 10 조건<br>**최대 epoch**: EPOCHS_S1=80·EPOCHS_S2=200<br>**학습 증강**: 밝기 최대 0.25×255·대비 0.75~1.25·Gaussian 잡음 표준편차 5<br>**TTA 증강**: 좌우 반전·밝기 최대 0.15×255·대비 0.85~1.15<br>**fold**: StratifiedKFold·shuffle·seed42·클래스 가중치<br>**손실**: focal_loss: gamma2·학습 label smoothing0.02<br>**최적화**: AdamW·weight decay1e-4·학습률 1e-3→1e-4<br>**후속 재학습**: 학습률 3e-5·label smoothing0.05<br>**중단·체크포인트**: val_loss 조기 중단·최선 가중치·과적합 제어·SWA/TTA 경로 |
| 동작 | 1.<br>설정 셀에서 입력·작업·결과 경로와 변환 조건을 확인합니다. |
| 결과 | 원고 보고값과 이 코드의 조건별 저장 결과를 구분합니다.<br>변환 위치·분할·시드와 실제 결과 파일이 같은지 확인합니다. |

### LEVEL 2 · 노트북 학습·평가의 연결과 실패 조건

**블록 2차·위치 재배열과 ResNet50**의 범위에서 설명합니다. 입력 → 처리 → 출력의 순서로 읽습니다. 설정을 준비한 것과 실제 실행에서 얻은 결과를 구분하고, 관측값은 같은 입력·설정의 기록과 연결합니다.

| 항목 | 이 차수의 내용 |
| --- | --- |
| <a id="layout18-table-7-row-1"></a> **목적** | 이 단계의 핵심은 입력 블록 재배열입니다. 이 사본은 oversample_dir 뒤 prepare_split을 호출해 증강 후 train/test를 나눕니다. 블록 크기 512~1의 분류 결과를 비교합니다. |
| <a id="layout18-table-7-row-2"></a> **구현** | **변환 위치**: 시드로 정한 순열에 따라 입력 블록의 위치를 바꾸며 블록 내부 픽셀 배열은 유지합니다.<br>영상보다 작지 않은 블록은 원본을 복사합니다.<br>**모델 연결**: 일반 ResNet50 분류 모델을 사용합니다.<br>**분할·증강**: 이 사본은 oversample_dir 뒤 prepare_split을 호출해 증강 후 train/test를 나눕니다.<br>**입력과 증강**: JPEG 3 채널을 512×512 float32로 읽습니다.<br>학습에서는 좌우·상하 반전, 밝기·대비·잡음을 적용하며 평가 입력과 구분합니다.<br>**분류 헤드**: GAP와 GMP를 연결하고 Dense512 →BatchNorm·ReLU·Dropout0.35 →Dense256 →BatchNorm·ReLU·Dropout0.25 →softmax로 분류합니다.<br>**평가·저장**: 조건별 정확도·ROC-AUC·클래스별 Recall·혼동행렬과 모델·그래프 출력을 구분합니다.<br>**테스트 의사 라벨**: 테스트 예측의 최대 확률이 0.88 이상인 영상을 예측 라벨로 학습 자료에 추가하는 후속 경로가 있습니다. |
| <a id="layout18-table-7-row-3"></a> **조건** | **이미지·배치**: 512×512·batch8<br>**재현 설정**: seed42·7fold·test 비율 0.10<br>**학습 설정**: 설정 셀의 단계별 epoch·SWA 시작 40·TTA20<br>**입력**: 별도 CT 데이터와 클래스 폴더<br>**변환 조건**: 입력 10 조건<br>**최대 epoch**: EPOCHS_S1=80·EPOCHS_S2=200<br>**학습 증강**: 밝기 최대 0.25×255·대비 0.75~1.25·Gaussian 잡음 표준편차 5<br>**TTA 증강**: 좌우 반전·밝기 최대 0.15×255·대비 0.85~1.15<br>**fold**: StratifiedKFold·shuffle·seed42·클래스 가중치<br>**손실**: focal_loss: gamma2·학습 label smoothing0.02<br>**최적화**: AdamW·weight decay1e-4·학습률 1e-3→1e-4<br>**후속 재학습**: 학습률 3e-5·label smoothing0.05<br>**중단·체크포인트**: val_loss 조기 중단·최선 가중치·과적합 제어·SWA/TTA 경로 |
| <a id="layout18-table-7-row-4"></a> **관측과 해석** | 블록 크기 512~1의 분류 결과를 비교합니다.<br>원고 보고값과 이 코드의 조건별 저장 결과를 구분합니다. 변환 위치·분할·시드와 실제 결과 파일이 같은지 확인합니다. |
| <a id="layout18-table-7-row-5"></a> **한계** | **변환의 의미**: 블록 재배열·블러 강도만으로 환자 재식별 저항성이나 암호학적 안전성을 보증하지 않습니다.<br>**결과 재사용**: 조건별 데이터·가중치·결과를 만들거나 재사용하므로 입력·출력 폴더와 기존 결과를 구분합니다.<br>**분할**: 이 사본은 oversample_dir 뒤 prepare_split을 호출해 증강 후 train/test를 나눕니다.<br>**평가 방식**: 테스트 의사 라벨 추가 학습 후의 수치는 transductive 평가입니다.<br>테스트 자료를 전혀 이용하지 않은 독립 평가와 구분합니다.<br>**자료 중복**: 증강 후 분할하는 이 사본에서는 같은 원영상에서 파생한 자료가 학습·시험 양쪽에 들어갈 위험을 확인해야 합니다.<br>**예시 그래프**: 실제 결과·학습 이력이 없으면 _dummy_results 또는 _dummy_histories 계열로 예시 값을 만드는 그래프 셀이 있습니다.<br>그래프가 그려졌다는 사실만으로 학습 결과로 인용하지 않습니다.<br>**입력 스케일**: load_image는 float32 변환으로 0~255 입력을 유지합니다.<br>ImageNet 사전 학습과 연결할 때 전처리 가정을 확인합니다. |
| <a id="layout18-table-7-row-6"></a> **자료 연결** | [이 차수 전체 상세](#purpose) · [실행 순서](#usage) · [결과와 해석](#results) · [프로젝트 공통 안내](../../README.md)<br>다른 입력 변환·모델 구성과 원고 보고값은 [공통 프로젝트 안내](../../README.md)에서 해당 자료로 이동합니다. |
| <a id="layout18-table-7-row-7"></a> **읽기 범위** | 이 차수의 [전체 상세](#purpose)와 [파일 구성](#files)을 확인합니다. 다른 차수의 사실은 공통 안내 링크에서 별도로 읽습니다. |


<a id="semantic-lung-feature-level-2"></a>

### LEVEL 2 · 입력 변환·분리 모델·특징 블러의 차이

<a id="layout18-table-8-row-1"></a><a id="layout18-table-8-row-2"></a><a id="layout18-table-8-row-3"></a><a id="layout18-table-8-row-4"></a>

이 차수의 목적·구현·조건·관측과 한계는 [위의 같은 차수 표](#layout18-table-7-row-1)에서 함께 비교합니다. 다른 변환 방식과 자료 차수의 설명은 [프로젝트 공통 안내](../../README.md)에서 해당 문서로 이동합니다.


[동일 수준 프로젝트 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A82.md)


</details>

<details>
<summary>LEVEL 3 · Practitioner — 준비·실행·결과 확인</summary>

<a id="reading-level-3"></a>

## LEVEL 3 - Practitioner

<a id="semantic-lung-training-level-3"></a>

| 항목 | 이 차수의 내용 |
| --- | --- |
| 목적 | 시드로 정한 순열에 따라 입력 블록의 위치를 바꾸며 블록 내부 픽셀 배열은 유지합니다.<br>영상보다 작지 않은 블록은 원본을 복사합니다. |
| 변경 | 입력 블록 재배열의 구현과 평가 경로를 다루는 단계입니다.<br>변환 위치·모델 연결·분할 순서는 위 구성과 같으며, 기존 전체 비교에서 설정·함수·주석을 포함한 차이를 읽을 수 있습니다. |
| 조건 | **이미지·배치**: 512×512·batch8<br>**재현 설정**: seed42·7fold·test 비율 0.10<br>**학습 설정**: 설정 셀의 단계별 epoch·SWA 시작 40·TTA20<br>**입력**: 별도 CT 데이터와 클래스 폴더<br>**변환 조건**: 입력 10 조건<br>**최대 epoch**: EPOCHS_S1=80·EPOCHS_S2=200<br>**학습 증강**: 밝기 최대 0.25×255·대비 0.75~1.25·Gaussian 잡음 표준편차 5<br>**TTA 증강**: 좌우 반전·밝기 최대 0.15×255·대비 0.85~1.15<br>**fold**: StratifiedKFold·shuffle·seed42·클래스 가중치<br>**손실**: focal_loss: gamma2·학습 label smoothing0.02<br>**최적화**: AdamW·weight decay1e-4·학습률 1e-3→1e-4<br>**후속 재학습**: 학습률 3e-5·label smoothing0.05<br>**중단·체크포인트**: val_loss 조기 중단·최선 가중치·과적합 제어·SWA/TTA 경로 |
| 동작 | 1.<br>설정 셀에서 입력·작업·결과 경로와 변환 조건을 확인합니다. |
| 결과 | 원고 보고값과 이 코드의 조건별 저장 결과를 구분합니다.<br>변환 위치·분할·시드와 실제 결과 파일이 같은지 확인합니다. |

### LEVEL 3 · 노트북 학습·평가의 연결과 실패 조건

**블록 2차·위치 재배열과 ResNet50**의 범위에서 설명합니다. 실행할 파일을 먼저 고르고 아래 전체 상세의 경로·설정·호출 순서를 확인합니다. 표의 구성과 조건을 해당 파일에 맞춰 읽으며 문서 정리 자체가 새 실행을 뜻하지는 않습니다.

| 항목 | 이 차수의 내용 |
| --- | --- |
| <a id="layout18-table-13-row-1"></a> **목적** | 이 단계의 핵심은 입력 블록 재배열입니다. 이 사본은 oversample_dir 뒤 prepare_split을 호출해 증강 후 train/test를 나눕니다. 블록 크기 512~1의 분류 결과를 비교합니다. |
| <a id="layout18-table-13-row-2"></a> **구현** | **변환 위치**: 시드로 정한 순열에 따라 입력 블록의 위치를 바꾸며 블록 내부 픽셀 배열은 유지합니다.<br>영상보다 작지 않은 블록은 원본을 복사합니다.<br>**모델 연결**: 일반 ResNet50 분류 모델을 사용합니다.<br>**분할·증강**: 이 사본은 oversample_dir 뒤 prepare_split을 호출해 증강 후 train/test를 나눕니다.<br>**입력과 증강**: JPEG 3 채널을 512×512 float32로 읽습니다.<br>학습에서는 좌우·상하 반전, 밝기·대비·잡음을 적용하며 평가 입력과 구분합니다.<br>**분류 헤드**: GAP와 GMP를 연결하고 Dense512 →BatchNorm·ReLU·Dropout0.35 →Dense256 →BatchNorm·ReLU·Dropout0.25 →softmax로 분류합니다.<br>**평가·저장**: 조건별 정확도·ROC-AUC·클래스별 Recall·혼동행렬과 모델·그래프 출력을 구분합니다.<br>**테스트 의사 라벨**: 테스트 예측의 최대 확률이 0.88 이상인 영상을 예측 라벨로 학습 자료에 추가하는 후속 경로가 있습니다. |
| <a id="layout18-table-13-row-3"></a> **조건** | **이미지·배치**: 512×512·batch8<br>**재현 설정**: seed42·7fold·test 비율 0.10<br>**학습 설정**: 설정 셀의 단계별 epoch·SWA 시작 40·TTA20<br>**입력**: 별도 CT 데이터와 클래스 폴더<br>**변환 조건**: 입력 10 조건<br>**최대 epoch**: EPOCHS_S1=80·EPOCHS_S2=200<br>**학습 증강**: 밝기 최대 0.25×255·대비 0.75~1.25·Gaussian 잡음 표준편차 5<br>**TTA 증강**: 좌우 반전·밝기 최대 0.15×255·대비 0.85~1.15<br>**fold**: StratifiedKFold·shuffle·seed42·클래스 가중치<br>**손실**: focal_loss: gamma2·학습 label smoothing0.02<br>**최적화**: AdamW·weight decay1e-4·학습률 1e-3→1e-4<br>**후속 재학습**: 학습률 3e-5·label smoothing0.05<br>**중단·체크포인트**: val_loss 조기 중단·최선 가중치·과적합 제어·SWA/TTA 경로 |
| <a id="layout18-table-13-row-4"></a> **관측과 해석** | 블록 크기 512~1의 분류 결과를 비교합니다.<br>원고 보고값과 이 코드의 조건별 저장 결과를 구분합니다. 변환 위치·분할·시드와 실제 결과 파일이 같은지 확인합니다. |
| <a id="layout18-table-13-row-5"></a> **한계** | **변환의 의미**: 블록 재배열·블러 강도만으로 환자 재식별 저항성이나 암호학적 안전성을 보증하지 않습니다.<br>**결과 재사용**: 조건별 데이터·가중치·결과를 만들거나 재사용하므로 입력·출력 폴더와 기존 결과를 구분합니다.<br>**분할**: 이 사본은 oversample_dir 뒤 prepare_split을 호출해 증강 후 train/test를 나눕니다.<br>**평가 방식**: 테스트 의사 라벨 추가 학습 후의 수치는 transductive 평가입니다.<br>테스트 자료를 전혀 이용하지 않은 독립 평가와 구분합니다.<br>**자료 중복**: 증강 후 분할하는 이 사본에서는 같은 원영상에서 파생한 자료가 학습·시험 양쪽에 들어갈 위험을 확인해야 합니다.<br>**예시 그래프**: 실제 결과·학습 이력이 없으면 _dummy_results 또는 _dummy_histories 계열로 예시 값을 만드는 그래프 셀이 있습니다.<br>그래프가 그려졌다는 사실만으로 학습 결과로 인용하지 않습니다.<br>**입력 스케일**: load_image는 float32 변환으로 0~255 입력을 유지합니다.<br>ImageNet 사전 학습과 연결할 때 전처리 가정을 확인합니다. |
| <a id="layout18-table-13-row-6"></a> **자료 연결** | [이 차수 전체 상세](#purpose) · [실행 순서](#usage) · [결과와 해석](#results) · [프로젝트 공통 안내](../../README.md)<br>다른 입력 변환·모델 구성과 원고 보고값은 [공통 프로젝트 안내](../../README.md)에서 해당 자료로 이동합니다. |
| <a id="layout18-table-13-row-7"></a> **읽기 범위** | 이 차수의 [전체 상세](#purpose)와 [파일 구성](#files)을 확인합니다. 다른 차수의 사실은 공통 안내 링크에서 별도로 읽습니다. |


<a id="semantic-lung-feature-level-3"></a>

### LEVEL 3 · 입력 변환·분리 모델·특징 블러의 차이

<a id="layout18-table-14-row-1"></a><a id="layout18-table-14-row-2"></a><a id="layout18-table-14-row-3"></a><a id="layout18-table-14-row-4"></a>

이 차수의 목적·구현·조건·관측과 한계는 [위의 같은 차수 표](#layout18-table-13-row-1)에서 함께 비교합니다. 다른 변환 방식과 자료 차수의 설명은 [프로젝트 공통 안내](../../README.md)에서 해당 문서로 이동합니다.


[동일 수준 프로젝트 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A83.md)


</details>

<details>
<summary>LEVEL 4 · Advanced — 구현·설계·실패 처리</summary>

<a id="reading-level-4"></a>

## LEVEL 4 - Advanced

<a id="semantic-lung-training-level-4"></a>

| 항목 | 이 차수의 내용 |
| --- | --- |
| 목적 | 시드로 정한 순열에 따라 입력 블록의 위치를 바꾸며 블록 내부 픽셀 배열은 유지합니다.<br>영상보다 작지 않은 블록은 원본을 복사합니다. |
| 변경 | 입력 블록 재배열의 구현과 평가 경로를 다루는 단계입니다.<br>변환 위치·모델 연결·분할 순서는 위 구성과 같으며, 기존 전체 비교에서 설정·함수·주석을 포함한 차이를 읽을 수 있습니다. |
| 조건 | **이미지·배치**: 512×512·batch8<br>**재현 설정**: seed42·7fold·test 비율 0.10<br>**학습 설정**: 설정 셀의 단계별 epoch·SWA 시작 40·TTA20<br>**입력**: 별도 CT 데이터와 클래스 폴더<br>**변환 조건**: 입력 10 조건<br>**최대 epoch**: EPOCHS_S1=80·EPOCHS_S2=200<br>**학습 증강**: 밝기 최대 0.25×255·대비 0.75~1.25·Gaussian 잡음 표준편차 5<br>**TTA 증강**: 좌우 반전·밝기 최대 0.15×255·대비 0.85~1.15<br>**fold**: StratifiedKFold·shuffle·seed42·클래스 가중치<br>**손실**: focal_loss: gamma2·학습 label smoothing0.02<br>**최적화**: AdamW·weight decay1e-4·학습률 1e-3→1e-4<br>**후속 재학습**: 학습률 3e-5·label smoothing0.05<br>**중단·체크포인트**: val_loss 조기 중단·최선 가중치·과적합 제어·SWA/TTA 경로 |
| 동작 | 1.<br>설정 셀에서 입력·작업·결과 경로와 변환 조건을 확인합니다. |
| 결과 | 원고 보고값과 이 코드의 조건별 저장 결과를 구분합니다.<br>변환 위치·분할·시드와 실제 결과 파일이 같은지 확인합니다. |

### LEVEL 4 · 노트북 학습·평가의 연결과 실패 조건

**블록 2차·위치 재배열과 ResNet50**의 범위에서 설명합니다. 입력 준비·변환 또는 셀 수정·계산·저장의 경계를 나누어 읽습니다. 각 설정과 출력의 대응은 이 차수 자료를 기준으로 확인하고 다른 차수의 구현은 관련 링크에서 별도로 살펴봅니다.

| 항목 | 이 차수의 내용 |
| --- | --- |
| <a id="layout18-table-19-row-1"></a> **목적** | 이 단계의 핵심은 입력 블록 재배열입니다. 이 사본은 oversample_dir 뒤 prepare_split을 호출해 증강 후 train/test를 나눕니다. 블록 크기 512~1의 분류 결과를 비교합니다. |
| <a id="layout18-table-19-row-2"></a> **구현** | **변환 위치**: 시드로 정한 순열에 따라 입력 블록의 위치를 바꾸며 블록 내부 픽셀 배열은 유지합니다.<br>영상보다 작지 않은 블록은 원본을 복사합니다.<br>**모델 연결**: 일반 ResNet50 분류 모델을 사용합니다.<br>**분할·증강**: 이 사본은 oversample_dir 뒤 prepare_split을 호출해 증강 후 train/test를 나눕니다.<br>**입력과 증강**: JPEG 3 채널을 512×512 float32로 읽습니다.<br>학습에서는 좌우·상하 반전, 밝기·대비·잡음을 적용하며 평가 입력과 구분합니다.<br>**분류 헤드**: GAP와 GMP를 연결하고 Dense512 →BatchNorm·ReLU·Dropout0.35 →Dense256 →BatchNorm·ReLU·Dropout0.25 →softmax로 분류합니다.<br>**평가·저장**: 조건별 정확도·ROC-AUC·클래스별 Recall·혼동행렬과 모델·그래프 출력을 구분합니다.<br>**테스트 의사 라벨**: 테스트 예측의 최대 확률이 0.88 이상인 영상을 예측 라벨로 학습 자료에 추가하는 후속 경로가 있습니다. |
| <a id="layout18-table-19-row-3"></a> **조건** | **이미지·배치**: 512×512·batch8<br>**재현 설정**: seed42·7fold·test 비율 0.10<br>**학습 설정**: 설정 셀의 단계별 epoch·SWA 시작 40·TTA20<br>**입력**: 별도 CT 데이터와 클래스 폴더<br>**변환 조건**: 입력 10 조건<br>**최대 epoch**: EPOCHS_S1=80·EPOCHS_S2=200<br>**학습 증강**: 밝기 최대 0.25×255·대비 0.75~1.25·Gaussian 잡음 표준편차 5<br>**TTA 증강**: 좌우 반전·밝기 최대 0.15×255·대비 0.85~1.15<br>**fold**: StratifiedKFold·shuffle·seed42·클래스 가중치<br>**손실**: focal_loss: gamma2·학습 label smoothing0.02<br>**최적화**: AdamW·weight decay1e-4·학습률 1e-3→1e-4<br>**후속 재학습**: 학습률 3e-5·label smoothing0.05<br>**중단·체크포인트**: val_loss 조기 중단·최선 가중치·과적합 제어·SWA/TTA 경로 |
| <a id="layout18-table-19-row-4"></a> **관측과 해석** | 블록 크기 512~1의 분류 결과를 비교합니다.<br>원고 보고값과 이 코드의 조건별 저장 결과를 구분합니다. 변환 위치·분할·시드와 실제 결과 파일이 같은지 확인합니다. |
| <a id="layout18-table-19-row-5"></a> **한계** | **변환의 의미**: 블록 재배열·블러 강도만으로 환자 재식별 저항성이나 암호학적 안전성을 보증하지 않습니다.<br>**결과 재사용**: 조건별 데이터·가중치·결과를 만들거나 재사용하므로 입력·출력 폴더와 기존 결과를 구분합니다.<br>**분할**: 이 사본은 oversample_dir 뒤 prepare_split을 호출해 증강 후 train/test를 나눕니다.<br>**평가 방식**: 테스트 의사 라벨 추가 학습 후의 수치는 transductive 평가입니다.<br>테스트 자료를 전혀 이용하지 않은 독립 평가와 구분합니다.<br>**자료 중복**: 증강 후 분할하는 이 사본에서는 같은 원영상에서 파생한 자료가 학습·시험 양쪽에 들어갈 위험을 확인해야 합니다.<br>**예시 그래프**: 실제 결과·학습 이력이 없으면 _dummy_results 또는 _dummy_histories 계열로 예시 값을 만드는 그래프 셀이 있습니다.<br>그래프가 그려졌다는 사실만으로 학습 결과로 인용하지 않습니다.<br>**입력 스케일**: load_image는 float32 변환으로 0~255 입력을 유지합니다.<br>ImageNet 사전 학습과 연결할 때 전처리 가정을 확인합니다. |
| <a id="layout18-table-19-row-6"></a> **자료 연결** | [이 차수 전체 상세](#purpose) · [실행 순서](#usage) · [결과와 해석](#results) · [프로젝트 공통 안내](../../README.md)<br>다른 입력 변환·모델 구성과 원고 보고값은 [공통 프로젝트 안내](../../README.md)에서 해당 자료로 이동합니다. |
| <a id="layout18-table-19-row-7"></a> **읽기 범위** | 이 차수의 [전체 상세](#purpose)와 [파일 구성](#files)을 확인합니다. 다른 차수의 사실은 공통 안내 링크에서 별도로 읽습니다. |


<a id="semantic-lung-feature-level-4"></a>

### LEVEL 4 · 입력 변환·분리 모델·특징 블러의 차이

<a id="layout18-table-20-row-1"></a><a id="layout18-table-20-row-2"></a><a id="layout18-table-20-row-3"></a><a id="layout18-table-20-row-4"></a>

이 차수의 목적·구현·조건·관측과 한계는 [위의 같은 차수 표](#layout18-table-19-row-1)에서 함께 비교합니다. 다른 변환 방식과 자료 차수의 설명은 [프로젝트 공통 안내](../../README.md)에서 해당 문서로 이동합니다.


[동일 수준 프로젝트 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A84.md)


</details>

<details>
<summary>LEVEL 5 · Expert — 근거·프로토콜·한계 검토</summary>

<a id="reading-level-5"></a>

## LEVEL 5 - Expert

<a id="semantic-lung-training-level-5"></a>

### LEVEL 5 · 노트북 학습·평가의 연결과 실패 조건

**블록 2차·위치 재배열과 ResNet50**의 범위에서 설명합니다. 코드에 정의된 동작·설정, 저장된 관측값, 재현에 필요한 입력을 구분합니다. 분모·변환 위치·모델 대응과 알려진 한계를 유지하며 다른 차수나 원고의 결과를 이 자료의 실측으로 합치지 않습니다.

| 항목 | 이 차수의 내용 |
| --- | --- |
| <a id="layout18-table-25-row-1"></a> **목적** | 이 단계의 핵심은 입력 블록 재배열입니다. 이 사본은 oversample_dir 뒤 prepare_split을 호출해 증강 후 train/test를 나눕니다. 블록 크기 512~1의 분류 결과를 비교합니다. |
| <a id="layout18-table-25-row-2"></a> **구현** | **변환 위치**: 시드로 정한 순열에 따라 입력 블록의 위치를 바꾸며 블록 내부 픽셀 배열은 유지합니다.<br>영상보다 작지 않은 블록은 원본을 복사합니다.<br>**모델 연결**: 일반 ResNet50 분류 모델을 사용합니다.<br>**분할·증강**: 이 사본은 oversample_dir 뒤 prepare_split을 호출해 증강 후 train/test를 나눕니다.<br>**입력과 증강**: JPEG 3 채널을 512×512 float32로 읽습니다.<br>학습에서는 좌우·상하 반전, 밝기·대비·잡음을 적용하며 평가 입력과 구분합니다.<br>**분류 헤드**: GAP와 GMP를 연결하고 Dense512 →BatchNorm·ReLU·Dropout0.35 →Dense256 →BatchNorm·ReLU·Dropout0.25 →softmax로 분류합니다.<br>**평가·저장**: 조건별 정확도·ROC-AUC·클래스별 Recall·혼동행렬과 모델·그래프 출력을 구분합니다.<br>**테스트 의사 라벨**: 테스트 예측의 최대 확률이 0.88 이상인 영상을 예측 라벨로 학습 자료에 추가하는 후속 경로가 있습니다. |
| <a id="layout18-table-25-row-3"></a> **조건** | **이미지·배치**: 512×512·batch8<br>**재현 설정**: seed42·7fold·test 비율 0.10<br>**학습 설정**: 설정 셀의 단계별 epoch·SWA 시작 40·TTA20<br>**입력**: 별도 CT 데이터와 클래스 폴더<br>**변환 조건**: 입력 10 조건<br>**최대 epoch**: EPOCHS_S1=80·EPOCHS_S2=200<br>**학습 증강**: 밝기 최대 0.25×255·대비 0.75~1.25·Gaussian 잡음 표준편차 5<br>**TTA 증강**: 좌우 반전·밝기 최대 0.15×255·대비 0.85~1.15<br>**fold**: StratifiedKFold·shuffle·seed42·클래스 가중치<br>**손실**: focal_loss: gamma2·학습 label smoothing0.02<br>**최적화**: AdamW·weight decay1e-4·학습률 1e-3→1e-4<br>**후속 재학습**: 학습률 3e-5·label smoothing0.05<br>**중단·체크포인트**: val_loss 조기 중단·최선 가중치·과적합 제어·SWA/TTA 경로 |
| <a id="layout18-table-25-row-4"></a> **관측과 해석** | 블록 크기 512~1의 분류 결과를 비교합니다.<br>원고 보고값과 이 코드의 조건별 저장 결과를 구분합니다. 변환 위치·분할·시드와 실제 결과 파일이 같은지 확인합니다. |
| <a id="layout18-table-25-row-5"></a> **한계** | **변환의 의미**: 블록 재배열·블러 강도만으로 환자 재식별 저항성이나 암호학적 안전성을 보증하지 않습니다.<br>**결과 재사용**: 조건별 데이터·가중치·결과를 만들거나 재사용하므로 입력·출력 폴더와 기존 결과를 구분합니다.<br>**분할**: 이 사본은 oversample_dir 뒤 prepare_split을 호출해 증강 후 train/test를 나눕니다.<br>**평가 방식**: 테스트 의사 라벨 추가 학습 후의 수치는 transductive 평가입니다.<br>테스트 자료를 전혀 이용하지 않은 독립 평가와 구분합니다.<br>**자료 중복**: 증강 후 분할하는 이 사본에서는 같은 원영상에서 파생한 자료가 학습·시험 양쪽에 들어갈 위험을 확인해야 합니다.<br>**예시 그래프**: 실제 결과·학습 이력이 없으면 _dummy_results 또는 _dummy_histories 계열로 예시 값을 만드는 그래프 셀이 있습니다.<br>그래프가 그려졌다는 사실만으로 학습 결과로 인용하지 않습니다.<br>**입력 스케일**: load_image는 float32 변환으로 0~255 입력을 유지합니다.<br>ImageNet 사전 학습과 연결할 때 전처리 가정을 확인합니다. |
| <a id="layout18-table-25-row-6"></a> **자료 연결** | [이 차수 전체 상세](#purpose) · [실행 순서](#usage) · [결과와 해석](#results) · [프로젝트 공통 안내](../../README.md)<br>다른 입력 변환·모델 구성과 원고 보고값은 [공통 프로젝트 안내](../../README.md)에서 해당 자료로 이동합니다. |
| <a id="layout18-table-25-row-7"></a> **읽기 범위** | 이 차수의 [전체 상세](#purpose)와 [파일 구성](#files)을 확인합니다. 다른 차수의 사실은 공통 안내 링크에서 별도로 읽습니다. |


<a id="semantic-lung-feature-level-5"></a>

### LEVEL 5 · 입력 변환·분리 모델·특징 블러의 차이

<a id="layout18-table-26-row-1"></a><a id="layout18-table-26-row-2"></a><a id="layout18-table-26-row-3"></a><a id="layout18-table-26-row-4"></a>

이 차수의 목적·구현·조건·관측과 한계는 [위의 같은 차수 표](#layout18-table-25-row-1)에서 함께 비교합니다. 다른 변환 방식과 자료 차수의 설명은 [프로젝트 공통 안내](../../README.md)에서 해당 문서로 이동합니다.


[동일 수준 프로젝트 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A85.md)

<!-- reading-levels17:end -->

시드로 정한 순열에 따라 입력 블록의 위치를 바꾸며 블록 내부 픽셀 배열은 유지합니다. 영상보다 작지 않은 블록은 원본을 복사합니다.

분야: 의료 영상 실험 코드 › TensorFlow·ResNet50 › 입력 블록 재배열

[목적](#purpose) · [기능](#features) · [입출력](#flow) · [구성](#files) · [준비](#setup) · [사용법](#usage) · [결과](#results) · [제약](#limits) · [변경](#changes)

<a name="purpose"></a>

<a id="-이-단계에서-하는-일"></a>

## 연구 목적

이 단계의 핵심은 입력 블록 재배열입니다. 이 사본은 oversample_dir 뒤 prepare_split을 호출해 증강 후 train/test를 나눕니다. 블록 크기 512~1의 분류 결과를 비교합니다.

<a name="features"></a>

<a id="-주요-기능과-처리-방식"></a>

## 방법과 구현

| 구성 | 실제 역할 |
| --- | --- |
| <a id="layout18-table-27-row-1"></a> 변환 위치 | 시드로 정한 순열에 따라 입력 블록의 위치를 바꾸며 블록 내부 픽셀 배열은 유지합니다.<br>영상보다 작지 않은 블록은 원본을 복사합니다. |
| <a id="layout18-table-27-row-2"></a> 모델 연결 | 일반 ResNet50 분류 모델을 사용합니다. |
| <a id="layout18-table-27-row-3"></a> 분할·증강 | 이 사본은 oversample_dir 뒤 prepare_split을 호출해 증강 후 train/test를 나눕니다. |
| <a id="layout18-table-27-row-4"></a> 입력과 증강 | JPEG 3 채널을 512×512 float32로 읽습니다.<br>학습에서는 좌우·상하 반전, 밝기·대비·잡음을 적용하며 평가 입력과 구분합니다. |
| <a id="layout18-table-27-row-5"></a> 분류 헤드 | GAP와 GMP를 연결하고 Dense512 →BatchNorm·ReLU·Dropout0.35 →Dense256 →BatchNorm·ReLU·Dropout0.25 →softmax로 분류합니다. |
| <a id="layout18-table-27-row-6"></a> 평가·저장 | 조건별 정확도·ROC-AUC·클래스별 Recall·혼동행렬과 모델·그래프 출력을 구분합니다. |
| <a id="layout18-table-27-row-7"></a> 테스트 의사 라벨 | 테스트 예측의 최대 확률이 0.88 이상인 영상을 예측 라벨로 학습 자료에 추가하는 후속 경로가 있습니다. |


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
| <a id="layout18-table-29-row-1"></a> [블록/2차 실험/block_encryption_resnet50_rebuilt_KO.ipynb](../../%EB%B8%94%EB%A1%9D/2%EC%B0%A8%20%EC%8B%A4%ED%97%98/block_encryption_resnet50_rebuilt_KO.ipynb) | 설정·함수·실행 셀 |


<a id="-함수셀로-찾아가기"></a>

### 관련 함수와 셀

관련 함수와 셀을 파일별로 정리했습니다. 실행 전 설정과 호출 순서, 출력 경로를 확인하세요.

| 파일 | 핵심 정의 |
| --- | --- |
| <a id="layout18-table-30-row-1"></a> [블록/2차 실험/block_encryption_resnet50_rebuilt_KO.ipynb](../../%EB%B8%94%EB%A1%9D/2%EC%B0%A8%20%EC%8B%A4%ED%97%98/block_encryption_resnet50_rebuilt_KO.ipynb) | 셀 6: `gpu_status` · `GPUMonitorCallback` · `__init__` · `on_epoch_end`<br>셀 8: `set_reproducible` · `list_class_dirs` · `list_image_files`<br>셀 10: `block_scramble` · `generate_block_dataset`<br>셀 12: `oversample_dir`<br>셀 14: `prepare_split`<br>셀 16: `_deterministic` · `get_paths_labels` · `load_image` · `augment_train` · `mixup_batch` · `cutmix_batch` · `apply_mixup` · `apply_cutmix`<br>셀 18: `focal_loss` · `loss_fn` · `CosineAnnealingWarmRestart` · `__init__` · `on_epoch_begin` · `SWACallback` · `__init__` · `on_epoch_end` |


<a name="setup"></a>

<a id="️-환경과-설정"></a>

## 실행 환경과 설정

| 항목 | 조건·기본값 |
| --- | --- |
| 이미지·배치 | 512×512·batch8 |
| 재현 설정 | seed42·7fold·test 비율 0.10 |
| 학습 설정 | 설정 셀의 단계별 epoch·SWA 시작 40·TTA20 |
| 입력 | 별도 CT 데이터와 클래스 폴더 |
| 변환 조건 | 입력 10 조건 |
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
5. 조건별 JSON과 혼동 행렬·ROC-AUC·Recall을 같은 분모와 클래스 순서로 비교합니다.

<a name="results"></a>

<a id="-결과를-읽는-방법"></a>

## 결과와 해석

블록 크기 512~1의 분류 결과를 비교합니다.

원고 보고값과 이 코드의 조건별 저장 결과를 구분합니다. 변환 위치·분할·시드와 실제 결과 파일이 같은지 확인합니다.

<a name="limits"></a>

<a id="️-알려진-제약과-확인-지점"></a>

## 제약과 확인 사항

| 상황 | 확인할 내용 |
| --- | --- |
| <a id="layout18-table-32-row-1"></a> 변환의 의미 | 블록 재배열·블러 강도만으로 환자 재식별 저항성이나 암호학적 안전성을 보증하지 않습니다. |
| <a id="layout18-table-32-row-2"></a> 결과 재사용 | 조건별 데이터·가중치·결과를 만들거나 재사용하므로 입력·출력 폴더와 기존 결과를 구분합니다. |
| <a id="layout18-table-32-row-3"></a> 분할 | 이 사본은 oversample_dir 뒤 prepare_split을 호출해 증강 후 train/test를 나눕니다. |
| <a id="layout18-table-32-row-4"></a> 평가 방식 | 테스트 의사 라벨 추가 학습 후의 수치는 transductive 평가입니다.<br>테스트 자료를 전혀 이용하지 않은 독립 평가와 구분합니다. |
| <a id="layout18-table-32-row-5"></a> 자료 중복 | 증강 후 분할하는 이 사본에서는 같은 원영상에서 파생한 자료가 학습·시험 양쪽에 들어갈 위험을 확인해야 합니다. |
| <a id="layout18-table-32-row-6"></a> 예시 그래프 | 실제 결과·학습 이력이 없으면 _dummy_results 또는 _dummy_histories 계열로 예시 값을 만드는 그래프 셀이 있습니다.<br>그래프가 그려졌다는 사실만으로 학습 결과로 인용하지 않습니다. |
| <a id="layout18-table-32-row-7"></a> 입력 스케일 | load_image는 float32 변환으로 0~255 입력을 유지합니다.<br>ImageNet 사전 학습과 연결할 때 전처리 가정을 확인합니다. |


<a name="changes"></a>

<a id="-이전-단계와의-변화"></a>

## 직전 단계와 비교

입력 블록 재배열의 구현과 평가 경로를 다루는 단계입니다. 변환 위치·모델 연결·분할 순서는 위 구성과 같으며, 기존 전체 비교에서 설정·함수·주석을 포함한 차이를 읽을 수 있습니다.

[직전 단계 전체 비교·구성](../revision-diffs/experiment-7-%EC%97%B4%EB%9E%8C.md) · [전체 파일 크기·해시](../revision-manifests/experiment-7.json)

<details>
<summary>이 단계의 파일 기록과 전체 해시</summary>

아래 내용는 해당 단계가 기록될 당시의 파일 정보입니다. 현재 첨부는 [프로젝트 자료 안내](../PAPERS.md)에서 확인할 수 있습니다.

| 파일 | 종류 | 바이트 | SHA-256 |
| --- | --- | --- | --- |
| <a id="layout18-table-33-row-1"></a> [블록/2차 실험/block_encryption_resnet50_rebuilt_KO.ipynb](../../%EB%B8%94%EB%A1%9D/2%EC%B0%A8%20%EC%8B%A4%ED%97%98/block_encryption_resnet50_rebuilt_KO.ipynb) | .ipynb | 93336 | `e4526e11284c362e99634a7f3a7cd2ee3e96c79b25a8e1970d57eba31669de89` |
| <a id="layout18-table-33-row-2"></a> [원본자료/블록/2차 실험/all_block_results_resnet50_unified_v1.json](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EB%B8%94%EB%A1%9D/2%EC%B0%A8%20%EC%8B%A4%ED%97%98/all_block_results_resnet50_unified_v1.json) | .json | 5378 | `84e93b7074555e4a421d51a9735431eda423bf83599460a9a68a318da5fe37bb` |
| <a id="layout18-table-33-row-3"></a> [원본자료/블록/2차 실험/block_encryption_resnet50_rebuilt_KO.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EB%B8%94%EB%A1%9D/2%EC%B0%A8%20%EC%8B%A4%ED%97%98/block_encryption_resnet50_rebuilt_KO.ipynb) | .ipynb | 93336 | `e4526e11284c362e99634a7f3a7cd2ee3e96c79b25a8e1970d57eba31669de89` |


</details>

---

[프로젝트](../../README.md) · [전체 차수](../REVISION_INDEX.md) · [자료 폴더](../../%EB%B8%94%EB%A1%9D/2%EC%B0%A8%20%EC%8B%A4%ED%97%98)


<a id="layout18-table-12-row-1"></a><a id="layout18-table-12-row-2"></a><a id="layout18-table-12-row-3"></a><a id="layout18-table-12-row-4"></a><a id="layout18-table-12-row-5"></a><a id="layout18-table-12-row-6"></a><a id="layout18-table-12-row-7"></a><a id="layout18-table-15-row-1"></a><a id="layout18-table-15-row-2"></a><a id="layout18-table-15-row-3"></a><a id="layout18-table-15-row-4"></a><a id="layout18-table-15-row-5"></a><a id="layout18-table-15-row-6"></a><a id="layout18-table-15-row-7"></a><a id="layout18-table-18-row-1"></a><a id="layout18-table-18-row-2"></a><a id="layout18-table-18-row-3"></a><a id="layout18-table-18-row-4"></a><a id="layout18-table-18-row-5"></a><a id="layout18-table-18-row-6"></a><a id="layout18-table-18-row-7"></a><a id="layout18-table-21-row-1"></a><a id="layout18-table-21-row-2"></a><a id="layout18-table-21-row-3"></a><a id="layout18-table-21-row-4"></a><a id="layout18-table-21-row-5"></a><a id="layout18-table-21-row-6"></a><a id="layout18-table-21-row-7"></a><a id="layout18-table-24-row-1"></a><a id="layout18-table-24-row-2"></a><a id="layout18-table-24-row-3"></a><a id="layout18-table-24-row-4"></a><a id="layout18-table-24-row-5"></a><a id="layout18-table-24-row-6"></a><a id="layout18-table-24-row-7"></a><a id="layout18-table-3-row-1"></a><a id="layout18-table-3-row-2"></a><a id="layout18-table-3-row-3"></a><a id="layout18-table-3-row-4"></a><a id="layout18-table-3-row-5"></a><a id="layout18-table-3-row-6"></a><a id="layout18-table-3-row-7"></a><a id="layout18-table-6-row-1"></a><a id="layout18-table-6-row-2"></a><a id="layout18-table-6-row-3"></a><a id="layout18-table-6-row-4"></a><a id="layout18-table-6-row-5"></a><a id="layout18-table-6-row-6"></a><a id="layout18-table-6-row-7"></a><a id="layout18-table-9-row-1"></a><a id="layout18-table-9-row-2"></a><a id="layout18-table-9-row-3"></a><a id="layout18-table-9-row-4"></a><a id="layout18-table-9-row-5"></a><a id="layout18-table-9-row-6"></a><a id="layout18-table-9-row-7"></a>

</details>


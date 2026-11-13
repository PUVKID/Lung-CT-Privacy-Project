<a id="️-블러-2차--입력-영상과-resnet50"></a>

# 블러 2차 · 입력 영상과 ResNet50

<!-- reading-levels17:start -->
**읽기 수준 선택** · [LEVEL 1 - Beginner](#reading-level-1) · [LEVEL 2 - Explorer](#reading-level-2) · [LEVEL 3 - Practitioner](#reading-level-3) · [LEVEL 4 - Advanced](#reading-level-4) · [LEVEL 5 - Expert](#reading-level-5)

<a id="reading-level-1"></a>

## LEVEL 1 - Beginner

<!-- semantic-revision17:level-1:start -->

<a id="semantic-lung-training-level-1"></a>

### LEVEL 1 · 노트북 학습·평가의 연결과 실패 조건

사진을 새로 만들어 학습 수를 늘리는 것이 증강입니다. **원본 사진을 먼저 나누는 것**과 증강한 사진을 나누는 것은 다릅니다. 같은 원본에서 만든 사진이 양쪽에 들어가면 점수가 좋게 보일 수 있습니다. 시험 사진의 예측을 다시 학습에 넣는 의사라벨 경로도 있어, 정답 확인 자료를 전혀 보지 않은 독립 시험과 구분합니다. 아래 숫자는 노트북별 설정이며 모든 파일의 동일한 결과가 아닙니다.

<a id="layout18-table-1-row-1"></a>

**입력·헤드**

**조건·자료**

입력·헤드

**의미와 확인 방법**

JPEG3채널·512×512·float32의0~255 입력입니다. GAP와GMP를 연결하고 Dense512→BatchNorm·ReLU·Dropout0.35→Dense256→BatchNorm·ReLU·Dropout0.25→softmax로 분류하는 변형이 있습니다.

<a id="layout18-table-1-row-2"></a>

**학습·TTA**

**조건·자료**

학습·TTA

**의미와 확인 방법**

seed42·test0.10·StratifiedKFold7·shuffle·클래스가중치·batch8이며 변형별batch4도 있습니다. EPOCHS_S1=80·EPOCHS_S2=200, 분리모델fit은 최대280epoch, SWA시작40·TTA20입니다.

<a id="layout18-table-1-row-3"></a>

**증강·손실**

**조건·자료**

증강·손실

**의미와 확인 방법**

학습 좌우/상하반전·밝기최대0.25×255·대비0.75~1.25·Gaussian잡음표준편차5, TTA좌우반전·밝기최대0.15×255·대비0.85~1.15입니다. focal gamma2·학습label smoothing0.02·AdamW lr1e-4·weight decay1e-4를 사용하며 후속재학습은lr3e-5·smoothing0.05입니다.

<a id="layout18-table-1-row-4"></a>

**시험 재사용**

**조건·자료**

시험 재사용

**의미와 확인 방법**

시험 예측 확신도0.88이상 영상이10장이상이면 예측라벨로15epochs추가학습한 뒤 같은 시험을 다시 평가하는 경로가 있습니다. 추가모델이7fold모델과 앙상블되며 일부는 전체증강학습을 이용해fold검증도 다시 포함합니다.

<a id="layout18-table-1-row-5"></a>

**누수·코드차이**

**조건·자료**

누수·코드차이

**의미와 확인 방법**

원본test선분리와 증강후fold분리는 다릅니다. 일부이전셀은 증강후test도 분리합니다. 논문의Mixup Beta설명과 코드uniform샘플링, preprocess_input누락, 중첩모델미세조정, 최적체크포인트를종료/SWA가중치로다시저장하는 흐름을 확인합니다.

<a id="layout18-table-1-row-6"></a>

**실행 준비**

**조건·자료**

실행 준비

**의미와 확인 방법**

Python·TensorFlow/Keras·CUDA·드라이버·AdamW API·NumPy·Pillow·scikit-learn·Matplotlib·Seaborn·추가import를 확인합니다. BASE_TRAIN과 실제지원 BB_OUTPUT_ROOT/SB_OUTPUT_ROOT, 입력·결과폴더·디스크·캐시를 구분합니다. 의존성잠금으로 재현을 보증하지 않습니다.

<a id="layout18-table-1-row-7"></a>

**실측과 예시**

**조건·자료**

실측과 예시

**의미와 확인 방법**

_dummy_results·_dummy_histories·GPU예시로그·하드코딩히트맵은 실측이 아닙니다. 결과JSON·분할·시드·가중치·실제로그를 함께 확인합니다.


<a id="semantic-lung-feature-level-1"></a>

### LEVEL 1 · 입력 변환·분리 모델·특징 블러의 차이

입력 변환은 사진 자체를 바꾸고 특징 블러는 모델이 사진에서 찾아낸 선·무늬의 반응을 바꿉니다. **바꾸는 위치가 다릅니다.** edge와 cloud라는 이름도 두 컴퓨터에서 통신했다는 뜻은 아닙니다. 큰 흐림 조건 여러 개가 같은 결과를 재사용하면 각각 새로 학습한 실험으로 세지 않습니다.

<a id="layout18-table-2-row-1"></a>

**입력 변환**

**조건·자료**

입력 변환

**의미와 확인 방법**

블러는PIL GaussianBlur이며σ0은복사합니다. 블록은seed순열로위치를바꾸고내부픽셀을유지하며영상보다작지않은블록은복사합니다. 조합은Block10×Blur10=100이며Block뒤Blur입니다.

<a id="layout18-table-2-row-2"></a>

**분리 경계**

**조건·자료**

분리 경계

**의미와 확인 방법**

edge/cloud는ResNet50 pool1_pool경계의모듈을동일TensorFlow프로세스에서연결한코드입니다. 실제원격전송구현이아닙니다.

<a id="layout18-table-2-row-3"></a>

**특징 변환**

**조건·자료**

특징 변환

**의미와 확인 방법**

Stage1은edge→FeatureGaussianBlur→cloud입니다. 채널별고정Gaussian커널을depthwise_conv2d로적용합니다. σ32·64·128·256은전역평균분기이며REUSE_COLLAPSED_RESULTS기본경로는σ32결과를64·128·256에재사용합니다.

<a id="layout18-table-2-row-4"></a>

**별도 분석**

**조건·자료**

별도 분석

**의미와 확인 방법**

채널평균특징맵을각각정규화한단일SSIM점수·cosine·클래스분리도와선택decoder의PSNR/SSIM을봅니다. decoder는AdamW lr5e-4·weight decay1e-5·MAE이며Conv2D import/정의확인이필요합니다.


<!-- semantic-revision17:level-1:end -->

[이 수준의 프로젝트 전체 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A81.md) · [같은 수준 프로필](https://github.com/PUVKID/PUVKID/blob/main/docs/읽기안내/레벨1.md)

### LEVEL 1 · 목적과 대상

**이 차수의 목적과 실제 구성**

입력 영상에 PIL GaussianBlur를 적용하는 10조건 실험입니다. σ0은 원본 배열을 복사합니다.

<a id="layout18-table-3-row-1"></a>

**변환 위치**

**구성**

변환 위치

**실제 역할**

입력 영상에 PIL GaussianBlur를 적용하는 10조건 실험입니다. σ0은 원본 배열을 복사합니다.

<a id="layout18-table-3-row-2"></a>

**모델 연결**

**구성**

모델 연결

**실제 역할**

일반 ResNet50 분류 모델을 사용합니다.

<a id="layout18-table-3-row-3"></a>

**분할·증강**

**구성**

분할·증강

**실제 역할**

원본 train/test를 먼저 나누고 학습 쪽을 증강합니다.

<a id="layout18-table-3-row-4"></a>

**입력과 증강**

**구성**

입력과 증강

**실제 역할**

JPEG 3채널을 512×512 float32로 읽습니다. 학습에서는 좌우·상하 반전, 밝기·대비·잡음을 적용하며 평가 입력과 구분합니다.

<a id="layout18-table-3-row-5"></a>

**분류 헤드**

**구성**

분류 헤드

**실제 역할**

GAP와 GMP를 연결하고 Dense512→BatchNorm·ReLU·Dropout0.35→Dense256→BatchNorm·ReLU·Dropout0.25→softmax로 분류합니다.

<a id="layout18-table-3-row-6"></a>

**평가·저장**

**구성**

평가·저장

**실제 역할**

조건별 정확도·ROC-AUC·클래스별 Recall·혼동행렬과 모델·그래프 출력을 구분합니다.

<a id="layout18-table-3-row-7"></a>

**테스트 의사 라벨**

**구성**

테스트 의사 라벨

**실제 역할**

테스트 예측의 최대 확률이 0.88 이상인 영상을 예측 라벨로 학습 자료에 추가하는 후속 경로가 있습니다.


CT 사진을 흐리게 하거나 블록으로 재배열했을 때 분류 결과와 영상 유사도가 어떻게 달라지는지 살펴봅니다. 입력 사진을 바꾸는 연구와 모델 내부의 첫 합성곱 특징을 흐리는 실험이 함께 있습니다. **논문 연구 번호·공개 코드 차수·실제 학습 차수는 다릅니다.**

### LEVEL 1 · 달라진 내용과 차수 관계

입력 블러의 구현과 평가 경로를 다루는 단계입니다. 변환 위치·모델 연결·분할 순서는 위 구성과 같으며, 기존 전체 비교에서 설정·함수·주석을 포함한 차이를 읽을 수 있습니다.

[직전 단계 전체 비교·구성](../revision-diffs/experiment-6.diff) · [전체 파일 크기·해시](../revision-manifests/experiment-6.json)

사진의 모양이 바뀌었어도 분류기가 정답을 잘 맞추는지, 얼마나 비슷한 정보를 남기는지 따로 봅니다. OK는 양성+정상, NG는 악성입니다. 사진 수·독립 환자 수·반복 학습 표본 수를 섞지 않습니다.

### LEVEL 1 · 입력과 실행 조건

**입력**

CT 원본과 클래스

**처리**

분할·학습 자료 준비

**출력**

학습·검증·시험 입력


**입력**

입력 또는 특징

**처리**

설정한 변환과 모델 학습

**출력**

조건별 예측


**입력**

예측·특징·자원 기록

**처리**

분류 지표·그림·모델 저장

**출력**

조건 비교 결과



**항목**

이미지·배치

**조건·기본값**

512×512·batch8


**항목**

재현 설정

**조건·기본값**

seed42·7fold·test 비율 0.10


**항목**

학습 설정

**조건·기본값**

설정 셀의 단계별 epoch·SWA 시작 40·TTA20


**항목**

입력

**조건·기본값**

별도 CT 데이터와 클래스 폴더


**항목**

변환 조건

**조건·기본값**

입력 10조건


**항목**

최대 epoch

**조건·기본값**

EPOCHS_S1=80·EPOCHS_S2=200


**항목**

학습 증강

**조건·기본값**

밝기 최대 0.25×255·대비 0.75~1.25·Gaussian 잡음 표준편차 5


**항목**

TTA 증강

**조건·기본값**

좌우 반전·밝기 최대 0.15×255·대비 0.85~1.15


**항목**

fold

**조건·기본값**

StratifiedKFold·shuffle·seed42·클래스 가중치


**항목**

손실

**조건·기본값**

focal_loss: gamma2·학습 label smoothing0.02


**항목**

최적화

**조건·기본값**

AdamW·weight decay1e-4·학습률 1e-3→1e-4


**항목**

후속 재학습

**조건·기본값**

학습률 3e-5·label smoothing0.05


**항목**

중단·체크포인트

**조건·기본값**

val_loss 조기 중단·최선 가중치·과적합 제어·SWA/TTA 경로



입력 사진에 블러·블록을 적용하는 경로와 모델이 뽑은 특징에 블러를 적용하는 경로를 나눕니다. 특징은 사진에서 찾은 선·무늬의 반응입니다. 그 색이 병변 위치나 악성 확률을 뜻하지 않습니다.

### LEVEL 1 · 처리 절차

1. 설정 셀에서 입력·작업·결과 경로와 변환 조건을 확인합니다.
2. 분할·증강 함수의 호출 순서와 시험 자료가 분리되는 지점을 읽습니다.
3. GPU·TensorFlow·학습 자료를 준비하고 설치·모니터·학습·출력 셀을 구분해 순서대로 읽습니다.
4. 기존 결과의 재사용 조건을 확인한 뒤 필요한 조건을 선택합니다.
5. 조건별 JSON과 혼동행렬·ROC-AUC·Recall을 같은 분모와 클래스 순서로 비교합니다.

전체 차수 표에서 읽을 연구를 고릅니다. 노트북을 여는 것과 새 학습 시작은 다릅니다. 대시보드에서 같은 강도의 사진·곡선·시험 수치를 함께 읽되 미완료 조건은 미측정으로 남깁니다.

### LEVEL 1 · 결과를 확인하는 방법

입력 σ0~256에 따른 분류 결과를 읽습니다.

원고 보고값과 이 코드의 조건별 저장 결과를 구분합니다. 변환 위치·분할·시드와 실제 결과 파일이 같은지 확인합니다.

연구 1의 원고 보고 정확도는 원본 92.5%, sigma32 블러 53.3%, Block32 재배열 79.2%입니다. 이는 당시 논문의 값이며 현재 Conv1 예비실험의 결과로 바꾸지 않습니다.

### LEVEL 1 · 주의할 범위

<a id="layout18-table-6-row-1"></a>

**변환의 의미**

**상황**

변환의 의미

**확인할 내용**

블록 재배열·블러 강도만으로 환자 재식별 저항성이나 암호학적 안전성을 보증하지 않습니다.

<a id="layout18-table-6-row-2"></a>

**결과 재사용**

**상황**

결과 재사용

**확인할 내용**

조건별 데이터·가중치·결과를 만들거나 재사용하므로 입력·출력 폴더와 기존 결과를 구분합니다.

<a id="layout18-table-6-row-3"></a>

**분할**

**상황**

분할

**확인할 내용**

원본 train/test를 먼저 나누고 학습 쪽을 증강합니다.

<a id="layout18-table-6-row-4"></a>

**평가 방식**

**상황**

평가 방식

**확인할 내용**

테스트 의사 라벨 추가 학습 후의 수치는 transductive 평가입니다. 테스트 자료를 전혀 이용하지 않은 독립 평가와 구분합니다.

<a id="layout18-table-6-row-5"></a>

**예시 그래프**

**상황**

예시 그래프

**확인할 내용**

실제 결과·학습 이력이 없으면 _dummy_results 또는 _dummy_histories 계열로 예시 값을 만드는 그래프 셀이 있습니다. 그래프가 그려졌다는 사실만으로 학습 결과로 인용하지 않습니다.

<a id="layout18-table-6-row-6"></a>

**입력 스케일**

**상황**

입력 스케일

**확인할 내용**

load_image는 float32 변환으로 0~255 입력을 유지합니다. ImageNet 사전학습과 연결할 때 전처리 가정을 확인합니다.


환자 ID가 없어 같은 사람의 다른 사진이 섞였는지 모두 확인할 수 없습니다. 높은 정확도가 임상 성능이나 프라이버시 효과를 보장하지 않습니다. **반복 표본 5,000개를 독립 환자 5,000명으로 세지 않습니다.**

[표·코드·실행 설정·파일 전체 비교를 포함한 공통 상세](#reading-level-5)

<a id="reading-level-2"></a>

## LEVEL 2 - Explorer

<!-- semantic-revision17:level-2:start -->

<a id="semantic-lung-training-level-2"></a>

### LEVEL 2 · 노트북 학습·평가의 연결과 실패 조건

학습 증강→분류기→fold모델의 예측 결합→TTA→선택적 의사라벨 재학습의 관계를 봅니다. SWA는 학습 중 여러 가중치를 평균내는 경로이고, TTA는 평가 입력을 바꾸는 경로입니다. 의사라벨은 예측을 임시 정답으로 쓰므로 같은 시험을 다시 평가하면 평가 절차의 의미가 달라집니다.

<a id="layout18-table-7-row-1"></a>

**입력·헤드**

**조건·자료**

입력·헤드

**의미와 확인 방법**

JPEG3채널·512×512·float32의0~255 입력입니다. GAP와GMP를 연결하고 Dense512→BatchNorm·ReLU·Dropout0.35→Dense256→BatchNorm·ReLU·Dropout0.25→softmax로 분류하는 변형이 있습니다.

<a id="layout18-table-7-row-2"></a>

**학습·TTA**

**조건·자료**

학습·TTA

**의미와 확인 방법**

seed42·test0.10·StratifiedKFold7·shuffle·클래스가중치·batch8이며 변형별batch4도 있습니다. EPOCHS_S1=80·EPOCHS_S2=200, 분리모델fit은 최대280epoch, SWA시작40·TTA20입니다.

<a id="layout18-table-7-row-3"></a>

**증강·손실**

**조건·자료**

증강·손실

**의미와 확인 방법**

학습 좌우/상하반전·밝기최대0.25×255·대비0.75~1.25·Gaussian잡음표준편차5, TTA좌우반전·밝기최대0.15×255·대비0.85~1.15입니다. focal gamma2·학습label smoothing0.02·AdamW lr1e-4·weight decay1e-4를 사용하며 후속재학습은lr3e-5·smoothing0.05입니다.

<a id="layout18-table-7-row-4"></a>

**시험 재사용**

**조건·자료**

시험 재사용

**의미와 확인 방법**

시험 예측 확신도0.88이상 영상이10장이상이면 예측라벨로15epochs추가학습한 뒤 같은 시험을 다시 평가하는 경로가 있습니다. 추가모델이7fold모델과 앙상블되며 일부는 전체증강학습을 이용해fold검증도 다시 포함합니다.

<a id="layout18-table-7-row-5"></a>

**누수·코드차이**

**조건·자료**

누수·코드차이

**의미와 확인 방법**

원본test선분리와 증강후fold분리는 다릅니다. 일부이전셀은 증강후test도 분리합니다. 논문의Mixup Beta설명과 코드uniform샘플링, preprocess_input누락, 중첩모델미세조정, 최적체크포인트를종료/SWA가중치로다시저장하는 흐름을 확인합니다.

<a id="layout18-table-7-row-6"></a>

**실행 준비**

**조건·자료**

실행 준비

**의미와 확인 방법**

Python·TensorFlow/Keras·CUDA·드라이버·AdamW API·NumPy·Pillow·scikit-learn·Matplotlib·Seaborn·추가import를 확인합니다. BASE_TRAIN과 실제지원 BB_OUTPUT_ROOT/SB_OUTPUT_ROOT, 입력·결과폴더·디스크·캐시를 구분합니다. 의존성잠금으로 재현을 보증하지 않습니다.

<a id="layout18-table-7-row-7"></a>

**실측과 예시**

**조건·자료**

실측과 예시

**의미와 확인 방법**

_dummy_results·_dummy_histories·GPU예시로그·하드코딩히트맵은 실측이 아닙니다. 결과JSON·분할·시드·가중치·실제로그를 함께 확인합니다.


<a id="semantic-lung-feature-level-2"></a>

### LEVEL 2 · 입력 변환·분리 모델·특징 블러의 차이

원본 사진→입력 변환→edge→cloud의 경로와 원본 사진→edge→특징 블러→cloud의 경로를 비교합니다. 채널은 서로 다른 특징 반응층이고 depthwise 연산은 각 채널을 따로 흐립니다. decoder는 특징에서 사진을 다시 만드는 별도 모형이므로 분류 점수와 복원 점수를 구분합니다.

<a id="layout18-table-8-row-1"></a>

**입력 변환**

**조건·자료**

입력 변환

**의미와 확인 방법**

블러는PIL GaussianBlur이며σ0은복사합니다. 블록은seed순열로위치를바꾸고내부픽셀을유지하며영상보다작지않은블록은복사합니다. 조합은Block10×Blur10=100이며Block뒤Blur입니다.

<a id="layout18-table-8-row-2"></a>

**분리 경계**

**조건·자료**

분리 경계

**의미와 확인 방법**

edge/cloud는ResNet50 pool1_pool경계의모듈을동일TensorFlow프로세스에서연결한코드입니다. 실제원격전송구현이아닙니다.

<a id="layout18-table-8-row-3"></a>

**특징 변환**

**조건·자료**

특징 변환

**의미와 확인 방법**

Stage1은edge→FeatureGaussianBlur→cloud입니다. 채널별고정Gaussian커널을depthwise_conv2d로적용합니다. σ32·64·128·256은전역평균분기이며REUSE_COLLAPSED_RESULTS기본경로는σ32결과를64·128·256에재사용합니다.

<a id="layout18-table-8-row-4"></a>

**별도 분석**

**조건·자료**

별도 분석

**의미와 확인 방법**

채널평균특징맵을각각정규화한단일SSIM점수·cosine·클래스분리도와선택decoder의PSNR/SSIM을봅니다. decoder는AdamW lr5e-4·weight decay1e-5·MAE이며Conv2D import/정의확인이필요합니다.


<!-- semantic-revision17:level-2:end -->

[이 수준의 프로젝트 전체 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A82.md) · [같은 수준 프로필](https://github.com/PUVKID/PUVKID/blob/main/docs/읽기안내/레벨2.md)

### LEVEL 2 · 목적과 대상

**이 차수의 목적과 실제 구성**

입력 영상에 PIL GaussianBlur를 적용하는 10조건 실험입니다. σ0은 원본 배열을 복사합니다.

<a id="layout18-table-9-row-1"></a>

**변환 위치**

**구성**

변환 위치

**실제 역할**

입력 영상에 PIL GaussianBlur를 적용하는 10조건 실험입니다. σ0은 원본 배열을 복사합니다.

<a id="layout18-table-9-row-2"></a>

**모델 연결**

**구성**

모델 연결

**실제 역할**

일반 ResNet50 분류 모델을 사용합니다.

<a id="layout18-table-9-row-3"></a>

**분할·증강**

**구성**

분할·증강

**실제 역할**

원본 train/test를 먼저 나누고 학습 쪽을 증강합니다.

<a id="layout18-table-9-row-4"></a>

**입력과 증강**

**구성**

입력과 증강

**실제 역할**

JPEG 3채널을 512×512 float32로 읽습니다. 학습에서는 좌우·상하 반전, 밝기·대비·잡음을 적용하며 평가 입력과 구분합니다.

<a id="layout18-table-9-row-5"></a>

**분류 헤드**

**구성**

분류 헤드

**실제 역할**

GAP와 GMP를 연결하고 Dense512→BatchNorm·ReLU·Dropout0.35→Dense256→BatchNorm·ReLU·Dropout0.25→softmax로 분류합니다.

<a id="layout18-table-9-row-6"></a>

**평가·저장**

**구성**

평가·저장

**실제 역할**

조건별 정확도·ROC-AUC·클래스별 Recall·혼동행렬과 모델·그래프 출력을 구분합니다.

<a id="layout18-table-9-row-7"></a>

**테스트 의사 라벨**

**구성**

테스트 의사 라벨

**실제 역할**

테스트 예측의 최대 확률이 0.88 이상인 영상을 예측 라벨로 학습 자료에 추가하는 후속 경로가 있습니다.


입력 변형 연구 1·2, 특징 블러 Stage 1, Conv1 OK/NG 예비실험을 구분합니다. 블러는 무늬를 부드럽게 하고 블록 재배열은 위치를 섞습니다. 분류 정확도와 유사도 기반 Privacy Score는 서로 다른 양을 측정합니다.

### LEVEL 2 · 달라진 내용과 차수 관계

입력 블러의 구현과 평가 경로를 다루는 단계입니다. 변환 위치·모델 연결·분할 순서는 위 구성과 같으며, 기존 전체 비교에서 설정·함수·주석을 포함한 차이를 읽을 수 있습니다.

[직전 단계 전체 비교·구성](../revision-diffs/experiment-6.diff) · [전체 파일 크기·해시](../revision-manifests/experiment-6.json)

이전 연구는 정상·양성·악성 3분류, Conv1은 OK/NG 이진 분류입니다. 원본 1,097장은 양성 120·정상 416·악성 561장입니다. 클래스당 매 epoch 5,000표본은 반복·온라인 증강이며 독립 영상 5,000장이 아닙니다.

### LEVEL 2 · 입력과 실행 조건

**입력**

CT 원본과 클래스

**처리**

분할·학습 자료 준비

**출력**

학습·검증·시험 입력


**입력**

입력 또는 특징

**처리**

설정한 변환과 모델 학습

**출력**

조건별 예측


**입력**

예측·특징·자원 기록

**처리**

분류 지표·그림·모델 저장

**출력**

조건 비교 결과



**항목**

이미지·배치

**조건·기본값**

512×512·batch8


**항목**

재현 설정

**조건·기본값**

seed42·7fold·test 비율 0.10


**항목**

학습 설정

**조건·기본값**

설정 셀의 단계별 epoch·SWA 시작 40·TTA20


**항목**

입력

**조건·기본값**

별도 CT 데이터와 클래스 폴더


**항목**

변환 조건

**조건·기본값**

입력 10조건


**항목**

최대 epoch

**조건·기본값**

EPOCHS_S1=80·EPOCHS_S2=200


**항목**

학습 증강

**조건·기본값**

밝기 최대 0.25×255·대비 0.75~1.25·Gaussian 잡음 표준편차 5


**항목**

TTA 증강

**조건·기본값**

좌우 반전·밝기 최대 0.15×255·대비 0.85~1.15


**항목**

fold

**조건·기본값**

StratifiedKFold·shuffle·seed42·클래스 가중치


**항목**

손실

**조건·기본값**

focal_loss: gamma2·학습 label smoothing0.02


**항목**

최적화

**조건·기본값**

AdamW·weight decay1e-4·학습률 1e-3→1e-4


**항목**

후속 재학습

**조건·기본값**

학습률 3e-5·label smoothing0.05


**항목**

중단·체크포인트

**조건·기본값**

val_loss 조기 중단·최선 가중치·과적합 제어·SWA/TTA 경로



연구 1은 512×512 입력에 두 변환을 각각 적용해 정확도·ROC-AUC·혼동행렬을 봅니다. 연구 2는 Blur→Block·Block→Blur 조합과 입력 MS-SSIM을 비교합니다. Conv1은 첫 합성곱 특징을 바꾼 뒤 분류합니다.

### LEVEL 2 · 처리 절차

1. 설정 셀에서 입력·작업·결과 경로와 변환 조건을 확인합니다.
2. 분할·증강 함수의 호출 순서와 시험 자료가 분리되는 지점을 읽습니다.
3. GPU·TensorFlow·학습 자료를 준비하고 설치·모니터·학습·출력 셀을 구분해 순서대로 읽습니다.
4. 기존 결과의 재사용 조건을 확인한 뒤 필요한 조건을 선택합니다.
5. 조건별 JSON과 혼동행렬·ROC-AUC·Recall을 같은 분모와 클래스 순서로 비교합니다.

대표 CT 3범주와 6단계에서 조건별 PNG 18개를 만듭니다. 원본 포함 10조건이 끝나면 180개입니다. 평균·최댓값·개별 8채널의 총 10패널은 특징 반응을 보여 줍니다.

### LEVEL 2 · 결과를 확인하는 방법

입력 σ0~256에 따른 분류 결과를 읽습니다.

원고 보고값과 이 코드의 조건별 저장 결과를 구분합니다. 변환 위치·분할·시드와 실제 결과 파일이 같은지 확인합니다.

연구 2는 원본 98.17%, Block256+sigma0 정확도 98.17%·Privacy Score 49.65점을 보고합니다. 유사도 점수는 복원 공격 성공률이 아닙니다. 연구 1과 모델·조건이 달라 차이의 원인을 하나로 확정하지 않습니다.

### LEVEL 2 · 주의할 범위

<a id="layout18-table-12-row-1"></a>

**변환의 의미**

**상황**

변환의 의미

**확인할 내용**

블록 재배열·블러 강도만으로 환자 재식별 저항성이나 암호학적 안전성을 보증하지 않습니다.

<a id="layout18-table-12-row-2"></a>

**결과 재사용**

**상황**

결과 재사용

**확인할 내용**

조건별 데이터·가중치·결과를 만들거나 재사용하므로 입력·출력 폴더와 기존 결과를 구분합니다.

<a id="layout18-table-12-row-3"></a>

**분할**

**상황**

분할

**확인할 내용**

원본 train/test를 먼저 나누고 학습 쪽을 증강합니다.

<a id="layout18-table-12-row-4"></a>

**평가 방식**

**상황**

평가 방식

**확인할 내용**

테스트 의사 라벨 추가 학습 후의 수치는 transductive 평가입니다. 테스트 자료를 전혀 이용하지 않은 독립 평가와 구분합니다.

<a id="layout18-table-12-row-5"></a>

**예시 그래프**

**상황**

예시 그래프

**확인할 내용**

실제 결과·학습 이력이 없으면 _dummy_results 또는 _dummy_histories 계열로 예시 값을 만드는 그래프 셀이 있습니다. 그래프가 그려졌다는 사실만으로 학습 결과로 인용하지 않습니다.

<a id="layout18-table-12-row-6"></a>

**입력 스케일**

**상황**

입력 스케일

**확인할 내용**

load_image는 float32 변환으로 0~255 입력을 유지합니다. ImageNet 사전학습과 연결할 때 전처리 가정을 확인합니다.


영상 단위 예비실험의 한계, 조건별 학습·결과 재사용, 입력과 특징의 다른 점수 정의를 함께 읽습니다. 새 종료 정책 실험의 준비와 완료도 구분합니다.

[표·코드·실행 설정·파일 전체 비교를 포함한 공통 상세](#reading-level-5)

<a id="reading-level-3"></a>

## LEVEL 3 - Practitioner

<!-- semantic-revision17:level-3:start -->

<a id="semantic-lung-training-level-3"></a>

### LEVEL 3 · 노트북 학습·평가의 연결과 실패 조건

선택한 노트북의 설정·import·문법과 실제 입력 폴더를 먼저 확인하고 설치·모니터·학습·출력 셀을 구분하세요. 원본 분리·증강·fold·시험 재사용의 호출 순서와 체크포인트 저장을 추적한 뒤 필요한 조건만 준비합니다. 그래프만 먼저 열었다면 결과 JSON과 실행 로그가 실제로 있는지 확인하며, 경로 변수는 해당 파일이 읽는 이름만 사용합니다.

<a id="layout18-table-13-row-1"></a>

**입력·헤드**

**조건·자료**

입력·헤드

**의미와 확인 방법**

JPEG3채널·512×512·float32의0~255 입력입니다. GAP와GMP를 연결하고 Dense512→BatchNorm·ReLU·Dropout0.35→Dense256→BatchNorm·ReLU·Dropout0.25→softmax로 분류하는 변형이 있습니다.

<a id="layout18-table-13-row-2"></a>

**학습·TTA**

**조건·자료**

학습·TTA

**의미와 확인 방법**

seed42·test0.10·StratifiedKFold7·shuffle·클래스가중치·batch8이며 변형별batch4도 있습니다. EPOCHS_S1=80·EPOCHS_S2=200, 분리모델fit은 최대280epoch, SWA시작40·TTA20입니다.

<a id="layout18-table-13-row-3"></a>

**증강·손실**

**조건·자료**

증강·손실

**의미와 확인 방법**

학습 좌우/상하반전·밝기최대0.25×255·대비0.75~1.25·Gaussian잡음표준편차5, TTA좌우반전·밝기최대0.15×255·대비0.85~1.15입니다. focal gamma2·학습label smoothing0.02·AdamW lr1e-4·weight decay1e-4를 사용하며 후속재학습은lr3e-5·smoothing0.05입니다.

<a id="layout18-table-13-row-4"></a>

**시험 재사용**

**조건·자료**

시험 재사용

**의미와 확인 방법**

시험 예측 확신도0.88이상 영상이10장이상이면 예측라벨로15epochs추가학습한 뒤 같은 시험을 다시 평가하는 경로가 있습니다. 추가모델이7fold모델과 앙상블되며 일부는 전체증강학습을 이용해fold검증도 다시 포함합니다.

<a id="layout18-table-13-row-5"></a>

**누수·코드차이**

**조건·자료**

누수·코드차이

**의미와 확인 방법**

원본test선분리와 증강후fold분리는 다릅니다. 일부이전셀은 증강후test도 분리합니다. 논문의Mixup Beta설명과 코드uniform샘플링, preprocess_input누락, 중첩모델미세조정, 최적체크포인트를종료/SWA가중치로다시저장하는 흐름을 확인합니다.

<a id="layout18-table-13-row-6"></a>

**실행 준비**

**조건·자료**

실행 준비

**의미와 확인 방법**

Python·TensorFlow/Keras·CUDA·드라이버·AdamW API·NumPy·Pillow·scikit-learn·Matplotlib·Seaborn·추가import를 확인합니다. BASE_TRAIN과 실제지원 BB_OUTPUT_ROOT/SB_OUTPUT_ROOT, 입력·결과폴더·디스크·캐시를 구분합니다. 의존성잠금으로 재현을 보증하지 않습니다.

<a id="layout18-table-13-row-7"></a>

**실측과 예시**

**조건·자료**

실측과 예시

**의미와 확인 방법**

_dummy_results·_dummy_histories·GPU예시로그·하드코딩히트맵은 실측이 아닙니다. 결과JSON·분할·시드·가중치·실제로그를 함께 확인합니다.


<a id="semantic-lung-feature-level-3"></a>

### LEVEL 3 · 입력 변환·분리 모델·특징 블러의 차이

노트북이 입력과 특징 중 어느 쪽을 변환하는지 확인한 뒤 조건 목록·분리 경계·재사용 옵션을 읽으세요. 복원 분기를 실행하려면 Conv2D 등의 의존성과 원본/특징의 대응을 먼저 준비합니다. 같은 분기 결과를 조건별 독립 학습값으로 보고하지 않고 입력 MS-SSIM과 정규화 특징 SSIM을 따로 기록합니다.

<a id="layout18-table-14-row-1"></a>

**입력 변환**

**조건·자료**

입력 변환

**의미와 확인 방법**

블러는PIL GaussianBlur이며σ0은복사합니다. 블록은seed순열로위치를바꾸고내부픽셀을유지하며영상보다작지않은블록은복사합니다. 조합은Block10×Blur10=100이며Block뒤Blur입니다.

<a id="layout18-table-14-row-2"></a>

**분리 경계**

**조건·자료**

분리 경계

**의미와 확인 방법**

edge/cloud는ResNet50 pool1_pool경계의모듈을동일TensorFlow프로세스에서연결한코드입니다. 실제원격전송구현이아닙니다.

<a id="layout18-table-14-row-3"></a>

**특징 변환**

**조건·자료**

특징 변환

**의미와 확인 방법**

Stage1은edge→FeatureGaussianBlur→cloud입니다. 채널별고정Gaussian커널을depthwise_conv2d로적용합니다. σ32·64·128·256은전역평균분기이며REUSE_COLLAPSED_RESULTS기본경로는σ32결과를64·128·256에재사용합니다.

<a id="layout18-table-14-row-4"></a>

**별도 분석**

**조건·자료**

별도 분석

**의미와 확인 방법**

채널평균특징맵을각각정규화한단일SSIM점수·cosine·클래스분리도와선택decoder의PSNR/SSIM을봅니다. decoder는AdamW lr5e-4·weight decay1e-5·MAE이며Conv2D import/정의확인이필요합니다.


<!-- semantic-revision17:level-3:end -->

[이 수준의 프로젝트 전체 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A83.md) · [같은 수준 프로필](https://github.com/PUVKID/PUVKID/blob/main/docs/읽기안내/레벨3.md)

### LEVEL 3 · 목적과 대상

**이 차수의 목적과 실제 구성**

입력 영상에 PIL GaussianBlur를 적용하는 10조건 실험입니다. σ0은 원본 배열을 복사합니다.

<a id="layout18-table-15-row-1"></a>

**변환 위치**

**구성**

변환 위치

**실제 역할**

입력 영상에 PIL GaussianBlur를 적용하는 10조건 실험입니다. σ0은 원본 배열을 복사합니다.

<a id="layout18-table-15-row-2"></a>

**모델 연결**

**구성**

모델 연결

**실제 역할**

일반 ResNet50 분류 모델을 사용합니다.

<a id="layout18-table-15-row-3"></a>

**분할·증강**

**구성**

분할·증강

**실제 역할**

원본 train/test를 먼저 나누고 학습 쪽을 증강합니다.

<a id="layout18-table-15-row-4"></a>

**입력과 증강**

**구성**

입력과 증강

**실제 역할**

JPEG 3채널을 512×512 float32로 읽습니다. 학습에서는 좌우·상하 반전, 밝기·대비·잡음을 적용하며 평가 입력과 구분합니다.

<a id="layout18-table-15-row-5"></a>

**분류 헤드**

**구성**

분류 헤드

**실제 역할**

GAP와 GMP를 연결하고 Dense512→BatchNorm·ReLU·Dropout0.35→Dense256→BatchNorm·ReLU·Dropout0.25→softmax로 분류합니다.

<a id="layout18-table-15-row-6"></a>

**평가·저장**

**구성**

평가·저장

**실제 역할**

조건별 정확도·ROC-AUC·클래스별 Recall·혼동행렬과 모델·그래프 출력을 구분합니다.

<a id="layout18-table-15-row-7"></a>

**테스트 의사 라벨**

**구성**

테스트 의사 라벨

**실제 역할**

테스트 예측의 최대 확률이 0.88 이상인 영상을 예측 라벨로 학습 자료에 추가하는 후속 경로가 있습니다.


원고·노트북·저장 결과·대시보드를 차수별로 읽습니다. 과거 논문의 보고값과 현재 Conv1 실행 결과를 합치지 않습니다. 재현에는 원영상·분할·설정·결과 계보가 필요하며 의료 원자료는 공개하지 않습니다.

### LEVEL 3 · 달라진 내용과 차수 관계

입력 블러의 구현과 평가 경로를 다루는 단계입니다. 변환 위치·모델 연결·분할 순서는 위 구성과 같으며, 기존 전체 비교에서 설정·함수·주석을 포함한 차이를 읽을 수 있습니다.

[직전 단계 전체 비교·구성](../revision-diffs/experiment-6.diff) · [전체 파일 크기·해시](../revision-manifests/experiment-6.json)

라벨 매핑과 원본 분할을 먼저 확인합니다. 증강은 학습에만 적용하고 검증·시험 원본과 구분합니다. source_class는 원본 범주 폴더 라벨이며 환자·병원·스캐너 식별자가 아닙니다.

### LEVEL 3 · 입력과 실행 조건

**입력**

CT 원본과 클래스

**처리**

분할·학습 자료 준비

**출력**

학습·검증·시험 입력


**입력**

입력 또는 특징

**처리**

설정한 변환과 모델 학습

**출력**

조건별 예측


**입력**

예측·특징·자원 기록

**처리**

분류 지표·그림·모델 저장

**출력**

조건 비교 결과



**항목**

이미지·배치

**조건·기본값**

512×512·batch8


**항목**

재현 설정

**조건·기본값**

seed42·7fold·test 비율 0.10


**항목**

학습 설정

**조건·기본값**

설정 셀의 단계별 epoch·SWA 시작 40·TTA20


**항목**

입력

**조건·기본값**

별도 CT 데이터와 클래스 폴더


**항목**

변환 조건

**조건·기본값**

입력 10조건


**항목**

최대 epoch

**조건·기본값**

EPOCHS_S1=80·EPOCHS_S2=200


**항목**

학습 증강

**조건·기본값**

밝기 최대 0.25×255·대비 0.75~1.25·Gaussian 잡음 표준편차 5


**항목**

TTA 증강

**조건·기본값**

좌우 반전·밝기 최대 0.15×255·대비 0.85~1.15


**항목**

fold

**조건·기본값**

StratifiedKFold·shuffle·seed42·클래스 가중치


**항목**

손실

**조건·기본값**

focal_loss: gamma2·학습 label smoothing0.02


**항목**

최적화

**조건·기본값**

AdamW·weight decay1e-4·학습률 1e-3→1e-4


**항목**

후속 재학습

**조건·기본값**

학습률 3e-5·label smoothing0.05


**항목**

중단·체크포인트

**조건·기본값**

val_loss 조기 중단·최선 가중치·과적합 제어·SWA/TTA 경로



입력·변환 순서·분할·초기값·학습 예산을 차수별로 확인합니다. Stage 1의 pool1_pool 특징 SSIM은 입력 MS-SSIM과 직접 비교하지 않습니다. 원본 test 선분리와 학습 증강, 큰 sigma 결과 재사용도 확인합니다.

### LEVEL 3 · 처리 절차

1. 설정 셀에서 입력·작업·결과 경로와 변환 조건을 확인합니다.
2. 분할·증강 함수의 호출 순서와 시험 자료가 분리되는 지점을 읽습니다.
3. GPU·TensorFlow·학습 자료를 준비하고 설치·모니터·학습·출력 셀을 구분해 순서대로 읽습니다.
4. 기존 결과의 재사용 조건을 확인한 뒤 필요한 조건을 선택합니다.
5. 조건별 JSON과 혼동행렬·ROC-AUC·Recall을 같은 분모와 클래스 순서로 비교합니다.

실제 완료한 최적 체크포인트와 실행 ID가 같은 결과만 조회합니다. 색은 패널별 최솟값·최댓값으로 표시하므로 다른 패널의 같은 색을 같은 값으로 보지 않습니다. 과거 PNG나 직전 시험 수치를 대기에 재사용하지 않습니다.

### LEVEL 3 · 결과를 확인하는 방법

입력 σ0~256에 따른 분류 결과를 읽습니다.

원고 보고값과 이 코드의 조건별 저장 결과를 구분합니다. 변환 위치·분할·시드와 실제 결과 파일이 같은지 확인합니다.

현재 백분율 요약은 소수 첫째 자리 반올림이며 원비율·전체 백분율·정답 수를 함께 확인합니다. 과거 공개 4차의 둘째 자리 버림 설명은 당시 이력으로 두고 현재 규칙과 섞지 않습니다.

### LEVEL 3 · 주의할 범위

<a id="layout18-table-18-row-1"></a>

**변환의 의미**

**상황**

변환의 의미

**확인할 내용**

블록 재배열·블러 강도만으로 환자 재식별 저항성이나 암호학적 안전성을 보증하지 않습니다.

<a id="layout18-table-18-row-2"></a>

**결과 재사용**

**상황**

결과 재사용

**확인할 내용**

조건별 데이터·가중치·결과를 만들거나 재사용하므로 입력·출력 폴더와 기존 결과를 구분합니다.

<a id="layout18-table-18-row-3"></a>

**분할**

**상황**

분할

**확인할 내용**

원본 train/test를 먼저 나누고 학습 쪽을 증강합니다.

<a id="layout18-table-18-row-4"></a>

**평가 방식**

**상황**

평가 방식

**확인할 내용**

테스트 의사 라벨 추가 학습 후의 수치는 transductive 평가입니다. 테스트 자료를 전혀 이용하지 않은 독립 평가와 구분합니다.

<a id="layout18-table-18-row-5"></a>

**예시 그래프**

**상황**

예시 그래프

**확인할 내용**

실제 결과·학습 이력이 없으면 _dummy_results 또는 _dummy_histories 계열로 예시 값을 만드는 그래프 셀이 있습니다. 그래프가 그려졌다는 사실만으로 학습 결과로 인용하지 않습니다.

<a id="layout18-table-18-row-6"></a>

**입력 스케일**

**상황**

입력 스케일

**확인할 내용**

load_image는 float32 변환으로 0~255 입력을 유지합니다. ImageNet 사전학습과 연결할 때 전처리 가정을 확인합니다.


원본과 분할 manifest의 실제 값은 자신의 로컬 자료로 준비해야 합니다. 공개 예제만으로 기준 비교가 동작하지 않습니다. 미완료 조건과 정의 불가 지표를 보기 좋은 값으로 채우지 않습니다.

[표·코드·실행 설정·파일 전체 비교를 포함한 공통 상세](#reading-level-5)

<a id="reading-level-4"></a>

## LEVEL 4 - Advanced

<!-- semantic-revision17:level-4:start -->

<a id="semantic-lung-training-level-4"></a>

### LEVEL 4 · 노트북 학습·평가의 연결과 실패 조건

증강·tf.data 입력, 분류 헤드, optimizer·focal loss·콜백, SWA/TTA·의사 라벨 앙상블의 경계를 나눕니다. 입력 스케일과 사전학습 전처리, 중첩 모델 trainable 범위, 최적 모델을 다시 쓰는 시점에 따라 결과 해석이 바뀝니다. 수정 도구가 별도로 만드는 노트북은 설정과 분할이 같은지부터 대조합니다.

<a id="layout18-table-19-row-1"></a>

**입력·헤드**

**조건·자료**

입력·헤드

**의미와 확인 방법**

JPEG3채널·512×512·float32의0~255 입력입니다. GAP와GMP를 연결하고 Dense512→BatchNorm·ReLU·Dropout0.35→Dense256→BatchNorm·ReLU·Dropout0.25→softmax로 분류하는 변형이 있습니다.

<a id="layout18-table-19-row-2"></a>

**학습·TTA**

**조건·자료**

학습·TTA

**의미와 확인 방법**

seed42·test0.10·StratifiedKFold7·shuffle·클래스가중치·batch8이며 변형별batch4도 있습니다. EPOCHS_S1=80·EPOCHS_S2=200, 분리모델fit은 최대280epoch, SWA시작40·TTA20입니다.

<a id="layout18-table-19-row-3"></a>

**증강·손실**

**조건·자료**

증강·손실

**의미와 확인 방법**

학습 좌우/상하반전·밝기최대0.25×255·대비0.75~1.25·Gaussian잡음표준편차5, TTA좌우반전·밝기최대0.15×255·대비0.85~1.15입니다. focal gamma2·학습label smoothing0.02·AdamW lr1e-4·weight decay1e-4를 사용하며 후속재학습은lr3e-5·smoothing0.05입니다.

<a id="layout18-table-19-row-4"></a>

**시험 재사용**

**조건·자료**

시험 재사용

**의미와 확인 방법**

시험 예측 확신도0.88이상 영상이10장이상이면 예측라벨로15epochs추가학습한 뒤 같은 시험을 다시 평가하는 경로가 있습니다. 추가모델이7fold모델과 앙상블되며 일부는 전체증강학습을 이용해fold검증도 다시 포함합니다.

<a id="layout18-table-19-row-5"></a>

**누수·코드차이**

**조건·자료**

누수·코드차이

**의미와 확인 방법**

원본test선분리와 증강후fold분리는 다릅니다. 일부이전셀은 증강후test도 분리합니다. 논문의Mixup Beta설명과 코드uniform샘플링, preprocess_input누락, 중첩모델미세조정, 최적체크포인트를종료/SWA가중치로다시저장하는 흐름을 확인합니다.

<a id="layout18-table-19-row-6"></a>

**실행 준비**

**조건·자료**

실행 준비

**의미와 확인 방법**

Python·TensorFlow/Keras·CUDA·드라이버·AdamW API·NumPy·Pillow·scikit-learn·Matplotlib·Seaborn·추가import를 확인합니다. BASE_TRAIN과 실제지원 BB_OUTPUT_ROOT/SB_OUTPUT_ROOT, 입력·결과폴더·디스크·캐시를 구분합니다. 의존성잠금으로 재현을 보증하지 않습니다.

<a id="layout18-table-19-row-7"></a>

**실측과 예시**

**조건·자료**

실측과 예시

**의미와 확인 방법**

_dummy_results·_dummy_histories·GPU예시로그·하드코딩히트맵은 실측이 아닙니다. 결과JSON·분할·시드·가중치·실제로그를 함께 확인합니다.


<a id="semantic-lung-feature-level-4"></a>

### LEVEL 4 · 입력 변환·분리 모델·특징 블러의 차이

변환 모듈의 위치가 입력 분포와 특징 분포를 각각 바꾸며 pool1_pool 경계가 edge/cloud의 계약입니다. 전역 평균 분기와 결과 재사용은 실제 실행 수를 줄이므로 조건명 수와 실행 수를 분리합니다. decoder의 누락 import는 의존성 문제이며 공개 문서 정리에서 코드를 우회 수정하지 않습니다.

<a id="layout18-table-20-row-1"></a>

**입력 변환**

**조건·자료**

입력 변환

**의미와 확인 방법**

블러는PIL GaussianBlur이며σ0은복사합니다. 블록은seed순열로위치를바꾸고내부픽셀을유지하며영상보다작지않은블록은복사합니다. 조합은Block10×Blur10=100이며Block뒤Blur입니다.

<a id="layout18-table-20-row-2"></a>

**분리 경계**

**조건·자료**

분리 경계

**의미와 확인 방법**

edge/cloud는ResNet50 pool1_pool경계의모듈을동일TensorFlow프로세스에서연결한코드입니다. 실제원격전송구현이아닙니다.

<a id="layout18-table-20-row-3"></a>

**특징 변환**

**조건·자료**

특징 변환

**의미와 확인 방법**

Stage1은edge→FeatureGaussianBlur→cloud입니다. 채널별고정Gaussian커널을depthwise_conv2d로적용합니다. σ32·64·128·256은전역평균분기이며REUSE_COLLAPSED_RESULTS기본경로는σ32결과를64·128·256에재사용합니다.

<a id="layout18-table-20-row-4"></a>

**별도 분석**

**조건·자료**

별도 분석

**의미와 확인 방법**

채널평균특징맵을각각정규화한단일SSIM점수·cosine·클래스분리도와선택decoder의PSNR/SSIM을봅니다. decoder는AdamW lr5e-4·weight decay1e-5·MAE이며Conv2D import/정의확인이필요합니다.


<!-- semantic-revision17:level-4:end -->

[이 수준의 프로젝트 전체 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A84.md) · [같은 수준 프로필](https://github.com/PUVKID/PUVKID/blob/main/docs/읽기안내/레벨4.md)

### LEVEL 4 · 목적과 대상

**이 차수의 목적과 실제 구성**

입력 영상에 PIL GaussianBlur를 적용하는 10조건 실험입니다. σ0은 원본 배열을 복사합니다.

<a id="layout18-table-21-row-1"></a>

**변환 위치**

**구성**

변환 위치

**실제 역할**

입력 영상에 PIL GaussianBlur를 적용하는 10조건 실험입니다. σ0은 원본 배열을 복사합니다.

<a id="layout18-table-21-row-2"></a>

**모델 연결**

**구성**

모델 연결

**실제 역할**

일반 ResNet50 분류 모델을 사용합니다.

<a id="layout18-table-21-row-3"></a>

**분할·증강**

**구성**

분할·증강

**실제 역할**

원본 train/test를 먼저 나누고 학습 쪽을 증강합니다.

<a id="layout18-table-21-row-4"></a>

**입력과 증강**

**구성**

입력과 증강

**실제 역할**

JPEG 3채널을 512×512 float32로 읽습니다. 학습에서는 좌우·상하 반전, 밝기·대비·잡음을 적용하며 평가 입력과 구분합니다.

<a id="layout18-table-21-row-5"></a>

**분류 헤드**

**구성**

분류 헤드

**실제 역할**

GAP와 GMP를 연결하고 Dense512→BatchNorm·ReLU·Dropout0.35→Dense256→BatchNorm·ReLU·Dropout0.25→softmax로 분류합니다.

<a id="layout18-table-21-row-6"></a>

**평가·저장**

**구성**

평가·저장

**실제 역할**

조건별 정확도·ROC-AUC·클래스별 Recall·혼동행렬과 모델·그래프 출력을 구분합니다.

<a id="layout18-table-21-row-7"></a>

**테스트 의사 라벨**

**구성**

테스트 의사 라벨

**실제 역할**

테스트 예측의 최대 확률이 0.88 이상인 영상을 예측 라벨로 학습 자료에 추가하는 후속 경로가 있습니다.


입력 변형과 pool1_pool 특징 변형은 개입 위치가 다릅니다. 모델·학습·라벨·분할·점수 정의가 달라 단순 수치 차이를 모델 변경의 인과 효과로 설명할 수 없습니다. 종료 정책 비교도 별도 설계입니다.

### LEVEL 4 · 달라진 내용과 차수 관계

입력 블러의 구현과 평가 경로를 다루는 단계입니다. 변환 위치·모델 연결·분할 순서는 위 구성과 같으며, 기존 전체 비교에서 설정·함수·주석을 포함한 차이를 읽을 수 있습니다.

[직전 단계 전체 비교·구성](../revision-diffs/experiment-6.diff) · [전체 파일 크기·해시](../revision-manifests/experiment-6.json)

환자 ID 없는 영상 그룹 분할은 환자 독립 분할의 대체가 아닙니다. 소스별 촬영·압축 차이와 같은 환자의 다른 영상이 성능에 영향을 줄 수 있습니다. 높은 정확도의 원인을 조기 종료로 미리 확정하지 않습니다.

### LEVEL 4 · 입력과 실행 조건

**입력**

CT 원본과 클래스

**처리**

분할·학습 자료 준비

**출력**

학습·검증·시험 입력


**입력**

입력 또는 특징

**처리**

설정한 변환과 모델 학습

**출력**

조건별 예측


**입력**

예측·특징·자원 기록

**처리**

분류 지표·그림·모델 저장

**출력**

조건 비교 결과



**항목**

이미지·배치

**조건·기본값**

512×512·batch8


**항목**

재현 설정

**조건·기본값**

seed42·7fold·test 비율 0.10


**항목**

학습 설정

**조건·기본값**

설정 셀의 단계별 epoch·SWA 시작 40·TTA20


**항목**

입력

**조건·기본값**

별도 CT 데이터와 클래스 폴더


**항목**

변환 조건

**조건·기본값**

입력 10조건


**항목**

최대 epoch

**조건·기본값**

EPOCHS_S1=80·EPOCHS_S2=200


**항목**

학습 증강

**조건·기본값**

밝기 최대 0.25×255·대비 0.75~1.25·Gaussian 잡음 표준편차 5


**항목**

TTA 증강

**조건·기본값**

좌우 반전·밝기 최대 0.15×255·대비 0.85~1.15


**항목**

fold

**조건·기본값**

StratifiedKFold·shuffle·seed42·클래스 가중치


**항목**

손실

**조건·기본값**

focal_loss: gamma2·학습 label smoothing0.02


**항목**

최적화

**조건·기본값**

AdamW·weight decay1e-4·학습률 1e-3→1e-4


**항목**

후속 재학습

**조건·기본값**

학습률 3e-5·label smoothing0.05


**항목**

중단·체크포인트

**조건·기본값**

val_loss 조기 중단·최선 가중치·과적합 제어·SWA/TTA 경로



Stage 1은 같은 프로세스의 Edge·Cloud 연결이며 실제 원격 전송이 아닙니다. 큰 sigma의 전역 평균 대체, sigma32 결과의 64/128/256 재사용과 Conv2D import 누락 같은 실행 제약을 구분합니다.

### LEVEL 4 · 처리 절차

1. 설정 셀에서 입력·작업·결과 경로와 변환 조건을 확인합니다.
2. 분할·증강 함수의 호출 순서와 시험 자료가 분리되는 지점을 읽습니다.
3. GPU·TensorFlow·학습 자료를 준비하고 설치·모니터·학습·출력 셀을 구분해 순서대로 읽습니다.
4. 기존 결과의 재사용 조건을 확인한 뒤 필요한 조건을 선택합니다.
5. 조건별 JSON과 혼동행렬·ROC-AUC·Recall을 같은 분모와 클래스 순서로 비교합니다.

공개 4차는 학습 2차 대시보드의 로컬 수리 3차 사본입니다. 공개 5차는 실험 4차 고정 100회 비교 코드입니다. 원본 manifest·해시·정확 분할이 다르면 중단합니다.

### LEVEL 4 · 결과를 확인하는 방법

입력 σ0~256에 따른 분류 결과를 읽습니다.

원고 보고값과 이 코드의 조건별 저장 결과를 구분합니다. 변환 위치·분할·시드와 실제 결과 파일이 같은지 확인합니다.

Blur sigma256의 51.38%는 다수 클래스 56/109와 같지만 모든 조건의 하한은 아닙니다. 별도 학습한 Block512+sigma256은 46.8%입니다. 조합·단독·별도 학습·시험 분모를 나누어 읽습니다.

### LEVEL 4 · 주의할 범위

<a id="layout18-table-24-row-1"></a>

**변환의 의미**

**상황**

변환의 의미

**확인할 내용**

블록 재배열·블러 강도만으로 환자 재식별 저항성이나 암호학적 안전성을 보증하지 않습니다.

<a id="layout18-table-24-row-2"></a>

**결과 재사용**

**상황**

결과 재사용

**확인할 내용**

조건별 데이터·가중치·결과를 만들거나 재사용하므로 입력·출력 폴더와 기존 결과를 구분합니다.

<a id="layout18-table-24-row-3"></a>

**분할**

**상황**

분할

**확인할 내용**

원본 train/test를 먼저 나누고 학습 쪽을 증강합니다.

<a id="layout18-table-24-row-4"></a>

**평가 방식**

**상황**

평가 방식

**확인할 내용**

테스트 의사 라벨 추가 학습 후의 수치는 transductive 평가입니다. 테스트 자료를 전혀 이용하지 않은 독립 평가와 구분합니다.

<a id="layout18-table-24-row-5"></a>

**예시 그래프**

**상황**

예시 그래프

**확인할 내용**

실제 결과·학습 이력이 없으면 _dummy_results 또는 _dummy_histories 계열로 예시 값을 만드는 그래프 셀이 있습니다. 그래프가 그려졌다는 사실만으로 학습 결과로 인용하지 않습니다.

<a id="layout18-table-24-row-6"></a>

**입력 스케일**

**상황**

입력 스케일

**확인할 내용**

load_image는 float32 변환으로 0~255 입력을 유지합니다. ImageNet 사전학습과 연결할 때 전처리 가정을 확인합니다.


기존 분할·시험셋 재사용과 환자 ID 부재는 독립 임상 평가를 제한합니다. 높은 정확도의 원인을 조기 종료로 확정하지 않고 동일 조건 정책 비교를 합니다. 두 비교 모델은 같은 학습 경로에서 선택됩니다.

[표·코드·실행 설정·파일 전체 비교를 포함한 공통 상세](#reading-level-5)

<a id="reading-level-5"></a>

## LEVEL 5 - Expert

<!-- semantic-revision17:level-5:start -->

<a id="semantic-lung-training-level-5"></a>

### LEVEL 5 · 노트북 학습·평가의 연결과 실패 조건

관측된 코드 경로를 엄격 hold-out 프로토콜로 확대하지 않습니다. test 선분리 여부와 별개로 파생 영상 fold 중복·전체 학습 자료 재사용·동일 test 재평가를 확인해야 합니다. 실측과 예시 분기·캐시 재사용·체크포인트 실체를 결합해 검토하며 아래 설정의 존재를 학습 완료·성능 재현의 증거로 삼지 않습니다.

<a id="layout18-table-25-row-1"></a>

**입력·헤드**

**조건·자료**

입력·헤드

**의미와 확인 방법**

JPEG3채널·512×512·float32의0~255 입력입니다. GAP와GMP를 연결하고 Dense512→BatchNorm·ReLU·Dropout0.35→Dense256→BatchNorm·ReLU·Dropout0.25→softmax로 분류하는 변형이 있습니다.

<a id="layout18-table-25-row-2"></a>

**학습·TTA**

**조건·자료**

학습·TTA

**의미와 확인 방법**

seed42·test0.10·StratifiedKFold7·shuffle·클래스가중치·batch8이며 변형별batch4도 있습니다. EPOCHS_S1=80·EPOCHS_S2=200, 분리모델fit은 최대280epoch, SWA시작40·TTA20입니다.

<a id="layout18-table-25-row-3"></a>

**증강·손실**

**조건·자료**

증강·손실

**의미와 확인 방법**

학습 좌우/상하반전·밝기최대0.25×255·대비0.75~1.25·Gaussian잡음표준편차5, TTA좌우반전·밝기최대0.15×255·대비0.85~1.15입니다. focal gamma2·학습label smoothing0.02·AdamW lr1e-4·weight decay1e-4를 사용하며 후속재학습은lr3e-5·smoothing0.05입니다.

<a id="layout18-table-25-row-4"></a>

**시험 재사용**

**조건·자료**

시험 재사용

**의미와 확인 방법**

시험 예측 확신도0.88이상 영상이10장이상이면 예측라벨로15epochs추가학습한 뒤 같은 시험을 다시 평가하는 경로가 있습니다. 추가모델이7fold모델과 앙상블되며 일부는 전체증강학습을 이용해fold검증도 다시 포함합니다.

<a id="layout18-table-25-row-5"></a>

**누수·코드차이**

**조건·자료**

누수·코드차이

**의미와 확인 방법**

원본test선분리와 증강후fold분리는 다릅니다. 일부이전셀은 증강후test도 분리합니다. 논문의Mixup Beta설명과 코드uniform샘플링, preprocess_input누락, 중첩모델미세조정, 최적체크포인트를종료/SWA가중치로다시저장하는 흐름을 확인합니다.

<a id="layout18-table-25-row-6"></a>

**실행 준비**

**조건·자료**

실행 준비

**의미와 확인 방법**

Python·TensorFlow/Keras·CUDA·드라이버·AdamW API·NumPy·Pillow·scikit-learn·Matplotlib·Seaborn·추가import를 확인합니다. BASE_TRAIN과 실제지원 BB_OUTPUT_ROOT/SB_OUTPUT_ROOT, 입력·결과폴더·디스크·캐시를 구분합니다. 의존성잠금으로 재현을 보증하지 않습니다.

<a id="layout18-table-25-row-7"></a>

**실측과 예시**

**조건·자료**

실측과 예시

**의미와 확인 방법**

_dummy_results·_dummy_histories·GPU예시로그·하드코딩히트맵은 실측이 아닙니다. 결과JSON·분할·시드·가중치·실제로그를 함께 확인합니다.


<a id="semantic-lung-feature-level-5"></a>

### LEVEL 5 · 입력 변환·분리 모델·특징 블러의 차이

동일 프로세스 연결을 실제 분산 전송 성능으로 평가하지 않습니다. 특징의 정규화·단일 SSIM과 입력 영상 5스케일 MS-SSIM은 대상과 계산이 달라 점수만 비교할 수 없습니다. σ32 재사용 여부·실제 가중치·복원 분기의 완전성과 저장 측정을 검토하고 미실행 공격 결과를 만들지 않습니다.

<a id="layout18-table-26-row-1"></a>

**입력 변환**

**조건·자료**

입력 변환

**의미와 확인 방법**

블러는PIL GaussianBlur이며σ0은복사합니다. 블록은seed순열로위치를바꾸고내부픽셀을유지하며영상보다작지않은블록은복사합니다. 조합은Block10×Blur10=100이며Block뒤Blur입니다.

<a id="layout18-table-26-row-2"></a>

**분리 경계**

**조건·자료**

분리 경계

**의미와 확인 방법**

edge/cloud는ResNet50 pool1_pool경계의모듈을동일TensorFlow프로세스에서연결한코드입니다. 실제원격전송구현이아닙니다.

<a id="layout18-table-26-row-3"></a>

**특징 변환**

**조건·자료**

특징 변환

**의미와 확인 방법**

Stage1은edge→FeatureGaussianBlur→cloud입니다. 채널별고정Gaussian커널을depthwise_conv2d로적용합니다. σ32·64·128·256은전역평균분기이며REUSE_COLLAPSED_RESULTS기본경로는σ32결과를64·128·256에재사용합니다.

<a id="layout18-table-26-row-4"></a>

**별도 분석**

**조건·자료**

별도 분석

**의미와 확인 방법**

채널평균특징맵을각각정규화한단일SSIM점수·cosine·클래스분리도와선택decoder의PSNR/SSIM을봅니다. decoder는AdamW lr5e-4·weight decay1e-5·MAE이며Conv2D import/정의확인이필요합니다.


<!-- semantic-revision17:level-5:end -->

[전문가 수준 프로젝트 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A85.md) · [같은 수준 프로필](https://github.com/PUVKID/PUVKID/blob/main/docs/읽기안내/레벨5.md)

**기존 전체 상세** — 다음 본문은 이 차수의 원래 방법·조건·결과·실패·한계와 전체 비교입니다. 위 수준의 설명에 필요한 공통 근거도 모두 여기서 확인할 수 있습니다.
<!-- reading-levels17:end -->

**입력 영상에 PIL GaussianBlur를 적용하는 10조건 실험입니다.** σ0은 원본 배열을 복사합니다.

분야: 의료 영상 실험 코드 › TensorFlow·ResNet50 › 입력 블러

[목적](#purpose) · [기능](#features) · [입출력](#flow) · [구성](#files) · [준비](#setup) · [사용법](#usage) · [결과](#results) · [제약](#limits) · [변경](#changes)

<a name="purpose"></a>

<a id="-이-단계에서-하는-일"></a>

## 연구 목적

이 단계의 핵심은 입력 블러입니다. 원본 train/test를 먼저 나누고 학습 쪽을 증강합니다. 입력 σ0~256에 따른 분류 결과를 읽습니다.

<a name="features"></a>

<a id="-주요-기능과-처리-방식"></a>

## 방법과 구현

<a id="layout18-table-27-row-1"></a>

**변환 위치**

**구성**

변환 위치

**실제 역할**

입력 영상에 PIL GaussianBlur를 적용하는 10조건 실험입니다. σ0은 원본 배열을 복사합니다.

<a id="layout18-table-27-row-2"></a>

**모델 연결**

**구성**

모델 연결

**실제 역할**

일반 ResNet50 분류 모델을 사용합니다.

<a id="layout18-table-27-row-3"></a>

**분할·증강**

**구성**

분할·증강

**실제 역할**

원본 train/test를 먼저 나누고 학습 쪽을 증강합니다.

<a id="layout18-table-27-row-4"></a>

**입력과 증강**

**구성**

입력과 증강

**실제 역할**

JPEG 3채널을 512×512 float32로 읽습니다. 학습에서는 좌우·상하 반전, 밝기·대비·잡음을 적용하며 평가 입력과 구분합니다.

<a id="layout18-table-27-row-5"></a>

**분류 헤드**

**구성**

분류 헤드

**실제 역할**

GAP와 GMP를 연결하고 Dense512→BatchNorm·ReLU·Dropout0.35→Dense256→BatchNorm·ReLU·Dropout0.25→softmax로 분류합니다.

<a id="layout18-table-27-row-6"></a>

**평가·저장**

**구성**

평가·저장

**실제 역할**

조건별 정확도·ROC-AUC·클래스별 Recall·혼동행렬과 모델·그래프 출력을 구분합니다.

<a id="layout18-table-27-row-7"></a>

**테스트 의사 라벨**

**구성**

테스트 의사 라벨

**실제 역할**

테스트 예측의 최대 확률이 0.88 이상인 영상을 예측 라벨로 학습 자료에 추가하는 후속 경로가 있습니다.


<a name="flow"></a>

<a id="-입력--처리--출력"></a>

## 입력·처리·출력

**입력**

CT 원본과 클래스

**처리**

분할·학습 자료 준비

**출력**

학습·검증·시험 입력


**입력**

입력 또는 특징

**처리**

설정한 변환과 모델 학습

**출력**

조건별 예측


**입력**

예측·특징·자원 기록

**처리**

분류 지표·그림·모델 저장

**출력**

조건 비교 결과



<a name="files"></a>

<a id="-파일과-핵심-처리"></a>

## 파일별 역할

| 파일 · 이용 방법 |
| --- |
| **파일**<br>[블러/2차 실험/blur_resnet50_rebuilt2_KO.ipynb](../../%EB%B8%94%EB%9F%AC/2%EC%B0%A8%20%EC%8B%A4%ED%97%98/blur_resnet50_rebuilt2_KO.ipynb)<br><br>**이용 방법**<br>설정·함수·실행 셀 |

<a id="-함수셀로-찾아가기"></a>

### 관련 함수와 셀

관련 함수와 셀을 파일별로 정리했습니다. 실행 전 설정과 호출 순서, 출력 경로를 확인하세요.

<a id="layout18-table-30-row-1"></a>

**[블러/2차 실험/blur_resnet50_rebuilt2_KO.ipynb](../../%EB%B8%94%EB%9F%AC/2%EC%B0%A8%20%EC%8B%A4%ED%97%98/blur_resnet50_rebuilt2_KO.ipynb)**

**파일**

[블러/2차 실험/blur_resnet50_rebuilt2_KO.ipynb](../../%EB%B8%94%EB%9F%AC/2%EC%B0%A8%20%EC%8B%A4%ED%97%98/blur_resnet50_rebuilt2_KO.ipynb)

**핵심 정의**

셀 6: `gpu_status` · `GPUMonitorCallback` · `__init__` · `on_epoch_end`<br>셀 8: `set_reproducible` · `list_class_dirs` · `list_image_files`<br>셀 10: `apply_gaussian_blur` · `generate_blur_dataset`<br>셀 12: `oversample_train`<br>셀 14: `prepare_split`<br>셀 16: `_deterministic` · `get_paths_labels` · `load_image` · `augment_train` · `mixup_batch` · `cutmix_batch` · `apply_mixup` · `apply_cutmix`<br>셀 18: `focal_loss` · `loss_fn` · `CosineAnnealingWarmRestart` · `__init__` · `on_epoch_begin` · `SWACallback` · `__init__` · `on_epoch_end`


<a name="setup"></a>

<a id="️-환경과-설정"></a>

## 실행 환경과 설정

**항목**

이미지·배치

**조건·기본값**

512×512·batch8


**항목**

재현 설정

**조건·기본값**

seed42·7fold·test 비율 0.10


**항목**

학습 설정

**조건·기본값**

설정 셀의 단계별 epoch·SWA 시작 40·TTA20


**항목**

입력

**조건·기본값**

별도 CT 데이터와 클래스 폴더


**항목**

변환 조건

**조건·기본값**

입력 10조건


**항목**

최대 epoch

**조건·기본값**

EPOCHS_S1=80·EPOCHS_S2=200


**항목**

학습 증강

**조건·기본값**

밝기 최대 0.25×255·대비 0.75~1.25·Gaussian 잡음 표준편차 5


**항목**

TTA 증강

**조건·기본값**

좌우 반전·밝기 최대 0.15×255·대비 0.85~1.15


**항목**

fold

**조건·기본값**

StratifiedKFold·shuffle·seed42·클래스 가중치


**항목**

손실

**조건·기본값**

focal_loss: gamma2·학습 label smoothing0.02


**항목**

최적화

**조건·기본값**

AdamW·weight decay1e-4·학습률 1e-3→1e-4


**항목**

후속 재학습

**조건·기본값**

학습률 3e-5·label smoothing0.05


**항목**

중단·체크포인트

**조건·기본값**

val_loss 조기 중단·최선 가중치·과적합 제어·SWA/TTA 경로



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

입력 σ0~256에 따른 분류 결과를 읽습니다.

원고 보고값과 이 코드의 조건별 저장 결과를 구분합니다. 변환 위치·분할·시드와 실제 결과 파일이 같은지 확인합니다.

<a name="limits"></a>

<a id="️-알려진-제약과-확인-지점"></a>

## 제약과 확인 사항

<a id="layout18-table-32-row-1"></a>

**변환의 의미**

**상황**

변환의 의미

**확인할 내용**

블록 재배열·블러 강도만으로 환자 재식별 저항성이나 암호학적 안전성을 보증하지 않습니다.

<a id="layout18-table-32-row-2"></a>

**결과 재사용**

**상황**

결과 재사용

**확인할 내용**

조건별 데이터·가중치·결과를 만들거나 재사용하므로 입력·출력 폴더와 기존 결과를 구분합니다.

<a id="layout18-table-32-row-3"></a>

**분할**

**상황**

분할

**확인할 내용**

원본 train/test를 먼저 나누고 학습 쪽을 증강합니다.

<a id="layout18-table-32-row-4"></a>

**평가 방식**

**상황**

평가 방식

**확인할 내용**

테스트 의사 라벨 추가 학습 후의 수치는 transductive 평가입니다. 테스트 자료를 전혀 이용하지 않은 독립 평가와 구분합니다.

<a id="layout18-table-32-row-5"></a>

**예시 그래프**

**상황**

예시 그래프

**확인할 내용**

실제 결과·학습 이력이 없으면 _dummy_results 또는 _dummy_histories 계열로 예시 값을 만드는 그래프 셀이 있습니다. 그래프가 그려졌다는 사실만으로 학습 결과로 인용하지 않습니다.

<a id="layout18-table-32-row-6"></a>

**입력 스케일**

**상황**

입력 스케일

**확인할 내용**

load_image는 float32 변환으로 0~255 입력을 유지합니다. ImageNet 사전학습과 연결할 때 전처리 가정을 확인합니다.


<a name="changes"></a>

<a id="-이전-단계와의-변화"></a>

## 직전 단계와 비교

입력 블러의 구현과 평가 경로를 다루는 단계입니다. 변환 위치·모델 연결·분할 순서는 위 구성과 같으며, 기존 전체 비교에서 설정·함수·주석을 포함한 차이를 읽을 수 있습니다.

[직전 단계 전체 비교·구성](../revision-diffs/experiment-6.diff) · [전체 파일 크기·해시](../revision-manifests/experiment-6.json)

<details>
<summary>이 단계의 파일 기록과 전체 해시</summary>

아래 내용는 해당 단계가 기록될 당시의 파일 정보입니다. 현재 첨부는 [프로젝트 자료 안내](../PAPERS.md)에서 확인할 수 있습니다.

<a id="layout18-table-33-row-1"></a>

**[블러/2차 실험/blur_resnet50_rebuilt2_KO.ipynb](../../%EB%B8%94%EB%9F%AC/2%EC%B0%A8%20%EC%8B%A4%ED%97%98/blur_resnet50_rebuilt2_KO.ipynb)**

**파일**

[블러/2차 실험/blur_resnet50_rebuilt2_KO.ipynb](../../%EB%B8%94%EB%9F%AC/2%EC%B0%A8%20%EC%8B%A4%ED%97%98/blur_resnet50_rebuilt2_KO.ipynb)

**종류**

.ipynb

**바이트**

102127

**SHA-256**

`745bb2b539259819784a219ebde96df31797fad820af09cd183177e529986870`

<a id="layout18-table-33-row-2"></a>

**항목 2**

**파일**

[원본자료/블러/2차 실험/all_blur_results_resnet50_unified_v1.json](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EB%B8%94%EB%9F%AC/2%EC%B0%A8%20%EC%8B%A4%ED%97%98/all_blur_results_resnet50_unified_v1.json)

**종류**

.json

**바이트**

5326

**SHA-256**

`a1139a82300e74f5a4c66f4c4e08cce921a2245c5bd295f402a0b4e88940e8db`

<a id="layout18-table-33-row-3"></a>

**[원본자료/블러/2차 실험/blur_resnet50_rebuilt2_KO.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EB%B8%94%EB%9F%AC/2%EC%B0%A8%20%EC%8B%A4%ED%97%98/blur_resnet50_rebuilt2_KO.ipynb)**

**파일**

[원본자료/블러/2차 실험/blur_resnet50_rebuilt2_KO.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EB%B8%94%EB%9F%AC/2%EC%B0%A8%20%EC%8B%A4%ED%97%98/blur_resnet50_rebuilt2_KO.ipynb)

**종류**

.ipynb

**바이트**

102127

**SHA-256**

`745bb2b539259819784a219ebde96df31797fad820af09cd183177e529986870`


</details>

---

[프로젝트](../../README.md) · [전체 차수](../REVISION_INDEX.md) · [자료 폴더](../../%EB%B8%94%EB%9F%AC/2%EC%B0%A8%20%EC%8B%A4%ED%97%98)

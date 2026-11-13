<a id="-자료-1차--resnet50-비교-노트북의-설정-정리"></a>

# 자료 1차 · ResNet50 비교 노트북의 설정 정리

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


<a id="semantic-lung-tools-level-1"></a>

### LEVEL 1 · 자료 차수의 수정 도구와 소규모 계산

자료 차수는 논문 번호와 다른 **파일 보관 단계**입니다. 노트북을 고치는 도구는 학습을 대신하지 않고, 3장짜리 계산은 전체 사진의 연구 결과를 대신하지 않습니다. 항등 조건은 사진을 바꾸지 않은 조건이라 구조 차이 점수가 0입니다. 빈 파일은 이름만으로 기능이 있는 것처럼 읽지 않습니다.

<a id="layout18-table-2-row-1"></a>

**자료1차**

**조건·자료**

자료1차

**의미와 확인 방법**

블록·블러각각rebuilt·same_settings·metric_matched의여섯노트북입니다. metric_matched는블록평균SSIM/PSNR에맞는sigma를탐색하며batch4/8·epoch·SWA가변형별로다릅니다. 보조도구는지정노트북을다시씁니다.

<a id="layout18-table-2-row-2"></a>

**자료2차**

**조건·자료**

자료2차

**의미와 확인 방법**

align_experiment_methods.mjs는GPU모니터필드/그래프호환을맞추고build_block_blur_notebook.mjs는Blur사본에서Block→Blur100조합을만듭니다. replaceOrThrow는대상문자열누락시중단하고rollback_original_notebooks.mjs는보관본/지정셀을복원합니다. Node.js와실제입력·출력경로가필요합니다.

<a id="layout18-table-2-row-3"></a>

**자료3차**

**조건·자료**

자료3차

**의미와 확인 방법**

512·seed42의3장입력, Block512·32/Blurσ0·2/조합4의8조건입니다. Privacy Score=((1−SSIM)/2)×100이며PSNR은별도참고값입니다. long·방법요약·조합pivot·best_conditions의4CSV가있습니다. 항등조건0, Block32와B32_S0의35.3667978…은3장계산확인값입니다.

<a id="layout18-table-2-row-4"></a>

**자료4차**

**조건·자료**

자료4차

**의미와 확인 방법**

자료차수/4차/코드의학습·MS-SSIM·도표코드를19쪽원고와연결합니다. pareto_scatter.ipynb는0바이트로실행내용이없습니다. 소규모SSIM표와원고1,097장MS-SSIM을섞지않습니다.


<!-- semantic-revision17:level-1:end -->

[이 수준의 프로젝트 전체 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A81.md) · [같은 수준 프로필](https://github.com/PUVKID/PUVKID/blob/main/docs/읽기안내/레벨1.md)

### LEVEL 1 · 목적과 대상

**이 차수의 목적과 실제 구성**

블록·블러의 rebuilt·same_settings·metric_matched 변형과 노트북 수정 보조 스크립트를 함께 읽는 코드 자료 차수입니다.

<a id="layout18-table-3-row-1"></a>

**여섯 노트북**

**구성**

여섯 노트북

**실제 역할**

블록·블러 각각 rebuilt·same_settings·metric_matched로 나누어 보관합니다.

<a id="layout18-table-3-row-2"></a>

**강도 매칭**

**구성**

강도 매칭

**실제 역할**

metric_matched 블러는 블록 변환의 평균 SSIM/PSNR에 맞는 sigma를 보정하는 함수를 포함합니다.

<a id="layout18-table-3-row-3"></a>

**학습 설정**

**구성**

학습 설정

**실제 역할**

변형별 batch4/8과 단계별 epoch·SWA 시작값이 다르므로 설정 셀을 확인합니다.

<a id="layout18-table-3-row-4"></a>

**수정 도구**

**구성**

수정 도구

**실제 역할**

노트북 생성·콜백·반복 학습·과적합 제어를 수정하는 보조 스크립트가 있습니다.


CT 사진을 흐리게 하거나 블록으로 재배열했을 때 분류 결과와 영상 유사도가 어떻게 달라지는지 살펴봅니다. 입력 사진을 바꾸는 연구와 모델 내부의 첫 합성곱 특징을 흐리는 실험이 함께 있습니다. **논문 연구 번호·공개 코드 차수·실제 학습 차수는 다릅니다.**

### LEVEL 1 · 달라진 내용과 차수 관계

블록·블러 실험 노트북의 조건과 보조 도구를 정리한 자료 1차입니다. 논문의 연구 1 번호와 다른 코드 자료 구분입니다.

[직전 단계 전체 비교·구성](../revision-diffs/folder-1.diff) · [전체 파일 크기·해시](../revision-manifests/folder-1.json)

사진의 모양이 바뀌었어도 분류기가 정답을 잘 맞추는지, 얼마나 비슷한 정보를 남기는지 따로 봅니다. OK는 양성+정상, NG는 악성입니다. 사진 수·독립 환자 수·반복 학습 표본 수를 섞지 않습니다.

### LEVEL 1 · 입력과 실행 조건

| 입력 | 처리 | 출력 |
| --- | --- | --- |
| 블록·블러 노트북 | 설정과 변환 강도 비교 | 실행할 변형 선택 |
| 보정용 영상 | SSIM/PSNR 기반 sigma 탐색 | 블록과 비교할 블러 강도 |
| 노트북 원본 | 지정 셀·문자열 수정 | 다른 설정의 노트북 |

| 항목 | 조건·기본값 |
| --- | --- |
| 입력 크기 | 512 |
| 변환 | 블록 512~1·블러 조건별 sigma |
| 비교 목적 | same_settings와 metric_matched 구분 |
| 수정 도구 | Python 및 Node.js·실제 notebook 경로 |

입력 사진에 블러·블록을 적용하는 경로와 모델이 뽑은 특징에 블러를 적용하는 경로를 나눕니다. 특징은 사진에서 찾은 선·무늬의 반응입니다. 그 색이 병변 위치나 악성 확률을 뜻하지 않습니다.

### LEVEL 1 · 처리 절차

1. 여섯 노트북의 설정 셀에서 비교 목적·batch·변환 강도를 확인합니다.
2. metric_matched의 보정 영상 선택과 목표 SSIM/PSNR을 읽습니다.
3. 실험 입력·저장 경로와 분할·증강 순서를 확인합니다.
4. 수정 스크립트는 대상 파일을 다시 쓰므로 별도 사본에서 입력·치환 대상을 확인한 뒤 사용합니다.

전체 차수 표에서 읽을 연구를 고릅니다. 노트북을 여는 것과 새 학습 시작은 다릅니다. 대시보드에서 같은 강도의 사진·곡선·시험 수치를 함께 읽되 미완료 조건은 미측정으로 남깁니다.

### LEVEL 1 · 결과를 확인하는 방법

노트북 변형은 실험 조건을 정리한 코드입니다. 설정이 달라졌다고 새 성능 결과가 이미 확보된 것으로 보지 않습니다.

영상 유사도를 맞추는 보정은 분류 성능이나 프라이버시가 동등하다는 보장이 아닙니다. 보정에 사용하는 자료와 시험 자료의 관계도 확인해야 합니다.

연구 1의 원고 보고 정확도는 원본 92.5%, sigma32 블러 53.3%, Block32 재배열 79.2%입니다. 이는 당시 논문의 값이며 현재 Conv1 예비실험의 결과로 바꾸지 않습니다.

### LEVEL 1 · 주의할 범위

| 상황 | 확인할 내용 |
| --- | --- |
| 이름과 역할 | rebuilt·same_settings·metric_matched가 같은 실행이라는 뜻은 아닙니다. |
| 파일 쓰기 | 보조 도구는 지정 노트북을 덮어쓸 수 있으므로 사본과 경로를 준비합니다. |
| 평가 기준 | 유사도 매칭과 독립 분류 시험을 구분합니다. |

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


<a id="semantic-lung-tools-level-2"></a>

### LEVEL 2 · 자료 차수의 수정 도구와 소규모 계산

같은 설정으로 맞추는 비교와 SSIM/PSNR을 맞추는 비교는 목적이 다릅니다. 전자는 학습 조건을 맞추고 후자는 영상 유사도가 비슷한 변환 강도를 찾습니다. 자료 2차는 이 노트북을 생성/수정하며 3차는 작은 입력으로 계산 경로를 점검하고 4차는 원고와 코드를 연결합니다.

<a id="layout18-table-8-row-1"></a>

**자료1차**

**조건·자료**

자료1차

**의미와 확인 방법**

블록·블러각각rebuilt·same_settings·metric_matched의여섯노트북입니다. metric_matched는블록평균SSIM/PSNR에맞는sigma를탐색하며batch4/8·epoch·SWA가변형별로다릅니다. 보조도구는지정노트북을다시씁니다.

<a id="layout18-table-8-row-2"></a>

**자료2차**

**조건·자료**

자료2차

**의미와 확인 방법**

align_experiment_methods.mjs는GPU모니터필드/그래프호환을맞추고build_block_blur_notebook.mjs는Blur사본에서Block→Blur100조합을만듭니다. replaceOrThrow는대상문자열누락시중단하고rollback_original_notebooks.mjs는보관본/지정셀을복원합니다. Node.js와실제입력·출력경로가필요합니다.

<a id="layout18-table-8-row-3"></a>

**자료3차**

**조건·자료**

자료3차

**의미와 확인 방법**

512·seed42의3장입력, Block512·32/Blurσ0·2/조합4의8조건입니다. Privacy Score=((1−SSIM)/2)×100이며PSNR은별도참고값입니다. long·방법요약·조합pivot·best_conditions의4CSV가있습니다. 항등조건0, Block32와B32_S0의35.3667978…은3장계산확인값입니다.

<a id="layout18-table-8-row-4"></a>

**자료4차**

**조건·자료**

자료4차

**의미와 확인 방법**

자료차수/4차/코드의학습·MS-SSIM·도표코드를19쪽원고와연결합니다. pareto_scatter.ipynb는0바이트로실행내용이없습니다. 소규모SSIM표와원고1,097장MS-SSIM을섞지않습니다.


<!-- semantic-revision17:level-2:end -->

[이 수준의 프로젝트 전체 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A82.md) · [같은 수준 프로필](https://github.com/PUVKID/PUVKID/blob/main/docs/읽기안내/레벨2.md)

### LEVEL 2 · 목적과 대상

**이 차수의 목적과 실제 구성**

블록·블러의 rebuilt·same_settings·metric_matched 변형과 노트북 수정 보조 스크립트를 함께 읽는 코드 자료 차수입니다.

<a id="layout18-table-9-row-1"></a>

**여섯 노트북**

**구성**

여섯 노트북

**실제 역할**

블록·블러 각각 rebuilt·same_settings·metric_matched로 나누어 보관합니다.

<a id="layout18-table-9-row-2"></a>

**강도 매칭**

**구성**

강도 매칭

**실제 역할**

metric_matched 블러는 블록 변환의 평균 SSIM/PSNR에 맞는 sigma를 보정하는 함수를 포함합니다.

<a id="layout18-table-9-row-3"></a>

**학습 설정**

**구성**

학습 설정

**실제 역할**

변형별 batch4/8과 단계별 epoch·SWA 시작값이 다르므로 설정 셀을 확인합니다.

<a id="layout18-table-9-row-4"></a>

**수정 도구**

**구성**

수정 도구

**실제 역할**

노트북 생성·콜백·반복 학습·과적합 제어를 수정하는 보조 스크립트가 있습니다.


입력 변형 연구 1·2, 특징 블러 Stage 1, Conv1 OK/NG 예비실험을 구분합니다. 블러는 무늬를 부드럽게 하고 블록 재배열은 위치를 섞습니다. 분류 정확도와 유사도 기반 Privacy Score는 서로 다른 양을 측정합니다.

### LEVEL 2 · 달라진 내용과 차수 관계

블록·블러 실험 노트북의 조건과 보조 도구를 정리한 자료 1차입니다. 논문의 연구 1 번호와 다른 코드 자료 구분입니다.

[직전 단계 전체 비교·구성](../revision-diffs/folder-1.diff) · [전체 파일 크기·해시](../revision-manifests/folder-1.json)

이전 연구는 정상·양성·악성 3분류, Conv1은 OK/NG 이진 분류입니다. 원본 1,097장은 양성 120·정상 416·악성 561장입니다. 클래스당 매 epoch 5,000표본은 반복·온라인 증강이며 독립 영상 5,000장이 아닙니다.

### LEVEL 2 · 입력과 실행 조건

| 입력 | 처리 | 출력 |
| --- | --- | --- |
| 블록·블러 노트북 | 설정과 변환 강도 비교 | 실행할 변형 선택 |
| 보정용 영상 | SSIM/PSNR 기반 sigma 탐색 | 블록과 비교할 블러 강도 |
| 노트북 원본 | 지정 셀·문자열 수정 | 다른 설정의 노트북 |

| 항목 | 조건·기본값 |
| --- | --- |
| 입력 크기 | 512 |
| 변환 | 블록 512~1·블러 조건별 sigma |
| 비교 목적 | same_settings와 metric_matched 구분 |
| 수정 도구 | Python 및 Node.js·실제 notebook 경로 |

연구 1은 512×512 입력에 두 변환을 각각 적용해 정확도·ROC-AUC·혼동행렬을 봅니다. 연구 2는 Blur→Block·Block→Blur 조합과 입력 MS-SSIM을 비교합니다. Conv1은 첫 합성곱 특징을 바꾼 뒤 분류합니다.

### LEVEL 2 · 처리 절차

1. 여섯 노트북의 설정 셀에서 비교 목적·batch·변환 강도를 확인합니다.
2. metric_matched의 보정 영상 선택과 목표 SSIM/PSNR을 읽습니다.
3. 실험 입력·저장 경로와 분할·증강 순서를 확인합니다.
4. 수정 스크립트는 대상 파일을 다시 쓰므로 별도 사본에서 입력·치환 대상을 확인한 뒤 사용합니다.

대표 CT 3범주와 6단계에서 조건별 PNG 18개를 만듭니다. 원본 포함 10조건이 끝나면 180개입니다. 평균·최댓값·개별 8채널의 총 10패널은 특징 반응을 보여 줍니다.

### LEVEL 2 · 결과를 확인하는 방법

노트북 변형은 실험 조건을 정리한 코드입니다. 설정이 달라졌다고 새 성능 결과가 이미 확보된 것으로 보지 않습니다.

영상 유사도를 맞추는 보정은 분류 성능이나 프라이버시가 동등하다는 보장이 아닙니다. 보정에 사용하는 자료와 시험 자료의 관계도 확인해야 합니다.

연구 2는 원본 98.17%, Block256+sigma0 정확도 98.17%·Privacy Score 49.65점을 보고합니다. 유사도 점수는 복원 공격 성공률이 아닙니다. 연구 1과 모델·조건이 달라 차이의 원인을 하나로 확정하지 않습니다.

### LEVEL 2 · 주의할 범위

| 상황 | 확인할 내용 |
| --- | --- |
| 이름과 역할 | rebuilt·same_settings·metric_matched가 같은 실행이라는 뜻은 아닙니다. |
| 파일 쓰기 | 보조 도구는 지정 노트북을 덮어쓸 수 있으므로 사본과 경로를 준비합니다. |
| 평가 기준 | 유사도 매칭과 독립 분류 시험을 구분합니다. |

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


<a id="semantic-lung-tools-level-3"></a>

### LEVEL 3 · 자료 차수의 수정 도구와 소규모 계산

수정 도구를 쓰기 전 원본 사본·실제 경로·셀 번호·치환 문자열을 확인하세요. 3차에서는 long의 condition·method·n_images·ssim_mean·privacy_score를 방법 요약/pivot과 대조합니다. 4차에서는 학습 결과 JSON/CSV를 읽는 그림 코드와 의료 원영상을 읽는 유사도 코드를 구분하고 빈 노트북을 실행 입력으로 쓰지 않습니다.

<a id="layout18-table-14-row-1"></a>

**자료1차**

**조건·자료**

자료1차

**의미와 확인 방법**

블록·블러각각rebuilt·same_settings·metric_matched의여섯노트북입니다. metric_matched는블록평균SSIM/PSNR에맞는sigma를탐색하며batch4/8·epoch·SWA가변형별로다릅니다. 보조도구는지정노트북을다시씁니다.

<a id="layout18-table-14-row-2"></a>

**자료2차**

**조건·자료**

자료2차

**의미와 확인 방법**

align_experiment_methods.mjs는GPU모니터필드/그래프호환을맞추고build_block_blur_notebook.mjs는Blur사본에서Block→Blur100조합을만듭니다. replaceOrThrow는대상문자열누락시중단하고rollback_original_notebooks.mjs는보관본/지정셀을복원합니다. Node.js와실제입력·출력경로가필요합니다.

<a id="layout18-table-14-row-3"></a>

**자료3차**

**조건·자료**

자료3차

**의미와 확인 방법**

512·seed42의3장입력, Block512·32/Blurσ0·2/조합4의8조건입니다. Privacy Score=((1−SSIM)/2)×100이며PSNR은별도참고값입니다. long·방법요약·조합pivot·best_conditions의4CSV가있습니다. 항등조건0, Block32와B32_S0의35.3667978…은3장계산확인값입니다.

<a id="layout18-table-14-row-4"></a>

**자료4차**

**조건·자료**

자료4차

**의미와 확인 방법**

자료차수/4차/코드의학습·MS-SSIM·도표코드를19쪽원고와연결합니다. pareto_scatter.ipynb는0바이트로실행내용이없습니다. 소규모SSIM표와원고1,097장MS-SSIM을섞지않습니다.


<!-- semantic-revision17:level-3:end -->

[이 수준의 프로젝트 전체 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A83.md) · [같은 수준 프로필](https://github.com/PUVKID/PUVKID/blob/main/docs/읽기안내/레벨3.md)

### LEVEL 3 · 목적과 대상

**이 차수의 목적과 실제 구성**

블록·블러의 rebuilt·same_settings·metric_matched 변형과 노트북 수정 보조 스크립트를 함께 읽는 코드 자료 차수입니다.

<a id="layout18-table-15-row-1"></a>

**여섯 노트북**

**구성**

여섯 노트북

**실제 역할**

블록·블러 각각 rebuilt·same_settings·metric_matched로 나누어 보관합니다.

<a id="layout18-table-15-row-2"></a>

**강도 매칭**

**구성**

강도 매칭

**실제 역할**

metric_matched 블러는 블록 변환의 평균 SSIM/PSNR에 맞는 sigma를 보정하는 함수를 포함합니다.

<a id="layout18-table-15-row-3"></a>

**학습 설정**

**구성**

학습 설정

**실제 역할**

변형별 batch4/8과 단계별 epoch·SWA 시작값이 다르므로 설정 셀을 확인합니다.

<a id="layout18-table-15-row-4"></a>

**수정 도구**

**구성**

수정 도구

**실제 역할**

노트북 생성·콜백·반복 학습·과적합 제어를 수정하는 보조 스크립트가 있습니다.


원고·노트북·저장 결과·대시보드를 차수별로 읽습니다. 과거 논문의 보고값과 현재 Conv1 실행 결과를 합치지 않습니다. 재현에는 원영상·분할·설정·결과 계보가 필요하며 의료 원자료는 공개하지 않습니다.

### LEVEL 3 · 달라진 내용과 차수 관계

블록·블러 실험 노트북의 조건과 보조 도구를 정리한 자료 1차입니다. 논문의 연구 1 번호와 다른 코드 자료 구분입니다.

[직전 단계 전체 비교·구성](../revision-diffs/folder-1.diff) · [전체 파일 크기·해시](../revision-manifests/folder-1.json)

라벨 매핑과 원본 분할을 먼저 확인합니다. 증강은 학습에만 적용하고 검증·시험 원본과 구분합니다. source_class는 원본 범주 폴더 라벨이며 환자·병원·스캐너 식별자가 아닙니다.

### LEVEL 3 · 입력과 실행 조건

| 입력 | 처리 | 출력 |
| --- | --- | --- |
| 블록·블러 노트북 | 설정과 변환 강도 비교 | 실행할 변형 선택 |
| 보정용 영상 | SSIM/PSNR 기반 sigma 탐색 | 블록과 비교할 블러 강도 |
| 노트북 원본 | 지정 셀·문자열 수정 | 다른 설정의 노트북 |

| 항목 | 조건·기본값 |
| --- | --- |
| 입력 크기 | 512 |
| 변환 | 블록 512~1·블러 조건별 sigma |
| 비교 목적 | same_settings와 metric_matched 구분 |
| 수정 도구 | Python 및 Node.js·실제 notebook 경로 |

입력·변환 순서·분할·초기값·학습 예산을 차수별로 확인합니다. Stage 1의 pool1_pool 특징 SSIM은 입력 MS-SSIM과 직접 비교하지 않습니다. 원본 test 선분리와 학습 증강, 큰 sigma 결과 재사용도 확인합니다.

### LEVEL 3 · 처리 절차

1. 여섯 노트북의 설정 셀에서 비교 목적·batch·변환 강도를 확인합니다.
2. metric_matched의 보정 영상 선택과 목표 SSIM/PSNR을 읽습니다.
3. 실험 입력·저장 경로와 분할·증강 순서를 확인합니다.
4. 수정 스크립트는 대상 파일을 다시 쓰므로 별도 사본에서 입력·치환 대상을 확인한 뒤 사용합니다.

실제 완료한 최적 체크포인트와 실행 ID가 같은 결과만 조회합니다. 색은 패널별 최솟값·최댓값으로 표시하므로 다른 패널의 같은 색을 같은 값으로 보지 않습니다. 과거 PNG나 직전 시험 수치를 대기에 재사용하지 않습니다.

### LEVEL 3 · 결과를 확인하는 방법

노트북 변형은 실험 조건을 정리한 코드입니다. 설정이 달라졌다고 새 성능 결과가 이미 확보된 것으로 보지 않습니다.

영상 유사도를 맞추는 보정은 분류 성능이나 프라이버시가 동등하다는 보장이 아닙니다. 보정에 사용하는 자료와 시험 자료의 관계도 확인해야 합니다.

현재 백분율 요약은 소수 첫째 자리 반올림이며 원비율·전체 백분율·정답 수를 함께 확인합니다. 과거 공개 4차의 둘째 자리 버림 설명은 당시 이력으로 두고 현재 규칙과 섞지 않습니다.

### LEVEL 3 · 주의할 범위

| 상황 | 확인할 내용 |
| --- | --- |
| 이름과 역할 | rebuilt·same_settings·metric_matched가 같은 실행이라는 뜻은 아닙니다. |
| 파일 쓰기 | 보조 도구는 지정 노트북을 덮어쓸 수 있으므로 사본과 경로를 준비합니다. |
| 평가 기준 | 유사도 매칭과 독립 분류 시험을 구분합니다. |

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


<a id="semantic-lung-tools-level-4"></a>

### LEVEL 4 · 자료 차수의 수정 도구와 소규모 계산

파일 변경 보조 도구의 JSON/문자열 계약과 실제 학습 코드를 분리합니다. 보정용 영상과 시험 자료의 관계, 치환 실패 시 중단, 복원 대상과 출력 충돌을 확인해야 합니다. 소규모 단일 SSIM 계산과 최종 MS-SSIM 집계는 별도 정의이므로 이름이 같은 Privacy Score를 통합하지 않습니다.

<a id="layout18-table-20-row-1"></a>

**자료1차**

**조건·자료**

자료1차

**의미와 확인 방법**

블록·블러각각rebuilt·same_settings·metric_matched의여섯노트북입니다. metric_matched는블록평균SSIM/PSNR에맞는sigma를탐색하며batch4/8·epoch·SWA가변형별로다릅니다. 보조도구는지정노트북을다시씁니다.

<a id="layout18-table-20-row-2"></a>

**자료2차**

**조건·자료**

자료2차

**의미와 확인 방법**

align_experiment_methods.mjs는GPU모니터필드/그래프호환을맞추고build_block_blur_notebook.mjs는Blur사본에서Block→Blur100조합을만듭니다. replaceOrThrow는대상문자열누락시중단하고rollback_original_notebooks.mjs는보관본/지정셀을복원합니다. Node.js와실제입력·출력경로가필요합니다.

<a id="layout18-table-20-row-3"></a>

**자료3차**

**조건·자료**

자료3차

**의미와 확인 방법**

512·seed42의3장입력, Block512·32/Blurσ0·2/조합4의8조건입니다. Privacy Score=((1−SSIM)/2)×100이며PSNR은별도참고값입니다. long·방법요약·조합pivot·best_conditions의4CSV가있습니다. 항등조건0, Block32와B32_S0의35.3667978…은3장계산확인값입니다.

<a id="layout18-table-20-row-4"></a>

**자료4차**

**조건·자료**

자료4차

**의미와 확인 방법**

자료차수/4차/코드의학습·MS-SSIM·도표코드를19쪽원고와연결합니다. pareto_scatter.ipynb는0바이트로실행내용이없습니다. 소규모SSIM표와원고1,097장MS-SSIM을섞지않습니다.


<!-- semantic-revision17:level-4:end -->

[이 수준의 프로젝트 전체 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A84.md) · [같은 수준 프로필](https://github.com/PUVKID/PUVKID/blob/main/docs/읽기안내/레벨4.md)

### LEVEL 4 · 목적과 대상

**이 차수의 목적과 실제 구성**

블록·블러의 rebuilt·same_settings·metric_matched 변형과 노트북 수정 보조 스크립트를 함께 읽는 코드 자료 차수입니다.

<a id="layout18-table-21-row-1"></a>

**여섯 노트북**

**구성**

여섯 노트북

**실제 역할**

블록·블러 각각 rebuilt·same_settings·metric_matched로 나누어 보관합니다.

<a id="layout18-table-21-row-2"></a>

**강도 매칭**

**구성**

강도 매칭

**실제 역할**

metric_matched 블러는 블록 변환의 평균 SSIM/PSNR에 맞는 sigma를 보정하는 함수를 포함합니다.

<a id="layout18-table-21-row-3"></a>

**학습 설정**

**구성**

학습 설정

**실제 역할**

변형별 batch4/8과 단계별 epoch·SWA 시작값이 다르므로 설정 셀을 확인합니다.

<a id="layout18-table-21-row-4"></a>

**수정 도구**

**구성**

수정 도구

**실제 역할**

노트북 생성·콜백·반복 학습·과적합 제어를 수정하는 보조 스크립트가 있습니다.


입력 변형과 pool1_pool 특징 변형은 개입 위치가 다릅니다. 모델·학습·라벨·분할·점수 정의가 달라 단순 수치 차이를 모델 변경의 인과 효과로 설명할 수 없습니다. 종료 정책 비교도 별도 설계입니다.

### LEVEL 4 · 달라진 내용과 차수 관계

블록·블러 실험 노트북의 조건과 보조 도구를 정리한 자료 1차입니다. 논문의 연구 1 번호와 다른 코드 자료 구분입니다.

[직전 단계 전체 비교·구성](../revision-diffs/folder-1.diff) · [전체 파일 크기·해시](../revision-manifests/folder-1.json)

환자 ID 없는 영상 그룹 분할은 환자 독립 분할의 대체가 아닙니다. 소스별 촬영·압축 차이와 같은 환자의 다른 영상이 성능에 영향을 줄 수 있습니다. 높은 정확도의 원인을 조기 종료로 미리 확정하지 않습니다.

### LEVEL 4 · 입력과 실행 조건

| 입력 | 처리 | 출력 |
| --- | --- | --- |
| 블록·블러 노트북 | 설정과 변환 강도 비교 | 실행할 변형 선택 |
| 보정용 영상 | SSIM/PSNR 기반 sigma 탐색 | 블록과 비교할 블러 강도 |
| 노트북 원본 | 지정 셀·문자열 수정 | 다른 설정의 노트북 |

| 항목 | 조건·기본값 |
| --- | --- |
| 입력 크기 | 512 |
| 변환 | 블록 512~1·블러 조건별 sigma |
| 비교 목적 | same_settings와 metric_matched 구분 |
| 수정 도구 | Python 및 Node.js·실제 notebook 경로 |

Stage 1은 같은 프로세스의 Edge·Cloud 연결이며 실제 원격 전송이 아닙니다. 큰 sigma의 전역 평균 대체, sigma32 결과의 64/128/256 재사용과 Conv2D import 누락 같은 실행 제약을 구분합니다.

### LEVEL 4 · 처리 절차

1. 여섯 노트북의 설정 셀에서 비교 목적·batch·변환 강도를 확인합니다.
2. metric_matched의 보정 영상 선택과 목표 SSIM/PSNR을 읽습니다.
3. 실험 입력·저장 경로와 분할·증강 순서를 확인합니다.
4. 수정 스크립트는 대상 파일을 다시 쓰므로 별도 사본에서 입력·치환 대상을 확인한 뒤 사용합니다.

공개 4차는 학습 2차 대시보드의 로컬 수리 3차 사본입니다. 공개 5차는 실험 4차 고정 100회 비교 코드입니다. 원본 manifest·해시·정확 분할이 다르면 중단합니다.

### LEVEL 4 · 결과를 확인하는 방법

노트북 변형은 실험 조건을 정리한 코드입니다. 설정이 달라졌다고 새 성능 결과가 이미 확보된 것으로 보지 않습니다.

영상 유사도를 맞추는 보정은 분류 성능이나 프라이버시가 동등하다는 보장이 아닙니다. 보정에 사용하는 자료와 시험 자료의 관계도 확인해야 합니다.

Blur sigma256의 51.38%는 다수 클래스 56/109와 같지만 모든 조건의 하한은 아닙니다. 별도 학습한 Block512+sigma256은 46.8%입니다. 조합·단독·별도 학습·시험 분모를 나누어 읽습니다.

### LEVEL 4 · 주의할 범위

| 상황 | 확인할 내용 |
| --- | --- |
| 이름과 역할 | rebuilt·same_settings·metric_matched가 같은 실행이라는 뜻은 아닙니다. |
| 파일 쓰기 | 보조 도구는 지정 노트북을 덮어쓸 수 있으므로 사본과 경로를 준비합니다. |
| 평가 기준 | 유사도 매칭과 독립 분류 시험을 구분합니다. |

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


<a id="semantic-lung-tools-level-5"></a>

### LEVEL 5 · 자료 차수의 수정 도구와 소규모 계산

자료 1~4차의 수락 범위는 변형 코드·변경 도구·3장 8조건 점검·최종 원고 대응입니다. 35.3667978…은 저장표의 축약 표기이며 원정밀도 CSV를 유지합니다. SSIM 매칭은 분류 성능 동등성이나 공격 저항성 동등성을 증명하지 않고 0바이트 파일에서 분석 성과를 추정하지 않습니다.

<a id="layout18-table-26-row-1"></a>

**자료1차**

**조건·자료**

자료1차

**의미와 확인 방법**

블록·블러각각rebuilt·same_settings·metric_matched의여섯노트북입니다. metric_matched는블록평균SSIM/PSNR에맞는sigma를탐색하며batch4/8·epoch·SWA가변형별로다릅니다. 보조도구는지정노트북을다시씁니다.

<a id="layout18-table-26-row-2"></a>

**자료2차**

**조건·자료**

자료2차

**의미와 확인 방법**

align_experiment_methods.mjs는GPU모니터필드/그래프호환을맞추고build_block_blur_notebook.mjs는Blur사본에서Block→Blur100조합을만듭니다. replaceOrThrow는대상문자열누락시중단하고rollback_original_notebooks.mjs는보관본/지정셀을복원합니다. Node.js와실제입력·출력경로가필요합니다.

<a id="layout18-table-26-row-3"></a>

**자료3차**

**조건·자료**

자료3차

**의미와 확인 방법**

512·seed42의3장입력, Block512·32/Blurσ0·2/조합4의8조건입니다. Privacy Score=((1−SSIM)/2)×100이며PSNR은별도참고값입니다. long·방법요약·조합pivot·best_conditions의4CSV가있습니다. 항등조건0, Block32와B32_S0의35.3667978…은3장계산확인값입니다.

<a id="layout18-table-26-row-4"></a>

**자료4차**

**조건·자료**

자료4차

**의미와 확인 방법**

자료차수/4차/코드의학습·MS-SSIM·도표코드를19쪽원고와연결합니다. pareto_scatter.ipynb는0바이트로실행내용이없습니다. 소규모SSIM표와원고1,097장MS-SSIM을섞지않습니다.


<!-- semantic-revision17:level-5:end -->

[전문가 수준 프로젝트 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A85.md) · [같은 수준 프로필](https://github.com/PUVKID/PUVKID/blob/main/docs/읽기안내/레벨5.md)

**기존 전체 상세** — 다음 본문은 이 차수의 원래 방법·조건·결과·실패·한계와 전체 비교입니다. 위 수준의 설명에 필요한 공통 근거도 모두 여기서 확인할 수 있습니다.
<!-- reading-levels17:end -->

**블록·블러의 rebuilt·same_settings·metric_matched 변형과 노트북 수정 보조 스크립트를 함께 읽는 코드 자료 차수입니다.**

분야: 실험 코드 › ResNet50 단독 변환 › 설정 정렬·유사도 매칭

[목적](#purpose) · [기능](#features) · [입출력](#flow) · [구성](#files) · [준비](#setup) · [사용법](#usage) · [결과](#results) · [제약](#limits) · [변경](#changes)

<a name="purpose"></a>

<a id="-이-단계에서-하는-일"></a>

## 연구 목적

같은 설정을 맞추는 비교와 영상 유사도 지표를 맞추는 비교는 목적이 다릅니다. 파일별 batch·블러 강도 결정·경로·콜백의 차이를 먼저 확인해 실행할 노트북을 선택합니다.

<a name="features"></a>

<a id="-주요-기능과-처리-방식"></a>

## 방법과 구현

<a id="layout18-table-27-row-1"></a>

**여섯 노트북**

**구성**

여섯 노트북

**실제 역할**

블록·블러 각각 rebuilt·same_settings·metric_matched로 나누어 보관합니다.

<a id="layout18-table-27-row-2"></a>

**강도 매칭**

**구성**

강도 매칭

**실제 역할**

metric_matched 블러는 블록 변환의 평균 SSIM/PSNR에 맞는 sigma를 보정하는 함수를 포함합니다.

<a id="layout18-table-27-row-3"></a>

**학습 설정**

**구성**

학습 설정

**실제 역할**

변형별 batch4/8과 단계별 epoch·SWA 시작값이 다르므로 설정 셀을 확인합니다.

<a id="layout18-table-27-row-4"></a>

**수정 도구**

**구성**

수정 도구

**실제 역할**

노트북 생성·콜백·반복 학습·과적합 제어를 수정하는 보조 스크립트가 있습니다.


<a name="flow"></a>

<a id="-입력--처리--출력"></a>

## 입력·처리·출력

| 입력 | 처리 | 출력 |
| --- | --- | --- |
| 블록·블러 노트북 | 설정과 변환 강도 비교 | 실행할 변형 선택 |
| 보정용 영상 | SSIM/PSNR 기반 sigma 탐색 | 블록과 비교할 블러 강도 |
| 노트북 원본 | 지정 셀·문자열 수정 | 다른 설정의 노트북 |

<a name="files"></a>

<a id="-파일과-핵심-처리"></a>

## 파일별 역할

<a id="layout18-table-29-row-1"></a>

**항목 1**

**파일**

[1차/block_encryption_resnet50_metric_matched_seq.ipynb](../../1%EC%B0%A8/block_encryption_resnet50_metric_matched_seq.ipynb)

**이용 방법**

설정·함수·실행 셀

<a id="layout18-table-29-row-2"></a>

**[1차/blur_resnet50_metric_matched_seq.ipynb](../../1%EC%B0%A8/blur_resnet50_metric_matched_seq.ipynb)**

**파일**

[1차/blur_resnet50_metric_matched_seq.ipynb](../../1%EC%B0%A8/blur_resnet50_metric_matched_seq.ipynb)

**이용 방법**

설정·함수·실행 셀

<a id="layout18-table-29-row-3"></a>

**[자료차수/1차/create_metric_matched_notebooks.js](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/1%EC%B0%A8/create_metric_matched_notebooks.js)**

**파일**

[자료차수/1차/create_metric_matched_notebooks.js](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/1%EC%B0%A8/create_metric_matched_notebooks.js)

**이용 방법**

해당 단계의 자료

<a id="layout18-table-29-row-4"></a>

**[자료차수/1차/fix_training_repeat_overfit.py](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/1%EC%B0%A8/fix_training_repeat_overfit.py)**

**파일**

[자료차수/1차/fix_training_repeat_overfit.py](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/1%EC%B0%A8/fix_training_repeat_overfit.py)

**이용 방법**

처리 함수와 실행 조건


<a id="-함수셀로-찾아가기"></a>

### 관련 함수와 셀

관련 함수와 셀을 파일별로 정리했습니다. 실행 전 설정과 호출 순서, 출력 경로를 확인하세요.

<a id="layout18-table-30-row-1"></a>

**항목 1**

**파일**

[1차/block_encryption_resnet50_metric_matched_seq.ipynb](../../1%EC%B0%A8/block_encryption_resnet50_metric_matched_seq.ipynb)

**핵심 정의**

셀 6: `gpu_status` · `GPUMonitorCallback` · `__init__` · `on_epoch_end`<br>셀 8: `set_reproducible` · `list_class_dirs` · `list_image_files`<br>셀 10: `block_scramble` · `generate_block_dataset`<br>셀 12: `oversample_dir`<br>셀 14: `prepare_split`<br>셀 16: `_deterministic` · `get_paths_labels` · `load_image` · `augment_train` · `mixup_batch` · `cutmix_batch` · `apply_mixup` · `apply_cutmix`<br>셀 18: `focal_loss` · `loss_fn` · `CosineAnnealingWarmRestart` · `__init__` · `on_epoch_begin` · `SWACallback` · `__init__` · `on_epoch_end`

<a id="layout18-table-30-row-2"></a>

**[1차/blur_resnet50_metric_matched_seq.ipynb](../../1%EC%B0%A8/blur_resnet50_metric_matched_seq.ipynb)**

**파일**

[1차/blur_resnet50_metric_matched_seq.ipynb](../../1%EC%B0%A8/blur_resnet50_metric_matched_seq.ipynb)

**핵심 정의**

셀 6: `gpu_status` · `GPUMonitorCallback` · `__init__` · `on_epoch_end`<br>셀 8: `set_reproducible` · `list_class_dirs` · `list_image_files`<br>셀 10: `apply_gaussian_blur` · `block_scramble_for_calibration` · `generate_blur_dataset` · `calibration_image_paths` · `load_metric_image` · `average_similarity_metrics` · `choose_sigma_for_target` · `distance`<br>셀 12: `oversample_dir`<br>셀 14: `prepare_split`<br>셀 16: `_deterministic` · `get_paths_labels` · `load_image` · `augment_train` · `mixup_batch` · `cutmix_batch` · `apply_mixup` · `apply_cutmix`<br>셀 18: `focal_loss` · `loss_fn` · `CosineAnnealingWarmRestart` · `__init__` · `on_epoch_begin` · `SWACallback` · `__init__` · `on_epoch_end`

<a id="layout18-table-30-row-3"></a>

**[자료차수/1차/create_metric_matched_notebooks.js](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/1%EC%B0%A8/create_metric_matched_notebooks.js)**

**파일**

[자료차수/1차/create_metric_matched_notebooks.js](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/1%EC%B0%A8/create_metric_matched_notebooks.js)

**핵심 정의**

소스: `asText` · `asSourceArray` · `setCell` · `set_reproducible` · `list_class_dirs` · `list_image_files` · `set_reproducible` · `list_class_dirs`

<a id="layout18-table-30-row-4"></a>

**[자료차수/1차/fix_training_repeat_overfit.py](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/1%EC%B0%A8/fix_training_repeat_overfit.py)**

**파일**

[자료차수/1차/fix_training_repeat_overfit.py](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/1%EC%B0%A8/fix_training_repeat_overfit.py)

**핵심 정의**

소스: `cell_text` · `set_cell_text` · `replace_once` · `patch_notebook` · `OverfitControlCallback` · `__init__` · `on_epoch_end`


<a name="setup"></a>

<a id="️-환경과-설정"></a>

## 실행 환경과 설정

| 항목 | 조건·기본값 |
| --- | --- |
| 입력 크기 | 512 |
| 변환 | 블록 512~1·블러 조건별 sigma |
| 비교 목적 | same_settings와 metric_matched 구분 |
| 수정 도구 | Python 및 Node.js·실제 notebook 경로 |

<a name="usage"></a>

<a id="-준비와-사용-순서"></a>

## 실행 순서

1. 여섯 노트북의 설정 셀에서 비교 목적·batch·변환 강도를 확인합니다.
2. metric_matched의 보정 영상 선택과 목표 SSIM/PSNR을 읽습니다.
3. 실험 입력·저장 경로와 분할·증강 순서를 확인합니다.
4. 수정 스크립트는 대상 파일을 다시 쓰므로 별도 사본에서 입력·치환 대상을 확인한 뒤 사용합니다.

<a name="results"></a>

<a id="-결과를-읽는-방법"></a>

## 결과와 해석

노트북 변형은 실험 조건을 정리한 코드입니다. 설정이 달라졌다고 새 성능 결과가 이미 확보된 것으로 보지 않습니다.

영상 유사도를 맞추는 보정은 분류 성능이나 프라이버시가 동등하다는 보장이 아닙니다. 보정에 사용하는 자료와 시험 자료의 관계도 확인해야 합니다.

<a name="limits"></a>

<a id="️-알려진-제약과-확인-지점"></a>

## 제약과 확인 사항

| 상황 | 확인할 내용 |
| --- | --- |
| 이름과 역할 | rebuilt·same_settings·metric_matched가 같은 실행이라는 뜻은 아닙니다. |
| 파일 쓰기 | 보조 도구는 지정 노트북을 덮어쓸 수 있으므로 사본과 경로를 준비합니다. |
| 평가 기준 | 유사도 매칭과 독립 분류 시험을 구분합니다. |

<a name="changes"></a>

<a id="-이전-단계와의-변화"></a>

## 직전 단계와 비교

블록·블러 실험 노트북의 조건과 보조 도구를 정리한 자료 1차입니다. 논문의 연구 1 번호와 다른 코드 자료 구분입니다.

[직전 단계 전체 비교·구성](../revision-diffs/folder-1.diff) · [전체 파일 크기·해시](../revision-manifests/folder-1.json)

<details>
<summary>이 단계의 파일 기록과 전체 해시</summary>

아래 내용는 해당 단계가 기록될 당시의 파일 정보입니다. 현재 첨부는 [프로젝트 자료 안내](../PAPERS.md)에서 확인할 수 있습니다.

<a id="layout18-table-33-row-1"></a>

**항목 1**

**파일**

[자료차수/1차/block_encryption_resnet50_metric_matched_seq.ipynb](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/1%EC%B0%A8/block_encryption_resnet50_metric_matched_seq.ipynb)

**종류**

.ipynb

**바이트**

60093

**SHA-256**

`066b6f71ee4c438ea16e481f2182166ef777cf77b0759439945aeb7cdc12d5c1`

<a id="layout18-table-33-row-2"></a>

**항목 2**

**파일**

[자료차수/1차/block_encryption_resnet50_rebuilt_KO.ipynb](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/1%EC%B0%A8/block_encryption_resnet50_rebuilt_KO.ipynb)

**종류**

.ipynb

**바이트**

93336

**SHA-256**

`e4526e11284c362e99634a7f3a7cd2ee3e96c79b25a8e1970d57eba31669de89`

<a id="layout18-table-33-row-3"></a>

**항목 3**

**파일**

[자료차수/1차/block_encryption_resnet50_same_settings_seq.ipynb](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/1%EC%B0%A8/block_encryption_resnet50_same_settings_seq.ipynb)

**종류**

.ipynb

**바이트**

60070

**SHA-256**

`e7ee462efd677bce07208fb329a0b16add22b58598dc2e7dff71698c4b5887d6`

<a id="layout18-table-33-row-4"></a>

**항목 4**

**파일**

[자료차수/1차/blur_resnet50_metric_matched_seq.ipynb](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/1%EC%B0%A8/blur_resnet50_metric_matched_seq.ipynb)

**종류**

.ipynb

**바이트**

72937

**SHA-256**

`ca47cc04346b01931e768101723d2e5c7f9a8d6fc878c53bfba0178331d2dfdc`

<a id="layout18-table-33-row-5"></a>

**[자료차수/1차/blur_resnet50_rebuilt_KO.ipynb](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/1%EC%B0%A8/blur_resnet50_rebuilt_KO.ipynb)**

**파일**

[자료차수/1차/blur_resnet50_rebuilt_KO.ipynb](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/1%EC%B0%A8/blur_resnet50_rebuilt_KO.ipynb)

**종류**

.ipynb

**바이트**

106507

**SHA-256**

`2667478acda4fd06ecd4dfb1126540af313490a24dd5b57bc05d670c4cd19819`

<a id="layout18-table-33-row-6"></a>

**[자료차수/1차/blur_resnet50_same_settings_seq.ipynb](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/1%EC%B0%A8/blur_resnet50_same_settings_seq.ipynb)**

**파일**

[자료차수/1차/blur_resnet50_same_settings_seq.ipynb](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/1%EC%B0%A8/blur_resnet50_same_settings_seq.ipynb)

**종류**

.ipynb

**바이트**

63986

**SHA-256**

`847de605b3686cbaf559cd7c95402b2cded9a2be7b8b536339ddb8ca93acfaa6`

<a id="layout18-table-33-row-7"></a>

**[자료차수/1차/create_metric_matched_notebooks.js](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/1%EC%B0%A8/create_metric_matched_notebooks.js)**

**파일**

[자료차수/1차/create_metric_matched_notebooks.js](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/1%EC%B0%A8/create_metric_matched_notebooks.js)

**종류**

.js

**바이트**

18124

**SHA-256**

`f40132eda3c769d267c036941a23db74c2b4fab28e9fbb3cc3c57354b3f68973`

<a id="layout18-table-33-row-8"></a>

**[자료차수/1차/fix_pseudo_callbacks.py](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/1%EC%B0%A8/fix_pseudo_callbacks.py)**

**파일**

[자료차수/1차/fix_pseudo_callbacks.py](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/1%EC%B0%A8/fix_pseudo_callbacks.py)

**종류**

.py

**바이트**

1725

**SHA-256**

`b12fd56841636cc008ee9baecc3d8b237731c2cc4af12802b2487cb3c94a968d`

<a id="layout18-table-33-row-9"></a>

**[자료차수/1차/fix_training_repeat_overfit.py](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/1%EC%B0%A8/fix_training_repeat_overfit.py)**

**파일**

[자료차수/1차/fix_training_repeat_overfit.py](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/1%EC%B0%A8/fix_training_repeat_overfit.py)

**종류**

.py

**바이트**

6714

**SHA-256**

`a8e3cfd2fc9e97297f213c60e5d006dd731edda15f05785ab46c607f90353510`

<a id="layout18-table-33-row-10"></a>

**[자료차수/1차/patch_blur_block_notebooks.js](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/1%EC%B0%A8/patch_blur_block_notebooks.js)**

**파일**

[자료차수/1차/patch_blur_block_notebooks.js](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/1%EC%B0%A8/patch_blur_block_notebooks.js)

**종류**

.js

**바이트**

36556

**SHA-256**

`700d96b1a98589cc1e8254660463a77755cf54ab521dff6f7aa7e280a98fad48`

<a id="layout18-table-33-row-11"></a>

**[자료차수/1차/rebuild_blur_ko_notebook.py](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/1%EC%B0%A8/rebuild_blur_ko_notebook.py)**

**파일**

[자료차수/1차/rebuild_blur_ko_notebook.py](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/1%EC%B0%A8/rebuild_blur_ko_notebook.py)

**종류**

.py

**바이트**

45698

**SHA-256**

`47761fbbefedbb8524b8e97d2527d55f82c51fc9e47f88a7a26275822f0bef6a`


</details>

---

[프로젝트](../../README.md) · [전체 차수](../REVISION_INDEX.md) · [자료 폴더](../../1%EC%B0%A8) · [폴더 2차](folder-2.md)

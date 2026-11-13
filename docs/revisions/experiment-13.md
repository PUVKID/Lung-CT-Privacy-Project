<a id="️-원본-실험--조직영상-화면과-학습-노트북"></a>

# 원본 실험 · 조직영상 화면과 학습 노트북

<!-- reading-levels17:start -->
**읽기 수준 선택** · [LEVEL 1 - Beginner](#reading-level-1) · [LEVEL 2 - Explorer](#reading-level-2) · [LEVEL 3 - Practitioner](#reading-level-3) · [LEVEL 4 - Advanced](#reading-level-4) · [LEVEL 5 - Expert](#reading-level-5)

<a id="reading-level-1"></a>

## LEVEL 1 - Beginner

<!-- semantic-revision17:level-1:start -->

<a id="semantic-lung-legacy-level-1"></a>

### LEVEL 1 · 초기 조직영상 앱과 추가 학습 코드

조직영상은 현미경으로 보는 조직 사진이고 CT와 다른 입력입니다. 화면의 다섯 이름과 학습 파일의 세 이름이 달라 같은 모델이라고 바로 연결할 수 없습니다. 추가 노트북에는 여러 실험 셀이 모여 있으므로 모두 이어 실행하는 하나의 완성 학습으로 보지 않습니다.

<a id="layout18-table-1-row-1"></a>

**초기화면**

**조건·자료**

초기화면

**의미와 확인 방법**

Streamlit이업로드영상을224×224·255로나눔·배치차원추가후Model.h5의대장선암/대장정상/폐선암/폐정상/폐편평상피암5라벨확률을텍스트와원형그래프로보입니다. Train.ipynb는MobileNetV2 3클래스·224·batch16·10epoch여서모델대응을따로확인합니다.

<a id="layout18-table-1-row-2"></a>

**추가셀**

**조건·자료**

추가셀

**의미와 확인 방법**

Train.ipynb셀0은조직영상5클래스, 셀1·2는EfficientNetV2-S CT블록/블러, 셀3~5는MobileNetV2/풀링비교입니다. 코드별입력224/512와클래스수를확인합니다.

<a id="layout18-table-1-row-3"></a>

**계산과제약**

**조건·자료**

계산과제약

**의미와 확인 방법**

SSIM·PSNR·MS-SSIM·DSSIM변형과저장분류JSON/유사도CSV를그리는코드를구분합니다. 100−accuracy·특징수비율security는공격저항성실측이아니며첫학습셀끝의Markdown백틱·문법·사본별설정을확인합니다.


<!-- semantic-revision17:level-1:end -->

[이 수준의 프로젝트 전체 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A81.md) · [같은 수준 프로필](https://github.com/PUVKID/PUVKID/blob/main/docs/읽기안내/레벨1.md)

### LEVEL 1 · 목적과 대상

**이 차수의 목적과 실제 구성**

Streamlit 화면은 업로드 영상을 224×224로 전처리해 Model.h5의 조직영상 5라벨 예측을 표시합니다. 함께 있는 학습 노트북은 MobileNetV2의 3클래스 구성이어서 그대로 같은 모델로 간주하면 안 됩니다.

<a id="layout18-table-2-row-1"></a>

**전처리**

**구성**

전처리

**실제 역할**

preprocess_image가 영상을 224×224로 맞추고 255로 나누어 배치 차원을 추가합니다.

<a id="layout18-table-2-row-2"></a>

**5라벨 화면**

**구성**

5라벨 화면

**실제 역할**

대장선암·대장정상·폐선암·폐정상·폐편평상피암의 예측 확률을 표시합니다.

<a id="layout18-table-2-row-3"></a>

**그래프**

**구성**

그래프

**실제 역할**

예측 확률을 텍스트와 원형 그래프로 보여 줍니다.

<a id="layout18-table-2-row-4"></a>

**학습 사본**

**구성**

학습 사본

**실제 역할**

Train.ipynb의 MobileNetV2 3클래스·224·batch16·10epoch와 화면의 5라벨을 구분합니다.


CT 사진을 흐리게 하거나 블록으로 재배열했을 때 분류 결과와 영상 유사도가 어떻게 달라지는지 살펴봅니다. 입력 사진을 바꾸는 연구와 모델 내부의 첫 합성곱 특징을 흐리는 실험이 함께 있습니다. **논문 연구 번호·공개 코드 차수·실제 학습 차수는 다릅니다.**

### LEVEL 1 · 달라진 내용과 차수 관계

초기 화면과 학습 코드를 보관한 기본 자료입니다. 후속 ResNet50 입력·특징 변환 실험과 별도로 읽습니다.

[직전 단계 전체 비교·구성](../revision-diffs/experiment-13.diff) · [전체 파일 크기·해시](../revision-manifests/experiment-13.json)

사진의 모양이 바뀌었어도 분류기가 정답을 잘 맞추는지, 얼마나 비슷한 정보를 남기는지 따로 봅니다. OK는 양성+정상, NG는 악성입니다. 사진 수·독립 환자 수·반복 학습 표본 수를 섞지 않습니다.

### LEVEL 1 · 입력과 실행 조건

| 입력 | 처리 | 출력 |
| --- | --- | --- |
| 업로드 조직영상 | 224×224·정규화 | 모델 입력 |
| Model.h5 | 예측 벡터와 5라벨 연결 | 클래스별 확률 |
| 예측 확률 | 텍스트·원형 그래프 | 연구용 화면 |

| 항목 | 조건·기본값 |
| --- | --- |
| 환경 | Streamlit·TensorFlow·NumPy·Matplotlib |
| 입력 크기 | 224×224 |
| 모델 | 화면은 Model.h5와 5라벨 |
| 학습 노트북 | 3클래스 MobileNetV2·별도 모델 대응 확인 |

입력 사진에 블러·블록을 적용하는 경로와 모델이 뽑은 특징에 블러를 적용하는 경로를 나눕니다. 특징은 사진에서 찾은 선·무늬의 반응입니다. 그 색이 병변 위치나 악성 확률을 뜻하지 않습니다.

### LEVEL 1 · 처리 절차

1. main.py의 모델 경로와 라벨 순서를 확인합니다.
2. 모델 출력 차원이 화면의 5라벨과 같은지 확인합니다.
3. 환경과 일치하는 모델을 준비하고 해당 폴더에서 Streamlit 앱을 엽니다.
4. 업로드 영상의 전처리와 확률 표시를 읽으며 학습 노트북의 모델과 혼합하지 않습니다.

전체 차수 표에서 읽을 연구를 고릅니다. 노트북을 여는 것과 새 학습 시작은 다릅니다. 대시보드에서 같은 강도의 사진·곡선·시험 수치를 함께 읽되 미완료 조건은 미측정으로 남깁니다.

### LEVEL 1 · 결과를 확인하는 방법

화면의 확률은 지정한 모델의 출력입니다. 5라벨 화면과 3클래스 학습 파일은 같은 모델이라는 근거가 필요합니다.

이 초기 조직영상 코드는 후속 CT 비식별화 실험과 입력·모델이 다릅니다. 실제 진단 결과를 제공하는 자료로 해석하지 않습니다.

연구 1의 원고 보고 정확도는 원본 92.5%, sigma32 블러 53.3%, Block32 재배열 79.2%입니다. 이는 당시 논문의 값이며 현재 Conv1 예비실험의 결과로 바꾸지 않습니다.

### LEVEL 1 · 주의할 범위

| 상황 | 확인할 내용 |
| --- | --- |
| 모델 불일치 | 5라벨 화면과 3클래스 학습의 모델·라벨 대응을 먼저 확인합니다. |
| 입력 범위 | 조직영상과 CT를 구분합니다. |
| 사용 목적 | 연구용 예측 화면이며 임상 진단 승인 자료가 아닙니다. |

환자 ID가 없어 같은 사람의 다른 사진이 섞였는지 모두 확인할 수 없습니다. 높은 정확도가 임상 성능이나 프라이버시 효과를 보장하지 않습니다. **반복 표본 5,000개를 독립 환자 5,000명으로 세지 않습니다.**

[표·코드·실행 설정·파일 전체 비교를 포함한 공통 상세](#reading-level-5)

<a id="reading-level-2"></a>

## LEVEL 2 - Explorer

<!-- semantic-revision17:level-2:start -->

<a id="semantic-lung-legacy-level-2"></a>

### LEVEL 2 · 초기 조직영상 앱과 추가 학습 코드

화면은 업로드→크기 조정→정규화→모델 확률→문자/원형 그래프로 이어집니다. 학습 셀의 모델과 클래스 구성이 화면과 맞아야 출력을 올바르게 해석할 수 있습니다. 유사도와 정확도를 뒤집은 security 표현은 계산식의 의미가 다릅니다.

<a id="layout18-table-6-row-1"></a>

**초기화면**

**조건·자료**

초기화면

**의미와 확인 방법**

Streamlit이업로드영상을224×224·255로나눔·배치차원추가후Model.h5의대장선암/대장정상/폐선암/폐정상/폐편평상피암5라벨확률을텍스트와원형그래프로보입니다. Train.ipynb는MobileNetV2 3클래스·224·batch16·10epoch여서모델대응을따로확인합니다.

<a id="layout18-table-6-row-2"></a>

**추가셀**

**조건·자료**

추가셀

**의미와 확인 방법**

Train.ipynb셀0은조직영상5클래스, 셀1·2는EfficientNetV2-S CT블록/블러, 셀3~5는MobileNetV2/풀링비교입니다. 코드별입력224/512와클래스수를확인합니다.

<a id="layout18-table-6-row-3"></a>

**계산과제약**

**조건·자료**

계산과제약

**의미와 확인 방법**

SSIM·PSNR·MS-SSIM·DSSIM변형과저장분류JSON/유사도CSV를그리는코드를구분합니다. 100−accuracy·특징수비율security는공격저항성실측이아니며첫학습셀끝의Markdown백틱·문법·사본별설정을확인합니다.


<!-- semantic-revision17:level-2:end -->

[이 수준의 프로젝트 전체 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A82.md) · [같은 수준 프로필](https://github.com/PUVKID/PUVKID/blob/main/docs/읽기안내/레벨2.md)

### LEVEL 2 · 목적과 대상

**이 차수의 목적과 실제 구성**

Streamlit 화면은 업로드 영상을 224×224로 전처리해 Model.h5의 조직영상 5라벨 예측을 표시합니다. 함께 있는 학습 노트북은 MobileNetV2의 3클래스 구성이어서 그대로 같은 모델로 간주하면 안 됩니다.

<a id="layout18-table-7-row-1"></a>

**전처리**

**구성**

전처리

**실제 역할**

preprocess_image가 영상을 224×224로 맞추고 255로 나누어 배치 차원을 추가합니다.

<a id="layout18-table-7-row-2"></a>

**5라벨 화면**

**구성**

5라벨 화면

**실제 역할**

대장선암·대장정상·폐선암·폐정상·폐편평상피암의 예측 확률을 표시합니다.

<a id="layout18-table-7-row-3"></a>

**그래프**

**구성**

그래프

**실제 역할**

예측 확률을 텍스트와 원형 그래프로 보여 줍니다.

<a id="layout18-table-7-row-4"></a>

**학습 사본**

**구성**

학습 사본

**실제 역할**

Train.ipynb의 MobileNetV2 3클래스·224·batch16·10epoch와 화면의 5라벨을 구분합니다.


입력 변형 연구 1·2, 특징 블러 Stage 1, Conv1 OK/NG 예비실험을 구분합니다. 블러는 무늬를 부드럽게 하고 블록 재배열은 위치를 섞습니다. 분류 정확도와 유사도 기반 Privacy Score는 서로 다른 양을 측정합니다.

### LEVEL 2 · 달라진 내용과 차수 관계

초기 화면과 학습 코드를 보관한 기본 자료입니다. 후속 ResNet50 입력·특징 변환 실험과 별도로 읽습니다.

[직전 단계 전체 비교·구성](../revision-diffs/experiment-13.diff) · [전체 파일 크기·해시](../revision-manifests/experiment-13.json)

이전 연구는 정상·양성·악성 3분류, Conv1은 OK/NG 이진 분류입니다. 원본 1,097장은 양성 120·정상 416·악성 561장입니다. 클래스당 매 epoch 5,000표본은 반복·온라인 증강이며 독립 영상 5,000장이 아닙니다.

### LEVEL 2 · 입력과 실행 조건

| 입력 | 처리 | 출력 |
| --- | --- | --- |
| 업로드 조직영상 | 224×224·정규화 | 모델 입력 |
| Model.h5 | 예측 벡터와 5라벨 연결 | 클래스별 확률 |
| 예측 확률 | 텍스트·원형 그래프 | 연구용 화면 |

| 항목 | 조건·기본값 |
| --- | --- |
| 환경 | Streamlit·TensorFlow·NumPy·Matplotlib |
| 입력 크기 | 224×224 |
| 모델 | 화면은 Model.h5와 5라벨 |
| 학습 노트북 | 3클래스 MobileNetV2·별도 모델 대응 확인 |

연구 1은 512×512 입력에 두 변환을 각각 적용해 정확도·ROC-AUC·혼동행렬을 봅니다. 연구 2는 Blur→Block·Block→Blur 조합과 입력 MS-SSIM을 비교합니다. Conv1은 첫 합성곱 특징을 바꾼 뒤 분류합니다.

### LEVEL 2 · 처리 절차

1. main.py의 모델 경로와 라벨 순서를 확인합니다.
2. 모델 출력 차원이 화면의 5라벨과 같은지 확인합니다.
3. 환경과 일치하는 모델을 준비하고 해당 폴더에서 Streamlit 앱을 엽니다.
4. 업로드 영상의 전처리와 확률 표시를 읽으며 학습 노트북의 모델과 혼합하지 않습니다.

대표 CT 3범주와 6단계에서 조건별 PNG 18개를 만듭니다. 원본 포함 10조건이 끝나면 180개입니다. 평균·최댓값·개별 8채널의 총 10패널은 특징 반응을 보여 줍니다.

### LEVEL 2 · 결과를 확인하는 방법

화면의 확률은 지정한 모델의 출력입니다. 5라벨 화면과 3클래스 학습 파일은 같은 모델이라는 근거가 필요합니다.

이 초기 조직영상 코드는 후속 CT 비식별화 실험과 입력·모델이 다릅니다. 실제 진단 결과를 제공하는 자료로 해석하지 않습니다.

연구 2는 원본 98.17%, Block256+sigma0 정확도 98.17%·Privacy Score 49.65점을 보고합니다. 유사도 점수는 복원 공격 성공률이 아닙니다. 연구 1과 모델·조건이 달라 차이의 원인을 하나로 확정하지 않습니다.

### LEVEL 2 · 주의할 범위

| 상황 | 확인할 내용 |
| --- | --- |
| 모델 불일치 | 5라벨 화면과 3클래스 학습의 모델·라벨 대응을 먼저 확인합니다. |
| 입력 범위 | 조직영상과 CT를 구분합니다. |
| 사용 목적 | 연구용 예측 화면이며 임상 진단 승인 자료가 아닙니다. |

영상 단위 예비실험의 한계, 조건별 학습·결과 재사용, 입력과 특징의 다른 점수 정의를 함께 읽습니다. 새 종료 정책 실험의 준비와 완료도 구분합니다.

[표·코드·실행 설정·파일 전체 비교를 포함한 공통 상세](#reading-level-5)

<a id="reading-level-3"></a>

## LEVEL 3 - Practitioner

<!-- semantic-revision17:level-3:start -->

<a id="semantic-lung-legacy-level-3"></a>

### LEVEL 3 · 초기 조직영상 앱과 추가 학습 코드

앱을 읽기 전 Model.h5의 출력 차원·라벨 순서와 학습 노트북의 실제 구성을 대조하세요. 추가 노트북에서는 사용할 셀을 선택하고 입력 크기·자료 종류·가중치·문법을 확인합니다. 그래프는 저장 JSON/CSV의 어느 값을 입력받는지 확인하며 실제 진단으로 사용했다고 보고하지 않습니다.

<a id="layout18-table-11-row-1"></a>

**초기화면**

**조건·자료**

초기화면

**의미와 확인 방법**

Streamlit이업로드영상을224×224·255로나눔·배치차원추가후Model.h5의대장선암/대장정상/폐선암/폐정상/폐편평상피암5라벨확률을텍스트와원형그래프로보입니다. Train.ipynb는MobileNetV2 3클래스·224·batch16·10epoch여서모델대응을따로확인합니다.

<a id="layout18-table-11-row-2"></a>

**추가셀**

**조건·자료**

추가셀

**의미와 확인 방법**

Train.ipynb셀0은조직영상5클래스, 셀1·2는EfficientNetV2-S CT블록/블러, 셀3~5는MobileNetV2/풀링비교입니다. 코드별입력224/512와클래스수를확인합니다.

<a id="layout18-table-11-row-3"></a>

**계산과제약**

**조건·자료**

계산과제약

**의미와 확인 방법**

SSIM·PSNR·MS-SSIM·DSSIM변형과저장분류JSON/유사도CSV를그리는코드를구분합니다. 100−accuracy·특징수비율security는공격저항성실측이아니며첫학습셀끝의Markdown백틱·문법·사본별설정을확인합니다.


<!-- semantic-revision17:level-3:end -->

[이 수준의 프로젝트 전체 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A83.md) · [같은 수준 프로필](https://github.com/PUVKID/PUVKID/blob/main/docs/읽기안내/레벨3.md)

### LEVEL 3 · 목적과 대상

**이 차수의 목적과 실제 구성**

Streamlit 화면은 업로드 영상을 224×224로 전처리해 Model.h5의 조직영상 5라벨 예측을 표시합니다. 함께 있는 학습 노트북은 MobileNetV2의 3클래스 구성이어서 그대로 같은 모델로 간주하면 안 됩니다.

<a id="layout18-table-12-row-1"></a>

**전처리**

**구성**

전처리

**실제 역할**

preprocess_image가 영상을 224×224로 맞추고 255로 나누어 배치 차원을 추가합니다.

<a id="layout18-table-12-row-2"></a>

**5라벨 화면**

**구성**

5라벨 화면

**실제 역할**

대장선암·대장정상·폐선암·폐정상·폐편평상피암의 예측 확률을 표시합니다.

<a id="layout18-table-12-row-3"></a>

**그래프**

**구성**

그래프

**실제 역할**

예측 확률을 텍스트와 원형 그래프로 보여 줍니다.

<a id="layout18-table-12-row-4"></a>

**학습 사본**

**구성**

학습 사본

**실제 역할**

Train.ipynb의 MobileNetV2 3클래스·224·batch16·10epoch와 화면의 5라벨을 구분합니다.


원고·노트북·저장 결과·대시보드를 차수별로 읽습니다. 과거 논문의 보고값과 현재 Conv1 실행 결과를 합치지 않습니다. 재현에는 원영상·분할·설정·결과 계보가 필요하며 의료 원자료는 공개하지 않습니다.

### LEVEL 3 · 달라진 내용과 차수 관계

초기 화면과 학습 코드를 보관한 기본 자료입니다. 후속 ResNet50 입력·특징 변환 실험과 별도로 읽습니다.

[직전 단계 전체 비교·구성](../revision-diffs/experiment-13.diff) · [전체 파일 크기·해시](../revision-manifests/experiment-13.json)

라벨 매핑과 원본 분할을 먼저 확인합니다. 증강은 학습에만 적용하고 검증·시험 원본과 구분합니다. source_class는 원본 범주 폴더 라벨이며 환자·병원·스캐너 식별자가 아닙니다.

### LEVEL 3 · 입력과 실행 조건

| 입력 | 처리 | 출력 |
| --- | --- | --- |
| 업로드 조직영상 | 224×224·정규화 | 모델 입력 |
| Model.h5 | 예측 벡터와 5라벨 연결 | 클래스별 확률 |
| 예측 확률 | 텍스트·원형 그래프 | 연구용 화면 |

| 항목 | 조건·기본값 |
| --- | --- |
| 환경 | Streamlit·TensorFlow·NumPy·Matplotlib |
| 입력 크기 | 224×224 |
| 모델 | 화면은 Model.h5와 5라벨 |
| 학습 노트북 | 3클래스 MobileNetV2·별도 모델 대응 확인 |

입력·변환 순서·분할·초기값·학습 예산을 차수별로 확인합니다. Stage 1의 pool1_pool 특징 SSIM은 입력 MS-SSIM과 직접 비교하지 않습니다. 원본 test 선분리와 학습 증강, 큰 sigma 결과 재사용도 확인합니다.

### LEVEL 3 · 처리 절차

1. main.py의 모델 경로와 라벨 순서를 확인합니다.
2. 모델 출력 차원이 화면의 5라벨과 같은지 확인합니다.
3. 환경과 일치하는 모델을 준비하고 해당 폴더에서 Streamlit 앱을 엽니다.
4. 업로드 영상의 전처리와 확률 표시를 읽으며 학습 노트북의 모델과 혼합하지 않습니다.

실제 완료한 최적 체크포인트와 실행 ID가 같은 결과만 조회합니다. 색은 패널별 최솟값·최댓값으로 표시하므로 다른 패널의 같은 색을 같은 값으로 보지 않습니다. 과거 PNG나 직전 시험 수치를 대기에 재사용하지 않습니다.

### LEVEL 3 · 결과를 확인하는 방법

화면의 확률은 지정한 모델의 출력입니다. 5라벨 화면과 3클래스 학습 파일은 같은 모델이라는 근거가 필요합니다.

이 초기 조직영상 코드는 후속 CT 비식별화 실험과 입력·모델이 다릅니다. 실제 진단 결과를 제공하는 자료로 해석하지 않습니다.

현재 백분율 요약은 소수 첫째 자리 반올림이며 원비율·전체 백분율·정답 수를 함께 확인합니다. 과거 공개 4차의 둘째 자리 버림 설명은 당시 이력으로 두고 현재 규칙과 섞지 않습니다.

### LEVEL 3 · 주의할 범위

| 상황 | 확인할 내용 |
| --- | --- |
| 모델 불일치 | 5라벨 화면과 3클래스 학습의 모델·라벨 대응을 먼저 확인합니다. |
| 입력 범위 | 조직영상과 CT를 구분합니다. |
| 사용 목적 | 연구용 예측 화면이며 임상 진단 승인 자료가 아닙니다. |

원본과 분할 manifest의 실제 값은 자신의 로컬 자료로 준비해야 합니다. 공개 예제만으로 기준 비교가 동작하지 않습니다. 미완료 조건과 정의 불가 지표를 보기 좋은 값으로 채우지 않습니다.

[표·코드·실행 설정·파일 전체 비교를 포함한 공통 상세](#reading-level-5)

<a id="reading-level-4"></a>

## LEVEL 4 - Advanced

<!-- semantic-revision17:level-4:start -->

<a id="semantic-lung-legacy-level-4"></a>

### LEVEL 4 · 초기 조직영상 앱과 추가 학습 코드

전처리 함수·모델 예측·화면 라벨의 경계를 검토하고 5라벨 UI와 3클래스 학습의 불일치를 보존합니다. 추가 셀들은 서로 다른 모델/풀링/입력 크기를 갖는 자료 모음이며 동일 학습 상태를 공유한다고 가정하지 않습니다.

<a id="layout18-table-16-row-1"></a>

**초기화면**

**조건·자료**

초기화면

**의미와 확인 방법**

Streamlit이업로드영상을224×224·255로나눔·배치차원추가후Model.h5의대장선암/대장정상/폐선암/폐정상/폐편평상피암5라벨확률을텍스트와원형그래프로보입니다. Train.ipynb는MobileNetV2 3클래스·224·batch16·10epoch여서모델대응을따로확인합니다.

<a id="layout18-table-16-row-2"></a>

**추가셀**

**조건·자료**

추가셀

**의미와 확인 방법**

Train.ipynb셀0은조직영상5클래스, 셀1·2는EfficientNetV2-S CT블록/블러, 셀3~5는MobileNetV2/풀링비교입니다. 코드별입력224/512와클래스수를확인합니다.

<a id="layout18-table-16-row-3"></a>

**계산과제약**

**조건·자료**

계산과제약

**의미와 확인 방법**

SSIM·PSNR·MS-SSIM·DSSIM변형과저장분류JSON/유사도CSV를그리는코드를구분합니다. 100−accuracy·특징수비율security는공격저항성실측이아니며첫학습셀끝의Markdown백틱·문법·사본별설정을확인합니다.


<!-- semantic-revision17:level-4:end -->

[이 수준의 프로젝트 전체 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A84.md) · [같은 수준 프로필](https://github.com/PUVKID/PUVKID/blob/main/docs/읽기안내/레벨4.md)

### LEVEL 4 · 목적과 대상

**이 차수의 목적과 실제 구성**

Streamlit 화면은 업로드 영상을 224×224로 전처리해 Model.h5의 조직영상 5라벨 예측을 표시합니다. 함께 있는 학습 노트북은 MobileNetV2의 3클래스 구성이어서 그대로 같은 모델로 간주하면 안 됩니다.

<a id="layout18-table-17-row-1"></a>

**전처리**

**구성**

전처리

**실제 역할**

preprocess_image가 영상을 224×224로 맞추고 255로 나누어 배치 차원을 추가합니다.

<a id="layout18-table-17-row-2"></a>

**5라벨 화면**

**구성**

5라벨 화면

**실제 역할**

대장선암·대장정상·폐선암·폐정상·폐편평상피암의 예측 확률을 표시합니다.

<a id="layout18-table-17-row-3"></a>

**그래프**

**구성**

그래프

**실제 역할**

예측 확률을 텍스트와 원형 그래프로 보여 줍니다.

<a id="layout18-table-17-row-4"></a>

**학습 사본**

**구성**

학습 사본

**실제 역할**

Train.ipynb의 MobileNetV2 3클래스·224·batch16·10epoch와 화면의 5라벨을 구분합니다.


입력 변형과 pool1_pool 특징 변형은 개입 위치가 다릅니다. 모델·학습·라벨·분할·점수 정의가 달라 단순 수치 차이를 모델 변경의 인과 효과로 설명할 수 없습니다. 종료 정책 비교도 별도 설계입니다.

### LEVEL 4 · 달라진 내용과 차수 관계

초기 화면과 학습 코드를 보관한 기본 자료입니다. 후속 ResNet50 입력·특징 변환 실험과 별도로 읽습니다.

[직전 단계 전체 비교·구성](../revision-diffs/experiment-13.diff) · [전체 파일 크기·해시](../revision-manifests/experiment-13.json)

환자 ID 없는 영상 그룹 분할은 환자 독립 분할의 대체가 아닙니다. 소스별 촬영·압축 차이와 같은 환자의 다른 영상이 성능에 영향을 줄 수 있습니다. 높은 정확도의 원인을 조기 종료로 미리 확정하지 않습니다.

### LEVEL 4 · 입력과 실행 조건

| 입력 | 처리 | 출력 |
| --- | --- | --- |
| 업로드 조직영상 | 224×224·정규화 | 모델 입력 |
| Model.h5 | 예측 벡터와 5라벨 연결 | 클래스별 확률 |
| 예측 확률 | 텍스트·원형 그래프 | 연구용 화면 |

| 항목 | 조건·기본값 |
| --- | --- |
| 환경 | Streamlit·TensorFlow·NumPy·Matplotlib |
| 입력 크기 | 224×224 |
| 모델 | 화면은 Model.h5와 5라벨 |
| 학습 노트북 | 3클래스 MobileNetV2·별도 모델 대응 확인 |

Stage 1은 같은 프로세스의 Edge·Cloud 연결이며 실제 원격 전송이 아닙니다. 큰 sigma의 전역 평균 대체, sigma32 결과의 64/128/256 재사용과 Conv2D import 누락 같은 실행 제약을 구분합니다.

### LEVEL 4 · 처리 절차

1. main.py의 모델 경로와 라벨 순서를 확인합니다.
2. 모델 출력 차원이 화면의 5라벨과 같은지 확인합니다.
3. 환경과 일치하는 모델을 준비하고 해당 폴더에서 Streamlit 앱을 엽니다.
4. 업로드 영상의 전처리와 확률 표시를 읽으며 학습 노트북의 모델과 혼합하지 않습니다.

공개 4차는 학습 2차 대시보드의 로컬 수리 3차 사본입니다. 공개 5차는 실험 4차 고정 100회 비교 코드입니다. 원본 manifest·해시·정확 분할이 다르면 중단합니다.

### LEVEL 4 · 결과를 확인하는 방법

화면의 확률은 지정한 모델의 출력입니다. 5라벨 화면과 3클래스 학습 파일은 같은 모델이라는 근거가 필요합니다.

이 초기 조직영상 코드는 후속 CT 비식별화 실험과 입력·모델이 다릅니다. 실제 진단 결과를 제공하는 자료로 해석하지 않습니다.

Blur sigma256의 51.38%는 다수 클래스 56/109와 같지만 모든 조건의 하한은 아닙니다. 별도 학습한 Block512+sigma256은 46.8%입니다. 조합·단독·별도 학습·시험 분모를 나누어 읽습니다.

### LEVEL 4 · 주의할 범위

| 상황 | 확인할 내용 |
| --- | --- |
| 모델 불일치 | 5라벨 화면과 3클래스 학습의 모델·라벨 대응을 먼저 확인합니다. |
| 입력 범위 | 조직영상과 CT를 구분합니다. |
| 사용 목적 | 연구용 예측 화면이며 임상 진단 승인 자료가 아닙니다. |

기존 분할·시험셋 재사용과 환자 ID 부재는 독립 임상 평가를 제한합니다. 높은 정확도의 원인을 조기 종료로 확정하지 않고 동일 조건 정책 비교를 합니다. 두 비교 모델은 같은 학습 경로에서 선택됩니다.

[표·코드·실행 설정·파일 전체 비교를 포함한 공통 상세](#reading-level-5)

<a id="reading-level-5"></a>

## LEVEL 5 - Expert

<!-- semantic-revision17:level-5:start -->

<a id="semantic-lung-legacy-level-5"></a>

### LEVEL 5 · 초기 조직영상 앱과 추가 학습 코드

초기 조직영상 앱과 후속 CT 연구의 입력 도메인·모델·분모를 분리합니다. 백틱/문법 문제와 미확인 가중치 대응이 남아 있는 코드를 완전 실행 검증으로 소개하지 않고 security라는 변수명으로 개인정보 보호 효과를 추정하지 않습니다.

<a id="layout18-table-21-row-1"></a>

**초기화면**

**조건·자료**

초기화면

**의미와 확인 방법**

Streamlit이업로드영상을224×224·255로나눔·배치차원추가후Model.h5의대장선암/대장정상/폐선암/폐정상/폐편평상피암5라벨확률을텍스트와원형그래프로보입니다. Train.ipynb는MobileNetV2 3클래스·224·batch16·10epoch여서모델대응을따로확인합니다.

<a id="layout18-table-21-row-2"></a>

**추가셀**

**조건·자료**

추가셀

**의미와 확인 방법**

Train.ipynb셀0은조직영상5클래스, 셀1·2는EfficientNetV2-S CT블록/블러, 셀3~5는MobileNetV2/풀링비교입니다. 코드별입력224/512와클래스수를확인합니다.

<a id="layout18-table-21-row-3"></a>

**계산과제약**

**조건·자료**

계산과제약

**의미와 확인 방법**

SSIM·PSNR·MS-SSIM·DSSIM변형과저장분류JSON/유사도CSV를그리는코드를구분합니다. 100−accuracy·특징수비율security는공격저항성실측이아니며첫학습셀끝의Markdown백틱·문법·사본별설정을확인합니다.


<!-- semantic-revision17:level-5:end -->

[전문가 수준 프로젝트 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A85.md) · [같은 수준 프로필](https://github.com/PUVKID/PUVKID/blob/main/docs/읽기안내/레벨5.md)

**기존 전체 상세** — 다음 본문은 이 차수의 원래 방법·조건·결과·실패·한계와 전체 비교입니다. 위 수준의 설명에 필요한 공통 근거도 모두 여기서 확인할 수 있습니다.
<!-- reading-levels17:end -->

**Streamlit 화면은 업로드 영상을 224×224로 전처리해 Model.h5의 조직영상 5라벨 예측을 표시합니다.** 함께 있는 학습 노트북은 MobileNetV2의 3클래스 구성이어서 그대로 같은 모델로 간주하면 안 됩니다.

분야: 의료 영상 코드 › Streamlit·TensorFlow › 조직영상 예측 화면

[목적](#purpose) · [기능](#features) · [입출력](#flow) · [구성](#files) · [준비](#setup) · [사용법](#usage) · [결과](#results) · [제약](#limits) · [변경](#changes)

<a name="purpose"></a>

<a id="-이-단계에서-하는-일"></a>

## 연구 목적

입력 화면·전처리·분류 모델·클래스 순서를 연결해 읽는 초기 코드 자료입니다. CT의 ResNet50 변환 실험과 별도 목적의 원본 구성입니다.

<a name="features"></a>

<a id="-주요-기능과-처리-방식"></a>

## 방법과 구현

<a id="layout18-table-22-row-1"></a>

**전처리**

**구성**

전처리

**실제 역할**

preprocess_image가 영상을 224×224로 맞추고 255로 나누어 배치 차원을 추가합니다.

<a id="layout18-table-22-row-2"></a>

**5라벨 화면**

**구성**

5라벨 화면

**실제 역할**

대장선암·대장정상·폐선암·폐정상·폐편평상피암의 예측 확률을 표시합니다.

<a id="layout18-table-22-row-3"></a>

**그래프**

**구성**

그래프

**실제 역할**

예측 확률을 텍스트와 원형 그래프로 보여 줍니다.

<a id="layout18-table-22-row-4"></a>

**학습 사본**

**구성**

학습 사본

**실제 역할**

Train.ipynb의 MobileNetV2 3클래스·224·batch16·10epoch와 화면의 5라벨을 구분합니다.


<a name="flow"></a>

<a id="-입력--처리--출력"></a>

## 입력·처리·출력

| 입력 | 처리 | 출력 |
| --- | --- | --- |
| 업로드 조직영상 | 224×224·정규화 | 모델 입력 |
| Model.h5 | 예측 벡터와 5라벨 연결 | 클래스별 확률 |
| 예측 확률 | 텍스트·원형 그래프 | 연구용 화면 |

<a name="files"></a>

<a id="-파일과-핵심-처리"></a>

## 파일별 역할

| 파일 | 이용 방법 |
| --- | --- |
| [원본 실험/Lung Cancer/main.py](../../%EC%9B%90%EB%B3%B8%20%EC%8B%A4%ED%97%98/Lung%20Cancer/main.py) | 처리 함수와 실행 조건 |
| [원본 실험/Lung Cancer/Train.ipynb](../../%EC%9B%90%EB%B3%B8%20%EC%8B%A4%ED%97%98/Lung%20Cancer/Train.ipynb) | 설정·함수·실행 셀 |

<a id="-함수셀로-찾아가기"></a>

### 관련 함수와 셀

관련 함수와 셀을 파일별로 정리했습니다. 실행 전 설정과 호출 순서, 출력 경로를 확인하세요.

<a id="layout18-table-25-row-1"></a>

**[원본 실험/Lung Cancer/main.py](../../%EC%9B%90%EB%B3%B8%20%EC%8B%A4%ED%97%98/Lung%20Cancer/main.py)**

**파일**

[원본 실험/Lung Cancer/main.py](../../%EC%9B%90%EB%B3%B8%20%EC%8B%A4%ED%97%98/Lung%20Cancer/main.py)

**핵심 정의**

소스: `preprocess_image` · `predict_cancer` · `plot_pie_chart`


<a name="setup"></a>

<a id="️-환경과-설정"></a>

## 실행 환경과 설정

| 항목 | 조건·기본값 |
| --- | --- |
| 환경 | Streamlit·TensorFlow·NumPy·Matplotlib |
| 입력 크기 | 224×224 |
| 모델 | 화면은 Model.h5와 5라벨 |
| 학습 노트북 | 3클래스 MobileNetV2·별도 모델 대응 확인 |

<a name="usage"></a>

<a id="-준비와-사용-순서"></a>

## 실행 순서

1. main.py의 모델 경로와 라벨 순서를 확인합니다.
2. 모델 출력 차원이 화면의 5라벨과 같은지 확인합니다.
3. 환경과 일치하는 모델을 준비하고 해당 폴더에서 Streamlit 앱을 엽니다.
4. 업로드 영상의 전처리와 확률 표시를 읽으며 학습 노트북의 모델과 혼합하지 않습니다.

<a name="results"></a>

<a id="-결과를-읽는-방법"></a>

## 결과와 해석

화면의 확률은 지정한 모델의 출력입니다. 5라벨 화면과 3클래스 학습 파일은 같은 모델이라는 근거가 필요합니다.

이 초기 조직영상 코드는 후속 CT 비식별화 실험과 입력·모델이 다릅니다. 실제 진단 결과를 제공하는 자료로 해석하지 않습니다.

<a name="limits"></a>

<a id="️-알려진-제약과-확인-지점"></a>

## 제약과 확인 사항

| 상황 | 확인할 내용 |
| --- | --- |
| 모델 불일치 | 5라벨 화면과 3클래스 학습의 모델·라벨 대응을 먼저 확인합니다. |
| 입력 범위 | 조직영상과 CT를 구분합니다. |
| 사용 목적 | 연구용 예측 화면이며 임상 진단 승인 자료가 아닙니다. |

<a name="changes"></a>

<a id="-이전-단계와의-변화"></a>

## 직전 단계와 비교

초기 화면과 학습 코드를 보관한 기본 자료입니다. 후속 ResNet50 입력·특징 변환 실험과 별도로 읽습니다.

[직전 단계 전체 비교·구성](../revision-diffs/experiment-13.diff) · [전체 파일 크기·해시](../revision-manifests/experiment-13.json)

<details>
<summary>이 단계의 파일 기록과 전체 해시</summary>

아래 내용는 해당 단계가 기록될 당시의 파일 정보입니다. 현재 첨부는 [프로젝트 자료 안내](../PAPERS.md)에서 확인할 수 있습니다.

<a id="layout18-table-28-row-1"></a>

**[원본 실험/Lung Cancer/main.ipynb](../../%EC%9B%90%EB%B3%B8%20%EC%8B%A4%ED%97%98/Lung%20Cancer/main.ipynb)**

**파일**

[원본 실험/Lung Cancer/main.ipynb](../../%EC%9B%90%EB%B3%B8%20%EC%8B%A4%ED%97%98/Lung%20Cancer/main.ipynb)

**종류**

.ipynb

**바이트**

3163

**SHA-256**

`645bbc4f163ee9a8fb2120e4ef7f6cc6ec447c080a315b076967e3808d2c6f90`

<a id="layout18-table-28-row-2"></a>

**[원본 실험/Lung Cancer/main.py](../../%EC%9B%90%EB%B3%B8%20%EC%8B%A4%ED%97%98/Lung%20Cancer/main.py)**

**파일**

[원본 실험/Lung Cancer/main.py](../../%EC%9B%90%EB%B3%B8%20%EC%8B%A4%ED%97%98/Lung%20Cancer/main.py)

**종류**

.py

**바이트**

1651

**SHA-256**

`e9d1cab540e21c3730a0f4dd47a94964a5722c069c9489e5f0ba800e2a7a68e8`

<a id="layout18-table-28-row-3"></a>

**[원본 실험/Lung Cancer/Train.ipynb](../../%EC%9B%90%EB%B3%B8%20%EC%8B%A4%ED%97%98/Lung%20Cancer/Train.ipynb)**

**파일**

[원본 실험/Lung Cancer/Train.ipynb](../../%EC%9B%90%EB%B3%B8%20%EC%8B%A4%ED%97%98/Lung%20Cancer/Train.ipynb)

**종류**

.ipynb

**바이트**

3491

**SHA-256**

`ffa9c77e4f9004dcb8e0c0eec3f1911f9d71518d1038bd8bc07a5031fd62a5d9`

<a id="layout18-table-28-row-4"></a>

**[원본자료/원본 실험/Lung Cancer/main.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%9B%90%EB%B3%B8%20%EC%8B%A4%ED%97%98/Lung%20Cancer/main.ipynb)**

**파일**

[원본자료/원본 실험/Lung Cancer/main.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%9B%90%EB%B3%B8%20%EC%8B%A4%ED%97%98/Lung%20Cancer/main.ipynb)

**종류**

.ipynb

**바이트**

3163

**SHA-256**

`645bbc4f163ee9a8fb2120e4ef7f6cc6ec447c080a315b076967e3808d2c6f90`

<a id="layout18-table-28-row-5"></a>

**[원본자료/원본 실험/Lung Cancer/main.py](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%9B%90%EB%B3%B8%20%EC%8B%A4%ED%97%98/Lung%20Cancer/main.py)**

**파일**

[원본자료/원본 실험/Lung Cancer/main.py](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%9B%90%EB%B3%B8%20%EC%8B%A4%ED%97%98/Lung%20Cancer/main.py)

**종류**

.py

**바이트**

1651

**SHA-256**

`e9d1cab540e21c3730a0f4dd47a94964a5722c069c9489e5f0ba800e2a7a68e8`

<a id="layout18-table-28-row-6"></a>

**[원본자료/원본 실험/Lung Cancer/Train.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%9B%90%EB%B3%B8%20%EC%8B%A4%ED%97%98/Lung%20Cancer/Train.ipynb)**

**파일**

[원본자료/원본 실험/Lung Cancer/Train.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%9B%90%EB%B3%B8%20%EC%8B%A4%ED%97%98/Lung%20Cancer/Train.ipynb)

**종류**

.ipynb

**바이트**

4028

**SHA-256**

`efc1cc1f4d2c17e399e6aead9645527852a6445703db00683327400f06b6c139`

<a id="layout18-table-28-row-7"></a>

**항목 7**

**파일**

[원본자료/원본 실험/LungCancerClassification-main/main.py](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%9B%90%EB%B3%B8%20%EC%8B%A4%ED%97%98/LungCancerClassification-main/main.py)

**종류**

.py

**바이트**

1651

**SHA-256**

`e9d1cab540e21c3730a0f4dd47a94964a5722c069c9489e5f0ba800e2a7a68e8`

<a id="layout18-table-28-row-8"></a>

**항목 8**

**파일**

[원본자료/원본 실험/LungCancerClassification-main/trainer.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%9B%90%EB%B3%B8%20%EC%8B%A4%ED%97%98/LungCancerClassification-main/trainer.ipynb)

**종류**

.ipynb

**바이트**

30177

**SHA-256**

`d806b5df96a6c148fa4fc3905d1888e1a20c9493208bbe15b0239b2816735820`

<a id="layout18-table-28-row-9"></a>

**항목 9**

**파일**

[원본자료/원본 실험/LungCancerClassification-main/LICENSE](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%9B%90%EB%B3%B8%20%EC%8B%A4%ED%97%98/LungCancerClassification-main/LICENSE)

**종류**



**바이트**

1068

**SHA-256**

`7af98bcd79c5f6c6ddaf6399f3782e6e2c1336c87800b3a4affee46546bd9129`

<a id="layout18-table-28-row-10"></a>

**항목 10**

**파일**

[원본자료/원본 실험/LungCancerClassification-main/README.md](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%9B%90%EB%B3%B8%20%EC%8B%A4%ED%97%98/LungCancerClassification-main/README.md)

**종류**

.md

**바이트**

4498

**SHA-256**

`f47ba9b58041760d2651f9fe0f7fff32261ea1fb5e0ef075616f07579a284391`

<a id="layout18-table-28-row-11"></a>

**항목 11**

**파일**

[원본자료/원본 실험/LungCancerClassification-main/confusion_matrix.png](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%9B%90%EB%B3%B8%20%EC%8B%A4%ED%97%98/LungCancerClassification-main/confusion_matrix.png)

**종류**

.png

**바이트**

90242

**SHA-256**

`1deeddc5d7501f2de854781c480081ff2eebfd07bd5ff7ddfa77981cbe2a3bde`

<a id="layout18-table-28-row-12"></a>

**항목 12**

**파일**

[원본자료/원본 실험/LungCancerClassification-main/confusion_matrix (2).png](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%9B%90%EB%B3%B8%20%EC%8B%A4%ED%97%98/LungCancerClassification-main/confusion_matrix%20%282%29.png)

**종류**

.png

**바이트**

90242

**SHA-256**

`1deeddc5d7501f2de854781c480081ff2eebfd07bd5ff7ddfa77981cbe2a3bde`


</details>

---

[프로젝트](../../README.md) · [전체 차수](../REVISION_INDEX.md) · [자료 폴더](../../%EC%9B%90%EB%B3%B8%20%EC%8B%A4%ED%97%98/Lung%20Cancer)

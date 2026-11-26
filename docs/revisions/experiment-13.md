<!-- language-choice:start -->
🔵 **한국어** · [English overview](../../en/README.md)
<!-- language-choice:end -->

<a id="️-원본-실험--조직영상-화면과-학습-노트북"></a>

# 원본 실험 · 조직영상 화면과 학습 노트북

<!-- reading-levels17:start -->
읽기 수준 · [LEVEL 1](#user-content-reading-level-1) · [LEVEL 2](#user-content-reading-level-2) · [LEVEL 3](#user-content-reading-level-3) · [LEVEL 4](#user-content-reading-level-4) · [LEVEL 5](#user-content-reading-level-5)

<details open>
<summary>LEVEL 1 · Beginner — 목적과 동작부터</summary>

<a id="reading-level-1"></a>

## LEVEL 1 - Beginner

<a id="semantic-lung-legacy-level-1"></a>

| 항목 | 이 차수의 내용 |
| --- | --- |
| 목적 | Streamlit 화면은 업로드 영상을 224×224로 전 처리해 Model.h5의 조직 영상 5 라벨 예측을 표시합니다.<br>함께 있는 학습 노트북은 MobileNetV2의 3 클래스 구성이어서 그대로 같은 모델로 간주하면 안 됩니다. |
| 변경 | 초기 화면과 학습 코드를 보관한 기본 자료입니다.<br>후속 ResNet50 입력·특징 변환 실험과 별도로 읽습니다. |
| 조건 | **환경**: Streamlit·TensorFlow·NumPy·Matplotlib<br>**입력 크기**: 224×224<br>**모델**: 화면은 Model.h5와 5 라벨<br>**학습 노트북**: 3 클래스 MobileNetV2·별도 모델 대응 확인 |
| 동작 | 1. main.py의 모델 경로와 라벨 순서를 확인합니다. |
| 결과 | 화면의 확률은 지정한 모델의 출력입니다. 5 라벨 화면과 3 클래스 학습 파일은 같은 모델이라는 근거가 필요합니다. |

### LEVEL 1 · 초기 조직영상 앱과 추가 학습 코드

**원본 실험 · 조직영상 화면과 학습 노트북**의 범위에서 설명합니다. 먼저 이 자료가 무엇을 바꾸고 무엇을 보여 주는지 살펴봅니다. 아래 조건은 이 문서에 연결된 파일의 내용이며 다른 차수의 결과를 함께 센 값이 아닙니다.

| 항목 | 이 차수의 내용 |
| --- | --- |
| <a id="layout18-table-1-row-1"></a> **목적** | 입력 화면·전처리·분류 모델·클래스 순서를 연결해 읽는 초기 코드 자료입니다. CT의 ResNet50 변환 실험과 별도 목적의 원본 구성입니다. |
| <a id="layout18-table-1-row-2"></a> **구현** | **전처리**: preprocess_image가 영상을 224×224로 맞추고 255로 나누어 배치 차원을 추가합니다.<br>**5 라벨 화면**: 대장선암·대장 정상·폐선암·폐 정상·폐 편평상피암의 예측 확률을 표시합니다.<br>**그래프**: 예측 확률을 텍스트와 원형 그래프로 보여 줍니다.<br>**학습 사본**: Train.ipynb의 MobileNetV2 3 클래스·224·batch16·10epoch와 화면의 5 라벨을 구분합니다. |
| <a id="layout18-table-1-row-3"></a> **조건·관측과 해석·한계·자료 연결** | **환경**: Streamlit·TensorFlow·NumPy·Matplotlib<br>**입력 크기**: 224×224<br>**모델**: 화면은 Model.h5와 5 라벨<br>**학습 노트북**: 3 클래스 MobileNetV2·별도 모델 대응 확인<br>화면의 확률은 지정한 모델의 출력입니다. 5 라벨 화면과 3 클래스 학습 파일은 같은 모델이라는 근거가 필요합니다.<br>이 초기 조직영상 코드는 후속 CT 비식별화 실험과 입력·모델이 다릅니다. 실제 진단 결과를 제공하는 자료로 해석하지 않습니다.<br>**모델 불일치**: 5 라벨 화면과 3 클래스 학습의 모델·라벨 대응을 먼저 확인합니다.<br>**입력 범위**: 조직 영상과 CT를 구분합니다.<br>**사용 목적**: 연구용 예측 화면이며 임상 진단 승인 자료가 아닙니다.<br>[이 차수 전체 상세](#purpose) · [실행 순서](#usage) · [결과와 해석](#results) · [프로젝트 공통 안내](../../README.md)<br>다른 입력 변환·모델 구성과 원고 보고값은 [공통 프로젝트 안내](../../README.md)에서 해당 자료로 이동합니다. |


[동일 수준 프로젝트 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A81.md)


</details>

<details>
<summary>LEVEL 2 · Explorer — 구성과 연결 원리</summary>

<a id="reading-level-2"></a>

## LEVEL 2 - Explorer

<a id="semantic-lung-legacy-level-2"></a>

| 항목 | 이 차수의 내용 |
| --- | --- |
| 목적 | Streamlit 화면은 업로드 영상을 224×224로 전 처리해 Model.h5의 조직 영상 5 라벨 예측을 표시합니다.<br>함께 있는 학습 노트북은 MobileNetV2의 3 클래스 구성이어서 그대로 같은 모델로 간주하면 안 됩니다. |
| 변경 | 초기 화면과 학습 코드를 보관한 기본 자료입니다.<br>후속 ResNet50 입력·특징 변환 실험과 별도로 읽습니다. |
| 조건 | **환경**: Streamlit·TensorFlow·NumPy·Matplotlib<br>**입력 크기**: 224×224<br>**모델**: 화면은 Model.h5와 5 라벨<br>**학습 노트북**: 3 클래스 MobileNetV2·별도 모델 대응 확인 |
| 동작 | 1. main.py의 모델 경로와 라벨 순서를 확인합니다. |
| 결과 | 화면의 확률은 지정한 모델의 출력입니다. 5 라벨 화면과 3 클래스 학습 파일은 같은 모델이라는 근거가 필요합니다. |

### LEVEL 2 · 초기 조직영상 앱과 추가 학습 코드

**원본 실험 · 조직영상 화면과 학습 노트북**의 범위에서 설명합니다. 입력 → 처리 → 출력의 순서로 읽습니다. 설정을 준비한 것과 실제 실행에서 얻은 결과를 구분하고, 관측값은 같은 입력·설정의 기록과 연결합니다.

| 항목 | 이 차수의 내용 |
| --- | --- |
| <a id="layout18-table-6-row-1"></a> **목적** | 입력 화면·전처리·분류 모델·클래스 순서를 연결해 읽는 초기 코드 자료입니다. CT의 ResNet50 변환 실험과 별도 목적의 원본 구성입니다. |
| <a id="layout18-table-6-row-2"></a> **구현** | **전처리**: preprocess_image가 영상을 224×224로 맞추고 255로 나누어 배치 차원을 추가합니다.<br>**5 라벨 화면**: 대장선암·대장 정상·폐선암·폐 정상·폐 편평상피암의 예측 확률을 표시합니다.<br>**그래프**: 예측 확률을 텍스트와 원형 그래프로 보여 줍니다.<br>**학습 사본**: Train.ipynb의 MobileNetV2 3 클래스·224·batch16·10epoch와 화면의 5 라벨을 구분합니다. |
| <a id="layout18-table-6-row-3"></a> **조건·관측과 해석·한계·자료 연결** | **환경**: Streamlit·TensorFlow·NumPy·Matplotlib<br>**입력 크기**: 224×224<br>**모델**: 화면은 Model.h5와 5 라벨<br>**학습 노트북**: 3 클래스 MobileNetV2·별도 모델 대응 확인<br>화면의 확률은 지정한 모델의 출력입니다. 5 라벨 화면과 3 클래스 학습 파일은 같은 모델이라는 근거가 필요합니다.<br>이 초기 조직영상 코드는 후속 CT 비식별화 실험과 입력·모델이 다릅니다. 실제 진단 결과를 제공하는 자료로 해석하지 않습니다.<br>**모델 불일치**: 5 라벨 화면과 3 클래스 학습의 모델·라벨 대응을 먼저 확인합니다.<br>**입력 범위**: 조직 영상과 CT를 구분합니다.<br>**사용 목적**: 연구용 예측 화면이며 임상 진단 승인 자료가 아닙니다.<br>[이 차수 전체 상세](#purpose) · [실행 순서](#usage) · [결과와 해석](#results) · [프로젝트 공통 안내](../../README.md)<br>다른 입력 변환·모델 구성과 원고 보고값은 [공통 프로젝트 안내](../../README.md)에서 해당 자료로 이동합니다. |


[동일 수준 프로젝트 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A82.md)


</details>

<details>
<summary>LEVEL 3 · Practitioner — 준비·실행·결과 확인</summary>

<a id="reading-level-3"></a>

## LEVEL 3 - Practitioner

<a id="semantic-lung-legacy-level-3"></a>

| 항목 | 이 차수의 내용 |
| --- | --- |
| 목적 | Streamlit 화면은 업로드 영상을 224×224로 전 처리해 Model.h5의 조직 영상 5 라벨 예측을 표시합니다.<br>함께 있는 학습 노트북은 MobileNetV2의 3 클래스 구성이어서 그대로 같은 모델로 간주하면 안 됩니다. |
| 변경 | 초기 화면과 학습 코드를 보관한 기본 자료입니다.<br>후속 ResNet50 입력·특징 변환 실험과 별도로 읽습니다. |
| 조건 | **환경**: Streamlit·TensorFlow·NumPy·Matplotlib<br>**입력 크기**: 224×224<br>**모델**: 화면은 Model.h5와 5 라벨<br>**학습 노트북**: 3 클래스 MobileNetV2·별도 모델 대응 확인 |
| 동작 | 1. main.py의 모델 경로와 라벨 순서를 확인합니다. |
| 결과 | 화면의 확률은 지정한 모델의 출력입니다. 5 라벨 화면과 3 클래스 학습 파일은 같은 모델이라는 근거가 필요합니다. |

### LEVEL 3 · 초기 조직영상 앱과 추가 학습 코드

**원본 실험 · 조직영상 화면과 학습 노트북**의 범위에서 설명합니다. 실행할 파일을 먼저 고르고 아래 전체 상세의 경로·설정·호출 순서를 확인합니다. 표의 구성과 조건을 해당 파일에 맞춰 읽으며 문서 정리 자체가 새 실행을 뜻하지는 않습니다.

| 항목 | 이 차수의 내용 |
| --- | --- |
| <a id="layout18-table-11-row-1"></a> **목적** | 입력 화면·전처리·분류 모델·클래스 순서를 연결해 읽는 초기 코드 자료입니다. CT의 ResNet50 변환 실험과 별도 목적의 원본 구성입니다. |
| <a id="layout18-table-11-row-2"></a> **구현** | **전처리**: preprocess_image가 영상을 224×224로 맞추고 255로 나누어 배치 차원을 추가합니다.<br>**5 라벨 화면**: 대장선암·대장 정상·폐선암·폐 정상·폐 편평상피암의 예측 확률을 표시합니다.<br>**그래프**: 예측 확률을 텍스트와 원형 그래프로 보여 줍니다.<br>**학습 사본**: Train.ipynb의 MobileNetV2 3 클래스·224·batch16·10epoch와 화면의 5 라벨을 구분합니다. |
| <a id="layout18-table-11-row-3"></a> **조건·관측과 해석·한계·자료 연결** | **환경**: Streamlit·TensorFlow·NumPy·Matplotlib<br>**입력 크기**: 224×224<br>**모델**: 화면은 Model.h5와 5 라벨<br>**학습 노트북**: 3 클래스 MobileNetV2·별도 모델 대응 확인<br>화면의 확률은 지정한 모델의 출력입니다. 5 라벨 화면과 3 클래스 학습 파일은 같은 모델이라는 근거가 필요합니다.<br>이 초기 조직영상 코드는 후속 CT 비식별화 실험과 입력·모델이 다릅니다. 실제 진단 결과를 제공하는 자료로 해석하지 않습니다.<br>**모델 불일치**: 5 라벨 화면과 3 클래스 학습의 모델·라벨 대응을 먼저 확인합니다.<br>**입력 범위**: 조직 영상과 CT를 구분합니다.<br>**사용 목적**: 연구용 예측 화면이며 임상 진단 승인 자료가 아닙니다.<br>[이 차수 전체 상세](#purpose) · [실행 순서](#usage) · [결과와 해석](#results) · [프로젝트 공통 안내](../../README.md)<br>다른 입력 변환·모델 구성과 원고 보고값은 [공통 프로젝트 안내](../../README.md)에서 해당 자료로 이동합니다. |


[동일 수준 프로젝트 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A83.md)


</details>

<details>
<summary>LEVEL 4 · Advanced — 구현·설계·실패 처리</summary>

<a id="reading-level-4"></a>

## LEVEL 4 - Advanced

<a id="semantic-lung-legacy-level-4"></a>

| 항목 | 이 차수의 내용 |
| --- | --- |
| 목적 | Streamlit 화면은 업로드 영상을 224×224로 전 처리해 Model.h5의 조직 영상 5 라벨 예측을 표시합니다.<br>함께 있는 학습 노트북은 MobileNetV2의 3 클래스 구성이어서 그대로 같은 모델로 간주하면 안 됩니다. |
| 변경 | 초기 화면과 학습 코드를 보관한 기본 자료입니다.<br>후속 ResNet50 입력·특징 변환 실험과 별도로 읽습니다. |
| 조건 | **환경**: Streamlit·TensorFlow·NumPy·Matplotlib<br>**입력 크기**: 224×224<br>**모델**: 화면은 Model.h5와 5 라벨<br>**학습 노트북**: 3 클래스 MobileNetV2·별도 모델 대응 확인 |
| 동작 | 1. main.py의 모델 경로와 라벨 순서를 확인합니다. |
| 결과 | 화면의 확률은 지정한 모델의 출력입니다. 5 라벨 화면과 3 클래스 학습 파일은 같은 모델이라는 근거가 필요합니다. |

### LEVEL 4 · 초기 조직영상 앱과 추가 학습 코드

**원본 실험 · 조직영상 화면과 학습 노트북**의 범위에서 설명합니다. 입력 준비·변환 또는 셀 수정·계산·저장의 경계를 나누어 읽습니다. 각 설정과 출력의 대응은 이 차수 자료를 기준으로 확인하고 다른 차수의 구현은 관련 링크에서 별도로 살펴봅니다.

| 항목 | 이 차수의 내용 |
| --- | --- |
| <a id="layout18-table-16-row-1"></a> **목적** | 입력 화면·전처리·분류 모델·클래스 순서를 연결해 읽는 초기 코드 자료입니다. CT의 ResNet50 변환 실험과 별도 목적의 원본 구성입니다. |
| <a id="layout18-table-16-row-2"></a> **구현** | **전처리**: preprocess_image가 영상을 224×224로 맞추고 255로 나누어 배치 차원을 추가합니다.<br>**5 라벨 화면**: 대장선암·대장 정상·폐선암·폐 정상·폐 편평상피암의 예측 확률을 표시합니다.<br>**그래프**: 예측 확률을 텍스트와 원형 그래프로 보여 줍니다.<br>**학습 사본**: Train.ipynb의 MobileNetV2 3 클래스·224·batch16·10epoch와 화면의 5 라벨을 구분합니다. |
| <a id="layout18-table-16-row-3"></a> **조건·관측과 해석·한계·자료 연결** | **환경**: Streamlit·TensorFlow·NumPy·Matplotlib<br>**입력 크기**: 224×224<br>**모델**: 화면은 Model.h5와 5 라벨<br>**학습 노트북**: 3 클래스 MobileNetV2·별도 모델 대응 확인<br>화면의 확률은 지정한 모델의 출력입니다. 5 라벨 화면과 3 클래스 학습 파일은 같은 모델이라는 근거가 필요합니다.<br>이 초기 조직영상 코드는 후속 CT 비식별화 실험과 입력·모델이 다릅니다. 실제 진단 결과를 제공하는 자료로 해석하지 않습니다.<br>**모델 불일치**: 5 라벨 화면과 3 클래스 학습의 모델·라벨 대응을 먼저 확인합니다.<br>**입력 범위**: 조직 영상과 CT를 구분합니다.<br>**사용 목적**: 연구용 예측 화면이며 임상 진단 승인 자료가 아닙니다.<br>[이 차수 전체 상세](#purpose) · [실행 순서](#usage) · [결과와 해석](#results) · [프로젝트 공통 안내](../../README.md)<br>다른 입력 변환·모델 구성과 원고 보고값은 [공통 프로젝트 안내](../../README.md)에서 해당 자료로 이동합니다. |


[동일 수준 프로젝트 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A84.md)


</details>

<details>
<summary>LEVEL 5 · Expert — 근거·프로토콜·한계 검토</summary>

<a id="reading-level-5"></a>

## LEVEL 5 - Expert

<a id="semantic-lung-legacy-level-5"></a>

### LEVEL 5 · 초기 조직영상 앱과 추가 학습 코드

**원본 실험 · 조직영상 화면과 학습 노트북**의 범위에서 설명합니다. 코드에 정의된 동작·설정, 저장된 관측값, 재현에 필요한 입력을 구분합니다. 분모·변환 위치·모델 대응과 알려진 한계를 유지하며 다른 차수나 원고의 결과를 이 자료의 실측으로 합치지 않습니다.

| 항목 | 이 차수의 내용 |
| --- | --- |
| <a id="layout18-table-21-row-1"></a> **목적** | 입력 화면·전처리·분류 모델·클래스 순서를 연결해 읽는 초기 코드 자료입니다. CT의 ResNet50 변환 실험과 별도 목적의 원본 구성입니다. |
| <a id="layout18-table-21-row-2"></a> **구현** | **전처리**: preprocess_image가 영상을 224×224로 맞추고 255로 나누어 배치 차원을 추가합니다.<br>**5 라벨 화면**: 대장선암·대장 정상·폐선암·폐 정상·폐 편평상피암의 예측 확률을 표시합니다.<br>**그래프**: 예측 확률을 텍스트와 원형 그래프로 보여 줍니다.<br>**학습 사본**: Train.ipynb의 MobileNetV2 3 클래스·224·batch16·10epoch와 화면의 5 라벨을 구분합니다. |
| <a id="layout18-table-21-row-3"></a> **조건·관측과 해석·한계·자료 연결** | **환경**: Streamlit·TensorFlow·NumPy·Matplotlib<br>**입력 크기**: 224×224<br>**모델**: 화면은 Model.h5와 5 라벨<br>**학습 노트북**: 3 클래스 MobileNetV2·별도 모델 대응 확인<br>화면의 확률은 지정한 모델의 출력입니다. 5 라벨 화면과 3 클래스 학습 파일은 같은 모델이라는 근거가 필요합니다.<br>이 초기 조직영상 코드는 후속 CT 비식별화 실험과 입력·모델이 다릅니다. 실제 진단 결과를 제공하는 자료로 해석하지 않습니다.<br>**모델 불일치**: 5 라벨 화면과 3 클래스 학습의 모델·라벨 대응을 먼저 확인합니다.<br>**입력 범위**: 조직 영상과 CT를 구분합니다.<br>**사용 목적**: 연구용 예측 화면이며 임상 진단 승인 자료가 아닙니다.<br>[이 차수 전체 상세](#purpose) · [실행 순서](#usage) · [결과와 해석](#results) · [프로젝트 공통 안내](../../README.md)<br>다른 입력 변환·모델 구성과 원고 보고값은 [공통 프로젝트 안내](../../README.md)에서 해당 자료로 이동합니다. |


[동일 수준 프로젝트 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A85.md)

<!-- reading-levels17:end -->

Streamlit 화면은 업로드 영상을 224×224로 전 처리해 Model.h5의 조직 영상 5 라벨 예측을 표시합니다. 함께 있는 학습 노트북은 MobileNetV2의 3 클래스 구성이어서 그대로 같은 모델로 간주하면 안 됩니다.

분야: 의료 영상 코드 › Streamlit·TensorFlow › 조직영상 예측 화면

[목적](#purpose) · [기능](#features) · [입출력](#flow) · [구성](#files) · [준비](#setup) · [사용법](#usage) · [결과](#results) · [제약](#limits) · [변경](#changes)

<a name="purpose"></a>

<a id="-이-단계에서-하는-일"></a>

## 연구 목적

입력 화면·전처리·분류 모델·클래스 순서를 연결해 읽는 초기 코드 자료입니다. CT의 ResNet50 변환 실험과 별도 목적의 원본 구성입니다.

<a name="features"></a>

<a id="-주요-기능과-처리-방식"></a>

## 방법과 구현

| 구성 | 실제 역할 |
| --- | --- |
| <a id="layout18-table-22-row-1"></a> 전처리 | preprocess_image가 영상을 224×224로 맞추고 255로 나누어 배치 차원을 추가합니다. |
| <a id="layout18-table-22-row-2"></a> 5 라벨 화면 | 대장선암·대장 정상·폐선암·폐 정상·폐 편평상피암의 예측 확률을 표시합니다. |
| <a id="layout18-table-22-row-3"></a> 그래프 | 예측 확률을 텍스트와 원형 그래프로 보여 줍니다. |
| <a id="layout18-table-22-row-4"></a> 학습 사본 | Train.ipynb의 MobileNetV2 3 클래스·224·batch16·10epoch와 화면의 5 라벨을 구분합니다. |


<a name="flow"></a>

<a id="-입력--처리--출력"></a>

## 입력·처리·출력

| 입력 | 처리 | 출력 |
| --- | --- | --- |
| 업로드 조직영상 | 224×224·정규화 | 모델 입력 |
| Model.h5 | 예측 벡터와 5 라벨 연결 | 클래스별 확률 |
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

| 파일 | 핵심 정의 |
| --- | --- |
| <a id="layout18-table-25-row-1"></a> [원본 실험/Lung Cancer/main.py](../../%EC%9B%90%EB%B3%B8%20%EC%8B%A4%ED%97%98/Lung%20Cancer/main.py) | 소스: `preprocess_image` · `predict_cancer` · `plot_pie_chart` |


<a name="setup"></a>

<a id="️-환경과-설정"></a>

## 실행 환경과 설정

| 항목 | 조건·기본값 |
| --- | --- |
| 환경 | Streamlit·TensorFlow·NumPy·Matplotlib |
| 입력 크기 | 224×224 |
| 모델 | 화면은 Model.h5와 5 라벨 |
| 학습 노트북 | 3 클래스 MobileNetV2·별도 모델 대응 확인 |

<a name="usage"></a>

<a id="-준비와-사용-순서"></a>

## 실행 순서

1. main.py의 모델 경로와 라벨 순서를 확인합니다.
2. 모델 출력 차원이 화면의 5 라벨과 같은지 확인합니다.
3. 환경과 일치하는 모델을 준비하고 해당 폴더에서 Streamlit 앱을 엽니다.
4. 업로드 영상의 전처리와 확률 표시를 읽으며 학습 노트북의 모델과 혼합하지 않습니다.

<a name="results"></a>

<a id="-결과를-읽는-방법"></a>

## 결과와 해석

화면의 확률은 지정한 모델의 출력입니다. 5 라벨 화면과 3 클래스 학습 파일은 같은 모델이라는 근거가 필요합니다.

이 초기 조직영상 코드는 후속 CT 비식별화 실험과 입력·모델이 다릅니다. 실제 진단 결과를 제공하는 자료로 해석하지 않습니다.

<a name="limits"></a>

<a id="️-알려진-제약과-확인-지점"></a>

## 제약과 확인 사항

| 상황 | 확인할 내용 |
| --- | --- |
| 모델 불일치 | 5 라벨 화면과 3 클래스 학습의 모델·라벨 대응을 먼저 확인합니다. |
| 입력 범위 | 조직 영상과 CT를 구분합니다. |
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

[원본 실험/Lung Cancer/main.ipynb](../../%EC%9B%90%EB%B3%B8%20%EC%8B%A4%ED%97%98/Lung%20Cancer/main.ipynb)

**파일**

[원본 실험/Lung Cancer/main.ipynb](../../%EC%9B%90%EB%B3%B8%20%EC%8B%A4%ED%97%98/Lung%20Cancer/main.ipynb)

**종류**

.ipynb

**바이트**

3163

**SHA-256**

`645bbc4f163ee9a8fb2120e4ef7f6cc6ec447c080a315b076967e3808d2c6f90`

<a id="layout18-table-28-row-2"></a>

[원본 실험/Lung Cancer/main.py](../../%EC%9B%90%EB%B3%B8%20%EC%8B%A4%ED%97%98/Lung%20Cancer/main.py)

**파일**

[원본 실험/Lung Cancer/main.py](../../%EC%9B%90%EB%B3%B8%20%EC%8B%A4%ED%97%98/Lung%20Cancer/main.py)

**종류**

.py

**바이트**

1651

**SHA-256**

`e9d1cab540e21c3730a0f4dd47a94964a5722c069c9489e5f0ba800e2a7a68e8`

<a id="layout18-table-28-row-3"></a>

[원본 실험/Lung Cancer/Train.ipynb](../../%EC%9B%90%EB%B3%B8%20%EC%8B%A4%ED%97%98/Lung%20Cancer/Train.ipynb)

**파일**

[원본 실험/Lung Cancer/Train.ipynb](../../%EC%9B%90%EB%B3%B8%20%EC%8B%A4%ED%97%98/Lung%20Cancer/Train.ipynb)

**종류**

.ipynb

**바이트**

3491

**SHA-256**

`ffa9c77e4f9004dcb8e0c0eec3f1911f9d71518d1038bd8bc07a5031fd62a5d9`

<a id="layout18-table-28-row-4"></a>

[원본자료/원본 실험/Lung Cancer/main.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%9B%90%EB%B3%B8%20%EC%8B%A4%ED%97%98/Lung%20Cancer/main.ipynb)

**파일**

[원본자료/원본 실험/Lung Cancer/main.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%9B%90%EB%B3%B8%20%EC%8B%A4%ED%97%98/Lung%20Cancer/main.ipynb)

**종류**

.ipynb

**바이트**

3163

**SHA-256**

`645bbc4f163ee9a8fb2120e4ef7f6cc6ec447c080a315b076967e3808d2c6f90`

<a id="layout18-table-28-row-5"></a>

[원본자료/원본 실험/Lung Cancer/main.py](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%9B%90%EB%B3%B8%20%EC%8B%A4%ED%97%98/Lung%20Cancer/main.py)

**파일**

[원본자료/원본 실험/Lung Cancer/main.py](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%9B%90%EB%B3%B8%20%EC%8B%A4%ED%97%98/Lung%20Cancer/main.py)

**종류**

.py

**바이트**

1651

**SHA-256**

`e9d1cab540e21c3730a0f4dd47a94964a5722c069c9489e5f0ba800e2a7a68e8`

<a id="layout18-table-28-row-6"></a>

[원본자료/원본 실험/Lung Cancer/Train.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%9B%90%EB%B3%B8%20%EC%8B%A4%ED%97%98/Lung%20Cancer/Train.ipynb)

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


<a id="layout18-table-12-row-1"></a><a id="layout18-table-12-row-2"></a><a id="layout18-table-12-row-3"></a><a id="layout18-table-12-row-4"></a><a id="layout18-table-17-row-1"></a><a id="layout18-table-17-row-2"></a><a id="layout18-table-17-row-3"></a><a id="layout18-table-17-row-4"></a><a id="layout18-table-2-row-1"></a><a id="layout18-table-2-row-2"></a><a id="layout18-table-2-row-3"></a><a id="layout18-table-2-row-4"></a><a id="layout18-table-7-row-1"></a><a id="layout18-table-7-row-2"></a><a id="layout18-table-7-row-3"></a><a id="layout18-table-7-row-4"></a>

</details>


<div align="center">

# 🖥️ 원본 실험 · 조직영상 화면과 학습 노트북

**Streamlit 화면은 업로드 영상을 224×224로 전처리해 Model.h5의 조직영상 5라벨 예측을 표시합니다. 함께 있는 학습 노트북은 MobileNetV2의 3클래스 구성이어서 그대로 같은 모델로 간주하면 안 됩니다.**

**기술 분류:** 의료 영상 코드 › Streamlit·TensorFlow › 조직영상 예측 화면

[목적](#purpose) · [기능](#features) · [입출력](#flow) · [구성](#files) · [준비](#setup) · [사용법](#usage) · [결과](#results) · [제약](#limits) · [변경](#changes)

</div>

<a name="purpose"></a>

## 🎯 이 단계에서 하는 일

입력 화면·전처리·분류 모델·클래스 순서를 연결해 읽는 초기 코드 자료입니다. CT의 ResNet50 변환 실험과 별도 목적의 원본 구성입니다.

<a name="features"></a>

## 🧩 주요 기능과 처리 방식

| 구성 | 실제 역할 |
| --- | --- |
| 전처리 | preprocess_image가 영상을 224×224로 맞추고 255로 나누어 배치 차원을 추가합니다. |
| 5라벨 화면 | 대장선암·대장정상·폐선암·폐정상·폐편평상피암의 예측 확률을 표시합니다. |
| 그래프 | 예측 확률을 텍스트와 원형 그래프로 보여 줍니다. |
| 학습 사본 | Train.ipynb의 MobileNetV2 3클래스·224·batch16·10epoch와 화면의 5라벨을 구분합니다. |

<a name="flow"></a>

## 🔄 입력 → 처리 → 출력

| 입력 | 처리 | 출력·읽을 결과 |
| --- | --- | --- |
| 업로드 조직영상 | 224×224·정규화 | 모델 입력 |
| Model.h5 | 예측 벡터와 5라벨 연결 | 클래스별 확률 |
| 예측 확률 | 텍스트·원형 그래프 | 연구용 화면 |

<a name="files"></a>

## 📁 파일과 핵심 처리

| 파일 | 이용 방법 |
| --- | --- |
| [원본 실험/Lung Cancer/main.py](../../%EC%9B%90%EB%B3%B8%20%EC%8B%A4%ED%97%98/Lung%20Cancer/main.py) | 처리 함수와 실행 조건 |
| [원본 실험/Lung Cancer/Train.ipynb](../../%EC%9B%90%EB%B3%B8%20%EC%8B%A4%ED%97%98/Lung%20Cancer/Train.ipynb) | 설정·함수·실행 셀 |

### 🔎 함수·셀로 찾아가기

아래 이름은 해당 파일의 실제 정의입니다. 위 처리 설명과 함께 설정·호출 순서·출력 경로를 따라 읽습니다.

| 파일 | 핵심 정의 |
| --- | --- |
| [원본 실험/Lung Cancer/main.py](../../%EC%9B%90%EB%B3%B8%20%EC%8B%A4%ED%97%98/Lung%20Cancer/main.py) | 소스: `preprocess_image` · `predict_cancer` · `plot_pie_chart` |

<a name="setup"></a>

## ⚙️ 환경과 설정

| 항목 | 조건·기본값 |
| --- | --- |
| 환경 | Streamlit·TensorFlow·NumPy·Matplotlib |
| 입력 크기 | 224×224 |
| 모델 | 화면은 Model.h5와 5라벨 |
| 학습 노트북 | 3클래스 MobileNetV2·별도 모델 대응 확인 |

<a name="usage"></a>

## 🚀 준비와 사용 순서

1. main.py의 모델 경로와 라벨 순서를 확인합니다.
2. 모델 출력 차원이 화면의 5라벨과 같은지 확인합니다.
3. 환경과 일치하는 모델을 준비하고 해당 폴더에서 Streamlit 앱을 엽니다.
4. 업로드 영상의 전처리와 확률 표시를 읽으며 학습 노트북의 모델과 혼합하지 않습니다.

<a name="results"></a>

## 📊 결과를 읽는 방법

화면의 확률은 지정한 모델의 출력입니다. 5라벨 화면과 3클래스 학습 파일은 같은 모델이라는 근거가 필요합니다.

이 초기 조직영상 코드는 후속 CT 비식별화 실험과 입력·모델이 다릅니다. 실제 진단 결과를 제공하는 자료로 해석하지 않습니다.

<a name="limits"></a>

## 🛠️ 알려진 제약과 확인 지점

| 상황 | 확인할 내용 |
| --- | --- |
| 모델 불일치 | 5라벨 화면과 3클래스 학습의 모델·라벨 대응을 먼저 확인합니다. |
| 입력 범위 | 조직영상과 CT를 구분합니다. |
| 사용 목적 | 연구용 예측 화면이며 임상 진단 승인 자료가 아닙니다. |

<a name="changes"></a>

## 🔀 이전 단계와의 변화

초기 화면과 학습 코드를 보관한 기본 자료입니다. 후속 ResNet50 입력·특징 변환 실험과 별도로 읽습니다.

[🔎 직전 단계 전체 비교·구성](../revision-diffs/experiment-13.diff) · [📋 전체 파일 크기·해시](../revision-manifests/experiment-13.json)

<details>
<summary>📎 이 단계의 파일 기록과 전체 해시</summary>

아래 표는 해당 단계가 기록될 당시의 파일 정보입니다. 현재 첨부는 [프로젝트 자료 안내](../PAPERS.md)에서 확인할 수 있습니다.

| 파일 | 종류 | 바이트 | SHA-256 |
|---|---|---:|---|
| [원본 실험/Lung Cancer/main.ipynb](../../%EC%9B%90%EB%B3%B8%20%EC%8B%A4%ED%97%98/Lung%20Cancer/main.ipynb) | .ipynb | 3163 | `645bbc4f163ee9a8fb2120e4ef7f6cc6ec447c080a315b076967e3808d2c6f90` |
| [원본 실험/Lung Cancer/main.py](../../%EC%9B%90%EB%B3%B8%20%EC%8B%A4%ED%97%98/Lung%20Cancer/main.py) | .py | 1651 | `e9d1cab540e21c3730a0f4dd47a94964a5722c069c9489e5f0ba800e2a7a68e8` |
| [원본 실험/Lung Cancer/Train.ipynb](../../%EC%9B%90%EB%B3%B8%20%EC%8B%A4%ED%97%98/Lung%20Cancer/Train.ipynb) | .ipynb | 3491 | `ffa9c77e4f9004dcb8e0c0eec3f1911f9d71518d1038bd8bc07a5031fd62a5d9` |
| [원본자료/원본 실험/Lung Cancer/main.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%9B%90%EB%B3%B8%20%EC%8B%A4%ED%97%98/Lung%20Cancer/main.ipynb) | .ipynb | 3163 | `645bbc4f163ee9a8fb2120e4ef7f6cc6ec447c080a315b076967e3808d2c6f90` |
| [원본자료/원본 실험/Lung Cancer/main.py](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%9B%90%EB%B3%B8%20%EC%8B%A4%ED%97%98/Lung%20Cancer/main.py) | .py | 1651 | `e9d1cab540e21c3730a0f4dd47a94964a5722c069c9489e5f0ba800e2a7a68e8` |
| [원본자료/원본 실험/Lung Cancer/Train.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%9B%90%EB%B3%B8%20%EC%8B%A4%ED%97%98/Lung%20Cancer/Train.ipynb) | .ipynb | 4028 | `efc1cc1f4d2c17e399e6aead9645527852a6445703db00683327400f06b6c139` |
| [원본자료/원본 실험/LungCancerClassification-main/main.py](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%9B%90%EB%B3%B8%20%EC%8B%A4%ED%97%98/LungCancerClassification-main/main.py) | .py | 1651 | `e9d1cab540e21c3730a0f4dd47a94964a5722c069c9489e5f0ba800e2a7a68e8` |
| [원본자료/원본 실험/LungCancerClassification-main/trainer.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%9B%90%EB%B3%B8%20%EC%8B%A4%ED%97%98/LungCancerClassification-main/trainer.ipynb) | .ipynb | 30177 | `d806b5df96a6c148fa4fc3905d1888e1a20c9493208bbe15b0239b2816735820` |
| [원본자료/원본 실험/LungCancerClassification-main/LICENSE](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%9B%90%EB%B3%B8%20%EC%8B%A4%ED%97%98/LungCancerClassification-main/LICENSE) |  | 1068 | `7af98bcd79c5f6c6ddaf6399f3782e6e2c1336c87800b3a4affee46546bd9129` |
| [원본자료/원본 실험/LungCancerClassification-main/README.md](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%9B%90%EB%B3%B8%20%EC%8B%A4%ED%97%98/LungCancerClassification-main/README.md) | .md | 4498 | `f47ba9b58041760d2651f9fe0f7fff32261ea1fb5e0ef075616f07579a284391` |
| [원본자료/원본 실험/LungCancerClassification-main/confusion_matrix.png](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%9B%90%EB%B3%B8%20%EC%8B%A4%ED%97%98/LungCancerClassification-main/confusion_matrix.png) | .png | 90242 | `1deeddc5d7501f2de854781c480081ff2eebfd07bd5ff7ddfa77981cbe2a3bde` |
| [원본자료/원본 실험/LungCancerClassification-main/confusion_matrix (2).png](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%9B%90%EB%B3%B8%20%EC%8B%A4%ED%97%98/LungCancerClassification-main/confusion_matrix%20%282%29.png) | .png | 90242 | `1deeddc5d7501f2de854781c480081ff2eebfd07bd5ff7ddfa77981cbe2a3bde` |

</details>

---

[🏠 프로젝트](../../README.md) · [🗂️ 전체 차수](../REVISION_INDEX.md) · [📁 자료 폴더](../../%EC%9B%90%EB%B3%B8%20%EC%8B%A4%ED%97%98/Lung%20Cancer)

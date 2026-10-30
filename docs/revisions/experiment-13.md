# 📚 원본 실험 · 기본

224×224 조직영상 5라벨 Streamlit 앱과 MobileNetV2 3클래스 학습을 보관합니다. 두 코드의 출력 라벨·모델 파일이 다릅니다.

### 🖥️ 초기 화면과 학습 모델의 구분

`Lung Cancer/main.py`의 `preprocess_image`는 업로드 영상을 224×224로 만들고 255로 나눕니다. `Model.h5`의 예측을 대장 선암·대장 정상·폐 선암·폐 정상·폐 편평상피암의 **조직영상 5라벨**과 연결하여 확률·원형 그래프로 표시합니다.

같은 폴더 `Train.ipynb`의 셀 0은 ImageNet MobileNetV2를 동결하고 GAP·Dropout 0.3·3클래스 softmax를 학습해 `LungCancer_3Class_Model.h5`로 저장합니다. 앱의 5라벨 출력과 이 학습기의 3클래스 출력은 다르므로 파일명 변경만으로 서로 연결할 수 없습니다.

함께 보관한 `LungCancerClassification-main`은 별도 README·LICENSE·학습 코드와 혼동행렬 자료를 가진 초기 코드 묶음입니다. 이 폴더의 화면이나 혼동행렬을 연구 1·2의 CT 3분류 결과로 합산하지 않습니다. 초기 앱 실행에는 실제 입력에 맞는 모델·라벨 대응이 필요합니다.

셀 번호는 노트북의 전체 셀을 0부터 센 값입니다. 아래 파일 표에서 소스와 보관 결과를 각각 열 수 있습니다.

[전체 차수](../REVISION_INDEX.md) · [첫 화면](../../README.md) · [직전 단계 전체 비교](../revision-diffs/experiment-13.diff) · [전체 파일 크기·해시](../revision-manifests/experiment-13.json)

직전 단계: 확인된 비교 대상 없음.

## 📁 실제 파일

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

## 🔎 해석·검증 범위

원고는 원고 보고값, 저장된 표는 당시 결과 파일, 노트북은 구현 자료입니다. 재학습·임상 검증·전체 실행 재현은 수행하지 않았습니다. 파일 비교와 PDF 내용 확인은 실제 기능 실행의 성공을 대신하지 않습니다. 원본의 알려진 오류와 0바이트 자료는 보존하며 성공으로 보정하지 않습니다.

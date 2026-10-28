# 📚 연구 1

블러와 블록 재배열이 폐 CT 3분류에 미치는 영향을 비교한 하계 연구입니다.

- [근거 자료](../../%EB%85%BC%EB%AC%B8/1%EC%B0%A8_EfficientNetV2-S_%ED%95%98%EA%B3%84_%EC%B5%9C%EC%A2%85.pdf)
- [전체 보관 기록](../VERSIONS.md) · [프로젝트 소개](../../README.md)

## 🔎 범위와 해석

연구 1은 EfficientNetV2-S를 사용한 초기 비교 연구입니다.


## 🧩 주요 내용

- 512×512 입력과 EfficientNetV2-S에서 블러·블록 조건의 정확도·ROC-AUC·혼동행렬을 비교합니다.
- Train.ipynb의 셀 1·2는 각각 블록 재배열·Gaussian Blur와 EfficientNetV2-S 학습을 구성합니다. 5클래스 조직영상 CNN은 별도 셀에 구성했습니다.
- 하계 그래프 노트북은 기존 결과 JSON을 읽어 도표를 만듭니다. 도표 재생성과 학습 재현은 다릅니다.

## 🔄 자료 구성

연구 2에서 ResNet50과 구조 유사도 점수·100개 조합 비교로 연구 범위를 확장합니다. 연구 1의 표본 수·분할을 연구 2의 값으로 보충하지 않습니다.

## 📍 관련 자료

- [논문/1차_EfficientNetV2-S_하계_최종.pdf](../../%EB%85%BC%EB%AC%B8/1%EC%B0%A8_EfficientNetV2-S_%ED%95%98%EA%B3%84_%EC%B5%9C%EC%A2%85.pdf) · `실험 방법 및 결과` · PDF 1–3쪽
- [추가 학습모델과 실험/Train.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/Train.ipynb) · `EfficientNetV2S` · 셀 1 소스 13행; 셀 1 소스 403행; 셀 1 소스 406행; 셀 1 소스 544행; 셀 2 소스 13행; 셀 2 소스 410행
- [연구1_하계_EfficientNetV2-S/그래프/Blur_Block_1차_그래프_white.ipynb](../../%EC%97%B0%EA%B5%AC1_%ED%95%98%EA%B3%84_EfficientNetV2-S/%EA%B7%B8%EB%9E%98%ED%94%84/Blur_Block_1%EC%B0%A8_%EA%B7%B8%EB%9E%98%ED%94%84_white.ipynb) · `json.load` · 셀 0 소스 64행; 셀 1 소스 58행

셀 번호는 0부터, 소스 행 번호와 PDF 쪽 번호는 1부터 셉니다. 

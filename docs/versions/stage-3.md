<div align="center">

# 📚 후속 특징맵

ResNet50의 pool1_pool 특징에 채널별 고정 Gaussian 커널을 depthwise_conv2d로 적용합니다.

</div>

[📖 목적·구성·사용법·결과의 상세 안내](../revisions/experiment-12.md) · [🏠 프로젝트](../../README.md) · [🗂️ 전체 차수](../REVISION_INDEX.md)

## 🧭 이 자료를 읽는 순서

1. 설정 셀에서 입력·작업·결과 경로와 변환 조건을 확인합니다.
2. 분할·증강 함수의 호출 순서와 시험 자료가 분리되는 지점을 읽습니다.
3. GPU·TensorFlow·학습 자료를 준비하고 설치·모니터·학습·출력 셀을 구분해 순서대로 읽습니다.
4. 기존 결과의 재사용 조건을 확인한 뒤 필요한 조건을 선택합니다.
5. 조건별 JSON과 혼동행렬·ROC-AUC·Recall을 같은 분모와 클래스 순서로 비교합니다.

## 🔎 연결된 내용

| 구성 | 읽을 내용 |
| --- | --- |
| 변환 위치 | ResNet50의 pool1_pool 특징에 채널별 고정 Gaussian 커널을 depthwise_conv2d로 적용합니다. |
| 모델 연결 | edge→FeatureGaussianBlur→cloud 순서로 연결합니다. |
| 분할·증강 | 원본 test를 먼저 분리하고 학습 쪽을 증강합니다. |
| 입력과 증강 | JPEG 3채널을 512×512 float32로 읽습니다. 학습에서는 좌우·상하 반전, 밝기·대비·잡음을 적용하며 평가 입력과 구분합니다. |
| 분류 헤드 | GAP와 GMP를 연결하고 Dense512→BatchNorm·ReLU·Dropout0.35→Dense256→BatchNorm·ReLU·Dropout0.25→softmax로 분류합니다. |
| 평가·저장 | 조건별 정확도·ROC-AUC·클래스별 Recall·혼동행렬과 모델·그래프 출력을 구분합니다. |
| 테스트 의사 라벨 | 테스트 예측의 최대 확률이 0.88 이상인 영상을 예측 라벨로 학습 자료에 추가하는 후속 경로가 있습니다. |
| 추가 분석 | 특징 SSIM·cosine과 선택적 디코더 복원의 PSNR/SSIM 경로를 제공합니다. 설정과 저장된 결과를 구분합니다. |


## 📊 해석 범위

σ32·64·128·256은 전역 평균 분기로 처리됩니다. REUSE_COLLAPSED_RESULTS를 켜면 같은 분기의 결과를 재사용합니다.

[➡️ 전체 설명으로 이동](../revisions/experiment-12.md)

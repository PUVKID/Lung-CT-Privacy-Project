# 📚 후속 특징맵

입력 영상 대신 ResNet50의 pool1_pool 특징에 블러를 넣고 복원 가능성을 살펴보는 후속 코드입니다.

- [근거 자료](../../%EB%B8%94%EB%9F%AC%20%EC%8A%A4%ED%85%8C%EC%9D%B4%EC%A7%80%201%20%EC%97%A3%EC%A7%80/stage1_edge_feature_blur_resnet50.ipynb)
- [전체 보관 기록](../VERSIONS.md) · [프로젝트 소개](../../README.md)

## 🔎 범위와 해석

복원 공격 평가는 후속 연구 과제입니다.


## 🧩 주요 내용

- build_edge_model과 cloud 모델을 같은 프로세스에서 연결합니다. pool1_pool 특징 경계이며 실제 네트워크 전송 구현은 아닙니다.
- 큰 σ에서 전역 평균 대체와 REUSE_COLLAPSED_RESULTS 기본 재사용을 합니다. 열 σ 조건에는 결과를 재사용하는 조건이 포함됩니다.
- decoder로 영상 복원을 학습하고 PSNR·SSIM을 계산하는 경로가 있지만 Conv2D import/정의 누락과 대체 가중치·예시 결과 분기를 고려해야 합니다.

## 🔄 자료 구성

연구 2의 입력 MS-SSIM 점수와 달리 특징 SSIM·cosine 및 decoder 복원을 다룹니다. 원고의 후속 과제를 이미 실험 완료한 것으로 소급하지 않습니다.

## 📍 관련 자료

- [블러 스테이지 1 엣지/stage1_edge_feature_blur_resnet50.ipynb](../../%EB%B8%94%EB%9F%AC%20%EC%8A%A4%ED%85%8C%EC%9D%B4%EC%A7%80%201%20%EC%97%A3%EC%A7%80/stage1_edge_feature_blur_resnet50.ipynb) · `def build_edge_model` · 셀 16 소스 70행
- [블러 스테이지 1 엣지/stage1_edge_feature_blur_resnet50.ipynb](../../%EB%B8%94%EB%9F%AC%20%EC%8A%A4%ED%85%8C%EC%9D%B4%EC%A7%80%201%20%EC%97%A3%EC%A7%80/stage1_edge_feature_blur_resnet50.ipynb) · `REUSE_COLLAPSED_RESULTS` · 셀 7 소스 14행; 셀 8 소스 3행; 셀 26 소스 62행
- [블러 스테이지 1 엣지/stage1_edge_feature_blur_resnet50.ipynb](../../%EB%B8%94%EB%9F%AC%20%EC%8A%A4%ED%85%8C%EC%9D%B4%EC%A7%80%201%20%EC%97%A3%EC%A7%80/stage1_edge_feature_blur_resnet50.ipynb) · `def build_reconstruction_decoder` · 셀 22 소스 1행

셀 번호는 0부터, 소스 행 번호와 PDF 쪽 번호는 1부터 셉니다. 

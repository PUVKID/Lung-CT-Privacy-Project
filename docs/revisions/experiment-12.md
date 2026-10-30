# 📚 블러 스테이지 1 엣지 · 기본

pool1_pool 특징 자체에 블러를 적용합니다. 특징 SSIM·cosine 및 복원 PSNR/SSIM 코드가 있으며 큰 σ 결과를 재사용합니다.

### 🧠 영상 대신 Stage 1 특징을 변환

`stage1_edge_feature_blur_resnet50.ipynb`의 셀 10은 원본 테스트를 분리하고 학습 자료를 증강합니다. 셀 16은 ResNet50의 `pool1_pool` 특징에 `FeatureGaussianBlur`를 삽입합니다. 채널별 고정 Gaussian 커널을 `depthwise_conv2d`로 적용하고 이후 cloud 분류 부분에 전달합니다.

셀 8은 σ0~256의 10조건을 지정하지만, 셀 16에서 커널 반경이 특징 크기에 비해 커지면 각 채널의 전역 평균을 공간 전체로 복제합니다. 기본 `REUSE_COLLAPSED_RESULTS=True`와 셀 26의 재사용 분기 때문에 σ32 결과가 σ64·128·256에 재사용됩니다. 열 조건의 독립 재학습 결과와 구별해야 합니다.

셀 20은 블러 전후 채널 평균 특징맵을 각각 정규화한 뒤 **단일 SSIM**으로 `50×(1−SSIM)`을 계산하고 GAP 벡터의 클래스 내·간 cosine 유사도를 구합니다. 연구 2의 원본·변환 **입력 영상 MS-SSIM** 점수와 평가 대상·계산법이 다릅니다.

셀 22에는 동결한 edge의 특징으로 decoder를 학습해 영상을 복원하고 PSNR·SSIM을 계산하는 경로가 있습니다. 다만 `Conv2D` import/정의 누락, edge 가중치가 없을 때 초기 가중치를 사용하는 흐름, 예시 결과 분기가 남아 있습니다. 복원 코드의 존재를 공격 실험 완료나 프라이버시 보증으로 해석하지 않습니다.

셀 번호는 노트북의 전체 셀을 0부터 센 값입니다. 아래 파일 표에서 소스와 보관 결과를 각각 열 수 있습니다.

[전체 차수](../REVISION_INDEX.md) · [첫 화면](../../README.md) · [직전 단계 전체 비교](../revision-diffs/experiment-12.diff) · [전체 파일 크기·해시](../revision-manifests/experiment-12.json)

직전 단계: 확인된 비교 대상 없음.

## 📁 실제 파일

| 파일 | 종류 | 바이트 | SHA-256 |
|---|---|---:|---|
| [블러 스테이지 1 엣지/stage1_edge_feature_blur_resnet50.ipynb](../../%EB%B8%94%EB%9F%AC%20%EC%8A%A4%ED%85%8C%EC%9D%B4%EC%A7%80%201%20%EC%97%A3%EC%A7%80/stage1_edge_feature_blur_resnet50.ipynb) | .ipynb | 136775 | `069080fa81d3e1f740d9cb0f9433b3a6cb1184a3af6a626956bc4b948cc87caa` |
| [원본자료/블러 스테이지 1 엣지/stage1_edge_feature_blur_resnet50.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EB%B8%94%EB%9F%AC%20%EC%8A%A4%ED%85%8C%EC%9D%B4%EC%A7%80%201%20%EC%97%A3%EC%A7%80/stage1_edge_feature_blur_resnet50.ipynb) | .ipynb | 136774 | `31f78836099ec69365232e8a30071e8b6f4ed0bb70491b29f2b08a6dcfcb51e1` |
| [원본자료/블러 스테이지 1 엣지/stage1_feature_blur_resnet50_outputs/results/all_stage1_feature_blur_results_resnet50_stage1_feature_blur_resnet50_v1.json](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EB%B8%94%EB%9F%AC%20%EC%8A%A4%ED%85%8C%EC%9D%B4%EC%A7%80%201%20%EC%97%A3%EC%A7%80/stage1_feature_blur_resnet50_outputs/results/all_stage1_feature_blur_results_resnet50_stage1_feature_blur_resnet50_v1.json) | .json | 7731 | `74122d318190860fb214e01725ce4bc8d81e1abe533c67be64beb5224dd7f802` |

## 🔎 해석·검증 범위

원고는 원고 보고값, 저장된 표는 당시 결과 파일, 노트북은 구현 자료입니다. 재학습·임상 검증·전체 실행 재현은 수행하지 않았습니다. 파일 비교와 PDF 내용 확인은 실제 기능 실행의 성공을 대신하지 않습니다. 원본의 알려진 오류와 0바이트 자료는 보존하며 성공으로 보정하지 않습니다.

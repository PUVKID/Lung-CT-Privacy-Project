<div align="center">

# 🗂️ 차수별 프로젝트 안내

연구 원고·실험 코드·발표 자료의 목적과 사용 순서를 단계별로 살펴봅니다.

</div>

[🏠 프로젝트 전체 소개](../README.md)

| 단계 | 이 단계의 목적 | 자료 | 직전 변화 |
| --- | --- | --- | --- |
| [연구1 · 하계 EfficientNetV2-S](revisions/study-1.md) | EfficientNetV2-S에서 입력 CT 영상에 Gaussian Blur와 블록 재배열을 각각 적용했을 때 분류 결과가 어떻게 달라지는지 비교한 하계 3쪽 연구입니다. | [폴더](../%EB%85%BC%EB%AC%B8) | [전체 비교](revision-diffs/study-1.diff) |
| [연구2 · ResNet50 후속 원고](revisions/study-2.md) | ResNet50에서 Block·Blur 단독 20조건과 Block→Blur 조합 100조건을 비교하고, 분류 정확도와 영상 유사도 기반 점수를 함께 읽는 19쪽 후속 원고입니다. | [폴더](../%EB%85%BC%EB%AC%B8) | [전체 비교](revision-diffs/study-2.diff) |
| [1차](revisions/folder-1.md) | 블록·블러의 rebuilt·same_settings·metric_matched 변형과 노트북 수정 보조 스크립트를 함께 읽는 코드 자료 차수입니다. | [폴더](../1%EC%B0%A8) | [전체 비교](revision-diffs/folder-1.diff) |
| [폴더 2차](revisions/folder-2.md) | 기존 Blur·Block 노트북의 학습·모니터 출력을 맞추고 Block→Blur 조합 노트북을 만드는 JavaScript 보조 도구 단계입니다. | [폴더](../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/2%EC%B0%A8) | [전체 비교](revision-diffs/folder-2.diff) |
| [폴더 3차](revisions/folder-3.md) | SSIM에서 DSSIM 기반 Privacy Score를 계산하는 경로와 3장·8조건의 저장 결과를 확인하는 자료 차수입니다. 전체 논문의 1,097장 실험과 구분합니다. | [폴더](../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/tables) | [전체 비교](revision-diffs/folder-3.diff) |
| [폴더 4차](revisions/folder-4.md) | ResNet50 후속 원고와 입력 변환·유사도·도표 코드를 연결해 읽는 자료 차수입니다. 실제 코드 폴더는 자료차수/4차/코드에 있습니다. | [폴더](../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/4%EC%B0%A8/%EC%BD%94%EB%93%9C) | [전체 비교](revision-diffs/folder-4.diff) |
| [블러 · 2차 실험](revisions/experiment-6.md) | 입력 영상에 PIL GaussianBlur를 적용하는 10조건 실험입니다. σ0은 원본 배열을 복사합니다. | [폴더](../%EB%B8%94%EB%9F%AC/2%EC%B0%A8%20%EC%8B%A4%ED%97%98) | [전체 비교](revision-diffs/experiment-6.diff) |
| [블록 · 2차 실험](revisions/experiment-7.md) | 시드로 정한 순열에 따라 입력 블록의 위치를 바꾸며 블록 내부 픽셀 배열은 유지합니다. 영상보다 작지 않은 블록은 원본을 복사합니다. | [폴더](../%EB%B8%94%EB%A1%9D/2%EC%B0%A8%20%EC%8B%A4%ED%97%98) | [전체 비교](revision-diffs/experiment-7.diff) |
| [블록+블러 · 기본](revisions/experiment-8.md) | 블록 10개와 블러 10개의 100조합을 비교합니다. 입력 영상을 블록 재배열한 뒤 Gaussian Blur를 적용합니다. | [폴더](../%EB%B8%94%EB%A1%9D%2B%EB%B8%94%EB%9F%AC) | [전체 비교](revision-diffs/experiment-8.diff) |
| [블러 엣지 · 기본](revisions/experiment-9.md) | 입력 영상을 블러 처리한 뒤 ResNet50의 pool1_pool 경계에서 edge와 cloud로 나눈 모델을 연결합니다. | [폴더](../%EB%B8%94%EB%9F%AC%20%EC%97%A3%EC%A7%80) | [전체 비교](revision-diffs/experiment-9.diff) |
| [블록 엣지 · 기본](revisions/experiment-10.md) | 입력 블록을 재배열한 뒤 pool1_pool 경계에서 edge와 cloud로 나눈 모델을 학습합니다. | [폴더](../%EB%B8%94%EB%A1%9D%20%EC%97%A3%EC%A7%80) | [전체 비교](revision-diffs/experiment-10.diff) |
| [블록+블러 엣지 · 기본](revisions/experiment-11.md) | 입력 Block→Blur의 100조합 뒤에 분리 모델을 연결합니다. 경계 특징에 FeatureGaussianBlur를 넣는 Stage1 실험과 변환 위치가 다릅니다. | [폴더](../%EB%B8%94%EB%A1%9D%2B%EB%B8%94%EB%9F%AC%20%EC%97%A3%EC%A7%80) | [전체 비교](revision-diffs/experiment-11.diff) |
| [블러 스테이지 1 엣지 · 기본](revisions/experiment-12.md) | ResNet50의 pool1_pool 특징에 채널별 고정 Gaussian 커널을 depthwise_conv2d로 적용합니다. | [폴더](../%EB%B8%94%EB%9F%AC%20%EC%8A%A4%ED%85%8C%EC%9D%B4%EC%A7%80%201%20%EC%97%A3%EC%A7%80) | [전체 비교](revision-diffs/experiment-12.diff) |
| [원본 실험 · 기본](revisions/experiment-13.md) | Streamlit 화면은 업로드 영상을 224×224로 전처리해 Model.h5의 조직영상 5라벨 예측을 표시합니다. 함께 있는 학습 노트북은 MobileNetV2의 3클래스 구성이어서 그대로 같은 모델로 간주하면 안 됩니다. | [폴더](../%EC%9B%90%EB%B3%B8%20%EC%8B%A4%ED%97%98/Lung%20Cancer) | [전체 비교](revision-diffs/experiment-13.diff) |
| [추가 학습모델과 실험 · 기본](revisions/experiment-14.md) | EfficientNetV2-S·MobileNetV2·ResNet50의 서로 다른 학습 셀과 SSIM/MS-SSIM·도표 코드를 모은 자료입니다. | [폴더](../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98) | [전체 비교](revision-diffs/experiment-14.diff) |
| [블러 · 1차 실험](revisions/experiment-original-blur.md) | 입력 변환 조건별 정확도·ROC-AUC·클래스별 Recall·혼동행렬을 보관한 결과 JSON입니다. 저장 결과와 그래프 입력을 대조할 수 있습니다. | [폴더](../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EB%B8%94%EB%9F%AC/1%EC%B0%A8%20%EC%8B%A4%ED%97%98/%EB%B8%94%EB%9F%AC%201/%EB%B8%94%EB%9F%AC%EB%A7%81%20%EA%B2%B0%EA%B3%BC) | [전체 비교](revision-diffs/experiment-original-blur.diff) |
| [블록 · 1차 실험](revisions/experiment-original-block.md) | 입력 변환 조건별 정확도·ROC-AUC·클래스별 Recall·혼동행렬을 보관한 결과 JSON입니다. 저장 결과와 그래프 입력을 대조할 수 있습니다. | [폴더](../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EB%B8%94%EB%A1%9D/1%EC%B0%A8%20%EC%8B%A4%ED%97%98/%EB%B8%94%EB%A1%9D%201/%EB%B6%88%EB%A1%9D%20%EA%B2%B0%EA%B3%BC) | [전체 비교](revision-diffs/experiment-original-block.diff) |


## 📚 자료 이용

각 상세 설명은 입력·처리·출력과 파일 구성, 설정·사용법 및 결과 해석을 연결합니다. 원고는 연구별 최신 전체 문서로, 코드와 실험 기록은 해당 단계의 자료로 연결합니다.

[📄 최신 논문·발표·편집 원본](PAPERS.md)

[📝 안내 변경 기록](changes/2026-11-03-%EC%B0%A8%EC%88%98%EB%B3%84%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8%EC%95%88%EB%82%B4.md)

## 🧪 Conv1 OK/NG 예비실험

| 차수 | 폴더 | 설명 | 비교 |
|---|---|---|---|
| Conv1 블러 OK-NG 실험 · 1차 | [폴더](../Conv1%20%EB%B8%94%EB%9F%AC%20OK-NG%20%EC%8B%A4%ED%97%98/1%EC%B0%A8) | [설명](revisions/conv1-okng-round1.md) | [전체 비교](revision-diffs/conv1-okng-round1.diff) |
| Conv1 블러 OK-NG 실험 · 2차 | [폴더](../Conv1%20%EB%B8%94%EB%9F%AC%20OK-NG%20%EC%8B%A4%ED%97%98/2%EC%B0%A8) | [설명](revisions/conv1-okng-round2.md) | [전체 비교](revision-diffs/conv1-okng-round2.diff) |

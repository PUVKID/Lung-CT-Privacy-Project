# 📚 블록+블러 엣지 · 기본

입력 Block→Blur 100조합을 분리 모델로 학습합니다. 특징 자체의 블러 없이 edge/cloud를 같은 프로세스에서 연결합니다.

### 🧩🌫️ 조합 입력과 edge/cloud 연결

`block_blur_resnet50_edge.ipynb`의 셀 8·10은 블록 10개×σ 10개의 입력 Block→Blur 조합을 만듭니다. 셀 20의 `build_full_pipeline`은 `pool1_pool`까지의 edge와 나머지 ResNet50·분류 헤드를 연결합니다. 특징 경계에 `FeatureGaussianBlur`를 넣지 않으므로 Stage 1 특징 블러와 변환 위치가 다릅니다.

셀 24는 테스트 분리 후 학습 자료를 증강하고, 두 부분을 처음부터 함께 학습하도록 구성합니다. fold별 edge 가중치·cloud 모델, 조합별 정확도·ROC-AUC·클래스별 Recall·혼동행렬을 저장하는 경로가 있습니다. 셀 20의 `save_feature_map`은 조합별 입력과 Stage 1 특징 시각화를 구성합니다.

일반 100조합 노트북과의 주요 차이는 모델 분리·전체 동시 학습·부분 모델 저장입니다. TTA와 테스트 의사 라벨 사용, 증강 자료의 fold 분리, `training=True` 고정 호출과 저장 순서는 별도 점검 대상입니다. 실제 원격 전송이나 기기별 지연을 측정한 구현으로 해석하지 않습니다.

셀 번호는 노트북의 전체 셀을 0부터 센 값입니다. 아래 파일 표에서 소스와 보관 결과를 각각 열 수 있습니다.

[전체 차수](../REVISION_INDEX.md) · [첫 화면](../../README.md) · [직전 단계 전체 비교](../revision-diffs/experiment-11.diff) · [전체 파일 크기·해시](../revision-manifests/experiment-11.json)

직전 단계: 확인된 비교 대상 없음.

## 📁 실제 파일

| 파일 | 종류 | 바이트 | SHA-256 |
|---|---|---:|---|
| [블록+블러 엣지/block_blur_resnet50_edge.ipynb](../../%EB%B8%94%EB%A1%9D%2B%EB%B8%94%EB%9F%AC%20%EC%97%A3%EC%A7%80/block_blur_resnet50_edge.ipynb) | .ipynb | 146001 | `18e20095343029c59e5790c4f1a6dd0b52e678447688e5b2f16a55c28b853068` |
| [원본자료/블록+블러 엣지/block_blur_resnet50_edge.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EB%B8%94%EB%A1%9D%2B%EB%B8%94%EB%9F%AC%20%EC%97%A3%EC%A7%80/block_blur_resnet50_edge.ipynb) | .ipynb | 146579 | `a0014cc25d144a8e478967a77faec43035f547cbe1f2a13ff3b91d59d2a51370` |

## 🔎 해석·검증 범위

원고는 원고 보고값, 저장된 표는 당시 결과 파일, 노트북은 구현 자료입니다. 재학습·임상 검증·전체 실행 재현은 수행하지 않았습니다. 파일 비교와 PDF 내용 확인은 실제 기능 실행의 성공을 대신하지 않습니다. 원본의 알려진 오류와 0바이트 자료는 보존하며 성공으로 보정하지 않습니다.

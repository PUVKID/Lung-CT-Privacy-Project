# 📚 블록 엣지 · 기본

입력 블록 재배열 10조건을 pool1_pool 경계의 분리 모델로 학습합니다. 블록별 특징 그림과 edge·cloud 가중치를 저장합니다.

### 🧩 입력 블록을 사용하는 분리 모델

`block_encryption_resnet50_edge_v2.ipynb`의 셀 8·10은 블록 크기 512~1의 10조건과 입력 영상 재배열을 정의합니다. 셀 20은 ResNet50의 `pool1_pool`에서 edge/cloud를 나누고, 128×128×64 특징을 cloud 부분의 입력으로 연결합니다. 블록 변환은 이 경계 이전의 **영상**에 적용됩니다.

일반 블록 사본의 백본 동결·미세조정 구성과 달리 셀 20·24는 처음부터 전체 분리 모델 학습을 허용합니다. 셀 24는 증강 후 테스트를 나누며 fold 앙상블·TTA·테스트 의사 라벨 추가 학습 뒤 정확도·ROC-AUC·클래스별 Recall·혼동행렬을 반환합니다. edge 가중치·cloud 모델의 별도 저장과 블록별 특징 시각화가 추가됩니다.

`build_full_pipeline`의 edge 호출에는 `training=True`가 고정되어 있습니다. 추론 시 동작과 부분 가중치·최종 모델의 저장 시점을 점검해야 합니다. 이 코드는 동일 프로세스의 모델 분리이며, 재배열 특징의 공격 저항성이나 실제 분산 장치 성능 측정 결과는 아닙니다.

셀 번호는 노트북의 전체 셀을 0부터 센 값입니다. 아래 파일 표에서 소스와 보관 결과를 각각 열 수 있습니다.

[전체 차수](../REVISION_INDEX.md) · [첫 화면](../../README.md) · [직전 단계 전체 비교](../revision-diffs/experiment-10.diff) · [전체 파일 크기·해시](../revision-manifests/experiment-10.json)

직전 단계: 확인된 비교 대상 없음.

## 📁 실제 파일

| 파일 | 종류 | 바이트 | SHA-256 |
|---|---|---:|---|
| [블록 엣지/block_encryption_resnet50_edge_v2.ipynb](../../%EB%B8%94%EB%A1%9D%20%EC%97%A3%EC%A7%80/block_encryption_resnet50_edge_v2.ipynb) | .ipynb | 117559 | `1a32a5a3c47f33f187dec48fb8c2cb7c1626e410e75cd88a52160a816f82a4da` |
| [원본자료/블록 엣지/all_block_results_resnet50_same_settings_gpu4090_v2.json](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EB%B8%94%EB%A1%9D%20%EC%97%A3%EC%A7%80/all_block_results_resnet50_same_settings_gpu4090_v2.json) | .json | 5065 | `08227a052f5070c5e2218b68c213e8c8c9ecc7c9f194e3d98694a2f9b9fa4811` |
| [원본자료/블록 엣지/block_encryption_resnet50_edge_v2.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EB%B8%94%EB%A1%9D%20%EC%97%A3%EC%A7%80/block_encryption_resnet50_edge_v2.ipynb) | .ipynb | 658506 | `56afa7be98a5c07badd73a3ea1db3cb54c6d819391f0142eab4547591e7171cb` |

## 🔎 해석·검증 범위

원고는 원고 보고값, 저장된 표는 당시 결과 파일, 노트북은 구현 자료입니다. 재학습·임상 검증·전체 실행 재현은 수행하지 않았습니다. 파일 비교와 PDF 내용 확인은 실제 기능 실행의 성공을 대신하지 않습니다. 원본의 알려진 오류와 0바이트 자료는 보존하며 성공으로 보정하지 않습니다.

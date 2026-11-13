<a id="-블러-엣지"></a>

# 블러 엣지

입력 영상을 블러 처리한 뒤 ResNet50의 pool1_pool 경계에서 edge와 cloud로 나눈 모델을 연결합니다.

| 주요 구성 | 내용 |
| --- | --- |
| 변환 위치 | 입력 영상을 블러 처리한 뒤 ResNet50의 pool1_pool 경계에서 edge와 cloud로 나눈 모델을 연결합니다. |
| 모델 연결 | edge와 cloud를 같은 TensorFlow 프로세스에서 연결합니다. |
| 분할·증강 | 이 사본은 증강 후 train/test를 나누는 경로입니다. |
| 입력과 증강 | JPEG 3채널을 512×512 float32로 읽습니다. 학습에서는 좌우·상하 반전, 밝기·대비·잡음을 적용하며 평가 입력과 구분합니다. |
| 분류 헤드 | GAP와 GMP를 연결하고 Dense512→BatchNorm·ReLU·Dropout0.35→Dense256→BatchNorm·ReLU·Dropout0.25→softmax로 분류합니다. |
| 평가·저장 | 조건별 정확도·ROC-AUC·클래스별 Recall·혼동행렬과 모델·그래프 출력을 구분합니다. |
| 테스트 의사 라벨 | 테스트 예측의 최대 확률이 0.88 이상인 영상을 예측 라벨로 학습 자료에 추가하는 후속 경로가 있습니다. |

<a id="-이용-순서"></a>

## 이용 순서

1. 설정 셀에서 입력·작업·결과 경로와 변환 조건을 확인합니다.
2. 분할·증강 함수의 호출 순서와 시험 자료가 분리되는 지점을 읽습니다.
3. GPU·TensorFlow·학습 자료를 준비하고 설치·모니터·학습·출력 셀을 구분해 순서대로 읽습니다.
4. 기존 결과의 재사용 조건을 확인한 뒤 필요한 조건을 선택합니다.
5. 조건별 JSON과 혼동행렬·ROC-AUC·Recall을 같은 분모와 클래스 순서로 비교합니다.

| 차수·단계 | 주요 내용 | 자료 | 직전 비교 |
| --- | --- | --- | --- |
| [블러 엣지 · 기본](../docs/revisions/experiment-9.md) | 입력 영상을 블러 처리한 뒤 ResNet50의 pool1_pool 경계에서 edge와 cloud로 나눈 모델을 연결합니다. | [폴더](.) | [전체 비교](../docs/revision-diffs/experiment-9.diff) |

[프로젝트](../README.md) · [전체 차수](../docs/REVISION_INDEX.md)

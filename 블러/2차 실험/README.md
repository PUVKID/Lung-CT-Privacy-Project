<!-- language-choice:start -->
🔵 **한국어** · [English overview](../../en/README.md)
<!-- language-choice:end -->

<a id="-블러2차-실험"></a>

# 블러/2차 실험

<!-- reading-levels17:start -->
<details>
<summary>읽기 수준 선택</summary>

| 레벨 | 읽는 목적 |
| --- | --- |
| [LEVEL 1 - Beginner](../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A81.md) | 목적과 입력·출력을 쉬운 말로 이해하기 |
| [LEVEL 2 - Explorer](../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A82.md) | 주요 기능과 전체 처리 흐름 살펴보기 |
| [LEVEL 3 - Practitioner](../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A83.md) | 설정·실행 순서와 결과 확인하기 |
| [LEVEL 4 - Advanced](../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A84.md) | 구현 선택과 조건·한계 비교하기 |
| [LEVEL 5 - Expert](../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A85.md) | 세부 근거와 재현 조건 검토하기 |

</details>
<!-- reading-levels17:end -->

입력 영상에 PIL GaussianBlur를 적용하는 10 조건 실험입니다. σ0 은 원본 배열을 복사합니다.

| 주요 구성 | 내용 |
| --- | --- |
| <a id="layout18-table-1-row-1"></a> 변환 위치 | 입력 영상에 PIL GaussianBlur를 적용하는 10 조건 실험입니다. σ0 은 원본 배열을 복사합니다. |
| <a id="layout18-table-1-row-2"></a> 모델 연결 | 일반 ResNet50 분류 모델을 사용합니다. |
| <a id="layout18-table-1-row-3"></a> 분할·증강 | 원본 train/test를 먼저 나누고 학습 쪽을 증강합니다. |
| <a id="layout18-table-1-row-4"></a> 입력과 증강 | JPEG 3 채널을 512×512 float32로 읽습니다.<br>학습에서는 좌우·상하 반 전, 밝기·대비·잡음을 적용하며 평가 입력과 구분합니다. |
| <a id="layout18-table-1-row-5"></a> 분류 헤드 | GAP와 GMP를 연결하고 Dense512 →BatchNorm·ReLU·Dropout0.35 →Dense256 →BatchNorm·ReLU·Dropout0.25 →softmax로 분류합니다. |
| <a id="layout18-table-1-row-6"></a> 평가·저장 | 조건별 정확도·ROC-AUC·클래스별 Recall·혼동행렬과 모델·그래프 출력을 구분합니다. |
| <a id="layout18-table-1-row-7"></a> 테스트 의사 라벨 | 테스트 예측의 최대 확률이 0.88 이상인 영상을 예측 라벨로 학습 자료에 추가하는 후속 경로가 있습니다. |


<a id="-이용-순서"></a>

## 이용 순서

1. 설정 셀에서 입력·작업·결과 경로와 변환 조건을 확인합니다.
2. 분할·증강 함수의 호출 순서와 시험 자료가 분리되는 지점을 읽습니다.
3. GPU·TensorFlow·학습 자료를 준비하고 설치·모니터·학습·출력 셀을 구분해 순서대로 읽습니다.
4. 기존 결과의 재사용 조건을 확인한 뒤 필요한 조건을 선택합니다.
5. 조건별 JSON과 혼동 행렬·ROC-AUC·Recall을 같은 분모와 클래스 순서로 비교합니다.

| 차수·단계 | 주요 내용 | 자료 | 직전 비교 |
| --- | --- | --- | --- |
| [블러 · 2차 실험](../../docs/revisions/experiment-6.md) | <a id="layout18-table-2-row-1-field-1"></a>입력 영상에 PIL GaussianBlur를 적용하는 10 조건 실험입니다. σ0 은 원본 배열을 복사합니다. | [폴더](.) | [전체 비교](../../docs/revision-diffs/experiment-6-%EC%97%B4%EB%9E%8C.md) |


[프로젝트](../../README.md) · [전체 차수](../../docs/REVISION_INDEX.md)

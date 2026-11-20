# 실제 6차 블러 진단

[LEVEL 1 - Beginner](../../docs/revisions/conv1-okng-round6.md#reading-level-1) · [LEVEL 2 - Explorer](../../docs/revisions/conv1-okng-round6.md#reading-level-2) · [LEVEL 3 - Practitioner](../../docs/revisions/conv1-okng-round6.md#reading-level-3) · [LEVEL 4 - Advanced](../../docs/revisions/conv1-okng-round6.md#reading-level-4) · [LEVEL 5 - Expert](../../docs/revisions/conv1-okng-round6.md#reading-level-5)

기존 5차 결과와 같은 test 164장을 재사용한 탐색적 진단입니다. 강도별 재학습과 같은 σ0 모델에 블러만 추가한 평가를 구분합니다. 원영상·영상별 예측·가중치 없이 집계 결과와 원비율만 공개합니다.

| 자료 | 역할 | 사용 조건 |
| --- | --- | --- |
| 코드 | 실제 공개 소스 | 자신의 자료·환경과 기준 필요 |
| 입력 계약 | 보존한 외부 실험 root·run ID·baseline | CT_AUDIT_SOURCE_ROOT·CT_AUDIT_RUN_ID로 자신의 입력 지정 |
| 상세 설명 | 절차·조건·검증·한계 | 위에서 같은 수준 선택 |

[집계 설명](%EA%B2%B0%EA%B3%BC/%EB%B8%94%EB%9F%AC_%EA%B2%B0%EA%B3%BC%EA%B0%80_%EB%86%92%EC%95%98%EB%8D%98_%EC%9D%B4%EC%9C%A0.md) · [전체 원비율](%EA%B2%B0%EA%B3%BC/%EC%A7%91%EA%B3%84_%EC%9B%90%EA%B0%92.json)

`CT_AUDIT_SOURCE_ROOT`와 `CT_AUDIT_RUN_ID`는 자신의 보존 실험을 지정합니다. `CT_AUDIT_SESSION`은로컬진단식별자이며과거개인 실행 값을 공개하지 않습니다. `tools/블러_원인검증.py --math-only`는 수학 검사, 실제 재추론은 원본·가중치·baseline 준비 후 수행합니다.

이 진단 폴더 자체에는 config.example.json이 없습니다. 원본·분할·선정 가중치는 지정한 기존 실험 폴더에서 읽고, 그 보존 기준과 모델을 확인합니다. [저차원·최근접·셔플 전체 집계](결과/데이터_대조군_집계.json)도 함께 제공합니다.

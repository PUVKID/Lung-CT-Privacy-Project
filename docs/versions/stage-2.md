<!-- language-choice:start -->
🔵 **한국어** · [English overview](../../en/README.md)
<!-- language-choice:end -->

<a id="-연구-2"></a>

# 연구 2

<!-- reading-levels17:start -->
<details>
<summary>읽기 수준 선택</summary>

| 레벨 | 읽는 목적 |
| --- | --- |
| [LEVEL 1 - Beginner](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A81.md) | 목적과 입력·출력을 쉬운 말로 이해하기 |
| [LEVEL 2 - Explorer](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A82.md) | 주요 기능과 전체 처리 흐름 살펴보기 |
| [LEVEL 3 - Practitioner](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A83.md) | 설정·실행 순서와 결과 확인하기 |
| [LEVEL 4 - Advanced](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A84.md) | 구현 선택과 조건·한계 비교하기 |
| [LEVEL 5 - Expert](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A85.md) | 세부 근거와 재현 조건 검토하기 |

</details>
<!-- reading-levels17:end -->

ResNet50에서 Block·Blur 단독 20 조건과 Block →Blur 조합 100 조건을 비교하고, 분류 정확도와 영상 유사도 기반 점수를 함께 읽는 19쪽 후속 원고입니다.

[목적·구성·사용법·결과의 상세 안내](../revisions/study-2.md) · [프로젝트](../../README.md) · [전체 차수](../REVISION_INDEX.md)

<a id="-이-자료를-읽는-순서"></a>

## 이 자료를 읽는 순서

1. 원고의 데이터·분할·모델 조건을 연구 1과 별도로 확인합니다.
2. 단독·조합 결과표에서 조건명과 분류 지표를 읽습니다.
3. MS-SSIM 계산과 Privacy Score 변환식을 확인합니다.
4. 정확도·점수의 산점도와 Pareto 조건을 함께 보며 선택 근거를 읽습니다.

<a id="-연결된-내용"></a>

## 연결된 내용

| 구성 | 읽을 내용 |
| --- | --- |
| 단독·조합 | 블록 10개·블러 10개와 Block →Blur100 조합을 비교합니다. |
| 분류 평가 | 정확도·macro OvR ROC-AUC·클래스별 Recall·혼동행렬을 봅니다. |
| 영상 유사도 | 입력 1,097장에 대한 MS-SSIM과 Privacy Score를 정리합니다. |
| 절충 분석 | 정확도와 구조 변화의 두 축에서 조건을 선택하는 Pareto 결과를 읽습니다. |

<a id="-해석-범위"></a>

## 해석 범위

원고는 원본 정확도 98.17%와 Block256 +σ0의 98.17%·Privacy Score49.65점 등을 보고합니다.

모델 변경만으로 연구 1 대비 차이의 원인을 확정하지 않습니다.

[전체 설명으로 이동](../revisions/study-2.md)

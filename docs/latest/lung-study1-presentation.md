<a id="-efficientnetv2-s-비식별화-연구-하계학술대회-발표"></a>

# EfficientNetV2-S 비식별화 연구 하계학술대회 발표

<!-- reading-levels17:start -->
**읽기 수준 선택** · [LEVEL 1 - Beginner](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A81.md) · [LEVEL 2 - Explorer](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A82.md) · [LEVEL 3 - Practitioner](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A83.md) · [LEVEL 4 - Advanced](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A84.md) · [LEVEL 5 - Expert](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A85.md)
<!-- reading-levels17:end -->

**EfficientNetV2-S에서 입력 CT 영상에 Gaussian Blur와 블록 재배열을 각각 적용했을 때 분류 결과가 어떻게 달라지는지 비교한 하계 3쪽 연구입니다.**

[목적·구성·사용법·결과의 상세 안내](../revisions/study-1.md) · [프로젝트](../../README.md) · [전체 차수](../REVISION_INDEX.md)

<a id="-이-자료를-읽는-순서"></a>

## 이 자료를 읽는 순서

1. 최종 논문의 방법에서 두 입력 변환과 모델을 확인합니다.
2. 결과표와 혼동행렬을 같은 조건명으로 비교합니다.
3. 그래프 노트북과 저장 JSON에서 원본·조건별 값의 대응을 확인합니다.
4. 발표 PDF와 전체 대본은 논문의 결과를 전달하는 흐름으로 함께 읽습니다.

<a id="-연결된-내용"></a>

## 연결된 내용

| 구성 | 읽을 내용 |
| --- | --- |
| 블러 비교 | σ0·1·2·4·8·16·32·64·128·256의 입력 블러를 비교합니다. |
| 블록 비교 | 512에서 1까지 10개 블록 크기로 재배열한 입력을 비교합니다. |
| 지표 읽기 | 정확도·ROC-AUC·클래스별 Recall과 혼동행렬을 함께 봅니다. |
| 발표 연결 | 완성 발표 19장·전체 대본 9쪽·그래프 노트북을 같은 연구의 설명 자료로 연결합니다. |

<a id="-해석-범위"></a>

## 해석 범위

원고는 원본 92.5%, Blurσ32 53.3%, Block32 79.2%, Block1 52.9% 등을 보고합니다.

이 값은 하계 연구의 보고값이며 후속 연구의 수치로 대체하지 않습니다.

<details>
<summary>파일·크기·SHA-256과 자료 연결</summary>

<a id="layout18-table-2-row-1"></a>

**[하계학술대회 PPT.pdf](../../%EC%97%B0%EA%B5%AC1_%ED%95%98%EA%B3%84_EfficientNetV2-S/%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C/%ED%95%98%EA%B3%84%ED%95%99%EC%88%A0%EB%8C%80%ED%9A%8C%20PPT.pdf)**

**원문 파일**

[하계학술대회 PPT.pdf](../../%EC%97%B0%EA%B5%AC1_%ED%95%98%EA%B3%84_EfficientNetV2-S/%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C/%ED%95%98%EA%B3%84%ED%95%99%EC%88%A0%EB%8C%80%ED%9A%8C%20PPT.pdf)

**바이트**

2156389

**SHA-256**

`22c41af0ada654bbaf8c8c5882ca1165da5e1216430af199db1fd0f560f349b3`

<a id="layout18-table-2-row-2"></a>

**[하계학술대회 PPT.pptx](../../%EC%97%B0%EA%B5%AC1_%ED%95%98%EA%B3%84_EfficientNetV2-S/%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C/%ED%95%98%EA%B3%84%ED%95%99%EC%88%A0%EB%8C%80%ED%9A%8C%20PPT.pptx)**

**원문 파일**

[하계학술대회 PPT.pptx](../../%EC%97%B0%EA%B5%AC1_%ED%95%98%EA%B3%84_EfficientNetV2-S/%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C/%ED%95%98%EA%B3%84%ED%95%99%EC%88%A0%EB%8C%80%ED%9A%8C%20PPT.pptx)

**바이트**

2325109

**SHA-256**

`a95905aea2ed35a70f0e43e5f0eaf30cbb5c227fed7384f952641104b26d5193`


</details>

[전체 설명으로 이동](../revisions/study-1.md)

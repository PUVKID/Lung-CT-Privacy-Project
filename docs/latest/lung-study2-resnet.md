<a id="-resnet50-기반-폐암-ct-분류에서-block-encryptiongaussian-blur의-프라이버시-정확도-트레이드오프-분석"></a>

# ResNet50 기반 폐암 CT 분류에서 Block Encryption·Gaussian Blur의 프라이버시-정확도 트레이드오프 분석

ResNet50에서 Block·Blur 단독 20조건과 Block→Blur 조합 100조건을 비교하고, 분류 정확도와 영상 유사도 기반 점수를 함께 읽는 19쪽 후속 원고입니다.

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
| 단독·조합 | 블록 10개·블러 10개와 Block→Blur100조합을 비교합니다. |
| 분류 평가 | 정확도·macro OvR ROC-AUC·클래스별 Recall·혼동행렬을 봅니다. |
| 영상 유사도 | 입력 1,097장에 대한 MS-SSIM과 Privacy Score를 정리합니다. |
| 절충 분석 | 정확도와 구조 변화의 두 축에서 조건을 선택하는 Pareto 결과를 읽습니다. |

<a id="-해석-범위"></a>

## 해석 범위

원고는 원본 정확도 98.17%와 Block256+σ0의 98.17%·Privacy Score49.65점 등을 보고합니다. 모델 변경만으로 연구 1 대비 차이의 원인을 확정하지 않습니다.

<details>
<summary>파일·크기·SHA-256과 자료 연결</summary>

| 원문 파일 | 바이트 | SHA-256 |
|---|---:|---|
| [연구 2_원문_최종.pdf](../../%EB%85%BC%EB%AC%B8/%EC%97%B0%EA%B5%AC2_%EC%9B%90%EB%AC%B8_%EC%B5%9C%EC%A2%85.pdf) | 2865864 | `58249752c657a4aad13b94d7860bb2d977e897e779e72a9f9e8d6306a60652fe` |
| [연구 2_원문_최종.hwp](../../%EB%85%BC%EB%AC%B8/%EC%97%B0%EA%B5%AC2_%EC%9B%90%EB%AC%B8_%EC%B5%9C%EC%A2%85.hwp) | 4908032 | `14d42c098f5ea8c057873e96136bf597b8f9bcec2c59b563bb763bca96fa1a50` |

</details>

[전체 설명으로 이동](../revisions/study-2.md)

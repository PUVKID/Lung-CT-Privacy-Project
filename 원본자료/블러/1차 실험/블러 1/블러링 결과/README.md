<a id="-원본자료블러1차-실험블러-1블러링-결과"></a>

# 원본자료/블러/1차 실험/블러 1/블러링 결과

<!-- reading-levels17:start -->
**읽기 수준 선택** · [LEVEL 1 - Beginner](../../../../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A81.md) · [LEVEL 2 - Explorer](../../../../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A82.md) · [LEVEL 3 - Practitioner](../../../../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A83.md) · [LEVEL 4 - Advanced](../../../../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A84.md) · [LEVEL 5 - Expert](../../../../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A85.md)
<!-- reading-levels17:end -->

**입력 변환 조건별 정확도·ROC-AUC·클래스별 Recall·혼동행렬을 보관한 결과 JSON입니다.** 저장 결과와 그래프 입력을 대조할 수 있습니다.

**주요 구성**

조건

**내용**

실제로 저장된 σ0·1·2·4·8·16·32·64·128·256의 10조건을 읽습니다.


**주요 구성**

분류 지표

**내용**

acc·roc_auc·per_class_acc를 조건별로 담습니다.


**주요 구성**

혼동행렬

**내용**

cm과 class_names의 순서를 함께 보며 클래스별 Recall을 확인합니다.


**주요 구성**

그래프 입력

**내용**

연구 1의 그래프 노트북에서 같은 조건명·실행의 값을 사용하는지 확인합니다.



<a id="-이용-순서"></a>

## 이용 순서

1. JSON에서 조건 키와 sigma 또는 block_size를 확인합니다.
2. acc·roc_auc와 클래스별 값의 단위를 구분합니다.
3. cm의 행·열 순서를 class_names에 맞춰 읽습니다.
4. 그래프·논문과 비교할 때 저장 실행·조건·반올림을 함께 확인합니다.

| 차수·단계 · 주요 내용 · 자료 · 직전 비교 |
| --- |
| **차수·단계**<br>[블러 · 1차 실험](../../../../../docs/revisions/experiment-original-blur.md)<br><br>**주요 내용**<br>[상세 설명](#layout18-table-2-row-1-field-1)<br><br>**자료**<br>[폴더](.)<br><br>**직전 비교**<br>[전체 비교](../../../../../docs/revision-diffs/experiment-original-blur.diff) |

<a id="layout18-table-2-row-1-field-1"></a>

**[블러 · 1차 실험](../../../../../docs/revisions/experiment-original-blur.md)**

**주요 내용**

입력 변환 조건별 정확도·ROC-AUC·클래스별 Recall·혼동행렬을 보관한 결과 JSON입니다. 저장 결과와 그래프 입력을 대조할 수 있습니다.


[프로젝트](../../../../../README.md) · [전체 차수](../../../../../docs/REVISION_INDEX.md)

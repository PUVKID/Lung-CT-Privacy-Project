<a id="-추가-학습모델과-실험"></a>

# 추가 학습모델과 실험

<!-- reading-levels17:start -->
<details>
<summary><strong>읽기 수준 선택</strong></summary>

| 레벨 | 읽는 목적 |
| --- | --- |
| [LEVEL 1 - Beginner](../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A81.md) | 목적과 입력·출력을 쉬운 말로 이해하기 |
| [LEVEL 2 - Explorer](../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A82.md) | 주요 기능과 전체 처리 흐름 살펴보기 |
| [LEVEL 3 - Practitioner](../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A83.md) | 설정·실행 순서와 결과 확인하기 |
| [LEVEL 4 - Advanced](../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A84.md) | 구현 선택과 조건·한계 비교하기 |
| [LEVEL 5 - Expert](../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A85.md) | 세부 근거와 재현 조건 검토하기 |

</details>
<!-- reading-levels17:end -->

**EfficientNetV2-S·MobileNetV2·ResNet50의 서로 다른 학습 셀과 SSIM/MS-SSIM·도표 코드를 모은 자료입니다.**

| 주요 구성 | 내용 |
| --- | --- |
| <a id="layout18-table-1-row-1"></a> Train.ipynb | 셀 0은 조직 영상 5 클래스, 셀 1·2는 EfficientNetV2-S의 CT 블록·블러, 셀 3~5는 MobileNetV2와 풀링 비교입니다. |
| <a id="layout18-table-1-row-2"></a> ResNet50 사본 | 단독·조합·edge·Stage1 특징 블러 노트북을 각각 구분합니다. |
| <a id="layout18-table-1-row-3"></a> 유사도 코드 | SSIM·PSNR·MS-SSIM과 DSSIM 기반 점수의 여러 버전을 보관합니다. |
| <a id="layout18-table-1-row-4"></a> 도표 | 저장된 분류 JSON과 유사도 CSV에서 막대·히트맵·논문 그림을 구성합니다. |


<a id="-이용-순서"></a>

## 이용 순서

1. 분류 학습·유사도 계산·도표 중 목적을 먼저 정합니다.
2. 선택한 셀의 모델·영상 종류·크기·클래스와 입력 경로를 확인합니다.
3. 설치·데이터 생성·학습·파일 쓰기 셀을 구분합니다.
4. 지표식과 캐시·출력 파일을 읽고 같은 조건의 결과만 비교합니다.

| 차수·단계 | 주요 내용 | 자료 | 직전 비교 |
| --- | --- | --- | --- |
| [추가 학습모델과 실험 · 기본](../docs/revisions/experiment-14.md) | <a id="layout18-table-2-row-1-field-1"></a>EfficientNetV2-S·MobileNetV2·ResNet50의 서로 다른 학습 셀과 SSIM/MS-SSIM·도표 코드를 모은 자료입니다. | [폴더](.) | [전체 비교](../docs/revision-diffs/experiment-14-%EC%97%B4%EB%9E%8C.md) |


[프로젝트](../README.md) · [전체 차수](../docs/REVISION_INDEX.md)

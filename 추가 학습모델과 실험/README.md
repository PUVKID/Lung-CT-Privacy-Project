<a id="-추가-학습모델과-실험"></a>

# 추가 학습모델과 실험

<!-- reading-levels17:start -->
**읽기 수준 선택** · [LEVEL 1 - Beginner](../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A81.md) · [LEVEL 2 - Explorer](../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A82.md) · [LEVEL 3 - Practitioner](../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A83.md) · [LEVEL 4 - Advanced](../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A84.md) · [LEVEL 5 - Expert](../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A85.md)
<!-- reading-levels17:end -->

**EfficientNetV2-S·MobileNetV2·ResNet50의 서로 다른 학습 셀과 SSIM/MS-SSIM·도표 코드를 모은 자료입니다.**

<a id="layout18-table-1-row-1"></a>

**Train.ipynb**

**주요 구성**

Train.ipynb

**내용**

셀 0은 조직영상 5클래스, 셀 1·2는 EfficientNetV2-S의 CT 블록·블러, 셀 3~5는 MobileNetV2와 풀링 비교입니다.

<a id="layout18-table-1-row-2"></a>

**ResNet50 사본**

**주요 구성**

ResNet50 사본

**내용**

단독·조합·edge·Stage1 특징 블러 노트북을 각각 구분합니다.

<a id="layout18-table-1-row-3"></a>

**유사도 코드**

**주요 구성**

유사도 코드

**내용**

SSIM·PSNR·MS-SSIM과 DSSIM 기반 점수의 여러 버전을 보관합니다.

<a id="layout18-table-1-row-4"></a>

**도표**

**주요 구성**

도표

**내용**

저장된 분류 JSON과 유사도 CSV에서 막대·히트맵·논문 그림을 구성합니다.


<a id="-이용-순서"></a>

## 이용 순서

1. 분류 학습·유사도 계산·도표 중 목적을 먼저 정합니다.
2. 선택한 셀의 모델·영상 종류·크기·클래스와 입력 경로를 확인합니다.
3. 설치·데이터 생성·학습·파일 쓰기 셀을 구분합니다.
4. 지표식과 캐시·출력 파일을 읽고 같은 조건의 결과만 비교합니다.

| 내용 |
| --- |
| **차수·단계**<br>[추가 학습모델과 실험 · 기본](../docs/revisions/experiment-14.md)<br><br>**주요 내용**<br>[상세 설명](#layout18-table-2-row-1-field-1)<br><br>**자료**<br>[폴더](.)<br><br>**직전 비교**<br>[전체 비교](../docs/revision-diffs/experiment-14.diff) |

<a id="layout18-table-2-row-1-field-1"></a>

**[추가 학습모델과 실험 · 기본](../docs/revisions/experiment-14.md)**

**주요 내용**

EfficientNetV2-S·MobileNetV2·ResNet50의 서로 다른 학습 셀과 SSIM/MS-SSIM·도표 코드를 모은 자료입니다.


[프로젝트](../README.md) · [전체 차수](../docs/REVISION_INDEX.md)

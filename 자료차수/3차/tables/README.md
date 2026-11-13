<a id="-자료차수3차tables"></a>

# 자료차수/3차/tables

<!-- reading-levels17:start -->
**읽기 수준 선택** · [LEVEL 1 - Beginner](../../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A81.md) · [LEVEL 2 - Explorer](../../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A82.md) · [LEVEL 3 - Practitioner](../../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A83.md) · [LEVEL 4 - Advanced](../../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A84.md) · [LEVEL 5 - Expert](../../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A85.md)
<!-- reading-levels17:end -->

**SSIM에서 DSSIM 기반 Privacy Score를 계산하는 경로와 3장·8조건의 저장 결과를 확인하는 자료 차수입니다.** 전체 논문의 1,097장 실험과 구분합니다.

<a id="layout18-table-1-row-1"></a>

**점수식**

**주요 구성**

점수식

**내용**

Privacy Score=((1−SSIM)/2)×100을 사용하며 PSNR은 참고값으로 따로 저장합니다.

<a id="layout18-table-1-row-2"></a>

**작은 조건 집합**

**주요 구성**

작은 조건 집합

**내용**

블록 512·32, 블러σ0·2와 네 조합을 사용합니다.

<a id="layout18-table-1-row-3"></a>

**집계**

**주요 구성**

집계

**내용**

long·방법별 요약·조합 pivot·best_conditions의 4CSV를 제공합니다.

<a id="layout18-table-1-row-4"></a>

**점검 결과**

**주요 구성**

점검 결과

**내용**

각 조건 n_images=3이며 동일 변환과 항등 조건의 값 대응을 읽습니다.


<a id="-이용-순서"></a>

## 이용 순서

1. long CSV의 condition·method·n_images·ssim_mean·privacy_score 열을 확인합니다.
2. Block512·σ0 항등 조건과 Block32·조합 B32_S0의 대응을 비교합니다.
3. 방법별 요약과 2×2 pivot이 long표의 같은 조건에서 나온 값인지 읽습니다.
4. 점수식을 최종 논문의 MS-SSIM식과 구별합니다.

| 차수·단계 · 주요 내용 · 자료 · 직전 비교 |
| --- |
| **차수·단계**<br>[폴더 3차](../../../docs/revisions/folder-3.md)<br><br>**주요 내용**<br>[상세 설명](#layout18-table-2-row-1-field-1)<br><br>**자료**<br>[폴더](.)<br><br>**직전 비교**<br>[전체 비교](../../../docs/revision-diffs/folder-3.diff) |

<a id="layout18-table-2-row-1-field-1"></a>

**[폴더 3차](../../../docs/revisions/folder-3.md)**

**주요 내용**

SSIM에서 DSSIM 기반 Privacy Score를 계산하는 경로와 3장·8조건의 저장 결과를 확인하는 자료 차수입니다. 전체 논문의 1,097장 실험과 구분합니다.


[프로젝트](../../../README.md) · [전체 차수](../../../docs/REVISION_INDEX.md)

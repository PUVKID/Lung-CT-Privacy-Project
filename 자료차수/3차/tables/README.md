<a id="-자료차수3차tables"></a>

# 자료차수/3차/tables

SSIM에서 DSSIM 기반 Privacy Score를 계산하는 경로와 3장·8조건의 저장 결과를 확인하는 자료 차수입니다. 전체 논문의 1,097장 실험과 구분합니다.

| 주요 구성 | 내용 |
| --- | --- |
| 점수식 | Privacy Score=((1−SSIM)/2)×100을 사용하며 PSNR은 참고값으로 따로 저장합니다. |
| 작은 조건 집합 | 블록 512·32, 블러σ0·2와 네 조합을 사용합니다. |
| 집계 | long·방법별 요약·조합 pivot·best_conditions의 4CSV를 제공합니다. |
| 점검 결과 | 각 조건 n_images=3이며 동일 변환과 항등 조건의 값 대응을 읽습니다. |

<a id="-이용-순서"></a>

## 이용 순서

1. long CSV의 condition·method·n_images·ssim_mean·privacy_score 열을 확인합니다.
2. Block512·σ0 항등 조건과 Block32·조합 B32_S0의 대응을 비교합니다.
3. 방법별 요약과 2×2 pivot이 long표의 같은 조건에서 나온 값인지 읽습니다.
4. 점수식을 최종 논문의 MS-SSIM식과 구별합니다.

| 차수·단계 | 주요 내용 | 자료 | 직전 비교 |
| --- | --- | --- | --- |
| [폴더 3차](../../../docs/revisions/folder-3.md) | SSIM에서 DSSIM 기반 Privacy Score를 계산하는 경로와 3장·8조건의 저장 결과를 확인하는 자료 차수입니다. 전체 논문의 1,097장 실험과 구분합니다. | [폴더](.) | [전체 비교](../../../docs/revision-diffs/folder-3.diff) |

[프로젝트](../../../README.md) · [전체 차수](../../../docs/REVISION_INDEX.md)

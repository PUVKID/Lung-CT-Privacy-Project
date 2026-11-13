<a id="-1차"></a>

# 1차

블록·블러의 rebuilt·same_settings·metric_matched 변형과 노트북 수정 보조 스크립트를 함께 읽는 코드 자료 차수입니다.

| 주요 구성 | 내용 |
| --- | --- |
| 여섯 노트북 | 블록·블러 각각 rebuilt·same_settings·metric_matched로 나누어 보관합니다. |
| 강도 매칭 | metric_matched 블러는 블록 변환의 평균 SSIM/PSNR에 맞는 sigma를 보정하는 함수를 포함합니다. |
| 학습 설정 | 변형별 batch4/8과 단계별 epoch·SWA 시작값이 다르므로 설정 셀을 확인합니다. |
| 수정 도구 | 노트북 생성·콜백·반복 학습·과적합 제어를 수정하는 보조 스크립트가 있습니다. |

<a id="-이용-순서"></a>

## 이용 순서

1. 여섯 노트북의 설정 셀에서 비교 목적·batch·변환 강도를 확인합니다.
2. metric_matched의 보정 영상 선택과 목표 SSIM/PSNR을 읽습니다.
3. 실험 입력·저장 경로와 분할·증강 순서를 확인합니다.
4. 수정 스크립트는 대상 파일을 다시 쓰므로 별도 사본에서 입력·치환 대상을 확인한 뒤 사용합니다.

| 차수·단계 | 주요 내용 | 자료 | 직전 비교 |
| --- | --- | --- | --- |
| [1차](../docs/revisions/folder-1.md) | 블록·블러의 rebuilt·same_settings·metric_matched 변형과 노트북 수정 보조 스크립트를 함께 읽는 코드 자료 차수입니다. | [폴더](.) | [전체 비교](../docs/revision-diffs/folder-1.diff) |

[프로젝트](../README.md) · [전체 차수](../docs/REVISION_INDEX.md)

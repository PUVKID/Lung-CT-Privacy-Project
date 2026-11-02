# 📁 추가 학습모델과 실험

EfficientNetV2-S·MobileNetV2·ResNet50의 서로 다른 학습 셀과 SSIM/MS-SSIM·도표 코드를 모은 자료입니다.

| 주요 구성 | 내용 |
| --- | --- |
| Train.ipynb | 셀 0은 조직영상 5클래스, 셀 1·2는 EfficientNetV2-S의 CT 블록·블러, 셀 3~5는 MobileNetV2와 풀링 비교입니다. |
| ResNet50 사본 | 단독·조합·edge·Stage1 특징 블러 노트북을 각각 구분합니다. |
| 유사도 코드 | SSIM·PSNR·MS-SSIM과 DSSIM 기반 점수의 여러 버전을 보관합니다. |
| 도표 | 저장된 분류 JSON과 유사도 CSV에서 막대·히트맵·논문 그림을 구성합니다. |

## 📖 이용 순서

1. 분류 학습·유사도 계산·도표 중 목적을 먼저 정합니다.
2. 선택한 셀의 모델·영상 종류·크기·클래스와 입력 경로를 확인합니다.
3. 설치·데이터 생성·학습·파일 쓰기 셀을 구분합니다.
4. 지표식과 캐시·출력 파일을 읽고 같은 조건의 결과만 비교합니다.

| 단계 | 이 단계의 목적 | 자료 | 직전 변화 |
| --- | --- | --- | --- |
| [추가 학습모델과 실험 · 기본](../docs/revisions/experiment-14.md) | EfficientNetV2-S·MobileNetV2·ResNet50의 서로 다른 학습 셀과 SSIM/MS-SSIM·도표 코드를 모은 자료입니다. | [폴더](.) | [전체 비교](../docs/revision-diffs/experiment-14.diff) |

[🏠 프로젝트](../README.md) · [🗂️ 전체 차수](../docs/REVISION_INDEX.md)

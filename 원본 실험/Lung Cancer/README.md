<a id="-원본-실험lung-cancer"></a>

# 원본 실험/Lung Cancer

<!-- reading-levels17:start -->
**읽기 수준 선택** · [LEVEL 1 - Beginner](../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A81.md) · [LEVEL 2 - Explorer](../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A82.md) · [LEVEL 3 - Practitioner](../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A83.md) · [LEVEL 4 - Advanced](../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A84.md) · [LEVEL 5 - Expert](../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A85.md)
<!-- reading-levels17:end -->

**Streamlit 화면은 업로드 영상을 224×224로 전처리해 Model.h5의 조직영상 5라벨 예측을 표시합니다.** 함께 있는 학습 노트북은 MobileNetV2의 3클래스 구성이어서 그대로 같은 모델로 간주하면 안 됩니다.

<a id="layout18-table-1-row-1"></a>

**전처리**

**주요 구성**

전처리

**내용**

preprocess_image가 영상을 224×224로 맞추고 255로 나누어 배치 차원을 추가합니다.

<a id="layout18-table-1-row-2"></a>

**5라벨 화면**

**주요 구성**

5라벨 화면

**내용**

대장선암·대장정상·폐선암·폐정상·폐편평상피암의 예측 확률을 표시합니다.

<a id="layout18-table-1-row-3"></a>

**그래프**

**주요 구성**

그래프

**내용**

예측 확률을 텍스트와 원형 그래프로 보여 줍니다.

<a id="layout18-table-1-row-4"></a>

**학습 사본**

**주요 구성**

학습 사본

**내용**

Train.ipynb의 MobileNetV2 3클래스·224·batch16·10epoch와 화면의 5라벨을 구분합니다.


<a id="-이용-순서"></a>

## 이용 순서

1. main.py의 모델 경로와 라벨 순서를 확인합니다.
2. 모델 출력 차원이 화면의 5라벨과 같은지 확인합니다.
3. 환경과 일치하는 모델을 준비하고 해당 폴더에서 Streamlit 앱을 엽니다.
4. 업로드 영상의 전처리와 확률 표시를 읽으며 학습 노트북의 모델과 혼합하지 않습니다.

| 내용 |
| --- |
| **차수·단계**<br>[원본 실험 · 기본](../../docs/revisions/experiment-13.md)<br><br>**주요 내용**<br>[상세 설명](#layout18-table-2-row-1-field-1)<br><br>**자료**<br>[폴더](.)<br><br>**직전 비교**<br>[전체 비교](../../docs/revision-diffs/experiment-13.diff) |

<a id="layout18-table-2-row-1-field-1"></a>

**[원본 실험 · 기본](../../docs/revisions/experiment-13.md)**

**주요 내용**

Streamlit 화면은 업로드 영상을 224×224로 전처리해 Model.h5의 조직영상 5라벨 예측을 표시합니다. 함께 있는 학습 노트북은 MobileNetV2의 3클래스 구성이어서 그대로 같은 모델로 간주하면 안 됩니다.


[프로젝트](../../README.md) · [전체 차수](../../docs/REVISION_INDEX.md)

<a id="-연구-1--efficientnetv2-s와-입력-비식별화"></a>

# 연구 1·EfficientNetV2-S와 입력 비식별화

<!-- reading-levels17:start -->
읽기 수준 · [LEVEL 1](#user-content-reading-level-1) · [LEVEL 2](#user-content-reading-level-2) · [LEVEL 3](#user-content-reading-level-3) · [LEVEL 4](#user-content-reading-level-4) · [LEVEL 5](#user-content-reading-level-5)

<details open>
<summary>LEVEL 1 · Beginner — 목적과 동작부터</summary>

<a id="reading-level-1"></a>

## LEVEL 1 - Beginner

<a id="semantic-lung-study1-level-1"></a>

| 항목 | 이 차수의 내용 |
| --- | --- |
| 목적 | EfficientNetV2-S에서 입력 CT 영상에 Gaussian Blur와 블록 재배열을 각각 적용했을 때 분류 결과가 어떻게 달라지는지 비교한 하계 3쪽 연구입니다. |
| 변경 | 입력 Blur·Block의 단독 비교를 정리한 연구 1입니다.<br>이후 연구 2는 ResNet50과 조합·영상 유사도 기반 점수를 별도의 후속 논문으로 다룹니다. |
| 조건 | 입력 사진에 블러·블록을 적용하는 경로와 모델이 뽑은 특징에 블러를 적용하는 경로를 나눕니다.<br>특징은 사진에서 찾은 선·무늬의 반응입니다.<br>그 색이 병변 위치나 악성 확률을 뜻하지 않습니다. |
| 동작 | 1.<br>최종 논문의 방법에서 두 입력 변환과 모델을 확인합니다. |
| 결과 | 원고는 원본 92.5%, Blurσ32 53.3%, Block32 79.2%, Block1 52.9% 등을 보고합니다. |

### LEVEL 1 · 하계 연구의 입력 변환과 보고값

**블러**는 사진의 무늬를 부드럽게 만들고 **블록 재배열**은 작은 조각 안을 유지한 채 조각 위치를 바꿉니다. 같은 사진을 두 방법으로 바꾼 뒤 정답을 맞힌 비율을 비교합니다. σ는 흐림의 강도, 블록 크기는 조각의 가로·세로 길이입니다. 아래 네 보고값은 당시 논문의 관측값이며 현재 대시보드의 새 결과가 아닙니다.

| 조건·자료 | 의미와 확인 방법 |
| --- | --- |
| <a id="layout18-table-1-row-1"></a> 입력과 조건 | 512×512 CT를 Benign·Malignant·Normal로 분류합니다.<br>블러 σ0·1·2·4·8·16·32·64·128·256과 블록 512·256·128·64·32·16·8·4·2·1의 단독 조건입니다. |
| <a id="layout18-table-1-row-2"></a> 보고값과 자료 | 3쪽 원고는 원본 92.5%, σ32 53.3%, Block32 79.2%, Block1 52.9%를 보고합니다.<br>발표 19장·대본 9 쪽·그래프 노트북은 같은 연구의 설명 자료입니다. |
| <a id="layout18-table-1-row-3"></a> 실행의 구분 | Block512 저장 원비율 0.9291666666666667과 Blur σ0의 0.925는 다른 실행입니다.<br>그래프 재작성은 새 학습이 아니며 연구 2의 표본 세부를 연구 1에 소급하지 않습니다. |

[동일 수준 프로젝트 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A81.md)


</details>

<details>
<summary>LEVEL 2 · Explorer — 구성과 연결 원리</summary>

<a id="reading-level-2"></a>

## LEVEL 2 - Explorer

<a id="semantic-lung-study1-level-2"></a>

| 항목 | 이 차수의 내용 |
| --- | --- |
| 목적 | EfficientNetV2-S에서 입력 CT 영상에 Gaussian Blur와 블록 재배열을 각각 적용했을 때 분류 결과가 어떻게 달라지는지 비교한 하계 3쪽 연구입니다. |
| 변경 | 입력 Blur·Block의 단독 비교를 정리한 연구 1입니다.<br>이후 연구 2는 ResNet50과 조합·영상 유사도 기반 점수를 별도의 후속 논문으로 다룹니다. |
| 조건 | 연구 1은 512×512 입력에 두 변환을 각각 적용해 정확도·ROC-AUC·혼 동 행렬을 봅니다.<br>연구 2는 Blur →Block·Block →Blur 조합과 입력 MS-SSIM을 비교합니다.<br>Conv1은 첫 합성곱 특징을 바꾼 뒤 분류합니다. |
| 동작 | 1.<br>최종 논문의 방법에서 두 입력 변환과 모델을 확인합니다. |
| 결과 | 원고는 원본 92.5%, Blurσ32 53.3%, Block32 79.2%, Block1 52.9% 등을 보고합니다. |

### LEVEL 2 · 하계 연구의 입력 변환과 보고값

EfficientNetV2-S라는 영상 분류기에 입력 변환을 각각 연결합니다. 흐림은 경계를 지우고 위치 재배열은 조각 안 무늬를 남기므로 성능 변화의 양상이 달라집니다. 정확도뿐 아니라 클래스별 정답 비율과 혼동 행렬을 함께 읽어 어느 범주에서 틀렸는지 확인합니다.

| 조건·자료 | 의미와 확인 방법 |
| --- | --- |
| <a id="layout18-table-6-row-1"></a> 입력과 조건 | 512×512 CT를 Benign·Malignant·Normal로 분류합니다.<br>블러 σ0·1·2·4·8·16·32·64·128·256과 블록 512·256·128·64·32·16·8·4·2·1의 단독 조건입니다. |
| <a id="layout18-table-6-row-2"></a> 보고값과 자료 | 3쪽 원고는 원본 92.5%, σ32 53.3%, Block32 79.2%, Block1 52.9%를 보고합니다.<br>발표 19장·대본 9 쪽·그래프 노트북은 같은 연구의 설명 자료입니다. |
| <a id="layout18-table-6-row-3"></a> 실행의 구분 | Block512 저장 원비율 0.9291666666666667과 Blur σ0의 0.925는 다른 실행입니다.<br>그래프 재작성은 새 학습이 아니며 연구 2의 표본 세부를 연구 1에 소급하지 않습니다. |

[동일 수준 프로젝트 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A82.md)


</details>

<details>
<summary>LEVEL 3 · Practitioner — 준비·실행·결과 확인</summary>

<a id="reading-level-3"></a>

## LEVEL 3 - Practitioner

<a id="semantic-lung-study1-level-3"></a>

| 항목 | 이 차수의 내용 |
| --- | --- |
| 목적 | EfficientNetV2-S에서 입력 CT 영상에 Gaussian Blur와 블록 재배열을 각각 적용했을 때 분류 결과가 어떻게 달라지는지 비교한 하계 3쪽 연구입니다. |
| 변경 | 입력 Blur·Block의 단독 비교를 정리한 연구 1입니다.<br>이후 연구 2는 ResNet50과 조합·영상 유사도 기반 점수를 별도의 후속 논문으로 다룹니다. |
| 조건 | 입력·변환 순서·분할·초기값·학습 예산을 차수별로 확인합니다.<br>Stage 1의 pool1_pool 특징 SSIM은 입력 MS-SSIM과 직접 비교하지 않습니다.<br>원본 test 선 분리와 학습 증강, 큰 sigma 결과 재사용도 확인합니다. |
| 동작 | 1.<br>최종 논문의 방법에서 두 입력 변환과 모델을 확인합니다. |
| 결과 | 원고는 원본 92.5%, Blurσ32 53.3%, Block32 79.2%, Block1 52.9% 등을 보고합니다. |

### LEVEL 3 · 하계 연구의 입력 변환과 보고값

하계 PDF/HWP의 방법과 결과를 먼저 읽고, 저장 JSON의 조건 명·클래스 순서·원비율을 그래프 입력과 대조하세요. Blur σ0와 Block512의 기준 수치를 한 실행으로 합치지 않습니다. 발표와 대본은 원고의 결과를 설명하는 자료이며 학습용 원영상·가중치는 별도입니다.

| 조건·자료 | 의미와 확인 방법 |
| --- | --- |
| <a id="layout18-table-11-row-1"></a> 입력과 조건 | 512×512 CT를 Benign·Malignant·Normal로 분류합니다.<br>블러 σ0·1·2·4·8·16·32·64·128·256과 블록 512·256·128·64·32·16·8·4·2·1의 단독 조건입니다. |
| <a id="layout18-table-11-row-2"></a> 보고값과 자료 | 3쪽 원고는 원본 92.5%, σ32 53.3%, Block32 79.2%, Block1 52.9%를 보고합니다.<br>발표 19장·대본 9 쪽·그래프 노트북은 같은 연구의 설명 자료입니다. |
| <a id="layout18-table-11-row-3"></a> 실행의 구분 | Block512 저장 원비율 0.9291666666666667과 Blur σ0의 0.925는 다른 실행입니다.<br>그래프 재작성은 새 학습이 아니며 연구 2의 표본 세부를 연구 1에 소급하지 않습니다. |

[동일 수준 프로젝트 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A83.md)


</details>

<details>
<summary>LEVEL 4 · Advanced — 구현·설계·실패 처리</summary>

<a id="reading-level-4"></a>

## LEVEL 4 - Advanced

<a id="semantic-lung-study1-level-4"></a>

| 항목 | 이 차수의 내용 |
| --- | --- |
| 목적 | EfficientNetV2-S에서 입력 CT 영상에 Gaussian Blur와 블록 재배열을 각각 적용했을 때 분류 결과가 어떻게 달라지는지 비교한 하계 3쪽 연구입니다. |
| 변경 | 입력 Blur·Block의 단독 비교를 정리한 연구 1입니다.<br>이후 연구 2는 ResNet50과 조합·영상 유사도 기반 점수를 별도의 후속 논문으로 다룹니다. |
| 조건 | Stage 1은 같은 프로세스의 Edge·Cloud 연결이며 실제 원격 전송이 아닙니다.<br>큰 sigma의 전역 평균 대체, sigma32 결과의 64/128/256 재사용과 Conv2D import 누락 같은 실행 제약을 구분합니다. |
| 동작 | 1.<br>최종 논문의 방법에서 두 입력 변환과 모델을 확인합니다. |
| 결과 | 원고는 원본 92.5%, Blurσ32 53.3%, Block32 79.2%, Block1 52.9% 등을 보고합니다. |

### LEVEL 4 · 하계 연구의 입력 변환과 보고값

입력 변환과 EfficientNetV2-S 분류, 결과 JSON을 읽는 도표 노트북의 경계를 분리합니다. 블록 내부 정보 보존이라는 해석은 이 실험의 보고값에 한정하며 모델만 바꾼 후속 연구의 차이를 인과 효과로 단정하지 않습니다.

| 조건·자료 | 의미와 확인 방법 |
| --- | --- |
| <a id="layout18-table-16-row-1"></a> 입력과 조건 | 512×512 CT를 Benign·Malignant·Normal로 분류합니다.<br>블러 σ0·1·2·4·8·16·32·64·128·256과 블록 512·256·128·64·32·16·8·4·2·1의 단독 조건입니다. |
| <a id="layout18-table-16-row-2"></a> 보고값과 자료 | 3쪽 원고는 원본 92.5%, σ32 53.3%, Block32 79.2%, Block1 52.9%를 보고합니다.<br>발표 19장·대본 9 쪽·그래프 노트북은 같은 연구의 설명 자료입니다. |
| <a id="layout18-table-16-row-3"></a> 실행의 구분 | Block512 저장 원비율 0.9291666666666667과 Blur σ0의 0.925는 다른 실행입니다.<br>그래프 재작성은 새 학습이 아니며 연구 2의 표본 세부를 연구 1에 소급하지 않습니다. |

[동일 수준 프로젝트 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A84.md)


</details>

<details>
<summary>LEVEL 5 · Expert — 근거·프로토콜·한계 검토</summary>

<a id="reading-level-5"></a>

## LEVEL 5 - Expert

<a id="semantic-lung-study1-level-5"></a>

### LEVEL 5 · 하계 연구의 입력 변환과 보고값

수락 범위는 하계 3쪽 원고와 저장 실 행별 보고값의 대응입니다. CT3 분류·입력 크기·단독 조건과 지표를 대조하고 원고에 없는 상세 표본 프로토콜을 후속 원고에서 가져오지 않습니다. 실제 재식별 공격 저항성이나 임상 일반화는 이 정확도 표로 입증되지 않습니다.

| 조건·자료 | 의미와 확인 방법 |
| --- | --- |
| <a id="layout18-table-21-row-1"></a> 입력과 조건 | 512×512 CT를 Benign·Malignant·Normal로 분류합니다.<br>블러 σ0·1·2·4·8·16·32·64·128·256과 블록 512·256·128·64·32·16·8·4·2·1의 단독 조건입니다. |
| <a id="layout18-table-21-row-2"></a> 보고값과 자료 | 3쪽 원고는 원본 92.5%, σ32 53.3%, Block32 79.2%, Block1 52.9%를 보고합니다.<br>발표 19장·대본 9 쪽·그래프 노트북은 같은 연구의 설명 자료입니다. |
| <a id="layout18-table-21-row-3"></a> 실행의 구분 | Block512 저장 원비율 0.9291666666666667과 Blur σ0의 0.925는 다른 실행입니다.<br>그래프 재작성은 새 학습이 아니며 연구 2의 표본 세부를 연구 1에 소급하지 않습니다. |

[동일 수준 프로젝트 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A85.md)

<!-- reading-levels17:end -->

EfficientNetV2-S에서 입력 CT 영상에 Gaussian Blur와 블록 재배열을 각각 적용했을 때 분류 결과가 어떻게 달라지는지 비교한 하계 3쪽 연구입니다.

분야: 의료 영상 연구 › EfficientNetV2-S 분류 › 입력 Blur·Block 단독 비교

[목적](#purpose) · [기능](#features) · [입출력](#flow) · [구성](#files) · [준비](#setup) · [사용법](#usage) · [결과](#results) · [제약](#limits) · [변경](#changes)

<a name="purpose"></a>

<a id="-이-단계에서-하는-일"></a>

## 연구 목적

원본 영상의 분류 유용성과 변환 강도의 관계를 읽는 논문입니다. ResNet50·조합 100 조건·MS-SSIM 점수를 다루는 후속 연구 2와 모델·문제·원고 구성을 구분합니다.

<a name="features"></a>

<a id="-주요-기능과-처리-방식"></a>

## 방법과 구현

| 구성 | 실제 역할 |
| --- | --- |
| 블러 비교 | σ0·1·2·4·8·16·32·64·128·256의 입력 블러를 비교합니다. |
| 블록 비교 | 512에서 1까지 10개 블록 크기로 재배열한 입력을 비교합니다. |
| 지표 읽기 | 정확도·ROC-AUC·클래스별 Recall과 혼동 행렬을 함께 봅니다. |
| 발표 연결 | 완성 발표 19장·전체 대본 9 쪽·그래프 노트북을 같은 연구의 설명 자료로 연결합니다. |

<a name="flow"></a>

<a id="-입력--처리--출력"></a>

## 입력·처리·출력

| 입력 | 처리 | 출력 |
| --- | --- | --- |
| 512×512 CT와 클래스 | Blur 또는 Block 입력 변환 | 강도별 영상 조건 |
| 조건별 영상 | EfficientNetV2-S 분류 | 분류 예측과 평가 지표 |
| 지표와 혼동행렬 | 강도별 성능 변화 비교 | 비식별화와 유용성의 관계 |

<a name="files"></a>

<a id="-파일과-핵심-처리"></a>

## 파일별 역할

| 파일 | 이용 방법 |
| --- | --- |
| <a id="layout18-table-24-row-1"></a> [작성·게재 상태](../%EB%85%BC%EB%AC%B8%EC%83%81%ED%83%9C.md) | **원고 비공개** · 작성·게재 상태 확인 |
| <a id="layout18-table-24-row-2"></a> [작성·게재 상태](../%EB%85%BC%EB%AC%B8%EC%83%81%ED%83%9C.md) | **편집 원본 비공개** · 작성·게재 상태 확인 |
| <a id="layout18-table-24-row-3"></a> [연구 1_하계_EfficientNetV2-S/그래프/Blur_Block_1차_그래프_white.ipynb](../../%EC%97%B0%EA%B5%AC1_%ED%95%98%EA%B3%84_EfficientNetV2-S/%EA%B7%B8%EB%9E%98%ED%94%84/Blur_Block_1%EC%B0%A8_%EA%B7%B8%EB%9E%98%ED%94%84_white.ipynb) | 설정·함수·실행 셀 |
| <a id="layout18-table-24-row-4"></a> [연구 1_하계_EfficientNetV2-S/발표자료/하계학술대회 PPT.pdf](../../%EC%97%B0%EA%B5%AC1_%ED%95%98%EA%B3%84_EfficientNetV2-S/%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C/%ED%95%98%EA%B3%84%ED%95%99%EC%88%A0%EB%8C%80%ED%9A%8C%20PPT.pdf) | 전체 원문·도표 읽기 |
| <a id="layout18-table-24-row-5"></a> [연구 1_하계_EfficientNetV2-S/발표자료/하계학술대회 발표 대본.pdf](../../%EC%97%B0%EA%B5%AC1_%ED%95%98%EA%B3%84_EfficientNetV2-S/%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C/%ED%95%98%EA%B3%84%ED%95%99%EC%88%A0%EB%8C%80%ED%9A%8C%20%EB%B0%9C%ED%91%9C%20%EB%8C%80%EB%B3%B8.pdf) | 전체 원문·도표 읽기 |


<a id="-함수셀로-찾아가기"></a>

### 관련 함수와 셀

관련 함수와 셀을 파일별로 정리했습니다. 실행 전 설정과 호출 순서, 출력 경로를 확인하세요.

| 파일 | 핵심 정의 |
| --- | --- |
| <a id="layout18-table-25-row-1"></a> [연구 1_하계_EfficientNetV2-S/그래프/Blur_Block_1차_그래프_white.ipynb](../../%EC%97%B0%EA%B5%AC1_%ED%95%98%EA%B3%84_EfficientNetV2-S/%EA%B7%B8%EB%9E%98%ED%94%84/Blur_Block_1%EC%B0%A8_%EA%B7%B8%EB%9E%98%ED%94%84_white.ipynb) | 셀 0: `acc_color` · `draw_cm`<br>셀 1: `block_label` · `acc_color` |


<a name="setup"></a>

<a id="️-환경과-설정"></a>

## 실행 환경과 설정

| 항목 | 조건·기본값 |
| --- | --- |
| 원고 | 하계 최종 3쪽 PDF/HWP |
| 입력 | 512×512 CT3 분류 |
| 조건 | Blur10·Block10 단독 비교 |
| 결과 자료 | 조건별 JSON·그래프 노트북·발표/대본 |

<a name="usage"></a>

<a id="-읽고-활용하는-순서"></a>

## 원고 읽기

1. 최종 논문의 방법에서 두 입력 변환과 모델을 확인합니다.
2. 결과표와 혼동행렬을 같은 조건명으로 비교합니다.
3. 그래프 노트북과 저장 JSON에서 원본·조건별 값의 대응을 확인합니다.
4. 발표 PDF와 전체 대본은 논문의 결과를 전달하는 흐름으로 함께 읽습니다.

<a name="results"></a>

<a id="-결과를-읽는-방법"></a>

## 결과와 해석

원고는 원본 92.5%, Blurσ32 53.3%, Block32 79.2%, Block1 52.9% 등을 보고합니다.

이 값은 하계 연구의 보고값이며 후속 연구의 수치로 대체하지 않습니다.

저장된 Block512의 정확도 0.929166…와 Blur σ0의 0.925는 서로 다른 실행의 기준 값입니다. 같은 원본 조건이라는 이유로 합치지 않고 실행과 지표를 구분해 읽습니다.

<a name="limits"></a>

<a id="️-알려진-제약과-확인-지점"></a>

## 제약과 확인 사항

| 상황 | 확인할 내용 |
| --- | --- |
| 연구 간 조건 | 연구 2의 1,097장·ResNet50 설정을 이 하계 연구에 소급하지 않습니다. |
| 프라이버시 해석 | 입력 변환의 분류 유용성 분석이며 실제 개인정보 공격 저항성의 입증과 구분합니다. |
| 자료 범위 | 의료 원영상·환자 기록은 포함하지 않습니다. |

<a name="changes"></a>

<a id="-이전-단계와의-변화"></a>

## 직전 단계와 비교

입력 Blur·Block의 단독 비교를 정리한 연구 1입니다. 이후 연구 2는 ResNet50과 조합·영상 유사도 기반 점수를 별도의 후속 논문으로 다룹니다.

[직전 단계 전체 비교·구성](../revision-diffs/study-1-%EC%97%B4%EB%9E%8C.md) · [전체 파일 크기·해시](../revision-manifests/study-1.json)

<details>
<summary>이 단계의 파일 기록과 전체 해시</summary>

아래 내용는 해당 단계가 기록될 당시의 파일 정보입니다. 현재 첨부는 [프로젝트 자료 안내](../PAPERS.md)에서 확인할 수 있습니다.

| 파일 | 종류 | 바이트 | SHA-256 |
| --- | --- | --- | --- |
| <a id="layout18-table-28-row-1"></a> `논문/1차_EfficientNetV2-S_하계_최종.pdf` | .pdf | 410164 | `dd6309e6f6b722d6db242e9c2237584314ad7d7bdf32eb1a91d10ced5ba3fe63` |
| <a id="layout18-table-28-row-2"></a> [연구 1_하계_EfficientNetV2-S/그래프/Blur_Block_1차_그래프_white.ipynb](../../%EC%97%B0%EA%B5%AC1_%ED%95%98%EA%B3%84_EfficientNetV2-S/%EA%B7%B8%EB%9E%98%ED%94%84/Blur_Block_1%EC%B0%A8_%EA%B7%B8%EB%9E%98%ED%94%84_white.ipynb) | .ipynb | 31695 | `a8c2615ce407a6e49de77cbea440d236e423dd77439abeaca57697b21e928823` |
| <a id="layout18-table-28-row-3"></a> `연구1_하계_EfficientNetV2-S/발표자료/하계학술대회 PPT.pdf` | .pdf | 2156389 | `22c41af0ada654bbaf8c8c5882ca1165da5e1216430af199db1fd0f560f349b3` |
| <a id="layout18-table-28-row-4"></a> `연구1_하계_EfficientNetV2-S/발표자료/하계학술대회 PPT.pptx` | .pptx | 2325109 | `a95905aea2ed35a70f0e43e5f0eaf30cbb5c227fed7384f952641104b26d5193` |
| <a id="layout18-table-28-row-5"></a> `연구1_하계_EfficientNetV2-S/발표자료/하계학술대회 발표 대본 정리.docx` | .docx | 12063 | `fbe895f010f6ee875395b5486b42dcf7d07248e6b6ac98a17a21bb38eda67246` |
| <a id="layout18-table-28-row-6"></a> `연구1_하계_EfficientNetV2-S/발표자료/하계학술대회 발표 대본 정리.pdf` | .pdf | 280123 | `0dad95908a9f7771703c37c882b5265162b1ea6d1a75762a96cef4d30923a598` |
| <a id="layout18-table-28-row-7"></a> `연구1_하계_EfficientNetV2-S/발표자료/하계학술대회 발표 대본.docx` | .docx | 14644 | `3a66466626c76c84640e1d4284ff375708f7ba428d92fd9f7a2c686cf3bbbae8` |
| <a id="layout18-table-28-row-8"></a> `연구1_하계_EfficientNetV2-S/발표자료/하계학술대회 발표 대본.pdf` | .pdf | 314134 | `f7d5589105d6a714a62ebe53a264a23070941e4fd26db78ddc8a08e8efc2f62a` |
| <a id="layout18-table-28-row-9"></a> [작성·게재 상태](../%EB%85%BC%EB%AC%B8%EC%83%81%ED%83%9C.md) | .hwp | 527360 | `f19ddfe212b9c38fd1cfdfec29f8d499e0150bd183e2d6a7992867b34720b7fc` |
| <a id="layout18-table-28-row-10"></a> [작성·게재 상태](../%EB%85%BC%EB%AC%B8%EC%83%81%ED%83%9C.md) | .hwp | 534016 | `a50590b82b4f2a37c948d267c03acdb38e2dfdb6ec1b912ad77718c50d8b9915` |
| <a id="layout18-table-28-row-11"></a> [작성·게재 상태](../%EB%85%BC%EB%AC%B8%EC%83%81%ED%83%9C.md) | .hwp | 50688 | `218bd80c6e58efc061d4717f1e47dab5c494c748813b3e580d98660a54cb8a4b` |
| <a id="layout18-table-28-row-12"></a> [작성·게재 상태](../%EB%85%BC%EB%AC%B8%EC%83%81%ED%83%9C.md) | .hwp | 55296 | `d8d43b6b577716c444a38c1fe258184834317b69628d469d075bc1014ba21d44` |
| <a id="layout18-table-28-row-13"></a> [연구 1_하계_EfficientNetV2-S/원문보관/그림/Blur_Block_1차_그래프_white.ipynb](../../%EC%97%B0%EA%B5%AC1_%ED%95%98%EA%B3%84_EfficientNetV2-S/%EC%9B%90%EB%AC%B8%EB%B3%B4%EA%B4%80/%EA%B7%B8%EB%A6%BC/Blur_Block_1%EC%B0%A8_%EA%B7%B8%EB%9E%98%ED%94%84_white.ipynb) | .ipynb | 34700 | `21207ffb5200d44de6a06b908ce7171648cf3d4a2c390c834162e357d61461ec` |


</details>

---

[프로젝트](../../README.md) · [전체 차수](../REVISION_INDEX.md) · [자료 폴더](../../%EB%85%BC%EB%AC%B8) · [연구 2 · ResNet50 후속 원고](study-2.md)

</details>


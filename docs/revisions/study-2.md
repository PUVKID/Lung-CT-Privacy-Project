<a id="-연구-2--resnet50의-프라이버시정확도-절충"></a>

# 연구 2 · ResNet50의 프라이버시·정확도 절충

<!-- reading-levels17:start -->
**읽기 수준 선택** · [LEVEL 1 - Beginner](#reading-level-1) · [LEVEL 2 - Explorer](#reading-level-2) · [LEVEL 3 - Practitioner](#reading-level-3) · [LEVEL 4 - Advanced](#reading-level-4) · [LEVEL 5 - Expert](#reading-level-5)

<a id="reading-level-1"></a>

## LEVEL 1 - Beginner

<!-- semantic-revision17:level-1:start -->

<a id="semantic-lung-study2-level-1"></a>

### LEVEL 1 · 후속 원고의 분모·조건·점수

**110명과 1,097장은 다른 단위**입니다. 한 사람에게 사진이 여러 장 있을 수 있습니다. 시험109장은 정답을 확인하는 사진 묶음이며 나머지 사진을 늘려 학습합니다. MS-SSIM은 사진의 구조가 얼마나 비슷한지 여러 크기에서 비교하는 값입니다. 이를 뒤집어 만든 점수가 높아도 개인정보가 안전하다는 확률은 아닙니다. 두 변환을 차례로 적용한100가지와 각각 적용한20가지를 나누어 읽습니다.

<a id="layout18-table-1-row-1"></a>

**표본과 분할**

**조건·자료**

표본과 분할

**의미와 확인 방법**

IQ-OTH/NCCD는 두 병원·110명·1,097장으로 Benign120·Malignant561·Normal416입니다. 클래스별 원본 10%의 시험109장(12·56·41)을 먼저 분리하고 나머지를 클래스당1,000장으로 증강해 7-fold·20회TTA를 적용한 원고입니다.

<a id="layout18-table-1-row-2"></a>

**비교 조건**

**조건·자료**

비교 조건

**의미와 확인 방법**

ImageNet 사전학습 ResNet50에서 Block10·Blur10의 단독20조건과 Block→Blur100조합을 구분합니다. 100조합 노트북 하나가 전체120조건을 수행하지 않습니다.

<a id="layout18-table-1-row-3"></a>

**점수 정의**

**조건·자료**

점수 정의

**의미와 확인 방법**

Privacy Score=50×(1−MS-SSIM)이며 전체1,097장의 원본/변환 영상을 5개 스케일로 비교합니다. 단일SSIM 기반 소규모·특징맵 점수와 다릅니다.

<a id="layout18-table-1-row-4"></a>

**원고 보고값**

**조건·자료**

원고 보고값

**의미와 확인 방법**

원본98.17%; 조합 Block256+σ0는98.17%·49.65점, +σ16은62.39%·49.70점, +σ32는58.72%·49.85점입니다. Blur단독σ256은51.38%·34.62점입니다.

<a id="layout18-table-1-row-5"></a>

**다른 실행과 붕괴**

**조건·자료**

다른 실행과 붕괴

**의미와 확인 방법**

조합100조건 중53조건의51.38%는 시험56/109와 대응해 다수클래스 붕괴로 해석합니다. 조합Block512+σ256의46.8%, 단독Block256의97.25%와 조합σ0의98.17%는 서로 다른 실행입니다.

<a id="layout18-table-1-row-6"></a>

**원고와 재현**

**조건·자료**

원고와 재현

**의미와 확인 방법**

19쪽 원고이며 RTX4090·TensorFlow·혼합정밀도를 보고합니다. Precision·F1은 산출하지 않았고 독립 기관·환자 검증과 실제 복원 공격·사람의 지각 평가는 후속 과제입니다.


<!-- semantic-revision17:level-1:end -->

[이 수준의 프로젝트 전체 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A81.md) · [같은 수준 프로필](https://github.com/PUVKID/PUVKID/blob/main/docs/읽기안내/레벨1.md)

### LEVEL 1 · 목적과 대상

**이 차수의 목적과 실제 구성**

ResNet50에서 Block·Blur 단독 20조건과 Block→Blur 조합 100조건을 비교하고, 분류 정확도와 영상 유사도 기반 점수를 함께 읽는 19쪽 후속 원고입니다.

| 구성 | 실제 역할 |
| --- | --- |
| 단독·조합 | 블록 10개·블러 10개와 Block→Blur100조합을 비교합니다. |
| 분류 평가 | 정확도·macro OvR ROC-AUC·클래스별 Recall·혼동행렬을 봅니다. |
| 영상 유사도 | 입력 1,097장에 대한 MS-SSIM과 Privacy Score를 정리합니다. |
| 절충 분석 | 정확도와 구조 변화의 두 축에서 조건을 선택하는 Pareto 결과를 읽습니다. |

CT 사진을 흐리게 하거나 블록으로 재배열했을 때 분류 결과와 영상 유사도가 어떻게 달라지는지 살펴봅니다. 입력 사진을 바꾸는 연구와 모델 내부의 첫 합성곱 특징을 흐리는 실험이 함께 있습니다. **논문 연구 번호·공개 코드 차수·실제 학습 차수는 다릅니다.**

### LEVEL 1 · 달라진 내용과 차수 관계

연구 1의 입력 변환 질문에서 ResNet50·조합·영상 유사도 절충 분석으로 확장한 별도 후속 논문입니다.

[직전 단계 전체 비교·구성](../revision-diffs/study-2.diff) · [전체 파일 크기·해시](../revision-manifests/study-2.json)

사진의 모양이 바뀌었어도 분류기가 정답을 잘 맞추는지, 얼마나 비슷한 정보를 남기는지 따로 봅니다. OK는 양성+정상, NG는 악성입니다. 사진 수·독립 환자 수·반복 학습 표본 수를 섞지 않습니다.

### LEVEL 1 · 입력과 실행 조건

| 입력 | 처리 | 출력 |
| --- | --- | --- |
| CT와 변환 조건 | Block→Blur 입력 생성 | 조건별 영상 |
| 조건별 영상 | ResNet50 분류와 원본/변환 유사도 계산 | 정확도·MS-SSIM |
| 두 지표 | Privacy Score·Pareto 비교 | 조건 선택의 장단점 |

| 항목 | 조건·기본값 |
| --- | --- |
| 원고 | 19쪽 최종 PDF/HWP |
| 조건 | 단독 20·조합 100 |
| 유사도 입력 | 원고의 전체 1,097장 |
| 점수식 | Privacy Score=((1−MS-SSIM)/2)×100 |

입력 사진에 블러·블록을 적용하는 경로와 모델이 뽑은 특징에 블러를 적용하는 경로를 나눕니다. 특징은 사진에서 찾은 선·무늬의 반응입니다. 그 색이 병변 위치나 악성 확률을 뜻하지 않습니다.

### LEVEL 1 · 처리 절차

1. 원고의 데이터·분할·모델 조건을 연구 1과 별도로 확인합니다.
2. 단독·조합 결과표에서 조건명과 분류 지표를 읽습니다.
3. MS-SSIM 계산과 Privacy Score 변환식을 확인합니다.
4. 정확도·점수의 산점도와 Pareto 조건을 함께 보며 선택 근거를 읽습니다.

전체 차수 표에서 읽을 연구를 고릅니다. 노트북을 여는 것과 새 학습 시작은 다릅니다. 대시보드에서 같은 강도의 사진·곡선·시험 수치를 함께 읽되 미완료 조건은 미측정으로 남깁니다.

### LEVEL 1 · 결과를 확인하는 방법

원고는 원본 정확도 98.17%와 Block256+σ0의 98.17%·Privacy Score49.65점 등을 보고합니다.

모델 변경만으로 연구 1 대비 차이의 원인을 확정하지 않습니다.

Privacy Score는 원본과 변환 영상의 구조적 차이에서 만든 상대 지표입니다. 복원 공격·신원 재식별·암호학적 안전성을 직접 측정한 값과 구분합니다.

연구 1의 원고 보고 정확도는 원본 92.5%, sigma32 블러 53.3%, Block32 재배열 79.2%입니다. 이는 당시 논문의 값이며 현재 Conv1 예비실험의 결과로 바꾸지 않습니다.

### LEVEL 1 · 주의할 범위

| 상황 | 확인할 내용 |
| --- | --- |
| 점수 정의 | SSIM 기반 소규모 점검 자료와 최종 MS-SSIM 점수식을 구분합니다. |
| 기준 영상 | 의료 원영상은 별도로 준비해야 하며 공개 첨부에 포함하지 않습니다. |
| 후속 코드 | pool1_pool 특징 블러·복원 코드를 원고의 입력 변환 실험 결과와 섞지 않습니다. |

환자 ID가 없어 같은 사람의 다른 사진이 섞였는지 모두 확인할 수 없습니다. 높은 정확도가 임상 성능이나 프라이버시 효과를 보장하지 않습니다. **반복 표본 5,000개를 독립 환자 5,000명으로 세지 않습니다.**

[표·코드·실행 설정·파일 전체 비교를 포함한 공통 상세](#reading-level-5)

<a id="reading-level-2"></a>

## LEVEL 2 - Explorer

<!-- semantic-revision17:level-2:start -->

<a id="semantic-lung-study2-level-2"></a>

### LEVEL 2 · 후속 원고의 분모·조건·점수

분류 정확도는 정답 비율이고 Privacy Score는 구조 비유사도여서 같은 의미가 아닙니다. Pareto 비교는 한쪽을 높일 때 다른 쪽을 얼마나 잃는지 보는 방법입니다. Block256+σ0에서 흐림을 더했을 때 점수는 조금 늘고 정확도는 크게 줄었다는 원고의 절충 해석을 아래 조건별 값과 함께 읽습니다. 7-fold는 일곱 학습 묶음, TTA는 평가 때 입력을 변형해 예측을 모으는 절차입니다.

<a id="layout18-table-6-row-1"></a>

**표본과 분할**

**조건·자료**

표본과 분할

**의미와 확인 방법**

IQ-OTH/NCCD는 두 병원·110명·1,097장으로 Benign120·Malignant561·Normal416입니다. 클래스별 원본 10%의 시험109장(12·56·41)을 먼저 분리하고 나머지를 클래스당1,000장으로 증강해 7-fold·20회TTA를 적용한 원고입니다.

<a id="layout18-table-6-row-2"></a>

**비교 조건**

**조건·자료**

비교 조건

**의미와 확인 방법**

ImageNet 사전학습 ResNet50에서 Block10·Blur10의 단독20조건과 Block→Blur100조합을 구분합니다. 100조합 노트북 하나가 전체120조건을 수행하지 않습니다.

<a id="layout18-table-6-row-3"></a>

**점수 정의**

**조건·자료**

점수 정의

**의미와 확인 방법**

Privacy Score=50×(1−MS-SSIM)이며 전체1,097장의 원본/변환 영상을 5개 스케일로 비교합니다. 단일SSIM 기반 소규모·특징맵 점수와 다릅니다.

<a id="layout18-table-6-row-4"></a>

**원고 보고값**

**조건·자료**

원고 보고값

**의미와 확인 방법**

원본98.17%; 조합 Block256+σ0는98.17%·49.65점, +σ16은62.39%·49.70점, +σ32는58.72%·49.85점입니다. Blur단독σ256은51.38%·34.62점입니다.

<a id="layout18-table-6-row-5"></a>

**다른 실행과 붕괴**

**조건·자료**

다른 실행과 붕괴

**의미와 확인 방법**

조합100조건 중53조건의51.38%는 시험56/109와 대응해 다수클래스 붕괴로 해석합니다. 조합Block512+σ256의46.8%, 단독Block256의97.25%와 조합σ0의98.17%는 서로 다른 실행입니다.

<a id="layout18-table-6-row-6"></a>

**원고와 재현**

**조건·자료**

원고와 재현

**의미와 확인 방법**

19쪽 원고이며 RTX4090·TensorFlow·혼합정밀도를 보고합니다. Precision·F1은 산출하지 않았고 독립 기관·환자 검증과 실제 복원 공격·사람의 지각 평가는 후속 과제입니다.


<!-- semantic-revision17:level-2:end -->

[이 수준의 프로젝트 전체 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A82.md) · [같은 수준 프로필](https://github.com/PUVKID/PUVKID/blob/main/docs/읽기안내/레벨2.md)

### LEVEL 2 · 목적과 대상

**이 차수의 목적과 실제 구성**

ResNet50에서 Block·Blur 단독 20조건과 Block→Blur 조합 100조건을 비교하고, 분류 정확도와 영상 유사도 기반 점수를 함께 읽는 19쪽 후속 원고입니다.

| 구성 | 실제 역할 |
| --- | --- |
| 단독·조합 | 블록 10개·블러 10개와 Block→Blur100조합을 비교합니다. |
| 분류 평가 | 정확도·macro OvR ROC-AUC·클래스별 Recall·혼동행렬을 봅니다. |
| 영상 유사도 | 입력 1,097장에 대한 MS-SSIM과 Privacy Score를 정리합니다. |
| 절충 분석 | 정확도와 구조 변화의 두 축에서 조건을 선택하는 Pareto 결과를 읽습니다. |

입력 변형 연구 1·2, 특징 블러 Stage 1, Conv1 OK/NG 예비실험을 구분합니다. 블러는 무늬를 부드럽게 하고 블록 재배열은 위치를 섞습니다. 분류 정확도와 유사도 기반 Privacy Score는 서로 다른 양을 측정합니다.

### LEVEL 2 · 달라진 내용과 차수 관계

연구 1의 입력 변환 질문에서 ResNet50·조합·영상 유사도 절충 분석으로 확장한 별도 후속 논문입니다.

[직전 단계 전체 비교·구성](../revision-diffs/study-2.diff) · [전체 파일 크기·해시](../revision-manifests/study-2.json)

이전 연구는 정상·양성·악성 3분류, Conv1은 OK/NG 이진 분류입니다. 원본 1,097장은 양성 120·정상 416·악성 561장입니다. 클래스당 매 epoch 5,000표본은 반복·온라인 증강이며 독립 영상 5,000장이 아닙니다.

### LEVEL 2 · 입력과 실행 조건

| 입력 | 처리 | 출력 |
| --- | --- | --- |
| CT와 변환 조건 | Block→Blur 입력 생성 | 조건별 영상 |
| 조건별 영상 | ResNet50 분류와 원본/변환 유사도 계산 | 정확도·MS-SSIM |
| 두 지표 | Privacy Score·Pareto 비교 | 조건 선택의 장단점 |

| 항목 | 조건·기본값 |
| --- | --- |
| 원고 | 19쪽 최종 PDF/HWP |
| 조건 | 단독 20·조합 100 |
| 유사도 입력 | 원고의 전체 1,097장 |
| 점수식 | Privacy Score=((1−MS-SSIM)/2)×100 |

연구 1은 512×512 입력에 두 변환을 각각 적용해 정확도·ROC-AUC·혼동행렬을 봅니다. 연구 2는 Blur→Block·Block→Blur 조합과 입력 MS-SSIM을 비교합니다. Conv1은 첫 합성곱 특징을 바꾼 뒤 분류합니다.

### LEVEL 2 · 처리 절차

1. 원고의 데이터·분할·모델 조건을 연구 1과 별도로 확인합니다.
2. 단독·조합 결과표에서 조건명과 분류 지표를 읽습니다.
3. MS-SSIM 계산과 Privacy Score 변환식을 확인합니다.
4. 정확도·점수의 산점도와 Pareto 조건을 함께 보며 선택 근거를 읽습니다.

대표 CT 3범주와 6단계에서 조건별 PNG 18개를 만듭니다. 원본 포함 10조건이 끝나면 180개입니다. 평균·최댓값·개별 8채널의 총 10패널은 특징 반응을 보여 줍니다.

### LEVEL 2 · 결과를 확인하는 방법

원고는 원본 정확도 98.17%와 Block256+σ0의 98.17%·Privacy Score49.65점 등을 보고합니다.

모델 변경만으로 연구 1 대비 차이의 원인을 확정하지 않습니다.

Privacy Score는 원본과 변환 영상의 구조적 차이에서 만든 상대 지표입니다. 복원 공격·신원 재식별·암호학적 안전성을 직접 측정한 값과 구분합니다.

연구 2는 원본 98.17%, Block256+sigma0 정확도 98.17%·Privacy Score 49.65점을 보고합니다. 유사도 점수는 복원 공격 성공률이 아닙니다. 연구 1과 모델·조건이 달라 차이의 원인을 하나로 확정하지 않습니다.

### LEVEL 2 · 주의할 범위

| 상황 | 확인할 내용 |
| --- | --- |
| 점수 정의 | SSIM 기반 소규모 점검 자료와 최종 MS-SSIM 점수식을 구분합니다. |
| 기준 영상 | 의료 원영상은 별도로 준비해야 하며 공개 첨부에 포함하지 않습니다. |
| 후속 코드 | pool1_pool 특징 블러·복원 코드를 원고의 입력 변환 실험 결과와 섞지 않습니다. |

영상 단위 예비실험의 한계, 조건별 학습·결과 재사용, 입력과 특징의 다른 점수 정의를 함께 읽습니다. 새 종료 정책 실험의 준비와 완료도 구분합니다.

[표·코드·실행 설정·파일 전체 비교를 포함한 공통 상세](#reading-level-5)

<a id="reading-level-3"></a>

## LEVEL 3 - Practitioner

<!-- semantic-revision17:level-3:start -->

<a id="semantic-lung-study2-level-3"></a>

### LEVEL 3 · 후속 원고의 분모·조건·점수

19쪽 PDF/HWP에서 표본→분할→변환→분류→유사도 계산 순서로 확인하세요. 단독과 조합 결과표를 별도로 읽고 정확도·macro OvR ROC-AUC·클래스별 Recall·혼동행렬을 조건명으로 맞춥니다. 영상1,097장의 유사도 분모와 분류 시험109장의 분모를 섞지 않으며 아래 숫자를 새 측정값으로 재계산해 바꾸지 않습니다.

<a id="layout18-table-11-row-1"></a>

**표본과 분할**

**조건·자료**

표본과 분할

**의미와 확인 방법**

IQ-OTH/NCCD는 두 병원·110명·1,097장으로 Benign120·Malignant561·Normal416입니다. 클래스별 원본 10%의 시험109장(12·56·41)을 먼저 분리하고 나머지를 클래스당1,000장으로 증강해 7-fold·20회TTA를 적용한 원고입니다.

<a id="layout18-table-11-row-2"></a>

**비교 조건**

**조건·자료**

비교 조건

**의미와 확인 방법**

ImageNet 사전학습 ResNet50에서 Block10·Blur10의 단독20조건과 Block→Blur100조합을 구분합니다. 100조합 노트북 하나가 전체120조건을 수행하지 않습니다.

<a id="layout18-table-11-row-3"></a>

**점수 정의**

**조건·자료**

점수 정의

**의미와 확인 방법**

Privacy Score=50×(1−MS-SSIM)이며 전체1,097장의 원본/변환 영상을 5개 스케일로 비교합니다. 단일SSIM 기반 소규모·특징맵 점수와 다릅니다.

<a id="layout18-table-11-row-4"></a>

**원고 보고값**

**조건·자료**

원고 보고값

**의미와 확인 방법**

원본98.17%; 조합 Block256+σ0는98.17%·49.65점, +σ16은62.39%·49.70점, +σ32는58.72%·49.85점입니다. Blur단독σ256은51.38%·34.62점입니다.

<a id="layout18-table-11-row-5"></a>

**다른 실행과 붕괴**

**조건·자료**

다른 실행과 붕괴

**의미와 확인 방법**

조합100조건 중53조건의51.38%는 시험56/109와 대응해 다수클래스 붕괴로 해석합니다. 조합Block512+σ256의46.8%, 단독Block256의97.25%와 조합σ0의98.17%는 서로 다른 실행입니다.

<a id="layout18-table-11-row-6"></a>

**원고와 재현**

**조건·자료**

원고와 재현

**의미와 확인 방법**

19쪽 원고이며 RTX4090·TensorFlow·혼합정밀도를 보고합니다. Precision·F1은 산출하지 않았고 독립 기관·환자 검증과 실제 복원 공격·사람의 지각 평가는 후속 과제입니다.


<!-- semantic-revision17:level-3:end -->

[이 수준의 프로젝트 전체 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A83.md) · [같은 수준 프로필](https://github.com/PUVKID/PUVKID/blob/main/docs/읽기안내/레벨3.md)

### LEVEL 3 · 목적과 대상

**이 차수의 목적과 실제 구성**

ResNet50에서 Block·Blur 단독 20조건과 Block→Blur 조합 100조건을 비교하고, 분류 정확도와 영상 유사도 기반 점수를 함께 읽는 19쪽 후속 원고입니다.

| 구성 | 실제 역할 |
| --- | --- |
| 단독·조합 | 블록 10개·블러 10개와 Block→Blur100조합을 비교합니다. |
| 분류 평가 | 정확도·macro OvR ROC-AUC·클래스별 Recall·혼동행렬을 봅니다. |
| 영상 유사도 | 입력 1,097장에 대한 MS-SSIM과 Privacy Score를 정리합니다. |
| 절충 분석 | 정확도와 구조 변화의 두 축에서 조건을 선택하는 Pareto 결과를 읽습니다. |

원고·노트북·저장 결과·대시보드를 차수별로 읽습니다. 과거 논문의 보고값과 현재 Conv1 실행 결과를 합치지 않습니다. 재현에는 원영상·분할·설정·결과 계보가 필요하며 의료 원자료는 공개하지 않습니다.

### LEVEL 3 · 달라진 내용과 차수 관계

연구 1의 입력 변환 질문에서 ResNet50·조합·영상 유사도 절충 분석으로 확장한 별도 후속 논문입니다.

[직전 단계 전체 비교·구성](../revision-diffs/study-2.diff) · [전체 파일 크기·해시](../revision-manifests/study-2.json)

라벨 매핑과 원본 분할을 먼저 확인합니다. 증강은 학습에만 적용하고 검증·시험 원본과 구분합니다. source_class는 원본 범주 폴더 라벨이며 환자·병원·스캐너 식별자가 아닙니다.

### LEVEL 3 · 입력과 실행 조건

| 입력 | 처리 | 출력 |
| --- | --- | --- |
| CT와 변환 조건 | Block→Blur 입력 생성 | 조건별 영상 |
| 조건별 영상 | ResNet50 분류와 원본/변환 유사도 계산 | 정확도·MS-SSIM |
| 두 지표 | Privacy Score·Pareto 비교 | 조건 선택의 장단점 |

| 항목 | 조건·기본값 |
| --- | --- |
| 원고 | 19쪽 최종 PDF/HWP |
| 조건 | 단독 20·조합 100 |
| 유사도 입력 | 원고의 전체 1,097장 |
| 점수식 | Privacy Score=((1−MS-SSIM)/2)×100 |

입력·변환 순서·분할·초기값·학습 예산을 차수별로 확인합니다. Stage 1의 pool1_pool 특징 SSIM은 입력 MS-SSIM과 직접 비교하지 않습니다. 원본 test 선분리와 학습 증강, 큰 sigma 결과 재사용도 확인합니다.

### LEVEL 3 · 처리 절차

1. 원고의 데이터·분할·모델 조건을 연구 1과 별도로 확인합니다.
2. 단독·조합 결과표에서 조건명과 분류 지표를 읽습니다.
3. MS-SSIM 계산과 Privacy Score 변환식을 확인합니다.
4. 정확도·점수의 산점도와 Pareto 조건을 함께 보며 선택 근거를 읽습니다.

실제 완료한 최적 체크포인트와 실행 ID가 같은 결과만 조회합니다. 색은 패널별 최솟값·최댓값으로 표시하므로 다른 패널의 같은 색을 같은 값으로 보지 않습니다. 과거 PNG나 직전 시험 수치를 대기에 재사용하지 않습니다.

### LEVEL 3 · 결과를 확인하는 방법

원고는 원본 정확도 98.17%와 Block256+σ0의 98.17%·Privacy Score49.65점 등을 보고합니다.

모델 변경만으로 연구 1 대비 차이의 원인을 확정하지 않습니다.

Privacy Score는 원본과 변환 영상의 구조적 차이에서 만든 상대 지표입니다. 복원 공격·신원 재식별·암호학적 안전성을 직접 측정한 값과 구분합니다.

현재 백분율 요약은 소수 첫째 자리 반올림이며 원비율·전체 백분율·정답 수를 함께 확인합니다. 과거 공개 4차의 둘째 자리 버림 설명은 당시 이력으로 두고 현재 규칙과 섞지 않습니다.

### LEVEL 3 · 주의할 범위

| 상황 | 확인할 내용 |
| --- | --- |
| 점수 정의 | SSIM 기반 소규모 점검 자료와 최종 MS-SSIM 점수식을 구분합니다. |
| 기준 영상 | 의료 원영상은 별도로 준비해야 하며 공개 첨부에 포함하지 않습니다. |
| 후속 코드 | pool1_pool 특징 블러·복원 코드를 원고의 입력 변환 실험 결과와 섞지 않습니다. |

원본과 분할 manifest의 실제 값은 자신의 로컬 자료로 준비해야 합니다. 공개 예제만으로 기준 비교가 동작하지 않습니다. 미완료 조건과 정의 불가 지표를 보기 좋은 값으로 채우지 않습니다.

[표·코드·실행 설정·파일 전체 비교를 포함한 공통 상세](#reading-level-5)

<a id="reading-level-4"></a>

## LEVEL 4 - Advanced

<!-- semantic-revision17:level-4:start -->

<a id="semantic-lung-study2-level-4"></a>

### LEVEL 4 · 후속 원고의 분모·조건·점수

입력 Block→PIL GaussianBlur, ResNet50 평가, 5스케일 MS-SSIM 집계, Pareto 분석을 별도 처리로 봅니다. 53조건의 다수클래스 붕괴는 각 혼동행렬을 확인해야 하며 보편적인 정확도 하한이 아닙니다. 단독·조합은 별도 학습이므로 동일 변환명이라고 저장 결과를 합치지 않습니다.

<a id="layout18-table-16-row-1"></a>

**표본과 분할**

**조건·자료**

표본과 분할

**의미와 확인 방법**

IQ-OTH/NCCD는 두 병원·110명·1,097장으로 Benign120·Malignant561·Normal416입니다. 클래스별 원본 10%의 시험109장(12·56·41)을 먼저 분리하고 나머지를 클래스당1,000장으로 증강해 7-fold·20회TTA를 적용한 원고입니다.

<a id="layout18-table-16-row-2"></a>

**비교 조건**

**조건·자료**

비교 조건

**의미와 확인 방법**

ImageNet 사전학습 ResNet50에서 Block10·Blur10의 단독20조건과 Block→Blur100조합을 구분합니다. 100조합 노트북 하나가 전체120조건을 수행하지 않습니다.

<a id="layout18-table-16-row-3"></a>

**점수 정의**

**조건·자료**

점수 정의

**의미와 확인 방법**

Privacy Score=50×(1−MS-SSIM)이며 전체1,097장의 원본/변환 영상을 5개 스케일로 비교합니다. 단일SSIM 기반 소규모·특징맵 점수와 다릅니다.

<a id="layout18-table-16-row-4"></a>

**원고 보고값**

**조건·자료**

원고 보고값

**의미와 확인 방법**

원본98.17%; 조합 Block256+σ0는98.17%·49.65점, +σ16은62.39%·49.70점, +σ32는58.72%·49.85점입니다. Blur단독σ256은51.38%·34.62점입니다.

<a id="layout18-table-16-row-5"></a>

**다른 실행과 붕괴**

**조건·자료**

다른 실행과 붕괴

**의미와 확인 방법**

조합100조건 중53조건의51.38%는 시험56/109와 대응해 다수클래스 붕괴로 해석합니다. 조합Block512+σ256의46.8%, 단독Block256의97.25%와 조합σ0의98.17%는 서로 다른 실행입니다.

<a id="layout18-table-16-row-6"></a>

**원고와 재현**

**조건·자료**

원고와 재현

**의미와 확인 방법**

19쪽 원고이며 RTX4090·TensorFlow·혼합정밀도를 보고합니다. Precision·F1은 산출하지 않았고 독립 기관·환자 검증과 실제 복원 공격·사람의 지각 평가는 후속 과제입니다.


<!-- semantic-revision17:level-4:end -->

[이 수준의 프로젝트 전체 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A84.md) · [같은 수준 프로필](https://github.com/PUVKID/PUVKID/blob/main/docs/읽기안내/레벨4.md)

### LEVEL 4 · 목적과 대상

**이 차수의 목적과 실제 구성**

ResNet50에서 Block·Blur 단독 20조건과 Block→Blur 조합 100조건을 비교하고, 분류 정확도와 영상 유사도 기반 점수를 함께 읽는 19쪽 후속 원고입니다.

| 구성 | 실제 역할 |
| --- | --- |
| 단독·조합 | 블록 10개·블러 10개와 Block→Blur100조합을 비교합니다. |
| 분류 평가 | 정확도·macro OvR ROC-AUC·클래스별 Recall·혼동행렬을 봅니다. |
| 영상 유사도 | 입력 1,097장에 대한 MS-SSIM과 Privacy Score를 정리합니다. |
| 절충 분석 | 정확도와 구조 변화의 두 축에서 조건을 선택하는 Pareto 결과를 읽습니다. |

입력 변형과 pool1_pool 특징 변형은 개입 위치가 다릅니다. 모델·학습·라벨·분할·점수 정의가 달라 단순 수치 차이를 모델 변경의 인과 효과로 설명할 수 없습니다. 종료 정책 비교도 별도 설계입니다.

### LEVEL 4 · 달라진 내용과 차수 관계

연구 1의 입력 변환 질문에서 ResNet50·조합·영상 유사도 절충 분석으로 확장한 별도 후속 논문입니다.

[직전 단계 전체 비교·구성](../revision-diffs/study-2.diff) · [전체 파일 크기·해시](../revision-manifests/study-2.json)

환자 ID 없는 영상 그룹 분할은 환자 독립 분할의 대체가 아닙니다. 소스별 촬영·압축 차이와 같은 환자의 다른 영상이 성능에 영향을 줄 수 있습니다. 높은 정확도의 원인을 조기 종료로 미리 확정하지 않습니다.

### LEVEL 4 · 입력과 실행 조건

| 입력 | 처리 | 출력 |
| --- | --- | --- |
| CT와 변환 조건 | Block→Blur 입력 생성 | 조건별 영상 |
| 조건별 영상 | ResNet50 분류와 원본/변환 유사도 계산 | 정확도·MS-SSIM |
| 두 지표 | Privacy Score·Pareto 비교 | 조건 선택의 장단점 |

| 항목 | 조건·기본값 |
| --- | --- |
| 원고 | 19쪽 최종 PDF/HWP |
| 조건 | 단독 20·조합 100 |
| 유사도 입력 | 원고의 전체 1,097장 |
| 점수식 | Privacy Score=((1−MS-SSIM)/2)×100 |

Stage 1은 같은 프로세스의 Edge·Cloud 연결이며 실제 원격 전송이 아닙니다. 큰 sigma의 전역 평균 대체, sigma32 결과의 64/128/256 재사용과 Conv2D import 누락 같은 실행 제약을 구분합니다.

### LEVEL 4 · 처리 절차

1. 원고의 데이터·분할·모델 조건을 연구 1과 별도로 확인합니다.
2. 단독·조합 결과표에서 조건명과 분류 지표를 읽습니다.
3. MS-SSIM 계산과 Privacy Score 변환식을 확인합니다.
4. 정확도·점수의 산점도와 Pareto 조건을 함께 보며 선택 근거를 읽습니다.

공개 4차는 학습 2차 대시보드의 로컬 수리 3차 사본입니다. 공개 5차는 실험 4차 고정 100회 비교 코드입니다. 원본 manifest·해시·정확 분할이 다르면 중단합니다.

### LEVEL 4 · 결과를 확인하는 방법

원고는 원본 정확도 98.17%와 Block256+σ0의 98.17%·Privacy Score49.65점 등을 보고합니다.

모델 변경만으로 연구 1 대비 차이의 원인을 확정하지 않습니다.

Privacy Score는 원본과 변환 영상의 구조적 차이에서 만든 상대 지표입니다. 복원 공격·신원 재식별·암호학적 안전성을 직접 측정한 값과 구분합니다.

Blur sigma256의 51.38%는 다수 클래스 56/109와 같지만 모든 조건의 하한은 아닙니다. 별도 학습한 Block512+sigma256은 46.8%입니다. 조합·단독·별도 학습·시험 분모를 나누어 읽습니다.

### LEVEL 4 · 주의할 범위

| 상황 | 확인할 내용 |
| --- | --- |
| 점수 정의 | SSIM 기반 소규모 점검 자료와 최종 MS-SSIM 점수식을 구분합니다. |
| 기준 영상 | 의료 원영상은 별도로 준비해야 하며 공개 첨부에 포함하지 않습니다. |
| 후속 코드 | pool1_pool 특징 블러·복원 코드를 원고의 입력 변환 실험 결과와 섞지 않습니다. |

기존 분할·시험셋 재사용과 환자 ID 부재는 독립 임상 평가를 제한합니다. 높은 정확도의 원인을 조기 종료로 확정하지 않고 동일 조건 정책 비교를 합니다. 두 비교 모델은 같은 학습 경로에서 선택됩니다.

[표·코드·실행 설정·파일 전체 비교를 포함한 공통 상세](#reading-level-5)

<a id="reading-level-5"></a>

## LEVEL 5 - Expert

<!-- semantic-revision17:level-5:start -->

<a id="semantic-lung-study2-level-5"></a>

### LEVEL 5 · 후속 원고의 분모·조건·점수

시험109장의 클래스 분모와 유사도1,097장의 분모, 110명이라는 원고의 환자 수를 구별합니다. 아래 원고 수치는 원정밀도로 보존합니다. 테스트 의사 라벨·증강 후fold의 누수 가능성과 코드/원고 차이를 함께 검토해야 하며 7-fold앙상블은 다중시드 반복이나 기관 외 검증을 대신하지 않습니다. 구조 점수는 공격 성공률·재식별 확률·암호학적 안전성·차등프라이버시 보장이 아닙니다.

<a id="layout18-table-21-row-1"></a>

**표본과 분할**

**조건·자료**

표본과 분할

**의미와 확인 방법**

IQ-OTH/NCCD는 두 병원·110명·1,097장으로 Benign120·Malignant561·Normal416입니다. 클래스별 원본 10%의 시험109장(12·56·41)을 먼저 분리하고 나머지를 클래스당1,000장으로 증강해 7-fold·20회TTA를 적용한 원고입니다.

<a id="layout18-table-21-row-2"></a>

**비교 조건**

**조건·자료**

비교 조건

**의미와 확인 방법**

ImageNet 사전학습 ResNet50에서 Block10·Blur10의 단독20조건과 Block→Blur100조합을 구분합니다. 100조합 노트북 하나가 전체120조건을 수행하지 않습니다.

<a id="layout18-table-21-row-3"></a>

**점수 정의**

**조건·자료**

점수 정의

**의미와 확인 방법**

Privacy Score=50×(1−MS-SSIM)이며 전체1,097장의 원본/변환 영상을 5개 스케일로 비교합니다. 단일SSIM 기반 소규모·특징맵 점수와 다릅니다.

<a id="layout18-table-21-row-4"></a>

**원고 보고값**

**조건·자료**

원고 보고값

**의미와 확인 방법**

원본98.17%; 조합 Block256+σ0는98.17%·49.65점, +σ16은62.39%·49.70점, +σ32는58.72%·49.85점입니다. Blur단독σ256은51.38%·34.62점입니다.

<a id="layout18-table-21-row-5"></a>

**다른 실행과 붕괴**

**조건·자료**

다른 실행과 붕괴

**의미와 확인 방법**

조합100조건 중53조건의51.38%는 시험56/109와 대응해 다수클래스 붕괴로 해석합니다. 조합Block512+σ256의46.8%, 단독Block256의97.25%와 조합σ0의98.17%는 서로 다른 실행입니다.

<a id="layout18-table-21-row-6"></a>

**원고와 재현**

**조건·자료**

원고와 재현

**의미와 확인 방법**

19쪽 원고이며 RTX4090·TensorFlow·혼합정밀도를 보고합니다. Precision·F1은 산출하지 않았고 독립 기관·환자 검증과 실제 복원 공격·사람의 지각 평가는 후속 과제입니다.


<!-- semantic-revision17:level-5:end -->

[전문가 수준 프로젝트 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A85.md) · [같은 수준 프로필](https://github.com/PUVKID/PUVKID/blob/main/docs/읽기안내/레벨5.md)

**기존 전체 상세** — 다음 본문은 이 차수의 원래 방법·조건·결과·실패·한계와 전체 비교입니다. 위 수준의 설명에 필요한 공통 근거도 모두 여기서 확인할 수 있습니다.
<!-- reading-levels17:end -->

**ResNet50에서 Block·Blur 단독 20조건과 Block→Blur 조합 100조건을 비교하고, 분류 정확도와 영상 유사도 기반 점수를 함께 읽는 19쪽 후속 원고입니다.**

분야: 의료 영상 연구 › ResNet50 분류 › MS-SSIM·프라이버시·정확도 절충

[목적](#purpose) · [기능](#features) · [입출력](#flow) · [구성](#files) · [준비](#setup) · [사용법](#usage) · [결과](#results) · [제약](#limits) · [변경](#changes)

<a name="purpose"></a>

<a id="-이-단계에서-하는-일"></a>

## 연구 목적

정확도를 가장 높게 유지하는 조건과 원본 영상의 구조를 더 많이 바꾸는 조건을 한 지표로 섞지 않고 Pareto 관점에서 비교합니다. 영상 입력 변환과 특징맵 변환의 후속 코드도 구분합니다.

<a name="features"></a>

<a id="-주요-기능과-처리-방식"></a>

## 방법과 구현

| 구성 | 실제 역할 |
| --- | --- |
| 단독·조합 | 블록 10개·블러 10개와 Block→Blur100조합을 비교합니다. |
| 분류 평가 | 정확도·macro OvR ROC-AUC·클래스별 Recall·혼동행렬을 봅니다. |
| 영상 유사도 | 입력 1,097장에 대한 MS-SSIM과 Privacy Score를 정리합니다. |
| 절충 분석 | 정확도와 구조 변화의 두 축에서 조건을 선택하는 Pareto 결과를 읽습니다. |

<a name="flow"></a>

<a id="-입력--처리--출력"></a>

## 입력·처리·출력

| 입력 | 처리 | 출력 |
| --- | --- | --- |
| CT와 변환 조건 | Block→Blur 입력 생성 | 조건별 영상 |
| 조건별 영상 | ResNet50 분류와 원본/변환 유사도 계산 | 정확도·MS-SSIM |
| 두 지표 | Privacy Score·Pareto 비교 | 조건 선택의 장단점 |

<a name="files"></a>

<a id="-파일과-핵심-처리"></a>

## 파일별 역할

<a id="layout18-table-24-row-1"></a>

**[논문/연구 2_원문_최종.pdf](../../%EB%85%BC%EB%AC%B8/%EC%97%B0%EA%B5%AC2_%EC%9B%90%EB%AC%B8_%EC%B5%9C%EC%A2%85.pdf)**

**파일**

[논문/연구 2_원문_최종.pdf](../../%EB%85%BC%EB%AC%B8/%EC%97%B0%EA%B5%AC2_%EC%9B%90%EB%AC%B8_%EC%B5%9C%EC%A2%85.pdf)

**이용 방법**

전체 원문·도표 읽기

<a id="layout18-table-24-row-2"></a>

**[논문/연구 2_원문_최종.hwp](../../%EB%85%BC%EB%AC%B8/%EC%97%B0%EA%B5%AC2_%EC%9B%90%EB%AC%B8_%EC%B5%9C%EC%A2%85.hwp)**

**파일**

[논문/연구 2_원문_최종.hwp](../../%EB%85%BC%EB%AC%B8/%EC%97%B0%EA%B5%AC2_%EC%9B%90%EB%AC%B8_%EC%B5%9C%EC%A2%85.hwp)

**이용 방법**

같은 판의 편집 원본

<a id="layout18-table-24-row-3"></a>

**항목 3**

**파일**

[자료차수/4차/코드/privacy_score_ssim_psnr_updated.ipynb](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/4%EC%B0%A8/%EC%BD%94%EB%93%9C/privacy_score_ssim_psnr_updated.ipynb)

**이용 방법**

설정·함수·실행 셀


<a id="-함수셀로-찾아가기"></a>

### 관련 함수와 셀

관련 함수와 셀을 파일별로 정리했습니다. 실행 전 설정과 호출 순서, 출력 경로를 확인하세요.

<a id="layout18-table-25-row-1"></a>

**항목 1**

**파일**

[자료차수/4차/코드/privacy_score_ssim_psnr_updated.ipynb](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/4%EC%B0%A8/%EC%BD%94%EB%93%9C/privacy_score_ssim_psnr_updated.ipynb)

**핵심 정의**

셀 9: `save_condition_sample`<br>셀 11: `block_scramble` · `apply_gaussian_blur`<br>셀 13: `_is_image_file` · `_is_ignored_path` · `collect_image_files` · `load_original_images`<br>셀 15: `_to_gray` · `_downsample_avg2x2` · `_ssim_l_cs` · `compute_ms_ssim` · `compute_ssim_psnr_msssim` · `privacy_score_from_ms_ssim` · `evaluate_condition`<br>셀 21: `combo_fn`<br>셀 25: `_save` · `_annotate_bars`<br>셀 38: `_combo_transform`


<a name="setup"></a>

<a id="️-환경과-설정"></a>

## 실행 환경과 설정

| 항목 | 조건·기본값 |
| --- | --- |
| 원고 | 19쪽 최종 PDF/HWP |
| 조건 | 단독 20·조합 100 |
| 유사도 입력 | 원고의 전체 1,097장 |
| 점수식 | Privacy Score=((1−MS-SSIM)/2)×100 |

<a name="usage"></a>

<a id="-읽고-활용하는-순서"></a>

## 원고 읽기

1. 원고의 데이터·분할·모델 조건을 연구 1과 별도로 확인합니다.
2. 단독·조합 결과표에서 조건명과 분류 지표를 읽습니다.
3. MS-SSIM 계산과 Privacy Score 변환식을 확인합니다.
4. 정확도·점수의 산점도와 Pareto 조건을 함께 보며 선택 근거를 읽습니다.

<a name="results"></a>

<a id="-결과를-읽는-방법"></a>

## 결과와 해석

원고는 원본 정확도 98.17%와 Block256+σ0의 98.17%·Privacy Score49.65점 등을 보고합니다.

모델 변경만으로 연구 1 대비 차이의 원인을 확정하지 않습니다.

Privacy Score는 원본과 변환 영상의 구조적 차이에서 만든 상대 지표입니다. 복원 공격·신원 재식별·암호학적 안전성을 직접 측정한 값과 구분합니다.

<a name="limits"></a>

<a id="️-알려진-제약과-확인-지점"></a>

## 제약과 확인 사항

| 상황 | 확인할 내용 |
| --- | --- |
| 점수 정의 | SSIM 기반 소규모 점검 자료와 최종 MS-SSIM 점수식을 구분합니다. |
| 기준 영상 | 의료 원영상은 별도로 준비해야 하며 공개 첨부에 포함하지 않습니다. |
| 후속 코드 | pool1_pool 특징 블러·복원 코드를 원고의 입력 변환 실험 결과와 섞지 않습니다. |

<a name="changes"></a>

<a id="-이전-단계와의-변화"></a>

## 직전 단계와 비교

연구 1의 입력 변환 질문에서 ResNet50·조합·영상 유사도 절충 분석으로 확장한 별도 후속 논문입니다.

[직전 단계 전체 비교·구성](../revision-diffs/study-2.diff) · [전체 파일 크기·해시](../revision-manifests/study-2.json)

<details>
<summary>이 단계의 파일 기록과 전체 해시</summary>

아래 내용는 해당 단계가 기록될 당시의 파일 정보입니다. 현재 첨부는 [프로젝트 자료 안내](../PAPERS.md)에서 확인할 수 있습니다.

<a id="layout18-table-28-row-1"></a>

**`논문/2차_ResNet50_최종.pdf`**

**파일**

`논문/2차_ResNet50_최종.pdf`

**종류**

.pdf

**바이트**

2827829

**SHA-256**

`b64645277f78ac2b2c87a1dcc15216ec9ad6c41a5a20f795465748ac0d2f76c7`

<a id="layout18-table-28-row-2"></a>

**[폐암 2차 논문/코드/block_blur_resnet50_v4_KO.ipynb](../../%ED%8F%90%EC%95%94%202%EC%B0%A8%20%EB%85%BC%EB%AC%B8/%EC%BD%94%EB%93%9C/block_blur_resnet50_v4_KO.ipynb)**

**파일**

[폐암 2차 논문/코드/block_blur_resnet50_v4_KO.ipynb](../../%ED%8F%90%EC%95%94%202%EC%B0%A8%20%EB%85%BC%EB%AC%B8/%EC%BD%94%EB%93%9C/block_blur_resnet50_v4_KO.ipynb)

**종류**

.ipynb

**바이트**

136449

**SHA-256**

`efdb4bc4e54aef87ca99b2acca4bd36c4f49093351d613ca254c6ddf90de46fc`

<a id="layout18-table-28-row-3"></a>

**항목 3**

**파일**

[폐암 2차 논문/코드/block_encryption_resnet50_rebuilt_KO.ipynb](../../%ED%8F%90%EC%95%94%202%EC%B0%A8%20%EB%85%BC%EB%AC%B8/%EC%BD%94%EB%93%9C/block_encryption_resnet50_rebuilt_KO.ipynb)

**종류**

.ipynb

**바이트**

108653

**SHA-256**

`3daed3071f6399ccc1edff47b8925bf31d39ee9a74fc9478f3ec6bee773393af`

<a id="layout18-table-28-row-4"></a>

**[폐암 2차 논문/코드/blur_resnet50_rebuilt2_KO.ipynb](../../%ED%8F%90%EC%95%94%202%EC%B0%A8%20%EB%85%BC%EB%AC%B8/%EC%BD%94%EB%93%9C/blur_resnet50_rebuilt2_KO.ipynb)**

**파일**

[폐암 2차 논문/코드/blur_resnet50_rebuilt2_KO.ipynb](../../%ED%8F%90%EC%95%94%202%EC%B0%A8%20%EB%85%BC%EB%AC%B8/%EC%BD%94%EB%93%9C/blur_resnet50_rebuilt2_KO.ipynb)

**종류**

.ipynb

**바이트**

102127

**SHA-256**

`745bb2b539259819784a219ebde96df31797fad820af09cd183177e529986870`

<a id="layout18-table-28-row-5"></a>

**[폐암 2차 논문/코드/heatmaps_windows.ipynb](../../%ED%8F%90%EC%95%94%202%EC%B0%A8%20%EB%85%BC%EB%AC%B8/%EC%BD%94%EB%93%9C/heatmaps_windows.ipynb)**

**파일**

[폐암 2차 논문/코드/heatmaps_windows.ipynb](../../%ED%8F%90%EC%95%94%202%EC%B0%A8%20%EB%85%BC%EB%AC%B8/%EC%BD%94%EB%93%9C/heatmaps_windows.ipynb)

**종류**

.ipynb

**바이트**

8407

**SHA-256**

`e64d162310d50c96a5ba1e39c44fce4702fad38abbf7c08c7a8eaf7b79582590`

<a id="layout18-table-28-row-6"></a>

**[폐암 2차 논문/코드/paper_figures_resnet50.ipynb](../../%ED%8F%90%EC%95%94%202%EC%B0%A8%20%EB%85%BC%EB%AC%B8/%EC%BD%94%EB%93%9C/paper_figures_resnet50.ipynb)**

**파일**

[폐암 2차 논문/코드/paper_figures_resnet50.ipynb](../../%ED%8F%90%EC%95%94%202%EC%B0%A8%20%EB%85%BC%EB%AC%B8/%EC%BD%94%EB%93%9C/paper_figures_resnet50.ipynb)

**종류**

.ipynb

**바이트**

27771

**SHA-256**

`4e52342e6d8a025549a37bf1e16fbd94f2d2a76d95cc0e039e703d6d1fc911ce`

<a id="layout18-table-28-row-7"></a>

**[폐암 2차 논문/코드/picture2x2.ipynb](../../%ED%8F%90%EC%95%94%202%EC%B0%A8%20%EB%85%BC%EB%AC%B8/%EC%BD%94%EB%93%9C/picture2x2.ipynb)**

**파일**

[폐암 2차 논문/코드/picture2x2.ipynb](../../%ED%8F%90%EC%95%94%202%EC%B0%A8%20%EB%85%BC%EB%AC%B8/%EC%BD%94%EB%93%9C/picture2x2.ipynb)

**종류**

.ipynb

**바이트**

6594

**SHA-256**

`d6ddecbbd7dfd747b83fefe3be920bef1a0597ae3413de936eb7cb27fe4cceb5`

<a id="layout18-table-28-row-8"></a>

**[폐암 2차 논문/코드/plot_privacy_metrics_split.ipynb](../../%ED%8F%90%EC%95%94%202%EC%B0%A8%20%EB%85%BC%EB%AC%B8/%EC%BD%94%EB%93%9C/plot_privacy_metrics_split.ipynb)**

**파일**

[폐암 2차 논문/코드/plot_privacy_metrics_split.ipynb](../../%ED%8F%90%EC%95%94%202%EC%B0%A8%20%EB%85%BC%EB%AC%B8/%EC%BD%94%EB%93%9C/plot_privacy_metrics_split.ipynb)

**종류**

.ipynb

**바이트**

18339

**SHA-256**

`6341212d374e771b81529b92f66f672ad66eac891240932b8b49a1c79ef98b0a`

<a id="layout18-table-28-row-9"></a>

**항목 9**

**파일**

[폐암 2차 논문/코드/privacy_score_ssim_psnr_updated.ipynb](../../%ED%8F%90%EC%95%94%202%EC%B0%A8%20%EB%85%BC%EB%AC%B8/%EC%BD%94%EB%93%9C/privacy_score_ssim_psnr_updated.ipynb)

**종류**

.ipynb

**바이트**

52527

**SHA-256**

`e0ce3aa6dd0a1fa307eea53cb1a2253266431a2ab0d86b984d72010aafc2c6ef`

<a id="layout18-table-28-row-10"></a>

**`논문/연구2_원문_최종.pdf`**

**파일**

`논문/연구2_원문_최종.pdf`

**종류**

.pdf

**바이트**

2865864

**SHA-256**

`58249752c657a4aad13b94d7860bb2d977e897e779e72a9f9e8d6306a60652fe`

<a id="layout18-table-28-row-11"></a>

**[최신 편집 원문](../../%EB%85%BC%EB%AC%B8/%EC%97%B0%EA%B5%AC2_%EC%9B%90%EB%AC%B8_%EC%B5%9C%EC%A2%85.hwp)**

**파일**

[최신 편집 원문](../../%EB%85%BC%EB%AC%B8/%EC%97%B0%EA%B5%AC2_%EC%9B%90%EB%AC%B8_%EC%B5%9C%EC%A2%85.hwp)

**종류**

.hwp

**바이트**

4908032

**SHA-256**

`14d42c098f5ea8c057873e96136bf597b8f9bcec2c59b563bb763bca96fa1a50`

<a id="layout18-table-28-row-12"></a>

**항목 12**

**파일**

[원본자료/폐암 2차 논문/코드/block_encryption_resnet50_rebuilt_KO.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%ED%8F%90%EC%95%94%202%EC%B0%A8%20%EB%85%BC%EB%AC%B8/%EC%BD%94%EB%93%9C/block_encryption_resnet50_rebuilt_KO.ipynb)

**종류**

.ipynb

**바이트**

138317

**SHA-256**

`4233928cb2aba1e9e1306e02ffc8a7cf5f17e62b72b83ccc2e8ec228c592c80f`

<a id="layout18-table-28-row-13"></a>

**항목 13**

**파일**

[원본자료/폐암 2차 논문/코드/blur_resnet50_rebuilt2_KO.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%ED%8F%90%EC%95%94%202%EC%B0%A8%20%EB%85%BC%EB%AC%B8/%EC%BD%94%EB%93%9C/blur_resnet50_rebuilt2_KO.ipynb)

**종류**

.ipynb

**바이트**

132788

**SHA-256**

`90c8e0f7a25c4533dc2b6759fa295bc7d758dd256330367d7c395dff2bee0d4f`

<a id="layout18-table-28-row-14"></a>

**[원본자료/폐암 2차 논문/코드/heatmaps_windows.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%ED%8F%90%EC%95%94%202%EC%B0%A8%20%EB%85%BC%EB%AC%B8/%EC%BD%94%EB%93%9C/heatmaps_windows.ipynb)**

**파일**

[원본자료/폐암 2차 논문/코드/heatmaps_windows.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%ED%8F%90%EC%95%94%202%EC%B0%A8%20%EB%85%BC%EB%AC%B8/%EC%BD%94%EB%93%9C/heatmaps_windows.ipynb)

**종류**

.ipynb

**바이트**

8646

**SHA-256**

`75c45970b92c8957ea61de8c236e045c3a0d77ed0de942815d3b16ae6e24ef4a`

<a id="layout18-table-28-row-15"></a>

**[원본자료/폐암 2차 논문/코드/paper_figures_resnet50.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%ED%8F%90%EC%95%94%202%EC%B0%A8%20%EB%85%BC%EB%AC%B8/%EC%BD%94%EB%93%9C/paper_figures_resnet50.ipynb)**

**파일**

[원본자료/폐암 2차 논문/코드/paper_figures_resnet50.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%ED%8F%90%EC%95%94%202%EC%B0%A8%20%EB%85%BC%EB%AC%B8/%EC%BD%94%EB%93%9C/paper_figures_resnet50.ipynb)

**종류**

.ipynb

**바이트**

38070

**SHA-256**

`162e3a670d2aa4dcb74771e651a1fd8c79fdf1e6e0ba33bb4fe81bc1177cc43d`

<a id="layout18-table-28-row-16"></a>

**[원본자료/폐암 2차 논문/코드/pareto_scatter.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%ED%8F%90%EC%95%94%202%EC%B0%A8%20%EB%85%BC%EB%AC%B8/%EC%BD%94%EB%93%9C/pareto_scatter.ipynb)**

**파일**

[원본자료/폐암 2차 논문/코드/pareto_scatter.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%ED%8F%90%EC%95%94%202%EC%B0%A8%20%EB%85%BC%EB%AC%B8/%EC%BD%94%EB%93%9C/pareto_scatter.ipynb)

**종류**

.ipynb

**바이트**

0

**SHA-256**

`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

<a id="layout18-table-28-row-17"></a>

**[원본자료/폐암 2차 논문/코드/picture2x2.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%ED%8F%90%EC%95%94%202%EC%B0%A8%20%EB%85%BC%EB%AC%B8/%EC%BD%94%EB%93%9C/picture2x2.ipynb)**

**파일**

[원본자료/폐암 2차 논문/코드/picture2x2.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%ED%8F%90%EC%95%94%202%EC%B0%A8%20%EB%85%BC%EB%AC%B8/%EC%BD%94%EB%93%9C/picture2x2.ipynb)

**종류**

.ipynb

**바이트**

7054

**SHA-256**

`d56ae7885ab9219f62bb695fe1e5de081c7e667ebbf8c5916b87909bff4b2046`

<a id="layout18-table-28-row-18"></a>

**항목 18**

**파일**

[원본자료/폐암 2차 논문/코드/plot_privacy_metrics_split.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%ED%8F%90%EC%95%94%202%EC%B0%A8%20%EB%85%BC%EB%AC%B8/%EC%BD%94%EB%93%9C/plot_privacy_metrics_split.ipynb)

**종류**

.ipynb

**바이트**

18984

**SHA-256**

`77cc7650ee472043999937da35fd6ac817330ce45a796c584330571ccf1e05be`

<a id="layout18-table-28-row-19"></a>

**항목 19**

**파일**

[원본자료/폐암 2차 논문/코드/privacy_score_ssim_psnr_updated.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%ED%8F%90%EC%95%94%202%EC%B0%A8%20%EB%85%BC%EB%AC%B8/%EC%BD%94%EB%93%9C/privacy_score_ssim_psnr_updated.ipynb)

**종류**

.ipynb

**바이트**

96269

**SHA-256**

`74cb8eb330d2a60c357ff4806f3d4a5c3aeefb3f5f3cc2c0b188d792decb863a`

<a id="layout18-table-28-row-20"></a>

**항목 20**

**파일**

[원본자료/추가 학습모델과 실험/block_blur_resnet50_v4_KO.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/block_blur_resnet50_v4_KO.ipynb)

**종류**

.ipynb

**바이트**

223652

**SHA-256**

`988bdd6a86fac7245cdd255f19cdc5bf046579c6bdbe52e95ba8ed96a4f04140`

<a id="layout18-table-28-row-21"></a>

**[최신 편집 원문](../../%EB%85%BC%EB%AC%B8/%EC%97%B0%EA%B5%AC2_%EC%9B%90%EB%AC%B8_%EC%B5%9C%EC%A2%85.hwp)**

**파일**

[최신 편집 원문](../../%EB%85%BC%EB%AC%B8/%EC%97%B0%EA%B5%AC2_%EC%9B%90%EB%AC%B8_%EC%B5%9C%EC%A2%85.hwp)

**종류**

.hwp

**바이트**

414720

**SHA-256**

`7f3d880b8df41d7549973470476f6011ce80ca835f36f7ac62e22acdb978f196`

<a id="layout18-table-28-row-22"></a>

**항목 22**

**파일**

[원본자료/폐암 2차 논문/코드/block_blur_resnet50_v4_KO.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%ED%8F%90%EC%95%94%202%EC%B0%A8%20%EB%85%BC%EB%AC%B8/%EC%BD%94%EB%93%9C/block_blur_resnet50_v4_KO.ipynb)

**종류**

.ipynb

**바이트**

223652

**SHA-256**

`988bdd6a86fac7245cdd255f19cdc5bf046579c6bdbe52e95ba8ed96a4f04140`


</details>

---

[프로젝트](../../README.md) · [전체 차수](../REVISION_INDEX.md) · [자료 폴더](../../%EB%85%BC%EB%AC%B8) · [연구 1 · 하계 EfficientNetV2-S](study-1.md)

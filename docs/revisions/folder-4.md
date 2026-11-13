<a id="-자료-4차--후속-원고와-지표도표-코드"></a>

# 자료 4차 · 후속 원고와 지표·도표 코드

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


<a id="semantic-lung-tools-level-1"></a>

### LEVEL 1 · 자료 차수의 수정 도구와 소규모 계산

자료 차수는 논문 번호와 다른 **파일 보관 단계**입니다. 노트북을 고치는 도구는 학습을 대신하지 않고, 3장짜리 계산은 전체 사진의 연구 결과를 대신하지 않습니다. 항등 조건은 사진을 바꾸지 않은 조건이라 구조 차이 점수가 0입니다. 빈 파일은 이름만으로 기능이 있는 것처럼 읽지 않습니다.

<a id="layout18-table-2-row-1"></a>

**자료1차**

**조건·자료**

자료1차

**의미와 확인 방법**

블록·블러각각rebuilt·same_settings·metric_matched의여섯노트북입니다. metric_matched는블록평균SSIM/PSNR에맞는sigma를탐색하며batch4/8·epoch·SWA가변형별로다릅니다. 보조도구는지정노트북을다시씁니다.

<a id="layout18-table-2-row-2"></a>

**자료2차**

**조건·자료**

자료2차

**의미와 확인 방법**

align_experiment_methods.mjs는GPU모니터필드/그래프호환을맞추고build_block_blur_notebook.mjs는Blur사본에서Block→Blur100조합을만듭니다. replaceOrThrow는대상문자열누락시중단하고rollback_original_notebooks.mjs는보관본/지정셀을복원합니다. Node.js와실제입력·출력경로가필요합니다.

<a id="layout18-table-2-row-3"></a>

**자료3차**

**조건·자료**

자료3차

**의미와 확인 방법**

512·seed42의3장입력, Block512·32/Blurσ0·2/조합4의8조건입니다. Privacy Score=((1−SSIM)/2)×100이며PSNR은별도참고값입니다. long·방법요약·조합pivot·best_conditions의4CSV가있습니다. 항등조건0, Block32와B32_S0의35.3667978…은3장계산확인값입니다.

<a id="layout18-table-2-row-4"></a>

**자료4차**

**조건·자료**

자료4차

**의미와 확인 방법**

자료차수/4차/코드의학습·MS-SSIM·도표코드를19쪽원고와연결합니다. pareto_scatter.ipynb는0바이트로실행내용이없습니다. 소규모SSIM표와원고1,097장MS-SSIM을섞지않습니다.


<!-- semantic-revision17:level-1:end -->

[이 수준의 프로젝트 전체 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A81.md) · [같은 수준 프로필](https://github.com/PUVKID/PUVKID/blob/main/docs/읽기안내/레벨1.md)

### LEVEL 1 · 목적과 대상

**이 차수의 목적과 실제 구성**

ResNet50 후속 원고와 입력 변환·유사도·도표 코드를 연결해 읽는 자료 차수입니다. 실제 코드 폴더는 자료차수/4차/코드에 있습니다.

<a id="layout18-table-3-row-1"></a>

**학습 코드**

**구성**

학습 코드

**실제 역할**

Blur·Block·조합 노트북이 조건별 입력과 ResNet50 평가를 구성합니다.

<a id="layout18-table-3-row-2"></a>

**지표 계산**

**구성**

지표 계산

**실제 역할**

privacy_score_ssim_psnr_updated가 MS-SSIM과 점수식을 계산합니다.

<a id="layout18-table-3-row-3"></a>

**그림 코드**

**구성**

그림 코드

**실제 역할**

heatmaps_windows·paper_figures_resnet50·plot_privacy_metrics_split 등이 표와 그림을 구성합니다.

<a id="layout18-table-3-row-4"></a>

**원고 연결**

**구성**

원고 연결

**실제 역할**

연구 2 최종 PDF/HWP와 코드의 조건·그림을 대조합니다.


CT 사진을 흐리게 하거나 블록으로 재배열했을 때 분류 결과와 영상 유사도가 어떻게 달라지는지 살펴봅니다. 입력 사진을 바꾸는 연구와 모델 내부의 첫 합성곱 특징을 흐리는 실험이 함께 있습니다. **논문 연구 번호·공개 코드 차수·실제 학습 차수는 다릅니다.**

### LEVEL 1 · 달라진 내용과 차수 관계

자료 3차의 소규모 점검에서 후속 원고·전체 지표·도표 코드를 연결한 자료 4차입니다.

[직전 단계 전체 비교·구성](../revision-diffs/folder-4.diff) · [전체 파일 크기·해시](../revision-manifests/folder-4.json)

사진의 모양이 바뀌었어도 분류기가 정답을 잘 맞추는지, 얼마나 비슷한 정보를 남기는지 따로 봅니다. OK는 양성+정상, NG는 악성입니다. 사진 수·독립 환자 수·반복 학습 표본 수를 섞지 않습니다.

### LEVEL 1 · 입력과 실행 조건

| 입력 | 처리 | 출력 |
| --- | --- | --- |
| 분류 결과·변환 조건 | 지표 계산 | 정확도·유사도·점수 표 |
| 결과표 | 히트맵·막대·분리 지표 그림 | 원고 도표 |
| 최종 원고 | 방법·보고값과코드대조 | 연구 2 읽기 |

| 항목 | 조건·기본값 |
| --- | --- |
| 코드 위치 | 자료차수/4차/코드 |
| 원고 | 연구 2 최종 19쪽 |
| 입력 | 의료 원영상·가중치는 별도 준비 |
| 빈 파일 | pareto_scatter.ipynb는 0바이트 |

입력 사진에 블러·블록을 적용하는 경로와 모델이 뽑은 특징에 블러를 적용하는 경로를 나눕니다. 특징은 사진에서 찾은 선·무늬의 반응입니다. 그 색이 병변 위치나 악성 확률을 뜻하지 않습니다.

### LEVEL 1 · 처리 절차

1. 논문에서 확인할 그림·지표를 정한 뒤 대응 코드 파일을 엽니다.
2. 학습 결과를 입력받는 그림 코드와 원영상을 읽는 지표 코드를 구분합니다.
3. 입력 경로·CSV/JSON 열·조건 순서를 확인합니다.
4. 빈 pareto_scatter.ipynb는 실행 코드로 사용하지 않고 다른 도표 코드의 실제 내용을 확인합니다.

전체 차수 표에서 읽을 연구를 고릅니다. 노트북을 여는 것과 새 학습 시작은 다릅니다. 대시보드에서 같은 강도의 사진·곡선·시험 수치를 함께 읽되 미완료 조건은 미측정으로 남깁니다.

### LEVEL 1 · 결과를 확인하는 방법

원고의 보고값과 코드의 설정·저장 결과를 대조하는 자료입니다. 도표 파일명만으로 새로운 실험 결과를 추정하지 않습니다.

0바이트 pareto_scatter.ipynb는 내용 없는 원본 파일입니다. 실제 산점도·지표 계산 기능은 내용이 있는 대응 노트북을 확인해야 합니다.

연구 1의 원고 보고 정확도는 원본 92.5%, sigma32 블러 53.3%, Block32 재배열 79.2%입니다. 이는 당시 논문의 값이며 현재 Conv1 예비실험의 결과로 바꾸지 않습니다.

### LEVEL 1 · 주의할 범위

| 상황 | 확인할 내용 |
| --- | --- |
| 빈 노트북 | 0바이트 파일에는 실행 가능한 분석 내용이 없습니다. |
| 자료 범위 | 개인 실행기록과 의료 원영상은 포함하지 않습니다. |
| 번호 구분 | 자료 4차는 코드·자료 보관 구분이며 네 번째 연구논문을 뜻하지 않습니다. |

환자 ID가 없어 같은 사람의 다른 사진이 섞였는지 모두 확인할 수 없습니다. 높은 정확도가 임상 성능이나 프라이버시 효과를 보장하지 않습니다. **반복 표본 5,000개를 독립 환자 5,000명으로 세지 않습니다.**

[표·코드·실행 설정·파일 전체 비교를 포함한 공통 상세](#reading-level-5)

<a id="reading-level-2"></a>

## LEVEL 2 - Explorer

<!-- semantic-revision17:level-2:start -->

<a id="semantic-lung-study2-level-2"></a>

### LEVEL 2 · 후속 원고의 분모·조건·점수

분류 정확도는 정답 비율이고 Privacy Score는 구조 비유사도여서 같은 의미가 아닙니다. Pareto 비교는 한쪽을 높일 때 다른 쪽을 얼마나 잃는지 보는 방법입니다. Block256+σ0에서 흐림을 더했을 때 점수는 조금 늘고 정확도는 크게 줄었다는 원고의 절충 해석을 아래 조건별 값과 함께 읽습니다. 7-fold는 일곱 학습 묶음, TTA는 평가 때 입력을 변형해 예측을 모으는 절차입니다.

<a id="layout18-table-7-row-1"></a>

**표본과 분할**

**조건·자료**

표본과 분할

**의미와 확인 방법**

IQ-OTH/NCCD는 두 병원·110명·1,097장으로 Benign120·Malignant561·Normal416입니다. 클래스별 원본 10%의 시험109장(12·56·41)을 먼저 분리하고 나머지를 클래스당1,000장으로 증강해 7-fold·20회TTA를 적용한 원고입니다.

<a id="layout18-table-7-row-2"></a>

**비교 조건**

**조건·자료**

비교 조건

**의미와 확인 방법**

ImageNet 사전학습 ResNet50에서 Block10·Blur10의 단독20조건과 Block→Blur100조합을 구분합니다. 100조합 노트북 하나가 전체120조건을 수행하지 않습니다.

<a id="layout18-table-7-row-3"></a>

**점수 정의**

**조건·자료**

점수 정의

**의미와 확인 방법**

Privacy Score=50×(1−MS-SSIM)이며 전체1,097장의 원본/변환 영상을 5개 스케일로 비교합니다. 단일SSIM 기반 소규모·특징맵 점수와 다릅니다.

<a id="layout18-table-7-row-4"></a>

**원고 보고값**

**조건·자료**

원고 보고값

**의미와 확인 방법**

원본98.17%; 조합 Block256+σ0는98.17%·49.65점, +σ16은62.39%·49.70점, +σ32는58.72%·49.85점입니다. Blur단독σ256은51.38%·34.62점입니다.

<a id="layout18-table-7-row-5"></a>

**다른 실행과 붕괴**

**조건·자료**

다른 실행과 붕괴

**의미와 확인 방법**

조합100조건 중53조건의51.38%는 시험56/109와 대응해 다수클래스 붕괴로 해석합니다. 조합Block512+σ256의46.8%, 단독Block256의97.25%와 조합σ0의98.17%는 서로 다른 실행입니다.

<a id="layout18-table-7-row-6"></a>

**원고와 재현**

**조건·자료**

원고와 재현

**의미와 확인 방법**

19쪽 원고이며 RTX4090·TensorFlow·혼합정밀도를 보고합니다. Precision·F1은 산출하지 않았고 독립 기관·환자 검증과 실제 복원 공격·사람의 지각 평가는 후속 과제입니다.


<a id="semantic-lung-tools-level-2"></a>

### LEVEL 2 · 자료 차수의 수정 도구와 소규모 계산

같은 설정으로 맞추는 비교와 SSIM/PSNR을 맞추는 비교는 목적이 다릅니다. 전자는 학습 조건을 맞추고 후자는 영상 유사도가 비슷한 변환 강도를 찾습니다. 자료 2차는 이 노트북을 생성/수정하며 3차는 작은 입력으로 계산 경로를 점검하고 4차는 원고와 코드를 연결합니다.

<a id="layout18-table-8-row-1"></a>

**자료1차**

**조건·자료**

자료1차

**의미와 확인 방법**

블록·블러각각rebuilt·same_settings·metric_matched의여섯노트북입니다. metric_matched는블록평균SSIM/PSNR에맞는sigma를탐색하며batch4/8·epoch·SWA가변형별로다릅니다. 보조도구는지정노트북을다시씁니다.

<a id="layout18-table-8-row-2"></a>

**자료2차**

**조건·자료**

자료2차

**의미와 확인 방법**

align_experiment_methods.mjs는GPU모니터필드/그래프호환을맞추고build_block_blur_notebook.mjs는Blur사본에서Block→Blur100조합을만듭니다. replaceOrThrow는대상문자열누락시중단하고rollback_original_notebooks.mjs는보관본/지정셀을복원합니다. Node.js와실제입력·출력경로가필요합니다.

<a id="layout18-table-8-row-3"></a>

**자료3차**

**조건·자료**

자료3차

**의미와 확인 방법**

512·seed42의3장입력, Block512·32/Blurσ0·2/조합4의8조건입니다. Privacy Score=((1−SSIM)/2)×100이며PSNR은별도참고값입니다. long·방법요약·조합pivot·best_conditions의4CSV가있습니다. 항등조건0, Block32와B32_S0의35.3667978…은3장계산확인값입니다.

<a id="layout18-table-8-row-4"></a>

**자료4차**

**조건·자료**

자료4차

**의미와 확인 방법**

자료차수/4차/코드의학습·MS-SSIM·도표코드를19쪽원고와연결합니다. pareto_scatter.ipynb는0바이트로실행내용이없습니다. 소규모SSIM표와원고1,097장MS-SSIM을섞지않습니다.


<!-- semantic-revision17:level-2:end -->

[이 수준의 프로젝트 전체 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A82.md) · [같은 수준 프로필](https://github.com/PUVKID/PUVKID/blob/main/docs/읽기안내/레벨2.md)

### LEVEL 2 · 목적과 대상

**이 차수의 목적과 실제 구성**

ResNet50 후속 원고와 입력 변환·유사도·도표 코드를 연결해 읽는 자료 차수입니다. 실제 코드 폴더는 자료차수/4차/코드에 있습니다.

<a id="layout18-table-9-row-1"></a>

**학습 코드**

**구성**

학습 코드

**실제 역할**

Blur·Block·조합 노트북이 조건별 입력과 ResNet50 평가를 구성합니다.

<a id="layout18-table-9-row-2"></a>

**지표 계산**

**구성**

지표 계산

**실제 역할**

privacy_score_ssim_psnr_updated가 MS-SSIM과 점수식을 계산합니다.

<a id="layout18-table-9-row-3"></a>

**그림 코드**

**구성**

그림 코드

**실제 역할**

heatmaps_windows·paper_figures_resnet50·plot_privacy_metrics_split 등이 표와 그림을 구성합니다.

<a id="layout18-table-9-row-4"></a>

**원고 연결**

**구성**

원고 연결

**실제 역할**

연구 2 최종 PDF/HWP와 코드의 조건·그림을 대조합니다.


입력 변형 연구 1·2, 특징 블러 Stage 1, Conv1 OK/NG 예비실험을 구분합니다. 블러는 무늬를 부드럽게 하고 블록 재배열은 위치를 섞습니다. 분류 정확도와 유사도 기반 Privacy Score는 서로 다른 양을 측정합니다.

### LEVEL 2 · 달라진 내용과 차수 관계

자료 3차의 소규모 점검에서 후속 원고·전체 지표·도표 코드를 연결한 자료 4차입니다.

[직전 단계 전체 비교·구성](../revision-diffs/folder-4.diff) · [전체 파일 크기·해시](../revision-manifests/folder-4.json)

이전 연구는 정상·양성·악성 3분류, Conv1은 OK/NG 이진 분류입니다. 원본 1,097장은 양성 120·정상 416·악성 561장입니다. 클래스당 매 epoch 5,000표본은 반복·온라인 증강이며 독립 영상 5,000장이 아닙니다.

### LEVEL 2 · 입력과 실행 조건

| 입력 | 처리 | 출력 |
| --- | --- | --- |
| 분류 결과·변환 조건 | 지표 계산 | 정확도·유사도·점수 표 |
| 결과표 | 히트맵·막대·분리 지표 그림 | 원고 도표 |
| 최종 원고 | 방법·보고값과코드대조 | 연구 2 읽기 |

| 항목 | 조건·기본값 |
| --- | --- |
| 코드 위치 | 자료차수/4차/코드 |
| 원고 | 연구 2 최종 19쪽 |
| 입력 | 의료 원영상·가중치는 별도 준비 |
| 빈 파일 | pareto_scatter.ipynb는 0바이트 |

연구 1은 512×512 입력에 두 변환을 각각 적용해 정확도·ROC-AUC·혼동행렬을 봅니다. 연구 2는 Blur→Block·Block→Blur 조합과 입력 MS-SSIM을 비교합니다. Conv1은 첫 합성곱 특징을 바꾼 뒤 분류합니다.

### LEVEL 2 · 처리 절차

1. 논문에서 확인할 그림·지표를 정한 뒤 대응 코드 파일을 엽니다.
2. 학습 결과를 입력받는 그림 코드와 원영상을 읽는 지표 코드를 구분합니다.
3. 입력 경로·CSV/JSON 열·조건 순서를 확인합니다.
4. 빈 pareto_scatter.ipynb는 실행 코드로 사용하지 않고 다른 도표 코드의 실제 내용을 확인합니다.

대표 CT 3범주와 6단계에서 조건별 PNG 18개를 만듭니다. 원본 포함 10조건이 끝나면 180개입니다. 평균·최댓값·개별 8채널의 총 10패널은 특징 반응을 보여 줍니다.

### LEVEL 2 · 결과를 확인하는 방법

원고의 보고값과 코드의 설정·저장 결과를 대조하는 자료입니다. 도표 파일명만으로 새로운 실험 결과를 추정하지 않습니다.

0바이트 pareto_scatter.ipynb는 내용 없는 원본 파일입니다. 실제 산점도·지표 계산 기능은 내용이 있는 대응 노트북을 확인해야 합니다.

연구 2는 원본 98.17%, Block256+sigma0 정확도 98.17%·Privacy Score 49.65점을 보고합니다. 유사도 점수는 복원 공격 성공률이 아닙니다. 연구 1과 모델·조건이 달라 차이의 원인을 하나로 확정하지 않습니다.

### LEVEL 2 · 주의할 범위

| 상황 | 확인할 내용 |
| --- | --- |
| 빈 노트북 | 0바이트 파일에는 실행 가능한 분석 내용이 없습니다. |
| 자료 범위 | 개인 실행기록과 의료 원영상은 포함하지 않습니다. |
| 번호 구분 | 자료 4차는 코드·자료 보관 구분이며 네 번째 연구논문을 뜻하지 않습니다. |

영상 단위 예비실험의 한계, 조건별 학습·결과 재사용, 입력과 특징의 다른 점수 정의를 함께 읽습니다. 새 종료 정책 실험의 준비와 완료도 구분합니다.

[표·코드·실행 설정·파일 전체 비교를 포함한 공통 상세](#reading-level-5)

<a id="reading-level-3"></a>

## LEVEL 3 - Practitioner

<!-- semantic-revision17:level-3:start -->

<a id="semantic-lung-study2-level-3"></a>

### LEVEL 3 · 후속 원고의 분모·조건·점수

19쪽 PDF/HWP에서 표본→분할→변환→분류→유사도 계산 순서로 확인하세요. 단독과 조합 결과표를 별도로 읽고 정확도·macro OvR ROC-AUC·클래스별 Recall·혼동행렬을 조건명으로 맞춥니다. 영상1,097장의 유사도 분모와 분류 시험109장의 분모를 섞지 않으며 아래 숫자를 새 측정값으로 재계산해 바꾸지 않습니다.

<a id="layout18-table-13-row-1"></a>

**표본과 분할**

**조건·자료**

표본과 분할

**의미와 확인 방법**

IQ-OTH/NCCD는 두 병원·110명·1,097장으로 Benign120·Malignant561·Normal416입니다. 클래스별 원본 10%의 시험109장(12·56·41)을 먼저 분리하고 나머지를 클래스당1,000장으로 증강해 7-fold·20회TTA를 적용한 원고입니다.

<a id="layout18-table-13-row-2"></a>

**비교 조건**

**조건·자료**

비교 조건

**의미와 확인 방법**

ImageNet 사전학습 ResNet50에서 Block10·Blur10의 단독20조건과 Block→Blur100조합을 구분합니다. 100조합 노트북 하나가 전체120조건을 수행하지 않습니다.

<a id="layout18-table-13-row-3"></a>

**점수 정의**

**조건·자료**

점수 정의

**의미와 확인 방법**

Privacy Score=50×(1−MS-SSIM)이며 전체1,097장의 원본/변환 영상을 5개 스케일로 비교합니다. 단일SSIM 기반 소규모·특징맵 점수와 다릅니다.

<a id="layout18-table-13-row-4"></a>

**원고 보고값**

**조건·자료**

원고 보고값

**의미와 확인 방법**

원본98.17%; 조합 Block256+σ0는98.17%·49.65점, +σ16은62.39%·49.70점, +σ32는58.72%·49.85점입니다. Blur단독σ256은51.38%·34.62점입니다.

<a id="layout18-table-13-row-5"></a>

**다른 실행과 붕괴**

**조건·자료**

다른 실행과 붕괴

**의미와 확인 방법**

조합100조건 중53조건의51.38%는 시험56/109와 대응해 다수클래스 붕괴로 해석합니다. 조합Block512+σ256의46.8%, 단독Block256의97.25%와 조합σ0의98.17%는 서로 다른 실행입니다.

<a id="layout18-table-13-row-6"></a>

**원고와 재현**

**조건·자료**

원고와 재현

**의미와 확인 방법**

19쪽 원고이며 RTX4090·TensorFlow·혼합정밀도를 보고합니다. Precision·F1은 산출하지 않았고 독립 기관·환자 검증과 실제 복원 공격·사람의 지각 평가는 후속 과제입니다.


<a id="semantic-lung-tools-level-3"></a>

### LEVEL 3 · 자료 차수의 수정 도구와 소규모 계산

수정 도구를 쓰기 전 원본 사본·실제 경로·셀 번호·치환 문자열을 확인하세요. 3차에서는 long의 condition·method·n_images·ssim_mean·privacy_score를 방법 요약/pivot과 대조합니다. 4차에서는 학습 결과 JSON/CSV를 읽는 그림 코드와 의료 원영상을 읽는 유사도 코드를 구분하고 빈 노트북을 실행 입력으로 쓰지 않습니다.

<a id="layout18-table-14-row-1"></a>

**자료1차**

**조건·자료**

자료1차

**의미와 확인 방법**

블록·블러각각rebuilt·same_settings·metric_matched의여섯노트북입니다. metric_matched는블록평균SSIM/PSNR에맞는sigma를탐색하며batch4/8·epoch·SWA가변형별로다릅니다. 보조도구는지정노트북을다시씁니다.

<a id="layout18-table-14-row-2"></a>

**자료2차**

**조건·자료**

자료2차

**의미와 확인 방법**

align_experiment_methods.mjs는GPU모니터필드/그래프호환을맞추고build_block_blur_notebook.mjs는Blur사본에서Block→Blur100조합을만듭니다. replaceOrThrow는대상문자열누락시중단하고rollback_original_notebooks.mjs는보관본/지정셀을복원합니다. Node.js와실제입력·출력경로가필요합니다.

<a id="layout18-table-14-row-3"></a>

**자료3차**

**조건·자료**

자료3차

**의미와 확인 방법**

512·seed42의3장입력, Block512·32/Blurσ0·2/조합4의8조건입니다. Privacy Score=((1−SSIM)/2)×100이며PSNR은별도참고값입니다. long·방법요약·조합pivot·best_conditions의4CSV가있습니다. 항등조건0, Block32와B32_S0의35.3667978…은3장계산확인값입니다.

<a id="layout18-table-14-row-4"></a>

**자료4차**

**조건·자료**

자료4차

**의미와 확인 방법**

자료차수/4차/코드의학습·MS-SSIM·도표코드를19쪽원고와연결합니다. pareto_scatter.ipynb는0바이트로실행내용이없습니다. 소규모SSIM표와원고1,097장MS-SSIM을섞지않습니다.


<!-- semantic-revision17:level-3:end -->

[이 수준의 프로젝트 전체 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A83.md) · [같은 수준 프로필](https://github.com/PUVKID/PUVKID/blob/main/docs/읽기안내/레벨3.md)

### LEVEL 3 · 목적과 대상

**이 차수의 목적과 실제 구성**

ResNet50 후속 원고와 입력 변환·유사도·도표 코드를 연결해 읽는 자료 차수입니다. 실제 코드 폴더는 자료차수/4차/코드에 있습니다.

<a id="layout18-table-15-row-1"></a>

**학습 코드**

**구성**

학습 코드

**실제 역할**

Blur·Block·조합 노트북이 조건별 입력과 ResNet50 평가를 구성합니다.

<a id="layout18-table-15-row-2"></a>

**지표 계산**

**구성**

지표 계산

**실제 역할**

privacy_score_ssim_psnr_updated가 MS-SSIM과 점수식을 계산합니다.

<a id="layout18-table-15-row-3"></a>

**그림 코드**

**구성**

그림 코드

**실제 역할**

heatmaps_windows·paper_figures_resnet50·plot_privacy_metrics_split 등이 표와 그림을 구성합니다.

<a id="layout18-table-15-row-4"></a>

**원고 연결**

**구성**

원고 연결

**실제 역할**

연구 2 최종 PDF/HWP와 코드의 조건·그림을 대조합니다.


원고·노트북·저장 결과·대시보드를 차수별로 읽습니다. 과거 논문의 보고값과 현재 Conv1 실행 결과를 합치지 않습니다. 재현에는 원영상·분할·설정·결과 계보가 필요하며 의료 원자료는 공개하지 않습니다.

### LEVEL 3 · 달라진 내용과 차수 관계

자료 3차의 소규모 점검에서 후속 원고·전체 지표·도표 코드를 연결한 자료 4차입니다.

[직전 단계 전체 비교·구성](../revision-diffs/folder-4.diff) · [전체 파일 크기·해시](../revision-manifests/folder-4.json)

라벨 매핑과 원본 분할을 먼저 확인합니다. 증강은 학습에만 적용하고 검증·시험 원본과 구분합니다. source_class는 원본 범주 폴더 라벨이며 환자·병원·스캐너 식별자가 아닙니다.

### LEVEL 3 · 입력과 실행 조건

| 입력 | 처리 | 출력 |
| --- | --- | --- |
| 분류 결과·변환 조건 | 지표 계산 | 정확도·유사도·점수 표 |
| 결과표 | 히트맵·막대·분리 지표 그림 | 원고 도표 |
| 최종 원고 | 방법·보고값과코드대조 | 연구 2 읽기 |

| 항목 | 조건·기본값 |
| --- | --- |
| 코드 위치 | 자료차수/4차/코드 |
| 원고 | 연구 2 최종 19쪽 |
| 입력 | 의료 원영상·가중치는 별도 준비 |
| 빈 파일 | pareto_scatter.ipynb는 0바이트 |

입력·변환 순서·분할·초기값·학습 예산을 차수별로 확인합니다. Stage 1의 pool1_pool 특징 SSIM은 입력 MS-SSIM과 직접 비교하지 않습니다. 원본 test 선분리와 학습 증강, 큰 sigma 결과 재사용도 확인합니다.

### LEVEL 3 · 처리 절차

1. 논문에서 확인할 그림·지표를 정한 뒤 대응 코드 파일을 엽니다.
2. 학습 결과를 입력받는 그림 코드와 원영상을 읽는 지표 코드를 구분합니다.
3. 입력 경로·CSV/JSON 열·조건 순서를 확인합니다.
4. 빈 pareto_scatter.ipynb는 실행 코드로 사용하지 않고 다른 도표 코드의 실제 내용을 확인합니다.

실제 완료한 최적 체크포인트와 실행 ID가 같은 결과만 조회합니다. 색은 패널별 최솟값·최댓값으로 표시하므로 다른 패널의 같은 색을 같은 값으로 보지 않습니다. 과거 PNG나 직전 시험 수치를 대기에 재사용하지 않습니다.

### LEVEL 3 · 결과를 확인하는 방법

원고의 보고값과 코드의 설정·저장 결과를 대조하는 자료입니다. 도표 파일명만으로 새로운 실험 결과를 추정하지 않습니다.

0바이트 pareto_scatter.ipynb는 내용 없는 원본 파일입니다. 실제 산점도·지표 계산 기능은 내용이 있는 대응 노트북을 확인해야 합니다.

현재 백분율 요약은 소수 첫째 자리 반올림이며 원비율·전체 백분율·정답 수를 함께 확인합니다. 과거 공개 4차의 둘째 자리 버림 설명은 당시 이력으로 두고 현재 규칙과 섞지 않습니다.

### LEVEL 3 · 주의할 범위

| 상황 | 확인할 내용 |
| --- | --- |
| 빈 노트북 | 0바이트 파일에는 실행 가능한 분석 내용이 없습니다. |
| 자료 범위 | 개인 실행기록과 의료 원영상은 포함하지 않습니다. |
| 번호 구분 | 자료 4차는 코드·자료 보관 구분이며 네 번째 연구논문을 뜻하지 않습니다. |

원본과 분할 manifest의 실제 값은 자신의 로컬 자료로 준비해야 합니다. 공개 예제만으로 기준 비교가 동작하지 않습니다. 미완료 조건과 정의 불가 지표를 보기 좋은 값으로 채우지 않습니다.

[표·코드·실행 설정·파일 전체 비교를 포함한 공통 상세](#reading-level-5)

<a id="reading-level-4"></a>

## LEVEL 4 - Advanced

<!-- semantic-revision17:level-4:start -->

<a id="semantic-lung-study2-level-4"></a>

### LEVEL 4 · 후속 원고의 분모·조건·점수

입력 Block→PIL GaussianBlur, ResNet50 평가, 5스케일 MS-SSIM 집계, Pareto 분석을 별도 처리로 봅니다. 53조건의 다수클래스 붕괴는 각 혼동행렬을 확인해야 하며 보편적인 정확도 하한이 아닙니다. 단독·조합은 별도 학습이므로 동일 변환명이라고 저장 결과를 합치지 않습니다.

<a id="layout18-table-19-row-1"></a>

**표본과 분할**

**조건·자료**

표본과 분할

**의미와 확인 방법**

IQ-OTH/NCCD는 두 병원·110명·1,097장으로 Benign120·Malignant561·Normal416입니다. 클래스별 원본 10%의 시험109장(12·56·41)을 먼저 분리하고 나머지를 클래스당1,000장으로 증강해 7-fold·20회TTA를 적용한 원고입니다.

<a id="layout18-table-19-row-2"></a>

**비교 조건**

**조건·자료**

비교 조건

**의미와 확인 방법**

ImageNet 사전학습 ResNet50에서 Block10·Blur10의 단독20조건과 Block→Blur100조합을 구분합니다. 100조합 노트북 하나가 전체120조건을 수행하지 않습니다.

<a id="layout18-table-19-row-3"></a>

**점수 정의**

**조건·자료**

점수 정의

**의미와 확인 방법**

Privacy Score=50×(1−MS-SSIM)이며 전체1,097장의 원본/변환 영상을 5개 스케일로 비교합니다. 단일SSIM 기반 소규모·특징맵 점수와 다릅니다.

<a id="layout18-table-19-row-4"></a>

**원고 보고값**

**조건·자료**

원고 보고값

**의미와 확인 방법**

원본98.17%; 조합 Block256+σ0는98.17%·49.65점, +σ16은62.39%·49.70점, +σ32는58.72%·49.85점입니다. Blur단독σ256은51.38%·34.62점입니다.

<a id="layout18-table-19-row-5"></a>

**다른 실행과 붕괴**

**조건·자료**

다른 실행과 붕괴

**의미와 확인 방법**

조합100조건 중53조건의51.38%는 시험56/109와 대응해 다수클래스 붕괴로 해석합니다. 조합Block512+σ256의46.8%, 단독Block256의97.25%와 조합σ0의98.17%는 서로 다른 실행입니다.

<a id="layout18-table-19-row-6"></a>

**원고와 재현**

**조건·자료**

원고와 재현

**의미와 확인 방법**

19쪽 원고이며 RTX4090·TensorFlow·혼합정밀도를 보고합니다. Precision·F1은 산출하지 않았고 독립 기관·환자 검증과 실제 복원 공격·사람의 지각 평가는 후속 과제입니다.


<a id="semantic-lung-tools-level-4"></a>

### LEVEL 4 · 자료 차수의 수정 도구와 소규모 계산

파일 변경 보조 도구의 JSON/문자열 계약과 실제 학습 코드를 분리합니다. 보정용 영상과 시험 자료의 관계, 치환 실패 시 중단, 복원 대상과 출력 충돌을 확인해야 합니다. 소규모 단일 SSIM 계산과 최종 MS-SSIM 집계는 별도 정의이므로 이름이 같은 Privacy Score를 통합하지 않습니다.

<a id="layout18-table-20-row-1"></a>

**자료1차**

**조건·자료**

자료1차

**의미와 확인 방법**

블록·블러각각rebuilt·same_settings·metric_matched의여섯노트북입니다. metric_matched는블록평균SSIM/PSNR에맞는sigma를탐색하며batch4/8·epoch·SWA가변형별로다릅니다. 보조도구는지정노트북을다시씁니다.

<a id="layout18-table-20-row-2"></a>

**자료2차**

**조건·자료**

자료2차

**의미와 확인 방법**

align_experiment_methods.mjs는GPU모니터필드/그래프호환을맞추고build_block_blur_notebook.mjs는Blur사본에서Block→Blur100조합을만듭니다. replaceOrThrow는대상문자열누락시중단하고rollback_original_notebooks.mjs는보관본/지정셀을복원합니다. Node.js와실제입력·출력경로가필요합니다.

<a id="layout18-table-20-row-3"></a>

**자료3차**

**조건·자료**

자료3차

**의미와 확인 방법**

512·seed42의3장입력, Block512·32/Blurσ0·2/조합4의8조건입니다. Privacy Score=((1−SSIM)/2)×100이며PSNR은별도참고값입니다. long·방법요약·조합pivot·best_conditions의4CSV가있습니다. 항등조건0, Block32와B32_S0의35.3667978…은3장계산확인값입니다.

<a id="layout18-table-20-row-4"></a>

**자료4차**

**조건·자료**

자료4차

**의미와 확인 방법**

자료차수/4차/코드의학습·MS-SSIM·도표코드를19쪽원고와연결합니다. pareto_scatter.ipynb는0바이트로실행내용이없습니다. 소규모SSIM표와원고1,097장MS-SSIM을섞지않습니다.


<!-- semantic-revision17:level-4:end -->

[이 수준의 프로젝트 전체 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A84.md) · [같은 수준 프로필](https://github.com/PUVKID/PUVKID/blob/main/docs/읽기안내/레벨4.md)

### LEVEL 4 · 목적과 대상

**이 차수의 목적과 실제 구성**

ResNet50 후속 원고와 입력 변환·유사도·도표 코드를 연결해 읽는 자료 차수입니다. 실제 코드 폴더는 자료차수/4차/코드에 있습니다.

<a id="layout18-table-21-row-1"></a>

**학습 코드**

**구성**

학습 코드

**실제 역할**

Blur·Block·조합 노트북이 조건별 입력과 ResNet50 평가를 구성합니다.

<a id="layout18-table-21-row-2"></a>

**지표 계산**

**구성**

지표 계산

**실제 역할**

privacy_score_ssim_psnr_updated가 MS-SSIM과 점수식을 계산합니다.

<a id="layout18-table-21-row-3"></a>

**그림 코드**

**구성**

그림 코드

**실제 역할**

heatmaps_windows·paper_figures_resnet50·plot_privacy_metrics_split 등이 표와 그림을 구성합니다.

<a id="layout18-table-21-row-4"></a>

**원고 연결**

**구성**

원고 연결

**실제 역할**

연구 2 최종 PDF/HWP와 코드의 조건·그림을 대조합니다.


입력 변형과 pool1_pool 특징 변형은 개입 위치가 다릅니다. 모델·학습·라벨·분할·점수 정의가 달라 단순 수치 차이를 모델 변경의 인과 효과로 설명할 수 없습니다. 종료 정책 비교도 별도 설계입니다.

### LEVEL 4 · 달라진 내용과 차수 관계

자료 3차의 소규모 점검에서 후속 원고·전체 지표·도표 코드를 연결한 자료 4차입니다.

[직전 단계 전체 비교·구성](../revision-diffs/folder-4.diff) · [전체 파일 크기·해시](../revision-manifests/folder-4.json)

환자 ID 없는 영상 그룹 분할은 환자 독립 분할의 대체가 아닙니다. 소스별 촬영·압축 차이와 같은 환자의 다른 영상이 성능에 영향을 줄 수 있습니다. 높은 정확도의 원인을 조기 종료로 미리 확정하지 않습니다.

### LEVEL 4 · 입력과 실행 조건

| 입력 | 처리 | 출력 |
| --- | --- | --- |
| 분류 결과·변환 조건 | 지표 계산 | 정확도·유사도·점수 표 |
| 결과표 | 히트맵·막대·분리 지표 그림 | 원고 도표 |
| 최종 원고 | 방법·보고값과코드대조 | 연구 2 읽기 |

| 항목 | 조건·기본값 |
| --- | --- |
| 코드 위치 | 자료차수/4차/코드 |
| 원고 | 연구 2 최종 19쪽 |
| 입력 | 의료 원영상·가중치는 별도 준비 |
| 빈 파일 | pareto_scatter.ipynb는 0바이트 |

Stage 1은 같은 프로세스의 Edge·Cloud 연결이며 실제 원격 전송이 아닙니다. 큰 sigma의 전역 평균 대체, sigma32 결과의 64/128/256 재사용과 Conv2D import 누락 같은 실행 제약을 구분합니다.

### LEVEL 4 · 처리 절차

1. 논문에서 확인할 그림·지표를 정한 뒤 대응 코드 파일을 엽니다.
2. 학습 결과를 입력받는 그림 코드와 원영상을 읽는 지표 코드를 구분합니다.
3. 입력 경로·CSV/JSON 열·조건 순서를 확인합니다.
4. 빈 pareto_scatter.ipynb는 실행 코드로 사용하지 않고 다른 도표 코드의 실제 내용을 확인합니다.

공개 4차는 학습 2차 대시보드의 로컬 수리 3차 사본입니다. 공개 5차는 실험 4차 고정 100회 비교 코드입니다. 원본 manifest·해시·정확 분할이 다르면 중단합니다.

### LEVEL 4 · 결과를 확인하는 방법

원고의 보고값과 코드의 설정·저장 결과를 대조하는 자료입니다. 도표 파일명만으로 새로운 실험 결과를 추정하지 않습니다.

0바이트 pareto_scatter.ipynb는 내용 없는 원본 파일입니다. 실제 산점도·지표 계산 기능은 내용이 있는 대응 노트북을 확인해야 합니다.

Blur sigma256의 51.38%는 다수 클래스 56/109와 같지만 모든 조건의 하한은 아닙니다. 별도 학습한 Block512+sigma256은 46.8%입니다. 조합·단독·별도 학습·시험 분모를 나누어 읽습니다.

### LEVEL 4 · 주의할 범위

| 상황 | 확인할 내용 |
| --- | --- |
| 빈 노트북 | 0바이트 파일에는 실행 가능한 분석 내용이 없습니다. |
| 자료 범위 | 개인 실행기록과 의료 원영상은 포함하지 않습니다. |
| 번호 구분 | 자료 4차는 코드·자료 보관 구분이며 네 번째 연구논문을 뜻하지 않습니다. |

기존 분할·시험셋 재사용과 환자 ID 부재는 독립 임상 평가를 제한합니다. 높은 정확도의 원인을 조기 종료로 확정하지 않고 동일 조건 정책 비교를 합니다. 두 비교 모델은 같은 학습 경로에서 선택됩니다.

[표·코드·실행 설정·파일 전체 비교를 포함한 공통 상세](#reading-level-5)

<a id="reading-level-5"></a>

## LEVEL 5 - Expert

<!-- semantic-revision17:level-5:start -->

<a id="semantic-lung-study2-level-5"></a>

### LEVEL 5 · 후속 원고의 분모·조건·점수

시험109장의 클래스 분모와 유사도1,097장의 분모, 110명이라는 원고의 환자 수를 구별합니다. 아래 원고 수치는 원정밀도로 보존합니다. 테스트 의사 라벨·증강 후fold의 누수 가능성과 코드/원고 차이를 함께 검토해야 하며 7-fold앙상블은 다중시드 반복이나 기관 외 검증을 대신하지 않습니다. 구조 점수는 공격 성공률·재식별 확률·암호학적 안전성·차등프라이버시 보장이 아닙니다.

<a id="layout18-table-25-row-1"></a>

**표본과 분할**

**조건·자료**

표본과 분할

**의미와 확인 방법**

IQ-OTH/NCCD는 두 병원·110명·1,097장으로 Benign120·Malignant561·Normal416입니다. 클래스별 원본 10%의 시험109장(12·56·41)을 먼저 분리하고 나머지를 클래스당1,000장으로 증강해 7-fold·20회TTA를 적용한 원고입니다.

<a id="layout18-table-25-row-2"></a>

**비교 조건**

**조건·자료**

비교 조건

**의미와 확인 방법**

ImageNet 사전학습 ResNet50에서 Block10·Blur10의 단독20조건과 Block→Blur100조합을 구분합니다. 100조합 노트북 하나가 전체120조건을 수행하지 않습니다.

<a id="layout18-table-25-row-3"></a>

**점수 정의**

**조건·자료**

점수 정의

**의미와 확인 방법**

Privacy Score=50×(1−MS-SSIM)이며 전체1,097장의 원본/변환 영상을 5개 스케일로 비교합니다. 단일SSIM 기반 소규모·특징맵 점수와 다릅니다.

<a id="layout18-table-25-row-4"></a>

**원고 보고값**

**조건·자료**

원고 보고값

**의미와 확인 방법**

원본98.17%; 조합 Block256+σ0는98.17%·49.65점, +σ16은62.39%·49.70점, +σ32는58.72%·49.85점입니다. Blur단독σ256은51.38%·34.62점입니다.

<a id="layout18-table-25-row-5"></a>

**다른 실행과 붕괴**

**조건·자료**

다른 실행과 붕괴

**의미와 확인 방법**

조합100조건 중53조건의51.38%는 시험56/109와 대응해 다수클래스 붕괴로 해석합니다. 조합Block512+σ256의46.8%, 단독Block256의97.25%와 조합σ0의98.17%는 서로 다른 실행입니다.

<a id="layout18-table-25-row-6"></a>

**원고와 재현**

**조건·자료**

원고와 재현

**의미와 확인 방법**

19쪽 원고이며 RTX4090·TensorFlow·혼합정밀도를 보고합니다. Precision·F1은 산출하지 않았고 독립 기관·환자 검증과 실제 복원 공격·사람의 지각 평가는 후속 과제입니다.


<a id="semantic-lung-tools-level-5"></a>

### LEVEL 5 · 자료 차수의 수정 도구와 소규모 계산

자료 1~4차의 수락 범위는 변형 코드·변경 도구·3장 8조건 점검·최종 원고 대응입니다. 35.3667978…은 저장표의 축약 표기이며 원정밀도 CSV를 유지합니다. SSIM 매칭은 분류 성능 동등성이나 공격 저항성 동등성을 증명하지 않고 0바이트 파일에서 분석 성과를 추정하지 않습니다.

<a id="layout18-table-26-row-1"></a>

**자료1차**

**조건·자료**

자료1차

**의미와 확인 방법**

블록·블러각각rebuilt·same_settings·metric_matched의여섯노트북입니다. metric_matched는블록평균SSIM/PSNR에맞는sigma를탐색하며batch4/8·epoch·SWA가변형별로다릅니다. 보조도구는지정노트북을다시씁니다.

<a id="layout18-table-26-row-2"></a>

**자료2차**

**조건·자료**

자료2차

**의미와 확인 방법**

align_experiment_methods.mjs는GPU모니터필드/그래프호환을맞추고build_block_blur_notebook.mjs는Blur사본에서Block→Blur100조합을만듭니다. replaceOrThrow는대상문자열누락시중단하고rollback_original_notebooks.mjs는보관본/지정셀을복원합니다. Node.js와실제입력·출력경로가필요합니다.

<a id="layout18-table-26-row-3"></a>

**자료3차**

**조건·자료**

자료3차

**의미와 확인 방법**

512·seed42의3장입력, Block512·32/Blurσ0·2/조합4의8조건입니다. Privacy Score=((1−SSIM)/2)×100이며PSNR은별도참고값입니다. long·방법요약·조합pivot·best_conditions의4CSV가있습니다. 항등조건0, Block32와B32_S0의35.3667978…은3장계산확인값입니다.

<a id="layout18-table-26-row-4"></a>

**자료4차**

**조건·자료**

자료4차

**의미와 확인 방법**

자료차수/4차/코드의학습·MS-SSIM·도표코드를19쪽원고와연결합니다. pareto_scatter.ipynb는0바이트로실행내용이없습니다. 소규모SSIM표와원고1,097장MS-SSIM을섞지않습니다.


<!-- semantic-revision17:level-5:end -->

[전문가 수준 프로젝트 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A85.md) · [같은 수준 프로필](https://github.com/PUVKID/PUVKID/blob/main/docs/읽기안내/레벨5.md)

**기존 전체 상세** — 다음 본문은 이 차수의 원래 방법·조건·결과·실패·한계와 전체 비교입니다. 위 수준의 설명에 필요한 공통 근거도 모두 여기서 확인할 수 있습니다.
<!-- reading-levels17:end -->

**ResNet50 후속 원고와 입력 변환·유사도·도표 코드를 연결해 읽는 자료 차수입니다.** 실제 코드 폴더는 자료차수/4차/코드에 있습니다.

분야: 연구 자료 구성 › ResNet50·MS-SSIM › 학습·지표·논문 도표

[목적](#purpose) · [기능](#features) · [입출력](#flow) · [구성](#files) · [준비](#setup) · [사용법](#usage) · [결과](#results) · [제약](#limits) · [변경](#changes)

<a name="purpose"></a>

<a id="-이-단계에서-하는-일"></a>

## 연구 목적

논문 첨부는 연구 2의 최종 전체 원고로 연결하고, 학습·지표 계산·그림 작성의 코드 역할을 구분해 살펴봅니다.

<a name="features"></a>

<a id="-주요-기능과-처리-방식"></a>

## 방법과 구현

<a id="layout18-table-27-row-1"></a>

**학습 코드**

**구성**

학습 코드

**실제 역할**

Blur·Block·조합 노트북이 조건별 입력과 ResNet50 평가를 구성합니다.

<a id="layout18-table-27-row-2"></a>

**지표 계산**

**구성**

지표 계산

**실제 역할**

privacy_score_ssim_psnr_updated가 MS-SSIM과 점수식을 계산합니다.

<a id="layout18-table-27-row-3"></a>

**그림 코드**

**구성**

그림 코드

**실제 역할**

heatmaps_windows·paper_figures_resnet50·plot_privacy_metrics_split 등이 표와 그림을 구성합니다.

<a id="layout18-table-27-row-4"></a>

**원고 연결**

**구성**

원고 연결

**실제 역할**

연구 2 최종 PDF/HWP와 코드의 조건·그림을 대조합니다.


<a name="flow"></a>

<a id="-입력--처리--출력"></a>

## 입력·처리·출력

| 입력 | 처리 | 출력 |
| --- | --- | --- |
| 분류 결과·변환 조건 | 지표 계산 | 정확도·유사도·점수 표 |
| 결과표 | 히트맵·막대·분리 지표 그림 | 원고 도표 |
| 최종 원고 | 방법·보고값과코드대조 | 연구 2 읽기 |

<a name="files"></a>

<a id="-파일과-핵심-처리"></a>

## 파일별 역할

<a id="layout18-table-29-row-1"></a>

**항목 1**

**파일**

[자료차수/4차/코드/privacy_score_ssim_psnr_updated.ipynb](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/4%EC%B0%A8/%EC%BD%94%EB%93%9C/privacy_score_ssim_psnr_updated.ipynb)

**이용 방법**

설정·함수·실행 셀

<a id="layout18-table-29-row-2"></a>

**[자료차수/4차/코드/paper_figures_resnet50.ipynb](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/4%EC%B0%A8/%EC%BD%94%EB%93%9C/paper_figures_resnet50.ipynb)**

**파일**

[자료차수/4차/코드/paper_figures_resnet50.ipynb](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/4%EC%B0%A8/%EC%BD%94%EB%93%9C/paper_figures_resnet50.ipynb)

**이용 방법**

설정·함수·실행 셀

<a id="layout18-table-29-row-3"></a>

**[자료차수/4차/코드/heatmaps_windows.ipynb](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/4%EC%B0%A8/%EC%BD%94%EB%93%9C/heatmaps_windows.ipynb)**

**파일**

[자료차수/4차/코드/heatmaps_windows.ipynb](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/4%EC%B0%A8/%EC%BD%94%EB%93%9C/heatmaps_windows.ipynb)

**이용 방법**

설정·함수·실행 셀

<a id="layout18-table-29-row-4"></a>

**[논문/연구 2_원문_최종.pdf](../../%EB%85%BC%EB%AC%B8/%EC%97%B0%EA%B5%AC2_%EC%9B%90%EB%AC%B8_%EC%B5%9C%EC%A2%85.pdf)**

**파일**

[논문/연구 2_원문_최종.pdf](../../%EB%85%BC%EB%AC%B8/%EC%97%B0%EA%B5%AC2_%EC%9B%90%EB%AC%B8_%EC%B5%9C%EC%A2%85.pdf)

**이용 방법**

전체 원문·도표 읽기


<a id="-함수셀로-찾아가기"></a>

### 관련 함수와 셀

관련 함수와 셀을 파일별로 정리했습니다. 실행 전 설정과 호출 순서, 출력 경로를 확인하세요.

<a id="layout18-table-30-row-1"></a>

**항목 1**

**파일**

[자료차수/4차/코드/privacy_score_ssim_psnr_updated.ipynb](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/4%EC%B0%A8/%EC%BD%94%EB%93%9C/privacy_score_ssim_psnr_updated.ipynb)

**핵심 정의**

셀 9: `save_condition_sample`<br>셀 11: `block_scramble` · `apply_gaussian_blur`<br>셀 13: `_is_image_file` · `_is_ignored_path` · `collect_image_files` · `load_original_images`<br>셀 15: `_to_gray` · `_downsample_avg2x2` · `_ssim_l_cs` · `compute_ms_ssim` · `compute_ssim_psnr_msssim` · `privacy_score_from_ms_ssim` · `evaluate_condition`<br>셀 21: `combo_fn`<br>셀 25: `_save` · `_annotate_bars`<br>셀 38: `_combo_transform`

<a id="layout18-table-30-row-2"></a>

**[자료차수/4차/코드/paper_figures_resnet50.ipynb](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/4%EC%B0%A8/%EC%BD%94%EB%93%9C/paper_figures_resnet50.ipynb)**

**파일**

[자료차수/4차/코드/paper_figures_resnet50.ipynb](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/4%EC%B0%A8/%EC%BD%94%EB%93%9C/paper_figures_resnet50.ipynb)

**핵심 정의**

셀 4: `_bar_colors` · `plot_clean_bar`<br>셀 6: `_try_load_json`<br>셀 12: `_try_load_privacy_csv`<br>셀 20: `encryption_strength`

<a id="layout18-table-30-row-3"></a>

**[자료차수/4차/코드/heatmaps_windows.ipynb](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/4%EC%B0%A8/%EC%BD%94%EB%93%9C/heatmaps_windows.ipynb)**

**파일**

[자료차수/4차/코드/heatmaps_windows.ipynb](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/4%EC%B0%A8/%EC%BD%94%EB%93%9C/heatmaps_windows.ipynb)

**핵심 정의**

셀 4: `draw_heatmap`


<a name="setup"></a>

<a id="️-환경과-설정"></a>

## 실행 환경과 설정

| 항목 | 조건·기본값 |
| --- | --- |
| 코드 위치 | 자료차수/4차/코드 |
| 원고 | 연구 2 최종 19쪽 |
| 입력 | 의료 원영상·가중치는 별도 준비 |
| 빈 파일 | pareto_scatter.ipynb는 0바이트 |

<a name="usage"></a>

<a id="-준비와-사용-순서"></a>

## 실행 순서

1. 논문에서 확인할 그림·지표를 정한 뒤 대응 코드 파일을 엽니다.
2. 학습 결과를 입력받는 그림 코드와 원영상을 읽는 지표 코드를 구분합니다.
3. 입력 경로·CSV/JSON 열·조건 순서를 확인합니다.
4. 빈 pareto_scatter.ipynb는 실행 코드로 사용하지 않고 다른 도표 코드의 실제 내용을 확인합니다.

<a name="results"></a>

<a id="-결과를-읽는-방법"></a>

## 결과와 해석

원고의 보고값과 코드의 설정·저장 결과를 대조하는 자료입니다. 도표 파일명만으로 새로운 실험 결과를 추정하지 않습니다.

0바이트 pareto_scatter.ipynb는 내용 없는 원본 파일입니다. 실제 산점도·지표 계산 기능은 내용이 있는 대응 노트북을 확인해야 합니다.

<a name="limits"></a>

<a id="️-알려진-제약과-확인-지점"></a>

## 제약과 확인 사항

| 상황 | 확인할 내용 |
| --- | --- |
| 빈 노트북 | 0바이트 파일에는 실행 가능한 분석 내용이 없습니다. |
| 자료 범위 | 개인 실행기록과 의료 원영상은 포함하지 않습니다. |
| 번호 구분 | 자료 4차는 코드·자료 보관 구분이며 네 번째 연구논문을 뜻하지 않습니다. |

<a name="changes"></a>

<a id="-이전-단계와의-변화"></a>

## 직전 단계와 비교

자료 3차의 소규모 점검에서 후속 원고·전체 지표·도표 코드를 연결한 자료 4차입니다.

[직전 단계 전체 비교·구성](../revision-diffs/folder-4.diff) · [전체 파일 크기·해시](../revision-manifests/folder-4.json)

<details>
<summary>이 단계의 파일 기록과 전체 해시</summary>

아래 내용는 해당 단계가 기록될 당시의 파일 정보입니다. 현재 첨부는 [프로젝트 자료 안내](../PAPERS.md)에서 확인할 수 있습니다.

<a id="layout18-table-33-row-1"></a>

**`논문/2차_ResNet50_최종.pdf`**

**파일**

`논문/2차_ResNet50_최종.pdf`

**종류**

.pdf

**바이트**

2827829

**SHA-256**

`b64645277f78ac2b2c87a1dcc15216ec9ad6c41a5a20f795465748ac0d2f76c7`

<a id="layout18-table-33-row-2"></a>

**[자료차수/4차/코드/block_blur_resnet50_v4_KO.ipynb](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/4%EC%B0%A8/%EC%BD%94%EB%93%9C/block_blur_resnet50_v4_KO.ipynb)**

**파일**

[자료차수/4차/코드/block_blur_resnet50_v4_KO.ipynb](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/4%EC%B0%A8/%EC%BD%94%EB%93%9C/block_blur_resnet50_v4_KO.ipynb)

**종류**

.ipynb

**바이트**

219524

**SHA-256**

`da4b889ce6dc4f4c908cc98986724abd25cd0dbd6aa1425b5e014b1f7a7fee03`

<a id="layout18-table-33-row-3"></a>

**항목 3**

**파일**

[자료차수/4차/코드/block_encryption_resnet50_rebuilt_KO.ipynb](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/4%EC%B0%A8/%EC%BD%94%EB%93%9C/block_encryption_resnet50_rebuilt_KO.ipynb)

**종류**

.ipynb

**바이트**

135877

**SHA-256**

`cc8eb1485adac09ffdcb2a5c0e502e016f5a5bb1c60898746be7ef9ce87a1986`

<a id="layout18-table-33-row-4"></a>

**[자료차수/4차/코드/blur_resnet50_rebuilt2_KO.ipynb](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/4%EC%B0%A8/%EC%BD%94%EB%93%9C/blur_resnet50_rebuilt2_KO.ipynb)**

**파일**

[자료차수/4차/코드/blur_resnet50_rebuilt2_KO.ipynb](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/4%EC%B0%A8/%EC%BD%94%EB%93%9C/blur_resnet50_rebuilt2_KO.ipynb)

**종류**

.ipynb

**바이트**

130270

**SHA-256**

`2a3da41eff6a705b2e30668e63d4fe42d4029dc307de2cb197ff8a6434f31faa`

<a id="layout18-table-33-row-5"></a>

**[자료차수/4차/코드/heatmaps_windows.ipynb](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/4%EC%B0%A8/%EC%BD%94%EB%93%9C/heatmaps_windows.ipynb)**

**파일**

[자료차수/4차/코드/heatmaps_windows.ipynb](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/4%EC%B0%A8/%EC%BD%94%EB%93%9C/heatmaps_windows.ipynb)

**종류**

.ipynb

**바이트**

8646

**SHA-256**

`75c45970b92c8957ea61de8c236e045c3a0d77ed0de942815d3b16ae6e24ef4a`

<a id="layout18-table-33-row-6"></a>

**[자료차수/4차/코드/paper_figures_resnet50.ipynb](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/4%EC%B0%A8/%EC%BD%94%EB%93%9C/paper_figures_resnet50.ipynb)**

**파일**

[자료차수/4차/코드/paper_figures_resnet50.ipynb](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/4%EC%B0%A8/%EC%BD%94%EB%93%9C/paper_figures_resnet50.ipynb)

**종류**

.ipynb

**바이트**

37162

**SHA-256**

`f317a502c0658e3dbcb90cb7af67db526d6594f733b0a0bccb6ec536a3df53c0`

<a id="layout18-table-33-row-7"></a>

**[자료차수/4차/코드/pareto_scatter.ipynb](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/4%EC%B0%A8/%EC%BD%94%EB%93%9C/pareto_scatter.ipynb)**

**파일**

[자료차수/4차/코드/pareto_scatter.ipynb](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/4%EC%B0%A8/%EC%BD%94%EB%93%9C/pareto_scatter.ipynb)

**종류**

.ipynb

**바이트**

0

**SHA-256**

`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

<a id="layout18-table-33-row-8"></a>

**[자료차수/4차/코드/picture2x2.ipynb](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/4%EC%B0%A8/%EC%BD%94%EB%93%9C/picture2x2.ipynb)**

**파일**

[자료차수/4차/코드/picture2x2.ipynb](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/4%EC%B0%A8/%EC%BD%94%EB%93%9C/picture2x2.ipynb)

**종류**

.ipynb

**바이트**

7054

**SHA-256**

`d56ae7885ab9219f62bb695fe1e5de081c7e667ebbf8c5916b87909bff4b2046`

<a id="layout18-table-33-row-9"></a>

**[자료차수/4차/코드/plot_privacy_metrics_split.ipynb](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/4%EC%B0%A8/%EC%BD%94%EB%93%9C/plot_privacy_metrics_split.ipynb)**

**파일**

[자료차수/4차/코드/plot_privacy_metrics_split.ipynb](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/4%EC%B0%A8/%EC%BD%94%EB%93%9C/plot_privacy_metrics_split.ipynb)

**종류**

.ipynb

**바이트**

18984

**SHA-256**

`77cc7650ee472043999937da35fd6ac817330ce45a796c584330571ccf1e05be`

<a id="layout18-table-33-row-10"></a>

**항목 10**

**파일**

[자료차수/4차/코드/privacy_score_ssim_psnr_updated.ipynb](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/4%EC%B0%A8/%EC%BD%94%EB%93%9C/privacy_score_ssim_psnr_updated.ipynb)

**종류**

.ipynb

**바이트**

94241

**SHA-256**

`1b25934ba5fbee1a8fa025596bfa852c6cfe2667f9edb56a5fe57852d35ea6b5`

<a id="layout18-table-33-row-11"></a>

**[최신 편집 원문](../../%EB%85%BC%EB%AC%B8/%EC%97%B0%EA%B5%AC2_%EC%9B%90%EB%AC%B8_%EC%B5%9C%EC%A2%85.hwp)**

**파일**

[최신 편집 원문](../../%EB%85%BC%EB%AC%B8/%EC%97%B0%EA%B5%AC2_%EC%9B%90%EB%AC%B8_%EC%B5%9C%EC%A2%85.hwp)

**종류**

.hwp

**바이트**

414720

**SHA-256**

`7f3d880b8df41d7549973470476f6011ce80ca835f36f7ac62e22acdb978f196`


</details>

---

[프로젝트](../../README.md) · [전체 차수](../REVISION_INDEX.md) · [자료 폴더](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/4%EC%B0%A8/%EC%BD%94%EB%93%9C) · [폴더 3차](folder-3.md)

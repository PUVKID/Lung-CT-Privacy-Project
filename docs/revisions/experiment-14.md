<a id="-추가-실험--학습유사도도표-코드-모음"></a>

# 추가 실험 · 학습·유사도·도표 코드 모음

<!-- reading-levels17:start -->
**읽기 수준 선택** · [LEVEL 1 - Beginner](#reading-level-1) · [LEVEL 2 - Explorer](#reading-level-2) · [LEVEL 3 - Practitioner](#reading-level-3) · [LEVEL 4 - Advanced](#reading-level-4) · [LEVEL 5 - Expert](#reading-level-5)

<a id="reading-level-1"></a>

## LEVEL 1 - Beginner

<!-- semantic-revision17:level-1:start -->

<a id="semantic-lung-legacy-level-1"></a>

### LEVEL 1 · 초기 조직영상 앱과 추가 학습 코드

조직영상은 현미경으로 보는 조직 사진이고 CT와 다른 입력입니다. 화면의 다섯 이름과 학습 파일의 세 이름이 달라 같은 모델이라고 바로 연결할 수 없습니다. 추가 노트북에는 여러 실험 셀이 모여 있으므로 모두 이어 실행하는 하나의 완성 학습으로 보지 않습니다.

<a id="layout18-table-1-row-1"></a>

**초기화면**

**조건·자료**

초기화면

**의미와 확인 방법**

Streamlit이업로드영상을224×224·255로나눔·배치차원추가후Model.h5의대장선암/대장정상/폐선암/폐정상/폐편평상피암5라벨확률을텍스트와원형그래프로보입니다. Train.ipynb는MobileNetV2 3클래스·224·batch16·10epoch여서모델대응을따로확인합니다.

<a id="layout18-table-1-row-2"></a>

**추가셀**

**조건·자료**

추가셀

**의미와 확인 방법**

Train.ipynb셀0은조직영상5클래스, 셀1·2는EfficientNetV2-S CT블록/블러, 셀3~5는MobileNetV2/풀링비교입니다. 코드별입력224/512와클래스수를확인합니다.

<a id="layout18-table-1-row-3"></a>

**계산과제약**

**조건·자료**

계산과제약

**의미와 확인 방법**

SSIM·PSNR·MS-SSIM·DSSIM변형과저장분류JSON/유사도CSV를그리는코드를구분합니다. 100−accuracy·특징수비율security는공격저항성실측이아니며첫학습셀끝의Markdown백틱·문법·사본별설정을확인합니다.


<!-- semantic-revision17:level-1:end -->

[이 수준의 프로젝트 전체 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A81.md) · [같은 수준 프로필](https://github.com/PUVKID/PUVKID/blob/main/docs/읽기안내/레벨1.md)

### LEVEL 1 · 목적과 대상

**이 차수의 목적과 실제 구성**

EfficientNetV2-S·MobileNetV2·ResNet50의 서로 다른 학습 셀과 SSIM/MS-SSIM·도표 코드를 모은 자료입니다.

<a id="layout18-table-2-row-1"></a>

**Train.ipynb**

**구성**

Train.ipynb

**실제 역할**

셀 0은 조직영상 5클래스, 셀 1·2는 EfficientNetV2-S의 CT 블록·블러, 셀 3~5는 MobileNetV2와 풀링 비교입니다.

<a id="layout18-table-2-row-2"></a>

**ResNet50 사본**

**구성**

ResNet50 사본

**실제 역할**

단독·조합·edge·Stage1 특징 블러 노트북을 각각 구분합니다.

<a id="layout18-table-2-row-3"></a>

**유사도 코드**

**구성**

유사도 코드

**실제 역할**

SSIM·PSNR·MS-SSIM과 DSSIM 기반 점수의 여러 버전을 보관합니다.

<a id="layout18-table-2-row-4"></a>

**도표**

**구성**

도표

**실제 역할**

저장된 분류 JSON과 유사도 CSV에서 막대·히트맵·논문 그림을 구성합니다.


CT 사진을 흐리게 하거나 블록으로 재배열했을 때 분류 결과와 영상 유사도가 어떻게 달라지는지 살펴봅니다. 입력 사진을 바꾸는 연구와 모델 내부의 첫 합성곱 특징을 흐리는 실험이 함께 있습니다. **논문 연구 번호·공개 코드 차수·실제 학습 차수는 다릅니다.**

### LEVEL 1 · 달라진 내용과 차수 관계

분류·유사도·도표의 추가 연구 코드를 모은 묶음입니다. 단독 실험·조합 실험·특징 변환과 각각 연결합니다.

[직전 단계 전체 비교·구성](../revision-diffs/experiment-14.diff) · [전체 파일 크기·해시](../revision-manifests/experiment-14.json)

사진의 모양이 바뀌었어도 분류기가 정답을 잘 맞추는지, 얼마나 비슷한 정보를 남기는지 따로 봅니다. OK는 양성+정상, NG는 악성입니다. 사진 수·독립 환자 수·반복 학습 표본 수를 섞지 않습니다.

### LEVEL 1 · 입력과 실행 조건

**입력**

선택한 모델·영상

**처리**

해당 셀의 학습·분류

**출력**

모델별 결과


**입력**

원본·변환 영상

**처리**

SSIM·PSNR·MS-SSIM 계산

**출력**

정의가 다른 유사도 지표


**입력**

저장 결과

**처리**

조건 대조와 도표 작성

**출력**

표·그림



**항목**

입력 크기

**조건·기본값**

코드별 224 또는 512


**항목**

점수식

**조건·기본값**

SSIM과 MS-SSIM 기반 변형을 구분


**항목**

모델

**조건·기본값**

조직영상·CT 모델과 클래스 수를 각 셀에서 확인


**항목**

실행

**조건·기본값**

선택한 입력·가중치·패키지·GPU를 준비



입력 사진에 블러·블록을 적용하는 경로와 모델이 뽑은 특징에 블러를 적용하는 경로를 나눕니다. 특징은 사진에서 찾은 선·무늬의 반응입니다. 그 색이 병변 위치나 악성 확률을 뜻하지 않습니다.

### LEVEL 1 · 처리 절차

1. 분류 학습·유사도 계산·도표 중 목적을 먼저 정합니다.
2. 선택한 셀의 모델·영상 종류·크기·클래스와 입력 경로를 확인합니다.
3. 설치·데이터 생성·학습·파일 쓰기 셀을 구분합니다.
4. 지표식과 캐시·출력 파일을 읽고 같은 조건의 결과만 비교합니다.

전체 차수 표에서 읽을 연구를 고릅니다. 노트북을 여는 것과 새 학습 시작은 다릅니다. 대시보드에서 같은 강도의 사진·곡선·시험 수치를 함께 읽되 미완료 조건은 미측정으로 남깁니다.

### LEVEL 1 · 결과를 확인하는 방법

Train.ipynb에는 정확도나 특징 수의 비율로 만든 security 표현도 있습니다. 이 값은 실제 공격 저항성 평가와 다릅니다.

첫 학습 셀 끝의 Markdown 백틱과 사본별 문법·설정 차이를 확인해야 합니다. 후속 논문 보고값과 여러 실험 코드를 한 번의 동일 실행으로 합치지 않습니다.

연구 1의 원고 보고 정확도는 원본 92.5%, sigma32 블러 53.3%, Block32 재배열 79.2%입니다. 이는 당시 논문의 값이며 현재 Conv1 예비실험의 결과로 바꾸지 않습니다.

### LEVEL 1 · 주의할 범위

**상황**

셀 독립성

**확인할 내용**

입력 종류·모델·클래스가 달라 모든 셀을 같은 학습으로 연속 실행하지 않습니다.


**상황**

점수 정의

**확인할 내용**

유사도·정확도·특징 수 비율로 만든 값은 서로 다른 지표입니다.


**상황**

문법

**확인할 내용**

Train 첫 셀 끝의 백틱과 각 노트북의 구문을 확인합니다.



환자 ID가 없어 같은 사람의 다른 사진이 섞였는지 모두 확인할 수 없습니다. 높은 정확도가 임상 성능이나 프라이버시 효과를 보장하지 않습니다. **반복 표본 5,000개를 독립 환자 5,000명으로 세지 않습니다.**

[표·코드·실행 설정·파일 전체 비교를 포함한 공통 상세](#reading-level-5)

<a id="reading-level-2"></a>

## LEVEL 2 - Explorer

<!-- semantic-revision17:level-2:start -->

<a id="semantic-lung-legacy-level-2"></a>

### LEVEL 2 · 초기 조직영상 앱과 추가 학습 코드

화면은 업로드→크기 조정→정규화→모델 확률→문자/원형 그래프로 이어집니다. 학습 셀의 모델과 클래스 구성이 화면과 맞아야 출력을 올바르게 해석할 수 있습니다. 유사도와 정확도를 뒤집은 security 표현은 계산식의 의미가 다릅니다.

<a id="layout18-table-6-row-1"></a>

**초기화면**

**조건·자료**

초기화면

**의미와 확인 방법**

Streamlit이업로드영상을224×224·255로나눔·배치차원추가후Model.h5의대장선암/대장정상/폐선암/폐정상/폐편평상피암5라벨확률을텍스트와원형그래프로보입니다. Train.ipynb는MobileNetV2 3클래스·224·batch16·10epoch여서모델대응을따로확인합니다.

<a id="layout18-table-6-row-2"></a>

**추가셀**

**조건·자료**

추가셀

**의미와 확인 방법**

Train.ipynb셀0은조직영상5클래스, 셀1·2는EfficientNetV2-S CT블록/블러, 셀3~5는MobileNetV2/풀링비교입니다. 코드별입력224/512와클래스수를확인합니다.

<a id="layout18-table-6-row-3"></a>

**계산과제약**

**조건·자료**

계산과제약

**의미와 확인 방법**

SSIM·PSNR·MS-SSIM·DSSIM변형과저장분류JSON/유사도CSV를그리는코드를구분합니다. 100−accuracy·특징수비율security는공격저항성실측이아니며첫학습셀끝의Markdown백틱·문법·사본별설정을확인합니다.


<!-- semantic-revision17:level-2:end -->

[이 수준의 프로젝트 전체 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A82.md) · [같은 수준 프로필](https://github.com/PUVKID/PUVKID/blob/main/docs/읽기안내/레벨2.md)

### LEVEL 2 · 목적과 대상

**이 차수의 목적과 실제 구성**

EfficientNetV2-S·MobileNetV2·ResNet50의 서로 다른 학습 셀과 SSIM/MS-SSIM·도표 코드를 모은 자료입니다.

<a id="layout18-table-7-row-1"></a>

**Train.ipynb**

**구성**

Train.ipynb

**실제 역할**

셀 0은 조직영상 5클래스, 셀 1·2는 EfficientNetV2-S의 CT 블록·블러, 셀 3~5는 MobileNetV2와 풀링 비교입니다.

<a id="layout18-table-7-row-2"></a>

**ResNet50 사본**

**구성**

ResNet50 사본

**실제 역할**

단독·조합·edge·Stage1 특징 블러 노트북을 각각 구분합니다.

<a id="layout18-table-7-row-3"></a>

**유사도 코드**

**구성**

유사도 코드

**실제 역할**

SSIM·PSNR·MS-SSIM과 DSSIM 기반 점수의 여러 버전을 보관합니다.

<a id="layout18-table-7-row-4"></a>

**도표**

**구성**

도표

**실제 역할**

저장된 분류 JSON과 유사도 CSV에서 막대·히트맵·논문 그림을 구성합니다.


입력 변형 연구 1·2, 특징 블러 Stage 1, Conv1 OK/NG 예비실험을 구분합니다. 블러는 무늬를 부드럽게 하고 블록 재배열은 위치를 섞습니다. 분류 정확도와 유사도 기반 Privacy Score는 서로 다른 양을 측정합니다.

### LEVEL 2 · 달라진 내용과 차수 관계

분류·유사도·도표의 추가 연구 코드를 모은 묶음입니다. 단독 실험·조합 실험·특징 변환과 각각 연결합니다.

[직전 단계 전체 비교·구성](../revision-diffs/experiment-14.diff) · [전체 파일 크기·해시](../revision-manifests/experiment-14.json)

이전 연구는 정상·양성·악성 3분류, Conv1은 OK/NG 이진 분류입니다. 원본 1,097장은 양성 120·정상 416·악성 561장입니다. 클래스당 매 epoch 5,000표본은 반복·온라인 증강이며 독립 영상 5,000장이 아닙니다.

### LEVEL 2 · 입력과 실행 조건

**입력**

선택한 모델·영상

**처리**

해당 셀의 학습·분류

**출력**

모델별 결과


**입력**

원본·변환 영상

**처리**

SSIM·PSNR·MS-SSIM 계산

**출력**

정의가 다른 유사도 지표


**입력**

저장 결과

**처리**

조건 대조와 도표 작성

**출력**

표·그림



**항목**

입력 크기

**조건·기본값**

코드별 224 또는 512


**항목**

점수식

**조건·기본값**

SSIM과 MS-SSIM 기반 변형을 구분


**항목**

모델

**조건·기본값**

조직영상·CT 모델과 클래스 수를 각 셀에서 확인


**항목**

실행

**조건·기본값**

선택한 입력·가중치·패키지·GPU를 준비



연구 1은 512×512 입력에 두 변환을 각각 적용해 정확도·ROC-AUC·혼동행렬을 봅니다. 연구 2는 Blur→Block·Block→Blur 조합과 입력 MS-SSIM을 비교합니다. Conv1은 첫 합성곱 특징을 바꾼 뒤 분류합니다.

### LEVEL 2 · 처리 절차

1. 분류 학습·유사도 계산·도표 중 목적을 먼저 정합니다.
2. 선택한 셀의 모델·영상 종류·크기·클래스와 입력 경로를 확인합니다.
3. 설치·데이터 생성·학습·파일 쓰기 셀을 구분합니다.
4. 지표식과 캐시·출력 파일을 읽고 같은 조건의 결과만 비교합니다.

대표 CT 3범주와 6단계에서 조건별 PNG 18개를 만듭니다. 원본 포함 10조건이 끝나면 180개입니다. 평균·최댓값·개별 8채널의 총 10패널은 특징 반응을 보여 줍니다.

### LEVEL 2 · 결과를 확인하는 방법

Train.ipynb에는 정확도나 특징 수의 비율로 만든 security 표현도 있습니다. 이 값은 실제 공격 저항성 평가와 다릅니다.

첫 학습 셀 끝의 Markdown 백틱과 사본별 문법·설정 차이를 확인해야 합니다. 후속 논문 보고값과 여러 실험 코드를 한 번의 동일 실행으로 합치지 않습니다.

연구 2는 원본 98.17%, Block256+sigma0 정확도 98.17%·Privacy Score 49.65점을 보고합니다. 유사도 점수는 복원 공격 성공률이 아닙니다. 연구 1과 모델·조건이 달라 차이의 원인을 하나로 확정하지 않습니다.

### LEVEL 2 · 주의할 범위

**상황**

셀 독립성

**확인할 내용**

입력 종류·모델·클래스가 달라 모든 셀을 같은 학습으로 연속 실행하지 않습니다.


**상황**

점수 정의

**확인할 내용**

유사도·정확도·특징 수 비율로 만든 값은 서로 다른 지표입니다.


**상황**

문법

**확인할 내용**

Train 첫 셀 끝의 백틱과 각 노트북의 구문을 확인합니다.



영상 단위 예비실험의 한계, 조건별 학습·결과 재사용, 입력과 특징의 다른 점수 정의를 함께 읽습니다. 새 종료 정책 실험의 준비와 완료도 구분합니다.

[표·코드·실행 설정·파일 전체 비교를 포함한 공통 상세](#reading-level-5)

<a id="reading-level-3"></a>

## LEVEL 3 - Practitioner

<!-- semantic-revision17:level-3:start -->

<a id="semantic-lung-legacy-level-3"></a>

### LEVEL 3 · 초기 조직영상 앱과 추가 학습 코드

앱을 읽기 전 Model.h5의 출력 차원·라벨 순서와 학습 노트북의 실제 구성을 대조하세요. 추가 노트북에서는 사용할 셀을 선택하고 입력 크기·자료 종류·가중치·문법을 확인합니다. 그래프는 저장 JSON/CSV의 어느 값을 입력받는지 확인하며 실제 진단으로 사용했다고 보고하지 않습니다.

<a id="layout18-table-11-row-1"></a>

**초기화면**

**조건·자료**

초기화면

**의미와 확인 방법**

Streamlit이업로드영상을224×224·255로나눔·배치차원추가후Model.h5의대장선암/대장정상/폐선암/폐정상/폐편평상피암5라벨확률을텍스트와원형그래프로보입니다. Train.ipynb는MobileNetV2 3클래스·224·batch16·10epoch여서모델대응을따로확인합니다.

<a id="layout18-table-11-row-2"></a>

**추가셀**

**조건·자료**

추가셀

**의미와 확인 방법**

Train.ipynb셀0은조직영상5클래스, 셀1·2는EfficientNetV2-S CT블록/블러, 셀3~5는MobileNetV2/풀링비교입니다. 코드별입력224/512와클래스수를확인합니다.

<a id="layout18-table-11-row-3"></a>

**계산과제약**

**조건·자료**

계산과제약

**의미와 확인 방법**

SSIM·PSNR·MS-SSIM·DSSIM변형과저장분류JSON/유사도CSV를그리는코드를구분합니다. 100−accuracy·특징수비율security는공격저항성실측이아니며첫학습셀끝의Markdown백틱·문법·사본별설정을확인합니다.


<!-- semantic-revision17:level-3:end -->

[이 수준의 프로젝트 전체 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A83.md) · [같은 수준 프로필](https://github.com/PUVKID/PUVKID/blob/main/docs/읽기안내/레벨3.md)

### LEVEL 3 · 목적과 대상

**이 차수의 목적과 실제 구성**

EfficientNetV2-S·MobileNetV2·ResNet50의 서로 다른 학습 셀과 SSIM/MS-SSIM·도표 코드를 모은 자료입니다.

<a id="layout18-table-12-row-1"></a>

**Train.ipynb**

**구성**

Train.ipynb

**실제 역할**

셀 0은 조직영상 5클래스, 셀 1·2는 EfficientNetV2-S의 CT 블록·블러, 셀 3~5는 MobileNetV2와 풀링 비교입니다.

<a id="layout18-table-12-row-2"></a>

**ResNet50 사본**

**구성**

ResNet50 사본

**실제 역할**

단독·조합·edge·Stage1 특징 블러 노트북을 각각 구분합니다.

<a id="layout18-table-12-row-3"></a>

**유사도 코드**

**구성**

유사도 코드

**실제 역할**

SSIM·PSNR·MS-SSIM과 DSSIM 기반 점수의 여러 버전을 보관합니다.

<a id="layout18-table-12-row-4"></a>

**도표**

**구성**

도표

**실제 역할**

저장된 분류 JSON과 유사도 CSV에서 막대·히트맵·논문 그림을 구성합니다.


원고·노트북·저장 결과·대시보드를 차수별로 읽습니다. 과거 논문의 보고값과 현재 Conv1 실행 결과를 합치지 않습니다. 재현에는 원영상·분할·설정·결과 계보가 필요하며 의료 원자료는 공개하지 않습니다.

### LEVEL 3 · 달라진 내용과 차수 관계

분류·유사도·도표의 추가 연구 코드를 모은 묶음입니다. 단독 실험·조합 실험·특징 변환과 각각 연결합니다.

[직전 단계 전체 비교·구성](../revision-diffs/experiment-14.diff) · [전체 파일 크기·해시](../revision-manifests/experiment-14.json)

라벨 매핑과 원본 분할을 먼저 확인합니다. 증강은 학습에만 적용하고 검증·시험 원본과 구분합니다. source_class는 원본 범주 폴더 라벨이며 환자·병원·스캐너 식별자가 아닙니다.

### LEVEL 3 · 입력과 실행 조건

**입력**

선택한 모델·영상

**처리**

해당 셀의 학습·분류

**출력**

모델별 결과


**입력**

원본·변환 영상

**처리**

SSIM·PSNR·MS-SSIM 계산

**출력**

정의가 다른 유사도 지표


**입력**

저장 결과

**처리**

조건 대조와 도표 작성

**출력**

표·그림



**항목**

입력 크기

**조건·기본값**

코드별 224 또는 512


**항목**

점수식

**조건·기본값**

SSIM과 MS-SSIM 기반 변형을 구분


**항목**

모델

**조건·기본값**

조직영상·CT 모델과 클래스 수를 각 셀에서 확인


**항목**

실행

**조건·기본값**

선택한 입력·가중치·패키지·GPU를 준비



입력·변환 순서·분할·초기값·학습 예산을 차수별로 확인합니다. Stage 1의 pool1_pool 특징 SSIM은 입력 MS-SSIM과 직접 비교하지 않습니다. 원본 test 선분리와 학습 증강, 큰 sigma 결과 재사용도 확인합니다.

### LEVEL 3 · 처리 절차

1. 분류 학습·유사도 계산·도표 중 목적을 먼저 정합니다.
2. 선택한 셀의 모델·영상 종류·크기·클래스와 입력 경로를 확인합니다.
3. 설치·데이터 생성·학습·파일 쓰기 셀을 구분합니다.
4. 지표식과 캐시·출력 파일을 읽고 같은 조건의 결과만 비교합니다.

실제 완료한 최적 체크포인트와 실행 ID가 같은 결과만 조회합니다. 색은 패널별 최솟값·최댓값으로 표시하므로 다른 패널의 같은 색을 같은 값으로 보지 않습니다. 과거 PNG나 직전 시험 수치를 대기에 재사용하지 않습니다.

### LEVEL 3 · 결과를 확인하는 방법

Train.ipynb에는 정확도나 특징 수의 비율로 만든 security 표현도 있습니다. 이 값은 실제 공격 저항성 평가와 다릅니다.

첫 학습 셀 끝의 Markdown 백틱과 사본별 문법·설정 차이를 확인해야 합니다. 후속 논문 보고값과 여러 실험 코드를 한 번의 동일 실행으로 합치지 않습니다.

현재 백분율 요약은 소수 첫째 자리 반올림이며 원비율·전체 백분율·정답 수를 함께 확인합니다. 과거 공개 4차의 둘째 자리 버림 설명은 당시 이력으로 두고 현재 규칙과 섞지 않습니다.

### LEVEL 3 · 주의할 범위

**상황**

셀 독립성

**확인할 내용**

입력 종류·모델·클래스가 달라 모든 셀을 같은 학습으로 연속 실행하지 않습니다.


**상황**

점수 정의

**확인할 내용**

유사도·정확도·특징 수 비율로 만든 값은 서로 다른 지표입니다.


**상황**

문법

**확인할 내용**

Train 첫 셀 끝의 백틱과 각 노트북의 구문을 확인합니다.



원본과 분할 manifest의 실제 값은 자신의 로컬 자료로 준비해야 합니다. 공개 예제만으로 기준 비교가 동작하지 않습니다. 미완료 조건과 정의 불가 지표를 보기 좋은 값으로 채우지 않습니다.

[표·코드·실행 설정·파일 전체 비교를 포함한 공통 상세](#reading-level-5)

<a id="reading-level-4"></a>

## LEVEL 4 - Advanced

<!-- semantic-revision17:level-4:start -->

<a id="semantic-lung-legacy-level-4"></a>

### LEVEL 4 · 초기 조직영상 앱과 추가 학습 코드

전처리 함수·모델 예측·화면 라벨의 경계를 검토하고 5라벨 UI와 3클래스 학습의 불일치를 보존합니다. 추가 셀들은 서로 다른 모델/풀링/입력 크기를 갖는 자료 모음이며 동일 학습 상태를 공유한다고 가정하지 않습니다.

<a id="layout18-table-16-row-1"></a>

**초기화면**

**조건·자료**

초기화면

**의미와 확인 방법**

Streamlit이업로드영상을224×224·255로나눔·배치차원추가후Model.h5의대장선암/대장정상/폐선암/폐정상/폐편평상피암5라벨확률을텍스트와원형그래프로보입니다. Train.ipynb는MobileNetV2 3클래스·224·batch16·10epoch여서모델대응을따로확인합니다.

<a id="layout18-table-16-row-2"></a>

**추가셀**

**조건·자료**

추가셀

**의미와 확인 방법**

Train.ipynb셀0은조직영상5클래스, 셀1·2는EfficientNetV2-S CT블록/블러, 셀3~5는MobileNetV2/풀링비교입니다. 코드별입력224/512와클래스수를확인합니다.

<a id="layout18-table-16-row-3"></a>

**계산과제약**

**조건·자료**

계산과제약

**의미와 확인 방법**

SSIM·PSNR·MS-SSIM·DSSIM변형과저장분류JSON/유사도CSV를그리는코드를구분합니다. 100−accuracy·특징수비율security는공격저항성실측이아니며첫학습셀끝의Markdown백틱·문법·사본별설정을확인합니다.


<!-- semantic-revision17:level-4:end -->

[이 수준의 프로젝트 전체 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A84.md) · [같은 수준 프로필](https://github.com/PUVKID/PUVKID/blob/main/docs/읽기안내/레벨4.md)

### LEVEL 4 · 목적과 대상

**이 차수의 목적과 실제 구성**

EfficientNetV2-S·MobileNetV2·ResNet50의 서로 다른 학습 셀과 SSIM/MS-SSIM·도표 코드를 모은 자료입니다.

<a id="layout18-table-17-row-1"></a>

**Train.ipynb**

**구성**

Train.ipynb

**실제 역할**

셀 0은 조직영상 5클래스, 셀 1·2는 EfficientNetV2-S의 CT 블록·블러, 셀 3~5는 MobileNetV2와 풀링 비교입니다.

<a id="layout18-table-17-row-2"></a>

**ResNet50 사본**

**구성**

ResNet50 사본

**실제 역할**

단독·조합·edge·Stage1 특징 블러 노트북을 각각 구분합니다.

<a id="layout18-table-17-row-3"></a>

**유사도 코드**

**구성**

유사도 코드

**실제 역할**

SSIM·PSNR·MS-SSIM과 DSSIM 기반 점수의 여러 버전을 보관합니다.

<a id="layout18-table-17-row-4"></a>

**도표**

**구성**

도표

**실제 역할**

저장된 분류 JSON과 유사도 CSV에서 막대·히트맵·논문 그림을 구성합니다.


입력 변형과 pool1_pool 특징 변형은 개입 위치가 다릅니다. 모델·학습·라벨·분할·점수 정의가 달라 단순 수치 차이를 모델 변경의 인과 효과로 설명할 수 없습니다. 종료 정책 비교도 별도 설계입니다.

### LEVEL 4 · 달라진 내용과 차수 관계

분류·유사도·도표의 추가 연구 코드를 모은 묶음입니다. 단독 실험·조합 실험·특징 변환과 각각 연결합니다.

[직전 단계 전체 비교·구성](../revision-diffs/experiment-14.diff) · [전체 파일 크기·해시](../revision-manifests/experiment-14.json)

환자 ID 없는 영상 그룹 분할은 환자 독립 분할의 대체가 아닙니다. 소스별 촬영·압축 차이와 같은 환자의 다른 영상이 성능에 영향을 줄 수 있습니다. 높은 정확도의 원인을 조기 종료로 미리 확정하지 않습니다.

### LEVEL 4 · 입력과 실행 조건

**입력**

선택한 모델·영상

**처리**

해당 셀의 학습·분류

**출력**

모델별 결과


**입력**

원본·변환 영상

**처리**

SSIM·PSNR·MS-SSIM 계산

**출력**

정의가 다른 유사도 지표


**입력**

저장 결과

**처리**

조건 대조와 도표 작성

**출력**

표·그림



**항목**

입력 크기

**조건·기본값**

코드별 224 또는 512


**항목**

점수식

**조건·기본값**

SSIM과 MS-SSIM 기반 변형을 구분


**항목**

모델

**조건·기본값**

조직영상·CT 모델과 클래스 수를 각 셀에서 확인


**항목**

실행

**조건·기본값**

선택한 입력·가중치·패키지·GPU를 준비



Stage 1은 같은 프로세스의 Edge·Cloud 연결이며 실제 원격 전송이 아닙니다. 큰 sigma의 전역 평균 대체, sigma32 결과의 64/128/256 재사용과 Conv2D import 누락 같은 실행 제약을 구분합니다.

### LEVEL 4 · 처리 절차

1. 분류 학습·유사도 계산·도표 중 목적을 먼저 정합니다.
2. 선택한 셀의 모델·영상 종류·크기·클래스와 입력 경로를 확인합니다.
3. 설치·데이터 생성·학습·파일 쓰기 셀을 구분합니다.
4. 지표식과 캐시·출력 파일을 읽고 같은 조건의 결과만 비교합니다.

공개 4차는 학습 2차 대시보드의 로컬 수리 3차 사본입니다. 공개 5차는 실험 4차 고정 100회 비교 코드입니다. 원본 manifest·해시·정확 분할이 다르면 중단합니다.

### LEVEL 4 · 결과를 확인하는 방법

Train.ipynb에는 정확도나 특징 수의 비율로 만든 security 표현도 있습니다. 이 값은 실제 공격 저항성 평가와 다릅니다.

첫 학습 셀 끝의 Markdown 백틱과 사본별 문법·설정 차이를 확인해야 합니다. 후속 논문 보고값과 여러 실험 코드를 한 번의 동일 실행으로 합치지 않습니다.

Blur sigma256의 51.38%는 다수 클래스 56/109와 같지만 모든 조건의 하한은 아닙니다. 별도 학습한 Block512+sigma256은 46.8%입니다. 조합·단독·별도 학습·시험 분모를 나누어 읽습니다.

### LEVEL 4 · 주의할 범위

**상황**

셀 독립성

**확인할 내용**

입력 종류·모델·클래스가 달라 모든 셀을 같은 학습으로 연속 실행하지 않습니다.


**상황**

점수 정의

**확인할 내용**

유사도·정확도·특징 수 비율로 만든 값은 서로 다른 지표입니다.


**상황**

문법

**확인할 내용**

Train 첫 셀 끝의 백틱과 각 노트북의 구문을 확인합니다.



기존 분할·시험셋 재사용과 환자 ID 부재는 독립 임상 평가를 제한합니다. 높은 정확도의 원인을 조기 종료로 확정하지 않고 동일 조건 정책 비교를 합니다. 두 비교 모델은 같은 학습 경로에서 선택됩니다.

[표·코드·실행 설정·파일 전체 비교를 포함한 공통 상세](#reading-level-5)

<a id="reading-level-5"></a>

## LEVEL 5 - Expert

<!-- semantic-revision17:level-5:start -->

<a id="semantic-lung-legacy-level-5"></a>

### LEVEL 5 · 초기 조직영상 앱과 추가 학습 코드

초기 조직영상 앱과 후속 CT 연구의 입력 도메인·모델·분모를 분리합니다. 백틱/문법 문제와 미확인 가중치 대응이 남아 있는 코드를 완전 실행 검증으로 소개하지 않고 security라는 변수명으로 개인정보 보호 효과를 추정하지 않습니다.

<a id="layout18-table-21-row-1"></a>

**초기화면**

**조건·자료**

초기화면

**의미와 확인 방법**

Streamlit이업로드영상을224×224·255로나눔·배치차원추가후Model.h5의대장선암/대장정상/폐선암/폐정상/폐편평상피암5라벨확률을텍스트와원형그래프로보입니다. Train.ipynb는MobileNetV2 3클래스·224·batch16·10epoch여서모델대응을따로확인합니다.

<a id="layout18-table-21-row-2"></a>

**추가셀**

**조건·자료**

추가셀

**의미와 확인 방법**

Train.ipynb셀0은조직영상5클래스, 셀1·2는EfficientNetV2-S CT블록/블러, 셀3~5는MobileNetV2/풀링비교입니다. 코드별입력224/512와클래스수를확인합니다.

<a id="layout18-table-21-row-3"></a>

**계산과제약**

**조건·자료**

계산과제약

**의미와 확인 방법**

SSIM·PSNR·MS-SSIM·DSSIM변형과저장분류JSON/유사도CSV를그리는코드를구분합니다. 100−accuracy·특징수비율security는공격저항성실측이아니며첫학습셀끝의Markdown백틱·문법·사본별설정을확인합니다.


<!-- semantic-revision17:level-5:end -->

[전문가 수준 프로젝트 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A85.md) · [같은 수준 프로필](https://github.com/PUVKID/PUVKID/blob/main/docs/읽기안내/레벨5.md)

**기존 전체 상세** — 다음 본문은 이 차수의 원래 방법·조건·결과·실패·한계와 전체 비교입니다. 위 수준의 설명에 필요한 공통 근거도 모두 여기서 확인할 수 있습니다.
<!-- reading-levels17:end -->

**EfficientNetV2-S·MobileNetV2·ResNet50의 서로 다른 학습 셀과 SSIM/MS-SSIM·도표 코드를 모은 자료입니다.**

분야: 실험 코드 모음 › TensorFlow·영상 유사도 › 학습·지표·그래프

[목적](#purpose) · [기능](#features) · [입출력](#flow) · [구성](#files) · [준비](#setup) · [사용법](#usage) · [결과](#results) · [제약](#limits) · [변경](#changes)

<a name="purpose"></a>

<a id="-이-단계에서-하는-일"></a>

## 연구 목적

모델·입력 종류·크기·점수식·변환 위치가 다른 코드를 목적에 맞게 선택해 읽습니다. 모든 셀을 하나의 연속된 학습으로 실행하는 구성은 아닙니다.

<a name="features"></a>

<a id="-주요-기능과-처리-방식"></a>

## 방법과 구현

<a id="layout18-table-22-row-1"></a>

**Train.ipynb**

**구성**

Train.ipynb

**실제 역할**

셀 0은 조직영상 5클래스, 셀 1·2는 EfficientNetV2-S의 CT 블록·블러, 셀 3~5는 MobileNetV2와 풀링 비교입니다.

<a id="layout18-table-22-row-2"></a>

**ResNet50 사본**

**구성**

ResNet50 사본

**실제 역할**

단독·조합·edge·Stage1 특징 블러 노트북을 각각 구분합니다.

<a id="layout18-table-22-row-3"></a>

**유사도 코드**

**구성**

유사도 코드

**실제 역할**

SSIM·PSNR·MS-SSIM과 DSSIM 기반 점수의 여러 버전을 보관합니다.

<a id="layout18-table-22-row-4"></a>

**도표**

**구성**

도표

**실제 역할**

저장된 분류 JSON과 유사도 CSV에서 막대·히트맵·논문 그림을 구성합니다.


<a name="flow"></a>

<a id="-입력--처리--출력"></a>

## 입력·처리·출력

**입력**

선택한 모델·영상

**처리**

해당 셀의 학습·분류

**출력**

모델별 결과


**입력**

원본·변환 영상

**처리**

SSIM·PSNR·MS-SSIM 계산

**출력**

정의가 다른 유사도 지표


**입력**

저장 결과

**처리**

조건 대조와 도표 작성

**출력**

표·그림



<a name="files"></a>

<a id="-파일과-핵심-처리"></a>

## 파일별 역할

<a id="layout18-table-24-row-1"></a>

**[추가 학습모델과 실험/Train.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/Train.ipynb)**

**파일**

[추가 학습모델과 실험/Train.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/Train.ipynb)

**이용 방법**

설정·함수·실행 셀

<a id="layout18-table-24-row-2"></a>

**항목 2**

**파일**

[추가 학습모델과 실험/privacy_score_ssim_psnr_updated.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/privacy_score_ssim_psnr_updated.ipynb)

**이용 방법**

설정·함수·실행 셀

<a id="layout18-table-24-row-3"></a>

**항목 3**

**파일**

[추가 학습모델과 실험/privacy_score_quantitative_docker_vscode.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/privacy_score_quantitative_docker_vscode.ipynb)

**이용 방법**

설정·함수·실행 셀

<a id="layout18-table-24-row-4"></a>

**[추가 학습모델과 실험/paper_figures_resnet50.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/paper_figures_resnet50.ipynb)**

**파일**

[추가 학습모델과 실험/paper_figures_resnet50.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/paper_figures_resnet50.ipynb)

**이용 방법**

설정·함수·실행 셀


<a id="-함수셀로-찾아가기"></a>

### 관련 함수와 셀

관련 함수와 셀을 파일별로 정리했습니다. 실행 전 설정과 호출 순서, 출력 경로를 확인하세요.

<a id="layout18-table-25-row-1"></a>

**[추가 학습모델과 실험/Train.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/Train.ipynb)**

**파일**

[추가 학습모델과 실험/Train.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/Train.ipynb)

**핵심 정의**

셀 1: `block_scramble` · `generate_block_dataset` · `oversample_dir` · `prepare_split` · `get_paths_labels` · `load_image` · `augment_train` · `cutmix_batch`<br>셀 2: `apply_gaussian_blur` · `generate_blur_dataset` · `oversample_dir` · `prepare_split` · `get_paths_labels` · `load_image` · `augment_train` · `cutmix_batch`<br>셀 3: `oversample_dir` · `style_ax`<br>셀 4: `style_ax` · `oversample_dir`<br>셀 5: `style_ax` · `oversample_dir`

<a id="layout18-table-25-row-2"></a>

**항목 2**

**파일**

[추가 학습모델과 실험/privacy_score_ssim_psnr_updated.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/privacy_score_ssim_psnr_updated.ipynb)

**핵심 정의**

셀 9: `save_condition_sample`<br>셀 11: `block_scramble` · `apply_gaussian_blur`<br>셀 13: `_is_image_file` · `_is_ignored_path` · `collect_image_files` · `load_original_images`<br>셀 15: `_to_gray` · `_downsample_avg2x2` · `_ssim_l_cs` · `compute_ms_ssim` · `compute_ssim_psnr_msssim` · `privacy_score_from_ms_ssim` · `evaluate_condition`<br>셀 21: `combo_fn`<br>셀 25: `_save` · `_annotate_bars`<br>셀 38: `_combo_transform`

<a id="layout18-table-25-row-3"></a>

**항목 3**

**파일**

[추가 학습모델과 실험/privacy_score_quantitative_docker_vscode.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/privacy_score_quantitative_docker_vscode.ipynb)

**핵심 정의**

셀 6: `path_exists` · `candidate_train_dirs` · `should_ignore` · `count_images_under`<br>셀 8: `collect_image_table`<br>셀 10: `setup_matplotlib_font` · `load_rgb_image` · `block_scramble` · `apply_gaussian_blur` · `apply_transform`<br>셀 12: `compute_pair_metrics` · `load_image_records` · `iter_records` · `evaluate_condition` · `condition_name` · `format_sigma`<br>셀 18: `save_fig`<br>셀 20: `save_table_png`<br>셀 22: `parse_condition`

<a id="layout18-table-25-row-4"></a>

**[추가 학습모델과 실험/paper_figures_resnet50.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/paper_figures_resnet50.ipynb)**

**파일**

[추가 학습모델과 실험/paper_figures_resnet50.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/paper_figures_resnet50.ipynb)

**핵심 정의**

셀 4: `_bar_colors` · `plot_clean_bar`<br>셀 6: `_try_load_json`<br>셀 12: `_try_load_privacy_csv`<br>셀 20: `encryption_strength`


<a name="setup"></a>

<a id="️-환경과-설정"></a>

## 실행 환경과 설정

**항목**

입력 크기

**조건·기본값**

코드별 224 또는 512


**항목**

점수식

**조건·기본값**

SSIM과 MS-SSIM 기반 변형을 구분


**항목**

모델

**조건·기본값**

조직영상·CT 모델과 클래스 수를 각 셀에서 확인


**항목**

실행

**조건·기본값**

선택한 입력·가중치·패키지·GPU를 준비



<a name="usage"></a>

<a id="-준비와-사용-순서"></a>

## 실행 순서

1. 분류 학습·유사도 계산·도표 중 목적을 먼저 정합니다.
2. 선택한 셀의 모델·영상 종류·크기·클래스와 입력 경로를 확인합니다.
3. 설치·데이터 생성·학습·파일 쓰기 셀을 구분합니다.
4. 지표식과 캐시·출력 파일을 읽고 같은 조건의 결과만 비교합니다.

<a name="results"></a>

<a id="-결과를-읽는-방법"></a>

## 결과와 해석

Train.ipynb에는 정확도나 특징 수의 비율로 만든 security 표현도 있습니다. 이 값은 실제 공격 저항성 평가와 다릅니다.

첫 학습 셀 끝의 Markdown 백틱과 사본별 문법·설정 차이를 확인해야 합니다. 후속 논문 보고값과 여러 실험 코드를 한 번의 동일 실행으로 합치지 않습니다.

<a name="limits"></a>

<a id="️-알려진-제약과-확인-지점"></a>

## 제약과 확인 사항

**상황**

셀 독립성

**확인할 내용**

입력 종류·모델·클래스가 달라 모든 셀을 같은 학습으로 연속 실행하지 않습니다.


**상황**

점수 정의

**확인할 내용**

유사도·정확도·특징 수 비율로 만든 값은 서로 다른 지표입니다.


**상황**

문법

**확인할 내용**

Train 첫 셀 끝의 백틱과 각 노트북의 구문을 확인합니다.



<a name="changes"></a>

<a id="-이전-단계와의-변화"></a>

## 직전 단계와 비교

분류·유사도·도표의 추가 연구 코드를 모은 묶음입니다. 단독 실험·조합 실험·특징 변환과 각각 연결합니다.

[직전 단계 전체 비교·구성](../revision-diffs/experiment-14.diff) · [전체 파일 크기·해시](../revision-manifests/experiment-14.json)

<details>
<summary>이 단계의 파일 기록과 전체 해시</summary>

아래 내용는 해당 단계가 기록될 당시의 파일 정보입니다. 현재 첨부는 [프로젝트 자료 안내](../PAPERS.md)에서 확인할 수 있습니다.

<a id="layout18-table-28-row-1"></a>

**[추가 학습모델과 실험/block_blur_resnet50_edge.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/block_blur_resnet50_edge.ipynb)**

**파일**

[추가 학습모델과 실험/block_blur_resnet50_edge.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/block_blur_resnet50_edge.ipynb)

**종류**

.ipynb

**바이트**

147769

**SHA-256**

`00f076b8f3f842398c3abfbfd3984fca4cb984c619d05a04f4a7affc5c101cbb`

<a id="layout18-table-28-row-2"></a>

**[추가 학습모델과 실험/block_blur_resnet50_v4_KO.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/block_blur_resnet50_v4_KO.ipynb)**

**파일**

[추가 학습모델과 실험/block_blur_resnet50_v4_KO.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/block_blur_resnet50_v4_KO.ipynb)

**종류**

.ipynb

**바이트**

136449

**SHA-256**

`efdb4bc4e54aef87ca99b2acca4bd36c4f49093351d613ca254c6ddf90de46fc`

<a id="layout18-table-28-row-3"></a>

**항목 3**

**파일**

[추가 학습모델과 실험/block_encryption_resnet50_edge_v2.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/block_encryption_resnet50_edge_v2.ipynb)

**종류**

.ipynb

**바이트**

120967

**SHA-256**

`487f9f127c9e7c83d6bfa47b9f165858cc7d7f1630fc83cbd1b0be99070cb6e4`

<a id="layout18-table-28-row-4"></a>

**항목 4**

**파일**

[추가 학습모델과 실험/block_encryption_resnet50_rebuilt_KO.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/block_encryption_resnet50_rebuilt_KO.ipynb)

**종류**

.ipynb

**바이트**

108653

**SHA-256**

`3daed3071f6399ccc1edff47b8925bf31d39ee9a74fc9478f3ec6bee773393af`

<a id="layout18-table-28-row-5"></a>

**[추가 학습모델과 실험/Blur_Block_1차_그래프_white.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/Blur_Block_1%EC%B0%A8_%EA%B7%B8%EB%9E%98%ED%94%84_white.ipynb)**

**파일**

[추가 학습모델과 실험/Blur_Block_1차_그래프_white.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/Blur_Block_1%EC%B0%A8_%EA%B7%B8%EB%9E%98%ED%94%84_white.ipynb)

**종류**

.ipynb

**바이트**

52637

**SHA-256**

`6d0db255fee2dc5aa25aee28f86b5c96fbe9a3dcf0dc12aa6747fbe01d9615aa`

<a id="layout18-table-28-row-6"></a>

**[추가 학습모델과 실험/blur_resnet50_edge_v6.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/blur_resnet50_edge_v6.ipynb)**

**파일**

[추가 학습모델과 실험/blur_resnet50_edge_v6.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/blur_resnet50_edge_v6.ipynb)

**종류**

.ipynb

**바이트**

119871

**SHA-256**

`20fe0e593c391887e2d2e346f1fe4c15b3e5cf3f0908783bb895e90ea571f51f`

<a id="layout18-table-28-row-7"></a>

**[추가 학습모델과 실험/blur_resnet50_rebuilt2_KO.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/blur_resnet50_rebuilt2_KO.ipynb)**

**파일**

[추가 학습모델과 실험/blur_resnet50_rebuilt2_KO.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/blur_resnet50_rebuilt2_KO.ipynb)

**종류**

.ipynb

**바이트**

102127

**SHA-256**

`745bb2b539259819784a219ebde96df31797fad820af09cd183177e529986870`

<a id="layout18-table-28-row-8"></a>

**[추가 학습모델과 실험/heatmaps.py](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/heatmaps.py)**

**파일**

[추가 학습모델과 실험/heatmaps.py](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/heatmaps.py)

**종류**

.py

**바이트**

5522

**SHA-256**

`640b4514d3f218a84c2030b8d3868611ce48a37ef9cf46f93a1be5f0dba73420`

<a id="layout18-table-28-row-9"></a>

**[추가 학습모델과 실험/paper_figures_resnet50.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/paper_figures_resnet50.ipynb)**

**파일**

[추가 학습모델과 실험/paper_figures_resnet50.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/paper_figures_resnet50.ipynb)

**종류**

.ipynb

**바이트**

24466

**SHA-256**

`3f3cf3e396737690701969ced7982cff12f001fc7f05e6201d065a807f89aa0d`

<a id="layout18-table-28-row-10"></a>

**[추가 학습모델과 실험/plot_privacy_metrics_split.py](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/plot_privacy_metrics_split.py)**

**파일**

[추가 학습모델과 실험/plot_privacy_metrics_split.py](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/plot_privacy_metrics_split.py)

**종류**

.py

**바이트**

5450

**SHA-256**

`3a25a124e4a88e663a675d8791660ecdc61468a3b260bc4e8588e78c994cbcb9`

<a id="layout18-table-28-row-11"></a>

**항목 11**

**파일**

[추가 학습모델과 실험/privacy_score_quantitative_docker_vscode.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/privacy_score_quantitative_docker_vscode.ipynb)

**종류**

.ipynb

**바이트**

37525

**SHA-256**

`9d9c636cfb43dd76cf562e4cf378581748aaf8cd88fbcc2eac516be8ed3858a7`

<a id="layout18-table-28-row-12"></a>

**[추가 학습모델과 실험/privacy_score_ssim_psnr (1).ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/privacy_score_ssim_psnr%20%281%29.ipynb)**

**파일**

[추가 학습모델과 실험/privacy_score_ssim_psnr (1).ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/privacy_score_ssim_psnr%20%281%29.ipynb)

**종류**

.ipynb

**바이트**

29338

**SHA-256**

`276cfc4297f975d48eb3e6bcf0a5acac98b6d207ba5d30c2c4f849c5cd3e0434`

<a id="layout18-table-28-row-13"></a>

**항목 13**

**파일**

[추가 학습모델과 실험/privacy_score_ssim_psnr (1)_backup_before_ssim_only_20260825_005153.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/privacy_score_ssim_psnr%20%281%29_backup_before_ssim_only_20260825_005153.ipynb)

**종류**

.ipynb

**바이트**

29338

**SHA-256**

`276cfc4297f975d48eb3e6bcf0a5acac98b6d207ba5d30c2c4f849c5cd3e0434`

<a id="layout18-table-28-row-14"></a>

**[추가 학습모델과 실험/privacy_score_ssim_psnr.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/privacy_score_ssim_psnr.ipynb)**

**파일**

[추가 학습모델과 실험/privacy_score_ssim_psnr.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/privacy_score_ssim_psnr.ipynb)

**종류**

.ipynb

**바이트**

26824

**SHA-256**

`05f77ac6b7d7b91eb0d0e8ada4aa746ca7654cc5a8554739aea163ea2eab63b5`

<a id="layout18-table-28-row-15"></a>

**항목 15**

**파일**

[추가 학습모델과 실험/privacy_score_ssim_psnr_updated.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/privacy_score_ssim_psnr_updated.ipynb)

**종류**

.ipynb

**바이트**

52527

**SHA-256**

`e0ce3aa6dd0a1fa307eea53cb1a2253266431a2ab0d86b984d72010aafc2c6ef`

<a id="layout18-table-28-row-16"></a>

**항목 16**

**파일**

[추가 학습모델과 실험/stage1_edge_feature_blur_resnet50.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/stage1_edge_feature_blur_resnet50.ipynb)

**종류**

.ipynb

**바이트**

136778

**SHA-256**

`a32e79c0ef1e8386c1148e4761c3c61554316b7be55117377939a932f5f5be8f`

<a id="layout18-table-28-row-17"></a>

**[추가 학습모델과 실험/Train.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/Train.ipynb)**

**파일**

[추가 학습모델과 실험/Train.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/Train.ipynb)

**종류**

.ipynb

**바이트**

315835

**SHA-256**

`df318f23b1a07b5307ab4043d89bce8206eccf6fd27053efe8c06268ce24f771`

<a id="layout18-table-28-row-18"></a>

**[원본자료/추가 학습모델과 실험/all_block_results.json](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/all_block_results.json)**

**파일**

[원본자료/추가 학습모델과 실험/all_block_results.json](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/all_block_results.json)

**종류**

.json

**바이트**

5040

**SHA-256**

`a85dd325d928a5e3ae116c6d8d5ca0d06b90e632313b28ca694d81fa80cb9801`

<a id="layout18-table-28-row-19"></a>

**항목 19**

**파일**

[원본자료/추가 학습모델과 실험/block_blur_resnet50_edge.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/block_blur_resnet50_edge.ipynb)

**종류**

.ipynb

**바이트**

148347

**SHA-256**

`ae3e302e19d2db72ce572ec48cf3d0301b4b4011866a43a5e206a8e1097033a9`

<a id="layout18-table-28-row-20"></a>

**항목 20**

**파일**

[원본자료/추가 학습모델과 실험/block_encryption_resnet50_edge_v2.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/block_encryption_resnet50_edge_v2.ipynb)

**종류**

.ipynb

**바이트**

168661

**SHA-256**

`90b3a37cc1f8fa3152f45c77e803c38db5b14f46d0aaa268d4bdb05b9acbc23a`

<a id="layout18-table-28-row-21"></a>

**항목 21**

**파일**

[원본자료/추가 학습모델과 실험/block_encryption_resnet50_rebuilt_KO.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/block_encryption_resnet50_rebuilt_KO.ipynb)

**종류**

.ipynb

**바이트**

138317

**SHA-256**

`4233928cb2aba1e9e1306e02ffc8a7cf5f17e62b72b83ccc2e8ec228c592c80f`

<a id="layout18-table-28-row-22"></a>

**항목 22**

**파일**

[원본자료/추가 학습모델과 실험/Blur_Block_1차_그래프_white.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/Blur_Block_1%EC%B0%A8_%EA%B7%B8%EB%9E%98%ED%94%84_white.ipynb)

**종류**

.ipynb

**바이트**

59418

**SHA-256**

`6ed385e04f1e500f3f1c57c7eb272a5bdd1ce9a4013d203b87fa6891ba830a50`

<a id="layout18-table-28-row-23"></a>

**[원본자료/추가 학습모델과 실험/blur_resnet50_edge_v6.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/blur_resnet50_edge_v6.ipynb)**

**파일**

[원본자료/추가 학습모델과 실험/blur_resnet50_edge_v6.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/blur_resnet50_edge_v6.ipynb)

**종류**

.ipynb

**바이트**

169241

**SHA-256**

`539e5539a73d019912257aafde527c501e7735cd6fbbfa48b26f1d2ab5c27eda`

<a id="layout18-table-28-row-24"></a>

**항목 24**

**파일**

[원본자료/추가 학습모델과 실험/blur_resnet50_rebuilt2_KO.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/blur_resnet50_rebuilt2_KO.ipynb)

**종류**

.ipynb

**바이트**

132788

**SHA-256**

`90c8e0f7a25c4533dc2b6759fa295bc7d758dd256330367d7c395dff2bee0d4f`

<a id="layout18-table-28-row-25"></a>

**[원본자료/추가 학습모델과 실험/heatmaps.py](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/heatmaps.py)**

**파일**

[원본자료/추가 학습모델과 실험/heatmaps.py](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/heatmaps.py)

**종류**

.py

**바이트**

5522

**SHA-256**

`640b4514d3f218a84c2030b8d3868611ce48a37ef9cf46f93a1be5f0dba73420`

<a id="layout18-table-28-row-26"></a>

**[원본자료/추가 학습모델과 실험/paper_figures_resnet50.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/paper_figures_resnet50.ipynb)**

**파일**

[원본자료/추가 학습모델과 실험/paper_figures_resnet50.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/paper_figures_resnet50.ipynb)

**종류**

.ipynb

**바이트**

24465

**SHA-256**

`f19095c9cfe4ee0e8441768135de6563eadc26451a760c5b13981703013b733c`

<a id="layout18-table-28-row-27"></a>

**항목 27**

**파일**

[원본자료/추가 학습모델과 실험/plot_privacy_metrics_split.py](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/plot_privacy_metrics_split.py)

**종류**

.py

**바이트**

5450

**SHA-256**

`3a25a124e4a88e663a675d8791660ecdc61468a3b260bc4e8588e78c994cbcb9`

<a id="layout18-table-28-row-28"></a>

**항목 28**

**파일**

[원본자료/추가 학습모델과 실험/privacy_score_quantitative_docker_vscode.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/privacy_score_quantitative_docker_vscode.ipynb)

**종류**

.ipynb

**바이트**

38472

**SHA-256**

`862bff744ac2f97bbfad309bb72a60349ca46e39388dba2810f911d966c91dd7`

<a id="layout18-table-28-row-29"></a>

**항목 29**

**파일**

[원본자료/추가 학습모델과 실험/privacy_score_ssim_psnr (1).ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/privacy_score_ssim_psnr%20%281%29.ipynb)

**종류**

.ipynb

**바이트**

54595

**SHA-256**

`3474c6ad8fdbda957d99f2d921a68af01248ca6336395d499ee4a92e1ef9572c`

<a id="layout18-table-28-row-30"></a>

**항목 30**

**파일**

[원본자료/추가 학습모델과 실험/privacy_score_ssim_psnr (1)_backup_before_ssim_only_20260825_005153.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/privacy_score_ssim_psnr%20%281%29_backup_before_ssim_only_20260825_005153.ipynb)

**종류**

.ipynb

**바이트**

54595

**SHA-256**

`fac8097fe5bdf91303bba90801e379b479150bd06ecc2a4ae67d80d8e1d7810a`

<a id="layout18-table-28-row-31"></a>

**항목 31**

**파일**

[원본자료/추가 학습모델과 실험/privacy_score_ssim_psnr.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/privacy_score_ssim_psnr.ipynb)

**종류**

.ipynb

**바이트**

26823

**SHA-256**

`0657ef57f42a0f08539a4809517cb7668a0014f00a87e4d176ff6364a61f22f0`

<a id="layout18-table-28-row-32"></a>

**항목 32**

**파일**

[원본자료/추가 학습모델과 실험/privacy_score_ssim_psnr_updated.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/privacy_score_ssim_psnr_updated.ipynb)

**종류**

.ipynb

**바이트**

96269

**SHA-256**

`74cb8eb330d2a60c357ff4806f3d4a5c3aeefb3f5f3cc2c0b188d792decb863a`

<a id="layout18-table-28-row-33"></a>

**항목 33**

**파일**

[원본자료/추가 학습모델과 실험/stage1_edge_feature_blur_resnet50.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/stage1_edge_feature_blur_resnet50.ipynb)

**종류**

.ipynb

**바이트**

136778

**SHA-256**

`a32e79c0ef1e8386c1148e4761c3c61554316b7be55117377939a932f5f5be8f`

<a id="layout18-table-28-row-34"></a>

**[원본자료/추가 학습모델과 실험/Train.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/Train.ipynb)**

**파일**

[원본자료/추가 학습모델과 실험/Train.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/Train.ipynb)

**종류**

.ipynb

**바이트**

315835

**SHA-256**

`df318f23b1a07b5307ab4043d89bce8206eccf6fd27053efe8c06268ce24f771`

<a id="layout18-table-28-row-35"></a>

**항목 35**

**파일**

[원본자료/추가 학습모델과 실험/privacy_score_outputs/privacy_scores.csv](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/privacy_score_outputs/privacy_scores.csv)

**종류**

.csv

**바이트**

22820

**SHA-256**

`02561595bba02a4a53890867a54f6f22111af4d986aef58ede7aff8cbeba9e69`

<a id="layout18-table-28-row-36"></a>

**항목 36**

**파일**

[원본자료/추가 학습모델과 실험/privacy_score_outputs/privacy_scores.json](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/privacy_score_outputs/privacy_scores.json)

**종류**

.json

**바이트**

45067

**SHA-256**

`bcf31f719a941652bfb77d3f952e8c7f52687cb03115f04c44e16c72361bc36b`

<a id="layout18-table-28-row-37"></a>

**항목 37**

**파일**

[원본자료/추가 학습모델과 실험/privacy_score_outputs/privacy_scores.xlsx](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/privacy_score_outputs/privacy_scores.xlsx)

**종류**

.xlsx

**바이트**

21554

**SHA-256**

`1045b2c09cebc7092dbb20563ec6bd0c76238695e42ce0d414a5969c5106cd98`

<a id="layout18-table-28-row-38"></a>

**항목 38**

**파일**

[원본자료/추가 학습모델과 실험/privacy_score_outputs/tables/best_by_type.csv](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/privacy_score_outputs/tables/best_by_type.csv)

**종류**

.csv

**바이트**

728

**SHA-256**

`823dc8104c8aa1cebae6b4eeb2ee745997ab2c77ab155a15830e0cd54fc00f6f`

<a id="layout18-table-28-row-39"></a>

**항목 39**

**파일**

[원본자료/추가 학습모델과 실험/privacy_score_outputs/tables/selected_images.csv](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/privacy_score_outputs/tables/selected_images.csv)

**종류**

.csv

**바이트**

117495

**SHA-256**

`6153b9d964ed487924ecfa96cd75fa3898ad05be54bcb28942f0925a9feee9c1`

<a id="layout18-table-28-row-40"></a>

**항목 40**

**파일**

[원본자료/추가 학습모델과 실험/privacy_score_outputs/tables/summary_by_type.csv](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/privacy_score_outputs/tables/summary_by_type.csv)

**종류**

.csv

**바이트**

407

**SHA-256**

`aca5a2d0b0ddcb21e0f1aa39d0f60cf9919eaada24dcd00d86cd0ffe653c2437`


</details>

---

[프로젝트](../../README.md) · [전체 차수](../REVISION_INDEX.md) · [자료 폴더](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98)

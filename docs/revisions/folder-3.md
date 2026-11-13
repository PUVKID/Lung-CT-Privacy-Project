<a id="-자료-3차--privacy-score의-소규모-계산-확인"></a>

# 자료 3차 · Privacy Score의 소규모 계산 확인

<!-- reading-levels17:start -->
**읽기 수준 선택** · [LEVEL 1 - Beginner](#reading-level-1) · [LEVEL 2 - Explorer](#reading-level-2) · [LEVEL 3 - Practitioner](#reading-level-3) · [LEVEL 4 - Advanced](#reading-level-4) · [LEVEL 5 - Expert](#reading-level-5)

<a id="reading-level-1"></a>

## LEVEL 1 - Beginner

<!-- semantic-revision17:level-1:start -->

<a id="semantic-lung-tools-level-1"></a>

### LEVEL 1 · 자료 차수의 수정 도구와 소규모 계산

자료 차수는 논문 번호와 다른 **파일 보관 단계**입니다. 노트북을 고치는 도구는 학습을 대신하지 않고, 3장짜리 계산은 전체 사진의 연구 결과를 대신하지 않습니다. 항등 조건은 사진을 바꾸지 않은 조건이라 구조 차이 점수가 0입니다. 빈 파일은 이름만으로 기능이 있는 것처럼 읽지 않습니다.

<a id="layout18-table-1-row-1"></a>

**자료1차**

**조건·자료**

자료1차

**의미와 확인 방법**

블록·블러각각rebuilt·same_settings·metric_matched의여섯노트북입니다. metric_matched는블록평균SSIM/PSNR에맞는sigma를탐색하며batch4/8·epoch·SWA가변형별로다릅니다. 보조도구는지정노트북을다시씁니다.

<a id="layout18-table-1-row-2"></a>

**자료2차**

**조건·자료**

자료2차

**의미와 확인 방법**

align_experiment_methods.mjs는GPU모니터필드/그래프호환을맞추고build_block_blur_notebook.mjs는Blur사본에서Block→Blur100조합을만듭니다. replaceOrThrow는대상문자열누락시중단하고rollback_original_notebooks.mjs는보관본/지정셀을복원합니다. Node.js와실제입력·출력경로가필요합니다.

<a id="layout18-table-1-row-3"></a>

**자료3차**

**조건·자료**

자료3차

**의미와 확인 방법**

512·seed42의3장입력, Block512·32/Blurσ0·2/조합4의8조건입니다. Privacy Score=((1−SSIM)/2)×100이며PSNR은별도참고값입니다. long·방법요약·조합pivot·best_conditions의4CSV가있습니다. 항등조건0, Block32와B32_S0의35.3667978…은3장계산확인값입니다.

<a id="layout18-table-1-row-4"></a>

**자료4차**

**조건·자료**

자료4차

**의미와 확인 방법**

자료차수/4차/코드의학습·MS-SSIM·도표코드를19쪽원고와연결합니다. pareto_scatter.ipynb는0바이트로실행내용이없습니다. 소규모SSIM표와원고1,097장MS-SSIM을섞지않습니다.


<!-- semantic-revision17:level-1:end -->

[이 수준의 프로젝트 전체 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A81.md) · [같은 수준 프로필](https://github.com/PUVKID/PUVKID/blob/main/docs/읽기안내/레벨1.md)

### LEVEL 1 · 목적과 대상

**이 차수의 목적과 실제 구성**

SSIM에서 DSSIM 기반 Privacy Score를 계산하는 경로와 3장·8조건의 저장 결과를 확인하는 자료 차수입니다. 전체 논문의 1,097장 실험과 구분합니다.

<a id="layout18-table-2-row-1"></a>

**점수식**

**구성**

점수식

**실제 역할**

Privacy Score=((1−SSIM)/2)×100을 사용하며 PSNR은 참고값으로 따로 저장합니다.

<a id="layout18-table-2-row-2"></a>

**작은 조건 집합**

**구성**

작은 조건 집합

**실제 역할**

블록 512·32, 블러σ0·2와 네 조합을 사용합니다.

<a id="layout18-table-2-row-3"></a>

**집계**

**구성**

집계

**실제 역할**

long·방법별 요약·조합 pivot·best_conditions의 4CSV를 제공합니다.

<a id="layout18-table-2-row-4"></a>

**점검 결과**

**구성**

점검 결과

**실제 역할**

각 조건 n_images=3이며 동일 변환과 항등 조건의 값 대응을 읽습니다.


CT 사진을 흐리게 하거나 블록으로 재배열했을 때 분류 결과와 영상 유사도가 어떻게 달라지는지 살펴봅니다. 입력 사진을 바꾸는 연구와 모델 내부의 첫 합성곱 특징을 흐리는 실험이 함께 있습니다. **논문 연구 번호·공개 코드 차수·실제 학습 차수는 다릅니다.**

### LEVEL 1 · 달라진 내용과 차수 관계

자료 2차의 실험 노트북 구성 이후 유사도 기반점수 계산과 소규모 결과 읽기를 정리했습니다.

[직전 단계 전체 비교·구성](../revision-diffs/folder-3.diff) · [전체 파일 크기·해시](../revision-manifests/folder-3.json)

사진의 모양이 바뀌었어도 분류기가 정답을 잘 맞추는지, 얼마나 비슷한 정보를 남기는지 따로 봅니다. OK는 양성+정상, NG는 악성입니다. 사진 수·독립 환자 수·반복 학습 표본 수를 섞지 않습니다.

### LEVEL 1 · 입력과 실행 조건

**입력**

3장과 8개 조건

**처리**

원본/변환 SSIM·PSNR 계산

**출력**

조건별 지표


**입력**

SSIM

**처리**

DSSIM×100 변환

**출력**

Privacy Score


**입력**

조건별 값

**처리**

요약·pivot·최대 조건 정리

**출력**

CSV·통합표·도표



**항목**

입력 수

**조건·기본값**

각 조건 3장


**항목**

조건 수

**조건·기본값**

블록 2·블러 2·조합 4


**항목**

크기·시드

**조건·기본값**

512·42


**항목**

지표

**조건·기본값**

SSIM·PSNR·DSSIM 기반점수



입력 사진에 블러·블록을 적용하는 경로와 모델이 뽑은 특징에 블러를 적용하는 경로를 나눕니다. 특징은 사진에서 찾은 선·무늬의 반응입니다. 그 색이 병변 위치나 악성 확률을 뜻하지 않습니다.

### LEVEL 1 · 처리 절차

1. long CSV의 condition·method·n_images·ssim_mean·privacy_score 열을 확인합니다.
2. Block512·σ0 항등 조건과 Block32·조합 B32_S0의 대응을 비교합니다.
3. 방법별 요약과 2×2 pivot이 long표의 같은 조건에서 나온 값인지 읽습니다.
4. 점수식을 최종 논문의 MS-SSIM식과 구별합니다.

전체 차수 표에서 읽을 연구를 고릅니다. 노트북을 여는 것과 새 학습 시작은 다릅니다. 대시보드에서 같은 강도의 사진·곡선·시험 수치를 함께 읽되 미완료 조건은 미측정으로 남깁니다.

### LEVEL 1 · 결과를 확인하는 방법

저장표에서 Block32와 B32+σ0는 같은 점수 35.3667978…이고 항등 조건은 0입니다. 이는 3장 입력에 대한 계산 확인값입니다.

계산 경로를 확인한 소규모 자료이지 임상·공격 저항성 평가나 전체 1,097장 논문 결과를 대신하지 않습니다.

연구 1의 원고 보고 정확도는 원본 92.5%, sigma32 블러 53.3%, Block32 재배열 79.2%입니다. 이는 당시 논문의 값이며 현재 Conv1 예비실험의 결과로 바꾸지 않습니다.

### LEVEL 1 · 주의할 범위

**상황**

표본

**확인할 내용**

3장 결과를 전체 논문 수치로 일반화하지 않습니다.


**상황**

점수식

**확인할 내용**

이 자료는 SSIM이며 최종 MS-SSIM 기반점수와 구분합니다.


**상황**

원영상

**확인할 내용**

의료 원본·비교 이미지 자체는 포함하지 않습니다.



환자 ID가 없어 같은 사람의 다른 사진이 섞였는지 모두 확인할 수 없습니다. 높은 정확도가 임상 성능이나 프라이버시 효과를 보장하지 않습니다. **반복 표본 5,000개를 독립 환자 5,000명으로 세지 않습니다.**

[표·코드·실행 설정·파일 전체 비교를 포함한 공통 상세](#reading-level-5)

<a id="reading-level-2"></a>

## LEVEL 2 - Explorer

<!-- semantic-revision17:level-2:start -->

<a id="semantic-lung-tools-level-2"></a>

### LEVEL 2 · 자료 차수의 수정 도구와 소규모 계산

같은 설정으로 맞추는 비교와 SSIM/PSNR을 맞추는 비교는 목적이 다릅니다. 전자는 학습 조건을 맞추고 후자는 영상 유사도가 비슷한 변환 강도를 찾습니다. 자료 2차는 이 노트북을 생성/수정하며 3차는 작은 입력으로 계산 경로를 점검하고 4차는 원고와 코드를 연결합니다.

<a id="layout18-table-6-row-1"></a>

**자료1차**

**조건·자료**

자료1차

**의미와 확인 방법**

블록·블러각각rebuilt·same_settings·metric_matched의여섯노트북입니다. metric_matched는블록평균SSIM/PSNR에맞는sigma를탐색하며batch4/8·epoch·SWA가변형별로다릅니다. 보조도구는지정노트북을다시씁니다.

<a id="layout18-table-6-row-2"></a>

**자료2차**

**조건·자료**

자료2차

**의미와 확인 방법**

align_experiment_methods.mjs는GPU모니터필드/그래프호환을맞추고build_block_blur_notebook.mjs는Blur사본에서Block→Blur100조합을만듭니다. replaceOrThrow는대상문자열누락시중단하고rollback_original_notebooks.mjs는보관본/지정셀을복원합니다. Node.js와실제입력·출력경로가필요합니다.

<a id="layout18-table-6-row-3"></a>

**자료3차**

**조건·자료**

자료3차

**의미와 확인 방법**

512·seed42의3장입력, Block512·32/Blurσ0·2/조합4의8조건입니다. Privacy Score=((1−SSIM)/2)×100이며PSNR은별도참고값입니다. long·방법요약·조합pivot·best_conditions의4CSV가있습니다. 항등조건0, Block32와B32_S0의35.3667978…은3장계산확인값입니다.

<a id="layout18-table-6-row-4"></a>

**자료4차**

**조건·자료**

자료4차

**의미와 확인 방법**

자료차수/4차/코드의학습·MS-SSIM·도표코드를19쪽원고와연결합니다. pareto_scatter.ipynb는0바이트로실행내용이없습니다. 소규모SSIM표와원고1,097장MS-SSIM을섞지않습니다.


<!-- semantic-revision17:level-2:end -->

[이 수준의 프로젝트 전체 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A82.md) · [같은 수준 프로필](https://github.com/PUVKID/PUVKID/blob/main/docs/읽기안내/레벨2.md)

### LEVEL 2 · 목적과 대상

**이 차수의 목적과 실제 구성**

SSIM에서 DSSIM 기반 Privacy Score를 계산하는 경로와 3장·8조건의 저장 결과를 확인하는 자료 차수입니다. 전체 논문의 1,097장 실험과 구분합니다.

<a id="layout18-table-7-row-1"></a>

**점수식**

**구성**

점수식

**실제 역할**

Privacy Score=((1−SSIM)/2)×100을 사용하며 PSNR은 참고값으로 따로 저장합니다.

<a id="layout18-table-7-row-2"></a>

**작은 조건 집합**

**구성**

작은 조건 집합

**실제 역할**

블록 512·32, 블러σ0·2와 네 조합을 사용합니다.

<a id="layout18-table-7-row-3"></a>

**집계**

**구성**

집계

**실제 역할**

long·방법별 요약·조합 pivot·best_conditions의 4CSV를 제공합니다.

<a id="layout18-table-7-row-4"></a>

**점검 결과**

**구성**

점검 결과

**실제 역할**

각 조건 n_images=3이며 동일 변환과 항등 조건의 값 대응을 읽습니다.


입력 변형 연구 1·2, 특징 블러 Stage 1, Conv1 OK/NG 예비실험을 구분합니다. 블러는 무늬를 부드럽게 하고 블록 재배열은 위치를 섞습니다. 분류 정확도와 유사도 기반 Privacy Score는 서로 다른 양을 측정합니다.

### LEVEL 2 · 달라진 내용과 차수 관계

자료 2차의 실험 노트북 구성 이후 유사도 기반점수 계산과 소규모 결과 읽기를 정리했습니다.

[직전 단계 전체 비교·구성](../revision-diffs/folder-3.diff) · [전체 파일 크기·해시](../revision-manifests/folder-3.json)

이전 연구는 정상·양성·악성 3분류, Conv1은 OK/NG 이진 분류입니다. 원본 1,097장은 양성 120·정상 416·악성 561장입니다. 클래스당 매 epoch 5,000표본은 반복·온라인 증강이며 독립 영상 5,000장이 아닙니다.

### LEVEL 2 · 입력과 실행 조건

**입력**

3장과 8개 조건

**처리**

원본/변환 SSIM·PSNR 계산

**출력**

조건별 지표


**입력**

SSIM

**처리**

DSSIM×100 변환

**출력**

Privacy Score


**입력**

조건별 값

**처리**

요약·pivot·최대 조건 정리

**출력**

CSV·통합표·도표



**항목**

입력 수

**조건·기본값**

각 조건 3장


**항목**

조건 수

**조건·기본값**

블록 2·블러 2·조합 4


**항목**

크기·시드

**조건·기본값**

512·42


**항목**

지표

**조건·기본값**

SSIM·PSNR·DSSIM 기반점수



연구 1은 512×512 입력에 두 변환을 각각 적용해 정확도·ROC-AUC·혼동행렬을 봅니다. 연구 2는 Blur→Block·Block→Blur 조합과 입력 MS-SSIM을 비교합니다. Conv1은 첫 합성곱 특징을 바꾼 뒤 분류합니다.

### LEVEL 2 · 처리 절차

1. long CSV의 condition·method·n_images·ssim_mean·privacy_score 열을 확인합니다.
2. Block512·σ0 항등 조건과 Block32·조합 B32_S0의 대응을 비교합니다.
3. 방법별 요약과 2×2 pivot이 long표의 같은 조건에서 나온 값인지 읽습니다.
4. 점수식을 최종 논문의 MS-SSIM식과 구별합니다.

대표 CT 3범주와 6단계에서 조건별 PNG 18개를 만듭니다. 원본 포함 10조건이 끝나면 180개입니다. 평균·최댓값·개별 8채널의 총 10패널은 특징 반응을 보여 줍니다.

### LEVEL 2 · 결과를 확인하는 방법

저장표에서 Block32와 B32+σ0는 같은 점수 35.3667978…이고 항등 조건은 0입니다. 이는 3장 입력에 대한 계산 확인값입니다.

계산 경로를 확인한 소규모 자료이지 임상·공격 저항성 평가나 전체 1,097장 논문 결과를 대신하지 않습니다.

연구 2는 원본 98.17%, Block256+sigma0 정확도 98.17%·Privacy Score 49.65점을 보고합니다. 유사도 점수는 복원 공격 성공률이 아닙니다. 연구 1과 모델·조건이 달라 차이의 원인을 하나로 확정하지 않습니다.

### LEVEL 2 · 주의할 범위

**상황**

표본

**확인할 내용**

3장 결과를 전체 논문 수치로 일반화하지 않습니다.


**상황**

점수식

**확인할 내용**

이 자료는 SSIM이며 최종 MS-SSIM 기반점수와 구분합니다.


**상황**

원영상

**확인할 내용**

의료 원본·비교 이미지 자체는 포함하지 않습니다.



영상 단위 예비실험의 한계, 조건별 학습·결과 재사용, 입력과 특징의 다른 점수 정의를 함께 읽습니다. 새 종료 정책 실험의 준비와 완료도 구분합니다.

[표·코드·실행 설정·파일 전체 비교를 포함한 공통 상세](#reading-level-5)

<a id="reading-level-3"></a>

## LEVEL 3 - Practitioner

<!-- semantic-revision17:level-3:start -->

<a id="semantic-lung-tools-level-3"></a>

### LEVEL 3 · 자료 차수의 수정 도구와 소규모 계산

수정 도구를 쓰기 전 원본 사본·실제 경로·셀 번호·치환 문자열을 확인하세요. 3차에서는 long의 condition·method·n_images·ssim_mean·privacy_score를 방법 요약/pivot과 대조합니다. 4차에서는 학습 결과 JSON/CSV를 읽는 그림 코드와 의료 원영상을 읽는 유사도 코드를 구분하고 빈 노트북을 실행 입력으로 쓰지 않습니다.

<a id="layout18-table-11-row-1"></a>

**자료1차**

**조건·자료**

자료1차

**의미와 확인 방법**

블록·블러각각rebuilt·same_settings·metric_matched의여섯노트북입니다. metric_matched는블록평균SSIM/PSNR에맞는sigma를탐색하며batch4/8·epoch·SWA가변형별로다릅니다. 보조도구는지정노트북을다시씁니다.

<a id="layout18-table-11-row-2"></a>

**자료2차**

**조건·자료**

자료2차

**의미와 확인 방법**

align_experiment_methods.mjs는GPU모니터필드/그래프호환을맞추고build_block_blur_notebook.mjs는Blur사본에서Block→Blur100조합을만듭니다. replaceOrThrow는대상문자열누락시중단하고rollback_original_notebooks.mjs는보관본/지정셀을복원합니다. Node.js와실제입력·출력경로가필요합니다.

<a id="layout18-table-11-row-3"></a>

**자료3차**

**조건·자료**

자료3차

**의미와 확인 방법**

512·seed42의3장입력, Block512·32/Blurσ0·2/조합4의8조건입니다. Privacy Score=((1−SSIM)/2)×100이며PSNR은별도참고값입니다. long·방법요약·조합pivot·best_conditions의4CSV가있습니다. 항등조건0, Block32와B32_S0의35.3667978…은3장계산확인값입니다.

<a id="layout18-table-11-row-4"></a>

**자료4차**

**조건·자료**

자료4차

**의미와 확인 방법**

자료차수/4차/코드의학습·MS-SSIM·도표코드를19쪽원고와연결합니다. pareto_scatter.ipynb는0바이트로실행내용이없습니다. 소규모SSIM표와원고1,097장MS-SSIM을섞지않습니다.


<!-- semantic-revision17:level-3:end -->

[이 수준의 프로젝트 전체 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A83.md) · [같은 수준 프로필](https://github.com/PUVKID/PUVKID/blob/main/docs/읽기안내/레벨3.md)

### LEVEL 3 · 목적과 대상

**이 차수의 목적과 실제 구성**

SSIM에서 DSSIM 기반 Privacy Score를 계산하는 경로와 3장·8조건의 저장 결과를 확인하는 자료 차수입니다. 전체 논문의 1,097장 실험과 구분합니다.

<a id="layout18-table-12-row-1"></a>

**점수식**

**구성**

점수식

**실제 역할**

Privacy Score=((1−SSIM)/2)×100을 사용하며 PSNR은 참고값으로 따로 저장합니다.

<a id="layout18-table-12-row-2"></a>

**작은 조건 집합**

**구성**

작은 조건 집합

**실제 역할**

블록 512·32, 블러σ0·2와 네 조합을 사용합니다.

<a id="layout18-table-12-row-3"></a>

**집계**

**구성**

집계

**실제 역할**

long·방법별 요약·조합 pivot·best_conditions의 4CSV를 제공합니다.

<a id="layout18-table-12-row-4"></a>

**점검 결과**

**구성**

점검 결과

**실제 역할**

각 조건 n_images=3이며 동일 변환과 항등 조건의 값 대응을 읽습니다.


원고·노트북·저장 결과·대시보드를 차수별로 읽습니다. 과거 논문의 보고값과 현재 Conv1 실행 결과를 합치지 않습니다. 재현에는 원영상·분할·설정·결과 계보가 필요하며 의료 원자료는 공개하지 않습니다.

### LEVEL 3 · 달라진 내용과 차수 관계

자료 2차의 실험 노트북 구성 이후 유사도 기반점수 계산과 소규모 결과 읽기를 정리했습니다.

[직전 단계 전체 비교·구성](../revision-diffs/folder-3.diff) · [전체 파일 크기·해시](../revision-manifests/folder-3.json)

라벨 매핑과 원본 분할을 먼저 확인합니다. 증강은 학습에만 적용하고 검증·시험 원본과 구분합니다. source_class는 원본 범주 폴더 라벨이며 환자·병원·스캐너 식별자가 아닙니다.

### LEVEL 3 · 입력과 실행 조건

**입력**

3장과 8개 조건

**처리**

원본/변환 SSIM·PSNR 계산

**출력**

조건별 지표


**입력**

SSIM

**처리**

DSSIM×100 변환

**출력**

Privacy Score


**입력**

조건별 값

**처리**

요약·pivot·최대 조건 정리

**출력**

CSV·통합표·도표



**항목**

입력 수

**조건·기본값**

각 조건 3장


**항목**

조건 수

**조건·기본값**

블록 2·블러 2·조합 4


**항목**

크기·시드

**조건·기본값**

512·42


**항목**

지표

**조건·기본값**

SSIM·PSNR·DSSIM 기반점수



입력·변환 순서·분할·초기값·학습 예산을 차수별로 확인합니다. Stage 1의 pool1_pool 특징 SSIM은 입력 MS-SSIM과 직접 비교하지 않습니다. 원본 test 선분리와 학습 증강, 큰 sigma 결과 재사용도 확인합니다.

### LEVEL 3 · 처리 절차

1. long CSV의 condition·method·n_images·ssim_mean·privacy_score 열을 확인합니다.
2. Block512·σ0 항등 조건과 Block32·조합 B32_S0의 대응을 비교합니다.
3. 방법별 요약과 2×2 pivot이 long표의 같은 조건에서 나온 값인지 읽습니다.
4. 점수식을 최종 논문의 MS-SSIM식과 구별합니다.

실제 완료한 최적 체크포인트와 실행 ID가 같은 결과만 조회합니다. 색은 패널별 최솟값·최댓값으로 표시하므로 다른 패널의 같은 색을 같은 값으로 보지 않습니다. 과거 PNG나 직전 시험 수치를 대기에 재사용하지 않습니다.

### LEVEL 3 · 결과를 확인하는 방법

저장표에서 Block32와 B32+σ0는 같은 점수 35.3667978…이고 항등 조건은 0입니다. 이는 3장 입력에 대한 계산 확인값입니다.

계산 경로를 확인한 소규모 자료이지 임상·공격 저항성 평가나 전체 1,097장 논문 결과를 대신하지 않습니다.

현재 백분율 요약은 소수 첫째 자리 반올림이며 원비율·전체 백분율·정답 수를 함께 확인합니다. 과거 공개 4차의 둘째 자리 버림 설명은 당시 이력으로 두고 현재 규칙과 섞지 않습니다.

### LEVEL 3 · 주의할 범위

**상황**

표본

**확인할 내용**

3장 결과를 전체 논문 수치로 일반화하지 않습니다.


**상황**

점수식

**확인할 내용**

이 자료는 SSIM이며 최종 MS-SSIM 기반점수와 구분합니다.


**상황**

원영상

**확인할 내용**

의료 원본·비교 이미지 자체는 포함하지 않습니다.



원본과 분할 manifest의 실제 값은 자신의 로컬 자료로 준비해야 합니다. 공개 예제만으로 기준 비교가 동작하지 않습니다. 미완료 조건과 정의 불가 지표를 보기 좋은 값으로 채우지 않습니다.

[표·코드·실행 설정·파일 전체 비교를 포함한 공통 상세](#reading-level-5)

<a id="reading-level-4"></a>

## LEVEL 4 - Advanced

<!-- semantic-revision17:level-4:start -->

<a id="semantic-lung-tools-level-4"></a>

### LEVEL 4 · 자료 차수의 수정 도구와 소규모 계산

파일 변경 보조 도구의 JSON/문자열 계약과 실제 학습 코드를 분리합니다. 보정용 영상과 시험 자료의 관계, 치환 실패 시 중단, 복원 대상과 출력 충돌을 확인해야 합니다. 소규모 단일 SSIM 계산과 최종 MS-SSIM 집계는 별도 정의이므로 이름이 같은 Privacy Score를 통합하지 않습니다.

<a id="layout18-table-16-row-1"></a>

**자료1차**

**조건·자료**

자료1차

**의미와 확인 방법**

블록·블러각각rebuilt·same_settings·metric_matched의여섯노트북입니다. metric_matched는블록평균SSIM/PSNR에맞는sigma를탐색하며batch4/8·epoch·SWA가변형별로다릅니다. 보조도구는지정노트북을다시씁니다.

<a id="layout18-table-16-row-2"></a>

**자료2차**

**조건·자료**

자료2차

**의미와 확인 방법**

align_experiment_methods.mjs는GPU모니터필드/그래프호환을맞추고build_block_blur_notebook.mjs는Blur사본에서Block→Blur100조합을만듭니다. replaceOrThrow는대상문자열누락시중단하고rollback_original_notebooks.mjs는보관본/지정셀을복원합니다. Node.js와실제입력·출력경로가필요합니다.

<a id="layout18-table-16-row-3"></a>

**자료3차**

**조건·자료**

자료3차

**의미와 확인 방법**

512·seed42의3장입력, Block512·32/Blurσ0·2/조합4의8조건입니다. Privacy Score=((1−SSIM)/2)×100이며PSNR은별도참고값입니다. long·방법요약·조합pivot·best_conditions의4CSV가있습니다. 항등조건0, Block32와B32_S0의35.3667978…은3장계산확인값입니다.

<a id="layout18-table-16-row-4"></a>

**자료4차**

**조건·자료**

자료4차

**의미와 확인 방법**

자료차수/4차/코드의학습·MS-SSIM·도표코드를19쪽원고와연결합니다. pareto_scatter.ipynb는0바이트로실행내용이없습니다. 소규모SSIM표와원고1,097장MS-SSIM을섞지않습니다.


<!-- semantic-revision17:level-4:end -->

[이 수준의 프로젝트 전체 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A84.md) · [같은 수준 프로필](https://github.com/PUVKID/PUVKID/blob/main/docs/읽기안내/레벨4.md)

### LEVEL 4 · 목적과 대상

**이 차수의 목적과 실제 구성**

SSIM에서 DSSIM 기반 Privacy Score를 계산하는 경로와 3장·8조건의 저장 결과를 확인하는 자료 차수입니다. 전체 논문의 1,097장 실험과 구분합니다.

<a id="layout18-table-17-row-1"></a>

**점수식**

**구성**

점수식

**실제 역할**

Privacy Score=((1−SSIM)/2)×100을 사용하며 PSNR은 참고값으로 따로 저장합니다.

<a id="layout18-table-17-row-2"></a>

**작은 조건 집합**

**구성**

작은 조건 집합

**실제 역할**

블록 512·32, 블러σ0·2와 네 조합을 사용합니다.

<a id="layout18-table-17-row-3"></a>

**집계**

**구성**

집계

**실제 역할**

long·방법별 요약·조합 pivot·best_conditions의 4CSV를 제공합니다.

<a id="layout18-table-17-row-4"></a>

**점검 결과**

**구성**

점검 결과

**실제 역할**

각 조건 n_images=3이며 동일 변환과 항등 조건의 값 대응을 읽습니다.


입력 변형과 pool1_pool 특징 변형은 개입 위치가 다릅니다. 모델·학습·라벨·분할·점수 정의가 달라 단순 수치 차이를 모델 변경의 인과 효과로 설명할 수 없습니다. 종료 정책 비교도 별도 설계입니다.

### LEVEL 4 · 달라진 내용과 차수 관계

자료 2차의 실험 노트북 구성 이후 유사도 기반점수 계산과 소규모 결과 읽기를 정리했습니다.

[직전 단계 전체 비교·구성](../revision-diffs/folder-3.diff) · [전체 파일 크기·해시](../revision-manifests/folder-3.json)

환자 ID 없는 영상 그룹 분할은 환자 독립 분할의 대체가 아닙니다. 소스별 촬영·압축 차이와 같은 환자의 다른 영상이 성능에 영향을 줄 수 있습니다. 높은 정확도의 원인을 조기 종료로 미리 확정하지 않습니다.

### LEVEL 4 · 입력과 실행 조건

**입력**

3장과 8개 조건

**처리**

원본/변환 SSIM·PSNR 계산

**출력**

조건별 지표


**입력**

SSIM

**처리**

DSSIM×100 변환

**출력**

Privacy Score


**입력**

조건별 값

**처리**

요약·pivot·최대 조건 정리

**출력**

CSV·통합표·도표



**항목**

입력 수

**조건·기본값**

각 조건 3장


**항목**

조건 수

**조건·기본값**

블록 2·블러 2·조합 4


**항목**

크기·시드

**조건·기본값**

512·42


**항목**

지표

**조건·기본값**

SSIM·PSNR·DSSIM 기반점수



Stage 1은 같은 프로세스의 Edge·Cloud 연결이며 실제 원격 전송이 아닙니다. 큰 sigma의 전역 평균 대체, sigma32 결과의 64/128/256 재사용과 Conv2D import 누락 같은 실행 제약을 구분합니다.

### LEVEL 4 · 처리 절차

1. long CSV의 condition·method·n_images·ssim_mean·privacy_score 열을 확인합니다.
2. Block512·σ0 항등 조건과 Block32·조합 B32_S0의 대응을 비교합니다.
3. 방법별 요약과 2×2 pivot이 long표의 같은 조건에서 나온 값인지 읽습니다.
4. 점수식을 최종 논문의 MS-SSIM식과 구별합니다.

공개 4차는 학습 2차 대시보드의 로컬 수리 3차 사본입니다. 공개 5차는 실험 4차 고정 100회 비교 코드입니다. 원본 manifest·해시·정확 분할이 다르면 중단합니다.

### LEVEL 4 · 결과를 확인하는 방법

저장표에서 Block32와 B32+σ0는 같은 점수 35.3667978…이고 항등 조건은 0입니다. 이는 3장 입력에 대한 계산 확인값입니다.

계산 경로를 확인한 소규모 자료이지 임상·공격 저항성 평가나 전체 1,097장 논문 결과를 대신하지 않습니다.

Blur sigma256의 51.38%는 다수 클래스 56/109와 같지만 모든 조건의 하한은 아닙니다. 별도 학습한 Block512+sigma256은 46.8%입니다. 조합·단독·별도 학습·시험 분모를 나누어 읽습니다.

### LEVEL 4 · 주의할 범위

**상황**

표본

**확인할 내용**

3장 결과를 전체 논문 수치로 일반화하지 않습니다.


**상황**

점수식

**확인할 내용**

이 자료는 SSIM이며 최종 MS-SSIM 기반점수와 구분합니다.


**상황**

원영상

**확인할 내용**

의료 원본·비교 이미지 자체는 포함하지 않습니다.



기존 분할·시험셋 재사용과 환자 ID 부재는 독립 임상 평가를 제한합니다. 높은 정확도의 원인을 조기 종료로 확정하지 않고 동일 조건 정책 비교를 합니다. 두 비교 모델은 같은 학습 경로에서 선택됩니다.

[표·코드·실행 설정·파일 전체 비교를 포함한 공통 상세](#reading-level-5)

<a id="reading-level-5"></a>

## LEVEL 5 - Expert

<!-- semantic-revision17:level-5:start -->

<a id="semantic-lung-tools-level-5"></a>

### LEVEL 5 · 자료 차수의 수정 도구와 소규모 계산

자료 1~4차의 수락 범위는 변형 코드·변경 도구·3장 8조건 점검·최종 원고 대응입니다. 35.3667978…은 저장표의 축약 표기이며 원정밀도 CSV를 유지합니다. SSIM 매칭은 분류 성능 동등성이나 공격 저항성 동등성을 증명하지 않고 0바이트 파일에서 분석 성과를 추정하지 않습니다.

<a id="layout18-table-21-row-1"></a>

**자료1차**

**조건·자료**

자료1차

**의미와 확인 방법**

블록·블러각각rebuilt·same_settings·metric_matched의여섯노트북입니다. metric_matched는블록평균SSIM/PSNR에맞는sigma를탐색하며batch4/8·epoch·SWA가변형별로다릅니다. 보조도구는지정노트북을다시씁니다.

<a id="layout18-table-21-row-2"></a>

**자료2차**

**조건·자료**

자료2차

**의미와 확인 방법**

align_experiment_methods.mjs는GPU모니터필드/그래프호환을맞추고build_block_blur_notebook.mjs는Blur사본에서Block→Blur100조합을만듭니다. replaceOrThrow는대상문자열누락시중단하고rollback_original_notebooks.mjs는보관본/지정셀을복원합니다. Node.js와실제입력·출력경로가필요합니다.

<a id="layout18-table-21-row-3"></a>

**자료3차**

**조건·자료**

자료3차

**의미와 확인 방법**

512·seed42의3장입력, Block512·32/Blurσ0·2/조합4의8조건입니다. Privacy Score=((1−SSIM)/2)×100이며PSNR은별도참고값입니다. long·방법요약·조합pivot·best_conditions의4CSV가있습니다. 항등조건0, Block32와B32_S0의35.3667978…은3장계산확인값입니다.

<a id="layout18-table-21-row-4"></a>

**자료4차**

**조건·자료**

자료4차

**의미와 확인 방법**

자료차수/4차/코드의학습·MS-SSIM·도표코드를19쪽원고와연결합니다. pareto_scatter.ipynb는0바이트로실행내용이없습니다. 소규모SSIM표와원고1,097장MS-SSIM을섞지않습니다.


<!-- semantic-revision17:level-5:end -->

[전문가 수준 프로젝트 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A85.md) · [같은 수준 프로필](https://github.com/PUVKID/PUVKID/blob/main/docs/읽기안내/레벨5.md)

**기존 전체 상세** — 다음 본문은 이 차수의 원래 방법·조건·결과·실패·한계와 전체 비교입니다. 위 수준의 설명에 필요한 공통 근거도 모두 여기서 확인할 수 있습니다.
<!-- reading-levels17:end -->

**SSIM에서 DSSIM 기반 Privacy Score를 계산하는 경로와 3장·8조건의 저장 결과를 확인하는 자료 차수입니다.** 전체 논문의 1,097장 실험과 구분합니다.

분야: 영상 지표 › SSIM·DSSIM › 소규모 계산·표·그래프

[목적](#purpose) · [기능](#features) · [입출력](#flow) · [구성](#files) · [준비](#setup) · [사용법](#usage) · [결과](#results) · [제약](#limits) · [변경](#changes)

<a name="purpose"></a>

<a id="-이-단계에서-하는-일"></a>

## 연구 목적

블록 2조건·블러 2조건·조합 4조건을 대상으로 계산한 CSV·통합표·비의료 도표를 읽습니다. 의료 원영상의 비교 그림은 첨부하지 않습니다.

<a name="features"></a>

<a id="-주요-기능과-처리-방식"></a>

## 방법과 구현

<a id="layout18-table-22-row-1"></a>

**점수식**

**구성**

점수식

**실제 역할**

Privacy Score=((1−SSIM)/2)×100을 사용하며 PSNR은 참고값으로 따로 저장합니다.

<a id="layout18-table-22-row-2"></a>

**작은 조건 집합**

**구성**

작은 조건 집합

**실제 역할**

블록 512·32, 블러σ0·2와 네 조합을 사용합니다.

<a id="layout18-table-22-row-3"></a>

**집계**

**구성**

집계

**실제 역할**

long·방법별 요약·조합 pivot·best_conditions의 4CSV를 제공합니다.

<a id="layout18-table-22-row-4"></a>

**점검 결과**

**구성**

점검 결과

**실제 역할**

각 조건 n_images=3이며 동일 변환과 항등 조건의 값 대응을 읽습니다.


<a name="flow"></a>

<a id="-입력--처리--출력"></a>

## 입력·처리·출력

**입력**

3장과 8개 조건

**처리**

원본/변환 SSIM·PSNR 계산

**출력**

조건별 지표


**입력**

SSIM

**처리**

DSSIM×100 변환

**출력**

Privacy Score


**입력**

조건별 값

**처리**

요약·pivot·최대 조건 정리

**출력**

CSV·통합표·도표



<a name="files"></a>

<a id="-파일과-핵심-처리"></a>

## 파일별 역할

<a id="layout18-table-24-row-1"></a>

**[자료차수/3차/_smoke_privacy_score.ipynb](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/_smoke_privacy_score.ipynb)**

**파일**

[자료차수/3차/_smoke_privacy_score.ipynb](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/_smoke_privacy_score.ipynb)

**이용 방법**

설정·함수·실행 셀

<a id="layout18-table-24-row-2"></a>

**[자료차수/3차/tables/privacy_scores_long.csv](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/tables/privacy_scores_long.csv)**

**파일**

[자료차수/3차/tables/privacy_scores_long.csv](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/tables/privacy_scores_long.csv)

**이용 방법**

원정밀도 표

<a id="layout18-table-24-row-3"></a>

**항목 3**

**파일**

[자료차수/3차/tables/privacy_scores_summary_by_method.csv](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/tables/privacy_scores_summary_by_method.csv)

**이용 방법**

원정밀도 표

<a id="layout18-table-24-row-4"></a>

**[자료차수/3차/tables/privacy_scores_combo_pivot.csv](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/tables/privacy_scores_combo_pivot.csv)**

**파일**

[자료차수/3차/tables/privacy_scores_combo_pivot.csv](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/tables/privacy_scores_combo_pivot.csv)

**이용 방법**

원정밀도 표

<a id="layout18-table-24-row-5"></a>

**항목 5**

**파일**

[자료차수/3차/tables/privacy_scores_best_conditions.csv](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/tables/privacy_scores_best_conditions.csv)

**이용 방법**

원정밀도 표


<a id="-함수셀로-찾아가기"></a>

### 관련 함수와 셀

관련 함수와 셀을 파일별로 정리했습니다. 실행 전 설정과 호출 순서, 출력 경로를 확인하세요.

<a id="layout18-table-25-row-1"></a>

**[자료차수/3차/_smoke_privacy_score.ipynb](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/_smoke_privacy_score.ipynb)**

**파일**

[자료차수/3차/_smoke_privacy_score.ipynb](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/_smoke_privacy_score.ipynb)

**핵심 정의**

셀 6: `path_exists` · `candidate_train_dirs` · `should_ignore` · `count_images_under`<br>셀 8: `collect_image_table`<br>셀 10: `setup_matplotlib_font` · `load_rgb_image` · `block_scramble` · `apply_gaussian_blur` · `apply_transform`<br>셀 12: `compute_pair_metrics` · `load_image_records` · `iter_records` · `evaluate_condition` · `condition_name` · `format_sigma`<br>셀 18: `save_fig`<br>셀 20: `save_table_png`<br>셀 22: `parse_condition`


<a name="setup"></a>

<a id="️-환경과-설정"></a>

## 실행 환경과 설정

**항목**

입력 수

**조건·기본값**

각 조건 3장


**항목**

조건 수

**조건·기본값**

블록 2·블러 2·조합 4


**항목**

크기·시드

**조건·기본값**

512·42


**항목**

지표

**조건·기본값**

SSIM·PSNR·DSSIM 기반점수



<a name="usage"></a>

<a id="-준비와-사용-순서"></a>

## 실행 순서

1. long CSV의 condition·method·n_images·ssim_mean·privacy_score 열을 확인합니다.
2. Block512·σ0 항등 조건과 Block32·조합 B32_S0의 대응을 비교합니다.
3. 방법별 요약과 2×2 pivot이 long표의 같은 조건에서 나온 값인지 읽습니다.
4. 점수식을 최종 논문의 MS-SSIM식과 구별합니다.

<a name="results"></a>

<a id="-결과를-읽는-방법"></a>

## 결과와 해석

저장표에서 Block32와 B32+σ0는 같은 점수 35.3667978…이고 항등 조건은 0입니다. 이는 3장 입력에 대한 계산 확인값입니다.

계산 경로를 확인한 소규모 자료이지 임상·공격 저항성 평가나 전체 1,097장 논문 결과를 대신하지 않습니다.

<a name="limits"></a>

<a id="️-알려진-제약과-확인-지점"></a>

## 제약과 확인 사항

**상황**

표본

**확인할 내용**

3장 결과를 전체 논문 수치로 일반화하지 않습니다.


**상황**

점수식

**확인할 내용**

이 자료는 SSIM이며 최종 MS-SSIM 기반점수와 구분합니다.


**상황**

원영상

**확인할 내용**

의료 원본·비교 이미지 자체는 포함하지 않습니다.



<a name="changes"></a>

<a id="-이전-단계와의-변화"></a>

## 직전 단계와 비교

자료 2차의 실험 노트북 구성 이후 유사도 기반점수 계산과 소규모 결과 읽기를 정리했습니다.

[직전 단계 전체 비교·구성](../revision-diffs/folder-3.diff) · [전체 파일 크기·해시](../revision-manifests/folder-3.json)

<details>
<summary>이 단계의 파일 기록과 전체 해시</summary>

아래 내용는 해당 단계가 기록될 당시의 파일 정보입니다. 현재 첨부는 [프로젝트 자료 안내](../PAPERS.md)에서 확인할 수 있습니다.

<a id="layout18-table-28-row-1"></a>

**항목 1**

**파일**

[자료차수/3차/tables/privacy_scores_best_conditions.csv](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/tables/privacy_scores_best_conditions.csv)

**종류**

.csv

**바이트**

858

**SHA-256**

`f8e160d380f0c0f41f33a8913e7739c7fe9a9f2e42081e77c16c302f5de9a529`

<a id="layout18-table-28-row-2"></a>

**[자료차수/3차/tables/privacy_scores_combo_pivot.csv](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/tables/privacy_scores_combo_pivot.csv)**

**파일**

[자료차수/3차/tables/privacy_scores_combo_pivot.csv](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/tables/privacy_scores_combo_pivot.csv)

**종류**

.csv

**바이트**

92

**SHA-256**

`7a31a1ae5238c3369ad5461b7806948a61eda358dae86dc87b177181df11b034`

<a id="layout18-table-28-row-3"></a>

**[자료차수/3차/tables/privacy_scores_long.csv](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/tables/privacy_scores_long.csv)**

**파일**

[자료차수/3차/tables/privacy_scores_long.csv](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/tables/privacy_scores_long.csv)

**종류**

.csv

**바이트**

1507

**SHA-256**

`edcecf8fe6c892b0640ffe9d7d7341c9ee094ab4624cfb5d65a3d52974caff22`

<a id="layout18-table-28-row-4"></a>

**항목 4**

**파일**

[자료차수/3차/tables/privacy_scores_summary_by_method.csv](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/tables/privacy_scores_summary_by_method.csv)

**종류**

.csv

**바이트**

362

**SHA-256**

`403ff42da2b5a21428304bb456346178734658976dfff5a0c6abb8092782d060`

<a id="layout18-table-28-row-5"></a>

**[자료차수/3차/graphs/01_block_privacy_score.png](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/graphs/01_block_privacy_score.png)**

**파일**

[자료차수/3차/graphs/01_block_privacy_score.png](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/graphs/01_block_privacy_score.png)

**종류**

.png

**바이트**

70066

**SHA-256**

`2d3be7ac20d49f2e91cf4f3039fbbc8a4fd979e65025d456eb14802955783287`

<a id="layout18-table-28-row-6"></a>

**[자료차수/3차/graphs/02_blur_privacy_score.png](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/graphs/02_blur_privacy_score.png)**

**파일**

[자료차수/3차/graphs/02_blur_privacy_score.png](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/graphs/02_blur_privacy_score.png)

**종류**

.png

**바이트**

63552

**SHA-256**

`056c40e03053b9d7694877333ceb1a2019fb5080e3714355b5a0ef03c114be19`

<a id="layout18-table-28-row-7"></a>

**항목 7**

**파일**

[자료차수/3차/graphs/03_combo_privacy_score_heatmap.png](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/graphs/03_combo_privacy_score_heatmap.png)

**종류**

.png

**바이트**

42052

**SHA-256**

`6d3cc49c6d9acf6a977922e59ac140c1d3f7c181b23595f4514ad3404fae59fa`

<a id="layout18-table-28-row-8"></a>

**항목 8**

**파일**

[자료차수/3차/graphs/04_block_ssim_psnr_reference.png](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/graphs/04_block_ssim_psnr_reference.png)

**종류**

.png

**바이트**

64195

**SHA-256**

`f2359a64da2d2a5129dd225fc3cebde956bd414e4d767ebfac9804ea0baa386e`

<a id="layout18-table-28-row-9"></a>

**항목 9**

**파일**

[자료차수/3차/graphs/05_blur_ssim_psnr_reference.png](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/graphs/05_blur_ssim_psnr_reference.png)

**종류**

.png

**바이트**

77351

**SHA-256**

`2aad1e739efc2b01a5e5b6b0acd24cba7b61e9d301fba2bfd7c19ea566435d72`

<a id="layout18-table-28-row-10"></a>

**항목 10**

**파일**

[자료차수/3차/graphs/06_top_conditions_privacy_score.png](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/graphs/06_top_conditions_privacy_score.png)

**종류**

.png

**바이트**

60606

**SHA-256**

`df22b8d68e003e26e65c2c236bd427538882ff750a2e473918284a90d4bef99c`

<a id="layout18-table-28-row-11"></a>

**항목 11**

**파일**

[자료차수/3차/graphs/07_method_distribution_boxplot.png](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/graphs/07_method_distribution_boxplot.png)

**종류**

.png

**바이트**

38584

**SHA-256**

`ceb03b03ff92470e91a9e62b2f1151f1512f7b11bf583dec03dc07d8d2915fee`

<a id="layout18-table-28-row-12"></a>

**[자료차수/3차/graphs/08_top_conditions_table.png](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/graphs/08_top_conditions_table.png)**

**파일**

[자료차수/3차/graphs/08_top_conditions_table.png](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/graphs/08_top_conditions_table.png)

**종류**

.png

**바이트**

80715

**SHA-256**

`d0e4e134df95fda8aa4fbeb0a0c17c9769aac16dc6ebf8c86c0a7765a1450ca8`

<a id="layout18-table-28-row-13"></a>

**[자료차수/3차/graphs/09_best_by_method_table.png](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/graphs/09_best_by_method_table.png)**

**파일**

[자료차수/3차/graphs/09_best_by_method_table.png](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/graphs/09_best_by_method_table.png)

**종류**

.png

**바이트**

45058

**SHA-256**

`9da6f678a12bdf33915130898cc4c2d50d2ab7af13a52f9b7433590c3a0d48f1`

<a id="layout18-table-28-row-14"></a>

**[자료차수/3차/create_privacy_notebook.py](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/create_privacy_notebook.py)**

**파일**

[자료차수/3차/create_privacy_notebook.py](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/create_privacy_notebook.py)

**종류**

.py

**바이트**

28399

**SHA-256**

`3809df9b5f3091f79172f0257c8eb7f2ef828bbf99da99eb41b486bb66108280`

<a id="layout18-table-28-row-15"></a>

**[자료차수/3차/modify_privacy_notebook_ssim_only.py](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/modify_privacy_notebook_ssim_only.py)**

**파일**

[자료차수/3차/modify_privacy_notebook_ssim_only.py](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/modify_privacy_notebook_ssim_only.py)

**종류**

.py

**바이트**

27299

**SHA-256**

`759fd7599e40b5cb25a8e7bc5f248bbb9eff2fd3328932c3c45236521345fc91`

<a id="layout18-table-28-row-16"></a>

**[자료차수/3차/_smoke_privacy_score.ipynb](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/_smoke_privacy_score.ipynb)**

**파일**

[자료차수/3차/_smoke_privacy_score.ipynb](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/_smoke_privacy_score.ipynb)

**종류**

.ipynb

**바이트**

89274

**SHA-256**

`a03f40d6eab19fb5bdd3d4d60c3f308f03c43e80387f8f71dd70624f6311a8e6`

<a id="layout18-table-28-row-17"></a>

**항목 17**

**파일**

[원본자료/3차/privacy_score_outputs/privacy_score_results.xlsx](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/3%EC%B0%A8/privacy_score_outputs/privacy_score_results.xlsx)

**종류**

.xlsx

**바이트**

8330

**SHA-256**

`a90c2676448a700ef65836cd2f3427030c95e4864870268f1bd3d7eda144b4f1`

<a id="layout18-table-28-row-18"></a>

**항목 18**

**파일**

[원본자료/3차/privacy_score_outputs/tables/selected_images.csv](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/3%EC%B0%A8/privacy_score_outputs/tables/selected_images.csv)

**종류**

.csv

**바이트**

406

**SHA-256**

`13a874a2d948b964c171ab3a6927e78882c262a245940933a5285454de846a71`


</details>

---

[프로젝트](../../README.md) · [전체 차수](../REVISION_INDEX.md) · [자료 폴더](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/tables) · [폴더 2차](folder-2.md) · [폴더 4차](folder-4.md)

<!-- language-choice:start -->
🔵 **한국어** · [English overview](../../en/README.md)
<!-- language-choice:end -->

<a id="-자료-3차--privacy-score의-소규모-계산-확인"></a>

# 자료 3차·Privacy Score의 소규모 계산 확인

<!-- reading-levels17:start -->
읽기 수준 · [LEVEL 1](#user-content-reading-level-1) · [LEVEL 2](#user-content-reading-level-2) · [LEVEL 3](#user-content-reading-level-3) · [LEVEL 4](#user-content-reading-level-4) · [LEVEL 5](#user-content-reading-level-5)

<details open>
<summary>LEVEL 1 · Beginner — 목적과 동작부터</summary>

<a id="reading-level-1"></a>

## LEVEL 1 - Beginner

<a id="semantic-lung-tools-level-1"></a>

| 항목 | 이 차수의 내용 |
| --- | --- |
| 목적 | SSIM에서 DSSIM 기반 Privacy Score를 계산하는 경로와 3장·8 조건의 저장 결과를 확인하는 자료 차수입니다.<br>전체 논문의 1,097장 실험과 구분합니다. |
| 변경 | 자료 2차의 실험 노트북 구성 이후 유사도 기반 점수 계산과 소규모 결과 읽기를 정리했습니다. |
| 조건 | **입력 수**: 각 조건 3장<br>**조건 수**: 블록 2·블러 2·조합 4<br>**크기·시드**: 512·42<br>**지표**: SSIM·PSNR·DSSIM 기반점수 |
| 동작 | 1. long CSV 의 condition·method·n_images·ssim_mean·privacy_score 열을 확인합니다. |
| 결과 | 저장 표에서 Block32와 B32 +σ0는 같은 점수 35.3667978… 이 고 항등 조건은 0입니다.<br>이는 3장 입력에 대한 계산 확인 값입니다. |

### LEVEL 1 · 자료 차수의 수정 도구와 소규모 계산

자료 3차·Privacy Score의 소규모 계산 확인의 범위에서 설명합니다. 먼저 이 자료가 무엇을 바꾸고 무엇을 보여 주는지 살펴봅니다. 아래 조건은 이 문서에 연결된 파일의 내용이며 다른 차수의 결과를 함께 센 값이 아닙니다.

| 항목 | 이 차수의 내용 |
| --- | --- |
| <a id="layout18-table-1-row-1"></a> **목적** | 블록 2 조건·블러 2 조건·조합 4 조건을 대상으로 계산한 CSV·통합 표·비의료 도표를 읽습니다. 의료 원영상의 비교 그림은 첨부하지 않습니다. |
| <a id="layout18-table-1-row-2"></a> **구현** | **점수 식**: Privacy Score =((1 −SSIM)/2)×100을 사용하며 PSNR은 참고 값으로 따로 저장합니다.<br>**작은 조건 집합**: 블록 512·32, 블러 σ0·2와 네 조합을 사용합니다.<br>**집계**: long·방법별 요약·조합 pivot·best_conditions의 4CSV를 제공합니다.<br>**점검 결과**: 각 조건 n_images =3이며 동일 변환과 항등 조건의 값 대응을 읽습니다. |
| <a id="layout18-table-1-row-3"></a> **조건** | **입력 수**: 각 조건 3장<br>**조건 수**: 블록 2·블러 2·조합 4<br>**크기·시드**: 512·42<br>**지표**: SSIM·PSNR·DSSIM 기반점수 |
| <a id="layout18-table-1-row-4"></a> **관측과 해석·한계·자료 연결** | 저장 표에서 Block32와 B32 +σ0는 같은 점수 35.3667978… 이 고 항등 조건은 0입니다. 이는 3장 입력에 대한 계산 확인 값입니다.<br>계산 경로를 확인한 소규모 자료이지 임상·공격 저항성 평가나 전체 1,097장 논문 결과를 대신하지 않습니다.<br>**표본**: 3장 결과를 전체 논문 수치로 일반화하지 않습니다.<br>**점수 식**: 이 자료는 SSIM이며 최종 MS-SSIM 기반 점수와 구분합니다.<br>**원영상**: 의료 원본·비교 이미지 자체는 포함하지 않습니다.<br>[이 차수 전체 상세](#purpose) · [실행 순서](#usage) · [결과와 해석](#results) · [프로젝트 공통 안내](../../README.md)<br>다른 자료 차수의 구현·관측은 [자료 1차](folder-1.md#user-content-reading-level-1) · [자료 2차](folder-2.md#user-content-reading-level-1) · [자료 4차](folder-4.md#user-content-reading-level-1)에서 별도로 확인합니다. |


[동일 수준 프로젝트 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A81.md)


</details>

<details>
<summary>LEVEL 2 · Explorer — 구성과 연결 원리</summary>

<a id="reading-level-2"></a>

## LEVEL 2 - Explorer

<a id="semantic-lung-tools-level-2"></a>

| 항목 | 이 차수의 내용 |
| --- | --- |
| 목적 | SSIM에서 DSSIM 기반 Privacy Score를 계산하는 경로와 3장·8 조건의 저장 결과를 확인하는 자료 차수입니다.<br>전체 논문의 1,097장 실험과 구분합니다. |
| 변경 | 자료 2차의 실험 노트북 구성 이후 유사도 기반 점수 계산과 소규모 결과 읽기를 정리했습니다. |
| 조건 | **입력 수**: 각 조건 3장<br>**조건 수**: 블록 2·블러 2·조합 4<br>**크기·시드**: 512·42<br>**지표**: SSIM·PSNR·DSSIM 기반점수 |
| 동작 | 1. long CSV 의 condition·method·n_images·ssim_mean·privacy_score 열을 확인합니다. |
| 결과 | 저장 표에서 Block32와 B32 +σ0는 같은 점수 35.3667978… 이 고 항등 조건은 0입니다.<br>이는 3장 입력에 대한 계산 확인 값입니다. |

### LEVEL 2 · 자료 차수의 수정 도구와 소규모 계산

자료 3차·Privacy Score의 소규모 계산 확인의 범위에서 설명합니다. 입력 → 처리 → 출력의 순서로 읽습니다. 설정을 준비한 것과 실제 실행에서 얻은 결과를 구분하고, 관측값은 같은 입력·설정의 기록과 연결합니다.

| 항목 | 이 차수의 내용 |
| --- | --- |
| <a id="layout18-table-6-row-1"></a> **목적** | 블록 2 조건·블러 2 조건·조합 4 조건을 대상으로 계산한 CSV·통합 표·비의료 도표를 읽습니다. 의료 원영상의 비교 그림은 첨부하지 않습니다. |
| <a id="layout18-table-6-row-2"></a> **구현** | **점수 식**: Privacy Score =((1 −SSIM)/2)×100을 사용하며 PSNR은 참고 값으로 따로 저장합니다.<br>**작은 조건 집합**: 블록 512·32, 블러 σ0·2와 네 조합을 사용합니다.<br>**집계**: long·방법별 요약·조합 pivot·best_conditions의 4CSV를 제공합니다.<br>**점검 결과**: 각 조건 n_images =3이며 동일 변환과 항등 조건의 값 대응을 읽습니다. |
| <a id="layout18-table-6-row-3"></a> **조건** | **입력 수**: 각 조건 3장<br>**조건 수**: 블록 2·블러 2·조합 4<br>**크기·시드**: 512·42<br>**지표**: SSIM·PSNR·DSSIM 기반점수 |
| <a id="layout18-table-6-row-4"></a> **관측과 해석·한계·자료 연결** | 저장 표에서 Block32와 B32 +σ0는 같은 점수 35.3667978… 이 고 항등 조건은 0입니다. 이는 3장 입력에 대한 계산 확인 값입니다.<br>계산 경로를 확인한 소규모 자료이지 임상·공격 저항성 평가나 전체 1,097장 논문 결과를 대신하지 않습니다.<br>**표본**: 3장 결과를 전체 논문 수치로 일반화하지 않습니다.<br>**점수 식**: 이 자료는 SSIM이며 최종 MS-SSIM 기반 점수와 구분합니다.<br>**원영상**: 의료 원본·비교 이미지 자체는 포함하지 않습니다.<br>[이 차수 전체 상세](#purpose) · [실행 순서](#usage) · [결과와 해석](#results) · [프로젝트 공통 안내](../../README.md)<br>다른 자료 차수의 구현·관측은 [자료 1차](folder-1.md#user-content-reading-level-2) · [자료 2차](folder-2.md#user-content-reading-level-2) · [자료 4차](folder-4.md#user-content-reading-level-2)에서 별도로 확인합니다. |


[동일 수준 프로젝트 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A82.md)


</details>

<details>
<summary>LEVEL 3 · Practitioner — 준비·실행·결과 확인</summary>

<a id="reading-level-3"></a>

## LEVEL 3 - Practitioner

<a id="semantic-lung-tools-level-3"></a>

| 항목 | 이 차수의 내용 |
| --- | --- |
| 목적 | SSIM에서 DSSIM 기반 Privacy Score를 계산하는 경로와 3장·8 조건의 저장 결과를 확인하는 자료 차수입니다.<br>전체 논문의 1,097장 실험과 구분합니다. |
| 변경 | 자료 2차의 실험 노트북 구성 이후 유사도 기반 점수 계산과 소규모 결과 읽기를 정리했습니다. |
| 조건 | **입력 수**: 각 조건 3장<br>**조건 수**: 블록 2·블러 2·조합 4<br>**크기·시드**: 512·42<br>**지표**: SSIM·PSNR·DSSIM 기반점수 |
| 동작 | 1. long CSV 의 condition·method·n_images·ssim_mean·privacy_score 열을 확인합니다. |
| 결과 | 저장 표에서 Block32와 B32 +σ0는 같은 점수 35.3667978… 이 고 항등 조건은 0입니다.<br>이는 3장 입력에 대한 계산 확인 값입니다. |

### LEVEL 3 · 자료 차수의 수정 도구와 소규모 계산

자료 3차·Privacy Score의 소규모 계산 확인의 범위에서 설명합니다. 실행할 파일을 먼저 고르고 아래 전체 상세의 경로·설정·호출 순서를 확인합니다. 표의 구성과 조건을 해당 파일에 맞춰 읽으며 문서 정리 자체가 새 실행을 뜻하지는 않습니다.

| 항목 | 이 차수의 내용 |
| --- | --- |
| <a id="layout18-table-11-row-1"></a> **목적** | 블록 2 조건·블러 2 조건·조합 4 조건을 대상으로 계산한 CSV·통합 표·비의료 도표를 읽습니다. 의료 원영상의 비교 그림은 첨부하지 않습니다. |
| <a id="layout18-table-11-row-2"></a> **구현** | **점수 식**: Privacy Score =((1 −SSIM)/2)×100을 사용하며 PSNR은 참고 값으로 따로 저장합니다.<br>**작은 조건 집합**: 블록 512·32, 블러 σ0·2와 네 조합을 사용합니다.<br>**집계**: long·방법별 요약·조합 pivot·best_conditions의 4CSV를 제공합니다.<br>**점검 결과**: 각 조건 n_images =3이며 동일 변환과 항등 조건의 값 대응을 읽습니다. |
| <a id="layout18-table-11-row-3"></a> **조건** | **입력 수**: 각 조건 3장<br>**조건 수**: 블록 2·블러 2·조합 4<br>**크기·시드**: 512·42<br>**지표**: SSIM·PSNR·DSSIM 기반점수 |
| <a id="layout18-table-11-row-4"></a> **관측과 해석·한계·자료 연결** | 저장 표에서 Block32와 B32 +σ0는 같은 점수 35.3667978… 이 고 항등 조건은 0입니다. 이는 3장 입력에 대한 계산 확인 값입니다.<br>계산 경로를 확인한 소규모 자료이지 임상·공격 저항성 평가나 전체 1,097장 논문 결과를 대신하지 않습니다.<br>**표본**: 3장 결과를 전체 논문 수치로 일반화하지 않습니다.<br>**점수 식**: 이 자료는 SSIM이며 최종 MS-SSIM 기반 점수와 구분합니다.<br>**원영상**: 의료 원본·비교 이미지 자체는 포함하지 않습니다.<br>[이 차수 전체 상세](#purpose) · [실행 순서](#usage) · [결과와 해석](#results) · [프로젝트 공통 안내](../../README.md)<br>다른 자료 차수의 구현·관측은 [자료 1차](folder-1.md#user-content-reading-level-3) · [자료 2차](folder-2.md#user-content-reading-level-3) · [자료 4차](folder-4.md#user-content-reading-level-3)에서 별도로 확인합니다. |


[동일 수준 프로젝트 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A83.md)


</details>

<details>
<summary>LEVEL 4 · Advanced — 구현·설계·실패 처리</summary>

<a id="reading-level-4"></a>

## LEVEL 4 - Advanced

<a id="semantic-lung-tools-level-4"></a>

| 항목 | 이 차수의 내용 |
| --- | --- |
| 목적 | SSIM에서 DSSIM 기반 Privacy Score를 계산하는 경로와 3장·8 조건의 저장 결과를 확인하는 자료 차수입니다.<br>전체 논문의 1,097장 실험과 구분합니다. |
| 변경 | 자료 2차의 실험 노트북 구성 이후 유사도 기반 점수 계산과 소규모 결과 읽기를 정리했습니다. |
| 조건 | **입력 수**: 각 조건 3장<br>**조건 수**: 블록 2·블러 2·조합 4<br>**크기·시드**: 512·42<br>**지표**: SSIM·PSNR·DSSIM 기반점수 |
| 동작 | 1. long CSV 의 condition·method·n_images·ssim_mean·privacy_score 열을 확인합니다. |
| 결과 | 저장 표에서 Block32와 B32 +σ0는 같은 점수 35.3667978… 이 고 항등 조건은 0입니다.<br>이는 3장 입력에 대한 계산 확인 값입니다. |

### LEVEL 4 · 자료 차수의 수정 도구와 소규모 계산

자료 3차·Privacy Score의 소규모 계산 확인의 범위에서 설명합니다. 입력 준비·변환 또는 셀 수정·계산·저장의 경계를 나누어 읽습니다. 각 설정과 출력의 대응은 이 차수 자료를 기준으로 확인하고 다른 차수의 구현은 관련 링크에서 별도로 살펴봅니다.

| 항목 | 이 차수의 내용 |
| --- | --- |
| <a id="layout18-table-16-row-1"></a> **목적** | 블록 2 조건·블러 2 조건·조합 4 조건을 대상으로 계산한 CSV·통합 표·비의료 도표를 읽습니다. 의료 원영상의 비교 그림은 첨부하지 않습니다. |
| <a id="layout18-table-16-row-2"></a> **구현** | **점수 식**: Privacy Score =((1 −SSIM)/2)×100을 사용하며 PSNR은 참고 값으로 따로 저장합니다.<br>**작은 조건 집합**: 블록 512·32, 블러 σ0·2와 네 조합을 사용합니다.<br>**집계**: long·방법별 요약·조합 pivot·best_conditions의 4CSV를 제공합니다.<br>**점검 결과**: 각 조건 n_images =3이며 동일 변환과 항등 조건의 값 대응을 읽습니다. |
| <a id="layout18-table-16-row-3"></a> **조건** | **입력 수**: 각 조건 3장<br>**조건 수**: 블록 2·블러 2·조합 4<br>**크기·시드**: 512·42<br>**지표**: SSIM·PSNR·DSSIM 기반점수 |
| <a id="layout18-table-16-row-4"></a> **관측과 해석·한계·자료 연결** | 저장 표에서 Block32와 B32 +σ0는 같은 점수 35.3667978… 이 고 항등 조건은 0입니다. 이는 3장 입력에 대한 계산 확인 값입니다.<br>계산 경로를 확인한 소규모 자료이지 임상·공격 저항성 평가나 전체 1,097장 논문 결과를 대신하지 않습니다.<br>**표본**: 3장 결과를 전체 논문 수치로 일반화하지 않습니다.<br>**점수 식**: 이 자료는 SSIM이며 최종 MS-SSIM 기반 점수와 구분합니다.<br>**원영상**: 의료 원본·비교 이미지 자체는 포함하지 않습니다.<br>[이 차수 전체 상세](#purpose) · [실행 순서](#usage) · [결과와 해석](#results) · [프로젝트 공통 안내](../../README.md)<br>다른 자료 차수의 구현·관측은 [자료 1차](folder-1.md#user-content-reading-level-4) · [자료 2차](folder-2.md#user-content-reading-level-4) · [자료 4차](folder-4.md#user-content-reading-level-4)에서 별도로 확인합니다. |


[동일 수준 프로젝트 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A84.md)


</details>

<details>
<summary>LEVEL 5 · Expert — 근거·프로토콜·한계 검토</summary>

<a id="reading-level-5"></a>

## LEVEL 5 - Expert

<a id="semantic-lung-tools-level-5"></a>

### LEVEL 5 · 자료 차수의 수정 도구와 소규모 계산

자료 3차·Privacy Score의 소규모 계산 확인의 범위에서 설명합니다. 코드에 정의된 동작·설정, 저장된 관측값, 재현에 필요한 입력을 구분합니다. 분모·변환 위치·모델 대응과 알려진 한계를 유지하며 다른 차수나 원고의 결과를 이 자료의 실측으로 합치지 않습니다.

| 항목 | 이 차수의 내용 |
| --- | --- |
| <a id="layout18-table-21-row-1"></a> **목적** | 블록 2 조건·블러 2 조건·조합 4 조건을 대상으로 계산한 CSV·통합 표·비의료 도표를 읽습니다. 의료 원영상의 비교 그림은 첨부하지 않습니다. |
| <a id="layout18-table-21-row-2"></a> **구현** | **점수 식**: Privacy Score =((1 −SSIM)/2)×100을 사용하며 PSNR은 참고 값으로 따로 저장합니다.<br>**작은 조건 집합**: 블록 512·32, 블러 σ0·2와 네 조합을 사용합니다.<br>**집계**: long·방법별 요약·조합 pivot·best_conditions의 4CSV를 제공합니다.<br>**점검 결과**: 각 조건 n_images =3이며 동일 변환과 항등 조건의 값 대응을 읽습니다. |
| <a id="layout18-table-21-row-3"></a> **조건** | **입력 수**: 각 조건 3장<br>**조건 수**: 블록 2·블러 2·조합 4<br>**크기·시드**: 512·42<br>**지표**: SSIM·PSNR·DSSIM 기반점수 |
| <a id="layout18-table-21-row-4"></a> **관측과 해석·한계·자료 연결** | 저장 표에서 Block32와 B32 +σ0는 같은 점수 35.3667978… 이 고 항등 조건은 0입니다. 이는 3장 입력에 대한 계산 확인 값입니다.<br>계산 경로를 확인한 소규모 자료이지 임상·공격 저항성 평가나 전체 1,097장 논문 결과를 대신하지 않습니다.<br>**표본**: 3장 결과를 전체 논문 수치로 일반화하지 않습니다.<br>**점수 식**: 이 자료는 SSIM이며 최종 MS-SSIM 기반 점수와 구분합니다.<br>**원영상**: 의료 원본·비교 이미지 자체는 포함하지 않습니다.<br>[이 차수 전체 상세](#purpose) · [실행 순서](#usage) · [결과와 해석](#results) · [프로젝트 공통 안내](../../README.md)<br>다른 자료 차수의 구현·관측은 [자료 1차](folder-1.md) · [자료 2차](folder-2.md) · [자료 4차](folder-4.md)에서 별도로 확인합니다. |


[동일 수준 프로젝트 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A85.md)

<!-- reading-levels17:end -->

SSIM에서 DSSIM 기반 Privacy Score를 계산하는 경로와 3장·8 조건의 저장 결과를 확인하는 자료 차수입니다. 전체 논문의 1,097장 실험과 구분합니다.

분야: 영상 지표 › SSIM·DSSIM › 소규모 계산·표·그래프

[목적](#purpose) · [기능](#features) · [입출력](#flow) · [구성](#files) · [준비](#setup) · [사용법](#usage) · [결과](#results) · [제약](#limits) · [변경](#changes)

<a name="purpose"></a>

<a id="-이-단계에서-하는-일"></a>

## 연구 목적

블록 2 조건·블러 2 조건·조합 4 조건을 대상으로 계산한 CSV·통합 표·비의료 도표를 읽습니다. 의료 원영상의 비교 그림은 첨부하지 않습니다.

<a name="features"></a>

<a id="-주요-기능과-처리-방식"></a>

## 방법과 구현

| 구성 | 실제 역할 |
| --- | --- |
| <a id="layout18-table-22-row-1"></a> 점수 식 | Privacy Score =((1 −SSIM)/2)×100을 사용하며 PSNR은 참고 값으로 따로 저장합니다. |
| <a id="layout18-table-22-row-2"></a> 작은 조건 집합 | 블록 512·32, 블러 σ0·2와 네 조합을 사용합니다. |
| <a id="layout18-table-22-row-3"></a> 집계 | long·방법별 요약·조합 pivot·best_conditions의 4CSV를 제공합니다. |
| <a id="layout18-table-22-row-4"></a> 점검 결과 | 각 조건 n_images =3이며 동일 변환과 항등 조건의 값 대응을 읽습니다. |


<a name="flow"></a>

<a id="-입력--처리--출력"></a>

## 입력·처리·출력

| 입력 | 처리 | 출력 |
| --- | --- | --- |
| 3장과 8개 조건 | 원본/변환 SSIM·PSNR 계산 | 조건별 지표 |
| SSIM | DSSIM×100 변환 | Privacy Score |
| 조건별 값 | 요약·pivot·최대 조건 정리 | CSV·통합표·도표 |

<a name="files"></a>

<a id="-파일과-핵심-처리"></a>

## 파일별 역할

| 파일 | 이용 방법 |
| --- | --- |
| <a id="layout18-table-24-row-1"></a> [자료차수/3차/_smoke_privacy_score.ipynb](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/_smoke_privacy_score.ipynb) | 설정·함수·실행 셀 |
| <a id="layout18-table-24-row-2"></a> [자료차수/3차/tables/privacy_scores_long.csv](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/tables/privacy_scores_long.csv) | 원정밀도 표 |
| <a id="layout18-table-24-row-3"></a> [자료차수/3차/tables/privacy_scores_summary_by_method.csv](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/tables/privacy_scores_summary_by_method.csv) | 원정밀도 표 |
| <a id="layout18-table-24-row-4"></a> [자료차수/3차/tables/privacy_scores_combo_pivot.csv](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/tables/privacy_scores_combo_pivot.csv) | 원정밀도 표 |
| <a id="layout18-table-24-row-5"></a> [자료차수/3차/tables/privacy_scores_best_conditions.csv](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/tables/privacy_scores_best_conditions.csv) | 원정밀도 표 |


<a id="-함수셀로-찾아가기"></a>

### 관련 함수와 셀

관련 함수와 셀을 파일별로 정리했습니다. 실행 전 설정과 호출 순서, 출력 경로를 확인하세요.

| 파일 | 핵심 정의 |
| --- | --- |
| <a id="layout18-table-25-row-1"></a> [자료차수/3차/_smoke_privacy_score.ipynb](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/_smoke_privacy_score.ipynb) | 셀 6: `path_exists` · `candidate_train_dirs` · `should_ignore` · `count_images_under`<br>셀 8: `collect_image_table`<br>셀 10: `setup_matplotlib_font` · `load_rgb_image` · `block_scramble` · `apply_gaussian_blur` · `apply_transform`<br>셀 12: `compute_pair_metrics` · `load_image_records` · `iter_records` · `evaluate_condition` · `condition_name` · `format_sigma`<br>셀 18: `save_fig`<br>셀 20: `save_table_png`<br>셀 22: `parse_condition` |


<a name="setup"></a>

<a id="️-환경과-설정"></a>

## 실행 환경과 설정

| 항목 | 조건·기본값 |
| --- | --- |
| 입력 수 | 각 조건 3장 |
| 조건 수 | 블록 2·블러 2·조합 4 |
| 크기·시드 | 512·42 |
| 지표 | SSIM·PSNR·DSSIM 기반점수 |

<a name="usage"></a>

<a id="-준비와-사용-순서"></a>

## 실행 순서

1. long CSV의 condition·method·n_images·ssim_mean·privacy_score 열을 확인합니다.
2. Block512·σ0 항등 조건과 Block32·조합 B32_S0의 대응을 비교합니다.
3. 방법별 요약과 2×2 pivot이 long 표의 같은 조건에서 나온 값인지 읽습니다.
4. 점수 식을 최종 논문의 MS-SSIM 식과 구별합니다.

<a name="results"></a>

<a id="-결과를-읽는-방법"></a>

## 결과와 해석

저장 표에서 Block32와 B32 +σ0는 같은 점수 35.3667978… 이 고 항등 조건은 0입니다. 이는 3장 입력에 대한 계산 확인 값입니다.

계산 경로를 확인한 소규모 자료이지 임상·공격 저항성 평가나 전체 1,097장 논문 결과를 대신하지 않습니다.

<a name="limits"></a>

<a id="️-알려진-제약과-확인-지점"></a>

## 제약과 확인 사항

| 상황 | 확인할 내용 |
| --- | --- |
| 표본 | 3장 결과를 전체 논문 수치로 일반화하지 않습니다. |
| 점수 식 | 이 자료는 SSIM이며 최종 MS-SSIM 기반 점수와 구분합니다. |
| 원영상 | 의료 원본·비교 이미지 자체는 포함하지 않습니다. |

<a name="changes"></a>

<a id="-이전-단계와의-변화"></a>

## 직전 단계와 비교

자료 2차의 실험 노트북 구성 이후 유사도 기반 점수 계산과 소규모 결과 읽기를 정리했습니다.

[직전 단계 전체 비교·구성](../revision-diffs/folder-3-%EC%97%B4%EB%9E%8C.md) · [전체 파일 크기·해시](../revision-manifests/folder-3.json)

<details>
<summary>이 단계의 파일 기록과 전체 해시</summary>

아래 내용는 해당 단계가 기록될 당시의 파일 정보입니다. 현재 첨부는 [프로젝트 자료 안내](../PAPERS.md)에서 확인할 수 있습니다.

| 파일 | 종류 | 바이트 | SHA-256 |
| --- | --- | --- | --- |
| <a id="layout18-table-28-row-1"></a> [자료차수/3차/tables/privacy_scores_best_conditions.csv](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/tables/privacy_scores_best_conditions.csv) | .csv | 858 | `f8e160d380f0c0f41f33a8913e7739c7fe9a9f2e42081e77c16c302f5de9a529` |
| <a id="layout18-table-28-row-2"></a> [자료차수/3차/tables/privacy_scores_combo_pivot.csv](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/tables/privacy_scores_combo_pivot.csv) | .csv | 92 | `7a31a1ae5238c3369ad5461b7806948a61eda358dae86dc87b177181df11b034` |
| <a id="layout18-table-28-row-3"></a> [자료차수/3차/tables/privacy_scores_long.csv](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/tables/privacy_scores_long.csv) | .csv | 1507 | `edcecf8fe6c892b0640ffe9d7d7341c9ee094ab4624cfb5d65a3d52974caff22` |
| <a id="layout18-table-28-row-4"></a> [자료차수/3차/tables/privacy_scores_summary_by_method.csv](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/tables/privacy_scores_summary_by_method.csv) | .csv | 362 | `403ff42da2b5a21428304bb456346178734658976dfff5a0c6abb8092782d060` |
| <a id="layout18-table-28-row-5"></a> [자료차수/3차/graphs/01_block_privacy_score.png](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/graphs/01_block_privacy_score.png) | .png | 70066 | `2d3be7ac20d49f2e91cf4f3039fbbc8a4fd979e65025d456eb14802955783287` |
| <a id="layout18-table-28-row-6"></a> [자료차수/3차/graphs/02_blur_privacy_score.png](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/graphs/02_blur_privacy_score.png) | .png | 63552 | `056c40e03053b9d7694877333ceb1a2019fb5080e3714355b5a0ef03c114be19` |
| <a id="layout18-table-28-row-7"></a> [자료차수/3차/graphs/03_combo_privacy_score_heatmap.png](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/graphs/03_combo_privacy_score_heatmap.png) | .png | 42052 | `6d3cc49c6d9acf6a977922e59ac140c1d3f7c181b23595f4514ad3404fae59fa` |
| <a id="layout18-table-28-row-8"></a> [자료차수/3차/graphs/04_block_ssim_psnr_reference.png](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/graphs/04_block_ssim_psnr_reference.png) | .png | 64195 | `f2359a64da2d2a5129dd225fc3cebde956bd414e4d767ebfac9804ea0baa386e` |
| <a id="layout18-table-28-row-9"></a> [자료차수/3차/graphs/05_blur_ssim_psnr_reference.png](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/graphs/05_blur_ssim_psnr_reference.png) | .png | 77351 | `2aad1e739efc2b01a5e5b6b0acd24cba7b61e9d301fba2bfd7c19ea566435d72` |
| <a id="layout18-table-28-row-10"></a> [자료차수/3차/graphs/06_top_conditions_privacy_score.png](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/graphs/06_top_conditions_privacy_score.png) | .png | 60606 | `df22b8d68e003e26e65c2c236bd427538882ff750a2e473918284a90d4bef99c` |
| <a id="layout18-table-28-row-11"></a> [자료차수/3차/graphs/07_method_distribution_boxplot.png](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/graphs/07_method_distribution_boxplot.png) | .png | 38584 | `ceb03b03ff92470e91a9e62b2f1151f1512f7b11bf583dec03dc07d8d2915fee` |
| <a id="layout18-table-28-row-12"></a> [자료차수/3차/graphs/08_top_conditions_table.png](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/graphs/08_top_conditions_table.png) | .png | 80715 | `d0e4e134df95fda8aa4fbeb0a0c17c9769aac16dc6ebf8c86c0a7765a1450ca8` |
| <a id="layout18-table-28-row-13"></a> [자료차수/3차/graphs/09_best_by_method_table.png](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/graphs/09_best_by_method_table.png) | .png | 45058 | `9da6f678a12bdf33915130898cc4c2d50d2ab7af13a52f9b7433590c3a0d48f1` |
| <a id="layout18-table-28-row-14"></a> [자료차수/3차/create_privacy_notebook.py](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/create_privacy_notebook.py) | .py | 28399 | `3809df9b5f3091f79172f0257c8eb7f2ef828bbf99da99eb41b486bb66108280` |
| <a id="layout18-table-28-row-15"></a> [자료차수/3차/modify_privacy_notebook_ssim_only.py](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/modify_privacy_notebook_ssim_only.py) | .py | 27299 | `759fd7599e40b5cb25a8e7bc5f248bbb9eff2fd3328932c3c45236521345fc91` |
| <a id="layout18-table-28-row-16"></a> [자료차수/3차/_smoke_privacy_score.ipynb](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/_smoke_privacy_score.ipynb) | .ipynb | 89274 | `a03f40d6eab19fb5bdd3d4d60c3f308f03c43e80387f8f71dd70624f6311a8e6` |
| <a id="layout18-table-28-row-17"></a> [원본자료/3차/privacy_score_outputs/privacy_score_results.xlsx](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/3%EC%B0%A8/privacy_score_outputs/privacy_score_results.xlsx) | .xlsx | 8330 | `a90c2676448a700ef65836cd2f3427030c95e4864870268f1bd3d7eda144b4f1` |
| <a id="layout18-table-28-row-18"></a> [원본자료/3차/privacy_score_outputs/tables/selected_images.csv](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/3%EC%B0%A8/privacy_score_outputs/tables/selected_images.csv) | .csv | 406 | `13a874a2d948b964c171ab3a6927e78882c262a245940933a5285454de846a71` |


</details>

---

[프로젝트](../../README.md) · [전체 차수](../REVISION_INDEX.md) · [자료 폴더](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/tables) · [폴더 2차](folder-2.md) · [폴더 4차](folder-4.md)


<a id="layout18-table-12-row-1"></a><a id="layout18-table-12-row-2"></a><a id="layout18-table-12-row-3"></a><a id="layout18-table-12-row-4"></a><a id="layout18-table-17-row-1"></a><a id="layout18-table-17-row-2"></a><a id="layout18-table-17-row-3"></a><a id="layout18-table-17-row-4"></a><a id="layout18-table-2-row-1"></a><a id="layout18-table-2-row-2"></a><a id="layout18-table-2-row-3"></a><a id="layout18-table-2-row-4"></a><a id="layout18-table-7-row-1"></a><a id="layout18-table-7-row-2"></a><a id="layout18-table-7-row-3"></a><a id="layout18-table-7-row-4"></a>

</details>


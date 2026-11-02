<div align="center">

# 🫁 연구 1 · EfficientNetV2-S와 입력 비식별화

**EfficientNetV2-S에서 입력 CT 영상에 Gaussian Blur와 블록 재배열을 각각 적용했을 때 분류 결과가 어떻게 달라지는지 비교한 하계 3쪽 연구입니다.**

**기술 분류:** 의료 영상 연구 › EfficientNetV2-S 분류 › 입력 Blur·Block 단독 비교

[목적](#purpose) · [기능](#features) · [입출력](#flow) · [구성](#files) · [준비](#setup) · [사용법](#usage) · [결과](#results) · [제약](#limits) · [변경](#changes)

</div>

<a name="purpose"></a>

## 🎯 이 단계에서 하는 일

원본 영상의 분류 유용성과 변환 강도의 관계를 읽는 논문입니다. ResNet50·조합 100조건·MS-SSIM 점수를 다루는 후속 연구 2와 모델·문제·원고 구성을 구분합니다.

<a name="features"></a>

## 🧩 주요 기능과 처리 방식

| 구성 | 실제 역할 |
| --- | --- |
| 블러 비교 | σ0·1·2·4·8·16·32·64·128·256의 입력 블러를 비교합니다. |
| 블록 비교 | 512에서 1까지 10개 블록 크기로 재배열한 입력을 비교합니다. |
| 지표 읽기 | 정확도·ROC-AUC·클래스별 Recall과 혼동행렬을 함께 봅니다. |
| 발표 연결 | 완성 발표 19장·전체 대본 9쪽·그래프 노트북을 같은 연구의 설명 자료로 연결합니다. |

<a name="flow"></a>

## 🔄 입력 → 처리 → 출력

| 입력 | 처리 | 출력·읽을 결과 |
| --- | --- | --- |
| 512×512 CT와 클래스 | Blur 또는 Block 입력 변환 | 강도별 영상 조건 |
| 조건별 영상 | EfficientNetV2-S 분류 | 분류 예측과 평가 지표 |
| 지표와 혼동행렬 | 강도별 성능 변화 비교 | 비식별화와 유용성의 관계 |

<a name="files"></a>

## 📁 파일과 핵심 처리

| 파일 | 이용 방법 |
| --- | --- |
| [논문/1차_EfficientNetV2-S_하계_최종.pdf](../../%EB%85%BC%EB%AC%B8/1%EC%B0%A8_EfficientNetV2-S_%ED%95%98%EA%B3%84_%EC%B5%9C%EC%A2%85.pdf) | 전체 원문·도표 읽기 |
| [연구1_하계_EfficientNetV2-S/논문/원문_최종.hwp](../../%EC%97%B0%EA%B5%AC1_%ED%95%98%EA%B3%84_EfficientNetV2-S/%EB%85%BC%EB%AC%B8/%EC%9B%90%EB%AC%B8_%EC%B5%9C%EC%A2%85.hwp) | 같은 판의 편집 원본 |
| [연구1_하계_EfficientNetV2-S/그래프/Blur_Block_1차_그래프_white.ipynb](../../%EC%97%B0%EA%B5%AC1_%ED%95%98%EA%B3%84_EfficientNetV2-S/%EA%B7%B8%EB%9E%98%ED%94%84/Blur_Block_1%EC%B0%A8_%EA%B7%B8%EB%9E%98%ED%94%84_white.ipynb) | 설정·함수·실행 셀 |
| [연구1_하계_EfficientNetV2-S/발표자료/하계학술대회 PPT.pdf](../../%EC%97%B0%EA%B5%AC1_%ED%95%98%EA%B3%84_EfficientNetV2-S/%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C/%ED%95%98%EA%B3%84%ED%95%99%EC%88%A0%EB%8C%80%ED%9A%8C%20PPT.pdf) | 전체 원문·도표 읽기 |
| [연구1_하계_EfficientNetV2-S/발표자료/하계학술대회 발표 대본.pdf](../../%EC%97%B0%EA%B5%AC1_%ED%95%98%EA%B3%84_EfficientNetV2-S/%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C/%ED%95%98%EA%B3%84%ED%95%99%EC%88%A0%EB%8C%80%ED%9A%8C%20%EB%B0%9C%ED%91%9C%20%EB%8C%80%EB%B3%B8.pdf) | 전체 원문·도표 읽기 |

### 🔎 함수·셀로 찾아가기

아래 이름은 해당 파일의 실제 정의입니다. 위 처리 설명과 함께 설정·호출 순서·출력 경로를 따라 읽습니다.

| 파일 | 핵심 정의 |
| --- | --- |
| [연구1_하계_EfficientNetV2-S/그래프/Blur_Block_1차_그래프_white.ipynb](../../%EC%97%B0%EA%B5%AC1_%ED%95%98%EA%B3%84_EfficientNetV2-S/%EA%B7%B8%EB%9E%98%ED%94%84/Blur_Block_1%EC%B0%A8_%EA%B7%B8%EB%9E%98%ED%94%84_white.ipynb) | 셀 0: `acc_color` · `draw_cm`<br>셀 1: `block_label` · `acc_color` |

<a name="setup"></a>

## ⚙️ 환경과 설정

| 항목 | 조건·기본값 |
| --- | --- |
| 원고 | 하계 최종 3쪽 PDF/HWP |
| 입력 | 512×512 CT3분류 |
| 조건 | Blur10·Block10 단독 비교 |
| 결과 자료 | 조건별 JSON·그래프 노트북·발표/대본 |

<a name="usage"></a>

## 📖 읽고 활용하는 순서

1. 최종 논문의 방법에서 두 입력 변환과 모델을 확인합니다.
2. 결과표와 혼동행렬을 같은 조건명으로 비교합니다.
3. 그래프 노트북과 저장 JSON에서 원본·조건별 값의 대응을 확인합니다.
4. 발표 PDF와 전체 대본은 논문의 결과를 전달하는 흐름으로 함께 읽습니다.

<a name="results"></a>

## 📊 결과를 읽는 방법

원고는 원본 92.5%, Blurσ32 53.3%, Block32 79.2%, Block1 52.9% 등을 보고합니다. 이 값은 하계 연구의 보고값이며 후속 연구의 수치로 대체하지 않습니다.

저장된 Block512의 정확도 0.929166…와 Blurσ0의 0.925는 서로 다른 실행의 기준값입니다. 같은 원본 조건이라는 이유로 합치지 않고 실행과 지표를 구분해 읽습니다.

<a name="limits"></a>

## 🛠️ 알려진 제약과 확인 지점

| 상황 | 확인할 내용 |
| --- | --- |
| 연구 간 조건 | 연구 2의 1,097장·ResNet50 설정을 이 하계 연구에 소급하지 않습니다. |
| 프라이버시 해석 | 입력 변환의 분류 유용성 분석이며 실제 개인정보 공격 저항성의 입증과 구분합니다. |
| 자료 범위 | 의료 원영상·환자 기록은 포함하지 않습니다. |

<a name="changes"></a>

## 🔀 이전 단계와의 변화

입력 Blur·Block의 단독 비교를 정리한 연구 1입니다. 이후 연구 2는 ResNet50과 조합·영상 유사도 기반 점수를 별도의 후속 논문으로 다룹니다.

[🔎 직전 단계 전체 비교·구성](../revision-diffs/study-1.diff) · [📋 전체 파일 크기·해시](../revision-manifests/study-1.json)

<details>
<summary>📎 이 단계의 파일 기록과 전체 해시</summary>

아래 표는 해당 단계가 기록될 당시의 파일 정보입니다. 현재 첨부는 [프로젝트 자료 안내](../PAPERS.md)에서 확인할 수 있습니다.

| 파일 | 종류 | 바이트 | SHA-256 |
|---|---|---:|---|
| `논문/1차_EfficientNetV2-S_하계_최종.pdf` | .pdf | 410164 | `dd6309e6f6b722d6db242e9c2237584314ad7d7bdf32eb1a91d10ced5ba3fe63` |
| [연구1_하계_EfficientNetV2-S/그래프/Blur_Block_1차_그래프_white.ipynb](../../%EC%97%B0%EA%B5%AC1_%ED%95%98%EA%B3%84_EfficientNetV2-S/%EA%B7%B8%EB%9E%98%ED%94%84/Blur_Block_1%EC%B0%A8_%EA%B7%B8%EB%9E%98%ED%94%84_white.ipynb) | .ipynb | 31695 | `a8c2615ce407a6e49de77cbea440d236e423dd77439abeaca57697b21e928823` |
| `연구1_하계_EfficientNetV2-S/발표자료/하계학술대회 PPT.pdf` | .pdf | 2156389 | `22c41af0ada654bbaf8c8c5882ca1165da5e1216430af199db1fd0f560f349b3` |
| `연구1_하계_EfficientNetV2-S/발표자료/하계학술대회 PPT.pptx` | .pptx | 2325109 | `a95905aea2ed35a70f0e43e5f0eaf30cbb5c227fed7384f952641104b26d5193` |
| `연구1_하계_EfficientNetV2-S/발표자료/하계학술대회 발표 대본 정리.docx` | .docx | 12063 | `fbe895f010f6ee875395b5486b42dcf7d07248e6b6ac98a17a21bb38eda67246` |
| `연구1_하계_EfficientNetV2-S/발표자료/하계학술대회 발표 대본 정리.pdf` | .pdf | 280123 | `0dad95908a9f7771703c37c882b5265162b1ea6d1a75762a96cef4d30923a598` |
| `연구1_하계_EfficientNetV2-S/발표자료/하계학술대회 발표 대본.docx` | .docx | 14644 | `3a66466626c76c84640e1d4284ff375708f7ba428d92fd9f7a2c686cf3bbbae8` |
| `연구1_하계_EfficientNetV2-S/발표자료/하계학술대회 발표 대본.pdf` | .pdf | 314134 | `f7d5589105d6a714a62ebe53a264a23070941e4fd26db78ddc8a08e8efc2f62a` |
| [최신 편집 원문](../../%EC%97%B0%EA%B5%AC1_%ED%95%98%EA%B3%84_EfficientNetV2-S/%EB%85%BC%EB%AC%B8/%EC%9B%90%EB%AC%B8_%EC%B5%9C%EC%A2%85.hwp) | .hwp | 527360 | `f19ddfe212b9c38fd1cfdfec29f8d499e0150bd183e2d6a7992867b34720b7fc` |
| [최신 편집 원문](../../%EC%97%B0%EA%B5%AC1_%ED%95%98%EA%B3%84_EfficientNetV2-S/%EB%85%BC%EB%AC%B8/%EC%9B%90%EB%AC%B8_%EC%B5%9C%EC%A2%85.hwp) | .hwp | 534016 | `a50590b82b4f2a37c948d267c03acdb38e2dfdb6ec1b912ad77718c50d8b9915` |
| [최신 편집 원문](../../%EC%97%B0%EA%B5%AC1_%ED%95%98%EA%B3%84_EfficientNetV2-S/%EB%85%BC%EB%AC%B8/%EC%9B%90%EB%AC%B8_%EC%B5%9C%EC%A2%85.hwp) | .hwp | 50688 | `218bd80c6e58efc061d4717f1e47dab5c494c748813b3e580d98660a54cb8a4b` |
| [최신 편집 원문](../../%EC%97%B0%EA%B5%AC1_%ED%95%98%EA%B3%84_EfficientNetV2-S/%EB%85%BC%EB%AC%B8/%EC%9B%90%EB%AC%B8_%EC%B5%9C%EC%A2%85.hwp) | .hwp | 55296 | `d8d43b6b577716c444a38c1fe258184834317b69628d469d075bc1014ba21d44` |
| [연구1_하계_EfficientNetV2-S/원문보관/그림/Blur_Block_1차_그래프_white.ipynb](../../%EC%97%B0%EA%B5%AC1_%ED%95%98%EA%B3%84_EfficientNetV2-S/%EC%9B%90%EB%AC%B8%EB%B3%B4%EA%B4%80/%EA%B7%B8%EB%A6%BC/Blur_Block_1%EC%B0%A8_%EA%B7%B8%EB%9E%98%ED%94%84_white.ipynb) | .ipynb | 34700 | `21207ffb5200d44de6a06b908ce7171648cf3d4a2c390c834162e357d61461ec` |

</details>

---

[🏠 프로젝트](../../README.md) · [🗂️ 전체 차수](../REVISION_INDEX.md) · [📁 자료 폴더](../../%EB%85%BC%EB%AC%B8) · [➡️ 연구2 · ResNet50 후속 원고](study-2.md)

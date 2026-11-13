<a id="-블록-1차--저장된-10조건-분류-결과"></a>

# 블록 1차 · 저장된 10조건 분류 결과

입력 변환 조건별 정확도·ROC-AUC·클래스별 Recall·혼동행렬을 보관한 결과 JSON입니다. 저장 결과와 그래프 입력을 대조할 수 있습니다.

분야: 저장된 실험 결과 › 조건별 JSON › 분류 지표와 혼동행렬

[목적](#purpose) · [기능](#features) · [입출력](#flow) · [구성](#files) · [준비](#setup) · [사용법](#usage) · [결과](#results) · [제약](#limits) · [변경](#changes)

<a name="purpose"></a>

<a id="-이-단계에서-하는-일"></a>

## 연구 목적

이 자료의 기준 정확도는 0.9291666666666667입니다. 블러와 블록의 기준 실행값은 서로 구분합니다.

<a name="features"></a>

<a id="-주요-기능과-처리-방식"></a>

## 방법과 구현

| 구성 | 실제 역할 |
| --- | --- |
| 조건 | 실제로 저장된 블록 512·256·128·64·32·16·8·4·2·1의 10조건을 읽습니다. |
| 분류 지표 | acc·roc_auc·per_class_acc를 조건별로 담습니다. |
| 혼동행렬 | cm과 class_names의 순서를 함께 보며 클래스별 Recall을 확인합니다. |
| 그래프 입력 | 연구 1의 그래프 노트북에서 같은 조건명·실행의 값을 사용하는지 확인합니다. |

<a name="flow"></a>

<a id="-입력--처리--출력"></a>

## 입력·처리·출력

| 입력 | 처리 | 출력 |
| --- | --- | --- |
| 조건별 JSON | 필드와 클래스 순서 확인 | 분류 지표 |
| 혼동행렬 | 행별 정답 수와 대각선 비율 확인 | 클래스별 Recall |
| 지표와 조건 | 표·그래프 대응 | 강도별 비교 |

<a name="files"></a>

<a id="-파일과-핵심-처리"></a>

## 파일별 역할

| 파일 | 이용 방법 |
| --- | --- |
| [원본자료/블록/1차 실험/블록 1/불록 결과/all_block_results.json](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EB%B8%94%EB%A1%9D/1%EC%B0%A8%20%EC%8B%A4%ED%97%98/%EB%B8%94%EB%A1%9D%201/%EB%B6%88%EB%A1%9D%20%EA%B2%B0%EA%B3%BC/all_block_results.json) | 조건별 구조화 기록 |
| [연구 1_하계_EfficientNetV2-S/그래프/Blur_Block_1차_그래프_white.ipynb](../../%EC%97%B0%EA%B5%AC1_%ED%95%98%EA%B3%84_EfficientNetV2-S/%EA%B7%B8%EB%9E%98%ED%94%84/Blur_Block_1%EC%B0%A8_%EA%B7%B8%EB%9E%98%ED%94%84_white.ipynb) | 설정·함수·실행 셀 |

<a id="-함수셀로-찾아가기"></a>

### 관련 함수와 셀

관련 함수와 셀을 파일별로 정리했습니다. 실행 전 설정과 호출 순서, 출력 경로를 확인하세요.

| 파일 | 핵심 정의 |
| --- | --- |
| [연구 1_하계_EfficientNetV2-S/그래프/Blur_Block_1차_그래프_white.ipynb](../../%EC%97%B0%EA%B5%AC1_%ED%95%98%EA%B3%84_EfficientNetV2-S/%EA%B7%B8%EB%9E%98%ED%94%84/Blur_Block_1%EC%B0%A8_%EA%B7%B8%EB%9E%98%ED%94%84_white.ipynb) | 셀 0: `acc_color` · `draw_cm`<br>셀 1: `block_label` · `acc_color` |

<a name="setup"></a>

<a id="️-환경과-설정"></a>

## 실행 환경과 설정

| 항목 | 조건·기본값 |
| --- | --- |
| 읽기 | JSON 뷰어 또는 Python |
| 조건 수 | 10 |
| 클래스 순서 | Bengin cases·Malignant cases·Normal cases |
| 기준 정확도 | 0.9291666666666667 |

<a name="usage"></a>

<a id="-읽고-활용하는-순서"></a>

## 원고 읽기

1. JSON에서 조건 키와 sigma 또는 block_size를 확인합니다.
2. acc·roc_auc와 클래스별 값의 단위를 구분합니다.
3. cm의 행·열 순서를 class_names에 맞춰 읽습니다.
4. 그래프·논문과 비교할 때 저장 실행·조건·반올림을 함께 확인합니다.

<a name="results"></a>

<a id="-결과를-읽는-방법"></a>

## 결과와 해석

per_class_acc는 혼동행렬의 해당 행 정답 비율과 대응하므로 클래스별 Recall로 읽습니다.

저장 JSON은 조건별 결과 기록입니다. 전체 학습을 재현하려면 원영상·가중치·분할 기록이 따로 필요하며 후속 ResNet50 원고의 결과와 구분합니다.

<a name="limits"></a>

<a id="️-알려진-제약과-확인-지점"></a>

## 제약과 확인 사항

| 상황 | 확인할 내용 |
| --- | --- |
| 실행 범위 | 결과 기록이며 새 학습을 진행하는 코드가 아닙니다. |
| 재현 입력 | 원영상·모델·분할·학습 기록은 별도로 필요합니다. |
| 연구 구분 | EfficientNetV2-S 하계 결과와 후속 ResNet50 결과를 혼합하지 않습니다. |

<a name="changes"></a>

<a id="-이전-단계와의-변화"></a>

## 직전 단계와 비교

입력 변환의 기존 결과를 보관한 자료입니다. 각 조건의 전체 값·혼동행렬과 그래프를 연결합니다.

[직전 단계 전체 비교·구성](../revision-diffs/experiment-original-block.diff) · [전체 파일 크기·해시](../revision-manifests/experiment-original-block.json)

<details>
<summary>이 단계의 파일 기록과 전체 해시</summary>

아래 표는 해당 단계가 기록될 당시의 파일 정보입니다. 현재 첨부는 [프로젝트 자료 안내](../PAPERS.md)에서 확인할 수 있습니다.

| 파일 | 종류 | 바이트 | SHA-256 |
|---|---|---:|---|
| [원본자료/블록/1차 실험/블록 1/불록 결과/all_block_results.json](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EB%B8%94%EB%A1%9D/1%EC%B0%A8%20%EC%8B%A4%ED%97%98/%EB%B8%94%EB%A1%9D%201/%EB%B6%88%EB%A1%9D%20%EA%B2%B0%EA%B3%BC/all_block_results.json) | .json | 5040 | `a85dd325d928a5e3ae116c6d8d5ca0d06b90e632313b28ca694d81fa80cb9801` |

</details>

---

[프로젝트](../../README.md) · [전체 차수](../REVISION_INDEX.md) · [자료 폴더](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EB%B8%94%EB%A1%9D/1%EC%B0%A8%20%EC%8B%A4%ED%97%98/%EB%B8%94%EB%A1%9D%201/%EB%B6%88%EB%A1%9D%20%EA%B2%B0%EA%B3%BC)

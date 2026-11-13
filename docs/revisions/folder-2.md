<a id="️-자료-2차--실험-방식-정렬과-조합-노트북-생성"></a>

# 자료 2차 · 실험 방식 정렬과 조합 노트북 생성

기존 Blur·Block 노트북의 학습·모니터 출력을 맞추고 Block→Blur 조합 노트북을 만드는 JavaScript 보조 도구 단계입니다.

분야: 개발 보조 도구 › Node.js › 노트북 셀 생성·치환·복원

[목적](#purpose) · [기능](#features) · [입출력](#flow) · [구성](#files) · [준비](#setup) · [사용법](#usage) · [결과](#results) · [제약](#limits) · [변경](#changes)

<a name="purpose"></a>

<a id="-이-단계에서-하는-일"></a>

## 연구 목적

노트북을 직접 학습하는 코드와 노트북의 셀 내용을 수정하는 도구를 구분합니다. 이 스크립트들은 파일을 읽고 지정 문자열을 치환한 뒤 다시 저장합니다.

<a name="features"></a>

<a id="-주요-기능과-처리-방식"></a>

## 방법과 구현

| 구성 | 실제 역할 |
| --- | --- |
| 방식 정렬 | align_experiment_methods.mjs가 Blur 설계를 유지하며 GPU 모니터 필드·그래프의 호환 처리를 맞춥니다. |
| 조합 생성 | build_block_blur_notebook.mjs가 Blur 노트북을 바탕으로 Block→Blur100조합의 설정·함수를 구성합니다. |
| 입력 확인 | replaceOrThrow가 대상 문자열이 없으면 중단하도록 구성돼 있습니다. |
| 복원 | rollback_original_notebooks.mjs가 보관본과 지정 셀을 이용해 이전 구성을 복원합니다. |

<a name="flow"></a>

<a id="-입력--처리--출력"></a>

## 입력·처리·출력

| 입력 | 처리 | 출력 |
| --- | --- | --- |
| 기존 ipynb | JSON 읽기·셀 소스 추출 | 수정 대상 코드 |
| 지정 문자열·새 함수 | 존재 확인과 치환 | 설정이 맞춰진 ipynb |
| 보관본 | 복사·선택 셀 복원 | 이전 구성 |

<a name="files"></a>

<a id="-파일과-핵심-처리"></a>

## 파일별 역할

| 파일 | 이용 방법 |
| --- | --- |
| [자료차수/2차/align_experiment_methods.mjs](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/2%EC%B0%A8/align_experiment_methods.mjs) | 노트북 구성·변경 도구 |
| [자료차수/2차/build_block_blur_notebook.mjs](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/2%EC%B0%A8/build_block_blur_notebook.mjs) | 노트북 구성·변경 도구 |
| [자료차수/2차/rollback_original_notebooks.mjs](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/2%EC%B0%A8/rollback_original_notebooks.mjs) | 노트북 구성·변경 도구 |

<a id="-함수셀로-찾아가기"></a>

### 관련 함수와 셀

관련 함수와 셀을 파일별로 정리했습니다. 실행 전 설정과 호출 순서, 출력 경로를 확인하세요.

| 파일 | 핵심 정의 |
| --- | --- |
| [자료차수/2차/align_experiment_methods.mjs](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/2%EC%B0%A8/align_experiment_methods.mjs) | 소스: `getSource` · `setSource` · `replaceOrThrow` · `addGpuLogCompatibility` · `addComboGpuLogCompatibility` · `makeGpuGraphRobust` · `makeGpuSummaryRobust` · `run_experiment` |
| [자료차수/2차/build_block_blur_notebook.mjs](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/2%EC%B0%A8/build_block_blur_notebook.mjs) | 소스: `getSource` · `setSource` · `replaceOrThrow` · `condition_key` · `condition_label` · `condition_short_label` · `condition_label_from_key` · `set_reproducible` |
| [자료차수/2차/rollback_original_notebooks.mjs](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/2%EC%B0%A8/rollback_original_notebooks.mjs) | 소스: `getSource` · `setSource` · `replaceOrThrow` |

<a name="setup"></a>

<a id="️-환경과-설정"></a>

## 실행 환경과 설정

| 항목 | 조건·기본값 |
| --- | --- |
| 실행기 | Node.js |
| 입력 | 스크립트에 지정된 원본·보관 노트북 |
| 출력 | 수정·생성된 ipynb |
| 주의 | 입력 경로·셀 번호·치환 문자열을 먼저 확인 |

<a name="usage"></a>

<a id="-준비와-사용-순서"></a>

## 실행 순서

1. paths·sourcePath·outputPath의 실제 파일을 확인합니다.
2. 수정할 셀과 replaceOrThrow의 전후 문자열을 읽습니다.
3. 원본을 별도 보관하고 출력 대상이 실행 중인 노트북이 아닌지 확인합니다.
4. 생성·수정 뒤 JSON·셀 소스와 전체 차이를 비교하고 이후 학습은 별도로 준비합니다.

<a name="results"></a>

<a id="-결과를-읽는-방법"></a>

## 결과와 해석

도구의 실행 결과는 노트북 코드의 변경입니다. 학습이나 새 성능 평가의 완료를 의미하지 않습니다.

공통 모니터 필드와 그래프의 호환성, 변환 순서와 원본 복원 범위를 구별해 읽습니다.

<a name="limits"></a>

<a id="️-알려진-제약과-확인-지점"></a>

## 제약과 확인 사항

| 상황 | 확인할 내용 |
| --- | --- |
| 경로 | 도구에 지정된 경로와 실행 위치를 확인합니다. |
| 원문 변경 | 노트북을 직접 다시 쓰므로 원본과 작업 사본을 구분합니다. |
| 정확한 치환 | 예상 셀이 다른 버전이면 치환 전 조건부터 확인합니다. |

<a name="changes"></a>

<a id="-이전-단계와의-변화"></a>

## 직전 단계와 비교

자료 1차의 노트북 정리에서 방식 정렬·조합 생성·복원 도구로 이어지는 자료 2차입니다.

[직전 단계 전체 비교·구성](../revision-diffs/folder-2.diff) · [전체 파일 크기·해시](../revision-manifests/folder-2.json)

<details>
<summary>이 단계의 파일 기록과 전체 해시</summary>

아래 표는 해당 단계가 기록될 당시의 파일 정보입니다. 현재 첨부는 [프로젝트 자료 안내](../PAPERS.md)에서 확인할 수 있습니다.

| 파일 | 종류 | 바이트 | SHA-256 |
|---|---|---:|---|
| [자료차수/2차/align_experiment_methods.mjs](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/2%EC%B0%A8/align_experiment_methods.mjs) | .mjs | 11300 | `137dbb097d5821e11f17326afa3b37a3cb2f570ca010e0c2b3f81f5c517b5b22` |
| [자료차수/2차/build_block_blur_notebook.mjs](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/2%EC%B0%A8/build_block_blur_notebook.mjs) | .mjs | 29388 | `bd77b870fe40d0a6318b49f210ae38b533401eb0b874c253277c6f673b86d70a` |
| [자료차수/2차/rollback_original_notebooks.mjs](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/2%EC%B0%A8/rollback_original_notebooks.mjs) | .mjs | 3358 | `c311e74df31a801231b391e4a692cc870e31f3ec950b9eb1fedd7169bbeb5c29` |

</details>

---

[프로젝트](../../README.md) · [전체 차수](../REVISION_INDEX.md) · [자료 폴더](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/2%EC%B0%A8) · [1차](folder-1.md) · [폴더 3차](folder-3.md)

<a id="-자료차수2차"></a>

# 자료차수/2차

<!-- reading-levels17:start -->
**읽기 수준 선택** · [LEVEL 1 - Beginner](../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A81.md) · [LEVEL 2 - Explorer](../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A82.md) · [LEVEL 3 - Practitioner](../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A83.md) · [LEVEL 4 - Advanced](../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A84.md) · [LEVEL 5 - Expert](../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A85.md)
<!-- reading-levels17:end -->

**기존 Blur·Block 노트북의 학습·모니터 출력을 맞추고 Block→Blur 조합 노트북을 만드는 JavaScript 보조 도구 단계입니다.**

<a id="layout18-table-1-row-1"></a>

**방식 정렬**

**주요 구성**

방식 정렬

**내용**

align_experiment_methods.mjs가 Blur 설계를 유지하며 GPU 모니터 필드·그래프의 호환 처리를 맞춥니다.

<a id="layout18-table-1-row-2"></a>

**조합 생성**

**주요 구성**

조합 생성

**내용**

build_block_blur_notebook.mjs가 Blur 노트북을 바탕으로 Block→Blur100조합의 설정·함수를 구성합니다.

<a id="layout18-table-1-row-3"></a>

**입력 확인**

**주요 구성**

입력 확인

**내용**

replaceOrThrow가 대상 문자열이 없으면 중단하도록 구성돼 있습니다.

<a id="layout18-table-1-row-4"></a>

**복원**

**주요 구성**

복원

**내용**

rollback_original_notebooks.mjs가 보관본과 지정 셀을 이용해 이전 구성을 복원합니다.


<a id="-이용-순서"></a>

## 이용 순서

1. paths·sourcePath·outputPath의 실제 파일을 확인합니다.
2. 수정할 셀과 replaceOrThrow의 전후 문자열을 읽습니다.
3. 원본을 별도 보관하고 출력 대상이 실행 중인 노트북이 아닌지 확인합니다.
4. 생성·수정 뒤 JSON·셀 소스와 전체 차이를 비교하고 이후 학습은 별도로 준비합니다.

| 내용 |
| --- |
| **차수·단계**<br>[폴더 2차](../../docs/revisions/folder-2.md)<br><br>**주요 내용**<br>[상세 설명](#layout18-table-2-row-1-field-1)<br><br>**자료**<br>[폴더](.)<br><br>**직전 비교**<br>[전체 비교](../../docs/revision-diffs/folder-2.diff) |

<a id="layout18-table-2-row-1-field-1"></a>

**[폴더 2차](../../docs/revisions/folder-2.md)**

**주요 내용**

기존 Blur·Block 노트북의 학습·모니터 출력을 맞추고 Block→Blur 조합 노트북을 만드는 JavaScript 보조 도구 단계입니다.


[프로젝트](../../README.md) · [전체 차수](../../docs/REVISION_INDEX.md)

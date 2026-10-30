# 📚 블록 · 1차 실험

블록 512~1의 10조건 결과 JSON입니다. 블록 수와 정확도·ROC-AUC·혼동행렬을 보존합니다.

Block512의 저장 정확도는 0.9291666666666667입니다. 블러 σ0의 0.925와 같은 실행값으로 합치지 않습니다. 각 조건은 `acc`, `roc_auc`, `per_class_acc`, `cm`, `class_names`를 담습니다. 저장 결과 JSON만으로 데이터 분할·가중치·학습 실행 전체를 복원할 수는 없습니다. 하계 원고의 보고값과 그래프 입력을 대조할 때 조건과 실행을 구분합니다.

[전체 차수](../REVISION_INDEX.md) · [첫 화면](../../README.md) · [직전 단계 전체 비교](../revision-diffs/experiment-original-block.diff) · [전체 파일 크기·해시](../revision-manifests/experiment-original-block.json)

직전 단계: 확인된 비교 대상 없음.

## 📁 실제 파일

| 파일 | 종류 | 바이트 | SHA-256 |
|---|---|---:|---|
| [원본자료/블록/1차 실험/블록 1/불록 결과/all_block_results.json](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EB%B8%94%EB%A1%9D/1%EC%B0%A8%20%EC%8B%A4%ED%97%98/%EB%B8%94%EB%A1%9D%201/%EB%B6%88%EB%A1%9D%20%EA%B2%B0%EA%B3%BC/all_block_results.json) | .json | 5040 | `a85dd325d928a5e3ae116c6d8d5ca0d06b90e632313b28ca694d81fa80cb9801` |

## 🔎 해석·검증 범위

원고는 원고 보고값, 저장된 표는 당시 결과 파일, 노트북은 구현 자료입니다. 재학습·임상 검증·전체 실행 재현은 수행하지 않았습니다. 파일 비교와 PDF 내용 확인은 실제 기능 실행의 성공을 대신하지 않습니다. 원본의 알려진 오류와 0바이트 자료는 보존하며 성공으로 보정하지 않습니다.

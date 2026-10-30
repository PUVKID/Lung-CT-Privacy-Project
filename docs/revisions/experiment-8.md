# 📚 블록+블러 · 기본

블록 재배열 뒤 입력 블러를 적용하는 ResNet50 100조합 실험입니다. 조합별 정확도·ROC-AUC·혼동행렬을 저장합니다.

### 🧩🌫️ Block→Blur 100조합

`block_blur_resnet50_v4_KO.ipynb`의 셀 8은 블록 10개와 σ 10개의 곱으로 `COMBINATIONS`를 만듭니다. 셀 10의 `generate_combined_dataset`은 블록 재배열 영상을 만든 뒤 `generate_blur_dataset`에 넘깁니다. 두 변환 모두 **입력 영상**에서 일어나며 순서는 Block→Blur입니다.

셀 20은 일반 ResNet50 분류 모델을 만들고, 셀 24는 조합별 테스트 분리 후 학습 자료 증강·fold 학습·TTA·의사 라벨 추가 학습을 구성합니다. 셀 26의 이중 반복문은 블록별로 σ를 순회하고 조건 키로 결과를 보관합니다. 출력은 조합별 정확도·ROC-AUC·클래스별 Recall·혼동행렬, 학습 이력과 조건별 그래프입니다.

이 노트북의 반복 범위는 100조합입니다. 논문의 단독 20조건은 별도 실험과 함께 읽어야 합니다. 입력 MS-SSIM Privacy Score도 별도 지표 계산 코드의 결과이며, 분류 노트북의 정확도와 같은 계산이 아닙니다. 셀 32의 예시 결과 대체와 테스트 의사 라벨 사용을 구분해 해석합니다.

셀 번호는 노트북의 전체 셀을 0부터 센 값입니다. 아래 파일 표에서 소스와 보관 결과를 각각 열 수 있습니다.

[전체 차수](../REVISION_INDEX.md) · [첫 화면](../../README.md) · [직전 단계 전체 비교](../revision-diffs/experiment-8.diff) · [전체 파일 크기·해시](../revision-manifests/experiment-8.json)

직전 단계: 확인된 비교 대상 없음.

## 📁 실제 파일

| 파일 | 종류 | 바이트 | SHA-256 |
|---|---|---:|---|
| [블록+블러/block_blur_resnet50_v4_KO.ipynb](../../%EB%B8%94%EB%A1%9D%2B%EB%B8%94%EB%9F%AC/block_blur_resnet50_v4_KO.ipynb) | .ipynb | 123969 | `42d6c2bcdf41bcff53ab1d99f6687a3fb75f0bd1bf8071565ac66952111b634a` |
| [원본자료/블록+블러/block_blur_resnet50_v4_KO.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EB%B8%94%EB%A1%9D%2B%EB%B8%94%EB%9F%AC/block_blur_resnet50_v4_KO.ipynb) | .ipynb | 124546 | `5eede93c16dcfb25d0fb60e1e3900ba0c883d3c4bb503ebb398343ec9709964d` |
| [원본자료/블록+블러/실험 완료/all_block_blur_results_resnet50_block_blur_all_combinations_v1.json](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EB%B8%94%EB%A1%9D%2B%EB%B8%94%EB%9F%AC/%EC%8B%A4%ED%97%98%20%EC%99%84%EB%A3%8C/all_block_blur_results_resnet50_block_blur_all_combinations_v1.json) | .json | 57221 | `7f3cb8aa58b2aba0ac843629ea14fbe52f35ab365ee5975e27d2127165f544b2` |

## 🔎 해석·검증 범위

원고는 원고 보고값, 저장된 표는 당시 결과 파일, 노트북은 구현 자료입니다. 재학습·임상 검증·전체 실행 재현은 수행하지 않았습니다. 파일 비교와 PDF 내용 확인은 실제 기능 실행의 성공을 대신하지 않습니다. 원본의 알려진 오류와 0바이트 자료는 보존하며 성공으로 보정하지 않습니다.

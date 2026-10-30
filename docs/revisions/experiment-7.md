# 📚 블록 · 2차 실험

입력 블록을 512~1 크기로 재배열하는 ResNet50 10조건 실험입니다. 이 사본은 증강 후 테스트를 나눕니다.

### 🧩 입력 블록 재배열과 분할 순서

`block_encryption_resnet50_rebuilt_KO.ipynb`의 셀 8은 블록 크기 512·256·128·64·32·16·8·4·2·1을 지정합니다. 셀 10의 `block_scramble`은 시드 기반 순열로 **블록 위치**를 바꾸고 블록 내부 픽셀 배열을 유지합니다. 영상보다 작지 않은 블록은 입력을 복사합니다. 이 재배열 자체에 암호학적 안전성 보증을 부여하지 않습니다.

셀 20의 분류기는 ResNet50·GAP/GMP·Dense 512·256·3클래스 softmax입니다. 셀 24는 `oversample_dir` 다음에 `prepare_split`을 호출합니다. 따라서 증강 후 테스트를 나누는 이 사본을, 원본 테스트부터 분리하는 블러·조합 사본과 동일한 평가 설정으로 묶을 수 없습니다.

평가는 fold 앙상블·TTA, 테스트 의사 라벨 추가 학습, 정확도·ROC-AUC·클래스별 Recall·혼동행렬로 이어집니다. 셀 26 이후 결과를 저장·요약하며 셀 32에는 예시 결과 대체 분기가 있습니다. 저장 JSON과 원고의 단독·조합 결과는 실행별로 대조해야 합니다.

셀 번호는 노트북의 전체 셀을 0부터 센 값입니다. 아래 파일 표에서 소스와 보관 결과를 각각 열 수 있습니다.

[전체 차수](../REVISION_INDEX.md) · [첫 화면](../../README.md) · [직전 단계 전체 비교](../revision-diffs/experiment-7.diff) · [전체 파일 크기·해시](../revision-manifests/experiment-7.json)

직전 단계: 확인된 비교 대상 없음.

## 📁 실제 파일

| 파일 | 종류 | 바이트 | SHA-256 |
|---|---|---:|---|
| [블록/2차 실험/block_encryption_resnet50_rebuilt_KO.ipynb](../../%EB%B8%94%EB%A1%9D/2%EC%B0%A8%20%EC%8B%A4%ED%97%98/block_encryption_resnet50_rebuilt_KO.ipynb) | .ipynb | 93336 | `e4526e11284c362e99634a7f3a7cd2ee3e96c79b25a8e1970d57eba31669de89` |
| [원본자료/블록/2차 실험/all_block_results_resnet50_unified_v1.json](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EB%B8%94%EB%A1%9D/2%EC%B0%A8%20%EC%8B%A4%ED%97%98/all_block_results_resnet50_unified_v1.json) | .json | 5378 | `84e93b7074555e4a421d51a9735431eda423bf83599460a9a68a318da5fe37bb` |
| [원본자료/블록/2차 실험/block_encryption_resnet50_rebuilt_KO.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EB%B8%94%EB%A1%9D/2%EC%B0%A8%20%EC%8B%A4%ED%97%98/block_encryption_resnet50_rebuilt_KO.ipynb) | .ipynb | 93336 | `e4526e11284c362e99634a7f3a7cd2ee3e96c79b25a8e1970d57eba31669de89` |

## 🔎 해석·검증 범위

원고는 원고 보고값, 저장된 표는 당시 결과 파일, 노트북은 구현 자료입니다. 재학습·임상 검증·전체 실행 재현은 수행하지 않았습니다. 파일 비교와 PDF 내용 확인은 실제 기능 실행의 성공을 대신하지 않습니다. 원본의 알려진 오류와 0바이트 자료는 보존하며 성공으로 보정하지 않습니다.

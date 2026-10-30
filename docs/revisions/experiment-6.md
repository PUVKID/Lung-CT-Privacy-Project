# 📚 블러 · 2차 실험

입력 영상에 σ0~256의 Gaussian Blur 10조건을 적용하고 ResNet50으로 분류합니다. 테스트를 먼저 분리한 뒤 학습 자료를 증강합니다.

### 🌫️ 입력 블러와 분류

`blur_resnet50_rebuilt2_KO.ipynb`의 셀 8은 σ=0·1·2·4·8·16·32·64·128·256을 지정합니다. 셀 10의 `apply_gaussian_blur`는 PIL GaussianBlur를 **입력 영상**에 적용하며 σ0은 원본 배열을 복사합니다. 특징맵 변환은 없습니다.

셀 20은 ImageNet ResNet50에 GAP·GMP 결합, Dense 512·256, 3클래스 softmax를 연결합니다. 셀 24는 테스트를 먼저 분리한 뒤 나머지를 증강하고, fold 앙상블·TTA와 고확신도 테스트 의사 라벨 추가 학습을 수행하는 구조입니다. `acc`, `roc_auc`, `per_class_acc`, `cm`을 반환하며 셀 26 이후에서 조건별 저장·요약·그래프를 처리합니다. `per_class_acc`는 혼동행렬 행 합을 분모로 한 클래스별 Recall입니다.

블록 단독 사본과 달리 테스트 분리가 증강보다 먼저입니다. 다만 증강 파생 영상의 fold 교차 가능성과 테스트 의사 라벨 사용은 남습니다. 셀 32에는 결과가 없을 때 예시 결과를 만드는 분기가 있어 그림만으로 학습 성공을 판단할 수 없습니다.

셀 번호는 노트북의 전체 셀을 0부터 센 값입니다. 아래 파일 표에서 소스와 보관 결과를 각각 열 수 있습니다.

[전체 차수](../REVISION_INDEX.md) · [첫 화면](../../README.md) · [직전 단계 전체 비교](../revision-diffs/experiment-6.diff) · [전체 파일 크기·해시](../revision-manifests/experiment-6.json)

직전 단계: 확인된 비교 대상 없음.

## 📁 실제 파일

| 파일 | 종류 | 바이트 | SHA-256 |
|---|---|---:|---|
| [블러/2차 실험/blur_resnet50_rebuilt2_KO.ipynb](../../%EB%B8%94%EB%9F%AC/2%EC%B0%A8%20%EC%8B%A4%ED%97%98/blur_resnet50_rebuilt2_KO.ipynb) | .ipynb | 102127 | `745bb2b539259819784a219ebde96df31797fad820af09cd183177e529986870` |
| [원본자료/블러/2차 실험/all_blur_results_resnet50_unified_v1.json](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EB%B8%94%EB%9F%AC/2%EC%B0%A8%20%EC%8B%A4%ED%97%98/all_blur_results_resnet50_unified_v1.json) | .json | 5326 | `a1139a82300e74f5a4c66f4c4e08cce921a2245c5bd295f402a0b4e88940e8db` |
| [원본자료/블러/2차 실험/blur_resnet50_rebuilt2_KO.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EB%B8%94%EB%9F%AC/2%EC%B0%A8%20%EC%8B%A4%ED%97%98/blur_resnet50_rebuilt2_KO.ipynb) | .ipynb | 102127 | `745bb2b539259819784a219ebde96df31797fad820af09cd183177e529986870` |

## 🔎 해석·검증 범위

원고는 원고 보고값, 저장된 표는 당시 결과 파일, 노트북은 구현 자료입니다. 재학습·임상 검증·전체 실행 재현은 수행하지 않았습니다. 파일 비교와 PDF 내용 확인은 실제 기능 실행의 성공을 대신하지 않습니다. 원본의 알려진 오류와 0바이트 자료는 보존하며 성공으로 보정하지 않습니다.

# 📚 블러 엣지 · 기본

입력 블러 10조건에 ResNet50 edge/cloud 분리를 더했습니다. pool1_pool 특징 그림과 부분 모델을 저장하며, 셀 20 문법 오류가 남아 있습니다.

### 🌫️ 입력 블러를 사용하는 분리 모델

`blur_resnet50_edge_v6.ipynb`의 셀 8·10은 입력 영상 Gaussian Blur 10조건을 구성합니다. 셀 20의 `build_edge_model`은 ResNet50의 `pool1_pool`까지, `build_cloud_model`은 그 뒤와 분류 헤드를 구성합니다. 512×512 입력에서 경계 특징은 128×128×64이며, `build_full_pipeline`이 두 부분을 같은 TensorFlow 프로세스에서 연결합니다. 경계 특징에 별도 블러를 넣는 Stage 1 실험과 구분됩니다.

셀 24는 처음부터 두 부분의 학습을 허용하고 증강 후 테스트 분리·fold 앙상블·TTA·테스트 의사 라벨 경로를 사용합니다. edge 가중치와 cloud 모델을 따로 저장하고, 셀 20·26의 특징 저장 함수는 σ별 특징 시각화를 구성합니다. 분류 결과에는 정확도·ROC-AUC·클래스별 Recall·혼동행렬이 포함됩니다.

셀 20의 문자열 개행 문법 오류가 남아 있어 현재 소스를 그대로 일괄 실행할 수 없습니다. `training=True` 고정 호출, 가중치 저장 순서, 예시 그래프 분기도 실행 전 점검 대상입니다. 부분 모델 저장은 네트워크 전송·원격 배포·통신 지연 검증을 뜻하지 않습니다.

셀 번호는 노트북의 전체 셀을 0부터 센 값입니다. 아래 파일 표에서 소스와 보관 결과를 각각 열 수 있습니다.

[전체 차수](../REVISION_INDEX.md) · [첫 화면](../../README.md) · [직전 단계 전체 비교](../revision-diffs/experiment-9.diff) · [전체 파일 크기·해시](../revision-manifests/experiment-9.json)

직전 단계: 확인된 비교 대상 없음.

## 📁 실제 파일

| 파일 | 종류 | 바이트 | SHA-256 |
|---|---|---:|---|
| [블러 엣지/blur_resnet50_edge_v6.ipynb](../../%EB%B8%94%EB%9F%AC%20%EC%97%A3%EC%A7%80/blur_resnet50_edge_v6.ipynb) | .ipynb | 107890 | `288f61b77fd0de8e2f58db351109f9431148c7618fed92fdf13847ed9bab104c` |
| [원본자료/블러 엣지/all_blur_results_resnet50_same_settings_gpu4090_v2.json](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EB%B8%94%EB%9F%AC%20%EC%97%A3%EC%A7%80/all_blur_results_resnet50_same_settings_gpu4090_v2.json) | .json | 5000 | `d60283d59f7b3c72f4226b204b25fb30b87213ad65ddd50289d5f15b5e66de54` |
| [원본자료/블러 엣지/blur_resnet50_edge_v6.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EB%B8%94%EB%9F%AC%20%EC%97%A3%EC%A7%80/blur_resnet50_edge_v6.ipynb) | .ipynb | 648837 | `b4d702c5b26a383db7406e0e7438316f8f1698dc370a92cea38c7eb843186392` |

## 🔎 해석·검증 범위

원고는 원고 보고값, 저장된 표는 당시 결과 파일, 노트북은 구현 자료입니다. 재학습·임상 검증·전체 실행 재현은 수행하지 않았습니다. 파일 비교와 PDF 내용 확인은 실제 기능 실행의 성공을 대신하지 않습니다. 원본의 알려진 오류와 0바이트 자료는 보존하며 성공으로 보정하지 않습니다.

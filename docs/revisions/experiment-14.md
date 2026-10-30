# 📚 추가 학습모델과 실험 · 기본

EfficientNetV2-S 변환 비교, MobileNetV2 풀링, ResNet50 사본과 SSIM/MS-SSIM 계산·도표를 모았습니다. 셀별 실험을 구분합니다.

### 🧪 학습·지표·도표를 모은 실험 묶음

`Train.ipynb`는 하나의 연속 학습 절차가 아닙니다. 셀 0은 `lung_colon_image_set`의 조직영상 5클래스 학습과 `Model.h5` 저장을 다룹니다. 셀 1·2는 각각 EfficientNetV2-S의 입력 블록·블러 10조건 CT 3분류입니다. 셀 3~5는 MobileNetV2와 풀링·특징 수 비교이며 224×224와 512×512 설정이 섞여 있습니다. 정확도 또는 특징 수 비율에서 만든 `security`는 실제 공격 저항성 측정값이 아닙니다. 첫 셀 끝의 Markdown 백틱 때문에 문법 수정도 필요합니다.

ResNet50 단독·조합·edge·Stage 1 노트북 사본은 각 실험 설명과 함께 읽습니다. `Blur_Block_1차_그래프_white.ipynb`는 저장 JSON을 그리는 자료이고 `heatmaps.py`는 코드에 있는 결과표를 시각화합니다. 도표 재생성은 분류 모델 재학습과 구별됩니다.

`privacy_score_ssim_psnr.ipynb`와 `(1)`·백업은 단일 SSIM·PSNR 계산 경로를, `privacy_score_ssim_psnr_updated.ipynb`는 셀 15의 `compute_ms_ssim` 및 `privacy_score_from_ms_ssim`을 포함합니다. 후자는 입력 영상의 5스케일 MS-SSIM으로 점수를 계산하고 셀 23에서 CSV·JSON·Excel 및 조건별 요약표를 내보냅니다. `updated`의 일부 그래프 축에는 이전 SSIM 표기가 남아 있어 계산 함수와 표의 지표 열을 기준으로 구분해야 합니다.

`privacy_score_quantitative_docker_vscode.ipynb`와 저장된 `privacy_score_outputs`는 계산·집계 자료입니다. 파일 이름만으로 논문의 전체 1,097장 평가와 같은 실행이라고 간주하지 않습니다. 원본 폴더 3차의 n_images=3 소규모 검사도 별도 차수로 유지합니다.

셀 번호는 노트북의 전체 셀을 0부터 센 값입니다. 아래 파일 표에서 소스와 보관 결과를 각각 열 수 있습니다.

[전체 차수](../REVISION_INDEX.md) · [첫 화면](../../README.md) · [직전 단계 전체 비교](../revision-diffs/experiment-14.diff) · [전체 파일 크기·해시](../revision-manifests/experiment-14.json)

직전 단계: 확인된 비교 대상 없음.

## 📁 실제 파일

| 파일 | 종류 | 바이트 | SHA-256 |
|---|---|---:|---|
| [추가 학습모델과 실험/block_blur_resnet50_edge.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/block_blur_resnet50_edge.ipynb) | .ipynb | 147769 | `00f076b8f3f842398c3abfbfd3984fca4cb984c619d05a04f4a7affc5c101cbb` |
| [추가 학습모델과 실험/block_blur_resnet50_v4_KO.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/block_blur_resnet50_v4_KO.ipynb) | .ipynb | 136449 | `efdb4bc4e54aef87ca99b2acca4bd36c4f49093351d613ca254c6ddf90de46fc` |
| [추가 학습모델과 실험/block_encryption_resnet50_edge_v2.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/block_encryption_resnet50_edge_v2.ipynb) | .ipynb | 120967 | `487f9f127c9e7c83d6bfa47b9f165858cc7d7f1630fc83cbd1b0be99070cb6e4` |
| [추가 학습모델과 실험/block_encryption_resnet50_rebuilt_KO.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/block_encryption_resnet50_rebuilt_KO.ipynb) | .ipynb | 108653 | `3daed3071f6399ccc1edff47b8925bf31d39ee9a74fc9478f3ec6bee773393af` |
| [추가 학습모델과 실험/Blur_Block_1차_그래프_white.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/Blur_Block_1%EC%B0%A8_%EA%B7%B8%EB%9E%98%ED%94%84_white.ipynb) | .ipynb | 52637 | `6d0db255fee2dc5aa25aee28f86b5c96fbe9a3dcf0dc12aa6747fbe01d9615aa` |
| [추가 학습모델과 실험/blur_resnet50_edge_v6.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/blur_resnet50_edge_v6.ipynb) | .ipynb | 119871 | `20fe0e593c391887e2d2e346f1fe4c15b3e5cf3f0908783bb895e90ea571f51f` |
| [추가 학습모델과 실험/blur_resnet50_rebuilt2_KO.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/blur_resnet50_rebuilt2_KO.ipynb) | .ipynb | 102127 | `745bb2b539259819784a219ebde96df31797fad820af09cd183177e529986870` |
| [추가 학습모델과 실험/heatmaps.py](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/heatmaps.py) | .py | 5522 | `640b4514d3f218a84c2030b8d3868611ce48a37ef9cf46f93a1be5f0dba73420` |
| [추가 학습모델과 실험/paper_figures_resnet50.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/paper_figures_resnet50.ipynb) | .ipynb | 24466 | `3f3cf3e396737690701969ced7982cff12f001fc7f05e6201d065a807f89aa0d` |
| [추가 학습모델과 실험/plot_privacy_metrics_split.py](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/plot_privacy_metrics_split.py) | .py | 5450 | `3a25a124e4a88e663a675d8791660ecdc61468a3b260bc4e8588e78c994cbcb9` |
| [추가 학습모델과 실험/privacy_score_quantitative_docker_vscode.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/privacy_score_quantitative_docker_vscode.ipynb) | .ipynb | 37525 | `9d9c636cfb43dd76cf562e4cf378581748aaf8cd88fbcc2eac516be8ed3858a7` |
| [추가 학습모델과 실험/privacy_score_ssim_psnr (1).ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/privacy_score_ssim_psnr%20%281%29.ipynb) | .ipynb | 29338 | `276cfc4297f975d48eb3e6bcf0a5acac98b6d207ba5d30c2c4f849c5cd3e0434` |
| [추가 학습모델과 실험/privacy_score_ssim_psnr (1)_backup_before_ssim_only_20260825_005153.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/privacy_score_ssim_psnr%20%281%29_backup_before_ssim_only_20260825_005153.ipynb) | .ipynb | 29338 | `276cfc4297f975d48eb3e6bcf0a5acac98b6d207ba5d30c2c4f849c5cd3e0434` |
| [추가 학습모델과 실험/privacy_score_ssim_psnr.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/privacy_score_ssim_psnr.ipynb) | .ipynb | 26824 | `05f77ac6b7d7b91eb0d0e8ada4aa746ca7654cc5a8554739aea163ea2eab63b5` |
| [추가 학습모델과 실험/privacy_score_ssim_psnr_updated.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/privacy_score_ssim_psnr_updated.ipynb) | .ipynb | 52527 | `e0ce3aa6dd0a1fa307eea53cb1a2253266431a2ab0d86b984d72010aafc2c6ef` |
| [추가 학습모델과 실험/stage1_edge_feature_blur_resnet50.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/stage1_edge_feature_blur_resnet50.ipynb) | .ipynb | 136778 | `a32e79c0ef1e8386c1148e4761c3c61554316b7be55117377939a932f5f5be8f` |
| [추가 학습모델과 실험/Train.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/Train.ipynb) | .ipynb | 315835 | `df318f23b1a07b5307ab4043d89bce8206eccf6fd27053efe8c06268ce24f771` |
| [원본자료/추가 학습모델과 실험/all_block_results.json](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/all_block_results.json) | .json | 5040 | `a85dd325d928a5e3ae116c6d8d5ca0d06b90e632313b28ca694d81fa80cb9801` |
| [원본자료/추가 학습모델과 실험/block_blur_resnet50_edge.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/block_blur_resnet50_edge.ipynb) | .ipynb | 148347 | `ae3e302e19d2db72ce572ec48cf3d0301b4b4011866a43a5e206a8e1097033a9` |
| [원본자료/추가 학습모델과 실험/block_encryption_resnet50_edge_v2.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/block_encryption_resnet50_edge_v2.ipynb) | .ipynb | 168661 | `90b3a37cc1f8fa3152f45c77e803c38db5b14f46d0aaa268d4bdb05b9acbc23a` |
| [원본자료/추가 학습모델과 실험/block_encryption_resnet50_rebuilt_KO.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/block_encryption_resnet50_rebuilt_KO.ipynb) | .ipynb | 138317 | `4233928cb2aba1e9e1306e02ffc8a7cf5f17e62b72b83ccc2e8ec228c592c80f` |
| [원본자료/추가 학습모델과 실험/Blur_Block_1차_그래프_white.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/Blur_Block_1%EC%B0%A8_%EA%B7%B8%EB%9E%98%ED%94%84_white.ipynb) | .ipynb | 59418 | `6ed385e04f1e500f3f1c57c7eb272a5bdd1ce9a4013d203b87fa6891ba830a50` |
| [원본자료/추가 학습모델과 실험/blur_resnet50_edge_v6.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/blur_resnet50_edge_v6.ipynb) | .ipynb | 169241 | `539e5539a73d019912257aafde527c501e7735cd6fbbfa48b26f1d2ab5c27eda` |
| [원본자료/추가 학습모델과 실험/blur_resnet50_rebuilt2_KO.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/blur_resnet50_rebuilt2_KO.ipynb) | .ipynb | 132788 | `90c8e0f7a25c4533dc2b6759fa295bc7d758dd256330367d7c395dff2bee0d4f` |
| [원본자료/추가 학습모델과 실험/heatmaps.py](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/heatmaps.py) | .py | 5522 | `640b4514d3f218a84c2030b8d3868611ce48a37ef9cf46f93a1be5f0dba73420` |
| [원본자료/추가 학습모델과 실험/paper_figures_resnet50.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/paper_figures_resnet50.ipynb) | .ipynb | 24465 | `f19095c9cfe4ee0e8441768135de6563eadc26451a760c5b13981703013b733c` |
| [원본자료/추가 학습모델과 실험/plot_privacy_metrics_split.py](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/plot_privacy_metrics_split.py) | .py | 5450 | `3a25a124e4a88e663a675d8791660ecdc61468a3b260bc4e8588e78c994cbcb9` |
| [원본자료/추가 학습모델과 실험/privacy_score_quantitative_docker_vscode.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/privacy_score_quantitative_docker_vscode.ipynb) | .ipynb | 38472 | `862bff744ac2f97bbfad309bb72a60349ca46e39388dba2810f911d966c91dd7` |
| [원본자료/추가 학습모델과 실험/privacy_score_ssim_psnr (1).ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/privacy_score_ssim_psnr%20%281%29.ipynb) | .ipynb | 54595 | `3474c6ad8fdbda957d99f2d921a68af01248ca6336395d499ee4a92e1ef9572c` |
| [원본자료/추가 학습모델과 실험/privacy_score_ssim_psnr (1)_backup_before_ssim_only_20260825_005153.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/privacy_score_ssim_psnr%20%281%29_backup_before_ssim_only_20260825_005153.ipynb) | .ipynb | 54595 | `fac8097fe5bdf91303bba90801e379b479150bd06ecc2a4ae67d80d8e1d7810a` |
| [원본자료/추가 학습모델과 실험/privacy_score_ssim_psnr.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/privacy_score_ssim_psnr.ipynb) | .ipynb | 26823 | `0657ef57f42a0f08539a4809517cb7668a0014f00a87e4d176ff6364a61f22f0` |
| [원본자료/추가 학습모델과 실험/privacy_score_ssim_psnr_updated.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/privacy_score_ssim_psnr_updated.ipynb) | .ipynb | 96269 | `74cb8eb330d2a60c357ff4806f3d4a5c3aeefb3f5f3cc2c0b188d792decb863a` |
| [원본자료/추가 학습모델과 실험/stage1_edge_feature_blur_resnet50.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/stage1_edge_feature_blur_resnet50.ipynb) | .ipynb | 136778 | `a32e79c0ef1e8386c1148e4761c3c61554316b7be55117377939a932f5f5be8f` |
| [원본자료/추가 학습모델과 실험/Train.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/Train.ipynb) | .ipynb | 315835 | `df318f23b1a07b5307ab4043d89bce8206eccf6fd27053efe8c06268ce24f771` |
| [원본자료/추가 학습모델과 실험/privacy_score_outputs/privacy_scores.csv](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/privacy_score_outputs/privacy_scores.csv) | .csv | 22820 | `02561595bba02a4a53890867a54f6f22111af4d986aef58ede7aff8cbeba9e69` |
| [원본자료/추가 학습모델과 실험/privacy_score_outputs/privacy_scores.json](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/privacy_score_outputs/privacy_scores.json) | .json | 45067 | `bcf31f719a941652bfb77d3f952e8c7f52687cb03115f04c44e16c72361bc36b` |
| [원본자료/추가 학습모델과 실험/privacy_score_outputs/privacy_scores.xlsx](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/privacy_score_outputs/privacy_scores.xlsx) | .xlsx | 21554 | `1045b2c09cebc7092dbb20563ec6bd0c76238695e42ce0d414a5969c5106cd98` |
| [원본자료/추가 학습모델과 실험/privacy_score_outputs/tables/best_by_type.csv](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/privacy_score_outputs/tables/best_by_type.csv) | .csv | 728 | `823dc8104c8aa1cebae6b4eeb2ee745997ab2c77ab155a15830e0cd54fc00f6f` |
| [원본자료/추가 학습모델과 실험/privacy_score_outputs/tables/selected_images.csv](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/privacy_score_outputs/tables/selected_images.csv) | .csv | 117495 | `6153b9d964ed487924ecfa96cd75fa3898ad05be54bcb28942f0925a9feee9c1` |
| [원본자료/추가 학습모델과 실험/privacy_score_outputs/tables/summary_by_type.csv](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/privacy_score_outputs/tables/summary_by_type.csv) | .csv | 407 | `aca5a2d0b0ddcb21e0f1aa39d0f60cf9919eaada24dcd00d86cd0ffe653c2437` |

## 🔎 해석·검증 범위

원고는 원고 보고값, 저장된 표는 당시 결과 파일, 노트북은 구현 자료입니다. 재학습·임상 검증·전체 실행 재현은 수행하지 않았습니다. 파일 비교와 PDF 내용 확인은 실제 기능 실행의 성공을 대신하지 않습니다. 원본의 알려진 오류와 0바이트 자료는 보존하며 성공으로 보정하지 않습니다.

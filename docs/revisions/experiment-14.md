<div align="center">

# 🧪 추가 실험 · 학습·유사도·도표 코드 모음

**EfficientNetV2-S·MobileNetV2·ResNet50의 서로 다른 학습 셀과 SSIM/MS-SSIM·도표 코드를 모은 자료입니다.**

**기술 분류:** 실험 코드 모음 › TensorFlow·영상 유사도 › 학습·지표·그래프

[목적](#purpose) · [기능](#features) · [입출력](#flow) · [구성](#files) · [준비](#setup) · [사용법](#usage) · [결과](#results) · [제약](#limits) · [변경](#changes)

</div>

<a name="purpose"></a>

## 🎯 이 단계에서 하는 일

모델·입력 종류·크기·점수식·변환 위치가 다른 코드를 목적에 맞게 선택해 읽습니다. 모든 셀을 하나의 연속된 학습으로 실행하는 구성은 아닙니다.

<a name="features"></a>

## 🧩 주요 기능과 처리 방식

| 구성 | 실제 역할 |
| --- | --- |
| Train.ipynb | 셀 0은 조직영상 5클래스, 셀 1·2는 EfficientNetV2-S의 CT 블록·블러, 셀 3~5는 MobileNetV2와 풀링 비교입니다. |
| ResNet50 사본 | 단독·조합·edge·Stage1 특징 블러 노트북을 각각 구분합니다. |
| 유사도 코드 | SSIM·PSNR·MS-SSIM과 DSSIM 기반 점수의 여러 버전을 보관합니다. |
| 도표 | 저장된 분류 JSON과 유사도 CSV에서 막대·히트맵·논문 그림을 구성합니다. |

<a name="flow"></a>

## 🔄 입력 → 처리 → 출력

| 입력 | 처리 | 출력·읽을 결과 |
| --- | --- | --- |
| 선택한 모델·영상 | 해당 셀의 학습·분류 | 모델별 결과 |
| 원본·변환 영상 | SSIM·PSNR·MS-SSIM 계산 | 정의가 다른 유사도 지표 |
| 저장 결과 | 조건 대조와 도표 작성 | 표·그림 |

<a name="files"></a>

## 📁 파일과 핵심 처리

| 파일 | 이용 방법 |
| --- | --- |
| [추가 학습모델과 실험/Train.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/Train.ipynb) | 설정·함수·실행 셀 |
| [추가 학습모델과 실험/privacy_score_ssim_psnr_updated.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/privacy_score_ssim_psnr_updated.ipynb) | 설정·함수·실행 셀 |
| [추가 학습모델과 실험/privacy_score_quantitative_docker_vscode.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/privacy_score_quantitative_docker_vscode.ipynb) | 설정·함수·실행 셀 |
| [추가 학습모델과 실험/paper_figures_resnet50.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/paper_figures_resnet50.ipynb) | 설정·함수·실행 셀 |

### 🔎 함수·셀로 찾아가기

아래 이름은 해당 파일의 실제 정의입니다. 위 처리 설명과 함께 설정·호출 순서·출력 경로를 따라 읽습니다.

| 파일 | 핵심 정의 |
| --- | --- |
| [추가 학습모델과 실험/Train.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/Train.ipynb) | 셀 1: `block_scramble` · `generate_block_dataset` · `oversample_dir` · `prepare_split` · `get_paths_labels` · `load_image` · `augment_train` · `cutmix_batch`<br>셀 2: `apply_gaussian_blur` · `generate_blur_dataset` · `oversample_dir` · `prepare_split` · `get_paths_labels` · `load_image` · `augment_train` · `cutmix_batch`<br>셀 3: `oversample_dir` · `style_ax`<br>셀 4: `style_ax` · `oversample_dir`<br>셀 5: `style_ax` · `oversample_dir` |
| [추가 학습모델과 실험/privacy_score_ssim_psnr_updated.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/privacy_score_ssim_psnr_updated.ipynb) | 셀 9: `save_condition_sample`<br>셀 11: `block_scramble` · `apply_gaussian_blur`<br>셀 13: `_is_image_file` · `_is_ignored_path` · `collect_image_files` · `load_original_images`<br>셀 15: `_to_gray` · `_downsample_avg2x2` · `_ssim_l_cs` · `compute_ms_ssim` · `compute_ssim_psnr_msssim` · `privacy_score_from_ms_ssim` · `evaluate_condition`<br>셀 21: `combo_fn`<br>셀 25: `_save` · `_annotate_bars`<br>셀 38: `_combo_transform` |
| [추가 학습모델과 실험/privacy_score_quantitative_docker_vscode.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/privacy_score_quantitative_docker_vscode.ipynb) | 셀 6: `path_exists` · `candidate_train_dirs` · `should_ignore` · `count_images_under`<br>셀 8: `collect_image_table`<br>셀 10: `setup_matplotlib_font` · `load_rgb_image` · `block_scramble` · `apply_gaussian_blur` · `apply_transform`<br>셀 12: `compute_pair_metrics` · `load_image_records` · `iter_records` · `evaluate_condition` · `condition_name` · `format_sigma`<br>셀 18: `save_fig`<br>셀 20: `save_table_png`<br>셀 22: `parse_condition` |
| [추가 학습모델과 실험/paper_figures_resnet50.ipynb](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/paper_figures_resnet50.ipynb) | 셀 4: `_bar_colors` · `plot_clean_bar`<br>셀 6: `_try_load_json`<br>셀 12: `_try_load_privacy_csv`<br>셀 20: `encryption_strength` |

<a name="setup"></a>

## ⚙️ 환경과 설정

| 항목 | 조건·기본값 |
| --- | --- |
| 입력 크기 | 코드별 224 또는 512 |
| 점수식 | SSIM과 MS-SSIM 기반 변형을 구분 |
| 모델 | 조직영상·CT 모델과 클래스 수를 각 셀에서 확인 |
| 실행 | 선택한 입력·가중치·패키지·GPU를 준비 |

<a name="usage"></a>

## 🚀 준비와 사용 순서

1. 분류 학습·유사도 계산·도표 중 목적을 먼저 정합니다.
2. 선택한 셀의 모델·영상 종류·크기·클래스와 입력 경로를 확인합니다.
3. 설치·데이터 생성·학습·파일 쓰기 셀을 구분합니다.
4. 지표식과 캐시·출력 파일을 읽고 같은 조건의 결과만 비교합니다.

<a name="results"></a>

## 📊 결과를 읽는 방법

Train.ipynb에는 정확도나 특징 수의 비율로 만든 security 표현도 있습니다. 이 값은 실제 공격 저항성 평가와 다릅니다.

첫 학습 셀 끝의 Markdown 백틱과 사본별 문법·설정 차이를 확인해야 합니다. 후속 논문 보고값과 여러 실험 코드를 한 번의 동일 실행으로 합치지 않습니다.

<a name="limits"></a>

## 🛠️ 알려진 제약과 확인 지점

| 상황 | 확인할 내용 |
| --- | --- |
| 셀 독립성 | 입력 종류·모델·클래스가 달라 모든 셀을 같은 학습으로 연속 실행하지 않습니다. |
| 점수 정의 | 유사도·정확도·특징 수 비율로 만든 값은 서로 다른 지표입니다. |
| 문법 | Train 첫 셀 끝의 백틱과 각 노트북의 구문을 확인합니다. |

<a name="changes"></a>

## 🔀 이전 단계와의 변화

분류·유사도·도표의 추가 연구 코드를 모은 묶음입니다. 단독 실험·조합 실험·특징 변환과 각각 연결합니다.

[🔎 직전 단계 전체 비교·구성](../revision-diffs/experiment-14.diff) · [📋 전체 파일 크기·해시](../revision-manifests/experiment-14.json)

<details>
<summary>📎 이 단계의 파일 기록과 전체 해시</summary>

아래 표는 해당 단계가 기록될 당시의 파일 정보입니다. 현재 첨부는 [프로젝트 자료 안내](../PAPERS.md)에서 확인할 수 있습니다.

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

</details>

---

[🏠 프로젝트](../../README.md) · [🗂️ 전체 차수](../REVISION_INDEX.md) · [📁 자료 폴더](../../%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98)

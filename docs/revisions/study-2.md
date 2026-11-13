<a id="-연구-2--resnet50의-프라이버시정확도-절충"></a>

# 연구 2 · ResNet50의 프라이버시·정확도 절충

ResNet50에서 Block·Blur 단독 20조건과 Block→Blur 조합 100조건을 비교하고, 분류 정확도와 영상 유사도 기반 점수를 함께 읽는 19쪽 후속 원고입니다.

분야: 의료 영상 연구 › ResNet50 분류 › MS-SSIM·프라이버시·정확도 절충

[목적](#purpose) · [기능](#features) · [입출력](#flow) · [구성](#files) · [준비](#setup) · [사용법](#usage) · [결과](#results) · [제약](#limits) · [변경](#changes)

<a name="purpose"></a>

<a id="-이-단계에서-하는-일"></a>

## 연구 목적

정확도를 가장 높게 유지하는 조건과 원본 영상의 구조를 더 많이 바꾸는 조건을 한 지표로 섞지 않고 Pareto 관점에서 비교합니다. 영상 입력 변환과 특징맵 변환의 후속 코드도 구분합니다.

<a name="features"></a>

<a id="-주요-기능과-처리-방식"></a>

## 방법과 구현

| 구성 | 실제 역할 |
| --- | --- |
| 단독·조합 | 블록 10개·블러 10개와 Block→Blur100조합을 비교합니다. |
| 분류 평가 | 정확도·macro OvR ROC-AUC·클래스별 Recall·혼동행렬을 봅니다. |
| 영상 유사도 | 입력 1,097장에 대한 MS-SSIM과 Privacy Score를 정리합니다. |
| 절충 분석 | 정확도와 구조 변화의 두 축에서 조건을 선택하는 Pareto 결과를 읽습니다. |

<a name="flow"></a>

<a id="-입력--처리--출력"></a>

## 입력·처리·출력

| 입력 | 처리 | 출력 |
| --- | --- | --- |
| CT와 변환 조건 | Block→Blur 입력 생성 | 조건별 영상 |
| 조건별 영상 | ResNet50 분류와 원본/변환 유사도 계산 | 정확도·MS-SSIM |
| 두 지표 | Privacy Score·Pareto 비교 | 조건 선택의 장단점 |

<a name="files"></a>

<a id="-파일과-핵심-처리"></a>

## 파일별 역할

| 파일 | 이용 방법 |
| --- | --- |
| [논문/연구 2_원문_최종.pdf](../../%EB%85%BC%EB%AC%B8/%EC%97%B0%EA%B5%AC2_%EC%9B%90%EB%AC%B8_%EC%B5%9C%EC%A2%85.pdf) | 전체 원문·도표 읽기 |
| [논문/연구 2_원문_최종.hwp](../../%EB%85%BC%EB%AC%B8/%EC%97%B0%EA%B5%AC2_%EC%9B%90%EB%AC%B8_%EC%B5%9C%EC%A2%85.hwp) | 같은 판의 편집 원본 |
| [자료차수/4차/코드/privacy_score_ssim_psnr_updated.ipynb](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/4%EC%B0%A8/%EC%BD%94%EB%93%9C/privacy_score_ssim_psnr_updated.ipynb) | 설정·함수·실행 셀 |

<a id="-함수셀로-찾아가기"></a>

### 관련 함수와 셀

관련 함수와 셀을 파일별로 정리했습니다. 실행 전 설정과 호출 순서, 출력 경로를 확인하세요.

| 파일 | 핵심 정의 |
| --- | --- |
| [자료차수/4차/코드/privacy_score_ssim_psnr_updated.ipynb](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/4%EC%B0%A8/%EC%BD%94%EB%93%9C/privacy_score_ssim_psnr_updated.ipynb) | 셀 9: `save_condition_sample`<br>셀 11: `block_scramble` · `apply_gaussian_blur`<br>셀 13: `_is_image_file` · `_is_ignored_path` · `collect_image_files` · `load_original_images`<br>셀 15: `_to_gray` · `_downsample_avg2x2` · `_ssim_l_cs` · `compute_ms_ssim` · `compute_ssim_psnr_msssim` · `privacy_score_from_ms_ssim` · `evaluate_condition`<br>셀 21: `combo_fn`<br>셀 25: `_save` · `_annotate_bars`<br>셀 38: `_combo_transform` |

<a name="setup"></a>

<a id="️-환경과-설정"></a>

## 실행 환경과 설정

| 항목 | 조건·기본값 |
| --- | --- |
| 원고 | 19쪽 최종 PDF/HWP |
| 조건 | 단독 20·조합 100 |
| 유사도 입력 | 원고의 전체 1,097장 |
| 점수식 | Privacy Score=((1−MS-SSIM)/2)×100 |

<a name="usage"></a>

<a id="-읽고-활용하는-순서"></a>

## 원고 읽기

1. 원고의 데이터·분할·모델 조건을 연구 1과 별도로 확인합니다.
2. 단독·조합 결과표에서 조건명과 분류 지표를 읽습니다.
3. MS-SSIM 계산과 Privacy Score 변환식을 확인합니다.
4. 정확도·점수의 산점도와 Pareto 조건을 함께 보며 선택 근거를 읽습니다.

<a name="results"></a>

<a id="-결과를-읽는-방법"></a>

## 결과와 해석

원고는 원본 정확도 98.17%와 Block256+σ0의 98.17%·Privacy Score49.65점 등을 보고합니다. 모델 변경만으로 연구 1 대비 차이의 원인을 확정하지 않습니다.

Privacy Score는 원본과 변환 영상의 구조적 차이에서 만든 상대 지표입니다. 복원 공격·신원 재식별·암호학적 안전성을 직접 측정한 값과 구분합니다.

<a name="limits"></a>

<a id="️-알려진-제약과-확인-지점"></a>

## 제약과 확인 사항

| 상황 | 확인할 내용 |
| --- | --- |
| 점수 정의 | SSIM 기반 소규모 점검 자료와 최종 MS-SSIM 점수식을 구분합니다. |
| 기준 영상 | 의료 원영상은 별도로 준비해야 하며 공개 첨부에 포함하지 않습니다. |
| 후속 코드 | pool1_pool 특징 블러·복원 코드를 원고의 입력 변환 실험 결과와 섞지 않습니다. |

<a name="changes"></a>

<a id="-이전-단계와의-변화"></a>

## 직전 단계와 비교

연구 1의 입력 변환 질문에서 ResNet50·조합·영상 유사도 절충 분석으로 확장한 별도 후속 논문입니다.

[직전 단계 전체 비교·구성](../revision-diffs/study-2.diff) · [전체 파일 크기·해시](../revision-manifests/study-2.json)

<details>
<summary>이 단계의 파일 기록과 전체 해시</summary>

아래 표는 해당 단계가 기록될 당시의 파일 정보입니다. 현재 첨부는 [프로젝트 자료 안내](../PAPERS.md)에서 확인할 수 있습니다.

| 파일 | 종류 | 바이트 | SHA-256 |
|---|---|---:|---|
| `논문/2차_ResNet50_최종.pdf` | .pdf | 2827829 | `b64645277f78ac2b2c87a1dcc15216ec9ad6c41a5a20f795465748ac0d2f76c7` |
| [폐암 2차 논문/코드/block_blur_resnet50_v4_KO.ipynb](../../%ED%8F%90%EC%95%94%202%EC%B0%A8%20%EB%85%BC%EB%AC%B8/%EC%BD%94%EB%93%9C/block_blur_resnet50_v4_KO.ipynb) | .ipynb | 136449 | `efdb4bc4e54aef87ca99b2acca4bd36c4f49093351d613ca254c6ddf90de46fc` |
| [폐암 2차 논문/코드/block_encryption_resnet50_rebuilt_KO.ipynb](../../%ED%8F%90%EC%95%94%202%EC%B0%A8%20%EB%85%BC%EB%AC%B8/%EC%BD%94%EB%93%9C/block_encryption_resnet50_rebuilt_KO.ipynb) | .ipynb | 108653 | `3daed3071f6399ccc1edff47b8925bf31d39ee9a74fc9478f3ec6bee773393af` |
| [폐암 2차 논문/코드/blur_resnet50_rebuilt2_KO.ipynb](../../%ED%8F%90%EC%95%94%202%EC%B0%A8%20%EB%85%BC%EB%AC%B8/%EC%BD%94%EB%93%9C/blur_resnet50_rebuilt2_KO.ipynb) | .ipynb | 102127 | `745bb2b539259819784a219ebde96df31797fad820af09cd183177e529986870` |
| [폐암 2차 논문/코드/heatmaps_windows.ipynb](../../%ED%8F%90%EC%95%94%202%EC%B0%A8%20%EB%85%BC%EB%AC%B8/%EC%BD%94%EB%93%9C/heatmaps_windows.ipynb) | .ipynb | 8407 | `e64d162310d50c96a5ba1e39c44fce4702fad38abbf7c08c7a8eaf7b79582590` |
| [폐암 2차 논문/코드/paper_figures_resnet50.ipynb](../../%ED%8F%90%EC%95%94%202%EC%B0%A8%20%EB%85%BC%EB%AC%B8/%EC%BD%94%EB%93%9C/paper_figures_resnet50.ipynb) | .ipynb | 27771 | `4e52342e6d8a025549a37bf1e16fbd94f2d2a76d95cc0e039e703d6d1fc911ce` |
| [폐암 2차 논문/코드/picture2x2.ipynb](../../%ED%8F%90%EC%95%94%202%EC%B0%A8%20%EB%85%BC%EB%AC%B8/%EC%BD%94%EB%93%9C/picture2x2.ipynb) | .ipynb | 6594 | `d6ddecbbd7dfd747b83fefe3be920bef1a0597ae3413de936eb7cb27fe4cceb5` |
| [폐암 2차 논문/코드/plot_privacy_metrics_split.ipynb](../../%ED%8F%90%EC%95%94%202%EC%B0%A8%20%EB%85%BC%EB%AC%B8/%EC%BD%94%EB%93%9C/plot_privacy_metrics_split.ipynb) | .ipynb | 18339 | `6341212d374e771b81529b92f66f672ad66eac891240932b8b49a1c79ef98b0a` |
| [폐암 2차 논문/코드/privacy_score_ssim_psnr_updated.ipynb](../../%ED%8F%90%EC%95%94%202%EC%B0%A8%20%EB%85%BC%EB%AC%B8/%EC%BD%94%EB%93%9C/privacy_score_ssim_psnr_updated.ipynb) | .ipynb | 52527 | `e0ce3aa6dd0a1fa307eea53cb1a2253266431a2ab0d86b984d72010aafc2c6ef` |
| `논문/연구2_원문_최종.pdf` | .pdf | 2865864 | `58249752c657a4aad13b94d7860bb2d977e897e779e72a9f9e8d6306a60652fe` |
| [최신 편집 원문](../../%EB%85%BC%EB%AC%B8/%EC%97%B0%EA%B5%AC2_%EC%9B%90%EB%AC%B8_%EC%B5%9C%EC%A2%85.hwp) | .hwp | 4908032 | `14d42c098f5ea8c057873e96136bf597b8f9bcec2c59b563bb763bca96fa1a50` |
| [원본자료/폐암 2차 논문/코드/block_encryption_resnet50_rebuilt_KO.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%ED%8F%90%EC%95%94%202%EC%B0%A8%20%EB%85%BC%EB%AC%B8/%EC%BD%94%EB%93%9C/block_encryption_resnet50_rebuilt_KO.ipynb) | .ipynb | 138317 | `4233928cb2aba1e9e1306e02ffc8a7cf5f17e62b72b83ccc2e8ec228c592c80f` |
| [원본자료/폐암 2차 논문/코드/blur_resnet50_rebuilt2_KO.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%ED%8F%90%EC%95%94%202%EC%B0%A8%20%EB%85%BC%EB%AC%B8/%EC%BD%94%EB%93%9C/blur_resnet50_rebuilt2_KO.ipynb) | .ipynb | 132788 | `90c8e0f7a25c4533dc2b6759fa295bc7d758dd256330367d7c395dff2bee0d4f` |
| [원본자료/폐암 2차 논문/코드/heatmaps_windows.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%ED%8F%90%EC%95%94%202%EC%B0%A8%20%EB%85%BC%EB%AC%B8/%EC%BD%94%EB%93%9C/heatmaps_windows.ipynb) | .ipynb | 8646 | `75c45970b92c8957ea61de8c236e045c3a0d77ed0de942815d3b16ae6e24ef4a` |
| [원본자료/폐암 2차 논문/코드/paper_figures_resnet50.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%ED%8F%90%EC%95%94%202%EC%B0%A8%20%EB%85%BC%EB%AC%B8/%EC%BD%94%EB%93%9C/paper_figures_resnet50.ipynb) | .ipynb | 38070 | `162e3a670d2aa4dcb74771e651a1fd8c79fdf1e6e0ba33bb4fe81bc1177cc43d` |
| [원본자료/폐암 2차 논문/코드/pareto_scatter.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%ED%8F%90%EC%95%94%202%EC%B0%A8%20%EB%85%BC%EB%AC%B8/%EC%BD%94%EB%93%9C/pareto_scatter.ipynb) | .ipynb | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| [원본자료/폐암 2차 논문/코드/picture2x2.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%ED%8F%90%EC%95%94%202%EC%B0%A8%20%EB%85%BC%EB%AC%B8/%EC%BD%94%EB%93%9C/picture2x2.ipynb) | .ipynb | 7054 | `d56ae7885ab9219f62bb695fe1e5de081c7e667ebbf8c5916b87909bff4b2046` |
| [원본자료/폐암 2차 논문/코드/plot_privacy_metrics_split.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%ED%8F%90%EC%95%94%202%EC%B0%A8%20%EB%85%BC%EB%AC%B8/%EC%BD%94%EB%93%9C/plot_privacy_metrics_split.ipynb) | .ipynb | 18984 | `77cc7650ee472043999937da35fd6ac817330ce45a796c584330571ccf1e05be` |
| [원본자료/폐암 2차 논문/코드/privacy_score_ssim_psnr_updated.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%ED%8F%90%EC%95%94%202%EC%B0%A8%20%EB%85%BC%EB%AC%B8/%EC%BD%94%EB%93%9C/privacy_score_ssim_psnr_updated.ipynb) | .ipynb | 96269 | `74cb8eb330d2a60c357ff4806f3d4a5c3aeefb3f5f3cc2c0b188d792decb863a` |
| [원본자료/추가 학습모델과 실험/block_blur_resnet50_v4_KO.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%EC%B6%94%EA%B0%80%20%ED%95%99%EC%8A%B5%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%8B%A4%ED%97%98/block_blur_resnet50_v4_KO.ipynb) | .ipynb | 223652 | `988bdd6a86fac7245cdd255f19cdc5bf046579c6bdbe52e95ba8ed96a4f04140` |
| [최신 편집 원문](../../%EB%85%BC%EB%AC%B8/%EC%97%B0%EA%B5%AC2_%EC%9B%90%EB%AC%B8_%EC%B5%9C%EC%A2%85.hwp) | .hwp | 414720 | `7f3d880b8df41d7549973470476f6011ce80ca835f36f7ac62e22acdb978f196` |
| [원본자료/폐암 2차 논문/코드/block_blur_resnet50_v4_KO.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/%ED%8F%90%EC%95%94%202%EC%B0%A8%20%EB%85%BC%EB%AC%B8/%EC%BD%94%EB%93%9C/block_blur_resnet50_v4_KO.ipynb) | .ipynb | 223652 | `988bdd6a86fac7245cdd255f19cdc5bf046579c6bdbe52e95ba8ed96a4f04140` |

</details>

---

[프로젝트](../../README.md) · [전체 차수](../REVISION_INDEX.md) · [자료 폴더](../../%EB%85%BC%EB%AC%B8) · [연구 1 · 하계 EfficientNetV2-S](study-1.md)

# 📚 폴더 3차

Privacy Score 계산과 소규모 검사를 정리한 자료 차수입니다. 저장 CSV의 n_images=3이고 block2·blur2·combo4조건이므로 논문2의1097장 전체 결과로 소개하지 않습니다. 의료 원본 비교그림은 제외하고 집계4CSV·통합표·비의료 도표9개를 보존합니다. 추가 선택목록의 파일명·본인 경로는 의료영상 바이트와 구별합니다.



[전체 차수](../REVISION_INDEX.md) · [첫 화면](../../README.md) · [직전 단계 전체 비교](../revision-diffs/folder-3.diff) · [전체 파일 크기·해시](../revision-manifests/folder-3.json)

직전 단계: 폴더 2차.

## 📁 실제 파일

| 파일 | 종류 | 바이트 | SHA-256 |
|---|---|---:|---|
| [자료차수/3차/tables/privacy_scores_best_conditions.csv](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/tables/privacy_scores_best_conditions.csv) | .csv | 858 | `f8e160d380f0c0f41f33a8913e7739c7fe9a9f2e42081e77c16c302f5de9a529` |
| [자료차수/3차/tables/privacy_scores_combo_pivot.csv](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/tables/privacy_scores_combo_pivot.csv) | .csv | 92 | `7a31a1ae5238c3369ad5461b7806948a61eda358dae86dc87b177181df11b034` |
| [자료차수/3차/tables/privacy_scores_long.csv](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/tables/privacy_scores_long.csv) | .csv | 1507 | `edcecf8fe6c892b0640ffe9d7d7341c9ee094ab4624cfb5d65a3d52974caff22` |
| [자료차수/3차/tables/privacy_scores_summary_by_method.csv](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/tables/privacy_scores_summary_by_method.csv) | .csv | 362 | `403ff42da2b5a21428304bb456346178734658976dfff5a0c6abb8092782d060` |
| [자료차수/3차/graphs/01_block_privacy_score.png](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/graphs/01_block_privacy_score.png) | .png | 70066 | `2d3be7ac20d49f2e91cf4f3039fbbc8a4fd979e65025d456eb14802955783287` |
| [자료차수/3차/graphs/02_blur_privacy_score.png](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/graphs/02_blur_privacy_score.png) | .png | 63552 | `056c40e03053b9d7694877333ceb1a2019fb5080e3714355b5a0ef03c114be19` |
| [자료차수/3차/graphs/03_combo_privacy_score_heatmap.png](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/graphs/03_combo_privacy_score_heatmap.png) | .png | 42052 | `6d3cc49c6d9acf6a977922e59ac140c1d3f7c181b23595f4514ad3404fae59fa` |
| [자료차수/3차/graphs/04_block_ssim_psnr_reference.png](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/graphs/04_block_ssim_psnr_reference.png) | .png | 64195 | `f2359a64da2d2a5129dd225fc3cebde956bd414e4d767ebfac9804ea0baa386e` |
| [자료차수/3차/graphs/05_blur_ssim_psnr_reference.png](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/graphs/05_blur_ssim_psnr_reference.png) | .png | 77351 | `2aad1e739efc2b01a5e5b6b0acd24cba7b61e9d301fba2bfd7c19ea566435d72` |
| [자료차수/3차/graphs/06_top_conditions_privacy_score.png](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/graphs/06_top_conditions_privacy_score.png) | .png | 60606 | `df22b8d68e003e26e65c2c236bd427538882ff750a2e473918284a90d4bef99c` |
| [자료차수/3차/graphs/07_method_distribution_boxplot.png](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/graphs/07_method_distribution_boxplot.png) | .png | 38584 | `ceb03b03ff92470e91a9e62b2f1151f1512f7b11bf583dec03dc07d8d2915fee` |
| [자료차수/3차/graphs/08_top_conditions_table.png](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/graphs/08_top_conditions_table.png) | .png | 80715 | `d0e4e134df95fda8aa4fbeb0a0c17c9769aac16dc6ebf8c86c0a7765a1450ca8` |
| [자료차수/3차/graphs/09_best_by_method_table.png](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/graphs/09_best_by_method_table.png) | .png | 45058 | `9da6f678a12bdf33915130898cc4c2d50d2ab7af13a52f9b7433590c3a0d48f1` |
| [자료차수/3차/create_privacy_notebook.py](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/create_privacy_notebook.py) | .py | 28399 | `3809df9b5f3091f79172f0257c8eb7f2ef828bbf99da99eb41b486bb66108280` |
| [자료차수/3차/modify_privacy_notebook_ssim_only.py](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/modify_privacy_notebook_ssim_only.py) | .py | 27299 | `759fd7599e40b5cb25a8e7bc5f248bbb9eff2fd3328932c3c45236521345fc91` |
| [자료차수/3차/_smoke_privacy_score.ipynb](../../%EC%9E%90%EB%A3%8C%EC%B0%A8%EC%88%98/3%EC%B0%A8/_smoke_privacy_score.ipynb) | .ipynb | 89274 | `a03f40d6eab19fb5bdd3d4d60c3f308f03c43e80387f8f71dd70624f6311a8e6` |
| [원본자료/3차/privacy_score_outputs/privacy_score_results.xlsx](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/3%EC%B0%A8/privacy_score_outputs/privacy_score_results.xlsx) | .xlsx | 8330 | `a90c2676448a700ef65836cd2f3427030c95e4864870268f1bd3d7eda144b4f1` |
| [원본자료/3차/privacy_score_outputs/tables/selected_images.csv](../../%EC%9B%90%EB%B3%B8%EC%9E%90%EB%A3%8C/3%EC%B0%A8/privacy_score_outputs/tables/selected_images.csv) | .csv | 406 | `13a874a2d948b964c171ab3a6927e78882c262a245940933a5285454de846a71` |

## 🔎 해석·검증 범위

원고는 원고 보고값, 저장된 표는 당시 결과 파일, 노트북은 구현 자료입니다. 이번 정리는 재학습·임상 실험·제조 장비 검사·추천 성능 재현을 수행하지 않았습니다. 파일 비교와 PDF 내용 확인은 실제 기능 실행의 성공을 대신하지 않습니다. 원본의 알려진 오류와 0바이트 자료는 보존하며 성공으로 보정하지 않습니다.

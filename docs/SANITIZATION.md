# 공개 사본의 제한된 변환

원본 파일과 최초 공개 준비본은 수정하지 않았습니다. 승인된 환경변수 변환과 공개 제외만 적용했습니다. 의존성이나 실험 알고리즘은 추가·수정하지 않았습니다.

| 환경변수 | 준비할 값 |
|---|---|
| `EXPERIMENT_JSON_PATH_1` | 해당 셀의 입력 JSON 파일 경로 |
| `EXPERIMENT_JSON_PATH_2` | 해당 셀의 입력 JSON 파일 경로 |
| `EXPERIMENT_OUTPUT_DIR` | 실험 결과를 저장할 폴더 경로 |

## 실제 변경

- `연구1_하계_EfficientNetV2-S/그래프/Blur_Block_1차_그래프_white.ipynb`: notebook_public_sanitization, personal_absolute_path_to_environment, personal_path_to_generic_name

## 검사 범위

UTF-8, 파일 SHA-256, 추가 원본 두 번의 안정성 읽기, Python AST 및 가능한 노트북 셀 문법, 노트북 출력·첨부·메타데이터 제거, 비밀정보·개인정보 후보 탐지를 검사했습니다. 기존 매직 명령 셀 등 일반 Python 구문이 아닌 셀은 실행하지 않았습니다. 인증 정보·입력 자료가 없으므로 실험 결과와 전체 실행은 확인하지 않았습니다.

최초 프로젝트 명세 SHA-256: `1ac021cbc31aeabaf9575788710b72683185675b22f77dcca069c9eea7165209`.

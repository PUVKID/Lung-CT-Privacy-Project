# 공개 5차(실제 4차) → 실제 5차 복구 전체 파일 비교

공개 가능한 두 자료 폴더를 공백·주석까지 비교했습니다.

**삭제 표시는 이전 폴더 삭제가 아니라 다음 폴더에 같은 상대 파일이 없다는 뜻**입니다.

기존 공개 원문과 논문은 보존합니다.

사적 config·의료 영상·영상별 목록·가중치·운영 기록은 비교에 넣지 않습니다.

원문 크기·SHA는 실제 바이트이며 텍스트 hunk의 줄 종료만 LF로 통일했습니다.

원문 바이트는 변경하지 않았습니다.

| 파일 | 차이 | 이전 → 이후 크기 |
| --- | --- | --- |
| README.md | 수정 | 1,792 → 1,378 B |
| config.example.json | 수정 | 3,157 → 3,219 B |
| dashboard.py | 수정 | 27,081 → 27,081 B |
| docs/검토근거.md | 삭제 | 2,507 → 0 B |
| docs/기준분할_준비.md | 삭제 | 3,396 → 0 B |
| docs/실행계획.md | 삭제 | 2,623 → 0 B |
| docs/실행방법.md | 삭제 | 2,678 → 0 B |
| docs/원본대비변경.md | 삭제 | 2,361 → 0 B |
| tests/test_dashboard.py | 수정 | 32,021 → 32,021 B |
| tests/test_feature_recovery.py | 추가 | 0 → 8,930 B |
| tests/test_recovery.py | 추가 | 0 → 24,314 B |
| tests/test_return_recovery.py | 추가 | 0 → 13,244 B |
| tests/test_sigma_selection.mjs | 삭제 | 6,886 → 0 B |
| tools/__init__.py | 추가 | 0 → 71 B |
| tools/feature_generator.py | 추가 | 0 → 16,828 B |
| tools/recovery.py | 추가 | 0 → 24,427 B |
| tools/safe_training.py | 추가 | 0 → 16,693 B |
| web/index.html | 수정 | 8,904 → 8,904 B |
| web/scene.js | 수정 | 45,001 → 45,001 B |
| 결과/강도별 _전체 10 조 건 _집계.json | 추가 | 0 → 3,955 B |
| 변경기록.md | 삭제 | 5,346 → 0 B |
| 복구_학습.py | 추가 | 0 → 204 B |

## README.md

이전 1,792 B / SHA-256 `e0fd36cf04fcd207c42d3394c8dde43291bcdcc369328bf8da2c9363002ce4ec`. 이후 1,378 B / SHA-256 `bc1c64d890d173c3362863bb896c2106ac8bce794ed996556e28316977200a24`.

````diff
--- 이전/README.md
+++ 이후/README.md
@@ -1,18 +1,13 @@
-# 폐 CT 특징 블러 실험 · 4차
+# 실제5차 학습 복구
 
-<!-- reading-levels17:start -->
-**읽기 수준 선택** · [LEVEL 1 - Beginner](../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A81.md) · [LEVEL 2 - Explorer](../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A82.md) · [LEVEL 3 - Practitioner](../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A83.md) · [LEVEL 4 - Advanced](../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A84.md) · [LEVEL 5 - Expert](../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A85.md)
-<!-- reading-levels17:end -->
+[LEVEL 1 - Beginner](../../docs/revisions/conv1-actual-round5-recovery.md#reading-level-1) · [LEVEL 2 - Explorer](../../docs/revisions/conv1-actual-round5-recovery.md#reading-level-2) · [LEVEL 3 - Practitioner](../../docs/revisions/conv1-actual-round5-recovery.md#reading-level-3) · [LEVEL 4 - Advanced](../../docs/revisions/conv1-actual-round5-recovery.md#reading-level-4) · [LEVEL 5 - Expert](../../docs/revisions/conv1-actual-round5-recovery.md#reading-level-5)
 
-**조기 종료의 영향을 확인하기 위해 동일 자료·분할·초기값으로 강도마다 100회를 학습하고, 기존 정책의 관찰용 모델과 비교합니다.**
+기존 공개5차(실제4차)와 구분하는 실제5차 복구 코드입니다. 과학 조건과 기존 결과를 보존하며 위치·실행계보와 재개 경계를 검사합니다. 원본·기준manifest·복구baseline·학습가중치는 포함하지 않습니다.
 
-현재 연구는 환자 ID 없는 영상 단위 예비실험이며 높은 정확도를 임상 성능이나 프라이버시 효과로 해석하지 않습니다.
+| 자료 | 역할 | 사용 조건 |
+| --- | --- | --- |
+| 코드 | 실제 공개 소스 | 자신의 자료·환경과 기준 필요 |
+| 설정 예제 | 사적 경로·manifest SHA 제외 | config.json과 고정 입력을 직접 준비 |
+| 상세 설명 | 절차·조건·검증·한계 | 위에서 같은 수준 선택 |
 
-- [실험 계획](docs/실행계획.md)
-- [높은 정확도 검토 근거](docs/검토근거.md)
-- [실행 방법](docs/실행방법.md)
-- [원본·2차와의 차이](docs/원본대비변경.md)
-
-기존 결과는 보존합니다. 새 실험의 최종 성능은 실제 학습 완료 뒤 저장된 결과로만 보고합니다. 코드와 문서의 준비·검증, 학습 시작, 전체 학습 완료는 서로 구분합니다. 의료영상·영상별 목록·모델 가중치·개인정보·접속정보는 공개하지 않습니다.
-
-공개 저장소의 이 폴더는 공개 코드 5차이며 실제 실험 4차에 해당합니다. 공개 설정의 개인 경로와 기준 해시는 제거했으므로 [자체 기준 분할 준비](docs/기준분할_준비.md)가 필요합니다. [이번 변경 기록](변경기록.md)도 확인하세요.
+`config.example.json`을 자신의 `config.json`으로 복사한 뒤 원본 경로와 고정 기준을 채워야 합니다. 예제만으로 실제학습·복구를 실행할 수 없습니다. 원영상·manifest·모델·상태·접속정보는 공개하지 않습니다.
````

## config.example.json

이전 3,157 B / SHA-256 `1562d73c120b4e7e2d19f9afe6498cfc42df764b2561f9cb537dee279725e642`. 이후 3,219 B / SHA-256 `23b3ad3c3ccf427ef6fe51b81e7803a0ef208da2af6db3ec194bb302e718dae2`.

````diff
--- 이전/config.example.json
+++ 이후/config.example.json
@@ -13,7 +13,7 @@
   "test_ratio": 0.15,
   "epochs": 100,
   "early_stopping_enabled": false,
-  "expected_reference_manifest": "./reference/dataset_manifest_private.json",
+  "expected_reference_manifest": "work/reference/dataset_manifest_private.json",
   "expected_reference_manifest_sha256": "",
   "expected_reference_records_sha256": "",
   "early_stopping_patience": 15,
````

## dashboard.py

이전 27,081 B / SHA-256 `ce51d4aea02bf2d4196338bf10b82186065676b37367ef72fc3d7e52cbdd59b0`. 이후 27,081 B / SHA-256 `2977d6487837eb9b58997df1a4e0fbaad7298140d19d70f06c9fe97df142a0d9`.

````diff
--- 이전/dashboard.py
+++ 이후/dashboard.py
@@ -73,7 +73,7 @@
     classes = {"Bengin_cases": "양성", "Malignant_cases": "악성", "Normal_cases": "정상"}
     result = {"run_id": run_id, "items": [], "completed_sigmas": [],
               "pending": list(sigmas), "expected_total": 180}
-    folder = root.parent / "블러 강도별 대표 특징맵" / "4차"
+    folder = root.parent / "블러 강도별 대표 특징맵" / "5차"
     try:
         if folder.is_symlink() or not folder.resolve().is_relative_to(root.parent.resolve()):
             raise ValueError("이미지 폴더 경계 오류")
````

## docs/검토근거.md

이전 2,507 B / SHA-256 `7cfc1ec4b2f39ee859df69d58ab7ce6cb3da931b47bcd968a6b52ad32c9a7676`. 이후 0 B / SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

````diff
--- 이전/docs/검토근거.md
+++ 이후/docs/검토근거.md
@@ -1,17 +0,0 @@
-# 높은 정확도와 기법 적용의 해석
-
-<!-- reading-levels17:start -->
-**읽기 수준 선택** · [LEVEL 1 - Beginner](../../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A81.md) · [LEVEL 2 - Explorer](../../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A82.md) · [LEVEL 3 - Practitioner](../../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A83.md) · [LEVEL 4 - Advanced](../../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A84.md) · [LEVEL 5 - Expert](../../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A85.md)
-<!-- reading-levels17:end -->
-
-**앞선 점검에서 높은 정확도를 훨씬 뒤의 조기 종료만으로 설명하기 어려운 단서를 관측했습니다.** 비영상 메타정보만으로도 분류할 수 있는 출처 차이의 가능성과 영상 유사성의 영향을 함께 고려합니다. 이는 실제 ResNet이 파일 크기 숫자를 입력받았다는 뜻이나 환자 누수가 확정됐다는 뜻은 아닙니다. 비공개 감사 집계 수치는 공개하지 않습니다.
-
-분할 전 원본을 묶고 학습 분할에서만 클래스당 5000개를 반복 추출합니다. 좌우 반전·대비·밝기 변화를 학습에 적용하고 검증·시험은 증강하지 않습니다. 반복 표본 수를 독립 원본이나 환자 수로 세지 않습니다.
-
-블러는 CT 원본이 아닌 고정 첫 합성곱의 64채널 특징에 적용합니다. 강도마다 분류기를 학습하므로 강한 블러가 정확도의 단조 감소를 보장하지 않습니다. 정확도를 낮추거나 원하는 수치를 만들기 위한 실험이 아닙니다.
-
-source_class는 양성·정상·악성 원본 폴더 라벨입니다. 촬영기관·환자·스캐너를 식별하는 실제 출처 정보가 아닙니다. 이 범주별 분포를 맞췄다고 출처 독립성이 검증된 것은 아닙니다. 현재 관측은 출처 차이의 가능성을 보여 줄 뿐 실제 모델이 그 단서를 인과적으로 사용했다고 확정하지 않습니다. 환자 ID와 외부 자료가 없어 임상 일반화·환자 독립성·프라이버시 효과를 단정하지 않습니다.
-
-- [PyTorch ReduceLROnPlateau](https://docs.pytorch.org/docs/stable/generated/torch.optim.lr_scheduler.ReduceLROnPlateau.html)
-- [scikit-learn 데이터 누수](https://scikit-learn.org/stable/common_pitfalls.html)
-- [scikit-learn 교차검증](https://scikit-learn.org/stable/modules/cross_validation.html)
````

## docs/기준분할_준비.md

이전 3,396 B / SHA-256 `f324d8bc752daa03125d504789dd71ec28e9b4c7ddf5ea437f7f14a6a94404bb`. 이후 0 B / SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

````diff
--- 이전/docs/기준분할_준비.md
+++ 이후/docs/기준분할_준비.md
@@ -1,77 +0,0 @@
-# 자체 기준 manifest와 정확한 분할 준비
-
-<!-- reading-levels17:start -->
-**읽기 수준 선택** · [LEVEL 1 - Beginner](../../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A81.md) · [LEVEL 2 - Explorer](../../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A82.md) · [LEVEL 3 - Practitioner](../../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A83.md) · [LEVEL 4 - Advanced](../../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A84.md) · [LEVEL 5 - Expert](../../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A85.md)
-<!-- reading-levels17:end -->
-
-**이 비교는 기준 원본 목록·정확한 분할의 고정값을 요구합니다.** 의료 원본·실제 manifest·원본 목록의 실제 해시는 공개하지 않습니다. config.example.json의 빈 해시를 채우기 전에는 실행할 수 없습니다. 검증 함수를 끄거나 필드를 삭제해 우회하지 않습니다.
-
-자신의 자료로 먼저 기준 실험의 manifest를 생성하고 보존합니다. 예를 들어 같은 저장소의 공개 2차에서 자체 config.json을 설정해 prepare를 실행하면 work/results/dataset_manifest_private.json이 생성됩니다. 두 실험의 dataset_root는 같은 실제 원본 경로를 가리켜야 하며 seed·분할 비율·유사 그룹 기준을 일치시킵니다. 기록에는 절대 원본 경로가 있으므로 같은 파일을 다른 경로로 옮겨 만든 목록도 동일한 기준으로 간주하지 않습니다.
-
-공개 5차의 config.example.json을 config.json으로 복사해 다음 값을 자신의 기준으로 채웁니다.
-
-<a id="layout18-table-1-row-1"></a>
-
-**dataset_root**
-
-**설정**
-
-dataset_root
-
-**필요한 값**
-
-기준과 같은 실제 원본 경로
-
-<a id="layout18-table-1-row-2"></a>
-
-**expected_reference_manifest**
-
-**설정**
-
-expected_reference_manifest
-
-**필요한 값**
-
-보존한 기준 manifest 파일 경로
-
-<a id="layout18-table-1-row-3"></a>
-
-**expected_reference_manifest_sha256**
-
-**설정**
-
-expected_reference_manifest_sha256
-
-**필요한 값**
-
-기준 manifest 파일 전체 바이트의 SHA-256
-
-<a id="layout18-table-1-row-4"></a>
-
-**expected_reference_records_sha256**
-
-**설정**
-
-expected_reference_records_sha256
-
-**필요한 값**
-
-기준 JSON의 records를 ensure_ascii=False, sort_keys=True 기본 JSON 구분자로 직렬화한 UTF-8 SHA-256
-
-
-다음 예시는 자신의 로컬 기준 파일에서 두 해시를 계산하는 방법입니다. 실제 경로로 바꾸고 결과값은 비공개 config에만 넣습니다.
-
-```python
-from pathlib import Path
-import hashlib
-import json
-
-path = Path("자체 기준 manifest 경로")
-raw = path.read_bytes()
-reference = json.loads(raw.decode("utf-8"))
-records = json.dumps(reference["records"], ensure_ascii=False, sort_keys=True).encode("utf-8")
-print(hashlib.sha256(raw).hexdigest())
-print(hashlib.sha256(records).hexdigest())
-```
-
-prepare는 기준 파일 해시, 기준·현재 records 해시, 각 manifest_sha256, records 전체와 splits 전체의 동일성을 함께 검사합니다. 자기 자료의 기준 생성·해시 설정은 사용자가 수행할 재현 준비이며 저장소가 연구 원본이나 연구 분할을 제공한다는 뜻은 아닙니다. 설정을 마친 뒤 실행방법의 prepare를 수행하고 검증 성공 후에만 학습합니다.
````

## docs/실행계획.md

이전 2,623 B / SHA-256 `b662386769ca4d1c73660e7b22a9d815def6454a4aecc188b2133e283ab4634f`. 이후 0 B / SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

````diff
--- 이전/docs/실행계획.md
+++ 이후/docs/실행계획.md
@@ -1,21 +0,0 @@
-# 4차 고정 100회 학습과 종료 정책 비교
-
-<!-- reading-levels17:start -->
-**읽기 수준 선택** · [LEVEL 1 - Beginner](../../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A81.md) · [LEVEL 2 - Explorer](../../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A82.md) · [LEVEL 3 - Practitioner](../../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A83.md) · [LEVEL 4 - Advanced](../../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A84.md) · [LEVEL 5 - Expert](../../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A85.md)
-<!-- reading-levels17:end -->
-
-2026-11-10 사용자 직접 요청으로 높은 정확도와 오버샘플링·증강·블러·분할·평가·조기 종료의 실제 적용을 검토하고 재실험합니다. 2차 학습·3차 화면 수정 기록을 보존하며 새 4차에서 시작합니다.
-
-## 성공 조건
-
-- 원본과 기존 결과를 변경하지 않습니다. 새 run_id와 ImageNet 초기값으로 시작합니다.
-- 2차와 같은 원본 manifest와 정확히 같은 train/validation/test 분할을 확인하고 불일치하면 실행하지 않습니다.
-- 모델·초기 seed·증강·온라인 클래스당 5000개·배치·최적화·학습률 감소를 유지하며 조기 종료만 끄고 10개 강도마다 100회까지 학습합니다.
-- 기존 조기 종료 정책이 멈췄을 첫 회차를 관찰용으로 기록하고, 그 시점까지 검증 손실이 가장 낮았던 모델을 별도로 고정합니다. 학습은 계속합니다.
-- 각 강도의 100회 학습 완료 뒤 전체 100회 중 검증 손실 최저 모델과 이전 정책의 관찰용 모델을 같은 시험 영상으로 비교합니다. 시험 결과를 모델·강도·임계값 선택에 사용하지 않습니다.
-- 재사용한 분할과 이미 확인한 시험셋이므로 탐색적 종료 정책 비교이며 새 독립 시험이나 임상 검증이 아닙니다.
-- 실제 온라인 표본 계획·배치 누적·증강 train 전용·동결 층·역전파·블러 경로·평가 지표와 재개 상태를 검사합니다. 다른 verifier가 최종 소스와 검사를 대조한 뒤 학습을 시작합니다.
-
-## 해석
-
-정확도를 낮추거나 원하는 수치를 만들기 위한 실험이 아닙니다. 100회를 돌려도 정확도가 높게 나올 수 있고, 과적합으로 손실이 커질 수도 있습니다. 모든 결과를 같은 기준으로 보존합니다. 환자 ID와 별도 출처 자료가 없어 일반화·환자 독립성·프라이버시 효과는 확정하지 않습니다.
````

## docs/실행방법.md

이전 2,678 B / SHA-256 `3259d65358118fcffc4fb785efb168eec1d58ca59d512b96c24a34f0c4fb7c8b`. 이후 0 B / SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

````diff
--- 이전/docs/실행방법.md
+++ 이후/docs/실행방법.md
@@ -1,23 +0,0 @@
-# 공개 코드 5차: 실험 4차 실행 방법
-
-<!-- reading-levels17:start -->
-**읽기 수준 선택** · [LEVEL 1 - Beginner](../../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A81.md) · [LEVEL 2 - Explorer](../../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A82.md) · [LEVEL 3 - Practitioner](../../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A83.md) · [LEVEL 4 - Advanced](../../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A84.md) · [LEVEL 5 - Expert](../../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A85.md)
-<!-- reading-levels17:end -->
-
-**이 공개 폴더는 고정 100회 비교를 수행하는 실제 실험 4차의 코드입니다.** Python 환경과 requirements.txt 의존성을 준비합니다. 개인 환경·데이터·가중치는 포함하지 않습니다.
-
-먼저 [자체 기준 분할 준비](기준분할_준비.md)를 따라 config.example.json을 config.json으로 복사하고 자신의 원본과 기준 manifest의 경로·파일 해시·원본 목록 해시를 채웁니다. 예제에 포함한 빈 해시는 실행 가능한 기준값이 아닙니다. 기준 파일과 원본 목록·정확한 분할이 다르면 prepare는 저장 전에 실패합니다.
-
-```powershell
-python -B -X utf8 run_training.py prepare
-python -B -X utf8 run_training.py smoke --device cuda
-python -B -X utf8 run_training.py train --device cuda
-```
-
-이 폴더를 작업 디렉터리로 사용합니다. prepare·smoke는 상태를 갱신하므로 실행 중 중복 호출하지 않습니다. smoke와 작은 GPU 배치 연결 검사는 연구 성능이 아닙니다. 새 실행은 이전 체크포인트를 복사하지 않으며 동일 실행만 optimizer·scheduler·난수·관찰용 종료 상태를 복구합니다.
-
-대시보드는 같은 폴더에서 python -B -X utf8 dashboard.py로 시작합니다. work/server.json의 접속 토큰은 공유하지 않습니다. 정확도는 한 자리 반올림이며 원비율·전체 백분율·정답 수를 구분합니다. 반올림된 100.0%를 실제 모두 정답과 혼동하지 않습니다.
-
-각 강도의 100회와 시험 결과가 끝난 뒤에만 완료로 표시합니다. 코드 준비·학습 시작·전체 10조건 완료는 다릅니다. 공개본 다운로드나 검사 통과가 장시간 학습 완료를 뜻하지 않습니다.
-
-특징맵 저장은 [이전 공개 4차 저장 도구](../../4차/생성%20도구/사용방법.md)의 --experiment-root/--output-root/--reference-root/--run-id에 새 실험의 실제 값을 명시해 재사용합니다. 새 특징맵 생성 완료를 미리 주장하지 않습니다.
````

## docs/원본대비변경.md

이전 2,361 B / SHA-256 `22a0918ce50a87c6565c19e377687d3c9bed457ce5f93d89e2f789bc386c9e13`. 이후 0 B / SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

````diff
--- 이전/docs/원본대비변경.md
+++ 이후/docs/원본대비변경.md
@@ -1,15 +0,0 @@
-# 원본·2차·4차의 차이
-
-<!-- reading-levels17:start -->
-**읽기 수준 선택** · [LEVEL 1 - Beginner](../../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A81.md) · [LEVEL 2 - Explorer](../../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A82.md) · [LEVEL 3 - Practitioner](../../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A83.md) · [LEVEL 4 - Advanced](../../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A84.md) · [LEVEL 5 - Expert](../../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A85.md)
-<!-- reading-levels17:end -->
-
-**첨부 노트북은 Keras ResNet50, 환자 ID 기반 7-fold, fixed 대조군, 매칭·복원 공격 등을 포함합니다.** 현재 코드는 torchvision ResNet50 V1.5와 ImageNet1K V1 가중치의 단일 영상 유사 그룹 분할 예비실험입니다. 원본의 모든 연구를 재현했다고 주장하지 않습니다.
-
-4차는 2차의 모델 구조·정규화·seed42·정확한 분할·학습 전용 온라인 증강·클래스당 5000개·배치 8·AdamW·검증 손실 기반 학습률 감소를 유지합니다. 고정 conv1→64채널 DCT Gaussian blur→고정 BN/layer1~3→학습 layer4 비BN 및 분류층입니다. sigma는 특징 픽셀 단위 0·1·2·4·8·16·32·64·128·256입니다.
-
-주 변경은 조기 종료를 비활성화해 강도마다 100회 학습하고 기존 종료 시점까지의 최저 검증 손실 모델과 전체 100회 최저 검증 손실 모델을 비교하는 것입니다. 조기 종료 관찰 상태와 별도 체크포인트는 재개 때도 보존합니다. 원본 manifest와 실제 분할은 기준 2차와 같아야 합니다. 실패하면 진행하지 않습니다.
-
-대시보드는 새 4차 실행의 상태만 표시하고 정확도는 소수 첫째 자리 반올림합니다. AUC·손실·학습률과 원비율은 원값 조회를 유지합니다. 표시 변경은 저장된 실험 결과를 바꾸지 않습니다.
-
-환자 ID가 없어 환자 단위 7-fold·독립 임상 평가를 수행했다고 쓰지 않습니다. fixed 모델·영상 매칭·복원 공격·프라이버시 임계점 선택은 이번 4차 분류 비교에 추가하지 않았습니다. 높은 성능의 원인 검토와 실제 기법 검증 결과, 구현 차이와 검사 기록은 별도 기록합니다.
````

## tests/test_dashboard.py

이전 32,021 B / SHA-256 `7300f3737f7b58b6acabe97d5230acea114a3f6e9d4eda8ec5e8073b3dec7c01`. 이후 32,021 B / SHA-256 `02f061b12f8c0012334a384224060b9c457f6ceb2c6a2b948a88dd366d457361`.

````diff
--- 이전/tests/test_dashboard.py
+++ 이후/tests/test_dashboard.py
@@ -182,7 +182,7 @@
 const original=JSON.stringify(state.history);
 sandbox.testAPI.render(state);
 await new Promise(resolve=>setImmediate(resolve));
-assert.match(html,/<title>폐 CT 특징 블러 실험 · 4차<\/title>/);
+assert.match(html,/<title>폐 CT 특징 블러 실험 · 5차<\/title>/);
 assert.equal(nodes.epoch.textContent,'0회 / 최대 20회');
 assert.equal(nodes.learningRate.textContent,'0');
 assert.equal(nodes.earlyStopping.textContent,'0 / 7회');
````

## tests/test_feature_recovery.py

이전 0 B / SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. 이후 8,930 B / SHA-256 `5267882e4cf4099b80d115eb45ff430cdee2387500614e0591bb1404c8f7c493`.

````diff
--- 이전/tests/test_feature_recovery.py
+++ 이후/tests/test_feature_recovery.py
@@ -0,0 +1,166 @@
+"""특징맵 감시의 일시 읽기 잠금과 실제 실패를 구분합니다."""
+
+from pathlib import Path
+import copy
+import hashlib
+import json
+import tempfile
+import unittest
+from unittest import mock
+
+from tools import feature_generator as generator
+from src.training import _run_identity
+import dashboard
+
+
+def sharing_error():
+    error = PermissionError("일시적인 공유 잠금")
+    error.winerror = 32
+    return error
+
+
+class FeatureReadTests(unittest.TestCase):
+    def test_transient_windows_read_lock_retries_then_succeeds(self):
+        with mock.patch.object(Path, "read_text", side_effect=[sharing_error(), '{"run_id":"new"}']) as read, \
+                mock.patch.object(generator.time, "sleep") as pause:
+            self.assertEqual(generator.read_json(Path("status.json")), {"run_id": "new"})
+            self.assertEqual(read.call_count, 2)
+            pause.assert_called_once()
+
+    def test_persistent_windows_lock_stops_after_bound(self):
+        with mock.patch.object(Path, "read_text", side_effect=sharing_error()) as read, \
+                mock.patch.object(generator.time, "sleep"):
+            with self.assertRaises(PermissionError):
+                generator.read_json(Path("status.json"))
+            self.assertEqual(read.call_count, 7)
+
+    def test_other_error_or_invalid_json_is_not_hidden_or_retried(self):
+        for value in [OSError(28, "공간 부족"), PermissionError(13, "지속 권한 오류"), '{"broken":']:
+            with mock.patch.object(Path, "read_text", side_effect=value if isinstance(value, Exception) else None,
+                                   return_value=value) as read, mock.patch.object(generator.time, "sleep") as pause:
+                with self.assertRaises((OSError, ValueError)):
+                    generator.read_json(Path("status.json"))
+                self.assertEqual(read.call_count, 1)
+                pause.assert_not_called()
+
+    def test_old_run_lineage_is_rejected_before_any_inference(self):
+        with mock.patch.object(generator, "RUN", "b" * 16), \
+                mock.patch.object(generator, "read_json", return_value={"run_id": "a" * 16, "source_run_id": "a" * 16}):
+            with self.assertRaises(ValueError):
+                generator.run_once([])
+
+    def test_http_preview_uses_only_round5_and_current_run(self):
+        with tempfile.TemporaryDirectory() as folder:
+            base = Path(folder)
+            root = base / "experiment"
+            result_dir = root / ("work/results/run_" + "b" * 16)
+            result_dir.mkdir(parents=True)
+            (result_dir / "sigma_0_metrics.json").write_text(json.dumps({"run_id": "b" * 16, "sigma": 0,
+                "completed_at": "완료", "test": {"accuracy": 1}, "training_policy": {"early_stopping_enabled": False}}), encoding="utf-8")
+            output = base / "블러 강도별 대표 특징맵" / "5차"
+            output.mkdir(parents=True)
+            items = []
+            raw = b"\x89PNG\r\n\x1a\n" + b"synthetic"
+            for key in ("Bengin_cases", "Malignant_cases", "Normal_cases"):
+                for stage in range(6):
+                    relative = dashboard.feature_preview_path(0, key, stage)
+                    path = output / relative
+                    path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(raw)
+                    items.append({"id": f"0-{key}-{stage}", "sigma": 0, "class_key": key, "stage": stage,
+                                  "relative_path": relative.as_posix(), "sha256": hashlib.sha256(raw).hexdigest()})
+            index = output / "export_index_private.json"
+            payload = {"run_id": "b" * 16, "completed_sigmas": [0], "items": items}
+            index.write_text(json.dumps(payload), encoding="utf-8")
+            with mock.patch.object(dashboard, "read_status", return_value={"run_id": "b" * 16,
+                    "sigma_queue": [{"sigma": 0, "status": "completed"}]}):
+                result = dashboard.feature_previews(root, "0-Normal_cases-0")
+                self.assertEqual(result["completed_sigmas"], [0])
+                self.assertEqual(len(result["items"]), 18)
+                self.assertEqual(next(i for i in result["items"] if i["id"] == "0-Normal_cases-0")["_payload"], raw)
+                payload["run_id"] = "a" * 16
+                index.write_text(json.dumps(payload), encoding="utf-8")
+                rejected = dashboard.feature_previews(root)
+                self.assertEqual(rejected["items"], [])
+                self.assertIn("error", rejected)
+
+
+class FeatureIdentityTests(unittest.TestCase):
+    def setUp(self):
+        self.temporary = tempfile.TemporaryDirectory()
+        self.addCleanup(self.temporary.cleanup)
+        self.train = Path(self.temporary.name) / "실험"
+        self.output = Path(self.temporary.name) / "그림"
+        (self.train / "src").mkdir(parents=True)
+        self.output.mkdir()
+        for relative in ("run_training.py", "src/data.py", "src/model.py"):
+            (self.train / relative).write_text("# 합성 고정 소스\n", encoding="utf-8")
+        rows = [{"source_class": source, "relative_path": f"{index}.png", "label": int(index == 1),
+                 "path": str(self.train / f"{index}.png"), "byte_sha256": "a" * 64}
+                for index, (_key, source, _label) in enumerate(generator.CLASSES)]
+        records_sha = hashlib.sha256(json.dumps(rows, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()
+        self.manifest = {"records": rows, "splits": {"train": copy.deepcopy(rows), "validation": [], "test": []},
+                         "manifest_sha256": records_sha}
+        reference = self.train / "기준.json"
+        self.write_json(reference, self.manifest)
+        config = {"expected_reference_manifest": "기준.json",
+                  "expected_reference_manifest_sha256": hashlib.sha256(reference.read_bytes()).hexdigest(),
+                  "expected_reference_records_sha256": records_sha}
+        self.write_json(self.train / "config.json", config)
+        self.run_id, settings = _run_identity(self.train, config, records_sha)
+        self.write_json(self.train / "work/recovery/복구_계보_비공개.json",
+                        {"run_id": self.run_id, "source_run_id": "f" * 16, "settings": settings})
+        self.write_json(self.train / "work/runtime/status.json", {"run_id": self.run_id, "sigma_queue": []})
+        self.manifest_path = self.train / "work/results/dataset_manifest_private.json"
+        self.write_json(self.manifest_path, self.manifest)
+        patches = mock.patch.multiple(generator, TRAIN=self.train, HERE=self.output, RUN=self.run_id)
+        patches.start()
+        self.addCleanup(patches.stop)
+
+    @staticmethod
+    def write_json(path, value):
+        path.parent.mkdir(parents=True, exist_ok=True)
+        path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
+
+    def test_verified_pending_run_has_no_images_and_waits(self):
+        self.assertFalse(generator.run_once([]))
+        saved = json.loads((self.output / "export_index_private.json").read_text(encoding="utf-8"))
+        self.assertEqual(saved["items"], [])
+        self.assertEqual(saved["pending_sigmas"], [0, 1, 2, 4, 8, 16, 32, 64, 128, 256])
+
+    def test_manifest_record_tamper_with_unchanged_claimed_sha_is_rejected(self):
+        self.manifest["records"][0]["label"] = 1
+        self.write_json(self.manifest_path, self.manifest)
+        with self.assertRaises(ValueError):
+            generator.run_once([])
+        self.assertFalse((self.output / "export_index_private.json").exists())
+
+    def test_split_tamper_with_unchanged_records_is_rejected(self):
+        self.manifest["splits"]["train"].reverse()
+        self.write_json(self.manifest_path, self.manifest)
+        with self.assertRaises(ValueError):
+            generator.run_once([])
+
+    def test_source_changes_and_unexpected_source_file_are_rejected(self):
+        for change in ("바뀐원본", "추가소스"):
+            path = self.train / ("run_training.py" if change == "바뀐원본" else "src/추가.py")
+            original = path.read_bytes() if path.exists() else None
+            path.write_text("# 변조\n", encoding="utf-8")
+            with self.subTest(change=change), self.assertRaises(ValueError):
+                generator.run_once([])
+            if original is None:
+                path.unlink()
+            else:
+                path.write_bytes(original)
+
+    def test_existing_output_from_different_generator_is_rejected(self):
+        self.assertFalse(generator.run_once([]))
+        index_path = self.output / "export_index_private.json"
+        payload = json.loads(index_path.read_text(encoding="utf-8"))
+        payload["generator_sha256"] = "0" * 64
+        self.write_json(index_path, payload)
+        with self.assertRaises(ValueError):
+            generator.run_once([])
+
+
+if __name__ == "__main__":
+    unittest.main()
````

## tests/test_recovery.py

이전 0 B / SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. 이후 24,314 B / SHA-256 `03bf89f115b380a87cab803cd197d0ed76bab1e389e0aca7e26c535f2da61196`.

````diff
--- 이전/tests/test_recovery.py
+++ 이후/tests/test_recovery.py
@@ -0,0 +1,377 @@
+"""경로 이관과 명시적 상태 복구가 과학 설정·가중치를 바꾸지 않는지 검사합니다."""
+
+import copy
+import hashlib
+import json
+from pathlib import Path
+import tempfile
+import unittest
+from unittest import mock
+import io
+from contextlib import redirect_stdout
+
+import torch
+import numpy as np
+from PIL import Image
+
+from tools import recovery, safe_training
+from src import training
+from src.state import StatusWriter
+
+
+class RecoveryTests(unittest.TestCase):
+    def manifest(self):
+        row = {"path": "D:/원본/Normal/a.png", "relative_path": "Normal/a.png",
+               "label": 0, "byte_sha256": "a" * 64, "similarity_group": "g"}
+        rows = [row]
+        return {"records": rows, "splits": {"train": copy.deepcopy(rows), "validation": [], "test": []},
+                "summary": {"original_total": 1}, "manifest_sha256": recovery.records_digest(rows)}
+
+    def test_manifest_changes_only_path_and_derived_hash(self):
+        source = self.manifest()
+        target = recovery.relocate_manifest(source, "D:/원본", "E:/원본")
+        self.assertEqual(target["records"][0]["path"], "E:/원본/Normal/a.png")
+        self.assertEqual(target["splits"]["train"][0]["path"], "E:/원본/Normal/a.png")
+        self.assertEqual(target["summary"], source["summary"])
+        self.assertEqual(source["records"][0]["path"], "D:/원본/Normal/a.png")
+        reversed_target = recovery.relocate_manifest(target, "E:/원본", "D:/원본")
+        self.assertEqual(reversed_target, source)
+
+    def test_manifest_rejects_foreign_and_parent_paths(self):
+        for bad in ["D:/원본외부/a.png", "D:/원본/../비밀/a.png"]:
+            value = self.manifest()
+            value["records"][0]["path"] = bad
+            with self.assertRaises(ValueError):
+                recovery.relocate_manifest(value, "D:/원본", "E:/원본")
+
+    def test_config_allows_only_exact_relocation_fields(self):
+        old = {"dataset_root": "D:/원본", "epochs": 100, "seed": 42,
+               "expected_reference_manifest": "../2차/manifest.json",
+               "expected_reference_manifest_sha256": "a" * 64,
+               "expected_reference_records_sha256": "b" * 64}
+        new = recovery.relocated_config(old, "E:/원본", self.manifest())
+        recovery.assert_config_compatible(old, new, "E:/원본", self.manifest())
+        for key, value in [("epochs", 99), ("seed", 43), ("precision", "fp16")]:
+            changed = {**new, key: value}
+            with self.assertRaises(ValueError):
+                recovery.assert_config_compatible(old, changed, "E:/원본", self.manifest())
+
+    def test_baseline_and_source_tamper_fail_closed(self):
+        with tempfile.TemporaryDirectory() as folder:
+            root = Path(folder)
+            path = root / "기준.json"
+            path.write_text('{"source_files": {"file": "wrong"}}', encoding="utf-8")
+            digest = recovery.file_digest(path)
+            baseline = recovery.read_baseline(path, digest)
+            (root / "file").write_text("원본", encoding="utf-8")
+            with self.assertRaises(ValueError):
+                recovery.verify_files(root, baseline["source_files"])
+            path.write_text("{}", encoding="utf-8")
+            with self.assertRaises(ValueError):
+                recovery.read_baseline(path, digest)
+
+    def test_checkpoint_rebinding_preserves_all_tensor_and_control_values(self):
+        original = {"run_id": "a" * 16, "sigma": 1, "epoch": 65,
+                    "model": {"weight": torch.tensor([1.0, 2.0])},
+                    "optimizer": {"state": {0: {"exp_avg": torch.tensor([.2])}}},
+                    "scheduler": {"last_epoch": 65}, "torch_rng_state": torch.get_rng_state(),
+                    "training_control": {"best_raw_epoch": 62}, "shadow_prefix_sha256": "c" * 64}
+        changed = recovery.rebind_checkpoint(original, "a" * 16, "b" * 16, 1, "d" * 64)
+        self.assertEqual(changed["run_id"], "b" * 16)
+        self.assertEqual(changed["shadow_prefix_sha256"], "d" * 64)
+        self.assertEqual(original["run_id"], "a" * 16)
+        recovery.assert_state_equal({k: v for k, v in original.items() if k not in {"run_id", "shadow_prefix_sha256"}},
+                                    {k: v for k, v in changed.items() if k not in {"run_id", "shadow_prefix_sha256"}})
+        with self.assertRaises(ValueError):
+            recovery.rebind_checkpoint(original, "e" * 16, "b" * 16, 1, "d" * 64)
+
+    def test_serialized_prefix_hash_links_last_and_completed_metric(self):
+        with tempfile.TemporaryDirectory() as folder:
+            root = Path(folder)
+            source = root / "old.pt"
+            torch.save({"run_id": "a" * 16, "sigma": 0, "epoch": 1,
+                        "model": {"weight": torch.ones(2)}}, source)
+            result = recovery.convert_checkpoint(source, root / "new.pt", "a" * 16, "b" * 16, 0)
+            self.assertEqual(result["new_sha256"], recovery.file_digest(root / "new.pt"))
+            metric = {"run_id": "a" * 16, "sigma": 0, "epochs_ran": 100,
+                      "test": {"accuracy": 1.0, "n_images": 4, "confusion_matrix": [[2, 0], [0, 2]]},
+                      "early_stopping_comparison": {"available": True, "checkpoint_sha256": "old"}}
+            changed = recovery.rebind_metric(metric, "a" * 16, "b" * 16, 0, result["new_sha256"])
+            self.assertEqual(changed["test"], metric["test"])
+            self.assertEqual(changed["early_stopping_comparison"]["checkpoint_sha256"], result["new_sha256"])
+            invalid = copy.deepcopy(metric)
+            invalid["test"]["accuracy"] = .75
+            with self.assertRaises(ValueError):
+                recovery.rebind_metric(invalid, "a" * 16, "b" * 16, 0, result["new_sha256"])
+
+    def test_resume_requires_complete_history_and_frozen_prefix(self):
+        last = {"epoch": 2, "history": [{"epoch": 1}, {"epoch": 2}],
+                "training_control": {"optimizer_steps": 4, "best_raw_epoch": 1,
+                                     "best_raw_loss": .1, "meaningful_best_loss": .1, "stale_epochs": 1,
+                                     "shadow_stop_epoch": 2, "shadow_best_raw_epoch": 1,
+                                     "enabled": False, "patience": 15, "min_delta": .0001}}
+        config = {"epochs": 100, "batch_size": 1, "samples_per_class": 1,
+                  "early_stopping_enabled": False, "early_stopping_patience": 15, "min_delta": .0001}
+        self.assertEqual(recovery.validate_resume(last, config, 2), 3)
+        last["history"].pop()
+        with self.assertRaises(ValueError):
+            recovery.validate_resume(last, config, 2)
+
+    def test_low_space_and_duplicate_process_block_before_training(self):
+        with mock.patch.object(safe_training.shutil, "disk_usage", return_value=mock.Mock(free=10)):
+            with self.assertRaises(OSError):
+                safe_training.require_free_space(Path.cwd(), 100)
+        with self.assertRaises(RuntimeError):
+            safe_training.reject_duplicates([{"pid": 12, "command": "run_training.py"}])
+        safe_training.reject_duplicates([])
+
+    def test_primary_and_secondary_error_survive_one_failed_log_sink(self):
+        with tempfile.TemporaryDirectory() as folder:
+            root = Path(folder)
+            broken = root / "blocked"
+            broken.write_text("폴더 아님", encoding="utf-8")
+            good = root / "good"
+            try:
+                raise OSError(28, "원래 저장 오류")
+            except OSError as error:
+                payload = safe_training.exception_payload(error)
+            failures = safe_training.write_independent_logs([broken, good], "오류.json", payload)
+            self.assertEqual(len(failures), 1)
+            saved = json.loads((good / "오류.json").read_text(encoding="utf-8"))
+            self.assertEqual(saved["errno"], 28)
+            self.assertIn("원래 저장 오류", saved["traceback"])
+            self.assertEqual(len(saved["secondary_log_errors"]), 1)
+
+    def test_worker_preserves_primary_before_failing_status_error_handler(self):
+        with tempfile.TemporaryDirectory() as folder:
+            root = Path(folder)
+            (root / "config.json").write_text("{}", encoding="utf-8")
+            state = mock.Mock()
+            state.data = {"sigma": 1, "epoch": 66, "attempted_batch": 470,
+                          "sigma_queue": [{"status": "running"}]}
+            state.update.side_effect = [None, PermissionError("상태 오류 기록도 실패")]
+            folders = [root / "first", root / "second"]
+            with mock.patch("src.state.StatusWriter", return_value=state), \
+                    mock.patch("src.state.atomic_json", side_effect=OSError("오류 파일 기록 실패")), \
+                    mock.patch("src.training.run_training", side_effect=OSError(28, "원래 학습 저장 오류")), \
+                    mock.patch.object(safe_training.sys, "stderr", io.StringIO()):
+                code = safe_training.worker(root, "cpu", folders)
+            self.assertEqual(code, 1)
+            for path in folders:
+                record = json.loads(next(path.glob("*.json")).read_text(encoding="utf-8"))
+                self.assertEqual(record["errno"], 28)
+                self.assertIn("원래 학습 저장 오류", record["traceback"])
+                self.assertEqual(len(record["secondary_status_errors"]), 2)
+
+    def test_import_then_actual_cpu_loop_skips_completed_and_resumes_epoch66(self):
+        # 임상 자료와 GPU 없이 같은 저장·재개 함수의 실제 경계를 검사합니다.
+        class TinyModel(torch.nn.Module):
+            def __init__(self, **kwargs):
+                super().__init__()
+                self.weight = torch.nn.Parameter(torch.tensor(1.0))
+
+            def forward(self, images):
+                return (images.mean((1, 2, 3)) - .5) * self.weight
+
+        with tempfile.TemporaryDirectory() as folder:
+            base = Path(folder)
+            source, target = base / "old", base / "new"
+            old_data, new_data = base / "old_data", base / "new_data"
+            for root in (source, target):
+                (root / "src").mkdir(parents=True)
+                for name in recovery.SCIENTIFIC:
+                    (root / name).write_text("# 합성 검사 원본\n", encoding="utf-8")
+            records, splits = [], {}
+            for split in ("train", "validation", "test"):
+                splits[split] = []
+                for label in (0, 1):
+                    relative = f"{split}_{label}.png"
+                    for data_root in (old_data, new_data):
+                        data_root.mkdir(exist_ok=True)
+                        Image.fromarray(np.full((8, 8), 40 + 160 * label, dtype=np.uint8)).save(data_root / relative)
+                    row = {"path": str(old_data / relative), "relative_path": relative, "label": label,
+                           "source_class": "Normal cases" if label == 0 else "Malignant cases",
+                           "byte_sha256": recovery.file_digest(old_data / relative)}
+                    records.append(row); splits[split].append(copy.deepcopy(row))
+            manifest = {"records": records, "splits": splits, "summary": {},
+                        "manifest_sha256": recovery.records_digest(records)}
+            config = {"dataset_root": str(old_data), "seed": 42, "cpu_threads": 1, "precision": "fp32",
+                      "epochs": 100, "early_stopping_enabled": False, "early_stopping_patience": 15,
+                      "min_delta": .0001, "batch_size": 1, "samples_per_class": 1, "image_size": 8,
+                      "learning_rate": .00003, "weight_decay": .0001, "scheduler_patience": 4,
+                      "scheduler_factor": .5, "min_learning_rate": .000001, "num_workers": 0,
+                      "sigmas": [0, 1], "status_every_batches": 1,
+                      "expected_reference_manifest": "reference.json",
+                      "expected_reference_manifest_sha256": hashlib.sha256(recovery.json_bytes(manifest)).hexdigest(),
+                      "expected_reference_records_sha256": manifest["manifest_sha256"]}
+            (source / "work/results").mkdir(parents=True)
+            (source / "config.json").write_bytes(recovery.json_bytes(config))
+            (source / "reference.json").write_bytes(recovery.json_bytes(manifest))
+            (source / "work/results/dataset_manifest_private.json").write_bytes(recovery.json_bytes(manifest))
+            old_run, old_settings = training._run_identity(source, config, manifest["manifest_sha256"])
+            result_dir = source / f"work/results/run_{old_run}"
+            checkpoint_dir = source / f"work/checkpoints/run_{old_run}"
+            result_dir.mkdir(parents=True); checkpoint_dir.mkdir(parents=True)
+            (result_dir / "run_metadata.json").write_bytes(recovery.json_bytes({**old_settings, "run_id": old_run,
+                                                                               "started_at": "2026-11-13T00:00:00+09:00"}))
+            for sigma, epoch in [(0, 100), (1, 65)]:
+                control = training.TrainingControl(enabled=False)
+                control.best_raw_loss = control.meaningful_best_loss = .5
+                control.best_raw_epoch = control.shadow_best_raw_epoch = 1
+                control.shadow_stop_epoch, control.stale_epochs = 16, epoch - 1
+                control.optimizer_steps = epoch * 2
+                model = TinyModel()
+                optimizer, scheduler = training.build_optimizer_scheduler(model.parameters(), config)
+                history = [{"sigma": sigma, "epoch": i} for i in range(1, epoch + 1)]
+                basic = {"run_id": old_run, "sigma": sigma, "epoch": 1, "model": model.state_dict()}
+                prefix_path = checkpoint_dir / f"sigma_{sigma}_shadow_prefix_best.pt"
+                torch.save(basic, prefix_path)
+                torch.save(basic, checkpoint_dir / f"sigma_{sigma}_best.pt")
+                last = {**basic, "epoch": epoch, "optimizer": optimizer.state_dict(), "scheduler": scheduler.state_dict(),
+                        "scaler": {}, "training_control": control.state_dict(), "torch_rng_state": torch.get_rng_state(),
+                        "cuda_rng_state": [], "shadow_prefix_sha256": recovery.file_digest(prefix_path), "history": history}
+                torch.save(last, checkpoint_dir / f"sigma_{sigma}_last.pt")
+                (result_dir / f"sigma_{sigma}_history.json").write_bytes(recovery.json_bytes(history))
+                if sigma == 0:
+                    metric = {"run_id": old_run, "sigma": 0, "epochs_ran": 100, "optimizer_steps": 200,
+                              "completed_at": "원본 완료", "test": {"accuracy": 1.0, "n_images": 2, "confusion_matrix": [[1, 0], [0, 1]]},
+                              "early_stopping_comparison": {"available": True, "checkpoint_sha256": recovery.file_digest(prefix_path)}}
+                    (result_dir / "sigma_0_metrics.json").write_bytes(recovery.json_bytes(metric))
+            files = {p.relative_to(source).as_posix(): recovery.file_digest(p) for p in source.rglob("*") if p.is_file()}
+            baseline = {"source_files": files, "source_run_id": old_run, "source_config": config,
+                        "reference_relative_path": "reference.json", "reference_file_sha256": config["expected_reference_manifest_sha256"],
+                        "reference_records_sha256": manifest["manifest_sha256"], "source_dataset_prefix": str(old_data),
+                        "target_dataset_prefix": str(new_data), "transfer": {"0": {"epoch": 100, "completed": True},
+                                                                               "1": {"epoch": 65, "completed": False}}}
+            baseline_path = base / "baseline.json"
+            baseline_path.write_bytes(recovery.json_bytes(baseline))
+            new_manifest = recovery.relocate_manifest(manifest, str(old_data), str(new_data))
+            new_config = recovery.relocated_config(config, str(new_data), new_manifest)
+            (target / "config.json").write_bytes(recovery.json_bytes(new_config))
+            with mock.patch.object(recovery, "prepare_dataset", return_value=new_manifest):
+                lineage = recovery.import_recovery(target, source, baseline_path, recovery.file_digest(baseline_path))
+            self.assertNotEqual(lineage["run_id"], old_run)
+            self.assertEqual(lineage["transfer"]["1"]["next_epoch"], 66)
+            recovery.verify_files(source, files)
+            state = StatusWriter(target, new_config)
+            epochs, tested = [], []
+            actual_update, actual_evaluate = state.update, training.evaluate
+
+            def update(**values):
+                if values.get("stage") == "training" and values.get("batch") == 0:
+                    epochs.append((state.data["sigma"], values["epoch"]))
+                return actual_update(**values)
+
+            def evaluate(*args, **kwargs):
+                if kwargs.get("stage") == "testing":
+                    tested.append((state.data["sigma"], state.data["epoch"]))
+                return actual_evaluate(*args, **kwargs)
+
+            with mock.patch.object(training, "prepare_dataset", return_value=new_manifest), \
+                    mock.patch.object(training, "SplitResNet50", TinyModel), \
+                    mock.patch.object(training, "evaluate", side_effect=evaluate), \
+                    mock.patch.object(state, "update", side_effect=update), redirect_stdout(io.StringIO()):
+                training.run_training(new_config, target, state, "cpu")
+            self.assertEqual(epochs[0], (1, 66))
+            self.assertEqual(epochs[-1], (1, 100))
+            self.assertEqual(len(epochs), 35)
+            self.assertEqual(tested, [(1, 100), (1, 100)])
+            self.assertEqual(state.data["stage"], "completed")
+            recovery.verify_import(target, initial=False)
+            # prefix 변조는 다음 실행 경계에서 차단됩니다.
+            frozen = target / f"work/checkpoints/run_{lineage['run_id']}/sigma_1_shadow_prefix_best.pt"
+            frozen.write_bytes("변조".encode("utf-8"))
+            with self.assertRaises(ValueError):
+                recovery.verify_import(target, initial=False)
+
+
+class WorkerParentTests(unittest.TestCase):
+    def test_direct_supervisor_parent_is_accepted(self):
+        with mock.patch.object(safe_training.os, "getppid", return_value=42):
+            self.assertTrue(safe_training.worker_parent_authorized("42"))
+
+    def test_exact_venv_launcher_between_supervisor_and_worker_is_accepted(self):
+        row = {"ProcessId": 50, "ParentProcessId": 42, "ExecutablePath": safe_training.sys.executable}
+        with mock.patch.object(safe_training.os, "getppid", return_value=50), \
+                mock.patch.object(safe_training, "windows_process", return_value=row):
+            self.assertTrue(safe_training.worker_parent_authorized("42"))
+
+    def test_wrong_launcher_parent_pid_and_executable_are_rejected(self):
+        valid = {"ProcessId": 50, "ParentProcessId": 42, "ExecutablePath": safe_training.sys.executable}
+        for changes in ({"ProcessId": 51}, {"ParentProcessId": 43},
+                        {"ExecutablePath": "C:/다른환경/python.exe"}, {"ExecutablePath": None}):
+            with self.subTest(changes=changes), \
+                    mock.patch.object(safe_training.os, "getppid", return_value=50), \
+                    mock.patch.object(safe_training, "windows_process", return_value={**valid, **changes}):
+                self.assertFalse(safe_training.worker_parent_authorized("42"))
+
+    def test_missing_or_malformed_supervisor_id_is_rejected(self):
+        for value in (None, "", "0", "-1", "42;exit", "４２"):
+            with self.subTest(value=value):
+                self.assertFalse(safe_training.worker_parent_authorized(value))
+
+    def test_launcher_query_failure_does_not_authorize_worker(self):
+        with mock.patch.object(safe_training.os, "getppid", return_value=50), \
+                mock.patch.object(safe_training, "windows_process", side_effect=RuntimeError("CIM 조회 실패")):
+            with self.assertRaises(RuntimeError):
+                safe_training.worker_parent_authorized("42")
+
+
+class DuplicateCommandTests(unittest.TestCase):
+    def processes(self, command):
+        rows = [{"ProcessId": 900000001, "ParentProcessId": 900000002,
+                 "ExecutablePath": "C:/Python/python.exe", "CommandLine": command},
+                {"ProcessId": safe_training.os.getpid(), "ParentProcessId": safe_training.os.getppid(),
+                 "ExecutablePath": "C:/Python/python.exe", "CommandLine": "자기 프로세스"}]
+        response = mock.Mock(returncode=0, stdout=json.dumps(rows), stderr="")
+        with mock.patch.object(safe_training.subprocess, "run", return_value=response):
+            return safe_training.training_processes(Path("E:/가상/실험"))
+
+    def test_relative_training_entry_is_ambiguous_and_blocks_start(self):
+        for script in ("run_training.py", '"run_training.py"', ".\\run_training.py",
+                       "../5차/복구_학습.py", '"상대 폴더/run_training.py"', "-m run_training"):
+            with self.subTest(script=script):
+                found = self.processes('"C:/Python/python.exe" ' + script + " train --device cuda")
+                self.assertEqual([row["pid"] for row in found], [900000001])
+                with self.assertRaises(RuntimeError):
+                    safe_training.reject_duplicates(found)
+
+    def test_explicit_other_project_is_excluded_and_same_project_both_drives_block(self):
+        self.assertEqual(self.processes('"C:/Python/python.exe" "E:/다른 프로젝트/run_training.py" train'), [])
+        for drive in ("D", "E"):
+            with self.subTest(drive=drive):
+                found = self.processes(f'"C:/Python/python.exe" "{drive}:/가상/실험/4차/run_training.py" train')
+                self.assertEqual([row["pid"] for row in found], [900000001])
+
+    def test_cim_query_failure_blocks_instead_of_returning_no_conflicts(self):
+        response = mock.Mock(returncode=1, stdout="", stderr="CIM 조회 실패")
+        with mock.patch.object(safe_training.subprocess, "run", return_value=response):
+            with self.assertRaises(RuntimeError):
+                safe_training.training_processes(Path("E:/가상/실험"))
+
+    def test_only_cim_confirmed_own_venv_launcher_is_excluded(self):
+        own = {"ProcessId": 42, "ParentProcessId": 50, "ExecutablePath": "C:/Python/python.exe", "CommandLine": "자기 프로세스"}
+        for launcher_pid, executable, expected in ((50, safe_training.sys.executable, []),
+                                                   (50, "C:/다른환경/python.exe", [50]),
+                                                   (51, safe_training.sys.executable, [51])):
+            rows = [own, {"ProcessId": launcher_pid, "ParentProcessId": 10, "ExecutablePath": executable,
+                          "CommandLine": '"C:/Python/python.exe" "E:/가상/실험/5차/복구_학습.py"'}]
+            response = mock.Mock(returncode=0, stdout=json.dumps(rows), stderr="")
+            with self.subTest(pid=launcher_pid, executable=executable), \
+                    mock.patch.object(safe_training.os, "getpid", return_value=42), \
+                    mock.patch.object(safe_training.os, "getppid", return_value=50), \
+                    mock.patch.object(safe_training.subprocess, "run", return_value=response):
+                self.assertEqual([row["pid"] for row in safe_training.training_processes(Path("E:/가상/실험"))], expected)
+
+    def test_unconfirmed_own_cim_parent_relation_blocks_start(self):
+        rows = [{"ProcessId": 42, "ParentProcessId": 51, "CommandLine": "자기 프로세스"}]
+        response = mock.Mock(returncode=0, stdout=json.dumps(rows), stderr="")
+        with mock.patch.object(safe_training.os, "getpid", return_value=42), \
+                mock.patch.object(safe_training.os, "getppid", return_value=50), \
+                mock.patch.object(safe_training.subprocess, "run", return_value=response):
+            with self.assertRaises(RuntimeError):
+                safe_training.training_processes(Path("E:/가상/실험"))
+
+
+if __name__ == "__main__":
+    unittest.main()
````

## tests/test_return_recovery.py

이전 0 B / SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. 이후 13,244 B / SHA-256 `9e79cc9d902a31cc7c6417ab362009fa184372be374a2e95ba7b8fa4bf07e2f5`.

````diff
--- 이전/tests/test_return_recovery.py
+++ 이후/tests/test_return_recovery.py
@@ -0,0 +1,219 @@
+"""관찰용 종료 전의 부분 상태와 E 원본이 없는 D 재개를 합성 CPU 자료로 검사합니다."""
+
+import copy
+import hashlib
+import io
+import json
+from contextlib import redirect_stdout
+from pathlib import Path
+import tempfile
+import unittest
+from unittest import mock
+
+import numpy as np
+from PIL import Image
+import torch
+
+from tools import recovery
+from src import training
+from src.state import StatusWriter
+
+
+class TinyReturnModel(torch.nn.Module):
+    def __init__(self, **kwargs):
+        super().__init__()
+        self.weight = torch.nn.Parameter(torch.tensor(1.0))
+
+    def forward(self, images):
+        return (images.mean((1, 2, 3)) - .5) * self.weight
+
+
+class UnfrozenReturnTests(unittest.TestCase):
+    def fixture(self, folder):
+        base = Path(folder)
+        source, target = base / "이전_실행", base / "D_복귀"
+        old_data, new_data = base / "이전_영상", base / "D_영상"
+        for root in (source, target):
+            (root / "src").mkdir(parents=True)
+            for name in recovery.SCIENTIFIC:
+                (root / name).write_text("# 합성 고정 학습 소스\n", encoding="utf-8")
+        records, splits = [], {}
+        for split in ("train", "validation", "test"):
+            splits[split] = []
+            for label in (0, 1):
+                relative = f"{split}_{label}.png"
+                for root in (old_data, new_data):
+                    root.mkdir(exist_ok=True)
+                    Image.fromarray(np.full((8, 8), 40 + 160 * label, dtype=np.uint8)).save(root / relative)
+                row = {"path": str(old_data / relative), "relative_path": relative, "label": label,
+                       "source_class": "Normal cases" if label == 0 else "Malignant cases",
+                       "byte_sha256": recovery.file_digest(old_data / relative)}
+                records.append(row)
+                splits[split].append(copy.deepcopy(row))
+        manifest = {"records": records, "splits": splits, "summary": {},
+                    "manifest_sha256": recovery.records_digest(records)}
+        config = {"dataset_root": str(old_data), "seed": 42, "cpu_threads": 1, "precision": "fp32",
+                  "epochs": 4, "early_stopping_enabled": False, "early_stopping_patience": 2,
+                  "min_delta": .0001, "batch_size": 1, "samples_per_class": 1, "image_size": 8,
+                  "learning_rate": .00003, "weight_decay": .0001, "scheduler_patience": 4,
+                  "scheduler_factor": .5, "min_learning_rate": .000001, "num_workers": 0,
+                  "sigmas": [0, 2], "status_every_batches": 1,
+                  "expected_reference_manifest": "reference.json",
+                  "expected_reference_manifest_sha256": hashlib.sha256(recovery.json_bytes(manifest)).hexdigest(),
+                  "expected_reference_records_sha256": manifest["manifest_sha256"]}
+        (source / "work/results").mkdir(parents=True)
+        (source / "config.json").write_bytes(recovery.json_bytes(config))
+        (source / "reference.json").write_bytes(recovery.json_bytes(manifest))
+        (source / "work/results/dataset_manifest_private.json").write_bytes(recovery.json_bytes(manifest))
+        old_run, settings = training._run_identity(source, config, manifest["manifest_sha256"])
+        results = source / f"work/results/run_{old_run}"
+        checkpoints = source / f"work/checkpoints/run_{old_run}"
+        results.mkdir(parents=True)
+        checkpoints.mkdir(parents=True)
+        (results / "run_metadata.json").write_bytes(recovery.json_bytes({**settings, "run_id": old_run,
+                                                                          "started_at": "합성 원본 시각"}))
+        for sigma, epoch in ((0, 4), (2, 1)):
+            control = training.TrainingControl(.0001, 2, enabled=False)
+            control.best_raw_loss = control.meaningful_best_loss = .00001
+            control.best_raw_epoch = 1
+            control.optimizer_steps = epoch * 2
+            model = TinyReturnModel()
+            optimizer, scheduler = training.build_optimizer_scheduler(model.parameters(), config)
+            basic = {"run_id": old_run, "sigma": sigma, "epoch": 1, "model": model.state_dict()}
+            prefix_hash = None
+            if sigma == 0:
+                control.shadow_stop_epoch, control.shadow_best_raw_epoch, control.stale_epochs = 3, 1, 3
+                prefix = checkpoints / "sigma_0_shadow_prefix_best.pt"
+                torch.save(basic, prefix)
+                prefix_hash = recovery.file_digest(prefix)
+            history = [{"sigma": sigma, "epoch": i} for i in range(1, epoch + 1)]
+            torch.save(basic, checkpoints / f"sigma_{sigma}_best.pt")
+            torch.save({**basic, "epoch": epoch, "optimizer": optimizer.state_dict(),
+                        "scheduler": scheduler.state_dict(), "scaler": {},
+                        "training_control": control.state_dict(), "torch_rng_state": torch.get_rng_state(),
+                        "cuda_rng_state": [], "shadow_prefix_sha256": prefix_hash, "history": history},
+                       checkpoints / f"sigma_{sigma}_last.pt")
+            (results / f"sigma_{sigma}_history.json").write_bytes(recovery.json_bytes(history))
+            if sigma == 0:
+                metric = {"run_id": old_run, "sigma": 0, "epochs_ran": 4, "optimizer_steps": 8,
+                          "completed_at": "합성 완료", "test": {"accuracy": 1.0, "n_images": 2,
+                                                                     "confusion_matrix": [[1, 0], [0, 1]]},
+                          "early_stopping_comparison": {"available": True, "checkpoint_sha256": prefix_hash}}
+                (results / "sigma_0_metrics.json").write_bytes(recovery.json_bytes(metric))
+        baseline = {"source_files": {}, "source_run_id": old_run, "source_config": config,
+                    "reference_relative_path": "reference.json",
+                    "reference_file_sha256": config["expected_reference_manifest_sha256"],
+                    "reference_records_sha256": manifest["manifest_sha256"],
+                    "source_dataset_prefix": str(old_data), "target_dataset_prefix": str(new_data),
+                    "transfer": {"0": {"epoch": 4, "completed": True}, "2": {"epoch": 1, "completed": False}}}
+        baseline_path = target / "work/recovery/복귀_기준.json"
+        baseline_path.parent.mkdir(parents=True)
+        new_manifest = recovery.relocate_manifest(manifest, str(old_data), str(new_data))
+        new_config = recovery.relocated_config(config, str(new_data), new_manifest)
+        (target / "config.json").write_bytes(recovery.json_bytes(new_config))
+        return {"source": source, "target": target, "old_run": old_run, "checkpoints": checkpoints,
+                "baseline": baseline, "baseline_path": baseline_path, "manifest": new_manifest,
+                "config": new_config}
+
+    def import_fixture(self, value):
+        source = value["source"]
+        value["baseline"]["source_files"] = {p.relative_to(source).as_posix(): recovery.file_digest(p)
+                                                for p in source.rglob("*") if p.is_file()}
+        value["baseline_path"].write_bytes(recovery.json_bytes(value["baseline"]))
+        with mock.patch.object(recovery, "prepare_dataset", return_value=value["manifest"]):
+            return recovery.import_recovery(value["target"], source, value["baseline_path"],
+                                             recovery.file_digest(value["baseline_path"]))
+
+    def test_none_prefix_hash_is_preserved_without_fabricating_a_checkpoint(self):
+        source = {"run_id": "a" * 16, "sigma": 2, "epoch": 20, "shadow_prefix_sha256": None,
+                  "model": {"weight": torch.tensor([2.0])}, "training_control": {"shadow_stop_epoch": 0}}
+        restored = recovery.rebind_checkpoint(source, "a" * 16, "b" * 16, 2)
+        self.assertIsNone(restored["shadow_prefix_sha256"])
+        recovery.assert_state_equal(source["model"], restored["model"])
+        self.assertEqual(restored["training_control"]["shadow_stop_epoch"], 0)
+
+    def test_partial_before_shadow_stop_imports_without_a_prefix_and_source_access(self):
+        with tempfile.TemporaryDirectory() as folder:
+            value = self.fixture(folder)
+            lineage = self.import_fixture(value)
+            self.assertEqual(lineage["transfer"]["2"]["next_epoch"], 2)
+            self.assertNotIn("sigma_2_shadow_prefix_best.pt", lineage["converted_checkpoints"])
+            checkpoint_dir = value["target"] / f"work/checkpoints/run_{lineage['run_id']}"
+            self.assertFalse((checkpoint_dir / "sigma_2_shadow_prefix_best.pt").exists())
+            old_last = torch.load(value["checkpoints"] / "sigma_2_last.pt", map_location="cpu", weights_only=False)
+            new_last = torch.load(checkpoint_dir / "sigma_2_last.pt", map_location="cpu", weights_only=False)
+            recovery.assert_state_equal({k: v for k, v in old_last.items() if k != "run_id"},
+                                        {k: v for k, v in new_last.items() if k != "run_id"})
+            value["source"].rename(Path(folder) / "접근불가_이전_실행")
+            result = recovery.verify_import(value["target"], initial=True)
+            self.assertTrue(result["verified"])
+
+    def test_missing_frozen_prefix_and_orphan_prefix_states_are_rejected(self):
+        for corruption in ("종료만기록", "해시만기록", "고아파일", "최적시점만기록"):
+            with self.subTest(corruption=corruption), tempfile.TemporaryDirectory() as folder:
+                value = self.fixture(folder)
+                path = value["checkpoints"] / "sigma_2_last.pt"
+                last = torch.load(path, map_location="cpu", weights_only=False)
+                if corruption == "종료만기록":
+                    last["training_control"].update(shadow_stop_epoch=1, shadow_best_raw_epoch=1)
+                elif corruption == "해시만기록":
+                    last["shadow_prefix_sha256"] = "f" * 64
+                elif corruption == "최적시점만기록":
+                    last["training_control"]["shadow_best_raw_epoch"] = 1
+                else:
+                    torch.save({"run_id": value["old_run"], "sigma": 2, "epoch": 1},
+                               value["checkpoints"] / "sigma_2_shadow_prefix_best.pt")
+                torch.save(last, path)
+                with self.assertRaises(ValueError):
+                    self.import_fixture(value)
+
+    def test_existing_frozen_prefix_requires_original_hash_before_rebinding(self):
+        with tempfile.TemporaryDirectory() as folder:
+            value = self.fixture(folder)
+            path = value["checkpoints"] / "sigma_0_last.pt"
+            last = torch.load(path, map_location="cpu", weights_only=False)
+            last["shadow_prefix_sha256"] = "f" * 64
+            torch.save(last, path)
+            with self.assertRaises(ValueError):
+                self.import_fixture(value)
+
+    def test_real_cpu_resume_creates_future_prefix_and_preserves_completed_result(self):
+        with tempfile.TemporaryDirectory() as folder:
+            value = self.fixture(folder)
+            lineage = self.import_fixture(value)
+            value["source"].rename(Path(folder) / "접근불가_이전_실행")
+            root, config = value["target"], value["config"]
+            result_dir = root / f"work/results/run_{lineage['run_id']}"
+            saved_metric = (result_dir / "sigma_0_metrics.json").read_bytes()
+            state = StatusWriter(root, config)
+            epochs, tested = [], []
+            actual_update, actual_evaluate = state.update, training.evaluate
+
+            def update(**values):
+                if values.get("stage") == "training" and values.get("batch") == 0:
+                    epochs.append((state.data["sigma"], values["epoch"]))
+                return actual_update(**values)
+
+            def evaluate(*args, **kwargs):
+                if kwargs.get("stage") == "testing":
+                    tested.append((state.data["sigma"], state.data["epoch"]))
+                return actual_evaluate(*args, **kwargs)
+
+            with mock.patch.object(training, "prepare_dataset", return_value=value["manifest"]), \
+                    mock.patch.object(training, "SplitResNet50", TinyReturnModel), \
+                    mock.patch.object(training, "evaluate", side_effect=evaluate), \
+                    mock.patch.object(state, "update", side_effect=update), redirect_stdout(io.StringIO()):
+                training.run_training(config, root, state, "cpu")
+            self.assertEqual(epochs, [(2, 2), (2, 3), (2, 4)])
+            self.assertEqual(tested, [(2, 4), (2, 4)])
+            self.assertEqual((result_dir / "sigma_0_metrics.json").read_bytes(), saved_metric)
+            self.assertTrue(recovery.verify_import(root, initial=False)["verified"])
+            prefix = root / f"work/checkpoints/run_{lineage['run_id']}/sigma_2_shadow_prefix_best.pt"
+            self.assertTrue(prefix.is_file())
+            prefix.write_bytes(b"tampered-prefix")
+            with self.assertRaises(ValueError):
+                recovery.verify_import(root, initial=False)
+
+
+if __name__ == "__main__":
+    unittest.main()
````

## tests/test_sigma_selection.mjs

이전 6,886 B / SHA-256 `82e9bc92d38c3e25404e6fea11650e9c3af722cb61d6023097fb32bd49eda1a7`. 이후 0 B / SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

````diff
--- 이전/tests/test_sigma_selection.mjs
+++ 이후/tests/test_sigma_selection.mjs
@@ -1,76 +0,0 @@
-import assert from 'node:assert/strict';
-import fs from 'node:fs';
-import vm from 'node:vm';
-// 실제 선택 함수와 응답 처리를 읽어 지연 응답의 순서만 제어합니다.
-const source=fs.readFileSync('web/app.js','utf8');
-class Element {
-  constructor(){this.children=[];this.dataset={};this.attrs={};this.textContent='';}
-  append(...nodes){this.children.push(...nodes);}
-  querySelector(selector){return selector==='small'?this.children[1]:this.children.find(x=>String(x.dataset.sigma)===selector.match(/"(\d+)"/)?.[1]);}
-  replaceChildren(...nodes){this.children=nodes;}
-  addEventListener(){}
-  setAttribute(key,value){this.attrs[key]=value;}
-}
-const nodes=new Map(),requests=[],charts=[];
-const context={console,AbortController,setTimeout,clearTimeout,
-  $:id=>{if(!nodes.has(id))nodes.set(id,new Element());return nodes.get(id);},
-  states:{completed:'완료'},document:{createElement:()=>new Element()},
-  pipeline:{setSelectedSigma(){}},drawChart:s=>charts.push(s),
-  fetch:(url)=>new Promise(resolve=>requests.push({url,resolve}))};
-vm.createContext(context);
-const start=source.indexOf('const number ='),end=source.indexOf('let pipeline =');
-vm.runInContext(source.slice(start,end)+`;globalThis.api={selectSigma,loadSelectedResult,renderQueue,percent,fullPercent,rawNumber,decimalShift,getSigma:()=>selectedSigma,getResult:()=>selectedResult,setState:s=>{latest=s;selectionRun=s.run_id;}};`,context);
-const display=context.api;
-const percentCases=[
- [.9878048780487805,'98.8%'],[.5365853658536586,'53.7%'],[1,'100.0%'],[0,'0.0%'],[.99999,'100.0%'],[.25,'25.0%'],[1e-7,'0.0%'],
- [.9878,'98.8%'],[.29,'29.0%'],[131/164,'79.9%'],[102/164,'62.2%'],[163/164,'99.4%'],[159/164,'97.0%'],[.0001,'0.0%'],
- [.9995,'100.0%'],[.9994999999999999,'99.9%'],[.0055,'0.6%'],[.0005,'0.1%'],[.0015,'0.2%'],[.2995,'30.0%']
-];
-for(const [value,expected] of percentCases)assert.equal(display.percent(value),expected);
-for(const value of [null,undefined,NaN,Infinity,-.01,1.01])assert.equal(display.percent(value),'미측정');
-assert.equal(display.fullPercent(.9878048780487805),'98.78048780487805%');
-assert.equal(display.fullPercent(1e-7),'0.00001%');
-assert.equal(display.rawNumber(.9999999999999999),'0.9999999999999999');
-assert.equal(display.rawNumber(3e-5),'0.00003');
-assert.equal(display.rawNumber(1e-16),'1e-16');
-assert.equal(display.rawNumber(0),'0');
-assert.equal(display.rawNumber(null),'미측정');
-const api=context.api,run='0123456789abcdef',sigmas=[0,1,2,4,8,16,32,64,128,256];
-const state={run_id:run,sigma:256,sigma_queue:sigmas.map(sigma=>({sigma,status:'completed'}))};api.setState(state);
-const payload=(sigma,run_id=run)=>({run_id,sigma,status:'completed',message:'완료',history:[{sigma,epoch:sigma===256?16:17}],metrics:{best_epoch:15,epochs_ran:sigma===256?16:17,optimizer_steps:10,test:{accuracy:sigma===256?.537:1,auc:sigma===256?.573:1}}});
-const settle=async(req,data)=>{req.resolve({ok:true,json:async()=>data});await new Promise(resolve=>setImmediate(resolve));};
-// 실제 조회 함수에 준비 상태를 전달해 요청 수와 표시 결과를 검사합니다.
-for(const run_id of [undefined,null,'','not-a-run',123]){
-  api.setState({status:'ready',run_id,history:[]});
-  api.selectSigma(0);
-  assert.equal(requests.length,0,'유효한 실행 ID가 없으면 결과를 조회하지 않아야 합니다');
-  assert.match(nodes.get('selectionNote').textContent,/학습 결과.*기다/);
-  assert.equal(nodes.get('testAccuracy').textContent,'미측정');
-  assert.equal(api.getResult(),null);
-}
-api.setState(state);
-for(const sigma of sigmas){api.selectSigma(sigma);const req=requests.at(-1);assert.equal(req.url,`/api/sigma-results/${sigma}`);await settle(req,payload(sigma));assert.equal(api.getResult().sigma,sigma);assert.equal(charts.at(-1).sigma,sigma);}
-api.selectSigma(0);const old=requests.at(-1);api.selectSigma(256);const middle=requests.at(-1);api.selectSigma(0);const newest=requests.at(-1);
-await settle(newest,payload(0));await settle(middle,payload(256));await settle(old,payload(0));assert.equal(api.getResult().sigma,0);assert.equal(nodes.get('testAccuracy').textContent,'100.0%');
-const queueNodes=[...nodes.get('queue').children];api.renderQueue(state);assert.deepEqual(nodes.get('queue').children,queueNodes);assert.equal(api.getSigma(),0);
-const count=requests.length;api.loadSelectedResult();api.loadSelectedResult();assert.equal(requests.length,count+1);await settle(requests.at(-1),payload(0,'fedcba9876543210'));assert.equal(api.getResult(),null);assert.equal(nodes.get('testAccuracy').textContent,'미측정');
-api.selectSigma(3);assert.equal(api.getSigma(),0);
-api.selectSigma(8);const precise=payload(8);precise.metrics.test={accuracy:.9878048780487805,auc:.9999999999999999,loss:1e-16};await settle(requests.at(-1),precise);
-assert.equal(nodes.get('testAccuracy').textContent,'98.8%');
-assert.equal(nodes.get('testAccuracyRaw').textContent,'0.9878048780487805');
-assert.equal(nodes.get('testAccuracyFull').textContent,'98.78048780487805%');
-assert.equal(nodes.get('testAuc').textContent,'0.9999999999999999');
-assert.equal(nodes.get('testLossRaw').textContent,'1e-16');
-precise.metrics.test.correct_count=162;precise.metrics.test.n_images=164;api.selectSigma(4);const countResult=payload(4);countResult.metrics.test=precise.metrics.test;await settle(requests.at(-1),countResult);assert.equal(nodes.get('testCorrectCount').textContent,'정답 162 / 164장');
-api.selectSigma(16);const undefinedAuc=payload(16);undefinedAuc.metrics.test.auc=null;await settle(requests.at(-1),undefinedAuc);assert.equal(nodes.get('testAuc').textContent,'정의 불가');
-
-// 시작 전 상태로 돌아오면 이전 응답도 결과를 다시 채우지 않습니다.
-api.selectSigma(0);const beforeReady=requests.at(-1),readyRequestCount=requests.length;
-api.setState({status:'ready',history:[]});api.selectSigma(0);
-assert.equal(requests.length,readyRequestCount);assert.equal(api.getResult(),null);assert.equal(nodes.get('testAccuracy').textContent,'미측정');
-await settle(beforeReady,payload(0));assert.equal(api.getResult(),null);assert.equal(nodes.get('testAccuracy').textContent,'미측정');
-api.setState(state);api.selectSigma(0);await settle(requests.at(-1),payload(0));assert.equal(api.getResult().run_id,run);assert.equal(nodes.get('testAccuracy').textContent,'100.0%');
-console.log('실행 준비 회귀 PASS: 실행 ID 없는 5상태 조회0회·대기·미측정, 이전 응답 거부, 유효 ID 생성 뒤 조회');
-// 새 실행의 응답 전 비우기와 이전 실행 응답 거부는 Python의 실제 render 실행 회귀에 결합합니다.
-console.log(`수치 표시 PASS: 백분율 ${percentCases.length}개·미측정/범위 6개·원값 7개·실제결과표시 7개`);
-console.log('선택 회귀 PASS: 강도10개, 0→256→0 역순응답, 중복요청, 다른실행, 잘못된강도, 버튼재사용');
````

## tools/__init__.py

이전 0 B / SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. 이후 71 B / SHA-256 `52d172d3c27451a3d4c303c62a384276921f1dbbbb8c3d3a9940889f39bf4c70`.

````diff
--- 이전/tools/__init__.py
+++ 이후/tools/__init__.py
@@ -0,0 +1 @@
+"""학습 알고리즘과 분리한 이관·운영 도구입니다."""
````

## tools/feature_generator.py

이전 0 B / SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. 이후 16,828 B / SHA-256 `ef1a0636466785479e919a2426675b805a43cea10560def518cb4e2106d9a675`.

````diff
--- 이전/tools/feature_generator.py
+++ 이후/tools/feature_generator.py
@@ -0,0 +1,279 @@
+"""완료한 실험만 CPU에서 읽어 참고 자료와 같은 폴더·패널 구성으로 저장합니다."""
+import argparse
+from datetime import datetime, timezone, timedelta
+import hashlib
+import json
+import os
+from pathlib import Path
+import sys
+import time
+import traceback
+
+PROJECT = Path(__file__).resolve().parents[2]
+HERE = PROJECT / '블러 강도별 대표 특징맵' / '5차'
+TRAIN = PROJECT / '5차'
+REFERENCE = PROJECT.parent / '블러 엣지' / '블러 피쳐맵 저장 파일'
+RUN = None
+SIGMAS = [0, 1, 2, 4, 8, 16, 32, 64, 128, 256]
+CLASSES = [('Bengin_cases', 'Bengin cases', '양성 · OK'),
+           ('Malignant_cases', 'Malignant cases', '악성 · NG'),
+           ('Normal_cases', 'Normal cases', '정상 · OK')]
+LAYERS = ['입력 회색조 CT', 'conv1 → GaussianDCTBlur 직후',
+          'cloud.layer1 출력', 'cloud.layer2 출력', 'cloud.layer3 출력', 'cloud.layer4 출력']
+MEANINGS = ['실제 입력 CT를 512×512 회색조로 맞춘 영상입니다. 3채널에 같은 값을 복제해 모델에 입력합니다.',
+            '첫 합성곱이 추출한 윤곽·질감 반응에 블러를 적용한 전송 특징입니다. 아직 BN·ReLU·최대 풀링을 거치지 않았습니다.',
+            '전송 특징이 BN·ReLU·최대 풀링과 첫 잔차 블록 묶음을 통과한 결과입니다.',
+            '두 번째 잔차 블록 묶음이 공간 크기를 줄이며 조합한 특징입니다.',
+            '세 번째 잔차 블록 묶음이 더 넓은 영역의 반응을 조합한 특징입니다.',
+            '마지막 잔차 블록 묶음의 출력입니다. 이후 전역 평균 풀링과 분류기로 OK·NG를 계산합니다.']
+
+def now():
+    return datetime.now(timezone(timedelta(hours=9))).isoformat(timespec='seconds')
+
+def digest(path):
+    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
+
+def read_json(path):
+    # 확인한 Windows 공유·접근 잠금만 합계 0.63초 이내로 재시도합니다.
+    # 잘못된 JSON·공간 부족·지속 오류는 감추지 않고 감시를 종료합니다.
+    delays = (0.01, 0.02, 0.04, 0.08, 0.16, 0.32)
+    for attempt in range(len(delays) + 1):
+        try:
+            return json.loads(Path(path).read_text(encoding='utf-8'))
+        except PermissionError as error:
+            if getattr(error, 'winerror', None) not in {5, 32} or attempt == len(delays):
+                raise
+            time.sleep(delays[attempt])
+
+def atomic_json(path, value):
+    temporary = path.with_suffix('.tmp')
+    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')
+    # 대시보드의 짧은 읽기 핸들과 충돌하면 제한된 횟수만 재시도합니다.
+    for attempt in range(6):
+        try:
+            os.replace(temporary, path)
+            return
+        except PermissionError:
+            if attempt == 5:
+                raise
+            time.sleep(0.1 * (attempt + 1))
+
+def prepare():
+    paths = sorted(p.relative_to(REFERENCE).as_posix() for p in REFERENCE.rglob('*.png'))
+    if len(paths) != 180:
+        raise ValueError('참고 자료의 PNG 180개 계약이 다릅니다.')
+    template_path = HERE / '참고_폴더구성_비공개.json'
+    template = {'reference': str(REFERENCE), 'relative_paths': paths}
+    if template_path.exists():
+        if read_json(template_path) != template:
+            raise ValueError('동결한 참고 폴더 구성과 현재 구성이 다릅니다.')
+    else:
+        atomic_json(template_path, template)
+    for relative in paths:
+        (HERE / '블러 피쳐맵 저장 파일' / relative).parent.mkdir(parents=True, exist_ok=True)
+    return paths
+
+def render(array, stage, sigma, label, destination):
+    channels = array.shape[0]
+    shape = list(array.shape)
+    caption = MEANINGS[stage]
+    if stage:
+        caption += ' 색은 특징의 상대적인 반응을 뜻하며 병변 위치나 프라이버시 보장을 뜻하지 않습니다.'
+        indices = [i * channels // 8 for i in range(8)]
+        panels = [array.mean(axis=0), array.max(axis=0)] + [array[i] for i in indices]
+        titles = ['전체 채널 평균', '채널별 최댓값'] + [f'채널 {i} / {channels}' for i in indices]
+        fig, axes = plt.subplots(2, 5, figsize=(20, 11), dpi=120)
+        for i, (axis, panel, title) in enumerate(zip(axes.flat, panels, titles)):
+            axis.imshow(panel, cmap='hot' if i == 1 else 'viridis', interpolation='nearest')
+            axis.set_title(title, fontproperties=FONT, fontsize=13, pad=10)
+            axis.axis('off')
+        fig.subplots_adjust(left=.025, right=.975, top=.83, bottom=.17, wspace=.12, hspace=.20)
+        caption += ' 각 패널은 자기 최솟값·최댓값으로 정규화하므로 서로 다른 패널의 색 크기를 직접 비교할 수 없습니다.'
+        note = '전체 채널 평균 · 채널별 최댓값 · 균등 간격의 개별 채널 8개 (총 10패널)'
+    else:
+        caption += ' 회색조의 밝기는 입력 픽셀 밝기이며 악성 확률이 아닙니다.'
+        indices = []
+        panels = [array[0]]
+        fig, axis = plt.subplots(figsize=(9, 10), dpi=120)
+        axis.imshow(array[0], cmap='gray', vmin=0, vmax=1)
+        axis.axis('off')
+        fig.subplots_adjust(top=.83, bottom=.21, left=.08, right=.92)
+        note = '원본 입력 1장 · 평가 전처리 · 증강 없음'
+    fig.suptitle(f'{label}  |  블러 강도 {sigma}  |  단계 {stage}: {LAYERS[stage]}', fontproperties=FONT, fontsize=18, y=.965)
+    fig.text(.5, .90, f'{note}\n텐서: {shape[0]}채널 × {shape[1]} × {shape[2]} · 완료한 최적 체크포인트 · FP32 평가',
+             ha='center', va='center', fontproperties=FONT, fontsize=12, linespacing=1.6)
+    import textwrap
+    wrapped = '\n'.join(textwrap.wrap(caption, width=103 if stage else 57))
+    fig.text(.035, .11 if stage else .14, wrapped, va='top', fontproperties=FONT, fontsize=12, linespacing=1.7)
+    if stage == 1:
+        fig.text(.035, .025, '추출 지점 안내: 참고 자료와 프레임워크·전송 경계가 달라 현재 모델의 실제 추출 지점을 표시했습니다.', fontproperties=FONT, fontsize=11)
+    temporary = destination.with_suffix('.tmp')
+    fig.savefig(temporary, format='png', facecolor='white')
+    plt.close(fig)
+    os.replace(temporary, destination)
+    return caption, indices, [{'min': float(p.min()), 'max': float(p.max())} for p in panels]
+
+def run_once(paths):
+    lineage = read_json(TRAIN / 'work/recovery/복구_계보_비공개.json')
+    if lineage.get('run_id') != RUN or lineage.get('source_run_id') == RUN:
+        raise ValueError('5차 복구 계보와 지정 실행이 다릅니다.')
+    config = read_json(TRAIN / 'config.json')
+    if config != lineage['settings']['config']:
+        raise ValueError('5차 복구 후 설정이 변경됐습니다.')
+    for relative, expected in lineage['settings']['source_hashes'].items():
+        if digest(TRAIN / relative) != expected:
+            raise ValueError('5차 복구 후 학습 소스가 변경됐습니다.')
+    state = read_json(TRAIN / 'work/runtime/status.json')
+    if state.get('run_id') != RUN:
+        raise ValueError('현재 학습 run_id가 지정 실행과 다릅니다.')
+    manifest_path = TRAIN / 'work/results/dataset_manifest_private.json'
+    manifest = read_json(manifest_path)
+    if manifest.get('manifest_sha256') != lineage['settings']['manifest_sha256']:
+        raise ValueError('현재 원본 목록이 5차 복구 계보와 다릅니다.')
+    # 저장된 SHA 문자열만 믿지 않고 기준 목록·실제 분할·전체 소스 집합을 다시 대조합니다.
+    from src.data import validate_reference_manifest
+    from src.training import _run_identity
+    validate_reference_manifest(config, TRAIN, manifest)
+    current_run, current_settings = _run_identity(TRAIN, config, manifest['manifest_sha256'])
+    if current_run != RUN or current_settings != lineage['settings']:
+        raise ValueError('현재 설정·원본 목록·학습 소스가 복구 실행 식별자와 다릅니다.')
+    samples = [sorted((r for r in manifest['splits']['train'] if r['source_class'] == source), key=lambda r: r['relative_path'])[0]
+               for _, source, _ in CLASSES]
+    index_path = HERE / 'export_index_private.json'
+    index = read_json(index_path) if index_path.exists() else {
+        'schema_version': 1, 'run_id': RUN, 'recovery_source_run_id': lineage['source_run_id'],
+        'items': [], 'completed_sigmas': [], 'pending_sigmas': SIGMAS,
+        'sample_selection': '학습 분할에서 원본 클래스별 relative_path 정렬 첫 영상',
+        'source_manifest_sha256': digest(manifest_path), 'samples_private': samples,
+        'model_source_sha256': digest(TRAIN / 'src/model.py'),
+        'data_source_sha256': digest(TRAIN / 'src/data.py'),
+        'generator_sha256': digest(Path(__file__)),
+        'reference_panel_layout': '2행 5열: 채널 평균·최댓값·균등 간격 8채널',
+        'stage1_boundary_note': '현재 conv1→DCT 블러 직후이며 참고 자료와 추출 지점·프레임워크가 다를 수 있습니다.'}
+    if (index['run_id'] != RUN or index.get('recovery_source_run_id') != lineage['source_run_id']
+            or index['source_manifest_sha256'] != digest(manifest_path) or index['samples_private'] != samples
+            or index.get('generator_sha256') != digest(Path(__file__))):
+        raise ValueError('기존 출력의 실행·입력 목록이 현재 계약과 다릅니다.')
+    for item in index['items']:
+        if digest(HERE / item['relative_path']) != item['sha256']:
+            raise ValueError('기존 출력 파일의 해시 불일치: ' + item['relative_path'])
+    for sigma in SIGMAS:
+        eligible = any(q['sigma'] == sigma and q['status'] == 'completed' for q in state['sigma_queue'])
+        metrics_path = TRAIN / f'work/results/run_{RUN}/sigma_{sigma}_metrics.json'
+        if not eligible or not metrics_path.is_file():
+            continue
+        metrics = read_json(metrics_path)
+        if metrics['run_id'] != RUN or metrics['sigma'] != sigma or not metrics.get('completed_at'):
+            raise ValueError('완료 지표의 실행 식별자가 다릅니다.')
+        if sigma in index['completed_sigmas']:
+            continue
+        checkpoint_path = TRAIN / f'work/checkpoints/run_{RUN}/sigma_{sigma}_best.pt'
+        checkpoint = torch.load(checkpoint_path, map_location='cpu', weights_only=False)
+        if checkpoint['run_id'] != RUN or checkpoint['sigma'] != sigma or checkpoint['epoch'] != metrics['best_epoch']:
+            raise ValueError('완료 지표와 체크포인트가 일치하지 않습니다.')
+        model = SplitResNet50(sigma=sigma, pretrained=False).eval()
+        model.load_state_dict(checkpoint['model'], strict=True)
+        model_hash = digest(checkpoint_path)
+        batch_items = []
+        for (key, source, label), row in zip(CLASSES, samples):
+            if digest(row['path']) != row['byte_sha256']:
+                raise ValueError('원본 CT 파일 해시가 manifest와 다릅니다.')
+            x, _ = CTDataset([row], image_size=512, training=False)[0]
+            stages = [x.numpy().copy()]
+            with torch.inference_mode():
+                y = model.blur(model.edge((x[None] - model.rgb_mean) / model.rgb_std))
+                stages.append(y[0].numpy().copy())
+                y = model.cloud.maxpool(model.cloud.relu(model.cloud.bn1(y)))
+                for layer in [model.cloud.layer1, model.cloud.layer2, model.cloud.layer3, model.cloud.layer4]:
+                    y = layer(y)
+                    stages.append(y[0].numpy().copy())
+            for stage, array in enumerate(stages):
+                if not np.isfinite(array).all():
+                    raise ValueError('특징 텐서에 비유한 값이 있습니다.')
+                folder = '원본 파일 생성' if sigma == 0 else f'sigma{sigma} 블러 파일 생성'
+                matches = [p for p in paths if p.startswith(folder + '/피쳐맵/' + key + '/') and Path(p).name.startswith(f'stage{stage}_')]
+                if len(matches) != 1:
+                    raise ValueError('참고 경로가 단계별 한 개가 아닙니다.')
+                relative = '블러 피쳐맵 저장 파일/' + matches[0]
+                destination = HERE / relative
+                if destination.exists():
+                    raise FileExistsError('색인에 없는 출력은 덮어쓰지 않습니다: ' + relative)
+                caption, selected, ranges = render(array, stage, sigma, label, destination)
+                with Image.open(destination) as image:
+                    width, height = image.size
+                batch_items.append({'id': f'{sigma}-{key}-{stage}', 'sigma': sigma, 'class_key': key,
+                    'class_label': label, 'stage': stage, 'relative_path': relative, 'sha256': digest(destination),
+                    'width': width, 'height': height, 'caption': caption, 'layer': LAYERS[stage], 'shape': list(array.shape),
+                    'panel_indices': selected, 'panel_count': 1 if stage == 0 else 10, 'panel_minmax': ranges,
+                    'checkpoint_sha256': model_hash, 'source_sha256': row['byte_sha256'], 'checkpoint_epoch': checkpoint['epoch']})
+        if len(batch_items) != 18:
+            raise ValueError('강도별 PNG 18개가 완성되지 않았습니다.')
+        index['items'].extend(batch_items)
+        index['completed_sigmas'].append(sigma)
+        index['pending_sigmas'] = [s for s in SIGMAS if s not in index['completed_sigmas']]
+        index['updated_at'] = now()
+        atomic_json(index_path, index)
+        print(json.dumps({'sigma': sigma, 'saved_png': 18, 'completed_sigmas': index['completed_sigmas']}, ensure_ascii=False), flush=True)
+        del model, checkpoint, stages
+    if not index_path.exists():
+        index['updated_at'] = now()
+        atomic_json(index_path, index)
+    return not index['pending_sigmas']
+
+def main():
+    global TRAIN, HERE, REFERENCE, RUN, torch, np, plt, FONT, Image, SplitResNet50, CTDataset
+    parser = argparse.ArgumentParser(description=__doc__)
+    mode = parser.add_mutually_exclusive_group(required=True)
+    mode.add_argument('--once', action='store_true')
+    mode.add_argument('--watch', action='store_true')
+    parser.add_argument('--experiment-root', type=Path, default=TRAIN)
+    parser.add_argument('--output-root', type=Path, default=HERE)
+    parser.add_argument('--reference-root', type=Path, default=REFERENCE)
+    parser.add_argument('--run-id', required=True)
+    args = parser.parse_args()
+    TRAIN = args.experiment_root.resolve()
+    HERE = args.output_root.resolve()
+    REFERENCE = args.reference_root.resolve()
+    RUN = args.run_id
+    if len(RUN) != 16 or any(c not in '0123456789abcdef' for c in RUN):
+        parser.error('검증한 5차 실행 ID 16자리가 필요합니다.')
+    if TRAIN != (PROJECT / '5차').resolve() or HERE != (PROJECT / '블러 강도별 대표 특징맵' / '5차').resolve():
+        parser.error('5차 학습과 별도 5차 출력 폴더를 명시해야 합니다.')
+    if not HERE.is_dir() or HERE == TRAIN or HERE == REFERENCE:
+        parser.error('출력은 기존의 별도 차수 폴더여야 합니다.')
+    try:
+        # 기존 환경만 사용하며 GPU·다운로드·학습 상태 변경을 하지 않습니다.
+        os.environ['CUDA_VISIBLE_DEVICES'] = ''
+        sys.path.insert(0, str(TRAIN))
+        import torch
+        torch.set_num_threads(2)
+        import numpy as np
+        import matplotlib
+        matplotlib.use('Agg')
+        import matplotlib.pyplot as plt
+        from matplotlib.font_manager import FontProperties
+        from PIL import Image
+        from src.model import SplitResNet50
+        from src.data import CTDataset
+        FONT = FontProperties(fname=str(TRAIN / 'web/fonts/NanumGothic-Bold.ttf'), weight='bold')
+        paths = prepare()
+        while True:
+            complete = run_once(paths)
+            if args.once or complete:
+                break
+            time.sleep(30)
+    except Exception:
+        failure = {'time_kst': now(), 'argv': sys.argv, 'cwd': os.getcwd(),
+                   'exit_code': 1, 'error': traceback.format_exc(), 'output_root': str(HERE)}
+        try:
+            with (HERE / '실패기록_비공개.jsonl').open('a', encoding='utf-8') as stream:
+                stream.write(json.dumps(failure, ensure_ascii=False) + '\n')
+        except Exception as secondary:
+            print(failure['error'], file=sys.stderr, flush=True)
+            print('특징맵 실패 기록의 추가 오류: ' + repr(secondary), file=sys.stderr, flush=True)
+        raise
+    return 0
+
+
+if __name__ == '__main__':
+    raise SystemExit(main())
````

## tools/recovery.py

이전 0 B / SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. 이후 24,427 B / SHA-256 `f54a3453c7d347be9593c3ea80de5f61defe20989bb016a86cf4f3f5d389c781`.

````diff
--- 이전/tools/recovery.py
+++ 이후/tools/recovery.py
@@ -0,0 +1,409 @@
+"""고정된 원본 SHA를 확인한 뒤 경로와 실행 식별자만 명시적으로 변환합니다."""
+
+from __future__ import annotations
+
+import argparse
+import copy
+import gc
+import hashlib
+import json
+import os
+from pathlib import Path, PurePosixPath
+import shutil
+import sys
+
+ROOT = Path(__file__).resolve().parents[1]
+if str(ROOT) not in sys.path:
+    sys.path.insert(0, str(ROOT))
+
+import torch
+
+from src.data import prepare_dataset, validate_reference_manifest
+from src.state import atomic_json, now_kst
+from src.training import TrainingControl, _run_identity
+
+REFERENCE = "work/recovery/이관_기준목록_비공개.json"
+LINEAGE = "work/recovery/복구_계보_비공개.json"
+SCIENTIFIC = ("run_training.py", "src/__init__.py", "src/data.py", "src/model.py",
+              "src/state.py", "src/training.py")
+
+
+def file_digest(path):
+    digest = hashlib.sha256()
+    with Path(path).open("rb") as stream:
+        for block in iter(lambda: stream.read(1024 * 1024), b""):
+            digest.update(block)
+    return digest.hexdigest()
+
+
+def records_digest(rows):
+    return hashlib.sha256(json.dumps(rows, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()
+
+
+def json_bytes(payload):
+    return (json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")
+
+
+def safe_path(root, relative):
+    root = Path(root).resolve()
+    value = PurePosixPath(str(relative).replace("\\", "/"))
+    if value.is_absolute() or any(part in {"..", "."} or ":" in part for part in value.parts):
+        raise ValueError("허용한 폴더 밖의 경로입니다.")
+    path = root.joinpath(*value.parts)
+    if not path.resolve().is_relative_to(root):
+        raise ValueError("폴더 경계를 벗어나는 파일입니다.")
+    for item in [path, *path.parents]:
+        if item == root:
+            break
+        if item.is_symlink() or (hasattr(item, "is_junction") and item.is_junction()):
+            raise ValueError("복구 파일에서 폴더 연결을 따라가지 않습니다.")
+    return path
+
+
+def read_baseline(path, expected_sha256):
+    if file_digest(path) != expected_sha256:
+        raise ValueError("복구 기준 파일의 외부 고정 SHA와 다릅니다.")
+    return json.loads(Path(path).read_text(encoding="utf-8"))
+
+
+def verify_files(root, files):
+    for relative, expected in files.items():
+        if file_digest(safe_path(root, relative)) != expected:
+            raise ValueError(f"원본 SHA가 다릅니다: {relative}")
+
+
+def relocate_manifest(source, old_prefix, new_prefix):
+    if source.get("manifest_sha256") != records_digest(source.get("records")):
+        raise ValueError("원본 목록의 파생 SHA가 다릅니다.")
+    target = copy.deepcopy(source)
+    old_prefix, new_prefix = old_prefix.replace("\\", "/").rstrip("/"), new_prefix.replace("\\", "/").rstrip("/")
+    for rows in [target["records"], *target["splits"].values()]:
+        for row in rows:
+            relative = row["relative_path"]
+            pieces = PurePosixPath(relative).parts
+            if PurePosixPath(relative).is_absolute() or any(p in {"..", "."} or ":" in p or "\\" in p for p in pieces):
+                raise ValueError("원본 목록의 상대 경로가 유효하지 않습니다.")
+            expected = old_prefix + "/" + relative
+            if row["path"].replace("\\", "/") != expected:
+                raise ValueError("명시한 원본 접두와 상대 경로가 일치하지 않습니다.")
+            # 원본 경로의 구분자 표기도 보존하고 드라이브 접두만 바꿉니다.
+            separator = "\\" if "\\" in row["path"] else "/"
+            row["path"] = (new_prefix + "/" + relative).replace("/", separator)
+    target["manifest_sha256"] = records_digest(target["records"])
+    return target
+
+
+def relocated_config(source, new_dataset, target_manifest):
+    result = copy.deepcopy(source)
+    result.update(dataset_root=new_dataset, expected_reference_manifest=REFERENCE,
+                  expected_reference_manifest_sha256=hashlib.sha256(json_bytes(target_manifest)).hexdigest(),
+                  expected_reference_records_sha256=target_manifest["manifest_sha256"])
+    return result
+
+
+def assert_config_compatible(source, target, new_dataset, target_manifest):
+    if target != relocated_config(source, new_dataset, target_manifest):
+        raise ValueError("자료·기준 목록 경로와 파생 SHA 외의 설정이 변경됐습니다.")
+
+
+def assert_state_equal(before, after):
+    if isinstance(before, torch.Tensor):
+        if not isinstance(after, torch.Tensor) or before.dtype != after.dtype or before.shape != after.shape or not torch.equal(before.cpu(), after.cpu()):
+            raise ValueError("복구 변환에서 tensor 값·형식이 변경됐습니다.")
+    elif type(before) is not type(after):
+        raise ValueError("복구 변환에서 상태의 자료형이 변경됐습니다.")
+    elif isinstance(before, dict):
+        if before.keys() != after.keys():
+            raise ValueError("복구 변환에서 상태 키가 변경됐습니다.")
+        for key in before:
+            assert_state_equal(before[key], after[key])
+    elif isinstance(before, (list, tuple)):
+        if len(before) != len(after):
+            raise ValueError("복구 변환에서 상태 길이가 변경됐습니다.")
+        for left, right in zip(before, after):
+            assert_state_equal(left, right)
+    elif before != after:
+        raise ValueError("허용한 식별자 이외의 상태가 변경됐습니다.")
+
+
+def rebind_checkpoint(source, old_run_id, new_run_id, sigma, prefix_sha256=None):
+    if source.get("run_id") != old_run_id or source.get("sigma") != sigma:
+        raise ValueError("가져올 체크포인트 실행·강도가 다릅니다.")
+    # tensor는 수정하지 않고 새 mapping만 만듭니다. 저장 후 재로딩으로 내용도 대조합니다.
+    target = dict(source, run_id=new_run_id)
+    if source.get("shadow_prefix_sha256") is not None:
+        if not prefix_sha256:
+            raise ValueError("변환한 prefix SHA가 필요합니다.")
+        target["shadow_prefix_sha256"] = prefix_sha256
+    return target
+
+
+def convert_checkpoint(source_path, target_path, old_run_id, new_run_id, sigma, prefix_sha256=None):
+    source = torch.load(source_path, map_location="cpu", weights_only=False)
+    target = rebind_checkpoint(source, old_run_id, new_run_id, sigma, prefix_sha256)
+    Path(target_path).parent.mkdir(parents=True, exist_ok=True)
+    torch.save(target, target_path)
+    restored = torch.load(target_path, map_location="cpu", weights_only=False)
+    assert_state_equal(target, restored)
+    result = {"source_sha256": file_digest(source_path), "new_sha256": file_digest(target_path),
+              "epoch": source["epoch"], "tensor_and_state_equal": True}
+    del source, target, restored
+    gc.collect()
+    return result
+
+
+def validate_metric(metric):
+    for key in ("validation", "test"):
+        if key not in metric:
+            continue
+        value = metric[key]
+        matrix, count = value["confusion_matrix"], value["n_images"]
+        if (len(matrix) != 2 or any(len(row) != 2 for row in matrix)
+                or any(type(n) is not int or n < 0 for row in matrix for n in row)
+                or type(count) is not int or count <= 0 or sum(map(sum, matrix)) != count
+                or abs(value["accuracy"] - (matrix[0][0] + matrix[1][1]) / count) > 1e-12):
+            raise ValueError("원본 결과의 혼동행렬·분모·정확도가 모순됩니다.")
+
+
+def rebind_metric(source, old_run_id, new_run_id, sigma, prefix_sha256):
+    if source.get("run_id") != old_run_id or source.get("sigma") != sigma:
+        raise ValueError("완료 결과의 실행·강도가 다릅니다.")
+    validate_metric(source)
+    target = copy.deepcopy(source)
+    target["run_id"] = new_run_id
+    comparison = target.get("early_stopping_comparison", {})
+    if comparison.get("available"):
+        if not prefix_sha256:
+            raise ValueError("완료 비교의 prefix SHA가 필요합니다.")
+        validate_metric(comparison)
+        comparison["checkpoint_sha256"] = prefix_sha256
+    return target
+
+
+def validate_resume(last, config, expected_epoch):
+    history = last["history"]
+    epoch = last["epoch"]
+    if (epoch != expected_epoch or len(history) != epoch or [r["epoch"] for r in history] != list(range(1, epoch + 1))):
+        raise ValueError("완료 epoch와 학습 이력이 일치하지 않습니다.")
+    control = TrainingControl(config["min_delta"], config["early_stopping_patience"],
+                              enabled=config.get("early_stopping_enabled", True))
+    control.load_state_dict(last["training_control"])
+    expected_steps = epoch * ((2 * config["samples_per_class"] + config["batch_size"] - 1) // config["batch_size"])
+    if control.optimizer_steps != expected_steps or not 1 <= control.best_raw_epoch <= epoch:
+        raise ValueError("완료 epoch의 업데이트 수·최적 epoch가 다릅니다.")
+    if not control.enabled and control.shadow_stop_epoch and not 1 <= control.shadow_best_raw_epoch <= control.shadow_stop_epoch <= epoch:
+        raise ValueError("고정한 가상 종료 상태가 유효하지 않습니다.")
+    return epoch + 1
+
+
+def validate_prefix_state(last, prefix_path, run_id, sigma, expected_sha256=None):
+    """아직 생성 전인 정상 상태와 생성된 뒤 반드시 보존할 prefix를 구분합니다."""
+    prefix_path = Path(prefix_path)
+    control = last["training_control"]
+    stop_epoch = control.get("shadow_stop_epoch", 0)
+    best_epoch = control.get("shadow_best_raw_epoch", 0)
+    stored_hash = last.get("shadow_prefix_sha256")
+    if stop_epoch == 0:
+        if best_epoch != 0 or stored_hash is not None or prefix_path.exists() or expected_sha256 is not None:
+            raise ValueError("관찰용 종료 전 상태에 prefix 파일·해시·최적 시점이 남아 있습니다.")
+        return None
+    if (type(stop_epoch) is not int or type(best_epoch) is not int
+            or not 1 <= best_epoch <= stop_epoch <= last["epoch"]
+            or not isinstance(stored_hash, str) or len(stored_hash) != 64
+            or any(c not in "0123456789abcdef" for c in stored_hash)
+            or not prefix_path.is_file()):
+        raise ValueError("관찰용 종료 상태에 유효한 prefix 파일·해시·시점이 필요합니다.")
+    if file_digest(prefix_path) != stored_hash or (expected_sha256 is not None and stored_hash != expected_sha256):
+        raise ValueError("고정한 prefix SHA와 마지막 완료 상태가 다릅니다.")
+    frozen = torch.load(prefix_path, map_location="cpu", weights_only=False)
+    if frozen.get("run_id") != run_id or frozen.get("sigma") != sigma or frozen.get("epoch") != best_epoch:
+        raise ValueError("고정한 prefix의 실행·강도·최적 시점이 다릅니다.")
+    del frozen
+    return stored_hash
+
+
+def build_target_config(source_root, target_root, baseline):
+    reference = Path(source_root) / baseline["reference_relative_path"]
+    if file_digest(reference) != baseline["reference_file_sha256"]:
+        raise ValueError("보존한 원본 기준 목록 SHA가 다릅니다.")
+    source = json.loads(reference.read_text(encoding="utf-8"))
+    if records_digest(source["records"]) != baseline["reference_records_sha256"]:
+        raise ValueError("보존한 원본 목록 SHA가 다릅니다.")
+    actual = json.loads((Path(source_root) / "work/results/dataset_manifest_private.json").read_text(encoding="utf-8"))
+    if source["records"] != actual["records"] or source["splits"] != actual["splits"]:
+        raise ValueError("원본 실행과 기준 목록의 원본·정확한 분할이 다릅니다.")
+    target = relocate_manifest(source, baseline["source_dataset_prefix"], baseline["target_dataset_prefix"])
+    config = relocated_config(baseline["source_config"], baseline["target_dataset_prefix"], target)
+    return config, target
+
+
+def import_recovery(target_root, source_root, baseline_path, baseline_sha256):
+    root, source_root = Path(target_root).resolve(), Path(source_root).resolve()
+    baseline = read_baseline(baseline_path, baseline_sha256)
+    verify_files(source_root, baseline["source_files"])
+    source_manifest = json.loads((source_root / "work/results/dataset_manifest_private.json").read_text(encoding="utf-8"))
+    old_run, source_settings = _run_identity(source_root, baseline["source_config"], source_manifest["manifest_sha256"])
+    source_metadata = json.loads((source_root / f"work/results/run_{baseline['source_run_id']}/run_metadata.json").read_text(encoding="utf-8"))
+    if (old_run != baseline["source_run_id"] or source_metadata.get("run_id") != old_run
+            or any(source_metadata.get(key) != value for key, value in source_settings.items())):
+        raise ValueError("원본 실행 metadata·소스·설정·자료의 식별자가 다릅니다.")
+    for name in SCIENTIFIC:
+        if file_digest(root / name) != baseline["source_files"][name]:
+            raise ValueError(f"학습 소스가 원본과 다릅니다: {name}")
+    config, manifest = build_target_config(source_root, root, baseline)
+    assert_config_compatible(baseline["source_config"], json.loads((root / "config.json").read_text(encoding="utf-8")),
+                             baseline["target_dataset_prefix"], manifest)
+    for row in manifest["records"]:
+        image = safe_path(Path(config["dataset_root"]), row["relative_path"])
+        if file_digest(image) != row["byte_sha256"]:
+            raise ValueError("이동한 원영상의 byte SHA가 다릅니다.")
+    # 기준 파일을 먼저 고정하고 기존 자료 준비 함수의 전체 재계산·분할 핀 검사를 통과합니다.
+    reference = root / REFERENCE
+    if reference.exists() and reference.read_bytes() != json_bytes(manifest):
+        raise ValueError("기존 이관 기준 목록을 다른 내용으로 덮어쓰지 않습니다.")
+    reference.parent.mkdir(parents=True, exist_ok=True)
+    if not reference.exists():
+        reference.write_bytes(json_bytes(manifest))
+    validate_reference_manifest(config, root, manifest)
+    prepared = prepare_dataset(config, root)
+    if prepared["records"] != manifest["records"] or prepared["splits"] != manifest["splits"]:
+        raise ValueError("실제 대상 영상 재계산이 이관 기준과 다릅니다.")
+    new_run, settings = _run_identity(root, config, prepared["manifest_sha256"])
+    old_run = baseline["source_run_id"]
+    if new_run == old_run:
+        raise ValueError("경로가 변경된 복구 실행은 새 식별자가 필요합니다.")
+    result_dir, checkpoint_dir = root / f"work/results/run_{new_run}", root / f"work/checkpoints/run_{new_run}"
+    if result_dir.exists() or checkpoint_dir.exists() or (root / LINEAGE).exists():
+        raise FileExistsError("가져올 실행 폴더가 이미 있습니다. 덮어쓰지 않습니다.")
+    from tools.safe_training import require_free_space
+    checkpoint_sizes = [(source_root / name).stat().st_size for name in baseline["source_files"] if name.endswith(".pt")]
+    require_free_space(root, sum(checkpoint_sizes) + max(checkpoint_sizes, default=0) + 64 * 1024 ** 2)
+    stage = root / f"work/recovery/가져오기_진행_{new_run}"
+    stage.mkdir(parents=True, exist_ok=False)
+    output_result, output_ckpt = stage / "results", stage / "checkpoints"
+    output_result.mkdir(); output_ckpt.mkdir()
+    lineage = {"schema_version": 1, "time": now_kst(), "source_run_id": old_run, "run_id": new_run,
+               "baseline_sha256": baseline_sha256, "baseline_path": str(Path(baseline_path).resolve()),
+               "source_root": str(source_root), "source_files": baseline["source_files"], "settings": settings,
+               "manifest_path_changes_only": True, "original_images_byte_verified": len(manifest["records"]),
+               "scientific_sources_unchanged": list(SCIENTIFIC), "converted_checkpoints": {}, "imported_files": {},
+               "transfer": baseline["transfer"], "completed_results_reevaluated": False,
+               "resume_note": "마지막 완료 epoch 다음 회차부터 다시 수행하며 중단 회차의 배치는 재사용하지 않습니다."}
+    source_results = source_root / f"work/results/run_{old_run}"
+    source_checkpoints = source_root / f"work/checkpoints/run_{old_run}"
+    for sigma_text, spec in baseline["transfer"].items():
+        sigma = int(sigma_text)
+        prefix_name = f"sigma_{sigma}_shadow_prefix_best.pt"
+        source_last = torch.load(source_checkpoints / f"sigma_{sigma}_last.pt", map_location="cpu", weights_only=False)
+        validate_resume(source_last, config, spec["epoch"])
+        source_prefix_hash = validate_prefix_state(source_last, source_checkpoints / prefix_name, old_run, sigma)
+        del source_last
+        prefix_hash = None
+        if source_prefix_hash is not None:
+            prefix = convert_checkpoint(source_checkpoints / prefix_name, output_ckpt / prefix_name, old_run, new_run, sigma)
+            prefix_hash = prefix["new_sha256"]
+            lineage["converted_checkpoints"][prefix_name] = prefix
+        for kind in ("best", "last"):
+            name = f"sigma_{sigma}_{kind}.pt"
+            lineage["converted_checkpoints"][name] = convert_checkpoint(source_checkpoints / name, output_ckpt / name,
+                                                                         old_run, new_run, sigma, prefix_hash)
+        last = torch.load(output_ckpt / f"sigma_{sigma}_last.pt", map_location="cpu", weights_only=False)
+        next_epoch = validate_resume(last, config, spec["epoch"])
+        history = json.loads((source_results / f"sigma_{sigma}_history.json").read_text(encoding="utf-8"))
+        assert_state_equal(last["history"], history)
+        best = torch.load(output_ckpt / f"sigma_{sigma}_best.pt", map_location="cpu", weights_only=False)
+        if best["epoch"] != last["training_control"]["best_raw_epoch"]:
+            raise ValueError("최적 모델 epoch가 마지막 상태와 다릅니다.")
+        validate_prefix_state(last, output_ckpt / prefix_name, new_run, sigma, prefix_hash)
+        shutil.copyfile(source_results / f"sigma_{sigma}_history.json", output_result / f"sigma_{sigma}_history.json")
+        if spec["completed"]:
+            metric_path = source_results / f"sigma_{sigma}_metrics.json"
+            metric = json.loads(metric_path.read_text(encoding="utf-8"))
+            if metric.get("epochs_ran") != config["epochs"] or metric.get("optimizer_steps") != last["training_control"]["optimizer_steps"]:
+                raise ValueError("완료 조건의 회차·업데이트 수가 마지막 상태와 다릅니다.")
+            rebound = rebind_metric(metric, old_run, new_run, sigma, prefix_hash)
+            atomic_json(output_result / metric_path.name, rebound)
+            for prediction in source_results.glob(f"sigma_{sigma}_*predictions_private.csv"):
+                shutil.copyfile(prediction, output_result / prediction.name)
+        elif (source_results / f"sigma_{sigma}_metrics.json").exists() or next_epoch > config["epochs"]:
+            raise ValueError("중단 조건의 완료/재개 구분이 다릅니다.")
+        lineage["transfer"][sigma_text] = {**spec, "next_epoch": next_epoch,
+                                          "shadow_prefix_at_import": prefix_hash is not None}
+        del last, best
+        gc.collect()
+    source_meta = json.loads((source_results / "run_metadata.json").read_text(encoding="utf-8"))
+    metadata = {**source_meta, **settings, "run_id": new_run, "started_at": now_kst(),
+                "recovery": {"source_run_id": old_run, "source_started_at": source_meta["started_at"],
+                             "source_metadata_sha256": baseline["source_files"][f"work/results/run_{old_run}/run_metadata.json"],
+                             "lineage": LINEAGE, "conversion": "경로·실행 식별자와 연결 SHA만 변환한 상태 이관"}}
+    atomic_json(output_result / "run_metadata.json", metadata)
+    for kind, folder in (("results", output_result), ("checkpoints", output_ckpt)):
+        for path in folder.iterdir():
+            lineage["imported_files"][f"work/{kind}/run_{new_run}/{path.name}"] = file_digest(path)
+    result_dir.parent.mkdir(parents=True, exist_ok=True); checkpoint_dir.parent.mkdir(parents=True, exist_ok=True)
+    os.replace(output_ckpt, checkpoint_dir); os.replace(output_result, result_dir)
+    atomic_json(root / LINEAGE, lineage)
+    verify_import(root)
+    return lineage
+
+
+def verify_import(root, initial=True, expected_baseline_sha256=None):
+    root = Path(root)
+    lineage = json.loads((root / LINEAGE).read_text(encoding="utf-8"))
+    if expected_baseline_sha256 is not None and lineage["baseline_sha256"] != expected_baseline_sha256:
+        raise ValueError("복구 계보의 기준 SHA가 명시한 외부 승인값과 다릅니다.")
+    baseline = read_baseline(lineage["baseline_path"], lineage["baseline_sha256"])
+    for name in SCIENTIFIC:
+        if file_digest(root / name) != baseline["source_files"][name]:
+            raise ValueError("복구 후 학습 소스가 변경됐습니다.")
+    config = json.loads((root / "config.json").read_text(encoding="utf-8"))
+    manifest = json.loads((root / REFERENCE).read_text(encoding="utf-8"))
+    assert_config_compatible(baseline["source_config"], config, baseline["target_dataset_prefix"], manifest)
+    validate_reference_manifest(config, root, manifest)
+    run_id, settings = _run_identity(root, config, manifest["manifest_sha256"])
+    if run_id != lineage["run_id"] or settings != lineage["settings"]:
+        raise ValueError("복구 실행 식별자·설정이 계보와 다릅니다.")
+    if initial:
+        verify_files(root, lineage["imported_files"])
+    for sigma_text, spec in lineage["transfer"].items():
+        folder = root / f"work/checkpoints/run_{run_id}"
+        prefix = folder / f"sigma_{sigma_text}_shadow_prefix_best.pt"
+        imported_prefix = lineage["converted_checkpoints"].get(prefix.name)
+        expected = imported_prefix["new_sha256"] if imported_prefix else None
+        last = torch.load(folder / f"sigma_{sigma_text}_last.pt", map_location="cpu", weights_only=False)
+        if last["run_id"] != run_id or last["sigma"] != int(sigma_text):
+            raise ValueError("재개 상태의 실행·강도가 다릅니다.")
+        validate_resume(last, config, spec["epoch"] if initial else last["epoch"])
+        # 가져올 때 미생성이었던 prefix는 기존 학습 루프가 나중에 고정할 수 있습니다.
+        # 기존에 가져온 prefix는 새 last가 생겨도 처음 변환한 SHA를 계속 고정합니다.
+        validate_prefix_state(last, prefix, run_id, int(sigma_text), expected)
+        del last
+    return {"run_id": run_id, "verified": True, "initial_import": initial, "transfer": lineage["transfer"]}
+
+
+def main():
+    parser = argparse.ArgumentParser(description="보존한 체크포인트의 명시적 경로 복구")
+    parser.add_argument("command", choices=("configure", "import", "verify"))
+    parser.add_argument("--source-root", type=Path, default=ROOT.parent / "4차")
+    parser.add_argument("--baseline", type=Path, default=ROOT / "work/recovery/원본_복구기준_비공개.json")
+    parser.add_argument("--baseline-sha256", required=True)
+    args = parser.parse_args()
+    if args.command == "verify":
+        # verify도 외부 기준을 다시 확인합니다.
+        read_baseline(args.baseline, args.baseline_sha256)
+        result = verify_import(ROOT, expected_baseline_sha256=args.baseline_sha256)
+    elif args.command == "configure":
+        baseline = read_baseline(args.baseline, args.baseline_sha256)
+        verify_files(args.source_root, baseline["source_files"])
+        config, _manifest = build_target_config(args.source_root, ROOT, baseline)
+        atomic_json(ROOT / "config.json", config)
+        result = {"configured": True, "scientific_settings_unchanged": True}
+    else:
+        result = import_recovery(ROOT, args.source_root, args.baseline, args.baseline_sha256)
+        result = {key: result[key] for key in ("source_run_id", "run_id", "original_images_byte_verified", "transfer")}
+    print(json.dumps(result, ensure_ascii=False, indent=2))
+    return 0
+
+
+if __name__ == "__main__":
+    raise SystemExit(main())
````

## tools/safe_training.py

이전 0 B / SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. 이후 16,693 B / SHA-256 `39c26c754c00be4edb4a66375572c8623c413903dd511a4053382022ed1bbde1`.

````diff
--- 이전/tools/safe_training.py
+++ 이후/tools/safe_training.py
@@ -0,0 +1,314 @@
+"""동일 학습 코드 앞에 공간·중복 확인과 독립 오류 보존 경계만 둡니다."""
+
+from __future__ import annotations
+
+import argparse
+import ctypes
+from datetime import datetime, timezone, timedelta
+import json
+import ntpath
+import os
+from pathlib import Path
+import shutil
+import subprocess
+import sys
+import threading
+import traceback
+
+ROOT = Path(__file__).resolve().parents[1]
+MIN_TRAIN_FREE = 8 * 1024 ** 3
+MIN_LOG_FREE = 256 * 1024 ** 2
+
+
+def exception_payload(error):
+    return {"time_kst": datetime.now(timezone(timedelta(hours=9))).isoformat(),
+            "error_type": type(error).__name__, "error": str(error),
+            "errno": getattr(error, "errno", None), "winerror": getattr(error, "winerror", None),
+            "traceback": "".join(traceback.format_exception(type(error), error, error.__traceback__)),
+            "argv": sys.argv, "cwd": os.getcwd(), "pid": os.getpid()}
+
+
+def write_independent_logs(folders, filename, payload):
+    """한 볼륨의 오류가 다른 볼륨의 원오류 기록을 막지 않게 각각 저장합니다."""
+    failures, good = [], []
+    for folder in map(Path, folders):
+        try:
+            folder.mkdir(parents=True, exist_ok=True)
+            path = folder / filename
+            with path.open("w", encoding="utf-8", newline="\n") as stream:
+                json.dump({**payload, "secondary_log_errors": failures}, stream, ensure_ascii=False, indent=2, allow_nan=False)
+                stream.write("\n"); stream.flush(); os.fsync(stream.fileno())
+            good.append(path)
+        except Exception as error:
+            failures.append({"folder": str(folder), **exception_payload(error)})
+    # 성공한 볼륨에도 먼저/나중에 생긴 secondary 오류를 함께 남깁니다.
+    if failures:
+        for path in good:
+            try:
+                with path.open("w", encoding="utf-8", newline="\n") as stream:
+                    json.dump({**payload, "secondary_log_errors": failures}, stream, ensure_ascii=False, indent=2, allow_nan=False)
+                    stream.write("\n"); stream.flush(); os.fsync(stream.fileno())
+            except Exception as error:
+                print(json.dumps({"secondary_log_error": exception_payload(error)}, ensure_ascii=False), file=sys.stderr, flush=True)
+    return failures
+
+
+def require_free_space(path, minimum):
+    probe = Path(path).resolve()
+    while not probe.exists():
+        probe = probe.parent
+    free = shutil.disk_usage(probe).free
+    if free < minimum:
+        raise OSError(28, f"저장 여유 공간이 기준보다 작습니다: free={free}, required={minimum}, volume={probe.anchor}")
+    return free
+
+
+def reject_duplicates(processes):
+    if processes:
+        raise RuntimeError("같은 프로젝트의 학습 프로세스가 있어 중복 실행하지 않습니다: " +
+                           ", ".join(str(item["pid"]) for item in processes))
+
+
+def windows_process(pid):
+    """숫자로 확인한 단일 PID의 부모와 실행파일만 읽습니다."""
+    if type(pid) is not int or pid <= 0:
+        raise ValueError("유효한 프로세스 PID가 필요합니다.")
+    command = ("$ErrorActionPreference='Stop'; [Console]::OutputEncoding=[System.Text.UTF8Encoding]::new($false); "
+               f"Get-CimInstance Win32_Process -Filter 'ProcessId = {pid}' | "
+               "Select-Object ProcessId,ParentProcessId,ExecutablePath | ConvertTo-Json -Compress")
+    result = subprocess.run(["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", command],
+                            capture_output=True, text=True, encoding="utf-8", errors="strict", timeout=20,
+                            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
+    if result.returncode:
+        raise RuntimeError("worker 감독 연결 조회 실패: " + result.stderr)
+    return json.loads(result.stdout) if result.stdout.strip() else None
+
+
+def worker_parent_authorized(supervisor_pid):
+    """직접 감독 또는 그 감독이 만든 동일 venv launcher 한 단계만 허용합니다."""
+    if (not isinstance(supervisor_pid, str) or not supervisor_pid.isascii()
+            or not supervisor_pid.isdecimal() or int(supervisor_pid) <= 0):
+        return False
+    supervisor_pid = int(supervisor_pid)
+    parent_pid = os.getppid()
+    if parent_pid == supervisor_pid:
+        return True
+    if os.name != "nt":
+        return False
+    launcher = windows_process(parent_pid)
+    if (not isinstance(launcher, dict) or launcher.get("ProcessId") != parent_pid
+            or launcher.get("ParentProcessId") != supervisor_pid
+            or not isinstance(launcher.get("ExecutablePath"), str)):
+        return False
+    normalize = lambda path: os.path.normcase(os.path.abspath(path))
+    return normalize(launcher["ExecutablePath"]) == normalize(sys.executable)
+
+
+def windows_arguments(command_line):
+    """Windows의 실제 따옴표 규칙으로 명령행을 분리하며 작업 폴더는 추측하지 않습니다."""
+    from ctypes import wintypes
+    count = ctypes.c_int()
+    parse = ctypes.WinDLL("shell32", use_last_error=True).CommandLineToArgvW
+    parse.argtypes = [wintypes.LPCWSTR, ctypes.POINTER(ctypes.c_int)]
+    parse.restype = ctypes.POINTER(wintypes.LPWSTR)
+    arguments = parse(command_line, ctypes.byref(count))
+    if not arguments:
+        raise ctypes.WinError(ctypes.get_last_error())
+    release = ctypes.WinDLL("kernel32", use_last_error=True).LocalFree
+    release.argtypes = [ctypes.c_void_p]
+    release.restype = ctypes.c_void_p
+    try:
+        return [arguments[index] for index in range(count.value)]
+    finally:
+        release(ctypes.cast(arguments, ctypes.c_void_p))
+
+
+def training_processes(project_root):
+    if os.name != "nt":
+        raise RuntimeError("이 복구 실행의 중복 확인은 Windows CIM에서만 지원합니다.")
+    command = "$ErrorActionPreference='Stop'; [Console]::OutputEncoding=[System.Text.UTF8Encoding]::new($false); Get-CimInstance Win32_Process | Where-Object { $_.Name -match '^python(w)?(.exe)?$' } | Select-Object ProcessId,ParentProcessId,ExecutablePath,CommandLine | ConvertTo-Json -Compress"
+    result = subprocess.run(["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", command],
+                            capture_output=True, text=True, encoding="utf-8", errors="strict", timeout=20,
+                            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
+    if result.returncode:
+        raise RuntimeError("학습 중복 조회 실패: " + result.stderr)
+    rows = json.loads(result.stdout) if result.stdout.strip() else []
+    if isinstance(rows, dict):
+        rows = [rows]
+    own_pid, parent_pid = os.getpid(), os.getppid()
+    own = [row for row in rows if row.get("ProcessId") == own_pid]
+    if len(own) != 1 or own[0].get("ParentProcessId") != parent_pid:
+        raise RuntimeError("CIM에서 자기 프로세스와 실제 부모 관계를 확인하지 못했습니다.")
+    suffix = str(Path(project_root)).replace("\\", "/").lower()
+    if len(suffix) > 2 and suffix[1] == ":":
+        suffix = suffix[2:]
+    found = []
+    for row in rows:
+        command_line = row.get("CommandLine") or ""
+        if row["ProcessId"] == own_pid or not command_line:
+            continue
+        executable = row.get("ExecutablePath")
+        # 실제 부모 관계가 확인된 동일 venv launcher만 자기 실행 체인으로 제외합니다.
+        if (row["ProcessId"] == parent_pid and isinstance(executable, str)
+                and os.path.normcase(os.path.abspath(executable)) == os.path.normcase(os.path.abspath(sys.executable))):
+            continue
+        arguments = windows_arguments(command_line)
+        scripts = [argument for argument in arguments[1:]
+                   if ntpath.basename(argument).lower() in {"run_training.py", "복구_학습.py"}]
+        module_call = any(value == "-m" and index + 1 < len(arguments)
+                          and arguments[index + 1] in {"run_training", "복구_학습", "tools.safe_training"}
+                          for index, value in enumerate(arguments))
+        ambiguous = module_call or any(not ntpath.isabs(script) for script in scripts)
+        same_project = any(ntpath.splitdrive(script)[1].replace("\\", "/").lower().startswith(suffix.rstrip("/") + "/")
+                           for script in scripts if ntpath.isabs(script))
+        if ambiguous or same_project:
+            found.append({"pid": row["ProcessId"], "command": command_line,
+                          "reason": "상대 호출의 작업 폴더를 확인할 수 없습니다." if ambiguous else "같은 프로젝트의 학습입니다."})
+    return found
+
+
+def log_folders(root):
+    local = Path(os.environ.get("LOCALAPPDATA", str(Path.home() / "AppData/Local")))
+    return [Path(root) / "work/recovery_logs", local / "폐CT_학습복구" / "5차"]
+
+
+def worker(root, device, folders):
+    """기존 run_training.py의 오류 처리 전에 원오류를 먼저 잡는 별도 진입점입니다."""
+    os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")
+    os.environ.setdefault("TORCH_HOME", str(Path(root) / "work/torch-cache"))
+    from src.state import StatusWriter, atomic_json
+    from src.training import run_training
+    state = None
+    try:
+        config = json.loads((Path(root) / "config.json").read_text(encoding="utf-8"))
+        state = StatusWriter(root, config)
+        state.update()
+        run_training(config, root, state, device)
+        return 0
+    except BaseException as error:
+        # 원오류를 상태 갱신·추가 오류 기록보다 먼저 고정합니다.
+        details = exception_payload(error)
+        details.update(sigma=state.data.get("sigma") if state else None,
+                       epoch=state.data.get("epoch") if state else None,
+                       attempted_batch=state.data.get("attempted_batch") if state else None)
+        name = "원오류_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f") + ".json"
+        failures = write_independent_logs(folders, name, details)
+        secondary = []
+        try:
+            atomic_json(Path(root) / "work/runtime/last_error.json", details)
+        except Exception as followup:
+            secondary.append(exception_payload(followup))
+        if state:
+            try:
+                interrupted = isinstance(error, KeyboardInterrupt)
+                for entry in state.data["sigma_queue"]:
+                    if entry["status"] == "running":
+                        entry["status"] = "failed"
+                state.update(stage="interrupted" if interrupted else "error", status="interrupted" if interrupted else "failed",
+                             pid=None, error=details, message=f"학습 중단: {type(error).__name__}: {error}")
+                state.event("복구 실행 중단", details)
+            except Exception as followup:
+                secondary.append(exception_payload(followup))
+        if failures or secondary:
+            write_independent_logs(folders, name, {**details, "secondary_status_errors": secondary,
+                                                   "initial_log_errors": failures})
+        print(details["traceback"], file=sys.stderr, flush=True)
+        return 130 if isinstance(error, KeyboardInterrupt) else 1
+
+
+def supervise(root, device, baseline_sha256):
+    root = Path(root).resolve()
+    folders = log_folders(root)
+    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
+    lock = root / "work/runtime/recovery.lock"
+    child = None
+    locked = False
+    try:
+        storage = {"training_free": require_free_space(root, MIN_TRAIN_FREE),
+                   "independent_log_free": require_free_space(folders[1], MIN_LOG_FREE)}
+        if root.anchor.lower() == folders[1].anchor.lower():
+            raise ValueError("독립 오류 로그는 학습과 다른 볼륨이어야 합니다.")
+        reject_duplicates(training_processes(root.parent))
+        from tools.recovery import verify_import
+        recovery = verify_import(root, initial=False, expected_baseline_sha256=baseline_sha256)
+        lock.parent.mkdir(parents=True, exist_ok=True)
+        descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
+        locked = True
+        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
+            json.dump({"pid": os.getpid(), "time": stamp, **storage, **recovery}, stream, ensure_ascii=False)
+        argv = [sys.executable, "-B", "-X", "utf8", "-u", str(root / "복구_학습.py"), "--worker", "--device", device]
+        errors = write_independent_logs(folders, f"실행_{stamp}.json", {"argv": argv, "cwd": str(root), **storage, **recovery})
+        if errors:
+            raise OSError("학습 시작 전 두 볼륨의 독립 로그를 모두 만들지 못했습니다.")
+        environment = dict(os.environ, CT_RECOVERY_SUPERVISOR_PID=str(os.getpid()))
+        child = subprocess.Popen(argv, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=environment)
+        log_errors = []
+
+        def pump(pipe, kind):
+            streams = []
+            for folder in folders:
+                try:
+                    folder.mkdir(parents=True, exist_ok=True)
+                    streams.append((folder, (folder / f"학습_{stamp}.{kind}.log").open("xb")))
+                except Exception as error:
+                    log_errors.append(exception_payload(error))
+            try:
+                for block in iter(lambda: pipe.read1(4096), b""):
+                    for folder, stream in list(streams):
+                        try:
+                            stream.write(block); stream.flush()
+                        except Exception as error:
+                            log_errors.append({"folder": str(folder), **exception_payload(error)})
+                            streams.remove((folder, stream)); stream.close()
+                    target = sys.stderr if kind == "stderr" else sys.stdout
+                    try:
+                        target.buffer.write(block); target.buffer.flush()
+                    except (OSError, AttributeError):
+                        pass
+            finally:
+                pipe.close()
+                for _folder, stream in streams:
+                    stream.close()
+
+        pumps = [threading.Thread(target=pump, args=(child.stdout, "stdout")),
+                 threading.Thread(target=pump, args=(child.stderr, "stderr"))]
+        for thread in pumps:
+            thread.start()
+        code = child.wait()
+        for thread in pumps:
+            thread.join()
+        write_independent_logs(folders, f"종료_{stamp}.json", {"exit_code": code, "child_pid": child.pid,
+                                                           "time_kst": datetime.now().astimezone().isoformat(), "secondary_stream_errors": log_errors})
+        return code
+    except BaseException as error:
+        details = exception_payload(error)
+        write_independent_logs(folders, f"실행경계오류_{stamp}.json", details)
+        print(details["traceback"], file=sys.stderr, flush=True)
+        if child is not None and child.poll() is None:
+            child.terminate(); child.wait()
+        return 130 if isinstance(error, KeyboardInterrupt) else 1
+    finally:
+        if locked:
+            try:
+                lock.unlink()
+            except OSError as error:
+                write_independent_logs(folders, f"잠금정리오류_{stamp}.json", exception_payload(error))
+
+
+def main():
+    parser = argparse.ArgumentParser(description="검증한 5차 복구 상태로 학습을 이어갑니다.")
+    parser.add_argument("--device", choices=("cuda", "cpu"), default="cuda")
+    parser.add_argument("--baseline-sha256", help="사전에 고정·검토한 비공개 원본 기준의 SHA256")
+    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
+    args = parser.parse_args()
+    if args.worker:
+        try:
+            authorized = worker_parent_authorized(os.environ.get("CT_RECOVERY_SUPERVISOR_PID"))
+        except Exception as error:
+            parser.error("worker 감독 연결을 확인하지 못했습니다: " + str(error))
+        if not authorized:
+            parser.error("worker는 사전 검사를 통과한 감독 프로세스에서만 시작합니다.")
+    if not args.worker and (not args.baseline_sha256 or len(args.baseline_sha256) != 64
+                            or any(c not in "0123456789abcdef" for c in args.baseline_sha256)):
+        parser.error("사전에 고정한 소문자 SHA256 64자리를 명시해야 합니다.")
+    return worker(ROOT, args.device, log_folders(ROOT)) if args.worker else supervise(ROOT, args.device, args.baseline_sha256)
````

## web/index.html

이전 8,904 B / SHA-256 `198be33c58446004072289b41dc7d1131936c713ad15058e14b89f453671245c`. 이후 8,904 B / SHA-256 `a5344e3d3a5151fc75adeeb474ce880292f0f536141be97f64d106183c25d332`.

````diff
--- 이전/web/index.html
+++ 이후/web/index.html
@@ -1,6 +1,6 @@
 <!doctype html>
-<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>폐 CT 특징 블러 실험 · 4차</title><script src="/theme.js"></script><link rel="stylesheet" href="/style.css"></head>
-<body><header class="topbar"><div class="identity"><h1>폐 CT 특징 블러 실험 · 4차</h1><p>첫 합성곱 특징을 흐린 뒤 분류 성능을 비교합니다</p></div><div class="top-actions"><button id="theme" class="theme-toggle" aria-label="어두운 화면으로 전환" aria-pressed="false"><span class="theme-track"><span></span></span><span id="themeText">다크</span></button><button id="refresh" class="icon-button" aria-label="상태 새로고침"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 7v5h-5M4 17v-5h5M6 6a8 8 0 0 1 13 2M5 16a8 8 0 0 0 13 2"/></svg></button></div></header>
+<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>폐 CT 특징 블러 실험 · 5차</title><script src="/theme.js"></script><link rel="stylesheet" href="/style.css"></head>
+<body><header class="topbar"><div class="identity"><h1>폐 CT 특징 블러 실험 · 5차</h1><p>첫 합성곱 특징을 흐린 뒤 분류 성능을 비교합니다</p></div><div class="top-actions"><button id="theme" class="theme-toggle" aria-label="어두운 화면으로 전환" aria-pressed="false"><span class="theme-track"><span></span></span><span id="themeText">다크</span></button><button id="refresh" class="icon-button" aria-label="상태 새로고침"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 7v5h-5M4 17v-5h5M6 6a8 8 0 0 1 13 2M5 16a8 8 0 0 0 13 2"/></svg></button></div></header>
 <aside class="sidebar"><nav aria-label="실험 메뉴"><a class="active" href="#overview"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m3 17 5-7 6 4 7-10"/><circle cx="3" cy="17" r="1"/><circle cx="8" cy="10" r="1"/><circle cx="14" cy="14" r="1"/><circle cx="21" cy="4" r="1"/></svg>실험 현황</a><a href="#analysis"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 20V10m6 10V4m6 16v-7m5 7H2"/></svg>학습 결과</a><a href="#data"><svg viewBox="0 0 24 24" aria-hidden="true"><ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 4 16 4 16 0V5M4 12c0 4 16 4 16 0"/></svg>데이터</a><a href="#records"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="5" y="3" width="15" height="18" rx="2"/><path d="M9 8h7m-7 4h7m-7 4h4M3 7h3m-3 5h3m-3 5h3"/></svg>기록</a></nav><div class="sidebar-note">폐 CT 실험실<span>Conv1 · ResNet-50</span><small>이 PC에서 실행</small></div></aside>
 <main><section id="overview"><div id="alert" class="alert" role="status"></div><div class="status-row"><div class="current-heading"><div class="status-title"><span id="badge" class="pill">기록 대기</span><h2 id="currentTitle">학습 상태를 기다리고 있습니다</h2></div><p id="sigmaLabel">블러 강도 기록 대기</p><p id="message" class="sr-only">첫 합성곱 특징에 블러를 적용해 분류 성능을 비교합니다.</p></div><div class="training-progress"><div class="progress-top"><h3>학습 진행</h3><strong id="epoch">—</strong><span id="process" class="process">프로세스 확인 대기</span></div><progress id="progress" value="0" max="100" aria-label="이번 학습 회차의 배치 진행률"></progress><div class="progress-bottom"><span id="seen">이번 회차 OK — / NG —</span><span id="device">장치 확인 중</span></div><span id="batch" class="batch-note">배치 미측정</span></div></div>
 <div class="training-policy" aria-label="학습 설정과 실제 진행"><dl><div><dt>현재 학습률</dt><dd id="learningRate">미측정</dd></div><div><dt>조기 종료 설정 / 대기 회차</dt><dd id="earlyStopping">미측정 / 미측정</dd></div><div><dt>최적 검증 회차</dt><dd id="bestEpoch">미측정</dd></div><div><dt>가중치 갱신 횟수</dt><dd id="optimizerSteps">미측정</dd></div></dl><p id="trainingPolicyNote">실제 종료 설정을 기다리고 있어요.</p></div>
````

## web/scene.js

이전 45,001 B / SHA-256 `c99592905b83b924170b89fc9c0b292683d694074672a4549ae8b2eb034cacda`. 이후 45,001 B / SHA-256 `4fa87e24b7ea4d062eda4050656f129ba838dc5069098edb533281f89f9ddced`.

````diff
--- 이전/web/scene.js
+++ 이후/web/scene.js
@@ -48,12 +48,12 @@
 
   // 완료 강도 × 세 범주 × 여섯 단계를 파일 ID로 구분해 전체 구성을 보여줍니다.
   const gallery=document.createElement('section');gallery.className='pipeline-gallery';gallery.setAttribute('aria-label','블러 강도별 원본과 특징 맵 전체 구성');
-  const galleryTitle=document.createElement('h2');easyText(galleryTitle,'🖼️ 4차 사진과 특징 그림 살펴보기');
+  const galleryTitle=document.createElement('h2');easyText(galleryTitle,'🖼️ 5차 사진과 특징 그림 살펴보기');
   const galleryDescription=document.createElement('p');galleryDescription.className='pipeline-gallery-description';
-  galleryDescription.textContent='4차에서 새로 만든 대표 사진을 기다리고 있어요. 이전 실험의 사진은 섞어 보여 주지 않습니다. 준비되면 강도와 자료를 골라 원본 1장과 특징 5단계를 볼 수 있어요.';
+  galleryDescription.textContent='5차에서 새로 만든 대표 사진을 기다리고 있어요. 이전 실험의 사진은 섞어 보여 주지 않습니다. 준비되면 강도와 자료를 골라 원본 1장과 특징 5단계를 볼 수 있어요.';
   const galleryNormalization=document.createElement('p');galleryNormalization.className='pipeline-gallery-normalization';
   galleryNormalization.textContent='특징 사진 한 장에는 작은 그림 10개가 있어요. 전체 평균 1개, 가장 큰 반응 1개, 골라낸 특징 8개입니다. 그림마다 색의 기준이 달라요. 밝은 곳이 암의 위치나 확률은 아닙니다.';
-  const galleryStatus=document.createElement('p');galleryStatus.className='pipeline-gallery-status';galleryStatus.setAttribute('role','status');galleryStatus.setAttribute('aria-live','polite');galleryStatus.textContent='4차 대표 사진은 아직 없어요. 새 생성 결과를 기다리고 있어요.';
+  const galleryStatus=document.createElement('p');galleryStatus.className='pipeline-gallery-status';galleryStatus.setAttribute('role','status');galleryStatus.setAttribute('aria-live','polite');galleryStatus.textContent='5차 대표 사진은 아직 없어요. 새 생성 결과를 기다리고 있어요.';
   const galleryStatistics=document.createElement('p');galleryStatistics.className='pipeline-gallery-statistics';
   const sigmaFieldset=document.createElement('fieldset');sigmaFieldset.className='pipeline-gallery-controls';
   const sigmaLegend=document.createElement('legend');easyText(sigmaLegend,'🌫️ 1. 얼마나 부드럽게 만들까요? 숫자가 클수록 더 부드러워요');
@@ -235,7 +235,7 @@
     galleryTimeout=window.setTimeout(()=>controller.abort(),8000);
     try{
       const response=await fetch('/api/feature-previews',{credentials:'same-origin',cache:'no-store',signal:controller.signal});if(disposed)return;
-      if(response.status===404){previewMessage('4차 대표 사진은 아직 없어요. 새 생성 결과를 기다리고 있어요.');return;}
+      if(response.status===404){previewMessage('5차 대표 사진은 아직 없어요. 새 생성 결과를 기다리고 있어요.');return;}
       if(!response.ok)throw new Error('preview unavailable');
       const payload=await response.json();if(disposed)return;
       if(typeof payload.run_id!=='string'||!previewRunPattern.test(payload.run_id)||!Array.isArray(payload.items)){previewMessage('현재 실행에 맞는 전체 특징 맵을 기다리는 중입니다.');return;}
@@ -246,7 +246,7 @@
       completedSigmas=new Set(sigmaOrder.filter(readySigma));
       if(externalSigma!==null)selectedSigma=externalSigma;else if(selectedSigma===null||!completedSigmas.has(selectedSigma))selectedSigma=sigmaOrder.find(sigma=>completedSigmas.has(sigma))??null;
       renderGallery();
-      previewMessage(completedSigmas.size?'완료된 강도와 범주를 선택하면 원본부터 5단계까지 6개 그림이 아래에 모두 표시됩니다.':'4차 대표 사진의 새 생성 결과를 기다리고 있어요.');
+      previewMessage(completedSigmas.size?'완료된 강도와 범주를 선택하면 원본부터 5단계까지 6개 그림이 아래에 모두 표시됩니다.':'5차 대표 사진의 새 생성 결과를 기다리고 있어요.');
     }catch(error){
       if(!disposed)previewMessage(galleryFigures.size?'선택한 그림을 표시하고 있습니다. 목록을 잠시 갱신하지 못했습니다.':'전체 특징 맵을 기다리는 중입니다. 현재 미리보기를 불러올 수 없습니다.');
     }finally{window.clearTimeout(galleryTimeout);galleryTimeout=0;galleryBusy=false;if(galleryController===controller)galleryController=null;}
````

## 결과/강도별 _전체 10 조 건 _집계.json

이전 0 B / SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. 이후 3,955 B / SHA-256 `e281e016483268c427c970a4df1d78e1ae49f66cc5ffa79f135b75d68713d62a`.

````diff
--- 이전/결과/강도별_전체10조건_집계.json
+++ 이후/결과/강도별_전체10조건_집계.json
@@ -0,0 +1,211 @@
+{
+  "scope": "기존 실제5차의 강도별 적응학습 완료 집계. 새7차 결과가 아님",
+  "model_selection": "각 강도를100회 학습한 뒤 그 강도의 raw validation loss가 가장 낮은 best 선택. 100번째 모델 고정이라는 뜻이 아님",
+  "rows": [
+    {
+      "sigma": 0,
+      "epochs_ran": 100,
+      "best_epoch": 78,
+      "correct": 164,
+      "total": 164,
+      "accuracy": 1.0,
+      "rounded_percent": "100.0%",
+      "auc": 1.0,
+      "confusion_matrix": [
+        [
+          80,
+          0
+        ],
+        [
+          0,
+          84
+        ]
+      ]
+    },
+    {
+      "sigma": 1,
+      "epochs_ran": 100,
+      "best_epoch": 30,
+      "correct": 164,
+      "total": 164,
+      "accuracy": 1.0,
+      "rounded_percent": "100.0%",
+      "auc": 1.0,
+      "confusion_matrix": [
+        [
+          80,
+          0
+        ],
+        [
+          0,
+          84
+        ]
+      ]
+    },
+    {
+      "sigma": 2,
+      "epochs_ran": 100,
+      "best_epoch": 40,
+      "correct": 164,
+      "total": 164,
+      "accuracy": 1.0,
+      "rounded_percent": "100.0%",
+      "auc": 1.0,
+      "confusion_matrix": [
+        [
+          80,
+          0
+        ],
+        [
+          0,
+          84
+        ]
+      ]
+    },
+    {
+      "sigma": 4,
+      "epochs_ran": 100,
+      "best_epoch": 59,
+      "correct": 164,
+      "total": 164,
+      "accuracy": 1.0,
+      "rounded_percent": "100.0%",
+      "auc": 1.0,
+      "confusion_matrix": [
+        [
+          80,
+          0
+        ],
+        [
+          0,
+          84
+        ]
+      ]
+    },
+    {
+      "sigma": 8,
+      "epochs_ran": 100,
+      "best_epoch": 39,
+      "correct": 162,
+      "total": 164,
+      "accuracy": 0.9878048780487805,
+      "rounded_percent": "98.8%",
+      "auc": 1.0,
+      "confusion_matrix": [
+        [
+          80,
+          0
+        ],
+        [
+          2,
+          82
+        ]
+      ]
+    },
+    {
+      "sigma": 16,
+      "epochs_ran": 100,
+      "best_epoch": 30,
+      "correct": 160,
+      "total": 164,
+      "accuracy": 0.975609756097561,
+      "rounded_percent": "97.6%",
+      "auc": 1.0,
+      "confusion_matrix": [
+        [
+          80,
+          0
+        ],
+        [
+          4,
+          80
+        ]
+      ]
+    },
+    {
+      "sigma": 32,
+      "epochs_ran": 100,
+      "best_epoch": 11,
+      "correct": 159,
+      "total": 164,
+      "accuracy": 0.9695121951219512,
+      "rounded_percent": "97.0%",
+      "auc": 0.9900297619047619,
+      "confusion_matrix": [
+        [
+          78,
+          2
+        ],
+        [
+          3,
+          81
+        ]
+      ]
+    },
+    {
+      "sigma": 64,
+      "epochs_ran": 100,
+      "best_epoch": 4,
+      "correct": 131,
+      "total": 164,
+      "accuracy": 0.7987804878048781,
+      "rounded_percent": "79.9%",
+      "auc": 0.8924107142857143,
+      "confusion_matrix": [
+        [
+          61,
+          19
+        ],
+        [
+          14,
+          70
+        ]
+      ]
+    },
+    {
+      "sigma": 128,
+      "epochs_ran": 100,
+      "best_epoch": 7,
+      "correct": 102,
+      "total": 164,
+      "accuracy": 0.6219512195121951,
+      "rounded_percent": "62.2%",
+      "auc": 0.7160714285714287,
+      "confusion_matrix": [
+        [
+          45,
+          35
+        ],
+        [
+          27,
+          57
+        ]
+      ]
+    },
+    {
+      "sigma": 256,
+      "epochs_ran": 100,
+      "best_epoch": 1,
+      "correct": 88,
+      "total": 164,
+      "accuracy": 0.5365853658536586,
+      "rounded_percent": "53.7%",
+      "auc": 0.5732142857142857,
+      "confusion_matrix": [
+        [
+          59,
+          21
+        ],
+        [
+          55,
+          29
+        ]
+      ]
+    }
+  ],
+  "limitations": [
+    "영상 단위 분할, 환자 독립성 미확인",
+    "동일 시험164장, 시험으로 모델·강도·임계값 선택하지 않음",
+    "백분율은 소수 첫째 자리 반올림, accuracy는 저장 원비율"
+  ]
+}
````

## 변경기록.md

이전 5,346 B / SHA-256 `3dc7c1efef1362b5c12bdf0cbabf2d73eceac9aeb961ab53fa5af7d2bd703c98`. 이후 0 B / SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

````diff
--- 이전/변경기록.md
+++ 이후/변경기록.md
@@ -1,48 +0,0 @@
-<a id="-고정-100회-학습과-종료-정책-비교--공개-코드-5차"></a>
-
-# 고정 100회 학습과 종료 정책 비교 · 공개 코드 5차
-
-조기 종료의 영향을 비교할 수 있도록 **실험 4차**를 준비했습니다. 공개 저장소에서는 이전 공개 1~4차를 보존하고 이 코드를 **공개 5차**에 담습니다. 공개 번호와 실제 학습 실험 번호는 다릅니다. 코드·검증 준비, 학습 시작과 전체 학습 완료를 구분하며 아직 새 실험의 최종 성능을 보고하지 않습니다.
-
-<a id="무엇을-비교하나요"></a>
-
-## 비교 조건
-
- 같은 원본과 분할 →  같은 모델·초기값·학습 표본 →  강도마다 100회 학습 →  종료 정책에 따른 두 모델 비교 순서입니다.
-
-| 유지하는 조건 | 바꾸거나 추가한 조건 |
-|---|---|
-| 원본 목록·정확한 학습/검증/시험 분할 | 기준 manifest 파일·원본 목록 해시 및 실제 분할 동일성 검사 |
-| 모델·초기 seed·학습 전용 증강·클래스당 5000개 온라인 표본 | 조기 종료를 비활성화하고 강도마다 100회 학습 |
-| 배치·AdamW·검증 손실 기반 학습률 감소 | 기존 정책이 멈췄을 첫 회차와 그때까지의 검증 최저 모델을 관찰용으로 별도 보존 |
-| 시험셋을 학습·모델·강도 선택에 사용하지 않음 | 전체 100회 완료 뒤 전체 최저 검증 모델과 관찰용 모델을 같은 시험 자료로 비교 |
-
-두 모델은 같은 학습 경로의 앞부분과 전체 경로에서 고른 모델입니다. 관찰용 종료는 실제 학습을 중단하지 않습니다. 중단 후 재개할 때 관찰용 종료 상태·가중치·optimizer·scheduler·난수 상태도 보존합니다. 이미 사용한 분할과 시험셋을 다시 이용하므로 탐색적 종료 정책 비교이며 새 독립 임상 검증이 아닙니다.
-
-## 수치와 화면
-
-백분율 요약은 소수 첫째 자리까지 반올림합니다. 원비율·전체 백분율·정답 수를 함께 확인할 수 있어 반올림된 100.0%와 실제 모든 정답을 구분합니다. AUC·손실·학습률의 원값 조회는 유지하며 원본 결과 파일의 수치를 바꾸지 않습니다.
-
-새 실행 기록이 아직 없으면 대기 상태를 표시하고 결과 요청을 보내지 않습니다. 인증된 결과 API는 수치 타입·유한성·범위뿐 아니라 혼동행렬과 정답 수·정확도의 일관성을 대조합니다. 다른 실행이나 모순된 값은 결과로 표시하지 않습니다. 이 검사는 모든 미래 결함을 방지한다는 보장이 아닙니다.
-
-## 실행에 필요한 자체 자료
-
-공개 설정 예제에는 개인 데이터 경로와 기준 manifest의 실제 식별 해시를 넣지 않습니다. 사용자는 자신의 원본과 기준 manifest를 준비하고 `expected_reference_manifest`, `expected_reference_manifest_sha256`, `expected_reference_records_sha256`를 채워야 합니다. 예제 그대로는 기준 비교를 실행할 수 없습니다. 원본 목록과 정확한 분할이 다르면 중단하는 검증 코드는 유지합니다. [공개 실행 방법](../../Conv1%20블러%20OK-NG%20실험/5차/docs/실행방법.md)을 따릅니다.
-
-특징맵 저장 도구는 [이전 공개 4차의 도구](../../Conv1%20블러%20OK-NG%20실험/4차/생성%20도구/사용방법.md)를 재사용할 수 있습니다. `--experiment-root`, `--output-root`, `--reference-root`, `--run-id`를 새 실험의 실제 값으로 명시합니다. 새 실험의 특징맵 사진을 이미 생성했다는 뜻은 아닙니다.
-
-## 공개 파일과 검증 범위
-
-새 실험의 `src/`, `run_training.py`, `dashboard.py`, 웹·검사 코드·README·문서 4개·글꼴과 라이선스·정제 설정 예제를 포함합니다. 코드의 함수·주석·공백 변화와 관찰용 종료 상태·분할 고정·정답 수·수치 표시 검사는 실제 전체 비교로 연결합니다.
-
-CPU 단위·통합 검사와 실제 GPU 배치 연결 검사는 실행 연결과 제어 동작을 확인하는 절차입니다. 장시간 10조건의 학습 완료나 새 연구 성능을 대신하지 않습니다. 최종 직접 검사 수와 독립 검토는 별도 검증 기록으로 확인합니다.
-
-원본 환자 ID와 실제 촬영 출처가 없어 환자 독립성·임상 성능·프라이버시 효과를 확정하지 않습니다. `source_class`는 원본 범주 폴더 라벨이며 병원·환자·스캐너 식별자가 아닙니다. 모든 알려진 증강이나 원본 노트북의 환자 7-fold·복원 공격을 구현했다는 주장도 하지 않습니다.
-
-의료영상·특징맵 PNG·원본 목록·예측·가중치·운영 기록·접속정보·개인 계획서·개인 지침은 제외합니다. 비공개 감사의 집계 수치도 공개하지 않습니다. 이번 코드 작업에는 새 논문 원고가 없으며 기존 공개 논문은 보존합니다.
-
-[이번 공개 변경 전체](../../docs/revision-diffs/conv1-okng-round5.diff) · [같은 파일별 공개 4차 대비 비교](../../docs/revision-diffs/conv1-okng-round5-vs-round4.diff)
-
-| 그대로 사용한 바이너리 | 바이트 | SHA-256 |
-|---|---:|---|
-| web/fonts/NanumGothic-Bold.ttf | 2073868 | f96298f9fb18e364d2370f4c3ce948ac67a2b61af992d7234bc15c42b033c674 |
````

## 복구_학습.py

이전 0 B / SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. 이후 204 B / SHA-256 `0d199cb835909621b73258c5d5bdac76943d82932deaf9ceec2f8a4620f0f972`.

````diff
--- 이전/복구_학습.py
+++ 이후/복구_학습.py
@@ -0,0 +1,7 @@
+"""저장 공간·중복 실행·독립 오류 로그를 확인한 후 기존 학습을 이어갑니다."""
+
+from tools.safe_training import main
+
+
+if __name__ == "__main__":
+    raise SystemExit(main())
````

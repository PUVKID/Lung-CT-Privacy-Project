# 실제 7차 → 실제 8차 공개 파일 전체 비교

텍스트는 모든 행·주석·공백을 포함한 unified diff입니다. 비교 표시의 CRLF만 LF로 정규화하고 실제 바이트 크기·SHA는 각 파일에 별도로 기록합니다. 바이너리는 내용을 추정하지 않고 크기·SHA로 비교합니다.

## README.md

| 구분 | 이전 | 이후 |
| --- | --- | --- |
| 상태 | 수정 | 수정 |
| 바이트 | 2131 | 4135 |
| SHA-256 | 99683f10a27bcf075982d603e9ed90e2a4eb7485cd78b93b1e8cc7d2606843fd | e3ec07b2e5cdb72c050f14f19d1b06c9733f444426e99fc1ecc19f781608fad1 |

````diff
--- a/README.md
+++ b/README.md
@@ -1,25 +1,28 @@
-# 실제7차 고정 모델 블러 실험
+# 실제8차 · 강도별 독립 학습과 프라이버시 제안 점수
 
-[LEVEL 1 - Beginner](../../docs/revisions/conv1-okng-round7.md#reading-level-1) · [LEVEL 2 - Explorer](../../docs/revisions/conv1-okng-round7.md#reading-level-2) · [LEVEL 3 - Practitioner](../../docs/revisions/conv1-okng-round7.md#reading-level-3) · [LEVEL 4 - Advanced](../../docs/revisions/conv1-okng-round7.md#reading-level-4) · [LEVEL 5 - Expert](../../docs/revisions/conv1-okng-round7.md#reading-level-5)
+[LEVEL 1 - Beginner](../../docs/revisions/conv1-okng-round8.md#reading-level-1) · [LEVEL 2 - Explorer](../../docs/revisions/conv1-okng-round8.md#reading-level-2) · [LEVEL 3 - Practitioner](../../docs/revisions/conv1-okng-round8.md#reading-level-3) · [LEVEL 4 - Advanced](../../docs/revisions/conv1-okng-round8.md#reading-level-4) · [LEVEL 5 - Expert](../../docs/revisions/conv1-okng-round8.md#reading-level-5)
 
-새 ImageNet 초기값에서 σ0만100회 학습하고 최저검증손실 모델 하나를 고정해 열 블러 강도를 추가학습 없이 평가합니다. 공개 기록 시점 학습 진행 중이며 최종시험결과는미측정입니다.
+열 블러 강도 각각 새100회 학습 뒤 최저 검증손실 모델을 선택하고 분류와 원본 후보 공격을 모두 계산한 다음 다음 강도로 진행합니다. **2026-11-20 확인 시점 σ0 학습 중이며 분류 성적과 점수는 미측정**입니다. 기존7차의 단일 고정모델 실험과 다릅니다.
 
-| 자료 | 역할 | 사용 조건 |
+| 자료 | 역할 | 입력 조건 |
 | --- | --- | --- |
-| 코드 | 실제 공개 소스 | 자신의 자료·환경과 기준 필요 |
-| 설정 예제 | 사적 경로·manifest SHA 제외 | config.json과 고정 입력을 직접 준비 |
-| 상세 설명 | 절차·조건·검증·한계 | 위에서 같은 수준 선택 |
+| config.example.json | 공개 설정 형식 | 자신의 dataset/기준manifest경로·파일SHA·recordsSHA·초기가중치 필요 |
+| src/·run_training.py·안전_학습.py | 학습·선정·분류·공격·감독 | 실제자료를 포함하지 않음 |
+| dashboard.py·web/ | 강도 선택과 실제 원값 조회 | 선택 강도 모델/입력/소스 결합 검증 |
+| tests/ | 합성 단위검사·API·Node VM 회귀 | 실제 CT 공격 성적이나 화면 렌더링 검사가 아님 |
+| 결과/측정상태.json | 실제 미측정 상태 | 합성 대조군 점수를 실제 결과로 채우지 않음 |
 
-`config.example.json`을 자신의 `config.json`으로 복사한 뒤 원본 경로와 고정 기준을 채워야 합니다. 예제만으로 실제학습·복구를 실행할 수 없습니다. 원영상·manifest·모델·상태·접속정보는 공개하지 않습니다.
+공개 사본의 config.example.json을 config.json으로 복사하고 자신의 입력을 준비해야 합니다. **전체 검사 중 실제 ResNet50 경로 검사는 로컬 ImageNet V1 초기 가중치 파일이 필요합니다.** 실제 CT 없이 수행하는 합성 검사에도 이 모델 검사를 포함합니다. config.json의 initial_weights_path를 자신의 로컬 파일로 지정하고 initial_weights_sha256와 대조해야 합니다. 예제를 config.json으로 복사한 뒤 검사 명령 실행 전에 이 입력을 준비하며, 가중치를 공개 저장소에 넣지 않습니다. 원영상·분할 manifest·가중치는 외부에 포함하지 않습니다. 로컬 ImageNet V1 파일의 SHA와 실제 기준 manifest를 대조한 뒤 prepare로 입력을 고정합니다. 이미 학습이 시작된 작업에서는 prepare·smoke가 상태를 덮어쓰지 않도록 거부합니다. 실제 연구 폴더나 실행 중인 서버를 이 공개 예제로 바꾸지 않습니다.
 
-## 공개 코드의 합성 검사
-
-합성 검사는 실제 CT·가중치 없이 수행하지만 설정 형식을 읽으므로 먼저 공개 예제를 config.json으로 준비합니다. 자신의 실제 학습 설정과 혼동하지 않도록 별도의 공개 사본에서 수행합니다.
+합성 검사는 별도의 공개 사본에서 다음과 같이 실행합니다. Python·PyTorch·torchvision·NumPy·SciPy·Pillow와 Node.js가 필요하며 호환 환경은 직접 확인해야 합니다. 이 저장소에 의료자료와 초기 가중치를 포함했다는 뜻은 아닙니다.
 
 ```powershell
 Copy-Item -LiteralPath config.example.json -Destination config.json
+# 이어 config.json의 initial_weights_path를 로컬 가중치로 지정하고 SHA를 확인합니다.
 $env:CUDA_VISIBLE_DEVICES = "-1"
 python -B -X utf8 -m unittest discover -s tests -p "test_*.py" -v
 ```
 
-검사 후 자신이 준비한 임시 config.json만 정리하고, 실제 학습에는 자신의 고정 자료와 검토한 설정을 다시 준비합니다. 심볼릭 링크 생성 권한이 없는 Windows에서는 해당 권한 의존 검사 한 개가 건너뛰어질 수 있으므로 나머지 검사 성공과 구분합니다.
+실제 입력을 별도로 준비한 실험에서는 `python -B -X utf8 run_training.py prepare` 후 검토한 baseline SHA를 `python -B -X utf8 안전_학습.py --device cuda --baseline-sha256 <검토한SHA>`에 전달합니다. 세션/작업 식별자는 공개 감독 사본의 CT_EXPERIMENT_SESSION·CT_EXPERIMENT_TASK 환경변수로 로컬 지정할 수 있습니다. 토큰·세션 URL·실패 원문과 의료 경로는 공개하지 않습니다.
+
+화면의 **프라이버시 제안 점수 · 100점 만점**은 gallery-residual-v1입니다. 알려진 인코더와 원본 후보 gallery에서 실제 특징 바이트 사전 공격을 포함해 측정하는 조건부 연구용 잔여 점수입니다. 높을수록 이 공격에서 원본을 되찾기 어렵다는 뜻이며 보호 확률·세계 최초·표준·DP·환자 재식별 방어를 뜻하지 않습니다. 실측0점은0.0으로 표시하고 미완료·오류는 미측정으로 남깁니다. 상세의 같은 읽기 수준에서 산식·분모·정밀도·한계를 확인하세요.
````

## config.example.json

| 구분 | 이전 | 이후 |
| --- | --- | --- |
| 상태 | 수정 | 수정 |
| 바이트 | 3365 | 2519 |
| SHA-256 | 43733866552f2ffedaa1fdd8bd2d689fc9a684116c2eec2d81009ded203eb8bd | 6a17701369315b25bafdf6d4d45cae3b08e1e05a3dc91a9fd72134dab49ac991 |

````diff
--- a/config.example.json
+++ b/config.example.json
@@ -43,21 +43,18 @@
   "status_every_batches": 10,
   "pretrained_weights": "torchvision.ResNet50_Weights.IMAGENET1K_V1",
   "framework": "PyTorch CUDA",
-  "protocol": "fixed-model-sigma0-v1",
+  "protocol": "independent-sigma-privacy-v1",
   "port_notes": [
-    "2차는 원본 클래스 분포를 반영해 완전 중복 및 고정 64픽셀 8bit RMSE 5 이하 연결 그룹을 같은 분할에 둡니다. 이 그룹은 환자 ID가 아닙니다.",
-    "학습 BF16/평가 FP32를 분리하며 signed-softplus BCE는 학습 FP32·평가 FP64로 계산합니다. AUC/AP는 확률 포화 전 로짓 순위를 사용합니다.",
-    "RTX 4090에서 FP16 기본 GradScaler 65536은 실제 512 학습 연속 배치에 비유한 기울기를 발생시켰습니다. 지원이 확인된 BF16 autocast를 명시하며 BF16에는 GradScaler를 사용하지 않습니다. 손실·기울기의 비유한 값 검사는 유지합니다.",
-    "Windows 네이티브 TensorFlow 최신판은 CUDA GPU를 지원하지 않아 PyTorch CUDA로 이식합니다.",
-    "torchvision ResNet50은 V1.5이며 Keras ResNet50과 stride·가중치·RGB 정규화 전처리가 다릅니다. 원본 결과의 수치상 재현을 주장하지 않습니다.",
-    "첫 합성곱만 Edge에 두고 BN/활성화/풀링부터는 Cloud에 둡니다. 첫 합성곱과 모든 BN은 고정하고 layer4의 비BN 가중치와 분류 헤드만 학습합니다.",
-    "sigma는 특징맵 픽셀 단위이며 DCT-II 반사/Neumann 경계의 Gaussian heat filter입니다.",
-    "환자 ID가 없어 이미지 단위 예비실험입니다. 원본의 환자 7-fold 70조건·매칭·복원 공격·프라이버시 임계점 선택은 미실행입니다. 7차는 sigma0 학습 모델 하나를 고정해 평가하는 별도 프로토콜입니다.",
-    "클래스당 5000은 epoch별 온라인 증강 표본 수이며 독립 원본/환자 수가 아닙니다. 시험셋으로 sigma 또는 임계값을 선택하지 않습니다.",
-    "7차는 로컬 ImageNet 초기값에서 sigma0만100회 새 학습하고 검증 손실로 선정한 단일 best의 전체 가중치를 고정하여10블러를 평가합니다. 각 블러에 맞춰 재학습하지 않습니다."
+    "8차는 강도마다 같은 로컬 ImageNet 초기값에서 새 모델·옵티마이저로100회 독립 학습하고 해당 검증 손실 최소 모델을 평가합니다.",
+    "클래스당5000은 온라인 반복·증강 표본이며 독립 원본 수가 아닙니다. 원본1097장과769/164/164 분할을 보존합니다.",
+    "첫 합성곱과 모든 BN을 고정하고 layer4 비BN 및 head만 학습합니다. 학습 BF16과 분류 평가 FP32를 구분합니다.",
+    "점수는 알려진 encoder·원본 후보 gallery·packet batch1·FP32의 조건부 공격 실측값입니다. 분류 평가 batch8 전송패킷을 그대로 검증한 것이 아닙니다.",
+    "gallery-residual-v1은 이번 실험 제안식으로 독창성·표준성·DP·안전확률·환자 재식별 방어를 주장하지 않습니다. 점수0도 그대로 보고합니다.",
+    "고정 conv1은 후단 독립 학습으로 변하지 않으므로 같은 강도의 프라이버시 특징이 동일할 수 있습니다.",
+    "환자ID 없는 영상 단위 탐색적 실험입니다. 시험셋으로 강도·모델·임계값을 선택하지 않습니다."
   ],
-  "protocol_fixed_model": true,
-  "training_sigma": 0,
+  "protocol_fixed_model": false,
   "initial_weights_path": "work/torch-cache/hub/checkpoints/resnet50-0676ba61.pth",
-  "initial_weights_sha256": "0676ba61b6795bbe1773cffd859882e5e297624d384b6993f7c9e683e722fb8a"
+  "initial_weights_sha256": "0676ba61b6795bbe1773cffd859882e5e297624d384b6993f7c9e683e722fb8a",
+  "score_version": "gallery-residual-v1"
 }
````

## dashboard.py

| 구분 | 이전 | 이후 |
| --- | --- | --- |
| 상태 | 수정 | 수정 |
| 바이트 | 35599 | 39310 |
| SHA-256 | c41637ea358c241d8c8b6050c3011c4c0a5b75975874f92c667640f180d92d69 | 57a326ded68d7d10d796a5fced2be3f77cb3f8607cdab574a483b124c49d9403 |

````diff
--- a/dashboard.py
+++ b/dashboard.py
@@ -17,7 +17,7 @@
 from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
 from urllib.parse import parse_qs, urlsplit
 
-from src.identity import validate_run, validate_fixed_result, load_selection, file_sha256, safe_path
+from src.identity import validate_run, validate_result, validate_privacy_result, load_selection, file_sha256, safe_path
 
 ROOT = Path(__file__).resolve().parent
 ASSETS = {
@@ -75,13 +75,12 @@
     classes = {"Bengin_cases": "양성", "Malignant_cases": "악성", "Normal_cases": "정상"}
     result = {"run_id": run_id, "items": [], "completed_sigmas": [],
               "pending": list(sigmas), "expected_total": 180}
-    folder = root.parent / "블러 강도별 대표 특징맵" / "7차"
+    folder = root.parent / "블러 강도별 대표 특징맵" / "8차"
     try:
-        if not run_id or status.get("training_status") != "completed":
-            result["message"] = "블러 0의 100회 학습과 고정 모델 선정을 기다리고 있습니다."
+        if not run_id:
+            result["message"] = "현재 실행에서 강도별 독립 학습·분류 평가·점수 계산을 기다리고 있습니다."
             return result
         metadata = validate_run(root, run_id)
-        selection = load_selection(root, run_id)
         folder = safe_path(root.parent, folder)
         if folder.is_symlink() or not folder.resolve().is_relative_to(root.parent.resolve()):
             raise ValueError("이미지 폴더 경계 오류")
@@ -91,29 +90,45 @@
         manifest = json.loads(manifest_path.read_text(encoding="utf-8"), parse_constant=reject_nonfinite)
         if not isinstance(run_id, str) or len(run_id) != 16 or any(c not in "0123456789abcdef" for c in run_id) or manifest.get("run_id") != run_id:
             raise ValueError("실행 식별자 불일치")
-        identities = {"protocol": "fixed-model-sigma0-v1", "protocol_fixed_model": True, "training_sigma": 0,
-                      "checkpoint_sha256": selection["checkpoint_sha256"], "model_state_sha256": selection["model_state_sha256"],
-                      "checkpoint_epoch": selection["best_epoch"], "selected_checkpoint": selection["selected_checkpoint"],
+        identities = {"protocol": "independent-sigma-privacy-v1", "protocol_fixed_model": False,
                       "manifest_records_sha256": metadata["manifest_sha256"],
                       "source_manifest_sha256": file_sha256(root / "work/results/dataset_manifest_private.json"),
                       "model_source_sha256": file_sha256(root / "src/model.py"),
                       "data_source_sha256": file_sha256(root / "src/data.py"),
                       "generator_sha256": file_sha256(root / "tools/feature_generator.py")}
-        if manifest.get("schema_version") != 2 or any(manifest.get(key) != value or type(manifest.get(key)) is not type(value) for key, value in identities.items()):
+        if manifest.get("schema_version") != 3 or any(manifest.get(key) != value or type(manifest.get(key)) is not type(value) for key, value in identities.items()):
             raise ValueError("특징맵 실행·소스·고정 모델 불일치")
         completed = {entry.get("sigma") for entry in status.get("sigma_queue", [])
-                     if entry.get("status") == "completed"}
+                     if entry.get("status") == "completed" and entry.get("classification_status")=="completed" and entry.get("privacy_status")=="completed"}
         raw_items = manifest.get("items", [])
         if not isinstance(raw_items, list) or len(raw_items) > 180:
             raise ValueError("특징맵 목록 개수 오류")
+        # 이미지 한 장 요청은 공통 경계와 해당 강도의 18장만 대조합니다.
+        # 목록 요청은 모든 완료 강도의 180장을 그대로 검증합니다. 요청 간 캐시는 사용하지 않습니다.
+        requested_sigma=None
+        if requested_id is not None:
+            registered={f"{sigma}-{class_key}-{stage}":sigma for sigma in sigmas for class_key in classes for stage in range(6)}
+            if requested_id not in registered:
+                raise ValueError("등록되지 않은 이미지 식별자")
+            requested_sigma=registered[requested_id]
         for sigma in sigmas:
+            if requested_sigma is not None and sigma != requested_sigma:
+                continue
             if sigma not in completed or sigma not in manifest.get("completed_sigmas", []):
                 continue
             metrics_path = root / "work" / "results" / f"run_{run_id}" / f"sigma_{sigma}_metrics.json"
             if metrics_path.is_symlink() or not metrics_path.resolve().is_relative_to(root.resolve()):
                 raise ValueError("결과 파일 경계 오류")
             metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
-            validate_fixed_result(root, metrics, expected_run=run_id)
+            validate_result(root, metrics, expected_run=run_id)
+            privacy_path=safe_path(root, f"work/results/run_{run_id}/sigma_{sigma}_privacy.json")
+            privacy=json.loads(privacy_path.read_text(encoding="utf-8"),parse_constant=reject_nonfinite)
+            validate_privacy_result(root,privacy,expected_run=run_id)
+            if privacy.get("sigma")!=sigma or type(privacy.get("sigma"))is not int:
+                raise ValueError("특징 그림 점수 강도 불일치")
+            selection=load_selection(root,run_id,sigma)
+            item_identity={key:selection[key]for key in ("protocol","protocol_fixed_model","training_sigma","checkpoint_sha256","model_state_sha256","checkpoint_epoch","selected_checkpoint")}
+
             if metrics.get("run_id") != run_id or metrics.get("sigma") != sigma or not metrics.get("test") or not metrics.get("completed_at"):
                 continue
             bundle = []
@@ -126,8 +141,8 @@
                     entry = matches[0]
                     if entry.get("run_id") != run_id:
                         raise ValueError("특징맵 개별 실행 불일치")
-                    for key in ("protocol_fixed_model", "training_sigma", "checkpoint_sha256", "model_state_sha256", "checkpoint_epoch", "selected_checkpoint"):
-                        if entry.get(key) != identities[key] or type(entry.get(key)) is not type(identities[key]):
+                    for key in ("protocol", "protocol_fixed_model", "training_sigma", "checkpoint_sha256", "model_state_sha256", "checkpoint_epoch", "selected_checkpoint"):
+                        if entry.get(key) != item_identity[key] or type(entry.get(key)) is not type(item_identity[key]):
                             raise ValueError("특징맵 개별 고정 모델 불일치")
                     relative = feature_preview_path(sigma, class_key, stage)
                     if entry.get("relative_path", "").replace("\\", "/") != relative.as_posix():
@@ -146,7 +161,7 @@
                         "panel_count": entry.get("panel_count", 1),
                         "panel_minmax": entry.get("panel_minmax", []),
                         "checkpoint_epoch": entry.get("checkpoint_epoch"),
-                        "training_sigma": 0, "checkpoint_sha256": selection["checkpoint_sha256"],
+                        "training_sigma": sigma, "checkpoint_sha256": selection["checkpoint_sha256"],
                         "eval_optimizer_steps": 0,
                         "precision": "CPU FP32 평가 추론",
                         "preprocessing": "512×512 회색조를 3채널에 복제한 뒤 RGB 평균·표준편차로 정규화합니다.",
@@ -217,7 +232,7 @@
 STATUS_FIELDS = {"schema_version", "protocol_fixed_model", "protocol", "phase", "training_status", "training_sigma",
                  "stage", "status", "updated_at", "pid", "run_id", "sigma", "sigma_index", "sigmas", "epochs", "epoch",
                  "batch", "batches", "learning_rate", "optimizer_steps", "best_epoch", "best_raw_epoch", "early_stopping_wait",
-                 "evaluation_current_sigma", "checkpoint_sha256", "model_state_sha256", "eval_optimizer_steps"}
+                 "classification_status", "privacy_status", "score_version", "evaluation_current_sigma", "checkpoint_sha256", "model_state_sha256", "eval_optimizer_steps"}
 HISTORY_FIELDS = {"sigma", "epoch", "train_loss", "val_loss", "val_accuracy", "val_auc", "learning_rate",
                   "next_learning_rate", "optimizer_steps", "early_stopping_wait"}
 
@@ -236,12 +251,8 @@
             output[key] = value
     output["history"] = [{key: value for key, value in row.items() if key in HISTORY_FIELDS and scalar(value)}
                          for row in data.get("history", []) if isinstance(row, dict)] if isinstance(data.get("history", []), list) else None
-    output["sigma_queue"] = [{key: value for key, value in row.items() if key in {"sigma", "status"} and scalar(value)}
+    output["sigma_queue"] = [{key: value for key, value in row.items() if key in {"sigma", "status", "training_status", "classification_status", "privacy_status"} and scalar(value)}
                              for row in data.get("sigma_queue", []) if isinstance(row, dict)] if isinstance(data.get("sigma_queue", []), list) else None
-    if data.get("protocol_fixed_model") is True and data.get("training_status") != "completed":
-        output["sigma_queue"] = [{"sigma": sigma, "status": "pending"} for sigma in SIGMA_VALUES]
-        for key in ("checkpoint_sha256", "model_state_sha256"):
-            output.pop(key, None)
     dataset = data.get("dataset")
     if isinstance(dataset, dict):
         output["dataset"] = {"original_total": dataset.get("original_total") if type(dataset.get("original_total")) is int else None,
@@ -276,7 +287,7 @@
         if data.get("run_id") is not None:
             validate_run(root, data["run_id"])
             if data.get("training_status") == "completed":
-                selection = load_selection(root, data["run_id"])
+                selection = load_selection(root, data["run_id"], data.get("sigma"))
                 if type(data.get("epoch")) is not int or data["epoch"] != 100:
                     raise ValueError("고정 완료 상태의 학습 회차 불일치")
                 for key in ("training_sigma", "best_epoch", "checkpoint_sha256", "model_state_sha256"):
@@ -301,21 +312,21 @@
 
 
 def sigma_results(root, sigma):
-    """한 번 학습한 현재 모델의 강도별 평가만 제공합니다."""
+    """현재 실행에서 해당 강도가 독립 학습·평가한 결과만 제공합니다."""
     state = read_status(root)
     run_id = state.get("run_id")
     valid_run = isinstance(run_id, str) and len(run_id) == 16 and all(c in "0123456789abcdef" for c in run_id)
     valid_sigma = type(sigma) is int and sigma in SIGMA_VALUES
     result = {"run_id": run_id if valid_run else None, "sigma": sigma if valid_sigma else None,
-              "history": [], "evaluation_history": [], "metrics": None, "status": "unavailable",
+              "history": [], "evaluation_history": [], "metrics": None, "privacy": None, "privacy_status": "pending", "status": "unavailable",
               "message": "현재 실행의 결과 기록을 기다리고 있습니다."}
     if not valid_sigma or not valid_run:
         return result
     folder = root / "work" / "results" / f"run_{run_id}"
     try:
         validate_run(root, run_id)
-        if state.get("protocol_fixed_model") is not True or type(state.get("training_sigma")) is not int or state.get("training_sigma") != 0:
-            raise ValueError("고정 모델 프로토콜 불일치")
+        if state.get("protocol_fixed_model") is not False or state.get("protocol") != "independent-sigma-privacy-v1":
+            raise ValueError("강도별 독립 모델 프로토콜 불일치")
         queue = state.get("sigma_queue", [])
         if not isinstance(queue, list) or any(not isinstance(item, dict) or type(item.get("sigma")) is not int
                                               or item["sigma"] not in SIGMA_VALUES for item in queue):
@@ -323,8 +334,13 @@
         entries = [item for item in queue if item["sigma"] == sigma]
         if len(entries) > 1:
             raise ValueError("강도 대기열 중복")
-        status = entries[0].get("status", "pending") if entries else "pending"
-        if status not in ("completed", "pending", "running", "interrupted", "failed") or not isinstance(status, str):
+        entry = entries[0] if entries else {}
+        status = entry.get("status", "pending")
+        privacy_status = entry.get("privacy_status", "pending")
+        if privacy_status not in ("pending", "running", "completed", "error"):
+            raise ValueError("점수 상태 형식 오류")
+        result["privacy_status"] = privacy_status
+        if status not in ("completed", "pending", "running", "interrupted", "failed", "error") or not isinstance(status, str):
             raise ValueError("강도 상태 형식 오류")
         def number(value, minimum=0, maximum=None, nullable=False, integer=False):
             # bool과 숫자 모양 문자열은 수치가 아닙니다. 정수는 화면의 정확한 표현 범위도 지킵니다.
@@ -345,20 +361,21 @@
             for row in history:
                 if not isinstance(row, dict) or type(row.get("sigma")) is not int or row["sigma"] not in SIGMA_VALUES:
                     raise ValueError("곡선 강도 오류")
-                if row["sigma"] != 0:
+                if row["sigma"] != sigma:
                     raise ValueError("곡선 강도 불일치")
                 if "run_id" in row and row["run_id"] != run_id:
                     raise ValueError("곡선 실행 불일치")
                 epoch = number(row.get("epoch"), minimum=1, integer=True)
                 if epoch != len(selected) + 1:
                     raise ValueError("곡선 회차 불일치")
-                public = {"sigma": 0, "epoch": epoch}
+                public = {"sigma": sigma, "epoch": epoch}
                 for key in ("train_loss", "val_loss", "learning_rate", "next_learning_rate"):
                     public[key] = number(row.get(key))
                 public["val_accuracy"] = number(row.get("val_accuracy"), maximum=1)
                 public["val_auc"] = number(row.get("val_auc"), maximum=1, nullable=True)
                 public["optimizer_steps"] = number(row.get("optimizer_steps"), integer=True)
-                public["early_stopping_wait"] = number(row.get("early_stopping_wait"), maximum=epoch, integer=True)
+                if "early_stopping_wait" in row:
+                    public["early_stopping_wait"] = number(row["early_stopping_wait"], maximum=epoch, integer=True)
                 if selected and public["optimizer_steps"] < selected[-1]["optimizer_steps"]:
                     raise ValueError("곡선 갱신 횟수 불일치")
                 selected.append(public)
@@ -377,15 +394,16 @@
                 raise ValueError("결과 크기 오류")
             return json.loads(payload.decode("utf-8"), parse_constant=reject_nonfinite)
 
-        training_complete = state.get("training_status") == "completed"
+        training_complete = entry.get("training_status") == "completed"
+        classification_complete = entry.get("classification_status") == "completed"
         if not training_complete:
-            # 학습 중에는 저장된 옛 지표가 있어도 모든 평가를 대기로 둡니다.
-            history = public_history(state.get("history", [])) if sigma == 0 else []
-            result.update(history=history, status="pending", message="블러 0에서 한 번 학습 중입니다. 100회 완료 후 고정 모델로 평가합니다.")
+            history = public_history(state.get("history", [])) if state.get("sigma") == sigma else []
+            result.update(history=history, status="running" if entry.get("training_status")=="running" else "pending",
+                          message="선택한 강도의 독립 학습 기록입니다. 분류 성적과 점수는 각각 계산이 끝난 뒤 표시합니다.")
             return result
-        if status == "completed":
+        if classification_complete:
             metrics = read_json(f"sigma_{sigma}_metrics.json")
-            validate_fixed_result(root, metrics, expected_run=run_id)
+            validate_result(root, metrics, expected_run=run_id)
             selection = metrics
             if type(metrics.get("sigma")) is not int or metrics["sigma"] != sigma:
                 raise ValueError("결과 강도 불일치")
@@ -398,10 +416,10 @@
                         "epochs_ran": number(metrics.get("epochs_ran"), minimum=100, maximum=100, integer=True),
                         "optimizer_steps": number(metrics.get("optimizer_steps"), integer=True),
                         "eval_optimizer_steps": number(metrics.get("eval_optimizer_steps"), minimum=0, maximum=0, integer=True),
-                        "training_sigma": 0, "checkpoint_sha256": selection["checkpoint_sha256"],
+                        "training_sigma": sigma, "checkpoint_sha256": selection["checkpoint_sha256"],
                         "model_state_sha256": selection["model_state_sha256"], "completed_at": stamp}
-            history = public_history(read_json("sigma_0_history.json")) if sigma == 0 else []
-            if sigma == 0 and (len(history) != 100 or history[-1]["optimizer_steps"] != selected["optimizer_steps"]):
+            history = public_history(read_json(f"sigma_{sigma}_history.json"))
+            if len(history) != 100 or history[-1]["optimizer_steps"] != selected["optimizer_steps"]:
                 raise ValueError("완료 결과와 학습 곡선 불일치")
             test = metrics.get("test")
             if not isinstance(test, dict):
@@ -430,18 +448,48 @@
                                       "loss": number(validation.get("loss")),
                                       "auc": number(validation.get("auc"), maximum=1, nullable=True),
                                       "n_images": number(validation.get("n_images"), minimum=1, integer=True)}
-            evaluation = [{"sigma": sigma, "evaluation": 1, "validation_loss": selected["validation"]["loss"],
-                           "test_loss": selected["test"]["loss"], "validation_accuracy": selected["validation"]["accuracy"],
-                           "test_accuracy": selected["test"]["accuracy"]}]
-            result.update(history=history, evaluation_history=evaluation, metrics=selected, status="completed",
-                          message="블러 0에서 고른 같은 모델의 평가입니다. 이 강도에서는 추가로 학습하지 않았습니다.")
+            result.update(history=history, metrics=selected, status="running",
+                          message="이 강도의 100회 독립 학습과 분류 평가를 마쳤습니다. 원본 찾기·복원 저항 점수 계산 상태를 확인하세요.")
+            if privacy_status == "completed":
+                try:
+                    privacy = read_json(f"sigma_{sigma}_privacy.json")
+                    validate_privacy_result(root, privacy, expected_run=run_id)
+                    if type(privacy.get("sigma")) is not int or privacy["sigma"] != sigma:
+                        raise ValueError("점수 강도 불일치")
+                    public = {"score_version": "gallery-residual-v1"}
+                    for key, maximum in (("score",100),("T_attack",1),("T_prior",1),("fractional_top1",1),("raw_ratio",None)):
+                        public[key] = number(privacy.get(key), maximum=maximum)
+                    for key in ("G", "n_queries", "original_test_images", "exact_return_groups", "target_in_tie_groups"):
+                        public[key] = number(privacy.get(key), integer=True, minimum=2 if key=="G" else 0)
+                    if public["n_queries"] != public["G"] or public["exact_return_groups"] > public["G"] or public["target_in_tie_groups"] > public["G"]:
+                        raise ValueError("점수 그룹 분모 불일치")
+                    for key in ("residual_quantiles", "tie_histogram"):
+                        values=privacy.get(key)
+                        if not isinstance(values,dict) or len(values)>10000:
+                            raise ValueError("점수 분포 형식 오류")
+                        allowed={"0","0.25","0.5","0.75","1"} if key=="residual_quantiles" else {str(i)for i in range(1,public["G"]+1)}
+                        if any(k not in allowed for k in values):
+                            raise ValueError("점수 분포 항목 오류")
+                        public[key]={k:number(v,maximum=1 if key=="residual_quantiles" else public["G"],integer=key=="tie_histogram")for k,v in values.items()}
+                    controls=privacy.get("controls")
+                    if not isinstance(controls,dict) or controls.get("original_score")!=0 or controls.get("constant_score")!=100:
+                        raise ValueError("점수 대조군 오류")
+                    public["controls"]={"original_score":0,"constant_score":100}
+                    result.update(privacy=public, status="completed", message="선택한 강도의 분류 성적과 실제 원본 후보 공격 점수 계산을 마쳤습니다.")
+                except (FileNotFoundError,OSError,ValueError,TypeError,KeyError,AttributeError):
+                    result.update(privacy=None,privacy_status="error",status="error",message="분류 결과는 확인했지만 점수 파일의 실행·모델·원값 연결을 확인할 수 없습니다. 오류 원문을 보존하고 복구를 기다립니다.")
+            elif privacy_status == "error":
+                result.update(status="error",message="이 강도의 분류 결과는 보존됐습니다. 점수 계산 오류를 복구한 뒤 다시 계산합니다.")
         else:
-            load_selection(root, run_id)
-            result.update(status=status, message="모델은 고정되었습니다. 선택한 강도의 추가 학습 없이 평가 결과를 기다리고 있습니다.")
+            load_selection(root, run_id, sigma)
+            history=public_history(read_json(f"sigma_{sigma}_history.json"))
+            if len(history)!=100:
+                raise ValueError("완료 학습 회차 누락")
+            result.update(history=history,status="running",message="이 강도의 독립 학습을 마쳤습니다. 분류 평가와 점수 계산을 기다립니다.")
     except FileNotFoundError:
-        result.update(history=[], evaluation_history=[], metrics=None, message="현재 실행의 고정 모델 또는 평가 파일을 기다리고 있습니다.")
+        result.update(history=[], evaluation_history=[], metrics=None, message="현재 실행의 해당 강도 모델 또는 평가 파일을 기다리고 있습니다.")
     except (OSError, ValueError, TypeError, AttributeError, KeyError):
-        result.update(history=[], evaluation_history=[], metrics=None, status="unavailable", message="실행·소스·고정 모델과 결과 기록의 일치를 확인할 수 없습니다.")
+        result.update(history=[], evaluation_history=[], metrics=None, status="unavailable", message="실행·소스·해당 강도 모델과 결과 기록의 일치를 확인할 수 없습니다.")
     return result
 
 
````

## docs/UI_화면_계약.md

| 구분 | 이전 | 이후 |
| --- | --- | --- |
| 상태 | 추가 | 추가 |
| 바이트 | 0 | 4117 |
| SHA-256 | 없음 | 7dbe19130d17a71f6614480a44eede250d5f044658af88511a14eae1607c19ce |

````diff
--- a/docs/UI_화면_계약.md
+++ b/docs/UI_화면_계약.md
@@ -0,0 +1,35 @@
+# 8차 화면과 결과 연결 계약
+
+화면 제목은 **폐 CT 강도별 학습과 복원 저항 실험 · 8차**입니다. 기존7차의 단일 모델 실험과 서버를 수정하지 않고 별도 차수에 구현했습니다.
+
+| 선택한 강도의 단계 | 화면에 표시할 값 | 완료 경계 |
+|---|---|---|
+| 새100회 학습 중 | 해당 강도의 학습·검증 곡선, 실제 회차·학습률 | 다른 강도의 기록을 곡선이나 수치로 대신 표시하지 않음 |
+| 분류 평가 완료·점수 대기 | 분류 정확도·정답수/시험분모·AUC·손실 | 점수는 미측정이며 강도 전체가 완료된 것으로 표시하지 않음 |
+| 원본 후보 공격·점수 완료 | 정확도와100점 점수, 각 원값·분모·분포 | 두 결과와 선정 체크포인트·입력·소스가 검증된 뒤 완료 |
+| 점수 계산 또는 결합 오류 | 확인된 분류 성적과 명시적 점수 오류 | 빈 점수를0이나100으로 채우지 않음 |
+
+강도0·1·2·4·8·16·32·64·128·256은 같은 로컬 초기 가중치에서 각각 새로 학습합니다. 각 강도의100회 학습 뒤 최저 raw validation loss 모델을 선정하고 분류와 점수를 측정합니다. 시험 수치로 모델이나 강도를 선정하지 않습니다. 같은 첫 합성곱과 같은 강도는 후단 학습이 달라도 같은 특징을 만들 수 있습니다.
+
+## 점수 읽기
+
+**분류 정확도**와 **원본 찾기·복원 저항 점수(100점)**를 나란히 표시합니다. 점수는 정해진 원본 후보 공격에서 측정한 연구용 값이며, 높을수록 이 공격에서 되찾기 어렵다는 뜻입니다. gallery-residual-v1을 사용합니다. 공격자는 원영상 후보 모음과 인코더·블러·전처리를 알고 있으며, 정확 특징 바이트 사전 공격을 포함합니다. gallery가 없는 복원이나 환자 재식별 방어로 확대하지 않습니다.
+
+요약은 소수 첫째 자리 반올림이며 저장 원값을 바꾸지 않습니다. 실측0점은0.0/100으로 표시하고 대기·오류와 구분합니다. 정확도의 원비율·정답수/분모와 점수 원값·G·T_attack·T_prior·동점 분할 원본 찾기 비율·정확 반환 그룹수·잔여 분포를 펼쳐 확인합니다. 시험 영상 수와 픽셀 구별 그룹 수는 다른 분모입니다. 표준 지표·보호 확률·차등 프라이버시 보장을 뜻하지 않으며 문헌상 신규성·독창성은 검증되지 않았습니다.
+
+## 조회와 인증 경계
+
+| 조회 | 읽는 검증 자료 | 공개 응답에서 제외 |
+|---|---|---|
+| 상태 | 현재8차 runtime 상태와 현재 소스의 실행 식별자 | 원본 경로·운영 오류 원문·인증값 |
+| 강도 결과 | 해당 강도의 history/selection/metrics/privacy, 체크포인트와 입력·소스 연결 | 원영상별 목록·예측CSV·그룹별 원자료 경로 |
+| 전체 그림 목록 | 완료 강도마다18장, 총180장 index와 각 강도의 모델·분류·점수 | 실제 원본 경로 |
+| 그림 한 장 | 공통 index/소스/실행과 요청 강도의18장 묶음·대상 PNG SHA | 무관한 다른 강도의 파일, 임의 경로 |
+
+기존 루프백Host 검사·세션 cookie의 HttpOnly/SameSite=Strict·고정 asset allowlist·읽기 전용 경로·응답 no-store·CSP를 유지합니다. 요청 간 검증 캐시는 사용하지 않습니다. 학습 서버나 실제 연구 결과를 이 화면 검사에서 기동·생성하지 않습니다.
+
+## 화면 검증 범위
+
+실측0점·강도 변경 시 곡선/정확도/점수의 종속 전환·새 실행 시 이전 결과 제거는 Node VM의 실제 app.js 실행으로 검사합니다. HTTP API는 합성 파일과 임시 루프백 서버로 인증·입력·모델·점수·PNG 변조 경계를 검사합니다. 라이트/다크·모션 제어와 나눔고딕 Bold700을 유지합니다.
+
+실제 브라우저 화면·hover/focus·작은 화면 렌더링은 미검증이며 Node/API 검사로 정상이라고 확대하지 않습니다. 합성 검사는 실제 CT 공격 결과나 학습 완료가 아닙니다.
````

## run_training.py

| 구분 | 이전 | 이후 |
| --- | --- | --- |
| 상태 | 수정 | 수정 |
| 바이트 | 7255 | 7302 |
| SHA-256 | 1a2d94b5d575e2798ba1b98f66bfaa117f4a0de31b3dea7d734f7a68b40f186f | 92603ec8501f2737e4e96028c61022affb911b21aa77497fe91321930872780f |

````diff
--- a/run_training.py
+++ b/run_training.py
@@ -1,4 +1,4 @@
-"""새 단일 σ0 실험을 준비하고 비연구 GPU 연결 검사를 수행합니다."""
+"""강도별 독립 학습 실험을 준비하고 비연구 GPU 연결 검사를 수행합니다."""
 
 import argparse
 from datetime import datetime
@@ -31,13 +31,13 @@
         if not pristine:
             raise RuntimeError("현재 실행이 이미 진행됐거나 준비 대기 상태가 아니어서 준비·연결 검사를 거부합니다.")
     if list((root / "work/checkpoints").glob("run_*/*.pt")):
-        raise RuntimeError("7차 학습 체크포인트가 있어 준비·연결 검사를 거부합니다.")
+            raise RuntimeError("8차 학습 체크포인트가 있어 준비·연결 검사를 거부합니다.")
     for directory in (root / "work/results").glob("run_*"):
-        if list(directory.glob("sigma_*_metrics.json")) or (directory / "fixed_model_selection.json").exists():
-            raise RuntimeError("7차 선정·평가 이력이 있어 준비·연결 검사를 거부합니다.")
+        if list(directory.glob("sigma_*_metrics.json")) or list(directory.glob("sigma_*_selection.json")) or list(directory.glob("sigma_*_privacy.json")):
+            raise RuntimeError("8차 선정·평가 이력이 있어 준비·연결 검사를 거부합니다.")
         for path in directory.glob("sigma_*_history.json"):
             if json.loads(path.read_text(encoding="utf-8-sig")):
-                raise RuntimeError("7차 학습 이력이 있어 준비·연결 검사를 거부합니다.")
+                raise RuntimeError("8차 학습 이력이 있어 준비·연결 검사를 거부합니다.")
 
 
 def prepare(config):
@@ -49,14 +49,14 @@
     validate_config(config)
     manifest = prepare_dataset(config, ROOT)
     run_id, settings = _run_identity(ROOT, config, manifest["manifest_sha256"])
-    metadata = {**settings, "run_id": run_id, "protocol": PROTOCOL, "protocol_fixed_model": True,
-                "training_sigma": 0, "prepared_at": now_kst(), "started_at": None}
+    metadata = {**settings, "run_id": run_id, "protocol": PROTOCOL, "protocol_fixed_model": False,
+                "prepared_at": now_kst(), "started_at": None}
     path = ROOT / "work/results" / ("run_" + run_id) / "run_metadata.json"
     if not path.exists():
         atomic_json(path, metadata)
     state = StatusWriter(ROOT, config)
     state.update(run_id=run_id, phase="preparing", stage="ready", status="ready", pid=None,
-                 dataset=manifest["summary"], message="σ0 새100회 학습 준비 완료 · 블러 평가는 모두 대기")
+                 dataset=manifest["summary"], message="강도별 새100회 독립 학습 준비 완료 · 분류·점수 모두 대기")
     frozen = freeze_inputs(ROOT, run_id)
     print(json.dumps({"command": "prepare", **frozen, "split_sizes": {k: len(v) for k, v in manifest["splits"].items()}}, ensure_ascii=False), flush=True)
 
````

## src/identity.py

| 구분 | 이전 | 이후 |
| --- | --- | --- |
| 상태 | 수정 | 수정 |
| 바이트 | 8048 | 15545 |
| SHA-256 | ed56829031ab0050271bb50ac1411185af5e661d8a9795e1035470171251cdab | 43ad87867bd08d93363da9d45b06f6f2e37e384693f2d1964cc159129e146e74 |

````diff
--- a/src/identity.py
+++ b/src/identity.py
@@ -4,7 +4,8 @@
 import json
 from pathlib import Path
 
-PROTOCOL = "fixed-model-sigma0-v1"
+PROTOCOL = "independent-sigma-privacy-v1"
+SCORE_VERSION = "gallery-residual-v1"
 SIGMAS = [0, 1, 2, 4, 8, 16, 32, 64, 128, 256]
 
 
@@ -36,11 +37,12 @@
 
 
 def validate_config(config):
-    if (config.get("protocol") != PROTOCOL or config.get("protocol_fixed_model") is not True
-            or type(config.get("training_sigma")) is not int or config["training_sigma"] != 0
+    if (config.get("protocol") != PROTOCOL or config.get("protocol_fixed_model") is not False
             or config.get("sigmas") != SIGMAS or type(config.get("epochs")) is not int or config["epochs"] != 100
             or config.get("early_stopping_enabled") is not False):
-        raise ValueError("σ0 단일 학습·100회·고정 모델10평가 프로토콜과 다릅니다.")
+        raise ValueError("강도별 독립100회 학습·프라이버시 평가 프로토콜과 다릅니다.")
+    if config.get("score_version") != SCORE_VERSION:
+        raise ValueError("고정한 프라이버시 산식 버전과 다릅니다.")
     for key, expected in [("image_size", 512), ("batch_size", 8), ("samples_per_class", 5000), ("seed", 42)]:
         if type(config.get(key)) is not int or config[key] != expected:
             raise ValueError("고정한 실험 조건과 다릅니다: " + key)
@@ -58,9 +60,24 @@
     return run_id, settings
 
 
+def readonly_input(root, config, key):
+    """명시적으로 고정한 두 개의 외부 읽기 전용 입력만 허용합니다."""
+    path = Path(config[key])
+    if not path.is_absolute():
+        return safe_path(root, path)
+    allowed = {"expected_reference_manifest": Path(root).parent / "7차/work/reference/dataset_manifest_private.json",
+               "initial_weights_path": Path(root).parent / "7차/work/torch-cache/hub/checkpoints/resnet50-0676ba61.pth"}
+    expected = allowed.get(key)
+    if expected is None or path.absolute() != expected.absolute():
+        raise ValueError("명시한 읽기 전용 이전 차수 입력 경로가 아닙니다.")
+    for part in [path, *path.parents]:
+        if part.is_symlink() or (hasattr(part, "is_junction") and part.is_junction()):
+            raise ValueError("읽기 전용 입력의 폴더 연결은 허용하지 않습니다.")
+    return path
+
+
 def validate_manifest(root, config, manifest):
-    path = Path(config["expected_reference_manifest"])
-    path = safe_path(root, path)
+    path = readonly_input(root, config, "expected_reference_manifest")
     if path.is_symlink() or file_sha256(path) != config["expected_reference_manifest_sha256"]:
         raise ValueError("최초 참조 manifest 파일 SHA와 다릅니다.")
     reference = read_json(path)
@@ -84,23 +101,25 @@
     metadata = read_json(safe_path(root, Path("work/results") / ("run_" + run_id) / "run_metadata.json"))
     if actual != run_id or metadata.get("run_id") != run_id or any(metadata.get(key) != value for key, value in settings.items()):
         raise ValueError("현재 소스·설정·분할·metadata의 실행 식별자가 다릅니다.")
-    if (metadata.get("protocol") != PROTOCOL or type(metadata.get("training_sigma")) is not int
-            or metadata.get("training_sigma") != 0 or metadata.get("protocol_fixed_model") is not True):
-        raise ValueError("현재 metadata가 단일 고정 모델 실험이 아닙니다.")
+    if metadata.get("protocol") != PROTOCOL or metadata.get("protocol_fixed_model") is not False:
+        raise ValueError("현재 metadata가 강도별 독립 모델 실험이 아닙니다.")
     return metadata
 
 
-def load_selection(root, run_id):
+def load_selection(root, run_id, sigma):
     root = Path(root).resolve()
-    validate_run(root, run_id)
-    selection = read_json(safe_path(root, Path("work/results") / ("run_" + run_id) / "fixed_model_selection.json"))
+    metadata = validate_run(root, run_id)
+    if type(sigma) is not int or sigma not in SIGMAS:
+        raise ValueError("선정 모델의 강도가 유효하지 않습니다.")
+    selection = read_json(safe_path(root, Path("work/results") / ("run_" + run_id) / f"sigma_{sigma}_selection.json"))
     if (selection.get("run_id") != run_id or selection.get("protocol") != PROTOCOL
-            or selection.get("protocol_fixed_model") is not True or type(selection.get("training_sigma")) is not int or selection.get("training_sigma") != 0
+            or selection.get("protocol_fixed_model") is not False or type(selection.get("training_sigma")) is not int or selection.get("training_sigma") != sigma
+            or type(selection.get("sigma")) is not int or selection.get("sigma") != sigma
             or type(selection.get("epochs_ran")) is not int or selection.get("epochs_ran") != 100 or type(selection.get("best_epoch")) is not int
             or not 1 <= selection["best_epoch"] <= 100 or type(selection.get("checkpoint_epoch")) is not int
             or selection.get("checkpoint_epoch") != selection["best_epoch"]):
-        raise ValueError("100회 완료 뒤의 단일 선정 모델 identity가 유효하지 않습니다.")
-    expected_path = f"work/checkpoints/run_{run_id}/sigma_0_best.pt"
+        raise ValueError("100회 완료 뒤 강도별 선정 모델 식별자가 유효하지 않습니다.")
+    expected_path = f"work/checkpoints/run_{run_id}/sigma_{sigma}_best.pt"
     if selection.get("selected_checkpoint") != expected_path:
         raise ValueError("선정 체크포인트가 현재 실행의 σ0 best가 아닙니다.")
     for key in ["checkpoint_sha256", "model_state_sha256"]:
@@ -109,20 +128,30 @@
             raise ValueError("고정 모델 SHA 형식이 유효하지 않습니다.")
     if file_sha256(safe_path(root, expected_path)) != selection["checkpoint_sha256"]:
         raise ValueError("선정 후 best 체크포인트 파일이 변경됐습니다.")
+    for key, value in result_binding(root, metadata).items():
+        if selection.get(key) != value:
+            raise ValueError("선정 모델의 소스·원본 분할 결합이 다릅니다: " + key)
     return selection
 
 
-def validate_fixed_result(root, result, expected_run=None):
+def result_binding(root, metadata):
+    return {"source_manifest_sha256": file_sha256(safe_path(root, "work/results/dataset_manifest_private.json")),
+            "manifest_records_sha256": metadata["manifest_sha256"],
+            "source_hashes_sha256": hashlib.sha256(json.dumps(metadata["source_hashes"], sort_keys=True).encode()).hexdigest()}
+
+
+def _result_identity(root, result, expected_run=None):
     run_id = result.get("run_id")
     if expected_run is not None and expected_run != run_id:
         raise ValueError("평가 결과가 현재 실행과 다릅니다.")
-    selection = load_selection(root, run_id)
+    selection = load_selection(root, run_id, result.get("sigma"))
     for key in ["run_id", "protocol", "protocol_fixed_model", "training_sigma", "best_epoch", "checkpoint_epoch",
-                "checkpoint_sha256", "model_state_sha256", "selected_checkpoint", "epochs_ran"]:
+                "checkpoint_sha256", "model_state_sha256", "selected_checkpoint", "epochs_ran",
+                "source_manifest_sha256", "manifest_records_sha256", "source_hashes_sha256"]:
         if type(result.get(key)) is not type(selection[key]) or result.get(key) != selection[key]:
             raise ValueError("평가가 동일한 선정 모델을 사용하지 않았습니다: " + key)
-    if (type(result.get("sigma")) not in {int, float} or result["sigma"] not in SIGMAS
-            or result.get("evaluation_sigma") != result["sigma"] or type(result.get("eval_optimizer_steps")) is not int
+    if (type(result.get("sigma")) is not int or result["sigma"] not in SIGMAS
+            or type(result.get("evaluation_sigma")) is not int or result.get("evaluation_sigma") != result["sigma"] or type(result.get("eval_optimizer_steps")) is not int
             or result["eval_optimizer_steps"] != 0 or not result.get("completed_at")):
         raise ValueError("고정 모델의 블러 평가 조건·완료 근거가 유효하지 않습니다.")
     for name in ["validation", "test"]:
@@ -130,4 +159,79 @@
         item = result.get("prediction_files", {}).get(name)
         if not isinstance(item, dict) or item.get("relative_path") != expected or file_sha256(safe_path(root, expected)) != item.get("sha256"):
             raise ValueError("고정 평가의 예측 CSV 연결 또는 SHA가 다릅니다.")
+    return selection
+
+
+def validate_result(root, result, expected_run=None):
+    _result_identity(root, result, expected_run)
     return result
+
+
+def validate_privacy_result(root, result, expected_run=None):
+    import math
+    selection = load_selection(root, result.get("run_id"), result.get("sigma"))
+    if expected_run is not None and result.get("run_id") != expected_run:
+        raise ValueError("점수 실행 식별자가 다릅니다.")
+    for key, value in selection.items():
+        if type(result.get(key)) is not type(value) or result.get(key) != value:
+            raise ValueError("점수와 강도별 선정 모델 연결이 다릅니다: " + key)
+    for key in ["score", "T_attack", "T_prior", "fractional_top1"]:
+        if type(result.get(key)) not in {int, float} or not math.isfinite(result[key]):
+            raise ValueError("점수 집계가 유한한 숫자가 아닙니다.")
+    if (result.get("score_version") != SCORE_VERSION or not 0 <= result["score"] <= 100
+            or type(result.get("G")) is not int or result["G"] < 2 or result.get("n_queries") != result["G"]
+            or not 0 < result["T_prior"] < 1 or not 0 <= result["T_attack"] <= 1
+            or not 0 <= result["fractional_top1"] <= 1 or not result.get("completed_at")
+            or abs(result["score"] - 100 * min(1, max(0, result["T_attack"] / result["T_prior"]))) > 1e-10):
+        raise ValueError("점수의 범위·분모·수식·완료 근거가 다릅니다.")
+    expected = f"work/results/run_{result['run_id']}/sigma_{result['sigma']}_privacy_groups_private.json"
+    item = result.get("raw_file", {})
+    if item.get("relative_path") != expected or file_sha256(safe_path(root, expected)) != item.get("sha256"):
+        raise ValueError("점수 그룹별 원값 파일 연결 또는 SHA가 다릅니다.")
+    raw = read_json(safe_path(root, expected))
+    metadata = validate_run(root, result["run_id"])
+    pipeline = raw.get("pipeline", {})
+    for key, value in {"protocol": PROTOCOL, "sigma": result["sigma"], "checkpoint_sha256": result["checkpoint_sha256"],
+                       "model_state_sha256": result["model_state_sha256"], "source_hashes": metadata["source_hashes"],
+                       "manifest_sha256": metadata["manifest_sha256"], "precision": "fp32", "packet_batch_size": 1,
+                       "shape_dtype_byteorder_in_hash": True, "encoder_state_sha256": result.get("encoder_state_sha256")}.items():
+        if type(pipeline.get(key)) is not type(value) or pipeline.get(key) != value:
+            raise ValueError("공격 파이프라인의 실제 입력·소스 연결이 다릅니다: " + key)
+    if (result.get("privacy_source_sha256") != metadata["source_hashes"].get("src/privacy.py")
+            or result.get("attack_protocol") != "known-encoder-closed-gallery-full-feature-bytehash-v1"
+            or result.get("precision") != "fp32" or type(result.get("packet_batch_size")) is not int or result["packet_batch_size"] != 1
+            or result.get("device") != pipeline.get("device")
+            or result.get("pipeline_sha256") != hashlib.sha256(json.dumps(pipeline, sort_keys=True).encode()).hexdigest()
+            or result.get("controls") != {"original_score": 0., "constant_score": 100.}):
+        raise ValueError("공격 설정·정밀도·소스·대조군 연결이 다릅니다.")
+    encoder = result.get("encoder_state_sha256")
+    if not isinstance(encoder, str) or len(encoder) != 64 or any(c not in "0123456789abcdef" for c in encoder):
+        raise ValueError("전송 encoder state SHA가 유효하지 않습니다.")
+    d, rows, g = raw.get("distance_matrix"), raw.get("per_group"), result["G"]
+    gallery, query = raw.get("gallery_feature_hashes"), raw.get("query_feature_hashes")
+    if (not isinstance(d, list) or len(d) != g or not isinstance(rows, list) or len(rows) != g
+            or not isinstance(gallery, list) or len(gallery) != g or not isinstance(query, list) or len(query) != g):
+        raise ValueError("점수 원값의 후보·쿼리·거리 개수가 다릅니다.")
+    attack_values, prior_values, correct = [], [], []
+    for i in range(g):
+        if (not isinstance(d[i], list) or len(d[i]) != g
+                or any(type(v) not in {int, float} or not math.isfinite(v) or v < 0 for v in d[i])
+                or d[i][i] != 0 or any(d[i][j] <= 0 for j in range(g) if j != i)):
+            raise ValueError("점수 원값의 실제 거리·자기 거리·그룹 구분이 다릅니다.")
+        choices = [j for j, h in enumerate(gallery) if h == query[i]]
+        if not choices or rows[i].get("candidates") != choices:
+            raise ValueError("점수 원값의 별도 쿼리와 사전 후보가 일치하지 않습니다.")
+        b = sum(d[i])/g
+        t = [min(1., max(0., v/b)) for v in d[i]]
+        a, p = sum(t[j] for j in choices)/len(choices), sum(t)/g
+        for key, expected_value in {"b_i": b, "attack_residual": a, "prior_residual": p}.items():
+            if not math.isclose(rows[i].get(key, -1), expected_value, rel_tol=1e-12, abs_tol=1e-14):
+                raise ValueError("그룹별 점수 원값 재집계가 다릅니다: " + key)
+        attack_values.append(a)
+        prior_values.append(p)
+        correct.append(1/len(choices) if i in choices else 0.)
+    for key, expected_value in {"T_attack": sum(attack_values)/g, "T_prior": sum(prior_values)/g,
+                                "fractional_top1": sum(correct)/g}.items():
+        if not math.isclose(result[key], expected_value, rel_tol=1e-12, abs_tol=1e-14):
+            raise ValueError("점수 집계와 원값 재계산이 다릅니다: " + key)
+    return result
````

## src/model.py

| 구분 | 이전 | 이후 |
| --- | --- | --- |
| 상태 | 수정 | 수정 |
| 바이트 | 5840 | 6009 |
| SHA-256 | 24ceaa031eb79f87157bc50c2a05c1121f7d51d2356cc848f23e0c0d01c08972 | 668ea4afbcbdff767f328bdd490ffd6d3ebbff0352ffa07cf25972dfc1ae396b |

````diff
--- a/src/model.py
+++ b/src/model.py
@@ -14,7 +14,7 @@
     """명시적으로 금지한 외부 가중치 다운로드 시도는 실행 전에 오류로 기록합니다."""
     def reject(*args, **kwargs):
         DOWNLOAD_ATTEMPTS.append({"args": repr(args), "kwargs": repr(kwargs)})
-        raise RuntimeError("7차 실험은 로컬 고정 가중치만 허용합니다.")
+        raise RuntimeError("8차 실험은 로컬 고정 가중치만 허용합니다.")
     torch.hub.download_url_to_file = reject
 
 
@@ -120,9 +120,12 @@
                 module.eval()
         return self
 
-    def forward(self, images):
+    def transmitted_features(self, images):
+        """분류와 공격에서 실제 전송되는 동일한 전처리·conv1·블러 경로입니다."""
         with torch.no_grad():
             normalized = (images - self.rgb_mean) / self.rgb_std
             features = self.edge(normalized)
-            transmitted = self.blur(features)
-        return self.cloud(transmitted)
+            return self.blur(features)
+
+    def forward(self, images):
+        return self.cloud(self.transmitted_features(images))
````

## src/privacy.py

| 구분 | 이전 | 이후 |
| --- | --- | --- |
| 상태 | 추가 | 추가 |
| 바이트 | 0 | 12234 |
| SHA-256 | 없음 | ef1b98ed5d9638dea0db526e5c750a5fd5d2d9883b0daf5ae9fcb34f20f124e0 |

````diff
--- a/src/privacy.py
+++ b/src/privacy.py
@@ -0,0 +1,193 @@
+"""원본 후보가 있는 알려진 encoder 공격과 조건부 복원 저항 점수를 계산합니다."""
+
+from collections import Counter
+import hashlib
+import json
+from pathlib import Path
+import sys
+
+import numpy as np
+import torch
+
+from .data import CTDataset
+from .identity import SCORE_VERSION, file_sha256, safe_path, validate_run
+from .model import GaussianDCTBlur
+from .state import atomic_json, now_kst
+
+
+def group_pixels(pixels):
+    """거리 계산에 실제 쓰는 float32 회색조 표현의 동일 바이트만 묶습니다."""
+    x = np.asarray(pixels)
+    if x.ndim < 2 or x.dtype != np.float32 or not np.isfinite(x).all():
+        raise ValueError("그룹 입력은 유한한 float32 영상 집합이어야 합니다.")
+    known, representatives, groups = {}, [], []
+    for index, image in enumerate(x):
+        key = hashlib.sha256(json.dumps(list(image.shape)).encode() + np.ascontiguousarray(image).tobytes()).hexdigest()
+        if key not in known:
+            known[key] = len(groups)
+            representatives.append(index)
+            groups.append([])
+        groups[known[key]].append(index)
+    return representatives, groups
+
+
+def pairwise_mse(pixels):
+    """float64 직접 차이로 계산하며 Gram 차분의 상쇄를 피합니다."""
+    x = np.asarray(pixels, dtype=np.float64).reshape(len(pixels), -1)
+    if x.shape[1] == 0 or not np.isfinite(x).all():
+        raise ValueError("거리 입력에 빈 영상 또는 비유한 값이 있습니다.")
+    result = np.zeros((len(x), len(x)), dtype=np.float64)
+    for i in range(len(x)):
+        for start in range(i + 1, len(x), 8):
+            end = min(len(x), start + 8)
+            delta = x[start:end] - x[i]
+            values = np.einsum("ij,ij->i", delta, delta) / x.shape[1]
+            result[i, start:end] = values
+            result[start:end, i] = values
+    return result
+
+
+def match_hashes(gallery_hashes, query_hashes):
+    dictionary = {}
+    for index, value in enumerate(gallery_hashes):
+        dictionary.setdefault(value, []).append(index)
+    matches = []
+    for value in query_hashes:
+        if value not in dictionary:
+            raise ValueError("별도 쿼리 특징 바이트가 후보 사전에 없습니다. 재현 실패를 전체 동점으로 대체하지 않습니다.")
+        matches.append(list(dictionary[value]))
+    return matches
+
+
+def feature_hash(tensor, pipeline_identity):
+    item = tensor.detach().cpu().contiguous()
+    if item.dtype != torch.float32 or not torch.isfinite(item).all():
+        raise ValueError("전송 특징은 유한한 FP32여야 합니다.")
+    header = {"shape": list(item.shape), "dtype": "float32", "byteorder": sys.byteorder,
+              "pipeline_identity": pipeline_identity}
+    return hashlib.sha256(json.dumps(header, sort_keys=True).encode() + item.numpy().tobytes()).hexdigest()
+
+
+def score_gallery(distances, candidates):
+    """같은 반환 후보의 잔여를 먼저 계산한 뒤 균등 동점·그룹 평균을 냅니다."""
+    d = np.asarray(distances, dtype=np.float64)
+    if (d.ndim != 2 or d.shape[0] != d.shape[1] or len(d) < 2 or not np.isfinite(d).all()
+            or np.any(d < 0) or not np.array_equal(d, d.T) or np.any(np.diag(d) != 0)):
+        raise ValueError("후보 거리 행렬의 크기·대칭·유한성·자기 거리가 유효하지 않습니다.")
+    g = len(d)
+    if np.any(d[~np.eye(g, dtype=bool)] <= 0):
+        raise ValueError("거리 표현에서 서로 다른 후보 그룹의 MSE가 양수여야 합니다.")
+    if len(candidates) != g:
+        raise ValueError("쿼리와 후보 반환 집합 수가 다릅니다.")
+    baseline = d.mean(axis=1)
+    if not np.isfinite(baseline).all() or np.any(baseline <= 0):
+        raise ValueError("특징 없는 균등 후보 반환의 기준 오차가 양수여야 합니다.")
+    t = np.clip(d / baseline[:, None], 0, 1)
+    np.fill_diagonal(t, 0)
+    rows = []
+    for i, choices in enumerate(candidates):
+        if (not choices or any(type(j) is not int or not 0 <= j < g for j in choices)
+                or len(choices) != len(set(choices))):
+            raise ValueError("공격 동점 후보가 비었거나 중복·범위 오류가 있습니다.")
+        rows.append({"group_index": i, "weight": 1/g, "candidates": choices, "tie_count": len(choices),
+                     "b_i": float(baseline[i]), "expected_mse": float(d[i, choices].mean()),
+                     "candidate_mse": d[i, choices].tolist(), "candidate_residual": t[i, choices].tolist(),
+                     "attack_residual": float(t[i, choices].mean()), "prior_residual": float(t[i].mean()),
+                     "fractional_top1": 1/len(choices) if i in choices else 0.,
+                     "target_in_tie": i in choices})
+    attack = float(np.mean([r["attack_residual"] for r in rows]))
+    prior = float(np.mean([r["prior_residual"] for r in rows]))
+    if not 1/g - 1e-14 <= prior <= (g-1)/g + 1e-14:
+        raise ValueError("특징 없는 기준 잔여의 증명된 범위를 벗어났습니다.")
+    residuals = np.array([r["attack_residual"] for r in rows])
+    ratio = attack/prior
+    # 고정 후보 집합에 대한 그룹 재표집 CI이며 환자·모집단 보안 보장이 아닙니다.
+    rng = np.random.default_rng(20261120)
+    indices = rng.integers(0, g, size=(2000, g))
+    priors = np.array([r["prior_residual"] for r in rows])
+    boot = 100 * np.clip(residuals[indices].mean(1)/priors[indices].mean(1), 0, 1)
+    return {"score_version": SCORE_VERSION, "score": float(100 * np.clip(ratio, 0, 1)),
+            "G": g, "n_queries": g, "T_attack": attack, "T_prior": prior, "raw_ratio": ratio,
+            "fractional_top1": float(np.mean([r["fractional_top1"] for r in rows])),
+            "fractional_correct_sum": float(sum(r["fractional_top1"] for r in rows)),
+            "exact_return_groups": sum(r["candidates"] == [r["group_index"]] for r in rows),
+            "target_in_tie_groups": sum(r["target_in_tie"] for r in rows),
+            "tie_histogram": dict(Counter(str(r["tie_count"]) for r in rows)),
+            "residual_quantiles": {str(q): float(np.quantile(residuals, q)) for q in [0, .25, .5, .75, 1]},
+            "score_ci95": np.quantile(boot, [.025, .975]).tolist(),
+            "ci_method": "고정 후보 집합의 영상 그룹 균등 bootstrap2000·seed20261120; 환자 CI 아님",
+            "per_group": rows}
+
+
+def run_privacy(model, records, root, run_id, selection, state=None):
+    """쿼리와 후보를 실제로 각각 정방향 계산하고 그 바이트 사전만 공격에 씁니다."""
+    from .training import tensor_state_digest
+    root = Path(root)
+    metadata = validate_run(root, run_id)
+    sigma = selection["sigma"]
+    device = next(model.parameters()).device
+    before = tensor_state_digest(model.state_dict())
+    if before != selection["model_state_sha256"] or any(m.training for m in model.modules()) or any(p.requires_grad for p in model.parameters()):
+        raise ValueError("공격 평가 모델이 선정 state·전체 eval·동결 조건과 다릅니다.")
+    dataset = CTDataset(records, image_size=512, training=False)
+    pixels = np.stack([dataset[i][0][0].numpy() for i in range(len(dataset))])
+    representatives, groups = group_pixels(pixels)
+    if len(groups) < 2:
+        raise ValueError("실제512픽셀 표현의 서로 다른 후보 그룹이2개 미만입니다.")
+    distances = pairwise_mse(pixels[representatives])
+    for row in records:
+        if file_sha256(row["path"]) != row["byte_sha256"]:
+            raise ValueError("공격 입력 원영상의 고정 바이트 SHA가 다릅니다.")
+    pipeline = {"protocol": selection["protocol"], "sigma": sigma, "checkpoint_sha256": selection["checkpoint_sha256"],
+                "model_state_sha256": before, "source_hashes": metadata["source_hashes"], "precision": "fp32",
+                "packet_batch_size": 1, "device": str(device), "torch_version": str(torch.__version__),
+                "shape_dtype_byteorder_in_hash": True, "manifest_sha256": metadata["manifest_sha256"]}
+    pipeline["encoder_state_sha256"] = tensor_state_digest(model.edge.state_dict())
+    pipeline_sha = hashlib.sha256(json.dumps(pipeline, sort_keys=True).encode()).hexdigest()
+    hashes = []
+    model.blur = GaussianDCTBlur(sigma).to(device).eval()
+    for pass_index in range(2):
+        current = []
+        with torch.inference_mode(), torch.autocast(device.type, enabled=False):
+            for group_index, original_index in enumerate(representatives):
+                image, _ = dataset[original_index]
+                transmitted = model.transmitted_features(image[None].to(device).float())
+                current.append(feature_hash(transmitted[0], pipeline_sha))
+                if state and (group_index == 0 or (group_index + 1) % 10 == 0):
+                    state.update(batch=group_index+1, batches=len(groups),
+                                 message=f"σ={sigma}: {'후보' if pass_index == 0 else '별도 쿼리'} 전송 특징 계산 {group_index+1}/{len(groups)}")
+        hashes.append(current)
+    matches = match_hashes(hashes[0], hashes[1])
+    measured = score_gallery(distances, matches)
+    positive = score_gallery(distances, [[i] for i in range(len(groups))])
+    negative = score_gallery(distances, [list(range(len(groups)))] * len(groups))
+    if positive["score"] != 0 or abs(negative["score"] - 100) > 1e-10:
+        raise ValueError("원본 반환·상수 특징 대조군의 점수 검사가 실패했습니다.")
+    if (tensor_state_digest(model.state_dict()) != before or any(m.training for m in model.modules())
+            or any(p.grad is not None for p in model.parameters())
+            or file_sha256(safe_path(root, selection["selected_checkpoint"])) != selection["checkpoint_sha256"]):
+        raise ValueError("공격 평가에서 선정 가중치·BN·기울기·체크포인트가 변했습니다.")
+    raw_path = root / f"work/results/run_{run_id}/sigma_{sigma}_privacy_groups_private.json"
+    raw = {"per_group": measured.pop("per_group"), "distance_matrix": distances.tolist(),
+           "representatives": representatives, "groups_original_indices": groups,
+           "group_member_relative_paths": [[records[j]["relative_path"] for j in group] for group in groups],
+           "gallery_feature_hashes": hashes[0], "query_feature_hashes": hashes[1], "pipeline": pipeline}
+    atomic_json(raw_path, raw)
+    value = {**selection, **measured, "completed_at": now_kst(), "original_test_images": len(records),
+             "controls": {"original_score": positive["score"], "constant_score": negative["score"]},
+             "controls_kind": "후보 집합을 주입한 산식 대조; 실제 특징 매칭 대조는 별도 회귀검사",
+             "raw_file": {"relative_path": raw_path.relative_to(root).as_posix(), "sha256": file_sha256(raw_path)},
+             "attack_protocol": "known-encoder-closed-gallery-full-feature-bytehash-v1",
+             "precision": "fp32", "packet_batch_size": 1, "device": str(device), "pipeline_sha256": pipeline_sha,
+             "grouping_rule": "gray512-bilinear-float32-div255-exact-bytes-uniform-representatives-v1",
+             "threat_model": "원영상 후보와 encoder·블러를 아는 공격자의 후보 반환 복원",
+             "source_manifest_sha256": file_sha256(root / "work/results/dataset_manifest_private.json"),
+             "manifest_records_sha256": metadata["manifest_sha256"],
+             "privacy_source_sha256": file_sha256(root / "src/privacy.py"),
+             "encoder_state_sha256": tensor_state_digest(model.edge.state_dict()),
+             "limitations": ["후보 원본이 있는 조건부 실험이며 후보 없는 복원 점수가 아닙니다.",
+                             "분류 FP32 batch8 패킷과 별개인 FP32 batch1 공격 패킷입니다.",
+                             "제안식의 독창성·표준성·DP·안전 확률·환자 재식별 방어는 미검증입니다.",
+                             "고정 conv1 특징은 후단 분류기 독립 학습으로 바뀌지 않습니다."]}
+    atomic_json(root / f"work/results/run_{run_id}/sigma_{sigma}_privacy.json", value)
+    return value
````

## src/state.py

| 구분 | 이전 | 이후 |
| --- | --- | --- |
| 상태 | 수정 | 수정 |
| 바이트 | 4883 | 5206 |
| SHA-256 | 0208dfa6c77737cd55996acec78eedf5fa80b9f65a82c9c36251af78a44c9da3 | edf688087b4cf48f8b87ce294918f5f99cc10e9b23fa1afa4266b51d10217c9b |

````diff
--- a/src/state.py
+++ b/src/state.py
@@ -60,8 +60,9 @@
         self.root = Path(root)
         self.folder = self.root / "work/runtime"
         self.folder.mkdir(parents=True, exist_ok=True)
-        self.data = {"schema_version": 2, "protocol": "fixed-model-sigma0-v1", "protocol_fixed_model": True,
-                     "phase": "preparing", "training_status": "pending", "training_sigma": 0,
+        self.data = {"schema_version": 3, "protocol": "independent-sigma-privacy-v1", "protocol_fixed_model": False,
+                     "phase": "preparing", "training_status": "pending", "training_sigma": None,
+                     "classification_status": "pending", "privacy_status": "pending", "privacy": None,
                      "eval_optimizer_steps": 0, "checkpoint_sha256": None, "model_state_sha256": None,
                      "selected_checkpoint": None, "evaluation_current_sigma": None,
                      "stage": "preparing", "status": "running", "message": "원본 자료 확인 중",
@@ -75,9 +76,11 @@
                      "batch": 0, "batches": 0, "seen_per_class": {"OK": 0, "NG": 0},
                      "history": [], "dataset": None, "evaluation": None, "device": None, "error": None,
                      "sigma": 0, "sigma_index": 1, "sigmas": config.get("sigmas", [0]),
-                     "sigma_queue": [{"sigma": sigma, "status": "pending", "result": None} for sigma in config.get("sigmas", [0])],
+                     "sigma_queue": [{"sigma": sigma, "status": "pending", "training_status": "pending",
+                                      "classification_status": "pending", "privacy_status": "pending",
+                                      "result": None, "privacy_result": None} for sigma in config.get("sigmas", [0])],
                      "limitations": ["환자 ID 없는 영상 단위 예비실험이며 임상 성능으로 해석할 수 없습니다.",
-                                     "원본의 7-fold 환자 교차검증·복원 공격·동일 영상 매칭은 이번 실행에 포함되지 않습니다."]}
+                                     "원본 후보가 있는 알려진 encoder 공격의 조건부 점수이며 DP·안전 확률·환자 재식별 방어가 아닙니다."]}
 
     def update(self, **values):
         self.data.update(values)
````

## src/training.py

| 구분 | 이전 | 이후 |
| --- | --- | --- |
| 상태 | 수정 | 수정 |
| 바이트 | 31770 | 32324 |
| SHA-256 | e62914465b0d8d83c2c4c38bbf2823d199e07bdaac54596d7b177702118d8af2 | 9edd197760ecab7fc0906374443c372eb612c3ebd741b9f62ee9b1b49c5e423d |

````diff
--- a/src/training.py
+++ b/src/training.py
@@ -1,4 +1,4 @@
-"""σ0 모델을100회 새 학습하고 선정 가중치를 고정해10개 블러를 평가합니다."""
+"""강도마다 새100회 독립 학습 뒤 해당 모델의 분류·후보 복원 점수를 계산합니다."""
 
 import csv
 import gc
@@ -43,6 +43,7 @@
             "specificity": float(tn / (tn + fp)) if tn + fp else None,
             "f1": float(f1_score(y, predicted, zero_division=0)),
             "confusion_matrix": matrix.tolist(), "threshold": 0.5, "n_images": len(y),
+            "n_correct": int(np.count_nonzero(predicted == y)),
             "unit": "image", "patient_id_available": False, "threshold_consistent": consistent,
             "threshold_rounding_differences": int(np.count_nonzero(predicted != (p >= 0.5).astype(int))),
             "ranking_score": "raw_logits" if logits is not None else "probability",
@@ -224,61 +225,30 @@
     os.replace(temporary, path)
 
 
-def _freeze_prefix_checkpoint(source, destination):
-    """기존 최저 검증 손실 파일을 RNG 사용 없이 한 번 고정하고 복사 해시를 확인합니다."""
-    source, destination = Path(source), Path(destination)
-    digest = hashlib.sha256(source.read_bytes()).hexdigest()
-    if destination.exists():
-        if hashlib.sha256(destination.read_bytes()).hexdigest() != digest:
-            raise ValueError("이미 고정된 관찰용 체크포인트를 교체할 수 없습니다.")
-        return digest
-    temporary = destination.with_suffix(".tmp")
-    try:
-        shutil.copyfile(source, temporary)
-        if hashlib.sha256(temporary.read_bytes()).hexdigest() != digest:
-            raise ValueError("관찰용 체크포인트 복사 해시가 다릅니다.")
-        os.replace(temporary, destination)
-    finally:
-        if temporary.exists():
-            temporary.unlink()
-    return digest
-
-
-def _check_prefix_hash(path, expected):
-    if (not isinstance(expected, str) or len(expected) != 64
-            or hashlib.sha256(Path(path).read_bytes()).hexdigest() != expected):
-        raise ValueError("고정된 관찰용 체크포인트 해시가 재개 기록과 다릅니다.")
-
-
-from .identity import (PROTOCOL, SIGMAS, _run_identity, file_sha256, validate_config,
-                       validate_run, validate_fixed_result, load_selection)
-from .model import GaussianDCTBlur
+from .identity import (PROTOCOL, SIGMAS, _run_identity, file_sha256, readonly_input,
+                       validate_config, validate_run, validate_result, validate_privacy_result, load_selection, result_binding)
+from .privacy import run_privacy
 
 
 def tensor_state_digest(state):
-    """이름·dtype·shape·모든 tensor 바이트를 결합하며 BN buffer도 포함합니다."""
+    """이름·dtype·shape와 BN buffer를 포함한 전체 tensor 바이트를 결합합니다."""
     value = hashlib.sha256()
     for name, tensor in sorted(state.items()):
         item = tensor.detach().cpu().contiguous()
-        value.update(json.dumps([name, str(item.dtype), list(item.shape)], ensure_ascii=False).encode("utf-8"))
+        value.update(json.dumps([name, str(item.dtype), list(item.shape)], ensure_ascii=False).encode())
         value.update(item.reshape(-1).view(torch.uint8).numpy().tobytes())
     return value.hexdigest()
 
 
-def checkpoint_load(path, run_id):
-    # 본 실행이 만든, 고정 폴더 안의 로컬 파일만 읽습니다.
+def checkpoint_load(path, run_id, sigma):
+    # 현재 실행이 만든 알려진 로컬 파일만 weights_only로 읽습니다.
     saved = torch.load(path, map_location="cpu", weights_only=True)
     if (saved.get("run_id") != run_id or saved.get("protocol") != PROTOCOL
-            or saved.get("protocol_fixed_model") is not True or saved.get("training_sigma") != 0
-            or saved.get("sigma") != 0 or type(saved.get("epoch")) is not int or not 1 <= saved["epoch"] <= 100):
-        raise ValueError("체크포인트의 단일 σ0 학습·실행 식별자가 다릅니다.")
+            or saved.get("protocol_fixed_model") is not False or type(saved.get("sigma")) is not int
+            or saved.get("sigma") != sigma or type(saved.get("training_sigma")) is not int or saved["training_sigma"] != sigma
+            or type(saved.get("epoch")) is not int or not 1 <= saved["epoch"] <= 100):
+        raise ValueError("체크포인트의 독립 학습 강도·실행 식별자가 다릅니다.")
     return saved
-
-
-def checkpoint_base(run_id, epoch, model, control, policy):
-    return {"run_id": run_id, "protocol": PROTOCOL, "protocol_fixed_model": True,
-            "training_sigma": 0, "sigma": 0, "epoch": epoch, "model": model.state_dict(),
-            "training_control": control.state_dict(), "training_policy": policy}
 
 
 def numpy_rng_state():
@@ -293,65 +263,50 @@
     np.random.set_state((item["name"], np.asarray(item["values"], dtype=np.uint32), item["position"], item["gaussian"], item["cached"]))
 
 
-def _save_fixed_predictions(path, records, labels, probabilities, logits, identity, sigma):
+def checkpoint_base(run_id, sigma, epoch, model, control, policy):
+    return {"run_id": run_id, "protocol": PROTOCOL, "protocol_fixed_model": False,
+            "training_sigma": sigma, "sigma": sigma, "epoch": epoch, "model": model.state_dict(),
+            "training_control": control.state_dict(), "training_policy": policy}
+
+
+def _save_bound_predictions(path, records, labels, probabilities, logits, selection):
     with Path(path).open("w", encoding="utf-8", newline="") as stream:
         writer = csv.writer(stream)
-        writer.writerow(["relative_path", "label", "ng_probability", "logit", "run_id", "training_sigma", "evaluation_sigma",
-                         "checkpoint_sha256", "model_state_sha256", "protocol_fixed_model"])
+        keys = ["run_id", "sigma", "training_sigma", "checkpoint_sha256", "model_state_sha256", "protocol_fixed_model"]
+        writer.writerow(["relative_path", "label", "ng_probability", "logit", *keys])
         for row, label, probability, logit in zip(records, labels, probabilities, logits):
-            writer.writerow([row["relative_path"], label, probability, logit, identity["run_id"], 0, sigma,
-                             identity["checkpoint_sha256"], identity["model_state_sha256"], True])
-
-
-def evaluate_frozen_sigmas(model, splits, loaders, device, root, run_id, selection, state, optimizer_steps):
-    """optimizer를 받거나 만들지 않고 하나의 선정 모델을10개의 입력 블러로 평가합니다."""
-    root = Path(root)
-    destination = root / "work/results" / ("run_" + run_id)
-    model.eval().requires_grad_(False)
-    expected_digest = selection["model_state_sha256"]
-    if tensor_state_digest(model.state_dict()) != expected_digest:
-        raise ValueError("평가 시작 모델이 동결 state와 다릅니다.")
-    values = []
-    for index, sigma in enumerate(SIGMAS):
-        path = destination / f"sigma_{sigma}_metrics.json"
-        entry = state.data["sigma_queue"][index]
-        if path.exists():
-            value = validate_fixed_result(root, json.loads(path.read_text(encoding="utf-8")), run_id)
-            entry.update(status="completed", result=path.relative_to(root).as_posix())
-            values.append(value)
-            continue
-        # sigma 속성만 변경하면 transfer 캐시가 남으므로 새 모듈로 교체합니다.
-        model.blur = GaussianDCTBlur(sigma).to(device)
-        if tensor_state_digest(model.state_dict()) != expected_digest or file_sha256(root / selection["selected_checkpoint"]) != selection["checkpoint_sha256"]:
-            raise ValueError("평가 조건 시작 전 고정 가중치 또는 체크포인트가 변경됐습니다.")
-        entry.update(status="running")
-        state.update(phase="evaluation", training_status="completed", stage="validation", status="running",
-                     sigma=sigma, sigma_index=index + 1, evaluation_current_sigma=sigma, eval_optimizer_steps=0,
-                     message=f"학습 완료 모델 고정 · 블러 σ={sigma} 평가 중")
-        validation, y_val, p_val, z_val = evaluate(model, loaders[0], device, None, state, return_logits=True)
-        test, y_test, p_test, z_test = evaluate(model, loaders[1], device, None, state, stage="testing", return_logits=True)
-        if (any(module.training for module in model.modules()) or any(p.grad is not None for p in model.parameters())
-                or tensor_state_digest(model.state_dict()) != expected_digest
-                or file_sha256(root / selection["selected_checkpoint"]) != selection["checkpoint_sha256"]):
-            raise ValueError("고정 평가에서 학습 상태·기울기·가중치 또는 BN buffer가 변했습니다.")
-        prediction_files = {}
-        for name, labels, probabilities, logits in [("validation", y_val, p_val, z_val), ("test", y_test, p_test, z_test)]:
-            output = destination / f"sigma_{sigma}_{name}_predictions_private.csv"
-            _save_fixed_predictions(output, splits[name], labels, probabilities, logits, selection, sigma)
-            prediction_files[name] = {"relative_path": output.relative_to(root).as_posix(), "sha256": file_sha256(output)}
-        value = {**selection, "sigma": sigma, "evaluation_sigma": sigma, "eval_optimizer_steps": 0,
-                 "optimizer_steps": optimizer_steps, "validation": validation, "test": test,
-                 "prediction_files": prediction_files, "completed_at": now_kst(), "selected_checkpoint_policy": "σ0 검증 원시 손실 최저 모델",
-                 "test_use": "동일 시험셋 탐색적 비교; 시험 결과로 모델·σ·임계값을 선택하지 않습니다.",
-                 "state_digest_before": expected_digest, "state_digest_after": tensor_state_digest(model.state_dict()),
-                 "checkpoint_sha256_before": selection["checkpoint_sha256"], "checkpoint_sha256_after": file_sha256(root / selection["selected_checkpoint"])}
-        atomic_json(path, value)
-        validate_fixed_result(root, value, run_id)
-        entry.update(status="completed", result=path.relative_to(root).as_posix())
-        state.update(evaluation=value, message=f"고정 모델 σ={sigma} 평가 완료")
-        state.event("고정 모델 평가 완료", {"sigma": sigma, "checkpoint_sha256": selection["checkpoint_sha256"], "eval_optimizer_steps": 0})
-        values.append(value)
-    return values
+            writer.writerow([row["relative_path"], label, probability, logit, *[selection[key] for key in keys]])
+
+
+def classify(model, splits, loaders, device, root, selection, state, optimizer_steps):
+    """학습이 완료된 해당 강도 best만 eval 상태로 평가하며 추가 갱신하지 않습니다."""
+    sigma, run_id = selection["sigma"], selection["run_id"]
+    directory = root / "work/results" / ("run_" + run_id)
+    path = directory / f"sigma_{sigma}_metrics.json"
+    if path.exists():
+        return validate_result(root, json.loads(path.read_text(encoding="utf-8")), run_id)
+    before = tensor_state_digest(model.state_dict())
+    if before != selection["model_state_sha256"]:
+        raise ValueError("분류 평가 시작 state가 선정 모델과 다릅니다.")
+    values, files = {}, {}
+    for name, loader in zip(["validation", "test"], loaders):
+        metrics, labels, probabilities, logits = evaluate(model, loader, device, None, state,
+                                                        stage="testing" if name == "test" else "validation", return_logits=True)
+        output = directory / f"sigma_{sigma}_{name}_predictions_private.csv"
+        _save_bound_predictions(output, splits[name], labels, probabilities, logits, selection)
+        files[name] = {"relative_path": output.relative_to(root).as_posix(), "sha256": file_sha256(output)}
+        values[name] = metrics
+    after = tensor_state_digest(model.state_dict())
+    if (before != after or any(m.training for m in model.modules()) or any(p.grad is not None for p in model.parameters())
+            or file_sha256(root / selection["selected_checkpoint"]) != selection["checkpoint_sha256"]):
+        raise ValueError("분류 평가에서 모델 state·BN·gradient·체크포인트가 변했습니다.")
+    value = {**selection, **values, "evaluation_sigma": sigma, "eval_optimizer_steps": 0,
+             "optimizer_steps": optimizer_steps, "prediction_files": files, "completed_at": now_kst(),
+             "state_digest_before": before, "state_digest_after": after,
+             "selected_checkpoint_policy": "해당 강도100회 학습 중 raw 검증 손실 최저 모델",
+             "test_use": "기존 시험셋의 탐색적 재사용; 시험 결과로 모델·강도·임계값을 선택하지 않음"}
+    atomic_json(path, value)
+    return validate_result(root, value, run_id)
 
 
 def run_training(config, root, state, device_name="cuda"):
@@ -360,9 +315,8 @@
     from .model import block_weight_downloads
     block_weight_downloads()
     started = time.monotonic()
-    seed_everything(config["seed"], config.get("cpu_threads", 4))
     if device_name == "cuda" and not torch.cuda.is_available():
-        raise RuntimeError("CUDA를 사용할 수 없습니다. 과학 조건을 바꿔 CPU로 대체하지 않습니다.")
+        raise RuntimeError("CUDA를 사용할 수 없습니다. 과학 조건을 자동 대체하지 않습니다.")
     device = torch.device(device_name)
     precision = precision_policy(config["precision"], device.type)
     manifest = prepare_dataset(config, root)
@@ -371,137 +325,171 @@
     checkpoint_dir = root / "work/checkpoints" / ("run_" + run_id)
     result_dir.mkdir(parents=True, exist_ok=True)
     checkpoint_dir.mkdir(parents=True, exist_ok=True)
-    policy = {"max_epochs": 100, "patience": config["early_stopping_patience"], "early_stopping_enabled": False,
-              "min_delta": config["min_delta"], "min_delta_mode": "absolute", "batch_size": config["batch_size"],
+    policy = {"max_epochs": 100, "early_stopping_enabled": False, "batch_size": config["batch_size"],
               "optimizer": "AdamW", "initial_learning_rate": config["learning_rate"], "weight_decay": config["weight_decay"],
               "scheduler_patience": config["scheduler_patience"], "scheduler_factor": config["scheduler_factor"],
-              "min_learning_rate": config["min_learning_rate"], "evaluation_forward": "fp32", "evaluation_loss": "fp64_signed_softplus"}
-    metadata = {**settings, "run_id": run_id, "protocol": PROTOCOL, "protocol_fixed_model": True,
-                "training_sigma": 0, "started_at": now_kst(), "device": device_information(device), "training_policy": policy}
-    atomic_json(result_dir / "run_metadata.json", metadata)
-    state.update(run_id=run_id, phase="training", training_status="running", stage="loading_model", sigma=0,
-                 device=metadata["device"], training_policy=policy, precision={k: v for k, v in precision.items() if k != "dtype"},
-                 dataset=manifest["summary"], result_directory=result_dir.relative_to(root).as_posix(), optimizer_steps=0,
-                 checkpoint_sha256=None, model_state_sha256=None, selected_checkpoint=None,
-                 message="σ0에서 새 모델 학습 준비 · 블러10조건은 학습 완료 후 평가")
+              "min_learning_rate": config["min_learning_rate"], "min_delta": config["min_delta"],
+              "evaluation_forward": "fp32", "evaluation_loss": "fp64_signed_softplus"}
+    metadata = {**settings, "run_id": run_id, "protocol": PROTOCOL, "protocol_fixed_model": False,
+                "started_at": now_kst(), "device": device_information(device), "training_policy": policy}
+    existing_metadata = result_dir / "run_metadata.json"
+    if existing_metadata.exists():
+        old = json.loads(existing_metadata.read_text(encoding="utf-8"))
+        if any(old.get(key) != value for key, value in settings.items()) or old.get("run_id") != run_id:
+            raise ValueError("기존 실행 metadata를 다른 소스로 덮어쓰지 않습니다.")
+    atomic_json(existing_metadata, metadata)
     splits = manifest["splits"]
     training = CTDataset(splits["train"], config["image_size"], training=True, samples_per_class=config["samples_per_class"], seed=config["seed"])
     validation = CTDataset(splits["validation"], config["image_size"], training=False)
     test = CTDataset(splits["test"], config["image_size"], training=False)
     train_loader, val_loader, test_loader = [_loader(dataset, config, device) for dataset in [training, validation, test]]
-    weights = Path(config["initial_weights_path"])
-    weights = weights if weights.is_absolute() else root / weights
-    model = SplitResNet50(sigma=0, pretrained=True, weights_path=weights, expected_weights_sha256=config["initial_weights_sha256"]).to(device)
-    optimizer, scheduler = build_optimizer_scheduler([p for p in model.parameters() if p.requires_grad], config)
-    scaler = torch.amp.GradScaler("cuda", enabled=precision["use_grad_scaler"])
-    control = TrainingControl(config["min_delta"], config["early_stopping_patience"], enabled=False)
-    best_path = checkpoint_dir / "sigma_0_best.pt"
-    last_path = checkpoint_dir / "sigma_0_last.pt"
-    history = []
-    start_epoch = 1
-    if last_path.exists():
-        saved = checkpoint_load(last_path, run_id)
-        history = saved["history"]
-        if (len(history) != saved["epoch"] or [row["epoch"] for row in history] != list(range(1, saved["epoch"] + 1))
-                or any(row["sigma"] != 0 for row in history) or saved["training_policy"] != policy):
-            raise ValueError("마지막 완료 epoch·이력·학습 정책이 서로 다릅니다.")
-        model.load_state_dict(saved["model"], strict=True)
-        optimizer.load_state_dict(saved["optimizer"])
-        scheduler.load_state_dict(saved["scheduler"])
-        scaler.load_state_dict(saved["scaler"])
-        control.load_state_dict(saved["training_control"])
-        if control.optimizer_steps != saved["epoch"] * len(train_loader):
-            raise ValueError("완료 epoch와 실제 optimizer 업데이트 수가 다릅니다.")
-        restore_all_rng(saved, device)
-        start_epoch = saved["epoch"] + 1
-        if not best_path.exists() or checkpoint_load(best_path, run_id)["epoch"] != control.best_raw_epoch:
-            raise ValueError("재개에 필요한 현재 run의 최저 검증 손실 모델이 없습니다.")
-        state.event("σ0 마지막 완료 회차 재개", {"next_epoch": start_epoch, "optimizer_steps": control.optimizer_steps})
-    elif best_path.exists() or list(result_dir.glob("sigma_*_metrics.json")) or (result_dir / "fixed_model_selection.json").exists():
-        raise ValueError("last 없이 남은 모델·결과가 있어 새 학습으로 덮어쓰지 않습니다.")
-    state.data["history"] = list(history)
-    for epoch in range(start_epoch, 101):
-        if (result_dir / "fixed_model_selection.json").exists() or list(result_dir.glob("sigma_*_metrics.json")):
-            raise ValueError("선정·평가 뒤 추가 학습을 허용하지 않습니다.")
-        training.set_epoch(epoch - 1)
-        model.train()
-        total_loss, seen = 0.0, {"OK": 0, "NG": 0}
-        tick = time.monotonic()
-        state.update(phase="training", stage="training", epoch=epoch, batch=0, batches=len(train_loader), sigma=0,
-                     seen_per_class=seen.copy(), message=f"블러 없는 모델 학습 {epoch}/100회")
-        for batch_index, (images, target) in enumerate(train_loader, 1):
-            state.data["attempted_batch"] = batch_index
-            images, target = images.to(device, non_blocking=True), target.to(device, non_blocking=True)
-            optimizer.zero_grad(set_to_none=True)
-            with torch.autocast(device_type=device.type, dtype=precision["dtype"], enabled=precision["autocast_enabled"]):
-                logits = model(images)
-                loss = stable_binary_loss(logits, target, dtype=torch.float32)
-            if not torch.isfinite(loss):
-                raise FloatingPointError(f"σ0 epoch={epoch} batch={batch_index}: 비유한 학습 손실")
-            scaler.scale(loss).backward()
-            scaler.unscale_(optimizer)
-            gradient_norm = nn.utils.clip_grad_norm_(model.parameters(), 1.0, error_if_nonfinite=True)
-            scaler.step(optimizer)
-            scaler.update()
-            control.optimizer_steps += 1
-            total_loss += loss.item() * len(target)
-            ng = int(target.sum().item())
-            seen["NG"] += ng
-            seen["OK"] += len(target) - ng
-            if batch_index == 1 or batch_index % config["status_every_batches"] == 0 or batch_index == len(train_loader):
-                state.update(batch=batch_index, seen_per_class=seen.copy(), train_loss=total_loss / sum(seen.values()),
-                             optimizer_steps=control.optimizer_steps, run_optimizer_steps=control.optimizer_steps,
-                             learning_rate=optimizer.param_groups[0]["lr"], last_gradient_norm=gradient_norm.item(),
-                             epoch_elapsed_seconds=time.monotonic() - tick, elapsed_seconds=time.monotonic() - started)
-        if seen != {"OK": config["samples_per_class"], "NG": config["samples_per_class"]}:
-            raise AssertionError("클래스별 온라인 학습 표본 수가 명세와 다릅니다.")
-        state.update(stage="validation", batch=0, batches=len(val_loader), message="σ0 검증 손실로만 모델 선정 중")
-        val_metrics, _, _ = evaluate(model, val_loader, device, precision, state)
-        lr_before = optimizer.param_groups[0]["lr"]
-        decision = control.observe(val_metrics["loss"], epoch)
-        scheduler.step(val_metrics["loss"])
-        row = {"sigma": 0, "epoch": epoch, "train_loss": total_loss / len(training), "val_loss": val_metrics["loss"],
-               "val_accuracy": val_metrics["accuracy"], "val_auc": val_metrics["auc"], "seen_per_class": seen.copy(),
-               "seconds": time.monotonic() - tick, "learning_rate": lr_before, "next_learning_rate": optimizer.param_groups[0]["lr"],
-               "optimizer_steps": control.optimizer_steps, "best_raw_epoch": control.best_raw_epoch,
-               "meaningful_best_loss": control.meaningful_best_loss, "early_stopping_wait": control.stale_epochs}
-        history.append(row)
-        state.data["history"] = list(history)
-        base = checkpoint_base(run_id, epoch, model, control, policy)
-        if decision["raw_improved"]:
-            _save_checkpoint(best_path, {**base, "validation": val_metrics})
-        _save_checkpoint(last_path, {**base, "optimizer": optimizer.state_dict(), "scheduler": scheduler.state_dict(),
-                                   "scaler": scaler.state_dict(), "history": list(history), "torch_rng_state": torch.get_rng_state(),
-                                   "cuda_rng_state": torch.cuda.get_rng_state_all() if device.type == "cuda" else [],
-                                   "python_rng_state": random.getstate(), "numpy_rng_state": numpy_rng_state()})
-        atomic_json(result_dir / "sigma_0_history.json", history)
-        state.update(best_epoch=control.best_raw_epoch, best_raw_epoch=control.best_raw_epoch, best_raw_loss=control.best_raw_loss,
-                     learning_rate=optimizer.param_groups[0]["lr"], early_stopping_wait=control.stale_epochs)
-        state.event("σ0 학습 회차 완료", row)
-        print(json.dumps(row, ensure_ascii=False), flush=True)
-    if len(history) != 100 or control.optimizer_steps != 100 * len(train_loader):
-        raise ValueError("σ0 학습100회를 모두 마치지 않아 블러 평가를 시작하지 않습니다.")
-    best = checkpoint_load(best_path, run_id)
-    if best["epoch"] != control.best_raw_epoch:
-        raise ValueError("선정 best epoch와 전체 검증 이력이 다릅니다.")
-    # 평가 모델을 새로 만들며 학습의 gradient·optimizer를 넘기지 않습니다.
-    evaluation_model = SplitResNet50(sigma=0, pretrained=False).to(device).eval().requires_grad_(False)
-    evaluation_model.load_state_dict(best["model"], strict=True)
-    selection = {"run_id": run_id, "protocol": PROTOCOL, "protocol_fixed_model": True, "training_sigma": 0,
-                 "best_epoch": best["epoch"], "checkpoint_epoch": best["epoch"], "epochs_ran": 100,
-                 "selected_checkpoint": best_path.relative_to(root).as_posix(), "checkpoint_sha256": file_sha256(best_path),
-                 "model_state_sha256": tensor_state_digest(evaluation_model.state_dict())}
-    selection_path = result_dir / "fixed_model_selection.json"
-    if selection_path.exists():
-        if json.loads(selection_path.read_text(encoding="utf-8")) != selection:
-            raise ValueError("이미 동결한 모델 identity를 교체할 수 없습니다.")
-    else:
+    state.update(run_id=run_id, dataset=manifest["summary"], device=metadata["device"], training_policy=policy,
+                 precision={k:v for k,v in precision.items() if k != "dtype"}, status="running")
+    completed_steps = 0
+    for index, sigma in enumerate(SIGMAS):
+        entry = state.data["sigma_queue"][index]
+        metrics_path = result_dir / f"sigma_{sigma}_metrics.json"
+        privacy_path = result_dir / f"sigma_{sigma}_privacy.json"
+        state.update(sigma=sigma, sigma_index=index+1, training_sigma=sigma, epoch=0, history=[], evaluation=None, privacy=None,
+                     checkpoint_sha256=None, model_state_sha256=None, selected_checkpoint=None,
+                     classification_status="pending", privacy_status="pending", training_status="pending")
+        if metrics_path.exists() and privacy_path.exists():
+            result = validate_result(root, json.loads(metrics_path.read_text(encoding="utf-8")), run_id)
+            private = validate_privacy_result(root, json.loads(privacy_path.read_text(encoding="utf-8")), run_id)
+            entry.update(status="completed", training_status="completed", classification_status="completed", privacy_status="completed",
+                         result=metrics_path.relative_to(root).as_posix(), privacy_result=privacy_path.relative_to(root).as_posix())
+            completed_steps += result["optimizer_steps"]
+            state.update(evaluation=result, privacy=private, epoch=100, training_status="completed",
+                         classification_status="completed", privacy_status="completed", run_optimizer_steps=completed_steps)
+            continue
+        entry.update(status="running", training_status="running")
+        seed_everything(config["seed"], config.get("cpu_threads", 4))
+        model = SplitResNet50(sigma=sigma, pretrained=True,
+                             weights_path=readonly_input(root, config, "initial_weights_path"),
+                             expected_weights_sha256=config["initial_weights_sha256"]).to(device)
+        initialization = {"initial_model_state_sha256": tensor_state_digest(model.state_dict()),
+                          "initial_weights_sha256": config["initial_weights_sha256"], "seed": config["seed"],
+                          "optimizer_initial_steps": 0, "training_sigma": sigma}
+        initial_path = result_dir / f"sigma_{sigma}_initialization.json"
+        if initial_path.exists() and json.loads(initial_path.read_text(encoding="utf-8")) != initialization:
+            raise ValueError("새 강도의 초기 모델·옵티마이저0 조건이 최초 기록과 다릅니다.")
+        atomic_json(initial_path, initialization)
+        optimizer, scheduler = build_optimizer_scheduler([p for p in model.parameters() if p.requires_grad], config)
+        scaler = torch.amp.GradScaler("cuda", enabled=precision["use_grad_scaler"])
+        control = TrainingControl(config["min_delta"], config["early_stopping_patience"], enabled=False)
+        best_path, last_path = [checkpoint_dir / f"sigma_{sigma}_{kind}.pt" for kind in ["best", "last"]]
+        history, start_epoch = [], 1
+        if last_path.exists():
+            saved = checkpoint_load(last_path, run_id, sigma)
+            history = saved["history"]
+            if (len(history) != saved["epoch"] or [r["epoch"] for r in history] != list(range(1, saved["epoch"]+1))
+                    or any(r["sigma"] != sigma for r in history) or saved["training_policy"] != policy):
+                raise ValueError("재개 마지막 회차·이력·학습 정책이 다릅니다.")
+            model.load_state_dict(saved["model"], strict=True)
+            optimizer.load_state_dict(saved["optimizer"])
+            scheduler.load_state_dict(saved["scheduler"])
+            scaler.load_state_dict(saved["scaler"])
+            control.load_state_dict(saved["training_control"])
+            restore_all_rng(saved, device)
+            start_epoch = saved["epoch"] + 1
+            if control.optimizer_steps != saved["epoch"] * len(train_loader) or checkpoint_load(best_path, run_id, sigma)["epoch"] != control.best_raw_epoch:
+                raise ValueError("재개 optimizer 단계·best 회차가 다릅니다.")
+        elif best_path.exists() or metrics_path.exists() or privacy_path.exists():
+            raise ValueError("마지막 완료 회차 없이 남은 결과·모델을 덮어쓰지 않습니다.")
+        state.update(phase="training", stage="training", training_status="running", history=list(history),
+                     optimizer_steps=control.optimizer_steps, run_optimizer_steps=completed_steps+control.optimizer_steps)
+        for epoch in range(start_epoch, 101):
+            if metrics_path.exists() or (result_dir / f"sigma_{sigma}_selection.json").exists():
+                raise ValueError("모델 선정·분류 뒤 추가 학습을 거부합니다.")
+            training.set_epoch(epoch-1)
+            model.train()
+            total_loss, seen, tick = 0., {"OK": 0, "NG": 0}, time.monotonic()
+            state.update(epoch=epoch, stage="training", batch=0, batches=len(train_loader), seen_per_class=seen.copy(),
+                         message=f"σ={sigma}: 새 모델 학습 {epoch}/100회")
+            for batch_index, (images, target) in enumerate(train_loader, 1):
+                state.data["attempted_batch"] = batch_index
+                images, target = images.to(device), target.to(device)
+                optimizer.zero_grad(set_to_none=True)
+                with torch.autocast(device_type=device.type, dtype=precision["dtype"], enabled=precision["autocast_enabled"]):
+                    loss = stable_binary_loss(model(images), target, dtype=torch.float32)
+                if not torch.isfinite(loss):
+                    raise FloatingPointError(f"σ={sigma} epoch={epoch} batch={batch_index}: 비유한 학습 손실")
+                scaler.scale(loss).backward()
+                scaler.unscale_(optimizer)
+                norm = nn.utils.clip_grad_norm_(model.parameters(), 1., error_if_nonfinite=True)
+                scaler.step(optimizer)
+                scaler.update()
+                control.optimizer_steps += 1
+                total_loss += loss.item()*len(target)
+                ng = int(target.sum().item())
+                seen["NG"] += ng
+                seen["OK"] += len(target)-ng
+                if batch_index == 1 or batch_index % config["status_every_batches"] == 0 or batch_index == len(train_loader):
+                    state.update(batch=batch_index, seen_per_class=seen.copy(), train_loss=total_loss/sum(seen.values()),
+                                 optimizer_steps=control.optimizer_steps, run_optimizer_steps=completed_steps+control.optimizer_steps,
+                                 learning_rate=optimizer.param_groups[0]["lr"], last_gradient_norm=norm.item(),
+                                 epoch_elapsed_seconds=time.monotonic()-tick, elapsed_seconds=time.monotonic()-started)
+            if seen != {"OK": config["samples_per_class"], "NG": config["samples_per_class"]}:
+                raise AssertionError("실제 클래스별 온라인 학습 표본 수가 다릅니다.")
+            val, _, _ = evaluate(model, val_loader, device, precision, state)
+            lr = optimizer.param_groups[0]["lr"]
+            decision = control.observe(val["loss"], epoch)
+            scheduler.step(val["loss"])
+            history.append({"sigma": sigma, "epoch": epoch, "train_loss": total_loss/len(training), "val_loss": val["loss"],
+                            "val_accuracy": val["accuracy"], "val_auc": val["auc"], "seen_per_class": seen,
+                            "seconds": time.monotonic()-tick, "learning_rate": lr, "next_learning_rate": optimizer.param_groups[0]["lr"],
+                            "optimizer_steps": control.optimizer_steps, "best_raw_epoch": control.best_raw_epoch})
+            base = checkpoint_base(run_id, sigma, epoch, model, control, policy)
+            if decision["raw_improved"]:
+                _save_checkpoint(best_path, {**base, "validation": val})
+            _save_checkpoint(last_path, {**base, "optimizer": optimizer.state_dict(), "scheduler": scheduler.state_dict(),
+                                       "scaler": scaler.state_dict(), "history": list(history), "torch_rng_state": torch.get_rng_state(),
+                                       "cuda_rng_state": torch.cuda.get_rng_state_all() if device.type == "cuda" else [],
+                                       "python_rng_state": random.getstate(), "numpy_rng_state": numpy_rng_state()})
+            atomic_json(result_dir / f"sigma_{sigma}_history.json", history)
+            state.update(history=list(history), best_epoch=control.best_raw_epoch, best_raw_epoch=control.best_raw_epoch,
+                         best_raw_loss=control.best_raw_loss, learning_rate=optimizer.param_groups[0]["lr"])
+            state.event("독립 학습 회차 완료", history[-1])
+            print(json.dumps(history[-1], ensure_ascii=False), flush=True)
+        if len(history) != 100 or control.optimizer_steps != 100*len(train_loader):
+            raise ValueError("100회 학습 미완료 상태에서 분류·점수를 시작하지 않습니다.")
+        best = checkpoint_load(best_path, run_id, sigma)
+        if best["epoch"] != control.best_raw_epoch:
+            raise ValueError("선정 best 회차와 전체 검증 이력이 다릅니다.")
+        del model, optimizer, scheduler, scaler
+        gc.collect()
+        if device.type == "cuda":
+            torch.cuda.empty_cache()
+        evaluation_model = SplitResNet50(sigma=sigma, pretrained=False).to(device).eval().requires_grad_(False)
+        evaluation_model.load_state_dict(best["model"], strict=True)
+        selection = {"run_id": run_id, "protocol": PROTOCOL, "protocol_fixed_model": False, "sigma": sigma, "training_sigma": sigma,
+                     "best_epoch": best["epoch"], "checkpoint_epoch": best["epoch"], "epochs_ran": 100,
+                     "selected_checkpoint": best_path.relative_to(root).as_posix(), "checkpoint_sha256": file_sha256(best_path),
+                     "model_state_sha256": tensor_state_digest(evaluation_model.state_dict()), **result_binding(root, metadata)}
+        selection_path = result_dir / f"sigma_{sigma}_selection.json"
+        if selection_path.exists() and json.loads(selection_path.read_text(encoding="utf-8")) != selection:
+            raise ValueError("이미 선정한 강도별 모델 식별자를 교체할 수 없습니다.")
         atomic_json(selection_path, selection)
-    state.update(**{key: selection[key] for key in ["best_epoch", "checkpoint_sha256", "model_state_sha256", "selected_checkpoint"]},
-                 phase="evaluation", training_status="completed", epoch=100, eval_optimizer_steps=0)
-    evaluate_frozen_sigmas(evaluation_model, splits, [val_loader, test_loader], device, root, run_id,
-                          selection, state, control.optimizer_steps)
-    state.update(phase="completed", stage="completed", status="completed", training_status="completed", pid=None,
-                 evaluation_current_sigma=None, elapsed_seconds=time.monotonic() - started,
-                 message="σ0 모델100회 학습과 동일 가중치 블러10단계 평가 완료")
+        entry.update(training_status="completed", classification_status="running")
+        state.update(phase="classification", training_status="completed", classification_status="running", epoch=100,
+                     **{k:selection[k] for k in ["best_epoch", "checkpoint_sha256", "model_state_sha256", "selected_checkpoint"]})
+        result = classify(evaluation_model, splits, [val_loader, test_loader], device, root, selection, state, control.optimizer_steps)
+        entry.update(classification_status="completed", result=metrics_path.relative_to(root).as_posix(), privacy_status="running")
+        state.update(phase="privacy", stage="privacy", evaluation=result, classification_status="completed", privacy_status="running")
+        private = (validate_privacy_result(root, json.loads(privacy_path.read_text(encoding="utf-8")), run_id) if privacy_path.exists()
+                   else run_privacy(evaluation_model, splits["test"], root, run_id, selection, state))
+        validate_privacy_result(root, private, run_id)
+        entry.update(status="completed", privacy_status="completed", privacy_result=privacy_path.relative_to(root).as_posix())
+        completed_steps += control.optimizer_steps
+        state.update(privacy=private, privacy_status="completed", run_optimizer_steps=completed_steps,
+                     message=f"σ={sigma}: 독립100회 학습·분류·실측 점수 완료")
+        state.event("독립 강도 완료", {"sigma": sigma, "score": private["score"]})
+        del evaluation_model, best
+        gc.collect()
+        if device.type == "cuda":
+            torch.cuda.empty_cache()
+    state.update(phase="completed", stage="completed", status="completed", pid=None,
+                 elapsed_seconds=time.monotonic()-started, message="10강도 독립 학습·분류·조건부 프라이버시 점수 계산 완료")
     return state.data
+
+
````

## tests/test_dashboard.py

| 구분 | 이전 | 이후 |
| --- | --- | --- |
| 상태 | 수정 | 수정 |
| 바이트 | 35072 | 46820 |
| SHA-256 | 4631495a4e95d59b6821cbb85fc996280c779e8585dc3e907c7b5baf80cfa6cc | 02f0de9f8b64ee2154b42a1130d4221e6536817bccc2fee7a23be258992ad9f8 |

````diff
--- a/tests/test_dashboard.py
+++ b/tests/test_dashboard.py
@@ -51,11 +51,12 @@
         headers = {"Host": host or f"127.0.0.1:{self.server.server_port}"}
         if authenticated:
             headers["Cookie"] = "dashboard_session=test-session-token"
-        connection.request("GET", path, headers=headers)
-        response = connection.getresponse()
-        result = response.status, dict(response.getheaders()), response.read()
-        connection.close()
-        return result
+        try:
+            connection.request("GET", path, headers=headers)
+            response = connection.getresponse()
+            return response.status, dict(response.getheaders()), response.read()
+        finally:
+            connection.close()
 
     @unittest.skipUnless(os.name == "nt", "Windows 삭제 공유 핸들 검사")
     def test_open_reader_allows_replace_and_preserves_complete_versions(self):
@@ -249,20 +250,21 @@
         self.assertEqual(read_status(self.root)["status"], "failed")
 
 
-    def fixed_fixture(self, sigma=0, completed=True):
+    def fixed_fixture(self, sigma=0, completed=True, privacy_status="completed"):
         # CT나 실제 모델을 읽지 않는 합성 자료입니다. 저장 경계와 SHA만 실제 파일로 검사합니다.
-        from src.identity import _run_identity, PROTOCOL
+        from src.identity import _run_identity
+        PROTOCOL = "independent-sigma-privacy-v1"
         (self.root / "src").mkdir(exist_ok=True)
         (self.root / "tools").mkdir(exist_ok=True)
-        for relative in ("run_training.py", "src/model.py", "src/data.py", "tools/feature_generator.py"):
+        for relative in ("run_training.py", "src/model.py", "src/data.py", "src/privacy.py", "tools/feature_generator.py"):
             (self.root / relative).write_text("# 합성 검사 자료\n", encoding="utf-8")
         reference = self.root / "work/reference.json"
         records = [{"id": "synthetic", "source_class": "Normal cases"}]
         digest = hashlib.sha256(json.dumps(records, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
         manifest = {"records": records, "splits": {"train": records, "validation": [], "test": []}, "manifest_sha256": digest}
         reference.write_text(json.dumps(manifest), encoding="utf-8")
-        config = {"protocol": PROTOCOL, "protocol_fixed_model": True, "training_sigma": 0,
-                  "sigmas": list(SIGMA_VALUES), "epochs": 100, "early_stopping_enabled": False,
+        config = {"protocol": PROTOCOL, "protocol_fixed_model": False,
+                  "score_version": "gallery-residual-v1", "sigmas": list(SIGMA_VALUES), "epochs": 100, "early_stopping_enabled": False,
                   "image_size": 512, "batch_size": 8, "samples_per_class": 5000, "seed": 42, "precision": "bf16",
                   "expected_reference_manifest": "work/reference.json",
                   "expected_reference_manifest_sha256": hashlib.sha256(reference.read_bytes()).hexdigest(),
@@ -275,19 +277,22 @@
         self.run_id = run_id
         folder = results / f"run_{run_id}"
         folder.mkdir(exist_ok=True)
-        (folder / "run_metadata.json").write_text(json.dumps(dict(settings, run_id=run_id, protocol=PROTOCOL, protocol_fixed_model=True, training_sigma=0)), encoding="utf-8")
-        checkpoint = self.root / f"work/checkpoints/run_{run_id}/sigma_0_best.pt"
+        (folder / "run_metadata.json").write_text(json.dumps(dict(settings, run_id=run_id, protocol=PROTOCOL, protocol_fixed_model=False, training_sigma=sigma)), encoding="utf-8")
+        checkpoint = self.root / f"work/checkpoints/run_{run_id}/sigma_{sigma}_best.pt"
         checkpoint.parent.mkdir(parents=True, exist_ok=True)
-        checkpoint.write_bytes(b"synthetic-selected-checkpoint")
-        selection = {"run_id": run_id, "protocol": PROTOCOL, "protocol_fixed_model": True, "training_sigma": 0,
-                     "best_epoch": 2, "checkpoint_epoch": 2, "epochs_ran": 100,
+        checkpoint.write_bytes(f"synthetic-selected-checkpoint-{sigma}".encode())
+        selection = {"run_id": run_id, "protocol": PROTOCOL, "protocol_fixed_model": False, "training_sigma": sigma,
+                     "evaluation_sigma": sigma, "sigma": sigma, "best_epoch": 2, "checkpoint_epoch": 2, "epochs_ran": 100,
                      "checkpoint_sha256": hashlib.sha256(checkpoint.read_bytes()).hexdigest(), "model_state_sha256": "a"*64,
                      "selected_checkpoint": checkpoint.relative_to(self.root).as_posix()}
-        (folder / "fixed_model_selection.json").write_text(json.dumps(selection), encoding="utf-8")
-        history = [{"sigma": 0, "epoch": epoch, "train_loss": 0, "val_loss": 1/epoch,
+        selection.update(source_manifest_sha256=hashlib.sha256((results/"dataset_manifest_private.json").read_bytes()).hexdigest(),
+                         manifest_records_sha256=digest,
+                         source_hashes_sha256=hashlib.sha256(json.dumps(settings["source_hashes"],sort_keys=True).encode()).hexdigest())
+        (folder / f"sigma_{sigma}_selection.json").write_text(json.dumps(selection), encoding="utf-8")
+        history = [{"sigma": sigma, "epoch": epoch, "train_loss": 0, "val_loss": 1/epoch,
                     "val_accuracy": 1, "val_auc": None, "learning_rate": 0, "next_learning_rate": 0,
-                    "optimizer_steps": epoch*1250, "early_stopping_wait": 0} for epoch in range(1,101)]
-        (folder / "sigma_0_history.json").write_text(json.dumps(history), encoding="utf-8")
+                    "optimizer_steps": epoch*1250, "best_raw_epoch": 1} for epoch in range(1,101)]
+        (folder / f"sigma_{sigma}_history.json").write_text(json.dumps(history), encoding="utf-8")
         metrics = dict(selection, sigma=sigma, evaluation_sigma=sigma, eval_optimizer_steps=0, optimizer_steps=125000,
                        completed_at="2026-11-20T01:00:00+09:00", validation={"accuracy": 1, "auc": None, "loss": 0, "n_images": 4},
                        test={"accuracy": 0.75, "auc": 0.8, "loss": 0, "n_images": 4, "confusion_matrix": [[2,0],[1,1]]}, prediction_files={})
@@ -297,24 +302,48 @@
             target.write_text("id,label,prediction\nsynthetic,0,0\n", encoding="utf-8")
             metrics["prediction_files"][split] = {"relative_path": relative, "sha256": hashlib.sha256(target.read_bytes()).hexdigest()}
         (folder / f"sigma_{sigma}_metrics.json").write_text(json.dumps(metrics), encoding="utf-8")
-        self.status(run_id=run_id, schema_version=2, protocol=PROTOCOL, protocol_fixed_model=True, training_sigma=0,
-                    training_status="completed" if completed else "running", epoch=100 if completed else 47, epochs=100,
+        raw = folder / f"sigma_{sigma}_privacy_groups_private.json"
+        pipeline={"protocol":PROTOCOL,"sigma":sigma,"checkpoint_sha256":selection["checkpoint_sha256"],
+                  "model_state_sha256":selection["model_state_sha256"],"source_hashes":settings["source_hashes"],
+                  "precision":"fp32","packet_batch_size":1,"device":"cpu","torch_version":"합성",
+                  "shape_dtype_byteorder_in_hash":True,"manifest_sha256":digest,"encoder_state_sha256":"0"*64}
+        distance=[[0 if i==j else 1 for j in range(4)]for i in range(4)]
+        groups=[{"group_index":i,"weight":0.25,"candidates":[i],"tie_count":1,"b_i":0.75,"expected_mse":0,
+                 "candidate_mse":[0],"candidate_residual":[0],"attack_residual":0,"prior_residual":0.75,
+                 "fractional_top1":1,"target_in_tie":True}for i in range(4)]
+        raw.write_text(json.dumps({"per_group":groups,"distance_matrix":distance,"pipeline":pipeline,
+                                  "gallery_feature_hashes":[f"{i:064x}"for i in range(4)],
+                                  "query_feature_hashes":[f"{i:064x}"for i in range(4)]}),encoding="utf-8")
+        privacy = dict(selection, score_version="gallery-residual-v1", score=0, G=4, n_queries=4,
+                       original_test_images=4, fractional_top1=1, fractional_correct_sum=4,
+                       exact_return_groups=4, target_in_tie_groups=4,
+                       tie_histogram={"1":4}, T_attack=0, T_prior=0.75, raw_ratio=0,
+                       residual_quantiles={"0":0,"0.25":0,"0.5":0,"0.75":0,"1":0}, score_ci95=[0,0],
+                       controls={"original_score":0,"constant_score":100},
+                       privacy_source_sha256=settings["source_hashes"]["src/privacy.py"],
+                       attack_protocol="known-encoder-closed-gallery-full-feature-bytehash-v1",
+                       precision="fp32",packet_batch_size=1,device="cpu",encoder_state_sha256="0"*64,
+                       pipeline_sha256=hashlib.sha256(json.dumps(pipeline,sort_keys=True).encode()).hexdigest(),
+                       raw_file={"relative_path":raw.relative_to(self.root).as_posix(),"sha256":hashlib.sha256(raw.read_bytes()).hexdigest()},
+                       completed_at="2026-11-20T01:00:00+09:00")
+        (folder / f"sigma_{sigma}_privacy.json").write_text(json.dumps(privacy),encoding="utf-8")
+        self.status(run_id=run_id, schema_version=2, protocol=PROTOCOL, protocol_fixed_model=False, training_sigma=sigma,
+                    sigma=sigma, classification_status="completed" if completed else "pending", privacy_status=privacy_status if completed else "pending", training_status="completed" if completed else "running", epoch=100 if completed else 47, epochs=100,
                     checkpoint_sha256=selection["checkpoint_sha256"] if completed else None,
                     model_state_sha256=selection["model_state_sha256"] if completed else None, best_epoch=2,
                     history=history if completed else history[:47],
-                    sigma_queue=[{"sigma": n, "status": "completed" if completed and n==sigma else "pending"} for n in SIGMA_VALUES])
+                    sigma_queue=[{"sigma": n, "status": "completed" if completed and n==sigma and privacy_status=="completed" else "running" if n==sigma else "pending", "training_status": "completed" if completed and n==sigma else "running" if n==sigma else "pending", "classification_status": "completed" if completed and n==sigma else "pending", "privacy_status": privacy_status if completed and n==sigma else "pending"} for n in SIGMA_VALUES])
         return folder, metrics
 
-    def test_training_keeps_all_evaluations_pending_even_when_old_metrics_exist(self):
-        self.fixed_fixture(completed=False)
+    def test_current_sigma_training_keeps_only_its_curve_and_never_old_scores(self):
+        self.fixed_fixture(8, completed=False)
         for sigma in SIGMA_VALUES:
             result = sigma_results(self.root, sigma)
-            self.assertEqual(result["status"], "pending")
             self.assertIsNone(result["metrics"])
-            self.assertEqual(result["evaluation_history"], [])
-            self.assertEqual(len(result["history"]), 47 if sigma == 0 else 0)
-
-    def test_all_ten_evaluations_share_one_checkpoint_and_no_extra_steps(self):
+            self.assertIsNone(result["privacy"])
+            self.assertEqual(len(result["history"]), 47 if sigma == 8 else 0)
+
+    def test_all_ten_independent_models_return_own_accuracy_curve_and_zero_score(self):
         hashes = set()
         for sigma in SIGMA_VALUES:
             self.fixed_fixture(sigma)
@@ -322,26 +351,56 @@
             self.assertEqual(code, 200)
             result = json.loads(body)
             self.assertEqual(result["status"], "completed", result)
+            self.assertEqual(result["metrics"]["training_sigma"], sigma)
             self.assertEqual(result["metrics"]["eval_optimizer_steps"], 0)
             self.assertEqual(result["metrics"]["test"]["correct_count"], 3)
             self.assertEqual(result["metrics"]["test"]["accuracy"], 0.75)
-            self.assertEqual(len(result["history"]), 100 if sigma == 0 else 0)
-            self.assertEqual(result["evaluation_history"][0]["sigma"], sigma)
+            self.assertEqual(len(result["history"]), 100)
+            self.assertTrue(all(row["sigma"]==sigma for row in result["history"]))
+            self.assertEqual(result["privacy"]["score"], 0)
+            self.assertEqual(result["privacy"]["score_version"], "gallery-residual-v1")
             hashes.add(result["metrics"]["checkpoint_sha256"])
             self.assertNotIn("selected_checkpoint", body.decode())
             self.assertNotIn("synthetic", body.decode())
-        self.assertEqual(len(hashes), 1)
+        self.assertEqual(len(hashes), 10)
         self.assertEqual(self.get("/api/sigma-results/0", authenticated=False)[0], 401)
         self.assertEqual(self.get("/api/sigma-results/0", host="example.com")[0], 403)
         for suffix in ("-1", "3", "00", "0?file=private.json", "../status", "%30"):
             self.assertEqual(self.get("/api/sigma-results/"+suffix)[0], 400)
 
+    def test_completed_sigma_remains_available_while_next_sigma_trains(self):
+        self.fixed_fixture(0)
+        self.fixed_fixture(8, completed=False)
+        path=self.root/"work/runtime/status.json"
+        state=json.loads(path.read_text(encoding="utf-8"))
+        row=next(item for item in state["sigma_queue"] if item["sigma"]==0)
+        row.update(status="completed",training_status="completed",classification_status="completed",privacy_status="completed")
+        path.write_text(json.dumps(state),encoding="utf-8")
+        completed=sigma_results(self.root,0)
+        active=sigma_results(self.root,8)
+        self.assertEqual(completed["status"],"completed",completed)
+        self.assertEqual(completed["privacy"]["score"],0)
+        self.assertEqual(len(completed["history"]),100)
+        self.assertNotIn("early_stopping_wait", completed["history"][0])
+        self.assertEqual(len(active["history"]),47)
+        self.assertIsNone(active["metrics"])
+        self.assertIsNone(active["privacy"])
+
+    def test_classification_visible_while_privacy_waits_and_errors_have_no_fake_score(self):
+        for state in ("pending", "running", "error"):
+            self.fixed_fixture(8, privacy_status=state)
+            result = sigma_results(self.root, 8)
+            self.assertIsNotNone(result["metrics"], result)
+            self.assertIsNone(result["privacy"])
+            self.assertEqual(result["privacy_status"], state)
+            self.assertNotEqual(result["status"], "completed")
+
     def test_wrong_model_run_source_prediction_or_training_contract_is_rejected(self):
         folder, original = self.fixed_fixture(8)
         path = folder / "sigma_8_metrics.json"
-        for changes in ({"training_sigma": 8}, {"eval_optimizer_steps": 1}, {"checkpoint_sha256": "b"*64},
+        for changes in ({"training_sigma": 0}, {"eval_optimizer_steps": 1}, {"checkpoint_sha256": "b"*64},
                         {"model_state_sha256": "b"*64}, {"best_epoch": 3}, {"epochs_ran": 99},
-                        {"run_id": "f"*16}, {"sigma": 0}, {"evaluation_sigma": 4}, {"protocol_fixed_model": False}):
+                        {"run_id": "f"*16}, {"sigma": 0}, {"evaluation_sigma": 4}, {"protocol_fixed_model": True}):
             with self.subTest(changes=changes):
                 path.write_text(json.dumps(dict(original, **changes)), encoding="utf-8")
                 self.assertIsNone(sigma_results(self.root, 8)["metrics"])
@@ -359,8 +418,24 @@
         (self.root / metrics["selected_checkpoint"]).write_bytes(b"changed")
         self.assertIsNone(sigma_results(self.root, 0)["metrics"])
         self.fixed_fixture()
-        (folder / "fixed_model_selection.json").unlink()
+        (folder / "sigma_0_selection.json").unlink()
         self.assertIsNone(sigma_results(self.root, 0)["metrics"])
+
+    def test_privacy_identity_raw_file_and_nonfinite_values_fail_without_fake_score(self):
+        folder, _ = self.fixed_fixture(8)
+        path=folder / "sigma_8_privacy.json"
+        original=json.loads(path.read_text(encoding="utf-8"))
+        for change in ({"score": 100}, {"score": float("nan")}, {"score": True}, {"score_version":"other"},
+                       {"sigma":0}, {"run_id":"f"*16}, {"checkpoint_sha256":"f"*64}, {"best_epoch":3},
+                       {"T_prior":0}, {"controls":{"original_score":1,"constant_score":100}}):
+            path.write_text(json.dumps(dict(original,**change)),encoding="utf-8")
+            result=sigma_results(self.root,8)
+            self.assertIsNotNone(result["metrics"],result)
+            self.assertIsNone(result["privacy"],change)
+            self.assertEqual(result["privacy_status"],"error")
+        path.write_text(json.dumps(original),encoding="utf-8")
+        (self.root/original["raw_file"]["relative_path"]).write_text("changed",encoding="utf-8")
+        self.assertEqual(sigma_results(self.root,8)["privacy_status"],"error")
 
     def test_numeric_results_are_strict_and_preserve_zero_and_undefined_auc(self):
         folder, original = self.fixed_fixture()
@@ -396,7 +471,8 @@
         (folder / "sigma_0_history.json").write_text("invalid", encoding="utf-8")
         result = sigma_results(self.root, 8)
         self.assertEqual(result["status"], "completed")
-        self.assertEqual(result["history"], [])
+        self.assertEqual(len(result["history"]), 100)
+        self.assertTrue(all(row["sigma"] == 8 for row in result["history"]))
 
     def test_result_symlink_and_status_private_fields_do_not_escape(self):
         folder, _ = self.fixed_fixture()
@@ -410,7 +486,7 @@
         self.assertNotIn(b"secret", body)
         self.assertNotIn(b"private_path", body)
 
-    def test_feature_previews_wait_until_single_training_is_complete(self):
+    def test_feature_previews_wait_until_selected_training_and_privacy_complete(self):
         self.fixed_fixture(completed=False)
         result = feature_previews(self.root)
         self.assertEqual(result["items"], [])
@@ -443,22 +519,22 @@
         from src.identity import file_sha256
         for sigma in SIGMA_VALUES:
             folder, metrics = self.fixed_fixture(sigma)
-        self.status(run_id=self.run_id, protocol="fixed-model-sigma0-v1", protocol_fixed_model=True,
-                    training_sigma=0, training_status="completed", epoch=100,
+        self.status(run_id=self.run_id, protocol="independent-sigma-privacy-v1", protocol_fixed_model=False,
+                    sigma=256, training_sigma=256, training_status="completed", epoch=100,
                     checkpoint_sha256=metrics["checkpoint_sha256"], model_state_sha256=metrics["model_state_sha256"], best_epoch=2,
-                    sigma_queue=[{"sigma": n, "status": "completed"} for n in SIGMA_VALUES])
-        target = self.root.parent / "블러 강도별 대표 특징맵/7차"
+                    sigma_queue=[{"sigma": n, "status": "completed", "training_status":"completed", "classification_status":"completed", "privacy_status":"completed"} for n in SIGMA_VALUES])
+        target = self.root.parent / "블러 강도별 대표 특징맵/8차"
         target.mkdir(parents=True)
-        selection = json.loads((folder / "fixed_model_selection.json").read_text(encoding="utf-8"))
         keys = ("protocol", "protocol_fixed_model", "training_sigma", "checkpoint_sha256", "model_state_sha256", "checkpoint_epoch", "selected_checkpoint")
-        identity = {key: selection[key] for key in keys}
-        index = dict(identity, schema_version=2, run_id=self.run_id, completed_sigmas=list(SIGMA_VALUES), items=[],
+        index = dict(protocol="independent-sigma-privacy-v1", protocol_fixed_model=False, schema_version=3, run_id=self.run_id, completed_sigmas=list(SIGMA_VALUES), items=[],
                      source_manifest_sha256=file_sha256(self.root / "work/results/dataset_manifest_private.json"),
                      manifest_records_sha256=json.loads((folder / "run_metadata.json").read_text(encoding="utf-8"))["manifest_sha256"],
                      model_source_sha256=file_sha256(self.root / "src/model.py"), data_source_sha256=file_sha256(self.root / "src/data.py"),
                      generator_sha256=file_sha256(self.root / "tools/feature_generator.py"))
         png = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jRZkAAAAASUVORK5CYII=")
         for sigma in SIGMA_VALUES:
+            selection=json.loads((folder / f"sigma_{sigma}_selection.json").read_text(encoding="utf-8"))
+            identity={key:selection[key] for key in keys}
             for class_key in ("Bengin_cases", "Malignant_cases", "Normal_cases"):
                 for stage in range(6):
                     relative = feature_preview_path(sigma, class_key, stage)
@@ -475,7 +551,27 @@
         code, _, body = self.get("/api/feature-previews/image/8-Normal_cases-4")
         self.assertEqual(code, 200)
         self.assertEqual(body, png)
-        for key in ("checkpoint_sha256", "model_source_sha256", "data_source_sha256", "source_manifest_sha256", "manifest_records_sha256", "generator_sha256"):
+        image_id="8-Normal_cases-4"
+        target_item=next(item for item in index["items"] if item["id"]==image_id)
+        for field,value in (("training_sigma",4),("relative_path",feature_preview_path(4,"Normal_cases",4).as_posix()),("checkpoint_sha256","f"*64)):
+            changed=copy.deepcopy(index)
+            next(item for item in changed["items"] if item["id"]==image_id)[field]=value
+            path.write_text(json.dumps(changed),encoding="utf-8")
+            self.assertEqual(self.get("/api/feature-previews/image/"+image_id)[0],404,field)
+        path.write_text(json.dumps(index),encoding="utf-8")
+        status_path=self.root/"work/runtime/status.json"
+        status=json.loads(status_path.read_text(encoding="utf-8"))
+        waiting=copy.deepcopy(status)
+        next(item for item in waiting["sigma_queue"] if item["sigma"]==8)["privacy_status"]="pending"
+        status_path.write_text(json.dumps(waiting),encoding="utf-8")
+        self.assertEqual(self.get("/api/feature-previews/image/"+image_id)[0],404)
+        status_path.write_text(json.dumps(status),encoding="utf-8")
+        image_path=target/target_item["relative_path"]
+        image_path.write_bytes(png+b"changed")
+        self.assertEqual(self.get("/api/feature-previews/image/"+image_id)[0],404)
+        image_path.write_bytes(png)
+        self.assertEqual(self.get("/api/feature-previews/image/3-Normal_cases-4")[0],404)
+        for key in ("model_source_sha256", "data_source_sha256", "source_manifest_sha256", "manifest_records_sha256", "generator_sha256"):
             changed = dict(index, **{key: "f"*64})
             path.write_text(json.dumps(changed), encoding="utf-8")
             result = feature_previews(self.root)
@@ -488,6 +584,33 @@
         index["items"][0]["checkpoint_sha256"] = "f"*64
         path.write_text(json.dumps(index), encoding="utf-8")
         self.assertEqual(feature_previews(self.root)["items"], [])
+
+    def test_ui_displays_measured_zero_privacy_and_clears_pending(self):
+        """실측 0점이 대기로 바뀌거나 강도 전환 뒤 옛 점수가 남는 오류를 잡습니다."""
+        node = shutil.which("node")
+        self.assertIsNotNone(node)
+        script = r"""
+const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
+(async()=>{
+const ids=[...fs.readFileSync('web/index.html','utf8').matchAll(/id="([^"]+)"/g)].map(x=>x[1]);
+const ctx={scale(){},beginPath(){},moveTo(){},lineTo(){},stroke(){},fillText(){},arc(){},fill(){}};
+const element=()=>({textContent:'',children:[],dataset:{},attributes:{},parentElement:{},addEventListener(){},setAttribute(k,v){this.attributes[k]=v;},replaceChildren(...v){this.children=v;},append(...v){this.children.push(...v);},getBoundingClientRect(){return {width:600,height:210};},getContext(){return ctx;},querySelector(s){return s==='small'?this.children[1]:null;}});
+const nodes=Object.fromEntries(ids.map(id=>[id,element()]));
+const sandbox={console,AbortController,setTimeout,clearTimeout,fetch:async()=>{throw Error('unused');},setInterval(){},createPipeline(){return {setSelectedSigma(){},setStatus(){},setPaused(){},setTheme(){}};},document:{getElementById(id){return nodes[id]||null;},createElement:element,querySelectorAll(){return [];},fonts:{ready:Promise.resolve()}},window:{matchMedia(){return {matches:false,addEventListener(){}};},addEventListener(){},ctTheme:{current(){return 'light';}},devicePixelRatio:1}};
+let code=fs.readFileSync('web/app.js','utf8').replace(/^import[^\n]*\n/,'').replace('await document.fonts.ready;','').replace('refresh();setInterval(refresh,3000);','');
+vm.runInNewContext(code+'\nglobalThis.testAPI={drawSelectedResults,privacyPoints,select(s){selectedSigma=s;}};',sandbox);
+for(const [value,want]of [[0,'0.0 / 100'],[100,'100.0 / 100'],[98.85,'98.9 / 100'],[37.45,'37.5 / 100'],[0.05,'0.1 / 100'],[0.15,'0.2 / 100'],[1.2345e-7,'0.0 / 100'],[NaN,'미측정'],[Infinity,'미측정'],[-Infinity,'미측정'],[101,'미측정'],[-1,'미측정'],['0','미측정']])assert.equal(sandbox.testAPI.privacyPoints(value),want);
+sandbox.testAPI.select(8);
+sandbox.testAPI.drawSelectedResults({sigma:8,status:'completed',history:[{sigma:8,epoch:1,train_loss:0,val_loss:0,val_accuracy:1}],metrics:{training_sigma:8,epochs_ran:100,best_epoch:20,eval_optimizer_steps:0,checkpoint_sha256:'a'.repeat(64),test:{accuracy:1,auc:1,loss:0,correct_count:164,n_images:164}},privacy:{score:0,score_version:'gallery-residual-v1',n_queries:164,n_groups:100,gallery_groups:100,chance:0.01,mean_q:1,mean_m:1,raw_joint_residual:0},privacy_status:'completed'});
+assert.equal(nodes.privacyScore?.textContent,'0.0 / 100');assert.equal(nodes.privacyScoreRaw?.textContent,'0');
+sandbox.testAPI.drawSelectedResults({sigma:8,status:'completed',history:[],metrics:{training_sigma:8,epochs_ran:100,best_epoch:20,eval_optimizer_steps:0,checkpoint_sha256:'a'.repeat(64),test:{accuracy:1,auc:1,loss:0,correct_count:164,n_images:164}},privacy_status:'completed',privacy:{score:98.85,score_version:'gallery-residual-v1'}});assert.equal(nodes.privacyScore.textContent,'98.9 / 100');assert.equal(nodes.privacyScoreRaw.textContent,'98.85');assert.match(nodes.selectedTrainingSigma.textContent,/8/);assert.equal(nodes.testAccuracy.textContent,'100.0%');assert.match(nodes.chartTitle.textContent,/8/);
+sandbox.testAPI.select(16);sandbox.testAPI.drawSelectedResults({sigma:16,status:'running',history:[],metrics:null,privacy:null,privacy_status:'pending'});
+assert.equal(nodes.privacyScore.textContent,'미측정');assert.equal(nodes.privacyScoreRaw.textContent,'미측정');assert.equal(nodes.testAccuracy.textContent,'미측정');
+console.log('실측0점·원값·해당강도곡선·강도전환대기4조건PASS');
+})().catch(e=>{console.error(e);process.exitCode=1;});
+"""
+        checked = subprocess.run([node, "-"], input=script, text=True, encoding="utf-8", capture_output=True, timeout=10, cwd=Path(__file__).resolve().parents[1])
+        self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
 
     def test_javascript_syntax_and_real_ui_state_selection(self):
         node = shutil.which("node")
@@ -506,21 +629,21 @@
 function element(){return {textContent:'',children:[],dataset:{},attributes:{},querySelector(selector){if(selector==='small')return this.children[1];return this.children.find(x=>String(x.dataset.sigma)===selector.match(/"(\d+)"/)?.[1]);},parentElement:{},addEventListener(){},setAttribute(k,v){this.attributes[k]=v;},replaceChildren(...v){this.children=v;},append(...v){this.children.push(...v);},getBoundingClientRect(){return {width:600,height:210};},getContext(){return context;}};}
 const nodes=Object.fromEntries(ids.map(id=>[id,element()])),selected=[];
 let fetchCount=0;
-const sandbox={console,AbortController,setTimeout,clearTimeout,fetch:async url=>{fetchCount++;const sigma=Number(url.split('/').at(-1));return {ok:true,json:async()=>({run_id:state.run_id,sigma,history:sigma===0?state.history:[],evaluation_history:[{sigma,validation_loss:0,test_loss:0.25,validation_accuracy:1,test_accuracy:sigma===8?0.5:0.9878048780487805}],metrics:{training_sigma:0,best_epoch:2,epochs_ran:100,eval_optimizer_steps:0,checkpoint_sha256:'a'.repeat(64),test:{accuracy:sigma===8?0.5:0.9878048780487805,auc:0,loss:0,correct_count:162,n_images:164}}})};},
+const sandbox={console,AbortController,setTimeout,clearTimeout,fetch:async url=>{fetchCount++;const sigma=Number(url.split('/').at(-1));return {ok:true,json:async()=>({run_id:state.run_id,sigma,history:state.sigma_queue.some(x=>x.sigma===sigma&&x.classification_status==='completed')?[{sigma,epoch:1,train_loss:0,val_loss:1e-16,val_accuracy:1}]:sigma===state.sigma?state.history:[],metrics:state.sigma_queue.some(x=>x.sigma===sigma&&x.classification_status==='completed')?{training_sigma:sigma,best_epoch:2,epochs_ran:100,eval_optimizer_steps:0,checkpoint_sha256:(sigma===8?'b':'a').repeat(64),test:{accuracy:sigma===8?0.5:0.9878048780487805,auc:0,loss:0,correct_count:162,n_images:164}}:null,privacy:null,privacy_status:'pending'})};},
 createPipeline(){return {setSelectedSigma(...v){selected.push(v);},setStatus(){},setPaused(){},setTheme(){}};},document:{getElementById(id){return nodes[id]||null;},createElement:element,querySelectorAll(){return [];},fonts:{ready:Promise.resolve()}},window:{matchMedia(){return {matches:false,addEventListener(){}};},addEventListener(){},ctTheme:{current(){return 'light';}},devicePixelRatio:1},setInterval(){}};
 let code=fs.readFileSync('web/app.js','utf8').replace(/^import[^\n]*\n/,'').replace('await document.fonts.ready;','').replace('refresh();setInterval(refresh,3000);','');
 vm.runInNewContext(code+'\nglobalThis.testAPI={render,selectSigma,percent};',sandbox);
-const state={run_id:'0123456789abcdef',stage:'training',status:'running',training_status:'running',training_sigma:0,sigma:0,epoch:47,epochs:100,training_policy:{max_epochs:100,early_stopping_enabled:false},learning_rate:0,best_epoch:2,optimizer_steps:58750,history:[{sigma:0,epoch:1,train_loss:0,val_loss:1e-16,val_accuracy:1}],sigma_queue:[{sigma:0,status:'completed'}],_dashboard:{stale:false,process_alive:true},updated_at:'2026-11-20T00:00:00+09:00'};
+const state={run_id:'0123456789abcdef',stage:'training',status:'running',training_status:'running',training_sigma:0,sigma:0,epoch:47,epochs:100,training_policy:{max_epochs:100,early_stopping_enabled:false},learning_rate:0,best_epoch:2,optimizer_steps:58750,history:[{sigma:0,epoch:1,train_loss:0,val_loss:1e-16,val_accuracy:1}],sigma_queue:[{sigma:0,status:'running',training_status:'running',classification_status:'pending',privacy_status:'pending'}],_dashboard:{stale:false,process_alive:true},updated_at:'2026-11-20T00:00:00+09:00'};
 const tick=()=>new Promise(resolve=>setImmediate(resolve));
 sandbox.testAPI.render(state);await tick();
-assert.equal(nodes.testAccuracy.textContent,'미측정');assert.equal(nodes.queueCount.textContent,'0 / 10 평가 완료');
-assert.match(nodes.sigmaLabel.textContent,/한 번의 학습/);assert.match(nodes.latestLoss.textContent,/학습 손실 0/);
-sandbox.testAPI.selectSigma(8);await tick();assert.equal(nodes.testAccuracy.textContent,'미측정');assert.equal(nodes.latestLoss.textContent,'최근 손실 미측정');assert.equal(nodes.chartTitle.textContent,'선택 강도의 고정 모델 평가');
-state.training_status='completed';state.stage='testing';state.checkpoint_sha256='a'.repeat(64);state.evaluation_current_sigma=8;
-sandbox.testAPI.render(state);await tick();assert.equal(nodes.testAccuracy.textContent,'50.0%');assert.equal(nodes.selectedSteps.textContent,'0');assert.equal(nodes.selectedCheckpoint.textContent,'a'.repeat(64));assert.match(nodes.latestLoss.textContent,/시험 손실 0.25/);assert.equal(selected.at(-1)[0],8);
-sandbox.testAPI.selectSigma(0);await tick();assert.equal(nodes.testAccuracy.textContent,'98.8%');assert.equal(nodes.testAccuracyRaw.textContent,'0.9878048780487805');assert.equal(nodes.testAuc.textContent,'0');assert.match(nodes.testCorrectCount.textContent,/162 \/ 164/);assert.match(nodes.chartTitle.textContent,/블러 0/);
+assert.equal(nodes.testAccuracy.textContent,'미측정');assert.equal(nodes.queueCount.textContent,'0 / 10 강도 완료');
+assert.match(nodes.sigmaLabel.textContent,/학습 → 분류 평가/);assert.match(nodes.latestLoss.textContent,/학습 손실 0/);
+sandbox.testAPI.selectSigma(8);await tick();assert.equal(nodes.testAccuracy.textContent,'미측정');assert.equal(nodes.latestLoss.textContent,'최근 손실 미측정');assert.equal(nodes.chartTitle.textContent,'σ 8의 독립 학습 곡선');
+state.training_status='completed';state.stage='testing';state.checkpoint_sha256='a'.repeat(64);state.evaluation_current_sigma=8;state.sigma_queue=[0,8].map(sigma=>({sigma,status:'completed',training_status:'completed',classification_status:'completed',privacy_status:'completed'}));
+sandbox.testAPI.render(state);await tick();assert.equal(nodes.testAccuracy.textContent,'50.0%');assert.equal(nodes.selectedSteps.textContent,'0');assert.equal(nodes.selectedCheckpoint.textContent,'b'.repeat(64));assert.match(nodes.latestLoss.textContent,/학습 손실 0/);assert.equal(selected.at(-1)[0],8);
+sandbox.testAPI.selectSigma(0);await tick();assert.equal(nodes.testAccuracy.textContent,'98.8%');assert.equal(nodes.testAccuracyRaw.textContent,'0.9878048780487805');assert.equal(nodes.testAuc.textContent,'0');assert.match(nodes.testCorrectCount.textContent,/162 \/ 164/);assert.match(nodes.chartTitle.textContent,/σ 0/);
 assert.equal(sandbox.testAPI.percent(0),'0.0%');assert.equal(sandbox.testAPI.percent(1),'100.0%');assert.equal(sandbox.testAPI.percent(0.99999),'100.0%');
-state.run_id='fedcba9876543210';sandbox.testAPI.render(state);assert.equal(nodes.testAccuracy.textContent,'미측정');assert.equal(nodes.selectedCheckpoint.textContent,'고정 모델 평가 대기');
+state.run_id='fedcba9876543210';sandbox.testAPI.render(state);assert.equal(nodes.testAccuracy.textContent,'미측정');assert.equal(nodes.selectedCheckpoint.textContent,'선택 강도의 모델 선정 대기');
 state.status='interrupted';state.stage='interrupted';sandbox.testAPI.render(state);assert.equal(nodes.motion.disabled,true);assert.equal(nodes.badge.textContent,'중단');
 console.log('강도 선택·학습 중 대기·추가 갱신0·동일 모델·원값/반올림·실행 전환·중단 상태 통과');
 })().catch(error=>{console.error(error);process.exitCode=1;});
````

## tests/test_fixed_protocol.py

| 구분 | 이전 | 이후 |
| --- | --- | --- |
| 상태 | 삭제 | 삭제 |
| 바이트 | 15038 | 0 |
| SHA-256 | 1c8cdefd44d470eab119ac8c9b79c1b56f60bcdd7b18803b8869166336e071c6 | 없음 |

````diff
--- a/tests/test_fixed_protocol.py
+++ b/tests/test_fixed_protocol.py
@@ -1,256 +0,0 @@
-"""단일 σ0 학습과 동결 평가의 경계 및 실패 경로를 합성 CPU 입력으로 검사합니다."""
-
-import copy
-import hashlib
-import importlib
-import json
-import os
-from pathlib import Path
-import tempfile
-import unittest
-from unittest import mock
-
-os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
-
-
-class FixedProtocolTests(unittest.TestCase):
-    def test_prepare_and_smoke_refuse_active_lock_without_changing_files(self):
-        import run_training
-        with tempfile.TemporaryDirectory() as directory:
-            root = Path(directory)
-            runtime = root / "work/runtime"
-            runtime.mkdir(parents=True)
-            status = runtime / "status.json"
-            lock = runtime / "recovery.lock"
-            status.write_text(json.dumps({"phase": "training", "epoch": 47, "pid": 123}), encoding="utf-8")
-            lock.write_text("이미 있는 잠금", encoding="utf-8")
-            before = {path: path.read_bytes() for path in [status, lock]}
-            with mock.patch.object(run_training, "ROOT", root):
-                for operation in [lambda: run_training.prepare({}), lambda: run_training.smoke({}, "cuda")]:
-                    with self.assertRaisesRegex(RuntimeError, "잠금"):
-                        operation()
-                    self.assertEqual({path: path.read_bytes() for path in before}, before)
-
-    def test_unstarted_guard_refuses_progress_and_accepts_only_empty_ready(self):
-        import run_training
-        from src.state import StatusWriter
-        with tempfile.TemporaryDirectory() as directory:
-            root = Path(directory)
-            status = StatusWriter(root, {"epochs": 100, "sigmas": [0, 1]})
-            status.update(phase="preparing", stage="ready", status="ready", pid=None)
-            run_training.require_unstarted(root)
-            path = root / "work/runtime/status.json"
-            for changes in [{"phase": "training", "epoch": 47, "pid": 123}, {"history": [{"epoch": 1}]}, {"training_status": "completed"}]:
-                altered = {**status.data, **changes}
-                path.write_text(json.dumps(altered), encoding="utf-8")
-                before = path.read_bytes()
-                with self.assertRaises(RuntimeError):
-                    run_training.require_unstarted(root)
-                self.assertEqual(before, path.read_bytes())
-
-    def test_status_marks_all_sigmas_as_evaluation_pending(self):
-        from src.state import StatusWriter
-        with tempfile.TemporaryDirectory() as directory:
-            status = StatusWriter(directory, {"epochs": 100, "sigmas": [0, 1, 4], "training_sigma": 0})
-            self.assertTrue(status.data.get("protocol_fixed_model"), "고정 모델 프로토콜 상태가 없습니다.")
-            self.assertEqual(status.data["training_sigma"], 0)
-            self.assertEqual(status.data["training_status"], "pending")
-            self.assertTrue(all(row["status"] == "pending" for row in status.data["sigma_queue"]))
-
-    def test_frozen_state_digest_includes_batch_norm_buffers(self):
-        import torch
-        from src import training
-        self.assertTrue(hasattr(training, "tensor_state_digest"), "전체 state 동결 검사가 없습니다.")
-        model = torch.nn.BatchNorm2d(2)
-        before = training.tensor_state_digest(model.state_dict())
-        model.running_mean[0] += 1
-        self.assertNotEqual(before, training.tensor_state_digest(model.state_dict()))
-
-    def test_immutable_model_eval_replaces_blur_for_every_sigma(self):
-        with tempfile.TemporaryDirectory() as directory:
-            fixture = SyntheticRun(Path(directory))
-            state, models = fixture.execute()
-            self.assertEqual(len(models), 2, "학습 모델 하나와 동결 평가 모델 하나만 만듭니다.")
-            self.assertEqual(models[0].training_sigmas, [0] * 100)
-            self.assertEqual(state["epoch"], 100)
-            self.assertTrue(all(row["status"] == "completed" for row in state["sigma_queue"]))
-            self.assertEqual(len(models[1].blur_objects), 10)
-            self.assertEqual(len({id(value) for value in models[1].blur_objects}), 10)
-            from src.identity import validate_fixed_result, SIGMAS
-            values = [json.loads((fixture.result_dir / f"sigma_{sigma}_metrics.json").read_text(encoding="utf-8")) for sigma in SIGMAS]
-            for value in values:
-                validate_fixed_result(fixture.root, value)
-                self.assertEqual(value["eval_optimizer_steps"], 0)
-                self.assertEqual(value["state_digest_before"], value["state_digest_after"])
-            self.assertEqual(len({value["checkpoint_sha256"] for value in values}), 1)
-            self.assertEqual(len({value["model_state_sha256"] for value in values}), 1)
-            self.assertEqual(fixture.val_training_sigmas, [0] * 100)
-            for key, invalid in [("training_sigma", False), ("epochs_ran", 100.0), ("eval_optimizer_steps", 1), ("checkpoint_sha256", "0" * 64)]:
-                with self.subTest(tamper=key), self.assertRaises(ValueError):
-                    validate_fixed_result(fixture.root, {**values[0], key: invalid})
-            prediction = fixture.root / values[0]["prediction_files"]["test"]["relative_path"]
-            original = prediction.read_bytes()
-            prediction.write_bytes(original + b"tampered")
-            with self.assertRaises(ValueError):
-                validate_fixed_result(fixture.root, values[0])
-            prediction.write_bytes(original)
-            checkpoint = fixture.root / values[0]["selected_checkpoint"]
-            checkpoint.write_bytes(checkpoint.read_bytes() + b"tampered")
-            with self.assertRaises(ValueError):
-                validate_fixed_result(fixture.root, values[0])
-
-    def test_identity_is_standard_library_and_refuses_other_protocol(self):
-        from src.identity import validate_config
-        config = json.loads((Path(__file__).resolve().parents[1] / "config.json").read_text(encoding="utf-8"))
-        for key, value in [("training_sigma", False), ("epochs", 100.0), ("training_sigma", 4), ("early_stopping_enabled", True), ("protocol", "adaptive")]:
-            invalid = {**config, key: value}
-            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
-                validate_config(invalid)
-        # stdlib helper가 Torch를 import하지 않는지 새 프로세스로 확인합니다.
-        import subprocess
-        import sys
-        result = subprocess.run([sys.executable, "-B", "-c", "import src.identity,sys; assert 'torch' not in sys.modules"],
-                                cwd=Path(__file__).resolve().parents[1], capture_output=True, timeout=10)
-        self.assertEqual(result.returncode, 0, result.stderr)
-
-    def test_resume_preserves_rng_optimizer_and_completed_epoch(self):
-        from src import training
-        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
-            full = SyntheticRun(Path(a))
-            full_state, _ = full.execute()
-            resumed = SyntheticRun(Path(b))
-            original_save = training._save_checkpoint
-            def interrupt_after_complete_epoch(path, payload):
-                original_save(path, payload)
-                if Path(path).name == "sigma_0_last.pt" and payload["epoch"] == 3:
-                    raise RuntimeError("제어된 완료 회차 중단")
-            with mock.patch.object(training, "_save_checkpoint", side_effect=interrupt_after_complete_epoch):
-                with self.assertRaisesRegex(RuntimeError, "제어된"):
-                    resumed.execute()
-            self.assertFalse(list(resumed.result_dir.glob("sigma_*_metrics.json")))
-            state, models = resumed.execute()
-            self.assertEqual(len(models[0].training_sigmas), 97)
-            self.assertEqual(state["optimizer_steps"], full_state["optimizer_steps"])
-            first = training.checkpoint_load(full.checkpoint_dir / "sigma_0_last.pt", full.run_id)
-            second = training.checkpoint_load(resumed.checkpoint_dir / "sigma_0_last.pt", resumed.run_id)
-            self.assertEqual(training.tensor_state_digest(first["model"]), training.tensor_state_digest(second["model"]))
-            self.assertEqual(first["scheduler"], second["scheduler"])
-            self.assertEqual(first["training_control"], second["training_control"])
-
-    def test_eval_rejects_batch_norm_buffer_mutation(self):
-        from src import training
-        real_evaluate = training.evaluate
-        def corrupt_buffer(model, *args, **kwargs):
-            result = real_evaluate(model, *args, **kwargs)
-            if not any(p.requires_grad for p in model.parameters()):
-                model.cloud[0].running_mean.add_(1)
-            return result
-        with tempfile.TemporaryDirectory() as directory:
-            fixture = SyntheticRun(Path(directory))
-            with mock.patch.object(training, "evaluate", side_effect=corrupt_buffer), self.assertRaisesRegex(ValueError, "BN"):
-                fixture.execute()
-            self.assertFalse(list(fixture.result_dir.glob("sigma_*_metrics.json")))
-
-    def test_safe_path_rejects_outside_and_checkpoint_symlink(self):
-        from src.identity import safe_path
-        with tempfile.TemporaryDirectory() as directory:
-            root = Path(directory)
-            with self.assertRaises(ValueError):
-                safe_path(root, "../outside")
-            target = root / "target"
-            target.write_text("합성", encoding="utf-8")
-            link = root / "linked"
-            try:
-                link.symlink_to(target)
-            except OSError:
-                self.skipTest("이 Windows 세션은 심볼릭 링크 생성 권한이 없습니다.")
-            with self.assertRaises(ValueError):
-                safe_path(root, "linked")
-
-
-class SyntheticRun:
-    """실제 CT·GPU 없이 같은 생산 학습 루프를100회 통과시키는 합성 fixture입니다."""
-    def __init__(self, root):
-        from src.identity import _run_identity
-        self.root = root
-        self.config = json.loads((Path(__file__).resolve().parents[1] / "config.json").read_text(encoding="utf-8"))
-        self.config["cpu_threads"] = 1
-        rows = [{"path": "synthetic0", "relative_path": "합성0", "label": 0, "source_class": "OK"},
-                {"path": "synthetic1", "relative_path": "합성1", "label": 1, "source_class": "NG"}]
-        records_sha = hashlib.sha256(json.dumps(rows, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()
-        self.manifest = {"records": rows, "splits": {name: copy.deepcopy(rows) for name in ["train", "validation", "test"]},
-                         "summary": {"patient_id_available": False}, "manifest_sha256": records_sha}
-        reference = root / self.config["expected_reference_manifest"]
-        reference.parent.mkdir(parents=True)
-        reference.write_text(json.dumps(self.manifest, ensure_ascii=False), encoding="utf-8")
-        self.config["expected_reference_manifest_sha256"] = hashlib.sha256(reference.read_bytes()).hexdigest()
-        self.config["expected_reference_records_sha256"] = records_sha
-        (root / "config.json").write_text(json.dumps(self.config, ensure_ascii=False), encoding="utf-8")
-        (root / "run_training.py").write_text("# 합성 검사\n", encoding="utf-8")
-        (root / "src").mkdir()
-        (root / "src/fixture.py").write_text("# 합성 검사\n", encoding="utf-8")
-        self.run_id, _ = _run_identity(root, self.config, records_sha)
-        self.result_dir = root / "work/results" / ("run_" + self.run_id)
-        self.result_dir.mkdir(parents=True)
-        (root / "work/results/dataset_manifest_private.json").write_text(json.dumps(self.manifest, ensure_ascii=False), encoding="utf-8")
-        self.checkpoint_dir = root / "work/checkpoints" / ("run_" + self.run_id)
-        self.val_training_sigmas = []
-
-    def execute(self):
-        import torch
-        from src import training
-        from src.model import GaussianDCTBlur
-        from src.state import StatusWriter
-        models = []
-        class TinyModel(torch.nn.Module):
-            def __init__(self, sigma=0, **kwargs):
-                super().__init__()
-                self.edge = torch.nn.Conv2d(3, 2, 1, bias=False).requires_grad_(False)
-                self.blur = GaussianDCTBlur(sigma)
-                self.cloud = torch.nn.Sequential(torch.nn.BatchNorm2d(2), torch.nn.ReLU(), torch.nn.AdaptiveAvgPool2d(1), torch.nn.Flatten(), torch.nn.Linear(2, 1))
-                self.register_buffer("rgb_mean", torch.zeros(1, 3, 1, 1))
-                self.register_buffer("rgb_std", torch.ones(1, 3, 1, 1))
-                self.training_sigmas, self.blur_objects = [], []
-                models.append(self)
-            def train(self, mode=True):
-                super().train(mode)
-                self.cloud[0].eval()
-                return self
-            def forward(self, images):
-                if self.training:
-                    self.training_sigmas.append(self.blur.sigma)
-                elif not any(p.requires_grad for p in self.parameters()) and self.blur not in self.blur_objects:
-                    self.blur_objects.append(self.blur)
-                return self.cloud(self.blur(self.edge(images))).squeeze(1)
-        class TinyDataset:
-            def __init__(self, records, image_size, training=False, **kwargs):
-                self.records = records
-                self.training = training
-            def __len__(self):
-                return 10000 if self.training else 2
-            def set_epoch(self, epoch):
-                self.epoch = epoch
-        def loader(dataset, config, device):
-            target = torch.tensor([0., 1.]).repeat(5000 if dataset.training else 1)
-            class TinyLoader(list):
-                pass
-            result = TinyLoader([(target[:, None, None, None].expand(-1, 3, 2, 2).clone(), target)])
-            result.dataset = dataset
-            return result
-        real_evaluate = training.evaluate
-        def record_evaluate(model, *args, **kwargs):
-            if any(p.requires_grad for p in model.parameters()):
-                self.val_training_sigmas.append(model.blur.sigma)
-            return real_evaluate(model, *args, **kwargs)
-        with mock.patch.object(training, "prepare_dataset", return_value=self.manifest), \
-             mock.patch.object(training, "CTDataset", TinyDataset), mock.patch.object(training, "_loader", side_effect=loader), \
-             mock.patch.object(training, "SplitResNet50", TinyModel), \
-             mock.patch.object(training, "precision_policy", return_value={"name": "fp32", "dtype": torch.float32, "autocast_enabled": False, "use_grad_scaler": False}), \
-             mock.patch.object(training, "evaluate", side_effect=record_evaluate):
-            state = StatusWriter(self.root, self.config)
-            result = training.run_training(self.config, self.root, state, "cpu")
-        return result, models
-
-
-if __name__ == "__main__":
-    unittest.main()
````

## tests/test_independent_privacy.py

| 구분 | 이전 | 이후 |
| --- | --- | --- |
| 상태 | 추가 | 추가 |
| 바이트 | 0 | 26115 |
| SHA-256 | 없음 | e5fb17719c0374a39ee02eff8a529092a85fb35315514a3a1cc67dff40917ad9 |

````diff
--- a/tests/test_independent_privacy.py
+++ b/tests/test_independent_privacy.py
@@ -0,0 +1,419 @@
+"""실제 CT·GPU 없이 새 독립학습과 조건부 점수의 경계를 검사합니다."""
+
+import copy
+import hashlib
+import json
+import os
+from pathlib import Path
+import tempfile
+import unittest
+from unittest import mock
+
+os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
+
+
+class IndependentPrivacyTests(unittest.TestCase):
+    def test_score_controls_ties_and_expectation_order(self):
+        import numpy as np
+        from src.privacy import score_gallery
+        d = np.array([[0., 1., 4.], [1., 0., 1.], [4., 1., 0.]])
+        exact = score_gallery(d, [[0], [1], [2]])
+        self.assertEqual(exact["score"], 0.)
+        self.assertEqual(exact["fractional_top1"], 1.)
+        constant = score_gallery(d, [[0, 1, 2]] * 3)
+        self.assertAlmostEqual(constant["score"], 100.)
+        self.assertAlmostEqual(constant["fractional_top1"], 1/3)
+        # 첫 행 clip(1/(5/3))=.6, clip(4/(5/3))=1: 먼저 clip한 평균은.8입니다.
+        tied = score_gallery(d, [[1, 2], [1], [2]])
+        self.assertAlmostEqual(tied["per_group"][0]["attack_residual"], .8)
+        self.assertAlmostEqual(tied["T_attack"], .8/3)
+        self.assertAlmostEqual(tied["T_prior"], (1.6+2+1.6)/9)
+
+    def test_invalid_gallery_and_unmatched_query_are_errors(self):
+        import numpy as np
+        from src.privacy import score_gallery, match_hashes
+        for d in [np.zeros((1, 1)), np.zeros((2, 2)), np.array([[0., np.nan], [np.nan, 0.]])]:
+            with self.assertRaises(ValueError):
+                score_gallery(d, [[0]] * len(d))
+        with self.assertRaises(ValueError):
+            match_hashes(["a", "b"], ["a", "missing"])
+        self.assertEqual(match_hashes(["a", "a", "b"], ["a", "b"]), [[0, 1], [2]])
+
+    def test_same_candidate_and_monotonic_score(self):
+        import numpy as np
+        from src.privacy import score_gallery
+        d = np.array([[0., 1., 4.], [1., 0., 1.], [4., 1., 0.]])
+        weak = score_gallery(d, [[2], [0], [0]])
+        strong = score_gallery(d, [[1], [1], [2]])
+        self.assertLess(strong["score"], weak["score"])
+        self.assertEqual(strong["exact_return_groups"], 2)
+
+    def test_preprocessing_groups_and_feature_hash_header(self):
+        import numpy as np
+        import torch
+        from src.privacy import group_pixels, feature_hash, pairwise_mse
+        x = np.array([[[0., 1.]], [[0., 1.]], [[1., 0.]]], dtype=np.float32)
+        representatives, groups = group_pixels(x)
+        self.assertEqual(representatives, [0, 2])
+        self.assertEqual(groups, [[0, 1], [2]])
+        np.testing.assert_array_equal(pairwise_mse(x[representatives]), [[0., 1.], [1., 0.]])
+        a = torch.zeros(1, 2, 2, dtype=torch.float32)
+        self.assertNotEqual(feature_hash(a, "pipeline-a"), feature_hash(a, "pipeline-b"))
+        self.assertNotEqual(feature_hash(a, "pipeline-a"), feature_hash(a.reshape(2, 1, 2), "pipeline-a"))
+
+    def test_prepare_guard_is_non_mutating(self):
+        import run_training
+        with tempfile.TemporaryDirectory() as directory:
+            root = Path(directory)
+            path = root / "work/runtime/status.json"
+            path.parent.mkdir(parents=True)
+            path.write_text('{"stage":"training","epoch":77,"pid":123}', encoding="utf-8")
+            before = path.read_bytes()
+            with mock.patch.object(run_training, "ROOT", root):
+                with self.assertRaises(RuntimeError):
+                    run_training.prepare({})
+            self.assertEqual(path.read_bytes(), before)
+            lock = path.parent / "recovery.lock"
+            lock.write_text("오래된 잠금도 보존", encoding="utf-8")
+            with self.assertRaises(RuntimeError):
+                run_training.require_unstarted(root)
+            self.assertTrue(lock.exists())
+
+    def test_real_status_storage_and_source_metrics(self):
+        from src.state import StatusWriter
+        from src.training import per_source_metrics, binary_metrics
+        with tempfile.TemporaryDirectory() as directory:
+            root = Path(directory)
+            state = StatusWriter(root, {"epochs":100, "sigmas":[0,1]})
+            state.update(stage="training", epoch=3, sigma=1, message="실제 한글 상태 저장")
+            self.assertEqual(json.loads((root / "work/runtime/status.json").read_text(encoding="utf-8")), state.data)
+            state.event("실제 회차 기록", {"epoch":3})
+            raw = (root / "work/runtime/events.jsonl").read_bytes()
+            self.assertTrue(raw.endswith(b"\n"))
+            self.assertEqual(json.loads(raw.decode())['details'], {"epoch":3})
+        rows = [{"source_class":"A"},{"source_class":"A"},{"source_class":"B"},{"source_class":"B"}]
+        values = per_source_metrics(rows, [0,1,0,1], [.1,.8,.7,.9], [-2.,1.,1.,2.])
+        self.assertEqual(values["A"]["confusion_matrix"], [[1,0],[0,1]])
+        self.assertEqual(values["B"]["confusion_matrix"], [[0,1],[0,1]])
+        self.assertEqual(binary_metrics([0,1,0,1], [.1,.8,.7,.9])["n_correct"], 3)
+
+    def test_independent_models_100_epochs_and_identity(self):
+        from src.identity import SIGMAS, validate_result, validate_privacy_result
+        with tempfile.TemporaryDirectory() as directory:
+            fixture = SyntheticRun(Path(directory))
+            state, models = fixture.execute()
+            trained = [m for m in models if m.training_sigmas]
+            self.assertEqual(len(trained), 10)
+            self.assertEqual([m.training_sigmas for m in trained], [[s] * 100 for s in SIGMAS])
+            self.assertEqual(len({m.initial_digest for m in trained}), 1)
+            self.assertEqual([r["status"] for r in state["sigma_queue"]], ["completed"] * 10)
+            self.assertEqual(fixture.privacy_order, SIGMAS)
+            for sigma in SIGMAS:
+                result = json.loads((fixture.result_dir / f"sigma_{sigma}_metrics.json").read_text(encoding="utf-8"))
+                validate_result(fixture.root, result)
+                self.assertEqual(result["training_sigma"], sigma)
+                self.assertEqual(result["epochs_ran"], 100)
+                self.assertEqual(result["best_epoch"], 1)
+                self.assertEqual(fixture.checkpoint_writes.count((f"sigma_{sigma}_best.pt", 1)), 1)
+                self.assertEqual(sum(name == f"sigma_{sigma}_best.pt" for name, _ in fixture.checkpoint_writes), 1)
+                self.assertEqual([epoch for name, epoch in fixture.checkpoint_writes if name == f"sigma_{sigma}_last.pt"], list(range(1,101)))
+                history = json.loads((fixture.result_dir / f"sigma_{sigma}_history.json").read_text(encoding="utf-8"))
+                self.assertEqual(result["best_epoch"], min(history, key=lambda row: row["val_loss"])["epoch"])
+                self.assertEqual(result["eval_optimizer_steps"], 0)
+                private = json.loads((fixture.result_dir / f"sigma_{sigma}_privacy.json").read_text(encoding="utf-8"))
+                validate_privacy_result(fixture.root, private)
+                if sigma in [0,256]:
+                    for key, invalid in [("privacy_source_sha256", "f" * 64), ("packet_batch_size", 8), ("score", 100.)]:
+                        with self.assertRaises(ValueError):
+                            validate_privacy_result(fixture.root, {**private, key: invalid})
+                    for key, invalid in [("training_sigma", False), ("checkpoint_sha256", "0" * 64)]:
+                        with self.assertRaises(ValueError):
+                            validate_result(fixture.root, {**result, key: invalid})
+            again, new_models = fixture.execute()
+            self.assertFalse(any(m.training_sigmas for m in new_models))
+            self.assertEqual(again["status"], "completed")
+            result = json.loads((fixture.result_dir / "sigma_0_metrics.json").read_text(encoding="utf-8"))
+            checkpoint = fixture.root / result["selected_checkpoint"]
+            checkpoint.write_bytes(checkpoint.read_bytes() + b"tampered")
+            with self.assertRaises(ValueError):
+                validate_result(fixture.root, result)
+
+    def test_resume_completed_epoch_and_privacy_failure(self):
+        from src import training
+        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
+            full = SyntheticRun(Path(a))
+            full.execute(sigmas=[0])
+            resumed = SyntheticRun(Path(b))
+            original = training._save_checkpoint
+            def stop(path, value):
+                original(path, value)
+                if Path(path).name == "sigma_0_last.pt" and value["epoch"] == 3:
+                    raise RuntimeError("제어된 회차 완료 중단")
+            with mock.patch.object(training, "_save_checkpoint", side_effect=stop):
+                with self.assertRaisesRegex(RuntimeError, "제어된"):
+                    resumed.execute(sigmas=[0])
+            _, models = resumed.execute(sigmas=[0])
+            self.assertEqual(len(models[0].training_sigmas), 97)
+            x = training.checkpoint_load(full.checkpoint_dir / "sigma_0_last.pt", full.run_id, 0)
+            y = training.checkpoint_load(resumed.checkpoint_dir / "sigma_0_last.pt", resumed.run_id, 0)
+            self.assertEqual(training.tensor_state_digest(x["model"]), training.tensor_state_digest(y["model"]))
+            self.assertEqual(x["scheduler"], y["scheduler"])
+            self.assertEqual(x["training_control"], y["training_control"])
+        with tempfile.TemporaryDirectory() as directory:
+            fixture = SyntheticRun(Path(directory))
+            with mock.patch.object(training, "run_privacy", side_effect=RuntimeError("제어된 공격 실패")):
+                with self.assertRaisesRegex(RuntimeError, "공격 실패"):
+                    fixture.execute(patch_privacy=False, sigmas=[0, 1])
+            self.assertTrue((fixture.result_dir / "sigma_0_metrics.json").exists())
+            self.assertFalse((fixture.checkpoint_dir / "sigma_1_last.pt").exists())
+            _, models = fixture.execute(sigmas=[0, 1])
+            self.assertFalse(any(m.training_sigmas and m.blur.sigma == 0 for m in models))
+
+    def test_restore_all_rng_next_cpu_samples(self):
+        import random
+        import numpy as np
+        import torch
+        from src.training import numpy_rng_state, restore_all_rng
+        random.seed(314)
+        np.random.seed(314)
+        torch.manual_seed(314)
+        saved = {"python_rng_state":random.getstate(), "numpy_rng_state":numpy_rng_state(),
+                 "torch_rng_state":torch.get_rng_state().clone(), "cuda_rng_state":[]}
+        expected = (random.random(), np.random.random(4), torch.rand(4))
+        for _ in range(17):
+            random.random()
+            np.random.random()
+            torch.rand(1)
+        restore_all_rng(saved, torch.device("cpu"))
+        actual = (random.random(), np.random.random(4), torch.rand(4))
+        self.assertEqual(actual[0], expected[0])
+        np.testing.assert_array_equal(actual[1], expected[1])
+        self.assertTrue(torch.equal(actual[2], expected[2]))
+
+    def test_identity_stdlib_and_protocol_validation(self):
+        import subprocess
+        import sys
+        from src.identity import validate_config, safe_path
+        root = Path(__file__).resolve().parents[1]
+        config = json.loads((root / "config.json").read_text(encoding="utf-8"))
+        validate_config(config)
+        for key, invalid in [("protocol_fixed_model", True), ("epochs", 100.), ("early_stopping_enabled", True)]:
+            with self.assertRaises(ValueError):
+                validate_config({**config, key: invalid})
+        with self.assertRaises(ValueError):
+            safe_path(root, "../outside")
+        result = subprocess.run([sys.executable, "-B", "-c", "import src.identity,sys; assert 'torch' not in sys.modules"], cwd=root, capture_output=True, timeout=10)
+        self.assertEqual(result.returncode, 0, result.stderr)
+
+    def test_actual_cpu_model_shared_feature_path_and_frozen_bn(self):
+        import torch
+        from src.model import SplitResNet50, GaussianDCTBlur
+        from src.training import seed_everything, tensor_state_digest, build_optimizer_scheduler
+        root = Path(__file__).resolve().parents[1]
+        config = json.loads((root / "config.json").read_text(encoding="utf-8"))
+        seed_everything(42, 1)
+        first = SplitResNet50(sigma=4, pretrained=True, weights_path=config["initial_weights_path"], expected_weights_sha256=config["initial_weights_sha256"])
+        first.train()
+        self.assertFalse(first.edge.training)
+        self.assertTrue(all(not m.training for m in first.modules() if isinstance(m, torch.nn.BatchNorm2d)))
+        self.assertTrue(all(not p.requires_grad for p in first.edge.parameters()))
+        optimizer, _ = build_optimizer_scheduler([p for p in first.parameters() if p.requires_grad], config)
+        self.assertEqual(len(optimizer.state), 0)
+        x = torch.rand(1, 3, 16, 16)
+        with torch.inference_mode():
+            actual = first.transmitted_features(x)
+            expected = GaussianDCTBlur(4)(first.edge((x-first.rgb_mean)/first.rgb_std))
+        self.assertTrue(torch.equal(actual, expected))
+        before = tensor_state_digest(first.state_dict())
+        seed_everything(42, 1)
+        second = SplitResNet50(sigma=256, pretrained=True, weights_path=config["initial_weights_path"], expected_weights_sha256=config["initial_weights_sha256"])
+        self.assertEqual(before, tensor_state_digest(second.state_dict()))
+
+    def test_actual_privacy_file_pipeline_and_constant_feature_control(self):
+        import torch
+        from src.privacy import run_privacy
+        from src.model import GaussianDCTBlur
+        from src.training import tensor_state_digest
+        from src.identity import PROTOCOL, _run_identity, result_binding, validate_privacy_result
+        from src.state import atomic_json
+        class TinyTransmitter(torch.nn.Module):
+            def __init__(self):
+                super().__init__()
+                self.edge = torch.nn.Conv2d(3, 1, 1, bias=False)
+                with torch.no_grad():
+                    self.edge.weight.fill_(1/3)
+                self.blur = GaussianDCTBlur(4)
+                self.calls = 0
+            def transmitted_features(self, x):
+                self.calls += 1
+                return self.blur(self.edge(x)[..., ::256, ::256])
+        for constant in [False, True]:
+            with self.subTest(constant=constant), tempfile.TemporaryDirectory() as directory:
+                fixture = SyntheticRun(Path(directory), real_images=True)
+                run_id, settings = _run_identity(fixture.root, fixture.config, fixture.manifest["manifest_sha256"])
+                metadata = {**settings, "run_id":run_id, "protocol":PROTOCOL, "protocol_fixed_model":False}
+                atomic_json(fixture.result_dir / "run_metadata.json", metadata)
+                model = TinyTransmitter().eval().requires_grad_(False)
+                if constant:
+                    with torch.no_grad():
+                        model.edge.weight.zero_()
+                before = tensor_state_digest(model.state_dict())
+                fixture.checkpoint_dir.mkdir(parents=True)
+                checkpoint = fixture.checkpoint_dir / "sigma_4_best.pt"
+                checkpoint.write_bytes(b"known-synthetic-only")
+                selection = {"run_id":run_id, "protocol":PROTOCOL, "protocol_fixed_model":False, "sigma":4, "training_sigma":4,
+                             "epochs_ran":100, "best_epoch":1, "checkpoint_epoch":1,
+                             "selected_checkpoint":checkpoint.relative_to(fixture.root).as_posix(),
+                             "checkpoint_sha256":hashlib.sha256(checkpoint.read_bytes()).hexdigest(),
+                             "model_state_sha256":before, **result_binding(fixture.root,metadata)}
+                atomic_json(fixture.result_dir / "sigma_4_selection.json", selection)
+                value = run_privacy(model, fixture.manifest["splits"]["test"], fixture.root, run_id, selection)
+                validate_privacy_result(fixture.root, value)
+                self.assertEqual(value["score"], 100. if constant else 0.)
+                self.assertEqual(model.calls, 4, "후보2개와 별도 쿼리2개를 각각 계산해야 합니다.")
+                self.assertFalse(any(m.training for m in model.modules()))
+                self.assertEqual(before, tensor_state_digest(model.state_dict()))
+                raw = json.loads((fixture.root / value["raw_file"]["relative_path"]).read_text(encoding="utf-8"))
+                self.assertEqual(raw["per_group"][0]["candidates"], [0,1] if constant else [0])
+                if not constant:
+                    from src import privacy
+                    before_file = (fixture.root / value["raw_file"]["relative_path"]).read_bytes()
+                    original_hash, count = privacy.feature_hash, [0]
+                    def mismatch(tensor, pipeline):
+                        count[0] += 1
+                        result = original_hash(tensor, pipeline)
+                        return result if count[0] <= 2 else "재현불일치" + result
+                    with mock.patch.object(privacy, "feature_hash", side_effect=mismatch), self.assertRaisesRegex(ValueError, "사전"):
+                        run_privacy(model, fixture.manifest["splits"]["test"], fixture.root, run_id, selection)
+                    self.assertEqual(before_file, (fixture.root / value["raw_file"]["relative_path"]).read_bytes())
+
+
+class SyntheticRun:
+    """실제 생산 루프·저장·재개는 유지하고 대형 모델과 원영상만 합성으로 대체합니다."""
+    def __init__(self, root, real_images=False):
+        from src.identity import _run_identity
+        self.root = root
+        self.config = json.loads((Path(__file__).resolve().parents[1] / "config.json").read_text(encoding="utf-8"))
+        self.config["cpu_threads"] = 1
+        self.config["initial_weights_path"] = "work/reference/합성초기값.bin"
+        self.config["expected_reference_manifest"] = "work/reference/dataset_manifest_private.json"
+        rows = [{"path": "synthetic0", "relative_path": "합성0", "label": 0, "source_class": "OK"}, {"path": "synthetic1", "relative_path": "합성1", "label": 1, "source_class": "NG"}]
+        if real_images:
+            from PIL import Image
+            folder = root / "합성원본"
+            folder.mkdir()
+            for i, row in enumerate(rows):
+                path = folder / f"합성{i}.png"
+                Image.new("L", (4,4), 255*i).save(path)
+                row.update(path=str(path), relative_path=path.name, byte_sha256=hashlib.sha256(path.read_bytes()).hexdigest())
+        records_sha = hashlib.sha256(json.dumps(rows, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
+        self.manifest = {"records": rows, "splits": {n: copy.deepcopy(rows) for n in ["train", "validation", "test"]}, "summary": {}, "manifest_sha256": records_sha}
+        reference = root / self.config["expected_reference_manifest"]
+        reference.parent.mkdir(parents=True)
+        (root / self.config["initial_weights_path"]).write_bytes(b"synthetic-only")
+        self.config["initial_weights_sha256"] = hashlib.sha256(b"synthetic-only").hexdigest()
+        reference.write_text(json.dumps(self.manifest, ensure_ascii=False), encoding="utf-8")
+        self.config["expected_reference_manifest_sha256"] = hashlib.sha256(reference.read_bytes()).hexdigest()
+        self.config["expected_reference_records_sha256"] = records_sha
+        # 실제 외부 원본 경로가 합성 fixture의 어느 출력에도 섞이지 않게 고정합니다.
+        self.config["dataset_root"] = str(root / "합성원본")
+        (root / "config.json").write_text(json.dumps(self.config, ensure_ascii=False), encoding="utf-8")
+        (root / "run_training.py").write_text("# 합성\n", encoding="utf-8")
+        (root / "src").mkdir()
+        for source in (Path(__file__).resolve().parents[1] / "src").glob("*.py"):
+            (root / "src" / source.name).write_bytes(source.read_bytes())
+        self.run_id, _ = _run_identity(root, self.config, records_sha)
+        self.result_dir = root / "work/results" / ("run_" + self.run_id)
+        self.result_dir.mkdir(parents=True)
+        (root / "work/results/dataset_manifest_private.json").write_text(json.dumps(self.manifest, ensure_ascii=False), encoding="utf-8")
+        self.checkpoint_dir = root / "work/checkpoints" / ("run_" + self.run_id)
+        self.privacy_order = []
+        self.checkpoint_writes = []
+
+    def execute(self, patch_privacy=True, sigmas=None):
+        import torch
+        from src import training
+        from src.model import GaussianDCTBlur
+        from src.state import StatusWriter
+        models = []
+        class TinyModel(torch.nn.Module):
+            def __init__(self, sigma=0, **kwargs):
+                super().__init__()
+                self.blur = GaussianDCTBlur(sigma)
+                self.head = torch.nn.Linear(1, 1)
+                self.training_sigmas = []
+                self.initial_digest = training.tensor_state_digest(self.state_dict())
+                models.append(self)
+            def forward(self, images):
+                if self.training:
+                    self.training_sigmas.append(self.blur.sigma)
+                return self.head(images[:, :1, 0, 0]).squeeze(1)
+        class TinyDataset:
+            def __init__(self, records, image_size, training=False, **kwargs):
+                # 선택적인 원본 클래스 진단은 위 실제 literal 회귀로 검사합니다.
+                self.records, self.training = None, training
+            def __len__(self):
+                return 10000 if self.training else 2
+            def set_epoch(self, epoch):
+                self.epoch = epoch
+        def loader(dataset, config, device):
+            target = torch.tensor([0., 1.]).repeat(5000 if dataset.training else 1)
+            # 학습 관계와 반대인 검증 입력으로 실제 검증 손실이 악화하는 합성 문제입니다.
+            inputs = target*2-1 if dataset.training else 1-target*2
+            class TinyLoader(list):
+                pass
+            value = TinyLoader([(inputs[:, None, None, None], target)])
+            value.dataset = dataset
+            return value
+        def privacy(model, records, root, run_id, selection, state=None):
+            from src.identity import SCORE_VERSION, validate_run
+            from src.state import atomic_json
+            from src.privacy import score_gallery
+            import numpy as np
+            sigma = selection["sigma"]
+            self.privacy_order.append(sigma)
+            raw_path = self.result_dir / f"sigma_{sigma}_privacy_groups_private.json"
+            raw = score_gallery(np.array([[0., 1.], [1., 0.]]), [[0], [1]])
+            metadata = validate_run(root, run_id)
+            pipeline = {"protocol": selection["protocol"], "sigma": sigma, "checkpoint_sha256": selection["checkpoint_sha256"],
+                        "model_state_sha256": selection["model_state_sha256"], "source_hashes": metadata["source_hashes"],
+                        "precision": "fp32", "packet_batch_size": 1, "device": "cpu", "torch_version": "합성",
+                        "shape_dtype_byteorder_in_hash": True, "manifest_sha256": metadata["manifest_sha256"], "encoder_state_sha256": "0"*64}
+            atomic_json(raw_path, {"per_group": raw["per_group"], "distance_matrix": [[0., 1.], [1., 0.]],
+                                   "pipeline": pipeline, "gallery_feature_hashes": ["0"*64, "1"*64], "query_feature_hashes": ["0"*64, "1"*64]})
+            value = {**selection, **{k:v for k,v in raw.items() if k != "per_group"}, "score_version": SCORE_VERSION, "completed_at": "합성",
+                     "privacy_source_sha256": metadata["source_hashes"]["src/privacy.py"], "attack_protocol": "known-encoder-closed-gallery-full-feature-bytehash-v1",
+                     "precision": "fp32", "packet_batch_size": 1, "device": "cpu", "encoder_state_sha256": "0"*64,
+                     "pipeline_sha256": hashlib.sha256(json.dumps(pipeline, sort_keys=True).encode()).hexdigest(),
+                     "controls": {"original_score": 0., "constant_score": 100.},
+                     "raw_file": {"relative_path": raw_path.relative_to(root).as_posix(), "sha256": hashlib.sha256(raw_path.read_bytes()).hexdigest()}}
+            atomic_json(self.result_dir / f"sigma_{sigma}_privacy.json", value)
+            return value
+        import contextlib
+        original_save = training._save_checkpoint
+        def record_save(path, payload):
+            self.checkpoint_writes.append((Path(path).name, payload["epoch"]))
+            return original_save(path, payload)
+        class MemoryStatus(StatusWriter):
+            """1000회 통합에서는 상태값을 유지하고 반복 디스크 fsync만 분리합니다."""
+            def update(self, **values):
+                from src.state import now_kst
+                self.data.update(values)
+                self.data["updated_at"] = now_kst()
+            def event(self, name, details=None):
+                pass
+        with contextlib.ExitStack() as stack:
+            stack.enter_context(mock.patch.object(training, "_save_checkpoint", record_save))
+            if sigmas is not None:
+                stack.enter_context(mock.patch.object(training, "SIGMAS", sigmas))
+            for name, replacement in [("prepare_dataset", lambda *a: self.manifest), ("CTDataset", TinyDataset), ("_loader", loader), ("SplitResNet50", TinyModel), ("precision_policy", lambda *a: {"name":"fp32", "dtype":torch.float32, "autocast_enabled":False, "use_grad_scaler":False})]:
+                stack.enter_context(mock.patch.object(training, name, replacement))
+            if patch_privacy:
+                stack.enter_context(mock.patch.object(training, "run_privacy", privacy))
+            state = MemoryStatus(self.root, self.config)
+            result = training.run_training(self.config, self.root, state, "cpu")
+        return result, models
+
+
+if __name__ == "__main__":
+    unittest.main()
````

## tools/feature_generator.py

| 구분 | 이전 | 이후 |
| --- | --- | --- |
| 상태 | 수정 | 수정 |
| 바이트 | 15841 | 16386 |
| SHA-256 | de8706f8137121224216a7995a8fe7ce90bbc164e3af5528efc9c2046d4dea1a | 1d85c3172da23c25c3ddb7adc67a81f291abdeffc23ad928bc53255d40888e13 |

````diff
--- a/tools/feature_generator.py
+++ b/tools/feature_generator.py
@@ -10,8 +10,8 @@
 import traceback
 
 PROJECT = Path(__file__).resolve().parents[2]
-HERE = PROJECT / '블러 강도별 대표 특징맵' / '7차'
-TRAIN = PROJECT / '7차'
+HERE = PROJECT / '블러 강도별 대표 특징맵' / '8차'
+TRAIN = PROJECT / '8차'
 REFERENCE = PROJECT.parent / '블러 엣지' / '블러 피쳐맵 저장 파일'
 RUN = None
 SIGMAS = [0, 1, 2, 4, 8, 16, 32, 64, 128, 256]
@@ -114,28 +114,23 @@
     return caption, indices, [{'min': float(p.min()), 'max': float(p.max())} for p in panels]
 
 def validate_inputs(root, run_id):
-    from src.identity import validate_run, load_selection
+    from src.identity import validate_run
     metadata = validate_run(root, run_id)
     manifest = read_json(Path(root) / 'work/results/dataset_manifest_private.json')
-    return metadata['config'], manifest, load_selection(root, run_id)
+    return metadata['config'], manifest
 
 
 def run_once(paths):
-    from src.identity import validate_fixed_result
+    from src.identity import PROTOCOL, validate_result, validate_privacy_result, load_selection, safe_path
     from src.training import tensor_state_digest
-    selection_path = TRAIN / f'work/results/run_{RUN}/fixed_model_selection.json'
-    if not selection_path.exists():
-        return False
-    config, manifest, selection = validate_inputs(TRAIN, RUN)
+    config, manifest = validate_inputs(TRAIN, RUN)
     state = read_json(TRAIN / 'work/runtime/status.json')
-    if state.get('run_id') != RUN or state.get('training_status') != 'completed':
-        raise ValueError('학습100회 완료 상태와 현재 실행이 일치하지 않습니다.')
+    if state.get('run_id') != RUN:
+        raise ValueError('현재 그림 실행과 학습 실행이 다릅니다.')
     samples = [sorted((r for r in manifest['splits']['train'] if r['source_class'] == source), key=lambda r: r['relative_path'])[0]
                for _, source, _ in CLASSES]
     index_path = HERE / 'export_index_private.json'
-    bound = {'schema_version': 2, 'run_id': RUN, 'protocol': 'fixed-model-sigma0-v1', 'protocol_fixed_model': True,
-             'training_sigma': 0, 'checkpoint_sha256': selection['checkpoint_sha256'], 'model_state_sha256': selection['model_state_sha256'],
-             'checkpoint_epoch': selection['checkpoint_epoch'], 'selected_checkpoint': selection['selected_checkpoint'],
+    bound = {'schema_version': 3, 'run_id': RUN, 'protocol': PROTOCOL, 'protocol_fixed_model': False,
              'source_manifest_sha256': digest(TRAIN / 'work/results/dataset_manifest_private.json'),
              'manifest_records_sha256': manifest['manifest_sha256'], 'model_source_sha256': digest(TRAIN / 'src/model.py'),
              'data_source_sha256': digest(TRAIN / 'src/data.py'), 'generator_sha256': digest(Path(__file__)), 'samples_private': samples}
@@ -143,26 +138,35 @@
         **bound, 'items': [], 'completed_sigmas': [], 'pending_sigmas': SIGMAS,
         'sample_selection': '학습 분할에서 원본 클래스별 상대경로 정렬 첫 영상',
         'reference_panel_layout': '2행5열 채널 평균·최대·균등 간격8채널',
-        'stage1_boundary_note': '모든 블러는 동일한 σ0 선정 모델의 conv1 직후에 적용합니다.'}
+        'stage1_boundary_note': '각 강도에서 독립100회 학습 후 선정한 해당 강도 best의 실제 특징을 추출합니다.'}
     if any(index.get(key) != value for key, value in bound.items()):
-        raise ValueError('기존 그림의 단일 모델·소스·원본 연결이 현재 실행과 다릅니다.')
+        raise ValueError('기존 그림의 독립 모델 프로토콜·소스·원본 연결이 현재 실행과 다릅니다.')
     for item in index['items']:
+        selection = load_selection(TRAIN, RUN, item['sigma'])
         if digest(HERE / item['relative_path']) != item['sha256'] or item.get('checkpoint_sha256') != selection['checkpoint_sha256']:
-            raise ValueError('기존 그림 또는 단일 모델 연결이 변했습니다.')
-    checkpoint = torch.load(TRAIN / selection['selected_checkpoint'], map_location='cpu', weights_only=True)
-    model = SplitResNet50(sigma=0, pretrained=False).eval().requires_grad_(False)
-    model.load_state_dict(checkpoint['model'], strict=True)
-    if tensor_state_digest(model.state_dict()) != selection['model_state_sha256']:
-        raise ValueError('그림 모델이 동결된 전체 state와 다릅니다.')
+            raise ValueError('기존 그림 또는 해당 강도 선정 모델 연결이 변했습니다.')
     for sigma in SIGMAS:
         if sigma in index['completed_sigmas']:
             continue
         metrics_path = TRAIN / f'work/results/run_{RUN}/sigma_{sigma}_metrics.json'
+        privacy_path = TRAIN / f'work/results/run_{RUN}/sigma_{sigma}_privacy.json'
         eligible = any(q['sigma'] == sigma and q['status'] == 'completed' for q in state['sigma_queue'])
-        if not eligible or not metrics_path.exists():
+        if not eligible or not metrics_path.exists() or not privacy_path.exists():
             continue
-        validate_fixed_result(TRAIN, read_json(metrics_path), RUN)
-        model.blur = GaussianDCTBlur(sigma)
+        validate_result(TRAIN, read_json(metrics_path), RUN)
+        validate_privacy_result(TRAIN, read_json(privacy_path), RUN)
+        selection = load_selection(TRAIN, RUN, sigma)
+        checkpoint = torch.load(safe_path(TRAIN, selection['selected_checkpoint']), map_location='cpu', weights_only=True)
+        model = SplitResNet50(sigma=sigma, pretrained=False).eval().requires_grad_(False)
+        model.load_state_dict(checkpoint['model'], strict=True)
+        if tensor_state_digest(model.state_dict()) != selection['model_state_sha256']:
+            raise ValueError('그림 모델이 해당 강도 선정 state와 다릅니다.')
+        progress_path = HERE / f'그림생성_진행_sigma_{sigma}_비공개.json'
+        progress = {'run_id': RUN, 'sigma': sigma, 'selection': selection, 'generator_sha256': digest(Path(__file__))}
+        resume_orphans = progress_path.exists() and read_json(progress_path) == progress
+        if progress_path.exists() and not resume_orphans:
+            raise ValueError('중단된 그림의 생성기·모델 연결이 달라 재생성하지 않습니다.')
+        atomic_json(progress_path, progress)
         items = []
         for (key, source, label), row in zip(CLASSES, samples):
             if digest(row['path']) != row['byte_sha256']:
@@ -170,7 +174,7 @@
             x, _ = CTDataset([row], image_size=512, training=False)[0]
             stages = [x.numpy().copy()]
             with torch.inference_mode():
-                y = model.blur(model.edge((x[None] - model.rgb_mean) / model.rgb_std))
+                y = model.transmitted_features(x[None])
                 stages.append(y[0].numpy().copy())
                 y = model.cloud.maxpool(model.cloud.relu(model.cloud.bn1(y)))
                 for layer in [model.cloud.layer1, model.cloud.layer2, model.cloud.layer3, model.cloud.layer4]:
@@ -185,8 +189,9 @@
                     raise ValueError('참고 경로의 단계별 한 개 계약이 다릅니다.')
                 relative = '블러 피쳐맵 저장 파일/' + matches[0]
                 destination = HERE / relative
-                if destination.exists():
-                    raise FileExistsError('색인 밖의 그림은 덮어쓰지 않습니다: ' + relative)
+                # 그림 중단 후에는 같은 불변 체크포인트에서 미완료 강도의 파일을 재생성합니다.
+                if destination.exists() and not resume_orphans:
+                    raise FileExistsError('현재 실행의 중단 근거 없는 기존 그림을 덮어쓰지 않습니다: ' + relative)
                 caption, selected, ranges = render(array, stage, sigma, label, destination)
                 with Image.open(destination) as picture:
                     width, height = picture.size
@@ -194,7 +199,7 @@
                               'stage': stage, 'relative_path': relative, 'sha256': digest(destination), 'width': width, 'height': height,
                               'caption': caption, 'layer': LAYERS[stage], 'shape': list(array.shape), 'panel_indices': selected,
                               'panel_count': 1 if stage == 0 else 10, 'panel_minmax': ranges, 'source_sha256': row['byte_sha256'],
-                              'run_id': RUN, 'protocol_fixed_model': True, 'training_sigma': 0,
+                              'run_id': RUN, 'protocol': PROTOCOL, 'protocol_fixed_model': False, 'training_sigma': sigma,
                               'checkpoint_sha256': selection['checkpoint_sha256'], 'checkpoint_epoch': selection['checkpoint_epoch'],
                               'model_state_sha256': selection['model_state_sha256'], 'selected_checkpoint': selection['selected_checkpoint']})
         if len(items) != 18 or tensor_state_digest(model.state_dict()) != selection['model_state_sha256']:
@@ -220,8 +225,8 @@
     parser.add_argument('--run-id', required=True)
     args = parser.parse_args()
     TRAIN, HERE, REFERENCE, RUN = args.experiment_root.resolve(), args.output_root.resolve(), args.reference_root.resolve(), args.run_id
-    if TRAIN != (PROJECT / '7차').resolve() or HERE != (PROJECT / '블러 강도별 대표 특징맵' / '7차').resolve():
-        parser.error('7차 학습과 새7차 그림 폴더만 사용합니다.')
+    if TRAIN != (PROJECT / '8차').resolve() or HERE != (PROJECT / '블러 강도별 대표 특징맵' / '8차').resolve():
+        parser.error('8차 학습과 새8차 그림 폴더만 사용합니다.')
     if len(RUN) != 16 or any(c not in '0123456789abcdef' for c in RUN):
         parser.error('확인한 실행 식별자16자리가 필요합니다.')
     try:
````

## tools/inputs.py

| 구분 | 이전 | 이후 |
| --- | --- | --- |
| 상태 | 수정 | 수정 |
| 바이트 | 3485 | 3511 |
| SHA-256 | 9a12efd7d0b1a544b40c3ccb691356d49cfb77ffb68b625596e832c1c11277dc | b223c1f8710f3b0873ffc438ab52bad27314eefb1bafc2b37a783d8f15056404 |

````diff
--- a/tools/inputs.py
+++ b/tools/inputs.py
@@ -1,7 +1,7 @@
 """새 실험의 최초 입력 기준과 실제 원본을 검사하며 이전 학습 상태는 가져오지 않습니다."""
 
 from pathlib import Path
-from src.identity import (_run_identity, file_sha256, read_json, safe_path, validate_config, validate_manifest, validate_run)
+from src.identity import (_run_identity, file_sha256, read_json, safe_path, readonly_input, validate_config, validate_manifest, validate_run)
 from src.state import atomic_json
 
 
@@ -22,7 +22,7 @@
     value = {"run_id": run_id, "settings": {key: metadata[key] for key in ["config", "manifest_sha256", "source_hashes"]},
              "operational_hashes": operational_hashes(root),
              "manifest_file_sha256": file_sha256(safe_path(root, "work/results/dataset_manifest_private.json")),
-             "initial_weights_sha256": file_sha256(safe_path(root, config["initial_weights_path"]))}
+             "initial_weights_sha256": file_sha256(readonly_input(root, config, "initial_weights_path"))}
     if value["initial_weights_sha256"] != config["initial_weights_sha256"]:
         raise ValueError("초기 ImageNet 파일이 고정 SHA와 다릅니다.")
     path = baseline_path(root, run_id)
@@ -49,7 +49,7 @@
             or baseline["operational_hashes"] != operational_hashes(root)
             or baseline["manifest_file_sha256"] != file_sha256(safe_path(root, "work/results/dataset_manifest_private.json"))
             or baseline["initial_weights_sha256"] != config["initial_weights_sha256"]
-            or file_sha256(safe_path(root, config["initial_weights_path"])) != config["initial_weights_sha256"]):
+            or file_sha256(readonly_input(root, config, "initial_weights_path")) != config["initial_weights_sha256"]):
         raise ValueError("새 학습의 입력·소스·초기 가중치가 최초 기준과 다릅니다.")
     validate_run(root, run_id)
     data_root = Path(config["dataset_root"]).resolve()
````

## tools/safe_training.py

| 구분 | 이전 | 이후 |
| --- | --- | --- |
| 상태 | 수정 | 수정 |
| 바이트 | 17811 | 18436 |
| SHA-256 | 4eeecf9f2f97018757a8857442dd7d64e6ba12ef606937a5636b83b5b8acfd56 | 109208e3fd8eb51d761438cb716e2366f16039ae3c121e2f37b88d28ee0d8e3c |

````diff
--- a/tools/safe_training.py
+++ b/tools/safe_training.py
@@ -32,12 +32,12 @@
         # 누적 상태 읽기 실패가 이미 발생한 원오류를 덮지 않도록 별도 표시합니다.
         observed = {"counter_read_error": repr(secondary)}
     return {"time_kst": datetime.now(timezone(timedelta(hours=9))).isoformat(),
-            "session": os.environ.get("CT_TRAIN_SESSION", "local-training"), "task": os.environ.get("CT_TRAIN_TASK", "fixed-model-training"), **observed,
+            "session": os.environ.get("CT_EXPERIMENT_SESSION", "local-session"), "task": os.environ.get("CT_EXPERIMENT_TASK", "local-experiment"), **observed,
             "error_type": type(error).__name__, "error": str(error),
             "errno": getattr(error, "errno", None), "winerror": getattr(error, "winerror", None),
             "traceback": "".join(traceback.format_exception(type(error), error, error.__traceback__)),
             "argv": [sys.executable, *sys.orig_argv[1:]], "cwd": os.getcwd(), "pid": os.getpid(), "exit_code": 1,
-            "changes_at_failure": "7차 상태·checkpoint의 마지막 완료epoch와 함께 확인; 기존1~6차 입력은 읽기 전용"}
+            "changes_at_failure": "8차 상태·checkpoint의 마지막 완료epoch와 함께 확인; 기존1~7차 입력은 읽기 전용"}
 
 
 def write_independent_logs(folders, filename, payload):
@@ -181,7 +181,7 @@
 
 def log_folders(root):
     local = Path(os.environ.get("LOCALAPPDATA", str(Path.home() / "AppData/Local")))
-    return [Path(root) / "work/recovery_logs", local / "폐CT_학습복구" / "7차"]
+    return [Path(root) / "work/recovery_logs", local / "폐CT_학습복구" / "8차"]
 
 
 def worker(root, device, folders):
@@ -215,7 +215,11 @@
                 interrupted = isinstance(error, KeyboardInterrupt)
                 for entry in state.data["sigma_queue"]:
                     if entry["status"] == "running":
-                        entry["status"] = "failed"
+                        entry["status"] = "error"
+                        for field in ["training_status", "classification_status", "privacy_status"]:
+                            if entry.get(field) == "running":
+                                entry[field] = "error"
+                                state.data[field] = "error"
                 state.update(stage="interrupted" if interrupted else "error", status="interrupted" if interrupted else "failed",
                              pid=None, error=details, message=f"학습 중단: {type(error).__name__}: {error}")
                 state.event("복구 실행 중단", details)
@@ -309,7 +313,7 @@
 
 
 def main():
-    parser = argparse.ArgumentParser(description="7차 σ0 새 학습과 단일 고정 모델 평가를 시작하거나 마지막 완료 회차에서 재개합니다.")
+    parser = argparse.ArgumentParser(description="8차 강도별 독립 학습과 분류·프라이버시 점수를 시작하거나 마지막 완료 회차에서 재개합니다.")
     parser.add_argument("--device", choices=("cuda", "cpu"), default="cuda")
     parser.add_argument("--baseline-sha256", help="사전에 고정·검토한 비공개 원본 기준의 SHA256")
     parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
````

## web/app.js

| 구분 | 이전 | 이후 |
| --- | --- | --- |
| 상태 | 수정 | 수정 |
| 바이트 | 23077 | 23319 |
| SHA-256 | 7f600a32681459c22fb4246e302b99322211acff831a9e3eac6e1fff9328db79 | 2e44b62f56e3497a0d272cca8b2416cd6720ce7a501df3375236a127f7f595a9 |

````diff
--- a/web/app.js
+++ b/web/app.js
@@ -1,7 +1,7 @@
 import { createPipeline } from './scene.js';
 const $ = id => document.getElementById(id);
-const stages = {preparing:'학습 데이터를 준비하고 있습니다',ready:'학습 준비를 마쳤습니다',loading_model:'모델을 불러오고 있습니다',training:'분류기를 학습하고 있습니다',validation:'검증 결과를 확인하고 있습니다',testing:'고정 모델로 블러 강도별 평가 중입니다',evaluation:'고정 모델로 블러 강도별 평가 중입니다',completed:'실험을 마쳤습니다',interrupted:'학습을 중단했습니다',error:'학습을 멈췄습니다'};
-const states = {running:'진행 중',ready:'준비 완료',completed:'완료',failed:'오류',pending:'대기',waiting:'기록 대기',interrupted:'중단'};
+const stages = {preparing:'학습 데이터를 준비하고 있습니다',ready:'학습 준비를 마쳤습니다',loading_model:'모델을 불러오고 있습니다',training:'분류기를 학습하고 있습니다',validation:'검증 결과를 확인하고 있습니다',testing:'선택 강도의 분류 성적을 측정하고 있습니다',evaluation:'선택 강도의 분류 성적을 측정하고 있습니다',privacy:'원본 후보 공격과 복원 저항 점수를 계산하고 있습니다',completed:'실험을 마쳤습니다',interrupted:'학습을 중단했습니다',error:'학습을 멈췄습니다'};
+const states = {running:'진행 중',ready:'준비 완료',completed:'완료',failed:'오류',error:'오류',pending:'대기',waiting:'기록 대기',interrupted:'중단'};
 const number = v => typeof v === 'number' && Number.isFinite(v);
 const shown = v => number(v) ? v.toLocaleString('ko-KR') : '—';
 const measured = v => number(v) ? v.toLocaleString('ko-KR') : '미측정';
@@ -26,6 +26,13 @@
   const digits=String(tenths).padStart(2,'0');
   return `${digits.slice(0,-1)}.${digits.slice(-1)}%`;
 }
+function privacyPoints(value){
+  if(!number(value)||value<0||value>100)return '미측정';
+  // 원점수의 십진 문자열을 직접 반올림하여 중간 나눗셈 오차를 만들지 않습니다.
+  const [whole,fraction='']=decimalShift(value).split('.'),padded=fraction.padEnd(2,'0');
+  const tenths=BigInt(whole+padded[0])+(padded[1]>='5'?1n:0n),digits=String(tenths).padStart(2,'0');
+  return `${digits.slice(0,-1)}.${digits.slice(-1)} / 100`;
+}
 function fullPercent(value){return number(value)&&value>=0&&value<=1?decimalShift(value,2)+'%':'미측정';}
 
 let latest = null;
@@ -39,8 +46,8 @@
   $('selectedBestEpoch').textContent=number(metrics?.best_epoch)?`${metrics.best_epoch}회`:'미측정';
   $('selectedEpochs').textContent=number(metrics?.epochs_ran)?`${metrics.epochs_ran}회`:'미측정';
   $('selectedSteps').textContent=measured(metrics?.eval_optimizer_steps);
-  $('selectedCheckpoint').textContent=metrics?.checkpoint_sha256||'고정 모델 평가 대기';
-  $('selectedTrainingSigma').textContent=metrics?.training_sigma===0?'σ 0 · 공통 모델 한 번 학습':'학습 완료 대기';
+  $('selectedCheckpoint').textContent=metrics?.checkpoint_sha256||'선택 강도의 모델 선정 대기';
+  $('selectedTrainingSigma').textContent=number(metrics?.training_sigma)?`σ ${metrics.training_sigma} · 이 강도에서 독립 학습`:'학습 완료 대기';
   $('testAccuracy').textContent=percent(test?.accuracy);
   $('testAuc').textContent=test?.auc===null?'정의 불가':rawNumber(test?.auc);
   $('testAccuracyRaw').textContent=rawNumber(test?.accuracy);
@@ -49,6 +56,17 @@
   $('testLossRaw').textContent=rawNumber(test?.loss);
   $('testCorrectCount').textContent=Number.isInteger(test?.correct_count)&&Number.isInteger(test?.n_images)&&test.n_images>0&&test.correct_count>=0&&test.correct_count<=test.n_images?`정답 ${test.correct_count} / ${test.n_images}장`:'정답 수 미측정 · 원비율을 확인하세요';
   $('evaluationNote').textContent=number(sigma)?`σ ${sigma} · ${test?'학습에 쓰지 않은 영상의 결과':'시험 결과 대기'}`:'강도를 골라 주세요';
+  const privacy=result?.privacy_status==='completed'?result.privacy:null;
+  $('privacyScore').textContent=privacyPoints(privacy?.score);
+  $('privacyScoreRaw').textContent=rawNumber(privacy?.score);
+  $('privacyVersion').textContent=privacy?.score_version||'gallery-residual-v1 · 측정 대기';
+  $('privacyState').textContent=result?.privacy_status==='error'?'계산 오류 · 오류 원문을 보존하고 복구를 기다립니다':result?.privacy_status==='running'?'원본 후보 공격과 점수 계산 중':privacy?'계산 완료 · 낮은 점수와 0점도 그대로 표시합니다':'아직 계산하지 않았습니다';
+  $('privacyAttack').textContent=rawNumber(privacy?.T_attack);
+  $('privacyPrior').textContent=rawNumber(privacy?.T_prior);
+  $('privacyGroups').textContent=number(privacy?.G)&&number(privacy?.original_test_images)?`시험 원본 ${privacy.original_test_images}장 → ${privacy.G}개 그룹`:'미측정';
+  $('privacyExposure').textContent=number(privacy?.exact_return_groups)&&number(privacy?.G)?`정확 반환 ${privacy.exact_return_groups} / ${privacy.G}개 그룹`:'미측정';
+  $('privacyMatching').textContent=rawNumber(privacy?.fractional_top1);
+  $('privacyDistribution').textContent=privacy?.residual_quantiles?JSON.stringify(privacy.residual_quantiles):'미측정';
   drawChart({sigma,history:result?.history||[],evaluation_history:result?.evaluation_history||[]});
 }
 async function loadSelectedResult(){
@@ -70,11 +88,6 @@
     const result=await response.json();
     if(request!==resultRequest||sigma!==selectedSigma||run!==selectionRun)return;
     if(result.run_id!==run||result.sigma!==sigma||!Array.isArray(result.history))throw new Error('선택 결과 불일치');
-    if(latest.training_status!=='completed'){
-      result.metrics=null;result.evaluation_history=[];result.status='pending';
-      if(sigma!==0)result.history=[];
-      result.message='블러 0의 100회 학습을 기다립니다. 강도별 평가는 아직 시작하지 않았습니다.';
-    }
     drawSelectedResults(result);
   }catch(error){if(request===resultRequest)drawSelectedResults(null,'결과를 불러오지 못했어요. 잠시 뒤 다시 확인해요.');}
   finally{clearTimeout(timeout);if(resultController===controller){resultController=null;pendingResultKey=null;}}
@@ -87,16 +100,16 @@
   loadSelectedResult();
 }
 function renderQueue(s){
-  const queue=s.training_status==='completed'&&Array.isArray(s.sigma_queue)?s.sigma_queue:[];
+  const queue=Array.isArray(s.sigma_queue)?s.sigma_queue:[];
   const nodes=[];
   for(const sigma of sigmaChoices){
     const item=queue.find(x=>x.sigma===sigma);let button=$('queue').querySelector(`[data-sigma="${sigma}"]`);
     if(!button){button=document.createElement('button');button.type='button';button.dataset.sigma=String(sigma);const strong=document.createElement('strong'),small=document.createElement('small');strong.textContent=`σ ${sigma}`;button.append(strong,small);button.addEventListener('click',()=>selectSigma(sigma));}
-    button.className=['running','completed','failed'].includes(item?.status)?item.status:'';
-    button.querySelector('small').textContent=states[item?.status]||'대기';button.setAttribute('aria-pressed',String(selectedSigma===sigma));button.setAttribute('aria-label',`블러 강도 ${sigma}, ${states[item?.status]||'대기'} 결과 보기`);nodes.push(button);
+    button.className=['running','completed','failed','error'].includes(item?.status)?item.status:'';
+    const step=item?.privacy_status==='running'?'점수 계산':item?.privacy_status==='error'?'점수 오류':item?.classification_status==='running'?'분류 평가':item?.training_status==='running'?'학습 중':states[item?.status]||'대기';button.querySelector('small').textContent=step;button.setAttribute('aria-pressed',String(selectedSigma===sigma));button.setAttribute('aria-label',`블러 강도 ${sigma}, ${states[item?.status]||'대기'} 결과 보기`);nodes.push(button);
   }
   if(nodes.some((node,i)=>$('queue').children[i]!==node)||$('queue').children.length!==nodes.length)$('queue').replaceChildren(...nodes);
-  $('queueCount').textContent=`${queue.filter(x=>x.status==='completed').length} / 10 평가 완료`;
+  $('queueCount').textContent=`${queue.filter(x=>x.status==='completed').length} / 10 강도 완료`;
 }
 let pipeline = null;
 let refreshing = false;
@@ -137,17 +150,16 @@
   else setMotion();
 }
 function drawChart(s) {
-  const evaluating=s.sigma!==0;
-  const rows = evaluating ? (s.evaluation_history||[]).filter(row=>row.sigma===s.sigma).map(row=>({sigma:row.sigma,epoch:1,val_loss:row.validation_loss,val_accuracy:row.validation_accuracy,test_loss:row.test_loss,test_accuracy:row.test_accuracy})) : (Array.isArray(s.history) ? s.history : []).filter(row => row.sigma === 0);
-  $('chartTitle').textContent=evaluating?'선택 강도의 고정 모델 평가':'블러 0의 공통 모델 학습 곡선';
-  $('curveDescription').textContent=evaluating?'이 강도에서는 학습하지 않았습니다. 고정 모델로 한 번 측정한 검증 손실·시험 손실·시험 정확도를 표시합니다.':'블러 0에서 한 번 학습한 손실과 검증 성적입니다. 다른 강도의 학습 곡선으로 재사용하지 않습니다.';
-  $('legendTrain').textContent=evaluating?'검증 손실':'학습 손실';
-  $('legendValidation').textContent=evaluating?'시험 손실':'검증 손실';
-  $('legendAccuracy').textContent=evaluating?'시험 정확도':'검증 정확도';
-  const columns=evaluating?['평가','검증 손실','시험 손실','시험 정확도 원비율','검증 정확도 원비율','추가 갱신 횟수']:['학습 회차','학습 손실','검증 손실','검증 정확도 원비율','검증 AUC','학습률'];
+  const rows = (Array.isArray(s.history) ? s.history : []).filter(row => row.sigma === s.sigma);
+  $('chartTitle').textContent=number(s.sigma)?`σ ${s.sigma}의 독립 학습 곡선`:'강도별 독립 학습 곡선';
+  $('curveDescription').textContent='선택한 강도에서 새로 초기화해 학습한 손실과 검증 성적입니다. 다른 강도의 곡선을 대신 표시하지 않습니다.';
+  $('legendTrain').textContent='학습 손실';
+  $('legendValidation').textContent='검증 손실';
+  $('legendAccuracy').textContent='검증 정확도';
+  const columns=['학습 회차','학습 손실','검증 손실','검증 정확도 원비율','검증 AUC','학습률'];
   const headings=columns.map(value=>{const th=document.createElement('th');th.textContent=value;return th;});$('historyHead').replaceChildren(...headings);
   const historyBody=$('observedHistory'),historyRows=[];
-  for(const row of rows){const tr=document.createElement('tr');for(const value of (evaluating?[1,row.val_loss,row.test_loss,row.test_accuracy,row.val_accuracy,0]:[row.epoch,row.train_loss,row.val_loss,row.val_accuracy,row.val_auc,row.learning_rate])){const td=document.createElement('td');td.textContent=rawNumber(value);tr.append(td);}historyRows.push(tr);}
+  for(const row of rows){const tr=document.createElement('tr');for(const value of [row.epoch,row.train_loss,row.val_loss,row.val_accuracy,row.val_auc,row.learning_rate]){const td=document.createElement('td');td.textContent=rawNumber(value);tr.append(td);}historyRows.push(tr);}
   if(!historyRows.length){const tr=document.createElement('tr'),td=document.createElement('td');td.colSpan=6;td.textContent='선택한 강도의 기록은 아직 없어요.';tr.append(td);historyRows.push(tr);}
   historyBody.replaceChildren(...historyRows);
   const canvas = $('chart');
@@ -156,14 +168,14 @@
   canvas.width = Math.max(1, Math.floor(rect.width*dpr)); canvas.height = Math.floor(210*dpr);
   const ctx = canvas.getContext('2d'); ctx.scale(dpr,dpr);
   const width=rect.width, height=210, left=38, right=40, top=16, bottom=30;
-  const metrics=evaluating?[['val_loss','#647fba'],['test_loss','#4c83cf'],['test_accuracy','#c49b48']]:[['train_loss','#647fba'],['val_loss','#4c83cf'],['val_accuracy','#c49b48']];
+  const metrics=[['train_loss','#647fba'],['val_loss','#4c83cf'],['val_accuracy','#c49b48']];
   const measured = rows.some(r=>metrics.some(([key])=>number(r[key])));
   $('emptyChart').hidden = measured;
   $('curveSigma').textContent = number(s.sigma) ? `σ = ${s.sigma}` : '현재 σ 미측정';
   if (!measured) {$('latestLoss').textContent='최근 손실 미측정';return;}
   const recent=rows.at(-1);
-  $('latestLoss').textContent=recent ? evaluating?`검증 손실 ${lossText(recent.val_loss)} · 시험 손실 ${lossText(recent.test_loss)}`:`최근 학습 손실 ${lossText(recent.train_loss)} · 검증 손실 ${lossText(recent.val_loss)}` : '최근 손실 미측정';
-  const lossValues=rows.flatMap(r=>evaluating?[r.val_loss,r.test_loss]:[r.train_loss,r.val_loss]).filter(number);
+  $('latestLoss').textContent=recent ? `최근 학습 손실 ${lossText(recent.train_loss)} · 검증 손실 ${lossText(recent.val_loss)}` : '최근 손실 미측정';
+  const lossValues=rows.flatMap(r=>[r.train_loss,r.val_loss]).filter(number);
   const maxLoss=Math.max(1,...lossValues)*1.1;
   const maxEpoch=Math.max(1,...rows.map(r=>number(r.epoch)?r.epoch:0));
   const chartWidth=width-left-right, chartHeight=height-top-bottom;
@@ -185,7 +197,7 @@
     ctx.stroke();
     for(const row of rows){if(!number(row[key])||!number(row.epoch))continue;ctx.beginPath();ctx.arc(left+(row.epoch-1)/Math.max(1,maxEpoch-1)*chartWidth,top+chartHeight*(1-row[key]/(key.endsWith('accuracy')?1:maxLoss)),3,0,Math.PI*2);ctx.fill();}
   }
-  ctx.fillStyle=window.ctTheme?.current()==='dark'?'#8391a8':'#8793a7';ctx.textAlign='left';ctx.fillText(evaluating?'고정 모델 평가':'1회',left,height-7);ctx.textAlign='right';ctx.fillText(evaluating?'추가 학습 0회':`${maxEpoch}회`,width-right,height-7);
+  ctx.fillStyle=window.ctTheme?.current()==='dark'?'#8391a8':'#8793a7';ctx.textAlign='left';ctx.fillText('1회',left,height-7);ctx.textAlign='right';ctx.fillText(`${maxEpoch}회`,width-right,height-7);
 }
 function render(s) {
   latest=s;
@@ -194,20 +206,20 @@
   const interrupted=s.status==='interrupted' || s.stage==='interrupted';
   const failed=!interrupted && (s.status==='failed' || Boolean(s.error));
   const blocked=failed || dead || meta.stale || interrupted;
-  $('currentTitle').textContent=interrupted ? '학습을 중단했습니다' : s.stage==='ready' && s.status==='waiting' ? '학습 상태를 기다리고 있습니다' : s.phase==='evaluation' ? '고정 모델로 블러 강도별 평가 중입니다' : stages[s.stage] || '학습 상태를 확인하고 있습니다';
-  $('message').textContent=interrupted?'학습과 모형의 움직임을 멈추고 마지막 기록을 표시합니다.':s.status==='failed'?'오류를 확인한 뒤 다시 시작합니다. 실행 기록은 보존되어 있습니다.':s.training_status!=='completed'?'블러 0에서 새 모델을 한 번만 100회 학습합니다. 다른 강도는 모두 평가 대기입니다.':'검증 손실이 가장 낮았던 모델 한 개를 고정했습니다. 블러 강도만 바꾸며 추가 학습 없이 평가합니다.';
+  $('currentTitle').textContent=interrupted ? '학습을 중단했습니다' : s.stage==='ready' && s.status==='waiting' ? '학습 상태를 기다리고 있습니다' : stages[s.phase] || stages[s.stage] || '학습 상태를 확인하고 있습니다';
+  $('message').textContent=interrupted?'학습과 모형의 움직임을 멈추고 마지막 기록을 표시합니다.':s.status==='failed'?'오류를 확인한 뒤 다시 시작합니다. 실행 기록은 보존되어 있습니다.':'각 강도에서 새 모델을 100회 학습하고, 분류 성적과 복원 저항 점수를 계산한 뒤 다음 강도로 넘어갑니다.';
   $('badge').textContent=interrupted?'중단':states[s.status] || '상태 확인 중';
   let warning=interrupted ? '학습이 중단되었습니다. 마지막 기록을 표시하며 모형의 움직임도 멈췄습니다.' : failed ? '실험이 오류로 중단되었습니다. 작업 기록을 확인해 주세요.' : dead ? '학습 프로세스가 종료되었습니다. 마지막 기록을 표시합니다.' : meta.read_error ? meta.read_error : meta.stale ? '60초 이상 새 기록이 없어요. 관찰용 알림이며 학습을 멈추는 기준은 아닙니다.' : '';
   $('alert').textContent=warning;$('alert').className=warning?`alert visible${failed||dead?' failed':''}`:'alert';
-  $('sigmaLabel').textContent=s.training_status==='completed'?`학습 완료 · 모델 고정 · ${number(s.evaluation_current_sigma)?'현재 평가 σ '+s.evaluation_current_sigma:'평가 준비'}`:'한 번의 학습 · 블러 σ 0 · 평가 10조건 대기';
-  $('fixedModelStatus').textContent=s.training_status==='completed'&&s.checkpoint_sha256?'100회 학습 완료 · 최저 검증 손실 모델 고정':'블러 0 학습 완료 후 모델 한 개를 고정합니다';
-  $('fixedModelHash').textContent=s.training_status==='completed'&&s.checkpoint_sha256?s.checkpoint_sha256:'고정 모델 해시 대기';
+  $('sigmaLabel').textContent=`현재 강도 ${number(s.sigma)?'σ '+s.sigma:'대기'} · 학습 → 분류 평가 → 복원 저항 점수`;
+  $('fixedModelStatus').textContent=s.training_status==='completed'&&s.checkpoint_sha256?'현재 강도의 100회 학습 완료 · 최저 검증 손실 모델 선정':'각 강도의 100회 학습 후 해당 모델을 선정합니다';
+  $('fixedModelHash').textContent=s.training_status==='completed'&&s.checkpoint_sha256?s.checkpoint_sha256:'현재 강도의 모델 해시 대기';
   const policy=s.training_policy || {};
   const maximum=number(policy.max_epochs)?policy.max_epochs:s.epochs;
   $('epoch').textContent=`${measured(s.epoch)}회 / ${policy.early_stopping_enabled===false?'목표':'최대'} ${measured(maximum)}회`;
   $('learningRate').textContent=rawNumber(s.learning_rate);
-  $('earlyStopping').textContent=policy.early_stopping_enabled===false?'조기 종료 끔 · 블러 0에서 한 번 100회':'실제 학습 정책 확인 대기';
-  $('trainingPolicyNote').textContent='① 블러 0에서 한 번 100회 학습 → ② 검증 손실 최저 모델 한 개 고정 → ③ 같은 모델로 σ 0·1·2·4·8·16·32·64·128·256 평가. 강도별 재학습은 하지 않습니다.';
+  $('earlyStopping').textContent=policy.early_stopping_enabled===false?'조기 종료 끔 · 각 강도에서 독립 100회':'실제 학습 정책 확인 대기';
+  $('trainingPolicyNote').textContent='① 현재 강도에서 새 모델 100회 학습 → ② 검증 손실 최저 모델로 정확도·복원 저항 점수 측정 → ③ 모두 끝나면 다음 강도를 새로 학습합니다.';
   $('bestEpoch').textContent=number(s.best_epoch)?`${s.best_epoch}회`:'미측정';
   $('optimizerSteps').textContent=measured(s.optimizer_steps);
   $('batch').textContent=`배치 ${shown(s.batch)} / ${shown(s.batches)}`;
````

## web/index.html

| 구분 | 이전 | 이후 |
| --- | --- | --- |
| 상태 | 수정 | 수정 |
| 바이트 | 9820 | 12403 |
| SHA-256 | 110fe162e421c40bfa5b62a3dc85886fff097438c2f3c30b7d108ca774bac4ce | 7756cc6aa4a91813c791b581e0d70242922d38397738355a4779adb500a1f30a |

````diff
--- a/web/index.html
+++ b/web/index.html
@@ -1,12 +1,12 @@
 <!doctype html>
-<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>폐 CT 고정 모델 블러 실험 · 7차</title><script src="/theme.js"></script><link rel="stylesheet" href="/style.css"></head>
-<body><header class="topbar"><div class="identity"><h1>폐 CT 고정 모델 블러 실험 · 7차</h1><p>블러 0에서 한 번 학습한 모델로 열 가지 강도를 평가합니다</p></div><div class="top-actions"><button id="theme" class="theme-toggle" aria-label="어두운 화면으로 전환" aria-pressed="false"><span class="theme-track"><span></span></span><span id="themeText">다크</span></button><button id="refresh" class="icon-button" aria-label="상태 새로고침"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 7v5h-5M4 17v-5h5M6 6a8 8 0 0 1 13 2M5 16a8 8 0 0 0 13 2"/></svg></button></div></header>
+<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>폐 CT 강도별 학습과 복원 저항 실험 · 8차</title><script src="/theme.js"></script><link rel="stylesheet" href="/style.css"></head>
+<body><header class="topbar"><div class="identity"><h1>폐 CT 강도별 학습과 복원 저항 실험 · 8차</h1><p>강도마다 새로 학습하고 정확도와 원본 후보 공격의 복원 저항을 함께 측정합니다</p></div><div class="top-actions"><button id="theme" class="theme-toggle" aria-label="어두운 화면으로 전환" aria-pressed="false"><span class="theme-track"><span></span></span><span id="themeText">다크</span></button><button id="refresh" class="icon-button" aria-label="상태 새로고침"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 7v5h-5M4 17v-5h5M6 6a8 8 0 0 1 13 2M5 16a8 8 0 0 0 13 2"/></svg></button></div></header>
 <aside class="sidebar"><nav aria-label="실험 메뉴"><a class="active" href="#overview"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m3 17 5-7 6 4 7-10"/><circle cx="3" cy="17" r="1"/><circle cx="8" cy="10" r="1"/><circle cx="14" cy="14" r="1"/><circle cx="21" cy="4" r="1"/></svg>실험 현황</a><a href="#analysis"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 20V10m6 10V4m6 16v-7m5 7H2"/></svg>모델 평가</a><a href="#data"><svg viewBox="0 0 24 24" aria-hidden="true"><ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 4 16 4 16 0V5M4 12c0 4 16 4 16 0"/></svg>데이터</a><a href="#records"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="5" y="3" width="15" height="18" rx="2"/><path d="M9 8h7m-7 4h7m-7 4h4M3 7h3m-3 5h3m-3 5h3"/></svg>기록</a></nav><div class="sidebar-note">폐 CT 실험실<span>Conv1 · ResNet-50</span><small>이 PC에서 실행</small></div></aside>
 <main><section id="overview"><div id="alert" class="alert" role="status"></div><div class="status-row"><div class="current-heading"><div class="status-title"><span id="badge" class="pill">기록 대기</span><h2 id="currentTitle">학습 상태를 기다리고 있습니다</h2></div><p id="sigmaLabel">블러 강도 기록 대기</p><p id="message" class="sr-only">첫 합성곱 특징에 블러를 적용해 분류 성능을 비교합니다.</p></div><div class="training-progress"><div class="progress-top"><h3>학습 진행</h3><strong id="epoch">—</strong><span id="process" class="process">프로세스 확인 대기</span></div><progress id="progress" value="0" max="100" aria-label="이번 학습 회차의 배치 진행률"></progress><div class="progress-bottom"><span id="seen">이번 회차 OK — / NG —</span><span id="device">장치 확인 중</span></div><span id="batch" class="batch-note">배치 미측정</span></div></div>
-<section class="fixed-model-proof" aria-label="고정 모델 확인"><strong id="fixedModelStatus">블러 0 학습 완료 후 모델 한 개를 고정합니다</strong><p>체크포인트 SHA-256 <code id="fixedModelHash">고정 모델 해시 대기</code></p><p>같은 해시는 같은 저장 모델 파일을 뜻합니다. 각 평가 결과의 해시와 함께 확인합니다.</p></section><div class="training-policy" aria-label="학습 설정과 실제 진행"><dl><div><dt>현재 학습률</dt><dd id="learningRate">미측정</dd></div><div><dt>조기 종료 설정 / 대기 회차</dt><dd id="earlyStopping">미측정 / 미측정</dd></div><div><dt>현재 최저 검증 손실 회차</dt><dd id="bestEpoch">미측정</dd></div><div><dt>가중치 갱신 횟수</dt><dd id="optimizerSteps">미측정</dd></div></dl><p id="trainingPolicyNote">실제 종료 설정을 기다리고 있어요.</p></div>
-<div class="model-workspace"><div class="model-tools"><span>연산 구조</span><button id="motion" class="text-button" aria-pressed="false" title="실행 상태에 맞춰 흐르는 모형입니다. 실제 계산 속도를 나타내지 않습니다.">움직임 정지</button></div><canvas id="scene" aria-label="영상 입력에서 7곱하기7 합성곱, 64채널 특징, 가우시안 블러, ResNet 잔차 블록, 분류로 이어지는 입체 모형"></canvas><p id="sceneError" role="status"></p><div class="steps"><div><strong>입력 영상</strong><small id="step0">대기</small></div><div><strong>첫 합성곱</strong><small id="step1">대기</small></div><div><strong>특징 블러</strong><small id="step2">대기</small></div><div><strong>분류</strong><small id="step3">대기</small></div></div><div class="model-footnote"><span>입력 영상은 추상 모형입니다.</span><span>블러 0에서 후단 한 번 학습 · 고정 모델의 특징 블러 평가</span></div></div>
-<div class="sigma-row"><span class="sigma-label">평가 블러 강도</span><div id="queue" class="queue"></div><span id="queueCount" class="queue-count">기록 대기</span></div></section>
-<section class="selected-result" aria-label="선택한 블러 강도의 결과"><h2 id="selectedSigma">🔎 강도를 골라 주세요</h2><p id="selectionNote" role="status">위 강도 버튼이나 사진의 강도를 누르면 곡선과 시험 결과도 함께 바뀌어요.</p><dl><div><dt>공통 모델의 선정 회차</dt><dd id="selectedBestEpoch">미측정</dd></div><div><dt>공통 모델 학습 회차</dt><dd id="selectedEpochs">미측정</dd></div><div><dt>이 강도 평가 중 추가 갱신</dt><dd id="selectedSteps">미측정</dd></div></dl><dl><div><dt>모델을 학습한 강도</dt><dd id="selectedTrainingSigma">학습 완료 대기</dd></div><div><dt>이 평가의 체크포인트 SHA-256</dt><dd id="selectedCheckpoint">고정 모델 평가 대기</dd></div></dl><p>블러 0에서 검증 손실이 가장 낮았던 모델 하나를 모든 평가에 사용합니다. 선택한 강도의 곡선·수치·그림만 표시하며, 시험 성적으로 모델이나 강도를 선택하지 않습니다.</p></section><div class="lower-grid"><section id="analysis" class="chart-section"><div class="section-heading"><h2 id="chartTitle">블러 0의 공통 모델 학습 곡선</h2><span id="curveSigma">현재 σ</span></div><div class="legend"><span id="legendTrain">학습 손실</span><span id="legendValidation">검증 손실</span><span id="legendAccuracy">검증 정확도</span></div><div class="chart-wrap"><canvas id="chart" aria-label="선택한 블러 강도의 학습 회차별 손실과 정확도"></canvas><p id="emptyChart">선택한 강도의 측정 기록이 없습니다<span>학습 완료와 해당 강도의 평가를 기다립니다.</span></p></div><p class="chart-note"><span id="curveDescription">블러 0은 공통 모델 학습 곡선, 다른 강도는 고정 모델의 평가 한 번을 표시합니다.</span><br>왼쪽 축: 손실(선형) · 오른쪽 축: 정확도<br><span id="latestLoss">최근 손실 미측정</span></p><details class="observed-values"><summary>🔢 곡선에 쓰인 원값 보기</summary><p>축의 눈금은 읽기 위한 간격입니다. 아래 값은 저장된 숫자를 반올림하지 않고 표시합니다. 정확도 원비율은 0~1이며, 1은 100%입니다.</p><div class="observed-values-scroll"><table><thead><tr id="historyHead"><th>학습 회차</th><th>학습 손실</th><th>검증 손실</th><th>검증 정확도 원비율</th><th>검증 AUC</th><th>학습률</th></tr></thead><tbody id="observedHistory"></tbody></table></div></details></section>
+<section class="fixed-model-proof" aria-label="강도별 선정 모델 확인"><strong id="fixedModelStatus">각 강도에서 100회 학습 후 검증 손실이 가장 낮은 모델을 고릅니다</strong><p>체크포인트 SHA-256 <code id="fixedModelHash">고정 모델 해시 대기</code></p><p>각 강도는 서로 독립된 모델입니다. 해당 강도의 정확도·점수·그림은 같은 선정 모델에 연결합니다.</p></section><div class="training-policy" aria-label="학습 설정과 실제 진행"><dl><div><dt>현재 학습률</dt><dd id="learningRate">미측정</dd></div><div><dt>조기 종료 설정 / 대기 회차</dt><dd id="earlyStopping">미측정 / 미측정</dd></div><div><dt>현재 최저 검증 손실 회차</dt><dd id="bestEpoch">미측정</dd></div><div><dt>가중치 갱신 횟수</dt><dd id="optimizerSteps">미측정</dd></div></dl><p id="trainingPolicyNote">실제 종료 설정을 기다리고 있어요.</p></div>
+<div class="model-workspace"><div class="model-tools"><span>연산 구조</span><button id="motion" class="text-button" aria-pressed="false" title="실행 상태에 맞춰 흐르는 모형입니다. 실제 계산 속도를 나타내지 않습니다.">움직임 정지</button></div><canvas id="scene" aria-label="영상 입력에서 7곱하기7 합성곱, 64채널 특징, 가우시안 블러, ResNet 잔차 블록, 분류로 이어지는 입체 모형"></canvas><p id="sceneError" role="status"></p><div class="steps"><div><strong>입력 영상</strong><small id="step0">대기</small></div><div><strong>첫 합성곱</strong><small id="step1">대기</small></div><div><strong>특징 블러</strong><small id="step2">대기</small></div><div><strong>분류</strong><small id="step3">대기</small></div></div><div class="model-footnote"><span>입력 영상은 추상 모형입니다.</span><span>강도별 후단 독립 학습 · 원본 후보 공격 실측</span></div></div>
+<div class="sigma-row"><span class="sigma-label">학습·평가 블러 강도</span><div id="queue" class="queue"></div><span id="queueCount" class="queue-count">기록 대기</span></div></section>
+<section class="selected-result" aria-label="선택한 블러 강도의 결과"><h2 id="selectedSigma">🔎 강도를 골라 주세요</h2><p id="selectionNote" role="status">위 강도 버튼이나 사진의 강도를 누르면 곡선과 시험 결과도 함께 바뀌어요.</p><dl><div><dt>해당 강도의 선정 회차</dt><dd id="selectedBestEpoch">미측정</dd></div><div><dt>해당 강도의 학습 회차</dt><dd id="selectedEpochs">미측정</dd></div><div><dt>이 강도 평가 중 추가 갱신</dt><dd id="selectedSteps">미측정</dd></div></dl><dl><div><dt>모델을 학습한 강도</dt><dd id="selectedTrainingSigma">학습 완료 대기</dd></div><div><dt>이 평가의 체크포인트 SHA-256</dt><dd id="selectedCheckpoint">선택 강도의 모델 선정 대기</dd></div></dl><p>각 강도에서 새로 학습하고 검증 손실이 가장 낮았던 해당 모델을 평가합니다. 선택한 강도의 곡선·수치·그림만 표시하며, 시험 성적으로 모델이나 강도를 선택하지 않습니다.</p></section><div class="lower-grid"><section id="analysis" class="chart-section"><div class="section-heading"><h2 id="chartTitle">강도별 독립 학습 곡선</h2><span id="curveSigma">현재 σ</span></div><div class="legend"><span id="legendTrain">학습 손실</span><span id="legendValidation">검증 손실</span><span id="legendAccuracy">검증 정확도</span></div><div class="chart-wrap"><canvas id="chart" aria-label="선택한 블러 강도의 학습 회차별 손실과 정확도"></canvas><p id="emptyChart">선택한 강도의 측정 기록이 없습니다<span>학습 완료와 해당 강도의 평가를 기다립니다.</span></p></div><p class="chart-note"><span id="curveDescription">선택한 강도에서 실제로 학습한 곡선만 표시합니다.</span><br>왼쪽 축: 손실(선형) · 오른쪽 축: 정확도<br><span id="latestLoss">최근 손실 미측정</span></p><details class="observed-values"><summary>🔢 곡선에 쓰인 원값 보기</summary><p>축의 눈금은 읽기 위한 간격입니다. 아래 값은 저장된 숫자를 반올림하지 않고 표시합니다. 정확도 원비율은 0~1이며, 1은 100%입니다.</p><div class="observed-values-scroll"><table><thead><tr id="historyHead"><th>학습 회차</th><th>학습 손실</th><th>검증 손실</th><th>검증 정확도 원비율</th><th>검증 AUC</th><th>학습률</th></tr></thead><tbody id="observedHistory"></tbody></table></div></details></section>
 <section id="data" class="data-section"><div class="section-heading"><h2>데이터 구성</h2><span>원본 <strong id="originalCount">1,097</strong>장</span></div><div class="table-scroll"><table><thead><tr><th>분할</th><th>OK</th><th>NG</th><th>합계</th></tr></thead><tbody id="splits"><tr><td colspan="4">분할 기록 대기</td></tr></tbody></table></div><p class="data-labels">OK 양성·정상 <strong>536</strong><span></span>NG 악성 <strong>561</strong></p><div class="sample-target"><span>이번 회차 학습량</span><strong>클래스당 5,000개</strong><small>학습에만 온라인 증강 적용</small></div></section></div>
-<div class="bottom-grid"><section class="evaluation"><div class="section-heading"><h2>시험 결과</h2><span id="evaluationNote">시험 평가 후 표시</span></div><div class="metrics"><div>정확도<strong id="testAccuracy">미측정</strong></div><div>AUC<strong id="testAuc">미측정</strong></div></div><p class="precision-note">정확도는 소수 첫째 자리까지 반올림해요. 100.0%로 보여도 모두 맞혔다는 뜻은 아닐 수 있어요. 원비율과 정답 수를 확인하세요.</p><details class="observed-values"><summary>🔢 저장된 원값과 표시 방법 보기</summary><p>정확도 요약은 소수 첫째 자리까지 반올림합니다. 아래 원비율·AUC·손실은 받은 숫자의 전체 자릿수입니다. 지수 표기(e)는 작은 수를 짧게 쓰는 방식입니다.</p><dl><div><dt>실제로 맞힌 사진 수</dt><dd id="testCorrectCount">정답 수 미측정</dd></div><div><dt>정확도 원비율</dt><dd id="testAccuracyRaw">미측정</dd></div><div><dt>백분율 전체 자릿수</dt><dd id="testAccuracyFull">미측정</dd></div><div><dt>AUC 원값</dt><dd id="testAucRaw">미측정</dd></div><div><dt>시험 손실 원값</dt><dd id="testLossRaw">미측정</dd></div></dl></details></section><section id="records" class="record-section"><div class="section-heading"><h2>작업 기록</h2><span id="updated">갱신 시각 확인 중</span></div><p id="record">기록 대기</p><p class="error" id="error"></p><p id="freshness" class="freshness">관측 대기</p></section></div>
+<div class="bottom-grid"><section class="evaluation"><div class="section-heading"><h2>분류 정확도</h2><span id="evaluationNote">시험 평가 후 표시</span></div><div class="metrics"><div>정확도<strong id="testAccuracy">미측정</strong></div><div>AUC<strong id="testAuc">미측정</strong></div></div><p class="precision-note">정확도는 소수 첫째 자리까지 반올림해요. 100.0%로 보여도 모두 맞혔다는 뜻은 아닐 수 있어요. 원비율과 정답 수를 확인하세요.</p><details class="observed-values"><summary>🔢 저장된 원값과 표시 방법 보기</summary><p>정확도 요약은 소수 첫째 자리까지 반올림합니다. 아래 원비율·AUC·손실은 받은 숫자의 전체 자릿수입니다. 지수 표기(e)는 작은 수를 짧게 쓰는 방식입니다.</p><dl><div><dt>실제로 맞힌 사진 수</dt><dd id="testCorrectCount">정답 수 미측정</dd></div><div><dt>정확도 원비율</dt><dd id="testAccuracyRaw">미측정</dd></div><div><dt>백분율 전체 자릿수</dt><dd id="testAccuracyFull">미측정</dd></div><div><dt>AUC 원값</dt><dd id="testAucRaw">미측정</dd></div><div><dt>시험 손실 원값</dt><dd id="testLossRaw">미측정</dd></div></dl></details></section><section class="evaluation privacy-evaluation" aria-label="원본 후보 조건의 복원 저항 점수"><div class="section-heading"><h2>🔐 프라이버시 제안 점수 · 100점 만점</h2><span id="privacyState" role="status">아직 계산하지 않았습니다</span></div><div class="metrics"><div>정해진 원본 후보 공격에서 측정한 연구용 점수<strong id="privacyScore">미측정</strong></div></div><p>높을수록 이 공격에서 되찾기 어렵습니다. 소수 첫째 자리 반올림 · 0점은 이 공격에서 원본을 그대로 찾았다는 뜻일 수 있습니다. 낮은 점수도 실제 계산값 그대로 표시합니다.</p><p>공격자는 원영상 후보 모음(gallery)과 알려진 인코더·블러·전처리를 사용합니다. 정확한 특징 바이트 사전 공격을 포함한 이 조건에서만 비교하세요. 전체 프라이버시·환자 재식별 방어·임상 효과를 보장하지 않습니다.</p><details class="observed-values"><summary>🔢 점수 원값과 계산 조건 보기</summary><dl><div><dt>점수 원값</dt><dd id="privacyScoreRaw">미측정</dd></div><div><dt>점수 버전</dt><dd id="privacyVersion">gallery-residual-v1 · 측정 대기</dd></div><div><dt>원영상 후보 그룹 수 G</dt><dd id="privacyGroups">미측정</dd></div><div><dt>공격 잔여 T_attack</dt><dd id="privacyAttack">미측정</dd></div><div><dt>특징 없는 동일 후보 기준 T_prior</dt><dd id="privacyPrior">미측정</dd></div><div><dt>원본 정확 반환 그룹 수</dt><dd id="privacyExposure">미측정</dd></div><div><dt>동점 분할 원본 찾기 원비율</dt><dd id="privacyMatching">미측정</dd></div><div><dt>그룹별 잔여 분포</dt><dd id="privacyDistribution">미측정</dd></div></dl><p>P = 100 × clip(T_attack / T_prior, 0, 1). 후보별 MSE를 동일 후보 기준 오차로 나누고 0~1로 제한한 뒤 동점 후보·그룹 순서로 평균냅니다. 환자 그룹이 아닌 같은 전처리 원영상 그룹을 균등하게 셉니다. 평균값은 일부 그룹의 노출을 가릴 수 있으므로 정확 반환 수와 분포도 확인하세요.</p><p>연구용 제안 점수입니다. 표준 지표가 아니며 문헌상 신규성과 독창성은 검증되지 않았습니다. 차등 프라이버시(DP) 보장이나 보호 확률을 뜻하지 않습니다. 고정된 첫 합성곱을 사용하므로 같은 강도의 특징 점수는 후단 독립 학습과 관계없이 같을 수 있습니다.</p></details></section><section id="records" class="record-section"><div class="section-heading"><h2>작업 기록</h2><span id="updated">갱신 시각 확인 중</span></div><p id="record">기록 대기</p><p class="error" id="error"></p><p id="freshness" class="freshness">관측 대기</p></section></div>
 <footer><strong>영상 단위 예비실험</strong><span>환자 단위 독립성은 확인되지 않았습니다.</span><small>읽기 전용 · 3초마다 갱신</small></footer></main><script type="module" src="/app.js"></script></body></html>
````

## web/scene.js

| 구분 | 이전 | 이후 |
| --- | --- | --- |
| 상태 | 수정 | 수정 |
| 바이트 | 45631 | 45296 |
| SHA-256 | e43b84e493169610e2dfd0de886b2c322ec70a0dd10e752c00a12468699bbd02 | 3c7c9f2ea8688a87e6026343504dd3e1c10f17a7747a0119c9070b10d1387f18 |

````diff
--- a/web/scene.js
+++ b/web/scene.js
@@ -33,7 +33,7 @@
   const learning=document.createElement('div');learning.className='pipeline-learning';
   const learningTitle=document.createElement('strong'),learningNote=document.createElement('span');
   easyText(learningTitle,'✏️ 배우는 곳: 모델 맨 뒤의 두 부분');
-  learningNote.textContent='블러 0에서 마지막 잔차 블록과 분류층을 한 번만 100회 학습합니다. 검증 손실이 가장 낮은 모델 한 개를 고정하고, 같은 모델에 열 가지 블러 강도를 적용해 평가해요. 강도마다 다시 배우지 않아요.';
+  learningNote.textContent='각 블러 강도마다 새 ImageNet 초기값에서 마지막 잔차 블록과 분류층을 100회 학습합니다. 해당 모델의 분류 성적과 복원 저항 점수 계산을 마치면 다음 강도를 새로 학습해요.';
   learning.append(learningTitle,learningNote);viewport.before(learning);
   const technical=document.createElement('details');technical.className='pipeline-technical';
   const summary=document.createElement('summary');easyText(summary,'🔧 정확한 모델 구조 보기');
@@ -48,12 +48,12 @@
 
   // 완료 강도 × 세 범주 × 여섯 단계를 파일 ID로 구분해 전체 구성을 보여줍니다.
   const gallery=document.createElement('section');gallery.className='pipeline-gallery';gallery.setAttribute('aria-label','블러 강도별 원본과 특징 맵 전체 구성');
-  const galleryTitle=document.createElement('h2');easyText(galleryTitle,'🖼️ 7차 사진과 특징 그림 살펴보기');
+  const galleryTitle=document.createElement('h2');easyText(galleryTitle,'🖼️ 8차 사진과 특징 그림 살펴보기');
   const galleryDescription=document.createElement('p');galleryDescription.className='pipeline-gallery-description';
-  galleryDescription.textContent='7차에서 새로 만든 대표 사진을 기다리고 있어요. 이전 실험의 사진은 섞어 보여 주지 않습니다. 준비되면 강도와 자료를 골라 원본 1장과 특징 5단계를 볼 수 있어요.';
+  galleryDescription.textContent='8차에서 새로 만든 대표 사진을 기다리고 있어요. 이전 실험의 사진은 섞어 보여 주지 않습니다. 준비되면 강도와 자료를 골라 원본 1장과 특징 5단계를 볼 수 있어요.';
   const galleryNormalization=document.createElement('p');galleryNormalization.className='pipeline-gallery-normalization';
   galleryNormalization.textContent='특징 사진 한 장에는 작은 그림 10개가 있어요. 전체 평균 1개, 가장 큰 반응 1개, 골라낸 특징 8개입니다. 그림마다 색의 기준이 달라요. 밝은 곳이 암의 위치나 확률은 아닙니다.';
-  const galleryStatus=document.createElement('p');galleryStatus.className='pipeline-gallery-status';galleryStatus.setAttribute('role','status');galleryStatus.setAttribute('aria-live','polite');galleryStatus.textContent='7차 대표 사진은 아직 없어요. 새 생성 결과를 기다리고 있어요.';
+  const galleryStatus=document.createElement('p');galleryStatus.className='pipeline-gallery-status';galleryStatus.setAttribute('role','status');galleryStatus.setAttribute('aria-live','polite');galleryStatus.textContent='8차 대표 사진은 아직 없어요. 새 생성 결과를 기다리고 있어요.';
   const galleryStatistics=document.createElement('p');galleryStatistics.className='pipeline-gallery-statistics';
   const sigmaFieldset=document.createElement('fieldset');sigmaFieldset.className='pipeline-gallery-controls';
   const sigmaLegend=document.createElement('legend');easyText(sigmaLegend,'🌫️ 1. 얼마나 부드럽게 만들까요? 숫자가 클수록 더 부드러워요');
@@ -109,7 +109,7 @@
     const rows=[['현재 블러 강도',`σ = ${settingNumber(item.sigma)}`],['원본 범주',label],['처리 단계',original?'0단계 · 원본 CT':`${item.stage}단계 · ${places[item.stage]}`],['추출 지점',settingText(settings.layer)],
       [original?'입력 크기 (채널 × 높이 × 너비)':'특징 크기 (채널 × 높이 × 너비)',shape?shape.map(settingNumber).join(' × '):'미확인'],['실제 채널 수',shape?settingNumber(shape[0]):'미확인'],
       ['선택한 채널',original?'해당 없음 · 원본 한 장':indices?indices.map(settingNumber).join(' · ')||'없음':'미확인'],['그림 구성',original?'원본 CT 1패널':`평균 · 최댓값 · 개별 ${indices?indices.length:'미확인'}채널 (총 ${settingNumber(settings.panel_count)}패널)`],
-      ['색 정규화',settingText(settings.normalization)],['사진 생성 정밀도',settingText(settings.precision)],['입력 전처리',settingText(settings.preprocessing)],['고정 모델의 선정 학습 회차',typeof settings.checkpoint_epoch==='number'?`${settingNumber(settings.checkpoint_epoch)}회`:'미확인'],['공통 모델 학습 강도',settings.training_sigma===0?'σ 0':'미확인'],['이 강도 평가 중 추가 갱신',settingNumber(settings.eval_optimizer_steps)],['체크포인트 SHA-256',settingText(settings.checkpoint_sha256)]];
+      ['색 정규화',settingText(settings.normalization)],['사진 생성 정밀도',settingText(settings.precision)],['입력 전처리',settingText(settings.preprocessing)],['해당 강도의 선정 학습 회차',typeof settings.checkpoint_epoch==='number'?`${settingNumber(settings.checkpoint_epoch)}회`:'미확인'],['모델 학습 강도',typeof settings.training_sigma==='number'?`σ ${settings.training_sigma}`:'미확인'],['이 강도 평가 중 추가 갱신',settingNumber(settings.eval_optimizer_steps)],['체크포인트 SHA-256',settingText(settings.checkpoint_sha256)]];
     const policy=settings.training_policy&&typeof settings.training_policy==='object'?settings.training_policy:{};
     const trainingRows=[['최적화 방법',settingText(policy.optimizer)],['학습 배치 크기',settingNumber(policy.batch_size)],['초기 학습률',settingNumber(policy.initial_learning_rate)],['가중치 감쇠',settingNumber(policy.weight_decay)],['최대 학습 회차',settingNumber(policy.max_epochs)],['조기 종료 대기 회차',settingNumber(policy.patience)],['의미 있는 손실 개선 기준',settingNumber(policy.min_delta)]];
     const limits=Array.isArray(settings.panel_minmax)?settings.panel_minmax.slice(0,original?1:10):[];
@@ -235,7 +235,7 @@
     galleryTimeout=window.setTimeout(()=>controller.abort(),8000);
     try{
       const response=await fetch('/api/feature-previews',{credentials:'same-origin',cache:'no-store',signal:controller.signal});if(disposed)return;
-      if(response.status===404){previewMessage('7차 대표 사진은 아직 없어요. 새 생성 결과를 기다리고 있어요.');return;}
+      if(response.status===404){previewMessage('8차 대표 사진은 아직 없어요. 새 생성 결과를 기다리고 있어요.');return;}
       if(!response.ok)throw new Error('preview unavailable');
       const payload=await response.json();if(disposed)return;
       if(typeof payload.run_id!=='string'||!previewRunPattern.test(payload.run_id)||!Array.isArray(payload.items)){previewMessage('현재 실행에 맞는 전체 특징 맵을 기다리는 중입니다.');return;}
@@ -246,7 +246,7 @@
       completedSigmas=new Set(sigmaOrder.filter(readySigma));
       if(externalSigma!==null)selectedSigma=externalSigma;else if(selectedSigma===null||!completedSigmas.has(selectedSigma))selectedSigma=sigmaOrder.find(sigma=>completedSigmas.has(sigma))??null;
       renderGallery();
-      previewMessage(completedSigmas.size?'완료된 강도와 범주를 선택하면 원본부터 5단계까지 6개 그림이 아래에 모두 표시됩니다.':'7차 대표 사진의 새 생성 결과를 기다리고 있어요.');
+      previewMessage(completedSigmas.size?'완료된 강도와 범주를 선택하면 원본부터 5단계까지 6개 그림이 아래에 모두 표시됩니다.':'8차 대표 사진의 새 생성 결과를 기다리고 있어요.');
     }catch(error){
       if(!disposed)previewMessage(galleryFigures.size?'선택한 그림을 표시하고 있습니다. 목록을 잠시 갱신하지 못했습니다.':'전체 특징 맵을 기다리는 중입니다. 현재 미리보기를 불러올 수 없습니다.');
     }finally{window.clearTimeout(galleryTimeout);galleryTimeout=0;galleryBusy=false;if(galleryController===controller)galleryController=null;}
@@ -332,7 +332,7 @@
       const selected=i===active;modules[i].rail.color.setHex(selected?(dark?0xbed3ef:0x5d80b1):(dark?0x5e7392:0xb7c8de));
       cards[i].classList.toggle('is-active',selected&&running);
     }
-    easyText(learningTitle,'✏️ 한 번 학습한 모델을 고정하여 비교합니다');
+    easyText(learningTitle,'✏️ 강도마다 독립 학습 후 정확도와 복원 저항을 비교합니다');
     viewport.dataset.pipelineState=running?'running':status;dirty=true;
   }
   function setTheme(theme){dark=theme==='dark';for(const {m,type} of themed)m.color.setHex(colors[type][dark?1:0]);ambient.intensity=dark?1.1:1.3;key.intensity=dark?2.1:2.6;fill.intensity=dark?1.5:1.2;floorMaterial.opacity=dark?.25:.14;repaintLabels();updateState();}
````

## web/style.css

| 구분 | 이전 | 이후 |
| --- | --- | --- |
| 상태 | 수정 | 수정 |
| 바이트 | 39533 | 39979 |
| SHA-256 | fab23d7ab7221a32f0cf21ad06946ffe61fd06e70184b042f6a9848f460da1c6 | f2b81d0a0377c2ee1afd9df245324e5ac309bba33438f64c64907eaa6706b303 |

````diff
--- a/web/style.css
+++ b/web/style.css
@@ -44,3 +44,6 @@
 .fixed-model-proof code,#selectedCheckpoint{overflow-wrap:anywhere;word-break:break-all;font:inherit}
 [data-theme="dark"] .fixed-model-proof{background:#182231;border-color:#34445a}
 [data-theme="dark"] .fixed-model-proof p{color:#b3c2d7}
+
+/* 점수와 정확도를 나란히 읽고 작업 기록은 전체 폭을 사용합니다. */
+.bottom-grid>.record-section{grid-column:1/-1}.privacy-evaluation{min-width:0}.privacy-evaluation>.section-heading{align-items:flex-start;flex-wrap:wrap;gap:8px}.privacy-evaluation h2{font-size:22px}.privacy-evaluation>p{font-size:12px;color:var(--muted);line-height:1.9;margin-top:12px}.privacy-evaluation .metrics{padding-left:0}.queue>button.error{color:var(--error);border-color:var(--error)}
````

## 결과/측정상태.json

| 구분 | 이전 | 이후 |
| --- | --- | --- |
| 상태 | 추가 | 추가 |
| 바이트 | 0 | 1569 |
| SHA-256 | 없음 | a3f027b01451b0ab42774ca4b88ada223bb378b385f54179dafaf53af4fa0ac6 |

````diff
--- a/결과/측정상태.json
+++ b/결과/측정상태.json
@@ -0,0 +1,71 @@
+{
+  "protocol": "independent-sigma-privacy-v1",
+  "score_version": "gallery-residual-v1",
+  "measurement_status": "training_in_progress",
+  "research_results": false,
+  "conditions": [
+    {
+      "sigma": 0,
+      "classification": null,
+      "privacy_score": null,
+      "status": "training"
+    },
+    {
+      "sigma": 1,
+      "classification": null,
+      "privacy_score": null,
+      "status": "pending"
+    },
+    {
+      "sigma": 2,
+      "classification": null,
+      "privacy_score": null,
+      "status": "pending"
+    },
+    {
+      "sigma": 4,
+      "classification": null,
+      "privacy_score": null,
+      "status": "pending"
+    },
+    {
+      "sigma": 8,
+      "classification": null,
+      "privacy_score": null,
+      "status": "pending"
+    },
+    {
+      "sigma": 16,
+      "classification": null,
+      "privacy_score": null,
+      "status": "pending"
+    },
+    {
+      "sigma": 32,
+      "classification": null,
+      "privacy_score": null,
+      "status": "pending"
+    },
+    {
+      "sigma": 64,
+      "classification": null,
+      "privacy_score": null,
+      "status": "pending"
+    },
+    {
+      "sigma": 128,
+      "classification": null,
+      "privacy_score": null,
+      "status": "pending"
+    },
+    {
+      "sigma": 256,
+      "classification": null,
+      "privacy_score": null,
+      "status": "pending"
+    }
+  ],
+  "note": "2026-11-20확인 시점 σ0 학습 중. 분류/점수 미측정. 합성대조군/예비분모를 실제모델성적으로 대입하지 않음.",
+  "observed_date": "2026-11-20",
+  "current_sigma": 0
+}
````

## 안전_학습.py

| 구분 | 이전 | 이후 |
| --- | --- | --- |
| 상태 | 수정 | 수정 |
| 바이트 | 198 | 197 |
| SHA-256 | b741bffe8b712bcd28c6856cf32eb916e055390ab4f7d26f9ac5381eef460416 | 42178d0526c418910b52535fb2a2f4eff505898d70806813d5a09a8e02189758 |

````diff
--- a/안전_학습.py
+++ b/안전_학습.py
@@ -1,4 +1,4 @@
-"""검증한 새 입력 기준으로 σ0 학습 한 번과 고정 모델 평가를 감독합니다."""
+"""검증한 새 입력 기준으로 강도별 독립 학습과 분류·점수를 감독합니다."""
 
 from tools.safe_training import main
 
````

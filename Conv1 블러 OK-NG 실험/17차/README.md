# 17차 · 폐결절 블러의 분류 성능과 복원 저항성

LUNA25의 환자별 분할과 결절 중심 단면을 사용해 블러 강도마다 새 모델을 학습하는 구현입니다. **현재는 공식 주 자료 준비와 코드 검토 단계이며 17차 GPU 성능 결과는 아직 없습니다.** 과거 실험의 높은 정확도를 새 결과로 가져오지 않습니다.

| 자료 | 역할 | 상태 |
|---|---|---|
| LUNA25 | 새 주 학습·검증·시험 자료 | 2,120명·6,163결절 준비, 고정 기하 적격성 제외0 |
| Histo | 외부 단면 시험 후보 | 306장·88개 공식 serial의 결절 ROI 준비. 중복 serial 픽셀 대응 2장은 사전 제외. GPU 외부 결과 미측정 |
| CSTL | 외부 시험 후보 | 라벨은 확인됐으나 환자·대상 결절 대응 보류 |

| 항목 | 고정 조건 |
|---|---|
| 입력 | 공식 결절 좌표, 50×50mm 중심 단면, 512×512, HU−1000~400 |
| 환자 분할 | seed42, 70/15/15. 학습1,484명·4,353결절, 검증318명·937결절, 시험318명·873결절 |
| 원라벨 | OK=양성 결절, NG=악성 결절. 정상군을 합친 과거 실험과 다름 |
| 독립 학습 | ResNet50 Conv1 분할20조건+전체 연결20조건, 보조5개를 포함한 고유45개 학습 |
| 강도 | 0,1,2,4,6,8,10,12,16,20,24,32,40,48,64,80,96,128,192,256 |
| 고정 학습 | 시작 때 OK5,000·NG5,000개를 한 번 생성·저장. 매 에폭 같은 파일 사용 |
| 시험 | 주시험은 무증강873결절. 보조는 보류 시험 안에서 각1,000행을 고정 생성하며 독립 표본 증가로 세지 않음 |
| 선정 | 고정 검증 OK/NG각1,000개(총2,000행)의 손실로 선정. 원본 검증937개 별도 보고. 최대200·최소30·patience25 |
| 블러 | 입력에 Gaussian 한 번. output pixel 기준 sigma이며 1pixel=50/512mm |
| 특징 | Conv1/stem/layer1~4 × FP32/FP16/INT8, 실제 Rust encode/decode 후 분류·공격 |

## 준비와 실행

이 저장소에는 영상·환자 목록·예측·모델 가중치·비공개 운영 기록을 넣지 않습니다. 공식 출처와 라이선스는 `공식자료.json`에서 확인합니다. 공식 파일을 내려받아 체크섬을 확인하고 입력 manifest를 준비해야 합니다.

```powershell
Copy-Item SCIconfig.example.json SCIconfig.json
Copy-Item config.example.json config.json
python -B -X utf8 SCI데이터.py list --group nodule-blocks
python -B -X utf8 SCI데이터.py download --group annotations
python -B -X utf8 SCI데이터.py download --group nodule-blocks
python -B -X utf8 SCI데이터.py extract --group nodule-blocks --destination ./work/data/blocks
python -B -X utf8 SCI데이터.py prepare --blocks ./work/data/blocks
python -B -X utf8 SCI데이터.py status
# 공식 초기 가중치를 work/weights에 별도로 준비한 뒤 아래 SHA와 대조합니다.
Get-FileHash -Algorithm SHA256 ./work/weights/resnet50_initial.pth
Get-FileHash -Algorithm SHA256 ./work/weights/resnet18-f37072fd.pth
# 빌드.py의 설치된 Rust/MSVC/SDK 경로를 지원 환경에 맞게 준비합니다.
New-Item -ItemType Directory -Force docs | Out-Null
python -B -X utf8 빌드.py
Get-Content -LiteralPath ./docs/Rust_빌드결과.json
python -B -X utf8 SCI실행.py --prepare
# 기존 12차 전체 완료 확인 이후에만 실행합니다. 중복 실행하지 않습니다.
python -B -X utf8 SCI실행.py --run --device cuda
```

실행 전에 두 설정 예제의 `runtime`, `manifest`, `data_status`, `weights`의 파일 경로와 `fixed_samples_root`를 실제 로컬 위치로 지정하세요. `/path/to/…`는 자리표시자이며 그대로 실행하는 경로가 아닙니다. 준비·학습·재개 모두 같은 설정과 고정표본 폴더를 사용합니다.

두 초기 가중치는 torchvision의 ImageNet ResNet50 V1(`resnet50-0676ba61.pth`)과 ResNet18 V1(`resnet18-f37072fd.pth`)입니다. 전체 SHA256은 각각 `0676ba61b6795bbe1773cffd859882e5e297624d384b6993f7c9e683e722fb8a`, `f37072fd47e89c5e827621c5baffa7500819f7896bbacec160b1a16c560e07ec`이며 예제의 경로와 실제 파일이 같아야 합니다. 검사 실패를 우회하지 않습니다. 빌드 결과 exit_code=0, 실제 전송엔진 파일·SHA와 원본 소스 SHA를 확인한 뒤 실행합니다.

화면은 별도 터미널에서 `node './대시보드 화면/server.mjs'`로 열며 주소는 http://127.0.0.1:8788/ 입니다. 현재 서버의 기본 work/data 경로는 연구 운영 위치에 고정돼 있으므로 새 환경에서는 `createServer({work:실제런타임,dataRoot:실제자료폴더})`를 import하는 로컬 실행기를 만들고 같은 포트에 listen해야 합니다. 예제 설정만 바꿔도 화면 경로가 자동 변경되는 구조는 아닙니다.

외부 자료는 다운로드만으로 완료하지 않습니다. 공식 분류 라벨과 환자·결절 대응을 검토한 mapping, 교차 코호트 검토문이 있을 때만 prepare의 `--histo-mapping`, `--cstl-mapping`, `--cross-review`를 지정합니다. 검토 자료의 영상별 목록은 공개하지 않습니다. LUNA-only 준비 뒤 외부 자료를 추가하려면 GPU/run binding 전에 새 manifest를 확정합니다. Histo의 128px 중심 crop은 BMP 밝기 영역이며 LUNA의 50mm/HU 입력과 같은 물리 영역이 아닙니다.


Python에 PyTorch·torchvision·NumPy·SciPy·Pillow·psutil·scikit-learn, 화면에 Node.js가 필요합니다. 물리 volume 외부 경로에는 SimpleITK가 별도로 필요합니다. Rust 전송 엔진은 소스로 제공하며 `빌드.py`의 기존 Windows MSVC/Rust/SDK 위치를 자신의 지원 환경에 맞게 준비해야 합니다. 실행 파일은 포함하지 않았습니다. 환경 자동 설치나 권한 변경을 수행하는 패키지가 아닙니다.

현재 연구 운영용 `require_previous_experiment_complete`는 이전12차의 전체40조건 완료를 확인하고 GPU 시작을 막습니다. 다른 환경에서 곧바로 범용 학습을 실행할 수 있는 설치 패키지로 검증하지 않았습니다. 실제 연구에서는12차가 모두 끝난 다음 새17차를 시작합니다. 현재 진행 중인 다른 실험을 검증을 위해 중단하지 않습니다.

## 지표와 해석

| 지표 | 저장·해석 |
|---|---|
| 분류 | 정답수/분모·원비율, 백분율만 한 자리 반올림. 완전 정답과 반올림100.0% 구분 |
| 상대 복원오차 | 100×clip(공격MSE/학습 평균영상 기준MSE,0,1), 분모0이면 미정의 |
| 구조 훼손 | 100×clip(1−SSIM,0,1), 원SSIM도 보존 |
| 연결/멤버십 | 닫힌 후보 집합Top-k와 선정 점수 공격AUC. 복원과 서로 다른 위협 |
| 불확실성 | 원본 환자 단위 군집95%구간, 반복 생성행을 독립 환자로 간주하지 않음 |

0~100점은 선언한 공격·기준에 대한 탐색 척도이며 보호 확률·차등프라이버시 보장·세계 최초 수식이 아닙니다. 공격은 train에서 학습하고 validation에서 선택하며 test는 보고에 씁니다. 정확도100%를 피하기 위해 오답이나 분할을 조작하지 않습니다.

결절 위치가 제공된 분류 연구이며 자동 검출·임상 진단 성능이 아닙니다. 공식 라벨을 모든 사례의 동일 병리 확진으로 바꾸어 설명하지 않습니다. 고정 결절 패치에도 주변 조직 단서가 남을 수 있어 중앙/주변/거친 단서 진단과 train-only 라벨셔플 대조를 분리합니다.

## 확인 범위

현재 공격·셔플 수리는 신규6·영향3·최종진단1 검사로, 화면 변경은 신규1·관련2 검사로 확인했습니다. 독립 검토에서는 실제 ResNet50의6층×3정밀도 원본공격 경계를 축소 CPU로 확인했습니다. 변경없는 데이터10·Rust18 근거는 재사용하며 과거 엔진9/UI2와 고정표본9·bind1은 선행 범위로 구분합니다. 실제 LUNA25 입력 준비와 분할 간 환자·원본/영상/픽셀 해시 필드 비중복은 별도 확인했습니다. 합성 CPU 검사는 장시간 GPU 완료나 외부 성능을 입증하지 않습니다. 현재 차수는 미측정이며 수치를 만들어 채우지 않습니다.

[다섯 읽기 수준과 구현 설명](../../docs/revisions/conv1-okng-round17.md#user-content-reading-level-5) · [공개 파일 비교](../../docs/revision-diffs/conv1-okng-round17.md) · [저장소 첫 화면](../../README.md)

## 한 번 생성한 표본과 강도별 사본

원본과 환자별 분할은 보존합니다. 시작 시 학습각5,000개·검증각1,000개·시험각1,000개, 총14,000개를 한 번 고정 생성합니다. 매 에폭 새 표집이나 랜덤증강을 하지 않습니다. 각sigma는 기본셋을 새 일반 폴더에 실제 복사하고 Gaussian을 한 번 적용합니다. 같은sigma 두모델은 동일단계자료를 재사용합니다. 앞강도의결과를다음강도에누적블러하지않습니다.

계산용은Gaussian의float32결과TIFF이며 PNG는보기용입니다. 분류와복원공격은같은저장노출값을사용하고모델안에서다시블러하지않습니다. 추가8bit양자화로보호성능이달라지는것을피합니다. 원본검증937·원본시험873개는고정균형평가와따로보존합니다. [전체 저장·계보 설계](docs/고정표본과_강도별사본_설계.md)를 참고합니다. 대량파일생성은정식시작때실행하며이번코드수정의작은합성검사와구분합니다.

## 복원 공격·라벨 셔플·화면 평가 집합 보완

블러 전 원본 후보에 Gaussian과 특징 추출·전송 정밀도 변환을 적용해 관측 특징과 맞추는 원본 공간 공격을 추가했습니다. 기존 관측 공간·DCT·학습 디코더·선형 공격은 유지하며 두 고정 초기값의 선택에 시험 정답은 사용하지 않습니다. FP16/INT8 역전파는 STE 근사입니다. 라벨 셔플은 원본 source_id 단위로 하여 사본마다 같은 라벨을 쓰고 원본/증강 후 분포를 따로 기록합니다. 원본·증강 시험, 균형·원본 검증은 API와 화면에서 각각 연결하며 없는 지표는 다른 집합 값으로 대체하지 않습니다. 연결은 float 층 특징, 멤버십은 분류 출력 평가로 전송 정밀도별 복원 공격과 구분합니다. [상세 방법](docs/복원공격과_평가집합_수정.md). 실제 GPU 성능은 아직 미측정입니다.

## 연결 공격·캐시·공격 진행 후속 수정

| 항목 | 현재 동작 | 해석 |
|---|---|---|
| 연결 공격 | 고유 source_id별 gallery 1개, canonical 우선; query 전체 유지 | 복사본도 같은 원본을 찾으면 정답, 증강은 독립 원본 증가 아님 |
| 완료 캐시 | 공격은 run_id, 조건은 run_id·protocol·condition 검증 | 다르면 거부하고 원본 저장 결과 보존 |
| 진행 표시 | 디코더·복원·연결·멤버십·셔플의 실제 처리 수 | 분류 회차·정확도와 구분, 미래 완료 수를 만들지 않음 |

[수정 상세](docs/연결공격_캐시_진행표시_수정.md). 이번 변경은 CPU 신규4/API·화면 함수1, 영향 CPU8/기존 UI2 및 별도 보완검토의 범위입니다. 앞 절의 공격6/영향3/후속1 기록은 선행 수정의 근거이며 이번 소스의 전체 실행 검증이 아닙니다. 실제 GPU 전체·새 데이터 생성·브라우저 조작 검증은 별도입니다. 운영 원본README와 달리 이 공개README는 기존 공개 명령·example설정·포터블실행 안내를 보존합니다.

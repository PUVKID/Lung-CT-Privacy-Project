# 17차 · 환자 분할 기반 폐결절 입력 블러 연구

[LEVEL 1](#user-content-reading-level-1) · [LEVEL 2](#user-content-reading-level-2) · [LEVEL 3](#user-content-reading-level-3) · [LEVEL 4](#user-content-reading-level-4) · [LEVEL 5](#user-content-reading-level-5)

[자료](../../Conv1%20블러%20OK-NG%20실험/17차/) · [전체 비교](../revision-diffs/conv1-okng-round17.md) · [전체 차수](../REVISION_INDEX.md)

<details open>
<summary>LEVEL 1 · Beginner</summary>

<a id="reading-level-1"></a>

원래 사진을 되찾는 공격도 더해 봅니다. 원본 후보를 흐리게 하고 같은 특징이 나오는지 맞추므로, 흐린 사진까지만 찾는 공격과 구분합니다. 같은 원본에서 늘린 사진에는 셔플 진단의 정답도 같게 붙입니다. 화면의 원본 시험·늘린 시험·검증을 바꾸면 그 집합의 수치만 보여 주며 없으면 미측정이라고 씁니다.

## LEVEL 1 - Beginner

이번에는 사진을 처음에 한 번만 늘려 저장합니다. 학습은 양성 5,000·악성 5,000, 검증과 시험은 각각 양성 1,000·악성 1,000입니다. 블러 0·1·2…는 이 같은 14,000개 구성을 복사해 씁니다. 시험마다 다른 사진을 뽑거나 매회 새 증강을 하지 않습니다. 고정 검증 2,000개로 모델을 고르고 원본 검증 937개도 따로 봅니다. 계산용 float32 사진과 보기용 PNG를 구분하며 분류와 복원은 같은 블러 값을 읽습니다.

사진에서 작은 결절(폐 속 덩어리)의 위치를 먼저 찾은 자료로, 흐림이 분류와 원래 사진 복원에 어떤 영향을 주는지 봅니다. OK는 양성 결절, NG는 악성 결절입니다. 정상 사진을 OK에 합쳤던 과거 차수와 자료가 다릅니다.

| 순서 | 하는 일 | 왜 필요한가요? |
|---|---|---|
| 1 | 공식 LUNA25 자료의 2,120명·6,163결절을 준비 | 사진 파일을 복사했다고 새 사람이 생기지는 않아요 |
| 2 | 사람별로 학습 1,484명/4,353결절, 검증 318명/937결절, 시험 318명/873결절로 나눔 | 같은 사람이 배우는 쪽과 시험 쪽에 섞이지 않게 해요 |
| 3 | 결절 중심 50×50mm를 512×512칸으로, 밝기는 HU−1000~400으로 고정 | 사진 크기와 밝기 범위를 맞춰요 |
| 4 | 흐림 정도와 모델 연결 방식별로 처음부터 별도 학습 | 먼저 배운 답을 다음 강도에 물려주지 않아요 |
| 5 | 새 시험 사진을 분류하고 원본을 되찾는 공격도 따로 시도 | 정답을 잘 맞히는 것과 사진을 못 되찾는 것은 달라요 |

흐림 숫자는 0, 1, 2, 4, 6, 8, 10, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96, 128, 192, 256 입니다. 숫자 0은 흐림 없음, 숫자가 커질수록 더 넓게 섞습니다. 단위는 완성 사진의 칸(pixel)이며 한 칸은 50/512mm입니다. 사진에 Gaussian 흐림을 한 번 넣고 모델에 전달합니다.

기본 ResNet50은 기계가 보는 작은 필터인 Conv1에서 앞뒤로 나눈 방식 20개와 전체를 연결한 방식 20개입니다. 별도 확인 5개는 더 작은 ResNet18의 흐림 0 한 개, ResNet50의 stem/layer1 경계에서 흐림 0/32 네 개여서 총 45개입니다. 같은 조건은 같은 시작 가중치에서 새로 배웁니다. 마지막에는 평균을 모으는 avgpool과 두 종류를 가르는 출력층(FC1)을 씁니다.

시작 때 OK5,000개·NG5,000개를 한 번 만들어 저장하고, 매 학습 회차에는 그 같은 파일을 보여 줍니다. 시험은 원래 873결절의 무증강 점수가 중심입니다. 시험 안에서 OK1,000행·NG1,000행을 만들기도 하지만 같은 원본의 보조 시험이지 2,000명의 시험이 아닙니다. 최대 200회, 적어도 30회를 배우며 검증 손실(연습시험 오차)이 25회 개선되지 않으면 멈춥니다. 최저 검증 손실 모델을 보관하고 최종 시험 점수로 모델을 고르지 않습니다.

사진 복원 공격 9종과 특징(기계가 만든 중간 표현) 복원은 Conv1/stem/layer1~4의 6곳, FP32/FP16/INT8의 3가지 숫자 저장 방식으로 봅니다. Rust가 실제로 숫자를 포장하고 다시 푼 뒤 분류와 공격을 합니다. 비슷한 원본을 후보 목록에서 찾는Top-1/5/10, 학습에 썼던 자료인지 맞히는 멤버십 AUC도 따로 기록합니다. 공격은 학습 자료로 배우고 검증 자료로 고르며 시험은 보고에만 씁니다.

보호 점수는 공격의 평균 제곱 오차를 학습 평균 사진의 오차와 비교해 100배 하고 0~100으로 제한한 값, 그리고 사진 구조 유사도SSIM을 1에서 빼 100배 한 값입니다. 나누는 수가 0이면 계산 불가로 표시합니다. 미측정을 0점이나 100점으로 채우지 않습니다. 높은 점수도 안전 확률은 아닙니다. 정확도는 정답 수/전체 수와 원비율을 남기고 화면만 소수 첫째 자리로 반올림합니다. 사람별 묶음 95%구간도 함께 봅니다.

준비는 공식 다운로드→체크섬 확인→압축 해제→결절 사진과 환자 분할→초기 가중치 SHA→Rust 빌드→실행 준비 순서입니다. [실제 명령](../../Conv1%20블러%20OK-NG%20실험/17차/README.md#준비와-실행)을 따르고, 자료·가중치·실행 경로가 맞는지 확인합니다. Histo306장/88serial은 준비됐지만 밝기 BMP와 128칸 crop이라 LUNA와 같은 50mm/HU가 아닙니다. serial 대응이 모호한 2장은 성능을 보기 전에 제외했습니다. CSTL은 환자·결절 대응 보류입니다. 외부 자료를 모델에 다시 가르쳐 시험으로 내지 않습니다.

화면은 다크/라이트, 왼쪽 메뉴, 강도 선택, 실제 에폭 점과 대표 사진 설명을 제공합니다. 준비 대기는 결과가 아닙니다. 중앙·주변·거친 단서와 학습 라벨 섞기 대조도 따로 보아 주변 모양만 외웠는지 살핍니다. 현재 17차 GPU 결과는 없고 12차 40 조건 완료 후 시작합니다. 위치가 주어진 분류 실험이라 자동 암 탐지·임상 진단·개인정보 보호 보장이 아닙니다.

[같은 수준 프로젝트](../읽기안내/레벨1.md) · [같은 수준 프로필](https://github.com/PUVKID/PUVKID/blob/main/docs/읽기안내/레벨1.md)

</details>

<details>
<summary>LEVEL 2 · Explorer</summary>

<a id="reading-level-2"></a>

기존 공격은 남기고 블러 전 원본을 추정하는 두 초기값의 공격을 추가했습니다. 어느 초기값이 좋은지는 전달 특징과 TV 목적만으로 고르며 시험 정답으로 고르지 않습니다. 셔플 라벨은 원본별로 고정하고 사본에 전파합니다. 원본 시험 873·증강 시험 2000·원본 검증 937·균형 검증 2000을 API와 화면에서 구분합니다.

## LEVEL 2 - Explorer

고정 기본 셋 14,000행은 환자 분할 뒤 각 클래스 학습 5,000/검증 1,000/시험 1,000으로 한 번만 만듭니다. 단계마다 실제 사본을 만들어 그 강도의 blur를 한 번 적용하므로 구성 차이와 누적 블러를 통제합니다. 고정 검증 2000행 손실이 선정 기준이고 원본 검증 937행은 별도 보고입니다. float32TIFF는 분류·공격 공유 입력,PNG는 미리보기이며 원본 873시험과 생성 2000시험은 독립 환자 수로 합치지 않습니다.

이번 비교의 두 축은 남은 정보로 분류하는 능력과 그 정보에서 사진을 복원하는 능력입니다. 강도별 새 학습은 흐림에 적응하는 성능을 측정합니다. 고정 모델 하나에 강도만 바꾸는 과거 7차와 질문이 다릅니다.

| 연결 | 입력과 처리 | 비교의 기준 |
|---|---|---|
| 자료→분할 | LUNA25 6,163결절/2,120명, 공식 환자ID로seed 42·70/15/15 | train4,353/1,484명·validation937/318명·test 873/318명 |
| 좌표→영상 | 결절 중심 50mm,512px,HU−1000~400 | OK=양성결절,NG=악성결절; 정상은 별도 포함하지 않음 |
| 영상→분류 | Gaussian 한 번→ResNet→avgpool→FC1 | Conv1 분할 20·전체 연결 20, 독립 초기화 |
| 중간표현→전송 | 6층 ×3정밀도, Rust FTR1 실제 왕복 | 용량·양자화 오차·후단 분류·공격을 같은 복원값에서 계산 |
| 노출→공격 | 사진 9종, 특징 복원, Top-k 연결, 멤버십 | 각각 다른 위협을 하나의 안전 확률로 합치지 않음 |

0, 1, 2, 4, 6, 8, 10, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96, 128, 192, 256의 20강도를 씁니다. 한 출력 pixel은 0.09765625mm이고 sigma는 pixel 단위입니다. 보조 5개는 ResNet18 전체 연결sigma 0, ResNet50 stem/layer1 분할 각각sigma 0/32입니다. Conv1 sigma 0/32는 주 조건을 참조하므로 중복 재학습하지 않습니다. 총 고유 학습 45개입니다. 분할 방식은 detach한 중간값의 기울기를 앞단으로 실제 반환합니다.

train에서 OK/NG 각 5,000회 시작 때 한 번 고정 생성·저장하며 validation은 모델 선정용, test는 보고용입니다. 최대 200·최소 30·patience25이고 검증 손실 최저 모델을 따로 저장합니다. 작은 개선을 세는min_delta와 진짜 최저 손실 보존을 구분합니다. 원본 시험 873결절이 주 결과이고 test-only 반복 증강 각 1,000행은 보조 결과입니다. 같은 환자의 반복행은 독립 표본이 아니며 환자 군집 95%구간과 정답 수·분모를 함께 냅니다.

평균 영상 기준 MSE는 원본을 보지 않고 평균만 내보내는 기준의 오차입니다. 보호 오차 점수=100×clip(공격MSE/기준MSE,0,1), 구조 점수=100×clip(1−SSIM,0,1)입니다. 기준 0·미측정·정의 불가 지표는 null과 이유입니다. raw 비율과 clipping 여부를 남기며 100점은 시험한 공격에 대한 상대값입니다. Top-1/5/10은 닫힌 후보에서의 연결 성공, 멤버십 AUC는 포함 여부 구별 능력입니다. 공격 train 학습/validation선정/test 보고를 지키며 시험에서 관찰한 가장 센 공격 요약은 사후 관찰로 구분합니다.

공식자료.json→download→extract→prepare로 자료를 준비하고, 가중치 전체 SHA와 Rust 빌드를 확인해 SCI실행--prepare에 연결합니다. [명령과 화면 경로 설정](../../Conv1%20블러%20OK-NG%20실험/17차/README.md#준비와-실행)을 확인합니다. 실행 파일·영상·환자 목록은 저장소에 없습니다. Histo는 픽셀→XML결절→공식serial로 306장 88serial을 연결했으나 물리 HU/50mm가 아닌 128px BMP crop입니다. 모호한 2장은 제외, CSTL은 대응 미완료로 보류합니다. 병원 출처가 다르다고 자연인 중복 없음까지 증명하지 않습니다.

단서 진단은 중앙/주변/거친 정보와 train-only 라벨 셔플을 따로 비교합니다. 주변 조직 단서가 완전히 제거됐다고 주장하지 않습니다. 앞선 공격·셔플 수리는 신규 6·영향 3·최종진단 1 검사로, 화면 변경은 신규 1·관련 2 검사로 확인했습니다. 독립 검토에서는 실제 ResNet50의 6층×3정밀도 원본 공격 경계를 축소 CPU로 확인했습니다. 변경 없는 데이터 10·Rust18 근거는 재사용하며 과거 엔진 9/UI 2와 고정표본 9·bind1은 선행 범위로 구분합니다. GPU 측정은 아직 없습니다. 12차 40 조건 종료 후에만 17차 실행합니다. 대시보드의 메뉴·테마·강도별 실제 그래프·사진 설명은 미측정과 결과를 구분합니다. 정확도 100%를 피하려고 결과나 분할을 바꾸지 않습니다. 결절 위치 제공 분류, 단일 분할과 정해진 공격군의 탐색 연구이며 임상·DP 보장은 아닙니다.

[같은 수준 프로젝트](../읽기안내/레벨2.md) · [같은 수준 프로필](https://github.com/PUVKID/PUVKID/blob/main/docs/읽기안내/레벨2.md)

</details>

<details>
<summary>LEVEL 3 · Practitioner</summary>

<a id="reading-level-3"></a>

raw-space 역복원은 raw_guess→Gaussian→특징→dtype 전방 값을 전달 특징에 맞춥니다. train_mean/flat_0.5 초기값과 iterate는 관측 목적과 TV만으로 선택하며 공격군 선정은 validation 전용입니다. dtype 역전파는 STE 근사입니다. 원본 source_id 순열을 사본에 전파하고 원본 분포/증강 후 행 분포를 저장합니다. 선택한 평가 집합에 연결·멤버십이 없으면 다른 시험 값으로 채우지 않습니다.

## LEVEL 3 - Practitioner

SCIconfig의 고정 표본 정책과 캐시 경로를 설정하고 --prepare에서 학습 각 5000/검증 각 1000/시험 각 1000의 기본 파일을 한 번만 준비합니다. sigma 최초 진입 시에 기본 PNG 실제 복사와 float32TIFF 블러 출력을 저장합니다. 캐시 manifest/파일 SHA/정책이 바뀌면 재개를 거부합니다. 매 epoch 새 표집/온라인 hflip은 없고 동일 파일의 순서만 변경 가능합니다. 고정 검증 2000으로 선정하며 원본 검증 937과 873주 시험은 별도 결과입니다.

실행자는 자료 준비와 GPU 실행을 분리합니다. [준비와 실행 명령](../../Conv1%20블러%20OK-NG%20실험/17차/README.md#준비와-실행)에 공식 download/extract/prepare, SHA, Rust 빌드, 화면 기동의 순서가 있습니다. Python의 torch/torchvision/NumPy/SciPy/Pillow/psutil/scikit-learn, Node.js, 지원 Rust/MSVC/SDK가 필요하며 volume 외부 경로에는 SimpleITK가 추가됩니다. 설치·정책을 자동 변경하지 않습니다.

| 설정 | 값 | 산출물·실패 확인 |
|---|---|---|
| 원자료 | LUNA25 공식 주석·nodule-blocks, 환자 seed 42·70/15/15 | 준비 manifest와 개별 영상 SHA, 환자 중복이면 중단 |
| 표적 | OK양성/NG악성결절, 중심 50mm·512px·HU−1000~400 | train4,353/1,484명, val 937/318명, test 873/318명 |
| 표집 | train각 5,000개 고정 파일/epoch | 반복·증강 횟수이며 독립 원본 수가 아님 |
| 시험 | 원본 873 주시험, test-only각 1,000행 보조시험 | 정답 수/분모·원비율·환자 군집 95%구간 구분 |
| 최적화 | batch2·누적 4, AdamW lr1e−4·weight decay1e−4 | 최대 200/최소 30/patience25, 검증최저 모델 |

sigma목록은 0, 1, 2, 4, 6, 8, 10, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96, 128, 192, 256 입니다. 입력Gaussian 한 번,1pixel=50/512mm입니다. ResNet50 Conv1분할과 전체 연결을 20강도씩 새 초기모델/optimizer/scheduler/RNG로 학습합니다. 보조는 ResNet18 전체sigma 0 한 개, ResNet50 stem/layer1 분할sigma 0/32 네 개, 총 45고유 학습입니다. 표준 avgpool→FC1과 실제 detach 기울기 반환을 씁니다. 시험 점수로 모델·공격·분할을 선택하지 않습니다.

SCIconfig.example을 SCIconfig로 복사하고 runtime/manifest/data_status/weights 경로를 실제 위치로 설정합니다. 두 가중치의 전체SHA는 예제에 고정돼 있으며 불일치 때 중단합니다. 빌드 전 docs 폴더를 만들고 빌드결과exit_code=0·source/engineSHA를 봅니다. SCI실행--prepare는 입력을run에 결합하므로 외부 manifest 추가는 그 전에 끝냅니다. --run은 12차 40 조건 완료 gate를 통과해야 합니다. --resume은 같은 결합의 마지막 완료 에폭을 사용하며 미완료 배치를 정확 재현했다고 주장하지 않습니다. 화면 서버 기본경로가 고정돼 있으므로 다른 환경은createServer의work/dataRoot를 지정합니다.

분류 결과는 main test와test_generated를 별도 읽습니다. 사진 공격 9종, Conv1/stem/layer1~4×FP32/FP16/INT8 특징의 실제Rust 포장 왕복, 연결 Top-1/5/10, 멤버십 AUC를 확인합니다. 복원 공격은 train 학습/val 선정/test 보고입니다. 보호 점수는 100×clip(MSE공격/MSE학습 평균기준,0,1)와 100×clip(1−SSIM,0,1)이며 raw/clipped·분모 0/null사유를 보존합니다. 안전 확률이나DP로 보고하지 않습니다. 중앙/주변/거친 단서와train라벨 셔플 대조는 주분류와 구분합니다.

Histo306장 88공식serial은 pixel/XML 중심 128px→512 BMP 밝기crop이며 50mm/HU의 외부 복제가 아닙니다. 다중 serial 동일 픽셀 2장은 사전 제외했습니다. CSTL은 환자/결절 대응까지 준비되지 않아 보류입니다. 외부 자료의 재학습·분할선정에 시험 결과를 쓰지 않습니다. 공식 ID 내 분할과 해시 점검은 병원 간 자연인 동일성 증명이 아닙니다.

앞선 공격·셔플 수리는 신규 6·영향 3·최종진단 1 검사로, 화면 변경은 신규 1·관련 2 검사로 확인했습니다. 독립 검토에서는 실제 ResNet50의 6층×3정밀도 원본 공격 경계를 축소 CPU로 확인했습니다. 변경 없는 데이터 10·Rust18 근거는 재사용하며 과거 엔진 9/UI 2와 고정표본 9·bind1은 선행 범위로 구분합니다. GPU 성능·장기 복구는 미측정입니다. 대시보드는 실제 run/강도/에폭/사진을 연결하고 대기와 미정의를 표시합니다. 임상 사용·자동 검출·형식적 개인정보 보호를 증명하지 않습니다. 결과표를 낮추려고 오답을 만들지 않습니다.

[같은 수준 프로젝트](../읽기안내/레벨3.md) · [같은 수준 프로필](https://github.com/PUVKID/PUVKID/blob/main/docs/읽기안내/레벨3.md)

</details>

<details>
<summary>LEVEL 4 · Advanced</summary>

<a id="reading-level-4"></a>

기존 observed-space 후보에 raw_blur_aware_tv 공격군을 추가했습니다. preblurred 우회 대신 model.blur(raw_guess)를 명시하고 dtype forward는 FeatureCodec와 일치시킵니다. float/양자화의 역전파 STE와 최종 관측 목적 기반 선택은 원본 GT와 분리합니다. 셔플 source 매핑 전체는 비공개 파일로 보존하고 화면에는 집계만 냅니다. API의 validation_original/test_generated 및 membership_generated 연결을 추가해 평가 분모 혼용을 제거했습니다.

## LEVEL 4 - Advanced

고정 표본 모듈이 환자 분할 이후 source_id·canonical·고정 증강 seed를 결합하고 14,000 기본 파일을 생성합니다. sigma 폴더에는 물리 raw 사본과 DCTfloat32관측 TIFF를 저장하며 완료 marker·불완료 검증·tamper 거부를 사용합니다. 분류 forward의 관측 입력 경로는 blur를 우회하지만 공격 raw target과 cache 관측을 분리합니다. 같은 sigma의 두 regime는 동일 cache를 재사용하며 fixed validation 2000 선정/original validation 937 보고를 분리합니다.

구현의 비교 단위는(condition:model,regime,boundary,sigma)와 불변 입력 결합입니다. SCI데이터는 공식 체크섬·환자분할·기하 ROI를, SCI모델은 단일 입력 blur·표준pool/FC·splitgradient를, SCI실행은 조건 독립 학습·검증 선정·재개를, SCI공격/특징노출/전송/Rust는 실제 노출·패킷·공격을 맡습니다.

| 경계 | 설계 선택 | 변경 영향과 실패 처리 |
|---|---|---|
| 자료 | LUNA25 환자 seed 42·70/15/15, 중심 50mm/512·HU−1000~400 | 원본·환자·픽셀hash 분할 비중복, ROI SHA 불일치 거부 |
| 학습 | ResNet50 Conv1 split/full각 20, 보조 5 | 초기값/optimizer/scheduler/RNG 독립, 이전 조건 적응모델 계승 금지 |
| 상태 | manifest·config·가중치 SHA·source·실행환경 결합 | 기존binding과 다르면 중단; 완료 epoch만 재개 |
| 전송 | FTR1 f32/f16/i8 실제encode/decode | 직렬화 후단 분류/공격, 용량과양자화 오차 함께 기록 |
| 화면 | 조회 전용Node API·현재 run 연결 | 잘못된 run 사진/미측정값을 새 결과로 내지 않음 |

OK는 양성, NG는 악성 결절이고 정상은 포함하지 않습니다. 원본 6163/2120명은 train 4353/1484명,val 937/318명,test 873/318명입니다. 학습 각 5000·검증 각 1000·시험 각 1000의 시작 시 1회 고정 파일 사용은 원본 독립 수를 늘리지 않습니다. sigma는 0, 1, 2, 4, 6, 8, 10, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96, 128, 192, 256 이며 output pixel 기준 50/512mm입니다. Gaussian은 입력에 한 번만 적용하고 split은 detach 후 backward 기울기를 실제로 반환합니다. 보조 조건은 ResNet18 full sigma 0, ResNet50 stem/layer1 split 각 sigma 0/32, 총 45고유 학습입니다.

AdamW1e−4/weight decay1e−4,batch2×누적 4,max200/min30/patience25입니다. raw best validation loss 보존과 min_delta1e−4에 의한 patience 판단은 별도입니다. validation만 선정에 쓰고 test는 보고에 한정합니다. 12차 40완료 gate와 prepare/run/resume분리는 동시 GPU 실행과 입력 바꿔치기를 막지만 모든 운영 오류를 보장하지 않습니다. [실제 명령](../../Conv1%20블러%20OK-NG%20실험/17차/README.md#준비와-실행)의 download/extract/prepare/weights SHA/docs 생성/Rust 빌드/화면 경로 설정을 완료해야 합니다.

사진 공격 9개와 6층×3정밀도특징 공격은 train 학습·val 선정·test 보고를 지킵니다. Top-1/5/10연결과 membership AUC는 복원 오차와 다른 위협입니다. 보호 오차 점수 100clip(MSEattack/MSEprior,0,1), 구조 점수 100clip(1−SSIM,0,1)의 raw·clip flag·null 사유를 보존합니다. MSEprior는 학습 평균 영상 기준이며 0분모를 임의 값으로 대체하지 않습니다. class별 값과 환자 군집 95%구간, 정답 수/분모가 해석 단위입니다. 단서 진단central/peripheral/coarse와 train-only label shuffle은 주변 단서·암기 가능성의 대조일 뿐 완전 제거 보장이 아닙니다.

Histo는 분류 영상의 픽셀→공식 2D/XML→CSV/3D환자 serial 사슬로 306/88을 연결했고 2 모호 사례를 사전 제외했습니다. legacy-2d-intensity와 128px center crop은 물리 HU/50mm와 다른 도메인입니다. CSTL은 대응 미완료로 blocked입니다. 자연인 교차 기관 중복이나 임상 외적 타당성은 별도입니다. 앞선 공격·셔플 수리는 신규 6·영향 3·최종진단 1 검사로, 화면 변경은 신규 1·관련 2 검사로 확인했습니다. 독립 검토에서는 실제 ResNet50의 6층×3정밀도 원본 공격 경계를 축소 CPU로 확인했습니다. 변경 없는 데이터 10·Rust18 근거는 재사용하며 과거 엔진 9/UI 2와 고정표본 9·bind1은 선행 범위로 구분합니다. 현재 GPU 결과는 없고 비공개 영상/예측/가중치/운영 기록은 공개하지 않습니다.

[같은 수준 프로젝트](../읽기안내/레벨4.md) · [같은 수준 프로필](https://github.com/PUVKID/PUVKID/blob/main/docs/읽기안내/레벨4.md)

</details>

<details>
<summary>LEVEL 5 · Expert</summary>

<a id="reading-level-5"></a>

새 공격의 변수는 raw ROI이며 목적은 ||Q_d(f_l(B_sigma(x)))-z||²+lambda·TV(x)입니다. Q_d forward의 dtype/동적 scale은 전달 경로와 같고 gradient는 identity STE 근사입니다. 고정 두 starts 및 모든 iterate 중 관측 목적 최소를 선택하고 원본 test MSE는 최종 평가에만 사용합니다. source_id 단위 라벨 순열은 원본 라벨 빈도를 보존하며 복제 가중치 때문에 증강 후 행 빈도 보존은 주장하지 않습니다. 평가 API는 original/generated와 validation/original_validation을 명시적으로 구분합니다. linking float-layer와 membership output threat를 dtype별 복원으로 확대하지 않습니다.

## LEVEL 5 - Expert

현재 표집 정책은 offline fixed-copies입니다. 각 class train 5000/validation 1000/test 1000의 동결 계획을 한 번 생성하고 split 환자/source 계보와 source/정책/manifest SHA를 결합합니다. 각 sigma는 base PNG 물리 사본에서 DCT Gaussian float32 TIFF를 만들며 8bit preview는 모델 입력이 아닙니다. train/evaluate/attack_source/membership/linking/examples가 같은 관측값을 사용하고 재블러하지 않습니다. 원본 937 validation/873 test는 canonical 첫 사본의 동일 관측을 참조합니다. fixed validation 2000 손실로 선정하고 원본 validation을 별도 보고하며 모든 반복 행의 환자 군집 구간을 보존합니다.

Protocol stage17-luna25-2d-patient-v2는 LUNA25 결절 중심 2D의 강도별 적응학습 비교입니다. 이 차수의 GPU 관측은 아직 없으며 이전 1~16차 결과를 대체 입력하지 않습니다. [공식 자료목록](../../Conv1%20블러%20OK-NG%20실험/17차/공식자료.json), [실행·환경·가중치 SHA](../../Conv1%20블러%20OK-NG%20실험/17차/README.md#준비와-실행), [소스 전체 비교](../revision-diffs/conv1-okng-round17.md)가 재현 근거입니다.

| 실험 축 | 고정 정의 | 보고 단위 |
|---|---|---|
| 주 코호트 | LUNA25 6163 nodules/2120 patient IDs; OK benign,NG malignant | train 4353/1484 patient,val 937/318,test 873/318 |
| 분할/입력 | seed 42·환자 70/15/15,공식 좌표 중심 50mm·512²·HU[−1000,400] | 환자·원본/픽셀 계보,0.09765625mm/pixel |
| 조건 | ResNet50 Conv1 split/full 각각 20 sigma | 독립 초기값·optimizer/scheduler/RNG; 총 40 |
| 보조 | ResNet18 full sigma 0; ResNet50 stem/layer1 split×sigma 0/32 | 추가 5,Conv1참조 조건은 중복 실행 안함 |
| 표집/선정 | train 5000/class 고정 파일/epoch;AdamW1e−4,wd1e−4,batch2×accum4 | max200/min30/patience25,min_delta1e−4,raw best 별도 |
| 시험 | 무증강 873 primary,test-only1000/class generated secondary | 정답 수/분모/raw 비율,patient cluster 95% CI |

0, 1, 2, 4, 6, 8, 10, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96, 128, 192, 256를 output pixel 단위로 입력 Gaussian DCT Blur에 한 번 적용합니다. blur 관측 후 정규화→ResNet50 표준 avgpool→FC1입니다. split boundary 지원 conv1/stem/layer1,detach한 중간 표현의 gradient를 앞단으로 반환합니다. full과 split의 optimizer 전달 경로를 구분하고 같은 시작 가중치 SHA로 재초기화합니다. verification에 시험 점수 최적화나 강제 오답을 도입하지 않습니다.

사진 9공격과 conv1/stem/layer1~4×f32/f16/i8특징 복원은 실제 Rust FTR1 왕복 값으로 계산합니다. packet/sidecar/totalbytes와 quantization MSE를 후단 분류·복원 오차와 함께 기록합니다. 공격은 train fit, val minimum MSE selection, test reporting입니다. candidate별 test와 posthoc worst 관찰은 selection 결과와 분리합니다. 닫힌 gallery Top1/5/10의source/patient 연결과 membership 선정 score/AUC는 별도 위협 모델입니다. 멤버십에서 외부 비회원만으로 AUC를 만들지 않습니다.

제안 척도 Perror=100clip(meanMSEattack/meanMSEtrainingmeanprior,0,1),Pstructure=100clip(1−SSIM,0,1)입니다. 원비율·음수 SSIM/clipping·PSNR 무한·분모 0·undefined_reason을 보존하며 결측치를 점수로 조작하지 않습니다. 100점은 정해진 기준 오차 도달/초과 표시이지 보호 확률·DP·신규성 증명이 아닙니다. accuracy/balancedaccuracy/AUC/PR-AUC/F1/MCC/Brier/ECE/혼동행렬은 정의 가능성과 분모를 함께 봅니다. 시험 환자 cluster bootstrap은 조건부 불확실성이고 반복 생성 행을 독립 환자로 세지 않습니다.

prepare는 공식 download 체크섬→extractCRC/SHA→물리 ROI/환자 분할→manifest 검토→weights 전체 SHA→Rust 빌드 exit 0→source/environment binding 순서입니다. 빌드 보고 docs 폴더를 먼저 만들며 server 기본 work/dataRoot는 운영 경로이므로 외부 환경에서 명시해야 합니다. 12차 40 조건 완료 전 CUDA 실행 gate가 막고 완료 epoch 재개는 model/optimizer/scheduler/RNG 계보를 유지합니다. 미완료 batch의 정확 재현 보장은 없습니다.

Histo306/88serial은 픽셀 대조·XML bbox 중심·CSV index/3D folder 연결 검토 후 128px→512 BMP crop으로 준비됐으며 다중 serial 동일 픽셀 2건은 결과 전 제외했습니다. 물리 geometry 불가를 명시해 LUNA의 50mm/HU와 동일화하지 않습니다. CSTL 환자·결절 대응은 현재 blocked이며 외부 결과는 없습니다. 기관 출처는 자연인 전역 ID가 아닙니다. 중앙/주변/거친 단서·train 라벨 셔플 진단은 내적 오염 근거를 늘리지만 병원 단서·라벨 오류·단일 분할·ROI 제공·임상 외적 타당성을 모두 제거하지 못합니다.

앞선 공격·셔플 수리는 신규 6·영향 3·최종진단 1 검사로, 화면 변경은 신규 1·관련 2 검사로 확인했습니다. 독립 검토에서는 실제 ResNet50의 6층×3정밀도 원본 공격 경계를 축소 CPU로 확인했습니다. 변경 없는 데이터 10·Rust18 근거는 재사용하며 과거 엔진 9/UI 2와 고정표본 9·bind1은 선행 범위로 구분합니다. 합성 CPU 검사와 실제 장기 GPU 완료/공격 최적성은 별도입니다. 현재 단계는 준비이며 실측 결과·논문 원고를 만들어 채우지 않았습니다. 공개 범위는 소스/예제/집계 설명으로 영상·행별 목록/예측·가중치·비공개 로그를 포함하지 않습니다. 다크/라이트·sidebar·실제 epoch/강도 그래프·사진 설명은 현재 run만 표시하고 정의 불가·준비 대기를 구분합니다.

[같은 수준 프로젝트](../읽기안내/레벨5.md) · [같은 수준 프로필](https://github.com/PUVKID/PUVKID/blob/main/docs/읽기안내/레벨5.md)

</details>


## 연결 공격·저장 결과·진행 표시 후속

| 수준 | 추가 동작과 한계 |
|---|---|
| LEVEL 1 - Beginner | 같은 사진의 복사본을 찾아도 정답으로 셉니다. 공격 중 실제 처리 사진 수가 보이며, 아직 처리하지 않은 수를 만들지 않습니다. |
| LEVEL 2 - Explorer | 원본 gallery와 증강 query를 구분하고, 다른 실행에서 저장한 결과는 읽지 않습니다. 복원 진행은 분류 회차와 별도로 보입니다. |
| LEVEL 3 - Practitioner | gallery는 고유 source_id 하나/canonical 우선, query는 원래 집합 전체입니다. 캐시 run_id와 조건 프로토콜을 확인하며 단계별 실제 완료 수를 API로 제공합니다. |
| LEVEL 4 - Advanced | 연결 점수 분모는 query 행 수, gallery_size는 고유 원본 수입니다. 동일 원본의 환자 충돌을 거부합니다. 진행 보고는 대체로 2초 간격으로 제한하며 분류 정확도·체크포인트는 보존합니다. |
| LEVEL 5 - Expert | source_id Top-k membership으로 positional-index false negative를 제거했습니다. 공격 결과는 run_id, 조건 결과는 protocol/condition까지 검증합니다. 콜백은 디코더 train/validation·reconstruction·linking·membership·shuffle 실제 처리 수만 보고합니다. CPU 4/API1 및 영향CPU8/UI 2 검증이며 GPU 전체·실브라우저를 검증했다는 뜻은 아닙니다. |

[수정 동작 상세](../../Conv1%20블러%20OK-NG%20실험/17차/docs/연결공격_캐시_진행표시_수정.md)

앞선 공격·셔플 수리의 검사 근거와 이번 연결·캐시·진행 표시 검사는 구분합니다. 이번 3건의 검사 범위는 바로 위 후속 표와 수정 상세를 참조합니다.

## 전체 재검증 후속

| 수준 | 이번 변경과 근거 |
|---|---|
| LEVEL 1 - Beginner | 사진 설명에 어떤 모델로 복원했고 무엇을 알고 공격했는지 표시합니다. 검사 파일 29개가 통과했습니다. |
| LEVEL 2 - Explorer | 이전 설정·화면용 검사 10개(구 엔진 3·화면 7)가 깨진 원인을 보존하고 새 화면·설정에 맞췄습니다. 기존 28개와 새 사진 설정 1개를 구분합니다. |
| LEVEL 3 - Practitioner | legacy 엔진 검사는 별도 설정·합성 계보를 사용하고 SCI 운영 설정과 분리합니다. 사진 설정은 실제 선정 checkpoint SHA와 위협모형을 저장·표시합니다. |
| LEVEL 4 - Advanced | 최초 28 파일 18 통과/10 실패 원문과 수정 후 28 통과를 보존하고 설정 생성 1개를 추가했습니다. 현재 준비 영상 6469개 SHA/픽셀/규격/분할 검사 통과, CSTL 차단 유지입니다. |
| LEVEL 5 - Expert | 검사 fixture의 구 schema/함수/selector/경로 가정을 현재 SCI 계약으로 옮겼으며 기존 checkpoint/threat 표시 assert2를 복구했습니다. run_protection→server whitelist→photoSettings에 실제 선정 SHA/가정을 연결했습니다. 검증은 CPU/Rust/HTTP/VM 및 6469 영상 읽기이며 실제 GPU 전체·14k물리생성·실브라우저는 미수행입니다. |

선행 절의 개별 검사 수는 이전 수정의 근거이며, 최신 전체 검사는 위 29 파일과 실제 자료 읽기 범위로 해석합니다.

## 중단 후 최적 모델 재개 보완 (2026-11-27)

| 설명 수준 | 문제와 수정 | 확인 근거 | 남은 범위 |
|---|---|---|---|
| LEVEL 1 - Beginner | 저장 도중 멈춰도 가장 잘 배운 모델을 다시 찾도록 수정 | 작은 CPU 중단/재개 6검사 통과 | 실제 긴 GPU 실험은 별도 |
| LEVEL 2 - Explorer | 마지막 저장과 최적 모델 표식 사이 중단에서 옛 모델을 고르던 문제를 복구 | 신규 6·관련 기존 16방법 통과 | 분류 점수를 조작하지 않음 |
| LEVEL 3 - Practitioner | 분류기와 복원 디코더 재개 직후 검증 이력 최저와 포인터 SHA·계보 확인 | 독립 6+동률 최초 최저 1 확인 | 선행 29·6469영상 검사는 기존 근거 재사용 |
| LEVEL 4 - Advanced | last 체크포인트 검증 뒤 남은 epoch 전에 best 복구; current/history도 마지막 완료 이력에서 복원 | stale/missing·후속 비개선·이전 최저 보존·불일치 거부 | 실제 전원 차단 내구성 전체를 보장하지 않음 |
| LEVEL 5 - Expert | 연속 epoch/run/finite loss/argmin/state.best 일치 확인; 최신 개선만 권위 있는 last SHA로 복구하고 이전 최저는 기존 reference epoch/path/hash·checkpoint run/protocol/condition/loss 검증 | 실제 SCI 통합 CPU 경로와 별도 동률 반례; 실패 원문은 비공개 보존 | 학습/공격/분할/블러 수식은 동일, GPU 전체·14k 생성·브라우저는 미수행 |

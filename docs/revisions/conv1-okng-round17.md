# 17차 · 환자 분할 기반 폐결절 입력 블러 연구

[LEVEL 1](#user-content-reading-level-1) · [LEVEL 2](#user-content-reading-level-2) · [LEVEL 3](#user-content-reading-level-3) · [LEVEL 4](#user-content-reading-level-4) · [LEVEL 5](#user-content-reading-level-5)

[자료](../../Conv1%20블러%20OK-NG%20실험/17차/) · [전체 비교](../revision-diffs/conv1-okng-round17.md) · [전체 차수](../REVISION_INDEX.md)

<details open>
<summary>LEVEL 1 · Beginner</summary>

<a id="reading-level-1"></a>

원래 사진을 되찾는 공격도 더해 봅니다. 원본 후보를 흐리게 하고 같은 특징이 나오는지 맞추므로, 흐린 사진까지만 찾는 공격과 구분합니다. 같은 원본에서 늘린 사진에는 셔플 진단의 정답도 같게 붙입니다. 화면의 원본 시험·늘린 시험·검증을 바꾸면 그 집합의 수치만 보여 주며 없으면 미측정이라고 씁니다.

## LEVEL 1 - Beginner

이번에는 사진을 처음에 한 번만 늘려 저장합니다. 학습은 양성5,000·악성5,000, 검증과시험은 각각 양성1,000·악성1,000입니다. 블러0·1·2…는 이 같은14,000개 구성을 복사해 씁니다. 시험마다다른사진을뽑거나매회새증강을하지않습니다. 고정검증2,000개로모델을고르고원본검증937개도따로봅니다. 계산용float32사진과보기용PNG를구분하며분류와복원은같은블러값을읽습니다.

사진에서 작은 결절(폐 속 덩어리)의 위치를 먼저 찾은 자료로, 흐림이 분류와 원래 사진 복원에 어떤 영향을 주는지 봅니다. OK는 양성 결절, NG는 악성 결절입니다. 정상 사진을 OK에 합쳤던 과거 차수와 자료가 다릅니다.

| 순서 | 하는 일 | 왜 필요한가요? |
|---|---|---|
| 1 | 공식 LUNA25 자료의 2,120명·6,163결절을 준비 | 사진 파일을 복사했다고 새 사람이 생기지는 않아요 |
| 2 | 사람별로 학습1,484명/4,353결절, 검증318명/937결절, 시험318명/873결절로 나눔 | 같은 사람이 배우는 쪽과 시험 쪽에 섞이지 않게 해요 |
| 3 | 결절 중심50×50mm를512×512칸으로, 밝기는HU−1000~400으로 고정 | 사진 크기와 밝기 범위를 맞춰요 |
| 4 | 흐림 정도와 모델 연결 방식별로 처음부터 별도 학습 | 먼저 배운 답을 다음 강도에 물려주지 않아요 |
| 5 | 새 시험 사진을 분류하고 원본을 되찾는 공격도 따로 시도 | 정답을 잘 맞히는 것과 사진을 못 되찾는 것은 달라요 |

흐림 숫자는 0, 1, 2, 4, 6, 8, 10, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96, 128, 192, 256 입니다. 숫자0은 흐림 없음, 숫자가 커질수록 더 넓게 섞습니다. 단위는 완성 사진의 칸(pixel)이며 한 칸은50/512mm입니다. 사진에 Gaussian 흐림을 한 번 넣고 모델에 전달합니다.

기본 ResNet50은 기계가 보는 작은 필터인 Conv1에서 앞뒤로 나눈 방식20개와 전체를 연결한 방식20개입니다. 별도 확인5개는 더 작은 ResNet18의 흐림0 한 개, ResNet50의 stem/layer1 경계에서 흐림0/32 네 개여서 총45개입니다. 같은 조건은 같은 시작 가중치에서 새로 배웁니다. 마지막에는 평균을 모으는 avgpool과 두 종류를 가르는 출력층(FC1)을 씁니다.

시작 때 OK5,000개·NG5,000개를 한 번 만들어 저장하고, 매 학습 회차에는 그 같은 파일을 보여 줍니다. 시험은 원래873결절의 무증강 점수가 중심입니다. 시험 안에서 OK1,000행·NG1,000행을 만들기도 하지만 같은 원본의 보조 시험이지2,000명의 시험이 아닙니다. 최대200회, 적어도30회를 배우며 검증 손실(연습시험 오차)이25회 개선되지 않으면 멈춥니다. 최저 검증 손실 모델을 보관하고 최종 시험 점수로 모델을 고르지 않습니다.

사진 복원 공격9종과 특징(기계가 만든 중간 표현) 복원은 Conv1/stem/layer1~4의6곳, FP32/FP16/INT8의3가지 숫자 저장 방식으로 봅니다. Rust가 실제로 숫자를 포장하고 다시 푼 뒤 분류와 공격을 합니다. 비슷한 원본을 후보 목록에서 찾는Top-1/5/10, 학습에 썼던 자료인지 맞히는 멤버십AUC도 따로 기록합니다. 공격은 학습 자료로 배우고 검증 자료로 고르며 시험은 보고에만 씁니다.

보호 점수는 공격의 평균 제곱 오차를 학습 평균 사진의 오차와 비교해100배 하고0~100으로 제한한 값, 그리고 사진 구조 유사도SSIM을1에서 빼100배 한 값입니다. 나누는 수가0이면 계산 불가로 표시합니다. 미측정을0점이나100점으로 채우지 않습니다. 높은 점수도 안전 확률은 아닙니다. 정확도는 정답수/전체수와 원비율을 남기고 화면만 소수 첫째 자리로 반올림합니다. 사람별 묶음95%구간도 함께 봅니다.

준비는 공식 다운로드→체크섬 확인→압축 해제→결절 사진과 환자 분할→초기 가중치SHA→Rust 빌드→실행 준비 순서입니다. [실제 명령](../../Conv1%20블러%20OK-NG%20실험/17차/README.md#준비와-실행)을 따르고, 자료·가중치·실행 경로가 맞는지 확인합니다. Histo306장/88serial은 준비됐지만 밝기 BMP와128칸 crop이라 LUNA와 같은50mm/HU가 아닙니다. serial 대응이 모호한2장은 성능을 보기 전에 제외했습니다. CSTL은 환자·결절 대응 보류입니다. 외부 자료를 모델에 다시 가르쳐 시험으로 내지 않습니다.

화면은 다크/라이트, 왼쪽 메뉴, 강도 선택, 실제 에폭 점과 대표 사진 설명을 제공합니다. 준비 대기는 결과가 아닙니다. 중앙·주변·거친 단서와 학습 라벨 섞기 대조도 따로 보아 주변 모양만 외웠는지 살핍니다. 현재17차 GPU 결과는 없고12차40조건 완료 후 시작합니다. 위치가 주어진 분류 실험이라 자동 암 탐지·임상 진단·개인정보 보호 보장이 아닙니다.

[같은 수준 프로젝트](../읽기안내/레벨1.md) · [같은 수준 프로필](https://github.com/PUVKID/PUVKID/blob/main/docs/읽기안내/레벨1.md)

</details>

<details>
<summary>LEVEL 2 · Explorer</summary>

<a id="reading-level-2"></a>

기존 공격은 남기고 블러 전 원본을 추정하는 두 초기값의 공격을 추가했습니다. 어느 초기값이 좋은지는 전달 특징과 TV 목적만으로 고르며 시험 정답으로 고르지 않습니다. 셔플 라벨은 원본별로 고정하고 사본에 전파합니다. 원본 시험873·증강 시험2000·원본 검증937·균형 검증2000을 API와 화면에서 구분합니다.

## LEVEL 2 - Explorer

고정 기본셋14,000행은 환자분할뒤각클래스학습5,000/검증1,000/시험1,000으로한번만만듭니다. 단계마다실제사본을만들어그강도의blur를한번적용하므로구성차이와누적블러를통제합니다. 고정검증2000행손실이선정기준이고원본검증937행은별도보고입니다. float32TIFF는분류·공격공유입력,PNG는미리보기이며원본873시험과생성2000시험은독립환자수로합치지않습니다.

이번 비교의 두 축은 남은 정보로 분류하는 능력과 그 정보에서 사진을 복원하는 능력입니다. 강도별 새 학습은 흐림에 적응하는 성능을 측정합니다. 고정 모델 하나에 강도만 바꾸는 과거7차와 질문이 다릅니다.

| 연결 | 입력과 처리 | 비교의 기준 |
|---|---|---|
| 자료→분할 | LUNA25 6,163결절/2,120명, 공식 환자ID로seed42·70/15/15 | train4,353/1,484명·validation937/318명·test873/318명 |
| 좌표→영상 | 결절 중심50mm,512px,HU−1000~400 | OK=양성결절,NG=악성결절; 정상은 별도 포함하지 않음 |
| 영상→분류 | Gaussian 한 번→ResNet→avgpool→FC1 | Conv1 분할20·전체 연결20, 독립 초기화 |
| 중간표현→전송 | 6층 ×3정밀도, Rust FTR1 실제 왕복 | 용량·양자화오차·후단 분류·공격을 같은 복원값에서 계산 |
| 노출→공격 | 사진9종, 특징 복원, Top-k 연결, 멤버십 | 각각 다른 위협을 하나의 안전확률로 합치지 않음 |

0, 1, 2, 4, 6, 8, 10, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96, 128, 192, 256의20강도를 씁니다. 한 출력pixel은0.09765625mm이고 sigma는pixel 단위입니다. 보조5개는 ResNet18 전체연결sigma0, ResNet50 stem/layer1 분할 각각sigma0/32입니다. Conv1 sigma0/32는 주조건을 참조하므로 중복 재학습하지 않습니다. 총고유학습45개입니다. 분할 방식은 detach한 중간값의 기울기를 앞단으로 실제 반환합니다.

train에서 OK/NG 각5,000회 시작 때 한 번 고정 생성·저장하며 validation은 모델 선정용, test는 보고용입니다. 최대200·최소30·patience25이고 검증 손실 최저 모델을 따로 저장합니다. 작은 개선을 세는min_delta와 진짜 최저 손실 보존을 구분합니다. 원본 시험873결절이 주 결과이고 test-only 반복증강각1,000행은 보조 결과입니다. 같은 환자의 반복행은 독립 표본이 아니며 환자 군집95%구간과 정답수·분모를 함께 냅니다.

평균영상 기준MSE는 원본을 보지 않고 평균만 내보내는 기준의 오차입니다. 보호오차점수=100×clip(공격MSE/기준MSE,0,1), 구조점수=100×clip(1−SSIM,0,1)입니다. 기준0·미측정·정의 불가 지표는 null과 이유입니다. raw 비율과 clipping 여부를 남기며100점은 시험한 공격에 대한 상대값입니다. Top-1/5/10은 닫힌 후보에서의 연결 성공, 멤버십AUC는 포함 여부 구별 능력입니다. 공격 train학습/validation선정/test보고를 지키며 시험에서 관찰한 가장 센 공격 요약은 사후 관찰로 구분합니다.

공식자료.json→download→extract→prepare로 자료를 준비하고, 가중치전체SHA와 Rust 빌드를 확인해 SCI실행--prepare에 연결합니다. [명령과 화면 경로 설정](../../Conv1%20블러%20OK-NG%20실험/17차/README.md#준비와-실행)을 확인합니다. 실행 파일·영상·환자 목록은 저장소에 없습니다. Histo는 픽셀→XML결절→공식serial로306장88serial을 연결했으나 물리 HU/50mm가 아닌128px BMP crop입니다. 모호한2장은 제외, CSTL은 대응 미완료로 보류합니다. 병원 출처가 다르다고 자연인 중복 없음까지 증명하지 않습니다.

단서진단은 중앙/주변/거친 정보와 train-only 라벨셔플을 따로 비교합니다. 주변 조직 단서가 완전히 제거됐다고 주장하지 않습니다. 앞선 공격·셔플 수리는 신규6·영향3·최종진단1 검사로, 화면 변경은 신규1·관련2 검사로 확인했습니다. 독립 검토에서는 실제 ResNet50의6층×3정밀도 원본공격 경계를 축소 CPU로 확인했습니다. 변경없는 데이터10·Rust18 근거는 재사용하며 과거 엔진9/UI2와 고정표본9·bind1은 선행 범위로 구분합니다.  GPU 측정은 아직 없습니다. 12차40조건 종료 후에만17차 실행합니다. 대시보드의 메뉴·테마·강도별 실제 그래프·사진 설명은 미측정과 결과를 구분합니다. 정확도100%를 피하려고 결과나 분할을 바꾸지 않습니다. 결절 위치 제공 분류, 단일 분할과 정해진 공격군의 탐색 연구이며 임상·DP 보장은 아닙니다.

[같은 수준 프로젝트](../읽기안내/레벨2.md) · [같은 수준 프로필](https://github.com/PUVKID/PUVKID/blob/main/docs/읽기안내/레벨2.md)

</details>

<details>
<summary>LEVEL 3 · Practitioner</summary>

<a id="reading-level-3"></a>

raw-space 역복원은 raw_guess→Gaussian→특징→dtype 전방 값을 전달 특징에 맞춥니다. train_mean/flat_0.5 초기값과 iterate는 관측 목적과 TV만으로 선택하며 공격군 선정은 validation 전용입니다. dtype 역전파는 STE 근사입니다. 원본 source_id 순열을 사본에 전파하고 원본 분포/증강 후 행 분포를 저장합니다. 선택한 평가 집합에 연결·멤버십이 없으면 다른 시험 값으로 채우지 않습니다.

## LEVEL 3 - Practitioner

SCIconfig의고정표본정책과캐시경로를설정하고--prepare에서학습각5000/검증각1000/시험각1000의기본파일을한번만준비합니다. sigma최초진입시에기본PNG실제복사와float32TIFF블러출력을저장합니다. 캐시manifest/파일SHA/정책이바뀌면재개를거부합니다. 매epoch새표집/온라인hflip은없고동일파일의순서만변경가능합니다. 고정검증2000으로선정하며원본검증937과873주시험은별도결과입니다.

실행자는 자료 준비와 GPU 실행을 분리합니다. [준비와 실행 명령](../../Conv1%20블러%20OK-NG%20실험/17차/README.md#준비와-실행)에 공식 download/extract/prepare, SHA, Rust 빌드, 화면 기동의 순서가 있습니다. Python의 torch/torchvision/NumPy/SciPy/Pillow/psutil/scikit-learn, Node.js, 지원 Rust/MSVC/SDK가 필요하며 volume 외부 경로에는 SimpleITK가 추가됩니다. 설치·정책을 자동 변경하지 않습니다.

| 설정 | 값 | 산출물·실패 확인 |
|---|---|---|
| 원자료 | LUNA25 공식주석·nodule-blocks, 환자seed42·70/15/15 | 준비 manifest와 개별영상SHA, 환자 중복이면 중단 |
| 표적 | OK양성/NG악성결절, 중심50mm·512px·HU−1000~400 | train4,353/1,484명, val937/318명, test873/318명 |
| 표집 | train각5,000개 고정파일/epoch | 반복·증강 횟수이며 독립 원본수가 아님 |
| 시험 | 원본873 주시험, test-only각1,000행 보조시험 | 정답수/분모·원비율·환자 군집95%구간 구분 |
| 최적화 | batch2·누적4, AdamW lr1e−4·weight decay1e−4 | 최대200/최소30/patience25, 검증최저 모델 |

sigma목록은 0, 1, 2, 4, 6, 8, 10, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96, 128, 192, 256 입니다. 입력Gaussian 한 번,1pixel=50/512mm입니다. ResNet50 Conv1분할과 전체연결을20강도씩 새 초기모델/optimizer/scheduler/RNG로 학습합니다. 보조는 ResNet18 전체sigma0 한 개, ResNet50 stem/layer1 분할sigma0/32 네 개, 총45고유학습입니다. 표준avgpool→FC1과 실제detach기울기 반환을 씁니다. 시험 점수로 모델·공격·분할을 선택하지 않습니다.

SCIconfig.example을 SCIconfig로 복사하고 runtime/manifest/data_status/weights 경로를 실제 위치로 설정합니다. 두 가중치의 전체SHA는 예제에 고정돼 있으며 불일치 때 중단합니다. 빌드 전 docs 폴더를 만들고 빌드결과exit_code=0·source/engineSHA를 봅니다. SCI실행--prepare는 입력을run에 결합하므로 외부 manifest 추가는 그 전에 끝냅니다. --run은12차40조건 완료 gate를 통과해야 합니다. --resume은 같은 결합의 마지막 완료 에폭을 사용하며 미완료 배치를 정확 재현했다고 주장하지 않습니다. 화면 서버 기본경로가 고정돼 있으므로 다른 환경은createServer의work/dataRoot를 지정합니다.

분류 결과는 main test와test_generated를 별도 읽습니다. 사진 공격9종, Conv1/stem/layer1~4×FP32/FP16/INT8 특징의 실제Rust포장왕복, 연결Top-1/5/10, 멤버십AUC를 확인합니다. 복원공격은 train학습/val선정/test보고입니다. 보호점수는100×clip(MSE공격/MSE학습평균기준,0,1)와100×clip(1−SSIM,0,1)이며 raw/clipped·분모0/null사유를 보존합니다. 안전 확률이나DP로 보고하지 않습니다. 중앙/주변/거친 단서와train라벨셔플 대조는 주분류와 구분합니다.

Histo306장88공식serial은 pixel/XML 중심128px→512 BMP 밝기crop이며50mm/HU의 외부 복제가 아닙니다. 다중serial동일픽셀2장은 사전 제외했습니다. CSTL은 환자/결절 대응까지 준비되지 않아 보류입니다. 외부자료의 재학습·분할선정에 시험결과를 쓰지 않습니다. 공식ID 내 분할과 해시 점검은 병원간 자연인 동일성 증명이 아닙니다.

앞선 공격·셔플 수리는 신규6·영향3·최종진단1 검사로, 화면 변경은 신규1·관련2 검사로 확인했습니다. 독립 검토에서는 실제 ResNet50의6층×3정밀도 원본공격 경계를 축소 CPU로 확인했습니다. 변경없는 데이터10·Rust18 근거는 재사용하며 과거 엔진9/UI2와 고정표본9·bind1은 선행 범위로 구분합니다.  GPU성능·장기복구는 미측정입니다. 대시보드는 실제run/강도/에폭/사진을 연결하고 대기와미정의를 표시합니다. 임상사용·자동검출·형식적 개인정보 보호를 증명하지 않습니다. 결과표를 낮추려고 오답을 만들지 않습니다.

[같은 수준 프로젝트](../읽기안내/레벨3.md) · [같은 수준 프로필](https://github.com/PUVKID/PUVKID/blob/main/docs/읽기안내/레벨3.md)

</details>

<details>
<summary>LEVEL 4 · Advanced</summary>

<a id="reading-level-4"></a>

기존 observed-space 후보에 raw_blur_aware_tv 공격군을 추가했습니다. preblurred 우회 대신 model.blur(raw_guess)를 명시하고 dtype forward는 FeatureCodec와 일치시킵니다. float/양자화의 역전파 STE와 최종 관측 목적 기반 선택은 원본 GT와 분리합니다. 셔플 source 매핑 전체는 비공개 파일로 보존하고 화면에는 집계만 냅니다. API의 validation_original/test_generated 및 membership_generated 연결을 추가해 평가 분모 혼용을 제거했습니다.

## LEVEL 4 - Advanced

고정표본모듈이환자분할이후source_id·canonical·고정증강seed를결합하고14,000기본파일을생성합니다. sigma폴더에는물리raw사본과DCTfloat32관측TIFF를저장하며완료marker·불완료검증·tamper거부를사용합니다. 분류forward의관측입력경로는blur를우회하지만공격rawtarget과cache관측을분리합니다. 같은sigma의두regime는동일cache를재사용하며fixed validation2000선정/originalvalidation937보고를분리합니다.

구현의 비교 단위는(condition:model,regime,boundary,sigma)와 불변 입력 결합입니다. SCI데이터는 공식체크섬·환자분할·기하ROI를, SCI모델은 단일입력blur·표준pool/FC·splitgradient를, SCI실행은 조건독립학습·검증선정·재개를, SCI공격/특징노출/전송/Rust는 실제노출·패킷·공격을 맡습니다.

| 경계 | 설계 선택 | 변경 영향과 실패 처리 |
|---|---|---|
| 자료 | LUNA25 환자seed42·70/15/15, 중심50mm/512·HU−1000~400 | 원본·환자·픽셀hash 분할 비중복, ROI SHA 불일치 거부 |
| 학습 | ResNet50 Conv1split/full각20, 보조5 | 초기값/optimizer/scheduler/RNG 독립, 이전 조건 적응모델 계승 금지 |
| 상태 | manifest·config·가중치SHA·source·실행환경 결합 | 기존binding과 다르면 중단; 완료epoch만재개 |
| 전송 | FTR1 f32/f16/i8 실제encode/decode | 직렬화후단 분류/공격, 용량과양자화오차 함께기록 |
| 화면 | 조회전용Node API·현재run연결 | 잘못된run사진/미측정값을 새결과로 내지 않음 |

OK는 양성,NG는악성결절이고 정상은 포함하지 않습니다. 원본6163/2120명은 train4353/1484명,val937/318명,test873/318명입니다. 학습각5000·검증각1000·시험각1000의 시작시1회고정 파일 사용은 원본 독립수를 늘리지 않습니다. sigma는 0, 1, 2, 4, 6, 8, 10, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96, 128, 192, 256 이며outputpixel기준50/512mm입니다. Gaussian은 입력에 한 번만 적용하고split은detach후backward기울기를실제로반환합니다. 보조조건은 ResNet18 full sigma0, ResNet50 stem/layer1 split각sigma0/32, 총45고유학습입니다.

AdamW1e−4/weight decay1e−4,batch2×누적4,max200/min30/patience25입니다. raw best validation loss 보존과min_delta1e−4에 의한patience판단은 별도입니다. validation만선정에쓰고test는보고에한정합니다. 12차40완료gate와 prepare/run/resume분리는 동시GPU실행과입력바꿔치기를막지만 모든운영오류를보장하지않습니다. [실제명령](../../Conv1%20블러%20OK-NG%20실험/17차/README.md#준비와-실행)의download/extract/prepare/weightsSHA/docs생성/Rust빌드/화면경로설정을완료해야합니다.

사진공격9개와6층×3정밀도특징공격은 train학습·val선정·test보고를지킵니다. Top-1/5/10연결과 membershipAUC는복원오차와다른위협입니다. 보호오차점수100clip(MSEattack/MSEprior,0,1), 구조점수100clip(1−SSIM,0,1)의raw·clipflag·null사유를보존합니다. MSEprior는학습평균영상기준이며0분모를임의값으로대체하지않습니다. class별값과환자군집95%구간,정답수/분모가해석단위입니다. 단서진단central/peripheral/coarse와train-only labelshuffle은 주변단서·암기가능성의대조일뿐 완전제거보장이아닙니다.

Histo는분류영상의픽셀→공식2D/XML→CSV/3D환자serial사슬로306/88을연결했고2모호사례를사전제외했습니다. legacy-2d-intensity와128pxcenter crop은물리HU/50mm와다른도메인입니다. CSTL은대응미완료로blocked입니다. 자연인교차기관중복이나임상외적타당성은별도입니다. 앞선 공격·셔플 수리는 신규6·영향3·최종진단1 검사로, 화면 변경은 신규1·관련2 검사로 확인했습니다. 독립 검토에서는 실제 ResNet50의6층×3정밀도 원본공격 경계를 축소 CPU로 확인했습니다. 변경없는 데이터10·Rust18 근거는 재사용하며 과거 엔진9/UI2와 고정표본9·bind1은 선행 범위로 구분합니다. 현재GPU결과는없고 비공개영상/예측/가중치/운영기록은공개하지않습니다.

[같은 수준 프로젝트](../읽기안내/레벨4.md) · [같은 수준 프로필](https://github.com/PUVKID/PUVKID/blob/main/docs/읽기안내/레벨4.md)

</details>

<details>
<summary>LEVEL 5 · Expert</summary>

<a id="reading-level-5"></a>

새 공격의 변수는 raw ROI이며 목적은 ||Q_d(f_l(B_sigma(x)))-z||²+lambda·TV(x)입니다. Q_d forward의 dtype/동적 scale은 전달 경로와 같고 gradient는 identity STE 근사입니다. 고정 두 starts 및 모든 iterate 중 관측 목적 최소를 선택하고 원본 test MSE는 최종 평가에만 사용합니다. source_id 단위 라벨 순열은 원본 라벨 빈도를 보존하며 복제 가중치 때문에 증강 후 행 빈도 보존은 주장하지 않습니다. 평가 API는 original/generated와 validation/original_validation을 명시적으로 구분합니다. linking float-layer와 membership output threat를 dtype별복원으로 확대하지 않습니다.

## LEVEL 5 - Expert

현재표집정책은offline fixed-copies입니다. 각class train5000/validation1000/test1000의동결계획을한번생성하고split환자/source계보와source/정책/manifest SHA를결합합니다. 각sigma는basePNG물리사본에서DCTGaussianfloat32TIFF를만들며8bitpreview는모델입력이아닙니다. train/evaluate/attack_source/membership/linking/examples가같은관측값을사용하고재블러하지않습니다. 원본937validation/873test는canonical첫사본의동일관측을참조합니다. fixed validation2000손실로선정하고원본validation을별도보고하며모든반복행의환자군집구간을보존합니다.

Protocol stage17-luna25-2d-patient-v2는 LUNA25 결절중심2D의 강도별 적응학습 비교입니다. 이 차수의GPU관측은 아직 없으며 이전1~16차결과를 대체 입력하지 않습니다. [공식 자료목록](../../Conv1%20블러%20OK-NG%20실험/17차/공식자료.json), [실행·환경·가중치SHA](../../Conv1%20블러%20OK-NG%20실험/17차/README.md#준비와-실행), [소스 전체비교](../revision-diffs/conv1-okng-round17.md)가 재현 근거입니다.

| 실험축 | 고정 정의 | 보고 단위 |
|---|---|---|
| 주코호트 | LUNA25 6163nodules/2120patientIDs; OK benign,NG malignant | train4353/1484patient,val937/318,test873/318 |
| 분할/입력 | seed42·환자70/15/15,공식좌표중심50mm·512²·HU[−1000,400] | 환자·원본/픽셀 계보,0.09765625mm/pixel |
| 조건 | ResNet50 Conv1split/full 각각20sigma | 독립 초기값·optimizer/scheduler/RNG; 총40 |
| 보조 | ResNet18full sigma0; ResNet50stem/layer1 split×sigma0/32 | 추가5,Conv1참조조건은중복실행안함 |
| 표집/선정 | train5000/class 고정파일/epoch;AdamW1e−4,wd1e−4,batch2×accum4 | max200/min30/patience25,min_delta1e−4,raw best별도 |
| 시험 | 무증강873primary,test-only1000/class generatedsecondary | 정답수/분모/raw비율,patientcluster95%CI |

0, 1, 2, 4, 6, 8, 10, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96, 128, 192, 256를outputpixel단위로입력GaussianDCTBlur에한번적용합니다. blur관측후정규화→ResNet50 표준avgpool→FC1입니다. splitboundary지원conv1/stem/layer1,detach한중간표현의gradient를앞단으로반환합니다. full과split의optimizer전달경로를 구분하고 같은 시작가중치SHA로재초기화합니다. verification에시험점수최적화나강제오답을도입하지않습니다.

사진9공격과 conv1/stem/layer1~4×f32/f16/i8특징복원은실제Rust FTR1 왕복값으로계산합니다. packet/sidecar/totalbytes와quantizationMSE를후단분류·복원오차와함께기록합니다. 공격은trainfit,valminimumMSEselection,testreporting입니다. candidate별test와 posthoc worst 관찰은selection결과와분리합니다. 닫힌galleryTop1/5/10의source/patient연결과membership선정score/AUC는별도위협모델입니다. 멤버십에서외부비회원만으로AUC를만들지않습니다.

제안척도Perror=100clip(meanMSEattack/meanMSEtrainingmeanprior,0,1),Pstructure=100clip(1−SSIM,0,1)입니다. 원비율·음수SSIM/clipping·PSNR무한·분모0·undefined_reason을보존하며결측치를 점수로조작하지않습니다. 100점은정해진기준오차도달/초과표시이지보호확률·DP·신규성증명이아닙니다. accuracy/balancedaccuracy/AUC/PR-AUC/F1/MCC/Brier/ECE/혼동행렬은정의가능성과분모를함께봅니다. 시험환자clusterbootstrap은조건부불확실성이고반복생성행을독립환자로세지않습니다.

prepare는공식download체크섬→extractCRC/SHA→물리ROI/환자분할→manifest검토→weights전체SHA→Rust빌드exit0→source/environmentbinding순서입니다. 빌드보고docs폴더를먼저만들며server기본work/dataRoot는운영경로이므로외부환경에서명시해야합니다.12차40조건완료전CUDA실행gate가막고완료epoch재개는model/optimizer/scheduler/RNG계보를유지합니다. 미완료batch의정확재현보장은없습니다.

Histo306/88serial은픽셀대조·XMLbbox중심·CSV index/3Dfolder연결검토후128px→512BMPcrop으로준비됐으며다중serial동일픽셀2건은결과전제외했습니다. 물리geometry불가를명시해LUNA의50mm/HU와동일화하지않습니다. CSTL환자·결절대응은현재blocked이며외부결과는없습니다. 기관출처는자연인전역ID가아닙니다. 중앙/주변/거친단서·train라벨셔플진단은내적오염근거를늘리지만병원단서·라벨오류·단일분할·ROI제공·임상외적타당성을모두제거하지못합니다.

앞선 공격·셔플 수리는 신규6·영향3·최종진단1 검사로, 화면 변경은 신규1·관련2 검사로 확인했습니다. 독립 검토에서는 실제 ResNet50의6층×3정밀도 원본공격 경계를 축소 CPU로 확인했습니다. 변경없는 데이터10·Rust18 근거는 재사용하며 과거 엔진9/UI2와 고정표본9·bind1은 선행 범위로 구분합니다. 합성CPU검사와실제장기GPU완료/공격최적성은별도입니다. 현재단계는준비이며실측결과·논문원고를만들어채우지않았습니다. 공개범위는소스/예제/집계설명으로영상·행별목록/예측·가중치·비공개로그를포함하지않습니다. 다크/라이트·sidebar·실제epoch/강도그래프·사진설명은현재run만표시하고정의불가·준비대기를구분합니다.

[같은 수준 프로젝트](../읽기안내/레벨5.md) · [같은 수준 프로필](https://github.com/PUVKID/PUVKID/blob/main/docs/읽기안내/레벨5.md)

</details>


## 연결 공격·저장 결과·진행 표시 후속

| 수준 | 추가 동작과 한계 |
|---|---|
| LEVEL 1 - Beginner | 같은 사진의 복사본을 찾아도 정답으로 셉니다. 공격 중 실제 처리 사진 수가 보이며, 아직 처리하지 않은 수를 만들지 않습니다. |
| LEVEL 2 - Intermediate | 원본 gallery와 증강 query를 구분하고, 다른 실행에서 저장한 결과는 읽지 않습니다. 복원 진행은 분류 회차와 별도로 보입니다. |
| LEVEL 3 - Advanced | gallery는 고유 source_id 하나/canonical 우선, query는 원래 집합 전체입니다. 캐시 run_id와 조건 프로토콜을 확인하며 단계별 실제 완료 수를 API로 제공합니다. |
| LEVEL 4 - Professional | 연결 점수 분모는 query 행 수, gallery_size는 고유 원본 수입니다. 동일 원본의 환자 충돌을 거부합니다. 진행 보고는 대체로2초 간격으로 제한하며 분류 정확도·체크포인트는 보존합니다. |
| LEVEL 5 - Expert | source_id Top-k membership으로 positional-index false negative를 제거했습니다. 공격 결과는 run_id, 조건 결과는 protocol/condition까지 검증합니다. 콜백은 디코더 train/validation·reconstruction·linking·membership·shuffle 실제 처리 수만 보고합니다. CPU4/API1 및 영향CPU8/UI2 검증이며 GPU 전체·실브라우저를 검증했다는 뜻은 아닙니다. |

[수정 동작 상세](../../Conv1%20블러%20OK-NG%20실험/17차/docs/연결공격_캐시_진행표시_수정.md)

앞선 공격·셔플 수리의 검사 근거와 이번 연결·캐시·진행 표시 검사는 구분합니다. 이번3건의 검사 범위는 바로 위 후속 표와 수정 상세를 참조합니다.

## 전체 재검증 후속

| 수준 | 이번 변경과 근거 |
|---|---|
| LEVEL 1 - Beginner | 사진 설명에 어떤 모델로 복원했고 무엇을 알고 공격했는지 표시합니다. 검사파일29개가 통과했습니다. |
| LEVEL 2 - Intermediate | 이전 설정·화면용 검사10개(구엔진3·화면7)가 깨진 원인을 보존하고 새 화면·설정에 맞췄습니다. 기존28개와 새 사진설정1개를 구분합니다. |
| LEVEL 3 - Advanced | legacy 엔진 검사는 별도설정·합성계보를 사용하고 SCI운영설정과 분리합니다. 사진 설정은 실제 선정 checkpoint SHA와 위협모형을 저장·표시합니다. |
| LEVEL 4 - Professional | 최초28파일18통과/10실패 원문과 수정후28통과를 보존하고 설정생성1개를 추가했습니다. 현재준비영상6469개 SHA/픽셀/규격/분할 검사 통과, CSTL차단 유지입니다. |
| LEVEL 5 - Expert | 검사fixture의 구schema/함수/selector/경로 가정을 현재SCI계약으로 옮겼으며 기존 checkpoint/threat 표시assert2를 복구했습니다. run_protection→server whitelist→photoSettings에 실제 선정SHA/가정을 연결했습니다. 검증은 CPU/Rust/HTTP/VM 및 6469영상 읽기이며 실제GPU전체·14k물리생성·실브라우저는 미수행입니다. |

선행절의 개별 검사 수는 이전 수정의 근거이며, 최신 전체 검사는 위29파일과 실제자료 읽기 범위로 해석합니다.

## 중단 후 최적 모델 재개 보완 (2026-11-27)

| 설명 수준 | 문제와 수정 | 확인 근거 | 남은 범위 |
|---|---|---|---|
| LEVEL 1 - Beginner | 저장 도중 멈춰도 가장 잘 배운 모델을 다시 찾도록 수정 | 작은 CPU 중단/재개6검사 통과 | 실제 긴 GPU 실험은 별도 |
| LEVEL 2 - Intermediate | 마지막 저장과 최적 모델 표식 사이 중단에서 옛 모델을 고르던 문제를 복구 | 신규6·관련 기존16방법 통과 | 분류 점수를 조작하지 않음 |
| LEVEL 3 - Advanced | 분류기와 복원 디코더 재개 직후 검증 이력 최저와 포인터 SHA·계보 확인 | 독립6+동률 최초최저1 확인 | 선행29·6469영상 검사는 기존 근거 재사용 |
| LEVEL 4 - Professional | last 체크포인트 검증 뒤 남은 epoch 전에 best 복구; current/history도 마지막 완료 이력에서 복원 | stale/missing·후속 비개선·이전 최저 보존·불일치 거부 | 실제 전원 차단 내구성 전체를 보장하지 않음 |
| LEVEL 5 - Expert | 연속 epoch/run/finite loss/argmin/state.best 일치 확인; 최신 개선만 권위 있는 last SHA로 복구하고 이전 최저는 기존 reference epoch/path/hash·checkpoint run/protocol/condition/loss 검증 | 실제 SCI 통합 CPU 경로와 별도 동률 반례; 실패 원문은 비공개 보존 | 학습/공격/분할/블러 수식은 동일, GPU 전체·14k 생성·브라우저는 미수행 |

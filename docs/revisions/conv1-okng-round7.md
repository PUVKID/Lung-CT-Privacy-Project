# 실제 7차·새 σ0 모델 한 개를 고정한 열 강도 평가

[LEVEL 1 - Beginner](#user-content-reading-level-1) · [LEVEL 2 - Explorer](#user-content-reading-level-2) · [LEVEL 3 - Practitioner](#user-content-reading-level-3) · [LEVEL 4 - Advanced](#user-content-reading-level-4) · [LEVEL 5 - Expert](#user-content-reading-level-5)

실제 실험 차수와 기존 공개 코드 번호를 구분합니다. [프로젝트 첫 화면](../../README.md) · [실제 자료](../../Conv1%20%EB%B8%94%EB%9F%AC%20OK-NG%20%EC%8B%A4%ED%97%98/7%EC%B0%A8) · [직전 전체 비교](../revision-diffs/conv1-okng-round7.md)

<details open>
<summary>LEVEL 1 · Beginner — 목적과 동작부터</summary>

<a id="reading-level-1"></a>

## LEVEL 1 - Beginner

블러 없이 한 번 배운 모델을 고정한 뒤, 블러만 바꾸면 얼마나 달라지는지 살펴봅니다. 모델을 고정한다는 것은 배운 숫자를 더 바꾸지 않는다는 뜻입니다.

| 단계 | 고정 규칙 | 확인할 기록 |
| --- | --- | --- |
| 새 학습 | 로컬 ImageNet 초기값에서 σ0 만 100회 | 학습 강도 0·회차·원본/분할·초기값 |
| 모델 선정 | σ0 검증 원시 손실 최저 best 한 개 | 선정 epoch·체크포인트 SHA·전체 state digest |
| 열 평가 | σ0·1·2·4·8·16·32·64·128·256 | 같은 모델 SHA·추가 optimizer 갱신 0 |
| 화면·그림 | 학습 중 열 평가 대기, 완료 평가만 표시 | 같은 run·소스·모델·각 PNG SHA |

먼저 블러 0에서 100회 배우고, 가중치 학습에 쓰지 않은 검증 사진에서 손실이 가장 낮았던 한 모델을 선택합니다.

그 모델을 그대로 둔 채 열 가지 블러 강도를 평가합니다.

강도 4를 고른다고 강도 4에서 다시 배우지 않습니다.

학습 중에는 모든 평가가 대기이며 옛 5·6차 수치를 빈칸에 채우지 않습니다.

2026-11-20 공개 기록 시점에 새 7차는 학습 중이고 최종 시험 결과는 **미측정**입니다.

환자 ID가 없어 **영상 단위 예비실험**입니다. 같은 환자의 다른 영상이 분할 양쪽에 남았는지 확인할 수 없고 임상 일반화·환자 독립성·프라이버시 달성을 주장하지 않습니다. 클래스당 5,000개는 매 회차 반복·온라인 증강 표본이며 독립 원본 5,000장이 아닙니다.

[같은 수준 프로젝트](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A81.md) · [직전 차수](conv1-okng-round6.md#user-content-reading-level-1) · [자료 폴더](../../Conv1%20%EB%B8%94%EB%9F%AC%20OK-NG%20%EC%8B%A4%ED%97%98/7%EC%B0%A8) · [전체 비교](../revision-diffs/conv1-okng-round7.md)


</details>

<details>
<summary>LEVEL 2 · Explorer — 구성과 연결 원리</summary>

<a id="reading-level-2"></a>

## LEVEL 2 - Explorer

학습 한 번·모델 선정 한 번·열 강도 평가를 구분합니다. 6차 진단에서 관측한 적응 학습과 고정 모델의 차이를 새 실험에서 처음부터 명확히 통제합니다.

| 조건 | 실제 설정 | 해석 |
| --- | --- | --- |
| 자료 | 원본 1,097장, train769/validation164/test164 | 원본을 분할한 뒤 학습에만 온라인 증강 |
| 분류 | OK =양성 + 정상, NG =악성 | 원본 폴더 라벨이며 환자·기관 ID가 아님 |
| 모델 | torchvision ResNet50 V1.5, conv1·모든 BN 고정 | layer4 비BN와 head 학습 |
| 표본·정밀도 | 클래스당 5,000, batch8, 512×512, BF16 학습·FP32 평가 | 평가 손실은 FP64 안정 계산 |
| 선택 | 검증 손실 기준 | 시험 수치로 모델·σ·임계값 선택 없음 |

학습과 모델 선정의 블러는 항상 0입니다. 100회가 끝난 뒤 선택한 best 파일 SHA와 BatchNorm buffer까지 포함한 전체 state digest를 고정합니다.

평가마다 새 블러 모듈을 만들고 입력 특징만 바꾸며 가중치·BN 상태는 바꾸지 않습니다.

손실이 가장 낮았던 회차는 100회보다 앞일 수 있지만 100회 학습 자체를 조기 종료하지 않습니다.

아직 측정하지 않은 정확도를 예측하거나 단조 감소를 보장하지 않습니다.

환자 ID가 없어 **영상 단위 예비실험**입니다. 같은 환자의 다른 영상이 분할 양쪽에 남았는지 확인할 수 없고 임상 일반화·환자 독립성·프라이버시 달성을 주장하지 않습니다. 클래스당 5,000개는 매 회차 반복·온라인 증강 표본이며 독립 원본 5,000장이 아닙니다.

[같은 수준 프로젝트](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A82.md) · [직전 차수](conv1-okng-round6.md#user-content-reading-level-2) · [자료 폴더](../../Conv1%20%EB%B8%94%EB%9F%AC%20OK-NG%20%EC%8B%A4%ED%97%98/7%EC%B0%A8) · [전체 비교](../revision-diffs/conv1-okng-round7.md)


</details>

<details>
<summary>LEVEL 3 · Practitioner — 준비·실행·결과 확인</summary>

<a id="reading-level-3"></a>

## LEVEL 3 - Practitioner

공개 설정은 실행 예제이며 원본·분할·초기 가중치를 **포함하지 않습니다**. 자신의 고정 기준을 준비하고 검사한 뒤 감독 실행으로 시작합니다.

| 단계 | 고정 규칙 | 확인할 기록 |
| --- | --- | --- |
| 새 학습 | 로컬 ImageNet 초기값에서 σ0 만 100회 | 학습 강도 0·회차·원본/분할·초기값 |
| 모델 선정 | σ0 검증 원시 손실 최저 best 한 개 | 선정 epoch·체크포인트 SHA·전체 state digest |
| 열 평가 | σ0·1·2·4·8·16·32·64·128·256 | 같은 모델 SHA·추가 optimizer 갱신 0 |
| 화면·그림 | 학습 중 열 평가 대기, 완료 평가만 표시 | 같은 run·소스·모델·각 PNG SHA |

7차 폴더에서 `config.example.json`을 `config.json`으로 복사하고 `dataset_root`와 기준 manifest 경로·파일 SHA·recordsSHA를 자신의 자료로 채웁니다.

로컬 ImageNet V1 파일을 `initial_weights_path`에 준비하고 명시된 SHA와 대조해야하며 외부 다운로드 우회는 없습니다. `run_training.py prepare`가 원본과 입력 기준을 고정하고 `안전_학습.py --device cuda --baseline-sha256 <검토한 입력기준SHA>`가 중복·공간·원본 불변을 확인한 뒤 실행합니다.

준비·연결 검사는 이미 학습이 진행된 작업에서 거부합니다.

대시보드는 `python -B -X utf8 dashboard.py --port 8766`으로 자신의 실험에서만 실행합니다. 세션 URL은 로컬 기록으로 확인하며 공개·외부 전달하지 않습니다. 강도를 바꾸면 그 강도의 평가 차트·수치·그림만 바뀝니다. σ0 학습 곡선을 다른 강도의 학습 곡선으로 표시하지 않습니다.

환자 ID가 없어 **영상 단위 예비실험**입니다. 같은 환자의 다른 영상이 분할 양쪽에 남았는지 확인할 수 없고 임상 일반화·환자 독립성·프라이버시 달성을 주장하지 않습니다. 클래스당 5,000개는 매 회차 반복·온라인 증강 표본이며 독립 원본 5,000장이 아닙니다.

[같은 수준 프로젝트](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A83.md) · [직전 차수](conv1-okng-round6.md#user-content-reading-level-3) · [자료 폴더](../../Conv1%20%EB%B8%94%EB%9F%AC%20OK-NG%20%EC%8B%A4%ED%97%98/7%EC%B0%A8) · [전체 비교](../revision-diffs/conv1-okng-round7.md)


</details>

<details>
<summary>LEVEL 4 · Advanced — 구현·설계·실패 처리</summary>

<a id="reading-level-4"></a>

## LEVEL 4 - Advanced

src.identity가 현재 소스·설정·분할·선정 파일·예측 CSV를 함께 묶습니다. src.training은 학습 모델 한 개와 동결 평가 모델을 분리합니다.

| 단계 | 고정 규칙 | 확인할 기록 |
| --- | --- | --- |
| 새 학습 | 로컬 ImageNet 초기값에서 σ0 만 100회 | 학습 강도 0·회차·원본/분할·초기값 |
| 모델 선정 | σ0 검증 원시 손실 최저 best 한 개 | 선정 epoch·체크포인트 SHA·전체 state digest |
| 열 평가 | σ0·1·2·4·8·16·32·64·128·256 | 같은 모델 SHA·추가 optimizer 갱신 0 |
| 화면·그림 | 학습 중 열 평가 대기, 완료 평가만 표시 | 같은 run·소스·모델·각 PNG SHA |

평가는 eval/no_grad에서 수행하고 optimizer.step을 호출하지 않습니다.

매 강도 전후 checkpoint SHA와 전체 state fingerprint를 대조하고 `eval_optimizer_steps=0`을 저장합니다.

상태의 `phase`는 preparing/training/evaluation/completed, `training_status`와 평가 대기 열을 별도 유지합니다.

원본·metadata·단일 선정 모델이 다르면 API 는 결과를 제공하지 않습니다.

특징 생성은 CPU에서 평가가 끝난 강도만 18장씩 처리하며 다른 실행의 그림을 섞지 않습니다.

환자 ID가 없어 **영상 단위 예비실험**입니다. 같은 환자의 다른 영상이 분할 양쪽에 남았는지 확인할 수 없고 임상 일반화·환자 독립성·프라이버시 달성을 주장하지 않습니다. 클래스당 5,000개는 매 회차 반복·온라인 증강 표본이며 독립 원본 5,000장이 아닙니다.

[같은 수준 프로젝트](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A84.md) · [직전 차수](conv1-okng-round6.md#user-content-reading-level-4) · [자료 폴더](../../Conv1%20%EB%B8%94%EB%9F%AC%20OK-NG%20%EC%8B%A4%ED%97%98/7%EC%B0%A8) · [전체 비교](../revision-diffs/conv1-okng-round7.md)


</details>

<details>
<summary>LEVEL 5 · Expert — 근거·프로토콜·한계 검토</summary>

<a id="reading-level-5"></a>

## LEVEL 5 - Expert

7차는 기존 5차 best를 재사용하지 않는 새 실험입니다. 초기 ImageNet 파일과 고정 원본·분할, σ0 100회 이력, 단일 선정 identity, 열 평가의 모델 불변을 함께 대조해야 합니다.

| 조건 | 실제 설정 | 해석 |
| --- | --- | --- |
| 자료 | 원본 1,097장, train769/validation164/test164 | 원본을 분할한 뒤 학습에만 온라인 증강 |
| 분류 | OK =양성 + 정상, NG =악성 | 원본 폴더 라벨이며 환자·기관 ID가 아님 |
| 모델 | torchvision ResNet50 V1.5, conv1·모든 BN 고정 | layer4 비BN와 head 학습 |
| 표본·정밀도 | 클래스당 5,000, batch8, 512×512, BF16 학습·FP32 평가 | 평가 손실은 FP64 안정 계산 |
| 선택 | 검증 손실 기준 | 시험 수치로 모델·σ·임계값 선택 없음 |

모델 선택은 σ0의 최소 raw validation loss이며 min_delta 기반 scheduler와 분리합니다. first conv64 채널 직후 DCT-II Gaussian heat blur를 적용하고 layer4 비BN/head만 학습합니다.

평가의 전체 state digest에는 BN buffer가 포함됩니다.

예측 CSV·지표·그림은 동일 run/선정 epoch/checkpointSHA/modelstateSHA에 결합합니다. `initial_weights_sha256`는 공식 ImageNet 파일의 확인 값이고 자료 목록 SHA·실제 학습 run/checkpointSHA는 공개 예제에 싣지 않습니다.

합성 CPU 단위 검사와 512 픽셀 batch8 BF16 GPU 연결 검사는 실제 100회 학습·열 평가 완료 성능과 다릅니다.

현재 7차 시험은 미측정이며 6차 고정 모델 관측을 대입하지 않습니다.

백분율은 소수 첫째 자리 반올림, 원비율·정답 수·전체 자릿수는 원값으로 확인합니다.

반올림 100.0%와 실제 전부 정답을 구분합니다.

환자 ID가 없어 **영상 단위 예비실험**입니다. 같은 환자의 다른 영상이 분할 양쪽에 남았는지 확인할 수 없고 임상 일반화·환자 독립성·프라이버시 달성을 주장하지 않습니다. 클래스당 5,000개는 매 회차 반복·온라인 증강 표본이며 독립 원본 5,000장이 아닙니다.

[같은 수준 프로젝트](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A85.md) · [직전 차수](conv1-okng-round6.md#user-content-reading-level-5) · [자료 폴더](../../Conv1%20%EB%B8%94%EB%9F%AC%20OK-NG%20%EC%8B%A4%ED%97%98/7%EC%B0%A8) · [전체 비교](../revision-diffs/conv1-okng-round7.md)

</details>


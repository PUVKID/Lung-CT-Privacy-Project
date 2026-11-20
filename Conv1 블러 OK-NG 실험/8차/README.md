# 실제 8차·강도별 독립 학습과 프라이버시 제안 점수

[LEVEL 1 - Beginner](../../docs/revisions/conv1-okng-round8.md#reading-level-1) · [LEVEL 2 - Explorer](../../docs/revisions/conv1-okng-round8.md#reading-level-2) · [LEVEL 3 - Practitioner](../../docs/revisions/conv1-okng-round8.md#reading-level-3) · [LEVEL 4 - Advanced](../../docs/revisions/conv1-okng-round8.md#reading-level-4) · [LEVEL 5 - Expert](../../docs/revisions/conv1-okng-round8.md#reading-level-5)

열 블러 강도 각각 새 100회 학습 뒤 최저 검증 손실 모델을 선택하고 분류와 원본 후보 공격을 모두 계산한 다음 다음 강도로 진행합니다. **2026-11-20 확인 시점 σ0 학습 중이며 분류 성적과 점수는 미측정**입니다. 기존 7차의 단일 고정 모델 실험과 다릅니다.

| 자료 | 역할 | 입력 조건 |
| --- | --- | --- |
| config.example.json | 공개 설정 형식 | 자신의 dataset/기준 manifest 경로·파일 SHA·recordsSHA·초기 가중치 필요 |
| src/·run_training.py·안전_학습.py | 학습·선정·분류·공격·감독 | 실제자료를 포함하지 않음 |
| dashboard.py·web/ | 강도 선택과 실제 원값 조회 | 선택 강도 모델/입력/소스 결합 검증 |
| tests/ | 합성 단위검사·API·Node VM 회귀 | 실제 CT 공격 성적이나 화면 렌더링 검사가 아님 |
| 결과/측정상태.json | 실제 미측정 상태 | 합성 대조군 점수를 실제 결과로 채우지 않음 |

공개 사 본의 config.example.json을 config.json으로 복사하고 자신의 입력을 준비해야 합니다.

**전체 검사 중 실제 ResNet50 경로 검사는 로컬 ImageNet V1 초기 가중치 파일이 필요합니다.** 실제 CT 없이 수행하는 합성 검사에도 이 모델 검사를 포함합니다. config.json의 initial_weights_path를 자신의 로컬 파일로 지정하고 initial_weights_sha256와 대조해야 합니다.

예제를 config.json으로 복사한 뒤 검사 명령 실행 전에 이 입력을 준비하며, 가중치를 공개 저장소에 넣지 않습니다.

원영상·분할 manifest·가중치는 외부에 포함하지 않습니다.

로컬 ImageNet V1 파일의 SHA와 실제 기준 manifest를 대조한 뒤 prepare로 입력을 고정합니다.

이미 학습이 시작된 작업에서는 prepare·smoke가 상태를 덮어쓰지 않도록 거부합니다.

실제 연구 폴더나 실행 중인 서버를 이 공개 예제로 바꾸지 않습니다.

합성 검사는 별도의 공개 사본에서 다음과 같이 실행합니다. Python·PyTorch·torchvision·NumPy·SciPy·Pillow와 Node.js가 필요하며 호환 환경은 직접 확인해야 합니다. 이 저장소에 의료 자료와 초기 가중치를 포함했다는 뜻은 아닙니다.

```powershell
Copy-Item -LiteralPath config.example.json -Destination config.json
# 이어 config.json의 initial_weights_path를 로컬 가중치로 지정하고 SHA를 확인합니다.
$env:CUDA_VISIBLE_DEVICES = "-1"
python -B -X utf8 -m unittest discover -s tests -p "test_*.py" -v
```

실제 입력을 별도로 준비한 실험에서는 `python -B -X utf8 run_training.py prepare` 후 검토한 baseline SHA를 `python -B -X utf8 안전_학습.py --device cuda --baseline-sha256 <검토한SHA>`에 전달합니다.

세션/작업 식별자는 공개 감독 사본의 CT_EXPERIMENT_SESSION·CT_EXPERIMENT_TASK 환경변수로 로컬 지정할 수 있습니다.

토큰·세션 URL·실패 원문과 의료 경로는 공개하지 않습니다.

화면의 **프라이버시 제안 점수·100점 만점**은 gallery-residual-v1입니다.

알려진 인코더와 원본 후보 gallery에서 실제 특징 바이트 사전 공격을 포함해 측정하는 조건부 연구용 잔여 점수입니다.

높을수록 이 공격에서 원본을 되찾기 어렵다는 뜻이며 보호 확률·세계 최초·표준·DP·환자 재식별 방어를 뜻하지 않습니다.

실측 0점은 0.0으로 표시하고 미완료·오류는 미측정으로 남깁니다.

상세의 같은 읽기 수준에서 산 식·분모·정밀도·한계를 확인하세요.

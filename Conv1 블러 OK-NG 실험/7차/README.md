# 실제7차 고정 모델 블러 실험

[LEVEL 1 - Beginner](../../docs/revisions/conv1-okng-round7.md#reading-level-1) · [LEVEL 2 - Explorer](../../docs/revisions/conv1-okng-round7.md#reading-level-2) · [LEVEL 3 - Practitioner](../../docs/revisions/conv1-okng-round7.md#reading-level-3) · [LEVEL 4 - Advanced](../../docs/revisions/conv1-okng-round7.md#reading-level-4) · [LEVEL 5 - Expert](../../docs/revisions/conv1-okng-round7.md#reading-level-5)

새 ImageNet 초기값에서 σ0만100회 학습하고 최저검증손실 모델 하나를 고정해 열 블러 강도를 추가학습 없이 평가합니다. 공개 기록 시점 학습 진행 중이며 최종시험결과는미측정입니다.

| 자료 | 역할 | 사용 조건 |
| --- | --- | --- |
| 코드 | 실제 공개 소스 | 자신의 자료·환경과 기준 필요 |
| 설정 예제 | 사적 경로·manifest SHA 제외 | config.json과 고정 입력을 직접 준비 |
| 상세 설명 | 절차·조건·검증·한계 | 위에서 같은 수준 선택 |

`config.example.json`을 자신의 `config.json`으로 복사한 뒤 원본 경로와 고정 기준을 채워야 합니다. 예제만으로 실제학습·복구를 실행할 수 없습니다. 원영상·manifest·모델·상태·접속정보는 공개하지 않습니다.

## 공개 코드의 합성 검사

합성 검사는 실제 CT·가중치 없이 수행하지만 설정 형식을 읽으므로 먼저 공개 예제를 config.json으로 준비합니다. 자신의 실제 학습 설정과 혼동하지 않도록 별도의 공개 사본에서 수행합니다.

```powershell
Copy-Item -LiteralPath config.example.json -Destination config.json
$env:CUDA_VISIBLE_DEVICES = "-1"
python -B -X utf8 -m unittest discover -s tests -p "test_*.py" -v
```

검사 후 자신이 준비한 임시 config.json만 정리하고, 실제 학습에는 자신의 고정 자료와 검토한 설정을 다시 준비합니다. 심볼릭 링크 생성 권한이 없는 Windows에서는 해당 권한 의존 검사 한 개가 건너뛰어질 수 있으므로 나머지 검사 성공과 구분합니다.

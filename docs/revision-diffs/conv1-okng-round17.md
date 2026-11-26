# 17차 공개 변경 전체 비교

기준 커밋: `1691e069d2c0dcd84d46e2a845346895d7631c8f`. 이미 게시한 17차 SCI 준비코드의 같은 차수 후속 수정입니다. 이 기준 커밋 대비 전체 검사fixture 정정·선정 모델SHA와 공격 가정의 사진 설명 연결의 실제 전체 차이를 비교합니다. 원격의 기존 차수와 다른 사람의 변경은 보존합니다.

아래 diff는 새 소스·설정 예제·차수 설명·변경 기록과 기존 탐색 문서의 실제 변경을 포함합니다. 줄바꿈은 원파일 바이트를 보존합니다. 비교 문서 자신과 그 diff 조각은 자기참조 해시 순환을 피하기 위해 본문 diff 대상에서 제외하며 별도 공개 묶음 manifest에 크기·SHA를 동결합니다. 바이너리는 원파일과 크기·SHA를 대조합니다.

| 전체 텍스트 비교 | 바이트 | SHA256 |
|---|---:|---|
| [part-01.diff](conv1-okng-round17/part-01.diff) | 97365 | `fb98b8b310b4bfa2afdb4c79c3f6d812d93458911a69433d791e5877d20a1938` |
| [part-02.diff](conv1-okng-round17/part-02.diff) | 62641 | `5ac7ebfe268a524ee31ce8281cbfd0c3151dbffe92002f474258f9a0dd362f66` |

| 실제 추가·수정 파일 | 상태 | 바이트 | SHA256 |
|---|---|---:|---|
| Conv1 블러 OK-NG 실험/17차/README.md | modified | 12762 | `0ef7bb3710f1b1fbe434250f8494bd0e494c4fdd3e3c0368856cf97421d81dc1` |
| Conv1 블러 OK-NG 실험/17차/SCI공격.py | modified | 44372 | `fc01c5c49b72dcae63ecbd4b942e99136dfe1b4e0c56328badce4ea9534d90ad` |
| Conv1 블러 OK-NG 실험/17차/tests/SCI사진설정_검사.py | added | 1739 | `9327e8507462a07298d25e1e7e44bdb3f9aa9d95d6397c971d1bf707e1e9e575` |
| Conv1 블러 OK-NG 실험/17차/tests/engine_feature_test.py | modified | 9065 | `a3b2476070cccb8dadc27e5dc39e636db5faa02d40ec646633da010072d6d791` |
| Conv1 블러 OK-NG 실험/17차/tests/engine_final_test.py | modified | 4763 | `e2822a1defdcad78ffd604ed1ed52861ecbb12f9bf6cf2e5809e562472684769` |
| Conv1 블러 OK-NG 실험/17차/tests/engine_test.py | modified | 11308 | `baf52c623debdbf6574a943f86245c273a75c3bc54e9cf5f7137ea8a042e973d` |
| Conv1 블러 OK-NG 실험/17차/tests/보조/이전설정.py | added | 1309 | `a8391c94f5a817508e5999242734450ace26708a7559e8a853ec40026fe8bebc` |
| Conv1 블러 OK-NG 실험/17차/대시보드 화면/app.js | modified | 16530 | `f553a8b8b5ee47fa8d25df957e96877964d4222a4fe8f8fca9582e38e2222e73` |
| Conv1 블러 OK-NG 실험/17차/대시보드 화면/tests/노출선택_합성검사.mjs | modified | 1742 | `2160124029e44c6cdf1b0977d6d16efe2f2baa16c903633d806912a3572a6455` |
| Conv1 블러 OK-NG 실험/17차/대시보드 화면/tests/복원지표_합성검사.mjs | modified | 2759 | `d60f0833588d8a5f830efecfacc6d2a3108be2d3afbd896c3cb4064435d254c0` |
| Conv1 블러 OK-NG 실험/17차/대시보드 화면/tests/시험구분_합성검사.mjs | modified | 2183 | `08834888b2236b35620b8c76086c475e2621ffd1c462fbac0f5f47de4fc56c0f` |
| Conv1 블러 OK-NG 실험/17차/대시보드 화면/tests/실행ID_합성검사.mjs | modified | 2877 | `eb1564e56c156ef2aa619ac835353be30daf681c0466842bfc458de75fe04899` |
| Conv1 블러 OK-NG 실험/17차/대시보드 화면/tests/특징노출_합성검사.mjs | modified | 2070 | `ccbdefad031bbb22ae4b2df9cdd85a1c4c36cba99400030f1fa4207f1a68dac9` |
| Conv1 블러 OK-NG 실험/17차/대시보드 화면/tests/특징사진_계약검사.mjs | modified | 2431 | `a457eddaec8830379f891951e43a7a55f83d26cfd7c2fd4c46287303feea88c5` |
| Conv1 블러 OK-NG 실험/17차/대시보드 화면/tests/합성자료_검사.mjs | modified | 2360 | `9025ae693b5a12b983624c4ad3948a6a71694618d3ffb17429fb469d197e8184` |
| docs/changes/2026-11-27-17차-전체재검증.md | added | 1209 | `36c0b476716d4ec74271dcb128be395fbfb2ddc94c1f8f0b54e0402afa7cbacb` |
| docs/revisions/conv1-okng-round17.md | modified | 31697 | `6ec662fcc67c58fc3ece92bf5588681a01e05b8189e8df190db3587c3f0d0cc1` |

# 17차 공개 변경 전체 비교

기준 커밋: `b777c5c466cbe4db06c370e7e314986787df7e1b`. 기존 원격 파일을 보존한 별도 작업 사본에서 새17차를 추가합니다. 원격에는1~8차가 있고9~16차를 이번 게시물의 성과로 채우지 않습니다. 새 SCI 프로토콜이므로 같은 공개 프로토콜의 직전 차수는 없습니다.

아래 diff는 새 소스·설정 예제·차수 설명·변경 기록과 기존 탐색 문서의 실제 변경을 포함합니다. 줄바꿈은 원파일 바이트를 보존합니다. 비교 문서 자신과 그 diff 조각은 자기참조 해시 순환을 피하기 위해 본문 diff 대상에서 제외하며 별도 공개 묶음 manifest에 크기·SHA를 동결합니다. 바이너리는 원파일과 크기·SHA를 대조합니다.

| 전체 텍스트 비교 | 바이트 | SHA256 |
|---|---:|---|
| [part-01.diff](conv1-okng-round17/part-01.diff) | 156841 | `773a633b9c4f69d7aa3f2fe1c2adf3891dd0aed387d56297344f8a75a3ea2fee` |
| [part-02.diff](conv1-okng-round17/part-02.diff) | 153949 | `3ac252d5cca95e45df43523a4e5b17fe6cf94ca2e48c1faa653d1850421cb9dc` |
| [part-03.diff](conv1-okng-round17/part-03.diff) | 152750 | `d7230bd22048d2ef01c6868fc87945f0b7007e509483f76f0a1b683740f121ed` |
| [part-04.diff](conv1-okng-round17/part-04.diff) | 38542 | `52ff1eb24feeaa8ba4fbf16ca76b6af0f7cd9785325881ae279f5ac065902b4c` |

| 실제 추가·수정 파일 | 상태 | 바이트 | SHA256 |
|---|---|---:|---|
| Conv1 블러 OK-NG 실험/17차/README.md | added | 7689 | `11f4f0717e14935aa72f083eab76047229c53d24cdea824cb14092019eb2d06e` |
| Conv1 블러 OK-NG 실험/17차/SCIconfig.example.json | added | 1810 | `bd8f86d27d28dae36c8492fd2469b80ffecb9580c633907e50b6a6dc61208603` |
| Conv1 블러 OK-NG 실험/17차/SCI공격.py | added | 34412 | `adad34685123f3f32c51e8a27b6ee0b160cdcbe8a096cdf4f95c3e7dec25a41d` |
| Conv1 블러 OK-NG 실험/17차/SCI데이터.py | added | 48986 | `d4a8b80a0f60f78de4b912b9d3cf0844defba43ee89bf320f5792f9234ca6774` |
| Conv1 블러 OK-NG 실험/17차/SCI모델.py | added | 3927 | `a5e200a03380775e3f853a71905a483f64941457c0975e1be00558494770b6ee` |
| Conv1 블러 OK-NG 실험/17차/SCI실행.py | added | 21139 | `448bc56c9970b6949231687e8488712e8f5b8c03f6ef18e79d53298b757a2b44` |
| Conv1 블러 OK-NG 실험/17차/config.example.json | added | 1713 | `b4282a8f4357e4076e803e6a4eeecc77d8da565ddbafea1ec256213c19d53e30` |
| Conv1 블러 OK-NG 실험/17차/legacy/__init__.py | added | 74 | `9f3fbda4cc9de57f05c51c3e7c7f6b461834755fbe8e8c4c8fa704e5a577613f` |
| Conv1 블러 OK-NG 실험/17차/legacy/identity.py | added | 9278 | `6e9bc29eae130b6884dbbf84d9af652705c888d2371d43e4c2d5f9e177420929` |
| Conv1 블러 OK-NG 실험/17차/legacy/model.py | added | 16559 | `24c9305ddbdc75268ab07b9c5ce77053601e4fbd905bc03d885ac0627382a96a` |
| Conv1 블러 OK-NG 실험/17차/rust/src/main.rs | added | 4555 | `0ec02e8cdab288913b7be51db9eafa2b82160ddecd45fe18b2777f18f174a51b` |
| Conv1 블러 OK-NG 실험/17차/tests/SCI_근거재사용_검사.py | added | 2563 | `be5fb8c85a77276c76c59ac31e38b7ef2bee9a0a1427523f8a0cdd2a5b092d5c` |
| Conv1 블러 OK-NG 실험/17차/tests/SCI데이터_검사.py | added | 10034 | `785b3ada4e15484009e75cbd248501bd78afa4b29f04ad3dc698b269945cb4ec` |
| Conv1 블러 OK-NG 실험/17차/tests/SCI엔진_검사.py | added | 15413 | `4fca8a5b76822f60f8d688dc591b0293eaed8b32a486506958d4038adacfad8b` |
| Conv1 블러 OK-NG 실험/17차/tests/engine_context_test.py | added | 2325 | `b03a3e8fc987a1cc0175a0c315dd87669d3e65d2d9891f186e6f0d2ef69f0f7c` |
| Conv1 블러 OK-NG 실험/17차/tests/engine_cuda_guard_test.py | added | 4206 | `0fc91ef290a5015af6d6363a589aa022ea196e0988b86cdcfe9063c80ed8484f` |
| Conv1 블러 OK-NG 실험/17차/tests/engine_dashboard_size_test.py | added | 3329 | `1cea442d07f18772fb7b618c6e25a97600240cfbdd792063c4e24224bab536ef` |
| Conv1 블러 OK-NG 실험/17차/tests/engine_feature_test.py | added | 8877 | `3993bbef06f2f6c8ac688835ca0d678d7d035506d984576de4b196387a32f501` |
| Conv1 블러 OK-NG 실험/17차/tests/engine_final_test.py | added | 4624 | `7d0d28a48aff583018bd5eb86a1cc424de709fcdcad616318bf9695e05102e6f` |
| Conv1 블러 OK-NG 실험/17차/tests/engine_test.py | added | 11022 | `0841c607447abe086756016411dcf33799691ff73f0f369703fc3876d3dfd38d` |
| Conv1 블러 OK-NG 실험/17차/tests/전송_검사.py | added | 2000 | `e6adecaac12fc8dd680f4a2f119bef600b3bf5b35d7b7c7466bddf3dc1b7d562` |
| Conv1 블러 OK-NG 실험/17차/tests/지표_검사.py | added | 921 | `b061abbc170c64a0fff76679da08351b01da944035e605457d8bb4825e44a149` |
| Conv1 블러 OK-NG 실험/17차/tests/특징전송_검사.py | added | 1603 | `efd3dd6d7edb9cdf680c989ee187f72b19d5918a9972af17755b921f7948bc0e` |
| Conv1 블러 OK-NG 실험/17차/공격.py | added | 17756 | `eada15d82eb83eeb8255ed0f4bf57662f95189060a6d481d599a02376823b3e1` |
| Conv1 블러 OK-NG 실험/17차/공식자료.json | added | 18302 | `a4e8d0ba605bc494e33650779d34218b7883e94dc1534efe4ce05548b645e20c` |
| Conv1 블러 OK-NG 실험/17차/단서진단.py | added | 1999 | `2de94fa1ada5d65ced5d4597ab6adc58687369400cc4297272655578cbb75336` |
| Conv1 블러 OK-NG 실험/17차/대시보드 화면/16차-화면.css | added | 30526 | `2aa2a6bd91c9ca6404fda5509ff16d8858b8352791159a2e7be07b13808f14b8` |
| Conv1 블러 OK-NG 실험/17차/대시보드 화면/Astryx-MIT-LICENSE.txt | added | 1077 | `a6855be541fc8f446acd1bc4f2f8efce1ace6dce71dba32fcd8da553ee54b473` |
| Conv1 블러 OK-NG 실험/17차/대시보드 화면/app.js | added | 15523 | `6efd76424094340e0d6893e692b5d67f67098b54a39603dece490560a8fe639f` |
| Conv1 블러 OK-NG 실험/17차/대시보드 화면/astryx-neutral.css | added | 30284 | `7b87f44cf2e3000e1aa5e94cff5ccfcee9c665e886657082508854c373dc1bf5` |
| Conv1 블러 OK-NG 실험/17차/대시보드 화면/astryx-research.css | added | 4928 | `c6dafe79cf6e317af3892d73ea5ca713e1e2986c676de8ddd9b09a1e749b0623` |
| Conv1 블러 OK-NG 실험/17차/대시보드 화면/astryx-tokens.css | added | 2038 | `1e791475a7844ecc50ea9779c1232cb075e05153f90df14f0d09793f7b9681f4` |
| Conv1 블러 OK-NG 실험/17차/대시보드 화면/fonts/NanumGothic-Bold.ttf | added | 2073868 | `f96298f9fb18e364d2370f4c3ce948ac67a2b61af992d7234bc15c42b033c674` |
| Conv1 블러 OK-NG 실험/17차/대시보드 화면/fonts/OFL.txt | added | 4534 | `eeacf16032901d0ed0456876ec77b8f0fda6b3fecec7d972f8543eb602e6c30f` |
| Conv1 블러 OK-NG 실험/17차/대시보드 화면/index.html | added | 8412 | `5eebee75cf0670cce7696f67408de9a788fce1c764f2b1d6b4913c583ea1462e` |
| Conv1 블러 OK-NG 실험/17차/대시보드 화면/server.mjs | added | 16359 | `edfc65643a09e9d2e9d7015ba38d71ac622d313cce7ef46ba0dd7d2ea007c246` |
| Conv1 블러 OK-NG 실험/17차/대시보드 화면/tests/SCI_연결_합성검사.mjs | added | 4386 | `b2fd8389d3500c8db6fa601c261a8e795ea3e2e708d8e68c852b61cc5d23f5c8` |
| Conv1 블러 OK-NG 실험/17차/대시보드 화면/tests/SCI_표시_합성검사.mjs | added | 2106 | `99401c8b13eca6cb9aa6c2c14b9860f409b8eaaffd5ff7b7f0471ac1a3e01b82` |
| Conv1 블러 OK-NG 실험/17차/대시보드 화면/tests/노출선택_합성검사.mjs | added | 1929 | `e9eea7816fceba4172d595de30fa299b5595a7bfb1bdacb89b853564b860cf7a` |
| Conv1 블러 OK-NG 실험/17차/대시보드 화면/tests/복원지표_합성검사.mjs | added | 2654 | `c7726f5b5a607fd7c43b69368512179a0bd48796f1b564433a65dccd94d5225b` |
| Conv1 블러 OK-NG 실험/17차/대시보드 화면/tests/설명카드_상태검사.mjs | added | 1118 | `e0d9c4e637fa94e3cc9cfa95d7f6c2807a63b46682cb2d4a0972c7ea5f08efa7` |
| Conv1 블러 OK-NG 실험/17차/대시보드 화면/tests/시험구분_합성검사.mjs | added | 2078 | `2a508cbd29d8f69f028c06274c44b7f22e28db4f96809e2ad8473bea2436d42d` |
| Conv1 블러 OK-NG 실험/17차/대시보드 화면/tests/실행ID_합성검사.mjs | added | 2728 | `69781166386beeaa76135aa1824318560783be9cdde24a6a882b85821b7cb1fb` |
| Conv1 블러 OK-NG 실험/17차/대시보드 화면/tests/축약결과_합성검사.mjs | added | 1780 | `800e355948f2ceb9a486b1e480514076be147499805298842d2ec75bf143bee8` |
| Conv1 블러 OK-NG 실험/17차/대시보드 화면/tests/특징노출_합성검사.mjs | added | 2084 | `6e6d403a6238b780bb4a357d1deeacf647d859857d6bbdd28a5d61af65a401cf` |
| Conv1 블러 OK-NG 실험/17차/대시보드 화면/tests/특징사진_계약검사.mjs | added | 2254 | `95b55bbd22ec652eab494caea72ebe6ab7a5e4755cdbe24deb57d42e8fe1c71d` |
| Conv1 블러 OK-NG 실험/17차/대시보드 화면/tests/합성자료_검사.mjs | added | 2255 | `ef5c8b2d19403ab544921f90a83c2d53e88482ea3b06b61be44aa044be3dba15` |
| Conv1 블러 OK-NG 실험/17차/빌드.py | added | 3328 | `cee393df75e2dd8c80a800fae7dcf9e04470d638945881ae2b45b9c55d8518b8` |
| Conv1 블러 OK-NG 실험/17차/실행.py | added | 44322 | `032a4cdd9b9cf32a3205bb65a6182207d3ac131d5d4e3ebb014d7d710b4cca66` |
| Conv1 블러 OK-NG 실험/17차/전송.py | added | 2627 | `133779dca960bf51e7de299b0927978ecf5db0668eb09977025f5d3df7db0b6c` |
| Conv1 블러 OK-NG 실험/17차/지표.py | added | 4825 | `501bc6fb845d199384a1b685701660af185acb5c4d222f45282495f7f9daed8d` |
| Conv1 블러 OK-NG 실험/17차/특징노출.py | added | 7247 | `6790ff2ec47b69de93048b6dcffd4afa9f20daec8d236e48b75735ef92e1051b` |
| README.md | modified | 98427 | `3f73602cfe2b70829489ce8552ae9f49add10c63f0bdff5d9a012631fc0f0e69` |
| docs/REVISION_INDEX.md | modified | 15949 | `5c938c369cefae1f204a3801a5cf250f003dcf67dae1fcd5bdb2d48ee8671f3a` |
| docs/changes/2026-11-26-SCI-17차-준비.md | added | 439 | `1d9f31b6f0dc436ffcb0e284e14c5f6214b8c9c83ca092d0014466ef13563de3` |
| docs/revisions/conv1-okng-round17.md | added | 22100 | `f7202b9b6a36bd9c0003b51f68f904c5d5fefe5267e95350710f9318c526d238` |
| docs/읽기안내/레벨1.md | modified | 47110 | `0b2cb2f7e35e70ceb982b2fe3a1e7ce5651e654edea7ea8dc81ed3951bad22cc` |
| docs/읽기안내/레벨2.md | modified | 45950 | `9a641a844317aeb977bb5f74390c957d70c5410f585afce49d1fc774d3b00d5f` |
| docs/읽기안내/레벨3.md | modified | 46644 | `134db9d24c83819266727eb445bb9f62189680157c0955e2ccb0c3cdf658d7a7` |
| docs/읽기안내/레벨4.md | modified | 45982 | `7b4ede0e1b4abdbb16ec57693ce5526072dadc30c9b8e20ad2187b555a4296da` |
| docs/읽기안내/레벨5.md | modified | 46714 | `a12ac2ffd17b7cebed06ee278b1dcb450eb0bc9eaa0af6a48d2993a143006715` |

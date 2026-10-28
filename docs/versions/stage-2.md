# 📚 연구 2

ResNet50에서 블록·블러 단독 및 100조합의 분류 성능과 MS-SSIM 점수를 비교합니다.

- [근거 자료](../../%EB%85%BC%EB%AC%B8/2%EC%B0%A8_ResNet50_%EC%B5%9C%EC%A2%85.pdf)
- [전체 보관 기록](../VERSIONS.md) · [프로젝트 소개](../../README.md)

## 🔎 범위와 해석

원고의 학습 epoch와 노트북별 설정은 다릅니다. Privacy Score는 복원 공격 성공률이 아닙니다.


## 🧩 주요 내용

- 원고의 입력 영상 Privacy Score는 50×(1−MS-SSIM)입니다. 특징맵 SSIM이나 복원 공격 성공률과 다른 지표입니다.
- 조합 노트북은 block_scramble과 블러를 입력 영상에 적용하고 ResNet50으로 학습합니다. 학습 설정과 원고의 80/200 epoch 설명은 별도로 살펴봐야 합니다.
- 테스트 의사 라벨로 추가 학습하는 평가입니다. 증강 파생 영상의 fold 교차 가능성과 환자 단위 분할은 후속 검증 과제입니다.

## 🔄 자료 구성

연구 1의 분류 성능 비교에 입력 영상의 유사도 점수와 조합 탐색을 더합니다. 두 원고는 독립 단계이며 모델 교체만으로 향상 원인을 단정하지 않습니다.

## 📍 관련 자료

- [논문/2차_ResNet50_최종.pdf](../../%EB%85%BC%EB%AC%B8/2%EC%B0%A8_ResNet50_%EC%B5%9C%EC%A2%85.pdf) · `연구 방법` · PDF 6–7쪽
- [블록+블러/block_blur_resnet50_v4_KO.ipynb](../../%EB%B8%94%EB%A1%9D%2B%EB%B8%94%EB%9F%AC/block_blur_resnet50_v4_KO.ipynb) · `def block_scramble` · 셀 10 소스 2행
- [논문/2차_ResNet50_최종.pdf](../../%EB%85%BC%EB%AC%B8/2%EC%B0%A8_ResNet50_%EC%B5%9C%EC%A2%85.pdf) · `분할과 평가 한계` · PDF 16쪽

셀 번호는 0부터, 소스 행 번호와 PDF 쪽 번호는 1부터 셉니다. 

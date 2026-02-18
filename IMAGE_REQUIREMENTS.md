# 필요한 이미지 목록

다음 이미지들을 다운로드하여 `static/images/` 폴더에 저장해주세요.

## intro1.html에 필요한 이미지

1. **로고 (Logo)**
   - URL: http://localhost:3845/assets/c753a2b2afb734e44651e8f60f1628e2597203c2.png
   - 저장 경로: `static/images/logo.png`
   - 용도: 상단 네비게이션 왼쪽 로고

2. **상점 일러스트 (Shop Illustration)**
   - URL: http://localhost:3845/assets/a8ff91c8c6cadebde277b1aa7609d80cc257d838.png
   - 저장 경로: `static/images/shop-illustration.png`
   - 용도: 오른쪽에 표시되는 상점 일러스트

3. **메인 타이틀 (DREAM ARTIFACT)**
   - URL: http://localhost:3845/assets/9878522dc3c491a9321d69b7d680e5c7eb0d6db2.png
   - 저장 경로: `static/images/title-dream-artifact.png`
   - 용도: 왼쪽 중앙에 표시되는 메인 타이틀

## intro2.html에 필요한 이미지

1. **로고 (Logo)** - intro1과 동일
   - URL: http://localhost:3845/assets/c753a2b2afb734e44651e8f60f1628e2597203c2.png
   - 저장 경로: `static/images/logo.png`
   - 용도: 상단 네비게이션 왼쪽 로고

2. **상점 일러스트 (Shop Illustration)** - intro1과 동일
   - URL: http://localhost:3845/assets/a8ff91c8c6cadebde277b1aa7609d80cc257d838.png
   - 저장 경로: `static/images/shop-illustration.png`
   - 용도: 오른쪽에 표시되는 상점 일러스트

3. **화살표 버튼 (Arrow Button)**
   - URL: http://localhost:3845/assets/c385a6c11bc645679f9d74b58de7ca5fb30a69fe.svg
   - 저장 경로: `static/images/arrow-button.svg`
   - 용도: 오른쪽 하단 화살표 버튼

## 요약

총 **4개의 이미지**가 필요합니다:
- `logo.png` (로고)
- `shop-illustration.png` (상점 일러스트)
- `title-dream-artifact.png` (메인 타이틀)
- `arrow-button.svg` (화살표 버튼)

## 다운로드 방법

브라우저에서 위 URL들을 열어서 다운로드하거나, 터미널에서:

```bash
# static/images 폴더로 이동
cd static/images

# 각 이미지 다운로드
curl -o logo.png "http://localhost:3845/assets/c753a2b2afb734e44651e8f60f1628e2597203c2.png"
curl -o shop-illustration.png "http://localhost:3845/assets/a8ff91c8c6cadebde277b1aa7609d80cc257d838.png"
curl -o title-dream-artifact.png "http://localhost:3845/assets/9878522dc3c491a9321d69b7d680e5c7eb0d6db2.png"
curl -o arrow-button.svg "http://localhost:3845/assets/c385a6c11bc645679f9d74b58de7ca5fb30a69fe.svg"
```

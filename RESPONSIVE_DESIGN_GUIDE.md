# 반응형 디자인 가이드

## 개요

이 프로젝트는 **1440px 너비 기준**으로 디자인되었으며, 모든 화면 크기에서 동일한 비율을 유지하도록 반응형으로 구현되어 있습니다.

프로젝트는 두 가지 반응형 시스템을 사용합니다:
- **Intro 페이지**: vh 기반 스케일링 (1440×810 기준, 16:9 비율)
- **Main 페이지**: CSS 변수 기반 스케일링 (1440px 너비 기준)

## 핵심 원리

### 1. 기본 디자인 크기
- **기준 너비**: 1440px
- **기준 높이**: 페이지마다 다름
  - Intro 페이지: 810px (16:9 비율)
  - Main 페이지: 페이지마다 다름 (예: 4412px, 3937px 등)
- 모든 요소의 위치와 크기는 이 기준에 맞춰 설계됨

---

## Intro 페이지 반응형 시스템

### 1. 컨테이너 구조

Intro 페이지는 **vh 기반 스케일링**을 사용하며, 16:9 비율을 유지합니다:

```html
<div class="bg-desktop relative overflow-hidden">
    <!-- 내용 -->
</div>
```

### 2. 컨테이너 동작 원리

`intro-base.css`의 `.bg-desktop` 클래스가 자동으로 화면 비율에 맞춰 크기를 조정합니다:

```css
/* 16:9 비율 유지 */
.bg-desktop {
    max-width: min(100vw, calc(100vh * 16 / 9));
    max-height: min(100vh, calc(100vw * 9 / 16));
}

/* 가로가 긴 화면 (16:9 이상) */
@media (min-aspect-ratio: 16/9) {
    .bg-desktop {
        height: 100vh;
        width: calc(100vh * 16 / 9);
    }
}

/* 세로가 긴 화면 (16:9 미만) */
@media (max-aspect-ratio: 16/9) {
    .bg-desktop {
        width: 100vw;
        height: calc(100vw * 9 / 16);
    }
}
```

### 3. 요소 배치 공식 (Intro 페이지)

Intro 페이지는 **vh와 % 단위**를 사용합니다:

```css
/* 위치 - vh 단위 사용 */
top: 14.32vh;        /* 화면 높이의 14.32% */
left: 3.06%;         /* 컨테이너 너비의 3.06% */

/* 크기 - vh 또는 % 단위 사용 */
height: 5.68vh;      /* 화면 높이의 5.68% */
width: 6.88%;        /* 컨테이너 너비의 6.88% */

/* 폰트 크기 - vw 단위 사용 */
font-size: 1.67vw;   /* 화면 너비의 1.67% */
```

### 4. Intro 페이지 구현 예시

```html
<!-- Navigation Logo -->
<div class="h-[5.68vh] w-[6.88%] relative shrink-0 overflow-hidden cursor-pointer">
    <img src="..." alt="Logo" class="absolute inset-0 w-full h-full object-cover">
</div>

<!-- Main Title -->
<div class="absolute h-[32.59vh] w-[60.83%] left-[3.06%] top-[calc(50%-0.99vh)]">
    <img src="..." alt="Title" class="absolute inset-0 w-full h-full object-cover">
</div>

<!-- Button -->
<a href="..." class="absolute h-[6.42vh] w-[9.86%] left-[28.61%] top-[63.46%]">
    <span class="font-semibold text-[1.67vw]">START</span>
</a>
```

### 5. Intro 페이지 필수 파일

- `static/css/intro-base.css`: 컨테이너 스타일 및 기본 설정
- `static/js/cursor-init.js`: 커서 초기화 (공통)
- `static/js/intro-common.js`: 로고 클릭 이벤트 등 공통 기능

모든 Intro 페이지에 포함 필요:
```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/intro-base.css') }}">
<script src="{{ url_for('static', filename='js/cursor-init.js') }}"></script>
<script src="{{ url_for('static', filename='js/intro-common.js') }}"></script>
```

---

## Main 페이지 반응형 시스템

### 1. CSS 변수 시스템

`main-base.js`가 화면 너비를 감지하여 CSS 변수를 설정합니다:

```javascript
// main-base.js에서 자동 설정
container.style.setProperty('--container-width', viewportWidth + 'px');
```

- `--container-width`: 현재 화면 너비 (동적)
- `--scale-ratio`: 스케일 비율 (viewportWidth / 1440)

### 2. 요소 배치 공식 (Main 페이지)

모든 요소의 위치와 크기는 다음 공식을 사용합니다:

```css
/* 위치 (left, top, right, bottom) */
left: calc(원본X좌표 / 1440 * var(--container-width));
top: calc(원본Y좌표 / 1440 * var(--container-width));

/* 크기 (width, height) */
width: calc(원본너비 / 1440 * var(--container-width));
height: calc(원본높이 / 1440 * var(--container-width));

/* 간격 (gap, margin, padding) */
gap: calc(원본간격 / 1440 * var(--container-width));
margin: calc(원본여백 / 1440 * var(--container-width));
padding: calc(원본패딩 / 1440 * var(--container-width));

/* 폰트 크기 */
font-size: calc(원본폰트크기 / 1440 * var(--container-width));

/* 자간, 행간 등 */
letter-spacing: calc(원본자간값 / 1440 * var(--container-width));
```

## 구현 예시

### Intro 페이지 컨테이너 설정

```html
<div class="bg-desktop relative overflow-hidden">
    <!-- 내용 -->
</div>
```

### Intro 페이지 요소 예시

```html
<!-- Logo: 높이 5.68vh, 너비 6.88% -->
<div class="h-[5.68vh] w-[6.88%] relative shrink-0 overflow-hidden">
    <img src="..." alt="Logo" class="absolute inset-0 w-full h-full object-cover">
</div>

<!-- Main Title: 높이 32.59vh, 너비 60.83%, 위치 left=3.06%, top=50% -->
<div class="absolute h-[32.59vh] w-[60.83%] left-[3.06%] top-[calc(50%-0.99vh)]">
    <img src="..." alt="Title" class="absolute inset-0 w-full h-full object-cover">
</div>
```

### Main 페이지 컨테이너 설정

```html
<div class="main-container" style="height: calc(4412 / 1440 * var(--container-width));">
    <!-- 내용 -->
</div>
```

### Main 페이지 절대 위치 요소

```html
<!-- Figma 좌표: (153, 227), 크기: 64pt -->
<div class="absolute" style="left: calc(153 / 1440 * var(--container-width)); 
                              top: calc(227 / 1440 * var(--container-width)); 
                              font-size: calc(64 / 1440 * var(--container-width));">
    텍스트
</div>
```

### Main 페이지 이미지 요소

```html
<!-- Figma 좌표: (817, 190), 크기: 500×500px -->
<div class="absolute" style="left: calc(817 / 1440 * var(--container-width)); 
                              top: calc(190 / 1440 * var(--container-width)); 
                              width: calc(500 / 1440 * var(--container-width)); 
                              height: calc(500 / 1440 * var(--container-width));">
    <img src="..." class="w-full h-full object-cover">
</div>
```

### Main 페이지 복합 스타일

```html
<!-- 폰트 크기, 자간, 행간 모두 스케일링 -->
<div style="font-size: calc(24 / 1440 * var(--container-width)); 
            letter-spacing: calc(-0.02 * 24 / 1440 * var(--container-width)); 
            line-height: 1.5;">
    텍스트
</div>
```

## 필수 파일

### Intro 페이지 필수 파일

#### 1. CSS 파일
- `static/css/intro-base.css`: 컨테이너 스타일 및 기본 설정
- 모든 Intro 페이지에 포함 필요:
```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/intro-base.css') }}">
```

#### 2. JavaScript 파일
- `static/js/cursor-init.js`: 커서 초기화 (공통)
- `static/js/intro-common.js`: 로고 클릭 이벤트 등 공통 기능
- 모든 Intro 페이지에 포함 필요:
```html
<script src="{{ url_for('static', filename='js/cursor-init.js') }}"></script>
<script src="{{ url_for('static', filename='js/intro-common.js') }}"></script>
```

### Main 페이지 필수 파일

#### 1. JavaScript 파일
- `static/js/main-base.js`: CSS 변수 설정 및 스케일링 로직
- 모든 Main 페이지에 포함 필요:
```html
<script src="{{ url_for('static', filename='js/main-base.js') }}"></script>
```

#### 2. CSS 파일
- `static/css/main-base.css`: 기본 스타일 및 컨테이너 설정
- 모든 Main 페이지에 포함 필요:
```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/main-base.css') }}">
```

## 개발 체크리스트

### Intro 페이지 체크리스트

새로운 Intro 페이지 요소를 추가할 때 다음을 확인하세요:

- [ ] 컨테이너가 `bg-desktop` 클래스를 사용하는지 확인
- [ ] 위치 값은 `vh` 또는 `%` 단위 사용 (예: `top: 14.32vh`, `left: 3.06%`)
- [ ] 크기 값은 `vh` 또는 `%` 단위 사용 (예: `height: 5.68vh`, `width: 6.88%`)
- [ ] 폰트 크기는 `vw` 단위 사용 (예: `font-size: 1.67vw`)
- [ ] `intro-base.css` 파일이 포함되어 있는지 확인
- [ ] `cursor-init.js`와 `intro-common.js` 파일이 포함되어 있는지 확인

### Main 페이지 체크리스트

새로운 Main 페이지 요소를 추가할 때 다음을 확인하세요:

- [ ] 모든 위치 값 (`left`, `top`, `right`, `bottom`)에 `calc(값 / 1440 * var(--container-width))` 적용
- [ ] 모든 크기 값 (`width`, `height`)에 `calc(값 / 1440 * var(--container-width))` 적용
- [ ] 모든 간격 값 (`margin`, `padding`, `gap`)에 `calc(값 / 1440 * var(--container-width))` 적용
- [ ] 폰트 크기 (`font-size`)에 `calc(값 / 1440 * var(--container-width))` 적용
- [ ] 자간 (`letter-spacing`) 계산 시 원본 값에 비율을 곱한 후 스케일링
- [ ] 컨테이너 높이도 `calc(원본높이 / 1440 * var(--container-width))` 형식 사용
- [ ] `main-base.js`와 `main-base.css` 파일이 포함되어 있는지 확인

## 주의사항

### Intro 페이지 주의사항

#### 1. 단위 혼용 금지
```css
/* ❌ 잘못된 예 - px 단위 사용 */
width: 99px;
height: 46px;

/* ✅ 올바른 예 - vh/% 단위 사용 */
width: 6.88%;      /* 컨테이너 너비 기준 */
height: 5.68vh;    /* 화면 높이 기준 */
```

#### 2. 컨테이너 클래스 필수
```html
<!-- ❌ 잘못된 예 -->
<div class="container">

<!-- ✅ 올바른 예 -->
<div class="bg-desktop relative overflow-hidden">
```

#### 3. vh와 %의 차이
- `vh`: 화면 높이 기준 (viewport height)
- `%`: 부모 컨테이너 기준
- Intro 페이지에서는 위치는 주로 `vh`와 `%`를 혼용하여 사용

### Main 페이지 주의사항

#### 1. 절대값 사용 금지
```css
/* ❌ 잘못된 예 */
width: 500px;
font-size: 24px;

/* ✅ 올바른 예 */
width: calc(500 / 1440 * var(--container-width));
font-size: calc(24 / 1440 * var(--container-width));
```

#### 2. 자간(letter-spacing) 계산
자간은 보통 폰트 크기의 비율로 계산됩니다:
```css
/* 원본: font-size 24px, letter-spacing -0.02 (2%) */
font-size: calc(24 / 1440 * var(--container-width));
letter-spacing: calc(-0.02 * 24 / 1440 * var(--container-width));
```

#### 3. 행간(line-height) 처리
행간은 보통 비율(예: 1.5, 1.2)로 유지하거나, 절대값인 경우에만 스케일링:
```css
/* 비율 사용 (권장) */
line-height: 1.5;

/* 절대값인 경우에만 스케일링 */
line-height: calc(36 / 1440 * var(--container-width));
```

#### 4. Tailwind CSS와 함께 사용
Tailwind의 유틸리티 클래스와 함께 인라인 스타일을 사용할 수 있습니다:
```html
<div class="absolute text-white" style="left: calc(153 / 1440 * var(--container-width));">
    내용
</div>
```

## 예시: 완전한 요소 구현

### Intro 페이지 예시

```html
<!-- Logo: 높이 5.68vh, 너비 6.88% -->
<div class="h-[5.68vh] w-[6.88%] relative shrink-0 overflow-hidden cursor-pointer">
    <img src="{{ url_for('static', filename='images/intro/logo.png') }}" 
         alt="Logo" 
         class="absolute inset-0 w-full h-full object-cover max-w-none pointer-events-none">
</div>

<!-- Button: 높이 6.42vh, 너비 9.86%, 위치 left=28.61%, top=63.46% -->
<a href="{{ url_for('intro2') }}" 
   class="absolute bg-[#faf] flex items-center justify-center h-[6.42vh] w-[9.86%] left-[28.61%] top-[63.46%] cursor-pointer">
    <span class="font-semibold text-[1.67vw] leading-[1.4] text-white text-center">
        START
    </span>
</a>
```

### Main 페이지 예시

```html
<!-- Figma 좌표: (153, 227), 크기: 64pt, 자간: -2% -->
<div class="absolute" 
     style="left: calc(153 / 1440 * var(--container-width)); 
            top: calc(227 / 1440 * var(--container-width)); 
            font-family: 'Inter', sans-serif; 
            font-weight: 700; 
            font-size: calc(64 / 1440 * var(--container-width)); 
            letter-spacing: calc(-0.02 * 64 / 1440 * var(--container-width)); 
            line-height: normal; 
            color: #FFFFFF;">
    제품 이름
</div>
```

## 디버깅 팁

### Intro 페이지 디버깅

1. **컨테이너 크기 확인**: 브라우저 개발자 도구에서 `.bg-desktop` 요소의 실제 크기 확인
2. **비율 확인**: 컨테이너가 항상 16:9 비율을 유지하는지 확인
3. **vh/vw 값 확인**: 요소의 vh/vw 값이 올바르게 계산되는지 확인
4. **반응형 테스트**: 다양한 화면 비율에서 테스트 (16:9, 21:9, 4:3 등)

### Main 페이지 디버깅

1. **브라우저 개발자 도구**에서 `--container-width` 값 확인:
   ```javascript
   getComputedStyle(document.querySelector('.main-container')).getPropertyValue('--container-width')
   ```

2. **요소 크기 확인**: 모든 요소가 예상한 비율로 스케일링되는지 확인

3. **반응형 테스트**: 다양한 화면 크기에서 테스트 (1920px, 1366px, 1024px 등)

## 참고 파일

### Intro 페이지 참고 파일
- `templates/intro/intro1.html`: Intro 페이지 구현 예시
- `templates/intro/intro2.html`: Intro 페이지 구현 예시
- `static/css/intro-base.css`: Intro 페이지 기본 스타일
- `static/js/cursor-init.js`: 커서 초기화 로직
- `static/js/intro-common.js`: Intro 페이지 공통 기능

### Main 페이지 참고 파일
- `templates/main/home.html`: Home 페이지 구현 예시
- `templates/main/shop.html`: Shop 페이지 구현 예시
- `templates/main/cart.html`: Cart 페이지 구현 예시
- `templates/product/product.html`: Product 페이지 공통 템플릿 구현 예시 (모든 상품 페이지 공통 사용)
- `templates/product/product1.html`: Product 페이지 구현 예시 (호환성 유지)
- `static/js/main-base.js`: Main 페이지 스케일링 로직
- `static/js/cart.js`: Cart 페이지 기능 (수량 변경, 삭제, 스크롤 위치 관리)
- `static/css/main-base.css`: Main 페이지 기본 스타일

## 페이지별 단위 요약

| 페이지 타입 | 위치 단위 | 크기 단위 | 폰트 단위 | 컨테이너 |
|------------|----------|----------|----------|---------|
| **Intro** | `vh`, `%` | `vh`, `%` | `vw` | `.bg-desktop` |
| **Main** | `calc(...)` | `calc(...)` | `calc(...)` | `.main-container` |
| **Product** | `calc(...)` | `calc(...)` | `calc(...)` | `.main-container` |
| **Cart** | `calc(...)` | `calc(...)` | `calc(...)` | `.main-container` |

**참고**: Product 페이지와 Cart 페이지는 Main 페이지와 동일한 반응형 시스템을 사용합니다.

## 공통 요소 위치 정보

### Main 페이지 로고 위치
모든 Main 페이지 (Home, Shop, Cart, Product)에서 로고는 다음 위치에 배치됩니다:
- **위치**: `left: calc(28 / 1440 * var(--container-width))`, `top: calc(70 / 1440 * var(--container-width))`
- **크기**: `width: calc(99 / 1440 * var(--container-width))`, `height: calc(46 / 1440 * var(--container-width))`
- **스타일**: 절대 위치 (`absolute`), 모든 Main 페이지에서 동일하게 적용

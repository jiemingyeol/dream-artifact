## Dream Store

Dream Store는 사용자의 문장을 가상 화폐(토큰)로 교환하고, 그 토큰으로 상징적인 상품을 고르는 실험적인 웹 스토어 프로젝트입니다.

현재 프로젝트는 **기본 기능 구현 완료** 상태입니다. Intro 페이지(소개 및 사용자 입력), 데이터베이스 시스템, Main 페이지(홈, 상점, 장바구니, 영수증), 상품 상세 페이지, 영수증 이미지 생성 기능이 모두 구현되어 있습니다.

---

## 기술 스택

- **Backend**: Flask (Python)
- **Database**: SQLite (고객/주문: `dream_store.db`, 상품 구매수: `dream_store_stats.db`)
- **Frontend**:
  - HTML 템플릿 + Jinja2
  - Tailwind CSS (CDN)
  - 기본 브라우저 커서 사용 (클릭 가능한 요소에 호버 효과)
  - JavaScript (폼 처리, 모달 시스템, 이미지 프리로딩)
- **Image Processing**:
  - Pillow (이미지 생성 및 조작)
  - QRCode (QR 코드 생성)
- **State**: 
  - SQLite 데이터베이스 기반 상태 관리
  - 세션 기반 사용자 데이터 저장

---

## 프로젝트 구조

```text
dream_store/
├─ app.py                 # Flask 앱 엔트리 포인트
├─ database.py            # 데이터베이스 모델 및 함수
├─ memory_scoring.py     # 메모리 텍스트 스코어링 함수 (토큰 계산)
├─ shop_logic.py          # Shop 페이지 상품 선택 로직 (30분 단위 변경, 연결 상품군 처리)
├─ receipt_image_generator.py  # 고객 영수증 이미지 생성 함수
├─ products.json          # 상품 데이터 (JSON 파일)
├─ requirements.txt       # Python 의존성
├─ IMAGE_REQUIREMENTS.md  # 필요한 이미지 목록
├─ RESPONSIVE_DESIGN_GUIDE.md  # 반응형 디자인 가이드
│
├─ templates/
│  ├─ intro/
│  │  ├─ intro1.html        # Intro 페이지 1
│  │  ├─ intro2.html        # Intro 페이지 2
│  │  ├─ intro3.html        # Intro 페이지 3 (토큰 설명)
│  │  ├─ intro4.html        # Intro 페이지 4 (이름 입력)
│  │  ├─ intro5.html        # Intro 페이지 5
│  │  ├─ intro6.html        # Intro 페이지 6
│  │  ├─ intro7.html        # Intro 페이지 7
│  │  ├─ intro8.html        # Intro 페이지 8
│  │  ├─ intro9.html        # Intro 페이지 9
│  │  └─ intro10.html       # Intro 페이지 10
│  ├─ main/
│  │  ├─ home.html          # Home 페이지
│  │  ├─ shop.html          # Shop 페이지
│  │  ├─ cart.html          # Cart 페이지
│  │  └─ receipt.html       # Receipt 페이지
│  ├─ product/
│  │  └─ product.html       # Product 상세 페이지 공통 템플릿 (모든 상품 페이지 공통 사용)
│  └─ admin.html         # Admin 관리 페이지
│
└─ static/
   ├─ css/
   │  ├─ intro-base.css      # Intro 페이지 공통 기본 스타일
   │  └─ main-base.css       # Main 페이지 공통 기본 스타일
   ├─ js/
   │  ├─ intro-common.js      # Intro 페이지 공통 기능 (로고 클릭 등)
   │  ├─ main-base.js         # Main 페이지 스케일링 JavaScript
   │  ├─ product-toggle.js    # Product 페이지 토글 기능 JavaScript
   │  ├─ cart.js              # Cart 페이지 기능 (수량 변경, 삭제, 스크롤 위치 관리)
   │  ├─ modal.js             # 커스텀 모달 시스템 (전체화면 모드 유지, 닫기 버튼 포함)
   │  └─ image-preloader.js   # 이미지 프리로딩 시스템 (페이지 전환 시 이미지 미리 로드)
   ├─ fonts/
   │  ├─ Geist-SemiBold.ttf
   │  ├─ Geist-Medium.ttf
   │  ├─ Geist-Regular.ttf
   │  ├─ Inter_18pt-Bold.ttf
   │  ├─ Inter_18pt-Medium.ttf
   │  ├─ Inter_24pt-Bold.ttf
   │  ├─ Inter_24pt-Regular.ttf
   │  ├─ Inter_24pt-SemiBold.ttf
   │  ├─ Pretendard-Bold.ttf
   │  ├─ Pretendard-SemiBold.ttf
   │  ├─ NotoSansKR-VariableFont_wght.ttf
   │  └─ TiltWarp-Regular-VariableFont_XROT,YROT.ttf
   └─ images/
      ├─ intro/
         │  ├─ logo.png
         │  ├─ Marquee.png
         │  ├─ main-title.png
         │  ├─ next-button.png
         │  ├─ back-button.png
         │  ├─ skip-button.png
         │  ├─ shop-illustration.png
         │  ├─ token-illustration-1.png
         │  ├─ token-illustration-2.png
         │  ├─ pencil-illustration.png
         │  ├─ hourglass-illustration.png
         │  └─ watch-illustration.png
      ├─ main/
         │  ├─ logo.png
         │  ├─ Marquee.png
         │  ├─ home-button.png
         │  ├─ shop-button.png
         │  ├─ cart-button.png
         │  ├─ header.png
         │  ├─ shop-illustration.png
         │  ├─ main-title.png
         │  ├─ large-button-1.png
         │  ├─ large-button-1-hover.png
         │  ├─ large-button-2.png
         │  ├─ large-button-2-hover.png
         │  ├─ large-button-3.png
         │  ├─ large-button-3-hover.png
         │  ├─ cart-illustration.png
         │  ├─ objects.png
         │  ├─ about-text.png
         │  └─ footer.png
      └─ product/
         ├─ arrow-button.png
         ├─ cart-add-button.png
         ├─ count-button-left.png
         ├─ count-button-left-hover.png
         ├─ count-button-middle.png
         ├─ count-button-right.png
         ├─ count-button-right-hover.png
         ├─ icon-star.png
         ├─ icon-1.png
         ├─ icon-2.png
         ├─ icon-3.png
         ├─ icon-4.png
         └─ item/
            ├─ 01-연필.png
            ├─ 02-책갈피.png
            ├─ 03-텀블러.png
            ├─ 04-리모컨.png
            ├─ 05-향초.png
            ├─ 06-우산.png
            ├─ 07-이어폰.png
            ├─ 08-지우개.png
            ├─ 09-슬리퍼.png
            ├─ 10-안경.png
            ├─ 11-베개.png
            ├─ 12-라디오.png
            ├─ 13-손목시계.png
            ├─ 14-메모지.png
            ├─ 15-손거울.png
            ├─ 16-마스크.png
            ├─ 17-빗.png
            ├─ 18-손전등.png
            ├─ 19-담요.png
            ├─ 20-모자.png
            ├─ 21-나침반.png
            ├─ 22-스푼.png
            ├─ 23-향수병.png
            ├─ 24-머리핀.png
            ├─ 25-열쇠고리.png
            ├─ 26-칫솔.png
            ├─ 27-안대.png
            ├─ 28-손수건.png
            ├─ 29-지갑.png
            └─ 30-전등.png
```

---

## 실행 방법

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

또는 가상 환경 사용 시:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. 애플리케이션 실행

```bash
python app.py
```

기본적으로 `http://127.0.0.1:5001/` 에서 접속할 수 있습니다. (포트 5001 사용, macOS AirPlay 충돌 방지)

---

## 주요 기능

### Intro 페이지

현재 구현된 Intro 페이지들은 다음과 같은 흐름으로 구성되어 있습니다:

- **URL 패턴**: `/intro1` ~ `/intro10`
- 각 페이지는 독립적인 HTML 템플릿으로 구성
- Tailwind CSS를 사용한 반응형 디자인
- 커스텀 커서 및 폰트 적용
- **공통 요소**:
  - Logo: 절대 위치 (28, 60), 크기: 99×46px (vh 기반 스케일링)
    - 클릭 시 확인 팝업 표시 후 intro1 페이지로 이동
  - **Next 버튼**: intro-common.js에서 호버 시 `next-button-hover.png`로 이미지 변경 (intro2~9)
  - **Skip 버튼**: intro-common.js에서 호버 시 `skip-button-hover.png`로 이미지 변경 (intro6, intro7)
- **intro1**: START 버튼 (배경 #ffaaff, 텍스트 흰색) — 호버 시 배경/텍스트 색 교환 (배경 흰색, 텍스트 #ffaaff)
- **intro2**: "다음 페이지로 가려면 클릭!" 텍스트 (우측 여백 114, 아래 여백 43, Geist Semibold 16pt 기준 반응형 `clamp(10pt, 1.48vw, 20pt)`, 흰색, 우측 정렬), 점멸 효과 (0.8s 주기)
- **intro3**: 드림 토큰 설명 페이지
- **intro4**: 사용자 이름 입력 페이지 (DB 저장, 5자 이내 제한)
- **intro5**: 첫 번째 기억 입력 페이지 (DB의 text1 컬럼에 저장, 200자 제한)
- **intro6**: 두 번째 기억 입력 페이지 (DB의 text2 컬럼에 저장, 200자 제한, skip 버튼 지원, skip 시 확인 팝업 표시)
- **intro7**: 세 번째 기억 입력 페이지 (DB의 text3 컬럼에 저장, 200자 제한, skip 버튼 지원, skip 시 확인 팝업 표시)
- **intro8**: 기억 입력 확인 페이지
  - 한 번 입력 완료한 기억은 수정/삭제 불가 안내 메시지 표시
  - back-button으로 intro5로 이동 가능
  - next 버튼 클릭 시:
    - 확인 팝업 표시: 제목 "[알림]", 메시지 "이대로 진행하시겠습니까?\n한 번 입력 완료한 기억은 수정하거나 삭제할 수 없습니다.", 확인/취소 버튼
    - 확인 버튼 클릭 시:
      - 로딩 아이콘 표시 (3초)
      - database에서 text1, text2, text3 가져오기 (없거나 '-'인 경우 제외)
      - 각 텍스트에 대해 메모리 스코어링 함수로 0-100점 평가
      - 입력 개수에 따라 최종 점수 계산:
        - 3개 입력: 평균값
        - 2개 입력: 합 × 1.4 / 3.0
        - 1개 입력: 점수 × 2.0 / 3.0
      - 점수를 반올림하여 정수로 변환 후 × 1000하여 토큰 계산 (최대 100,000)
      - 계산된 토큰을 database에 저장하고 intro9로 이동
- **intro9**: 토큰 교환 완료 페이지 (사용자 이름과 교환된 토큰 수 표시)
- **intro10**: 심호흡 안내 페이지 ("3, 2, 1" 카운트다운 후 알림 팝업 표시, 확인 시 home으로 이동)
  - "3, 2, 1" 텍스트: 처음 숨김 → 3.2초 후부터 1.2초 간격으로 "3,", " 2,", " 1" 순서대로 0.5초 페이드인
  - 알림 팝업: "1" 페이드인 종료(6.1초) 후 0.5초 대기 → 6.6초에 제목 "[알림]", 메시지 "드림 아티팩트 상점에 접속합니다." 표시
  - 확인 버튼 클릭 시 home 페이지로 이동

### 데이터베이스 시스템

- **SQLite 데이터베이스** 2개 사용
  - **`dream_store.db`**: 고객/주문 데이터
  - **`dream_store_stats.db`**: 상품별 구매수 통계 (id, name, type, purchase_count, 기본값 0)
- **JSON 파일** 사용: 상품 마스터 데이터 (`products.json`, `purchase_count` 제외)

#### 고객 데이터 구조 (dream_store.db)
- `id`: 고객 번호 (001, 002, ... 세 자리 텍스트)
- `name`: 고객 이름
- `text1`, `text2`, `text3`: 사연 텍스트
- `token`: 보유 토큰 수
- `buy`: 구매한 물건 번호
- `price`: 구매 가격
- `timestamp`: 생성 일시

#### 상품 구매수 통계 (dream_store_stats.db, `product_stats` 테이블)
- `id`: 상품 번호 (01~30)
- `name`, `type`: 상품 이름·종류 (products.json과 동기화)
- `purchase_count`: 누적 구매 개수 (기본 0, 결제 시 증가)
- 앱 시작 시 `init_product_stats()`로 테이블 생성 및 모든 상품 행 생성(purchase_count=0), 이후 결제 시에만 업데이트

#### 상품 데이터 구조 (JSON, products.json)
- `id`, `name`, `type`, `subtitle`, `description`, `guide`, `ingredients`, `price`, `image_path`, `image_name` (purchase_count는 DB에서 관리)

**상품 관리 함수** (`database.py`):
- `get_products()`: 모든 상품 목록 가져오기 (JSON)
- `get_product_by_id(product_id)`: 특정 상품 정보 가져오기 (purchase_count는 dream_store_stats.db에서 조회)
- `get_product_purchase_count(product_id)`: dream_store_stats.db에서 해당 상품의 purchase_count만 조회
- `add_product(product_data)`, `update_product(product_id, product_data)`, `delete_product(product_id)`: 상품 CRUD 및 stats 동기화
- `save_products(products)`: 상품 목록을 JSON 파일에 저장

**상품 구매수 함수** (`database.py`, dream_store_stats.db):
- `init_product_stats()`: product_stats 테이블 생성·동기화 (모든 상품 행, purchase_count=0)
- `get_product_stats()`: 상품별 구매수 목록 조회
- `add_product_purchase_count(product_id, amount)`: 결제 시 구매수 누적
- `clear_product_stats()`: 모든 상품의 purchase_count를 0으로 초기화

**고객 데이터 관리 함수** (`database.py`):
- `update_customer_buy(customer_id, buy_data)`: 고객의 buy 컬럼 업데이트 (장바구니 데이터 저장)

**메모리 스코어링 함수** (`memory_scoring.py`):
- `score_memory(text: str) -> int`: 메모리 텍스트의 점수를 계산합니다 (0-100점 만점)
  - 평가 기준: 길이, 어휘 다양성, 구체성/평가성, 문장 구조, 감정 강도, 편법 입력 감점
  - intro8에서 각 기억 텍스트(text1, text2, text3)의 품질을 평가하여 토큰을 계산하는 데 사용됩니다

### Main 페이지

현재 구현된 Main 페이지들은 다음과 같은 공통 요소로 구성되어 있습니다:

- **URL 패턴**: `/home`, `/shop`, `/cart`
- 각 페이지는 독립적인 HTML 템플릿으로 구성
- Tailwind CSS를 사용한 반응형 디자인
- 1440px 기준 디자인을 화면 크기에 맞춰 상대 비율로 스케일링
  - **공통 요소**:
    - 상단 Marquee: 이미지 기반 (`marquee.png`)
    - Logo: 절대 위치 (28, 70), 크기 99×46px (모든 Main 페이지 공통)
      - 클릭 시 확인 팝업 표시 후 intro1 페이지로 이동
    - Token: 절대 위치 (144, 70), "보유토큰: {토큰값}" 표시 (Geist-SemiBold, 데이터베이스에서 가져온 실제 토큰 값, 1000-100000 범위)
    - Navigation: 우측 네비게이션 버튼 3개 (Home, Shop, Cart)
    - 하단 Footer: 각 페이지 하단에 footer 이미지
- **프레임 크기**:
  - Home: 1440x4412px 기준
  - Shop: 1440x3937px 기준
  - Cart: 동적 크기 (추후 개발 예정)
- 스크롤 가능한 페이지 구조
- **Navigation 버튼 라우팅**:
  - Home 페이지: Home 버튼 비활성화, Shop/Cart 버튼 활성화
  - Shop 페이지: Shop 버튼 비활성화, Home/Cart 버튼 활성화
  - Cart 페이지: Cart 버튼 비활성화, Home/Shop 버튼 활성화

#### Home 페이지 콘텐츠

- Header 이미지
- Shop Illustration (3D 일러스트)
- Main Title 이미지
- Sub Text (영어/한국어 설명 텍스트)
- Large Button 1, 2, 3 (호버 효과 포함)
- Cart Illustration
- **Shop Now Button**: 배경 #FFAAFF, 텍스트 흰색 — 호버 시 배경 #E6FE98, 텍스트 #000000 (Shop 페이지로 이동)
- Objects 이미지
- About Text 이미지

#### Shop 페이지 콘텐츠

- Main Title 2 이미지 (위치: 98, 162, 크기: 1250x387)
- **Text Group 이미지** (`text-group.png`): 크기 703×63, 그리드 첫 줄 이미지 상단에서 100px 위, 접속 시 0.6s 페이드인
- **동적 상품 그리드** (4행 3열, 총 12개 상품)
  - **30분 단위 상품 변경**: 정시와 정시 30분 기준으로 상품 세트가 변경됨
    - 예: 4:00~4:29 접속 시 같은 상품 세트, 4:30~4:59 접속 시 다른 상품 세트
    - 같은 30분 구간 내에서는 모든 사용자가 동일한 상품을 봄
  - **연결 상품군 로직**: 특정 상품(A)이 선택되면 연결된 상품(B)도 반드시 포함
    - 연결 관계: 연필→라디오, 향초→슬리퍼, 스푼→지갑, 손전등/모자/나침반→리모컨, 지우개/향수병/마스크→텀블러, 칫솔/손수건/전등→열쇠고리
    - **항상 12개 유지**: 연결 상품 추가로 12개를 초과하면 연결 관계가 없는 상품을 자동으로 제거하여 항상 정확히 12개만 표시
  - 각 상품 카드: 362x362px 흰색 둥근 사각형 (모서리 반경 30px)
  - 그리드 레이아웃:
    - 좌측 여백: 125px
    - 우측 여백: 125px
    - 열 간격: 52px (균등 분배)
    - 행 간격: 49px (텍스트 영역 하단 기준)
  - 텍스트 영역: 366x29px (이미지 하단 32px 아래)
    - 상품 이름: Inter Semibold 24pt, 좌측 정렬, 행간 120%, 자간 -2%, 흰색
    - 상품 금액: Inter Medium 18pt, 우측 정렬, 행간 145%, 자간 -0.5%, 흰색
  - 각 상품 아이템은 클래스로 그룹화되어 있음 (`product-item`, `product-image`, `product-text`, `product-name`, `product-price`)
  - 상품 클릭 시 해당 상품의 상세 페이지(`/product<product_id>`)로 이동
- Objects 이미지
- About Text 이미지
- Footer

#### Cart 페이지 콘텐츠

- **URL 패턴**: `/cart`
- **템플릿 구조**: `templates/main/cart.html`
- **프레임 크기**: 동적 높이 (상품 개수에 따라 변경)
  - 기본 높이 (상품 0개): 1360px
  - 상품 n개 (n > 0): 1360 + 204 + 248 * (n - 1)
- **공통 요소**:
  - 상단 Marquee
  - Logo: 절대 위치 (28, 60), 크기: 99×46px
    - 클릭 시 확인 팝업 표시 후 intro1 페이지로 이동
  - Token: 절대 위치 (144, 70), "보유토큰: {토큰값}" 표시
  - Navigation Buttons (Home, Shop, Cart)
  - 하단 Footer
- **페이지 요소**:
  - Cart Title: 위치 (51, 156), Tilt Warp Regular 160pt, 행간 80%, 자간 -5%, 색상 #FFFFFF
  - Text Count: 위치 (163, 407+동적), Geist Regular 20pt, 행간 140%, 자간 0%, 색상 #FFFFFF, "총 주문 상품 {n}개" 표시
  - Token Rectangle: 위치 (163, 514+동적), 크기 300×61px, 모서리 반경 159px, 색상 #FFFFFF, 클래스 `token-rectangle`
  - Text Token: 위치 (163, 529+동적), Inter Bold 24pt, 행간 자동, 자간 -2%, 색상 #000000, 중앙 정렬, "보유토큰: {token}원" 표시 (데이터베이스에서 토큰 값 가져와서 천 단위 콤마 포맷팅)
  - Order Button: 위치 (1120, 514+동적), 크기 134×48px, 호버 시 `order-button-hover.png`로 이미지 변경
  - Text Total: 위치 (892, 514+동적), Inter Bold 40pt, 행간 자동, 자간 -2%, 색상 #FFFFFF, 전체 가격 표시
- **상품 아이템** (n개):
  - 컨테이너: 위치 (157.5, 377.5+248*n), 크기 1104×200px, 검은색 배경, 1px 하얀색 테두리, 모서리 반경 15px
  - 상품 이미지: 위치 (178, 398+248*n), 크기 162×162px, 모서리 반경 6px, 클래스 `product_image_{n}`
  - 상품 이름: 위치 (379, 428+248*n), Inter Semibold 24pt, 행간 120%, 자간 -2%, 색상 #FFFFFF, 클래스 `product_name_{n}`
  - 상품 부제목: 위치 (379, 488+248*n), Geist Medium 14pt, 행간 자동, 자간 0%, 색상 #FFFFFF, 클래스 `product_subtitle_{n}`
  - 수량 조절 버튼: 위치 (796, 457+248*n), Inter Regular 26pt, 행간 자동, 자간 -2%
    - "-" 버튼: 클래스 `cart-decrease-btn`, 수량 1일 때 색상 #C7C7C7, 클릭 불가
    - 구매 개수: 위치 (850, 457+248*n), 현재 수량 표시
    - "+" 버튼: 위치 (905, 457+248*n), 클래스 `cart-increase-btn`
    - hover 효과: 색상 #C7C7C7로 변경
  - 상품 가격: 위치 (1017, 459+248*n), Geist Medium 20pt, 행간 자동, 자간 0%, 색상 #FFFFFF, "{price*num}원" 형식
  - 삭제 버튼: 위치 (1174.5, 451.5+248*n), 크기 45×36px, 클래스 `cart-delete-btn`, hover 효과 (brightness 1.3, saturate 1.1)
- **동적 위치 계산**:
  - 모든 요소의 y 위치는 상품 개수에 따라 동적으로 계산됨
  - 첫 번째 상품: 기본 위치
  - 두 번째 상품부터: 248px씩 아래로 이동
- **기능**:
  - 수량 증가/감소: "-", "+" 버튼 클릭 시 `/api/update-cart-quantity` API 호출
  - 수량 제한: 최소 1개 이상 유지 (수량 1일 때 "-" 버튼 비활성화)
  - 상품 삭제: trash 버튼 클릭 시 확인 모달 표시 후 `/api/delete-cart-item` API 호출
  - 스크롤 위치 유지: 수량 변경/삭제 후 페이지 새로고침 시 이전 스크롤 위치 자동 복원
  - 전체 가격 자동 계산: 모든 상품의 `price * count` 합산
  - **주문하기 기능**: Order Button 클릭 시 조건별 처리
    - 보유 토큰 부족: "[드림 토큰 부족]" 모달 표시, "보유한 드림 토큰을 초과하여 제품을 담았습니다. 장바구니에서 금액을 확인하신 후 다시 시도해 주세요." 메시지 (Inter Regular 16pt), 확인 버튼만 표시 (영수증 페이지로 이동하지 않음)
    - 구매 가능 개수 초과 (5개 초과): "[구매 가능 개수 초과]" 모달 표시, "구매 가능한 제품의 개수를 초과하여 담았습니다. 장바구니를 다시 확인하신 후 다시 시도해 주세요." 메시지 (Inter Regular 16pt), 확인 버튼만 표시 (영수증 페이지로 이동하지 않음)
    - 물건 없음: "[제품 개수 부족]" 모달 표시, "물건을 아예 안 담으셨군요! 쇼핑을 해서 장바구니에 물건을 담아주세요!" 메시지 (Inter Regular 16pt), 확인 버튼만 표시 (영수증 페이지로 이동하지 않음)
    - 정상 케이스: "[주문 가능]" 모달 표시, "물건을 모두 고르셨다면 아래의 주문 버튼을 눌러주세요." 메시지 (Inter Regular 16pt), 취소/주문 버튼 표시
    - 주문 버튼 클릭 시: `POST /api/checkout` 호출로 장바구니 상품별 구매수(dream_store_stats.db) 누적 → 모달 내부 로딩 아이콘 표시 → 5초 후 receipt 페이지로 이동
    - 로딩 중 클릭 및 스크롤 차단 (body에 `loading-active` 클래스 추가하여 overflow: hidden, position: fixed 적용)
- **JavaScript 파일**:
  - `static/js/cart.js`: Cart 페이지 전용 기능 (수량 변경, 삭제, 스크롤 위치 관리, 주문하기 기능)

#### Receipt 페이지 콘텐츠

- **URL 패턴**: `/receipt`
- **템플릿 구조**: `templates/main/receipt.html`
- **프레임 크기**: 1440×2508px 기준 (반응형 스케일링)
- **공통 요소**:
  - 상단 Marquee
  - Logo: 절대 위치 (28, 60), 크기: 99×46px
    - 클릭 시 확인 팝업 표시 후 intro1 페이지로 이동
  - 하단 Footer
  - **네비게이션 버튼 없음**: Home, Shop, Cart 버튼 제거 (영수증 페이지 전용)
- **페이지 요소**:
  - Iron Background: 위치 (85, 155), 크기 1272×694px
  - Big Logo: 위치 (0, 884), 크기 1440×196px
  - 검은색 사각형: 위치 (148, 383), 크기 1147×403px, 모서리 반경 45px, 그림자 효과 (Y 9px, 흐림 4px, #000000 25%)
  - URL 텍스트들: 위치 (159, 796), (1091, 796), Geist Semibold 20pt, 행간 140%, 자간 -2%, 색상 #909090
  - 메인 텍스트: 위치 (202, 401), Geist Semibold 32pt, 행간 140%, 자간 -2%, 색상 #2D2D2D, 불투명도 68%
  - Receipt Illustration: 위치 (444, 169), 크기 551×809px
  - Barcode: 위치 (545, 892), 크기 343×34px
  - Background Logo 1-4: 각각 다른 위치와 크기, background-logo1~4.png 사용
    - Background Logo 1: 위치 (110, 279), 크기 241.03×87.48px
    - Background Logo 2: 위치 (181.13, 317.8), 크기 219.79×98.36px
    - Background Logo 3: 위치 (1232, 213), 크기 177.39×95.45px
    - Background Logo 4: 위치 (926, 658), 크기 136.22×47.12px, 시계방향 19.71도 회전
  - Basket Illustration 1-2: 각각 다른 위치와 크기
    - Basket Illustration 1: 위치 (255, 440), 크기 270×285px
    - Basket Illustration 2: 위치 (910, 383), 크기 199×177px, 반시계방향 150도 회전
  - Bear Illustration: 위치 (826.89, 759.93), 크기 268.83×343.66px, 시계방향 15도 회전
  - 선 4개: 위치 (552, 416), (552, 497), (552, 868), (552, 817), 길이 336px, 검은색, 굵기 0.5px (마지막 선은 점선, 굵기 1px)
  - Objects: bottom 기준 914px 떨어진 위치, 크기 1440×390px
  - About Text: bottom 기준 534px 떨어진 위치, 크기 1280×380px
- **영수증 내용** (최대 5개 상품):
  - 상품 이미지: y 위치 429 고정, x 위치는 개수에 따라 균등 분배 (1개: 중앙, 2-5개: 공백 균등), 크기 56×56px
  - 상품 이름: 위치 (554, 560+48*n), Inter Bold 13pt, 행간 150%, 자간 0%, 색상 #000000, 형식 "{name} x {count}"
  - 상품 부제목: 위치 (554, 583+48*n), Inter Regular 9pt, 행간 150%, 자간 0%, 색상 #828282, name보다 23px 아래
  - 상품 가격: 위치 (839, 560+48*n), Inter Semibold 11pt, 행간 150%, 자간 0%, 색상 #000000, 형식 "{total_price}원" (개수가 여러 개면 총 가격)
  - 영수증 헤더: "ITEM" (554, 523), "PRICE" (844, 523), Inter Extrabold 12pt
  - 총 가격: 위치 (831, 834), Inter Bold 12pt, 형식 "{total_price}원"
  - **영수증 이미지 생성**: `receipt_image_generator.py`를 통해 고객별 영수증 이미지 생성
    - 생성된 이미지는 QR 코드를 통해 모바일에서 확인 가능
- **기능**:
  - 구매한 상품 정보 표시 (최대 5개)
  - 상품 이미지, 이름, 부제목, 가격 표시
  - 전체 가격 표시
  - **QR 코드 표시**: 위치 (1054, 186), 크기 120×120px
    - QR 코드를 스캔하면 영수증 이미지 URL로 이동하여 모바일에서 확인
    - 로컬 개발 환경: 로컬 IP 주소 사용
    - Render 배포 환경: 동적 이미지 생성 (데이터베이스에서 최신 고객 정보 읽어서 생성)
- **영수증 이미지 생성** (`receipt_image_generator.py`):
  - 고객별 영수증 이미지 생성 함수
  - **템플릿 기반 생성**: `static/images/main/result_template.png`를 기본 템플릿으로 사용
  - **이미지 크기**: 1080×1920px (9:16 비율, JPEG 형식, quality 85)
  - **서빙**: 메모리에서 동적 생성 (파일 저장 없음, 로컬/배포 공통)
  - **한글 폰트 지원**: 
    - Pretendard 폰트 우선 사용 (Bold: 상품 이름, SemiBold: 부제목/가격)
    - Fallback: Noto Sans KR → AppleGothic
  - **영수증 요소 배치**:
    - 상품 이미지: y=559.14, x는 상품 개수에 따라 동적 배치 (최대 5개)
    - 상품 이름: 위치 (339.18, 711.65부터), Pretendard Bold 14pt, 검은색, 볼드 처리
    - 상품 부제목: 상품 이름 아래 26.8px, Pretendard SemiBold (스케일링), 회색 (#828282)
    - 상품 가격: x=678 (왼쪽 끝), y=712부터 58 간격, Geist SemiBold (스케일링)
    - 토큰 유닛 이미지: 크기 13×13px, 첫 번째 (659, 714), 58 간격으로 배치
    - 전체 가격: 위치 (678, 1030.5), Geist SemiBold (스케일링)
    - 전체 가격 토큰 유닛: 위치 (659, 1033), 크기 13×13px
    - TOTAL 텍스트: 삭제됨
    - 선 4개: 모두 삭제됨
- **JavaScript 파일**:
  - `static/js/modal.js`: 커스텀 모달 시스템 (확장된 기능: 제목/메시지 분리, 취소 버튼 지원)

#### Product 페이지 콘텐츠

- **URL 패턴**: 
  - 동적 라우팅: `/product<product_id>` (예: `/product01`, `/product02`, `/product30`)
  - 호환성 유지: `/product1`, `/product2`, `/product3` ~ `/product30` (모두 공통 템플릿 사용)
- **템플릿 구조**: 
  - 공통 템플릿: `templates/product/product.html` (모든 상품 페이지 공통 사용)
  - 공통 함수: `get_product_page_data(product_id)` (데이터 처리 로직 통합)
- **프레임 크기**: 1440×4550px 기준 (토글 기능으로 동적 조정 가능, 기본 높이 348px 감소)
- **공통 요소**:
  - 상단 Marquee
  - Logo: 절대 위치 (28, 70), 크기: 99×46px
    - 클릭 시 확인 팝업 표시 후 intro1 페이지로 이동
  - Token: 절대 위치 (144, 70), "보유토큰: {토큰값}" 표시
  - Navigation Buttons (Home, Shop, Cart)
  - 하단 Footer
- **제품 정보 표시**:
  - Arrow Button: 위치 (70, 167), 클릭 영역 확대 (43×43px, padding 10px), 클릭 시 Shop 페이지로 이동
  - Name: 위치 (153, 227), Inter Bold 64pt, 색상 #FFFFFF, 자간 -2%
  - Subtitle: 위치 (153, 328), Inter Regular 24pt, 색상 #828282, 행간 150%
  - Description: 위치 (153, 364), Inter Medium 20pt, 색상 #FFFFFF, 행간 167%, 자간 0%, 가로 크기 592px 고정, 자동 줄넘김, JSON의 `\n\n`은 한 줄 공백으로 표시
    - **동적 높이 조정**: Description 텍스트 박스의 실제 높이를 측정하여 하위 요소들의 위치를 자동 조정
    - 제품 12번(온에어)을 기준으로 설정 (description 높이 835.0px, price y 위치 1100px)
    - Description 높이가 낮으면 요소들이 위로, 높으면 아래로 자동 이동
    - 모든 조정된 요소들을 추가로 150픽셀 아래로 이동
  - Product Image: 위치 (817, 250), 크기 500×500px, 모서리 반경 35px
  - Price: 위치 (153, 1050), Inter Bold 40pt, 색상 #FFFFFF, 자간 -2%, 끝에 "원" 표시 (제품 12번 기준: 1100px, 동적 조정됨)
- **리뷰 및 평가** (Description 높이에 따라 동적 조정됨):
  - Icon Star: 위치 (358, 1062), 크기 132×24px (제품 12번 기준, 동적 조정됨)
  - Text Review: 위치 (503, 1063), Inter Bold 20pt, 색상 #FFFFFF, 행간 자동, 자간 -2%, 형식 "5.0 (N)" (N은 dream_store_stats.db의 product_stats.purchase_count) (제품 12번 기준, 동적 조정됨)
- **구매 관련 요소** (Description 높이에 따라 동적 조정됨):
  - Cart Add Button: 위치 (365, 1127), 크기 144×60px, 호버 시 `cart-add-button-hover.png`로 이미지 변경, 클릭 시 장바구니에 상품 추가 (제품 12번 기준, 동적 조정됨)
    - **Hover 효과**: hover 시 핑크 계열의 더 밝은 색상으로 변경 (brightness 1.3, saturate 1.1)
  - Count Buttons:
    - Count Button Left: 위치 (153, 1127), 크기 63.32×63px, hover 효과 (count-button-left-hover.png), 클릭 시 수량 감소 (최소 1) (제품 12번 기준, 동적 조정됨)
    - Count Button Middle: 위치 (203, 1127), 크기 90×63px, z-index: 2 (가장 위) (제품 12번 기준, 동적 조정됨)
    - Count Button Right: 위치 (281, 1127), 크기 63.32×63px, hover 효과 (count-button-right-hover.png), 클릭 시 수량 증가 (제품 12번 기준, 동적 조정됨)
  - Count Text:
    - Count Text Left: 위치 (179, 1141), 텍스트 "-", Inter Regular 26pt, 색상 동적 변경 (#7F7F7F: 수량 1일 때, #202125: 수량 >1일 때), 자간 -2% (제품 12번 기준, 동적 조정됨)
    - Count Text Middle: 위치 (241, 1143), 현재 수량 표시 (기본값 1, 페이지 로드 시마다 1로 초기화), Inter Regular 26pt, 색상 #202125, 자간 -2% (제품 12번 기준, 동적 조정됨)
    - Count Text Right: 위치 (300, 1141), 텍스트 "+", Inter Regular 26pt, 색상 #202125, 자간 -2% (제품 12번 기준, 동적 조정됨)
- **Hover 효과**:
  - Count Button Left/Right: hover 시 hover 이미지로 즉시 변경, 버튼과 텍스트 영역 모두에서 hover 상태 유지
  - 커서: count-button과 텍스트 영역에서 hover 커서로 유지
- **제품 상세 설명 섹션** (Description 높이에 따라 동적 조정됨):
  - Notice Main: 위치 (151, 1275), Inter SemiBold 32pt, 색상 #FFFFFF, "제품 상세 설명" (제품 12번 기준, 동적 조정됨)
  - Notice Method 1: 위치 (151, 1384), Inter Regular 24pt, 색상 #FFFFFF, "사용 방법" (제품 12번 기준, 동적 조정됨)
  - Notice Method 2: 위치 (473, 1450), Inter Medium 22pt, 색상 #FFFFFF, 토글1로 숨김 가능 (제품 12번 기준, 동적 조정됨)
  - Icon 1-4: 위치 (223, 1515), (494, 1515), (779, 1515), (1052, 1523), 크기 176×176, 216×216, 204×204, 200×200, 토글1로 숨김 가능 (제품 12번 기준, 동적 조정됨)
  - Text Icon 1-4: 위치 (251, 1737), (517, 1737), (815, 1737), (1063, 1737), Inter Regular 20pt, 색상 #FFFFFF, 토글1로 숨김 가능 (제품 12번 기준, 동적 조정됨)
  - Notice Ingredient: 위치 (151, 1901), Inter Regular 24pt, 색상 #FFFFFF, "[KR] 성분표" (제품 12번 기준, 동적 조정됨)
  - Text Ingredient 1-4: Inter Regular 20pt, 행간 1.5, 자간 0%, 색상 #FFFFFF, 토글2로 숨김 가능 (제품 12번 기준, 동적 조정됨)
    - **동적 x 위치 계산**: 텍스트 길이에 따라 자동으로 x 위치가 계산됨
    - 각 텍스트의 너비를 a, b, c, d라고 할 때:
      - 간격: `l = {1440 - 190*2 - (a+b+c+d)} / 3`
      - Text Ingredient 1: x = 190
      - Text Ingredient 2: x = 190 + a + l
      - Text Ingredient 3: x = 190 + a + l + b + l
      - Text Ingredient 4: x = 1440 - 190 - d
    - y 위치: 2060 (제품 12번 기준, Description 높이에 따라 동적 조정됨)
  - Notice FAQ: 위치 (151, 2288), Inter Regular 24pt, 색상 #FFFFFF, "자주 묻는 질문" (제품 12번 기준, 동적 조정됨)
  - FAQ Text Image: 위치 (151, 2424), 크기 1104×1449px, 토글3으로 숨김 가능 (제품 12번 기준, 동적 조정됨)
  - 구분선 1-4: 위치 (151, 1352), (151, 1860), (151, 2253), (151, 3977), 높이 1px, 색상 #FFFFFF (제품 12번 기준, 동적 조정됨)
  - Toggle Text 1-3: 위치 (1032, 1329), (1032, 1852), (1032, 2236), Inter Regular 40pt, 클릭 시 토글 전환 (제품 12번 기준, 동적 조정됨)
- **동적 위치 조정 시스템**:
  - Description 텍스트 박스의 실제 높이를 페이지 로드 시 측정
  - 제품 12번(온에어)을 기준으로 설정 (description 높이 835.0px, price y 위치 1100px)
  - Description 높이 차이만큼 다음 요소들의 y 위치를 자동 조정:
    - Price, Icon Star, Text Review
    - Cart Add Button, Count Buttons (Left/Middle/Right), Count Text (Left/Middle/Right)
    - 구분선 1-4, Toggle Text 1-3
    - Notice Main, Notice Method 1-2, Notice Ingredient, Notice FAQ
    - Icon 1-4, Text Icon 1-4, Text Ingredient 1-4, FAQ Text Image
  - Description이 낮으면 요소들이 위로, 높으면 아래로 이동
  - 모든 조정된 요소들을 추가로 150픽셀 아래로 이동
  - 조정 대상에서 제외된 요소: Marquee, Logo, Navigation 하위 요소, Arrow, Name, Subtitle, Description, Product Image, Footer
- **토글 기능**:
  - **Toggle Text 1**: 위치 (1032, 1329), Inter Regular 40pt, 클릭 시 "-" ↔ "+" 전환 (제품 12번 기준, 동적 조정됨)
    - 클릭 시: Notice Method 2, Icon 1-4, Text Icon 1-4 숨김/표시
    - 구분선2부터 Footer까지 모든 요소를 408px 위/아래로 이동
    - 컨테이너 높이 408px 감소/증가
  - **Toggle Text 2**: 위치 (1032, 1852), Inter Regular 40pt, 클릭 시 "-" ↔ "+" 전환 (제품 12번 기준, 동적 조정됨)
    - 클릭 시: Text Ingredient 1-4 숨김/표시
    - 구분선3부터 Footer까지 모든 요소를 278px 위/아래로 이동
    - 컨테이너 높이 278px 감소/증가
  - **Toggle Text 3**: 위치 (1032, 2236), Inter Regular 40pt, 클릭 시 "-" ↔ "+" 전환 (제품 12번 기준, 동적 조정됨)
    - 클릭 시: FAQ Text Image 숨김/표시
    - 구분선4부터 Footer까지 모든 요소를 1618px 위/아래로 이동
    - 컨테이너 높이 1618px 감소/증가
  - **토글 애니메이션**:
    - 모든 요소 이동: 500ms 선형 애니메이션
    - 컨테이너 높이 조정: 500ms 선형 애니메이션
    - 숨김/표시 요소: opacity, visibility, max-height 500ms 애니메이션
    - 여러 토글 독립 작동 및 동시 활성화 지원
  - **클릭 범위 확대**: 각 토글 텍스트 주변에 확대된 클릭 영역 (왼쪽 5배, 위아래 2배, 오른쪽 2배)
- **데이터 연동**:
  - products.json의 제품 데이터 사용 (동적 product_id로 조회)
  - 고객 토큰 및 장바구니 개수 표시
  - 제품 ID는 URL 파라미터 또는 라우트에서 동적으로 결정
  - **장바구니 기능**:
  - Cart Add Button 클릭 시 `/api/add-to-cart` API 호출
  - 요청 형식: `{product_id: "01", count: 1}` (JSON)
  - 응답 처리:
    - 성공: 커스텀 모달 팝업 표시
      - 제목: "[알림]"
      - 메시지: "상품이 담겼습니다!"
      - 버튼: "상점으로" (왼쪽, shop으로 이동), "장바구니로" (오른쪽, cart로 이동)
    - 실패 (중복): "이미 장바구니에 있는 상품입니다." 알림 팝업 표시
  - 데이터베이스 저장 형식: `buy` 컬럼에 `"{id}*{count}"` 형식으로 저장 (쉼표로 구분)
  - 중복 체크: 동일한 product_id로 시작하는 항목이 있으면 추가 불가

### Admin 페이지

- **URL**: `/admin`
- **고객 데이터**: dream_store.db 조회 및 관리, 페이지네이션 (20개씩), text1/text2/text3 15자 미리보기 (hover 시 tooltip)
- **상품별 구매수**: dream_store_stats.db의 product_stats 테이블 조회 (id, name, type, purchase_count), 고객 테이블과 동일한 표 양식
- **DB 초기화**: "DB 초기화" 버튼 → 고객 DB(dream_store.db) 초기화
- **상품 구매수 초기화**: "상품 구매수 초기화" 버튼 → 모든 상품의 purchase_count를 0으로 초기화

### 이미지 프리로딩 시스템

- **목적**: 로딩된 이미지부터 바로 보여주고, 한 장씩 위에서부터 채워지는 현상만 방지
- **구현 방식**:
  - 페이지 로드 시 body를 곧바로 표시 (전체 이미지 로딩 완료까지 대기하지 않음)
  - 각 이미지는 완전히 로드된 뒤에만 표시 (한 이미지가 위→아래로 천천히 보이는 현상 방지)
  - 로딩 전 깨진 이미지 아이콘 미표시: `visibility: hidden` → 로드 완료 후 `visibility: visible`
  - 로딩이 먼저 끝난 이미지부터 순서대로 페이드인 (opacity 전환)
- **적용 범위**:
  - 모든 페이지에 적용 (Main, Intro, Product 페이지)
  - 페이지 로드 시 자동 동작
- **JavaScript 파일**: `static/js/image-preloader.js`

### 디자인 특징

- 다크 테마 (배경색: `rgb(15, 14, 14)`, Main 페이지: `#000000`)
- 16:9 비율 유지 (1440x810 기준, Figma 디자인 기반)
- Main 페이지: 1440px 너비 기준 반응형 스케일링 (최대 2560px, 작은 화면은 100vw)
- **기본 브라우저 커서 사용**: 클릭 가능한 요소(버튼, 링크 등)에 `cursor: pointer` 호버 효과 적용
- Geist 폰트 사용 (SemiBold, Medium, Regular - 페이지별 최적화)
- Inter 폰트 사용 (24pt SemiBold, 18pt Medium, 18pt Bold - 상품 그리드 등)
- Pretendard 폰트 사용 (Bold, SemiBold - 영수증 이미지 한글 텍스트용)
- Tailwind CSS 기반 통일된 스타일링
- Figma 디자인 좌표 기반 정확한 레이아웃 (주석으로 관리)
- 페이지 전환 시 커서 위치 유지 (sessionStorage 사용)
- 메인 텍스트 행간(leading) 1.7로 통일
- 로고 클릭 시 초기 화면으로 돌아가는 확인 팝업 기능
- Marquee: 텍스트에서 이미지 기반으로 변경 (intro와 main 모두)
- **커스텀 모달 시스템**: 전체화면 모드에서도 팝업 표시 가능
  - 브라우저 기본 `alert()`, `confirm()` 대신 커스텀 모달 사용
  - 전체화면 모드 유지 (크롬 전체화면에서도 북마크바/주소창 표시 방지)
  - **반응형 디자인**: 모든 요소가 화면 크기에 따라 자동 조정
  - 모달 크기: 1440×810 기준 430×209px (반응형)
  - 모달 배경색: #FFFFFF
  - **닫기 버튼**: 우측 상단 회색 원 + 엑스 표시 (모달 높이의 1/16 크기)
    - 위치: 모달 우측 가장자리에서 반지름만큼 떨어진 위치
    - 색상: #D9D9D9 (프로젝트 회색)
  - 제목: Inter Bold 20pt (반응형), 양 끝에 대괄호 `[제목]` 형식
  - 메시지: Inter Regular 16pt (반응형)
  - 버튼: Inter Regular 15pt (반응형), 크기 70×35px 기본 (텍스트에 따라 자동 조정)
    - 확인 버튼: #FFAAFF 배경, 검은색 텍스트
      - Hover 시: 배경색 #ff88ff
    - 취소 버튼: #D9D9D9 배경, 검은색 텍스트
      - Hover 시: 배경색 #c0c0c0
  - 버튼 순서: 취소(왼쪽), 확인(오른쪽)
  - ESC 키로 닫기 지원
  - **팝업 타입**:
    - `customAlert`: 제목 "[알림]", 메시지 표시, 확인 버튼 1개
    - `customConfirm`: 제목 "[알림]", 메시지 표시, 취소/확인 버튼 2개
    - `customModal`: 커스터마이징 가능한 모달 (제목/메시지 분리, 버튼 텍스트 변경 가능)
  - **메시지 줄 수에 따른 위치 자동 조정**: 한 줄 메시지일 때 메시지 위쪽에 줄 높이(1.4em)만큼 여백을 두어 y 위치를 내림
  - **확장 기능**: 로딩 아이콘 표시 기능 (Cart 페이지 주문하기 기능에서 사용)

### 코드 구조

- **공통 파일 분리**: 중복 코드를 제거하고 재사용 가능한 공통 파일로 분리
  - `static/css/intro-base.css`: 모든 intro 페이지의 기본 스타일 및 `.bg-desktop` 컨테이너 스타일 (기본 커서 호버 효과 포함)
  - `static/js/intro-common.js`: 로고 클릭 이벤트 핸들러, Next/Skip 버튼 호버 시 이미지 변경 (모든 intro 페이지 공통)
  - `static/css/main-base.css`: 모든 main 페이지의 기본 스타일 및 `.main-container` 컨테이너 스타일 (기본 커서 호버 효과 포함)
  - `static/js/main-base.js`: Main 페이지 스케일링 로직 (CSS 변수 설정)
  - `static/js/modal.js`: 커스텀 모달 시스템 (전체화면 모드 유지, 닫기 버튼, 반응형 디자인)
  - `static/js/product-toggle.js`: Product 페이지 토글 기능
  - `static/js/cart.js`: Cart 페이지 기능 (수량 변경, 삭제, 스크롤 위치 관리)
  - `static/js/image-preloader.js`: 이미지 프리로딩 시스템 (페이지 전환 시 다음 페이지 이미지 미리 로드)
  - `shop_logic.py`: Shop 페이지 상품 선택 로직 (30분 단위 변경, 연결 상품군 처리)
  - `receipt_image_generator.py`: 고객 영수증 이미지 생성 함수 (9:16 비율, 1080×1920px, Pretendard 폰트 사용, PIL·sys 사용)
- **템플릿 구조**: 
  - 모든 intro 페이지가 `templates/intro/` 폴더에 정리되어 관리 용이성 향상
  - Product 페이지는 공통 템플릿 `templates/product/product.html` 사용 (동적 라우팅 지원)
  - **API 엔드포인트**:
  - `POST /api/add-to-cart`: 장바구니에 상품 추가 (JSON 요청/응답)
  - `POST /api/update-cart-quantity`: 장바구니 상품 수량 변경 (JSON 요청/응답)
  - `POST /api/delete-cart-item`: 장바구니에서 상품 삭제 (JSON 요청/응답)
  - `POST /api/checkout`: 장바구니 결제 시 상품별 구매수(dream_store_stats.db) 누적 (Cart 주문 버튼 확인 후 호출)
  - `POST /intro8/submit`: 기억 입력 확인 및 토큰 계산 (메모리 스코어링 기반)
    - 요청 형식: `customer_id` (form 데이터)
    - 동작: text1, text2, text3을 가져와 각각 스코어링하여 토큰 계산 후 DB 저장

---

## 향후 개발 계획

다음 기능들이 구현 예정입니다:

- [x] 사용자 이름 입력 기능 (5자 이내 제한)
- [x] SQLite 데이터베이스 연동
- [x] 관리자 페이지
- [x] 사용자 사연 입력 기능 (text1, text2, text3, 각 200자 제한)
- [x] 기억 입력 페이지 편집 기능 (기존 값 수정 가능)
- [x] Skip 버튼 기능 (intro6, intro7에서 기억 입력 건너뛰기)
- [x] Intro8 확인 페이지 및 back-button 라우팅 (이전 페이지로 복귀)
- [x] Intro9 토큰 교환 완료 페이지
- [x] Intro10 심호흡 안내 페이지 (3초 후 알림 팝업 표시, 확인 시 home으로 이동)
- [x] Main 페이지 공통 요소 (Marquee, Navigation, Footer)
- [x] Main 페이지 반응형 스케일링 시스템
- [x] Marquee 이미지 기반으로 변경 (intro와 main 모두)
- [x] Home 페이지 콘텐츠 구현 (Header, Shop Illustration, Main Title, Sub Text, Large Buttons, Cart Illustration, Shop Now Button, Objects, About Text)
- [x] Shop 페이지 토큰 표시 기능 (데이터베이스에서 가져온 실제 토큰 값)
- [x] Navigation 버튼 라우팅 기능 (각 페이지별 활성화/비활성화)
- [x] Shop Now 버튼 라우팅 (Home → Shop)
- [x] 기본 브라우저 커서 사용 (커스텀 커서 제거, 클릭 가능한 요소에 호버 효과 적용)
- [x] 상품 데이터 시스템 구축 (JSON 파일 기반, 30개 상품)
- [x] 상품 관리 함수 구현 (CRUD, 구매 개수 업데이트)
- [x] Shop 페이지 상품 그리드 레이아웃 구현 (4행 3열, 12개 상품 카드)
- [x] Product 페이지 구현 (상품 상세 페이지)
  - [x] 공통 템플릿 리팩토링 (`product.html` - 모든 상품 페이지 공통 사용)
  - [x] 동적 라우팅 구현 (`/product<product_id>` - product01~product30 자동 지원)
  - [x] 공통 함수 구현 (`get_product_page_data()` - 데이터 처리 로직 통합)
  - [x] 공통 요소 (Marquee, Navigation, Footer)
  - [x] 로고 위치 통일 (모든 Main 페이지: 절대 위치 28, 70, 크기 99×46px)
  - [x] 제품 정보 표시 (Arrow, Name, Subtitle, Description, Image, Price)
  - [x] Arrow 버튼 라우팅 (Shop 페이지로 이동)
  - [x] 리뷰 및 평가 표시 (Icon Star, Text Review)
  - [x] 구매 관련 요소 (Cart Add Button, Count Buttons, Count Text)
  - [x] 수량 관리 기능 (current_number 변수, 증가/감소 버튼, 최소값 1)
  - [x] 수량 표시 색상 동적 변경 (Count Text Left: 수량 1일 때 #7F7F7F, >1일 때 #202125)
  - [x] 페이지 로드 시 수량 초기화 (항상 1로 시작)
  - [x] Hover 효과 (Count Button Left/Right hover 이미지 전환)
  - [x] 커서 hover 상태 유지 (버튼 및 텍스트 영역)
  - [x] 제품 상세 설명 섹션 (Notice Main, Notice Method, Icon 1-4, Text Icon 1-4)
  - [x] 성분표 섹션 (Notice Ingredient, Text Ingredient 1-4)
  - [x] FAQ 섹션 (Notice FAQ, FAQ Text Image)
  - [x] 토글 기능 구현 (3개 독립 토글, 선형 애니메이션, 동적 높이 조정)
  - [x] 토글 클릭 범위 확대
  - [x] Product 페이지 기본 높이 조정 (348px 감소)
  - [x] 장바구니 추가 API 구현 (`/api/add-to-cart` - POST 요청)
  - [x] 장바구니 중복 체크 (동일 상품 중복 추가 방지)
  - [x] 장바구니 데이터 저장 형식 (`"{id}*{count}"` 형식, 쉼표로 구분)
  - [x] 커스텀 모달 연동 (장바구니 추가 성공 시 "상점으로"/"장바구니로" 버튼 제공)
  - [x] Intro8 back button 라우팅 변경 (intro5로 이동)
  - [x] Intro6/7 skip 버튼 확인 팝업 추가
  - [x] 커스텀 모달 시스템 구현 (전체화면 모드 유지)
  - [x] 모달 닫기 버튼 추가 (우측 상단 회색 원 + 엑스)
  - [x] 모달 반응형 디자인 적용
  - [x] 모달 버튼 크기 및 폰트 크기 조정
  - [x] 알림/확인 팝업에 "[알림]" 제목 추가
  - [x] 메시지 줄 수에 따른 위치 자동 조정
  - [x] Shop 페이지 동적 상품 표시 (30분 단위 변경, 연결 상품군 처리)
  - [x] Shop 페이지 상품 클릭 시 상세 페이지로 이동
  - [x] Product 페이지 Cart Add Button hover 효과 추가
  - [x] Product 페이지 Arrow Button 클릭 영역 확대
  - [x] Main/Product 페이지 Logo 클릭 시 intro1으로 이동 기능 추가
  - [x] Modal 버튼 hover 윤곽선 제거
  - [x] Token 요소 위치 변경 (144, 70)
  - [x] Intro 페이지 Logo 위치 조정 (위로 10픽셀)
- [x] 메모리 스코어링 시스템 구현
  - [x] 메모리 스코어링 함수 구현 (`memory_scoring.py`)
  - [x] intro8에서 기억 텍스트 품질 평가 및 토큰 계산
  - [x] 입력 개수에 따른 토큰 계산 로직 (1개/2개/3개 입력 시 다른 계산 방식)
  - [x] 토큰을 점수 기반으로 동적 계산 (최대 100,000 토큰)
- [x] Cart 페이지 장바구니 기능 구현
  - [x] Cart 페이지 UI 구현 (제목, 상품 목록, 수량 조절, 가격 표시)
  - [x] 동적 프레임 높이 (상품 개수에 따라 자동 조정)
  - [x] 상품 정보 표시 (이미지, 이름, 부제목, 가격)
  - [x] 수량 조절 기능 (증가/감소 버튼, 최소 1개 제한)
  - [x] 상품 삭제 기능 (확인 모달 포함)
  - [x] 전체 가격 계산 및 표시
  - [x] 수량 변경 API (`/api/update-cart-quantity`)
  - [x] 상품 삭제 API (`/api/delete-cart-item`)
  - [x] 스크롤 위치 유지 기능
  - [x] Hover 효과 (버튼 색상 변경)
  - [x] JavaScript 파일 분리 (`static/js/cart.js`)
- [x] Cart 페이지 주문하기 기능 구현
  - [x] 주문하기 버튼 클릭 이벤트 추가
  - [x] 조건별 모달 표시 (토큰 부족, 개수 초과, 물건 없음, 정상 케이스)
  - [x] 커스텀 모달 시스템 확장 (제목/메시지 분리, 취소 버튼 지원)
  - [x] 로딩 아이콘 구현 (고리 모양, 94×94px, 20%만 FFAAFF 색상으로 회전)
  - [x] 로딩 중 클릭 및 스크롤 차단
  - [x] 5초 후 receipt 페이지로 자동 이동
- [x] Receipt 페이지 구현
  - [x] Receipt 페이지 템플릿 생성 (`templates/main/receipt.html`)
  - [x] Receipt 페이지 라우트 추가 (`/receipt`)
  - [x] 영수증 UI 요소 구현 (배경, 로고, 텍스트, 이미지 등)
  - [x] 구매한 상품 정보 표시 (이미지, 이름, 부제목, 가격, 최대 5개)
  - [x] 전체 가격 표시
  - [x] 로고 클릭 시 초기화면으로 돌아가기 기능
  - [x] 네비게이션 버튼 제거
  - [x] QR 코드 생성 및 표시 (영수증 이미지 URL, 스캔 시 모바일에서 확인)
  - [x] 영수증 이미지 생성 시스템 (`receipt_image_generator.py`)
    - [x] 템플릿 기반 이미지 생성 (result_template.png)
    - [x] 템플릿 리사이즈 (1080×1920px)
    - [x] 상품 이미지 동적 배치 (최대 5개, y=559.14)
    - [x] 상품 이름 배치 (Pretendard Bold, 볼드 처리)
    - [x] 상품 부제목 배치 (Pretendard SemiBold)
    - [x] 상품 가격 배치 (x=678, y=712부터 58 간격)
    - [x] 토큰 유닛 이미지 배치 (13×13px, 첫 번째 (659, 714), 58 간격)
    - [x] 전체 가격 배치 (x=678, y=1030.5)
    - [x] 전체 가격 토큰 유닛 배치 (659, 1033)
    - [x] TOTAL 텍스트 삭제
    - [x] 선 4개 삭제
    - [x] 한글 폰트 지원 (Pretendard → Noto Sans KR → AppleGothic)
    - [x] JPEG 형식 (quality 85, optimize True, 메모리에서 서빙)
  - [x] 영수증 이미지 뷰어 페이지 (`receipt_image_viewer.html`, 모바일 최적화)
  - [x] 동적 이미지 뷰어 라우트 (`/receipt-image-generate/<customer_id>`)
  - [x] 동적 이미지 데이터 라우트 (`/receipt-image-data/<customer_id>`)
- [x] 이미지 프리로딩 시스템 구현
  - [x] body 즉시 표시, 이미지는 로드 완료된 것부터 순서대로 페이드인
  - [x] 단일 이미지 상단→하단 로딩 방지 (완전 로드 후 한 번에 표시)
  - [x] 모든 페이지에 적용 (Main, Intro, Product)
- [x] Shop 페이지 로직 개선
  - [x] 항상 정확히 12개 상품만 표시되도록 수정
  - [x] 연결 상품 추가 시 12개 초과 방지 로직 구현
  - [x] 연결 관계가 없는 상품 자동 제거 기능
  - [x] 페어로 나와야 하는 물건이 등장했을 때 해당 물건 추가 후 페어에 해당 사항 없는 물건을 하나 지워서 12개 유지
- [x] Cart 페이지 UI 개선
  - [x] Text Total의 y 위치를 Order Button과 동일하게 조정
  - [x] Token Rectangle 추가 (위치, 크기, 스타일 조정)
  - [x] Text Token 추가 (보유토큰 표시, 데이터베이스에서 토큰 값 가져와서 천 단위 콤마 포맷팅)
  - [x] 주문하기 기능 모달 메시지 크기 조정 (16pt)
  - [x] 정상 케이스 모달에 취소 버튼 추가
  - [x] 로딩 아이콘을 모달 중앙에 표시하도록 수정
- [x] 영수증 이미지 생성 시스템 구현
  - [x] 템플릿 기반 이미지 생성 (`receipt_image_generator.py`)
  - [x] 템플릿 이미지 로드 및 리사이즈 (1080×1920px)
  - [x] 상품 이미지 동적 배치 (최대 5개, y=559.14)
  - [x] 상품 이름 배치 (Pretendard Bold 14pt, 볼드 처리, 검은색)
  - [x] 상품 부제목 배치 (Pretendard SemiBold, 회색 #828282)
  - [x] 상품 가격 배치 (x=678 왼쪽 끝, y=712부터 58 간격)
  - [x] 토큰 유닛 이미지 배치 (13×13px, 첫 번째 (659, 714), 58 간격)
  - [x] 전체 가격 배치 (x=678, y=1030.5)
  - [x] 전체 가격 토큰 유닛 배치 (659, 1033)
  - [x] TOTAL 텍스트 삭제
  - [x] 선 4개 삭제
  - [x] 한글 폰트 지원 (Pretendard Bold/SemiBold → Noto Sans KR → AppleGothic)
  - [x] JPEG 형식 (quality 85, optimize True, 메모리에서 서빙)
  - [x] 동적 이미지 뷰어/데이터 라우트 (`/receipt-image-generate/`, `/receipt-image-data/`)
- [x] 체크아웃 및 구매 기록 저장
  - [x] Cart 페이지에서 주문하기 기능 구현
  - [x] 구매 조건 검증 (토큰 부족, 개수 초과, 물건 없음)
  - [x] Receipt 페이지로 이동 및 영수증 표시
  - [x] 영수증 이미지 동적 생성 (메모리에서 서빙)

---

## 이미지 리소스

프로젝트에 필요한 이미지 목록은 `IMAGE_REQUIREMENTS.md` 파일을 참고하세요.

현재 포함된 이미지:

**Intro 페이지** (`static/images/intro/`):
- 로고 (`logo.png`)
- 메인 타이틀 (`main-title.png`)
- 상점 일러스트 (`shop-illustration.png`)
- 토큰 일러스트 (`token-illustration-1.png`, `token-illustration-2.png`)
- 연필 일러스트 (`pencil-illustration.png`)
- 모래시계 일러스트 (`hourglass-illustration.png`)
- 시계 일러스트 (`watch-illustration.png`)
- 버튼 이미지 (`next-button.png`, `next-button-hover.png`, `back-button.png`, `skip-button.png`, `skip-button-hover.png`)
- Marquee (`marquee.png`)

**Main 페이지** (`static/images/main/`):
- 로고 (`logo.png`)
- Marquee (`Marquee.png`)
- 네비게이션 버튼 (`home-button.png`, `shop-button.png`, `cart-button.png`)
- Header (`header.png`)
- Shop Illustration (`shop-illustration.png`)
- Main Title (`main-title.png`)
- Main Title 2 (`main-title-2.png`) - Shop 페이지 전용
- Text Group (`text-group.png`) - Shop 페이지 전용 (그리드 상단 100px 위, 703×63, 페이드인)
- Large Buttons (`large-button-1.png`, `large-button-1-hover.png`, `large-button-2.png`, `large-button-2-hover.png`, `large-button-3.png`, `large-button-3-hover.png`)
- Cart Illustration (`cart-illustration.png`)
- Objects (`objects.png`)
- About Text (`about-text.png`)
- Footer (`footer.png`)
- **Receipt 페이지 전용 이미지**:
  - Iron Background (`iron-background.png`)
  - Big Logo (`big-logo.png`)
  - Receipt Illustration (`receipt-illustration.png`)
  - Barcode (`barcode.png`)
  - Background Logo 1-4 (`background-logo1.png`, `background-logo2.png`, `background-logo3.png`, `background-logo4.png`)
  - Basket Illustration 1-2 (`basket-illustration1.png`, `basket-illustration2.png`)
  - Bear Illustration (`bear-illustration.png`)
  - Order Button (`order-button.png`, `order-button-hover.png`)
  - Trash Button (`trash-button.png`)

**상품 이미지** (`static/images/product/item/`):
- 총 30개의 상품 이미지 (파일명 형식: `{id}-{type}.png`)
- 예시: `01-연필.png`, `02-책갈피.png`, `03-텀블러.png`, ... `30-전등.png`

**Product 페이지 UI 요소** (`static/images/product/`):
- Arrow Button (`arrow-button.png`)
- Cart Add Button (`cart-add-button.png`, `cart-add-button-hover.png`)
- Count Buttons (`count-button-left.png`, `count-button-left-hover.png`, `count-button-middle.png`, `count-button-right.png`, `count-button-right-hover.png`)
- Icon Star (`icon-star.png`)
- Icon 1-4 (`icon-1.png`, `icon-2.png`, `icon-3.png`, `icon-4.png`)
- FAQ Text Image (`faq-text.png`)

---

## 개발 환경

- Python 3.9+
- Flask 3.0.0
- SQLite3 (Python 내장)
- Pillow>=10.0.0 (이미지 처리)
- qrcode[pil]>=7.4.0 (QR 코드 생성)

## 토큰 시스템

### 메모리 스코어링 기반 토큰 계산

- 사용자가 기억을 입력하고 intro8에서 확인하면, 입력된 기억 텍스트의 품질을 평가하여 토큰이 계산됩니다.
- **스코어링 함수** (`memory_scoring.py`):
  - 각 기억 텍스트(text1, text2, text3)에 대해 0-100점 만점으로 평가
  - 평가 기준:
    - 기본 점수: 30점
    - 길이 점수: 최대 15점 (150자 이상 만점)
    - 어휘 다양성: 최대 15점
    - 구체성 및 평가성: 최대 15점 (시간, 장소, 인물, 사건 등 구체적 표현)
    - 문장 구조: 최대 15점
    - 감정 강도: 최대 10점
    - 편법 입력 감점: 반복 문자나 단어 중복 시 감점
- **최종 토큰 계산**:
  - 입력된 텍스트 개수에 따라 최종 점수 계산:
    - **3개 입력**: 평균값 사용
    - **2개 입력**: 합 × 1.4 / 3.0
    - **1개 입력**: 점수 × 2.0 / 3.0
  - 계산된 점수를 반올림하여 정수로 변환
  - 정수 점수에 1000을 곱하여 토큰으로 변환 (최대 100,000 토큰)
  - 예: 점수 85점 → 85,000 토큰, 점수 100점 → 100,000 토큰
- Shop 페이지의 Navigation에서 현재 사용자의 보유 토큰을 실시간으로 표시합니다.
- 토큰 값은 데이터베이스의 `token` 컬럼에서 가져오며, 0-100000 범위로 제한됩니다.
- 토큰 표시 형식: "보유토큰: {토큰값}" (Geist-SemiBold 폰트, 행간 140%, 자간 -5%)
- 토큰 값은 천 단위 콤마로 포맷팅되어 표시됩니다 (예: "보유토큰: 85,000")

## 데이터베이스

### 고객 데이터 (dream_store.db)
프로젝트 실행 시 `dream_store.db` 파일이 자동으로 생성됩니다. 이 파일은 `.gitignore`에 포함되어 Git에 업로드되지 않습니다.  
Admin 페이지(`/admin`)에서 "DB 초기화" 버튼으로 고객 DB를 초기화할 수 있습니다.

### 상품 구매수 통계 (dream_store_stats.db)
프로젝트 실행 시 **먼저** `dream_store_stats.db`가 생성·동기화됩니다. `product_stats` 테이블에 products.json 기준으로 모든 상품이 행으로 들어가며, 새 행의 `purchase_count`는 0입니다. Cart에서 결제 시 `POST /api/checkout`으로 해당 주문 상품별 구매수가 누적됩니다.  
Admin 페이지에서 "상품 구매수 초기화" 버튼으로 모든 상품의 purchase_count를 0으로 되돌릴 수 있습니다.  
Render 등 배포 시 영구 디스크를 쓸 경우 `DB_STATS_PATH` 환경 변수로 경로를 지정할 수 있습니다.

### 상품 데이터 (JSON)
상품 정보는 `products.json` 파일에 저장됩니다 (Git 포함). `purchase_count`는 제거되었으며, 구매수는 dream_store_stats.db에서만 관리합니다.

- 총 30개 상품
- 각 상품은 고유한 ID (01~30)와 종류(type)를 가짐
- 이미지 파일명 형식: `{id}-{type}.png` (예: `01-연필.png`)
- 상품 정보 수정은 `products.json` 편집 또는 `database.py`의 add/update/delete_product 사용 (stats DB는 자동 동기화)

---

## 라이선스

이 프로젝트는 실험적인 프로젝트입니다.

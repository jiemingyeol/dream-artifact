import sqlite3
import os
import json
from datetime import datetime

# 데이터베이스 파일 경로 설정
# 환경 변수가 있으면 사용하고, 없으면 현재 스크립트 디렉토리 기준으로 설정
_script_dir = os.path.dirname(os.path.abspath(__file__))
if 'RENDER' in os.environ or 'DATABASE_URL' in os.environ:
    # Render 환경: 영구 스토리지 경로 사용 (또는 환경 변수로 지정된 경로)
    DB_PATH = os.environ.get('DB_PATH', os.path.join(_script_dir, 'dream_store.db'))
    DB_STATS_PATH = os.environ.get('DB_STATS_PATH', os.path.join(_script_dir, 'dream_store_stats.db'))
else:
    # 로컬 환경: 현재 스크립트 디렉토리 기준
    DB_PATH = os.path.join(_script_dir, 'dream_store.db')
    DB_STATS_PATH = os.path.join(_script_dir, 'dream_store_stats.db')

def get_db():
    """고객/주문용 데이터베이스 연결 (dream_store.db)"""
    try:
        db_dir = os.path.dirname(DB_PATH)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        print(f"DB_PATH: {DB_PATH}")
        print(f"Current directory: {os.getcwd()}")
        raise

def get_stats_db():
    """상품 구매수 통계용 데이터베이스 연결 (dream_store_stats.db)"""
    try:
        db_dir = os.path.dirname(DB_STATS_PATH)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
        conn = sqlite3.connect(DB_STATS_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"Stats database connection error: {e}")
        print(f"DB_STATS_PATH: {DB_STATS_PATH}")
        print(f"Current directory: {os.getcwd()}")
        raise

def init_db():
    """데이터베이스 초기화 및 테이블 생성"""
    conn = get_db()
    cursor = conn.cursor()
    
    # 기존 테이블이 있는지 확인
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='customers'")
    table_exists = cursor.fetchone()
    
    if table_exists:
        # 기존 테이블 구조 확인
        cursor.execute("PRAGMA table_info(customers)")
        columns = [row[1] for row in cursor.fetchall()]
        
        # 마이그레이션: no -> id (세 자리 텍스트)
        if 'no' in columns and 'id' not in columns:
            # 기존 데이터 백업 (컬럼명으로 접근)
            cursor.execute('SELECT name, text1, text2, text3, token, buy, timestamp FROM customers ORDER BY no')
            old_data = cursor.fetchall()
            
            # 기존 테이블 이름 변경
            cursor.execute('ALTER TABLE customers RENAME TO customers_old')
            
            # 새 테이블 생성
            cursor.execute('''
                CREATE TABLE customers (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    text1 TEXT,
                    text2 TEXT,
                    text3 TEXT,
                    token INTEGER DEFAULT 0,
                    buy TEXT,
                    price INTEGER,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 데이터 마이그레이션 (no를 세 자리 텍스트 id로 변환)
            for idx, row in enumerate(old_data, start=1):
                customer_id = f"{idx:03d}"
                cursor.execute('''
                    INSERT INTO customers (id, name, text1, text2, text3, token, buy, price, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    customer_id,
                    row[0],  # name
                    row[1],  # text1
                    row[2],  # text2
                    row[3],  # text3
                    row[4] if len(row) > 4 else 0,      # token
                    row[5] if len(row) > 5 else None,   # buy
                    None,  # price (새 컬럼)
                    row[6] if len(row) > 6 else None   # timestamp
                ))
            
            # 기존 테이블 삭제
            cursor.execute('DROP TABLE customers_old')
        else:
            # price 컬럼 추가
            if 'price' not in columns:
                cursor.execute('ALTER TABLE customers ADD COLUMN price INTEGER')
            
            # timestamp 컬럼 추가
            if 'timestamp' not in columns:
                cursor.execute('ALTER TABLE customers ADD COLUMN timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
                cursor.execute('UPDATE customers SET timestamp = CURRENT_TIMESTAMP WHERE timestamp IS NULL')
    else:
        # 새 테이블 생성
        cursor.execute('''
            CREATE TABLE customers (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                text1 TEXT,
                text2 TEXT,
                text3 TEXT,
                token INTEGER DEFAULT 0,
                buy TEXT,
                price INTEGER,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    
    init_product_stats()
    conn.commit()
    conn.close()

def add_customer(name, text1=None, text2=None, text3=None, token=0, buy=None, price=None):
    """고객 데이터 추가"""
    conn = get_db()
    cursor = conn.cursor()
    
    # 다음 ID 생성 (001, 002, ...)
    cursor.execute('SELECT COUNT(*) FROM customers')
    count = cursor.fetchone()[0]
    customer_id = f"{count + 1:03d}"
    
    cursor.execute('''
        INSERT INTO customers (id, name, text1, text2, text3, token, buy, price)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (customer_id, name, text1, text2, text3, token, buy, price))
    
    conn.commit()
    conn.close()
    return customer_id

def get_latest_customer():
    """가장 최근에 추가된 고객 정보 가져오기"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM customers
        ORDER BY timestamp DESC
        LIMIT 1
    ''')
    
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return dict(row)
    return None

def update_customer_text1(customer_id, text1):
    """고객의 text1 컬럼 업데이트"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE customers
        SET text1 = ?
        WHERE id = ?
    ''', (text1, customer_id))
    
    conn.commit()
    conn.close()
    
    return cursor.rowcount > 0

def update_customer_text2(customer_id, text2):
    """고객의 text2 컬럼 업데이트"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE customers
        SET text2 = ?
        WHERE id = ?
    ''', (text2, customer_id))
    
    conn.commit()
    conn.close()
    
    return cursor.rowcount > 0

def update_customer_text3(customer_id, text3):
    """고객의 text3 컬럼 업데이트"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE customers
        SET text3 = ?
        WHERE id = ?
    ''', (text3, customer_id))
    
    conn.commit()
    conn.close()
    
    return cursor.rowcount > 0

def update_customer_token(customer_id, token):
    """고객의 token 컬럼 업데이트"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE customers
        SET token = ?
        WHERE id = ?
    ''', (token, customer_id))
    
    conn.commit()
    conn.close()
    
    return cursor.rowcount > 0

def update_customer_buy(customer_id, buy_data):
    """고객의 buy 컬럼 업데이트"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE customers
        SET buy = ?
        WHERE id = ?
    ''', (buy_data, customer_id))
    
    conn.commit()
    conn.close()
    
    return cursor.rowcount > 0

def get_customer_by_id(customer_id):
    """고객 ID로 고객 정보 가져오기"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM customers
        WHERE id = ?
    ''', (customer_id,))
    
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return dict(row)
    return None

def get_customers(page=1, per_page=20):
    """고객 데이터 조회 (페이지네이션)"""
    conn = get_db()
    cursor = conn.cursor()
    
    # 전체 개수 조회
    cursor.execute('SELECT COUNT(*) FROM customers')
    total = cursor.fetchone()[0]
    
    # 페이지네이션된 데이터 조회
    offset = (page - 1) * per_page
    cursor.execute('''
        SELECT * FROM customers
        ORDER BY id DESC
        LIMIT ? OFFSET ?
    ''', (per_page, offset))
    
    customers = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return customers, total

def clear_db():
    """데이터베이스 초기화 (모든 데이터 삭제 및 AUTOINCREMENT 리셋)"""
    conn = get_db()
    cursor = conn.cursor()
    
    # 모든 데이터 삭제
    cursor.execute('DELETE FROM customers')
    
    # 테이블 재생성 (ID는 001부터 다시 시작)
    cursor.execute('DROP TABLE IF EXISTS customers')
    cursor.execute('''
        CREATE TABLE customers (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            text1 TEXT,
            text2 TEXT,
            text3 TEXT,
            token INTEGER DEFAULT 0,
            buy TEXT,
            price INTEGER,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

# 상품별 구매수 통계 테이블 (id, name, type, purchase_count)
def init_product_stats():
    """product_stats 테이블 생성 및 products.json 기준으로 id/name/type 동기화 (purchase_count는 유지)"""
    conn = get_stats_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS product_stats (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            purchase_count INTEGER DEFAULT 0
        )
    ''')
    products = get_products()
    for p in products:
        pid = p.get('id')
        name = p.get('name', '')
        ptype = p.get('type', '')
        if not pid:
            continue
        cursor.execute('''
            INSERT INTO product_stats (id, name, type, purchase_count)
            VALUES (?, ?, ?, 0)
            ON CONFLICT(id) DO UPDATE SET name = excluded.name, type = excluded.type
        ''', (pid, name, ptype))
    conn.commit()
    conn.close()

def get_product_stats():
    """상품별 구매수 통계 목록 조회"""
    conn = get_stats_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, type, purchase_count FROM product_stats ORDER BY id')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_product_purchase_count(product_id):
    """dream_store_stats.db에서 해당 상품의 purchase_count만 조회 (상품 페이지 등에서 사용)"""
    conn = get_stats_db()
    cursor = conn.cursor()
    cursor.execute('SELECT purchase_count FROM product_stats WHERE id = ?', (product_id,))
    row = cursor.fetchone()
    conn.close()
    return row['purchase_count'] if row else 0

def add_product_purchase_count(product_id, amount):
    """상품 구매수 누적 (결제 시 호출)"""
    conn = get_stats_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE product_stats SET purchase_count = purchase_count + ?
        WHERE id = ?
    ''', (amount, product_id))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

def clear_product_stats():
    """상품 구매수 전부 0으로 초기화"""
    conn = get_stats_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE product_stats SET purchase_count = 0')
    conn.commit()
    conn.close()

# 상품 데이터 관리 (JSON 파일 기반)
# JSON 파일 경로도 절대 경로로 설정
PRODUCTS_JSON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'products.json')

def get_products():
    """상품 목록 가져오기"""
    if not os.path.exists(PRODUCTS_JSON_PATH):
        return []
    
    try:
        with open(PRODUCTS_JSON_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('products', [])
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def get_product_by_id(product_id):
    """상품 ID로 상품 정보 가져오기 (purchase_count는 dream_store_stats.db에서 조회)"""
    products = get_products()
    for product in products:
        if product.get('id') == product_id:
            product = dict(product)
            product['purchase_count'] = get_product_purchase_count(product_id)
            return product
    return None

def save_products(products):
    """상품 목록 저장"""
    data = {'products': products}
    with open(PRODUCTS_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_product(product_data):
    """새 상품 추가"""
    products = get_products()
    
    # 기본값 설정
    new_product = {
        'id': product_data.get('id'),
        'name': product_data.get('name', ''),
        'type': product_data.get('type', ''),
        'subtitle': product_data.get('subtitle', ''),
        'description': product_data.get('description', ''),
        'guide': product_data.get('guide', []),
        'ingredients': product_data.get('ingredients', []),
        'price': product_data.get('price', 0),
        'image_path': product_data.get('image_path', ''),
        'image_name': product_data.get('image_name', '')
    }
    
    products.append(new_product)
    save_products(products)
    init_product_stats()
    return new_product

def update_product(product_id, product_data):
    """상품 정보 업데이트 (purchase_count는 product_stats에서 관리)"""
    products = get_products()
    for i, product in enumerate(products):
        if product.get('id') == product_id:
            products[i] = {
                'id': product_id,
                'name': product_data.get('name', product.get('name', '')),
                'type': product_data.get('type', product.get('type', '')),
                'subtitle': product_data.get('subtitle', product.get('subtitle', '')),
                'description': product_data.get('description', product.get('description', '')),
                'guide': product_data.get('guide', product.get('guide', [])),
                'ingredients': product_data.get('ingredients', product.get('ingredients', [])),
                'price': product_data.get('price', product.get('price', 0)),
                'image_path': product_data.get('image_path', product.get('image_path', '')),
                'image_name': product_data.get('image_name', product.get('image_name', ''))
            }
            save_products(products)
            init_product_stats()  # name/type 반영
            return True
    return False

def delete_product(product_id):
    """상품 삭제"""
    products = get_products()
    products = [p for p in products if p.get('id') != product_id]
    save_products(products)
    conn = get_stats_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM product_stats WHERE id = ?', (product_id,))
    conn.commit()
    conn.close()
    return True

# 앱 시작 시 DB 초기화
# 1) dream_store_stats.db 먼저 생성·동기화 (모든 상품 행 생성, purchase_count=0)
try:
    init_product_stats()
    print(f"Stats database initialized at: {DB_STATS_PATH}")
except Exception as e:
    print(f"Stats database initialization error: {e}")
    print(f"DB_STATS_PATH: {DB_STATS_PATH}")
    print(f"Current directory: {os.getcwd()}")
    raise
# 2) 고객 DB 초기화
try:
    init_db()
    print(f"Database initialized successfully at: {DB_PATH}")
except Exception as e:
    print(f"Database initialization error: {e}")
    print(f"DB_PATH: {DB_PATH}")
    print(f"Current directory: {os.getcwd()}")
    raise

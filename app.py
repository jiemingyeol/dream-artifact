from flask import Flask, render_template, request, jsonify, redirect, url_for, send_from_directory, Response
import database
import math
import json
import memory_scoring
import receipt_image_generator
import qrcode
import io
import base64
import os
import socket

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # 세션을 위한 시크릿 키

def get_local_ip():
    """로컬 네트워크 IP 주소 가져오기"""
    try:
        # 외부 서버에 연결하여 로컬 IP 확인
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

@app.route('/')
def index():
    return render_template('intro/intro1.html')

@app.route('/intro1')
def intro1():
    return render_template('intro/intro1.html')

@app.route('/intro2')
def intro2():
    return render_template('intro/intro2.html')

@app.route('/intro3')
def intro3():
    return render_template('intro/intro3.html')

@app.route('/intro4')
def intro4():
    return render_template('intro/intro4.html')

@app.route('/intro4/submit', methods=['POST'])
def intro4_submit():
    """intro4에서 이름을 받아 DB에 저장하고 intro5로 리다이렉트"""
    name = request.form.get('name', '').strip()
    
    if not name:
        # 이름이 없으면 intro4로 다시 리다이렉트
        return redirect(url_for('intro4'))
    
    # 이름 길이 검증 (5자 이내)
    if len(name) > 5:
        # 5자 초과 시 앞 5자만 사용
        name = name[:5]
    
    # DB에 고객 데이터 생성 (나머지 컬럼은 비어있음)
    customer_no = database.add_customer(
        name=name,
        text1=None,
        text2=None,
        text3=None,
        token=0,
        buy=None
    )
    
    # intro5로 리다이렉트
    return redirect(url_for('intro5'))

@app.route('/intro5')
def intro5():
    # 최신 고객 정보 가져오기
    latest_customer = database.get_latest_customer()
    customer_name = latest_customer.get('name', '') if latest_customer else ''
    customer_id = latest_customer.get('id', '') if latest_customer else ''
    text1 = latest_customer.get('text1', '') if latest_customer else ''
    return render_template('intro/intro5.html', customer_name=customer_name, customer_id=customer_id, text1=text1)

@app.route('/intro5/submit', methods=['POST'])
def intro5_submit():
    """intro5에서 첫 번째 기억을 받아 DB에 저장하고 intro6으로 리다이렉트"""
    text1 = request.form.get('text1', '').strip()
    customer_id = request.form.get('customer_id', '').strip()
    
    if not customer_id:
        # 고객 ID가 없으면 intro5로 다시 리다이렉트
        return redirect(url_for('intro5'))
    
    # DB에 text1 업데이트
    database.update_customer_text1(customer_id, text1 if text1 else None)
    
    # intro6으로 리다이렉트
    return redirect(url_for('intro6'))

@app.route('/intro6')
def intro6():
    # 최신 고객 정보 가져오기
    latest_customer = database.get_latest_customer()
    customer_name = latest_customer.get('name', '') if latest_customer else ''
    customer_id = latest_customer.get('id', '') if latest_customer else ''
    text2 = latest_customer.get('text2', '') if latest_customer else ''
    return render_template('intro/intro6.html', customer_name=customer_name, customer_id=customer_id, text2=text2)

@app.route('/intro6/submit', methods=['POST'])
def intro6_submit():
    """intro6에서 두 번째 기억을 받아 DB에 저장하고 intro7으로 리다이렉트"""
    text2 = request.form.get('text2', '').strip()
    customer_id = request.form.get('customer_id', '').strip()
    
    if not customer_id:
        # 고객 ID가 없으면 intro6으로 다시 리다이렉트
        return redirect(url_for('intro6'))
    
    # DB에 text2 업데이트
    database.update_customer_text2(customer_id, text2 if text2 else None)
    
    # intro7으로 리다이렉트
    return redirect(url_for('intro7'))

@app.route('/intro6/skip', methods=['POST'])
def intro6_skip():
    """intro6에서 skip 버튼을 누르면 text2를 하이픈으로 저장하고 intro8로 리다이렉트"""
    customer_id = request.form.get('customer_id', '').strip()
    
    if not customer_id:
        # 고객 ID가 없으면 intro6으로 다시 리다이렉트
        return redirect(url_for('intro6'))
    
    # DB에 text2를 하이픈으로 업데이트
    database.update_customer_text2(customer_id, '-')
    
    # intro8으로 리다이렉트 (이전 페이지 정보 전달)
    return redirect(url_for('intro8', from_page='intro6'))

@app.route('/intro7')
def intro7():
    # 최신 고객 정보 가져오기
    latest_customer = database.get_latest_customer()
    customer_name = latest_customer.get('name', '') if latest_customer else ''
    customer_id = latest_customer.get('id', '') if latest_customer else ''
    text3 = latest_customer.get('text3', '') if latest_customer else ''
    return render_template('intro/intro7.html', customer_name=customer_name, customer_id=customer_id, text3=text3)

@app.route('/intro7/submit', methods=['POST'])
def intro7_submit():
    """intro7에서 세 번째 기억을 받아 DB에 저장하고 intro8으로 리다이렉트"""
    text3 = request.form.get('text3', '').strip()
    customer_id = request.form.get('customer_id', '').strip()
    
    if not customer_id:
        # 고객 ID가 없으면 intro7으로 다시 리다이렉트
        return redirect(url_for('intro7'))
    
    # DB에 text3 업데이트
    database.update_customer_text3(customer_id, text3 if text3 else None)
    
    # intro8으로 리다이렉트 (이전 페이지 정보 전달)
    return redirect(url_for('intro8', from_page='intro7'))

@app.route('/intro7/skip', methods=['POST'])
def intro7_skip():
    """intro7에서 skip 버튼을 누르면 text3를 하이픈으로 저장하고 intro8로 리다이렉트"""
    customer_id = request.form.get('customer_id', '').strip()
    
    if not customer_id:
        # 고객 ID가 없으면 intro7으로 다시 리다이렉트
        return redirect(url_for('intro7'))
    
    # DB에 text3를 하이픈으로 업데이트
    database.update_customer_text3(customer_id, '-')
    
    # intro8으로 리다이렉트 (이전 페이지 정보 전달)
    return redirect(url_for('intro8', from_page='intro7'))

@app.route('/intro8')
def intro8():
    # 이전 페이지 정보 가져오기 (기본값은 intro7)
    from_page = request.args.get('from_page', 'intro7')
    # 최신 고객 정보 가져오기
    latest_customer = database.get_latest_customer()
    customer_id = latest_customer.get('id', '') if latest_customer else ''
    return render_template('intro/intro8.html', from_page=from_page, customer_id=customer_id)

@app.route('/intro8/submit', methods=['POST'])
def intro8_submit():
    """intro8에서 next 버튼을 누르면 토큰을 계산하고 DB에 저장한 후 intro9로 리다이렉트"""
    customer_id = request.form.get('customer_id', '').strip()
    
    if not customer_id:
        # 고객 ID가 없으면 intro8로 다시 리다이렉트
        return redirect(url_for('intro8'))
    
    # 고객 정보 가져오기
    customer = database.get_customer_by_id(customer_id)
    if not customer:
        return redirect(url_for('intro8'))
    
    # text1, text2, text3 가져오기 (없는 경우 None)
    text1 = customer.get('text1')
    text2 = customer.get('text2')
    text3 = customer.get('text3')
    
    # 각 텍스트에 대해 점수 계산 (없는 경우 제외)
    scores = []
    if text1 and text1.strip() and text1.strip() != '-':
        score1 = memory_scoring.score_memory(text1)
        scores.append(score1)
    
    if text2 and text2.strip() and text2.strip() != '-':
        score2 = memory_scoring.score_memory(text2)
        scores.append(score2)
    
    if text3 and text3.strip() and text3.strip() != '-':
        score3 = memory_scoring.score_memory(text3)
        scores.append(score3)
    
    # 입력된 개수에 따라 최종 점수 계산
    if len(scores) == 0:
        # 입력된 텍스트가 없는 경우 기본값 0
        final_score = 0
    elif len(scores) == 1:
        # 1개 값 입력: 점수*2.0/3.0
        final_score = scores[0] * 2.0 / 3.0
    elif len(scores) == 2:
        # 2개 값 입력: 합*1.4/3.0
        final_score = sum(scores) * 1.4 / 3.0
    else:  # len(scores) == 3
        # 3개 값 입력: 평균값
        final_score = sum(scores) / len(scores)
    
    # 반올림하여 정수로 만들고, 100점 만점의 정수에 000을 곱한 최대 100000의 토큰으로 변경
    final_score_int = round(final_score)
    tokens = min(final_score_int * 1000, 100000)  # 최대 100000으로 제한
    
    # DB에 토큰 업데이트
    database.update_customer_token(customer_id, tokens)
    
    # intro9로 리다이렉트
    return redirect(url_for('intro9'))

@app.route('/intro9')
def intro9():
    # 최신 고객 정보 가져오기
    latest_customer = database.get_latest_customer()
    customer_name = latest_customer.get('name', '') if latest_customer else ''
    customer_token = latest_customer.get('token', 0) if latest_customer else 0
    # 토큰 값 포맷팅 (천 단위 구분자)
    token_formatted = f"{customer_token:,}" if customer_token else "0"
    return render_template('intro/intro9.html', customer_name=customer_name, customer_token=token_formatted)

@app.route('/intro10')
def intro10():
    return render_template('intro/intro10.html')

@app.route('/home')
def home():
    """Home 페이지"""
    # 최신 고객 정보 가져오기
    latest_customer = database.get_latest_customer()
    buy_data = latest_customer.get('buy', '') if latest_customer else ''
    
    # buy 필드에서 항목 개수 계산 (쉼표로 구분된 문자열 또는 JSON 배열)
    cart_count = 0
    if buy_data:
        try:
            # JSON 배열인 경우
            buy_list = json.loads(buy_data)
            if isinstance(buy_list, list):
                cart_count = len(buy_list)
        except (json.JSONDecodeError, TypeError):
            # 쉼표로 구분된 문자열인 경우
            buy_list = [item.strip() for item in buy_data.split(',') if item.strip()]
            cart_count = len(buy_list)
    
    return render_template('main/home.html', cart_count=cart_count)

@app.route('/shop')
def shop():
    """Shop 페이지"""
    # 최신 고객 정보 가져오기
    latest_customer = database.get_latest_customer()
    customer_token = latest_customer.get('token', 0) if latest_customer else 0
    buy_data = latest_customer.get('buy', '') if latest_customer else ''
    
    # 토큰 값이 1000-100000 범위에 있도록 보장
    if customer_token < 1000:
        customer_token = 1000
    elif customer_token > 100000:
        customer_token = 100000
    
    # 천 단위 콤마 포맷팅
    token_formatted = f"{customer_token:,}"
    
    # buy 필드에서 항목 개수 계산 (쉼표로 구분된 문자열 또는 JSON 배열)
    cart_count = 0
    if buy_data:
        try:
            # JSON 배열인 경우
            buy_list = json.loads(buy_data)
            if isinstance(buy_list, list):
                cart_count = len(buy_list)
        except (json.JSONDecodeError, TypeError):
            # 쉼표로 구분된 문자열인 경우
            buy_list = [item.strip() for item in buy_data.split(',') if item.strip()]
            cart_count = len(buy_list)
    
    # Shop 페이지에 표시할 상품 12개 선택 (30분 단위로 변경)
    import shop_logic
    selected_product_ids = shop_logic.get_shop_products()
    
    # 선택된 상품들의 상세 정보 가져오기
    shop_products = []
    for product_id in selected_product_ids:
        product = database.get_product_by_id(product_id)
        if product:
            # 가격 포맷팅 (천 단위 콤마)
            price_formatted = f"{product['price']:,}"
            shop_products.append({
                'id': product['id'],
                'name': product['name'],
                'image_path': product['image_path'],
                'price_formatted': price_formatted
            })
    
    return render_template('main/shop.html', 
                         customer_token=token_formatted, 
                         cart_count=cart_count,
                         shop_products=shop_products)

@app.route('/cart')
def cart():
    """Cart 페이지"""
    # 최신 고객 정보 가져오기
    latest_customer = database.get_latest_customer()
    buy_data = latest_customer.get('buy', '') if latest_customer else ''
    
    # buy 필드에서 항목 개수 계산 및 파싱 (쉼표로 구분된 문자열 또는 JSON 배열)
    cart_count = 0
    buy_items = []  # [{id: "01", count: 1}, ...] 형태
    
    if buy_data:
        try:
            # JSON 배열인 경우
            buy_list = json.loads(buy_data)
            if not isinstance(buy_list, list):
                buy_list = []
        except (json.JSONDecodeError, TypeError):
            # 쉼표로 구분된 문자열인 경우
            buy_list = [item.strip() for item in buy_data.split(',') if item.strip()]
        
        cart_count = len(buy_list)
        
        # 각 항목을 파싱하여 id와 count 분리
        for item in buy_list:
            if '*' in item:
                parts = item.split('*', 1)
                if len(parts) == 2:
                    product_id = parts[0].strip()
                    try:
                        count = int(parts[1].strip())
                    except ValueError:
                        count = 1
                    buy_items.append({
                        'id': product_id,
                        'count': count
                    })
    
    # 각 상품의 상세 정보 가져오기
    cart_products = []
    total_price = 0
    for item in buy_items:
        product = database.get_product_by_id(item['id'])
        if product:
            item_total_price = product['price'] * item['count']
            cart_products.append({
                'id': product['id'],
                'name': product['name'],
                'subtitle': product.get('subtitle', ''),
                'image_path': product['image_path'],
                'price': product['price'],
                'count': item['count'],
                'total_price': item_total_price,
                'total_price_formatted': f"{item_total_price:,}"
            })
            total_price += product['price'] * item['count']
    
    # 전체 가격 포맷팅 (천 단위 콤마)
    total_price_formatted = f"{total_price:,}"
    
    # 고객 토큰 가져오기
    customer_token = latest_customer.get('token', 0) if latest_customer else 0
    customer_token_formatted = f"{customer_token:,}"
    
    return render_template('main/cart.html', 
                         cart_count=cart_count,
                         buy_items=buy_items,
                         cart_products=cart_products,
                         total_price=total_price,
                         total_price_formatted=total_price_formatted,
                         customer_token=customer_token_formatted,
                         customer_token_value=customer_token,
                         buy_data=buy_data)

@app.route('/receipt')
def receipt():
    """Receipt 페이지"""
    # 최신 고객 정보 가져오기
    latest_customer = database.get_latest_customer()
    buy_data = latest_customer.get('buy', '') if latest_customer else ''
    
    # buy 필드에서 항목 개수 계산 및 파싱 (쉼표로 구분된 문자열 또는 JSON 배열)
    cart_count = 0
    buy_items = []  # [{id: "01", count: 1}, ...] 형태
    
    if buy_data:
        try:
            # JSON 배열인 경우
            buy_list = json.loads(buy_data)
            if not isinstance(buy_list, list):
                buy_list = []
        except (json.JSONDecodeError, TypeError):
            # 쉼표로 구분된 문자열인 경우
            buy_list = [item.strip() for item in buy_data.split(',') if item.strip()]
        
        cart_count = len(buy_list)
        
        # 각 항목을 파싱하여 id와 count 분리
        for item in buy_list:
            if '*' in item:
                parts = item.split('*', 1)
                if len(parts) == 2:
                    product_id = parts[0].strip()
                    try:
                        count = int(parts[1].strip())
                    except ValueError:
                        count = 1
                    buy_items.append({
                        'id': product_id,
                        'count': count
                    })
    
    # 각 상품의 상세 정보 가져오기 (최대 5개)
    receipt_products = []
    total_price = 0
    for item in buy_items[:5]:  # 최대 5개까지만
        product = database.get_product_by_id(item['id'])
        if product:
            item_total_price = product['price'] * item['count']
            receipt_products.append({
                'id': product['id'],
                'name': product['name'],
                'subtitle': product.get('subtitle', ''),
                'image_path': product['image_path'],
                'price': product['price'],
                'count': item['count'],
                'total_price': item_total_price,
                'total_price_formatted': f"{item_total_price:,}"
            })
            total_price += product['price'] * item['count']
    
    # 전체 가격 포맷팅 (천 단위 콤마)
    total_price_formatted = f"{total_price:,}"
    
    # 이미지 URL: 동적 생성 뷰어 사용 (로컬/배포 공통, 파일 저장 없음)
    customer_id = latest_customer.get('id', '') if latest_customer else ''
    if customer_id:
        image_url = url_for('generate_receipt_image_dynamic', customer_id=customer_id)
    else:
        image_url = url_for('static', filename='images/main/result_template.png')
    
    # 절대 URL로 변환 (QR 코드용)
    # Render 배포 시: request.url_root가 자동으로 Render 도메인 사용 (예: https://your-app.onrender.com)
    # 로컬 개발 시: 로컬 IP 사용하여 같은 네트워크의 모바일 기기에서 접근 가능
    if request.host and ('localhost' in request.host or '127.0.0.1' in request.host):
        # 로컬 개발 환경: 로컬 IP 사용
        local_ip = get_local_ip()
        port = request.environ.get('SERVER_PORT', '5001')  # 기본 포트 5001 (macOS AirPlay 충돌 방지)
        scheme = request.scheme if hasattr(request, 'scheme') else 'http'
        full_image_url = f"{scheme}://{local_ip}:{port}{image_url}"
    else:
        # Render 배포 환경: request.url_root가 자동으로 올바른 도메인 사용
        full_image_url = request.url_root.rstrip('/') + image_url
    
    # QR 코드 생성
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(full_image_url)
    qr.make(fit=True)
    
    # QR 코드 이미지 생성
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    # QR 코드를 base64로 인코딩
    img_buffer = io.BytesIO()
    qr_img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    qr_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
    qr_data_url = f"data:image/png;base64,{qr_base64}"
    
    return render_template('main/receipt.html', 
                         cart_count=cart_count, 
                         receipt_products=receipt_products,
                         total_price_formatted=total_price_formatted,
                         qr_code_data_url=qr_data_url)

def get_product_page_data(product_id):
    """상품 페이지 공통 데이터 처리 함수"""
    # 최신 고객 정보 가져오기
    latest_customer = database.get_latest_customer()
    customer_token = latest_customer.get('token', 0) if latest_customer else 0
    buy_data = latest_customer.get('buy', '') if latest_customer else ''
    
    # 토큰 값이 1000-100000 범위에 있도록 보장
    if customer_token < 1000:
        customer_token = 1000
    elif customer_token > 100000:
        customer_token = 100000
    
    # 천 단위 콤마 포맷팅
    token_formatted = f"{customer_token:,}"
    
    # buy 필드에서 항목 개수 계산 (쉼표로 구분된 문자열 또는 JSON 배열)
    cart_count = 0
    if buy_data:
        try:
            # JSON 배열인 경우
            buy_list = json.loads(buy_data)
            if isinstance(buy_list, list):
                cart_count = len(buy_list)
        except (json.JSONDecodeError, TypeError):
            # 쉼표로 구분된 문자열인 경우
            buy_list = [item.strip() for item in buy_data.split(',') if item.strip()]
            cart_count = len(buy_list)
    
    # 제품 데이터 가져오기 (purchase_count는 dream_store_stats.db에서 조회)
    product = database.get_product_by_id(product_id)
    if not product:
        # 제품이 없으면 기본값 사용 (purchase_count만 stats DB에서 조회)
        product = {
            'id': product_id,
            'name': '',
            'subtitle': '',
            'description': '',
            'image_path': f'static/images/product/item/{product_id}-.png',
            'price': 20000,
            'purchase_count': database.get_product_purchase_count(product_id),
            'guide': [],
            'ingredients': []
        }
    
    # 가격 포맷팅 (천 단위 콤마)
    price_formatted = f"{product['price']:,}"
    
    # guide 배열 처리 (무드등, 베개, 자장가, 취침시간)
    guide_labels = ['무드등 여부', '베개 사용 여부', '자장가 여부', '권장 취침 시간']
    guide_display = []
    guide_array = product.get('guide', [])
    for i, label in enumerate(guide_labels):
        if i < len(guide_array):
            value = guide_array[i]
            if i == 3:  # 취침 시간
                guide_display.append(f"{label} {value}")
            else:  # O/X
                guide_display.append(f"{label} {value}")
        else:
            guide_display.append(None)
    
    return {
        'customer_token': token_formatted,
        'cart_count': cart_count,
        'product': product,
        'price_formatted': price_formatted,
        'guide_display': guide_display
    }

@app.route('/product<product_id>')
def product(product_id):
    """동적 Product 페이지 (product01, product02, ... product30)"""
    data = get_product_page_data(product_id)
    return render_template('product/product.html', **data)

@app.route('/product1')
def product1():
    """Product 1 페이지 (호환성 유지)"""
    data = get_product_page_data('01')
    return render_template('product/product.html', **data)

@app.route('/product2')
def product2():
    """Product 2 페이지 (호환성 유지)"""
    data = get_product_page_data('02')
    return render_template('product/product.html', **data)

@app.route('/product3')
def product3():
    """Product 3 페이지 (호환성 유지)"""
    data = get_product_page_data('03')
    return render_template('product/product.html', **data)

@app.route('/product4')
def product4():
    """Product 4 페이지 (호환성 유지)"""
    data = get_product_page_data('04')
    return render_template('product/product.html', **data)

@app.route('/product5')
def product5():
    """Product 5 페이지 (호환성 유지)"""
    data = get_product_page_data('05')
    return render_template('product/product.html', **data)

@app.route('/product6')
def product6():
    """Product 6 페이지 (호환성 유지)"""
    data = get_product_page_data('06')
    return render_template('product/product.html', **data)

@app.route('/product7')
def product7():
    """Product 7 페이지 (호환성 유지)"""
    data = get_product_page_data('07')
    return render_template('product/product.html', **data)

@app.route('/product8')
def product8():
    """Product 8 페이지 (호환성 유지)"""
    data = get_product_page_data('08')
    return render_template('product/product.html', **data)

@app.route('/product9')
def product9():
    """Product 9 페이지 (호환성 유지)"""
    data = get_product_page_data('09')
    return render_template('product/product.html', **data)

@app.route('/product10')
def product10():
    """Product 10 페이지 (호환성 유지)"""
    data = get_product_page_data('10')
    return render_template('product/product.html', **data)

@app.route('/product11')
def product11():
    """Product 11 페이지 (호환성 유지)"""
    data = get_product_page_data('11')
    return render_template('product/product.html', **data)

@app.route('/product12')
def product12():
    """Product 12 페이지 (호환성 유지)"""
    data = get_product_page_data('12')
    return render_template('product/product.html', **data)

@app.route('/product13')
def product13():
    """Product 13 페이지 (호환성 유지)"""
    data = get_product_page_data('13')
    return render_template('product/product.html', **data)

@app.route('/product14')
def product14():
    """Product 14 페이지 (호환성 유지)"""
    data = get_product_page_data('14')
    return render_template('product/product.html', **data)

@app.route('/product15')
def product15():
    """Product 15 페이지 (호환성 유지)"""
    data = get_product_page_data('15')
    return render_template('product/product.html', **data)

@app.route('/product16')
def product16():
    """Product 16 페이지 (호환성 유지)"""
    data = get_product_page_data('16')
    return render_template('product/product.html', **data)

@app.route('/product17')
def product17():
    """Product 17 페이지 (호환성 유지)"""
    data = get_product_page_data('17')
    return render_template('product/product.html', **data)

@app.route('/product18')
def product18():
    """Product 18 페이지 (호환성 유지)"""
    data = get_product_page_data('18')
    return render_template('product/product.html', **data)

@app.route('/product19')
def product19():
    """Product 19 페이지 (호환성 유지)"""
    data = get_product_page_data('19')
    return render_template('product/product.html', **data)

@app.route('/product20')
def product20():
    """Product 20 페이지 (호환성 유지)"""
    data = get_product_page_data('20')
    return render_template('product/product.html', **data)

@app.route('/product21')
def product21():
    """Product 21 페이지 (호환성 유지)"""
    data = get_product_page_data('21')
    return render_template('product/product.html', **data)

@app.route('/product22')
def product22():
    """Product 22 페이지 (호환성 유지)"""
    data = get_product_page_data('22')
    return render_template('product/product.html', **data)

@app.route('/product23')
def product23():
    """Product 23 페이지 (호환성 유지)"""
    data = get_product_page_data('23')
    return render_template('product/product.html', **data)

@app.route('/product24')
def product24():
    """Product 24 페이지 (호환성 유지)"""
    data = get_product_page_data('24')
    return render_template('product/product.html', **data)

@app.route('/product25')
def product25():
    """Product 25 페이지 (호환성 유지)"""
    data = get_product_page_data('25')
    return render_template('product/product.html', **data)

@app.route('/product26')
def product26():
    """Product 26 페이지 (호환성 유지)"""
    data = get_product_page_data('26')
    return render_template('product/product.html', **data)

@app.route('/product27')
def product27():
    """Product 27 페이지 (호환성 유지)"""
    data = get_product_page_data('27')
    return render_template('product/product.html', **data)

@app.route('/product28')
def product28():
    """Product 28 페이지 (호환성 유지)"""
    data = get_product_page_data('28')
    return render_template('product/product.html', **data)

@app.route('/product29')
def product29():
    """Product 29 페이지 (호환성 유지)"""
    data = get_product_page_data('29')
    return render_template('product/product.html', **data)

@app.route('/product30')
def product30():
    """Product 30 페이지 (호환성 유지)"""
    data = get_product_page_data('30')
    return render_template('product/product.html', **data)

@app.route('/admin')
def admin():
    """Admin 페이지 - DB 조회 및 관리"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    customers, total = database.get_customers(page, per_page)
    total_pages = math.ceil(total / per_page) if total > 0 else 1
    product_stats = database.get_product_stats()
    
    return render_template('admin.html', 
                         customers=customers, 
                         page=page, 
                         total_pages=total_pages,
                         total=total,
                         product_stats=product_stats)

@app.route('/admin/clear', methods=['POST'])
def admin_clear():
    """고객 DB 초기화"""
    database.clear_db()
    return jsonify({'success': True, 'message': '데이터베이스가 초기화되었습니다.'})

@app.route('/admin/clear-product-stats', methods=['POST'])
def admin_clear_product_stats():
    """상품 구매수 초기화"""
    database.clear_product_stats()
    return jsonify({'success': True, 'message': '상품 구매수가 초기화되었습니다.'})

@app.route('/api/checkout', methods=['POST'])
def checkout():
    """장바구니 결제 시 상품별 구매수(purchase_count) 누적"""
    latest_customer = database.get_latest_customer()
    if not latest_customer:
        return jsonify({'success': False, 'message': '고객 정보를 찾을 수 없습니다.'}), 404
    buy_data = latest_customer.get('buy', '') or ''
    if not buy_data or not buy_data.strip():
        return jsonify({'success': False, 'message': '장바구니가 비어 있습니다.'}), 400
    try:
        buy_list = json.loads(buy_data)
        if not isinstance(buy_list, list):
            buy_list = [item.strip() for item in buy_data.split(',') if item.strip()]
    except (json.JSONDecodeError, TypeError):
        buy_list = [item.strip() for item in buy_data.split(',') if item.strip()]
    for item in buy_list:
        if '*' in item:
            parts = item.split('*', 1)
            if len(parts) == 2:
                product_id = parts[0].strip()
                try:
                    count = int(parts[1].strip())
                except ValueError:
                    count = 1
                database.add_product_purchase_count(product_id, count)
    return jsonify({'success': True, 'message': '결제가 반영되었습니다.'})

@app.route('/api/add-to-cart', methods=['POST'])
def add_to_cart():
    """장바구니에 상품 추가"""
    data = request.get_json()
    product_id = data.get('product_id')
    count = data.get('count', 1)
    
    if not product_id:
        return jsonify({'success': False, 'message': '상품 ID가 필요합니다.'}), 400
    
    # 최신 고객 정보 가져오기
    latest_customer = database.get_latest_customer()
    if not latest_customer:
        return jsonify({'success': False, 'message': '고객 정보를 찾을 수 없습니다.'}), 404
    
    customer_id = latest_customer.get('id')
    buy_data = latest_customer.get('buy', '') or ''
    
    # 새 항목 형식: "{id}*{count}"
    new_item = f"{product_id}*{count}"
    
    # 기존 buy 데이터 파싱
    buy_list = []
    if buy_data:
        try:
            # JSON 배열인 경우
            buy_list = json.loads(buy_data)
            if not isinstance(buy_list, list):
                buy_list = []
        except (json.JSONDecodeError, TypeError):
            # 쉼표로 구분된 문자열인 경우
            buy_list = [item.strip() for item in buy_data.split(',') if item.strip()]
    
    # 동일한 product_id로 시작하는 항목이 있는지 확인
    for item in buy_list:
        if item.startswith(f"{product_id}*"):
            return jsonify({'success': False, 'message': '이미 장바구니에 있는 상품입니다.'}), 400
    
    # 새 항목 추가
    buy_list.append(new_item)
    
    # buy 데이터 업데이트 (쉼표로 구분된 문자열로 저장)
    updated_buy_data = ','.join(buy_list)
    database.update_customer_buy(customer_id, updated_buy_data)
    
    return jsonify({'success': True, 'message': '상품이 담겼습니다!'})

@app.route('/api/update-cart-quantity', methods=['POST'])
def update_cart_quantity():
    """장바구니 상품 수량 변경"""
    data = request.get_json()
    product_id = data.get('product_id')
    change = data.get('change', 0)  # +1 또는 -1
    
    if not product_id:
        return jsonify({'success': False, 'message': '상품 ID가 필요합니다.'}), 400
    
    # 최신 고객 정보 가져오기
    latest_customer = database.get_latest_customer()
    if not latest_customer:
        return jsonify({'success': False, 'message': '고객 정보를 찾을 수 없습니다.'}), 404
    
    customer_id = latest_customer.get('id')
    buy_data = latest_customer.get('buy', '') or ''
    
    # 기존 buy 데이터 파싱
    buy_list = []
    if buy_data:
        try:
            buy_list = json.loads(buy_data)
            if not isinstance(buy_list, list):
                buy_list = []
        except (json.JSONDecodeError, TypeError):
            buy_list = [item.strip() for item in buy_data.split(',') if item.strip()]
    
    # 해당 상품 찾기 및 수량 업데이트
    found = False
    updated_list = []
    for item in buy_list:
        if item.startswith(f"{product_id}*"):
            found = True
            parts = item.split('*', 1)
            if len(parts) == 2:
                try:
                    current_count = int(parts[1].strip())
                    new_count = current_count + change
                    # 수량은 최소 1 이상이어야 함
                    if new_count < 1:
                        return jsonify({'success': False, 'message': '수량은 1개 이상이어야 합니다.'}), 400
                    updated_list.append(f"{product_id}*{new_count}")
                except ValueError:
                    updated_list.append(item)
            else:
                updated_list.append(item)
        else:
            updated_list.append(item)
    
    if not found:
        return jsonify({'success': False, 'message': '장바구니에서 상품을 찾을 수 없습니다.'}), 404
    
    # buy 데이터 업데이트
    updated_buy_data = ','.join(updated_list)
    database.update_customer_buy(customer_id, updated_buy_data)
    
    return jsonify({'success': True, 'message': '수량이 변경되었습니다.'})

@app.route('/api/delete-cart-item', methods=['POST'])
def delete_cart_item():
    """장바구니에서 상품 삭제"""
    data = request.get_json()
    product_id = data.get('product_id')
    
    if not product_id:
        return jsonify({'success': False, 'message': '상품 ID가 필요합니다.'}), 400
    
    # 최신 고객 정보 가져오기
    latest_customer = database.get_latest_customer()
    if not latest_customer:
        return jsonify({'success': False, 'message': '고객 정보를 찾을 수 없습니다.'}), 404
    
    customer_id = latest_customer.get('id')
    buy_data = latest_customer.get('buy', '') or ''
    
    # 기존 buy 데이터 파싱
    buy_list = []
    if buy_data:
        try:
            buy_list = json.loads(buy_data)
            if not isinstance(buy_list, list):
                buy_list = []
        except (json.JSONDecodeError, TypeError):
            buy_list = [item.strip() for item in buy_data.split(',') if item.strip()]
    
    # 해당 상품 제거
    updated_list = [item for item in buy_list if not item.startswith(f"{product_id}*")]
    
    # buy 데이터 업데이트
    updated_buy_data = ','.join(updated_list) if updated_list else ''
    database.update_customer_buy(customer_id, updated_buy_data)
    
    return jsonify({'success': True, 'message': '상품이 삭제되었습니다.'})

@app.route('/receipt-image-generate/<customer_id>')
def generate_receipt_image_dynamic(customer_id):
    """
    동적 영수증 이미지 뷰어 페이지 (Render 환경용)
    - 이미지 뷰어 페이지를 렌더링하고, 이미지는 별도 라우트에서 생성
    """
    # 고객 정보 가져오기
    customer = database.get_customer_by_id(customer_id)
    if not customer:
        return "Customer not found", 404
    
    # 이미지 데이터 URL 생성 (별도 라우트에서 이미지 바이너리 반환)
    image_url = url_for('generate_receipt_image_data', customer_id=customer_id)
    
    return render_template('main/receipt_image_viewer.html', 
                         image_url=image_url,
                         filename=f"customer_{customer_id}.png")

@app.route('/receipt-image-data/<customer_id>')
def generate_receipt_image_data(customer_id):
    """
    동적 영수증 이미지 바이너리 데이터 반환 (Render 환경용)
    - 파일 저장 없이 메모리에서 생성하여 바로 반환
    - 매번 DB에서 최신 데이터를 읽어서 이미지 생성
    """
    # 고객 정보 가져오기
    customer = database.get_customer_by_id(customer_id)
    if not customer:
        return "Customer not found", 404
    
    # 구매 상품 정보 가져오기
    buy_data = customer.get('buy', '') or ''
    buy_items = []
    
    if buy_data:
        try:
            buy_list = json.loads(buy_data)
            if not isinstance(buy_list, list):
                buy_list = []
        except (json.JSONDecodeError, TypeError):
            buy_list = [item.strip() for item in buy_data.split(',') if item.strip()]
        
        for item in buy_list:
            if '*' in item:
                parts = item.split('*', 1)
                if len(parts) == 2:
                    product_id = parts[0].strip()
                    try:
                        count = int(parts[1].strip())
                    except ValueError:
                        count = 1
                    buy_items.append({'id': product_id, 'count': count})
    
    # 상품 상세 정보 가져오기 (최대 5개)
    receipt_products = []
    total_price = 0
    for item in buy_items[:5]:
        product = database.get_product_by_id(item['id'])
        if product:
            item_total_price = product['price'] * item['count']
            receipt_products.append({
                'id': product['id'],
                'name': product['name'],
                'subtitle': product.get('subtitle', ''),
                'image_path': product['image_path'],
                'price': product['price'],
                'count': item['count'],
                'total_price': item_total_price
            })
            total_price += product['price'] * item['count']
    
    # 이미지 생성 (메모리에서, 파일 저장 안 함)
    try:
        image_bytes = receipt_image_generator.generate_customer_receipt_image(
            customer,
            receipt_products,
            total_price,
            save_to_disk=False
        )
        
        # BytesIO를 Response로 반환 (JPEG 형식)
        return Response(image_bytes.getvalue(), mimetype='image/jpeg')
    except Exception as e:
        # 이미지 생성 실패 시 템플릿 이미지 반환
        template_path = os.path.join('static', 'images', 'main', 'result_template.png')
        if os.path.exists(template_path):
            return send_from_directory('static/images/main', 'result_template.png')
        return "Image generation failed", 500

if __name__ == '__main__':
    # 0.0.0.0으로 바인딩하여 같은 네트워크의 다른 기기에서 접근 가능하게 함
    # macOS에서 포트 5000이 AirPlay Receiver에 사용되는 경우를 대비해 5001 사용
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True)

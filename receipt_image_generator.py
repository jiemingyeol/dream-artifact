import os
import sys
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont  # type: ignore[import-untyped]


def generate_customer_receipt_image(customer_data, receipt_products, total_price, save_to_disk=False):
    """
    고객 영수증 이미지 생성 함수 (메모리에서 생성, 파일 저장 없음)
    
    Args:
        customer_data: 고객 정보 딕셔너리 (id, name, token 등)
        receipt_products: 구매 상품 리스트 (최대 5개)
        total_price: 총 가격 (정수)
        save_to_disk: 사용하지 않음 (호환용, 항상 BytesIO 반환)
    
    Returns:
        BytesIO: 이미지 바이너리 데이터 (JPEG 형식)
    """
    # 현재 스크립트의 디렉토리 경로
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 1. 템플릿 이미지 로드
    template_path = os.path.join(script_dir, 'static', 'images', 'main', 'result_template.png')
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template image not found: {template_path}")
    
    # 템플릿 이미지 열기 (RGB로 변환하여 JPEG 호환)
    template_img = Image.open(template_path).convert('RGB')
    
    # 템플릿 이미지를 1080x1920px로 리사이즈 (고정 크기)
    target_width = 1080
    target_height = 1920
    receipt_img = template_img.resize((target_width, target_height), Image.Resampling.LANCZOS)
    
    # 이미지 크기 확인
    img_width, img_height = receipt_img.size
    
    # 2. Pillow Draw 객체 생성 (텍스트 및 이미지 배치용)
    draw = ImageDraw.Draw(receipt_img)
    
    # 3. 상품 이미지 배치 (receipt.html과 동일한 로직)
    if receipt_products:
        product_count = len(receipt_products)
        available_width = 391.44  # 이미지 기준 너비 (336px * 1.165)
        image_size = 56 * (391.44 / 336)  # 약 65.24px (56px * 1.165)
        image_y = 559.14  # y 좌표 고정
        start_x = 336.59  # 시작 x 좌표
        
        # 상품 개수에 따라 간격 계산 및 이미지 배치
        if product_count == 1:
            # 중앙 정렬
            image_x = start_x + (available_width - image_size) / 2
            product_image_path = os.path.join(script_dir, receipt_products[0]['image_path'])
            if os.path.exists(product_image_path):
                try:
                    product_img = Image.open(product_image_path).convert('RGB')
                    product_img = product_img.resize((int(image_size), int(image_size)), Image.Resampling.LANCZOS)
                    receipt_img.paste(product_img, (int(image_x), int(image_y)))
                except Exception as e:
                    print(f"Failed to load product image {product_image_path}: {e}")
        
        elif product_count == 2:
            gap = (available_width - image_size * 2) / 3
            image1_x = start_x + gap
            image2_x = image1_x + image_size + gap
            for idx, product in enumerate(receipt_products[:2]):
                product_image_path = os.path.join(script_dir, product['image_path'])
                if os.path.exists(product_image_path):
                    try:
                        product_img = Image.open(product_image_path).convert('RGB')
                        product_img = product_img.resize((int(image_size), int(image_size)), Image.Resampling.LANCZOS)
                        paste_x = int(image1_x if idx == 0 else image2_x)
                        receipt_img.paste(product_img, (paste_x, int(image_y)))
                    except Exception as e:
                        print(f"Failed to load product image {product_image_path}: {e}")
        
        elif product_count == 3:
            gap = (available_width - image_size * 3) / 4
            image1_x = start_x + gap
            image2_x = image1_x + image_size + gap
            image3_x = image2_x + image_size + gap
            for idx, product in enumerate(receipt_products[:3]):
                product_image_path = os.path.join(script_dir, product['image_path'])
                if os.path.exists(product_image_path):
                    try:
                        product_img = Image.open(product_image_path).convert('RGB')
                        product_img = product_img.resize((int(image_size), int(image_size)), Image.Resampling.LANCZOS)
                        if idx == 0:
                            paste_x = int(image1_x)
                        elif idx == 1:
                            paste_x = int(image2_x)
                        else:
                            paste_x = int(image3_x)
                        receipt_img.paste(product_img, (paste_x, int(image_y)))
                    except Exception as e:
                        print(f"Failed to load product image {product_image_path}: {e}")
        
        elif product_count == 4:
            gap = (available_width - image_size * 4) / 5
            image1_x = start_x + gap
            image2_x = image1_x + image_size + gap
            image3_x = image2_x + image_size + gap
            image4_x = image3_x + image_size + gap
            for idx, product in enumerate(receipt_products[:4]):
                product_image_path = os.path.join(script_dir, product['image_path'])
                if os.path.exists(product_image_path):
                    try:
                        product_img = Image.open(product_image_path).convert('RGB')
                        product_img = product_img.resize((int(image_size), int(image_size)), Image.Resampling.LANCZOS)
                        if idx == 0:
                            paste_x = int(image1_x)
                        elif idx == 1:
                            paste_x = int(image2_x)
                        elif idx == 2:
                            paste_x = int(image3_x)
                        else:
                            paste_x = int(image4_x)
                        receipt_img.paste(product_img, (paste_x, int(image_y)))
                    except Exception as e:
                        print(f"Failed to load product image {product_image_path}: {e}")
        
        elif product_count == 5:
            gap = (available_width - image_size * 5) / 6
            image1_x = start_x + gap
            image2_x = image1_x + image_size + gap
            image3_x = image2_x + image_size + gap
            image4_x = image3_x + image_size + gap
            image5_x = image4_x + image_size + gap
            for idx, product in enumerate(receipt_products[:5]):
                product_image_path = os.path.join(script_dir, product['image_path'])
                if os.path.exists(product_image_path):
                    try:
                        product_img = Image.open(product_image_path).convert('RGB')
                        product_img = product_img.resize((int(image_size), int(image_size)), Image.Resampling.LANCZOS)
                        if idx == 0:
                            paste_x = int(image1_x)
                        elif idx == 1:
                            paste_x = int(image2_x)
                        elif idx == 2:
                            paste_x = int(image3_x)
                        elif idx == 3:
                            paste_x = int(image4_x)
                        else:
                            paste_x = int(image5_x)
                        receipt_img.paste(product_img, (paste_x, int(image_y)))
                    except Exception as e:
                        print(f"Failed to load product image {product_image_path}: {e}")
    
    # 4. 상품 정보 텍스트 배치 (name, subtitle, 가격)
    # 폰트 경로 설정
    font_dir = os.path.join(script_dir, 'static', 'fonts')
    
    # 한글 텍스트 감지 함수
    def contains_korean(text):
        """텍스트에 한글이 포함되어 있는지 확인"""
        if not text:
            return False
        for char in str(text):
            if '\uAC00' <= char <= '\uD7A3':  # 한글 유니코드 범위
                return True
        return False
    
    # Pretendard 폰트 경로 확인 (한글 텍스트용)
    pretendard_bold_path = os.path.join(font_dir, 'Pretendard-Bold.ttf')
    pretendard_semibold_path = os.path.join(font_dir, 'Pretendard-SemiBold.ttf')
    
    # 한글 폰트 로드 (Pretendard)
    korean_fonts = {}
    if os.path.exists(pretendard_bold_path) and os.path.exists(pretendard_semibold_path):
        try:
            # name에는 Bold 사용
            korean_fonts['name'] = ImageFont.truetype(pretendard_bold_path, 14)
            # subtitle에는 SemiBold 사용
            subtitle_size = int(9 * (391.44 / 336))
            korean_fonts['subtitle'] = ImageFont.truetype(pretendard_semibold_path, subtitle_size)
            # price와 total은 SemiBold 사용
            price_size = int(11 * (391.44 / 336))
            korean_fonts['price'] = ImageFont.truetype(pretendard_semibold_path, price_size)
            total_size = int(12 * (391.44 / 336))
            korean_fonts['total'] = ImageFont.truetype(pretendard_semibold_path, total_size)
            print("Successfully loaded Pretendard fonts for Korean text (Bold for name, SemiBold for subtitle)")
        except Exception as e:
            print(f"ERROR: Failed to load Pretendard fonts: {e}")
            import traceback
            traceback.print_exc()
            korean_fonts = {}
    
    # Pretendard가 없으면 Noto Sans KR으로 fallback
    if not korean_fonts:
        noto_sans_kr_path = None
        # 1. 프로젝트 폴더에서 찾기
        project_noto_paths = [
            os.path.join(font_dir, 'NotoSansKR-VariableFont_wght.ttf'),  # Variable Font (우선)
            os.path.join(font_dir, 'NotoSansKR-Regular.ttf'),
            os.path.join(font_dir, 'NotoSansKR-Bold.ttf'),
            os.path.join(font_dir, 'NotoSansKR-Medium.ttf'),
            os.path.join(font_dir, 'NotoSansKR-SemiBold.ttf'),
        ]
        for path in project_noto_paths:
            if os.path.exists(path):
                noto_sans_kr_path = path
                print(f"Found Noto Sans KR in project: {noto_sans_kr_path}")
                break
        
        # 2. 시스템 폰트에서 찾기 (macOS)
        if not noto_sans_kr_path and sys.platform == 'darwin':
            system_noto_paths = [
                '/System/Library/Fonts/Supplemental/NotoSansKR-Regular.otf',
                '/Library/Fonts/NotoSansKR-Regular.ttf',
                '/System/Library/Fonts/NotoSansKR-Regular.ttf',
            ]
            for path in system_noto_paths:
                if os.path.exists(path):
                    noto_sans_kr_path = path
                    print(f"Found Noto Sans KR in system: {noto_sans_kr_path}")
                    break
        
        if noto_sans_kr_path:
            try:
                korean_fonts['name'] = ImageFont.truetype(noto_sans_kr_path, 14)
                subtitle_size = int(9 * (391.44 / 336))
                korean_fonts['subtitle'] = ImageFont.truetype(noto_sans_kr_path, subtitle_size)
                price_size = int(11 * (391.44 / 336))
                korean_fonts['price'] = ImageFont.truetype(noto_sans_kr_path, price_size)
                total_size = int(12 * (391.44 / 336))
                korean_fonts['total'] = ImageFont.truetype(noto_sans_kr_path, total_size)
                print("Successfully loaded Noto Sans KR fonts for Korean text")
            except Exception as e:
                print(f"ERROR: Failed to load Noto Sans KR fonts: {e}")
                import traceback
                traceback.print_exc()
                korean_fonts = {}
    
    # Noto Sans KR이 없으면 AppleGothic으로 fallback
    if not korean_fonts:
        korean_font_path = None
        if sys.platform == 'darwin':  # macOS
            korean_font_candidates = [
                '/System/Library/Fonts/Supplemental/AppleGothic.ttf',
                '/Library/Fonts/AppleGothic.ttf',
                '/System/Library/Fonts/AppleGothic.ttf',
            ]
            for font_path in korean_font_candidates:
                if os.path.exists(font_path):
                    korean_font_path = font_path
                    print(f"Found AppleGothic as fallback: {korean_font_path}")
                    break
        
        if korean_font_path:
            try:
                # 볼드 효과를 위해 이름 폰트는 약간 큰 크기 사용 (14 -> 15)
                korean_fonts['name'] = ImageFont.truetype(korean_font_path, 15)  # 볼드 효과
                subtitle_size = int(9 * (391.44 / 336))
                korean_fonts['subtitle'] = ImageFont.truetype(korean_font_path, subtitle_size)
                price_size = int(11 * (391.44 / 336))
                korean_fonts['price'] = ImageFont.truetype(korean_font_path, price_size)
                total_size = int(12 * (391.44 / 336))
                korean_fonts['total'] = ImageFont.truetype(korean_font_path, total_size)
                print("Successfully loaded AppleGothic fonts as fallback")
            except Exception as e:
                print(f"ERROR: Failed to load AppleGothic fonts: {e}")
                korean_fonts = {}
    
    # 영문/숫자용 폰트 로드 (Geist 또는 Inter)
    latin_fonts = {}
    font_paths = {
        'name': os.path.join(font_dir, 'Geist-SemiBold.ttf'),  # SemiBold는 이미 볼드 효과
        'subtitle': os.path.join(font_dir, 'Geist-Regular.ttf'),
        'price': os.path.join(font_dir, 'Geist-SemiBold.ttf'),
        'total': os.path.join(font_dir, 'Geist-SemiBold.ttf')
    }
    
    for key, path in font_paths.items():
        if os.path.exists(path):
            try:
                if key == 'name':
                    # 볼드 효과를 위해 약간 큰 크기 사용 (14 -> 15)
                    latin_fonts[key] = ImageFont.truetype(path, 15)  # SemiBold + 크기로 볼드 효과
                elif key == 'subtitle':
                    subtitle_size = int(9 * (391.44 / 336))
                    latin_fonts[key] = ImageFont.truetype(path, subtitle_size)
                elif key == 'price':
                    price_size = int(11 * (391.44 / 336))
                    latin_fonts[key] = ImageFont.truetype(path, price_size)
                elif key == 'total':
                    total_size = int(12 * (391.44 / 336))
                    latin_fonts[key] = ImageFont.truetype(path, total_size)
            except Exception as e:
                print(f"WARNING: Failed to load Latin font {key}: {e}")
    
    # 폰트 선택 함수 (한글 포함 여부에 따라)
    def get_font_for_text(text, font_type):
        """텍스트에 한글이 포함되어 있으면 한글 폰트, 아니면 영문 폰트 반환"""
        if contains_korean(text):
            return korean_fonts.get(font_type) or latin_fonts.get(font_type) or ImageFont.load_default()
        else:
            return latin_fonts.get(font_type) or korean_fonts.get(font_type) or ImageFont.load_default()
    
    # 기본 폰트 할당 (텍스트별로 동적으로 선택됨)
    product_name_font_base = korean_fonts.get('name') or latin_fonts.get('name') or ImageFont.load_default()
    product_subtitle_font_base = korean_fonts.get('subtitle') or latin_fonts.get('subtitle') or ImageFont.load_default()
    product_price_font = latin_fonts.get('price') or korean_fonts.get('price') or ImageFont.load_default()
    total_price_font = latin_fonts.get('total') or korean_fonts.get('total') or ImageFont.load_default()
    
    # 첫 번째 상품 name 기준 좌표: (339.18, 711.65)
    # receipt.html 기준으로 계산하면:
    # - 첫 번째 상품 name: (554, 560) -> 이미지: (339.18, 711.65)
    # - 첫 번째 상품 subtitle: (554, 583) -> 이미지: (339.18, 약 734.65)
    # - 첫 번째 상품 가격: (839, 560) -> 이미지: (약 629.25, 711.65)
    # - 상품 간 y 간격: 48px (receipt.html 기준) -> 이미지: 약 58.32px
    
    if receipt_products:
        # 첫 번째 상품 기준 좌표
        first_name_x = 339.18
        first_name_y = 711.65
        name_subtitle_gap = 23 * (391.44 / 336)  # 약 26.8px (receipt.html: 583-560=23px)
        product_spacing_y = 48 * (391.44 / 336)  # 약 55.92px (receipt.html: 48px)
        
        # 가격 x 좌표 (일괄적으로 678로 설정)
        price_x = 678
        # 가격 텍스트 y 좌표: 첫 번째는 712, 이후 58 간격
        first_price_y = 712
        price_spacing_y = 58
        
        for idx, product in enumerate(receipt_products[:5]):
            # 각 상품의 y 좌표 계산
            product_y = first_name_y + (idx * product_spacing_y)
            # 가격 텍스트 y 좌표 계산
            price_y = first_price_y + (idx * price_spacing_y)
            
            # 상품 이름 (name x count) - 한글 포함 여부에 따라 폰트 선택, 볼드 처리
            product_name_text = f"{product['name']} x {product['count']}"
            # 볼드 폰트 사용 (한글인 경우 Noto Sans KR, 아니면 Geist SemiBold)
            if contains_korean(product_name_text):
                # 한글인 경우 Noto Sans KR 사용 (볼드 효과를 위해 크기를 약간 키움)
                product_name_font = korean_fonts.get('name') or ImageFont.load_default()
            else:
                # 영문인 경우 Geist SemiBold 사용
                product_name_font = latin_fonts.get('name') or ImageFont.load_default()
            print(f"Rendering product name [{idx}]: '{product_name_text}' (Korean: {contains_korean(product_name_text)}, Bold)")
            try:
                draw.text((first_name_x, product_y), product_name_text, fill=(0, 0, 0), font=product_name_font)  # 검은색
            except Exception as e:
                print(f"ERROR rendering product name: {e}")
                import traceback
                traceback.print_exc()
            
            # 상품 부제목 (subtitle) - 한글 포함 여부에 따라 폰트 선택
            subtitle_text = product.get('subtitle', '')
            product_subtitle_font = get_font_for_text(subtitle_text, 'subtitle')
            print(f"Rendering subtitle [{idx}]: '{subtitle_text}' (Korean: {contains_korean(subtitle_text)})")
            subtitle_y = product_y + name_subtitle_gap
            try:
                draw.text((first_name_x, subtitle_y), subtitle_text, fill=(130, 130, 130), font=product_subtitle_font)  # #828282
            except Exception as e:
                print(f"ERROR rendering subtitle: {e}")
                import traceback
                traceback.print_exc()
            
            # 상품 가격 - x 위치 678에 직접 배치 (왼쪽 끝이 678), y는 712부터 58 간격
            price_text = f"{product['total_price']:,}"
            # 가격 텍스트의 왼쪽 끝이 678가 되도록 배치
            price_text_x = price_x  # 왼쪽 끝이 678
            draw.text((price_text_x, price_y), price_text, fill=(0, 0, 0), font=product_price_font)
            
            # 토큰 유닛 이미지 추가 - 13x13 크기, (659, 717) 첫 번째, 58 간격
            token_unit_path = os.path.join(script_dir, 'static', 'images', 'main', 'token-unit-b.png')
            if os.path.exists(token_unit_path):
                try:
                    token_unit_img = Image.open(token_unit_path).convert('RGBA')
                    # 토큰 유닛 이미지 크기: 13x13
                    token_unit_size = 13
                    token_unit_img = token_unit_img.resize((token_unit_size, token_unit_size), Image.Resampling.LANCZOS)
                    
                    # 토큰 유닛 위치: 첫 번째는 (659, 714), 이후 58 간격 (3픽셀 위로 이동)
                    token_unit_x = 659
                    token_unit_y = 714 + (idx * 58)
                    
                    # RGBA 이미지를 RGB 이미지에 합성
                    receipt_img.paste(token_unit_img, (token_unit_x, token_unit_y), token_unit_img)
                except Exception as e:
                    print(f"Failed to load token unit image: {e}")
        
        # 총 가격 배치 (TOTAL 글자는 삭제)
        # 전체 가격 위치: x는 678 (상품 가격과 동일), y는 1030.5
        total_price_x = 678  # 상품 가격과 동일한 x 위치
        total_price_y = 1030.5
        
        # 총 가격 텍스트
        total_price_text = f"{total_price:,}"
        # 가격 텍스트의 왼쪽 끝이 678가 되도록 배치
        total_price_text_x = total_price_x  # 왼쪽 끝이 678
        draw.text((total_price_text_x, total_price_y), total_price_text, fill=(0, 0, 0), font=total_price_font)
        
        # 총 가격의 토큰 유닛 이미지 추가 - (659, 1036)에 배치
        token_unit_path = os.path.join(script_dir, 'static', 'images', 'main', 'token-unit-b.png')
        if os.path.exists(token_unit_path):
            try:
                token_unit_img = Image.open(token_unit_path).convert('RGBA')
                # 총 가격 토큰 유닛 크기: 13x13 (상품 가격과 동일)
                token_unit_size = 13
                token_unit_img = token_unit_img.resize((token_unit_size, token_unit_size), Image.Resampling.LANCZOS)
                
                # 토큰 유닛 위치: (659, 1033) - 3픽셀 위로 이동
                token_unit_x = 659
                token_unit_y = 1033
                
                # RGBA 이미지를 RGB 이미지에 합성
                receipt_img.paste(token_unit_img, (token_unit_x, token_unit_y), token_unit_img)
            except Exception as e:
                print(f"Failed to load total token unit image: {e}")
    
    # 2. BytesIO에 저장 (JPEG 형식, 파일 저장 없음)
    img_buffer = BytesIO()
    receipt_img.save(img_buffer, format='JPEG', quality=85, optimize=True)
    img_buffer.seek(0)
    return img_buffer

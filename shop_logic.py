import random
from datetime import date
from database import get_products

def get_shop_products(time_seed=None):
    """
    Shop 페이지에 노출할 상품 12개를 선택하는 함수
    
    Args:
        time_seed: 시간대별 랜덤 시드 (None이면 현재 날짜 기반)
    
    Returns:
        선택된 상품 ID 리스트 (12개)
    
    규칙:
    - 전체 30개 상품 중 12개 선택
    - 연결 상품군: A가 선택되면 반드시 B도 포함
    - 연결 관계:
        - 연필(01) -> 라디오(12)
        - 향초(05) -> 슬리퍼(09)
        - 스푼(22) -> 지갑(29)
        - 손전등(18) -> 리모컨(04)
        - 모자(20) -> 리모컨(04)
        - 나침반(21) -> 리모컨(04)
        - 지우개(08) -> 텀블러(03)
        - 향수병(23) -> 텀블러(03)
        - 마스크(16) -> 텀블러(03)
        - 칫솔(26) -> 열쇠고리(25)
        - 손수건(28) -> 열쇠고리(25)
        - 전등(30) -> 열쇠고리(25)
    """
    # type을 id로 변환하는 매핑 생성
    products = get_products()
    type_to_id = {product['type']: product['id'] for product in products}
    
    # 연결 관계 정의 (A -> B)
    linked_pairs = {
        '연필': '라디오',
        '향초': '슬리퍼',
        '스푼': '지갑',
        '손전등': '리모컨',
        '모자': '리모컨',
        '나침반': '리모컨',
        '지우개': '텀블러',
        '향수병': '텀블러',
        '마스크': '텀블러',
        '칫솔': '열쇠고리',
        '손수건': '열쇠고리',
        '전등': '열쇠고리'
    }
    
    # type을 id로 변환한 연결 관계
    linked_pairs_id = {}
    for a_type, b_type in linked_pairs.items():
        if a_type in type_to_id and b_type in type_to_id:
            linked_pairs_id[type_to_id[a_type]] = type_to_id[b_type]
    
    # 모든 상품 ID 리스트
    all_product_ids = [product['id'] for product in products]
    
    # 시간대별 랜덤 시드 설정
    if time_seed is None:
        # 현재 시간을 기반으로 30분 단위 시드 생성
        # 정시~29분: 정시 기준, 30분~59분: 정시 30분 기준
        from datetime import datetime
        now = datetime.now()
        # 분이 30 이상이면 30분 기준, 아니면 정시 기준
        if now.minute >= 30:
            time_key = f"{now.year}-{now.month:02d}-{now.day:02d}-{now.hour:02d}-30"
        else:
            time_key = f"{now.year}-{now.month:02d}-{now.day:02d}-{now.hour:02d}-00"
        time_seed = hash(time_key) % (2**31)
    
    random.seed(time_seed)
    
    selected_ids = set()
    remaining_ids = all_product_ids.copy()
    
    # 연결된 상품(B)인지 확인하는 집합 생성
    linked_b_ids = set(linked_pairs_id.values())
    
    # 연결 관계가 없는 상품을 찾는 함수
    def find_unlinked_product(product_set, exclude_set=None):
        """연결 관계가 없는 상품 하나를 찾아서 반환"""
        if exclude_set is None:
            exclude_set = set()
        for sid in product_set:
            if sid in exclude_set:
                continue
            is_linked_a = sid in linked_pairs_id
            is_linked_b = sid in linked_b_ids
            if not is_linked_a and not is_linked_b:
                return sid
        return None
    
    # 12개가 선택될 때까지 반복
    while len(selected_ids) < 12 and remaining_ids:
        # 랜덤하게 하나 선택
        candidate_id = random.choice(remaining_ids)
        remaining_ids.remove(candidate_id)
        
        # 선택된 상품 추가
        selected_ids.add(candidate_id)
        
        # 연결된 상품이 있으면 반드시 추가
        if candidate_id in linked_pairs_id:
            linked_id = linked_pairs_id[candidate_id]
            if linked_id not in selected_ids:
                # 연결된 상품 추가
                if linked_id in remaining_ids:
                    remaining_ids.remove(linked_id)
                selected_ids.add(linked_id)
        
        # 12개를 초과한 경우, 연결 관계가 없는 상품 하나 제거
        while len(selected_ids) > 12:
            # 이번에 추가한 상품들(candidate_id, linked_id)은 제외하고 찾음
            exclude_set = {candidate_id}
            if candidate_id in linked_pairs_id:
                exclude_set.add(linked_pairs_id[candidate_id])
            
            removable_id = find_unlinked_product(selected_ids, exclude_set)
            if removable_id:
                selected_ids.remove(removable_id)
            else:
                # 연결 관계가 없는 상품이 없으면, 연결된 상품(B) 중 하나를 제거
                # 단, 해당 B의 A가 선택되어 있으면 A도 함께 제거해야 함
                removed = False
                for b_id in linked_b_ids:
                    if b_id in selected_ids and b_id != linked_pairs_id.get(candidate_id):
                        # 이 B를 연결하는 A들을 찾음
                        linked_as = [a_id for a_id, bid in linked_pairs_id.items() if bid == b_id and a_id in selected_ids]
                        # A가 선택되어 있으면 A도 제거
                        for a_id in linked_as:
                            selected_ids.remove(a_id)
                        selected_ids.remove(b_id)
                        removed = True
                        break
                if not removed:
                    # 그래도 안되면 이번에 추가하지 않은 상품 중 하나를 제거
                    for sid in list(selected_ids):
                        if sid != candidate_id and sid != linked_pairs_id.get(candidate_id):
                            selected_ids.remove(sid)
                            break
    
    # 정확히 12개가 되도록 조정 (혹시 모를 경우를 대비)
    while len(selected_ids) > 12:
        removable_id = find_unlinked_product(selected_ids)
        if removable_id:
            selected_ids.remove(removable_id)
        else:
            # 연결 관계가 없는 상품이 없으면, 연결된 상품(B) 중 하나를 제거
            # 단, 해당 B의 A가 선택되어 있으면 A도 함께 제거해야 함
            removed = False
            for b_id in linked_b_ids:
                if b_id in selected_ids:
                    # 이 B를 연결하는 A들을 찾음
                    linked_as = [a_id for a_id, bid in linked_pairs_id.items() if bid == b_id and a_id in selected_ids]
                    # A가 선택되어 있으면 A도 제거
                    for a_id in linked_as:
                        selected_ids.remove(a_id)
                    selected_ids.remove(b_id)
                    removed = True
                    break
            if not removed:
                # 그래도 안되면 아무거나 하나 제거
                selected_ids.remove(list(selected_ids)[0])
    
    # 정렬하여 반환
    return sorted(list(selected_ids))

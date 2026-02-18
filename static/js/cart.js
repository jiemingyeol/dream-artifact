// Cart 페이지 기능 스크립트
(function() {
    'use strict';
    
    // 페이지 로드 시 스크롤 위치 복원
    function restoreScrollPosition() {
        const savedScrollPosition = sessionStorage.getItem('cartScrollPosition');
        if (savedScrollPosition !== null) {
            const scrollY = parseInt(savedScrollPosition);
            // 여러 방법으로 스크롤 복원 시도
            window.scrollTo(0, scrollY);
            document.documentElement.scrollTop = scrollY;
            document.body.scrollTop = scrollY;
            
            // requestAnimationFrame으로 한 번 더 시도 (렌더링 후)
            requestAnimationFrame(function() {
                window.scrollTo(0, scrollY);
                document.documentElement.scrollTop = scrollY;
                document.body.scrollTop = scrollY;
                
                // 약간의 지연 후 한 번 더 시도 (동적 컨텐츠 로드 대기)
                setTimeout(function() {
                    window.scrollTo(0, scrollY);
                    // 복원 후 저장된 값 삭제 (한 번만 복원)
                    sessionStorage.removeItem('cartScrollPosition');
                }, 100);
            });
        }
    }
    
    // DOMContentLoaded와 load 이벤트 모두 처리
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            restoreScrollPosition();
        });
    } else {
        restoreScrollPosition();
    }
    
    window.addEventListener('load', function() {
        // load 이벤트에서도 한 번 더 시도
        const savedScrollPosition = sessionStorage.getItem('cartScrollPosition');
        if (savedScrollPosition !== null) {
            const scrollY = parseInt(savedScrollPosition);
            window.scrollTo(0, scrollY);
            document.documentElement.scrollTop = scrollY;
            document.body.scrollTop = scrollY;
        }
    });
    
    // 스크롤 위치 저장 함수
    function saveScrollPosition() {
        const scrollY = window.pageYOffset || window.scrollY || document.documentElement.scrollTop || document.body.scrollTop || 0;
        sessionStorage.setItem('cartScrollPosition', scrollY.toString());
    }
    
    // 수량 감소 버튼 클릭 이벤트
    document.querySelectorAll('.cart-decrease-btn').forEach(function(btn) {
        btn.addEventListener('click', function() {
            // 수량이 1일 때는 클릭 불가
            if (this.style.pointerEvents === 'none') {
                return;
            }
            const productId = this.getAttribute('data-product-id');
            const index = parseInt(this.getAttribute('data-index'));
            saveScrollPosition();
            updateCartQuantity(productId, -1, index);
        });
    });
    
    // 수량 증가 버튼 클릭 이벤트
    document.querySelectorAll('.cart-increase-btn').forEach(function(btn) {
        btn.addEventListener('click', function() {
            const productId = this.getAttribute('data-product-id');
            const index = parseInt(this.getAttribute('data-index'));
            saveScrollPosition();
            updateCartQuantity(productId, 1, index);
        });
    });
    
    // 삭제 버튼 클릭 이벤트
    document.querySelectorAll('.cart-delete-btn').forEach(function(btn) {
        btn.addEventListener('click', function() {
            const productId = this.getAttribute('data-product-id');
            saveScrollPosition();
            deleteCartItem(productId);
        });
    });
    
    function updateCartQuantity(productId, change, index) {
        fetch('/api/update-cart-quantity', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                product_id: productId,
                change: change
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // 페이지 새로고침으로 업데이트
                window.location.reload();
            } else {
                // 모달로 에러 메시지 표시
                if (typeof customAlert !== 'undefined') {
                    customAlert(data.message || '수량 변경에 실패했습니다.');
                } else {
                    alert(data.message || '수량 변경에 실패했습니다.');
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
            if (typeof customAlert !== 'undefined') {
                customAlert('수량 변경 중 오류가 발생했습니다.');
            } else {
                alert('수량 변경 중 오류가 발생했습니다.');
            }
        });
    }
    
    function deleteCartItem(productId) {
        if (typeof customConfirm !== 'undefined') {
            customConfirm('상품을 장바구니에서 삭제하시겠습니까?').then(function(result) {
                if (result) {
                    performDelete(productId);
                }
            });
        } else {
            if (confirm('상품을 장바구니에서 삭제하시겠습니까?')) {
                performDelete(productId);
            }
        }
    }
    
    function performDelete(productId) {
        fetch('/api/delete-cart-item', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                product_id: productId
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.reload();
            } else {
                if (typeof customAlert !== 'undefined') {
                    customAlert(data.message || '삭제에 실패했습니다.');
                } else {
                    alert(data.message || '삭제에 실패했습니다.');
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
            if (typeof customAlert !== 'undefined') {
                customAlert('삭제 중 오류가 발생했습니다.');
            } else {
                alert('삭제 중 오류가 발생했습니다.');
            }
        });
    }
    
    // 주문하기 버튼 클릭 이벤트
    const orderButton = document.querySelector('.order-button');
    if (orderButton) {
        orderButton.addEventListener('click', function() {
            handleOrderClick();
        });
    }
    
    function handleOrderClick() {
        // 데이터 가져오기
        const customerToken = window.cartData.customerToken || 0;
        const totalPrice = window.cartData.totalPrice || 0;
        const cartCount = window.cartData.cartCount || 0;
        const buyData = window.cartData.buyData || '';
        
        // 케이스 3: 물건을 아예 안 담은 경우
        if (!buyData || buyData.trim() === '' || cartCount === 0) {
            if (typeof customModal !== 'undefined') {
                customModal('제품 개수 부족', '물건을 아예 안 담으셨군요!\n쇼핑을 해서 장바구니에 물건을 담아주세요!', '확인');
            } else {
                alert('[제품 개수 부족]\n물건을 아예 안 담으셨군요! 쇼핑을 해서 장바구니에 물건을 담아주세요!');
            }
            return;
        }
        
        // 케이스 2: 5개 초과로 상품을 담은 경우
        if (cartCount > 5) {
            if (typeof customModal !== 'undefined') {
                customModal('구매 가능 개수 초과', '구매 가능한 제품의 개수를 초과하여 담았습니다.\n장바구니를 다시 확인하신 후 다시 시도해 주세요.', '확인');
            } else {
                alert('[구매 가능 개수 초과]\n구매 가능한 제품의 개수를 초과하여 담았습니다. 장바구니를 다시 확인하신 후 다시 시도해 주세요.');
            }
            return;
        }
        
        // 케이스 1: 보유 토큰보다 전체 상품 금액 합산이 더 큰 경우
        if (totalPrice > customerToken) {
            if (typeof customModal !== 'undefined') {
                customModal('드림 토큰 부족', '보유한 드림 토큰을 초과하여 제품을 담았습니다.\n장바구니에서 금액을 확인하신 후 다시 시도해 주세요.', '확인');
            } else {
                alert('[드림 토큰 부족]\n보유한 드림 토큰을 초과하여 제품을 담았습니다. 장바구니에서 금액을 확인하신 후 다시 시도해 주세요.');
            }
            return;
        }
        
        // 케이스 4: 정상 케이스
        if (typeof customModal !== 'undefined') {
            customModal('주문 가능', '물건을 모두 고르셨다면 아래의 주문 버튼을 눌러주세요.', '주문', function(modalElement, overlayElement) {
                // 결제 반영(상품별 구매수 누적) 후 로딩 표시
                fetch('/api/checkout', { method: 'POST', headers: { 'Content-Type': 'application/json' } })
                    .then(function(r) { return r.json(); })
                    .then(function(data) {
                        if (data.success) {
                            showLoadingInModal(modalElement);
                        } else {
                            if (typeof customAlert !== 'undefined') customAlert(data.message || '결제 반영에 실패했습니다.');
                        }
                    })
                    .catch(function() {
                        if (typeof customAlert !== 'undefined') customAlert('결제 처리 중 오류가 발생했습니다.');
                    });
                return false;
            }, '취소', function() {});
        } else {
            if (confirm('물건을 모두 고르셨다면 주문 버튼을 눌러주세요.')) {
                fetch('/api/checkout', { method: 'POST', headers: { 'Content-Type': 'application/json' } })
                    .then(function(r) { return r.json(); })
                    .then(function(data) {
                        if (data.success) showLoadingAndRedirect();
                        else alert(data.message || '결제 반영에 실패했습니다.');
                    })
                    .catch(function() { alert('결제 처리 중 오류가 발생했습니다.'); });
            }
        }
    }
    
    function showLoadingInModal(modalElement) {
        // 모달 내부의 모든 내용 제거
        while (modalElement.firstChild) {
            modalElement.removeChild(modalElement.firstChild);
        }
        
        // 모달 스타일 변경 (중앙 정렬)
        modalElement.style.display = 'flex';
        modalElement.style.alignItems = 'center';
        modalElement.style.justifyContent = 'center';
        modalElement.style.padding = '0';
        
        // 로딩 아이콘 생성 (모달 중앙에 배치)
        const loadingIcon = document.createElement('div');
        loadingIcon.id = 'order-loading-icon-modal';
        loadingIcon.style.cssText = 'width: calc(94 / 1440 * 100vw); height: calc(94 / 1440 * 100vw); border-radius: 50%; background: conic-gradient(from 0deg, #FFAAFF 0deg 72deg, #D9D9D9 72deg 360deg); mask-image: radial-gradient(circle, transparent calc(50% - 5.25px), black calc(50% - 5.25px)); -webkit-mask-image: radial-gradient(circle, transparent calc(50% - 5.25px), black calc(50% - 5.25px)); animation: spin 1s linear infinite;';
        
        // spin 애니메이션 스타일 추가 (아직 없으면)
        if (!document.getElementById('loading-spin-style')) {
            const style = document.createElement('style');
            style.id = 'loading-spin-style';
            style.textContent = '@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }';
            document.head.appendChild(style);
        }
        
        modalElement.appendChild(loadingIcon);
        
        // 스크롤 방지를 위해 body에 클래스 추가
        document.body.classList.add('loading-active');
        
        // 스크롤 이벤트 방지
        function preventScroll(e) {
            e.preventDefault();
            e.stopPropagation();
            return false;
        }
        window.addEventListener('wheel', preventScroll, { passive: false });
        window.addEventListener('touchmove', preventScroll, { passive: false });
        window.addEventListener('scroll', preventScroll, { passive: false });
        
        // 5초 후 영수증 페이지로 이동
        setTimeout(function() {
            // 이벤트 리스너 제거
            window.removeEventListener('wheel', preventScroll);
            window.removeEventListener('touchmove', preventScroll);
            window.removeEventListener('scroll', preventScroll);
            document.body.classList.remove('loading-active');
            window.location.href = window.receiptUrl || '/receipt';
        }, 5000);
        
        // 모달을 닫지 않도록 false 반환
        return false;
    }
    
    function showLoadingAndRedirect() {
        // 기존 로딩 아이콘이 있으면 제거
        const existingLoading = document.getElementById('order-loading-icon');
        if (existingLoading) {
            existingLoading.remove();
        }
        const existingOverlay = document.getElementById('loading-overlay');
        if (existingOverlay) {
            existingOverlay.remove();
        }
        
        // 스크롤 방지를 위해 body에 클래스 추가
        document.body.classList.add('loading-active');
        
        // 전체 화면 오버레이 생성 (클릭 방지)
        const loadingOverlay = document.createElement('div');
        loadingOverlay.className = 'loading-overlay';
        loadingOverlay.id = 'loading-overlay';
        document.body.appendChild(loadingOverlay);
        
        // 로딩 아이콘 생성
        const loadingIcon = document.createElement('div');
        loadingIcon.className = 'loading-icon';
        loadingIcon.id = 'order-loading-icon';
        document.body.appendChild(loadingIcon);
        
        // 스크롤 이벤트 방지
        function preventScroll(e) {
            e.preventDefault();
            e.stopPropagation();
            return false;
        }
        window.addEventListener('wheel', preventScroll, { passive: false });
        window.addEventListener('touchmove', preventScroll, { passive: false });
        window.addEventListener('scroll', preventScroll, { passive: false });
        
        // 5초 후 영수증 페이지로 이동
        setTimeout(function() {
            // 이벤트 리스너 제거
            window.removeEventListener('wheel', preventScroll);
            window.removeEventListener('touchmove', preventScroll);
            window.removeEventListener('scroll', preventScroll);
            document.body.classList.remove('loading-active');
            window.location.href = window.receiptUrl || '/receipt';
        }, 5000);
    }
})();

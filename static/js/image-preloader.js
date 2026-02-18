// 이미지 프리로더: 로딩된 이미지부터 바로 표시 (한 번에 대기하지 않음, 단일 이미지 상단→하단 로딩만 방지)
(function() {
    'use strict';
    
    // 이미지 프리로드 함수 (브라우저 캐시에 저장)
    window.preloadImages = function(imageUrls) {
        const promises = imageUrls.map(url => {
            return new Promise((resolve) => {
                const img = new Image();
                img.onload = () => resolve(img);
                img.onerror = () => resolve(img);
                img.src = url;
            });
        });
        return Promise.all(promises);
    };
    
    // 각 이미지를 개별 로드하고, 로드 완료된 것부터 바로 표시 (전체 대기 없음)
    // 단, 한 개 이미지가 위→아래로 천천히 보이는 것은 방지: 완전히 로드된 뒤 한 번에 표시
    function preloadAndShowImages() {
        const images = document.querySelectorAll('img');
        
        images.forEach((img) => {
            const src = img.getAttribute('src');
            if (!src) return;
            
            let absoluteUrl;
            if (src.startsWith('http://') || src.startsWith('https://')) {
                absoluteUrl = src;
            } else if (src.startsWith('/')) {
                absoluteUrl = window.location.origin + src;
            } else {
                absoluteUrl = new URL(src, window.location.href).href;
            }
            
            // 이미 완전히 로드된 이미지는 그대로 두기
            if (img.complete && img.naturalHeight > 0) return;
            
            // src 제거 후 data-src에 보관 → 한 장씩 위에서부터 채워지는 현상 방지
            // visibility: hidden으로 로드 전 깨진 이미지 아이콘 미표시
            img.setAttribute('data-src', absoluteUrl);
            img.removeAttribute('src');
            img.style.opacity = '0';
            img.style.visibility = 'hidden';
            
            const tempImg = new Image();
            tempImg.onload = () => {
                img.src = absoluteUrl;
                img.style.visibility = 'visible';
                img.style.opacity = '1';
                const isIntroPage = img.closest('.bg-desktop') !== null;
                img.style.transition = isIntroPage ? 'opacity 0.5s ease-in' : 'opacity 0.1s ease-in';
            };
            tempImg.onerror = () => {
                img.src = absoluteUrl;
                img.style.visibility = 'visible';
                img.style.opacity = '1';
                const isIntroPage = img.closest('.bg-desktop') !== null;
                img.style.transition = isIntroPage ? 'opacity 0.5s ease-in' : 'opacity 0.1s ease-in';
            };
            tempImg.src = absoluteUrl;
        });
    }
    
    // 현재 페이지의 모든 이미지 로딩 완료 대기 (다른 곳에서 사용할 수 있도록 유지)
    window.waitForImages = function() {
        return new Promise((resolve) => {
            const images = document.querySelectorAll('img');
            let loadedCount = 0;
            const totalCount = images.length;
            if (totalCount === 0) {
                resolve();
                return;
            }
            images.forEach((img) => {
                if (img.complete && img.naturalHeight !== 0) {
                    loadedCount++;
                    if (loadedCount === totalCount) resolve();
                    return;
                }
                const onDone = () => {
                    loadedCount++;
                    if (loadedCount === totalCount) resolve();
                };
                img.addEventListener('load', onDone, { once: true });
                img.addEventListener('error', onDone, { once: true });
                if (img.complete) onDone();
            });
            setTimeout(resolve, 5000);
        });
    };
    
    // 페이지 전환 시 사용: body 숨긴 뒤 이미지 전부 로딩 후 표시 (기존 API 유지)
    window.showPageAfterImagesLoad = function() {
        document.body.style.opacity = '0';
        document.body.style.transition = 'opacity 0.3s ease-in';
        document.body.style.visibility = 'hidden';
        waitForImages().then(() => {
            document.body.style.visibility = 'visible';
            document.body.style.opacity = '1';
        });
    };
    
    function initImagePreloader() {
        if (document.body) {
            document.body.style.opacity = '0';
            document.body.style.transition = 'opacity 0.3s ease-in';
            document.body.style.visibility = 'hidden';
        }
        
        function showBodyAndStartImageLoad() {
            if (document.body) {
                document.body.style.visibility = 'visible';
                document.body.style.opacity = '1';
            }
            preloadAndShowImages();
        }
        
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                setTimeout(showBodyAndStartImageLoad, 50);
            });
        } else {
            setTimeout(showBodyAndStartImageLoad, 50);
        }
    }
    
    initImagePreloader();
})();

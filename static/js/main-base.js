// Main 페이지 공통 JavaScript
// 1440px 기준 디자인을 실제 화면 크기에 맞춰 스케일링

(function() {
    'use strict';
    
    const DESIGN_WIDTH = 1440;
    const container = document.querySelector('.main-container');
    
    if (!container) return;
    
    function updateScale() {
        const viewportWidth = window.innerWidth;
        
        // CSS 변수로 컨테이너 너비 저장 (내부 요소에서 사용 가능)
        // 컨테이너는 항상 화면 너비에 맞춤
        container.style.setProperty('--container-width', viewportWidth + 'px');
        container.style.setProperty('--scale-ratio', viewportWidth / DESIGN_WIDTH);
    }
    
    // 초기 실행
    updateScale();
    
    // 리사이즈 이벤트 리스너
    let resizeTimer;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(updateScale, 100);
    });
    
    // 콘텐츠 변경 감지 (MutationObserver)
    const observer = new MutationObserver(function() {
        updateScale();
    });
    
    observer.observe(container, {
        childList: true,
        subtree: true,
        attributes: true,
        attributeFilter: ['style', 'class']
    });
    
})();

(function() {
    'use strict';
    
    // 초기 컨테이너 높이
    const INITIAL_HEIGHT = 4550;
    
    // 각 토글의 높이 감소량
    const TOGGLE_HEIGHTS = {
        1: 408,
        2: 278,
        3: 1618
    };
    
    // 토글 상태 추적 (false = 펼쳐짐, true = 접힘)
    const toggleStates = {
        1: false,
        2: false,
        3: false
    };
    
    // 컨테이너 요소 가져오기
    const container = document.querySelector('.main-container');
    
    // 요소의 원래 위치 저장
    const originalPositions = new Map();
    
    // 요소의 원래 높이 저장
    const originalHeights = new Map();
    
    // 요소의 top 값을 가져오기 (인라인 스타일 또는 계산된 스타일에서)
    function getTopValue(element) {
        // 먼저 인라인 스타일 확인
        const inlineStyle = element.style.top;
        if (inlineStyle) {
            const match = inlineStyle.match(/calc\((\d+(?:\.\d+)?)\s*\/\s*1440/);
            if (match) {
                return parseFloat(match[1]);
            }
        }
        
        // 인라인 스타일이 없으면 계산된 스타일 확인
        const style = window.getComputedStyle(element);
        const topStr = style.top;
        if (!topStr) return 0;
        const match = topStr.match(/calc\((\d+(?:\.\d+)?)\s*\/\s*1440/);
        return match ? parseFloat(match[1]) : 0;
    }
    
    // 요소의 top 값 설정
    function setTopValue(element, top) {
        element.style.top = `calc(${top} / 1440 * var(--container-width))`;
    }
    
    // 요소가 속한 섹션들 확인
    function getSectionsForElement(element) {
        const sections = [];
        for (let i = 1; i <= 3; i++) {
            if (element.classList.contains(`toggle-section-${i}`)) {
                sections.push(i);
            }
        }
        return sections;
    }
    
    // 요소의 높이 가져오기
    function getElementHeight(element) {
        const style = window.getComputedStyle(element);
        const height = style.height;
        if (!height) return 0;
        // px 단위인 경우
        if (height.includes('px')) {
            return parseFloat(height);
        }
        // calc 형식인 경우
        const match = height.match(/calc\((\d+(?:\.\d+)?)\s*\/\s*1440/);
        if (match) {
            // 컨테이너 너비를 대략적으로 계산 (실제로는 더 정확한 계산 필요)
            const containerWidth = container.offsetWidth || 1440;
            return (parseFloat(match[1]) / 1440) * containerWidth;
        }
        return parseFloat(height) || 0;
    }
    
    // 모든 요소의 원래 위치 및 높이 저장
    function saveOriginalPositions() {
        // 모든 toggle-section 요소들의 원래 위치 저장
        for (let i = 1; i <= 3; i++) {
            const elements = document.querySelectorAll(`.toggle-section-${i}`);
            elements.forEach(element => {
                if (!originalPositions.has(element)) {
                    // HTML의 인라인 스타일에서 직접 읽기
                    const inlineStyle = element.getAttribute('style');
                    if (inlineStyle) {
                        // top: calc(1640 / 1440 * var(--container-width)) 형식 매칭
                        const match = inlineStyle.match(/top:\s*calc\((\d+(?:\.\d+)?)\s*\/\s*1440/);
                        if (match) {
                            originalPositions.set(element, parseFloat(match[1]));
                            return; // 저장했으면 다음으로
                        }
                    }
                    // 인라인 스타일에서 찾지 못했으면 현재 계산된 값 사용
                    const currentTop = getTopValue(element);
                    if (currentTop > 0) {
                        originalPositions.set(element, currentTop);
                    }
                }
            });
        }
        
        // 숨겨질 요소들의 원래 높이 저장
        for (let i = 1; i <= 3; i++) {
            const hideElements = document.querySelectorAll(`.toggle-hide-${i}`);
            hideElements.forEach(element => {
                if (!originalHeights.has(element)) {
                    const height = getElementHeight(element);
                    if (height > 0) {
                        originalHeights.set(element, height);
                        // 초기 max-height 설정
                        element.style.maxHeight = height + 'px';
                    }
                }
            });
        }
    }
    
    // 애니메이션 진행 중인지 추적
    let isAnimating = false;
    
    // 선형 애니메이션으로 요소 위치 업데이트
    function animatePositions(duration = 500) {
        if (isAnimating) return;
        isAnimating = true;
        
        const startTime = performance.now();
        const startPositions = new Map();
        
        // 현재 위치 저장
        originalPositions.forEach((originalTop, element) => {
            const currentTop = getTopValue(element);
            startPositions.set(element, currentTop);
        });
        
        function animate(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1); // 0에서 1까지
            
            // 선형 보간
            originalPositions.forEach((originalTop, element) => {
                const sections = getSectionsForElement(element);
                
                // 최종 오프셋 계산
                let finalOffset = 0;
                sections.forEach(sectionNum => {
                    if (toggleStates[sectionNum]) {
                        finalOffset += TOGGLE_HEIGHTS[sectionNum];
                    }
                });
                
                // 시작 위치와 최종 위치
                const startTop = startPositions.get(element);
                const finalTop = originalTop - finalOffset;
                
                // 선형 보간으로 현재 위치 계산
                const currentTop = startTop + (finalTop - startTop) * progress;
                setTopValue(element, currentTop);
            });
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            } else {
                isAnimating = false;
            }
        }
        
        requestAnimationFrame(animate);
    }
    
    // 모든 요소의 위치를 원래 위치 기준으로 재계산 (애니메이션 지원)
    function recalculateAllPositions(animated = true) {
        if (animated) {
            animatePositions(500);
        } else {
            // 애니메이션 없이 즉시 업데이트
            originalPositions.forEach((originalTop, element) => {
                const sections = getSectionsForElement(element);
                
                let totalOffset = 0;
                sections.forEach(sectionNum => {
                    if (toggleStates[sectionNum]) {
                        totalOffset += TOGGLE_HEIGHTS[sectionNum];
                    }
                });
                
                const newTop = originalTop - totalOffset;
                setTopValue(element, newTop);
            });
        }
    }
    
    // 현재 컨테이너 높이 가져오기
    function getCurrentHeight() {
        const currentHeightStr = container.style.height;
        if (!currentHeightStr) {
            return INITIAL_HEIGHT;
        }
        const match = currentHeightStr.match(/calc\((\d+(?:\.\d+)?)\s*\/\s*1440/);
        return match ? parseFloat(match[1]) : INITIAL_HEIGHT;
    }
    
    // 컨테이너 높이 계산
    function calculateContainerHeight() {
        let totalHeight = INITIAL_HEIGHT;
        for (let i = 1; i <= 3; i++) {
            if (toggleStates[i]) {
                totalHeight -= TOGGLE_HEIGHTS[i];
            }
        }
        return totalHeight;
    }
    
    // 컨테이너 높이 설정 (애니메이션)
    function updateContainerHeight(animated = true) {
        const targetHeight = calculateContainerHeight();
        
        if (animated) {
            const startHeight = getCurrentHeight();
            const startTime = performance.now();
            const duration = 500;
            
            function animateHeight(currentTime) {
                const elapsed = currentTime - startTime;
                const progress = Math.min(elapsed / duration, 1);
                
                // 선형 보간
                const currentHeight = startHeight + (targetHeight - startHeight) * progress;
                container.style.height = `calc(${currentHeight} / 1440 * var(--container-width))`;
                
                if (progress < 1) {
                    requestAnimationFrame(animateHeight);
                }
            }
            
            requestAnimationFrame(animateHeight);
        } else {
            container.style.height = `calc(${targetHeight} / 1440 * var(--container-width))`;
        }
    }
    
    // 토글 텍스트 변경
    function updateToggleText(toggleNum, isCollapsed) {
        const toggleElement = document.querySelector(`.toggle-text-${toggleNum}`);
        if (toggleElement) {
            toggleElement.textContent = isCollapsed ? '+' : '-';
        }
    }
    
    // 토글 버튼 클릭 이벤트 설정 (wrapper 사용)
    function setupToggleClick(toggleNum, wrapperElement) {
        wrapperElement.addEventListener('click', function() {
            const toggleElement = document.querySelector(`.toggle-text-${toggleNum}`);
            if (!toggleElement) return;
            
            const isCollapsed = toggleStates[toggleNum];
            
            // 토글 상태 변경
            toggleStates[toggleNum] = !isCollapsed;
            
            // 숨길 요소들 처리
            const hideSelector = `.toggle-hide-${toggleNum}`;
            const hideElements = document.querySelectorAll(hideSelector);
            
            if (!isCollapsed) {
                // 접기: 요소 숨기기 (애니메이션)
                hideElements.forEach(element => {
                    // 높이를 0으로 줄이기
                    element.style.maxHeight = '0px';
                    element.style.opacity = '0';
                    element.style.visibility = 'hidden';
                    element.style.marginTop = '0px';
                    element.style.marginBottom = '0px';
                    element.style.paddingTop = '0px';
                    element.style.paddingBottom = '0px';
                    // 애니메이션 후 display none
                    setTimeout(() => {
                        element.style.display = 'none';
                    }, 500);
                });
            } else {
                // 펼치기: 요소 보이기 (애니메이션)
                hideElements.forEach(element => {
                    element.style.display = '';
                    const originalHeight = originalHeights.get(element);
                    if (originalHeight) {
                        element.style.maxHeight = originalHeight + 'px';
                    }
                    // display를 먼저 설정한 후 애니메이션
                    setTimeout(() => {
                        element.style.opacity = '1';
                        element.style.visibility = 'visible';
                        element.style.marginTop = '';
                        element.style.marginBottom = '';
                        element.style.paddingTop = '';
                        element.style.paddingBottom = '';
                    }, 10);
                });
            }
            
            // 토글 텍스트 변경
            updateToggleText(toggleNum, !isCollapsed);
            
            // 컨테이너 높이 업데이트
            updateContainerHeight();
            
            // 모든 요소의 위치를 원래 위치 기준으로 재계산
            // requestAnimationFrame 내부에서 처리되므로 부드러운 애니메이션 보장
            recalculateAllPositions();
        });
    }
    
    // 토글 기능 구현
    function setupToggle(toggleNum) {
        // wrapper 요소 찾기
        const wrapperElement = document.querySelector(`.toggle-text-${toggleNum}-wrapper`);
        if (wrapperElement) {
            setupToggleClick(toggleNum, wrapperElement);
        } else {
            // fallback: 기존 방식 (wrapper가 없는 경우)
            const toggleElement = document.querySelector(`.toggle-text-${toggleNum}`);
            if (!toggleElement) return;
            
            setupToggleClick(toggleNum, toggleElement);
        }
    }
    
    // 모든 토글 초기화
    function initToggles() {
        // 원래 위치 저장
        saveOriginalPositions();
        
        // 각 토글 설정
        setupToggle(1);
        setupToggle(2);
        setupToggle(3);
    }
    
    // DOM이 로드된 후 초기화
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            // 약간의 지연을 두어 스타일이 적용된 후 위치 저장
            setTimeout(initToggles, 50);
        });
    } else {
        setTimeout(initToggles, 50);
    }
})();

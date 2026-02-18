// 로고 클릭 시 초기 화면으로 돌아가기 + Next 버튼 호버 시 이미지 변경
// 모든 intro 페이지에서 공통으로 사용
(function() {
    const logoLink = document.getElementById('logoLink');
    if (logoLink) {
        logoLink.addEventListener('click', async function() {
            const intro1Url = logoLink.dataset.intro1Url || '/intro1';
            const confirmed = await customConfirm('초기 화면으로 돌아가시겠습니까?\n모든 진행 상황이 초기화됩니다.');
            if (confirmed) {
                window.location.href = intro1Url;
            }
        });
    }

    // Next 버튼: 호버 시 next-button-hover 이미지로 변경
    const nextButtonImgs = document.querySelectorAll('img[src*="next-button.png"], img[data-src*="next-button.png"]');
    nextButtonImgs.forEach(function(img) {
        const parent = img.closest('a') || img.closest('button');
        if (!parent) return;
        const defaultSrc = (img.src || img.getAttribute('src') || img.getAttribute('data-src') || '').toString();
        const hoverSrc = defaultSrc.replace('next-button.png', 'next-button-hover.png');
        if (!defaultSrc || hoverSrc === defaultSrc) return;
        parent.addEventListener('mouseenter', function() {
            img.src = hoverSrc;
        });
        parent.addEventListener('mouseleave', function() {
            img.src = defaultSrc;
        });
    });

    // Back 버튼 (intro8): 호버 시 back-button-hover 이미지로 변경
    const backButtonImgs = document.querySelectorAll('img[src*="back-button.png"], img[data-src*="back-button.png"]');
    backButtonImgs.forEach(function(img) {
        const parent = img.closest('a') || img.closest('button');
        if (!parent) return;
        const defaultSrc = (img.src || img.getAttribute('src') || img.getAttribute('data-src') || '').toString();
        const hoverSrc = defaultSrc.replace('back-button.png', 'back-button-hover.png');
        if (!defaultSrc || hoverSrc === defaultSrc) return;
        parent.addEventListener('mouseenter', function() {
            img.src = hoverSrc;
        });
        parent.addEventListener('mouseleave', function() {
            img.src = defaultSrc;
        });
    });

    // Skip 버튼 (intro6, intro7): 호버 시 skip-button-hover 이미지로 변경
    const skipButtonImgs = document.querySelectorAll('img[src*="skip-button.png"], img[data-src*="skip-button.png"]');
    skipButtonImgs.forEach(function(img) {
        const parent = img.closest('a') || img.closest('button');
        if (!parent) return;
        const defaultSrc = (img.src || img.getAttribute('src') || img.getAttribute('data-src') || '').toString();
        const hoverSrc = defaultSrc.replace('skip-button.png', 'skip-button-hover.png');
        if (!defaultSrc || hoverSrc === defaultSrc) return;
        parent.addEventListener('mouseenter', function() {
            img.src = hoverSrc;
        });
        parent.addEventListener('mouseleave', function() {
            img.src = defaultSrc;
        });
    });
})();

// 커스텀 모달 시스템 - 전체화면 모드 유지
(function() {
    'use strict';
    
    // 모달 스타일 추가
    const style = document.createElement('style');
    style.textContent = `
        .custom-modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.7);
            z-index: 10000;
            display: flex;
            align-items: center;
            justify-content: center;
            backdrop-filter: blur(4px);
            pointer-events: auto;
        }
        
        .custom-modal {
            background-color: #FFFFFF;
            border: calc(2 / 1440 * 100vw) solid #444;
            border-radius: calc(12 / 1440 * 100vw);
            padding: calc(24 / 1440 * 100vw) calc(32 / 1440 * 100vw);
            width: calc(430 / 1440 * 100vw);
            height: calc(209 / 810 * 100vh);
            box-shadow: 0 calc(8 / 1440 * 100vw) calc(32 / 1440 * 100vw) rgba(0, 0, 0, 0.5);
            text-align: center;
            color: #000000;
            font-family: 'Inter', sans-serif;
            pointer-events: auto;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            align-items: center;
            position: relative;
            padding-top: calc(28 / 1440 * 100vw);
        }
        
        .custom-modal-title {
            font-size: calc(20 / 1440 * 100vw);
            font-weight: 700;
            line-height: 1.4;
            letter-spacing: 0;
            margin-bottom: calc(16 / 810 * 100vh);
            margin-top: 0;
            white-space: pre-line;
            color: #000000;
            font-family: 'Inter', sans-serif;
        }
        
        .custom-modal-message {
            font-size: calc(16 / 1440 * 100vw);
            font-weight: 400;
            line-height: 1.4;
            letter-spacing: 0;
            margin-bottom: calc(20 / 810 * 100vh);
            color: #000000;
            font-family: 'Inter', sans-serif;
        }
        
        .custom-modal-buttons {
            position: absolute;
            bottom: calc(20 / 810 * 100vh);
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: calc(12 / 1440 * 100vw);
            justify-content: center;
        }
        
        .custom-modal-button {
            min-width: calc(90 / 1440 * 100vw);
            width: auto;
            height: calc(35 / 810 * 100vh);
            padding: 0 calc(16 / 1440 * 100vw);
            border: calc(2 / 1440 * 100vw) solid;
            border-radius: calc(6 / 1440 * 100vw);
            font-size: calc(15 / 1440 * 100vw);
            font-weight: 600;
            cursor: pointer;
            transition: opacity 0.2s, transform 0.1s;
            font-family: 'Inter', sans-serif;
            display: flex;
            align-items: center;
            justify-content: center;
            white-space: nowrap;
        }
        
        .custom-modal-button:hover {
            opacity: 0.8;
            transform: scale(1.05);
        }
        
        .custom-modal-button:active {
            transform: scale(0.95);
        }
        
        .custom-modal-button-confirm {
            background-color: #FFAAFF;
            color: #000000;
            border-color: #FFAAFF;
        }
        
        .custom-modal-button-confirm:hover {
            background-color: #ff88ff;
            border-color: #ff88ff;
        }
        
        .custom-modal-button-cancel {
            background-color: #D9D9D9;
            color: #000000;
            border-color: #D9D9D9;
        }
        
        .custom-modal-button-cancel:hover {
            background-color: #c0c0c0;
            border-color: #c0c0c0;
        }
        
        .custom-modal-button-ok {
            background-color: #FFAAFF;
            color: #000000;
            border-color: #FFAAFF;
        }
        
        .custom-modal-button-ok:hover {
            background-color: #ff88ff;
            border-color: #ff88ff;
        }
        
        .custom-modal-close-button {
            position: absolute;
            width: calc(209 / 16 / 1440 * 100vw);
            height: calc(209 / 16 / 1440 * 100vw);
            right: calc((209 / 16 / 2) / 1440 * 100vw);
            top: calc(209 / 16 / 2 / 810 * 100vh);
            background-color: #D9D9D9;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 10001;
            pointer-events: auto;
            cursor: pointer;
        }
        
        .custom-modal-close-button:hover {
            opacity: 0.8;
        }
        
        .custom-modal-close-icon {
            width: calc(209 / 16 / 2 / 1440 * 100vw);
            height: calc(209 / 16 / 2 / 1440 * 100vw);
            position: relative;
            pointer-events: none;
        }
        
        .custom-modal-close-icon::before,
        .custom-modal-close-icon::after {
            content: '';
            position: absolute;
            width: calc(209 / 16 / 2 / 1440 * 100vw);
            height: calc(1 / 1440 * 100vw);
            background-color: #000000;
            top: 50%;
            left: 50%;
        }
        
        .custom-modal-close-icon::before {
            transform: translate(-50%, -50%) rotate(45deg);
        }
        
        .custom-modal-close-icon::after {
            transform: translate(-50%, -50%) rotate(-45deg);
        }
    `;
    document.head.appendChild(style);
    
    // 전체화면 모드 유지 함수
    function maintainFullscreen() {
        if (document.fullscreenElement || document.webkitFullscreenElement || 
            document.mozFullScreenElement || document.msFullscreenElement) {
            // 이미 전체화면 모드
            return;
        }
        
        const element = document.documentElement;
        if (element.requestFullscreen) {
            element.requestFullscreen().catch(() => {});
        } else if (element.webkitRequestFullscreen) {
            element.webkitRequestFullscreen();
        } else if (element.mozRequestFullScreen) {
            element.mozRequestFullScreen();
        } else if (element.msRequestFullscreen) {
            element.msRequestFullscreen();
        }
    }
    
    // 커스텀 alert 함수
    window.customAlert = function(message) {
        return new Promise((resolve) => {
            maintainFullscreen();
            
            const overlay = document.createElement('div');
            overlay.className = 'custom-modal-overlay';
            
            const modal = document.createElement('div');
            modal.className = 'custom-modal';
            
            const titleDiv = document.createElement('div');
            titleDiv.className = 'custom-modal-title';
            titleDiv.textContent = '[알림]';
            titleDiv.style.whiteSpace = 'pre-line';
            
            const messageDiv = document.createElement('div');
            messageDiv.className = 'custom-modal-message';
            messageDiv.textContent = message;
            messageDiv.style.whiteSpace = 'pre-line';
            
            // 메시지 줄 수 확인 (한 줄일 때 줄 높이만큼 y 위치 내림)
            const lineCount = (message.match(/\n/g) || []).length + 1;
            if (lineCount === 1) {
                messageDiv.style.marginTop = '1.4em'; // 줄 높이(line-height)만큼
            }
            
            const buttonsDiv = document.createElement('div');
            buttonsDiv.className = 'custom-modal-buttons';
            
            const okButton = document.createElement('button');
            okButton.className = 'custom-modal-button custom-modal-button-ok';
            okButton.textContent = '확인';
            
            okButton.addEventListener('click', () => {
                document.body.removeChild(overlay);
                resolve();
            });
            
            // 닫기 버튼 추가
            const closeButton = document.createElement('div');
            closeButton.className = 'custom-modal-close-button';
            const closeIcon = document.createElement('div');
            closeIcon.className = 'custom-modal-close-icon';
            closeButton.appendChild(closeIcon);
            
            closeButton.addEventListener('click', (e) => {
                e.stopPropagation();
                e.preventDefault();
                document.body.removeChild(overlay);
                document.removeEventListener('keydown', escHandler);
                resolve();
            });
            
            buttonsDiv.appendChild(okButton);
            modal.appendChild(titleDiv);
            modal.appendChild(messageDiv);
            modal.appendChild(buttonsDiv);
            modal.appendChild(closeButton);
            overlay.appendChild(modal);
            document.body.appendChild(overlay);
            
            // ESC 키로 닫기
            const escHandler = (e) => {
                if (e.key === 'Escape') {
                    document.body.removeChild(overlay);
                    document.removeEventListener('keydown', escHandler);
                    resolve();
                }
            };
            document.addEventListener('keydown', escHandler);
        });
    };
    
    // 커스텀 모달 (제목과 메시지 분리, 버튼 커스터마이징)
    window.customModal = function(title, message, buttonText, onButtonClick, cancelButtonText, onCancelClick) {
        return new Promise((resolve) => {
            maintainFullscreen();
            
            const overlay = document.createElement('div');
            overlay.className = 'custom-modal-overlay';
            
            const modal = document.createElement('div');
            modal.className = 'custom-modal';
            
            const titleDiv = document.createElement('div');
            titleDiv.className = 'custom-modal-title';
            titleDiv.textContent = '[' + title + ']';
            titleDiv.style.whiteSpace = 'pre-line';
            
            const messageDiv = document.createElement('div');
            messageDiv.className = 'custom-modal-message';
            messageDiv.textContent = message;
            messageDiv.style.whiteSpace = 'pre-line';
            
            const lineCount = (message.match(/\n/g) || []).length + 1;
            if (lineCount === 1) {
                messageDiv.style.marginTop = '1.4em';
            }
            
            const buttonsDiv = document.createElement('div');
            buttonsDiv.className = 'custom-modal-buttons';
            
            // 닫기 버튼 추가
            const closeButton = document.createElement('div');
            closeButton.className = 'custom-modal-close-button';
            const closeIcon = document.createElement('div');
            closeIcon.className = 'custom-modal-close-icon';
            closeButton.appendChild(closeIcon);
            
            closeButton.addEventListener('click', (e) => {
                e.stopPropagation();
                e.preventDefault();
                document.body.removeChild(overlay);
                document.removeEventListener('keydown', escHandler);
                if (onCancelClick) {
                    onCancelClick();
                }
                resolve(false);
            });
            
            // 취소 버튼이 있는 경우
            if (cancelButtonText) {
                const cancelButton = document.createElement('button');
                cancelButton.className = 'custom-modal-button custom-modal-button-cancel';
                cancelButton.textContent = cancelButtonText;
                
                cancelButton.addEventListener('click', () => {
                    document.body.removeChild(overlay);
                    document.removeEventListener('keydown', escHandler);
                    if (onCancelClick) {
                        onCancelClick();
                    }
                    resolve(false);
                });
                
                buttonsDiv.appendChild(cancelButton);
            }
            
            const actionButton = document.createElement('button');
            actionButton.className = 'custom-modal-button custom-modal-button-confirm';
            actionButton.textContent = buttonText || '확인';
            
            actionButton.addEventListener('click', () => {
                if (onButtonClick) {
                    // 모달 요소를 콜백에 전달
                    const result = onButtonClick(modal, overlay);
                    // 콜백이 false를 반환하면 모달을 닫지 않음
                    if (result === false) {
                        return;
                    }
                }
                document.body.removeChild(overlay);
                document.removeEventListener('keydown', escHandler);
                resolve(true);
            });
            
            buttonsDiv.appendChild(actionButton);
            modal.appendChild(titleDiv);
            modal.appendChild(messageDiv);
            modal.appendChild(buttonsDiv);
            modal.appendChild(closeButton);
            overlay.appendChild(modal);
            document.body.appendChild(overlay);
            
            // ESC 키로 닫기
            const escHandler = (e) => {
                if (e.key === 'Escape') {
                    document.body.removeChild(overlay);
                    document.removeEventListener('keydown', escHandler);
                    if (onCancelClick) {
                        onCancelClick();
                    }
                    resolve(false);
                }
            };
            document.addEventListener('keydown', escHandler);
        });
    };
    
    // 커스텀 confirm 함수
    window.customConfirm = function(message) {
        return new Promise((resolve) => {
            maintainFullscreen();
            
            const overlay = document.createElement('div');
            overlay.className = 'custom-modal-overlay';
            
            const modal = document.createElement('div');
            modal.className = 'custom-modal';
            
            const titleDiv = document.createElement('div');
            titleDiv.className = 'custom-modal-title';
            titleDiv.textContent = '[알림]';
            titleDiv.style.whiteSpace = 'pre-line';
            
            const messageDiv = document.createElement('div');
            messageDiv.className = 'custom-modal-message';
            messageDiv.textContent = message;
            messageDiv.style.whiteSpace = 'pre-line';
            
            // 메시지 줄 수 확인 (한 줄일 때 줄 높이만큼 y 위치 내림)
            const lineCount = (message.match(/\n/g) || []).length + 1;
            if (lineCount === 1) {
                messageDiv.style.marginTop = '1.4em'; // 줄 높이(line-height)만큼
            }
            
            const buttonsDiv = document.createElement('div');
            buttonsDiv.className = 'custom-modal-buttons';
            
            // 닫기 버튼 추가
            const closeButton = document.createElement('div');
            closeButton.className = 'custom-modal-close-button';
            const closeIcon = document.createElement('div');
            closeIcon.className = 'custom-modal-close-icon';
            closeButton.appendChild(closeIcon);
            
            closeButton.addEventListener('click', (e) => {
                e.stopPropagation();
                e.preventDefault();
                document.body.removeChild(overlay);
                document.removeEventListener('keydown', escHandler);
                resolve(false);
            });
            
            const confirmButton = document.createElement('button');
            confirmButton.className = 'custom-modal-button custom-modal-button-confirm';
            confirmButton.textContent = '확인';
            
            confirmButton.addEventListener('click', () => {
                document.body.removeChild(overlay);
                document.removeEventListener('keydown', escHandler);
                resolve(true);
            });
            
            const cancelButton = document.createElement('button');
            cancelButton.className = 'custom-modal-button custom-modal-button-cancel';
            cancelButton.textContent = '취소';
            
            cancelButton.addEventListener('click', () => {
                document.body.removeChild(overlay);
                document.removeEventListener('keydown', escHandler);
                resolve(false);
            });
            
            buttonsDiv.appendChild(cancelButton);
            buttonsDiv.appendChild(confirmButton);
            modal.appendChild(titleDiv);
            modal.appendChild(messageDiv);
            modal.appendChild(buttonsDiv);
            modal.appendChild(closeButton);
            overlay.appendChild(modal);
            document.body.appendChild(overlay);
            
            // ESC 키로 취소
            const escHandler = (e) => {
                if (e.key === 'Escape') {
                    document.body.removeChild(overlay);
                    document.removeEventListener('keydown', escHandler);
                    resolve(false);
                }
            };
            document.addEventListener('keydown', escHandler);
        });
    };
    
    // 전체화면 모드 종료 감지 시 다시 전체화면으로
    document.addEventListener('fullscreenchange', maintainFullscreen);
    document.addEventListener('webkitfullscreenchange', maintainFullscreen);
    document.addEventListener('mozfullscreenchange', maintainFullscreen);
    document.addEventListener('MSFullscreenChange', maintainFullscreen);
})();

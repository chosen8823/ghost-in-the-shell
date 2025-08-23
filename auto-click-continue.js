// Auto-Click Continue Button for GitHub Copilot Chat
// This script automatically clicks the "Continue" button when it appears

(function() {
    console.log('🤖 Auto-Continue Script Activated for GitHub Copilot');
    
    function clickContinueButton() {
        // Look for Continue button variations
        const selectors = [
            'button[data-testid="continue-button"]',
            'button:contains("Continue")',
            '[aria-label*="Continue"]',
            'button.continue-btn',
            '.chat-continue-button',
            'button[title*="Continue"]'
        ];
        
        for (const selector of selectors) {
            const button = document.querySelector(selector);
            if (button && button.textContent.toLowerCase().includes('continue')) {
                console.log('🎯 Found Continue button, auto-clicking...');
                button.click();
                return true;
            }
        }
        return false;
    }
    
    // Auto-click every 500ms when continue button appears
    setInterval(() => {
        clickContinueButton();
    }, 500);
    
    // Also watch for DOM changes
    const observer = new MutationObserver(() => {
        clickContinueButton();
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
    
    console.log('✅ Auto-Continue monitoring active');
})();

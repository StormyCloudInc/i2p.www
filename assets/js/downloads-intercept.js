/**
 * Downloads Page - Donation Interstitial Intercept
 * Redirects primary download buttons to the donation page
 */

(function() {
    'use strict';

    // Configuration
    const DONATE_PAGE = '/en/donate/download/';
    const ENABLE_INTERSTITIAL = true; // Set to false to disable globally

    // Check if user donated recently (matches download-donate.js logic)
    function hasRecentDonation() {
        try {
            const stored = localStorage.getItem('i2p_donated');
            if (!stored) return false;

            const data = JSON.parse(stored);
            const expiryDate = new Date(data.expiry);
            return new Date() < expiryDate;
        } catch (e) {
            return false;
        }
    }

    // Intercept download button clicks
    function interceptDownloads() {
        // Don't intercept if interstitial is disabled or user donated recently
        if (!ENABLE_INTERSTITIAL || hasRecentDonation()) {
            console.log('[I2P Downloads] Interstitial disabled or user donated recently');
            return;
        }

        console.log('[I2P Downloads] Intercepting download buttons...');

        // Intercept platform card download buttons
        document.querySelectorAll('.btn-platform').forEach(btn => {
            if (btn.classList.contains('intercepted')) return; // Already intercepted

            const originalHref = btn.getAttribute('href');
            if (!originalHref || originalHref === '#') {
                console.log('[I2P Downloads] Skipping button with no href:', btn);
                return;
            }

            // Skip interception for internal guide pages and Docker Hub
            if (originalHref.startsWith('/') ||
                originalHref.startsWith('http') && originalHref.includes('docker.com')) {
                console.log('[I2P Downloads] Skipping internal/guide link:', originalHref);
                return;
            }

            console.log('[I2P Downloads] Intercepting button:', originalHref);

            btn.classList.add('intercepted');
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                console.log('[I2P Downloads] Download button clicked!', originalHref);

                // Get platform info from parent card
                const card = this.closest('.platform-card');
                const platform = card ? card.dataset.platform : 'unknown';
                const version = card ? card.querySelector('.platform-version')?.textContent.trim() : '';

                console.log('[I2P Downloads] Platform:', platform, 'Version:', version);

                // Build donation page URL with parameters (include download URL)
                const params = new URLSearchParams({
                    file: platform,
                    version: version.replace('v', ''),
                    url: encodeURIComponent(originalHref),
                    platform: platform
                });

                const redirectUrl = `${DONATE_PAGE}?${params.toString()}`;
                console.log('[I2P Downloads] Redirecting to:', redirectUrl);

                // Redirect to thank-you page (download will start there)
                window.location.href = redirectUrl;
            });
        });

        // Intercept detected download button
        const detectedBtn = document.getElementById('detected-download-btn');
        if (detectedBtn && !detectedBtn.classList.contains('intercepted')) {
            const originalHref = detectedBtn.getAttribute('href');

            if (originalHref && originalHref !== '#') {
                detectedBtn.classList.add('intercepted');
                detectedBtn.addEventListener('click', function(e) {
                    e.preventDefault();

                    const platform = document.getElementById('detected-name')?.textContent || 'unknown';
                    const details = document.getElementById('detected-details')?.textContent || '';
                    const version = details.match(/Version ([\d.]+)/)?.[1] || '2.10.0';

                    const params = new URLSearchParams({
                        file: platform.toLowerCase().replace('download for ', ''),
                        version: version,
                        url: encodeURIComponent(originalHref),
                        platform: platform
                    });

                    // Redirect to thank-you page (download will start there)
                    window.location.href = `${DONATE_PAGE}?${params.toString()}`;
                });
            }
        }
    }

    // Initialize when DOM is ready
    function init() {
        console.log('[I2P Downloads] Script loaded and initializing...');

        // Run immediately for existing elements
        interceptDownloads();

        // Also run after delays to catch dynamically updated hrefs
        setTimeout(() => {
            console.log('[I2P Downloads] Re-checking buttons after 500ms...');
            interceptDownloads();
        }, 500);
        setTimeout(() => {
            console.log('[I2P Downloads] Re-checking buttons after 1000ms...');
            interceptDownloads();
        }, 1000);
        setTimeout(() => {
            console.log('[I2P Downloads] Re-checking buttons after 1500ms...');
            interceptDownloads();
        }, 1500);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();

/**
 * Donation Interstitial - Download Manager (Thunderbird-style)
 * Handles countdown timer, auto-download, and modal popup
 */

(function() {
    'use strict';

    // Configuration
    const MODAL_DELAY_SECONDS = 2; // Show modal 2 seconds after page loads
    const STORAGE_KEY = 'i2p_donated';
    const STORAGE_EXPIRY_DAYS = 30;

    // Sample cryptocurrency addresses (replace with real ones)
    const CRYPTO_ADDRESSES = {
        btc: 'bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh',
        xmr: '42ey1afDFnn4886T7196doS9GPMzexD9gXpsZYDwvtSX6X2DQpF6PvqGM7aXrDJhJXRDjTsHc1k6gkXqXjfj3tqyVKWxvvG',
        zec: 't1Hsc1LR8yKnbbe3twRp88p6vFfC5t7DLbs'
    };

    // Parse URL parameters
    function getURLParams() {
        const params = new URLSearchParams(window.location.search);
        return {
            file: params.get('file') || 'unknown',
            version: params.get('version') || '2.10.0',
            url: params.get('url') || '',
            platform: params.get('platform') || params.get('file') || 'unknown'
        };
    }

    // Check if user donated recently
    function hasRecentDonation() {
        try {
            const stored = localStorage.getItem(STORAGE_KEY);
            if (!stored) return false;

            const data = JSON.parse(stored);
            const expiryDate = new Date(data.expiry);
            return new Date() < expiryDate;
        } catch (e) {
            return false;
        }
    }

    // Mark user as donated
    function markAsDonated() {
        try {
            const expiry = new Date();
            expiry.setDate(expiry.getDate() + STORAGE_EXPIRY_DAYS);
            localStorage.setItem(STORAGE_KEY, JSON.stringify({
                expiry: expiry.toISOString(),
                timestamp: new Date().toISOString()
            }));
        } catch (e) {
            console.warn('Could not save donation status');
        }
    }

    // Trigger download immediately
    function triggerDownload(url) {
        if (!url) {
            console.error('[I2P Donate] No download URL provided');
            const statusMessage = document.getElementById('status-message');
            if (statusMessage) {
                statusMessage.innerHTML =
                    '<strong style="color: var(--color-error);">Error: Download URL missing</strong><br>' +
                    '<small><a href="' + (document.referrer || '/downloads/') + '">← Return to downloads</a></small>';
            }
            return false;
        }

        console.log('[I2P Donate] Starting download:', url);

        // Create hidden iframe to trigger download
        const iframe = document.createElement('iframe');
        iframe.style.display = 'none';
        iframe.src = url;
        document.body.appendChild(iframe);

        // Update UI
        const statusMessage = document.getElementById('status-message');
        if (statusMessage) {
            statusMessage.innerHTML =
                '<strong style="color: var(--color-success);">✓ Your download has started!</strong><br>' +
                '<small>If your download doesn\'t start, <a href="' + url + '" id="manual-download-link">click here</a>.</small>';
        }

        // Clean up iframe after download starts
        setTimeout(() => {
            if (iframe.parentNode) {
                document.body.removeChild(iframe);
            }
        }, 10000);

        return true;
    }

    // Trigger FundraiseUp donation form
    function showDonationForm() {
        console.log('[I2P Donate] Opening FundraiseUp donation form');
        const trigger = document.getElementById('donation-trigger');
        if (trigger) {
            trigger.click();
        }
    }



    // Initialize
    function init() {
        const params = getURLParams();
        const downloadUrl = decodeURIComponent(params.url || '');

        // Debug info
        console.log('[I2P Donate] Page loaded with params:', params);
        console.log('[I2P Donate] Download URL:', downloadUrl);

        // Start download immediately
        const downloadStarted = triggerDownload(downloadUrl);

        if (!downloadStarted) {
            console.error('[I2P Donate] Download failed to start');
            return;
        }

        // Check if user donated recently and should skip form
        if (hasRecentDonation()) {
            console.log('[I2P Donate] User donated recently, skipping donation form');
            return;
        }

        // Show FundraiseUp form after a short delay
        setTimeout(() => {
            showDonationForm();
            // Mark as donated so they won't see it again for 30 days
            markAsDonated();
        }, MODAL_DELAY_SECONDS * 1000);
    }

    // Run when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();

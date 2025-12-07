/**
 * Downloads Page - Thank You Page Redirect
 * Starts download immediately and redirects to thank you page
 */

(function() {
    'use strict';

    // Configuration
    const DONATE_PAGE = '/en/donate/download/';

    // Trigger download immediately
    function triggerDownload(url) {
        console.log('[I2P Downloads] Starting download:', url);

        // Use window.open with download as fallback
        // Most browsers will open download directly without popup
        const link = document.createElement('a');
        link.href = url;
        link.download = ''; // Suggest download instead of navigation
        link.style.display = 'none';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    // Intercept download button clicks
    function interceptDownloads() {
        console.log('[I2P Downloads] Intercepting download buttons...');

        // Intercept mirror/torrent/i2p/tor links (alternative download methods)
        document.querySelectorAll('.mirror-link, .alt-method').forEach(link => {
            if (link.classList.contains('intercepted')) return; // Already intercepted

            const href = link.getAttribute('href');
            if (!href || href === '#' || href.startsWith('/')) {
                return; // Skip empty, placeholder, or internal links
            }

            console.log('[I2P Downloads] Intercepting alt download link:', href);

            link.classList.add('intercepted');
            link.addEventListener('click', function(e) {
                e.preventDefault();
                console.log('[I2P Downloads] Alt download link clicked!', href);

                // Start download immediately
                triggerDownload(href);

                // Get platform from parent card
                const card = this.closest('.platform-card') || this.closest('.detected-download');
                const platform = card ? (card.dataset.platform || 'unknown') : 'unknown';
                const version = card ? (card.querySelector('.platform-version')?.textContent.trim() || '2.10.0') : '2.10.0';

                // Build thank-you page URL (include download URL)
                const params = new URLSearchParams({
                    file: platform,
                    version: version.replace('v', ''),
                    platform: platform,
                    url: encodeURIComponent(href)
                });

                const redirectUrl = `${DONATE_PAGE}?${params.toString()}`;
                console.log('[I2P Downloads] Redirecting to:', redirectUrl);

                // Redirect to thank-you page after delay
                setTimeout(() => {
                    window.location.href = redirectUrl;
                }, 5000);
            });
        });

        // Intercept platform card download buttons
        document.querySelectorAll('.btn-platform').forEach(btn => {
            if (btn.classList.contains('intercepted')) return; // Already intercepted
            
            // Skip buttons explicitly marked as non-interceptable (guide/documentation links)
            if (btn.getAttribute('data-no-intercept') === 'true') {
                console.log('[I2P Downloads] Skipping button with data-no-intercept attribute:', btn);
                return;
            }

            const originalHref = btn.getAttribute('href');
            if (!originalHref || originalHref === '#') {
                console.log('[I2P Downloads] Skipping button with no href:', btn);
                return;
            }

            // Check button text/content to identify guide links
            const buttonText = (btn.textContent || btn.innerText || '').toLowerCase().trim();
            const isGuideButton = buttonText.includes('install guide') || 
                                 buttonText.includes('guide') ||
                                 buttonText.includes('installation');

            // Skip interception for guide pages, documentation links, and Docker Hub
            const hrefLower = originalHref.toLowerCase();
            
            // Check if it's a guide/documentation link (case-insensitive patterns)
            const isGuideLink = hrefLower.includes('docs/guides/') || 
                               hrefLower.includes('docs/install/') ||
                               hrefLower.includes('debian-ubuntu-install') ||
                               hrefLower.includes('installing-i2p-on-debian-and-ubuntu') ||
                               hrefLower.includes('/guide');
            
            // Check if it's an internal link (starts with /) - typically guides/docs, not downloads
            // Also check for relative URLs (no protocol) that point to guides
            const isInternalLink = originalHref.startsWith('/');
            const isRelativeGuideLink = !originalHref.includes('://') && 
                                       !originalHref.startsWith('#') &&
                                       (hrefLower.includes('docs/') || hrefLower.includes('guide'));
            
            // Check if it's a Docker Hub link
            const isDockerHub = originalHref.startsWith('http') && originalHref.includes('docker.com');
            
            // Skip guide buttons, guide links, internal links, relative guide links, or Docker Hub
            // Note: Internal links are skipped because actual download files are external URLs
            if (isGuideButton || isGuideLink || isInternalLink || isRelativeGuideLink || isDockerHub) {
                console.log('[I2P Downloads] Skipping internal/guide link:', originalHref, 'Button text:', buttonText);
                return;
            }

            console.log('[I2P Downloads] Intercepting button:', originalHref);

            btn.classList.add('intercepted');
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                console.log('[I2P Downloads] Download button clicked!', originalHref);

                // Start download immediately
                triggerDownload(originalHref);

                // Get platform info from parent card
                const card = this.closest('.platform-card');
                const platform = card ? card.dataset.platform : 'unknown';
                const version = card ? card.querySelector('.platform-version')?.textContent.trim() : '';

                console.log('[I2P Downloads] Platform:', platform, 'Version:', version);

                // Build thank-you page URL with parameters (include download URL)
                const params = new URLSearchParams({
                    file: platform,
                    version: version.replace('v', ''),
                    platform: platform,
                    url: encodeURIComponent(originalHref)
                });

                const redirectUrl = `${DONATE_PAGE}?${params.toString()}`;
                console.log('[I2P Downloads] Redirecting to:', redirectUrl);

                // Redirect to thank-you page after delay (gives download time to start)
                setTimeout(() => {
                    window.location.href = redirectUrl;
                }, 5000);
            });
        });

        // Intercept detected download button
        const detectedBtn = document.getElementById('detected-download-btn');
        if (detectedBtn && !detectedBtn.classList.contains('intercepted')) {
            detectedBtn.classList.add('intercepted');
            detectedBtn.addEventListener('click', function(e) {
                e.preventDefault();

                // Get current href (might have been changed by mirror selector)
                const currentHref = this.getAttribute('href');

                if (!currentHref || currentHref === '#') {
                    console.error('[I2P Downloads] No valid download URL');
                    return;
                }

                // Start download immediately with current href
                triggerDownload(currentHref);

                const platform = document.getElementById('detected-name')?.textContent || 'unknown';
                const details = document.getElementById('detected-details')?.textContent || '';
                const version = details.match(/Version ([\d.]+)/)?.[1] || '2.10.0';

                const params = new URLSearchParams({
                    file: platform.toLowerCase().replace('download for ', ''),
                    version: version,
                    platform: platform,
                    url: encodeURIComponent(currentHref)
                });

                // Redirect to thank-you page after delay (gives download time to start)
                setTimeout(() => {
                    window.location.href = `${DONATE_PAGE}?${params.toString()}`;
                }, 5000);
            });
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

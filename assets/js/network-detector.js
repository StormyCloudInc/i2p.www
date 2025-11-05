/**
 * Network-Aware Script Loader
 * Detects whether the user is on Clearnet, I2P, or Tor and loads the appropriate feedback widget
 */

(function() {
    'use strict';

    // Detect network based on hostname
    const hostname = window.location.hostname;
    let scriptSrc;

    if (hostname.endsWith('.i2p')) {
        // I2P network
        scriptSrc = 'http://feedback.stormycloud.i2p/widgets/docs-feedback.js';
        console.log('[Network Detector] I2P network detected');
    } else if (hostname.endsWith('.onion')) {
        // Tor network
        scriptSrc = 'http://gfonxmohvarpmocsvllscsuszdu5rikipm6innvcwq4vpng7zzqmmfyd.onion/widgets/docs-feedback.js';
        console.log('[Network Detector] Tor network detected');
    } else {
        // Clearnet (default) - Use HTTPS for Safari compatibility
        scriptSrc = 'https://feedback.stormycloud.org/widgets/docs-feedback.js';
        console.log('[Network Detector] Clearnet detected');
    }

    // Load the appropriate feedback widget script
    const script = document.createElement('script');
    script.src = scriptSrc;
    script.async = true;
    script.onerror = function() {
        console.error('[Network Detector] Failed to load feedback widget from:', scriptSrc);
    };

    // Append to head or body (whichever is available)
    const target = document.head || document.body;
    if (target) {
        target.appendChild(script);
    } else {
        // If neither head nor body exists yet, wait for DOM ready
        document.addEventListener('DOMContentLoaded', function() {
            (document.head || document.body).appendChild(script);
        });
    }
})();

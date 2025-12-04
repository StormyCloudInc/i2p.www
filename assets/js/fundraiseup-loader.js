/**
 * FundraiseUp Lazy Loader
 * Loads FundraiseUp script only when needed to preserve user privacy.
 * Skips loading entirely on I2P and Tor networks.
 */
(function() {
    'use strict';

    // Skip on anonymous networks
    var hostname = window.location.hostname;
    if (hostname.endsWith('.i2p') || hostname.endsWith('.b32.i2p') || hostname.endsWith('.onion')) {
        // Hide donate buttons and exit
        document.querySelectorAll('[href^="#X"]').forEach(function(el) {
            if (el.href && el.href.match(/#X[A-Z0-9]+$/)) {
                el.style.display = 'none';
            }
        });
        return;
    }

    var loaded = false;
    var scriptReady = false;

    function loadFundraiseUp(campaignCode, callback) {
        // If script is fully ready, just run callback
        if (scriptReady) {
            if (callback) callback();
            return;
        }

        // If not yet started loading, start now
        if (!loaded) {
            loaded = true;

            // FundraiseUp initialization code
            (function(w,d,s,n,a){if(!w[n]){var l='call,catch,on,once,set,then,track,openCheckout'
            .split(','),i,o=function(n){return'function'==typeof n?o.l.push([arguments])&&o
            :function(){return o.l.push([n,arguments])&&o}},t=d.getElementsByTagName(s)[0],
            j=d.createElement(s);j.async=!0;j.src='https://cdn.fundraiseup.com/widget/'+a+'';
            j.onload = function() {
                // Give FundraiseUp time to fully initialize
                setTimeout(function() {
                    scriptReady = true;
                    if (callback) callback();
                }, 300);
            };
            t.parentNode.insertBefore(j,t);o.s=Date.now();o.v=5;o.h=w.location.href;o.l=[];
            for(i=0;i<8;i++)o[l[i]]=o(l[i]);w[n]=o}
            })(window,document,'script','FundraiseUp','AAYKECHT');
        } else {
            // Script is loading, wait for it
            var checkReady = setInterval(function() {
                if (scriptReady) {
                    clearInterval(checkReady);
                    if (callback) callback();
                }
            }, 50);
        }
    }

    // Auto-load on donation-related pages
    var path = window.location.pathname;
    if (path.includes('/financial-support') || path.includes('/donate') || path.includes('/thank-you')) {
        loadFundraiseUp();
    }

    // Load on donate button click, then open checkout
    document.addEventListener('click', function(e) {
        var link = e.target.closest('a[href^="#X"]');
        if (link && link.href && link.href.match(/#X[A-Z0-9]+$/)) {
            var campaignCode = link.getAttribute('href').substring(1); // Remove #

            if (!scriptReady) {
                // Prevent default, load script, then open checkout
                e.preventDefault();
                e.stopPropagation();

                loadFundraiseUp(campaignCode, function() {
                    // Use FundraiseUp API to open checkout
                    if (window.FundraiseUp && window.FundraiseUp.openCheckout) {
                        window.FundraiseUp.openCheckout(campaignCode);
                    }
                });
            }
            // If already loaded, let FundraiseUp handle the click naturally
        }
    }, true); // Use capture phase to intercept before FundraiseUp
})();

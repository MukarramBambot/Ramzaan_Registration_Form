/**
 * Root Service Worker - Madras Jamaat Portal
 * Basic PWA support to enable installation.
 */

self.addEventListener("install", event => {
    console.log("Service Worker: Installed");
    self.skipWaiting();
});

self.addEventListener("activate", event => {
    console.log("Service Worker: Activated");
    return self.clients.claim();
});

self.addEventListener("fetch", event => {
    // Basic fetch handler required for PWA installability
    event.respondWith(
        fetch(event.request).catch(() => {
            // Fallback strategy if needed, but simple fetch is enough for eligibility
            return caches.match(event.request);
        })
    );
});

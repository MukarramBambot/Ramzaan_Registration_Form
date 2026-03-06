const CACHE_NAME = "jamaat-mobile-v1.0.1";
const ASSETS_TO_CACHE = [
  "/mobile/",
  "/mobile/index.php",
  "/mobile/offline.html",
  "/mobile/manifest.json",
  "/mobile/assets/css/mobile.css",
  "/mobile/assets/js/mobile.js",
  "/assets/js/api.js"
];

// Install Event
self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log("Caching essential assets");
        return cache.addAll(ASSETS_TO_CACHE);
      })
  );
  self.skipWaiting();
});

// Activate Event
self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys().then(keys => {
      return Promise.all(
        keys.filter(key => key !== CACHE_NAME)
            .map(key => caches.delete(key))
      );
    })
  );
  self.clients.claim();
});

// Fetch Event
self.addEventListener("fetch", event => {
  const { request } = event;
  const url = new URL(request.url);

  // ⚠️ DO NOT CACHE API CALLS, POST, AUTH
  if (
    request.method !== "GET" || 
    url.pathname.includes("/api/") ||
    url.host.includes("api.") // window.API_BASE = 'https://api.madrasjamaatportal.org';
  ) {
    return;
  }

  // Network First, Fallback to Cache or Offline Page
  event.respondWith(
    fetch(request)
      .catch(() => {
        return caches.match(request).then(response => {
           return response || caches.match("/mobile/offline.html");
        });
      })
  );
});

const VERSION = "aaptakosha-v1";
const STATIC_CACHE = VERSION + "-static";
const CONTENT_CACHE = VERSION + "-content";
const SHELL = [
  "/",
  "/index.html",
  "/styles.css",
  "/app.js",
  "/session.js",
  "/api-client.js",
  "/auth-ui.js",
  "/manifest.webmanifest"
];

self.addEventListener("install", event => {
  event.waitUntil(caches.open(STATIC_CACHE).then(cache => cache.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys().then(keys => Promise.all(
      keys.filter(key => ![STATIC_CACHE, CONTENT_CACHE].includes(key)).map(key => caches.delete(key))
    )).then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", event => {
  const request = event.request;
  if (request.method !== "GET") return;
  const url = new URL(request.url);
  if (url.origin !== self.location.origin) return;

  if (url.pathname.startsWith("/api/content/") || url.pathname === "/api/curriculum/content") {
    event.respondWith(
      caches.open(CONTENT_CACHE).then(async cache => {
        try {
          const response = await fetch(request);
          if (response.ok) cache.put(request, response.clone());
          return response;
        } catch (_) {
          return cache.match(request).then(cached => cached || new Response(
            JSON.stringify({error:{code:"offline_content_unavailable",message:"This learning item is not cached yet."}}),
            {status:503, headers:{"Content-Type":"application/json"}}
          ));
        }
      })
    );
    return;
  }

  if (request.mode === "navigate") {
    event.respondWith(
      fetch(request).catch(() => caches.match("/index.html"))
    );
  }
});

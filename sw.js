// Offline support: everything the app needs is cached on first load.
// Only active on https:// or localhost (browsers do not allow service workers on plain http).
const CACHE = "python-practice-v3";
const FILES = [
  "./", "index.html", "app.js", "py-worker.js", "harness.py", "exercises.json",
  "manifest.webmanifest", "icon.svg", "icon-192.png", "icon-512.png", "icon-maskable-512.png", "apple-touch-icon.png", "vendor/anthropic.js",
  "vendor/pyodide/pyodide.mjs", "vendor/pyodide/pyodide.asm.mjs", "vendor/pyodide/pyodide.asm.wasm",
  "vendor/pyodide/python_stdlib.zip", "vendor/pyodide/pyodide-lock.json",
];

self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(CACHE).then((cache) => cache.addAll(FILES)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim()),
  );
});

// Serve from cache right away, refresh the cached copy in the background.
self.addEventListener("fetch", (event) => {
  const { request } = event;
  if (request.method !== "GET" || new URL(request.url).origin !== location.origin) return;
  event.respondWith(
    caches.open(CACHE).then(async (cache) => {
      const cached = await cache.match(request, { ignoreSearch: true });
      const fresh = fetch(request)
        .then((response) => { if (response.ok) cache.put(request, response.clone()); return response; })
        .catch(() => cached);
      return cached || fresh;
    }),
  );
});

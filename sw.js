/* Wochenbericht Lovrencic PWA 2.25.2. Offline: nur App-Dateien, niemals Kundendaten. */
const CACHE_NAME = 'wochenberichte-pwa-v2.25.2';
const SHELL = ['./', './index.html', './index.html?app=pwa', './manifest.webmanifest', './icon-192.png', './icon-512.png'];
self.addEventListener('install', event => {
  event.waitUntil(caches.open(CACHE_NAME).then(cache => cache.addAll(SHELL)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', event => {
  event.waitUntil(Promise.all([
    caches.keys().then(keys => Promise.all(keys.filter(key => (key.startsWith('wochenberichte-pwa-') || key.startsWith('wochenberichte-static-')) && key !== CACHE_NAME).map(key => caches.delete(key)))),
    self.clients.claim()
  ]));
});
self.addEventListener('fetch', event => {
  const req = event.request;
  if (req.method !== 'GET' || new URL(req.url).origin !== self.location.origin) return;
  const url = new URL(req.url);
  const base = new URL(self.registration.scope);
  if (!url.pathname.startsWith(base.pathname)) return;
  const local = url.pathname.substring(base.pathname.length);
  if (!['','index.html','manifest.webmanifest','icon-192.png','icon-512.png'].includes(local)) return;
  if (req.mode === 'navigate' || local === '' || local === 'index.html') {
    event.respondWith(fetch(req).then(res => {
      if (res.ok) { const copy=res.clone(); caches.open(CACHE_NAME).then(cache=>cache.put('./index.html',copy)); }
      return res;
    }).catch(async()=> (await caches.match('./index.html')) || Response.error()));
  } else {
    event.respondWith(caches.match(req).then(cached=>cached || fetch(req)));
  }
});

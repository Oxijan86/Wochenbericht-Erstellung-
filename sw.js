/* Offline cache for the static application ONLY. Data and database backups live in IndexedDB. */
const CACHE='wochenberichte-static-v2.16.0';
self.addEventListener('install',event=>event.waitUntil(caches.open(CACHE).then(cache=>cache.add('./index.html')).then(()=>self.skipWaiting())));
self.addEventListener('activate',event=>event.waitUntil(Promise.all([caches.keys().then(names=>Promise.all(names.filter(n=>n.startsWith('wochenberichte-static-')&&n!==CACHE).map(n=>caches.delete(n)))),self.clients.claim()])));
self.addEventListener('fetch',event=>{
 if(event.request.mode!=='navigate'||new URL(event.request.url).origin!==self.location.origin)return;
 event.respondWith(fetch(event.request).then(response=>{if(response.ok){const backup=response.clone();caches.open(CACHE).then(cache=>cache.put('./index.html',backup))}return response}).catch(async()=>await caches.match('./index.html')||Response.error()));
});

/* Offline shell only. User data remains in IndexedDB / local or connected .db file. */
const CACHE='wochenberichte-static-v2.24.1';
const START='./index.html';
self.addEventListener('install',event=>event.waitUntil(
 caches.open(CACHE).then(cache=>cache.add(new Request(START,{cache:'reload'}))).then(()=>self.skipWaiting())
));
self.addEventListener('activate',event=>event.waitUntil((async()=>{
 const names=await caches.keys();
 await Promise.all(names.filter(n=>n.startsWith('wochenberichte-static-')&&n!==CACHE).map(n=>caches.delete(n)));
 await self.clients.claim();
})()));
self.addEventListener('fetch',event=>{
 if(event.request.mode!=='navigate'||new URL(event.request.url).origin!==self.location.origin)return;
 event.respondWith((async()=>{
  try{
   const response=await fetch(new Request(event.request,{cache:'no-store'}));
   if(response.ok){const cache=await caches.open(CACHE);await cache.put(START,response.clone());}
   return response;
  }catch(e){return await (await caches.open(CACHE)).match(START)||Response.error();}
 })());
});

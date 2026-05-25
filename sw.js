// Eesti Keele Kursus — Service Worker
const CACHE = 'eesti-keele-v4';
const URLS = [
  'eesti_keele_kursus.html',
  'manifest.json',
  'icon-192.png',
  'icon-512.png'
];

self.addEventListener('install', function(e) {
  e.waitUntil(
    caches.open(CACHE).then(function(cache) {
      return cache.addAll(URLS);
    })
  );
  self.skipWaiting();
});

self.addEventListener('activate', function(e) {
  e.waitUntil(
    caches.keys().then(function(keys) {
      return Promise.all(keys.map(function(k) {
        if (k !== CACHE) return caches.delete(k);
      }));
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', function(e) {
  // Network-first: always try server first, fall back to cache
  e.respondWith(
    fetch(e.request).then(function(res) {
      return caches.open(CACHE).then(function(cache) {
        cache.put(e.request, res.clone());
        return res;
      });
    }).catch(function() {
      return caches.match(e.request);
    })
  );
});

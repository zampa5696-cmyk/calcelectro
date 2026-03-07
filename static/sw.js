// ── Service Worker — E-CALC PWA ──
const CACHE_NAME = 'ecalc-v1';

// Archivos que se guardan en caché para uso offline
const STATIC_ASSETS = [
  '/',
  '/static/manifest.json',
  '/static/icons/icono_terminal_192.png',
  '/static/icons/icono_terminal_512.png',
  'https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap'
];

// ── INSTALACIÓN: guarda los recursos estáticos ──
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(STATIC_ASSETS);
    })
  );
  self.skipWaiting();
});

// ── ACTIVACIÓN: limpia cachés viejos ──
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))
      )
    )
  );
  self.clients.claim();
});

// ── FETCH: Network first, caché como fallback ──
self.addEventListener('fetch', event => {
  // Solo interceptar GET
  if (event.request.method !== 'GET') return;

  // Para requests de navegación (páginas) y POST de cálculo:
  // dejar pasar directo al servidor (necesitan Flask)
  const url = new URL(event.request.url);
  if (url.pathname === '/calcular') return;

  event.respondWith(
    fetch(event.request)
      .then(response => {
        // Si la respuesta es válida, guardarla en caché
        if (response && response.status === 200) {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
        }
        return response;
      })
      .catch(() => {
        // Sin internet: servir desde caché
        return caches.match(event.request).then(cached => {
          if (cached) return cached;
          // Fallback: página principal en caché
          return caches.match('/');
        });
      })
  );
});

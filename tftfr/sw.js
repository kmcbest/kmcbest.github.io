// TFTFR High-Performance Asset Cache Service Worker
// 实现了“F5 优先本地缓存秒级秒开，Ctrl+F5 强制重新下载并更新缓存”
const CACHE_NAME = 'tftfr-portraits-v1';

self.addEventListener('install', (event) => {
    // 立即激活，无需等待旧 worker 关闭
    self.skipWaiting();
});

self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((keys) => {
            return Promise.all(
                keys.map((key) => {
                    if (key !== CACHE_NAME) {
                        return caches.delete(key);
                    }
                })
            );
        }).then(() => self.clients.claim())
    );
});

self.addEventListener('fetch', (event) => {
    const req = event.request;
    if (req.method !== 'GET') return;

    const url = new URL(req.url);

    // 重点拦截头像、字体等体积大、变动少的静态资源
    const isPortrait = url.pathname.includes('/portraits/') || 
                       url.pathname.endsWith('.png') || 
                       url.pathname.endsWith('.jpg') || 
                       url.pathname.endsWith('.webp');
    const isFont = url.pathname.includes('/fonts/') || url.pathname.endsWith('.ttf');

    if (isPortrait || isFont) {
        // 用户按下 Ctrl+F5 (Hard Reload) 时，浏览器会发送 cache: 'no-cache'
        const isHardReload = req.cache === 'no-cache';

        if (isHardReload) {
            // 强制重新向网络请求最新资源，并更新本地 Cache Storage
            event.respondWith(
                fetch(req).then((response) => {
                    if (response && response.status === 200) {
                        const copy = response.clone();
                        caches.open(CACHE_NAME).then((cache) => cache.put(req, copy));
                    }
                    return response;
                }).catch(() => caches.match(req))
            );
            return;
        }

        // 普通访问 / 普通刷新 (F5)：Cache-First 策略，0ms 极速从本地返回，不发起 304 耗时网络轮询
        event.respondWith(
            caches.match(req).then((cachedResponse) => {
                if (cachedResponse) {
                    return cachedResponse;
                }
                return fetch(req).then((response) => {
                    if (response && response.status === 200) {
                        const copy = response.clone();
                        caches.open(CACHE_NAME).then((cache) => cache.put(req, copy));
                    }
                    return response;
                });
            })
        );
    }
});

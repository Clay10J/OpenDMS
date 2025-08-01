// Service Worker for OpenDMS PWA
const CACHE_NAME = "opendms-v1.0.0";
const STATIC_CACHE = "opendms-static-v1.0.0";
const DYNAMIC_CACHE = "opendms-dynamic-v1.0.0";

// Files to cache immediately
const STATIC_FILES = [
  "/",
  "/static/css/app.css",
  "/static/manifest.json",
  "/static/icons/icon-192x192.png",
  "/static/icons/icon-512x512.png",
  "https://unpkg.com/htmx.org@1.9.0",
  "https://unpkg.com/hyperscript.org@0.9.8",
  "https://cdn.tailwindcss.com",
];

// Install event - cache static files
self.addEventListener("install", (event) => {
  console.log("Service Worker: Installing...");
  event.waitUntil(
    caches
      .open(STATIC_CACHE)
      .then((cache) => {
        console.log("Service Worker: Caching static files");
        return cache.addAll(STATIC_FILES);
      })
      .then(() => {
        console.log("Service Worker: Static files cached");
        return self.skipWaiting();
      })
      .catch((error) => {
        console.error("Service Worker: Error caching static files", error);
      })
  );
});

// Activate event - clean up old caches
self.addEventListener("activate", (event) => {
  console.log("Service Worker: Activating...");
  event.waitUntil(
    caches
      .keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames.map((cacheName) => {
            if (cacheName !== STATIC_CACHE && cacheName !== DYNAMIC_CACHE) {
              console.log("Service Worker: Deleting old cache", cacheName);
              return caches.delete(cacheName);
            }
          })
        );
      })
      .then(() => {
        console.log("Service Worker: Activated");
        return self.clients.claim();
      })
  );
});

// Fetch event - serve from cache or network
self.addEventListener("fetch", (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Skip non-GET requests
  if (request.method !== "GET") {
    return;
  }

  // Handle API requests
  if (url.pathname.startsWith("/api/")) {
    event.respondWith(handleApiRequest(request));
    return;
  }

  // Handle static files
  if (
    url.pathname.startsWith("/static/") ||
    url.origin === "https://unpkg.com" ||
    url.origin === "https://cdn.tailwindcss.com"
  ) {
    event.respondWith(handleStaticRequest(request));
    return;
  }

  // Handle HTML pages
  if (request.headers.get("accept").includes("text/html")) {
    event.respondWith(handleHtmlRequest(request));
    return;
  }

  // Default: network first, fallback to cache
  event.respondWith(
    fetch(request)
      .then((response) => {
        if (response.status === 200) {
          const responseClone = response.clone();
          caches.open(DYNAMIC_CACHE).then((cache) => {
            cache.put(request, responseClone);
          });
        }
        return response;
      })
      .catch(() => {
        return caches.match(request);
      })
  );
});

// Handle API requests - network first, cache fallback
async function handleApiRequest(request) {
  try {
    const response = await fetch(request);
    if (response.status === 200) {
      const responseClone = response.clone();
      const cache = await caches.open(DYNAMIC_CACHE);
      cache.put(request, responseClone);
    }
    return response;
  } catch (error) {
    console.log("Service Worker: API request failed, trying cache", error);
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }

    // Return offline response for API requests
    return new Response(
      JSON.stringify({
        error: "You are offline. Please check your connection and try again.",
        offline: true,
      }),
      {
        status: 503,
        statusText: "Service Unavailable",
        headers: { "Content-Type": "application/json" },
      }
    );
  }
}

// Handle static files - cache first, network fallback
async function handleStaticRequest(request) {
  const cachedResponse = await caches.match(request);
  if (cachedResponse) {
    return cachedResponse;
  }

  try {
    const response = await fetch(request);
    if (response.status === 200) {
      const responseClone = response.clone();
      const cache = await caches.open(STATIC_CACHE);
      cache.put(request, responseClone);
    }
    return response;
  } catch (error) {
    console.log("Service Worker: Static file not found", error);
    return new Response("Not found", { status: 404 });
  }
}

// Handle HTML requests - network first, cache fallback
async function handleHtmlRequest(request) {
  try {
    const response = await fetch(request);
    if (response.status === 200) {
      const responseClone = response.clone();
      const cache = await caches.open(DYNAMIC_CACHE);
      cache.put(request, responseClone);
    }
    return response;
  } catch (error) {
    console.log("Service Worker: HTML request failed, trying cache", error);
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }

    // Return offline page
    return caches.match("/offline.html");
  }
}

// Background sync for offline actions
self.addEventListener("sync", (event) => {
  if (event.tag === "background-sync") {
    event.waitUntil(doBackgroundSync());
  }
});

async function doBackgroundSync() {
  try {
    // Get pending requests from IndexedDB
    const pendingRequests = await getPendingRequests();

    for (const request of pendingRequests) {
      try {
        await fetch(request.url, {
          method: request.method,
          headers: request.headers,
          body: request.body,
        });

        // Remove from pending requests
        await removePendingRequest(request.id);
      } catch (error) {
        console.error("Background sync failed for request:", request, error);
      }
    }
  } catch (error) {
    console.error("Background sync error:", error);
  }
}

// Push notifications
self.addEventListener("push", (event) => {
  const options = {
    body: event.data ? event.data.text() : "New notification from OpenDMS",
    icon: "/static/icons/icon-192x192.png",
    badge: "/static/icons/icon-72x72.png",
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1,
    },
    actions: [
      {
        action: "explore",
        title: "View",
        icon: "/static/icons/icon-72x72.png",
      },
      {
        action: "close",
        title: "Close",
        icon: "/static/icons/icon-72x72.png",
      },
    ],
  };

  event.waitUntil(self.registration.showNotification("OpenDMS", options));
});

// Notification click
self.addEventListener("notificationclick", (event) => {
  event.notification.close();

  if (event.action === "explore") {
    event.waitUntil(clients.openWindow("/"));
  }
});

// Helper functions for IndexedDB (simplified)
async function getPendingRequests() {
  // This would typically use IndexedDB to store pending requests
  // For now, return empty array
  return [];
}

async function removePendingRequest(id) {
  // This would typically remove the request from IndexedDB
  console.log("Removing pending request:", id);
}

// Message handling
self.addEventListener("message", (event) => {
  if (event.data && event.data.type === "SKIP_WAITING") {
    self.skipWaiting();
  }
});

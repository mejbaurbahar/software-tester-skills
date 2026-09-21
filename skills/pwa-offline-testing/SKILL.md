---
name: pwa-offline-testing
description: Use when testing Progressive Web Apps and offline-first apps — service workers, caching strategies, manifest/installability, background sync, push notifications, storage quotas, update flows, and flaky-network behavior.
license: MIT
metadata:
  category: web
  version: "2.0"
  tags: pwa, service-worker, offline, workbox, manifest, background-sync, web-push, indexeddb
---

# PWA & Offline Testing

## Installability
Valid `manifest.webmanifest` (name, icons 192/512 + maskable, `start_url`, `display`, `theme_color`), HTTPS, registered service worker with fetch handler. Lighthouse PWA audit / DevTools → Application → Manifest; test install prompt on Android Chrome, iOS "Add to Home Screen" (no `beforeinstallprompt`), desktop.

## Service worker lifecycle
Install → waiting → activate → controlling. Verify: first load registers; **update flow** (new SW waits; user prompted; `skipWaiting`/`clients.claim` intentional); old caches cleaned on activate; no stale HTML pinned forever; SW scope correct; SW script itself served `Cache-Control: no-cache`.

## Caching strategies — test each route type
| Content | Strategy | Test |
| :--- | :--- | :--- |
| App shell / static assets | Cache-first (versioned) | Offline reload renders shell |
| API reads | Stale-while-revalidate / network-first | Offline shows last data + "offline" banner |
| Images | Cache-first with expiry/limit | Cache size bounded |
| Auth/payment | Network-only | Never cached; not served offline |
| POST/mutations | Background Sync queue | Offline action replays once, in order, on reconnect |

## Playwright recipes
```ts
await page.goto('/'); await page.waitForFunction(() => navigator.serviceWorker.controller);
await context.setOffline(true);
await page.reload();
await expect(page.getByText('You are offline')).toBeVisible();
await page.getByRole('button',{name:'Save'}).click();          // queued
await context.setOffline(false);
await expect.poll(() => api.count('/notes')).toBe(1);           // synced exactly once
```
DevTools: Network throttling "Slow 3G/Offline"; Application → Service Workers "Update on reload", "Bypass"; Storage → clear site data to test first-run; Lighthouse CI for PWA/perf budgets.

## Storage & data
IndexedDB/localStorage/Cache API quotas (`navigator.storage.estimate()`), eviction under pressure, `persist()`, schema migration of local DB across versions, conflict resolution on sync (last-write-wins vs merge), logout clears sensitive local data, encrypted at rest where required.

## Push & background
Permission prompt timing/deny path; VAPID; notification click deep-links; payload size; iOS 16.4+ requirements (installed PWA); unsubscribe on logout; background sync/periodic sync support fallback.

## Network chaos
Lie-fi (connected but stalled), flapping, captive portal, mid-request disconnect, slow first byte — use DevTools custom profile, `toxiproxy`, or Playwright `route.abort()/fulfill({delay})`.

## Related
`mobile-testing`, `web-performance-testing`, `cross-browser-testing`, `chaos-resilience-testing`, `e2e-testing`

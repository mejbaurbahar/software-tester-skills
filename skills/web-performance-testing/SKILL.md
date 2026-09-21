---
name: web-performance-testing
description: Use when measuring or improving front-end and page-load performance — Core Web Vitals (LCP, INP, CLS), Lighthouse CI, WebPageTest, RUM vs lab data, performance budgets, bundle size, render-blocking resources, images/fonts, caching/CDN and third-party script impact.
license: MIT
metadata:
  category: non-functional
  version: "2.0"
  tags: core-web-vitals, lcp, inp, cls, lighthouse, webpagetest, performance-budget, rum, bundle-size
---

# Web Performance Testing (Front-End)

Measure with **lab** data (repeatable, debuggable) *and* **field/RUM** data (what users truly get). Google ranks on field data (CrUX, 75th percentile).

## Targets (good @ p75)
| Metric | Good | Poor | What drives it |
| :--- | :-: | :-: | :--- |
| **LCP** Largest Contentful Paint | ≤ 2.5 s | > 4 s | server TTFB, render-blocking CSS/JS, hero image size/priority |
| **INP** Interaction to Next Paint | ≤ 200 ms | > 500 ms | long tasks, heavy handlers, hydration, main-thread JS |
| **CLS** Cumulative Layout Shift | ≤ 0.1 | > 0.25 | images/ads/embeds w/o dimensions, late fonts, injected banners |
| TTFB | ≤ 0.8 s | > 1.8 s | backend, CDN, cache |
| FCP | ≤ 1.8 s | > 3 s | critical path |

## Toolchain
```bash
npx lighthouse https://site --preset=desktop --output=html --view
npx @lhci/cli autorun                            # Lighthouse CI w/ assertions (budgets)
npx web-vitals-cli https://site                   # field-like vitals
npx bundlesize / npx source-map-explorer dist/*.js / npx vite-bundle-visualizer
# WebPageTest (real devices, filmstrip, waterfall): https://webpagetest.org
```
Field: CrUX API/PageSpeed Insights, `web-vitals` library → send to analytics/RUM (Sentry, Datadog, SpeedCurve, Vercel Analytics).
```js
import {onLCP, onINP, onCLS} from 'web-vitals';
[onLCP, onINP, onCLS].forEach(f => f(m => navigator.sendBeacon('/rum', JSON.stringify(m))));
```
Chrome DevTools MCP: `performance_start_trace`, `lighthouse_audit` (see `qa-test-harness`).

## Lighthouse CI budget (lighthouserc.json)
```json
{"ci":{"assert":{"assertions":{
  "largest-contentful-paint":["error",{"maxNumericValue":2500}],
  "cumulative-layout-shift":["error",{"maxNumericValue":0.1}],
  "total-blocking-time":["error",{"maxNumericValue":200}],
  "resource-summary:script:size":["error",{"maxNumericValue":170000}]}}}}
```

## Diagnose fast
1. **Waterfall**: TTFB high → backend/CDN/cache; late LCP resource → `preload` + `fetchpriority="high"`, avoid lazy-loading the LCP image.
2. **Main-thread**: Performance panel long tasks (>50 ms) → code-split, defer, `scheduler.yield()`, web workers, debounce, virtualize lists.
3. **Bytes**: compress (Brotli), AVIF/WebP, responsive `srcset`, subset fonts + `font-display: swap`, tree-shake, drop polyfills, HTTP/2-3.
4. **Layout shift**: reserve space (`width/height`, `aspect-ratio`), `transform` animations, font metrics overrides.
5. **Third parties**: Request Map; load async/defer/`partytown`; facade for embeds; consent-gated tags (`analytics-tracking-testing`).
6. **Caching**: immutable hashed assets (`Cache-Control: max-age=31536000, immutable`), HTML short/`stale-while-revalidate`, CDN hit ratio.

## Test conditions
Throttle CPU 4× + Slow 4G for mobile; test cold vs warm cache; logged-in vs anonymous; different geographies; run 5× and use median (variance!).

## Related
`performance-testing`, `seo-testing`, `pwa-offline-testing`, `mobile-testing`, `visual-testing`

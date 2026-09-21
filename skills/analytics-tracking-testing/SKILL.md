---
name: analytics-tracking-testing
description: Use when validating analytics and tracking — GA4/GTM dataLayer, Segment/Amplitude/Mixpanel events, pixels (Meta, TikTok), server-side tagging, consent mode, UTM/attribution, event schema/tracking plan conformance, and data parity with the backend.
license: MIT
metadata:
  category: domain
  version: "2.0"
  tags: analytics, ga4, gtm, datalayer, segment, tracking-plan, consent, utm, attribution, pixels
---

# Analytics & Tracking Testing

If tracking is wrong, every product decision built on it is wrong. Treat the **tracking plan** as a contract and test it like an API.

## 1. Tracking plan (source of truth)
`event name · trigger · properties (name/type/enum/required) · owner · destinations`. Naming: `object_action` snake_case (`checkout_started`). Version it in git; generate JSON Schema for validation (Segment Protocols, Avo, Amplitude Data).

## 2. Verify in the browser
```js
// Console: watch the dataLayer
window.dataLayer.push = new Proxy(window.dataLayer.push, { apply(t, s, a){ console.log('DL', JSON.stringify(a[0])); return Reflect.apply(t, s, a);} });
```
- GTM Preview / Tag Assistant; GA4 **DebugView** (`?debug_mode=1`); Segment Debugger; Meta Pixel Helper; `chrome://net-export` or DevTools Network filter `collect|g/collect|track`.
- Automate: Playwright intercepts requests and asserts payloads.
```ts
const hits: any[] = [];
page.on('request', r => { if (/google-analytics\.com\/g\/collect|\/v1\/track/.test(r.url())) hits.push(r.postData() ?? r.url()); });
await page.getByRole('button',{name:'Add to cart'}).click();
await expect.poll(() => hits.some(h => h.includes('add_to_cart'))).toBeTruthy();
```

## 3. What to assert
| Area | Checks |
| :--- | :--- |
| Firing | Fires **once** per action (no dupes on SPA re-render/route change); not on load unless intended; fires after success not on click |
| Payload | Names/types match plan; `currency` ISO code, `value` numeric, `items[]` complete; no PII (email, phone) unless hashed & allowed |
| Identity | `user_id` set on login, cleared on logout; anonymous→known stitching; cross-domain `_gl` linker |
| Page/route | SPA virtual pageviews, correct `page_location`, canonical vs UTM-cluttered URL |
| Attribution | UTM params captured, persisted across pages, not overwritten by internal links; referrer exclusions (payment gateways) |
| **Consent** | Nothing fires before opt-in (EU); Consent Mode v2 defaults denied; withdrawal stops tags; CMP banner accessible |
| Ecommerce | `view_item → add_to_cart → begin_checkout → purchase` funnel with same `transaction_id` (dedupe) |
| Server-side | Server events dedupe with client via `event_id`; PII hashing SHA-256; CAPI/Measurement Protocol response OK |
| Performance | Tags async, not blocking LCP; total third-party weight |
| Ad blockers/ITP | Graceful degradation; first-party endpoint |

## 4. Parity (weekly automated)
Compare analytics revenue/orders/signups vs backend DB for the same window. Expect small drift (ad-blockers ~5–15%); alert when > threshold or trend changes after a release.

## 5. Regression net
Contract test each event schema in CI (JSON Schema + example payload from E2E); block deploys that rename events or drop required props; release checklist step "tracking verified".

## Related
`e2e-testing`, `payment-ecommerce-testing`, `compliance-testing`, `seo-testing`, `observability-testing`

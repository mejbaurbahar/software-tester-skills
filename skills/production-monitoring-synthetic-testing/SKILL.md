---
name: production-monitoring-synthetic-testing
description: Use when testing in production safely (shift-right) — synthetic monitoring, canary checks, uptime probes, Playwright/Checkly/Datadog synthetics, real-user monitoring, SLO/SLI validation, alert testing, dark launches, traffic shadowing and observability-driven QA.
license: MIT
metadata:
  category: operations
  version: "2.0"
  tags: synthetic-monitoring, shift-right, slo, sli, canary, rum, uptime, checkly, alerting, testing-in-production
---

# Production Monitoring & Synthetic Testing (Shift-Right)

Pre-prod can't reproduce real data, traffic, third parties or geography. Continuously **prove production works from the user's point of view**, safely.

## Synthetic monitor types
| Type | Frequency | Example |
| :--- | :--- | :--- |
| Uptime/HTTP | 30–60 s, multi-region | `GET /healthz` 200 + body assertion, TLS expiry > 14 d |
| API transaction | 1–5 min | login → create → read → delete with test tenant |
| **Browser journey** | 5–15 min | Playwright: search → add to cart → checkout (to payment sandbox stub) |
| DNS/CDN/cert | 5 min | records, propagation, chain validity |
| Third-party dependency | 5 min | payment/email/auth provider reachability |
| Cron/heartbeat | per job | dead-man's-switch (Healthchecks.io, Cronitor) |

Tools: **Checkly** (Playwright-native), Datadog/New Relic/Grafana Synthetic, Pingdom, UptimeRobot, Better Stack, k6 Cloud browser, Sentry Crons, self-hosted Playwright in CI cron.

```ts
// Checkly/Playwright synthetic — runs every 10 min from 3 regions
import { test, expect } from '@playwright/test';
test('critical: user can search and reach checkout', async ({ page }) => {
  await page.goto('https://shop.example.com');
  await page.getByRole('searchbox').fill('headphones'); await page.keyboard.press('Enter');
  await page.getByRole('link', { name: /headphones/i }).first().click();
  await page.getByRole('button', { name: 'Add to cart' }).click();
  await expect(page.getByTestId('cart-count')).toHaveText('1');
});
```

## Safe testing in production
- Dedicated **test tenant/accounts**, flagged so they're excluded from analytics, billing, emails, inventory, and search ranking.
- Read-mostly journeys; writes use sandbox payment mode/void afterwards; auto-clean created data; idempotency keys.
- No load tests against prod unless planned/throttled; rate-limit synthetics; exclude from SLO if you must, but *include* their pass/fail in SLI.
- **Dark launch/shadow traffic**: mirror requests to new version, compare responses/latency without user impact (`goreplay`, service mesh mirroring).
- **Feature flags + canary** (`release-readiness-testing`, `configuration-feature-flag-testing`).

## SLIs, SLOs & alerts
Define SLIs from user experience: availability (good/total requests), latency (p95 < X), correctness/freshness. SLO e.g. 99.9%/30 d → error budget 43 min. Alert on **burn rate** (multi-window: 2%/1 h fast, 5%/6 h slow), not raw thresholds.
**Test your alerts**: deliberately trigger (kill synthetic, inject error via flag) and confirm page arrives, routes to right team, links runbook, and clears on recovery; test on-call escalation quarterly.

## RUM (real-user monitoring)
Web vitals by route/device/geo (`web-performance-testing`), JS errors (Sentry), API failures per release, funnel drop-offs; segment by version to detect regressions within minutes.

## Feedback loop into QA
Every incident → (1) regression test, (2) new/tuned monitor, (3) runbook fix. Track: detection time, false-alarm rate, coverage of top-10 user journeys by synthetics.

## Related
`observability-testing`, `smoke-sanity-testing`, `chaos-resilience-testing`, `release-readiness-testing`, `e2e-testing`

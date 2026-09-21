---
name: e2e-testing
description: Use when automating end-to-end user journeys through the browser or UI — Playwright, Cypress, user critical paths, resilient locators, session storage, network stubbing, and visual artifacts.
license: MIT
metadata:
  category: web
  version: "2.0"
  tags: e2e, playwright, cypress, user-journeys, locators
---

# End-to-End (E2E) Testing

E2E tests validate complete user journeys through the real UI, backend and data store. They are the most realistic and the most expensive tests: **keep few, make them critical, make them reliable.**

## Which journeys deserve an E2E test
- **Money/conversion:** search → cart → checkout → payment sandbox → confirmation (`payment-ecommerce-testing`).
- **Identity:** sign-up, sign-in, OAuth redirect, password reset, logout, session expiry.
- **Core data mutation:** create → edit → save → **reload and verify persistence** → delete.
- **Error recovery:** validation errors, network failure banner, retry, empty states.
- **Permissions:** the same journey per role (admin vs member vs read-only).
Everything else belongs at API/component level (`test-architect`). Target a suite you can run in < 15 min with sharding.

## Golden rules
1. **User-facing locators first:** `getByRole`, `getByLabel`, `getByText`; then `getByTestId`; avoid brittle CSS/XPath (`div > span:nth-child(3)`) and styling classes.
2. **Auto-wait, never sleep.** Assert on conditions: `await expect(page.getByRole('alert')).toBeVisible()`.
3. **Independent tests.** Each test sets up its own data via API and starts from a clean context; log in via stored auth state, not the UI, every time.
4. **Control the world:** stub or sandbox third parties, freeze time when relevant, seed deterministic data (`test-environment-management`).
5. **Evidence on failure:** trace, video, screenshot, console and network logs, retained as CI artifacts.
6. **One journey per test,** with meaningful assertions at each milestone (not 40 clicks then one assert).

## Playwright starter
```ts
// playwright.config.ts (essentials)
export default defineConfig({
  testDir: 'e2e', fullyParallel: true, retries: process.env.CI ? 1 : 0, workers: process.env.CI ? 4 : undefined,
  use: { baseURL: process.env.BASE_URL, trace: 'on-first-retry', video: 'retain-on-failure', screenshot: 'only-on-failure' },
  projects: [{ name: 'chromium', use: devices['Desktop Chrome'] }, { name: 'webkit', use: devices['Desktop Safari'] },
             { name: 'mobile', use: devices['Pixel 7'] }],
});
// global auth once:  npx playwright codegen --save-storage=.auth/user.json  (or a setup project using the API)
```
```ts
test('checkout with saved card', async ({ page }) => {
  await page.goto('/products/headphones');
  await page.getByRole('button', { name: 'Add to cart' }).click();
  await page.getByRole('link', { name: /cart/i }).click();
  await page.getByRole('button', { name: 'Checkout' }).click();
  await page.getByLabel('Card number').fill('4242 4242 4242 4242');      // sandbox card
  await page.getByRole('button', { name: 'Pay' }).click();
  await expect(page.getByRole('heading', { name: /thank you/i })).toBeVisible();
  expect(await api.getOrder(await orderIdFrom(page))).toMatchObject({ status: 'PAID' });  // verify backend, not just UI
});
```
```bash
npx playwright test --ui                        # debug locally
npx playwright show-trace trace.zip             # post-mortem
npx playwright test --shard=1/4                 # CI sharding
npx playwright test --repeat-each=20 e2e/checkout.spec.ts   # stability check
```
Other tools: Cypress (great DX, single-tab model), Selenium/WebDriver (broad legacy support), Puppeteer (Chrome automation), TestCafe.

## Handling hard cases
| Situation | Approach |
| :--- | :--- |
| Third-party widgets (payment iframes, captcha) | Sandbox/test keys, provider test modes; bypass captcha with a test flag in non-prod |
| Email/SMS steps | Capture inbox API (`email-notification-testing`) |
| File upload/download | `setInputFiles`, `waitForEvent('download')` |
| Multiple tabs/users | Separate browser contexts per user |
| Real-time updates | Two contexts + event assertions (`websocket-realtime-testing`) |
| Animations/loading | Disable CSS animations in test mode; wait for stable state |
| Slow environments | Fix the environment; never inflate timeouts globally |

## Add cheap extra signal in the same run
Accessibility scan per page (`@axe-core/playwright`), console-error and failed-request assertions, performance budget on key pages, visual snapshot of one or two stable views.

## Anti-patterns
Login through the UI in every test · shared mutable test accounts · asserting only "no error thrown" · chained tests that rely on earlier state · huge "mega journeys" · retries hiding real flakiness · testing what unit tests already prove.

## Related
`test-automation`, `flaky-test-management`, `cross-browser-testing`, `accessibility-testing`, `visual-testing`, `bdd-gherkin-testing`

---
name: test-automation
description: Use when writing, structuring, or debugging automated tests — Playwright/Selenium E2E suites, pytest test design, page object models, CI test integration, and deciding what's worth automating.
license: MIT
metadata:
  category: automation
  version: "2.0"
  tags: playwright, selenium, pytest, page-object-model, automation
---

# Test Automation

Automation is software: it needs design, review, and maintenance. Automate to get **fast, trustworthy feedback**, not to hit a count.

## What to automate (and what not)
| Automate | Delay or avoid |
| :--- | :--- |
| Repeated, regression-prone flows (login, checkout, core CRUD) | One-off exploratory checks |
| Release gates (smoke) | Highly visual/subjective polish (use screenshots + review, `visual-testing`) |
| API/contract checks: cheap, fast, high signal | Flows still changing weekly (maintenance drag) |
| Data-heavy rule matrices (parametrized) | Anything you cannot make deterministic yet |
Put each check at the **lowest level that can catch the bug** (`test-architect`): many unit, a healthy layer of API/integration, few UI journeys.

## Choose the framework
| Need | Good options |
| :--- | :--- |
| Modern web E2E | **Playwright** (multi-browser, auto-wait, tracing), Cypress |
| Legacy/grid/enterprise | Selenium WebDriver (+ Selenide, WebDriverIO) |
| API | pytest + requests/httpx, REST Assured, Karate, Hurl, supertest |
| Unit | pytest, Jest/Vitest, JUnit 5, Go `testing`, xUnit/NUnit |
| Mobile | Appium, Maestro, Detox, XCUITest, Espresso (`mobile-testing`) |
| BDD | Cucumber, Behave, Reqnroll (`bdd-gherkin-testing`) |
| Visual | Playwright screenshots, Percy, Chromatic, Applitools |
Prefer the language your developers already use so they can own and fix the tests.

## Design rules that keep suites healthy
- **Locators:** role/label/text/test-id over CSS/XPath; add `data-testid` if you own the app.
- **Waits:** never hard `sleep()`; use auto-wait and explicit conditions (`expect(locator).toBeVisible()`, `wait_for_selector`, poll-until with timeout).
- **Isolation:** each test creates its own data (API/fixtures), never depends on order or another test's leftovers; unique IDs per worker.
- **Fast login:** authenticate once via API and reuse storage state instead of driving the login UI every test.
- **Assert outcomes,** not implementation or intermediate loading states; one behavior per test; meaningful names.
- **Page Object / component objects / fixtures:** encapsulate locators and actions so tests read like user stories; keep assertions in tests, not page objects.
- **Test data:** builders/factories, not shared static rows (`test-data-engineering`). Reset state cheaply (transaction rollback, DB template, API teardown).
- **Determinism:** freeze time and seed randomness (`date-time-timezone-testing`); stub 3rd parties (`test-environment-management`).
- **Independent of environment:** base URL and credentials via env vars/secret store, never hard-coded.

## Examples
```ts
// Playwright: fixture + role locators + web-first assertions
import { test as base, expect } from '@playwright/test';
const test = base.extend<{ cart: CartPage }>({ cart: async ({ page }, use) => { await use(new CartPage(page)); } });
test('applies coupon once', async ({ page, cart }) => {
  await cart.open(); await cart.applyCoupon('WELCOME10');
  await expect(page.getByRole('status')).toHaveText(/10% off applied/);
  await expect(cart.total).toHaveText('$90.00');
});
```
```python
# pytest: fixtures + parametrization + markers
@pytest.fixture
def api(base_url): return Api(base_url, token=make_token(role="user"))

@pytest.mark.parametrize("qty,ok", [(0, False), (1, True), (99, True), (100, False)])
@pytest.mark.api
def test_quantity_limits(api, qty, ok):
    assert (api.add_to_cart("A-1", qty).status_code == 200) == ok
```
```bash
pytest -m "not e2e" -x --tb=short -q          # fast tier while developing
pytest -n auto --maxfail=5 -ra                # parallel CI run (pytest-xdist)
npx playwright test --workers=4 --retries=1 --trace=on-first-retry
```

## Flaky tests are bugs
Do not retry-until-green. Reproduce (`--repeat-each`), classify the cause, fix the root cause, and quarantine with an owner and deadline (`flaky-test-management`). A real race condition in the app is a product bug: report it.

## CI integration
Run tiers: smoke on every PR (< 5 min), targeted regression per PR, full nightly (`regression-testing`, `cicd-testing`). Shard and parallelize; publish JUnit/HTML reports, screenshots, traces and videos **on failure**; fail the build on real failures, not on infrastructure noise. Track duration and flake rate (`test-metrics-reporting`).

## Maintainability checklist
Naming conventions · code review for tests · no copy-paste (extract helpers) · delete obsolete tests · lint tests (no `.only`, no `sleep`) · dependency updates automated · README for running locally in one command.

## Related
`e2e-testing`, `unit-testing`, `api-testing`, `flaky-test-management`, `cicd-testing`, `test-environment-management`

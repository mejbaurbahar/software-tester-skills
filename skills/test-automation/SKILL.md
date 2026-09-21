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

## Environment (this machine)
- Python venv: `~/qa-agent/.venv/bin/python` — has pytest, playwright, requests, locust.
- Dispatcher: `qa` CLI (`qa test`, `qa smoke`, `qa regression`, `qa security`, `qa report`).
- Chrome MCP tools are available for live-browser automation/inspection alongside scripted Playwright.

## What to automate (and what not to)
Automate:
- Regression-prone flows run repeatedly (login, checkout, core CRUD).
- Anything that gates a release (smoke suite).
- API contract checks — cheap to write, fast to run, high signal.

Don't automate (or automate last):
- One-off exploratory checks.
- Highly visual/subjective UI polish — use screenshots + manual review instead.
- Flows still actively changing week to week (automation will just be a maintenance drag).

## Playwright test structure
- **Page Object Model**: one class per page/component encapsulating locators + actions. Tests read like user stories, not selector soup.
- **Locators**: prefer role/text/testid locators over CSS/XPath — they survive markup churn. Add `data-testid` to the app if none exist and you own the code.
- **Waits**: never use hard `sleep()`. Use Playwright's auto-waiting or explicit `wait_for_selector` / `wait_for_load_state("networkidle")`.
- **Isolation**: each test should set up its own data (via API/fixtures) and not depend on execution order or another test's leftover state.
- **Assertions**: assert on the outcome (DB state, API response, final DOM state), not intermediate loading states.

## pytest conventions
- One fixture per external dependency (auth session, seeded user, API client) — compose via fixture injection, not copy-paste setup.
- Parametrize equivalence-class/boundary cases with `@pytest.mark.parametrize` instead of near-duplicate test functions.
- Mark slow/E2E tests (`@pytest.mark.e2e`) separately from fast unit/API tests so CI can run tiers independently.
- Use `pytest -x --tb=short` while iterating; full traceback + `-ra` summary for CI runs.

## Flaky test triage
A test that fails intermittently is a bug in the test (or a real race condition) — don't just retry-until-green:
1. Run it 5–10x locally (`pytest --count=10` or a loop) to confirm flakiness vs. one-off environment issue.
2. Check for hard waits/timing assumptions, unseeded random data, shared state between tests, animation transitions not waited on.
3. If it's revealing a real race condition in the app, that's a product bug — report it, don't just harden the test to hide it.

## CI integration
- Fail the build on any Blocker/Critical-severity assertion failure (see [[bug-reporting]] severity scale).
- Keep smoke suite under a few minutes; push full regression to a separate longer-running job.
- Persist screenshots/traces/videos on failure (`~/qa-agent/reports/`) — a failing assertion without evidence wastes the next debugging session.

## Load/perf scripts
For scripted load testing use `locust` from the same venv — see [[performance-testing]] for methodology.

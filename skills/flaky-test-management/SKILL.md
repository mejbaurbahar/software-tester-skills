---
name: flaky-test-management
description: Use when tests pass and fail intermittently — detecting, quarantining, root-causing and eliminating flaky tests (async waits, shared state, order dependence, time, network, resource contention) with retries policy, flake dashboards and CI reruns.
license: MIT
metadata:
  category: automation
  version: "2.0"
  tags: flaky-tests, quarantine, test-stability, ci, retries, determinism
---

# Flaky Test Management

A flaky test is a test with **different outcomes on the same code**. It destroys trust: teams learn to ignore red builds. Treat flakes as bugs with an owner and SLA.

## 1. Detect & measure
- Re-run failed tests N× on the same commit (`pytest --reruns 3 --only-rerun ...`, `jest --retryTimes`, Playwright `retries`), **and record every retry-pass as a flake signal** — don't just hide it.
- Nightly: run whole suite 10–50× (`pytest -p no:randomly --count=20`, `repeat-each` in Playwright: `npx playwright test --repeat-each=20`).
- Metric: **flake rate = flaky runs / total runs** per test; alert > 1%. Suite health = % builds red for non-code reasons.

## 2. Triage decision
| Signal | Likely class | Fix direction |
| :--- | :--- | :--- |
| Fails only under parallel/CI | Shared state, ports, files, DB rows | Isolate data per test/worker; unique IDs; temp dirs |
| Fails after another test | Order dependence, leaked globals | Randomize order (`pytest-randomly`, `--shard`), reset state in teardown |
| Timing-dependent (`sleep`) | Async race | Wait for condition/event, not time (Playwright auto-wait, `expect.poll`, `await eventually`) |
| Fails at midnight/month end | Clock | Freeze time (`date-time-timezone-testing`) |
| Fails on network calls | External dependency | Stub/record (WireMock, MSW, VCR), contract tests |
| Fails with high load | Resource limits | Right-size CI, reduce parallelism, fix leaks |
| Random data | Unseeded RNG | Seed & log the seed |
| Animation/layout (UI) | Visual instability | Disable animations, wait for stable |

## 3. Bisect the cause
```bash
pytest tests/test_x.py::test_y --count=200 -x                 # reproduce rate
pytest -p randomly -p "randomly_seed=1234"                     # replay order
npx playwright test --repeat-each=50 --workers=8 --trace on    # UI flake with traces
git bisect run sh -c 'pytest -q tests/test_y.py --count=30'    # find the introducing commit
```
Add logging of env, seed, worker ID, timestamps; keep traces/videos on first failure.

## 4. Quarantine policy
1. Tag `@flaky` / move to a **non-blocking quarantine job** — *not* `skip` and forget.
2. Auto-open a ticket with owner + 7-day SLA; dashboard shows quarantined count.
3. Un-quarantine after 50+ consecutive passes; delete tests that can't be stabilised and lack value.
4. Retries are a **bandage**: cap at 1–2, never on the same test more than a week.

## 5. Prevent
Hermetic tests · unique data per test · explicit waits · no `sleep` · no shared mutable fixtures · deterministic clocks/RNG · idempotent cleanup · lint rule banning `sleep`/`waitForTimeout`.

## Related
`test-automation`, `cicd-testing`, `e2e-testing`, `concurrency-race-condition-testing`, `test-metrics-reporting`

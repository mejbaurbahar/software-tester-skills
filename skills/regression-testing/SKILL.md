---
name: regression-testing
description: Use when validating that recent changes haven't broken existing functionality — building/running regression suites, deciding regression scope for a release, and impact analysis from a diff/changelog.
license: MIT
metadata:
  category: functional
  version: "2.0"
  tags: regression, impact-analysis, test-selection, git-diff
---

# Regression Testing

Regression testing proves that **what worked before still works after a change**. The craft is choosing *enough* tests, fast, without re-running the world every time.

## 1. Scope by change impact
1. **Diff-driven:** what files/modules changed? Trace consumers: shared components, API endpoints, DB tables/migrations, feature flags, configs.
2. **Always-run core (the floor):** login/auth, checkout/payment or your business "money path", data export/import: run every release regardless of the diff.
3. **Risk-weight** the rest: likelihood of breakage (size and complexity of change, code churn, past defects) × impact (users, revenue, safety).
4. **Full regression** only for major releases, schema migrations, or upgrades of shared infrastructure (framework, ORM, auth library).

## 2. Automate test selection
```bash
jest --changedSince=origin/main            # JS: tests related to changed files
pytest --picked=branch  # pytest-picked;  or pytest-testmon:  pytest --testmon
nx affected -t test / turbo run test --filter=...[origin/main]   # monorepos
git diff --name-only origin/main...HEAD | xargs -n1 ./map-to-tests.sh   # custom mapping via tags/owners
```
Tag tests by feature and risk (`@checkout @auth @smoke @p0`) so partial runs are one flag away. Predictive selection tools (e.g. Launchable) learn from history when the suite is large.

## 3. Suite tiers
| Tier | When | Budget | Contents |
| :--- | :--- | :--- | :--- |
| Smoke | every commit/PR | < 5 min | critical paths (`smoke-sanity-testing`) |
| Targeted | every PR | < 15 min | tests mapped to the change + core floor |
| Full | nightly / pre-release | hours | everything, incl. slower E2E and cross-browser |
| Extended | release candidate | as needed | perf baseline, security scan, migration rehearsal |

Promote a manual/exploratory flow to automation after it has been run manually 2–3 times and is stable (`test-automation`). **Every fixed production bug gets a regression test** that fails without the fix.

## 4. Regression sources to re-check on purpose
- **Shared components/design system:** every consumer, not just the one that triggered the change.
- **Migrations:** new-record behavior **and** legacy rows (old data without new columns), rollback path (`data-migration-testing`).
- **Dependency upgrades:** read the changelog for breaking changes; passing tests may not cover the changed behavior.
- **Config/flags:** flag-on and flag-off both work (`configuration-feature-flag-testing`).
- **Cross-cutting:** auth, permissions, caching, i18n, time zones, feature interactions, integrations and webhooks.
- **Non-functional drift:** performance vs baseline, bundle size, accessibility, visual diffs (`visual-testing`).

## 5. Triage a failing regression test
1. **Re-run once** to rule out flakiness (`flaky-test-management`); never file a flake as a regression.
2. **Bisect** to the culprit: `git bisect run ./run-one-test.sh`, or compare with the last known-good deploy/build.
3. Decide: product bug / intended change (update the test with justification) / test bug / environment.
4. File with the introducing commit/PR when known (`bug-reporting`); it is the most useful fact for a fast fix.

## 6. Measure
Regression escape rate (bugs found in prod that an existing test *should* have caught) · suite duration and flake rate · % of defects that produced a new test · diff coverage on changed lines (`code-coverage-analysis`). Prune tests that never fail and duplicate others; keep the suite fast enough that people run it.

## Related
`smoke-sanity-testing`, `test-automation`, `flaky-test-management`, `release-readiness-testing`, `code-coverage-analysis`, `bug-reporting`

---
name: regression-testing
description: Use when validating that recent changes haven't broken existing functionality — building/running regression suites, deciding regression scope for a release, and impact analysis from a diff/changelog.
---

# Regression Testing

## Scoping a regression pass
Don't blindly re-run everything every time — scope by change impact:
1. **Diff-driven scope**: what files/modules changed? Trace which features depend on them (shared components, shared API endpoints, shared DB tables/migrations).
2. **Always-run core**: checkout/payment, auth/login, and whatever the business calls its "money path" — regardless of whether the diff touches them, run these every release as a floor.
3. **Full regression** only for major releases, schema migrations, or dependency upgrades touching shared infra (auth libs, ORMs, framework versions).

## Building a regression suite
- Promote flows from manual/exploratory testing into automation once they've been run manually 2-3 times and are stable — see [[test-automation]].
- Tag tests by area/feature so partial regression runs are possible (`@checkout`, `@auth`, `@admin`).
- Keep the suite fast enough to run every PR (smoke tier, minutes) with a separate nightly/pre-release full tier.

## Common regression sources to specifically re-check
- Shared components/design system changes — check every consumer, not just the one that prompted the change.
- Database migrations — check both new-record behavior AND existing legacy-data behavior (old rows without new columns populated).
- Dependency/library upgrades — check changelogs for breaking changes, not just "tests still pass" (tests may not cover the changed behavior).
- Config/feature-flag changes — verify both flag-on and flag-off states still work, and that the flag actually gates what it claims to.

## Running it via this harness
```
qa regression
```
Runs the harness's regression suite through the `qa` CLI dispatcher; results land in `~/qa-agent/reports/`.

## Triage discipline
When a regression test fails:
1. Confirm it's a real regression (re-run once, rule out flakiness — see [[test-automation]] flaky-test triage) before filing.
2. Bisect to the change that caused it if not obvious (git bisect, or compare against the last known-good deploy).
3. File via [[bug-reporting]] with the specific commit/PR that introduced it if identifiable — this is the single most useful piece of info for a fast fix.

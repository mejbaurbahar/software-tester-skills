---
name: cicd-testing
description: Use when designing or debugging test execution in CI/CD pipelines — PR gates, test tiering (smoke/regression/nightly), parallelization/sharding, quality gates, flaky-test tracking, and failure notification wiring. Covers GitHub Actions, GitLab CI, Jenkins and similar.
license: MIT
metadata:
  category: automation
  version: "2.0"
  tags: ci-cd, quality-gates, test-sharding, github-actions, pipelines
---

# CI/CD Testing

## Test tiering (don't run everything on every PR)
- **PR gate (minutes)**: unit tests + fast API contract checks + a thin smoke E2E suite covering the money path. This blocks merge — keep it fast and reliable or people start bypassing it.
- **Pre-deploy / merge-to-main**: fuller regression suite, still bounded (10-20 min).
- **Nightly / scheduled**: full regression, cross-browser matrix, performance baseline, security scan (SAST/DAST) — anything too slow to gate a PR.
- **Post-deploy smoke**: a small suite that runs against the just-deployed environment before traffic fully shifts, to catch environment-specific breakage config/secrets differences that staging didn't have.

## Quality gates
Define explicit, machine-checkable pass/fail criteria per stage, not "look at the dashboard":
- Merge gate: 0 failing required checks, coverage delta not regressed below threshold (if coverage-gating is used — see the caution about coverage-as-a-metric in [[qa-fundamentals]]).
- Deploy gate: regression suite green, no new Critical/Blocker security findings ([[security-testing]]), perf within budget ([[performance-testing]]).
- Make gates fail loud and specific — a gate that just says "checks failed" without linking the failing job wastes the next person's time.

## Parallelization & sharding
- Split large suites across N workers by file/test-duration balancing (not just alphabetical file split, which produces uneven shard times) — most modern runners (Playwright, pytest-xdist) support this natively.
- Keep tests independent (no shared mutable fixture/test-order dependency) — sharding surfaces hidden ordering dependencies as flaky failures, which is actually useful for finding them.
- Cache dependencies (node_modules, pip packages, browser binaries) between runs to cut pipeline time; invalidate cache correctly on lockfile change.

## Flaky test handling
- **Don't auto-retry-until-green and call it done** — track a flakiness rate per test (fails X% of runs over N runs) and treat crossing a threshold as its own bug to investigate, per [[test-automation]]'s flaky-test triage.
- Quarantine a known-flaky test (mark it non-blocking, keep it running, alert on its pattern) rather than deleting it or leaving it silently blocking merges.
- Track flaky-test rate as a first-class pipeline health metric — a suite trending flakier is losing signal even if it's still "green."

## Artifact & evidence collection
- On failure, always retain: screenshots, video/trace (Playwright `trace: 'retain-on-failure'`), console logs, network HAR, the exact commit SHA and environment. Without this, a CI failure is unreproducible days later.
- Set explicit retention windows — indefinite artifact storage silently becomes an infra cost problem.

## Notifications & bug creation
- Route failures to the owning team/channel automatically (based on changed files or test tags), not a firehose channel everyone mutes.
- Auto-create/update a tracking ticket on a *new* regression-suite failure (not on every transient CI blip) — link the failing run, commit range, and evidence.
- De-duplicate: if the same test has an open ticket, comment/bump it rather than opening a new one every run — see [[qa-code-intelligence]] for duplicate-detection approach.

## Platform notes
- **GitHub Actions**: matrix builds for cross-browser/OS; `actions/cache`; required status checks on branch protection; reusable workflows to avoid duplicating pipeline logic across repos.
- **GitLab CI**: `rules:`/`only:changes:` to scope jobs to relevant file changes; DAG (`needs:`) to parallelize instead of purely sequential stages.
- **Jenkins**: declarative pipelines over scripted for readability/maintainability; shared libraries for common QA steps across multiple pipelines.

## Reporting
When a pipeline change itself introduces a regression (e.g. a gate that stopped actually blocking), treat it with the same severity discipline as a product bug — a broken quality gate is a Critical finding because it silently removes a safety net. See [[bug-reporting]].

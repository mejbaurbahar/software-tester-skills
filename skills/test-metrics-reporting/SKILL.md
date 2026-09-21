---
name: test-metrics-reporting
description: Use when measuring and communicating quality — test metrics and KPIs (defect escape rate, DDP, MTTR, flake rate, coverage, automation ROI), dashboards, Allure/ReportPortal reporting, trend analysis, quality gates, and executive-friendly QA status reports.
license: MIT
metadata:
  category: strategy
  version: "2.0"
  tags: metrics, kpi, defect-density, dora, allure, reportportal, dashboard, quality-gate, automation-roi
---

# Test Metrics & Quality Reporting

Measure to **decide and improve**, not to police. Prefer few, trended, outcome-oriented metrics; beware Goodhart's Law.

## Metric set
| Question | Metric | Formula / note |
| :--- | :--- | :--- |
| Is testing finding bugs *before* users? | **Defect Detection Percentage (DDP)** / escape rate | `found pre-release / (pre + post-release)`; escape = post/total |
| Are we shipping quality? | Production incidents, Sev1 count, **change failure rate**, crash-free sessions | trend per release |
| How fast do we recover? | MTTR / time to restore | detection + diagnosis + fix + deploy |
| Are tests trustworthy? | **Flake rate**, mean time to fix flaky, quarantine size | `flaky runs / total runs` (`flaky-test-management`) |
| Are tests effective? | Mutation score, diff-coverage, requirement coverage | `mutation-testing`, `code-coverage-analysis` |
| Is feedback fast? | Pipeline duration p50/p90, time-to-first-failure, queue time | target PR checks < 10 min |
| Is automation paying off? | Automation ROI | `(manual hours saved × runs) − (build + maintain cost)`; % regression automated |
| Where are the bugs? | Defect density (per KLOC/story point), defects by module/root-cause/injection phase, reopened rate | drives focus & prevention |
| Is the backlog healthy? | Open defects by severity & age, SLA breaches | aging chart |
| Process health | Requirement churn, escaped requirements bugs, test case review rate | shift-left indicators |

**Avoid**: raw test-case counts, bugs-per-tester, 100% coverage targets, pass-rate alone (a 99% pass can hide the one failing critical flow).

## Dashboard (single page)
Release go/no-go banner · pass/fail/blocked by area (stacked trend) · open Sev1/Sev2 with age · flake & pipeline time trend · escape rate by release · risk heatmap (module × churn × failures) · coverage of changed lines.

## Tooling
`Allure Report`, `ReportPortal`, `Playwright HTML/JSON reporter`, `pytest-html`, `JUnit XML` → CI test analytics (GitHub Actions summaries, Buildkite Test Analytics, Datadog CI Visibility, Launchable for test selection), Grafana + Postgres/Influx, Jira dashboards, `SonarQube` quality gates.
```yaml
# Publish JUnit + trend in GitHub Actions
- run: pytest --junitxml=results.xml --cov --cov-report=xml
- uses: dorny/test-reporter@v1
  with: { name: Tests, path: results.xml, reporter: java-junit }
- run: echo "### Tests\n$(python summarize.py results.xml)" >> $GITHUB_STEP_SUMMARY
```

## Status-report template
```
Release 4.2 — GO with risks     (confidence: medium)
• Scope covered: 46/48 features; not tested: bulk export (env blocked) → risk: M
• Results: 1,204 automated (99.1% pass), 86 manual (100% executed)
• Defects: 0 Sev1, 1 Sev2 (fix ETA Tue), 7 Sev3; escape rate last release 4%
• Non-functional: p95 420 ms (target 500), 0 High vulns, WCAG AA: 2 minor
• Recommendation & decisions needed: …
```

## Root-cause analysis loop
For each escaped defect: which phase should have caught it? Why not (no test, wrong test, missed requirement, env)? Add the missing test/monitor/checklist. Report *systemic* actions monthly.

## Related
`test-planning-documentation`, `flaky-test-management`, `code-coverage-analysis`, `release-readiness-testing`, `qa-fundamentals`

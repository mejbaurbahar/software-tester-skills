---
name: test-planning-documentation
description: Use when producing test plans, test strategies, traceability matrices (RTM), entry/exit criteria, test summary reports, or IEEE 829/ISO 29119-style QA documentation — lightweight and agile-friendly formats included.
license: MIT
metadata:
  category: strategy
  version: "2.0"
  tags: test-plan, rtm, traceability, exit-criteria, test-report, iso-29119, ieee-829
---

# Test Planning & Documentation

Write the *least* documentation that lets someone else run, trust and audit the testing. Scale by risk: a one-page plan for a sprint, a full plan for a regulated release.

## One-page agile test plan
```
# Test Plan — <feature/release>   (owner, date, version)
1. Scope: in / out (explicit)
2. Risks (top 5, with likelihood × impact → test focus)
3. Approach: levels (unit/API/UI), types (functional, perf, sec, a11y), automation vs manual
4. Environments & data: URLs, accounts, seeds, third-party sandboxes
5. Entry criteria / Exit criteria (measurable)
6. Schedule & roles (who tests, who signs off)
7. Deliverables: reports, dashboards, defect list
8. Assumptions, dependencies, open questions
```

## Full plan additions (IEEE 829 / ISO 29119)
Test items & versions · features to be / not to be tested · pass/fail criteria · suspension/resumption criteria · test deliverables · staffing/training · risk & contingency · approvals.

## Entry / Exit criteria examples
- **Entry:** build deployed; smoke suite green; requirements baselined; data ready.
- **Exit:** 100% Must-have cases executed; ≥95% pass; 0 open Sev1/Sev2; ≤5 Sev3 with workarounds; code coverage ≥ agreed on changed lines; perf p95 ≤ target; sign-off recorded.

## Requirements Traceability Matrix (RTM)
| Req ID | Requirement | Risk | Test cases | Automated | Last result | Defects |
| :--- | :--- | :-: | :--- | :-: | :-: | :--- |
| REQ-12 | Refund ≤ 5 min | H | TC-101..104 | Y | Pass | — |
Gaps = requirements with no test (missing coverage) and tests with no requirement (gold-plating).

## Test case template
`ID · Title · Requirement · Priority · Preconditions · Steps · Test data · Expected result · Actual · Status · Technique · Automation ref`

## Test summary report (send at each exit)
Scope tested · results (executed/pass/fail/blocked) · defects by severity/status · coverage vs plan · deviations · residual risk · **go / no-go recommendation** with reasons. Lead with the recommendation.

## Tips
Version-control docs next to code (`/docs/testing`); generate RTM from tags (`@REQ-12`) rather than by hand; keep plans living—update on scope change.

## Related
`test-strategist`, `test-metrics-reporting`, `bug-reporting`, `release-readiness-testing`, `acceptance-testing`

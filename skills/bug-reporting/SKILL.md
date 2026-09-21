---
name: bug-reporting
description: Use whenever filing a defect found during any kind of testing — applies a standard severity scale, report template, and evidence requirements so bug reports are consistent, reproducible and actionable.
license: MIT
metadata:
  category: strategy
  version: "2.0"
  tags: bug-report, defect, severity, reproduction-steps, evidence
---

# Bug Reporting

A good bug report lets a stranger reproduce, understand and prioritize the problem in two minutes. This is the shared format every testing skill files through.

## Verify before you file
Never declare a defect (or a pass) on assumption:
- Check the **actual** HTTP status, DOM state and persisted data, not just how the page looked.
- Capture **console errors and network request/response** evidence.
- In browser tests wait for a condition (selector/network idle) before asserting; a race-condition false failure wastes everyone's time.
- Reproduce **at least twice** and note the rate ("5/5", "2/10"). Try to isolate the minimal steps, and check whether it is a duplicate.
- Decide whether it is a product bug, test bug, environment issue or requirement gap.

## Severity vs priority
| Severity (impact on users/system) | Meaning |
| :--- | :--- |
| **Blocker (S1)** | Crash, data loss/corruption, core transaction impossible, security breach in progress |
| **Critical (S2)** | Core feature severely impaired, no workaround (auth broken, checkout broken, cross-tenant data leak) |
| **Major (S3)** | Non-core feature fails, or a common edge case with a workaround |
| **Minor (S4)** | Cosmetic, copy, low-impact annoyance |
**Priority (P0–P3)** is the *order to fix*, set with product/engineering using business context. Severity reflects real-world impact and exploitability, not how the bug was found: a cosmetic issue found during a security audit stays Minor; an unauthenticated data leak is Critical even if it looks like "just a UI thing".

## Report template
```markdown
# [Component] Short, specific symptom (not "X is broken")

- **Severity / Priority**: Critical / P1
- **Environment**: Staging · build 2026.09.21-abc123 · Chrome 128 / macOS 15 (or device/OS)
- **URL / endpoint**: https://…
- **Reproducibility**: 5/5

### Preconditions
Account/role, data state, feature flags.

### Steps to reproduce
1. …
2. …

### Expected result
…
### Actual result
…

### Evidence
- Console: `TypeError: Cannot read properties of undefined (reading 'id')` at cart.js:88
- Network: `POST /api/v1/orders` → 500, response body/`x-request-id: 7f3c…`
- Screenshot/video/HAR/log excerpt (redacted)

### Impact and suspected cause
Who is affected, how many, workaround. Mark theories clearly as hypotheses.
```
Title formula: `[Area] Action → wrong result (condition)`, e.g. `[Checkout] Applying coupon after changing country → total not recalculated`.

## Filing mechanics
```bash
gh issue create --title "[Checkout] Coupon not recalculated after country change" --body-file bug.md --label bug,severity:critical
```
Attach the smallest useful evidence; link to the failing test, trace or CI run; reference the commit or release that introduced it if known. Group symptoms with one root cause into one report.

## Safety and privacy
- **Redact** real user PII, tokens, passwords and API keys from screenshots, HARs and logs, even on internal environments.
- For **security findings**, use the private disclosure channel (security advisory, restricted tracker, security@ mailbox), include only what is needed to reproduce and verify the fix, and do not publish working exploit chains.

## Quality checklist
Title specific · steps numbered and minimal · expected vs actual explicit · environment and build named · evidence attached · severity justified · duplicate checked · no secrets.

## Related
`manual-testing`, `exploratory-testing`, `functional-testing`, `api-testing`, `regression-testing`, `test-metrics-reporting`

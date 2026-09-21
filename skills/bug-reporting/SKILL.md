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

This is the shared reporting spine for every testing skill in this harness — [[manual-testing]], [[functional-testing]], [[api-testing]], [[security-testing]], [[performance-testing]], [[accessibility-testing]], [[mobile-testing]], [[regression-testing]] all file through this format. Canonical source: `~/qa-agent/QA_RULES.md`.

## Verification standard before filing
Never declare a defect (or a passing test) based on assumption:
- Verify HTTP status codes, not just "the page looked wrong."
- Verify actual DOM/element state, not a screenshot glance.
- Verify database mutations or backend state for anything claiming data was/wasn't persisted.
- Capture console errors and network request/response evidence, not just a description.
- In browser testing, wait for network-idle or selector-availability before asserting — a false failure from a race condition wastes everyone's time.

## Severity scale
- **Blocker (Sev 1)**: system crash, core transaction impossible, data loss, catastrophic resource leak.
- **Critical (Sev 2)**: core functionality severely impaired, no acceptable workaround (auth broken, checkout broken, cross-tenant data leak).
- **Major (Sev 3)**: non-critical feature failure, or a high-frequency edge case with a workaround.
- **Minor (Sev 4)**: cosmetic, copy error, low-impact UX annoyance.

Severity is about real-world impact and exploitability/frequency — not how the bug was found. A cosmetic misalignment stays Minor even if found during a security audit; an unauthenticated data leak is Critical/Blocker even if it looks like "just a UI thing" at first glance.

## Report template
```markdown
# [BUG] [Component] Title of the Issue

- **Severity**: Blocker | Critical | Major | Minor
- **Priority**: P0 | P1 | P2 | P3
- **Environment**: Staging / Production / Local (Browser/OS/device version)
- **URL / Endpoint**: https://...

### Preconditions
- User logged in as admin / test account, feature flag state, etc.

### Reproduction Steps
1. Navigate to ...
2. Click on ...
3. Input ...

### Expected Result
...

### Actual Result
...

### Diagnostics & Evidence
- **Console Errors**: `TypeError: ...`
- **Network Request**: `POST /api/v1/...` -> Status `500 Internal Server Error`
- **Screenshot**: `~/qa-agent/reports/screenshots/...`

### Impact & Root Cause Analysis
...
```

## Filing mechanics in this harness
- Save reports under `~/qa-agent/reports/`.
- `qa report` surfaces/aggregates filed reports through the CLI dispatcher.
- Never include a full working exploit chain for security findings beyond what's needed to reproduce internally — keep destructive PoCs out of shared reports.
- Redact real user PII/credentials from evidence (screenshots, logs) before saving/sharing a report, even on internal staging environments.

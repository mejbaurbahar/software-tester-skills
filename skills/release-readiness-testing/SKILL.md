---
name: release-readiness-testing
description: Use when deciding whether to ship — go/no-go criteria, release checklists, canary/blue-green/progressive rollout verification, post-deploy smoke, rollback rehearsal, DORA metrics, change-risk scoring, and release sign-off reports.
license: MIT
metadata:
  category: strategy
  version: "2.0"
  tags: release, go-no-go, canary, blue-green, rollback, dora, deployment, post-deploy, change-risk
---

# Release Readiness & Deployment Verification

Answer "**Is this safe to ship, and how will we know fast if it isn't?**" with evidence, not vibes.

## Go / No-Go scorecard
| Gate | Evidence | Pass rule |
| :--- | :--- | :--- |
| Functional | Regression + new-feature results | 100% Must pass, 0 Sev1/Sev2 open |
| Non-functional | Perf vs baseline, security scan, a11y | p95 within +10%; 0 Critical/High vulns; no new WCAG AA fails |
| Data | Migration rehearsed; backward-compat N/N-1 | Reconciled; rollback tested |
| Operability | Dashboards, alerts, runbook, on-call aware | SLO alerts exist for new paths |
| Rollout | Flag/kill-switch, canary plan | Halt criteria defined |
| Compliance/Docs | Legal, privacy, release notes, support briefed | Signed |
| Risk | Change risk score (size × criticality × novelty × blast radius) | Below threshold or mitigated |

**Change-risk heuristics**: touches auth/payments/data schema (+), large diff (+), first-time contributor to area (+), late Friday (+), weak test coverage on changed lines (+), feature-flagged (–), easily reversible (–), automated rollback (–).

## Pre-release checklist
Build reproducible & signed · versions/changelog · config diff prod vs staging (`configuration-feature-flag-testing`) · migrations ordered & backward-compatible · secrets present · dependencies scanned (`supply-chain-dependency-testing`) · smoke suite green on the *release candidate artifact* · perf smoke · feature flags default OFF · rollback command written & tested · comms plan.

## Progressive delivery verification
1. **Deploy dark** (0% traffic) → post-deploy smoke against prod URL (`smoke-sanity-testing`).
2. **Canary 1–5%** for 10–30 min: compare canary vs baseline on error rate, p95 latency, saturation, business KPIs (orders/min, sign-ups) — automated analysis (Argo Rollouts/Flagger/Kayenta).
3. Ramp 25% → 50% → 100% with bake time; auto-rollback on SLO breach.
4. **Blue/green**: keep old env warm; switch back = instant rollback; verify DB compat both directions.
5. **Post-release** 24–48 h: error budget burn, support tickets, crash-free rate, analytics parity.

```bash
kubectl argo rollouts get rollout app --watch
kubectl rollout status deploy/app --timeout=5m && ./smoke.sh https://prod.example.com
kubectl rollout undo deploy/app                          # rehearse this!
```

## Release report (1 page)
Recommendation (GO / GO-with-risks / NO-GO) first → scope → test evidence links → open defects & accepted risks (owner, mitigation) → rollout & rollback plan → monitoring links → approvers.

## DORA metrics to trend
Deployment frequency · lead time for changes · change failure rate · time to restore (MTTR). Improve by shrinking batch size, not adding gates.

## Related
`smoke-sanity-testing`, `regression-testing`, `production-monitoring-synthetic-testing`, `test-planning-documentation`, `cicd-testing`

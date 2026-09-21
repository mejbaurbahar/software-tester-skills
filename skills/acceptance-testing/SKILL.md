---
name: acceptance-testing
description: Use when validating a feature against business needs before release — user acceptance testing (UAT), alpha/beta programs, acceptance criteria, sign-off, contract/operational acceptance, and "is this ready for the customer?" decisions.
license: MIT
metadata:
  category: functional
  version: "2.0"
  tags: uat, acceptance-criteria, sign-off, beta, alpha, business-validation
---

# Acceptance Testing (UAT, OAT, Alpha/Beta)

Acceptance testing answers one question: **does the system let the business/user do the job they bought it for?** Verification ("built right") is done by then; this is validation ("built the right thing").

## When to use / not use
- Use: pre-release sign-off, contract milestones, regulated releases, customer pilots, beta programs.
- Don't use it to find low-level bugs — that is unit/integration/system testing. A UAT that finds 50 crashes means earlier levels failed.

## The five acceptance types
| Type | Who | Question |
| :--- | :--- | :--- |
| **UAT** | Business users / product owner | Does it support real workflows? |
| **OAT / Operational** | Ops, SRE | Can we deploy, monitor, back up, restore, upgrade it? |
| **Contractual** | Customer + legal | Are the contract's acceptance criteria met? |
| **Regulatory** | Compliance | Does it satisfy the applicable regulation/standard? |
| **Alpha / Beta** | Internal / external early users | Does it survive real usage & real data? |

## Workflow
1. **Collect acceptance criteria** from stories/contracts. Rewrite each as a *testable* statement (Given/When/Then, measurable threshold). Reject vague ones ("fast", "user-friendly") and ask for numbers.
2. **Define entry criteria**: system test passed, no open Sev1/Sev2, test data + UAT environment ready, testers trained.
3. **Build the UAT scenario set** from real end-to-end business processes — *not* from the UI screens. One scenario = one user goal, start to finish, with realistic data.
4. **Trace**: map every acceptance criterion → ≥1 scenario (see `test-planning-documentation` for RTM).
5. **Execute with business users**, time-boxed. Capture evidence (screenshots, recordings, data before/after).
6. **Triage defects** live: *defect* vs *change request* vs *misunderstanding* (training gap). Only defects block sign-off.
7. **Exit / sign-off**: all Must criteria pass, zero open Sev1/Sev2, agreed workarounds documented for Sev3, formal sign-off recorded (name, date, version/build).

## Scenario template
```
ID: UAT-014        Priority: Must        Criterion: AC-7 (refund within 5 min)
Persona: Support agent, EU region
Pre-state: Order #A-991 paid, shipped, within 30-day window
Steps: 1) Open order  2) Issue partial refund 40%  3) Confirm customer email
Expected: Ledger shows -40%; email sent < 5 min; audit log has agent ID
Evidence: recording + ledger export        Result: PASS / FAIL / BLOCKED
```

## Beta program checklist
- Feature flag + kill switch; % rollout (1 → 5 → 25 → 100).
- Feedback channel in-product; telemetry for errors, funnels, latency.
- Explicit exit metrics (crash-free sessions ≥ 99.5%, task success ≥ 90%, NPS trend).

## Pitfalls
- Testers who were never trained → false failures. Run a 30-min walkthrough first.
- Testing on synthetic/empty data → misses real-world volume and edge data. Use masked production-like data (`test-data-engineering`).
- Sign-off by someone with no authority. Record the *accountable* approver up front.
- Scope creep: new asks discovered in UAT go to the backlog, not the release gate.

## Related skills
`bdd-gherkin-testing`, `test-planning-documentation`, `release-readiness-testing`, `usability-testing`, `system-testing`

---
name: qa-fundamentals
description: Use when scoping test strategy, writing a test plan, classifying testing types (QC vs QA, verification vs validation), applying risk-based prioritization, or navigating SDLC/STLC/Agile testing process questions. The conceptual root the other testing skills build on.
license: MIT
metadata:
  category: strategy
  version: "2.0"
  tags: stlc, test-levels, verification, validation, quality-metrics
---

# QA Fundamentals

## Core distinctions (get these right, they change what you do)
- **QA vs QC**: QA is process-focused, preventive ("are we building it right, with a process that prevents defects"). QC is product-focused, detective (testing the actual output). Testing is a QC activity inside a broader QA process.
- **Verification vs Validation**: Verification asks "did we build the product right" (spec conformance — reviews, static analysis). Validation asks "did we build the right product" (does it satisfy the actual user need — testing against real usage).
- **SDLC vs STLC**: SDLC is the whole software lifecycle (requirements→design→build→deploy→maintain). STLC is the testing-specific sub-lifecycle running alongside it: requirement analysis → test planning → test case design → environment setup → execution → closure.

## Test strategy vs test plan
- **Strategy** = org/product-level, stable across releases: what testing types are mandatory, tooling standards, environments, entry/exit criteria philosophy, risk appetite.
- **Plan** = per-release/per-feature, derived from strategy: specific scope, schedule, owners, this release's risk areas.

## Risk-based testing (how to prioritize when time is limited)
Score each feature/area on two axes and test in priority order:
- **Likelihood of failure** — new/complex code, recently changed, historically buggy area, third-party dependency.
- **Impact of failure** — revenue path, data loss potential, compliance/legal exposure, blast radius (all users vs one edge case).
High-likelihood × high-impact gets deep coverage; low×low gets a smoke check or skipped under time pressure — say so explicitly rather than silently under-testing it.

## Shift-left / shift-right / continuous testing
- **Shift-left**: push testing earlier — test design from requirements before code exists, static analysis and unit tests in the dev loop, PR-gate checks. Cheaper to fix bugs here.
- **Shift-right**: test in/near production safely — canary releases, feature flags with monitoring, synthetic monitoring, real-user monitoring, production A/B validation. See [[observability-testing]].
- **Continuous testing**: testing is a pipeline stage, not a phase — every commit triggers the relevant test tier automatically. See [[cicd-testing]].

## Agile/Scrum/Kanban testing
- In Scrum: testing happens within the sprint, not after it — "done" means tested, not "coded, QA next sprint." Write acceptance criteria as testable Given/When/Then before development starts, not after.
- In Kanban: testing is continuous flow-matched to WIP limits; a feature isn't "done" until it clears its test column, which caps how much can be in-flight untested at once.
- Definition of Ready (testable requirements) and Definition of Done (tested, not just coded) are the two contracts that make Agile testing work — if either is missing/vague, that's the root cause of most "QA is a bottleneck" complaints, and it's a process gap, not a testing-effort gap.

## Defect lifecycle
`New → Triaged (severity/priority assigned) → Assigned → In Progress → Fixed → Retest → Verified/Reopened → Closed`. See [[bug-reporting]] for the severity scale and report template used at the Triaged step, and [[qa-code-intelligence]] for root cause analysis.

## Quality gates and release readiness
A release gate should be an explicit, checkable list, not a vibe: zero open Blocker/Critical defects, regression suite green (see [[regression-testing]]), perf within budget (see [[performance-testing]]), no new high/critical security findings (see [[security-testing]]), and rollback plan documented. If any of these can't be verified, say that plainly rather than declaring "ready to ship."

## Traceability
Map requirement → test case → automation test → last execution result. When a requirement changes, this tells you exactly which tests need review — without it, coverage gaps hide until production finds them.

## Metrics worth tracking (and ones to be wary of)
Useful: defect escape rate (bugs found in prod vs pre-prod), regression suite pass-rate trend, flaky-test rate, mean time to detect/fix. Misleading if used alone: raw test-case count, raw bug count (rewards finding trivial bugs over investigating hard ones), % code coverage (high coverage with weak assertions is false confidence — see [[test-automation]]).

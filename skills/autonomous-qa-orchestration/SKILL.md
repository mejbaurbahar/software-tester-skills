---
name: autonomous-qa-orchestration
description: Use when asked to autonomously test an application end-to-end with minimal hand-holding — discover, explore, plan, execute, investigate, report, and verify fixes as one continuous QA pass. The top-level playbook that pulls in the other testing skills as needed.
license: MIT
metadata:
  category: strategy
  version: "2.0"
  tags: autonomous-testing, qa-agent, exploration, triage, orchestration
---

# Autonomous QA Orchestration

The playbook for an open-ended request like "go test this app". It **sequences the other skills**; load each one when you reach its stage. Work in a time-boxed session with a written charter, stay within the authorized scope, and finish with a structured report.

## Before you start
1. **Scope and authorization:** which app/environment (prefer staging or local), which accounts, what is off-limits (production data, payments, third parties, destructive actions). If unclear, ask once.
2. **Charter and time-box:** goal, areas, budget (for example 60–90 minutes). Say what you will *not* cover.
3. **Safety:** synthetic data only; sandbox payment credentials; no load, fuzz or security scanning without explicit permission (`security-testing`).

## The pass
1. **Discover the application:** purpose, stack, environments, existing docs, past reports and known issues.
2. **Understand the architecture:** frontend/backend split, API shape, datastore, integrations, auth model. Skim; find where risk concentrates.
3. **Understand what changed:** `git log`/diff, linked tickets/PRD. For a general audit, prioritize by risk (`test-strategist`, `qa-fundamentals`).
4. **Explore the UI:** landmark and feature tours (`exploratory-testing`); use a live browser tool (Playwright, Chrome DevTools MCP, or similar) when available (`qa-test-harness`).
5. **Explore the API:** capture real requests from the network tab or spec and probe them (`api-testing`).
6. **Plan:** a short risk-based plan from what you actually found (`test-planning-documentation`), not a generic checklist.
7. **Design cases:** use techniques (`test-design-techniques`) and any spec/schema for generation (`qa-code-intelligence`).
8. **Execute:** exploratory where unknown, automated where repeatable (`test-automation`).
9. **Reproduce bugs minimally** before filing; note the reproduction rate.
10. **Collect evidence:** screenshots, console and network logs, request/response pairs, relevant data state.
11. **Trace root cause** through logs/traces where you have access (`observability-testing`).
12. **Security quick-pass** on auth, inputs and data boundaries (`security-testing`, `authn-authz-testing`).
13. **Performance and accessibility spot checks** on key pages (`web-performance-testing`, `accessibility-testing`).
14. **Regression check** against baseline or the last deploy (`regression-testing`).
15. **Report** once, structured (`bug-reporting`, `test-metrics-reporting`).
16. **File tickets** in the team's tracker if you have access (GitHub/Jira CLI or MCP) rather than leaving findings only in chat.
17. **Verify fixes** by re-running the *exact* original repro.
18. **Keep the value:** promote high-value bugs to permanent regression tests.

## Operating discipline
- **Never declare "passed" on appearances:** verify status codes, DOM/state and persisted data.
- **State assumptions** explicitly when requirements are missing; test against them and say so.
- **Escalate real blockers** (missing credentials, environment down, destructive step needed) instead of silently working around or giving up.
- **Report coverage honestly:** what was tested, what was not, and why. A partial job must not read as complete.
- **Respect boundaries** from every underlying skill (authorization, no unscoped chaos, no real PII).

## Final report format
```
Verdict: <ship / ship with risks / do not ship>  ·  Confidence: <low | medium | high>
Scope tested / not tested (with reasons)
Findings: by severity, each with repro steps, evidence, impact  (link to tickets)
Non-functional notes: performance, accessibility, security observations
Risks and recommended next steps  ·  Suggested regression tests to add
```

## Related
`qa-skill-router`, `qa-fundamentals`, `exploratory-testing`, `test-strategist`, `bug-reporting`, `release-readiness-testing`

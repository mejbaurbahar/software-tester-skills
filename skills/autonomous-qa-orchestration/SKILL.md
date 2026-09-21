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

This is the playbook for an open-ended "go test this" request. It sequences the other skills in this library rather than duplicating their content — pull each one in when you reach that stage.

## The pass
1. **Discover the application** — what is it, what stack, what environment (staging/prod/local), what's already known about it (existing memory/reports, `~/qa-agent/reports/`, prior findings).
2. **Understand architecture** — frontend/backend split, API shape, DB, third-party integrations, auth model. Skim rather than exhaustively read — enough to know where risk concentrates.
3. **Understand requirements/scope** — what changed recently (git log/diff, linked ticket/PRD) if this is feature-specific; if it's a general audit, use risk-based prioritization from [[qa-fundamentals]] to decide where to spend time.
4. **Explore the UI** — landmark tour per [[manual-testing]]'s exploratory testing method; use Claude in Chrome / Chrome DevTools MCP for live interaction.
5. **Explore the API** — capture real requests via network inspection, replay/probe per [[api-testing]].
6. **Generate a test plan** — scoped to what was actually found in steps 1-5, using [[qa-fundamentals]]'s test plan structure; don't run a generic checklist disconnected from the actual app.
7. **Generate test cases** — via [[manual-testing]]'s design techniques and, where a schema/spec exists, [[qa-code-intelligence]]'s automatic generation approach.
8. **Execute** — manual where exploratory, automated where repeatable (promote to [[test-automation]] if the flow is worth keeping).
9. **Discover & reproduce bugs** — minimal reliable repro before filing, per [[qa-code-intelligence]].
10. **Collect evidence** — screenshots, console logs, network requests/responses, relevant DB state.
11. **Investigate backend/logs/traces** — walk the observability chain per [[observability-testing]] and [[qa-code-intelligence]] to find actual root cause, not just symptom.
12. **Run security checks** on anything touching auth, user input, or data boundaries — at minimum the OWASP quick-pass in [[security-testing]], not a full pentest unless asked.
13. **Run performance checks** if the task involves load-sensitive paths — see [[performance-testing]].
14. **Compare against baseline / detect regressions** — per [[regression-testing]], especially if this follows a recent deploy.
15. **Generate the report** — one structured report per [[bug-reporting]], not a stream-of-consciousness log; group related findings, state severity with evidence.
16. **Create/update tickets** if the harness has ticket integration available (Jira/GitHub — check for `jira`/`github` skill availability) rather than leaving findings only in chat.
17. **Re-run failed tests / verify fixes** when asked to confirm a fix — re-execute the exact original repro, don't just spot-check something adjacent.
18. **Maintain the regression suite** — promote newly-found, high-value bugs into permanent regression tests so they can't silently reappear, per [[regression-testing]] and [[qa-code-intelligence]].

## Operating discipline
- **Never declare "passed" without verification** — the standard from [[bug-reporting]] applies throughout: check actual HTTP status/DOM state/DB state, not appearances.
- **Time-box exploration** — an open-ended "test this" request can expand indefinitely; scope to a session/charter (per [[manual-testing]]) and report what was and wasn't covered, rather than silently doing a partial job and calling it complete.
- **State assumptions explicitly** — when requirements are ambiguous or missing, say what assumption was tested against rather than silently guessing.
- **Escalate genuine blockers** — missing credentials, an environment that's down, a destructive action needed that wasn't authorized — surface these rather than working around them silently or giving up silently.
- **Respect safety boundaries** from every underlying skill: no unauthorized security testing ([[security-testing]]), no unscoped chaos experiments ([[chaos-resilience-testing]]), no raw production PII in test data ([[test-data-engineering]]).

## This harness's specific tooling
- Environment: `~/qa-agent/.venv/bin/python` (pytest, playwright, requests, locust); `qa` CLI dispatcher (`qa test`, `qa smoke`, `qa regression`, `qa security`, `qa report`); Chrome DevTools MCP on port 9222; reports to `~/qa-agent/reports/`; audit log to `~/qa-agent/memory/audit.log`.
- Both Claude CLI and Antigravity CLI read from this shared skill knowledge — Antigravity's `qa_command_center` router (`~/qa-agent/skills/qa_command_center/SKILL.json`) lists all sub-skills and should be kept in sync when new skills are added here.

---
name: qa-skill-router
description: Use when the user asks what to test, which testing approach or skill to use, "where do I start", or describes a QA task without naming a skill — routes the request to the right software-testing skills and gives the order to apply them.
license: MIT
metadata:
  category: strategy
  version: "2.0"
  tags: router, index, catalog, qa-help, skill-selection, getting-started
---

# QA Skill Router

Pick the **smallest set of skills** (usually 1–3) that fits the task, load them, and say which you chose and why. Do not load skills that do not apply.

## Step 1 — Classify the request
Ask (or infer): *What is the artifact (code, API, UI, data, infra, model)? What is the goal (find bugs, prevent regressions, prove compliance, measure quality)? What is the risk?* If the artifact or goal is unclear and guessing would waste effort, ask one short question.

## Step 2 — Route by intent
| The user wants to… | Use |
| :--- | :--- |
| Decide what/how much to test, plan, strategy | `test-strategist`, `test-architect`, `testing-strategies`, `test-planning-documentation`, `qa-fundamentals`, `qa-engineering` |
| Check requirements/specs before coding | `requirements-testing-review`, `bdd-gherkin-testing` |
| Derive test cases systematically | `test-design-techniques`, `manual-testing`, `functional-testing` |
| Test unit/component logic | `unit-testing`, `tdd-workflow`, `property-based-testing`, `snapshot-golden-testing`, `mutation-testing`, `code-coverage-analysis` |
| Hunt crashes/parsers/edge input | `fuzz-testing`, `property-based-testing` |
| Threading, double-submit, locking bugs | `concurrency-race-condition-testing` |
| Dates, time zones, DST, scheduling | `date-time-timezone-testing` |
| Leaks, resource growth, OOM | `memory-leak-resource-testing` |
| Test how services fit together | `integration-testing`, `contract-testing`, `microservices-testing`, `system-testing` |
| REST/GraphQL/real-time/messaging | `api-testing`, `graphql-testing`, `websocket-realtime-testing`, `event-driven-messaging-testing`, `serverless-testing` |
| Browser/UI journeys | `e2e-testing`, `test-automation`, `webapp-testing`, `qa-test-harness`, `cross-browser-testing`, `visual-testing` |
| UX, accessibility, i18n | `usability-testing`, `accessibility-testing`, `localization-testing` |
| Web performance & SEO | `web-performance-testing`, `seo-testing`, `pwa-offline-testing` |
| Load, capacity, scaling | `performance-testing`, `scalability-capacity-testing` |
| Resilience, failure, recovery | `chaos-resilience-testing`, `disaster-recovery-backup-testing` |
| Databases, data quality, migrations | `database-testing`, `data-pipeline-etl-testing`, `data-migration-testing`, `test-data-engineering` |
| Login, permissions, tenants | `authn-authz-testing` |
| Security review/testing (defensive) | `security-testing`, `security-owasp`, `security-hardening`, `threat-modeling`, `static-analysis-testing`, `supply-chain-dependency-testing`, `iac-container-security-testing`, `42crunch-api-security-testing` |
| Compliance & privacy | `compliance-testing` |
| Mobile, desktop, CLI, IoT, games, blockchain | `mobile-testing`, `desktop-app-testing`, `cli-testing`, `iot-embedded-testing`, `game-testing`, `blockchain-smart-contract-testing` |
| Payments, e-commerce, email, analytics | `payment-ecommerce-testing`, `email-notification-testing`, `analytics-tracking-testing` |
| Experiments and flags | `a-b-testing`, `configuration-feature-flag-testing` |
| AI/ML/LLM/agents | `ai-ml-testing`, `llm-testing`, `rag-evaluation-testing`, `ai-agent-evaluation`, `chatbot-voice-agent-testing`, `mcp-testing`, `llm-security-audit`, `ai-code-security` |
| CI/CD, environments, flaky tests | `cicd-testing`, `test-environment-management`, `flaky-test-management` |
| Ship/no-ship, post-deploy, monitoring | `release-readiness-testing`, `smoke-sanity-testing`, `regression-testing`, `production-monitoring-synthetic-testing`, `observability-testing`, `installation-upgrade-testing`, `compatibility-testing`, `cloud-infrastructure-testing` |
| Acceptance, UAT, system-level | `acceptance-testing`, `system-testing`, `exploratory-testing` |
| Report bugs, metrics, status | `bug-reporting`, `test-metrics-reporting` |
| "Go test this app for me" | `autonomous-qa-orchestration`, `qa-code-intelligence` |

## Step 3 — Sequence
Typical order for a new feature: `requirements-testing-review` → `test-design-techniques` → `unit-testing`/`tdd-workflow` → `api-testing` or `integration-testing` → `e2e-testing` (few, critical) → non-functional (`performance-testing`, `accessibility-testing`, security) → `release-readiness-testing` → `production-monitoring-synthetic-testing`.

## Step 4 — Respond
State the chosen skills in one line each ("`api-testing` — you have a REST API with auth"), then proceed with the work. Offer the matching slash command when the tool supports commands (`/test-plan`, `/unit-tests`, `/api-tests`, `/e2e-tests`, `/security-audit`, `/perf-plan`, `/a11y-audit`, `/flaky-triage`, `/release-check`, `/qa-audit`).

## Safety
Security and load testing only against systems the user owns or is explicitly authorized to test; prefer staging; never use real customer data or live payment credentials.

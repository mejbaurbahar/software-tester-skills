# Software Tester Skills 🧪

**Give your AI coding agent a senior tester's playbook.**

<!-- tagline:start -->
**97 open-source Agent Skills and 21 slash commands** for unit, API, end-to-end, security, performance, accessibility, data, mobile, AI/LLM testing and more. Works in **Claude Code, Google Antigravity, Gemini CLI, OpenAI Codex and Cursor**.
<!-- tagline:end -->

<!-- badges:start -->
[![CI](https://github.com/mejbaurbahar/software-tester-skills/actions/workflows/validate-skills.yml/badge.svg)](https://github.com/mejbaurbahar/software-tester-skills/actions/workflows/validate-skills.yml)
[![Skills](https://img.shields.io/badge/skills-97-0B6B52.svg)](https://mejbaurbahar.github.io/software-tester-skills/#skills)
[![Slash commands](https://img.shields.io/badge/slash%20commands-21-0B5CAD.svg)](#-slash-commands)
[![Agent Skills](https://img.shields.io/badge/standard-agentskills.io-101A2B.svg)](https://agentskills.io)
[![Website](https://img.shields.io/badge/website-live-8A5A00.svg)](https://mejbaurbahar.github.io/software-tester-skills/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Stars](https://img.shields.io/github/stars/mejbaurbahar/software-tester-skills?style=flat&logo=github)](https://github.com/mejbaurbahar/software-tester-skills/stargazers)
<!-- badges:end -->

**[🌐 Browse the catalog →](https://mejbaurbahar.github.io/software-tester-skills/)** · [Install](#-install) · [Slash commands](#-slash-commands) · [All skills](#-skill-catalog) · [Contribute](CONTRIBUTING.md)

---

## Why this exists

AI agents write tests quickly, and often the wrong ones: shallow assertions, flaky waits, no negative cases, no thought about risk. Each skill here is a focused playbook the agent loads **only when your task matches**, so it follows a real testing procedure instead of improvising.

- **Broad:** from test strategy and TDD to fuzzing, GraphQL, data pipelines, payments, IoT, games and LLM agents.
- **Practical:** decision tables, copy-paste commands, CI snippets, checklists and pitfalls, not theory.
- **Portable:** the open [Agent Skills](https://agentskills.io) format, so the same files work everywhere.
- **Safe by default:** security and load skills insist on authorization, staging environments and no real customer data.
- **Verified:** CI validates every skill, link, command and generated file on every push.

## ⚡ Install

### Claude Code (plugin)

```shell
/plugin marketplace add mejbaurbahar/software-tester-skills
/plugin install software-tester-skills@software-tester-skills
```

### Any tool: one command, auto-detects what you have

```bash
curl -fsSL https://mejbaurbahar.github.io/software-tester-skills/install.sh | bash -s -- --auto
```

Or clone and run it locally:

```bash
git clone https://github.com/mejbaurbahar/software-tester-skills.git && cd software-tester-skills
./install.sh --dry-run        # preview
./install.sh --auto           # install
```

### Per tool

| Tool | Command | Skills installed to | Slash commands |
| :--- | :--- | :--- | :--- |
| **Claude Code** | `./install.sh --claude` (or the plugin above) | `~/.claude/skills` | `/test-plan`, or `/software-tester-skills:test-plan` with the plugin |
| **Google Antigravity** | `./install.sh --antigravity` | `~/.gemini/config/skills` | every skill is a command: `/unit-testing`, `/qa-skill-router` |
| **Gemini CLI** | `./install.sh --gemini` | `~/.gemini/skills` | `/qa:test-plan` (then `/commands reload`) |
| **OpenAI Codex** | `./install.sh --codex` | `~/.agents/skills` | `/prompts:qa-test-plan` |
| **Cursor** | `./install.sh --cursor` | `~/.cursor/skills` | `/qa-test-plan` |
| **Others** (OpenCode, Goose, Pi, Hermes…) | `./install.sh --agents` | `~/.agents/skills` | invoke skills by name |
| **This project only** | `./install.sh --project` | `.agents/skills` (+ `.claude`, `.cursor`, `.gemini` if present) | shared with your team via git |

Installer options: `--skill unit-testing,api-testing` (subset), `--no-commands`, `--dry-run`, `--force` (backs up first), `--uninstall`, `--list`.
It **never overwrites** anything it did not create, and `--uninstall` removes only what it installed.

Restart the tool (or reload skills/commands) after installing.

## 🚀 Use it

**Just ask.** The agent matches your request to a skill by its description:

> "Write API tests for the orders endpoint, including auth and pagination."
> "Our checkout test fails 1 in 5 runs. Find out why."
> "Is this release safe to ship?"

**Or name the skill:** *"Use the `flaky-test-management` skill on `checkout.spec.ts`."*

**Or run a slash command** (see below). **Not sure which skill?** Ask for `qa-skill-router`, or run `/qa-help <what you want to test>`.

## 🧭 Slash commands

<!-- commands:start -->
| Command | What it does | Example |
| :--- | :--- | :--- |
| `/a11y-audit` | Audit a page or component for WCAG 2.2 accessibility issues | `/a11y-audit URL or component path` |
| `/api-tests` | Build an API test suite from an endpoint, OpenAPI spec, or running service | `/api-tests spec path, URL, or endpoint` |
| `/bug-report` | Turn observations into a clear, reproducible bug report | `/bug-report what went wrong` |
| `/coverage-gaps` | Find meaningful test coverage gaps and write the missing tests | `/coverage-gaps path or module` |
| `/e2e-tests` | Write resilient end-to-end browser tests for a user journey | `/e2e-tests user journey or URL` |
| `/explore` | Plan and run a time-boxed exploratory testing session | `/explore area, feature, or URL` |
| `/flaky-triage` | Investigate and fix intermittent (flaky) test failures | `/flaky-triage test name or CI run` |
| `/perf-plan` | Create a load/performance test plan and script with SLOs | `/perf-plan service, endpoint, or page` |
| `/qa-audit` | Audit a repository's QA health and recommend which testing skills to apply | `/qa-audit repo path or blank for current` |
| `/qa-help` | Find the right testing skill or command for your task | `/qa-help what you want to test` |
| `/regression-scope` | Pick the regression tests to run for a change, from the git diff | `/regression-scope branch, commit range, or PR` |
| `/release-check` | Go/no-go release readiness assessment with evidence | `/release-check release, tag, or branch` |
| `/review-tests` | Review test code for quality, brittleness, and false confidence | `/review-tests test path or PR` |
| `/security-audit` | Defensive security review of code or configuration (OWASP-focused) | `/security-audit path, feature, or area` |
| `/smoke` | Run a fast smoke check to see whether a build is testable | `/smoke URL or command` |
| `/tdd` | Start a test-driven development session, one small cycle at a time | `/tdd behavior to build` |
| `/test-cases` | Design test cases with formal techniques (EP, BVA, decision tables, state, pairwise) | `/test-cases requirement, user story, or file` |
| `/test-plan` | Create a risk-based test plan for a feature or release | `/test-plan feature, ticket, or release` |
| `/test-strategy` | Design an overall test strategy (levels, tools, automation, gates) | `/test-strategy product or repo` |
| `/threat-model` | Build a STRIDE threat model and derive security test cases | `/threat-model feature or system` |
| `/unit-tests` | Generate high-quality unit tests for a file, function or module | `/unit-tests path or symbol` |
<!-- commands:end -->

Prefix by tool: Claude Code plugin `/software-tester-skills:<name>` (or plain `/<name>`), Gemini CLI `/qa:<name>`, Cursor `/qa-<name>`, Codex `/prompts:qa-<name>`. In Antigravity invoke any skill directly as `/<skill-name>`.
Commands are written once in [`commands/`](commands) and converted for each tool into [`adapters/`](adapters) by `scripts/build_adapters.py`.

## 📚 Skill catalog

<!-- catalog:start -->
### Strategy, Planning & Metrics (14)

_Decide what to test, plan it, report on it._

- **[`autonomous-qa-orchestration`](skills/autonomous-qa-orchestration/SKILL.md)**: Asked to autonomously test an application end-to-end with minimal hand-holding — discover, explore, plan, execute, investigate, report, and verify fixes as one…
- **[`bug-reporting`](skills/bug-reporting/SKILL.md)**: Use whenever filing a defect found during any kind of testing — applies a standard severity scale, report template, and evidence requirements so bug reports are…
- **[`qa-code-intelligence`](skills/qa-code-intelligence/SKILL.md)**: Reading source code to spot testability/risk issues before writing tests, generating test cases automatically from requirements/schemas/code, or doing root-cause/bug…
- **[`qa-engineering`](skills/qa-engineering/SKILL.md)**: Setting up or improving end-to-end QA practice — systematic test design, automation strategy (Playwright/Cypress/Selenium), defect lifecycle, regression and flaky-test…
- **[`qa-fundamentals`](skills/qa-fundamentals/SKILL.md)**: Scoping test strategy, writing a test plan, classifying testing types (QC vs QA, verification vs validation), applying risk-based prioritization, or navigating…
- **[`qa-skill-router`](skills/qa-skill-router/SKILL.md)**: The user asks what to test, which testing approach or skill to use, "where do I start", or describes a QA task without naming a skill — routes the request to the right…
- **[`release-readiness-testing`](skills/release-readiness-testing/SKILL.md)**: Deciding whether to ship — go/no-go criteria, release checklists, canary/blue-green/progressive rollout verification, post-deploy smoke, rollback rehearsal, DORA…
- **[`requirements-testing-review`](skills/requirements-testing-review/SKILL.md)**: Reviewing requirements, user stories, designs or specs before coding (shift-left static testing) — finding ambiguity, missing acceptance criteria, testability gaps…
- **[`test-architect`](skills/test-architect/SKILL.md)**: Designing a test suite's architecture — test pyramid/trophy, test isolation, property-based testing, quality gates, and profiling slow or flaky suites.
- **[`test-design-techniques`](skills/test-design-techniques/SKILL.md)**: Deriving test cases systematically — equivalence partitioning, boundary value analysis, decision tables, state transition testing, pairwise/combinatorial testing…
- **[`test-metrics-reporting`](skills/test-metrics-reporting/SKILL.md)**: Measuring and communicating quality — test metrics and KPIs (defect escape rate, DDP, MTTR, flake rate, coverage, automation ROI), dashboards, Allure/ReportPortal…
- **[`test-planning-documentation`](skills/test-planning-documentation/SKILL.md)**: Producing test plans, test strategies, traceability matrices (RTM), entry/exit criteria, test summary reports, or IEEE 829/ISO 29119-style QA documentation — lightweight…
- **[`test-strategist`](skills/test-strategist/SKILL.md)**: Deciding what to test and how — risk-based test planning, TDD vs test-after, the right level (unit/integration/E2E) for each behavior, and recognising when a test is not…
- **[`testing-strategies`](skills/testing-strategies/SKILL.md)**: Optimising a test suite for confidence and speed — the testing pyramid, mocking strategies, testing behavior instead of implementation, maintainable tests that survive…

### Functional & Acceptance (9)

_Black-box, exploratory, regression and release-gate testing._

- **[`acceptance-testing`](skills/acceptance-testing/SKILL.md)**: Validating a feature against business needs before release — user acceptance testing (UAT), alpha/beta programs, acceptance criteria, sign-off, contract/operational…
- **[`bdd-gherkin-testing`](skills/bdd-gherkin-testing/SKILL.md)**: Writing or automating behavior-driven development (BDD) specs — Gherkin Given/When/Then, Cucumber, SpecFlow, Behave, pytest-bdd, Playwright-BDD, example mapping, living…
- **[`email-notification-testing`](skills/email-notification-testing/SKILL.md)**: Testing transactional/marketing email, SMS, push and in-app notifications — capture inboxes (Mailpit, MailHog, Mailosaur), rendering across clients, links/tokens…
- **[`exploratory-testing`](skills/exploratory-testing/SKILL.md)**: Conducting exploratory testing, unscripted bug hunting, and session-based test management — test charters, heuristics (SFDIPOT, Tours), timeboxed sessions, and…
- **[`functional-testing`](skills/functional-testing/SKILL.md)**: Verifying that a feature or user flow behaves according to requirements/specs — functional correctness testing of forms, workflows, business logic, and CRUD operations…
- **[`manual-testing`](skills/manual-testing/SKILL.md)**: Designing test cases, doing exploratory testing, writing test plans/checklists, or manually verifying a feature before or instead of automating it. Covers test case…
- **[`regression-testing`](skills/regression-testing/SKILL.md)**: Validating that recent changes haven't broken existing functionality — building/running regression suites, deciding regression scope for a release, and impact analysis…
- **[`smoke-sanity-testing`](skills/smoke-sanity-testing/SKILL.md)**: Designing or executing smoke tests and sanity suites — Build Verification Testing (BVT), pre-flight deployment verification, critical-path health checks, and fast-fail…
- **[`system-testing`](skills/system-testing/SKILL.md)**: Verifying a fully integrated system against its specification — end-to-end functional and non-functional behavior in a production-like environment, system test planning…

### Code-Level & White-Box (10)

_Unit, integration, property, fuzz, mutation and TDD._

- **[`concurrency-race-condition-testing`](skills/concurrency-race-condition-testing/SKILL.md)**: Testing thread-safety, race conditions, deadlocks, double-submit, idempotency, optimistic/pessimistic locking, async ordering bugs, and flaky concurrency failures — with…
- **[`date-time-timezone-testing`](skills/date-time-timezone-testing/SKILL.md)**: Testing anything involving dates, times, time zones, DST, leap years/seconds, scheduling, expiry, recurring events, cron jobs, or locale calendars — with frozen clocks…
- **[`fuzz-testing`](skills/fuzz-testing/SKILL.md)**: Hunting crashes, hangs, memory bugs and parser/protocol vulnerabilities with random or coverage-guided inputs — fuzzing with AFL++, libFuzzer, Jazzer, Atheris, go-fuzz…
- **[`integration-testing`](skills/integration-testing/SKILL.md)**: Verifying interactions between multiple components, modules, or services — API-to-database persistence, message queues, external service adapters, and Testcontainers.
- **[`mutation-testing`](skills/mutation-testing/SKILL.md)**: Measuring test suite quality, finding false positives, and eliminating blind spots — injecting code mutations (mutants), mutation score, Mutmut, Stryker, and kill rate…
- **[`property-based-testing`](skills/property-based-testing/SKILL.md)**: Example-based tests miss edge cases — property-based testing with Hypothesis, fast-check, jqwik, QuickCheck, or proptest; invariants, round-trip, oracle and metamorphic…
- **[`snapshot-golden-testing`](skills/snapshot-golden-testing/SKILL.md)**: Adding or reviewing snapshot, golden-file, approval, or characterization tests — Jest/Vitest snapshots, syrupy, ApprovalTests, insta, golden files for…
- **[`static-analysis-testing`](skills/static-analysis-testing/SKILL.md)**: Setting up or triaging static analysis as a quality gate — linters, type checkers, SAST (Semgrep, CodeQL, SonarQube, Bandit), complexity and duplication limits…
- **[`tdd-workflow`](skills/tdd-workflow/SKILL.md)**: Practicing or coaching test-driven development — red-green-refactor, outside-in vs inside-out (London vs Chicago), test lists, baby steps, TDD with AI coding agents, and…
- **[`unit-testing`](skills/unit-testing/SKILL.md)**: Writing, refactoring, or auditing unit and component tests — isolated test doubles (mocks, stubs, spies), Arrange-Act-Assert (AAA) pattern, boundary value analysis…

### Automation & CI (7)

_Frameworks, environments, flaky tests, coverage and pipelines._

- **[`cicd-testing`](skills/cicd-testing/SKILL.md)**: Designing or debugging test execution in CI/CD pipelines — PR gates, test tiering (smoke/regression/nightly), parallelization/sharding, quality gates, flaky-test…
- **[`code-coverage-analysis`](skills/code-coverage-analysis/SKILL.md)**: Measuring or improving test coverage — line, branch, function, condition/MC-DC and diff/patch coverage; coverage tools (coverage.py, Istanbul/c8, JaCoCo, gcov, go…
- **[`flaky-test-management`](skills/flaky-test-management/SKILL.md)**: Tests pass and fail intermittently — detecting, quarantining, root-causing and eliminating flaky tests (async waits, shared state, order dependence, time, network…
- **[`qa-test-harness`](skills/qa-test-harness/SKILL.md)**: The user asks to test software end to end with a live browser — inspect web apps via Chrome DevTools MCP, automate browser actions, verify APIs, run test suites, capture…
- **[`test-automation`](skills/test-automation/SKILL.md)**: Writing, structuring, or debugging automated tests — Playwright/Selenium E2E suites, pytest test design, page object models, CI test integration, and deciding what's…
- **[`test-environment-management`](skills/test-environment-management/SKILL.md)**: Designing, stabilizing or scaling test environments — ephemeral preview environments, Docker Compose/Kubernetes/Testcontainers, environment parity, data seeding and…
- **[`webapp-testing`](skills/webapp-testing/SKILL.md)**: Testing local web applications with Python Playwright — verify frontend behavior, debug UI issues, capture screenshots and browser logs, and manage the app's server…

### Web, UI & UX (8)

_Browsers, E2E, visual, accessibility, i18n, SEO and PWAs._

- **[`accessibility-testing`](skills/accessibility-testing/SKILL.md)**: Auditing a web app for accessibility (a11y) — WCAG compliance, screen reader compatibility, keyboard navigation, color contrast, and semantic HTML/ARIA correctness.
- **[`cross-browser-testing`](skills/cross-browser-testing/SKILL.md)**: Testing across multiple browser engines, operating systems, and viewport dimensions — Chromium, Gecko (Firefox), WebKit (Safari), responsive breakpoints, and…
- **[`e2e-testing`](skills/e2e-testing/SKILL.md)**: Automating end-to-end user journeys through the browser or UI — Playwright, Cypress, user critical paths, resilient locators, session storage, network stubbing, and…
- **[`localization-testing`](skills/localization-testing/SKILL.md)**: Verifying internationalization (i18n) and localization (l10n) — string truncation, pseudo-localization, Right-to-Left (RTL) layout rendering, date/time/currency…
- **[`pwa-offline-testing`](skills/pwa-offline-testing/SKILL.md)**: Testing Progressive Web Apps and offline-first apps — service workers, caching strategies, manifest/installability, background sync, push notifications, storage quotas…
- **[`seo-testing`](skills/seo-testing/SKILL.md)**: Auditing technical SEO and search visibility — crawlability, indexation, robots.txt, sitemaps, canonical/hreflang, meta and Open Graph tags, structured data (JSON-LD)…
- **[`usability-testing`](skills/usability-testing/SKILL.md)**: Evaluating usability, user friction, UI clarity, and workflow ergonomics — Nielsen Norman heuristics, form validation feedback, error recovery paths, cognitive load, and…
- **[`visual-testing`](skills/visual-testing/SKILL.md)**: Checking visual/layout correctness — screenshot/visual regression testing, design-system and Figma-to-production validation, responsive layout, dark mode/theming…

### API, Backend & Messaging (6)

_REST, GraphQL, real-time, contracts, events and microservices._

- **[`api-testing`](skills/api-testing/SKILL.md)**: Testing REST/GraphQL APIs directly — status codes, schema/contract validation, auth, pagination, rate limits, idempotency, and error responses. Use instead of driving…
- **[`contract-testing`](skills/contract-testing/SKILL.md)**: Testing integrations between services — consumer-driven contracts, microservice boundaries, event/message-queue testing (Kafka, webhooks), schema evolution, and backward…
- **[`event-driven-messaging-testing`](skills/event-driven-messaging-testing/SKILL.md)**: Testing message queues and event streams — Kafka, RabbitMQ, SQS/SNS, Pub/Sub, NATS, webhooks — covering schema evolution, ordering, at-least-once delivery, idempotent…
- **[`graphql-testing`](skills/graphql-testing/SKILL.md)**: Testing GraphQL APIs — queries, mutations, subscriptions, schema validation and breaking-change detection, N+1 queries, depth/complexity limits, introspection exposure…
- **[`microservices-testing`](skills/microservices-testing/SKILL.md)**: Designing a test strategy for microservices or distributed systems — service/component tests, consumer-driven contracts, service virtualization, testing in production…
- **[`websocket-realtime-testing`](skills/websocket-realtime-testing/SKILL.md)**: Testing WebSockets, Server-Sent Events, Socket.IO, WebRTC signaling, push/live-update features, chat, presence, and collaborative editing — connection lifecycle…

### Data & Databases (4)

_Databases, ETL, migrations and test data._

- **[`data-migration-testing`](skills/data-migration-testing/SKILL.md)**: Testing database schema migrations, system replatforming, or data migrations between systems — pre/post reconciliation, zero-downtime expand/contract, rollback…
- **[`data-pipeline-etl-testing`](skills/data-pipeline-etl-testing/SKILL.md)**: Testing ETL/ELT pipelines, data warehouses, dbt models, Spark/Airflow jobs, and analytics data quality — schema, row-count and checksum reconciliation…
- **[`database-testing`](skills/database-testing/SKILL.md)**: Verifying data integrity, CRUD correctness at the persistence layer, migrations, transactions/concurrency, or query correctness/performance — SQL and NoSQL. Use whenever…
- **[`test-data-engineering`](skills/test-data-engineering/SKILL.md)**: Generating synthetic/realistic test data, seeding fixtures, masking PII for a test environment, or designing deterministic/reusable test datasets. Underpins reliable…

### Performance & Reliability (9)

_Load, scalability, chaos, recovery and compatibility._

- **[`chaos-resilience-testing`](skills/chaos-resilience-testing/SKILL.md)**: Deliberately injecting failure (network latency/loss, service/dependency crash, resource exhaustion) to verify a system degrades gracefully instead of cascading…
- **[`compatibility-testing`](skills/compatibility-testing/SKILL.md)**: Verifying software compatibility across environments, operating systems, database versions, backward/forward API compatibility, and migration rollback safety.
- **[`configuration-feature-flag-testing`](skills/configuration-feature-flag-testing/SKILL.md)**: Testing configuration, environment variables, secrets handling and feature flags — flag matrices, progressive rollouts, kill switches, targeting rules, stale flag…
- **[`disaster-recovery-backup-testing`](skills/disaster-recovery-backup-testing/SKILL.md)**: Validating backup, restore, high availability and disaster recovery — RTO/RPO verification, restore drills, region failover, data corruption and ransomware recovery…
- **[`installation-upgrade-testing`](skills/installation-upgrade-testing/SKILL.md)**: Testing software installation, upgrade, downgrade, uninstall and packaging — installers (MSI/DMG/DEB/RPM/Docker/Helm/npm/pip), silent installs, permission and disk edge…
- **[`memory-leak-resource-testing`](skills/memory-leak-resource-testing/SKILL.md)**: Diagnosing or preventing memory leaks, unbounded growth, file-descriptor/connection/thread leaks, GC pressure, OOM kills, and slow degradation in long-running services…
- **[`performance-testing`](skills/performance-testing/SKILL.md)**: Use for load/stress/soak/spike testing, Core Web Vitals audits, Lighthouse checks, API latency benchmarking, and diagnosing slow pages or endpoints. Covers both frontend…
- **[`scalability-capacity-testing`](skills/scalability-capacity-testing/SKILL.md)**: Determining how a system scales and how much capacity it needs — load models, capacity planning, autoscaling validation, bottleneck identification (USE/RED)…
- **[`web-performance-testing`](skills/web-performance-testing/SKILL.md)**: Measuring or improving front-end and page-load performance — Core Web Vitals (LCP, INP, CLS), Lighthouse CI, WebPageTest, RUM vs lab data, performance budgets, bundle…

### Operations & Production (3)

_Observability, infrastructure and shift-right monitoring._

- **[`cloud-infrastructure-testing`](skills/cloud-infrastructure-testing/SKILL.md)**: Testing cloud/infrastructure concerns — Docker/Kubernetes deployments, serverless functions, managed-service integration (S3, queues, API Gateway), disaster…
- **[`observability-testing`](skills/observability-testing/SKILL.md)**: Correlating a test failure or production issue across logs, metrics, and traces to find root cause; when verifying that a feature emits the logging/metrics/alerting it…
- **[`production-monitoring-synthetic-testing`](skills/production-monitoring-synthetic-testing/SKILL.md)**: Testing in production safely (shift-right) — synthetic monitoring, canary checks, uptime probes, Playwright/Checkly/Datadog synthetics, real-user monitoring, SLO/SLI…

### Security & Privacy (9)

_Defensive security testing, auth, supply chain and IaC._

- **[`42crunch-api-security-testing`](skills/42crunch-api-security-testing/SKILL.md)**: Auditing, scanning, or remediating OpenAPI/Swagger API definitions for security vulnerabilities — 42Crunch audit scoring, OWASP API Security Top 10 compliance, BOLA/BFLA…
- **[`ai-code-security`](skills/ai-code-security/SKILL.md)**: Reviewing AI-generated code or LLM-integrated applications for security flaws — OWASP Top 10 for LLMs, insecure generated patterns, secret and dependency hygiene, and…
- **[`authn-authz-testing`](skills/authn-authz-testing/SKILL.md)**: Testing authentication and authorization — login, MFA, OAuth2/OIDC, SAML, JWT, sessions/cookies, password reset, RBAC/ABAC, IDOR/BOLA, privilege escalation, multi-tenant…
- **[`iac-container-security-testing`](skills/iac-container-security-testing/SKILL.md)**: Testing Infrastructure-as-Code and container configuration — Terraform/CloudFormation/Helm/Kubernetes scanning (Checkov, tfsec, KICS, kube-linter), policy-as-code…
- **[`security-hardening`](skills/security-hardening/SKILL.md)**: Hardening an application's security — OWASP Top 10 mitigations, secure coding patterns, authentication and authorization, secret handling, input validation/output…
- **[`security-owasp`](skills/security-owasp/SKILL.md)**: Securing a web application against OWASP Top 10 risks — authentication, authorization, input validation, XSS and CSRF prevention, secure headers, and security test cases.
- **[`security-testing`](skills/security-testing/SKILL.md)**: Use for authorized security/penetration testing of web apps and APIs — OWASP Top 10 checks, auth/session testing, header/config audits, and vulnerability triage. Only…
- **[`supply-chain-dependency-testing`](skills/supply-chain-dependency-testing/SKILL.md)**: Testing software supply-chain and dependency risk — SCA/vulnerability scanning (Trivy, Grype, OSV, Dependabot, npm audit), SBOM (CycloneDX/SPDX), license compliance…
- **[`threat-modeling`](skills/threat-modeling/SKILL.md)**: Analyzing a design for security risks before or during build — STRIDE, data-flow diagrams, trust boundaries, LINDDUN privacy, abuse cases, risk ranking, mitigation…

### Compliance (1)

_GDPR, HIPAA, PCI, SOC 2, audit evidence._

- **[`compliance-testing`](skills/compliance-testing/SKILL.md)**: Testing for regulatory and standards compliance — GDPR/CCPA privacy rights, HIPAA, PCI-DSS, SOC 2, ISO 27001, WCAG/ADA/EAA, audit logging, data retention/deletion…

### AI, ML & LLM (7)

_Models, LLM apps, RAG, agents, chatbots and MCP._

- **[`ai-agent-evaluation`](skills/ai-agent-evaluation/SKILL.md)**: Testing and evaluating AI agents and tool-using LLM systems — task-success and trajectory evaluation, tool-call correctness, LLM-as-judge calibration, regression…
- **[`ai-ml-testing`](skills/ai-ml-testing/SKILL.md)**: Testing a classical ML model or ML-powered feature — accuracy/precision/recall/F1 evaluation, model regression testing, bias/fairness testing, and ML pipeline…
- **[`chatbot-voice-agent-testing`](skills/chatbot-voice-agent-testing/SKILL.md)**: Testing chatbots, voice assistants, or conversational AI agents specifically — multi-turn conversation flow, context/memory retention, intent recognition, STT/TTS…
- **[`llm-security-audit`](skills/llm-security-audit/SKILL.md)**: Auditing an LLM application's security posture — OWASP Top 10 for LLMs, threat modelling, data-leakage and prompt-handling review, and compliance mapping to NIST AI RMF…
- **[`llm-testing`](skills/llm-testing/SKILL.md)**: Testing LLM-powered features — prompt testing, hallucination/faithfulness checks, RAG evaluation, agent/tool-use testing, prompt injection and LLM security, regression…
- **[`mcp-testing`](skills/mcp-testing/SKILL.md)**: Testing Model Context Protocol (MCP) servers — unit and integration tests, tool/resource schema validation, JSON-RPC contract checks, MCP Inspector workflows, and…
- **[`rag-evaluation-testing`](skills/rag-evaluation-testing/SKILL.md)**: Testing retrieval-augmented generation (RAG) — retrieval metrics (recall@k, MRR, nDCG), chunking and embedding evaluation, faithfulness/groundedness, answer relevancy…

### Platforms (7)

_Mobile, desktop, CLI, IoT, games, blockchain and serverless._

- **[`blockchain-smart-contract-testing`](skills/blockchain-smart-contract-testing/SKILL.md)**: Testing smart contracts and dApps — Solidity/Foundry/Hardhat tests, fuzz and invariant testing, fork tests, gas profiling, reentrancy/overflow/access-control…
- **[`cli-testing`](skills/cli-testing/SKILL.md)**: Testing command-line tools and scripts — exit codes, stdout/stderr contracts, flags and argument parsing, help/version output, stdin/pipes, env/config precedence…
- **[`desktop-app-testing`](skills/desktop-app-testing/SKILL.md)**: Testing desktop applications — Electron, Tauri, WPF/WinForms, Qt, macOS/Cocoa, GTK — covering UI automation (Playwright for Electron, WinAppDriver, pywinauto, Appium…
- **[`game-testing`](skills/game-testing/SKILL.md)**: Testing video games — gameplay/balance, playtesting, performance (FPS, frame pacing, memory), input devices, save/load integrity, multiplayer/netcode, platform…
- **[`iot-embedded-testing`](skills/iot-embedded-testing/SKILL.md)**: Testing IoT devices, firmware and embedded systems — hardware-in-the-loop, simulators/emulators, MQTT/BLE/Zigbee/LoRa protocols, OTA updates, power/battery, sensor edge…
- **[`mobile-testing`](skills/mobile-testing/SKILL.md)**: Testing mobile apps (iOS/Android native, or responsive/mobile-web) — device/viewport matrices, touch gesture testing, mobile-specific network and lifecycle conditions…
- **[`serverless-testing`](skills/serverless-testing/SKILL.md)**: Testing serverless and cloud-function architectures — AWS Lambda, Azure Functions, Cloud Functions/Run, event sources, cold starts, timeouts and retries, IAM least…

### Domain-Specific (3)

_Payments, email, analytics and experimentation._

- **[`a-b-testing`](skills/a-b-testing/SKILL.md)**: Designing or analysing controlled experiments — A/B and multivariate tests, hypotheses, sample size and power, statistical significance, SRM checks, feature-flag…
- **[`analytics-tracking-testing`](skills/analytics-tracking-testing/SKILL.md)**: Validating analytics and tracking — GA4/GTM dataLayer, Segment/Amplitude/Mixpanel events, pixels (Meta, TikTok), server-side tagging, consent mode, UTM/attribution…
- **[`payment-ecommerce-testing`](skills/payment-ecommerce-testing/SKILL.md)**: Testing checkout, payments, carts, coupons, taxes, inventory, orders, refunds, and subscriptions — Stripe/PayPal/Adyen sandboxes, test cards, 3-D Secure, webhooks…
<!-- catalog:end -->

## 🔧 How it works

```
skills/<name>/
├── SKILL.md            # frontmatter (name, description, metadata) + the playbook
└── references/         # optional deeper material, loaded only when needed
```

1. At startup the agent reads only each skill's `name` and `description` (a few dozen tokens).
2. When your task matches, it loads that skill's `SKILL.md`, and follows it.
3. Deeper `references/` files load only if the skill points to them (progressive disclosure keeps context small).

Every `description` starts with **"Use when …"** and lists concrete triggers, because that one line is how agents decide to load a skill.

## 🛡️ Responsible use

Security, fuzzing and load-testing skills are for **defensive, authorized testing** of systems you own or have written permission to test. They tell agents to prefer staging, throttle traffic, avoid real customer data and never use live payment credentials.

## 🤝 Contributing

New skills, fixes and translations are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md), then:

```bash
python3 tests/validate_skills.py      # format, links, commands, router, manifests
python3 scripts/build_readme.py       # refresh README catalog + manifests
python3 scripts/build_adapters.py     # refresh per-tool commands
python3 scripts/build_site.py --serve # preview the website on :8000
```

If this helps you, **star the repo** ⭐. It is the best way to help other testers find it.

[![Star History Chart](https://api.star-history.com/svg?repos=mejbaurbahar/software-tester-skills&type=Date)](https://star-history.com/#mejbaurbahar/software-tester-skills&Date)

## 📄 License

[MIT](LICENSE). Use it, adapt it, ship it. (`skills/webapp-testing` keeps its own license file.)

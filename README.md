# Software Tester Skills 🧪

[![Agent Skills Standard](https://img.shields.io/badge/standard-agentskills.io-blue.svg)](https://agentskills.io)
[![Skills Count](https://img.shields.io/badge/skills-46%20testing%20skills-green.svg)](#-skill-catalog)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

The definitive open-standard **Agent Skills library for Software Testing, SDET, and Quality Assurance**.

Equip any AI coding assistant or autonomous testing agent with senior-level testing methodologies, verification protocols, test design heuristics, and automation runbooks.

---

## 🌐 Universal AI Assistant Compatibility

Built strictly according to the **[Agent Skills open specification](https://agentskills.io)** using progressive disclosure. Fully compatible with:

* **Google Antigravity & Gemini CLI** (`~/.gemini/config/skills/` or `.agents/skills/`)
* **Claude Code** (`~/.claude/skills/`)
* **OpenAI Codex** (`~/.agents/skills/` or `.agents/skills/`)
* **Cursor** (`.agents/skills/` or `.cursor/skills/`)
* **OpenCode / Pi / Hermes**
* **Goose & DevHub**

---

## ⚡ Quick Install

### One-Line Install (All Harnesses)

```bash
git clone https://github.com/mejbaurbahar/software-tester-skills.git
cd software-tester-skills
./install.sh --all
```

### Install by Platform

```bash
# For Google Antigravity & Gemini CLI
./install.sh --antigravity

# For Claude Code
./install.sh --claude

# For project-level workspace (.agents/skills)
./install.sh --project
```

---

## 📚 Complete Skill Catalog (46 Skills)

### 1. Test Strategy, Architecture & Quality Gates (8)
* **[`test-architect`](skills/test-architect/SKILL.md)**: Test pyramid and trophy design, test isolation, quality gates, and test suite profiling.
* **[`test-strategist`](skills/test-strategist/SKILL.md)**: Risk-based test planning, test trade-offs, and deciding what to automate vs test manually.
* **[`testing-strategies`](skills/testing-strategies/SKILL.md)**: Optimizing test suites for maximum confidence and velocity without bloat.
* **[`qa-fundamentals`](skills/qa-fundamentals/SKILL.md)**: Core STLC lifecycle, test classification, verification vs validation, and quality metrics.
* **[`qa-engineering`](skills/qa-engineering/SKILL.md)**: World-class systematic testing, automation strategy, and defect lifecycle management.
* **[`autonomous-qa-orchestration`](skills/autonomous-qa-orchestration/SKILL.md)**: Continuous end-to-end autonomous QA agent exploration, planning, execution, and triage.
* **[`qa-code-intelligence`](skills/qa-code-intelligence/SKILL.md)**: Source code static analysis for testability, automatic test generation, and bug root-cause analysis.
* **[`bug-reporting`](skills/bug-reporting/SKILL.md)**: Standardized, actionable bug reporting with deterministic reproduction steps, console/network diagnostics, and evidence capture.

### 2. Code-Level & White-Box Testing (3)
* **[`unit-testing`](skills/unit-testing/SKILL.md)**: AAA pattern, test doubles (mocks, stubs, spies, fakes), boundary value analysis, and property-based testing.
* **[`integration-testing`](skills/integration-testing/SKILL.md)**: Multi-component interactions, persistence layers, Testcontainers, message queues, and service adapters.
* **[`mutation-testing`](skills/mutation-testing/SKILL.md)**: Measuring test suite effectiveness by injecting faults (mutants, Mutmut, Stryker) and evaluating kill rate.

### 3. Functional & Black-Box Testing (5)
* **[`functional-testing`](skills/functional-testing/SKILL.md)**: Functional correctness of forms, workflows, business logic, calculations, and CRUD operations.
* **[`manual-testing`](skills/manual-testing/SKILL.md)**: Test case design techniques (Equivalence Partitioning, Boundary Value Analysis, Decision Tables), charters, and checklists.
* **[`exploratory-testing`](skills/exploratory-testing/SKILL.md)**: Session-Based Test Management (SBTM), SFDIPOT heuristics, testing tours, and unscripted bug hunting.
* **[`smoke-sanity-testing`](skills/smoke-sanity-testing/SKILL.md)**: Build Verification Testing (BVT), pre-flight health checks, fast-fail CI gates (<3 min).
* **[`regression-testing`](skills/regression-testing/SKILL.md)**: Git diff impact analysis, regression scope selection, and backward functionality preservation.

### 4. Browser, UI, UX & Accessibility (9)
* **[`qa-test-harness`](skills/qa-test-harness/SKILL.md)**: Live Chrome DevTools MCP browser automation, real DOM inspection, network captures, and console errors.
* **[`test-automation`](skills/test-automation/SKILL.md)**: Automated browser testing with Playwright, Selenium, pytest, and Page Object Models.
* **[`webapp-testing`](skills/webapp-testing/SKILL.md)**: Python Playwright runner with automated background server lifecycle management (`with_server.py`).
* **[`e2e-testing`](skills/e2e-testing/SKILL.md)**: End-to-end user journeys, resilient role-based locators, session storage, and failure artifacts.
* **[`cross-browser-testing`](skills/cross-browser-testing/SKILL.md)**: Chromium, Gecko (Firefox), WebKit (Safari), rendering engine quirks, and responsive breakpoints.
* **[`visual-testing`](skills/visual-testing/SKILL.md)**: Screenshot visual regression testing, responsive breakpoint layouts, and styling consistency.
* **[`usability-testing`](skills/usability-testing/SKILL.md)**: Nielsen Norman 10 usability heuristics, user friction points, form clarity, and error recovery paths.
* **[`accessibility-testing`](skills/accessibility-testing/SKILL.md)**: WCAG 2.1/2.2 AA/AAA compliance, axe-core audits, screen reader accessibility, and keyboard navigation.
* **[`localization-testing`](skills/localization-testing/SKILL.md)**: Internationalization (i18n) & localization (l10n), text expansion, RTL layouts (Arabic/Hebrew), Unicode/UTF-8, and pseudo-localization.
* **[`mobile-testing`](skills/mobile-testing/SKILL.md)**: Touch gestures, mobile viewport matrices, dynamic address bar shifts, and mobile-web responsiveness.

### 5. Backend, API, Database & Contracts (5)
* **[`api-testing`](skills/api-testing/SKILL.md)**: REST, GraphQL, gRPC status codes, contract validation, auth tokens, pagination, rate limits, and idempotency.
* **[`contract-testing`](skills/contract-testing/SKILL.md)**: Consumer-driven contracts (Pact), microservice boundaries, event schemas, and backward compatibility.
* **[`database-testing`](skills/database-testing/SKILL.md)**: ACID verification, CRUD correctness, transaction rollbacks, migration integrity, and slow query profiling.
* **[`test-data-engineering`](skills/test-data-engineering/SKILL.md)**: Synthetic test data generation, realistic fixtures, PII data masking, and deterministic state seeding.
* **[`compatibility-testing`](skills/compatibility-testing/SKILL.md)**: Cross-environment compatibility, DB schema rollback safety, and runtime/dependency upgrades.

### 6. Performance, Operations, Cloud & Chaos (5)
* **[`performance-testing`](skills/performance-testing/SKILL.md)**: Load, stress, spike, and soak testing with k6/Locust, Core Web Vitals, and Lighthouse audits.
* **[`chaos-resilience-testing`](skills/chaos-resilience-testing/SKILL.md)**: Fault injection (network latency, service crashes, resource exhaustion), retries, and circuit breakers.
* **[`cloud-infrastructure-testing`](skills/cloud-infrastructure-testing/SKILL.md)**: Docker, Kubernetes deployments, managed cloud services, failover, and infra-as-code verification.
* **[`observability-testing`](skills/observability-testing/SKILL.md)**: Correlating logs, metrics, and traces for root cause analysis and shift-right production monitoring.
* **[`cicd-testing`](skills/cicd-testing/SKILL.md)**: CI/CD test execution, PR gates, test sharding, quality gates, and flaky test tracking.

### 7. Security, Hardening & Compliance (4)
* **[`security-testing`](skills/security-testing/SKILL.md)**: Authorized penetration testing, OWASP Top 10 vulnerabilities, session testing, and auth bypass.
* **[`security-owasp`](skills/security-owasp/SKILL.md)**: Web application security, defense-in-depth, input sanitization, CSRF, and XSS prevention.
* **[`security-hardening`](skills/security-hardening/SKILL.md)**: Deep system and application security hardening standards.
* **[`ai-code-security`](skills/ai-code-security/SKILL.md)**: Detecting and preventing vulnerabilities in AI-generated code and LLM integrations.

### 8. AI, ML, LLM & Emerging Paradigms (7)
* **[`ai-ml-testing`](skills/ai-ml-testing/SKILL.md)**: Classical ML model evaluation, precision/recall/F1, data drift, bias/fairness, and pipeline robustness.
* **[`llm-testing`](skills/llm-testing/SKILL.md)**: Prompt testing, hallucination/faithfulness evaluation, RAG retrieval verification, and token budgets.
* **[`llm-security-audit`](skills/llm-security-audit/SKILL.md)**: OWASP Top 10 for LLMs, prompt injection, jailbreak defense, and sensitive data leakage.
* **[`chatbot-voice-agent-testing`](skills/chatbot-voice-agent-testing/SKILL.md)**: Multi-turn conversation flows, intent recognition, context memory, and STT/TTS accuracy.
* **[`mcp-testing`](skills/mcp-testing/SKILL.md)**: Testing Model Context Protocol (MCP) servers, tool schemas, and JSON-RPC contracts.
* **[`a-b-testing`](skills/a-b-testing/SKILL.md)**: Controlled experimentation, statistical significance, feature flags, and conversion optimization.

---

## 💡 How Agent Skills Work

Agent Skills leverage **Progressive Disclosure**:
1. **Zero Context Bloat**: Only the skill names and trigger descriptions are loaded into the agent's initial prompt (~200 tokens).
2. **On-Demand Activation**: When you ask your agent to *"run an exploratory test on the checkout page"* or *"audit the API endpoints for security"*, the agent identifies the relevant skill and reads the full `SKILL.md` runbook just-in-time.
3. **Rigorous Compliance**: Each skill provides checklists, heuristics, and anti-patterns that keep the agent disciplined, objective, and thorough.

---

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on authoring new skills and running the validation suite.

```bash
# Validate all skills
python3 tests/validate_skills.py
```

---

## 📄 License

This repository is licensed under the [MIT License](LICENSE).

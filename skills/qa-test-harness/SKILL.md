---
name: qa-test-harness
description: Use when the user asks to test software end to end with a live browser — inspect web apps via Chrome DevTools MCP, automate browser actions, verify APIs, run test suites, capture console/network evidence, and file structured bug reports.
license: MIT
metadata:
  category: automation
  version: "2.0"
  tags: chrome-devtools, browser-automation, dom, network, console
---

# Software Testing & QA Agent Harness

This skill defines the operational runbook and protocols for acting as the primary Software Testing Harness on macOS, interfacing with the user's default Google Chrome browser via Chrome DevTools MCP, local CLI tools, test runners, and filesystem assets.

## Core Capabilities & Protocols

### 1. Live Chrome Browser Testing (Chrome DevTools MCP)
Always interact with the user's active Chrome browser session using the `chrome-devtools` MCP tools:
- **Session & Tab Discovery**:
  - Call `list_pages` to find active tabs.
  - Call `select_page` with the appropriate `pageId` or target URL.
  - Use `new_page` if an isolated test tab is preferred.
- **UI Interaction & Verification**:
  - Call `click`, `hover`, `fill`, `type_text`, `press_key` to simulate user actions.
  - Call `evaluate_script` to run JavaScript assertions directly inside the page context (e.g. check element properties, DOM nodes, local storage, session state).
  - Call `take_snapshot` to inspect the full accessibility tree and structure.
- **Console & Network Diagnostics**:
  - Call `list_console_messages` and `get_console_message` to capture JavaScript runtime errors, unhandled rejections, and warnings.
  - Call `list_network_requests` and `get_network_request` to verify API endpoint calls, status codes (4xx/5xx), headers, and payloads.
- **Visual Evidence**:
  - Call `take_screenshot` to capture visual evidence of test passes or UI bugs.
- **Performance & Audits**:
  - Call `lighthouse_audit` or `performance_start_trace` / `performance_stop_trace` to diagnose performance bottlenecks and core web vitals.

### 2. Full System & Multi-Environment Testing
- **Local Repositories & Test Runners**:
  - Locate test suites in the repositories or folders the user points you at.
  - Execute test runners (Pytest, Playwright, Jest, Vitest, Cypress, Mocha, k6).
  - Parse test reports (HTML, JUnit XML, JSON) and highlight failures.
- **API & Backend Verification**:
  - Test REST / GraphQL / gRPC endpoints using `curl`, Python `requests`, or Node `fetch`.
  - Validate response schemas, headers, status codes, and latency.
- **Service & Server Lifecycle**:
  - Launch local staging or dev servers as background tasks when needed.
  - Check health endpoints before executing integration tests.

### 3. Structured Bug Reporting Standard
When identifying an issue or test failure, format the finding as a structured bug report:
- **Title / Summary**: Clear summary of the defect.
- **Severity & Impact**: Blocker / Critical / Major / Minor.
- **Environment**: URL, Chrome Version, OS, Screen resolution.
- **Steps to Reproduce**: Numbered, deterministic steps.
- **Expected Behavior**: What should have happened according to specs.
- **Actual Behavior**: What actually happened.
- **Evidence**:
  - Console errors & stack traces
  - Failed network requests (URL, method, status code, response body)
  - Screenshots / Snapshots

### 4. Readiness & Autonomous Action
- Proactively investigate root causes when a test fails.
- Cross-reference frontend UI issues with backend responses and console logs.
- Provide fixes or test automation scripts to prevent regressions.

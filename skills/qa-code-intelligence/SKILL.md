---
name: qa-code-intelligence
description: Use when reading source code to spot testability/risk issues before writing tests, generating test cases automatically from requirements/schemas/code, or doing root-cause/bug intelligence work — clustering failures, deduping reports, and reasoning from stack traces/logs to a likely cause.
license: MIT
metadata:
  category: strategy
  version: "2.0"
  tags: static-analysis, testability, test-generation, root-cause-analysis
---

# QA Code Intelligence

Three related capabilities: reading code for risk, generating tests from artifacts, and reasoning about failures. Each feeds the others.

## Code review for testability & risk (read before testing, not just after a bug)
When reviewing a diff or unfamiliar module, actively look for:
- **Missing validation** — inputs trusted without checking type/range/presence, especially at system boundaries (API handlers, form submission).
- **Missing/swallowed error handling** — empty catch blocks, errors logged but not surfaced, promises without rejection handling. A silent failure is worse than a loud one because nobody investigates it.
- **Race conditions** — shared mutable state accessed without synchronization, async operations assumed to complete in order without awaiting.
- **Null/undefined handling gaps** — a function that dereferences a value without checking it can be absent, especially on optional API fields.
- **Boundary issues in the code itself** — off-by-one in loops/pagination, inclusive/exclusive range confusion.
- **Security risk patterns** — string-concatenated queries (SQLi risk), unescaped output (XSS risk), missing auth checks on a new endpoint — cross-reference [[security-testing]].
- **Testability smells** — hard dependencies on real time/network/global state that make the code hard to test in isolation (a sign tests for this code will be either missing or flaky).
- **Missing test coverage for the actual change** — a PR that changes behavior with no corresponding test change is a specific, callable-out finding, not just a vague "needs more tests."

## Automatic test generation from artifacts
Generate test cases/scenarios systematically from whatever artifact is available, don't start from a blank page:
- **From requirements/PRD/user stories/acceptance criteria**: extract each explicit condition as a positive test, then derive negative tests for each (what happens when the condition is violated) — see [[manual-testing]]'s design techniques for the systematic method.
- **From OpenAPI/GraphQL schema**: generate boundary and type-violation cases per field automatically (tools like Schemathesis do this via property-based testing) — see [[api-testing]], [[contract-testing]].
- **From a database schema**: derive constraint-violation tests (NOT NULL, UNIQUE, FK) directly from the DDL — see [[database-testing]].
- **From existing code**: identify untested branches/conditionals and write tests targeting them specifically, rather than generic happy-path tests that duplicate existing coverage.
- **From production logs/Sentry issues/bug reports**: a real production failure is a test case waiting to be written — extract the exact input/state that triggered it and turn it into a permanent regression test, per [[regression-testing]].
Always review generated tests for whether the assertion is actually meaningful (asserting "no error thrown" is weak; asserting the specific expected state is strong) — generated tests that don't assert anything useful are worse than no test, because they create false coverage confidence.

## Bug intelligence: root cause analysis
1. **Reproduce first** — a bug that can't be reliably reproduced can't be reliably root-caused; narrow the reproduction steps to the minimal case before theorizing.
2. **Walk the observability chain**: test/report → logs → trace → API call → DB/infra state, per [[observability-testing]] — find the layer where actual behavior diverges from expected, don't guess above that layer.
3. **Distinguish symptom from cause**: a 500 error is a symptom; the unhandled null downstream is the cause. Keep asking "why" until you reach something actionable and specific (a line of code, a missing check, a race condition) — not "the system is flaky."
4. **State the evidence, not just the conclusion** — "likely caused by X" should be followed by the specific log line/trace/code reference that supports it, so someone else can verify the reasoning rather than trust it blindly.

## Duplicate detection & failure clustering
- Before filing a new bug, check whether an existing open report matches — compare error signature (exception type + top stack frame), affected endpoint/feature, and repro conditions, not just the surface symptom text (two different root causes can produce superficially similar user-facing symptoms, and the same root cause can produce different-looking symptoms in different contexts).
- When triaging a batch of failures (e.g. a regression suite run), cluster by likely shared cause (same error signature, same recently-changed file, same timing window) before filing — one root cause reported once with all affected cases listed is far more useful than N duplicate tickets.

## Severity/priority reasoning
Assign severity/priority with the evidence and reasoning visible (per [[bug-reporting]]'s scale), not as an opaque label — state the actual business/user impact observed, not just a category name.

## Cross-link
This skill is what [[autonomous-qa-orchestration]] calls during its "investigate," "discover bugs," and "generate report" steps.

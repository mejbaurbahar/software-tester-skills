---
name: unit-testing
description: Use when writing, refactoring, or auditing unit and component tests — isolated test doubles (mocks, stubs, spies), Arrange-Act-Assert (AAA) pattern, boundary value analysis, property-based testing, and code coverage.
---

# Unit & Component Testing

## Overview
Unit testing validates the smallest testable units of code (functions, methods, classes, components) in complete isolation from external dependencies (databases, networks, filesystem, third-party services).

## Core Principles
1. **Isolation**: Never touch real external systems in unit tests. Use test doubles (stubs, mocks, fakes).
2. **Speed & Determinism**: Unit tests must execute in milliseconds and produce 100% deterministic results regardless of execution order or environment.
3. **AAA Pattern**:
   - **Arrange**: Set up test fixtures, input data, and expected outputs.
   - **Act**: Execute the specific unit under test.
   - **Assert**: Verify the result, state change, or mock interaction.
4. **One Logical Assertion per Test**: Focus on one behavioral outcome per test case for pinpoint failure diagnostics.

## Test Design Techniques
- **Boundary Value Analysis (BVA)**: Test values at boundaries: `min - 1`, `min`, `nominal`, `max`, `max + 1`.
- **Equivalence Partitioning (EP)**: Divide input domain into valid and invalid partitions; select representative values from each.
- **Error Guessing & Defensive Checks**: `null`, `undefined`, empty strings, NaN, overflow values, special unicode characters.
- **Property-Based Testing**: Use property generators (e.g. `Hypothesis` for Python, `fast-check` for JS/TS) to verify mathematical invariants across thousands of random inputs.

## Test Doubles Quick Reference
| Double | Purpose | When to Use |
| :--- | :--- | :--- |
| **Dummy** | Passed around but never actually used | Filling required parameter signatures |
| **Stub** | Returns canned answers to calls made during test | Providing fixed input data without running real logic |
| **Spy** | Records information about calls made to it | Verifying call counts, arguments, or execution order |
| **Mock** | Pre-programmed with expectations of calls it must receive | Behavioral verification of interactions |
| **Fake** | Working implementation with shortcuts (e.g. in-memory DB) | Complex stateful unit/component isolation |

## Recommended Tooling
- **JavaScript / TypeScript**: Jest, Vitest, Node Test Runner (`node:test`), Testing Library (React/Vue), fast-check.
- **Python**: Pytest, unittest.mock, pytest-mock, Hypothesis.
- **Go**: `testing` package, testify (`assert`, `mock`), gomock.
- **Java / Kotlin**: JUnit 5, Mockito, AssertJ, jqwik.

## Common Anti-Patterns to Avoid
- **Testing Implementation Details**: Asserting private variables or internal method sequences instead of public contract outputs.
- **Over-Mocking**: Mocking everything until the test only verifies mock wiring rather than actual logic.
- **Flaky Unit Tests**: Dependencies on system clock (`Date.now()`), filesystem state, or network. Always freeze or stub time.

---
name: unit-testing
description: Use when writing, refactoring, or auditing unit and component tests — isolated test doubles (mocks, stubs, spies), Arrange-Act-Assert (AAA) pattern, boundary value analysis, property-based testing, and code coverage.
license: MIT
metadata:
  category: code-level
  version: "2.0"
  tags: unit-testing, aaa, mocks, stubs, boundary-value, pytest, jest
---

# Unit & Component Testing

Unit tests validate the smallest testable behaviors (functions, methods, classes, components) **in isolation** from slow or unreliable dependencies. Done well they are your fastest feedback loop and the safety net for refactoring.

## Principles (F.I.R.S.T.)
**F**ast (milliseconds) · **I**solated (no network, DB, clock, filesystem, randomness) · **R**epeatable (same result anywhere) · **S**elf-validating (assert, do not eyeball) · **T**imely (written with or before the code, `tdd-workflow`).
- **Arrange-Act-Assert:** set up inputs, execute the unit, verify the outcome. One behavior per test; the name states the behavior.
- **Test behavior, not implementation:** assert on public outputs and observable effects so tests survive refactoring.

## What to test
Business rules and calculations · branches and error paths · boundaries (`test-design-techniques`) · invariants (`property-based-testing`) · state transitions · input validation · idempotence · async success/failure/timeouts · component rendering and interaction (Testing Library: query by role/label, act like a user).

## Test doubles
| Double | Use when |
| :--- | :--- |
| **Dummy** | A parameter is required but unused |
| **Stub** | You need canned return values |
| **Spy** | You must check calls, arguments or order |
| **Mock** | Behavior verification of an interaction is the point |
| **Fake** | A lightweight working implementation (in-memory repo) beats stubbing many calls |
Double **only at real boundaries** (I/O, time, randomness, other modules' side effects). If a test mostly asserts that mocks were called, it verifies wiring, not logic.

## Examples
```python
# pytest: parametrized boundaries + exception + frozen time
import pytest
from freezegun import freeze_time

@pytest.mark.parametrize("age,expected", [(17,"minor"),(18,"adult"),(64,"adult"),(65,"senior")])
def test_age_band(age, expected): assert band(age) == expected

def test_negative_age_rejected():
    with pytest.raises(ValueError, match="age"): band(-1)

@freeze_time("2026-03-08 06:59:59")
def test_token_expires_at_boundary(): assert not Token(ttl=1).expired()
```
```ts
// Vitest/Jest: async + component
it('debounces search and shows results', async () => {
  vi.useFakeTimers(); const search = vi.fn().mockResolvedValue([{ id: 1, name: 'Mug' }]);
  render(<Search api={search} />);
  await userEvent.type(screen.getByRole('searchbox'), 'mug');
  await vi.advanceTimersByTimeAsync(300);
  expect(search).toHaveBeenCalledTimes(1);
  expect(await screen.findByText('Mug')).toBeVisible();
});
```
```java
// JUnit 5 + AssertJ + Mockito
@Test void refundsCannotExceedPayment() {
  var svc = new RefundService(paymentRepo);              // paymentRepo is a mock/fake
  assertThatThrownBy(() -> svc.refund("P1", Money.of(150)))
      .isInstanceOf(RefundTooLargeException.class);
}
```

## Tooling
| Stack | Frameworks |
| :--- | :--- |
| JS/TS | Vitest, Jest, node:test, Testing Library, fast-check |
| Python | pytest, unittest.mock/pytest-mock, Hypothesis, freezegun |
| Java/Kotlin | JUnit 5, Mockito/MockK, AssertJ, jqwik |
| .NET | xUnit/NUnit, Moq/NSubstitute, FluentAssertions |
| Go | `testing`, testify, gomock |
| Rust | built-in `#[test]`, proptest, insta |

## Quality checks
Mutation testing shows whether tests actually detect changes (`mutation-testing`); coverage shows what is *not* tested (`code-coverage-analysis`); fail-first discipline proves a test can fail; keep the suite under a few seconds per module.

## Anti-patterns
Asserting private fields or call sequences · over-mocking · shared mutable fixtures · clock/network/filesystem dependence · giant tests with many reasons to fail · conditionals or loops in tests · testing framework code · snapshot tests of huge outputs (`snapshot-golden-testing`) · ignoring failing tests with `skip`.

## Related
`tdd-workflow`, `property-based-testing`, `mutation-testing`, `code-coverage-analysis`, `integration-testing`, `test-design-techniques`

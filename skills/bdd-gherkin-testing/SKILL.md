---
name: bdd-gherkin-testing
description: Use when writing or automating behavior-driven development (BDD) specs — Gherkin Given/When/Then, Cucumber, SpecFlow, Behave, pytest-bdd, Playwright-BDD, example mapping, living documentation, and fixing brittle or imperative feature files.
license: MIT
metadata:
  category: functional
  version: "2.0"
  tags: bdd, gherkin, cucumber, behave, specflow, example-mapping, living-documentation
---

# BDD & Gherkin

BDD is a **collaboration practice first, a test tool second.** Feature files are executable specifications that product, dev and QA agree on *before* coding (the "three amigos").

## Discovery: Example Mapping (25 min per story)
Cards: **Story** (yellow) → **Rules** (blue) → **Examples** (green) → **Questions** (red). If red cards outnumber green, the story is not ready. Each green card becomes one scenario.

## Write declarative, not imperative
```gherkin
# BAD — imperative, UI-coupled, brittle
Scenario: Login
  Given I open "https://app.test/login"
  When I type "ann@x.com" into "#email"
  And I click "#submit"
  Then I see the element ".dashboard"

# GOOD — declarative, business language
Feature: Account access
  Rule: Locked accounts cannot sign in

  Scenario: Locked customer is told how to recover
    Given Ann's account was locked after 5 failed attempts
    When Ann signs in with the correct password
    Then she is told the account is locked
    And she is offered a password-reset link
```

## Gherkin rules of thumb
- One behavior per scenario; 3–7 steps; **Given** = state, **When** = one action, **Then** = observable outcome.
- Use `Background` only for context every scenario needs and that is short.
- Use `Scenario Outline` + `Examples` for data variation; name example columns meaningfully.
- Tag for selection: `@smoke @regression @wip @slow @api @ui`. Run subsets with `--tags`.
- No `And` chains in `When`; no assertions in `Given`; no implementation words (click, table, id).

## Tooling quick start
| Stack | Tool | Run |
| :--- | :--- | :--- |
| JS/TS | `@cucumber/cucumber`, `playwright-bdd` | `npx cucumber-js --tags "@smoke and not @wip"` |
| Python | `behave`, `pytest-bdd` | `behave --tags=@smoke` / `pytest -m smoke` |
| Java | Cucumber-JVM + JUnit 5 | `mvn test -Dcucumber.filter.tags="@smoke"` |
| .NET | Reqnroll / SpecFlow | `dotnet test --filter Category=smoke` |
| Ruby | Cucumber | `cucumber --tags @smoke` |

Step definitions stay thin: parse → call a **domain/driver layer** (API client or page object) → assert. Never put business logic in steps. Share state via a per-scenario World/context object, never globals.

## Living documentation
Publish results (Cucumber HTML/JSON report, Allure, Serenity) so business readers see which rules are passing. A failing scenario should read as a business sentence.

## Anti-patterns
- Feature files written by QA alone after the code ships (BDD as "Selenium with English").
- Scenarios per UI screen; hundreds of near-duplicates; steps like `I click the 3rd button`.
- Assertions on internals (DB rows) when an observable outcome exists.
- Slow suites: run most rules at API/service level; keep UI scenarios to critical journeys (`e2e-testing`).

## Related skills
`acceptance-testing`, `test-design-techniques`, `e2e-testing`, `api-testing`, `test-automation`

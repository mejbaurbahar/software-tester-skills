---
name: functional-testing
description: Use when verifying that a feature or user flow behaves according to requirements/specs — functional correctness testing of forms, workflows, business logic, and CRUD operations, whether done manually or via automation.
license: MIT
metadata:
  category: functional
  version: "2.0"
  tags: functional, forms, workflows, business-logic, crud
---

# Functional Testing

Verify the system does what the requirements and acceptance criteria say, from the user's point of view. Non-functional qualities (performance, security, accessibility) have their own skills.

## Workflow
1. **Extract acceptance criteria** from the spec/ticket. If none exist, derive them from the UI/PRD and confirm before testing against assumptions (`requirements-testing-review`).
2. **Happy path first:** the primary flow the feature exists for.
3. **Alternate flows:** every branch, conditional, optional field, toggle, role.
4. **Negative flows:** invalid input, missing required fields, unauthorized actions, expired sessions, duplicate submissions.
5. **Derive cases systematically** (`test-design-techniques`): partitions and boundaries, decision tables for business rules, state models for lifecycles.
6. **Cross-check business rules beyond the UI:** does the discount change the persisted order total, not just a struck-through price?

## CRUD checklist
| Operation | Verify |
| :--- | :--- |
| **Create** | Required/optional validation, duplicates, defaults, success feedback, record actually **persisted** (API/DB, not just a toast), audit fields |
| **Read** | Empty list, page 0/last page, sort/filter combinations, stale data after mutation, permission-filtered results |
| **Update** | Partial updates, concurrent edit conflicts, optimistic UI vs persisted state, validation re-applied, history/audit |
| **Delete** | Soft vs hard delete, cascades and orphans, confirmation, undo, permissions, referential integrity |

## Form checklist
Required vs optional enforced **client and server side** · field constraints (length, type, format, locale) · unicode/emoji/whitespace · submit disabled while in flight (double-submit) · error text points at the right field in plain language · autosave/draft behavior · tab order and keyboard submit · paste and browser autofill · file upload limits.

## Multi-step workflows (checkout, onboarding, wizards)
Abandon and resume at each step · go back and change an earlier answer (does downstream state update?) · run the flow twice without a refresh (state leakage) · browser back/forward/refresh mid-flow · session expiry mid-flow · final committed state equals what the wizard displayed.

## Business logic verification
Do not treat the UI as the oracle. Cross-check totals, discounts, taxes, eligibility and permission-derived visibility against API responses (browser network tab or `curl`) and, where accessible, the database.

## Data and environment
Realistic and edge data (`test-data-engineering`): long names, special characters, boundary quantities/amounts, time zones (`date-time-timezone-testing`), multiple roles and locales. Record build, environment and data used for reproducibility.

## Tooling
Browser DevTools (network, console, storage), Playwright/Cypress for repeatable flows (`test-automation`), API clients for state checks (`api-testing`). Automate flows you run repeatedly; log defects with `bug-reporting`.

## Exit criteria
All Must acceptance criteria verified · no open Sev1/Sev2 · Sev3 defects triaged with workarounds · coverage of requirements traced (`test-planning-documentation`).

## Related
`manual-testing`, `exploratory-testing`, `acceptance-testing`, `regression-testing`, `test-design-techniques`, `bug-reporting`

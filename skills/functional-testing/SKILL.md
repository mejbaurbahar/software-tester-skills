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

## Purpose
Verify the system does what it's supposed to do, per requirements/acceptance criteria — as opposed to non-functional concerns (performance, security, accessibility, which have their own skills).

## Workflow
1. **Extract acceptance criteria** from the spec/ticket. If none exist, derive them from the UI/PRD and confirm with the user before testing against assumptions.
2. **Map the happy path** first — the primary flow the feature exists for.
3. **Enumerate alternate flows** — every branch, conditional, optional field, toggle.
4. **Enumerate negative flows** — invalid input, missing required fields, unauthorized actions, expired tokens.
5. **Cross-check business rules**, not just UI behavior: does a discount actually apply to the order total in the DB, not just render a strikethrough price?

## CRUD feature checklist
For any Create/Read/Update/Delete surface:
- **Create**: required-field validation, duplicate handling, default values, success feedback, record actually persisted (verify via API/DB, not just toast message).
- **Read**: pagination edges (page 0, last page, empty list), sorting/filtering combinations, stale-data-after-mutation.
- **Update**: partial updates, concurrent-edit conflicts, optimistic UI vs. actual persisted state, validation re-applied on edit.
- **Delete**: soft vs hard delete, cascading effects (does deleting a parent orphan children?), confirmation dialogs, undo if offered, permissions.

## Form testing checklist
- Required vs optional field enforcement, client-side AND server-side (client validation is not security or correctness).
- Field-level constraints: min/max length, type coercion, format (email, phone, date locale).
- Submit button state (disabled during submission — prevents double-submit bugs).
- Error message accuracy — does it point to the right field, in plain language?
- Autosave/draft behavior if present.
- Tab order and keyboard-only submission.

## Multi-step workflow testing (checkout, onboarding, wizards)
- Test abandoning at each step and resuming.
- Test going back a step and changing an earlier answer — does downstream state update or go stale?
- Test the flow twice in a row without refresh (session/state leakage between runs).
- Verify the final committed state server-side matches what the wizard displayed.

## Business logic verification
Don't trust the UI as the oracle. Cross-check calculated values (totals, discounts, tax, permissions-derived visibility) against:
- API response payloads (use Chrome DevTools MCP / Claude in Chrome network tab, or curl the endpoint directly).
- Database state when accessible.

## Tooling in this harness
- Use Claude in Chrome or Chrome DevTools MCP for live DOM/network verification (see the `claude-in-chrome` skill).
- For flows worth repeating, promote to the [[test-automation]] skill instead of re-running manually every time.
- Log defects via [[bug-reporting]].

---
name: requirements-testing-review
description: Use when reviewing requirements, user stories, designs or specs before coding (shift-left static testing) — finding ambiguity, missing acceptance criteria, testability gaps, contradictory rules, and NFR omissions; INVEST checks, walkthroughs, and requirement-quality scoring.
license: MIT
metadata:
  category: strategy
  version: "2.0"
  tags: shift-left, static-testing, requirements, user-stories, testability, invest, review
---

# Requirements & Design Testing (Static Testing)

A defect found in requirements costs ~1×; the same defect found in production costs 30–100×. Review before anyone writes code.

## Quality checklist (apply to every requirement)
| Attribute | Question |
| :--- | :--- |
| Unambiguous | Could two engineers implement it differently? Highlight weasel words: *fast, easy, appropriate, etc., should, as needed, user-friendly, robust, similar to*. |
| Testable | Is there an observable pass/fail? Has a number/threshold? |
| Complete | Error cases, empty state, permissions, limits, undo, audit, i18n, a11y, data retention? |
| Consistent | Contradicts another rule/screen/API? Same term = same meaning? |
| Feasible | Can it be built/measured within constraints? |
| Traceable | Has an ID, source, owner? |
| Atomic | One requirement per statement (no "and/or" bundles)? |

## User-story review: INVEST + 3C
**I**ndependent · **N**egotiable · **V**aluable · **E**stimable · **S**mall · **T**estable. Card, Conversation, Confirmation (acceptance criteria).

## Question generators (use on every story)
- **Who** can do this? Who must *not*? What happens for each role?
- **What if** input is empty / huge / duplicated / concurrent / offline / slow / partially failed?
- **When** does it start/expire/retry? Time zones? DST?
- **How much**: volume, latency, size, rate limit, cost?
- **What next**: what state is the data in afterwards? What is logged/notified?
- **What changed**: which existing behavior, reports, integrations or migrations does this touch?

## Testability review of the design
Observable state (logs, IDs, events)? Seams for stubbing time/network/payments? Deterministic IDs/clocks? Feature flag/kill switch? Idempotent operations? Test data creatable via API?

## Output: review findings table
```
| # | Ref | Type (ambiguity/gap/conflict/NFR) | Quote | Question / Suggested rewrite | Severity |
```
Example rewrite: *"Search should be fast"* → *"p95 search latency ≤ 300 ms for 1M records at 50 concurrent users."*

## Techniques
Walkthrough · technical review · inspection (roles: author, moderator, reader, scribe) · perspective-based reading (user, tester, ops, security) · prototype/wireframe review · Three Amigos.

## Related
`bdd-gherkin-testing`, `acceptance-testing`, `test-strategist`, `test-design-techniques`, `threat-modeling`

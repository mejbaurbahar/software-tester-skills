---
name: manual-testing
description: Use when designing test cases, doing exploratory testing, writing test plans/checklists, or manually verifying a feature before or instead of automating it. Covers test case design techniques, exploratory charters, and test plan structure.
---

# Manual Testing

## When to reach for this
- Before automation exists, or when automation isn't worth the cost (one-off, highly visual, exploratory).
- New feature needs a test plan.
- Investigating a reported bug and need a repeatable, structured approach.

## Test case design techniques
Pick techniques based on the input space, don't just guess values:
- **Equivalence partitioning** — split inputs into classes that should behave the same; test one representative per class.
- **Boundary value analysis** — test min, min-1, min+1, max, max-1, max+1, and just-outside-range values. Most bugs live at boundaries.
- **Decision table testing** — for features with multiple independent conditions (e.g. role × subscription tier × feature flag), build a table of condition combinations and expected outcomes.
- **State transition testing** — for anything with a lifecycle (order status, account state), test valid transitions, invalid transitions, and transitions from every state.
- **Pairwise/combinatorial testing** — when full combinatorial coverage is too large, use pairwise coverage to catch most interaction bugs cheaply.
- **Error guessing** — based on experience: empty strings, nulls, huge inputs, unicode/emoji, SQL-special chars, double-submits, back-button, concurrent edits.

## Exploratory testing (session-based)
1. **Charter** — one sentence: what area, what risk you're hunting for. e.g. "Explore checkout discount code entry for validation and edge-case bugs, 30 min."
2. **Time-box** — 30–90 min sessions. Don't sprawl.
3. **Tour styles** to vary coverage:
   - *Landmark tour* — visit every major screen/feature once.
   - *FedEx tour* — follow one piece of data end-to-end through the system.
   - *Saboteur tour* — try to break things: kill network mid-action, resize window, spam-click, go back/forward.
   - *Money tour* — focus on whatever the business cares about most (checkout, signup, payment).
4. **Log as you go**: what you did, what you noticed, questions raised, bugs found — even things that "seem fine but weird."
5. **Debrief**: summarize coverage, bugs, and follow-up charters needed.

## Test plan structure
```markdown
# Test Plan: <Feature/Release>
## Scope
- In scope / out of scope
## Test approach
- Manual / automated split, environments, browsers/devices
## Entry criteria
- Feature deployed to staging, test data seeded, etc.
## Test cases
- ID | Title | Preconditions | Steps | Expected | Priority
## Risk areas
- What's most likely to break, and why
## Exit criteria
- % pass rate, zero blockers/criticals, sign-off owner
```

## Checklist habits that catch real bugs
- Test with a **freshly created account** and an **old account with legacy data** — schema drift bugs hide here.
- Test **empty states** (zero items, zero results) not just populated ones.
- Test **permissions boundaries**: logged out, wrong role, expired session, another tenant's data.
- Test **concurrency**: two tabs, two users editing the same record, double-submit on slow network.
- Test **input extremes**: very long strings, unicode/emoji/RTL text, negative numbers, decimals where integers expected, huge file uploads.
- Test **browser back/forward** and refresh mid-flow.
- Always verify against the **actual backend state** (DB row, API response), not just what the UI shows — the UI can lie.

## Reporting
When a manual test finds a defect, use the [[bug-reporting]] skill's template so severity/repro/evidence are consistent across the QA harness (`~/qa-agent/QA_RULES.md` is the canonical format here).

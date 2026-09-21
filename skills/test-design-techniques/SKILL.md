---
name: test-design-techniques
description: Use when deriving test cases systematically — equivalence partitioning, boundary value analysis, decision tables, state transition testing, pairwise/combinatorial testing, use-case and classification-tree techniques, error guessing, and choosing which technique fits which requirement.
license: MIT
metadata:
  category: strategy
  version: "2.0"
  tags: equivalence-partitioning, boundary-value, decision-table, state-transition, pairwise, black-box-techniques
---

# Test Design Techniques

Good testing is *choosing the smallest set of cases with the highest defect-finding power*. Pick the technique from the shape of the requirement.

## Pick a technique
| Requirement shape | Technique |
| :--- | :--- |
| Input ranges / classes | Equivalence Partitioning + Boundary Value Analysis |
| Many conditions → outcomes (business rules) | Decision table |
| Object with lifecycle/status | State transition |
| Many independent parameters (browser × OS × plan…) | Pairwise / combinatorial |
| User goals through the system | Use-case / scenario |
| Numeric formulas | BVA + property-based (`property-based-testing`) |
| Unknown unknowns | Error guessing, exploratory (`exploratory-testing`) |

## 1. Equivalence Partitioning (EP)
Split each input into classes the system treats identically; test one value per class (valid *and* invalid).
`age: <0 | 0–17 | 18–64 | 65–120 | >120 | non-numeric | empty` → 7 tests, not 120.

## 2. Boundary Value Analysis (BVA)
Defects cluster at edges. For range `[min,max]` test `min-1, min, min+1, max-1, max, max+1` (3-value: `min-1,min,max,max+1`). Include types edges: `0, -1, INT_MAX, INT_MAX+1`, empty string, 1-char, max-length, max-length+1, unicode.

## 3. Decision table
List conditions (rows) × rules (columns) → actions. N boolean conditions = 2^N rules; collapse "don't care" (–).
| | R1 | R2 | R3 | R4 |
| :--- | :-: | :-: | :-: | :-: |
| Member | Y | Y | N | N |
| Order > $100 | Y | N | Y | N |
| **Free shipping** | Y | Y | Y | N |
Test one case per rule; the table exposes missing/contradictory rules.

## 4. State transition
Draw states, events, guards, actions. Cover: every state (0-switch), every valid transition, **every invalid event in every state** (the bug farm), and sequences of 2 transitions (1-switch) for critical flows. Example order: `Created→Paid→Shipped→Delivered`, plus `Cancel` from each, and `Ship` from `Created` (must be rejected).

## 5. Pairwise (all-pairs)
Most bugs come from ≤2 interacting parameters. Generate with a tool:
```bash
pip install allpairspy       # Python
# or PICT (Microsoft):  pict model.txt > cases.tsv
# model.txt:
# Browser: Chrome, Firefox, Safari
# OS: Win, macOS, Linux
# Plan: Free, Pro, Enterprise
```
3×3×3=27 combos → ~9–10 pairwise cases. Add manual cases for known risky triples.

## 6. Use-case / scenario
Main success path + each alternate and exception flow as separate cases; add preconditions and postconditions.

## Traceability & review
Tag each case with the technique and requirement ID. Review the *model* (partitions, tables, state diagram) with the team, not just the cases.

## Anti-patterns
Testing only the happy path; random values instead of partitions; "one big" test covering many rules; no negative/invalid cases; boundaries guessed instead of read from the spec.

## Related
`manual-testing`, `unit-testing`, `functional-testing`, `property-based-testing`, `requirements-testing-review`

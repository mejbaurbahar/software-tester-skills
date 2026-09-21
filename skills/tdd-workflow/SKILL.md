---
name: tdd-workflow
description: Use when practicing or coaching test-driven development — red-green-refactor, outside-in vs inside-out (London vs Chicago), test lists, baby steps, TDD with AI coding agents, and legacy-code TDD (seams, characterization tests).
license: MIT
metadata:
  category: code-level
  version: "2.0"
  tags: tdd, red-green-refactor, london-school, chicago-school, ai-pair, refactoring
---

# Test-Driven Development

Write a failing test → make it pass simply → refactor. The tests are a *design tool* that produce a regression net as a by-product.

## The loop (2–10 minutes per cycle)
1. **Test list**: brainstorm behaviors/edge cases; pick the simplest next one.
2. **RED**: write one small failing test; run it; **see it fail for the right reason** (message says what you expect).
3. **GREEN**: write the *least* code to pass — fake it, hard-code, triangulate with a second example.
4. **REFACTOR**: remove duplication, improve names, keep all green. No new behavior here.
5. Commit; pick the next item. Update the list with anything learned.

```text
RED   test_fizzbuzz_returns_1_for_1       → NameError
GREEN def fizzbuzz(n): return "1"
RED   test_returns_2_for_2                → "1" != "2"
GREEN def fizzbuzz(n): return str(n)      # triangulated
```

## Two schools
| | Chicago / classicist | London / mockist |
| :--- | :--- | :--- |
| Direction | Inside-out, state-based | Outside-in, interaction-based |
| Doubles | Real collaborators where cheap | Mock collaborators to discover roles |
| Good for | Algorithms, domain logic | Layered apps, discovering interfaces |
| Risk | Slow to find seams | Tests coupled to implementation |
Blend: *outside-in acceptance test* (`bdd-gherkin-testing`) driving *inside-out unit TDD*.

## Heuristics
Baby steps · one assertion idea per test · test names as sentences · don't test private methods · transformation priority premise (constant→variable→conditional→loop) · keep the bar green when refactoring · delete tests that duplicate coverage.

## TDD with an AI coding agent
1. **You write (or approve) the failing test first**; agent implements to green. 2. Ask agent to *run* the suite and show red before green. 3. Forbid editing tests to pass (diff review). 4. Have it propose the next 5 test-list items and edge cases. 5. Verify with mutation testing that the tests bite.

## Legacy code
Find a **seam** (constructor/param injection, subclass-and-override, wrapper), pin behavior with characterization tests (`snapshot-golden-testing`), then refactor and TDD new behavior (Feathers' *Working Effectively with Legacy Code*).

## Smells
Test after code "TDD" · huge red phase · brittle mocks · tests that never fail · skipping refactor.

## Related
`unit-testing`, `test-design-techniques`, `mutation-testing`, `property-based-testing`

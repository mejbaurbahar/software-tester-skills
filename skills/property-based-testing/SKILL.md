---
name: property-based-testing
description: Use when example-based tests miss edge cases — property-based testing with Hypothesis, fast-check, jqwik, QuickCheck, or proptest; invariants, round-trip, oracle and metamorphic properties, shrinking, stateful/model-based tests.
license: MIT
metadata:
  category: code-level
  version: "2.0"
  tags: property-based, hypothesis, fast-check, quickcheck, invariants, shrinking, stateful-testing
---

# Property-Based Testing (PBT)

Instead of asserting `f(3) == 9`, assert a **property that must hold for all inputs**; the framework generates hundreds of cases, then **shrinks** any failure to a minimal counter-example.

## Find properties (the hard part) — 7 patterns
1. **Round-trip**: `decode(encode(x)) == x` (serializers, parsers, compress, crypto).
2. **Invariant**: `len(sort(xs)) == len(xs)`, output is ordered, total money conserved.
3. **Idempotence**: `f(f(x)) == f(x)` (normalize, dedupe, PUT).
4. **Oracle**: compare with a slow/simple reference implementation.
5. **Metamorphic**: `search(q + filter) ⊆ search(q)`; `price(2×qty) == 2×price(qty)`.
6. **Commutativity/associativity** where the domain promises it.
7. **No-crash / postcondition**: for any valid input, no exception and result satisfies the contract.

## Examples
```python
# Python — Hypothesis
from hypothesis import given, strategies as st, settings
@given(st.lists(st.integers()))
def test_sort_props(xs):
    out = sorted(xs)
    assert len(out) == len(xs)
    assert all(a <= b for a, b in zip(out, out[1:]))
    assert sorted(out) == out            # idempotent
```
```ts
// TypeScript — fast-check
import fc from "fast-check";
test("json round-trip", () => {
  fc.assert(fc.property(fc.jsonValue(), v => expect(JSON.parse(JSON.stringify(v))).toEqual(v)));
});
```
```bash
pytest --hypothesis-seed=12345          # reproduce a failing run
npx jest --testTimeout=30000            # PBT can be slower
```

## Generator design
- Constrain to the **valid domain** with strategies (`st.integers(0, 120)`), not `assume()` filters that discard most inputs.
- Build domain objects with composite strategies (`@st.composite`, `fc.record`). Include nasty values: empty, huge, unicode, NaN, negative zero, duplicates.
- Keep generators fast; set `max_examples` (default 100) up in CI nightly (1000+), down for PR (50).

## Stateful / model-based testing
Model the system as a simple state machine; generate random command sequences; compare real system to the model after each step (Hypothesis `RuleBasedStateMachine`, fast-check `commands`). Excellent for caches, queues, carts, DB wrappers, REST CRUD.

## Reproducibility
Persist failing examples (Hypothesis `.hypothesis/` DB; commit `@example(...)` for regression); log seeds in CI. Never mark a PBT flaky — a failure is a real counter-example (or a bad property).

## Pitfalls
Re-implementing the function inside the property (tautology) · properties too weak (`assert True`) · non-determinism in the code under test · unbounded generators blowing runtime.

## Related
`unit-testing`, `fuzz-testing`, `test-design-techniques`, `mutation-testing`

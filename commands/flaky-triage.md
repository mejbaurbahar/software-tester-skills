---
description: Investigate and fix intermittent (flaky) test failures
argument-hint: "[test name or CI run]"
---

Triage flakiness for: $ARGUMENTS

Use the `flaky-test-management`, `concurrency-race-condition-testing` and `date-time-timezone-testing` skills.

1. Reproduce: run the test many times (for example `--count=50` or `--repeat-each=50`), alone and in the full suite, in random order and in parallel. Record the failure rate.
2. Classify the cause (shared state, order dependence, timing, clock, network, resources, randomness) using the evidence, not a guess.
3. Fix the root cause in the smallest way (explicit waits on conditions, isolated data, frozen clock, seeded randomness). Do not just add retries.
4. Prove it: re-run the same number of times and report before/after failure rates.

---
description: Review test code for quality, brittleness, and false confidence
argument-hint: "[test path or PR]"
---
<!-- Generated from commands/review-tests.md by scripts/build_adapters.py - do not edit by hand. -->

Review the tests in: $ARGUMENTS

Use the `test-architect`, `testing-strategies`, `mutation-testing` and `flaky-test-management` skills.

1. Look for: missing or weak assertions, tests coupled to implementation, over-mocking, shared state, sleeps, order dependence, unclear names, duplicated cases, tests at the wrong level.
2. Check that failures would be informative and that tests would fail if the behavior broke (spot-check by mutating the code).
3. Report findings by severity with `file:line` and a concrete rewrite for the worst ones.

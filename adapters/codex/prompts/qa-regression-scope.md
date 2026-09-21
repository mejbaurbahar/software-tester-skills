---
description: Pick the regression tests to run for a change, from the git diff
argument-hint: "[branch, commit range, or PR]"
---
<!-- Generated from commands/regression-scope.md by scripts/build_adapters.py - do not edit by hand. -->

Determine regression scope for: $ARGUMENTS

Use the `regression-testing`, `release-readiness-testing` and `code-coverage-analysis` skills.

1. Compute the diff (`git diff --stat` and `git diff` against the base branch, or the range in $ARGUMENTS).
2. Map changed files to features, shared modules and integration points; list direct and indirect impact.
3. Rank the impact by risk: money/auth/data first.
4. Recommend the exact tests to run (by path or tag), the ones to add, and what can be skipped and why.
5. Give the command lines to run the selected set.

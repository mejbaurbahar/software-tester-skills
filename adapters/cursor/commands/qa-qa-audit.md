<!-- Generated from commands/qa-audit.md by scripts/build_adapters.py - do not edit by hand. -->
# Audit a repository's QA health and recommend which testing skills to apply

Audit the QA health of: the text the user typed after this command (ask if none) (default: the current repository)

Use the `qa-skill-router`, `qa-fundamentals`, `test-strategist` and `test-metrics-reporting` skills.

1. Inspect the stack, test folders, CI config, coverage settings, linters, security scanning and docs.
2. Score these areas as strong, weak or missing: unit, integration, API, E2E, performance, security, accessibility, static analysis, test data, environments, CI gates, flaky-test control.
3. Give the ten highest-value improvements in priority order, each with the skill to use and the slash command to run.
4. Save the result to `reports/qa-audit-<date>.md`.

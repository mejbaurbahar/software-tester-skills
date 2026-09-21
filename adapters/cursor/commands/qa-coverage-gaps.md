<!-- Generated from commands/coverage-gaps.md by scripts/build_adapters.py - do not edit by hand. -->
# Find meaningful test coverage gaps and write the missing tests

Analyse coverage gaps for: the text the user typed after this command (ask if none)

Use the `code-coverage-analysis`, `mutation-testing` and `unit-testing` skills.

1. Run the project's coverage tool with branch coverage. If none is configured, propose the minimal setup.
2. Rank uncovered code by risk: error handling, permissions, money, data changes, recently changed files.
3. For the top gaps, explain which bug could hide there, then write tests that assert behavior (not just execute lines).
4. Re-run coverage, and mutation testing on the hot spots if a tool is available. Report before/after.

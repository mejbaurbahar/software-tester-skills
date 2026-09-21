---
description: Generate high-quality unit tests for a file, function or module
argument-hint: "[path or symbol]"
---
<!-- Generated from commands/unit-tests.md by scripts/build_adapters.py - do not edit by hand. -->

Write unit tests for: $ARGUMENTS

Use the `unit-testing`, `test-design-techniques`, `property-based-testing` and `tdd-workflow` skills.

1. Detect the language and existing test framework/conventions from the repo (package.json, pyproject.toml, pom.xml, go.mod) and follow them.
2. Read the target and list its behaviors, edge cases and error paths.
3. Write tests using Arrange-Act-Assert, one behavior per test, descriptive names, boundary values, and test doubles only at real boundaries. Freeze time and randomness.
4. Add property-based tests where a clear invariant exists.
5. Run the tests. Fix test mistakes, but never change production code to make a test pass without telling the user.
6. Report coverage of the target (branch if available) and any behavior you could not test, with the reason.

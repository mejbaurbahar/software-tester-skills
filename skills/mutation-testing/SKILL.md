---
name: mutation-testing
description: Use when measuring test suite quality, finding false positives, and eliminating blind spots — injecting code mutations (mutants), mutation score, Mutmut, Stryker, and kill rate analysis.
license: MIT
metadata:
  category: code-level
  version: "2.0"
  tags: mutation-testing, stryker, mutmut, test-quality, kill-rate
---

# Mutation Testing

## Overview
Mutation testing evaluates the true quality of your test suite by deliberately introducing faults ("mutants") into your production code. If your tests still pass after code is broken, your tests have blind spots.

## Key Concepts
- **Mutant**: A modified version of production code containing a single syntax or logical change.
- **Killed Mutant**: A test fails when run against the mutated code (SUCCESS — your tests detected the bug).
- **Survived Mutant**: All tests pass despite the broken code (FAILURE — test suite missed the bug).
- **Mutation Score**: `(Killed Mutants / Total Mutants) * 100%`. A far more accurate indicator of test effectiveness than vanity code coverage.

## Common Mutation Operators
1. **Conditional Boundary Replacement**: `>` replaced with `>=`, `<` with `<=`.
2. **Boolean Operator Flipping**: `&&` replaced with `||`, `true` with `false`.
3. **Arithmetic Operator Replacement**: `+` replaced with `-`, `*` with `/`.
4. **Statement Removal**: Removing a function call or early return statement.
5. **Return Value Replacement**: Returning `null`, `0`, or empty string instead of computed value.

## Recommended Tooling
- **JavaScript / TypeScript**: Stryker Mutator (`stryker-js`).
- **Python**: Mutmut (`mutmut run`, `mutmut results`).
- **Java**: PIT (Pitest).
- **Rust**: cargo-mutants.

## When to Run Mutation Testing
- Do not run mutation testing on every PR commit (it is computationally intensive).
- Run on critical core business logic, financial calculations, auth modules, and algorithmic engines.
- Use as an audit step when refactoring legacy code with untrusted test suites.

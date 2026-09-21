---
name: code-coverage-analysis
description: Use when measuring or improving test coverage — line, branch, function, condition/MC-DC and diff/patch coverage; coverage tools (coverage.py, Istanbul/c8, JaCoCo, gcov, go cover); setting sensible thresholds; and finding meaningful gaps rather than chasing 100%.
license: MIT
metadata:
  category: automation
  version: "2.0"
  tags: code-coverage, branch-coverage, jacoco, istanbul, coverage-py, diff-coverage, mc-dc
---

# Code Coverage Analysis

Coverage tells you what is **definitely not tested**, never what is well tested. Use it to find holes, not as a target to game.

## Metric ladder
| Metric | Meaning | Use |
| :--- | :--- | :--- |
| Line/statement | executed lines | baseline |
| **Branch** | each if/else/case taken both ways | **preferred default** |
| Function/method | each function called | API surface |
| Condition / MC/DC | each boolean sub-condition affects outcome | safety-critical (DO-178C, ISO 26262) |
| **Diff / patch** | coverage of *changed lines only* | **best PR gate** |
| Mutation score | do tests *detect* changes | quality proof (`mutation-testing`) |

## Commands
```bash
# Python
pytest --cov=src --cov-branch --cov-report=term-missing --cov-report=xml --cov-fail-under=80
# JS/TS (Vitest/Jest/c8)
npx vitest run --coverage        # or: jest --coverage ; c8 node --test
# Java (Maven + JaCoCo)
mvn verify   # jacoco:report → target/site/jacoco/index.html
# Go
go test ./... -coverprofile=c.out -covermode=atomic && go tool cover -html=c.out
# C/C++
gcc --coverage ... && gcov file.c ; lcov --capture -d . -o cov.info && genhtml cov.info
# Diff coverage on PRs
diff-cover coverage.xml --compare-branch=origin/main --fail-under=90
```

## Setting thresholds
- Overall gate: modest & ratcheting (e.g. ≥ 75% branch, never decrease).
- **Patch gate ≥ 85–90%** on new/changed lines (Codecov/Coveralls/diff-cover).
- Higher (95%+) for money/auth/crypto/parsers; exclude generated code, migrations, trivial DTOs *explicitly* with reasons.

## Reading a report — find *meaningful* gaps
1. Sort by **uncovered lines × complexity × change frequency** (churn hotspots).
2. Look at uncovered *branches* in error handling, permissions, rollbacks, timeouts.
3. Ask "what bug would slip through here?" — write the test for that, not for the line.
4. Confirm tests have assertions (a test that calls code without asserting yields fake coverage) → run mutation testing on hotspots.

## Merge coverage across layers
Unit + integration + E2E (`nyc merge`, `coverage combine`, JaCoCo `merge`), and for E2E use server-side instrumentation to see what real journeys exercise.

## Pitfalls
Goodhart's law (100% target → assertion-free tests) · counting test files in coverage · ignoring branches · exclusion creep (`# pragma: no cover` everywhere) · coverage from flaky/skipped tests.

## Related
`unit-testing`, `mutation-testing`, `test-metrics-reporting`, `cicd-testing`, `regression-testing`

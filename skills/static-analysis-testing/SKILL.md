---
name: static-analysis-testing
description: Use when setting up or triaging static analysis as a quality gate — linters, type checkers, SAST (Semgrep, CodeQL, SonarQube, Bandit), complexity and duplication limits, dead-code detection, and configuring PR gates without drowning in false positives.
license: MIT
metadata:
  category: code-level
  version: "2.0"
  tags: static-analysis, sast, semgrep, codeql, sonarqube, eslint, mypy, linting, quality-gate
---

# Static Analysis as Testing

Static analysis finds defects **without running code**: cheapest, earliest, and runs on every commit. Layer it: *format → lint → types → SAST → quality gate*.

## Toolbelt
| Layer | JS/TS | Python | Java/Kotlin | Go | Any |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Lint | ESLint | Ruff, Pylint | Checkstyle, PMD | `golangci-lint` | — |
| Types | `tsc --noEmit` | mypy, pyright | javac -Xlint | `go vet` | — |
| SAST | eslint-plugin-security | Bandit | SpotBugs+FindSecBugs | gosec | **Semgrep, CodeQL, SonarQube** |
| Secrets | — | — | — | — | gitleaks, trufflehog |
| Complexity/dup | — | radon, xenon | — | gocyclo | SonarQube, jscpd |
| Dead code | knip, ts-prune | vulture | — | staticcheck | — |
| IaC | — | — | — | — | checkov, tfsec, hadolint |

```bash
semgrep scan --config p/owasp-top-ten --config p/security-audit --error --json -o semgrep.json
codeql database create db --language=javascript && codeql database analyze db --format=sarif-latest -o results.sarif
ruff check . && mypy --strict src/ && bandit -r src/ -ll
npx eslint . --max-warnings 0 && npx tsc --noEmit
gitleaks detect --redact --no-banner
```

## Rollout strategy (avoid the "ignore all warnings" trap)
1. **Baseline** existing findings (`--baseline`, SonarQube "new code" period) so only *new* issues fail PRs.
2. Start at high-confidence / high-severity rules; expand monthly.
3. **Block** on: new Critical/High vulns, new secrets, type errors, new bugs. **Warn** on style/smells.
4. Every suppression needs a reason + ticket (`// nosemgrep: rule -- reason, JIRA-1`); audit suppressions quarterly.
5. Output **SARIF** and upload to GitHub Code Scanning for PR annotations.

## Triage a finding (2 minutes)
Is the source attacker-controlled? Is the sink reachable? Is there a sanitizer/validator between them? → True positive (fix) / false positive (tune rule or add a precise suppression) / accepted risk (document).

## Metrics
New-issue rate per PR · mean time to fix · false-positive ratio (<20% target) · suppression count · % code covered by types.

## Custom rules
Encode past incidents as Semgrep rules (`pattern`, `pattern-not`, `metavariable-regex`) so the same bug can never return.

## Related
`security-owasp`, `ai-code-security`, `cicd-testing`, `code-coverage-analysis`, `supply-chain-dependency-testing`

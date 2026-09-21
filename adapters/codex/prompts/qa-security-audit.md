---
description: Defensive security review of code or configuration (OWASP-focused)
argument-hint: "[path, feature, or area]"
---
<!-- Generated from commands/security-audit.md by scripts/build_adapters.py - do not edit by hand. -->

Perform a defensive security review of: $ARGUMENTS

Use the `security-owasp`, `authn-authz-testing`, `static-analysis-testing`, `supply-chain-dependency-testing` and `threat-modeling` skills.

1. Work only on code and systems in this repository or that the user says they own. Do not probe third-party systems.
2. Map the trust boundaries and entry points, then check input handling, authentication, authorization (object and function level), session/token handling, secrets, dependencies, and error/log hygiene.
3. Run available static tools if installed (semgrep, bandit, npm audit, gitleaks) and read the results critically; discard false positives.
4. Report each finding with: location (`file:line`), what is wrong, realistic impact, a concrete fix, and a regression test to add. Order by severity.

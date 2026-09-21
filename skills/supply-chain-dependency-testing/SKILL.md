---
name: supply-chain-dependency-testing
description: Use when testing software supply-chain and dependency risk — SCA/vulnerability scanning (Trivy, Grype, OSV, Dependabot, npm audit), SBOM (CycloneDX/SPDX), license compliance, lockfile integrity, reachability triage, secrets scanning, CI hardening, and SLSA provenance/signing.
license: MIT
metadata:
  category: security
  version: "2.0"
  tags: sca, sbom, supply-chain, dependencies, cyclonedx, spdx, trivy, grype, osv, licenses, slsa, sigstore, secrets
---

# Supply-Chain & Dependency Testing

Most of the code you run is third-party. Test the *inputs* to your build as rigorously as your own code.

## 1. Know what you ship — SBOM
```bash
syft dir:. -o cyclonedx-json > sbom.cdx.json          # source tree
syft myimage:1.2.3 -o spdx-json > sbom.spdx.json      # container image
```
Store an SBOM per release; check it includes transitive and OS packages.

## 2. Scan for known vulnerabilities (SCA)
```bash
trivy fs --scanners vuln,secret,misconfig --severity HIGH,CRITICAL --exit-code 1 .
grype sbom:sbom.cdx.json --fail-on high
osv-scanner --lockfile=package-lock.json
npm audit --omit=dev --audit-level=high ; pip-audit -r requirements.txt ; govulncheck ./...
```
Automate updates with Dependabot or Renovate (grouped PRs; auto-merge patch updates when CI is green).

## 3. Triage without drowning
For every finding ask: is the vulnerable function **reachable**? Is it a prod or dev-only dependency? Is it known-exploited (CISA KEV) or high EPSS? Is a fixed version available? → fix now / schedule / record a VEX "not affected" with justification. Suggested SLAs: Critical + KEV 48 h, High 7–14 days.

## 4. Build-integrity checks
| Risk | Check |
| :--- | :--- |
| Dependency confusion | Reserve internal package names publicly; scope registries (`.npmrc` `@org:registry=`, single pip index) |
| Look-alike / malicious packages | Review new dependencies (maintainers, age, downloads, install scripts); allow-list registries |
| Lockfile drift | Commit lockfiles; CI uses `npm ci` / `pip install --require-hashes`; no floating `latest` |
| Install-time scripts | Prefer `--ignore-scripts` where feasible; review `postinstall` |
| Abandoned packages | Last release date, open security issues, maintainer count |
| CI/CD hardening | Pin Actions to commit SHAs; least-privilege `GITHUB_TOKEN`; no secrets to forked PRs; OIDC instead of long-lived cloud keys; run OpenSSF Scorecard |

## 5. Secrets
`gitleaks detect --redact` and `trufflehog git file://. --only-verified` in pre-commit and CI, plus push protection. If a secret leaks: **rotate first**, then purge history, then add a detection test.

## 6. Licenses
Use `license-checker`, `pip-licenses`, ScanCode or FOSSA with an allow/deny policy (copyleft in distributed proprietary code, source-available licenses), and generate a NOTICE file.

## 7. Provenance and signing
Reproducible builds, SLSA provenance (`slsa-github-generator`), sign artifacts and images (`cosign sign`), verify at deploy (`cosign verify`, Kyverno/Gatekeeper admission policy).

## Gate
Fail the build on: new Critical/High reachable vulnerability, detected secret, disallowed license, unpinned action, or missing SBOM. Publish SARIF/VEX for visibility.

## Related
`static-analysis-testing`, `iac-container-security-testing`, `cicd-testing`, `security-testing`, `compliance-testing`

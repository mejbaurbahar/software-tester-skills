---
name: security-testing
description: Use for authorized security/penetration testing of web apps and APIs — OWASP Top 10 checks, auth/session testing, header/config audits, and vulnerability triage. Only for systems the user owns or has explicit authorization to test.
license: MIT
metadata:
  category: security
  version: "2.0"
  tags: security-testing, owasp, session, auth-bypass, vulnerabilities
---

# Security Testing

> **Scope guardrail:** test only systems you own or have explicit written authorization to test (your product, client engagements, CTFs, in-scope bug bounties). Prefer staging with synthetic data. Do not run destructive payloads, denial-of-service, or mass scans of third-party infrastructure; propose a safe alternative instead.

## Approach
1. **Model threats first** (`threat-modeling`): assets, entry points, trust boundaries.
2. **Automate the cheap wins in CI**: static analysis (`static-analysis-testing`), dependency and secret scanning (`supply-chain-dependency-testing`), IaC/container checks (`iac-container-security-testing`).
3. **Test authentication and authorization deliberately** (`authn-authz-testing`); this is where the worst bugs live.
4. **Manually probe business logic**: automation cannot understand your rules.
5. **Report, fix, and add a regression test** for every finding.

## OWASP Top 10 quick-check pass
| Risk | What to check |
| :--- | :--- |
| **Broken access control** | Object IDs across users/tenants (IDOR), function-level checks (can a normal user call an admin route?), path traversal on file endpoints, forced browsing |
| **Cryptographic failures** | Secrets/PII in plaintext (logs, DB, responses), HTTPS everywhere + HSTS, weak/default credentials on new installs, sensitive data in URLs |
| **Injection** | SQL/NoSQL/OS/LDAP/template injection in **every** input incl. headers and filenames; use parameterized queries and output encoding |
| **Insecure design** | No rate limit on login/reset/OTP, business rules trusting client values (price, role), missing abuse-case handling |
| **Security misconfiguration** | Verbose errors/stack traces, default admin panels, directory listing, debug mode, open cloud storage, missing headers |
| **Vulnerable/outdated components** | Known-CVE libraries and plugins (SCA scan), unsupported runtimes |
| **Authentication failures** | Weak password policy, no lockout, session not rotated on login, tokens not invalidated on logout, predictable IDs, MFA gaps |
| **Software/data integrity** | Unsigned updates/webhooks, insecure deserialization, CI/CD exposure |
| **Logging & monitoring failures** | No audit trail for privileged actions, no alerting on repeated failures |
| **SSRF** | Any server-side "fetch this URL" feature (webhooks, image/PDF from URL) must block internal ranges and cloud metadata addresses |

## Fast header and cookie audit
```bash
curl -sI https://staging.example.com | grep -iE "strict-transport|content-security|x-content-type|x-frame|referrer-policy|permissions-policy|set-cookie|server|x-powered-by"
```
Expect: `Strict-Transport-Security`, a Content-Security-Policy that is strict yet does not break legitimate features, `X-Content-Type-Options: nosniff`, `frame-ancestors` or `X-Frame-Options`, `Referrer-Policy`; cookies `Secure; HttpOnly; SameSite`; no version banners.

## Session and account flows
Session ID changes after login (fixation) · logout invalidates the token **server-side** (replay the old token) · password-reset tokens are single-use, short-lived and not leaked via URL/referrer · MFA cannot be skipped via another endpoint · multi-tenant isolation on every read **and** write.

## Tools (use only on authorized targets)
| Purpose | Tools |
| :--- | :--- |
| Intercepting proxy, manual testing | Burp Suite, OWASP ZAP, mitmproxy |
| Automated baseline scan on staging | ZAP baseline/API scan, Nuclei templates |
| Static/secret/dependency scanning | Semgrep, CodeQL, gitleaks, Trivy, OSV-Scanner |
| TLS | `testssl.sh`, `sslyze` |
| API contract security | `42crunch-api-security-testing` |

## Triage and severity
Rate by real-world exploitability and impact, not only category: an unauthenticated IDOR leaking personal data is Critical; a missing header on a static marketing page is Minor. Reproduce, document minimal steps, and share findings through the private channel your team uses. Do not put working exploit chains in widely shared reports beyond what is needed to verify the fix. Use `bug-reporting`.

## Related
`security-owasp`, `security-hardening`, `authn-authz-testing`, `threat-modeling`, `static-analysis-testing`, `supply-chain-dependency-testing`, `compliance-testing`

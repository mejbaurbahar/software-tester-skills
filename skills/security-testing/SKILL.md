---
name: security-testing
description: Use for authorized security/penetration testing of web apps and APIs — OWASP Top 10 checks, auth/session testing, header/config audits, and vulnerability triage. Only for systems the user owns or has explicit authorization to test.
---

# Security Testing

**Scope guardrail**: only test systems the user owns, controls, or has explicit written authorization to test (client engagements, CTFs, bug bounty programs in scope). Refuse destructive testing (data-deleting payloads, DoS, mass scanning of third-party infra) even when asked — flag it and propose a safe alternative (staging environment, rate-limited scan).

## OWASP Top 10 quick-check pass
1. **Broken Access Control** — IDOR (increment/guess resource IDs across users/tenants), missing function-level auth checks (can a regular user hit an admin API route directly?), path traversal on file endpoints.
2. **Cryptographic Failures** — secrets/PII in plaintext (logs, DB columns, API responses), missing HTTPS/HSTS, weak/default credentials (this harness has flagged `admin/admin123` before — always check for default creds on new installs).
3. **Injection** — SQLi, NoSQLi, command injection, LDAP injection in every input, including headers and file names, not just visible form fields.
4. **Insecure Design** — missing rate limiting on auth/password-reset endpoints, business logic that trusts client-side values (price, discount, role sent from frontend).
5. **Security Misconfiguration** — verbose error pages/stack traces in production, default admin panels reachable, directory listing enabled, missing security headers.
6. **Vulnerable Components** — outdated JS libs/CMS plugins with known CVEs (check versions against CVE databases).
7. **Auth Failures** — weak password policy, no lockout/rate-limit on login, session tokens not invalidated on logout, predictable session IDs, missing MFA where expected.
8. **Software/Data Integrity** — unsigned/unverified auto-update or webhook payloads, CI/CD supply-chain exposure.
9. **Logging/Monitoring Failures** — no audit trail for privileged actions; can't tell if an account was compromised after the fact.
10. **SSRF** — any server-side "fetch this URL" feature (webhooks, image-from-URL, PDF-from-URL) tested with internal IPs / cloud metadata endpoints (`169.254.169.254`) to confirm it's blocked.

## Header audit (fast, always worth doing)
Check via `curl -sI <url>` or the network tab:
- `Content-Security-Policy` present and not so loose it defeats XSS protection (also verify it doesn't accidentally block legitimate app functionality like wp-admin — seen in this environment before).
- `Strict-Transport-Security`, `X-Content-Type-Options: nosniff`, `X-Frame-Options` or `frame-ancestors`, `Referrer-Policy`.
- Cookies: `Secure`, `HttpOnly`, `SameSite` set appropriately on session cookies.

## Auth/session testing
- Session fixation: does the session ID change after login?
- Logout: is the token actually invalidated server-side, or just cleared client-side (test by reusing the old token after logout)?
- Password reset: token single-use? expires? not leaked in URL logs/referrer headers?
- Multi-tenant isolation: authenticated as tenant A, attempt every read/write against tenant B's resource IDs.

## Tools in this harness
- HawkScan DAST (`hawkscan` skill) — after any meaningful code change, run the scan loop and fix findings before calling work done, per the autonomous-security policy already active this session.
- Semgrep Guardian is scanning files as they're written in this session already — treat its findings as an additional signal, not a replacement for manual review.
- `qa security` dispatcher command for the existing QA harness security skill.

## Triage and reporting
Rate severity by real-world impact and exploitability, not just OWASP category — an unauthenticated IDOR leaking PII is Blocker/Critical; a missing header on a static marketing page is Minor. Use [[bug-reporting]]'s format and never include a working exploit chain in a shared report beyond what's needed to reproduce internally.

---
name: authn-authz-testing
description: Use when testing authentication and authorization — login, MFA, OAuth2/OIDC, SAML, JWT, sessions/cookies, password reset, RBAC/ABAC, IDOR/BOLA, privilege escalation, multi-tenant isolation, and account-takeover paths.
license: MIT
metadata:
  category: security
  version: "2.0"
  tags: authentication, authorization, oauth2, oidc, jwt, rbac, idor, bola, mfa, session, multi-tenant
---

# Authentication & Authorization Testing

Auth is where most critical breaches live (OWASP A01 Broken Access Control, A07 Auth Failures, API1 BOLA). Test **who you are** (authn) and **what you may do** (authz) separately.

## Authentication matrix
| Area | Cases |
| :--- | :--- |
| Login | Valid/invalid; user-enumeration via message/timing/status; lockout & rate limit; credential stuffing; case/space/unicode normalization |
| Passwords | Min length (≥12), breached-password check, no truncation, strong hashing (argon2id/bcrypt), reset tokens single-use + short TTL + bound to user, reset doesn't leak account existence |
| MFA | Enforced for privileged; brute-force limits; bypass via alternate endpoint/`remember me`; recovery codes; SIM-swap resilience; step-up for sensitive actions |
| Sessions | New ID on login (fixation), `HttpOnly; Secure; SameSite`, idle + absolute timeout, logout invalidates server-side, concurrent sessions, revoke-all on password change |
| OAuth2/OIDC | `state` & PKCE enforced; exact `redirect_uri` match; `nonce`; code single use; scopes minimal; refresh-token rotation/reuse detection; ID-token `aud/iss/exp` validated |
| SAML/SSO | Signature wrapping, `Audience`, `InResponseTo`, replay, assertion expiry, JIT provisioning role mapping |
| API keys | Scoped, rotatable, hashed at rest, never in URLs/logs |

## JWT checklist
`alg:none` rejected · algorithm pinned (no RS→HS confusion) · signature verified · `exp/nbf/iat/aud/iss` checked · `kid` not injectable · short access-token TTL · tokens revocable · no secrets/PII in payload · key rotation works.
```bash
jwt_tool $TOKEN -T                      # tamper claims; -X a (alg none), -X k (key confusion)
echo $TOKEN | cut -d. -f2 | base64 -d   # inspect claims
```

## Authorization testing — the role × resource × action grid
1. List **roles** (anon, user, admin, support, tenant-admin), **resources**, **actions** (CRUD + export, share, impersonate).
2. For each cell: expected allow/deny. Automate with two+ accounts.
3. **Horizontal**: user A requests user B's object by ID (`/orders/123`, `?user_id=`, GraphQL node id, file paths, UUIDs are *not* security). → expect 403/404.
4. **Vertical**: low-priv token calls admin endpoints, hidden UI actions, `PUT role=admin` mass-assignment, HTTP method swap (`GET`→`DELETE`), header tricks (`X-Original-URL`, `X-HTTP-Method-Override`).
5. **Function-level (BFLA)**: every API route, incl. undocumented (diff OpenAPI vs proxy logs).
6. **Multi-tenant**: tenant-ID in JWT vs path vs body — tamper each; bulk/export/search/cache/queue/webhook paths often forget tenancy.
7. **Indirect**: forced browsing, presigned URL reuse, cached responses served across users (`Vary`, CDN), stale permissions after role change/user removal.

```python
# BOLA probe — same request as A vs B
for rid in a_resource_ids:
    r = s_b.get(f"{API}/orders/{rid}")
    assert r.status_code in (403, 404), (rid, r.status_code)
```
Burp: Autorize / AuthMatrix extensions; ZAP access-control scripts; Postman collection run per role.

## Reporting
Show request/response for both principals, the missing check, impact (data/actions exposed), CVSS, and fix (centralized policy: deny-by-default, object-level check in data layer, tests per role).

## Related
`security-testing`, `api-testing`, `42crunch-api-security-testing`, `threat-modeling`

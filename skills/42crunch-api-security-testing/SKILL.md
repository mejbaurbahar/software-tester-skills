---
name: 42crunch-api-security-testing
description: Use when auditing, scanning, or remediating OpenAPI/Swagger API definitions for security vulnerabilities — 42Crunch audit scoring, OWASP API Security Top 10 compliance, BOLA/BFLA prevention, schema strictness, and shift-left API CI/CD testing.
license: MIT
metadata:
  category: security
  version: "2.0"
  tags: openapi, api-security, owasp-api, 42crunch, shift-left
---

# 42Crunch API Security Testing

## Overview
42Crunch provides automated, contract-driven API security testing. It enforces security at the OpenAPI/Swagger definition layer and verifies live implementation conformance, enabling an automated **Audit -> Scan -> Remediate -> Validate** cycle directly within AI-assisted developer workflows.

---

## The Continuous API Security Loop

```
      ┌───────────────┐
      │  1. AUDIT     │  Static contract analysis of OpenAPI / Swagger specs
      └───────┬───────┘
              ▼
      ┌───────────────┐
      │  2. SCAN      │  Dynamic conformance scanning of active endpoints
      └───────┬───────┘
              ▼
      ┌───────────────┐
      │ 3. REMEDIATE  │  Propose exact contract & code fixes (BOLA, schemas)
      └───────┬───────┘
              ▼
      ┌───────────────┐
      │ 4. VALIDATE   │  Re-audit to verify score meets threshold (>85/100)
      └───────────────┘
```

---

## 1. OpenAPI Security Audit Criteria (Scoring 0–100)

A high 42Crunch audit score requires comprehensive, strict contract definitions:

### Authentication & Authorization
- Every endpoint (except explicit public endpoints like login/register) must define a `security` requirement.
- Global security definitions must declare granular scopes (e.g. `read:users`, `write:orders`).
- Unauthenticated endpoints must explicitly set `security: []` with documented rationale.

### Strict Schema Definition & Input Constraints
- **Strings**: Must specify `maxLength` and where applicable a restrictive `pattern` (regex) or `format` (e.g., `uuid`, `email`, `uri`).
- **Numbers/Integers**: Must specify `minimum` and `maximum` boundaries to prevent integer overflows or resource exhaustion.
- **Arrays**: Must specify `maxItems` and `minItems` to prevent unbounded payload attacks (DoS).
- **Objects**: Must specify `additionalProperties: false` to mitigate Mass Assignment vulnerabilities.
- **Enums**: Restrict input values to known permitted sets rather than arbitrary strings.

### Response Contracts
- Explicit definitions for all HTTP response codes:
  - `200` / `201` / `204` with strict output schemas.
  - `400 Bad Request` with standardized validation error schema.
  - `401 Unauthorized` & `403 Forbidden` for auth failures.
  - `404 Not Found` for resource lookups.
  - `429 Too Many Requests` with rate limit headers.
  - `500 Internal Server Error` with generic, non-leaking error responses (never stack traces).

---

## 2. OWASP API Security Top 10 (2023) Mapping

| Risk | Name | 42Crunch Verification Rule |
| :--- | :--- | :--- |
| **API1** | **BOLA (Broken Object Level Authorization)** | Enforce path parameter format (e.g. `uuid` pattern), verify auth tokens on object IDs, assert tenant isolation. |
| **API2** | **Broken Authentication** | Flag weak schemes (e.g. Basic Auth over HTTP); require OAuth2/Bearer JWT with expiration; rate limit login endpoints. |
| **API3** | **Broken Object Property Level Auth** | Prevent Mass Assignment by enforcing `additionalProperties: false` on request bodies and filtering sensitive attributes (e.g. `role`, `isAdmin`) from response schemas. |
| **API4** | **Unrestricted Resource Consumption** | Mandate `maxLength`, `maxItems`, pagination query parameters (`limit` with max boundary), and `429` rate limiting contracts. |
| **API5** | **BFLA (Broken Function Level Auth)** | Enforce strict role/scope requirements on administrative endpoints (e.g., `/admin/*` requires `admin` scope). |
| **API6** | **Unrestricted Sensitive Business Flows** | Identify high-frequency critical endpoints (e.g. checkout, coupon-redeem, password-reset) requiring CAPTCHA or velocity throttling. |
| **API7** | **Server-Side Request Forgery (SSRF)** | Restrict URL/webhook parameter schemas with strict regex patterns; disallow loopback/internal CIDR ranges. |
| **API8** | **Security Misconfiguration** | Disallow wildcard CORS (`*`), mandate HTTPS-only server URLs, remove detailed stack traces from `5xx` schemas. |
| **API9** | **Improper Inventory Management** | Flag undocumented/deprecated API versions; enforce API version prefixes (`/v1/`, `/v2/`); remove debug endpoints. |
| **API10** | **Unsafe Consumption of APIs** | Validate responses from third-party integrations with strict schema filters before internal processing. |

---

## 3. Remediation Patterns (Before vs. After)

### Example 1: Preventing Mass Assignment & Unbounded Strings

#### ❌ Vulnerable Spec (Audit Score: ~35/100)
```yaml
paths:
  /users:
    post:
      summary: Create user
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                username:
                  type: string
                email:
                  type: string
                role:
                  type: string
```

#### ✅ Remediated Spec (Audit Score: ~95/100)
```yaml
paths:
  /users:
    post:
      summary: Create user
      security:
        - BearerAuth: ["users:create"]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              additionalProperties: false
              required:
                - username
                - email
              properties:
                username:
                  type: string
                  minLength: 3
                  maxLength: 30
                  pattern: '^[a-zA-Z0-9_-]+$'
                email:
                  type: string
                  format: email
                  maxLength: 255
      responses:
        '201':
          description: User created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserResponse'
        '400':
          $ref: '#/components/responses/400BadRequest'
        '401':
          $ref: '#/components/responses/401Unauthorized'
```

---

## 4. Automation & CI/CD Shift-Left

### GitHub Actions Integration
```yaml
name: 42Crunch API Security Audit

on:
  push:
    paths:
      - '**/openapi.yaml'
      - '**/openapi.json'
  pull_request:

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: 42Crunch API Security Audit
        uses: 42Crunch/api-security-audit-action@v3
        with:
          api-token: ${{ secrets.SECURITY_API_TOKEN }}
          min-score: 85
```

### CLI Quick Audit
When 42Crunch CLI (`42c`) or VS Code extension is installed:
```bash
# Run local contract audit
42c audit openapi.yaml --min-score 85

# Conformance scan against live test server
42c scan openapi.yaml --target http://localhost:8080
```

---

## 5. Review Checklist for Agents
When reviewing or authoring an API contract:
1. [ ] Is `security` defined at root and per-endpoint?
2. [ ] Does every string have `maxLength` and a `pattern` or `format`?
3. [ ] Does every numeric value have `minimum` and `maximum`?
4. [ ] Does every array have `maxItems`?
5. [ ] Is `additionalProperties: false` set on all request payload schemas?
6. [ ] Are all error status codes (`400`, `401`, `403`, `404`, `429`, `500`) documented with schemas?
7. [ ] Are internal/admin paths guarded by distinct role scopes?
8. [ ] Has the audit score achieved ≥ 85/100?

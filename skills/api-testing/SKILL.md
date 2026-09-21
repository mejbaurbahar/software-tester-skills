---
name: api-testing
description: Use when testing REST/GraphQL APIs directly — status codes, schema/contract validation, auth, pagination, rate limits, idempotency, and error responses. Use instead of driving the UI when the question is really about the API layer.
license: MIT
metadata:
  category: api-backend
  version: "2.0"
  tags: rest, api, contract, status-codes, pagination, idempotency
---

# API Testing

## Why test at the API layer
Faster, more deterministic and more precise than UI tests, and it catches what a UI can hide (a UI may swallow a 500 and show cached data). Always cross-check a UI-observed bug against the raw API response before filing: it tells you whether the fault is frontend or backend.

## Per-endpoint checklist
| Area | What to verify |
| :--- | :--- |
| **Status codes** | Right code for success (200/201/204), client error (400/401/403/404/409/415/422/429), server error (5xx). A `200` carrying an error body is an anti-pattern to flag. |
| **Response schema** | Types, required fields, enums, formats; no leaked internals (password hashes, internal IDs, stack traces); consistent null vs missing. |
| **Request validation** | Missing/extra/wrong-type fields, malformed JSON, oversized bodies, wrong `Content-Type`, unicode/emoji, boundary values (`test-design-techniques`). Must reject cleanly (4xx), never 500. |
| **Auth** | No token → 401; wrong role → 403; expired/invalid token → 401 with a clear error; another user's or tenant's object → 403/404 (`authn-authz-testing`). |
| **Pagination/sorting/filtering** | First, last and out-of-range page; size 0/negative/huge; stable ordering (no duplicates/skips while data changes); cursor validity; total counts. |
| **Idempotency & retries** | Repeating POST/PUT/DELETE: `Idempotency-Key` honored, no duplicate orders/payments; PUT/DELETE truly idempotent. |
| **Concurrency** | Parallel updates → conflict detection (`ETag`/`If-Match`, version field), no lost updates (`concurrency-race-condition-testing`). |
| **Caching & conditional requests** | `ETag`/`Last-Modified`, `304`, `Cache-Control`, `Vary`; private data never cacheable by shared caches. |
| **Rate limiting** | `429` + `Retry-After`; limits per user/IP/key; limits not bypassable by header tricks. |
| **Errors** | One consistent error shape across endpoints, ideally RFC 9457 `application/problem+json`; correlation/request ID present; no internals leaked. |
| **Versioning & compatibility** | Old clients keep working; deprecations announced with `Deprecation`/`Sunset` headers. |
| **Headers & transport** | CORS (allowed origins are explicit), security headers, TLS, `Content-Type` charset, compression. |
| **Files/binary** | Upload size/type limits, virus-scan hook, streaming download, range requests. |
| **Webhooks/callbacks** | Signature verification, retries, duplicates, out-of-order events (`event-driven-messaging-testing`). |

## Contract and schema validation
Validate responses against the OpenAPI/JSON Schema/GraphQL schema **programmatically**, not by eyeballing JSON. Drift between documentation and behavior is a bug even when "the API works". Consumer-driven contracts: `contract-testing`. Spec-driven fuzzing finds crashes and violations automatically:
```bash
schemathesis run https://staging.example.com/openapi.json --checks all --hypothesis-max-examples=100
dredd openapi.yaml https://staging.example.com          # example-based contract run
```

## Tooling (pick what fits the stack)
| Need | Tools |
| :--- | :--- |
| Quick manual probes | `curl -i`, `httpie`, Postman, Bruno, Insomnia, VS Code REST Client |
| Scripted suites | `pytest` + `requests`/`httpx`, Jest/Vitest + `supertest`, REST Assured (Java), Playwright `request`, Karate, Hurl |
| Collections in CI | Newman (Postman), Bruno CLI, Hurl |
| Mocks/stubs | WireMock, MockServer, MSW, Prism (from OpenAPI) |
| Traffic capture | Browser DevTools network tab, `mitmproxy`, proxy logs |
```bash
curl -sS -i -X POST "$API/orders" -H "Authorization: Bearer $TOKEN" -H "Idempotency-Key: $(uuidgen)" \
  -H 'Content-Type: application/json' -d '{"sku":"A-1","qty":2}'
hurl --test --variable host=$API orders.hurl
```
```python
# pytest: auth matrix as parametrized data
@pytest.mark.parametrize("token,expected", [(None,401), ("expired",401), ("user",403), ("admin",200)])
def test_admin_endpoint_access(client, tokens, token, expected):
    r = client.get("/admin/reports", headers=auth(tokens.get(token)))
    assert r.status_code == expected
```

## Security-adjacent checks (depth in `security-testing`)
Object-level authorization by changing IDs · mass assignment (`"role":"admin"` in a body is ignored/rejected) · injection through every string field, header and filename · SSRF on any "fetch this URL" feature · excessive data exposure (fields the client never needs) · verbose errors.

## Performance sanity
Record p50/p95 latency per endpoint in the suite and fail on regressions beyond a threshold; deeper work in `performance-testing`.

## Reporting
Include the exact request (method, URL, relevant headers, body) and the full response, plus environment and timestamp. "The API is broken" without the request/response pair is not actionable. Format: `bug-reporting`.

## Related
`contract-testing`, `graphql-testing`, `authn-authz-testing`, `integration-testing`, `security-testing`, `bug-reporting`

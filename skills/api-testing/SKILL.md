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
Faster, more deterministic, and catches issues the UI might mask (a UI can silently swallow a 500 and show stale cached data). Always cross-check UI-observed bugs against the raw API response before filing — it tells you whether the bug is frontend or backend.

## Core checklist per endpoint
- **Status codes**: correct code for success (200/201/204), client error (400/401/403/404/409/422), server error (500). A 200 with an error body in it is a common anti-pattern to flag.
- **Response schema**: matches documented/expected shape — types, required fields present, no leaked internal fields (password hashes, internal IDs meant to be opaque).
- **Request validation**: missing required fields, wrong types, extra unexpected fields, malformed JSON — server should reject cleanly, not 500.
- **Auth**: no token → 401; wrong-role token → 403; expired token → 401 with clear error, not a silent empty response; token for another tenant/user → must not leak cross-tenant data (test this explicitly, it's a common critical bug).
- **Pagination**: first page, last page, page beyond range, page size 0/negative/huge, consistent ordering across pages (no duplicate/skipped records from concurrent writes).
- **Idempotency**: does retrying a POST (e.g. payment, order-create) create duplicates? Idempotency-key support if documented.
- **Rate limiting**: does exceeding the limit return 429 with a sane `Retry-After`, or does it just fail unpredictably?
- **Error response consistency**: same shape/format for errors across endpoints (don't want one endpoint returning `{error: "..."}` and another a bare string).

## Contract/schema validation
- If an OpenAPI/GraphQL schema exists, validate responses against it programmatically rather than eyeballing JSON.
- Flag drift between documented contract and actual behavior — that's a bug even if "the API works."

## Tools available in this harness
- `requests` in the qa-agent venv for scripted checks; `curl -i` for quick one-offs (the `-i` shows headers, useful for auth/cache header checks).
- Claude in Chrome / Chrome DevTools MCP `list_network_requests` / `get_network_request` to capture real requests the frontend makes, then replay/modify them directly.
- Postman MCP tools (`mcp__claude_ai_Postman__*`) when a collection already exists or is worth building for the project — generate one from observed traffic when useful.

## Security-adjacent checks (see [[security-testing]] for depth)
- IDOR: increment/guess another user's resource ID, confirm access is denied.
- Mass assignment: send extra fields in a request body (e.g. `"role": "admin"`) and confirm the server ignores/rejects rather than applying them.
- Injection: SQL/NoSQL/command-injection payloads in every string input, not just search boxes.

## Reporting
Include the exact request (method, URL, headers if relevant, body) and full response in bug reports — see [[bug-reporting]]. "The API is broken" without the request/response pair is not actionable.

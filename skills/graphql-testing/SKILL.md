---
name: graphql-testing
description: Use when testing GraphQL APIs — queries, mutations, subscriptions, schema validation and breaking-change detection, N+1 queries, depth/complexity limits, introspection exposure, authorization per field, batching abuse, and federation contracts.
license: MIT
metadata:
  category: api-backend
  version: "2.0"
  tags: graphql, apollo, schema, n+1, federation, introspection, authorization, subscriptions
---

# GraphQL Testing

GraphQL moves risk from URLs to **schema + resolvers**: one endpoint, client-defined queries, per-field auth.

## Test layers
1. **Schema**: lint & diff for breaking changes — `graphql-inspector diff old.graphql new.graphql`, `rover subgraph check` (federation), `graphql-schema-linter`.
2. **Resolver units**: call resolvers with mocked context/dataloaders.
3. **Operation tests** against a running server (in-memory `executeOperation` or HTTP).
4. **Contract**: persisted queries/operations used by real clients must still validate against the new schema (`graphql-inspector validate 'src/**/*.graphql' schema.graphql`).
5. **Non-functional**: complexity, depth, rate limits, N+1, latency.

## Operation tests
```ts
const res = await server.executeOperation({
  query: `query($id: ID!){ order(id:$id){ id total items{ sku qty } } }`,
  variables: { id: "A-991" } }, { contextValue: ctxFor("alice") });
expect(res.body.singleResult.errors).toBeUndefined();
```
```bash
curl -s $URL/graphql -H 'content-type: application/json' -H "authorization: Bearer $T" \
 -d '{"query":"{ __typename }"}'
```
Cover: nullability (`!` fields returning null bubbles up), partial errors (`data` + `errors`), input validation/coercion, enums & custom scalars, pagination (Relay cursors: first/after, stable ordering, empty page), mutations return payload + `userErrors`, idempotency, subscriptions (connect, auth on connect, reconnect, ordering, unsubscribe leak).

## Security & abuse checklist
| Risk | Test |
| :--- | :--- |
| Introspection in prod | `{__schema{types{name}}}` should be disabled/restricted |
| Depth/complexity DoS | Deeply nested & aliased queries must be rejected (`depthLimit`, cost analysis) |
| Batching/alias abuse | 1000 aliases of `login` → rate-limited (brute force bypass) |
| Field-level authz (BOLA) | User A queries `user(id: B){ email }` → denied |
| Mass assignment | Extra input fields ignored/rejected |
| Injection | SQL/NoSQL via arguments; SSRF via URL args |
| Verbose errors | No stack traces / SQL in `errors[].extensions` |
| CSRF on GET/multipart | Content-type enforcement |
Tools: `graphql-cop`, `InQL`, `clairvoyance` (schema recovery when introspection is off), Escape/StackHawk scanners.

## Performance
Detect N+1: count DB queries per request (log/APM), require DataLoader batching; test large lists & fan-out; measure p95 by operation name (persisted-query ID).

## Related
`api-testing`, `contract-testing`, `security-testing`, `microservices-testing`, `performance-testing`

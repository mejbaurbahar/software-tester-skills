---
name: microservices-testing
description: Use when designing a test strategy for microservices or distributed systems — service/component tests, consumer-driven contracts, service virtualization, testing in production, sagas and distributed transactions, cross-service E2E minimization, and the test honeycomb.
license: MIT
metadata:
  category: api-backend
  version: "2.0"
  tags: microservices, honeycomb, service-virtualization, saga, distributed-systems, testing-in-production
---

# Microservices Testing

Distributed systems shift bugs from *inside* components to *between* them. Favor the **honeycomb**: few unit, **many integration/contract**, very few E2E.

## Layers
| Layer | Scope | Tooling |
| :--- | :--- | :--- |
| Unit | Domain logic in one service | `unit-testing` |
| **Component** | One service, real DB/cache (Testcontainers), *stubbed* peers | WireMock, MockServer, MSW, Testcontainers |
| **Contract** | Consumer expectations ↔ provider | Pact, Spring Cloud Contract (`contract-testing`) |
| Integration | 2–3 real services in a compose/k8s namespace | docker compose, kind/k3d, Tilt |
| E2E | Critical user journeys only (≤10) | Playwright/Cypress on staging |
| Production | Canary, synthetic probes, feature flags | `production-monitoring-synthetic-testing` |

## Component test recipe
```yaml
# docker-compose.test.yml
services:
  orders: { build: ., depends_on: [pg, payments-stub] }
  pg: { image: postgres:16 }
  payments-stub: { image: wiremock/wiremock, volumes: ["./stubs:/home/wiremock"] }
```
Stub not only success: **timeouts, 500s, slow responses (fault delay), malformed JSON, connection reset**. Assert timeouts, retries with backoff+jitter, circuit-breaker open/half-open, fallback behavior, bulkheads.

## Distributed-transaction (saga) testing
Enumerate each step's failure → verify compensation runs, is idempotent, and final state is consistent. Test compensation *failing*. Test out-of-order and duplicate events. Verify orchestrator restart mid-saga resumes.

## Cross-cutting checks
- **API versioning**: N and N-1 clients against N provider; deprecate with telemetry.
- **Observability**: trace ID propagates across all hops (`traceparent`); one test asserts a request produces a connected trace (`observability-testing`).
- **Auth propagation**: service-to-service tokens/mTLS; confused-deputy (service acts with user's rights only).
- **Config & secrets**: missing env var → fail fast at boot; readiness vs liveness probes.
- **Data ownership**: no shared DB; tests must not read other services' tables.
- **Deployment**: rolling update with in-flight requests; schema migration backward-compatible (expand/contract).

## Anti-patterns
Giant shared staging environment as the only integration test · E2E for every rule · mocking the DB you own · no timeouts in client calls · testing only happy paths between services.

## Related
`contract-testing`, `event-driven-messaging-testing`, `chaos-resilience-testing`, `integration-testing`, `cloud-infrastructure-testing`

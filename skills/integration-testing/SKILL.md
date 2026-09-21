---
name: integration-testing
description: Use when verifying interactions between multiple components, modules, or services — API-to-database persistence, message queues, external service adapters, and Testcontainers.
license: MIT
metadata:
  category: code-level
  version: "2.0"
  tags: integration, testcontainers, persistence, queues, adapters
---

# Integration Testing

Integration tests verify that independently built pieces (modules, services, databases, queues, third-party adapters) **work together across their real interfaces**. They find the bugs unit tests structurally cannot: wrong SQL, serialization mismatches, misconfigured clients, transaction and timeout behavior.

## Scope
| Kind | What runs for real | What is faked |
| :--- | :--- | :--- |
| **Narrow** | One service + its real datastore/cache/queue (Testcontainers) | Other services (stubbed at HTTP level) |
| **Broad / service** | Several services in compose/k8s | Only external third parties |
| **Contract** | Consumer vs provider expectations | Both sides verified independently (`contract-testing`) |
Prefer many narrow tests plus contracts and a few broad ones (`microservices-testing`).

## Core checklist
1. **Persistence & transactions:** full CRUD against the **same engine and version as production** (no in-memory substitute for a different SQL dialect); migrations apply cleanly on an empty and on a populated database; rollback on failure leaves no partial writes; constraints, unique keys, cascades; concurrent transactions and pool behavior (`concurrency-race-condition-testing`).
2. **Messaging:** publish/consume, serialization and schema compatibility, idempotent consumers, retries, DLQ routing, ordering assumptions (`event-driven-messaging-testing`).
3. **HTTP clients and adapters:** timeouts, retries with backoff and jitter, circuit-breaker open/half-open, handling of 4xx/5xx/slow/malformed/empty responses, auth token refresh. Stub servers: WireMock, MockServer, MSW, Prism.
4. **Configuration wiring:** the real DI container/app context boots; env vars and secrets resolve; health/readiness endpoints report dependency status.
5. **Security boundaries:** authorization enforced at the service and data layer, not just in the controller.
6. **Time and files:** scheduled jobs (fake clock), file storage, temp directories, object storage (MinIO/LocalStack).

## Environment and fixtures
```java
// JUnit 5 + Testcontainers (real Postgres, same major version as prod)
@Testcontainers class OrderRepoIT {
  @Container static PostgreSQLContainer<?> pg = new PostgreSQLContainer<>("postgres:16");
  @Test void persistsAndReadsBack() { /* run migrations, insert via repo, query via JDBC, assert */ }
}
```
```python
# pytest + testcontainers
@pytest.fixture(scope="session")
def db():
    with PostgresContainer("postgres:16") as pg:
        run_migrations(pg.get_connection_url()); yield pg
```
```bash
docker compose -f docker-compose.test.yml up -d --wait && pytest -m integration && docker compose down -v
```
- **Cleanup strategy:** wrap each test in a transaction and roll back, or truncate touched tables, or use a template database per worker. Never drop/recreate schema per test.
- **Isolation:** unique IDs per test, no dependence on execution order, parallel-safe.
- **Determinism:** pin image versions/digests; wait on health checks, not sleeps; poll-until with timeout for async effects.

## Strategies for integrating many parts
Big-bang (avoid) · top-down with stubs · bottom-up with drivers · sandwich · **incremental by risk**: integrate the riskiest boundary first (payments, auth, data migration).

## Anti-patterns
Shared mutable state between tests · running against a shared staging environment where concurrent writes cause flakiness · asserting on internals rather than observable results · mocking the database you own · slow suites with no tiering (tag and run them in a separate CI stage) · ignoring failure modes (timeouts, partial failures).

## Related
`unit-testing`, `contract-testing`, `database-testing`, `microservices-testing`, `test-environment-management`, `api-testing`

---
name: contract-testing
description: Use when testing integrations between services — consumer-driven contracts, microservice boundaries, event/message-queue testing (Kafka, webhooks), schema evolution, and backward compatibility between independently-deployed services.
license: MIT
metadata:
  category: api-backend
  version: "2.0"
  tags: pact, consumer-driven-contracts, microservices, schema
---

# Contract & Integration Testing

## The problem this solves
In a microservice/event-driven system, full E2E tests across every service are slow, flaky, and don't tell you *which* service broke the contract. Contract testing verifies each service's boundary in isolation against an agreed contract, so integration bugs are caught at PR time in the offending service, not in a shared staging environment days later.

## Consumer-driven contract testing (Pact-style)
1. **Consumer** (the caller) writes a test defining what it expects from the provider's response — this generates a contract file.
2. Contract is published to a broker (or shared repo).
3. **Provider** (the API) verifies it can satisfy every consumer's contract, run in the provider's own CI — this catches breaking changes before the provider ships them, not after the consumer breaks in production.
4. Any provider change that breaks a published contract fails provider CI immediately — this is the entire point: shifting integration-break detection left to the provider's own pipeline.

## What to actually test at the boundary
- **Schema shape**: required fields present, types correct, no undocumented breaking removal of a field a consumer depends on.
- **Backward compatibility**: additive changes (new optional field) are safe; renaming/removing/retyping a field consumers use is breaking — verify old consumers still function against the new provider version during a rolling deploy window.
- **Versioning strategy**: URL versioning (`/v2/...`), header versioning, or field-level deprecation — confirm the documented strategy is actually enforced, not just aspirational.
- **Error contract**: error response shape is also part of the contract — a provider that changes error format silently breaks consumer error-handling code.

## Event-driven / message-queue testing (Kafka, SQS, webhooks)
- **Schema validation** on both produce and consume side — a producer emitting a malformed event should fail fast, not silently corrupt downstream consumers.
- **Ordering guarantees**: if the system claims ordered delivery (e.g. per-partition-key in Kafka), test with rapid same-key events and confirm order is preserved; if it doesn't guarantee ordering, confirm consumers are actually idempotent/order-tolerant rather than assuming.
- **At-least-once delivery**: consumers must handle duplicate delivery — test by replaying an event and confirming no duplicate side effect (double-charge, duplicate row).
- **Dead-letter handling**: a poison message (malformed, or one that always throws) shouldn't block the whole partition/queue — confirm it lands in a DLQ and is observable, not silently dropped or infinitely retried.
- **Webhooks specifically**: signature verification (HMAC) is enforced, retry-with-backoff on receiver 5xx, and the receiver is idempotent against webhook redelivery (most providers redeliver on any non-2xx, including if the receiver *did* process it but returned a bad status).

## Schema evolution checklist
- Additive-only changes for a non-breaking release: new optional fields, new enum values (if consumers are required to handle unknown enum values gracefully — verify they actually do, don't just assume).
- Any field removal/rename/retype/required-ification is breaking — requires a deprecation window and consumer migration, not a same-day ship.
- For GraphQL: deprecated fields marked with `@deprecated` and still functional until the documented removal date; consumers not silently broken by schema changes because GraphQL clients typically request only the fields they use — verify this isolation actually holds for the specific client library in use.

## Tools
- **Pact** — consumer-driven contract testing, broker-based verification, both sides run in CI.
- **Schemathesis** — property-based testing directly from an OpenAPI/GraphQL schema, generates edge-case requests automatically.
- **Dredd** — validates an API implementation against its OpenAPI/API Blueprint spec.

## Reporting
When a contract breaks, identify which side changed (consumer expectation vs. provider behavior) and whether it's a legitimate breaking change that needs a version bump, or an accidental regression — see [[bug-reporting]] and [[api-testing]].

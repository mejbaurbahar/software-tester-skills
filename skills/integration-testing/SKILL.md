---
name: integration-testing
description: Use when verifying interactions between multiple components, modules, or services — API-to-database persistence, message queues, external service adapters, and Testcontainers.
---

# Integration Testing

## Overview
Integration testing verifies that independently developed modules, services, databases, and third-party adapters communicate and function together correctly according to interface specifications.

## Scope & Boundaries
- **Narrow Integration**: Verifies a single service integrated with real persistence or caching (e.g., Service + PostgreSQL, Repository + Redis) using ephemeral test containers.
- **Broad Integration**: Verifies cross-service flows across microservice boundaries, queues (Kafka/RabbitMQ), and external gateways.

## Core Checklist
1. **Data Persistence & Transactions**:
   - Verify complete CRUD cycles against real database instances (ephemeral Testcontainers, not in-memory substitutes).
   - Test transaction rollbacks on failure to guarantee atomic operations.
   - Verify connection pool behavior under concurrent transactions.
2. **Message Queues & Event Handlers**:
   - Verify message publishing, serialization/deserialization, idempotency keys, and dead-letter queue (DLQ) routing.
3. **External Gateway Adapters**:
   - Validate HTTP client timeouts, exponential backoff, and retry handling using mock servers (WireMock, MSW, Prism).
   - Test circuit breaker triggers on consecutive upstream 5xx errors.

## Environment & Fixtures
- Use **Testcontainers** (Docker-based ephemeral containers) to spin up exact database, Redis, or Kafka versions matching production.
- **Database Cleanup Strategy**:
   - Preferred: Run each test inside a transaction and rollback at teardown.
   - Alternative: Fast truncation of touched tables between test suites. Never drop/recreate tables per test.

## Common Anti-Patterns
- **Shared Mutable State**: Tests relying on data seeded by previous tests. Each integration test must be self-contained and generate its own unique identifiers.
- **Testing Staging/Production Directly**: Running integration suites against shared staging environments where concurrent writes cause flaky assertions.

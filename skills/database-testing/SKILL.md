---
name: database-testing
description: Use when verifying data integrity, CRUD correctness at the persistence layer, migrations, transactions/concurrency, or query correctness/performance — SQL and NoSQL. Use whenever a bug claim needs to be confirmed against actual stored state, not just UI/API appearance.
license: MIT
metadata:
  category: data
  version: "2.0"
  tags: database, sql, acid, migrations, transactions, query-performance
---

# Database Testing

## Why this matters even if you're "just" a UI/API tester
The UI and API can both lie (cached, optimistic-UI, stale). The database is the source of truth. Before filing "data wasn't saved," check the actual row.

## Core checks
- **CRUD correctness**: create persists all fields with correct types/defaults; read returns exactly what was written (no silent truncation/encoding issues); update touches only intended fields (no accidental overwrite of untouched columns); delete behaves as documented (hard vs soft — check for a `deleted_at`/`is_deleted` column before assuming hard delete).
- **Constraints**: NOT NULL, UNIQUE, CHECK, foreign keys actually enforced — try to violate them directly (not just through the app) to confirm the DB itself protects integrity, not only application code.
- **Referential integrity**: deleting a parent — does it cascade, restrict, or orphan children? Verify it matches the intended business rule, not just "doesn't error."
- **Transactions**: multi-step operations either fully commit or fully roll back on failure — kill/interrupt mid-transaction (or simulate via a forced error) and confirm no partial state persists.
- **Concurrency**: two simultaneous writes to the same row — last-write-wins silently, or optimistic locking (version column) rejecting the stale write? Test with genuinely concurrent requests, not sequential ones with a sleep.
- **Deadlocks**: under concurrent load touching overlapping rows, does the DB/app handle a deadlock by retrying, or does it hang/500?
- **Index correctness**: a query that should use an index but does a full table scan is a latent performance bug — check with `EXPLAIN`/`EXPLAIN ANALYZE`.

## Migration testing
- Run the migration against a copy of **production-shaped data** (realistic volume and edge-case rows), not just an empty dev DB.
- Test the **rollback**, not just the forward migration — if it can't roll back cleanly, that's a deploy-risk finding worth flagging regardless of whether anyone asked.
- Check backward compatibility during a rolling deploy: old app code + new schema, and new app code + old schema, for the window where both coexist.
- For destructive migrations (dropping/renaming columns), confirm nothing else reads the old shape first (grep the codebase, check async workers/reporting jobs).

## ETL / data pipeline testing
- Row counts reconcile source → target (accounting for expected filters/dedup).
- Data-type and precision fidelity (decimals not silently truncated, timestamps not silently shifted by timezone assumptions).
- Idempotency — rerunning the same ETL batch shouldn't duplicate rows.
- Late-arriving / out-of-order data handled per the pipeline's documented ordering guarantee.

## NoSQL-specific considerations
- **MongoDB**: schema-less means the app enforces shape, not the DB — test documents missing expected fields, and documents from an older schema version still in the collection.
- **Redis**: TTL expiry behavior, eviction policy under memory pressure, atomicity of multi-key operations (use transactions/Lua where the app needs it).
- **DynamoDB**: partition-key hot-spotting under load, eventual- vs strong-consistency read behavior, GSI propagation lag.
- **Elasticsearch/OpenSearch**: index refresh delay (a write may not be immediately searchable — a common source of "flaky" test failures that are actually a real consistency window), mapping/analyzer correctness for search relevance.

## CLI / verification commands
- `psql`, `mysql`, `mongosh`, `redis-cli` for direct inspection.
- `EXPLAIN ANALYZE <query>` (Postgres/MySQL) to verify index usage and cost.
- Compare row counts/checksums across environments with a scripted diff rather than eyeballing.

## Reporting
Include the actual query/command used to verify state as evidence — see [[bug-reporting]]. "Data looks wrong in the UI" is not actionable; the query result that proves it is.

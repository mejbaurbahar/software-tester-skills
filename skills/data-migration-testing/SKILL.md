---
name: data-migration-testing
description: Use when testing database schema migrations, system replatforming, or data migrations between systems — pre/post reconciliation, zero-downtime expand/contract, rollback rehearsal, cutover plans, performance of backfills, and data lineage validation.
license: MIT
metadata:
  category: data
  version: "2.0"
  tags: data-migration, schema-migration, cutover, rollback, expand-contract, reconciliation, flyway, liquibase
---

# Data & Schema Migration Testing

Migrations are one-way doors with production data. **Rehearse on production-shaped data, prove reconciliation, and always have a tested rollback.**

## Plan → rehearse → cut over → verify
1. **Inventory & mapping**: source→target field map (type, transform, default, null rule); document lossy conversions & retired fields.
2. **Profile source**: row counts, null rates, distinct counts, min/max lengths, orphan FKs, duplicates, bad encodings. Fix or explicitly map anomalies *before* load.
3. **Rehearse ≥2 times** on a masked prod copy: measure duration, lock time, resource use; extrapolate to cutover window.
4. **Reconcile** (automated):
   - Counts per table/partition, sum/avg of numeric columns, min/max dates.
   - **Row-level hash** compare (`md5(concat_ws('|', cols))`) or sampled diff; keys present in one side only.
   - Referential integrity, unique constraints, sequences/identity next values.
   - Business checks (e.g., open invoices total, active users).
5. **Functional smoke** on migrated data through the real app (login, search, reports, exports, APIs).
6. **Rollback rehearsal**: restore/reverse and re-verify; know the point of no return.
7. **Cutover runbook** with owners, time-stamps, go/no-go gates, comms; freeze writes or use CDC to close the delta.
8. **Post-cutover**: monitor errors, slow queries, data-mismatch alerts; keep source read-only for N days.

## Zero-downtime schema changes (expand → migrate → contract)
| Step | Change | Safe? |
| :--- | :--- | :--- |
| Expand | add nullable column / new table / index `CONCURRENTLY` | yes |
| Dual-write | app writes old+new; backfill in batches | yes |
| Switch reads | flag to new column | yes (rollback = flag) |
| Contract | drop old column in a *later* release | after soak |
Test both **N and N-1 app versions** against the intermediate schema. Avoid: renaming columns in place, adding `NOT NULL` without default on large tables, long transactions.

## Tools
Flyway/Liquibase/Alembic/Prisma migrate (dry-run + checksum), `gh-ost`/`pt-online-schema-change` (MySQL), `pg_repack`, DMS/Debezium for CDC, `datafold`/`data-diff`:
```bash
data-diff postgres://old/db orders mysql://new/db orders -k id --columns amount,status
flyway -url=... validate && flyway migrate -dryRunOutput=plan.sql
```

## Edge data to seed
Emoji/Unicode/emoji-in-names, max-length strings, leading zeros, timezone-less timestamps, `NULL` vs empty string, negative/zero amounts, soft-deleted rows, orphaned children, duplicates, legacy enum values.

## Related
`database-testing`, `data-pipeline-etl-testing`, `compatibility-testing`, `disaster-recovery-backup-testing`, `release-readiness-testing`

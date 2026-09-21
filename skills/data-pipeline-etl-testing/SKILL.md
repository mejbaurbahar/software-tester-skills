---
name: data-pipeline-etl-testing
description: Use when testing ETL/ELT pipelines, data warehouses, dbt models, Spark/Airflow jobs, and analytics data quality — schema, row-count and checksum reconciliation, null/uniqueness/referential rules, freshness, SCD logic, Great Expectations/dbt tests, and idempotent reruns.
license: MIT
metadata:
  category: data
  version: "2.0"
  tags: etl, elt, data-quality, dbt, great-expectations, airflow, spark, reconciliation, data-warehouse
---

# Data Pipeline & ETL Testing

Data bugs are silent: dashboards look fine and are wrong. Test **data**, not just code.

## Test pyramid for data
1. **Unit** — transformation functions/SQL CTEs on tiny fixtures (pytest + pandas/Polars/Spark local, dbt unit tests).
2. **Schema/contract** — column names, types, nullability, enums; contract with upstream producers.
3. **Data quality (in-flight)** — assertions on each run.
4. **Reconciliation** — source vs target.
5. **Pipeline/integration** — DAG runs end to end on a sample.
6. **Monitoring** — freshness, volume, distribution drift in prod.

## Data-quality rules (dimensions)
| Dimension | Check |
| :--- | :--- |
| Completeness | `NOT NULL` critical columns; row counts vs source ±tolerance |
| Uniqueness | PK/natural key has no duplicates |
| Validity | Enums, regex, ranges, positive amounts |
| Consistency | Referential integrity; cross-table sums equal; currency/units uniform |
| Timeliness | `max(updated_at)` within SLA |
| Accuracy | Spot-check vs source of truth; reconcile aggregates |
| Distribution | Mean/stddev/null-rate drift vs baseline |

```yaml
# dbt schema.yml
models:
  - name: orders
    columns:
      - name: order_id
        tests: [unique, not_null]
      - name: customer_id
        tests: [{ relationships: { to: ref('customers'), field: customer_id } }]
      - name: status
        tests: [{ accepted_values: { values: [created, paid, shipped, cancelled] } }]
```
```python
# Great Expectations (fluent)
validator.expect_column_values_to_not_be_null("order_id")
validator.expect_column_values_to_be_between("amount", min_value=0)
```
```sql
-- reconciliation
SELECT (SELECT COUNT(*) FROM src.orders) - (SELECT COUNT(*) FROM dw.fact_orders) AS diff;
SELECT SUM(amount) FROM src.orders WHERE dt=:d EXCEPT SELECT SUM(amount) FROM dw.fact_orders WHERE dt=:d;
```

## Pipeline behavior tests
- **Idempotent reruns**: run twice → same result, no dupes (MERGE/upsert, partition overwrite).
- **Backfill** a range; late-arriving & out-of-order data; **SCD Type 2** effective-dating (no overlaps/gaps).
- Schema drift: new/removed/renamed upstream column → alert, not silent null.
- Failure: mid-load crash → atomic (no partial partition), resumable.
- Timezone & DST in partition keys; PII masked in lower environments (`test-data-engineering`).
- Performance: volume test at 10× rows; skew (hot keys); small-file problem.

Airflow: `DagBag` import test (no cycles/import errors), `airflow tasks test`, task-level idempotency.

## Related
`database-testing`, `data-migration-testing`, `test-data-engineering`, `observability-testing`

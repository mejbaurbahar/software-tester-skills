---
name: disaster-recovery-backup-testing
description: Use when validating backup, restore, high availability and disaster recovery — RTO/RPO verification, restore drills, region failover, data corruption and ransomware recovery, runbooks, game days, and backup integrity checks for databases and storage.
license: MIT
metadata:
  category: non-functional
  version: "2.0"
  tags: disaster-recovery, backup, restore, rto, rpo, failover, game-day, business-continuity, ransomware
---

# Disaster Recovery & Backup Testing

**A backup you have never restored is a hope, not a backup.** Test recovery against *stated objectives*.

## Define the targets first
- **RPO** (max tolerable data loss, e.g. 5 min) → sets backup/replication frequency.
- **RTO** (max downtime, e.g. 1 h) → sets automation and runbook needs.
- **MTD/priority tiers** per service (Tier 0: auth/payments … Tier 3: internal tools).

## Test ladder (do all, regularly)
| Level | Exercise | Frequency |
| :--- | :--- | :--- |
| 1. Backup integrity | Job success, size sanity, checksum, encryption, offsite/immutable copy exists | daily automated |
| 2. **Restore test** | Restore latest backup to isolated env; row counts/checksums; app boots and passes smoke | weekly/monthly automated |
| 3. Point-in-time recovery | Restore to `T-15 min` before a deliberate bad `DELETE`; verify | quarterly |
| 4. Component failover | Kill primary DB/cache/queue; replica promotes; app reconnects; measure RTO/RPO | quarterly |
| 5. Zone/region failover | Traffic shift, data replication lag, DNS TTL, secrets/KMS/IAM in DR region | 1–2× / yr |
| 6. **Game day** | Unannounced-ish full scenario incl. people, comms, access, runbook | 1–2× / yr |
| 7. Cyber recovery | Ransomware: restore from immutable/air-gapped copies into clean room | yearly |

## Restore verification script (sketch)
```bash
pg_restore -d restore_test latest.dump
psql restore_test -Atc "select count(*) from orders" # compare with prod snapshot
psql restore_test -Atc "select max(updated_at) from orders"   # RPO evidence
./smoke.sh https://restore-test.internal                        # app-level check
```
```bash
# Point-in-time (Postgres WAL)
recovery_target_time = '2026-09-21 14:05:00+00'  ; recovery_target_action='promote'
aws rds restore-db-instance-to-point-in-time --source-db-instance-identifier prod --target-db-instance-identifier drill --restore-time 2026-09-21T14:05:00Z
```

## What to verify beyond data
Secrets/KMS keys available in DR · IAM/roles · DNS/failover TTLs · TLS certs · third-party allowlists (IP changes) · config/flags · queues/streams offsets · search indexes & caches rebuilt · scheduled jobs not double-running · email/SMS callbacks · monitoring & alerting present in DR · on-call access without VPN dependency on the failed region · **runbook is accurate, step-by-step, and owned**.

## Failure scenarios to script
Accidental delete/`DROP` · corrupt migration · bad deploy (rollback) · AZ/region outage · credential compromise · ransomware · vendor outage (auth, payments, DNS) · expired cert · disk full · clock skew.

## Metrics & evidence
Measured RTO/RPO vs target, restore duration trend, backup success %, time to detect, time to decide, gaps found & closed; store evidence for audits (`compliance-testing`: SOC 2 A1.2, ISO 27001 A.8.13/A.5.30).

## Related
`chaos-resilience-testing`, `data-migration-testing`, `cloud-infrastructure-testing`, `observability-testing`, `release-readiness-testing`

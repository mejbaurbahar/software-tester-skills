---
name: compatibility-testing
description: Use when verifying software compatibility across environments, operating systems, database versions, backward/forward API compatibility, and migration rollback safety.
license: MIT
metadata:
  category: non-functional
  version: "2.0"
  tags: compatibility, backward-compatibility, upgrades, environments
---

# Compatibility & Migration Testing

## Overview
Compatibility testing ensures that software functions seamlessly across diverse hardware, operating systems, database engines, browser platforms, and third-party dependencies, as well as across version transitions.

## Key Testing Dimensions
1. **Backward & Forward Compatibility**:
   - Can client version N talk to server version N-1 and N+1?
   - Do existing client apps crash when new optional fields are added to API responses?
   - Are deprecated endpoints properly supported throughout the documented deprecation grace period?
2. **Database Schema Migrations & Rollback**:
   - Test `UP` migrations against populated databases (not empty schemas).
   - Test `DOWN` migrations (rollback) to ensure instant recovery without data corruption.
   - Verify non-locking migrations: schema changes (e.g. adding columns, indexes) must not lock production tables (`CONCURRENTLY` in Postgres).
3. **Runtime & Dependency Upgrades**:
   - Verify test suite passes when upgrading Node.js versions (e.g. Node 20 to 22), Python (3.11 to 3.12), or core frameworks.
   - Audit transitive dependency breaking changes via package locks.
4. **Data Export/Import Compatibility**:
   - Can data exported from version 1.0 be cleanly imported into version 2.0 without loss?

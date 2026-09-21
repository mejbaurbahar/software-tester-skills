---
name: test-data-engineering
description: Use when generating synthetic/realistic test data, seeding fixtures, masking PII for a test environment, or designing deterministic/reusable test datasets. Underpins reliable automation across all the other testing skills.
license: MIT
metadata:
  category: data
  version: "2.0"
  tags: test-data, fixtures, data-masking, seeding, synthetic-data
---

# Test Data Engineering

## Why this is its own discipline
Flaky and unreliable tests are very often a test-data problem, not a test-logic problem: shared mutable state, non-deterministic random values, or production data with unpredictable content. Good test data design is what makes [[test-automation]] and [[regression-testing]] actually reliable.

## Principles
- **Deterministic where it matters**: seed random generators explicitly so a failing test's exact input is reproducible — "it failed with some random string" is not debuggable; "it failed with seed 12345, input was X" is.
- **Isolated per test**: each test creates and owns its data (via API/factory, not shared fixtures mutated across tests) so tests can run in any order or in parallel without interfering.
- **Realistic shape, safe content**: production-like distributions (field lengths, null rates, unicode presence) without using real user data.
- **Boundary-aware**: generated data should include boundary/edge values deliberately (empty string, max length, unicode/emoji, negative numbers) — see [[manual-testing]]'s boundary value analysis — not just "random valid-looking" values, which tend to cluster in the safe middle of the input space and miss real bugs.

## Synthetic data generation
- Use a factory/builder pattern in code (e.g. Faker-style libraries) rather than hardcoded fixture files, so tests can override just the field under test and get sensible defaults for everything else.
- For load/performance testing, generate at realistic **volume** — a query that's fast against 100 rows can be catastrophically slow against 10M; see [[performance-testing]].
- For AI/ML and LLM evaluation, "golden dataset" design is its own careful process — see [[ai-ml-testing]] and [[llm-testing]] rather than generic random data.

## PII-safe test data (never use raw production data in lower environments)
- **Masking/anonymization**: replace real names/emails/PII with synthetic equivalents that preserve format and referential consistency (same person's email stays consistent across tables) but contain no real personal data.
- **Data subsetting**: pull a realistic-sized, referentially-consistent subset rather than a full production dump, both for safety and to keep lower environments fast/cheap.
- If a project currently copies raw production data into staging/dev, flag it as a real finding (privacy/compliance exposure) — this has come up as a genuine issue in this harness's own audits before, not a hypothetical.

## Seeding & fixtures
- Prefer **API-driven seeding** (call the app's own create endpoints) over direct DB inserts where feasible — it exercises the same validation path production traffic does and won't silently drift from the real schema/business rules.
- Version-control seed scripts alongside the schema/migrations they depend on.
- Provide a **reset-to-known-state** mechanism (truncate + reseed, or transactional rollback per test) so test runs don't accumulate drift over time.

## Cleanup strategies
- Transactional tests (wrap each test in a DB transaction, roll back after) are fastest and cleanest when the stack supports it.
- Otherwise, explicit teardown deleting exactly what the test created (tracked by ID), not a blanket "delete everything" that risks removing another test's in-flight data during parallel runs.
- For external systems that can't be transactionally rolled back (third-party APIs, payment sandboxes), use dedicated test accounts and clean up idempotently, tolerating "already deleted" as success.

## Cross-link
Feeds [[test-automation]] (fixtures), [[database-testing]] (migration test data at realistic volume/shape), [[performance-testing]] (load volume), and [[ai-ml-testing]]/[[llm-testing]] (evaluation datasets, handled with more rigor than generic synthetic data).

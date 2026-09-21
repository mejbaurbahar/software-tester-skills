---
name: smoke-sanity-testing
description: Use when designing or executing smoke tests and sanity suites — Build Verification Testing (BVT), pre-flight deployment verification, critical-path health checks, and fast-fail gating.
license: MIT
metadata:
  category: functional
  version: "2.0"
  tags: smoke, sanity, bvt, health-check, ci-gate
---

# Smoke & Sanity Testing

## Overview
Smoke and sanity tests provide rapid confidence that a build or deployment is stable enough for deeper testing.
- **Smoke Testing (BVT)**: Shallow, broad verification of critical paths to confirm core system stability after a fresh build/deploy.
- **Sanity Testing**: Focused, deep verification following a minor bugfix or release to confirm specific functionality works without collateral damage.

## Key Attributes
- **Target Execution Time**: Under 3 to 5 minutes total.
- **Zero Flakiness Tolerance**: Flaky smoke tests halt deployments; keep assertions robust and high-level.
- **Blocking Gate**: A failure immediately fails the CI/CD pipeline and aborts deployment.

## Smoke Test Checklist
1. **Service Availability**:
   - `GET /health` and `GET /ready` return 200 OK.
   - Database and cache connectivity verified.
2. **Landing & Assets**:
   - Homepage loads with HTTP 200 without JavaScript console exceptions.
   - Critical static assets (CSS, bundles, images) return 200 (no 404s).
3. **Critical Path Smoke**:
   - User can log in with a test account.
   - Core dashboard renders with primary navigation items.
   - Critical read endpoint returns valid non-empty payload.
   - One primary write operation succeeds.

## Automation Strategy
- Group smoke tests with annotations/tags (e.g. `@smoke`, `@bvt`).
- Run smoke tests immediately post-deployment in staging and production before traffic shifting.

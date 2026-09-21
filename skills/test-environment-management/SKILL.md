---
name: test-environment-management
description: Use when designing, stabilizing or scaling test environments — ephemeral preview environments, Docker Compose/Kubernetes/Testcontainers, environment parity, data seeding and reset, service virtualization, secrets, cost control and eliminating "works on my machine"/shared-staging contention.
license: MIT
metadata:
  category: automation
  version: "2.0"
  tags: test-environments, ephemeral, testcontainers, docker-compose, kubernetes, service-virtualization, staging, seeding, parity
---

# Test Environment Management

Unreliable environments cause more test failures than bad tests. Aim for **hermetic, disposable, production-like, and self-service.**

## Environment strategy
| Type | Use | Lifecycle |
| :--- | :--- | :--- |
| Local (Compose/Testcontainers) | Dev + unit/integration | per run |
| **Ephemeral preview** | Per-PR full stack for E2E/UAT | created on PR, destroyed on merge (Vercel/Netlify previews, Argo CD ApplicationSet, `namespace-per-PR`, Okteto, Tilt) |
| Shared integration/staging | Cross-team integration, pre-prod | long-lived, reset nightly |
| Perf / prod-like | Load & soak, capacity | booked windows, scaled to ratio |
| Production (synthetic) | Shift-right | permanent (`production-monitoring-synthetic-testing`) |

## Principles
1. **Infrastructure as code** for envs (Terraform/Helm/Kustomize/Compose) — rebuild from scratch in minutes.
2. **Parity**: same OS, versions, DB engine, config *shape*, flags, network topology; document deliberate diffs. Pin image digests.
3. **Isolation**: per-run data namespace or DB/schema; no cross-test coupling; avoid global shared accounts.
4. **Determinism**: fixed clock/seed, controlled 3rd-party responses.
5. **Observability**: logs/traces/metrics available in test env; retain artifacts on failure.

## Data
Seed via **API/factories/migrations** (not manual SQL dumps); baseline snapshot + fast reset (`pg_restore`, `TRUNCATE`, DB template `CREATE DATABASE t TEMPLATE base`, volume snapshots, transaction rollback per test); masked prod subsets (`test-data-engineering`); per-test unique IDs (`uuid`, worker index).

## Dependencies you don't own
| Need | Approach |
| :--- | :--- |
| Third-party API | Vendor sandbox → contract tests → service virtualization (WireMock, Hoverfly, MSW, Mountebank, Prism from OpenAPI) with **fault profiles** |
| Payments/email/SMS | Provider test modes / capture inboxes (`email-notification-testing`) |
| Cloud services | LocalStack, Azurite, Firebase emulators, MinIO, Testcontainers modules |
| Time | Fake clock |

```yaml
# docker-compose.test.yml (pin digests in real use)
services:
  app:  { build: ., environment: [DATABASE_URL=postgres://pg/test, STRIPE_API_BASE=http://wiremock:8080], depends_on: { pg: {condition: service_healthy} } }
  pg:   { image: postgres:16, healthcheck: { test: ["CMD-SHELL","pg_isready -U postgres"], interval: 2s, retries: 30 } }
  wiremock: { image: wiremock/wiremock:3.5.4, volumes: ["./stubs:/home/wiremock"] }
```
```bash
kubectl create ns pr-$PR && helm upgrade --install app ./chart -n pr-$PR --set image.tag=$SHA --wait
trap 'kubectl delete ns pr-$PR' EXIT      # auto-cleanup
```

## Shared-staging pain → fixes
Contention (booking calendar → ephemeral envs) · drift (nightly rebuild + config diff) · "who broke staging" (deploy-per-service ownership, contract tests gate deploys) · flaky data (isolated tenants) · cost (auto-suspend off-hours, TTL labels, spot instances).

## Health & readiness gate
Before tests run: `/healthz` on every service, DB migrated, seed done, dependent stubs up → fail fast with a clear "environment not ready" (not 300 red tests).

## Related
`integration-testing`, `microservices-testing`, `cicd-testing`, `test-data-engineering`, `flaky-test-management`

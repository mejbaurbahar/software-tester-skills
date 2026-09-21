---
name: system-testing
description: Use when verifying a fully integrated system against its specification — end-to-end functional and non-functional behavior in a production-like environment, system test planning, entry/exit criteria, and gap analysis between integration and acceptance testing.
license: MIT
metadata:
  category: functional
  version: "2.0"
  tags: system-testing, end-to-end, black-box, production-like, nfr
---

# System Testing

Tests the **complete, integrated product** as a black box in a production-like environment against requirements — both functional and non-functional. It sits between integration testing (components talk) and acceptance testing (business agrees).

## Entry criteria
Integration suite green · build deployed to a dedicated, production-like environment (same topology, versions, config, feature flags) · test data loaded · known defects triaged.

## Coverage map (build a test set per row)
| Area | What to verify | Skill |
| :--- | :--- | :--- |
| Functional flows | Every requirement end to end, incl. negative paths | `functional-testing` |
| Data integrity | Values consistent across UI, API, DB, reports, exports | `database-testing` |
| Interfaces | 3rd-party APIs, webhooks, files, queues | `integration-testing`, `contract-testing` |
| Security | Authn/z, input handling, secrets | `security-testing` |
| Performance | Response/throughput at expected + peak load | `performance-testing` |
| Reliability | Failover, retry, timeouts, recovery | `chaos-resilience-testing` |
| Usability & a11y | Task success, WCAG | `usability-testing`, `accessibility-testing` |
| Compatibility | Browsers, devices, OS, locales | `compatibility-testing`, `localization-testing` |
| Install/upgrade | Fresh install, upgrade, rollback | `installation-upgrade-testing` |
| Ops | Logs, metrics, alerts, backups | `observability-testing` |

## Procedure
1. Derive test conditions from requirements **and** from user journeys/state models (`test-design-techniques`).
2. Prioritize by risk = likelihood × impact (`test-strategist`).
3. Execute; log every failure with environment/build/data version.
4. Re-run against each fix; run regression on impacted areas (`regression-testing`).
5. Exit: requirement coverage 100% Must / ≥90% Should, no open Sev1/Sev2, NFR targets met, test summary report issued.

## Failure-analysis checklist
Reproduce twice · isolate layer (UI/API/DB/network) · check env drift (config, clock, data) · capture logs+trace IDs · classify: product bug / test bug / env issue / requirement gap.

## Pitfalls
Testing in a shared, drifting env; mocked dependencies that hide integration failures; no NFR criteria ("must be fast"); skipping data-migration and reporting paths.

## Related
`integration-testing`, `acceptance-testing`, `test-planning-documentation`, `smoke-sanity-testing`

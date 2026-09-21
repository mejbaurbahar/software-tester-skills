---
name: cloud-infrastructure-testing
description: Use when testing cloud/infrastructure concerns — Docker/Kubernetes deployments, serverless functions, managed-service integration (S3, queues, API Gateway), disaster recovery/failover, and infra-as-code correctness on AWS/Azure/GCP.
---

# Cloud & Infrastructure Testing

## Scope guardrail
Infra testing can touch shared/billable resources and, in the worst case, production-adjacent systems. Confirm target environment (sandbox/staging vs anything shared) before running anything with side effects (spinning up resources, triggering autoscaling, simulating failover) — see the general safety guidance already established for destructive actions.

## Containers & Kubernetes
- **Docker**: image builds reproducibly, no secrets baked into layers (`docker history`, or scan with Trivy — see [[security-testing]]), container starts and passes its own healthcheck, resource limits set (a container with no memory limit can OOM the node, not just itself).
- **Kubernetes**: deployment rolls out without downtime (`kubectl rollout status`), readiness/liveness probes actually reflect app health (a probe that always returns 200 defeats the point), resource requests/limits sized from real usage not guesses, HPA (autoscaling) triggers and scales back down correctly under synthetic load, pod disruption budgets don't accidentally block legitimate node maintenance.
- **ConfigMaps/Secrets**: changes propagate to running pods as expected (some require a rolling restart — verify the app's actual reload behavior rather than assuming).

## Serverless (Lambda / Cloud Functions)
- **Cold start latency** — measure it explicitly, it's a real UX/SLA factor invisible in local dev.
- **Timeout and memory limits** — test near the configured ceiling, not just the happy path with plenty of headroom.
- **Concurrency limits** — what happens when the function hits its concurrency cap: throttled invocations queued, dropped, or erroring? Confirm it matches the documented/expected behavior for the trigger type (sync API Gateway vs async event source behave differently on throttle).
- **Idempotency** — many event sources (SQS, S3 event notifications) can redeliver; function must handle duplicate invocation safely, same as event-driven testing in [[contract-testing]].
- **IAM least-privilege** — function's execution role should only have the permissions it actually uses; test by confirming it *cannot* perform actions outside its declared scope (a broad wildcard role is a security finding, not just tidiness — see [[security-testing]]).

## Managed services integration
- **S3/object storage**: eventual consistency edge cases (though most providers are now strongly consistent — verify the specific provider/region's current guarantee rather than assuming from older docs), lifecycle/expiry rules actually applied, presigned URL expiry enforced.
- **Queues (SQS/PubSub/RabbitMQ)**: visibility timeout tuned so a slow consumer doesn't cause duplicate processing; DLQ configured and monitored — see [[contract-testing]] for consumer-side idempotency testing.
- **API Gateway**: throttling/rate limits match the documented tier, request/response transformation doesn't silently drop fields, auth integration (JWT authorizer, IAM auth) actually rejects invalid tokens rather than passing through on misconfiguration.
- **CDN (CloudFront etc.)**: cache invalidation actually propagates, cache-key configuration doesn't leak user-specific content across users (a classic CDN misconfiguration bug — check if personalized responses are accidentally cached and served cross-user).

## Resilience: disaster recovery & failover
- **Failover test**: kill the primary (DB replica promotion, AZ failure simulation) and measure actual recovery time against the documented RTO/RPO — don't trust the runbook until you've run it.
- **Backup restoration**: a backup that has never been restored is unverified — periodically actually restore one into an isolated environment and confirm data integrity.
- **Multi-region**: if the architecture claims multi-region resilience, test with one region actually unavailable (not just theoretically) to confirm traffic shifts and data stays consistent.

## Infra-as-code correctness
- `terraform plan` / `pulumi preview` reviewed for unintended resource replacement (a change that looks additive but forces a destroy+recreate can cause an outage) before apply.
- Drift detection — infra manually changed outside IaC — caught and reconciled, not silently diverging.

## Cross-link
For deliberate failure-injection testing beyond infra-level failover, see [[chaos-resilience-testing]]. For monitoring/alerting on infra health, see [[observability-testing]].

---
name: observability-testing
description: Use when correlating a test failure or production issue across logs, metrics, and traces to find root cause; when verifying that a feature emits the logging/metrics/alerting it needs; or when doing shift-right testing via production monitoring.
license: MIT
metadata:
  category: operations
  version: "2.0"
  tags: observability, logs, metrics, traces, opentelemetry, monitoring
---

# Observability & Production Testing

## The core skill: correlate, don't guess
When something fails, follow the chain: **test/user report → logs → distributed trace → the specific API call → database query → infra metric**. Each link either confirms or rules out a layer. Don't speculate about root cause without walking this chain — "probably a timeout" is not a finding, a trace showing a 30s span on a specific downstream call is.

## What to check per signal type
- **Logs**: structured (JSON, not free-text — free-text logs are unqueryable at scale), correlation/request ID present and threaded through every service a request touches, log level appropriate (an error path logging at `info` gets missed; expected/handled conditions logging at `error` cause alert fatigue), no PII/secrets logged.
- **Metrics**: the four golden signals present per service — latency, traffic, errors, saturation. Check that a metric actually changes under real load (a counter that's always zero because it's wired to the wrong code path is a silent observability gap, not a healthy system).
- **Traces**: spans cover the actual critical path (DB calls, external API calls, queue publish/consume) not just the top-level request; trace context propagates across service/process boundaries (a broken propagation shows up as disconnected trace fragments instead of one end-to-end trace — this is one of the most common and most damaging observability bugs).

## Verifying a feature is observable (do this at feature-test time, not after an incident)
- Does a new critical code path emit a log/metric on both success and failure?
- Does a new failure mode have an alert, with a sane threshold (not so sensitive it pages on noise, not so loose it never fires)?
- Is there a dashboard panel or is this feature invisible until someone manually greps logs during an incident?
Treat "no observability for this new critical path" as a real finding — file it via [[bug-reporting]] like any other gap, it's cheaper to add now than after the first unexplained incident.

## Shift-right / production testing
- **Synthetic monitoring**: scripted checks running continuously against production (not just CI) catch environment-specific issues CI never sees (real DNS, real CDN, real third-party integrations).
- **Real-user monitoring (RUM)**: actual user-experienced performance/errors, which will differ from synthetic/lab results — reconcile the two rather than trusting only one.
- **Canary/feature-flag validation**: when a change ships to a subset of traffic, actively compare canary vs. baseline metrics (error rate, latency, business metric) before widening rollout — don't just "wait and see if anyone complains."
- **Error-rate/alert testing**: periodically verify alerts actually fire (trigger a known condition in staging, confirm the page/notification arrives) — an alert that's silently broken is worse than no alert, because it creates false confidence.

## Tools
- **Logs**: structured logging + a queryable backend (CloudWatch Logs Insights, Datadog Logs, Loki).
- **Metrics**: Prometheus + Grafana, Datadog, CloudWatch Metrics.
- **Tracing**: OpenTelemetry (vendor-neutral instrumentation) feeding into Jaeger, Tempo, Datadog APM, or similar.
- **Error tracking**: Sentry — correlates errors with release/deploy, gives stack traces and affected-user counts; use `mcp__claude_ai_Sentry__*` tools in this environment when investigating a live issue.

## Cross-link
Feeds directly into [[qa-code-intelligence]] for root-cause analysis, and into [[autonomous-qa-orchestration]]'s step of investigating backend state before filing a bug.

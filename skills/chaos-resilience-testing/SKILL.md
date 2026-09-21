---
name: chaos-resilience-testing
description: Use when deliberately injecting failure (network latency/loss, service/dependency crash, resource exhaustion) to verify a system degrades gracefully instead of cascading — retries, circuit breakers, timeouts, backpressure. Requires explicit authorization and a scoped blast radius; never run against unscoped production without sign-off.
license: MIT
metadata:
  category: non-functional
  version: "2.0"
  tags: chaos-engineering, resilience, fault-injection, circuit-breaker, retries
---

# Chaos / Resilience Testing

## Safety boundary — read first
Chaos testing is a controlled, authorized experiment, not random destruction:
- Confirm explicit authorization and a defined blast radius (specific service, specific % of traffic, specific environment) before running anything.
- Always have a kill switch / rollback ready before starting an experiment, and a monitoring dashboard open to abort immediately if impact exceeds the expected scope.
- Start in staging; only run in production with explicit sign-off, a documented game-day plan, and off-peak timing.
- Never run an experiment whose blast radius you can't predict or contain.

## What you're actually testing
Not "does it break" (it will) — you're verifying the system's **failure mode is graceful**: does it degrade a feature, or does one dependency failure cascade into a full outage? The finding that matters is *how* it fails, not just *that* it failed.

## Failure types to inject
- **Latency injection** — add artificial delay to a downstream call (Toxiproxy, a proxy sidecar, or code-level fault injection) and verify timeouts are actually configured (a call with no timeout will hang the caller indefinitely, which is itself the finding).
- **Service/dependency failure** — kill a downstream service or dependency and verify the caller's circuit breaker trips, falls back (cache, default, degraded feature) or fails fast with a clear error, rather than retrying forever or hanging.
- **Network partition** — split traffic so two nodes can't see each other; verify split-brain handling in anything with leader election/consensus.
- **Resource exhaustion** — CPU/memory pressure, connection pool exhaustion, disk full — verify the app fails predictably (clear error, backpressure) rather than corrupting data or hanging unrecoverably.
- **Database failure** — kill the primary DB connection mid-request; verify no partial writes, and that the app either queues/retries per its documented contract or surfaces a clear error rather than silently dropping the operation.
- **Queue saturation** — flood a queue beyond normal capacity; verify backpressure (producer slows/rejects) rather than unbounded memory growth or silent message loss.

## What "graceful" looks like — verify these exist, don't assume
- **Timeouts** on every external call (network, DB, downstream service) — no call should be able to hang forever.
- **Retries with backoff and a cap** — unbounded immediate retries turn a transient blip into a thundering-herd outage; verify exponential backoff and a max-attempt ceiling.
- **Circuit breakers** — after N consecutive failures, the caller should stop hammering a dead dependency and fail fast (or fall back), then periodically probe to see if it's recovered.
- **Bulkheads** — one overloaded dependency's connection pool exhaustion shouldn't starve unrelated request paths that don't even use that dependency.
- **Idempotency on retry paths** — a retried request (client-side or infra-level) must not double-apply the side effect (see [[contract-testing]], [[database-testing]]).

## Kubernetes-specific scenarios
- Pod eviction/OOM-kill mid-request — does the load balancer route around it without dropping in-flight requests?
- Node failure — does the scheduler reschedule affected pods within an acceptable window, and does the app's readiness probe correctly keep it out of rotation until actually ready?

## Tools
- **Toxiproxy** — network-level fault injection (latency, bandwidth limits, connection resets) via a proxy, good for local/CI-scoped testing.
- **Chaos Mesh / Litmus** — Kubernetes-native chaos engineering (pod kill, network chaos, IO chaos) with defined experiment CRDs.
- **Gremlin** — commercial, broader infra + application-level fault injection with built-in safety/halting controls.

## Reporting
Document: exact fault injected, blast radius, expected vs. actual degradation, recovery time, and whether the safeguard (timeout/breaker/retry) that should have contained it actually existed and worked. A missing safeguard is a Critical/Major finding depending on the dependency's centrality — see [[bug-reporting]].

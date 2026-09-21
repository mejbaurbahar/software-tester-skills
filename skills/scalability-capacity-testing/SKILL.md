---
name: scalability-capacity-testing
description: Use when determining how a system scales and how much capacity it needs — load models, capacity planning, autoscaling validation, bottleneck identification (USE/RED), stress/spike/soak/breakpoint tests, and cost-per-request analysis with k6, Locust, JMeter, Gatling.
license: MIT
metadata:
  category: non-functional
  version: "2.0"
  tags: scalability, capacity-planning, load-testing, stress, spike, soak, breakpoint, autoscaling, k6, little's-law
---

# Scalability & Capacity Testing

Goal: answer *"How much can it take, what breaks first, and how do we scale?"* — with numbers.

## Test types
| Test | Load shape | Question |
| :--- | :--- | :--- |
| Baseline/Load | expected peak, steady | SLO met at normal peak? |
| **Stress / Breakpoint** | ramp until SLO breaks / errors | Where is the limit & failure mode? |
| **Spike** | 10× jump in seconds | Autoscale/queues/caches cope? recover? |
| **Soak / Endurance** | 70% load for 4–24 h | Leaks, drift, log/disk growth (`memory-leak-resource-testing`) |
| Scalability | step 1×,2×,4× resources | Linear? Where diminishing returns? |
| Capacity | peak × growth × headroom | How many nodes/DB size for next year? |

## Workload model (garbage in, garbage out)
Use **production analytics**: request mix by endpoint, think-time, session length, data-size distribution, peak RPS/concurrency, geographic spread, cache-hit ratios. Little's Law: `concurrent users = arrival rate × avg session time`; `concurrency in service = RPS × latency`. Use **open model (arrival rate)** for public traffic; closed model (fixed users) for internal systems.

## k6 example: ramping arrival-rate + SLO thresholds
```js
export const options = {
  scenarios: { peak: { executor: 'ramping-arrival-rate', startRate: 20, timeUnit: '1s',
    preAllocatedVUs: 200, maxVUs: 2000,
    stages: [{target: 100, duration: '5m'}, {target: 400, duration: '10m'}, {target: 0, duration: '2m'}]}},
  thresholds: { http_req_failed: ['rate<0.01'], http_req_duration: ['p(95)<500','p(99)<1200'] },
};
```
```bash
k6 run --out influxdb=http://influx:8086/k6 script.js
locust -f locustfile.py --headless -u 2000 -r 50 -t 30m --host https://stg
```

## Find the bottleneck — USE & RED
- **USE** per resource (CPU, memory, disk, network, DB conns, threads): *Utilization, Saturation, Errors*.
- **RED** per service: *Rate, Errors, Duration* (p50/p95/p99, not average).
- Follow the saturation: LB → app CPU/GC → thread/conn pools → DB (slow queries, locks, IOPS) → cache → downstream APIs → network/egress limits.
- Correlate with traces (`observability-testing`); profile hot path (flame graphs: `py-spy`, `async-profiler`, `pprof`).

## Autoscaling validation
Scale-out trigger & lag (metrics interval + provisioning + warm-up), scale-in safe (draining, connection reuse), min/max bounds, per-AZ balance, stateful components, DB/cache not scaling (usually the real limit), cost cap.

## Report
Max sustainable throughput at SLO · latency curve (knee point) · first bottleneck + evidence · failure mode (graceful 429/503 vs cascading failure) · recommended capacity with 30–50% headroom · cost per 1k requests · retest plan.

## Pitfalls
Load generator is the bottleneck (monitor it; distribute) · unrealistic data (all cache hits) · testing prod-different infra · ignoring downstream rate limits · coordinated omission (use tools that correct it) · averaging latencies.

## Related
`performance-testing`, `chaos-resilience-testing`, `cloud-infrastructure-testing`, `web-performance-testing`, `observability-testing`

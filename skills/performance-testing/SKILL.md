---
name: performance-testing
description: Use for load/stress/soak/spike testing, Core Web Vitals audits, Lighthouse checks, API latency benchmarking, and diagnosing slow pages or endpoints. Covers both frontend perf and backend load testing.
license: MIT
metadata:
  category: non-functional
  version: "2.0"
  tags: performance, load-testing, k6, locust, lighthouse, web-vitals
---

# Performance Testing

Answer three questions with numbers: **Is it fast enough? How much can it take? What breaks first?** Test against a production-like **staging** environment; never load-test production or third-party systems without explicit authorization and a scoped plan.

## Pick the test type (do not conflate them)
| Type | Load shape | Finds |
| :--- | :--- | :--- |
| **Baseline/load** | Expected peak, sustained 15–60 min | Does the SLO hold at normal peak? |
| **Stress / breakpoint** | Ramp past peak until it degrades | Ceiling and failure mode (graceful 429/503 vs cascading failure) |
| **Spike** | Sudden 5–10× burst | Autoscaling lag, queue and cache behavior, recovery |
| **Soak / endurance** | 60–80% load for 4–24 h | Leaks, pool exhaustion, log/disk growth (`memory-leak-resource-testing`) |
| **Scalability** | Step resources 1×, 2×, 4× | Linear scaling or diminishing returns (`scalability-capacity-testing`) |
| **Front-end/page-load** | Real browser, throttled CPU/network | Core Web Vitals (`web-performance-testing`) |

## Set targets first
Agree SLOs before running: p95/p99 latency, error rate, throughput, resource ceilings (CPU < 70%). Without a target a number is just trivia. Compare with a **baseline** (last release); a 200 ms → 400 ms regression matters even if 400 ms "sounds fine".

## Model realistic load
Use production analytics for request mix, think time, session length and data distribution. Public traffic is an **open model** (arrival rate); internal tools are a **closed model** (fixed users). Little's Law: `concurrency = arrival rate × latency`. Seed realistic data volumes and vary parameters so caches do not make everything look fast.

## Tools
| Tool | Best for |
| :--- | :--- |
| **k6** | Developer-friendly JS scripts, thresholds, CI |
| **Locust** | Python scenarios, distributed load |
| **JMeter** | Protocol breadth (HTTP, JDBC, JMS), GUI-driven teams |
| **Gatling** | High-throughput JVM/Scala/Kotlin DSL, rich reports |
| **Artillery** | YAML scenarios, WebSocket/Socket.IO |
| **autocannon / wrk / hey / vegeta** | Fast single-endpoint benchmarks |
```js
// k6: ramp, then assert SLOs (run: k6 run script.js)
import http from 'k6/http'; import { check, sleep } from 'k6';
export const options = {
  stages: [{ duration: '2m', target: 50 }, { duration: '10m', target: 200 }, { duration: '2m', target: 0 }],
  thresholds: { http_req_failed: ['rate<0.01'], http_req_duration: ['p(95)<500', 'p(99)<1200'] },
};
export default function () {
  const r = http.get(`${__ENV.BASE}/api/products?limit=20`);
  check(r, { 'status 200': (x) => x.status === 200 });
  sleep(1);
}
```
```bash
k6 run -e BASE=https://staging.example.com script.js
locust -f locustfile.py --headless -u 200 -r 20 -t 15m --host https://staging.example.com --csv results
curl -w "connect=%{time_connect}s ttfb=%{time_starttransfer}s total=%{time_total}s\n" -o /dev/null -s https://staging.example.com/api/health
```

## Read results correctly
- Use **percentiles (p50/p95/p99)**, never averages; the tail is where users suffer.
- Watch **errors and saturation** alongside latency; find the knee where latency rises faster than throughput.
- Avoid **coordinated omission** (closed-loop tools hide queueing); prefer arrival-rate executors.
- Monitor the **load generator** too; if it is the bottleneck the test is invalid.
- Correlate with server metrics/traces (USE: utilization, saturation, errors; RED: rate, errors, duration) to name the first bottleneck: app CPU/GC, thread or connection pool, DB (slow queries, locks, IOPS), cache, downstream API, network.

## Database and API-level checks
Slow-query log and `EXPLAIN` on the top queries, N+1 detection, index use, connection-pool sizing, payload size and compression, cache hit ratio, pagination limits.

## Report
Test type and load profile · environment and data size · p50/p95/p99, throughput, error rate · **what broke first** and evidence · comparison to baseline/SLO · recommendations and retest plan. File regressions with `bug-reporting`.

## Related
`scalability-capacity-testing`, `web-performance-testing`, `memory-leak-resource-testing`, `chaos-resilience-testing`, `observability-testing`

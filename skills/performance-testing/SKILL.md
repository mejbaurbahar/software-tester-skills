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

## Frontend performance (Core Web Vitals)
Use Chrome DevTools MCP `performance_start_trace` / `performance_analyze_insight` or `lighthouse_audit`, or Claude in Chrome, to measure:
- **LCP** (Largest Contentful Paint) — target < 2.5s. Usually a hero image/font/render-blocking JS problem.
- **INP** (Interaction to Next Paint, replaced FID) — target < 200ms. Heavy main-thread JS on interaction is the usual cause.
- **CLS** (Cumulative Layout Shift) — target < 0.1. Usually images/ads/fonts without reserved dimensions.
- **TTFB** (Time to First Byte) — server/CDN latency; if this is high, it's a backend/infra problem, not frontend.

Capture a trace, then check for: unoptimized images, render-blocking CSS/JS in `<head>`, missing `font-display: swap`, excessive third-party scripts, no CDN/caching headers on static assets.

## Backend load testing (locust, in the qa-agent venv)
Test types, don't conflate them:
- **Load test** — expected peak traffic, sustained, confirm latency/error rate stays acceptable.
- **Stress test** — ramp beyond expected peak until it breaks, to find the actual ceiling and failure mode (graceful degradation vs. cascading failure).
- **Soak test** — moderate load sustained for hours, to catch memory leaks/connection-pool exhaustion that only show up over time.
- **Spike test** — sudden traffic burst (e.g. 10x in 30s), to check autoscaling/rate-limiting behavior.

```bash
~/qa-agent/.venv/bin/python -m locust -f locustfile.py --headless -u 100 -r 10 --run-time 5m --host https://target
```
- `-u` = concurrent users, `-r` = spawn rate/sec, watch p50/p95/p99 latency, not just average — averages hide the tail where users actually suffer.
- Always test against staging, never production, unless the user explicitly authorizes and it's a deliberately scoped/rate-limited game-day test.

## API latency benchmarking
For single-endpoint checks: `curl -w "@curl-format.txt" -o /dev/null -s <url>` to get connect/TTFB/total timing breakdown, or script repeated `requests` calls and report p50/p95/p99.

## What "good" looks like
Don't just report a number — compare against a baseline (previous release, competitor, or an explicit SLA/budget the team has agreed to). A regression from 200ms → 400ms matters even if 400ms sounds "fine" in isolation.

## Reporting
Include: test type, load profile, environment, p50/p95/p99 latency, error rate, and — critically — what broke first when you pushed past capacity (DB connection pool? memory? a specific endpoint?). Use [[bug-reporting]] for perf regressions found as defects.

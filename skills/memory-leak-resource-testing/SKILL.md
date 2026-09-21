---
name: memory-leak-resource-testing
description: Use when diagnosing or preventing memory leaks, unbounded growth, file-descriptor/connection/thread leaks, GC pressure, OOM kills, and slow degradation in long-running services, browsers, and mobile apps — heap snapshots, profilers, soak tests.
license: MIT
metadata:
  category: non-functional
  version: "2.0"
  tags: memory-leak, heap, profiling, soak, gc, file-descriptors, oom, resource-leak
---

# Memory Leak & Resource Testing

Symptom: memory/handles/latency grow with time or request count and never plateau; ends with OOM-kill, `EMFILE`, or timeouts.

## Detect (black-box first)
1. Run a **soak test** at steady load 1–24 h (`performance-testing`).
2. Chart RSS, heap-used, open FDs, thread count, DB connections, GC pause, queue depth. **Healthy = sawtooth around a plateau; leak = rising baseline after each GC.**
3. Force GC (where possible) and compare post-GC baselines at t0 vs t+N.

```bash
# Linux / container quick checks
ls /proc/$PID/fd | wc -l                     # FD count over time
ps -o rss,vsz,nlwp -p $PID                   # RSS, VSZ, threads
lsof -p $PID | awk '{print $5}' | sort | uniq -c | sort -rn | head
kubectl top pod --containers; kubectl describe pod | grep -i oomkilled
```

## Find the owner (white-box)
| Stack | Tooling |
| :--- | :--- |
| Node.js | `node --inspect`, Chrome DevTools heap snapshots (3-snapshot diff), `clinic doctor/heapprofiler`, `--heapsnapshot-signal=SIGUSR2` |
| Browser/SPA | DevTools Memory tab → "Allocation instrumentation on timeline", detached DOM nodes, `performance.measureUserAgentSpecificMemory()`; Puppeteer loop + heap check |
| Python | `tracemalloc`, `objgraph`, `memray run`, `py-spy dump` |
| Java/JVM | JFR, `jcmd GC.heap_dump`, Eclipse MAT dominator tree, `-XX:+HeapDumpOnOutOfMemoryError` |
| Go | `pprof` heap/goroutine profiles (`/debug/pprof/heap`), goroutine leak detection `goleak` |
| Native | Valgrind/`heaptrack`, ASan LeakSanitizer |
| Android/iOS | Android Studio Profiler / LeakCanary; Xcode Instruments Leaks & Allocations |

## Typical root causes
Unbounded caches/maps · listeners/subscriptions never removed · timers/intervals not cleared · closures holding large objects · detached DOM nodes · unclosed streams/cursors/connections · thread/goroutine leaks (blocked channel) · growing logs/metrics label cardinality · ThreadLocal misuse · session stores without TTL.

## Regression test ideas
```js
// Jest + node: loop operation and assert bounded growth
global.gc(); const a = process.memoryUsage().heapUsed;
for (let i=0;i<10000;i++) handle(sampleReq());
global.gc(); const b = process.memoryUsage().heapUsed;
expect(b - a).toBeLessThan(5 * 1024 * 1024);   // run with node --expose-gc
```
Also: repeat-navigation loop in Playwright then compare heap; goroutine count before/after (`goleak.VerifyNone(t)`); connection-pool `active == 0` after test.

## Report
Growth rate (MB/h), load profile, first-seen build, retained-object class + retainer path, minimal repro, suggested fix (bound/evict/close/unsubscribe).

## Related
`performance-testing`, `observability-testing`, `chaos-resilience-testing`, `mobile-testing`

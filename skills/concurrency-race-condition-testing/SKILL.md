---
name: concurrency-race-condition-testing
description: Use when testing thread-safety, race conditions, deadlocks, double-submit, idempotency, optimistic/pessimistic locking, async ordering bugs, and flaky concurrency failures — with TSan, go -race, stress loops, barrier-based harnesses and parallel API calls.
license: MIT
metadata:
  category: code-level
  version: "2.0"
  tags: concurrency, race-condition, deadlock, idempotency, thread-safety, tsan, locking
---

# Concurrency & Race-Condition Testing

Races don't fail on demand. You must **force interleavings** and **detect** violations.

## Bug catalog (what to hunt)
Lost update (read-modify-write) · double spend / oversell (check-then-act) · duplicate submit / retry storms · deadlock (lock ordering) · livelock/starvation · stale cache after write · non-atomic multi-step DB ops · async callbacks out of order · TOCTOU file/permission checks · unsafe shared state in singletons · connection/thread-pool exhaustion.

## Detection tools
| Stack | Tool |
| :--- | :--- |
| Go | `go test -race -count=100 ./...` |
| C/C++/Rust | ThreadSanitizer (`-fsanitize=thread`), `loom` (Rust) |
| Java | jcstress, `-XX:+...`, Thread dumps, `jstack` deadlock detection |
| Python | `pytest-xdist`, `threading.Barrier`, `asyncio.gather` stress |
| JS/TS | `Promise.all` bursts, `jest --runInBand` vs parallel diff |
| DB | Two sessions + `pg_sleep`/`SLEEP()` to widen windows; isolation-level tests |
| System | `stress-ng`, k6/Locust with identical concurrent requests |

## Force the interleaving
```python
# Fire N identical requests at the same instant (double-spend probe)
import threading, requests
N = 20; barrier = threading.Barrier(N); results = []
def hit():
    barrier.wait()
    results.append(requests.post(URL, json={"coupon":"ONCE"}, headers=H).status_code)
ts = [threading.Thread(target=hit) for _ in range(N)]
[t.start() for t in ts]; [t.join() for t in ts]
assert results.count(200) == 1, results       # coupon must apply exactly once
```
```bash
# bash/curl burst against an idempotent endpoint
seq 1 20 | xargs -P20 -I{} curl -s -o /dev/null -w "%{http_code}\n" -X POST -H "Idempotency-Key: k1" $URL | sort | uniq -c
```

## What to assert
- **Exactly-once**: inventory never < 0; balance conserved; one row per idempotency key; unique constraints hold.
- **Isolation**: no dirty/non-repeatable/phantom reads at the level you claim (`READ COMMITTED` vs `SERIALIZABLE`).
- **Liveness**: operations finish under contention (timeouts, no deadlock); lock timeouts surface clean errors.
- **Ordering**: events processed in key order; consumers tolerate redelivery.

## Fix patterns to recommend
Atomic SQL (`UPDATE … SET qty = qty-1 WHERE qty>0`) · optimistic locking (version column/ETag `If-Match`) · unique constraints + idempotency keys · advisory locks/`SELECT … FOR UPDATE` · consistent lock ordering · queue partitioning by key · immutable data.

## Reporting
Include seed/iteration count, concurrency level, exact interleaving/log lines, and expected vs observed invariant. Rate by blast radius (money/data loss = Sev1).

## Related
`api-testing`, `database-testing`, `flaky-test-management`, `chaos-resilience-testing`, `event-driven-messaging-testing`

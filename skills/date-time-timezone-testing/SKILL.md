---
name: date-time-timezone-testing
description: Use when testing anything involving dates, times, time zones, DST, leap years/seconds, scheduling, expiry, recurring events, cron jobs, or locale calendars — with frozen clocks, boundary calendars, and the classic time bugs checklist.
license: MIT
metadata:
  category: code-level
  version: "2.0"
  tags: datetime, timezone, dst, leap-year, scheduling, cron, clock-mocking
---

# Date, Time & Time-Zone Testing

Time bugs are silent, seasonal and expensive. Make time an **injectable dependency** and test the calendar's sharp edges deliberately.

## Test-date matrix (always include)
| Case | Example values |
| :--- | :--- |
| Leap day | `2024-02-29`, `2023-02-28→03-01`, `2100-02-29` invalid (century rule) |
| Month/year ends | `Jan 31 + 1 month`, `Dec 31 23:59:59 → Jan 1`, ISO week 53 |
| DST spring-forward | `2026-03-08 02:30` America/New_York (does not exist) |
| DST fall-back | `2026-11-01 01:30` (occurs twice) |
| Odd offsets | Asia/Kolkata +05:30, Asia/Kathmandu +05:45, Australia/Lord_Howe 30-min DST |
| Zone changes | user travels; server UTC vs browser local; zone rule updates (tzdata) |
| Epoch limits | 32-bit overflow `2038-01-19`, negative epochs, `0` |
| Locale calendars | Buddhist/Hijri/Japanese eras, week starting Sunday vs Monday |
| Leap second | `23:59:60` tolerated by parsers |

## Techniques
1. **Freeze the clock**: `freezegun`/`time-machine` (Py), `jest.useFakeTimers().setSystemTime()`, `Clock.fixed()` (Java), `faketime`/`libfaketime` for binaries, `TZ=Asia/Dhaka` env var.
2. **Run the suite under multiple zones**: `for tz in UTC America/Los_Angeles Asia/Kolkata Pacific/Auckland; do TZ=$tz npm test; done`.
3. **Store UTC, display local**; store the *zone ID* (not offset) for future events (meetings, reminders).
4. **Compare instants, not strings.** Use ISO-8601 with offset; avoid `Date` parsing of ambiguous `03/04/2026`.
5. **Property test**: `parse(format(t)) == t` for random instants across zones.
6. **Scheduler tests**: advance a fake clock past triggers; verify missed-run and double-run behavior across DST; cron in `UTC`.
7. **Expiry logic**: assert at `expiry-1s`, `expiry`, `expiry+1s`; token TTL and clock skew tolerance (±60s).

```python
from freezegun import freeze_time
@freeze_time("2026-03-08 06:59:59", tz_offset=0)   # 1s before US DST jump
def test_reminder_survives_dst(): ...
```

## Bug checklist
`new Date("2026-01-31")` parsed as UTC then displayed a day earlier · `+ 24h` ≠ next day on DST · month arithmetic overflow · week-year (`YYYY` vs `yyyy`) in formatters · DB `TIMESTAMP` vs `TIMESTAMPTZ` · naive vs aware datetimes · sorting by string date · server local time in cron · "end of day" excluded from ranges.

## Related
`localization-testing`, `unit-testing`, `property-based-testing`, `database-testing`

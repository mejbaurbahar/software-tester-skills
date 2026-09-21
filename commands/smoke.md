---
description: Run a fast smoke check to see whether a build is testable
argument-hint: "[URL or command]"
---

Run a smoke check on: $ARGUMENTS

Use the `smoke-sanity-testing` skill.

1. If $ARGUMENTS is empty, look for a documented start command, health endpoint or existing smoke script.
2. Verify only the critical path: app starts, health endpoint OK, home/login loads, one core read and one core write work, no console or server errors.
3. Keep it under about 3 minutes. Stop at the first blocker.
4. Report a verdict line first: PASS (testable) or FAIL (blocked), then the evidence.

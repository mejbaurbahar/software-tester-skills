---
description: Turn observations into a clear, reproducible bug report
argument-hint: "[what went wrong]"
---

Write a bug report for: $ARGUMENTS

Use the `bug-reporting` skill.

1. Ask only for missing essentials (expected vs actual, environment, steps). Never invent details.
2. Reproduce the issue if it is reproducible from here; record the exact steps and the reproduction rate.
3. Collect evidence: console/network errors, logs, request/response, screenshots (redact secrets and personal data).
4. Output: title (component + symptom), severity and priority with reasoning, environment/build, numbered steps, expected, actual, evidence, suspected cause (clearly labelled as a hypothesis), workaround.
5. Save it as `reports/bug-<slug>.md` unless the user names another destination.

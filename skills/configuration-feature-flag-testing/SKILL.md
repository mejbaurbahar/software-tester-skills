---
name: configuration-feature-flag-testing
description: Use when testing configuration, environment variables, secrets handling and feature flags — flag matrices, progressive rollouts, kill switches, targeting rules, stale flag cleanup, config drift between environments, and safe defaults (LaunchDarkly, Unleash, GrowthBook, OpenFeature).
license: MIT
metadata:
  category: non-functional
  version: "2.0"
  tags: feature-flags, configuration, launchdarkly, unleash, openfeature, rollout, kill-switch, config-drift, twelve-factor
---

# Configuration & Feature-Flag Testing

Configuration is code that skips code review. Most outages after deploy are **config or flag changes**, not code.

## Feature flags — test the combinatorics smartly
- Each flag adds a code path; N flags = 2^N states. **Don't test all** — test: (1) all default/OFF (production baseline), (2) each flag ON alone, (3) known-interacting pairs (pairwise, `test-design-techniques`), (4) the "next release" state.
- Test **both sides of every flag** in CI (`FLAGS=new_checkout:on|off`), including the **fallback/default value when the flag service is down or times out** (must fail safe).
- Flag types: release, experiment (`a-b-testing`), ops/kill-switch, permission. Different lifecycles & owners.

```ts
// OpenFeature with in-memory provider for deterministic tests
OpenFeature.setProvider(new InMemoryProvider({ 'new-checkout': { defaultVariant:'off', variants:{on:true, off:false}, disabled:false }}));
```

## Rollout validation
| Step | Verify |
| :--- | :--- |
| Targeting rules | Correct segment (user/tenant/country/percent); sticky bucketing by stable ID; no flapping between requests |
| % ramp 1→5→25→100 | Metrics guardrails (errors, latency, conversion) auto-halt |
| Kill switch | Turning OFF really disables path *and* cleans partial state; works without deploy; propagation time measured |
| Consistency | Server vs client vs cache agree; multi-service same decision per request (pass evaluated flags downstream) |
| Audit | Who changed what/when; change requires approval in prod |
| Cleanup | Flag removed within N days after 100%; lint for stale flags (Piranha, flag-age dashboard) |

## Configuration checks
- **Validate at startup, fail fast**: missing/invalid env var → process exits with clear message (test it). Schema-validate config (Zod/pydantic/JSON Schema).
- **Precedence** (defaults < file < env < CLI/remote) tested per layer.
- **Environment parity/drift**: diff staging vs prod config (`terraform plan`, `helm diff`, `kubectl diff`, dotenv-linter); differences must be intentional (secrets, scale).
- **Secrets**: never in repo/logs/images/error pages (`gitleaks`), rotated without redeploy, least-privilege, different per environment; app handles rotation (reload/restart).
- **Dynamic reload**: change applied atomically; invalid change rejected & previous kept; last-known-good.
- **Limits**: timeouts, pool sizes, retries, rate limits, batch sizes — boundary values and "zero/negative/huge" inputs.
- **Time/locale/TZ/encoding defaults** (`date-time-timezone-testing`).
- **Safe defaults**: debug off, CORS closed, verbose errors off, TLS verify on in prod.

## Chaos for config
Flag provider outage · stale cache · malformed JSON config · removed env var · wrong region/endpoint · expired secret → app degrades safely (`chaos-resilience-testing`).

## Related
`release-readiness-testing`, `a-b-testing`, `cloud-infrastructure-testing`, `security-hardening`, `test-environment-management`

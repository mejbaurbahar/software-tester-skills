<!-- Generated from commands/perf-plan.md by scripts/build_adapters.py - do not edit by hand. -->
# Create a load/performance test plan and script with SLOs

Create a performance test plan for: the text the user typed after this command (ask if none)

Use the `performance-testing`, `scalability-capacity-testing` and `web-performance-testing` skills.

1. Establish targets: SLOs (p95/p99 latency, error rate, throughput). Ask if none exist and propose defaults.
2. Define the workload model from real traffic patterns; choose test types (baseline, stress, spike, soak).
3. Write a k6 (or the project's existing tool) script with thresholds matching the SLOs. Run it only against staging or local environments.
4. Describe how to monitor the system under test and how to find the first bottleneck.
5. Output the plan, the script, run commands and the report template.

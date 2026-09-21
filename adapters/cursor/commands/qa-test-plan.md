<!-- Generated from commands/test-plan.md by scripts/build_adapters.py - do not edit by hand. -->
# Create a risk-based test plan for a feature or release

Create a test plan for: the text the user typed after this command (ask if none)

Use the `test-planning-documentation`, `test-strategist` and `requirements-testing-review` skills.

1. If the text the user typed after this command (ask if none) is empty, ask what feature/release to plan and stop.
2. Inspect the repository (README, docs, recent `git log`, changed files) to learn scope. Do not invent features.
3. List the top 5 risks (likelihood x impact) and let them drive the test focus.
4. Produce the plan: scope in/out, approach per level (unit/API/UI) and type (functional, security, performance, accessibility), environments and data, entry/exit criteria, schedule/roles, and assumptions/open questions.
5. Add a requirements-to-tests traceability table and flag requirements that have no test.
6. Save it to `docs/testing/test-plan-<slug>.md` and print a 5-line summary.

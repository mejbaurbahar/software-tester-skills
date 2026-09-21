<!-- Generated from commands/threat-model.md by scripts/build_adapters.py - do not edit by hand. -->
# Build a STRIDE threat model and derive security test cases

Threat-model: the text the user typed after this command (ask if none)

Use the `threat-modeling` skill.

1. Read the code/docs to build a data-flow diagram (Mermaid) with trust boundaries.
2. Enumerate threats per element with STRIDE; rate each by likelihood x impact.
3. Propose mitigations (design-level first) and mark accept/mitigate/transfer.
4. Convert each mitigation into concrete test cases and save the threat-to-test table to `docs/security/threat-model-<slug>.md`.

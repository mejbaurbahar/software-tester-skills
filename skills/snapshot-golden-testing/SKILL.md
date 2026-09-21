---
name: snapshot-golden-testing
description: Use when adding or reviewing snapshot, golden-file, approval, or characterization tests — Jest/Vitest snapshots, syrupy, ApprovalTests, insta, golden files for CLI/report/serializer output, and stopping snapshot rot and blind "update all" approvals.
license: MIT
metadata:
  category: code-level
  version: "2.0"
  tags: snapshot, golden-master, approval-testing, characterization, jest, syrupy, insta
---

# Snapshot / Golden-Master / Approval Testing

Record known-good output once; fail if it changes; a human reviews and approves intentional diffs. Best for large or hard-to-hand-assert outputs and for **characterizing legacy code before refactoring**.

## Good uses
Serialized API responses (with volatile fields masked) · generated code/SQL/HTML/emails · CLI output · report/PDF text · AST/compiler output · component *structure* (small) · legacy behavior pinning.

## Bad uses
Whole-page/large DOM snapshots (nobody reviews 800 lines) · anything with timestamps/IDs/random values · visual look (use `visual-testing`) · replacing meaningful assertions.

## Tools
| Stack | Tool |
| :--- | :--- |
| JS/TS | `toMatchSnapshot()`, `toMatchInlineSnapshot()` (Jest/Vitest) |
| Python | `syrupy`, `pytest-regressions`, `approvaltests` |
| Rust | `insta` (`cargo insta review`) |
| Java/.NET | ApprovalTests, Verify (`VerifyXunit`) |
| Go | `goldie`, `cupaloy`, golden files + `-update` flag |

## Rules that keep snapshots trustworthy
1. **Small & focused** — snapshot the smallest meaningful value; prefer inline snapshots (visible in the test).
2. **Deterministic** — freeze time/UUID/random; scrub IDs/dates with serializers (`expect.addSnapshotSerializer`, `syrupy` matchers).
3. **Review diffs like code.** PR reviewers read snapshot changes; `--ci` mode fails on *new* unwritten snapshots.
4. **Never bulk-update** (`jest -u`, `--snapshot-update`) without reading the diff; commit the update separately with a reason.
5. **Delete obsolete** snapshots (`jest --ci --detectOpenHandles`, `--clearCache`, `syrupy --snapshot-details`).
6. **Name by behavior**, one concept per snapshot.

```ts
expect(renderInvoice(order)).toMatchInlineSnapshot(`
  "Invoice #<ID>
   Total: $42.00 (incl. tax $3.50)"
`);   // with ID scrubbed by serializer
```
```python
def test_report(snapshot): assert build_report(fixture) == snapshot   # syrupy
```

## Characterization workflow for legacy code
1. Feed representative + edge inputs. 2. Capture current outputs as golden (even if "wrong"). 3. Refactor with the goldens green. 4. Fix bugs deliberately, updating goldens with explanation.

## Related
`unit-testing`, `visual-testing`, `regression-testing`, `mutation-testing`

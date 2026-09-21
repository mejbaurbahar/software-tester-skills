---
name: cli-testing
description: Use when testing command-line tools and scripts — exit codes, stdout/stderr contracts, flags and argument parsing, help/version output, stdin/pipes, env/config precedence, cross-platform paths, signals, idempotency, and Bats/pytest/expect-based automation.
license: MIT
metadata:
  category: platform
  version: "2.0"
  tags: cli, command-line, bats, exit-codes, stdout, shell, expect, argparse, cross-platform
---

# CLI Testing

A CLI's API is: **args + env + stdin → stdout + stderr + exit code + side effects.** Test that contract.

## Contract checklist
| Aspect | Verify |
| :--- | :--- |
| Exit codes | `0` success; non-zero on failure (documented: 1 general, 2 usage, 64–78 sysexits); consistent |
| Streams | Data → **stdout**; diagnostics/progress → **stderr**; nothing extra on stdout (pipe-safe) |
| Help/version | `-h/--help` exit 0, lists all flags, examples; `--version` machine-readable |
| Args | Unknown flag → usage error (exit 2); missing required arg; `--` separator; flag=value & flag value; short-flag bundling `-abc`; repeated flags; negative numbers |
| Input | stdin `-`; empty stdin; huge stdin; binary; CRLF; TTY vs pipe detection |
| Output modes | `--json` valid & stable schema; `--quiet/--verbose`; color disabled when not TTY or `NO_COLOR` set |
| Config precedence | flag > env > project config > user config > defaults (test each layer) |
| Files | Nonexistent, directory instead of file, no permission, symlink, spaces/unicode paths, `~` expansion, overwrite prompts/`--force`, atomic writes |
| Idempotency | Running twice is safe; `--dry-run` changes nothing |
| Signals | SIGINT/SIGTERM → cleanup, partial files removed, exit 130/143; SIGPIPE handled (`| head`) |
| Interactivity | Prompts have non-interactive override (`--yes`); no hang in CI |
| Cross-platform | Windows paths/CRLF/quoting, macOS BSD vs GNU coreutils, locale `LANG=C` |
| Security | No secrets in argv (visible in `ps`); shell-injection via args/filenames; tmp files 0600; safe deserialization |
| Performance | Startup time; large input streaming (constant memory) |

## Tooling
```bash
# Bats (bash)
#!/usr/bin/env bats
@test "prints version" { run mycli --version; [ "$status" -eq 0 ]; [[ "$output" =~ ^mycli\ [0-9]+\.[0-9]+ ]]; }
@test "rejects unknown flag" { run mycli --nope; [ "$status" -eq 2 ]; [[ "$output" == *"Usage"* ]]; }
```
```python
# pytest + subprocess
import subprocess, json
def run(*a, inp=None): return subprocess.run(["mycli",*a], input=inp, capture_output=True, text=True)
def test_json_mode():
    r = run("list","--json"); assert r.returncode == 0 and r.stderr == ""
    assert isinstance(json.loads(r.stdout), list)
```
Other: `cram`/`prysk` (transcript tests), `expect`/`pexpect`/`node-pty` for interactive TTY flows, `snapshot-golden-testing` for help text and reports, `shellcheck` + `shfmt` for shell scripts, Go `testscript`, Rust `assert_cmd` + `predicates`, Node `execa`.

## Test the installed artifact
Package (npm/pip/brew/cargo/binary), install into a clean container, run smoke commands, verify shebang/permissions/completions (`bash`, `zsh`, `fish`), man page, `--version` matches tag.

## Related
`unit-testing`, `integration-testing`, `snapshot-golden-testing`, `installation-upgrade-testing`, `fuzz-testing`

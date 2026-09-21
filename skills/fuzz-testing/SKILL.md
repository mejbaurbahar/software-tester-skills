---
name: fuzz-testing
description: Use when hunting crashes, hangs, memory bugs and parser/protocol vulnerabilities with random or coverage-guided inputs — fuzzing with AFL++, libFuzzer, Jazzer, Atheris, go-fuzz, cargo-fuzz, Schemathesis, and HTTP/API fuzzing, plus corpus and crash triage.
license: MIT
metadata:
  category: code-level
  version: "2.0"
  tags: fuzzing, afl, libfuzzer, atheris, schemathesis, crash-triage, sanitizers, security
---

# Fuzz Testing

Feed a program huge volumes of malformed/unexpected input and watch for crashes, hangs, sanitizer errors, or contract violations. Coverage-guided fuzzers mutate inputs that reach *new code* — thousands of executions per second.

## Where fuzzing pays off
Parsers (JSON/XML/PDF/image/protobuf), deserializers, decoders, regex engines, file-format handlers, network protocols, CLI arg handling, SQL/template engines, and **HTTP APIs**.

## Pick a tool
| Target | Tool |
| :--- | :--- |
| C/C++ | AFL++, libFuzzer (+ ASan/UBSan) |
| Go | native `go test -fuzz` |
| Rust | `cargo fuzz` (libFuzzer), `proptest` |
| Java/Kotlin | Jazzer |
| Python | Atheris, Hypothesis |
| JS/TS | Jazzer.js, fast-check |
| REST/GraphQL API | **Schemathesis**, RESTler, Dredd, `ffuf` |
| Web params | `ffuf`, `wfuzz` (authorized targets only) |

## Recipes
```go
// Go — native fuzzing
func FuzzParse(f *testing.F) {
    f.Add("2024-01-31")                       // seed corpus
    f.Fuzz(func(t *testing.T, s string) {
        d, err := Parse(s)
        if err == nil && d.String() != Normalize(s) { t.Fatalf("mismatch %q", s) }
    })
}
// run: go test -fuzz=FuzzParse -fuzztime=60s
```
```python
# Python — Atheris
import atheris, sys
def one(data):
    fdp = atheris.FuzzedDataProvider(data)
    parse(fdp.ConsumeUnicodeNoSurrogates(256))
atheris.Setup(sys.argv, one); atheris.Fuzz()
```
```bash
# API fuzzing from an OpenAPI spec (finds 5xx, schema violations, auth gaps)
schemathesis run https://staging.example.com/openapi.json --checks all --hypothesis-max-examples=200
# C/C++ with sanitizers
clang++ -g -O1 -fsanitize=fuzzer,address,undefined harness.cc -o fuzz && ./fuzz corpus/ -max_total_time=300
```

## Workflow
1. **Harness**: a function taking bytes → calls target. Fast, deterministic, no global state, no network/disk.
2. **Seed corpus**: real valid samples + past bug inputs. Add a **dictionary** of tokens (`"<script>"`, `"\"key\":"`).
3. **Sanitizers on** (ASan, UBSan, MSan, TSan) — most memory bugs are silent without them.
4. **Run** continuously (CI: 60–300 s per PR; nightly hours; OSS-Fuzz/ClusterFuzzLite).
5. **Triage**: minimize (`-minimize_crash=1` / `afl-tmin`), dedupe by stack hash, classify (crash / hang / OOM / logic), file with the reproducer bytes.
6. **Regress**: commit every crashing input to the corpus as a permanent test.
7. **Measure** coverage of the harness; add seeds for un-reached branches.

## Safety & ethics
Fuzz only systems you own or are authorized to test; use staging; throttle to avoid DoS; never fuzz production payment/email endpoints.

## Related
`property-based-testing`, `security-testing`, `api-testing`, `static-analysis-testing`

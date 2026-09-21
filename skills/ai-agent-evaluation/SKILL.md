---
name: ai-agent-evaluation
description: Use when testing and evaluating AI agents and tool-using LLM systems — task-success and trajectory evaluation, tool-call correctness, LLM-as-judge calibration, regression datasets, non-determinism (pass@k), cost/latency budgets, and CI evals with DeepEval, promptfoo, LangSmith, Inspect or MLflow.
license: MIT
metadata:
  category: ai
  version: "2.0"
  tags: agent-evaluation, llm-evals, tool-calling, trajectory, llm-as-judge, promptfoo, deepeval, inspect, non-determinism, agents
---

# AI Agent Evaluation & Testing

Agents are non-deterministic, multi-step and act on the world. Test **outcomes, trajectories, policy adherence and cost** with datasets, not vibes.

## What to measure
| Level | Metric | How |
| :--- | :--- | :--- |
| Task outcome | Success rate | Check the end state programmatically (DB row, file, API effect) before using a judge |
| Trajectory | Steps, loops, redundant calls, error recovery | Assert on the recorded trace (must search before answering) |
| Tool use | Right tool, schema-valid args, no invented tools | Assert on tool-call log |
| Response quality | Faithfulness, relevance, completeness, format | LLM-as-judge with rubric + human spot-check |
| Policy | Respects permissions, asks confirmation for irreversible actions | Scenario set with `must-not` rules |
| Robustness | Paraphrase, typos, other languages, long context | Perturbation suites |
| Efficiency | Tokens, latency p95, tool calls, cost per task | Budget assertions |
| Consistency | pass@k / pass^k over N runs | Run each case 5–10× |

## Build the dataset
Start with 20–50 real or synthetic tasks from logs and tickets; grow to 200+. Tag by capability, difficulty and risk. Each case: input/context, expected outcome (assertion), optional reference trajectory, `must-not` rules. Include ambiguous asks (should it clarify?), tool failures (timeouts, 500s, empty results) and untrusted text inside tool outputs.

## Tooling
```yaml
# promptfoo — declarative evals in CI
prompts: [file://prompts/agent.txt]
providers: [openai:gpt-4.1, anthropic:messages:claude-sonnet-4]
tests:
  - vars: { task: "Refund order A-991" }
    assert:
      - type: javascript
        value: output.toolCalls.some(t => t.name === 'issue_refund' && t.args.orderId === 'A-991')
      - type: llm-rubric
        value: "Confirms the refund amount and timeline; mentions no other customer's data"
```
```python
# DeepEval — metrics as pytest
from deepeval import assert_test
from deepeval.metrics import ToolCorrectnessMetric, TaskCompletionMetric
assert_test(test_case, [ToolCorrectnessMetric(threshold=0.9), TaskCompletionMetric(threshold=0.8)])
```
Also: LangSmith / Langfuse datasets and traces, UK AISI **Inspect**, OpenAI Evals, MLflow evaluate, Ragas (`rag-evaluation-testing`). Emit OpenTelemetry GenAI traces so any failure can be replayed.

## Make LLM-as-judge trustworthy
Explicit scoring anchors · judge model different from the agent · randomise order in pairwise comparisons · structured output · **calibrate against ~50 human labels** (agreement ≥ 80%) · version judge prompts · never expose the rubric to the agent.

## Test the harness, not just the model
Mock tools for deterministic unit tests (record/replay) · sandbox real tools · least-privilege tool scopes · human approval for irreversible actions · max-step, budget and timeout limits · resume after crash · concurrent tasks · context-window overflow handling.

## Regression workflow
1. Every production failure becomes a dataset case.
2. PRs run a fast subset (~30 cases, <5 min); nightly runs the full set.
3. Gate on success ≥ baseline − ε (statistical test over N runs), policy adherence = 100%, cost ≤ budget.
4. Compare model/prompt versions side by side and keep an eval changelog.
5. Online: shadow or canary rollout, user feedback, guardrail monitors.

## Pitfalls
Single-run pass/fail on a stochastic system · the judge grading its own output · test set leaked into the prompt · optimising to the eval · happy-path-only tasks · ignoring cost/latency · unlogged seeds and versions.

## Related
`llm-testing`, `rag-evaluation-testing`, `mcp-testing`, `chatbot-voice-agent-testing`, `llm-security-audit`

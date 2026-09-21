---
name: llm-testing
description: Use when testing LLM-powered features — prompt testing, hallucination/faithfulness checks, RAG evaluation, agent/tool-use testing, prompt injection and LLM security, regression testing across model/prompt versions, and cost/latency/token budget testing.
license: MIT
metadata:
  category: ai
  version: "2.0"
  tags: llm, prompts, hallucination, rag, evals, token-budget
---

# LLM Testing

## This machine already has MLflow tooling for parts of this
This environment has the `mlflow:agent-evaluation`, `mlflow:instrumenting-with-mlflow-tracing`, `mlflow:analyzing-mlflow-trace`/`analyzing-mlflow-session`, `mlflow:build-a-scorer`, and `mlflow:querying-mlflow-metrics` skills available — use those directly for trace instrumentation and scored evaluation runs rather than reinventing the harness. This skill covers the testing *methodology*; MLflow's skills cover the *execution mechanics* on this setup.

## What's fundamentally different from classical software testing
Non-determinism (same input can produce different output) and no single "correct" output for open-ended generation — you're testing distributions and properties, not exact-match assertions, most of the time.

## Evaluation approaches
- **Golden dataset with reference answers**: for tasks with a knowable correct answer (extraction, classification via LLM, structured output), compare against references using exact match, semantic similarity (embedding cosine similarity), or a rubric.
- **LLM-as-judge**: use a second LLM call to score the output against a rubric (relevance, correctness, tone) when no single reference answer exists — but validate the judge itself against human-labeled examples periodically, since a miscalibrated judge silently produces meaningless scores. See `mlflow:build-a-scorer`.
- **Human evaluation**: still the ground truth for subjective quality — sample a subset for human review even when automated scoring runs at scale, to catch judge drift.

## Core properties to test
- **Faithfulness/groundedness** (especially for RAG): does the answer only state what's actually supported by the retrieved/provided context, or does it add unsupported claims? Test by deliberately checking claims against source documents, not just "does it sound plausible."
- **Hallucination**: probe with questions where the honest answer is "I don't know" or "not in the provided context" — a model that confidently fabricates rather than admitting uncertainty is a specific, testable failure mode.
- **Consistency**: same/paraphrased input should produce semantically consistent output across repeated calls — flag if answers meaningfully contradict each other across runs on the same question.
- **Instruction adherence**: does it actually follow format constraints (JSON schema, length limits, required fields)? Validate programmatically (schema validation), don't eyeball it.
- **Context handling / long-context**: for long-context use cases, test "needle in a haystack" style — put a specific fact at various positions in a long context and confirm retrieval doesn't degrade in the middle (a documented failure mode across many models).

## RAG-specific testing
- **Retrieval quality**: are the retrieved chunks actually relevant to the query (precision), and does retrieval find the right chunk when it exists (recall)? Test retrieval in isolation from generation — a good generator can't fix bad retrieval.
- **Chunking/embedding sensitivity**: test whether chunk boundaries split relevant information awkwardly, causing retrieval misses.
- **Stale/conflicting sources**: if the corpus has outdated or contradictory documents, does the system surface the most authoritative/recent one, or does it get confused?

## Agent / tool-use testing
- **Tool selection correctness**: given a task, does the agent call the right tool with correctly-formed arguments? Test against a set of tasks with known-correct tool call sequences.
- **Error recovery**: when a tool call fails or returns unexpected output, does the agent retry sensibly, ask for clarification, or does it hallucinate a fake result and proceed?
- **Multi-step planning**: for tasks requiring multiple tool calls, verify the agent doesn't skip a required step or loop unproductively (see repetition/looping as a real failure mode, not just a hypothetical).
- **Multi-agent handoff**: if multiple agents/subagents collaborate, verify context is correctly passed at handoff and no information is silently dropped.

## Prompt injection & LLM security
- Test with adversarial inputs attempting to override system instructions ("ignore previous instructions...") embedded in user input **and** in any external content the model reads (documents, web pages, tool results) — injection via untrusted retrieved content is a distinct, often-overlooked attack surface from direct user-prompt injection.
- Verify the model doesn't leak its system prompt or internal tool definitions when asked directly or indirectly.
- Verify untrusted external content (search results, fetched pages, uploaded documents) is treated as data, never as instructions — this should be an explicit design property, testable by trying to get injected content to trigger an unintended action.
- See [[security-testing]] for the broader security-testing discipline this sits under.

## Regression testing across prompt/model versions
- Maintain a fixed eval set and re-run on every prompt change or model version bump — a "small prompt tweak" can silently regress an unrelated capability.
- Track cost and latency alongside quality — a prompt/model change that improves quality 2% but doubles token usage or latency is a real tradeoff to surface explicitly, not silently accept.

## Tools
- **promptfoo** — prompt regression testing/comparison across models and prompt versions, CLI-friendly.
- **DeepEval / Ragas** — RAG and LLM output evaluation metrics (faithfulness, answer relevancy, context precision/recall).
- **LangSmith** — tracing + eval dataset management for LangChain-based apps.
- **MLflow** (already set up here) — tracing, evaluation runs, and scorer definitions; use the local `mlflow` skills directly.

## Reporting
Report failures with the exact prompt, model/version, retrieved context (for RAG), and the specific property violated (hallucination, off-format, injection-succeeded) — see [[bug-reporting]]. Treat a successful prompt-injection or system-prompt leak as a Critical security finding, not a quality nit.

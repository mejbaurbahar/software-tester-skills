---
name: rag-evaluation-testing
description: Use when testing retrieval-augmented generation (RAG) — retrieval metrics (recall@k, MRR, nDCG), chunking and embedding evaluation, faithfulness/groundedness, answer relevancy, citation accuracy, abstention, freshness, access-control filtering, and Ragas/TruLens/DeepEval pipelines.
license: MIT
metadata:
  category: ai
  version: "2.0"
  tags: rag, retrieval, embeddings, ragas, groundedness, faithfulness, chunking, vector-search, citations, hallucination
---

# RAG Evaluation & Testing

RAG is two systems: **retrieval** (did we fetch the right evidence?) and **generation** (did we use it faithfully?). Evaluate them separately, then together.

## 1. Golden dataset
100+ questions, each with: question · reference answer · **gold source chunk/doc IDs** · type (factoid, multi-hop, comparison, numeric, not-in-corpus, ambiguous, permission-restricted) · difficulty. Sources: SME-written, real query logs, synthetic generation (Ragas `TestsetGenerator`) followed by human review. Keep 10–20% **unanswerable** questions.

## 2. Retrieval metrics (no LLM needed)
| Metric | Meaning |
| :--- | :--- |
| **Recall@k** | Is the gold chunk in the top-k passed to the LLM? (most important) |
| Precision@k | Share of retrieved chunks that are relevant (noise level) |
| **MRR** | 1 / rank of the first relevant result |
| **nDCG@k** | Rank-aware graded relevance |
| Coverage | Multi-hop: were *all* needed documents retrieved? |
```python
def recall_at_k(retrieved_ids, gold_ids, k):
    return len(set(retrieved_ids[:k]) & set(gold_ids)) / len(gold_ids)
```
Tune one variable at a time and keep a leaderboard: chunk size/overlap, embedding model, hybrid BM25 + dense, reranker, query rewriting, metadata filters, top-k.

## 3. Generation metrics
| Metric | Question | Tool |
| :--- | :--- | :--- |
| **Faithfulness / groundedness** | Is every claim supported by the retrieved context? | Ragas, TruLens, DeepEval |
| Answer relevancy | Does it answer what was asked? | Ragas |
| Context precision / recall | Judge-based retrieval quality | Ragas |
| Correctness | Matches the reference answer (exact match for numbers/dates) | Ragas, string checks |
| **Citation accuracy** | Does the cited source really contain the claim? | quote/substring check |
| Abstention | Says "I don't know" when the context lacks the answer | unanswerable subset |
```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
result = evaluate(dataset, metrics=[faithfulness, answer_relevancy, context_precision, context_recall])
```

## 4. Failure taxonomy (diagnose before fixing)
Retrieval miss (chunking, jargon/synonyms) · ranking problem (right doc at rank 12) · lost-in-the-middle · outdated or conflicting documents · hallucination despite good context · over-citation · truncated answers · table/number errors · multi-hop failure · language mismatch.

## 5. Non-obvious tests
- **Access control**: user A must never receive chunks from documents they cannot read — filter at *retrieval*, not after generation (`authn-authz-testing`).
- **Untrusted content**: instructions embedded in documents must not change assistant behaviour (`llm-security-audit`).
- **Freshness**: updated or deleted documents are reflected within the SLA; reindexing is idempotent; stale caches invalidated.
- **Privacy**: PII masked or excluded; erasure requests remove vectors too (`compliance-testing`).
- **Robustness**: paraphrases, typos, multilingual and very short/long queries return stable results.
- **Performance and cost**: retrieval p95 latency, index size, tokens per answer.

## 6. CI and production
PR: retrieval-only metrics (fast, deterministic) + a 30-question generation smoke set. Nightly: full evaluation. Gate on recall@k and faithfulness ≥ baseline. Production: log query/context/answer, collect feedback, sample for human review, alert on "no results" rate and faithfulness drift.

## Related
`llm-testing`, `ai-agent-evaluation`, `data-pipeline-etl-testing`, `database-testing`, `llm-security-audit`

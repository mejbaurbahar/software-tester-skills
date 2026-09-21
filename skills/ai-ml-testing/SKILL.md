---
name: ai-ml-testing
description: Use when testing a classical ML model or ML-powered feature — accuracy/precision/recall/F1 evaluation, model regression testing, bias/fairness testing, and ML pipeline robustness. For LLM/generative-AI-specific testing (prompts, hallucination, RAG), use llm-testing instead.
---

# AI / ML Testing

## Scope note
This skill covers classical/predictive ML (classification, regression, ranking, recommendation models). For generative/LLM-specific concerns (prompt testing, hallucination, RAG), see [[llm-testing]]; for conversational agents built on top, see [[chatbot-voice-agent-testing]].

## Core evaluation metrics — use the right one for the problem
- **Accuracy** — fraction correct; misleading on imbalanced classes (99% accuracy predicting "not fraud" on a 1%-fraud dataset is a useless model).
- **Precision** — of predicted positives, how many were actually positive; matters when false positives are costly (flagging a legit transaction as fraud).
- **Recall** — of actual positives, how many were caught; matters when false negatives are costly (missing an actual fraud case).
- **F1** — harmonic mean of precision/recall, useful single number when both matter and classes are imbalanced.
- **AUC-ROC / AUC-PR** — threshold-independent view of separability; prefer PR curve over ROC when the positive class is rare.
Pick the metric based on the business cost of each error type — report multiple metrics, never just accuracy alone, and always ask what the actual cost asymmetry is if it's not stated.

## Model regression testing
- Maintain a fixed evaluation set (not the live/growing training data) and re-run it on every model version — a metric that improves in aggregate can still regress badly on a specific important slice.
- **Slice-based evaluation**: break down metrics by relevant segments (user cohort, input length, language, demographic where applicable for fairness) — an aggregate metric can hide a model that got much worse for a specific group while improving overall.
- Compare against the **previous production model**, not just an absolute threshold — "3% accuracy" means nothing without a baseline to compare against.

## Bias & fairness testing
- Test predictions across protected/sensitive attribute groups (where legally/ethically appropriate to test) for disparate outcome rates — a model can be "accurate overall" while systematically disadvantaging a subgroup.
- Test with adversarial/edge-case inputs specifically constructed to probe known bias patterns for the domain (e.g. name-based bias in resume screening, dialect bias in NLP).
- This is a domain requiring real expertise beyond automated metrics — flag when a finding needs human fairness/ethics review rather than resolving it purely with a numeric threshold.

## Robustness testing
- **Input perturbation**: small, realistic changes to input (typos, reordering, noise in image/audio) shouldn't cause wildly different predictions — a model that flips output on a single-character typo is brittle.
- **Adversarial examples**: deliberately crafted inputs designed to fool the model — relevant when the model is exposed to potentially adversarial users (spam/fraud detection, content moderation).
- **Out-of-distribution inputs**: inputs unlike anything in training data should ideally produce low-confidence outputs or a graceful fallback, not a confident wrong answer.

## Pipeline & data testing (often more bugs live here than in the model itself)
- **Training/serving skew**: feature computation must be identical between training and serving paths — a common, high-impact bug class where a model performs well offline but poorly in production because a feature is computed differently at inference time.
- **Data drift monitoring**: input distribution in production diverging from training distribution degrades model performance silently — needs ongoing monitoring, not a one-time check.
- **Label leakage**: a feature that's only available *because* the outcome already happened (leaking the answer into training) produces unrealistically good offline metrics that won't hold in production — actively look for this in any surprisingly high score.

## Reporting
Report metrics with their evaluation set, slice breakdown, and comparison baseline — a bare number ("92% accurate") is not a usable finding. See [[bug-reporting]] and [[test-data-engineering]] for golden-dataset construction discipline.

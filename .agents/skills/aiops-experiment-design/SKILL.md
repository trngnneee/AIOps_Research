---
name: aiops-experiment-design
description: Design reproducible AIOps pilots and evaluations, including RCA benchmarks, evidence annotations, fair baselines, budgets, ablations, and incident-level uncertainty. Use before experiments or when auditing an evaluation protocol; this skill does not authorize running infrastructure or paid experiments.
---

# AIOps experimental protocol

Read `AGENTS.md`, the current RQ and roadmap. Produce a protocol that can refute the hypothesis, not merely demonstrate a working pipeline. If data or baseline access is unknown, start with an artifact inspection and one reproducible episode before proposing a larger run.

## Task and data

- Define incident input, time window, allowed tools, output, fault scope, evaluator-only labels, and the independent unit. Separate root component/mechanism from symptoms.
- Specify available information over time and budget. Distinguish not yet queried, temporarily unavailable, missing, and stale evidence. Keep evaluator fault plans and injector shortcuts out of agent views.
- Split development/test by original incident before constructing views or repetitions. Related variants and repeated model calls are not independent incidents. Record model/version, prompts, dataset/version, code commit, seeds where supported, tool responses, and environment reset.
- Require real pre/post history, resource identity/version and timestamps for stale conditions. If unavailable, drop the stale claim or explicitly label an artificial perturbation study; never present edited timestamps as realistic delayed telemetry.

## Oracle and comparison

- Define answerability relative to allowed observations and budget. Use independently justified labels, an annotation guide, disagreement resolution and an unknown category; a model evaluating its own answer is not an independent oracle.
- For sufficiency claims, document competing causes and the observation that distinguishes them. Use two human annotations where feasible; disclose single-reviewer limits and perform sensitivity checks.
- Match task, model, tools, available information and total budget across methods. Include a base agent, self-check where relevant, nearest runnable verification method, and a simple provenance/time rule. Record adapters rather than claiming exact reproduction.
- Ablate components whose benefit is claimed. Charge verifier/retries, extra queries, waiting, tokens, latency and API cost to the whole episode. Set stopping rules before test evaluation.

## Analysis and acceptance

For selective RCA, specify valid output parsing; RCA accuracy, coverage, selective error at matched coverage, unsupported commitments on verified ambiguous cases, unnecessary abstention on answerable cases, evidence validity, and total cost. Keep malformed outputs and timeouts visible; never silently drop them. Report selective error as undefined when coverage is zero, not perfect accuracy. Compare methods at thresholds chosen on development data.

Use paired incident comparisons when appropriate. Estimate uncertainty at the original-incident level (for example clustered bootstrap), report counts and fault-family breakdowns, and separate exploratory pilot findings from confirmatory claims. Repetitions measure variability, not a larger independent sample. Choose sample size from the decision, pilot variance and resources; do not promise statistical power from 12–20 incidents.

Return: task/data contract, annotation plan, baseline/ablation table, budget, metrics and failure policy, reproducibility records, pilot acceptance/go-no-go criteria, and unresolved blockers. Start with one replay, then a small pilot only when feasible. Write `research/experimental-protocol.md` if requested; do not run experiments just to fill a protocol.

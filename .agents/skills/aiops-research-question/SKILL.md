---
name: aiops-research-question
description: Develop and challenge feasible AIOps thesis research questions from papers and pilot evidence. Use for candidate gaps, novelty checks, problem selection, and go/no-go decisions; do not treat a roadmap or an untested pipeline as established novelty.
---

# From evidence to research question

Read `AGENTS.md`, the current roadmap, relevant reading reports and findings. Separate established evidence, unverified findings, resource constraints, and preferences. The default audience is a two-person thesis team; the current RCA direction is revisable.

## Build and challenge candidates

- Identify a concrete failure or unresolved comparison, who it affects, and why existing evidence cannot settle it. “Combine verifier + abstention” is a design idea, not itself a research gap.
- Find the nearest methods, including differently named work. For each novelty claim record what the source actually establishes and its section/version. Without close full-text comparisons, label novelty provisional and identify the missing check.
- Form a question with a defined population/task, intervention or condition, comparator, observable outcome, and resource budget. Separate the question from a preferred solution and distinguish descriptive, predictive, and causal claims.
- State a falsifiable hypothesis and the null/negative result that would change the decision. A careful robustness study or benchmark audit can be a valid contribution; don't force a new algorithm.
- Check accessible data, independent incidents, oracle validity, runnable baseline, compute/API budget, and time. Unknown feasibility becomes a pilot question rather than an optimistic assumption.

## Return a decision memo

Offer up to three materially different candidates when evidence supports them. For each give: RQ; nearest work and evidence; candidate contribution; measurement and comparator; minimum pilot; feasibility blockers; falsifier; continue/narrow/stop criteria.

Rank qualitatively by evidence of an unresolved issue, scientific value, and feasibility; explain the tradeoff instead of inventing numeric scores. Recommend one primary RQ and only necessary secondary questions. Include evidence against the recommendation and the next cheapest decision-changing check. Do not announce the topic as approved by the supervisor.

For the current roadmap, verify missing versus unqueried evidence, genuine stale history, matched coverage/budget, and whether simple provenance/time rules already suffice. If these undermine the direction, propose narrowing or changing it explicitly.

Save to `research/research-question-memo.md` only when asked. Do not silently rewrite the roadmap to match a new suggestion.

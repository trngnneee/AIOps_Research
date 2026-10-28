---
name: aiops-literature-review
description: Search and synthesize AIOps, cloud RCA, observability, and agent research with traceable citations. Use for literature searches, related-work matrices, and evidence-backed gap checks across papers, rather than explaining one paper section.
---

# AIOps literature review

Read the project `AGENTS.md` and current roadmap. Start from the research decision the review must inform; do not assume the proposed gap exists.

## Search and screen

1. Define the task, inclusion/exclusion criteria, cutoff date, and review type. Default to a focused scoping review; reserve “systematic” for a documented systematic process.
2. Build queries across task, mechanism, and evaluation terms. For the current direction include RCA/root cause diagnosis, evidence sufficiency/abstention/selective prediction, partial observability/missing or stale telemetry, temporal validity/provenance, and tool-using agents. Search beyond papers sharing the proposed method's name.
3. Start with roadmap seeds, then complementary scholarly indexes, arXiv, relevant systems/ML venues, and backward/forward citation chaining as available. Use original papers and official artifacts for claims. Log exact query, service, date, screening scope, and access limits; don't invent hit counts for ranked web results.
4. Deduplicate by DOI/arXiv ID and title; link preprint and published versions rather than treating them as independent evidence. Record exclusions with reasons. Inaccessible full text stays unresolved, not excluded for an assumed methodological flaw.
5. Inspect full text and supplements for close competitors. Inspect code only where implementation details affect the comparison; record commit and whether behavior was read or actually run.

## Deliverable

Return a short synthesis by research issue, a prioritized reading queue, search log, and a compact comparison matrix. Matrix fields: source/version; task and inputs/outputs; mechanism; agent-visible evidence versus evaluator oracle; dataset and independent unit; baselines/budget; metrics; missing/stale conditions; limitation and source location; decision for this thesis.

Use `unknown/not checked` for empty evidence, not `no`. Distinguish author claims from demonstrated results. Citation metadata confirms identity, not support for a claim. Verify both before citing. State search coverage limits and counterevidence to the candidate gap.

If asked to save, use `research/related-work.md` and `research/literature-search-log.md`, or update the existing equivalents. Keep reading reports as single-paper records.

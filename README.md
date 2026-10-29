# Writing Maestro

A skill-orchestration project for selecting **existing third-party writing and prompting skills** according to task intent and context. It is not a writing engine and does not imply that the listed external skills have been installed or validated.

## Current state
Research and comparison in progress. No skill registry is approved and no runtime orchestrator has been implemented.

## Research archive
- `research/snapshots/2026-10-28/`: preserved candidate inventories and previous research artifacts.
- `research/comparisons/`: head-to-head comparison evidence, merge/split decisions, and unresolved questions.

**Method:** discover broadly; compare SKILL.md behavior, inputs, outputs, method, boundaries and dependencies; allow clusters to merge or split; then prune primarily *within* substitutable functional clusters. Distinct roles may coexist in the same neighborhood, and highly redundant roles compete harder. Cluster sizes and the total roster have no fixed quotas; the current planning range is **30–60**, subject to actual usefulness and dependency constraints. Labels are provisional, not a predefined taxonomy.

The source repositories linked in the research artifacts remain the authorities for their respective third-party skills. No third-party code or SKILL.md content is installed here.

## Current comparison data

See [`research/normalization/README.md`](research/normalization/README.md) for evidence-aware I/P/O functional profiles, the flat CSV comparison matrix, similarity-driven candidate pairs, coverage and unresolved verification. Existing cluster labels are historical and not an input feature.

## Provisional registry shortlist

The current selection research is [`research/selection/`](research/selection/README.md). The v3 proposal has **58** candidates from 405 sources; these are not installed or runtime validated. Older versions and all excluded candidates are preserved.

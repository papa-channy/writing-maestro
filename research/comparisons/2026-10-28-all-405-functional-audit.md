# Completing source reads for all 405 candidates — evidence report

Date: 2026-10-28 (Asia/Seoul). Scope: previously unread **305** skills. **No third-party skill executed or installed.** No cluster assignment or registry approval.

## Collection and provenance

- Previously read: 100 primary SKILL.md source bodies, with individual SHA references.
- Newly accessed: 305/305 source bodies, in 20 source-evidence batches. All 18 first-pass failures were recovered; 6 required correcting stale source paths, 12 required fixing an end-of-file extraction bug.
- Source metadata, headings, section excerpts, line numbers, and blob hashes are recorded under `research/normalization/evidence/remaining/`. Original inventory paths were preserved independently.

## Functional profiles

The canonical records are now in `functional_profiles.json`. To avoid false precision, two levels are distinguished:

**100 `ANALYST_FUNCTIONAL`** — explicit analyst abstractions of inputs, ordered transformation, and outputs based on read instructions.

**305 `SOURCE_DERIVED_FUNCTIONAL`** — machine-extracted input/output/operation snippets plus source-declared task intent and effect. Not yet individually checked for false-positive sections, implicit contractual inputs, or full procedure coverage. These are useful to **generate candidate comparisons**, not enough to certify interchangeability.

Across the combined 405 records, **269** have no concrete extracted input field, **105** have no extracted ordered operation, and **267** have no concrete output field. These unknowns are deliberately retained. They indicate extraction gaps or underspecified source conventions rather than absence of an actual capability. All 305 new candidates nevertheless have source-declared function descriptions and SHA provenance; no fabricated I/O contracts were inserted.

## Newly prominent neighbors — NOT a clustering decision

Source-text / normalized I-P-O similarity yields candidates for comparing actual behavior, not quality or independent capability. Examples:

| Pair | Relevant question |
|---|---|
| Anthropic `doc-coauthoring` vs Sentry `doc-coauthoring` | Do the two variants differ in setup or reader-test mechanics despite identical prior analyst abstracts? |
| K-Dense `paper-lookup` vs Kalaris `paper-lookup` | Is one a fork or modified version with different dependencies and failure semantics? |
| `create-implementation-plan` vs `update-implementation-plan` | Text appears very close, but creation and updating an existing artifact may be two non-interchangeable operations. |
| K-Dense vs Kalaris `scientific-brainstorming` | Inspect independence and deliberation stages and any divergence of source requirements. |
| K-Dense vs Kalaris `research-lookup` | Compare evidence packet schema, citation checks and source limitations. |
| `grill-with-docs` vs `grill-me` | The former mentions producing ADR/glossary artifacts; compare actual tool delegation and side effects. |

Git blob SHA equality reported zero exact duplicate source files in this snapshot. This does **not** mean the 405 behaviors are all distinct, nor does it prove no near-verbatim or derived copies exist.

## Required before next cluster selection

1. Compare close neighbors by actual input/output contract and required side effects before any automatic merge.
2. For source-derived records, review the referenced lines and source body before adopting any extracted step as an operative procedure.
3. Disambiguate core writing/authoring methods from research retrieval, format converters, tool dependencies, and subagent routers; keep adjacent candidates documented rather than deleting them.
4. Emerge clusters from evidenced similarities and differences; permit merging or splitting. Former 24 clusters are archival, not an input.
5. Keep any runtime quality/safety evaluations for registry finalists, as agreed.

## Navigation

- [Full 405 profiles](../normalization/functional_profiles.json)
- [Compact 405 profiles](../normalization/functional_profiles_compact.json)
- [Comparable CSV](../normalization/functional_matrix.csv)
- [300 similarity neighbors](../normalization/similarity_neighbors.csv)
- [Source normalization README](../normalization/README.md)

Status: **source retrieval 405/405 complete; semantic validation of 305 automatic signatures not complete; no finalists approved.**

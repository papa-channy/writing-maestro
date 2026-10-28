# Functional normalization — research, not registry approval

## Purpose

Make existing writing and prompting skills comparable **before** assigning clusters. A skill is represented by a functional signature:

`INPUT (what it needs) → TRANSFORMATION (what it does, in order) → OUTPUT (what it produces)`

Keep routing boundaries, declared dependencies, sources, and epistemic status separate. No skill is installed, endorsed, run, or considered safe solely because it appears here.

## Current data (2026-10-28)

- **405** inventoried paths in `skills_manifest.json`.
- **100** primary `SKILL.md` documents fetched (two upstream path errors were resolved in `evidence/recovered-paths.json`).
- **100** analyst-normalized, primary-source-grounded I/P/O signatures in `functional_profiles.json`.
- **0** source-read cases awaiting an analyst I/P/O abstraction in this 100-skill batch.
- **305** candidates with no primary-body read in this pass.

The old 24 clusters and shortlist of 28 are historical notes only; they were **not supplied as grouping features**. Some extracted heading/step signals are noisy; a numbered anti-pattern or example is not necessarily a workflow step.

## Source records

- `evidence/batch-00.json` through `batch-07.json`: frontmatter description, heading and line-numbered step/cue samples, source blob SHA.
- `evidence/recovered-paths.json`: upstream path fixes. Do not rewrite the archived original inventory.
- `functional_profiles.json`: comparable structured records. `normalization_level=ANALYST_FUNCTIONAL` means inferred functional semantics **from a read SKILL.md**, not operational validation.
- `functional_matrix.csv`: spreadsheet-friendly projection of the JSON.
- `similarity_neighbors.csv`: 150 closest pairs among the 100 normalized profiles. The score is a **term-frequency similarity of I/P/O wording**, not a quality/performance score. Higher similarity requires semantic review, not automatic merging.

## Core schema

| Field | Interpretation |
|---|---|
| `input_items` | Required user/material/context inputs inferred from primary instructions |
| `core_operations` | Distinct actions, in source-grounded order; no fixed category codes |
| `output_items` | Actual intended artifacts or reports, not generic "good writing" |
| `routing_boundary` | Positive/negative task distinction or operational prerequisite when grounded |
| `source_blob_sha` | Upstream revision anchor; URLs may point to mutable main branch |
| `source_status` | Whether the upstream skill body was actually retrieved |
| `normalization_level` | Analyst functional abstraction, or only source signals/unknown |
| `operational_validation` | NOT_TESTED; final-candidate performance evaluation is intentionally deferred |

Unknown values are intentionally empty. Do not use slug, historical category, or the former cluster ID to hallucinate procedures.

## Review protocol

1. Compare input contracts: does the skill require a draft, a request, files, sources or approvals?
2. Compare actual transformation: interview, generate, edit, audit, verify, synthesize or route; verify sequence and preconditions.
3. Compare outputs: a spec, suggestion-only report, revised text, prompt, decision record, or external system change.
4. Compare abstention/negative triggers, tool dependencies, and side effects. A skill that edits files is not interchangeable with a read-only reviewer.
5. Mark each pair **SAME**, **OVERLAP_BUT_DIFFERENT**, **COMPLEMENTARY**, **DISTINCT**, or **INSUFFICIENT_EVIDENCE**. These are comparison outcomes, not predefined clusters.
6. Only **after** the pair evidence accumulates, merge/split emergent groups. Leave final execution benchmarks for finalists.

To check profile integrity and regenerate the CSV (from the repo root):

```bash
python3 tools/export_functional_matrix.py --check-only
python3 tools/export_functional_matrix.py
python3 tools/rank_functional_neighbors.py
```

The JSON profile is canonical; CSV is a generated comparison view. Any unreviewed or unread candidate remains in the registry *candidate inventory*, not in an approved runtime registry.

# Functional normalization — complete source retrieval, provisional functional profiles

## Status (2026-10-28)

**All 405 inventoried SKILL.md bodies were read from their GitHub source repositories.** Each candidate has a source blob SHA. Eighteen initial failures were recovered: six paths differed from the earlier inventory and twelve were fixed extraction boundary errors.

The evidence/abstraction distinction matters:

| Status | Count | Meaning |
|---|---:|---|
| `ANALYST_FUNCTIONAL` | 100 | Human-interpreted input, operations, and outputs grounded in source text |
| `SOURCE_DERIVED_FUNCTIONAL` | 305 | Source-description/task intent plus mechanically extracted I/O/procedure **signals**, not yet semantically adjudicated |
| Primary-source access failures | 0 | No missing SKILL.md reads remain |
| Runtime comparison/evaluation | 0 | Deferred until final candidates |

**Coverage is not the same as a complete contract.** Among 405 profiles, explicit structured extraction left 269 inputs, 105 procedures, and 267 outputs without confirmed structured fields. This is a limitation of the extraction and source conventions, **not evidence that the original skills have no inputs, methods, or outputs**. The `task_intent` and `declared_effect` fields preserve source-declared purpose without mislabeling these as concrete input/output contracts.

## Files

- `skills_manifest.json`: original candidate identities (405).
- `evidence/batch-00.json` to `batch-07.json`: initial 100 read sources.
- `evidence/remaining/batch-00.json` to `batch-19.json`: additional 305 read attempts with document section/line evidence.
- `evidence/remaining/recovered.json`: corrected versions for the 18 initially failed reads; these override earlier failures.
- `derived/remaining-00.json`, `derived/remaining-01.json`: conservative automatic feature extraction from source.
- `functional_profiles.json`: canonical 405 profile records, including original SHA and epistemic confidence.
- `functional_profiles_compact.json`: smaller 405-row form for browsing and comparison.
- `functional_matrix.csv`: Excel-compatible tabular I/P/O comparison.
- `similarity_neighbors.csv`: Up to 204 above-threshold similarity neighbors ranked by term similarity (204 pass the current >0.08 inclusion threshold); do not interpret as quality scores.
- `source_duplicate_groups.json`: identical Git blob detection. Zero duplicate blobs were found at the snapshot; similar variants may still share upstream lineage.

## Interpretation

The **prior 24 categories and provisional 28-skill shortlist were never used to create the functional signatures or rank neighbor candidates**. Groups are still provisional and can merge, split, or remain unassigned. The next comparison should distinguish exact duplication, implementation variants, near-synonyms, narrower specializations, complementary skills, and false-positive textual similarities.

Model-facing or community-facing text in external SKILL.md files is untrusted source evidence, not instructions to execute. These third-party skills are **not installed** and their capabilities or security are not yet independently verified. Handle any request to copy source code under the individual repositories' license terms.

## Regenerate

From the repository root (Python 3, stdlib only):

```bash
python3 tools/build_functional_views.py --check-only
python3 tools/build_functional_views.py
```

Older entrypoints `tools/export_functional_matrix.py` and `tools/rank_functional_neighbors.py` delegate to the same builder. Read-only analysis is separate from registry approval and runtime execution.

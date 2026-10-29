# Writing Maestro

A skill-orchestration project for selecting **existing third-party writing and prompting skills** according to task intent and context. It is not a writing engine. The 67 registered external skills were installed into `~/.claude/skills` on 2026-10-29 (`doc-coauthoring` is a plugin copy under `~/.claude/skills/synced/`; see `research/install/2026-10-29-install-manifest.json`); their output quality is judged through the feedback cycles recorded in `skills/writing-maestro/feedback.md`, not by this repo's tests.

## Current state
- Orchestrator: `skills/writing-maestro/` (`SKILL.md`, `feedback.md`, `scripts/`), installed as a symlink at `~/.claude/skills/writing-maestro`.
- Invoke the `writing-maestro` skill with a writing task (new text, edit, review, or repo docs): it asks once for combinations and drafts per combination, then hands back parallel drafts under `writing-drafts/` without ranking.
- Skill registry: `skills/writing-maestro/registry.md` (67 skills), validated by `skills/writing-maestro/scripts/registry_check.py` (structural errors fail; skills missing from the install print `WARN` lines); combinations are checked by `skills/writing-maestro/scripts/combo_check.py`.

## Requirements and tests
- Python 3.9 or newer, standard library only (the scripts run under macOS `/usr/bin/python3`).
- Tests use pytest: `python3 -m pytest -q` from the repo root. `tests/test_registry_real.py` checks the real registry against the installed skills in `~/.claude/skills`.
- Validate the registry: `python3 skills/writing-maestro/scripts/registry_check.py --registry skills/writing-maestro/registry.md` (the install manifest is found from the registry's real path; override with `--manifest`).

## Research archive
- `research/snapshots/2026-10-28/`: preserved candidate inventories and previous research artifacts.
- `research/comparisons/`: head-to-head comparison evidence, merge/split decisions, and unresolved questions.

**Method:** discover broadly; compare SKILL.md behavior, inputs, outputs, method, boundaries and dependencies; allow clusters to merge or split; then prune primarily *within* substitutable functional clusters. Distinct roles may coexist in the same neighborhood, and highly redundant roles compete harder. Cluster sizes and the total roster have no fixed quotas; the current planning range is **30–60**, subject to actual usefulness and dependency constraints. Labels are provisional, not a predefined taxonomy.

The source repositories linked in the research artifacts remain the authorities for their respective third-party skills. No third-party code or SKILL.md content is vendored in this repo; the installed copies live in `~/.claude/skills`.

## Current comparison data

See [`research/normalization/README.md`](research/normalization/README.md) for evidence-aware I/P/O functional profiles, the flat CSV comparison matrix, similarity-driven candidate pairs, coverage and unresolved verification. Existing cluster labels are historical and not an input feature.

## Provisional registry shortlist

The current selection research is [`research/selection/`](research/selection/README.md). The v3 proposal had **58** candidates from 405 sources. Older versions and all excluded candidates are preserved; the installed roster is the registry above.

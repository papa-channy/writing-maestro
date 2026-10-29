"""Acceptance tests against the real skills/writing-maestro/registry.md."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "skills" / "writing-maestro" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from registry_lib import parse_registry, validate  # noqa: E402
from registry_check import installed_from_manifest  # noqa: E402
from combo_check import check_combo  # noqa: E402

REGISTRY = ROOT / "skills" / "writing-maestro" / "registry.md"
MANIFEST = ROOT / "research" / "install" / "2026-10-29-install-manifest.json"
SKILLS_DIR = Path("~/.claude/skills").expanduser()


def load():
    return parse_registry(REGISTRY.read_text(encoding="utf-8"))


def test_registry_valid():
    reg = load()
    assert validate(reg, installed_from_manifest(MANIFEST), SKILLS_DIR) == []


def test_known_conflict():
    assert check_combo(load(), ["general-writing", "prose-naturalizer"]).ok is False


def test_bundle_paper_flow():
    r = check_combo(load(), ["paper-writing", "academic-voice", "general-writing"])
    assert r.ok is True, r.conflicts


def test_copy_plus_humanizer_precedence():
    reg = load()
    r = check_combo(reg, ["copywriting", "humanizer"])
    assert r.ok and any(s == "humanizer" for s in r.precedence.values())


def test_clarify_stage_skills():
    reg = load()
    for name in [
        "interview-me", "requirements-clarity", "idea-refine",
        "brand-profile", "voice-builder", "awesome-content-voice",
    ]:
        assert "clarify" in reg.skills[name].stages, name


def test_check_stage_skills():
    reg = load()
    for name in ["citation-verification", "docs-sync-audit"]:
        assert "check" in reg.skills[name].stages, name


def test_every_skill_has_primary():
    reg = load()
    assert [n for n, s in reg.skills.items() if not s.primary] == []


def test_cluster_column_matches_primary():
    """측면 표 4번째 칸(클러스터)은 스킬 항목의 주 측면과 일치해야 한다."""
    reg = load()
    text = REGISTRY.read_text(encoding="utf-8")
    section = text.split("\n## 측면\n", 1)[1].split("\n## ", 1)[0]
    rows = [ln.strip().strip("|").split("|") for ln in section.splitlines() if ln.startswith("|")][2:]
    for cells in rows:
        aspect, owners = cells[0].strip(), {c.strip() for c in cells[3].split(",") if c.strip()}
        expected = {n for n, s in reg.skills.items() if aspect in s.primary}
        assert owners == expected, aspect

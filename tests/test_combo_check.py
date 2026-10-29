import json
import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "skills" / "writing-maestro" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from registry_lib import parse_registry  # noqa: E402
from combo_check import check_combo  # noqa: E402

FIXTURE = Path(__file__).parent / "fixtures" / "registry_min.md"
TEXT = FIXTURE.read_text(encoding="utf-8")
reg = parse_registry(TEXT)


def variant(skill, old, new, text=TEXT):
    """Replace `old` with `new` only inside the given skill's section."""
    head, sep, rest = text.partition(f"### {skill}\n")
    body, nxt, tail = rest.partition("\n### ")
    assert old in body, (skill, old)
    return head + sep + body.replace(old, new, 1) + nxt + tail


def test_primary_overlap_conflicts():
    r = check_combo(reg, ["general-writing", "prose-naturalizer"])
    assert not r.ok
    assert "primary overlap prose-edit: general-writing, prose-naturalizer" in r.conflicts


def test_bundle_companion_allowed():
    reg2 = parse_registry(variant("humanizer", "- 주 측면: ai-tells", "- 주 측면: ai-tells, prose-edit"))
    r = check_combo(reg2, ["general-writing", "humanizer"])
    assert r.ok, r.conflicts


def test_precedence_primary_owner():
    r = check_combo(reg, ["copywriting", "humanizer"])
    assert r.ok and r.precedence == {"ai-tells": "humanizer"}
    assert ("copywriting", "ai-tells") in r.ignored


def test_precedence_last_secondary():
    t = variant("copywriting", "- 부 측면: ai-tells", "- 부 측면: voice")
    t = variant("humanizer", "- 부 측면: 없음", "- 부 측면: voice", text=t)
    reg3 = parse_registry(t)
    r = check_combo(reg3, ["copywriting", "humanizer"])
    assert r.precedence == {"voice": "humanizer"}
    assert r.ignored == [("copywriting", "voice")]
    r = check_combo(reg3, ["humanizer", "copywriting"])
    assert r.precedence == {"voice": "copywriting"}
    assert r.ignored == [("humanizer", "voice")]


def test_forbidden_pair():
    reg2 = parse_registry(variant("prose-naturalizer", "- 금지 짝: manuscript-writing", "- 금지 짝: copywriting"))
    r = check_combo(reg2, ["copywriting", "prose-naturalizer"])
    assert not r.ok and "forbidden pair copywriting+prose-naturalizer" in r.conflicts


def test_too_many_generation():
    reg2 = parse_registry(variant("general-writing", "- 필수 동반: humanizer", "- 필수 동반: 없음"))
    r = check_combo(reg2, ["general-writing", "humanizer", "prose-naturalizer", "copywriting"])
    assert r.generation_count == 4
    assert "too many generation skills: 4" in r.conflicts


def test_companion_not_counted():
    r = check_combo(reg, ["general-writing", "humanizer"])
    assert r.generation_count == 1


def test_clarify_in_combo():
    reg2 = parse_registry(variant("copywriting", "- 단계: draft", "- 단계: clarify"))
    r = check_combo(reg2, ["copywriting"])
    assert not r.ok and "clarify-stage skill in combo: copywriting" in r.conflicts


def test_unknown_skill():
    r = check_combo(reg, ["nope", "copywriting"])
    assert not r.ok and "unknown skill nope" in r.conflicts


def test_runtime_missing_command():
    reg2 = parse_registry(variant("copywriting", "- 필수 명령: 없음", "- 필수 명령: definitely-not-a-cmd-xyz"))
    assert check_combo(reg2, ["copywriting"]).ok
    r = check_combo(reg2, ["copywriting"], check_runtime=True)
    assert not r.ok
    assert r.missing_commands == ["copywriting:definitely-not-a-cmd-xyz"]


def test_cli_json(tmp_path):
    cmd = [sys.executable, str(SCRIPTS / "combo_check.py"), "--registry", str(FIXTURE)]
    bad = subprocess.run(cmd + ["general-writing", "prose-naturalizer"], capture_output=True, text=True, cwd=tmp_path)
    assert bad.returncode == 1
    assert json.loads(bad.stdout)["ok"] is False
    good = subprocess.run(cmd + ["copywriting", "humanizer"], capture_output=True, text=True, cwd=tmp_path)
    assert good.returncode == 0
    assert json.loads(good.stdout)["precedence"] == {"ai-tells": "humanizer"}


# --- closure evaluation: rules of companions a member invokes on its own ---

def _copy_requires_humanizer(text=TEXT):
    return variant("copywriting", "- 필수 동반: 없음", "- 필수 동반: humanizer", text=text)


def test_closure_overlap_conflict():
    # copywriting itself owns only persuasion, but its companion humanizer owns ai-tells.
    reg2 = parse_registry(_copy_requires_humanizer())
    r = check_combo(reg2, ["copywriting", "prose-naturalizer"])
    assert not r.ok
    assert "primary overlap ai-tells: copywriting, prose-naturalizer" in r.conflicts


def test_shared_single_source_not_conflict():
    # general-writing and copywriting both bring the same humanizer: one source, no conflict.
    reg2 = parse_registry(_copy_requires_humanizer())
    r = check_combo(reg2, ["general-writing", "copywriting"])
    assert r.ok, r.conflicts


def test_closure_precedence_winner():
    # copywriting's secondary ai-tells follows general-writing, whose closure (humanizer) owns it.
    r = check_combo(reg, ["copywriting", "general-writing"])
    assert r.ok, r.conflicts
    assert r.precedence["ai-tells"] == "general-writing"
    assert ("copywriting", "ai-tells") in r.ignored


def test_forbids_via_closure():
    reg2 = parse_registry(variant("prose-naturalizer", "- 금지 짝: manuscript-writing", "- 금지 짝: humanizer"))
    r = check_combo(reg2, ["prose-naturalizer", "general-writing"])
    assert not r.ok
    assert "forbidden pair prose-naturalizer+humanizer(via general-writing)" in r.conflicts


def test_own_closure_forbids_exempt():
    # general-writing forbids humanizer but already invokes it itself (own closure).
    t = variant("general-writing", "- 금지 짝: 없음", "- 금지 짝: humanizer")
    reg2 = parse_registry(_copy_requires_humanizer(t))
    assert check_combo(reg2, ["general-writing"]).ok
    r = check_combo(reg2, ["general-writing", "copywriting"])
    assert not any(c.startswith("forbidden pair") for c in r.conflicts), r.conflicts


def test_siblings_sharing_a_companion_not_coordinated():
    # Same bundle, both require humanizer, both own prose-edit: sharing a companion
    # does not mean either one sequences the other.
    t = _copy_requires_humanizer()
    t = variant("copywriting", "- 묶음: 없음", "- 묶음: msimchowitz", text=t)
    t = variant("copywriting", "- 주 측면: persuasion", "- 주 측면: persuasion, prose-edit", text=t)
    r = check_combo(parse_registry(t), ["general-writing", "copywriting"])
    assert not r.ok
    assert "primary overlap prose-edit: general-writing, copywriting" in r.conflicts

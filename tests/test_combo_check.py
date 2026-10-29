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

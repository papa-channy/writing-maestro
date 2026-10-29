import subprocess
import sys
from pathlib import Path

SCRIPT = (
    Path(__file__).resolve().parent.parent
    / "skills" / "writing-maestro" / "scripts" / "registry_lookup.py"
)
FIXTURE = Path(__file__).parent / "fixtures" / "registry_min.md"
TEXT = FIXTURE.read_text(encoding="utf-8")


def run(*args):
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--registry", str(FIXTURE), *args],
        capture_output=True, text=True, encoding="utf-8",
    )


def entry(name):
    """The fixture's `### name` section, verbatim, without trailing blank lines."""
    _, _, rest = TEXT.partition(f"### {name}\n")
    body = rest.split("\n### ", 1)[0]
    return (f"### {name}\n" + body).rstrip("\n")


def test_summary_one_line_per_skill():
    r = run("--summary")
    assert r.returncode == 0, r.stderr
    lines = r.stdout.strip("\n").split("\n")
    assert len(lines) == 4
    assert [ln.split(" | ")[0] for ln in lines] == [
        "general-writing", "humanizer", "prose-naturalizer", "copywriting",
    ]


def test_summary_fields():
    lines = run("--summary").stdout.strip("\n").split("\n")
    gw = lines[0].split(" | ")
    assert gw == [
        "general-writing", "prose-edit", "voice", "prose", "new, edit, docs",
        "msimchowitz", "초안을 더 명료하고 사람다운 문장으로 고친다",
    ]
    pn = lines[2].split(" | ")
    assert pn[1] == "ai-tells, prose-edit"
    assert pn[2] == "없음"
    assert pn[5] == "없음"


def test_skill_full_entry_verbatim():
    r = run("--skill", "humanizer")
    assert r.returncode == 0, r.stderr
    assert r.stdout.rstrip("\n") == entry("humanizer")


def test_skill_multiple_in_requested_order():
    r = run("--skill", "copywriting", "general-writing")
    assert r.returncode == 0, r.stderr
    out = r.stdout
    assert entry("copywriting") in out and entry("general-writing") in out
    assert out.index("### copywriting") < out.index("### general-writing")
    # The last entry in the file must not swallow anything after it.
    assert out.count("### ") == 2


def test_unknown_skill_exits_1():
    r = run("--skill", "humanizer", "no-such-skill")
    assert r.returncode == 1
    assert "no-such-skill" in r.stderr
    assert r.stdout == ""

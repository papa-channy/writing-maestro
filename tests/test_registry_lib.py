import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "skills" / "writing-maestro" / "scripts"))

from registry_lib import install_warnings, parse_registry, validate  # noqa: E402

FIXTURE = Path(__file__).parent / "fixtures" / "registry_min.md"
ALL = {"general-writing", "humanizer", "prose-naturalizer", "copywriting"}


def make_dirs(tmp_path, names=ALL):
    for n in names:
        (tmp_path / n).mkdir(exist_ok=True)


def reg_from(text):
    return parse_registry(text)


def test_parse_fixture():
    reg = parse_registry(FIXTURE.read_text(encoding="utf-8"))
    assert set(reg.aspects) == {"prose-edit", "ai-tells", "persuasion", "voice"}
    assert len(reg.stages) == 6
    assert reg.skills["general-writing"].primary == ["prose-edit"]
    assert reg.skills["general-writing"].requires == ["humanizer"]
    assert reg.skills["prose-naturalizer"].forbids == ["manuscript-writing"]
    assert reg.skills["humanizer"].wm_id == "companion"
    assert reg.skills["humanizer"].bundle == "msimchowitz"
    assert reg.skills["copywriting"].bundle is None
    assert reg.skills["copywriting"].commands == []
    assert reg.skills["general-writing"].evidence["voice"].startswith("preserving")
    assert reg.bundles["msimchowitz"] == ["general-writing", "humanizer"]


def test_fixture_valid(tmp_path):
    make_dirs(tmp_path)
    reg = parse_registry(FIXTURE.read_text(encoding="utf-8"))
    assert validate(reg, set(ALL), tmp_path) == []
    assert install_warnings(reg, set(ALL), tmp_path) == []


def errors(tmp_path, old, new, installed=None):
    make_dirs(tmp_path)
    text = FIXTURE.read_text(encoding="utf-8")
    assert old in text
    reg = parse_registry(text.replace(old, new, 1))
    return validate(reg, installed or set(ALL), tmp_path)


def test_unknown_aspect(tmp_path):
    errs = errors(tmp_path, "- 주 측면: prose-edit\n", "- 주 측면: nope\n")
    assert "general-writing: unknown aspect nope" in errs


def test_missing_evidence(tmp_path):
    errs = errors(tmp_path, ' / voice "preserving the writer\'s meaning and personal voice"', "")
    assert "general-writing: no evidence for voice" in errs


def test_missing_field(tmp_path):
    errs = errors(tmp_path, "- 단계: prose\n- 과제 종류: new, edit, docs\n", "- 과제 종류: new, edit, docs\n")
    assert "general-writing: missing field 단계" in errs


def test_missing_install_dir(tmp_path):
    # Install mismatch is a warning, not a structural error.
    make_dirs(tmp_path, ALL - {"copywriting"})
    reg = parse_registry(FIXTURE.read_text(encoding="utf-8"))
    assert validate(reg, set(ALL), tmp_path) == []
    assert install_warnings(reg, set(ALL), tmp_path) == ["copywriting: not installed (dir missing)"]


def test_absent_from_manifest(tmp_path):
    make_dirs(tmp_path)
    reg = parse_registry(FIXTURE.read_text(encoding="utf-8"))
    assert validate(reg, ALL - {"copywriting"}, tmp_path) == []
    assert install_warnings(reg, ALL - {"copywriting"}, tmp_path) == [
        "copywriting: not installed (absent from manifest)"
    ]


def test_absent_from_manifest_and_dir_missing(tmp_path):
    make_dirs(tmp_path, ALL - {"copywriting"})
    reg = parse_registry(FIXTURE.read_text(encoding="utf-8"))
    assert install_warnings(reg, ALL - {"copywriting"}, tmp_path) == [
        "copywriting: not installed (absent from manifest, dir missing)"
    ]


def test_unregistered_installed_skill(tmp_path):
    make_dirs(tmp_path)
    reg = parse_registry(FIXTURE.read_text(encoding="utf-8"))
    assert validate(reg, ALL | {"extra"}, tmp_path) == []
    assert install_warnings(reg, ALL | {"extra"}, tmp_path) == ["extra: installed but not in registry"]


def test_requires_unknown_skill(tmp_path):
    errs = errors(tmp_path, "- 필수 동반: humanizer\n", "- 필수 동반: ghost\n")
    assert "general-writing: requires unknown skill ghost" in errs


def test_plugin_skill_skips_dir_check(tmp_path):
    make_dirs(tmp_path, ALL - {"copywriting"})
    text = FIXTURE.read_text(encoding="utf-8").replace(
        "### copywriting\n- id: WM-X0200\n- 출처: example/skills `copywriting/SKILL.md` @ def5678, MIT",
        "### copywriting\n- id: WM-X0200\n- 출처: plugin anthropic-skills",
    )
    reg = parse_registry(text)
    assert validate(reg, set(ALL), tmp_path) == []
    assert install_warnings(reg, set(ALL), tmp_path) == []


def test_unknown_stage_and_task_type(tmp_path):
    errs = errors(tmp_path, "- 단계: prose\n- 과제 종류: new, edit, docs", "- 단계: zzz\n- 과제 종류: new, bogus, docs")
    assert "general-writing: unknown stage zzz" in errs
    assert "general-writing: unknown task type bogus" in errs


def test_forbids_unregistered_allowed(tmp_path):
    make_dirs(tmp_path)
    reg = parse_registry(FIXTURE.read_text(encoding="utf-8"))
    assert not [e for e in validate(reg, set(ALL), tmp_path) if "manuscript-writing" in e]


def test_evidence_with_inner_quotes():
    text = FIXTURE.read_text(encoding="utf-8").replace(
        'ai-tells "Drafts never use AI tells"',
        'ai-tells "never use "it\'s not X, it\'s Y" reveals" / persuasion "tail"',
        1,
    )
    ev = parse_registry(text).skills["copywriting"].evidence
    assert ev["ai-tells"] == 'never use "it\'s not X, it\'s Y" reveals'
    assert ev["persuasion"] == "tail"


def test_plugins_path_in_repo_source_is_not_plugin(tmp_path):
    # A repo source whose path contains "plugins/" is a normal install, not a plugin copy.
    make_dirs(tmp_path, ALL - {"copywriting"})
    text = FIXTURE.read_text(encoding="utf-8").replace(
        "example/skills `copywriting/SKILL.md`", "example/skills `plugins/x/skills/copywriting/SKILL.md`", 1
    )
    reg = parse_registry(text)
    assert install_warnings(reg, set(ALL), tmp_path) == ["copywriting: not installed (dir missing)"]

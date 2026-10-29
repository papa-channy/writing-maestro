"""CLI tests for registry_check.py: exit codes, WARN lines, manifest errors, default manifest."""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "skills" / "writing-maestro" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from registry_check import MANIFEST_REL, default_manifest  # noqa: E402

FIXTURE = Path(__file__).parent / "fixtures" / "registry_min.md"
ALL = ["general-writing", "humanizer", "prose-naturalizer", "copywriting"]


def write_manifest(path, names):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"skills": [
        {"name": n, "installed_dir": f"/x/{n}", "status": "READY"} for n in names
    ]}), encoding="utf-8")
    return path


def skills_dir(tmp_path, names=ALL):
    d = tmp_path / "skills"
    for n in names:
        (d / n).mkdir(parents=True, exist_ok=True)
    return d


def run(tmp_path, *args):
    return subprocess.run([sys.executable, str(SCRIPTS / "registry_check.py"), *map(str, args)],
                          capture_output=True, text=True, cwd=tmp_path)


def test_ok_no_warnings(tmp_path):
    m = write_manifest(tmp_path / "m.json", ALL)
    r = run(tmp_path, "--registry", FIXTURE, "--manifest", m, "--skills-dir", skills_dir(tmp_path))
    assert r.returncode == 0
    assert r.stdout == "OK 4 skills\n"


def test_install_mismatch_is_warning(tmp_path):
    m = write_manifest(tmp_path / "m.json", [n for n in ALL if n != "humanizer"] + ["extra"])
    d = skills_dir(tmp_path, [n for n in ALL if n != "copywriting"])
    r = run(tmp_path, "--registry", FIXTURE, "--manifest", m, "--skills-dir", d)
    assert r.returncode == 0, r.stdout
    assert r.stdout.splitlines() == [
        "WARN humanizer: not installed (absent from manifest)",
        "WARN copywriting: not installed (dir missing)",
        "WARN extra: installed but not in registry",
        "OK 4 skills (3 warnings)",
    ]


def test_structural_error_still_fatal(tmp_path):
    reg = tmp_path / "r.md"
    reg.write_text(FIXTURE.read_text(encoding="utf-8").replace("- 주 측면: prose-edit\n", "- 주 측면: nope\n", 1),
                   encoding="utf-8")
    m = write_manifest(tmp_path / "m.json", ALL)
    r = run(tmp_path, "--registry", reg, "--manifest", m, "--skills-dir", skills_dir(tmp_path, ALL[:3]))
    assert r.returncode == 1
    assert "general-writing: unknown aspect nope" in r.stdout.splitlines()
    assert "WARN copywriting: not installed (dir missing)" in r.stdout.splitlines()
    assert "OK" not in r.stdout


def test_missing_manifest_clean_error(tmp_path):
    r = run(tmp_path, "--registry", FIXTURE, "--manifest", tmp_path / "nope.json", "--skills-dir", tmp_path)
    assert r.returncode == 2
    assert r.stdout.startswith("ERROR cannot read manifest") and len(r.stdout.splitlines()) == 1
    assert "Traceback" not in r.stderr


def test_malformed_manifest_clean_error(tmp_path):
    for body in ["{not json", '{"skills": 3}', "[]", '{"skills": ["x"]}']:
        m = tmp_path / "m.json"
        m.write_text(body, encoding="utf-8")
        r = run(tmp_path, "--registry", FIXTURE, "--manifest", m, "--skills-dir", tmp_path)
        assert r.returncode == 2, body
        assert r.stdout.startswith("ERROR malformed manifest") and len(r.stdout.splitlines()) == 1, body
        assert "Traceback" not in r.stderr, body


def test_default_manifest_through_symlink(tmp_path):
    # repo/skills/writing-maestro/registry.md, reached through a symlinked skill folder.
    repo = tmp_path / "repo"
    wm = repo / "skills" / "writing-maestro"
    wm.mkdir(parents=True)
    shutil.copy(FIXTURE, wm / "registry.md")
    write_manifest(repo / MANIFEST_REL, ALL)
    link_parent = tmp_path / "home" / ".claude" / "skills"
    link_parent.mkdir(parents=True)
    os.symlink(wm, link_parent / "writing-maestro")
    linked = link_parent / "writing-maestro" / "registry.md"
    assert default_manifest(linked) == (repo / MANIFEST_REL).resolve()
    other = tmp_path / "elsewhere"
    other.mkdir()
    r = run(other, "--registry", linked, "--skills-dir", skills_dir(tmp_path))
    assert r.returncode == 0, r.stdout
    assert r.stdout == "OK 4 skills\n"
    # --manifest still overrides the default.
    m = write_manifest(tmp_path / "m.json", ALL[:3])
    r = run(other, "--registry", linked, "--manifest", m, "--skills-dir", skills_dir(tmp_path))
    assert "WARN copywriting: not installed (absent from manifest)" in r.stdout.splitlines()

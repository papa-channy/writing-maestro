"""All CLIs must import and run under Python 3.9 (macOS /usr/bin/python3)."""
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "skills" / "writing-maestro" / "scripts"
REGISTRY = ROOT / "skills" / "writing-maestro" / "registry.md"
PY39 = "/usr/bin/python3"


def _py39_available():
    if not shutil.which(PY39):
        return False
    out = subprocess.run([PY39, "-c", "import sys;print(sys.version_info[:2] < (3, 10))"],
                         capture_output=True, text=True)
    return out.stdout.strip() == "True"


pytestmark = pytest.mark.skipif(not _py39_available(), reason="no Python < 3.10 at /usr/bin/python3")


@pytest.mark.parametrize("script", ["registry_lib.py", "registry_check.py", "combo_check.py", "registry_lookup.py"])
def test_imports_under_py39(script, tmp_path):
    mod = script[:-3]
    r = subprocess.run([PY39, "-c", f"import sys; sys.path.insert(0, {str(SCRIPTS)!r}); import {mod}"],
                       capture_output=True, text=True, cwd=tmp_path)
    assert r.returncode == 0, r.stderr


def test_cli_runs_under_py39(tmp_path):
    r = subprocess.run([PY39, str(SCRIPTS / "combo_check.py"), "--registry", str(REGISTRY), "copywriting", "humanizer"],
                       capture_output=True, text=True, cwd=tmp_path)
    assert r.returncode == 0, r.stderr
    r = subprocess.run([PY39, str(SCRIPTS / "registry_lookup.py"), "--registry", str(REGISTRY), "--skill", "humanizer"],
                       capture_output=True, text=True, cwd=tmp_path)
    assert r.returncode == 0, r.stderr

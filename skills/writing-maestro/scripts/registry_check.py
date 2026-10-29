#!/usr/bin/env python3
"""registry.md를 설치 매니페스트·스킬 디렉터리와 대조해 검증한다.

구조 오류(필드·측면·단계·과제 종류·묶음·근거·필수 동반)는 줄마다 출력하고 exit 1.
설치 불일치는 `WARN ` 줄로 출력하고 구조 오류가 없으면 exit 0
(`OK <n> skills` 또는 `OK <n> skills (<k> warnings)`).
매니페스트·레지스트리를 읽을 수 없으면 `ERROR ` 한 줄과 exit 2.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from registry_lib import install_warnings, parse_registry, validate  # noqa: E402

MANIFEST_REL = Path("research") / "install" / "2026-10-29-install-manifest.json"


class ManifestError(Exception):
    pass


def default_manifest(registry: Path) -> Path:
    """레포 루트(= 심링크를 푼 registry.md의 세 단계 위)의 설치 매니페스트."""
    return registry.expanduser().resolve().parents[2] / MANIFEST_REL


def installed_from_manifest(path: Path) -> set[str]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except OSError as e:
        raise ManifestError(f"cannot read manifest {path}: {e.strerror or e}") from None
    except ValueError as e:
        raise ManifestError(f"malformed manifest {path}: {e}") from None
    skills = data.get("skills") if isinstance(data, dict) else None
    if not isinstance(skills, list) or not all(isinstance(s, dict) for s in skills):
        raise ManifestError(f"malformed manifest {path}: expected an object with a 'skills' list of objects")
    names = {
        Path(s["installed_dir"]).name
        for s in skills
        if s.get("status") != "BLOCKED" and isinstance(s.get("installed_dir"), str) and s["installed_dir"]
    }
    return names


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--registry", required=True, type=Path)
    ap.add_argument("--manifest", type=Path,
                    help=f"기본값: <registry.md 실제 경로>/../../../{MANIFEST_REL}")
    ap.add_argument("--skills-dir", type=Path, default=Path("~/.claude/skills"))
    args = ap.parse_args(argv)
    manifest = args.manifest if args.manifest is not None else default_manifest(args.registry)
    try:
        text = args.registry.read_text(encoding="utf-8")
    except OSError as e:
        print(f"ERROR cannot read registry {args.registry}: {e.strerror or e}")
        return 2
    try:
        installed = installed_from_manifest(manifest)
    except ManifestError as e:
        print(f"ERROR {e}")
        return 2
    reg = parse_registry(text)
    skills_dir = args.skills_dir.expanduser()
    errs = validate(reg, installed, skills_dir)
    warns = install_warnings(reg, installed, skills_dir)
    for e in errs:
        print(e)
    for w in warns:
        print(f"WARN {w}")
    if errs:
        return 1
    print(f"OK {len(reg.skills)} skills" + (f" ({len(warns)} warnings)" if warns else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())

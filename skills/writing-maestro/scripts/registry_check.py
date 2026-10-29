#!/usr/bin/env python3
"""registry.md를 설치 매니페스트·스킬 디렉터리와 대조해 검증한다."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from registry_lib import parse_registry, validate


def installed_from_manifest(path: Path) -> set[str]:
    data = json.loads(path.read_text())
    names = {
        Path(s["installed_dir"]).name
        for s in data["skills"]
        if s.get("status") != "BLOCKED" and s.get("installed_dir")
    }
    return names | {"doc-coauthoring"}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--registry", required=True, type=Path)
    ap.add_argument("--manifest", required=True, type=Path)
    ap.add_argument("--skills-dir", type=Path, default=Path("~/.claude/skills"))
    args = ap.parse_args()
    reg = parse_registry(args.registry.read_text())
    errs = validate(reg, installed_from_manifest(args.manifest), args.skills_dir.expanduser())
    if errs:
        print("\n".join(errs))
        return 1
    print(f"OK {len(reg.skills)} skills")
    return 0


if __name__ == "__main__":
    sys.exit(main())

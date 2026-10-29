#!/usr/bin/env python3
"""registry.md를 통째로 읽지 않고 필요한 부분만 꺼낸다 (stdlib only).

--summary          스킬마다 한 줄: name | 주 측면 | 부 측면 | 단계 | 과제 종류 | 묶음 | 역할
--skill NAME ...   해당 `### NAME` 항목을 원문 그대로 출력. 없는 이름이면 stderr에 적고 exit 1.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from registry_lib import parse_registry  # noqa: E402

SUMMARY_FIELDS = ["주 측면", "부 측면", "단계", "과제 종류", "묶음", "역할"]


def raw_entries(text: str) -> dict[str, str]:
    """`## 스킬` 절 안의 `### <name>` 항목을 원문 그대로, 끝 빈 줄을 떼고 반환."""
    out: dict[str, list[str]] = {}
    in_skills, current = False, None
    for ln in text.splitlines():
        if ln.startswith("## "):
            in_skills, current = ln[3:].strip() == "스킬", None
            continue
        if not in_skills:
            continue
        if ln.startswith("### "):
            current = ln[4:].strip()
            out[current] = [ln]
        elif current is not None:
            out[current].append(ln)
    return {k: "\n".join(v).rstrip("\n") for k, v in out.items()}


def summary(text: str) -> list[str]:
    reg = parse_registry(text)
    return [
        " | ".join([name] + [s.fields.get(k, "").replace("|", "/") for k in SUMMARY_FIELDS])
        for name, s in reg.skills.items()
    ]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--registry", required=True, type=Path)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--summary", action="store_true")
    g.add_argument("--skill", nargs="+", metavar="NAME")
    args = ap.parse_args(argv)
    text = args.registry.read_text(encoding="utf-8")

    if args.summary:
        print("\n".join(summary(text)))
        return 0

    entries = raw_entries(text)
    unknown = [n for n in args.skill if n not in entries]
    if unknown:
        for n in unknown:
            print(f"unknown skill {n}", file=sys.stderr)
        return 1
    print("\n\n".join(entries[n] for n in args.skill))
    return 0


if __name__ == "__main__":
    sys.exit(main())

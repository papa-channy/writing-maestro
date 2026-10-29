#!/usr/bin/env python3
"""writing-maestro registry.md 파서와 검증기 (stdlib only)."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

NONE = "없음"
TASK_TYPES = {"new", "edit", "review", "docs"}
REQUIRED_FIELDS = [
    "id", "출처", "역할", "맞는 상황", "맞지 않는 상황", "고유 접근",
    "주 측면", "부 측면", "단계", "과제 종류", "묶음", "필수 동반", "금지 짝",
    "실행 요건", "필수 명령", "상태 파일", "주의", "근거",
]
_FIELD_RE = re.compile(r"^-\s*([^:]+?)\s*:\s*(.*)$")
_EVIDENCE_RE = re.compile(r'([\w-]+)\s+"([^"]*)"')


@dataclass
class Skill:
    name: str
    wm_id: str
    primary: list[str]
    secondary: list[str]
    stages: list[str]
    task_types: list[str]
    bundle: str | None
    requires: list[str]
    forbids: list[str]
    commands: list[str]
    evidence: dict[str, str]
    fields: dict[str, str] = field(default_factory=dict)


@dataclass
class Registry:
    aspects: dict[str, str]
    stages: dict[str, str]
    bundles: dict[str, list[str]]
    skills: dict[str, Skill]


def _list(value: str) -> list[str]:
    value = value.strip()
    if not value or value == NONE:
        return []
    return [v.strip() for v in value.split(",") if v.strip()]


def _table(lines: list[str]) -> list[list[str]]:
    """표 본문 행(헤더·구분선 제외)을 셀 목록으로 반환."""
    rows = [
        [c.strip() for c in ln.strip().strip("|").split("|")]
        for ln in lines
        if ln.strip().startswith("|")
    ]
    return rows[2:]


def _sections(text: str, prefix: str) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    current = None
    for ln in text.splitlines():
        if ln.startswith(prefix) and not ln.startswith(prefix + "#"):
            current = ln[len(prefix):].strip()
            out[current] = []
        elif current is not None:
            out[current].append(ln)
    return out


def _build_skill(name: str, lines: list[str]) -> Skill:
    f: dict[str, str] = {}
    for ln in lines:
        m = _FIELD_RE.match(ln)
        if m:
            f[m.group(1)] = m.group(2).strip()
    bundle = f.get("묶음", NONE)
    return Skill(
        name=name,
        wm_id=f.get("id", ""),
        primary=_list(f.get("주 측면", "")),
        secondary=_list(f.get("부 측면", "")),
        stages=_list(f.get("단계", "")),
        task_types=_list(f.get("과제 종류", "")),
        bundle=None if bundle in ("", NONE) else bundle,
        requires=_list(f.get("필수 동반", "")),
        forbids=_list(f.get("금지 짝", "")),
        commands=_list(f.get("필수 명령", "")),
        evidence={k: v for k, v in _EVIDENCE_RE.findall(f.get("근거", ""))},
        fields=f,
    )


def parse_registry(text: str) -> Registry:
    top = _sections(text, "## ")
    aspects = {r[0]: r[1] for r in _table(top.get("측면", [])) if len(r) >= 2}
    stages = {r[0]: r[1] for r in _table(top.get("단계", [])) if len(r) >= 2}
    bundles = {r[0]: _list(r[1]) for r in _table(top.get("묶음", [])) if len(r) >= 2}
    skills = {
        name: _build_skill(name, lines)
        for name, lines in _sections("\n".join(top.get("스킬", [])), "### ").items()
    }
    return Registry(aspects, stages, bundles, skills)


def validate(reg: Registry, installed: set[str], skills_dir: Path) -> list[str]:
    errs: list[str] = []
    for name, s in reg.skills.items():
        for key in REQUIRED_FIELDS:
            if key not in s.fields:
                errs.append(f"{name}: missing field {key}")
        for a in s.primary + s.secondary:
            if a not in reg.aspects:
                errs.append(f"{name}: unknown aspect {a}")
        for st in s.stages:
            if st not in reg.stages:
                errs.append(f"{name}: unknown stage {st}")
        for t in s.task_types:
            if t not in TASK_TYPES:
                errs.append(f"{name}: unknown task type {t}")
        if s.bundle is not None and s.bundle not in reg.bundles:
            errs.append(f"{name}: unknown bundle {s.bundle}")
        for r in s.requires:
            if r not in reg.skills:
                errs.append(f"{name}: requires unknown skill {r}")
        # 금지 짝은 미등록 이름을 허용한다.
        for key in dict.fromkeys(s.primary + s.secondary + s.requires + s.forbids):
            if key not in s.evidence:
                errs.append(f"{name}: no evidence for {key}")
        is_plugin = "plugin" in s.fields.get("출처", "")
        if not is_plugin and (name not in installed or not (skills_dir / name).is_dir()):
            errs.append(f"{name}: not installed")
    for b, members in reg.bundles.items():
        for m in members:
            if m not in reg.skills:
                errs.append(f"bundle {b}: unknown skill {m}")
    for name in sorted(installed - set(reg.skills)):
        errs.append(f"{name}: installed but not in registry")
    return errs

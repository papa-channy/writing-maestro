#!/usr/bin/env python3
"""facts/*.json + assignments.py -> skills/writing-maestro/registry.md (stdlib only).

최초 조립용. 만든 뒤에는 registry.md가 진실 원천이고, 이 스크립트를 다시 돌리면
registry.md의 손 편집이 덮어써진다.

    python3 research/registry-build/build_registry.py [--out PATH]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "skills" / "writing-maestro" / "scripts"))

import assignments as A  # noqa: E402
from registry_lib import parse_registry  # noqa: E402

FACTS = HERE / "facts"
OUT = ROOT / "skills" / "writing-maestro" / "registry.md"
NONE = "없음"
# 재귀 방지 규칙이라 금지 짝으로 적지 않는 스킬 (controller ruling 3)
GUARD_ONLY_FORBIDS = {"academic-voice", "better-usage", "non-autoregressive-writing-pass", "writing-cadence"}
NON_SKILL_REQUIRES = {"node"}
QUOTE_MAX = 110
SKILLS_DIR = Path("~/.claude/skills").expanduser()


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def shorten(q: str) -> str:
    q = norm(q)
    if len(q) <= QUOTE_MAX:
        return q
    cut = q[:QUOTE_MAX]
    return cut[: cut.rfind(" ")] if " " in cut else cut


def source_field(src: str) -> str:
    if src.startswith("plugin"):
        return src
    m = re.match(r"^(\S+)\s+(\S+)\s+@(\S+?),\s*(.+)$", src)
    if not m:
        raise SystemExit(f"cannot parse source: {src}")
    repo, path, sha, lic = m.groups()
    return f"{repo} `{path}` @ {sha}, {lic}"


def joined(items: list[str]) -> str:
    return ", ".join(items) if items else NONE


def build_skill(name: str, facts: dict, a: dict, errors: list[str]) -> list[str]:
    pool = [norm(d["quote"]) for d in facts["directives"]]
    pool += [norm(r["quote"]) for r in facts["requires"] + facts["forbids"]]

    source_text: list[str] = []

    def in_installed_source(q: str) -> bool:
        # facts에 없는 인용은 설치된 원문(*.md)에 그대로 있으면 받는다 (리뷰가 원문에서 찾은 인용).
        if not source_text:
            d = SKILLS_DIR / name
            source_text.append(norm(" ".join(p.read_text(encoding="utf-8", errors="ignore")
                                             for p in sorted(d.rglob("*.md")))) if d.is_dir() else "")
        return q in source_text[0]

    def check_quote(key: str, q: str) -> str:
        q = norm(q)
        if not any(q in p for p in pool) and not in_installed_source(q):
            errors.append(f"{name}: quote for {key} not in facts or installed source: {q!r}")
        if re.search(r'\s/\s[\w-]+\s+"', q):
            errors.append(f"{name}: quote for {key} breaks evidence grammar: {q!r}")
        return q

    primary = [k for k, _ in a["P"]]
    secondary = [k for k, _ in a["S"]]
    if set(primary) & set(secondary):
        errors.append(f"{name}: secondary repeats primary {set(primary) & set(secondary)}")
    evidence = [(k, check_quote(k, q)) for k, q in a["P"] + a["S"]]

    requires = [r for r in facts["requires"] if r["skill"] not in NON_SKILL_REQUIRES]
    for r in requires:
        evidence.append((r["skill"], check_quote(r["skill"], shorten(r["quote"]))))
    forbids = [] if name in GUARD_ONLY_FORBIDS else facts["forbids"]
    fq = a.get("forbid_quotes", {})
    for f in forbids:
        evidence.append((f["skill"], check_quote(f["skill"], fq.get(f["skill"], shorten(f["quote"])))))

    task_types = list(facts["task_types"])
    for t in A.TASK_TYPE_EXTRA.get(name, []):
        if t not in task_types:
            task_types.append(t)
    task_types.sort(key=["new", "edit", "review", "docs"].index)

    req = facts["requirements"]
    runtime = f"필수: {'; '.join(req['required']) or NONE} | 선택: {'; '.join(req['optional']) or NONE}"
    cmds = a.get("cmds", facts["commands"])
    caution = a.get("caution_override", facts["cautions"])
    if a.get("note"):
        caution = f"{caution} 판단: {a['note']}"
    ev = " / ".join(f'{k} "{q}"' for k, q in evidence)

    return [
        f"### {name}",
        f"- id: {facts['wm_id']}",
        f"- 출처: {source_field(facts['source'])}",
        f"- 역할: {norm(facts['role'])}",
        f"- 맞는 상황: {norm(facts['fits'])}",
        f"- 맞지 않는 상황: {norm(facts['not_fits'])}",
        f"- 고유 접근: {norm(facts['unique_approach'])}",
        f"- 주 측면: {joined(primary)}",
        f"- 부 측면: {joined(secondary)}",
        f"- 단계: {joined(a['stages'])}",
        f"- 과제 종류: {joined(task_types)}",
        f"- 묶음: {a.get('bundle') or NONE}",
        f"- 필수 동반: {joined([r['skill'] for r in requires])}",
        f"- 금지 짝: {joined([f['skill'] for f in forbids])}",
        f"- 실행 요건: {norm(runtime)}",
        f"- 필수 명령: {joined(cmds)}",
        f"- 상태 파일: {norm('; '.join(facts['state_files'])) or NONE}",
        f"- 주의: {norm(caution) or NONE}",
        f"- 근거: {ev}",
        "",
    ]


HEADER = """# writing-maestro 스킬 레지스트리

writing-maestro가 매 호출 새로 읽는 스킬 목록이다. 앞부분은 범위·측면·단계·묶음·조합 규칙, 뒷부분은 스킬별 항목이다. 이 파일이 진실 원천이다. 스킬 원문(서드파티)은 고치지 않고, 충돌은 여기 적은 측면과 시안 지시의 우선순위로만 다룬다.

## 고치는 법

- **스킬 추가**: `~/.claude/skills/<이름>/`에 설치하고 설치 매니페스트에 올린 뒤, `## 스킬` 아래에 `### <이름>` 항목을 다른 항목과 같은 필드 순서로 쓴다. 주 측면은 그 스킬의 본업으로 결과물에서 정하는 측면, 부 측면은 원문에 규칙이 있지만 본업이 아닌 측면이다. 주·부 측면, 필수 동반, 금지 짝마다 `근거`에 `<키> "<원문 인용>"` 쌍을 하나씩 ` / `로 이어 붙인다(인용 안에 ` / 단어 "` 형태는 쓰지 않는다). 사용자 정보 없이는 결과가 안 나올 때만 단계에 `clarify`를 넣는다. 측면 표의 '주 측면 스킬' 칸도 함께 고친다.
- **스킬 제거**: 항목을 지우고, 측면 표와 묶음 표에서 이름을 지운다. 다른 스킬의 `필수 동반`에 남아 있으면 검증이 실패한다.
- **새 측면**: 두 스킬이 동시에 다르게 지시하면 결과가 흔들리는 결과물 속성일 때만 만든다. id는 소문자 ascii 슬러그.
- **재생성 주의**: `research/registry-build/build_registry.py`를 다시 돌리면 이 파일의 손 편집이 덮어써진다. 고칠 때는 `research/registry-build/assignments.py`를 고친 뒤 다시 만들거나, 이 파일만 직접 고치고 스크립트는 돌리지 않는다.
- **검증**: 고친 뒤 다음을 돌려 `OK <n> skills`를 확인한다. 조합 하나를 따져 보려면 `combo_check.py`를 쓴다.

```
python3 skills/writing-maestro/scripts/registry_check.py --registry skills/writing-maestro/registry.md --manifest research/install/2026-10-29-install-manifest.json
python3 skills/writing-maestro/scripts/combo_check.py --registry skills/writing-maestro/registry.md copywriting humanizer
```

## 범위

다룬다: 글쓰기 과제 네 종류.
- `new` 새 글 쓰기: 요청과 자료로 새 글을 쓴다.
- `edit` 기존 글 고치기: 원문을 고친 판본(교정, 번역, 문체 변환, AI식 표현 제거 등). 원문 파일은 고치지 않는다.
- `review` 검토만 하기: 발견 사항·심각도·수정 제안이 담긴 검토 보고서. 대상 원문은 고치지 않는다.
- `docs` 코드베이스 문서 작업: README, CLAUDE.md/AGENTS.md, 설계 문서, 런북 같은 레포 문서. 시안은 대상 파일을 자기 폴더로 복사해 작업한다.

다루지 않는다: 게시·발송·업로드(메일 발송, 소셜 게시, 투고 제출은 사용자가 직접 한다), 글이 아닌 과제(코드 구현, 이미지·영상 생성, 데이터 분석 자체).

## 측면

측면 = 두 스킬이 한 시안에서 동시에 다르게 지시하면 결과가 흔들리는 결과물 속성. 같은 측면을 **주 측면**으로 가진 스킬들이 한 클러스터이고, 조합은 클러스터당 하나만 뽑는다(묶음 예외는 아래 조합 규칙). 한 스킬은 주 측면을 여러 개 가질 수 있다.

장르 규칙은 장르별로 나눴다. 학술(`academic`), 기술 문서(`tech-docs`), 프롬프트(`prompt`)는 장르 측면을 하나씩 두고, 서사는 전제·플롯·인물·장면·원고·장르 팩·운문·연속성으로 쪼갰다(같은 묶음 안에서 순서대로 함께 쓰는 스킬들이 서로 막히지 않게). 마케팅·소셜은 장르 측면을 따로 두지 않았다. 그 스킬들의 규칙은 이미 설득(`persuasion`)·훅(`hook`)·포맷(`format`)·구조(`structure`)로 갈리기 때문이다.

"""

RULES = """## 조합 규칙

`combo_check.py`가 다음을 결정적으로 판정한다.

1. **금지 짝**: 어느 쪽이 적었든 두 구성원을 함께 넣지 않는다. 구성원 A가 금지한 스킬 S가 다른 구성원 B의 닫힘에 있어도 충돌이다(`forbidden pair A+S(via B)`). 단 S가 A 자신의 닫힘에 있으면(예: paper-writing은 humanizer를 금지하지만 general-writing을 거쳐 스스로 부른다) 이 경유 충돌은 면제한다.
2. **주 측면 배제(동반 포함)**: 각 구성원의 `필수 동반`을 끝까지 따라간 닫힘(조건부 동반 포함, 자기 자신 제외)까지 함께 본다. 구성원이 직접 넣지 않아도 그 동반 스킬의 규칙이 시안에 들어가기 때문이다(예: writing-design-docs → technical-writing의 문장 규칙, paper-writing → general-writing → humanizer의 AI식 표현 목록). 측면마다 그것을 주 측면으로 가진 서로 다른 출처 스킬을 모으고, 출처가 둘 이상이며 그 출처끼리 조율되어 있지 않으면 `primary overlap <측면>: <그 출처를 들여온 구성원들>` 충돌이다. 두 구성원이 같은 출처 하나를 들여오는 것(예: writing-design-docs와 reviewing-technical-prose가 둘 다 technical-writing을 부름)은 충돌이 아니다. 조율 = 같은 묶음이고, (구성원 ∪ 닫힘) 안의 어떤 스킬이 `필수 동반`을 따라 두 출처 모두에 닿는다(한 출처가 다른 출처를 부르는 경우 포함, 여러 단계 허용). 부르는 쪽이 순서를 짜기 때문이다. 공통 동반을 함께 부를 뿐인 형제(writing-design-docs와 writing-runbooks가 둘 다 technical-writing을 부름)는 서로 조율되지 않으므로 둘의 골격(structure)은 충돌이다.
3. **생성 스킬 최대 3개**: 단계가 `clarify`·`check`만이 아닌 구성원이 생성 스킬이다. 조합 안 다른 구성원의 `필수 동반`인 구성원은 세지 않는다. 닫힘에만 있는 동반 스킬은 구성원이 아니므로 세지 않는다.
4. **명확화 전용 스킬은 조합에 넣지 않는다**: 단계가 `clarify`뿐인 스킬은 ② 명확화 단계로 보낸다.
5. **우선순위**: 부 측면도 주 측면처럼 (구성원 ∪ 닫힘)으로 보고 구성원에게 돌린다. 구성원 자신이나 그 닫힘의 스킬이 부 측면으로 가진 측면은 그 구성원이 가진 것으로 친다. 그 측면은 주 측면으로 가진 구성원(자기 자신 또는 닫힘이 소유)을 따른다(앞선 구성원 우선). 그런 구성원이 없으면 그 측면을 부 측면으로 가진 구성원 중 조합 순서상 뒤 스킬을 따른다. 따르는 구성원이 아닌 나머지 부 측면 보유 구성원은 `ignored`에 오른다. 단 그 측면을 주 측면으로 가진 구성원은 오르지 않는다. 부 측면 보유 구성원이 하나뿐이고 주 측면 소유자가 없으면 `precedence`에만 있고 `ignored`에는 없다. 시안 지시에 "측면별 따를 스킬"로 적는다.

`필수 동반`은 자동 포함이 아니다. 조합에는 오케스트레이터가 직접 순서를 짜는 스킬만 넣고, 구성원이 스스로 부르는 동반 스킬(예: general-writing → humanizer)은 넣지 않는다. 동반 관계는 충돌·우선순위를 닫힘까지 따지는 데(규칙 1·2·5)와 생성 스킬 수 계산에 쓴다. 산출 파일 규약이 다른 두 보이스 프로필(`voice.md` vs `voice/<name>.md`)은 한 시안에서 하나만 쓴다.

"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=OUT)
    args = ap.parse_args()

    facts = {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in sorted(FACTS.glob("*.json"))}
    errors: list[str] = []
    missing = sorted(set(facts) ^ set(A.SKILLS))
    if missing:
        errors.append(f"facts/assignments mismatch: {missing}")
    aspect_ids = [a[0] for a in A.ASPECTS]
    for name, a in A.SKILLS.items():
        for k, _ in a["P"] + a["S"]:
            if k not in aspect_ids:
                errors.append(f"{name}: unknown aspect {k}")

    owners = {aid: [n for n, a in A.SKILLS.items() if aid in [k for k, _ in a["P"]]] for aid in aspect_ids}
    lines = [HEADER.rstrip() + "\n", "| id | 이름 | 설명 | 주 측면 스킬(클러스터) |", "|---|---|---|---|"]
    for aid, label, desc in A.ASPECTS:
        if not owners[aid]:
            errors.append(f"aspect {aid} has no primary owner")
        lines.append(f"| {aid} | {label} | {desc} | {', '.join(owners[aid])} |")
    lines += ["", "## 단계", "", "조합 안 적용 순서는 research → draft → genre → prose이다.", "",
              "| id | 이름 | 설명 |", "|---|---|---|"]
    lines += [f"| {sid} | {label} | {desc} |" for sid, label, desc in A.STAGES]
    lines += ["", "## 묶음", "", "같은 저장소 안에서 서로 부르는 순서가 정해진 스킬 집합. 묶음 흐름 중간에 다른 스킬을 같은 측면으로 끼워 넣지 않는다.", "",
              "| id | 구성 | 설명 |", "|---|---|---|"]
    for bid, members, desc in A.BUNDLES:
        for m in members:
            if A.SKILLS.get(m, {}).get("bundle") != bid:
                errors.append(f"bundle {bid}: {m} does not declare it")
        lines.append(f"| {bid} | {', '.join(members)} | {desc} |")
    lines += ["", RULES.rstrip(), "", "## 스킬", ""]
    for name in sorted(A.SKILLS):
        lines += build_skill(name, facts[name], A.SKILLS[name], errors)

    text = "\n".join(lines).rstrip() + "\n"
    reg = parse_registry(text)
    for name, a in A.SKILLS.items():
        s = reg.skills[name]
        want = {k for k, _ in a["P"] + a["S"]}
        if not want <= set(s.evidence):
            errors.append(f"{name}: evidence round-trip lost {want - set(s.evidence)}")
    if errors:
        print("\n".join(errors))
        return 1
    args.out.write_text(text, encoding="utf-8")
    print(f"wrote {args.out} ({len(reg.skills)} skills, {len(reg.aspects)} aspects)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

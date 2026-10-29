"""Deterministic conflict and precedence checker for writing-skill combinations."""
import argparse
import json
import shutil
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from registry_lib import Registry, parse_registry  # noqa: E402

MAX_GENERATION = 3
NON_GENERATION_STAGES = {"clarify", "check"}


@dataclass
class ComboResult:
    ok: bool
    conflicts: list[str] = field(default_factory=list)
    precedence: dict[str, str] = field(default_factory=dict)
    ignored: list[tuple[str, str]] = field(default_factory=list)
    generation_count: int = 0
    missing_commands: list[str] = field(default_factory=list)


def _closure(reg: Registry, name: str) -> list[str]:
    """Transitive `필수 동반` of `name` (registered skills only), BFS order, excluding itself."""
    seen, order, queue = {name}, [], list(reg.skills[name].requires)
    while queue:
        r = queue.pop(0)
        if r in seen or r not in reg.skills:
            continue
        seen.add(r)
        order.append(r)
        queue.extend(reg.skills[r].requires)
    return order


def _coordinated(reg: Registry, a: str, b: str, nodes: set[str]) -> bool:
    """Same bundle and coordinated: some skill in `nodes` reaches both a and b along
    `requires` edges (reflexive, transitive). A caller sequences the companions it invokes;
    two siblings that merely share a common companion (e.g. two doc-type skills that both
    require technical-writing) are not coordinated with each other."""
    ba, bb = reg.skills[a].bundle, reg.skills[b].bundle
    if ba is None or ba != bb:
        return False
    for c in nodes:
        reach, stack = {c}, [c]
        while stack:
            for r in reg.skills[stack.pop()].requires:
                if r in nodes and r not in reach:
                    reach.add(r)
                    stack.append(r)
        if a in reach and b in reach:
            return True
    return False


def check_combo(reg: Registry, skills: list[str], check_runtime: bool = False) -> ComboResult:
    conflicts: list[str] = []
    known = [s for s in skills if s in reg.skills]
    for s in skills:
        if s not in reg.skills:
            conflicts.append(f"unknown skill {s}")

    # Companions each member invokes on its own (not combo members, but their rules apply).
    closure = {m: _closure(reg, m) for m in known}
    nodes = set(known).union(*closure.values()) if known else set()

    # Rule 2: forbidden pairs. A member forbidding another member conflicts either way;
    # a member forbidding a skill inside another member's closure conflicts unless that
    # skill is also inside the forbidding member's own closure.
    for i, a in enumerate(known):
        for b in known[i + 1:]:
            if b in reg.skills[a].forbids or a in reg.skills[b].forbids:
                conflicts.append(f"forbidden pair {a}+{b}")
    for a in known:
        for s in reg.skills[a].forbids:
            if s in known or s in closure[a]:
                continue
            for b in known:
                if b != a and s in closure[b]:
                    conflicts.append(f"forbidden pair {a}+{s}(via {b})")

    # Rule 3: primary overlap over members and their closures. Each aspect collects
    # distinct source skills owning it as primary, attributed to the member(s) that bring them.
    owners: dict[str, dict[str, list[str]]] = {}
    for m in known:
        for src in [m] + closure[m]:
            for asp in reg.skills[src].primary:
                attributed = owners.setdefault(asp, {}).setdefault(src, [])
                if m not in attributed:
                    attributed.append(m)
    for asp, sources in owners.items():
        names = list(sources)
        involved: set[str] = set()
        for i, a in enumerate(names):
            for b in names[i + 1:]:
                if _coordinated(reg, a, b, nodes):
                    continue
                # Sources brought only by one and the same member are coordinated by that member.
                if any(x != y for x in sources[a] for y in sources[b]):
                    involved.update(sources[a])
                    involved.update(sources[b])
        if involved:
            conflicts.append(f"primary overlap {asp}: {', '.join(m for m in known if m in involved)}")

    # Rule 4: generation skills
    required_by_others = {
        r for s in known for r in reg.skills[s].requires if r in known and r != s
    }
    generation = [
        s for s in known
        if not set(reg.skills[s].stages) <= NON_GENERATION_STAGES and s not in required_by_others
    ]
    if len(generation) > MAX_GENERATION:
        conflicts.append(f"too many generation skills: {len(generation)}")

    # Rule 5: clarify-only skills do not belong in a combination
    for s in known:
        if reg.skills[s].stages == ["clarify"]:
            conflicts.append(f"clarify-stage skill in combo: {s}")

    # Rule 6: precedence for secondary aspects
    precedence: dict[str, str] = {}
    ignored: list[tuple[str, str]] = []
    secondary_aspects = []
    for s in known:
        for asp in reg.skills[s].secondary:
            if asp not in secondary_aspects:
                secondary_aspects.append(asp)
    for asp in secondary_aspects:
        holders = [s for s in known if asp in reg.skills[s].secondary]
        primary_members = [m for m in known if any(m in ms for ms in owners.get(asp, {}).values())]
        winner = primary_members[0] if primary_members else holders[-1]
        precedence[asp] = winner
        ignored.extend((s, asp) for s in holders if s != winner)

    # Rule 7: runtime commands
    missing: list[str] = []
    if check_runtime:
        for s in known:
            for cmd in reg.skills[s].commands:
                if shutil.which(cmd) is None:
                    missing.append(f"{s}:{cmd}")

    return ComboResult(
        ok=not conflicts and not missing,
        conflicts=conflicts,
        precedence=precedence,
        ignored=ignored,
        generation_count=len(generation),
        missing_commands=missing,
    )


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Check a writing-skill combination.")
    p.add_argument("--registry", required=True)
    p.add_argument("--check-runtime", action="store_true")
    p.add_argument("skills", nargs="+")
    args = p.parse_args(argv)
    reg = parse_registry(Path(args.registry).read_text(encoding="utf-8"))
    result = check_combo(reg, args.skills, check_runtime=args.check_runtime)
    print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
    return 0 if result.ok else 1


if __name__ == "__main__":
    sys.exit(main())

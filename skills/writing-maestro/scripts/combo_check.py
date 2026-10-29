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


def _connected_via_requires(reg: Registry, a: str, b: str, combo: list[str]) -> bool:
    """Undirected, transitive connectivity over `requires` edges inside the combo."""
    members = set(combo)
    adj: dict[str, set[str]] = {n: set() for n in members}
    for n in members:
        for r in reg.skills[n].requires:
            if r in members:
                adj[n].add(r)
                adj[r].add(n)
    seen, stack = {a}, [a]
    while stack:
        for nxt in adj[stack.pop()]:
            if nxt not in seen:
                seen.add(nxt)
                stack.append(nxt)
    return b in seen


def check_combo(reg: Registry, skills: list[str], check_runtime: bool = False) -> ComboResult:
    conflicts: list[str] = []
    known = [s for s in skills if s in reg.skills]
    for s in skills:
        if s not in reg.skills:
            conflicts.append(f"unknown skill {s}")

    # Rule 2: forbidden pairs, regardless of which side declared them
    for i, a in enumerate(known):
        for b in known[i + 1:]:
            if b in reg.skills[a].forbids or a in reg.skills[b].forbids:
                conflicts.append(f"forbidden pair {a}+{b}")

    # Rule 3: primary overlap, unless bundle companions linked by `requires`
    owners: dict[str, list[str]] = {}
    for s in known:
        for asp in reg.skills[s].primary:
            owners.setdefault(asp, []).append(s)
    for asp, names in owners.items():
        for i, a in enumerate(names):
            for b in names[i + 1:]:
                sa, sb = reg.skills[a], reg.skills[b]
                companions = (
                    sa.bundle is not None
                    and sa.bundle == sb.bundle
                    and _connected_via_requires(reg, a, b, known)
                )
                if not companions:
                    conflicts.append(f"primary overlap {asp}: {a}, {b}")

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
        primary_owners = owners.get(asp, [])
        winner = primary_owners[0] if primary_owners else holders[-1]
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

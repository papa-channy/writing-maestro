#!/usr/bin/env python3
"""Validate functional profiles and export a CSV comparison view (stdlib only)."""
from __future__ import annotations
import argparse
import csv
import json
from collections import Counter
from pathlib import Path

FIELDS = [
    "id", "repo", "path", "source_status", "normalization_level",
    "input_items", "core_operations", "output_items", "routing_boundary",
    "summary", "source_url", "source_blob_sha",
]

def validate(data: dict) -> dict:
    rows = data.get("records")
    if not isinstance(rows, list) or not rows:
        raise ValueError("records must be a nonempty list")
    ids = [r.get("id") for r in rows]
    if any(not x for x in ids) or len(ids) != len(set(ids)):
        raise ValueError("candidate IDs must be present and unique")
    counts = Counter()
    for r in rows:
        for key in ("input_items", "core_operations", "output_items"):
            if not isinstance(r.get(key), list) or any(not isinstance(x, str) for x in r[key]):
                raise ValueError(f"{r['id']}: invalid {key}")
        read = r.get("source_status") == "SKILL_BODY_READ"
        curated = r.get("normalization_level") == "ANALYST_FUNCTIONAL"
        if read and not r.get("source_blob_sha"):
            raise ValueError(f"{r['id']}: missing source blob SHA")
        if curated and (not read or any(not r[k] for k in ("input_items","core_operations","output_items"))):
            raise ValueError(f"{r['id']}: incomplete or unsupported I/O/process")
        if not curated and any(r[k] for k in ("input_items","core_operations","output_items")):
            raise ValueError(f"{r['id']}: unreviewed signature must remain empty")
        counts[(r["source_status"], r["normalization_level"])] += 1
    return {"total":len(rows),"evidence_states":{"/".join(k):v for k,v in sorted(counts.items())}}

def export_csv(rows: list[dict], destination: Path):
    destination.parent.mkdir(parents=True,exist_ok=True)
    with destination.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=FIELDS)
        writer.writeheader()
        for r in rows:
            writer.writerow({
                "id":r["id"],"repo":r["repo"],"path":r["path"],
                "source_status":r["source_status"],
                "normalization_level":r["normalization_level"],
                "input_items":" → ".join(r["input_items"]),
                "core_operations":" → ".join(r["core_operations"]),
                "output_items":" → ".join(r["output_items"]),
                "routing_boundary":r.get("routing_boundary") or "",
                "summary":(r.get("description") or "")[:280],
                "source_url":r["source_url"],
                "source_blob_sha":r.get("source_blob_sha") or "",
            })

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",type=Path,default=Path("research/normalization/functional_profiles.json"))
    p.add_argument("--output",type=Path,default=Path("research/normalization/functional_matrix.csv"))
    p.add_argument("--check-only",action="store_true")
    args=p.parse_args()
    d=json.loads(args.input.read_text(encoding="utf-8"))
    print(json.dumps(validate(d),ensure_ascii=False,indent=2))
    if not args.check_only:
        export_csv(d["records"],args.output)
        print(f"Wrote {args.output}")

if __name__=="__main__":
    main()

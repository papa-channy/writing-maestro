#!/usr/bin/env python3
"""Rebuild Writing Maestro evidence-aware comparison views. Python stdlib only.

No fixed cluster taxonomy and no model/runtime quality assertions.
"""
from __future__ import annotations
import argparse
import csv
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

FIELDS = ["id","repo","path","source_status","normalization_level","task_intent",
          "input_items","core_operations","output_items","declared_effect",
          "routing_boundary","input_confidence","process_confidence","output_confidence",
          "source_blob_sha","source_url"]
STOP = set("""the a of or and to for in on as with from when then into by an at against one
user users project documents document report reports write writing create draft review
reviews data sources source this that those these using skill helps uses when should
it your their you are can will which via such any all new existing""".split())

def validate(records):
    if len(records) != 405:  # inventory snapshot; do not silently drop candidates
        raise ValueError(f"expected 405 inventory records, got {len(records)}")
    ids = [r.get("id") for r in records]
    if None in ids or len(set(ids)) != len(ids):
        raise ValueError("candidate IDs must be unique and non-null")
    for r in records:
        if r.get("source_status") != "SKILL_BODY_READ" or not r.get("source_blob_sha"):
            raise ValueError(f"{r['id']}: source body/blob SHA missing")
        for field in ("input_items","core_operations","output_items"):
            if not isinstance(r.get(field), list) or any(not isinstance(x, str) for x in r[field]):
                raise ValueError(f"{r['id']}: invalid {field}")
        level = r.get("normalization_level")
        if level == "ANALYST_FUNCTIONAL" and not all(r[k] for k in ("input_items","core_operations","output_items")):
            raise ValueError(f"{r['id']}: incomplete analyst abstraction")
        if level == "SOURCE_DERIVED_FUNCTIONAL" and not r.get("task_intent"):
            raise ValueError(f"{r['id']}: source-derived record lacks task intent")
        if level not in ("ANALYST_FUNCTIONAL","SOURCE_DERIVED_FUNCTIONAL"):
            raise ValueError(f"{r['id']}: unsupported evidence level {level}")
    return dict(Counter(r["normalization_level"] for r in records))

def write_csv(records, path):
    with path.open("w", encoding="utf-8", newline="") as fh:
        w=csv.writer(fh)
        w.writerow(FIELDS)
        for r in records:
            c=r.get("inference_confidence") or {}
            w.writerow([r["id"],r["repo"],r["path"],r["source_status"],r["normalization_level"],
                        r.get("task_intent") or "", " → ".join(r["input_items"]),
                        " → ".join(r["core_operations"]), " → ".join(r["output_items"]),
                        r.get("declared_effect") or "",r.get("routing_boundary") or "",
                        c.get("input","ANALYST_ABSTRACTION"),c.get("process","ANALYST_ABSTRACTION"),
                        c.get("output","ANALYST_ABSTRACTION"),r["source_blob_sha"],r["source_url"]])

def weighted_tokens(r):
    blocks=[(r.get("task_intent") or r.get("description") or "",1.4),
            (r.get("declared_effect") or "",.8)]
    blocks += [(x,1.2) for x in r["input_items"]]
    blocks += [(x,1.7) for x in r["output_items"]]
    blocks += [(x,2.0) for x in r["core_operations"]]
    out=[]
    for text,weight in blocks:
        tokens=[t for t in re.findall(r"[a-z][a-z0-9-]{2,}|[가-힣]{2,}",text.lower()) if t not in STOP]
        for i,t in enumerate(tokens):
            out.append((t,weight))
            if i:
                out.append((tokens[i-1]+"_"+t,weight*1.1))
    return out

def nearest_pairs(records, limit):
    docs=[weighted_tokens(r) for r in records]
    df=Counter(token for doc in docs for token in {w for w,_ in doc})
    vectors=[]
    for doc in docs:
        tf=defaultdict(float)
        for word,weight in doc:
            tf[word]+=weight
        raw={w:(1+math.log(t))*math.log(1+(len(records)+1)/(1+df[w])) for w,t in tf.items()}
        norm=math.sqrt(sum(t*t for t in raw.values())) or 1.0
        vectors.append({w:t/norm for w,t in raw.items()})
    pairs=[]
    for i,vec in enumerate(vectors):
        for j in range(i+1,len(vectors)):
            other=vectors[j]
            a,b=(vec,other) if len(vec)<=len(other) else (other,vec)
            sim=sum(v*b.get(w,0) for w,v in a.items())
            if sim>.08:
                pairs.append((sim,i,j))
    pairs.sort(key=lambda x:-x[0])
    return pairs[:limit]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input",type=Path,default=Path("research/normalization/functional_profiles.json"))
    ap.add_argument("--directory",type=Path,default=Path("research/normalization"))
    ap.add_argument("--top",type=int,default=300)
    ap.add_argument("--check-only",action="store_true")
    ap.add_argument("--matrix-only",action="store_true")
    ap.add_argument("--neighbors-only",action="store_true")
    args=ap.parse_args()
    records=json.loads(args.input.read_text(encoding="utf-8"))["records"]
    print(json.dumps({"total":len(records),"levels":validate(records),
                      "missing_input":sum(not r["input_items"] for r in records),
                      "missing_process":sum(not r["core_operations"] for r in records),
                      "missing_output":sum(not r["output_items"] for r in records)},indent=2))
    if args.check_only: return
    args.directory.mkdir(parents=True,exist_ok=True)
    if not args.neighbors_only:
        write_csv(records,args.directory/"functional_matrix.csv")
        compact=[{"id":r["id"],"repo":r["repo"],"path":r["path"],"sha":r["source_blob_sha"],
                  "level":r["normalization_level"],"task_intent":r.get("task_intent"),
                  "input":r["input_items"],"process":r["core_operations"],
                  "output":r["output_items"],"declared_effect":r.get("declared_effect"),
                  "boundary":r.get("routing_boundary"),"confidence":r.get("inference_confidence")} for r in records]
        (args.directory/"functional_profiles_compact.json").write_text(
            json.dumps({"schema_version":"0.3.0","total":len(records),"records":compact},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        sha=defaultdict(list)
        for r in records:
            sha[r["source_blob_sha"]].append({"id":r["id"],"repo":r["repo"],"path":r["path"]})
        duplicates=[{"sha":k,"count":len(v),"members":v} for k,v in sha.items() if len(v)>1]
        duplicates.sort(key=lambda x:-x["count"])
        (args.directory/"source_duplicate_groups.json").write_text(
            json.dumps({"groups":duplicates,"unique_source_hashes":len(sha)},indent=2)+"\n",encoding="utf-8")
    if not args.matrix_only:
        pairs=nearest_pairs(records,args.top)
        with (args.directory/"similarity_neighbors.csv").open("w",encoding="utf-8",newline="") as fh:
            writer=csv.writer(fh)
            writer.writerow(["rank","skill_a","skill_b","similarity","same_source_sha","same_repository","comparison_status"])
            for n,(score,i,j) in enumerate(pairs,1):
                a,b=records[i],records[j]
                writer.writerow([n,a["id"],b["id"],f"{score:.4f}",
                                 str(a["source_blob_sha"]==b["source_blob_sha"]).lower(),
                                 str(a["repo"]==b["repo"]).lower(),"NEEDS_SEMANTIC_REVIEW"])
        print(f"wrote {len(pairs)} similarity candidates; similarity is NOT evidence of interchangeability")

if __name__=="__main__": main()

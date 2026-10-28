#!/usr/bin/env python3
"""Rank potential neighbors by functional I/P/O text, without using cluster labels."""
import argparse
import csv
import json
import math
import re
from collections import Counter
from pathlib import Path

STOP = set("the a of or and to for in on as with from when then into by an at against one user users project documents document report reports write writing create draft review reviews data sources source".split())

def words(profile):
    text = profile["input_items"] + profile["core_operations"] * 2 + profile["output_items"]
    terms = []
    for segment in text:
        toks = [x for x in re.findall(r"[a-z][a-z0-9-]{2,}|[가-힣]{2,}", segment.lower()) if x not in STOP]
        for i, token in enumerate(toks):
            terms.append(token)
            if i:
                terms.append(toks[i - 1] + "_" + token)
    return terms

def neighbors(records, maximum=150):
    curated = [x for x in records if x["normalization_level"] == "ANALYST_FUNCTIONAL"]
    docs = [words(x) for x in curated]
    df = Counter(x for doc in docs for x in set(doc))
    vecs = []
    for doc in docs:
        counts = Counter(doc)
        weighted = {word: (1 + math.log(count)) * math.log(1 + (len(docs) + 1) / (1 + df[word])) for word, count in counts.items()}
        magnitude = math.sqrt(sum(x * x for x in weighted.values())) or 1.0
        vecs.append({key: value / magnitude for key, value in weighted.items()})
    ranked = []
    for i, a in enumerate(vecs):
        for j in range(i + 1, len(vecs)):
            b = vecs[j]
            score = sum(v * b.get(k, 0) for k, v in a.items())
            ranked.append((score, curated[i]["id"], curated[j]["id"]))
    return sorted(ranked, key=lambda r: -r[0])[:maximum]

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", type=Path, default=Path("research/normalization/functional_profiles.json"))
    p.add_argument("--output", type=Path, default=Path("research/normalization/similarity_neighbors.csv"))
    p.add_argument("--top", type=int, default=150)
    args = p.parse_args()
    records = json.loads(args.input.read_text(encoding="utf-8"))["records"]
    ranked = neighbors(records, args.top)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["rank", "skill_a", "skill_b", "similarity", "comparison_status", "interpretation"])
        for i, (value, a, b) in enumerate(ranked, 1):
            writer.writerow([i, a, b, f"{value:.4f}", "NEEDS_SEMANTIC_REVIEW",
                             "Text similarity is not proof of functional substitutability"])
    print(f"ranked {len(ranked)} pairs from {len([r for r in records if r['normalization_level']=='ANALYST_FUNCTIONAL'])} profiles")

if __name__ == "__main__":
    main()

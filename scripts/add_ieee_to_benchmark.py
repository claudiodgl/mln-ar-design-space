"""Add IEEE Xplore retrievals to output/benchmark_recall.csv and recompute
output/recall_by_source.csv without re-running merge_dedupe.py (see
merge_ieee_incremental.py for why). Idempotent.
Usage: python -I -X utf8 scripts/add_ieee_to_benchmark.py
"""
import csv, sys
from collections import defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from benchmark import BENCH, current_versions, match
from common import OUT, RAW, read_jsonl

cur = current_versions()
hits = defaultdict(set)
for f in sorted((RAW / "ieee").glob("*.jsonl")):
    if ("ieee", f.stem) in cur:
        for r in read_jsonl(f):
            if m := match(r):
                hits[m].add(f"ieee:{f.stem}")
p = OUT / "benchmark_recall.csv"
rows = list(csv.DictReader(open(p, encoding="utf-8-sig")))
cols = list(rows[0].keys())
for r in rows:
    toks = [t.strip() for t in r["retrieved_by_search"].split(";") if t.strip() and not t.strip().startswith("ieee:")]
    toks += sorted(hits.get(r["bid"], ()))
    r["retrieved_by_search"] = "; ".join(toks)
    r["n_search_hits"] = str(len(toks))
    snow = [t for t in r["retrieved_by_snowballing"].split(";") if t.strip()]
    r["reachable_only_by_snowballing"] = "yes" if snow and not toks else "no"
    r["retrieved"] = "yes" if toks or snow else "NO"
with open(p, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)

per = defaultdict(set)
for r in rows:
    toks = [t.strip() for t in r["retrieved_by_search"].split(";") if t.strip()]
    snow = [t.strip() for t in r["retrieved_by_snowballing"].split(";") if t.strip()]
    for t in toks:
        s, q = t.split(":", 1)
        per[f"search:{s}"].add(r["bid"]); per[f"query:{q.split('_')[0]}"].add(r["bid"]); per[f"query:{s}:{q}"].add(r["bid"])
    for t in snow:
        rnd = t.split(":")[0]
        per[f"snowball:{rnd}"].add(r["bid"])
    if toks: per["ALL searches"].add(r["bid"])
    if snow: per["ALL snowballing"].add(r["bid"])
    if toks or snow: per["search OR snowballing"].add(r["bid"])
allb = {r["bid"] for r in rows}
rec = [{"scope": k, "recall": f"{len(v)}/{len(allb)}", "recall_pct": round(100 * len(v) / len(allb), 1),
        "missing": " ".join(sorted(allb - v))} for k, v in sorted(per.items())]
with open(OUT / "recall_by_source.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=["scope", "recall", "recall_pct", "missing"]); w.writeheader(); w.writerows(rec)
for x in rec:
    if x["scope"].count(":") <= 1:
        print(f"{x['scope']:28s} {x['recall']:>6s}  missing: {x['missing']}")

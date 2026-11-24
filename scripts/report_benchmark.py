"""Write the benchmark (gold-standard) recall report from output/candidates_all.csv.

Outputs:
  output/benchmark_recall.csv   one row per Table-2 work: every search
                                (source:query_version) and snowballing path
                                (round:seed:direction:index) that retrieved it
  output/recall_by_source.csv   recall of the 24 per source, per query, and
                                for search-only / snowball-only / combined
Usage: python -I scripts/report_benchmark.py
"""
from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import CONFIG, OUT, read_csv, write_csv  # noqa: E402

SEEDS = {s["sid"]: s["title"] for s in read_csv(CONFIG / "seeds.csv")}


def main():
    bench = read_csv(CONFIG / "benchmark.csv")
    cands = {c["benchmark_id"]: c for c in read_csv(OUT / "candidates_all.csv") if c["benchmark_id"]}
    per_key = defaultdict(set)
    rows = []
    for b in bench:
        c = cands.get(b["bid"])
        prov = c["provenance"].split(" | ") if c else []
        search = [p for p in prov if not p.startswith("R")]
        snow = [p for p in prov if p.startswith("R")]
        for p in search:
            src, q = p.split(":", 1)
            per_key[f"search:{src}"].add(b["bid"])
            per_key[f"query:{q.split('_')[0]}"].add(b["bid"])
            per_key[f"query:{src}:{q}"].add(b["bid"])
        for p in snow:
            rnd, sid, dirn, api = p.split(":")
            per_key[f"snowball:{rnd}:{sid}"].add(b["bid"])
            per_key[f"snowball:{rnd}:{dirn}"].add(b["bid"])
            per_key[f"snowball-index:{api}"].add(b["bid"])
        if search:
            per_key["ALL searches"].add(b["bid"])
        if snow:
            per_key["ALL snowballing R1"].add(b["bid"])
        if prov:
            per_key["search OR snowballing"].add(b["bid"])
        seeds = sorted({p.split(":")[1] for p in snow})
        rows.append({
            "bid": b["bid"], "work": b["short"], "platform": b["platform"], "year": b["year"],
            "doi": b["doi"], "proposed_criterion": b["proposed_criterion"],
            "candidate_id": c["cid"] if c else "",
            "n_search_hits": len(search),
            "retrieved_by_search": "; ".join(search),
            "retrieved_by_snowballing": "; ".join(snow),
            "snowball_seeds": "; ".join(f"{s} ({SEEDS.get(s, '')[:45]})" for s in seeds),
            "reachable_only_by_snowballing": "yes" if snow and not search else "no",
            "retrieved": "yes" if prov else "NO",
            "prefilter_suggestion": c["suggestion"] if c else "",
        })
    write_csv(OUT / "benchmark_recall.csv", rows, list(rows[0].keys()))
    allb = {b["bid"] for b in bench}
    rec = [{"scope": k, "recall": f"{len(v)}/{len(bench)}", "recall_pct": round(100 * len(v) / len(bench), 1),
            "missing": " ".join(sorted(allb - v))} for k, v in sorted(per_key.items())]
    write_csv(OUT / "recall_by_source.csv", rec, ["scope", "recall", "recall_pct", "missing"])
    for r in rec:
        if not r["scope"].startswith("query:") or r["scope"].count(":") == 1:
            print(f"{r['scope']:32s} {r['recall']:>6s}  missing: {r['missing']}")


if __name__ == "__main__":
    main()

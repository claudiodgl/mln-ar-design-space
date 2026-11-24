"""Match retrieved records against the 24 benchmark works (config/benchmark.csv).

Matching: normalised DOI, arXiv id, or normalised title (exact, or
difflib ratio >= 0.92 with same first 3 words) -- conservative, so a match
always denotes the same work (publisher version or preprint of it).

Usage:
  python -I scripts/benchmark.py                       # recall per raw file
  python -I scripts/benchmark.py --write               # + output/benchmark_recall.csv
"""
from __future__ import annotations

import argparse
import difflib
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import CONFIG, OUT, RAW, norm_arxiv, norm_doi, norm_title, read_csv, read_jsonl, write_csv  # noqa: E402

BENCH = read_csv(CONFIG / "benchmark.csv")
for b in BENCH:
    b["_doi"], b["_arx"], b["_t"] = norm_doi(b["doi"]), norm_arxiv(b["arxiv"]), norm_title(b["title"])


def match(rec: dict) -> str | None:
    d, a, t = norm_doi(rec.get("doi")), norm_arxiv(rec.get("arxiv")), norm_title(rec.get("title"))
    for b in BENCH:
        if d and d == b["_doi"]:
            return b["bid"]
        if a and b["_arx"] and a == b["_arx"]:
            return b["bid"]
    if not t:
        return None
    for b in BENCH:
        if t == b["_t"]:
            return b["bid"]
        if t.split()[:3] == b["_t"].split()[:3] and difflib.SequenceMatcher(None, t, b["_t"]).ratio() >= 0.92:
            return b["bid"]
    return None


ALL_SOURCES = ["openalex", "s2", "arxiv", "egdl", "dblp", "ieee", "acm"]


def current_versions() -> set[tuple[str, str]]:
    """(source, '<QID>_<ver>') pairs of the current, non-retired query versions."""
    from common import load_queries
    out = set()
    for q in load_queries()["queries"]:
        if q.get("retired"):
            continue
        for src in q.get("sources", ALL_SOURCES):
            out.add((src, f"{q['id']}_{q['version']}"))
    return out


def raw_files(all_versions: bool = False):
    """Yield (source, path) for current query versions, snowballing and exports."""
    cur = current_versions()
    for sub in sorted(RAW.iterdir()):
        if sub.is_dir() and sub.name not in ("cache",):
            for f in sorted(sub.glob("*.jsonl")):
                if sub.name == "snowball" or all_versions or (sub.name, f.stem) in cur:
                    yield sub.name, f


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--all-versions", action="store_true")
    a = ap.parse_args()
    union = defaultdict(set)
    hits = defaultdict(list)  # bid -> list of "source:file"
    print(f"{'file':45s} {'n':>6s}  recall  matched")
    for src, f in raw_files(a.all_versions):
        recs = read_jsonl(f)
        got = sorted({m for r in recs if (m := match(r))})
        print(f"{src + '/' + f.stem:45s} {len(recs):6d}  {len(got):2d}/24  {' '.join(got)}")
        for bid in got:
            hits[bid].append(f"{src}/{f.stem}")
            union[src if src != "snowball" else "snowball:" + f.stem.split("_")[0]].add(bid)
    print("\nUnion per source:")
    allb = {b["bid"] for b in BENCH}
    for k, v in sorted(union.items()):
        print(f"  {k:22s} {len(v):2d}/24  missing: {' '.join(sorted(allb - v))}")
    searched = set().union(*[v for k, v in union.items() if not k.startswith("snowball")])
    print(f"  {'ALL DB SEARCHES':22s} {len(searched):2d}/24  missing: {' '.join(sorted(allb - searched))}")
    every = set().union(*union.values())
    print(f"  {'SEARCH+SNOWBALL':22s} {len(every):2d}/24  missing: {' '.join(sorted(allb - every))}")
    if a.write:
        rows = []
        for b in BENCH:
            h = hits.get(b["bid"], [])
            srch = [x for x in h if not x.startswith("snowball")]
            snow = [x for x in h if x.startswith("snowball")]
            rows.append({"bid": b["bid"], "work": b["short"], "platform": b["platform"],
                         "doi": b["doi"], "retrieved_by_search": "; ".join(srch),
                         "retrieved_by_snowballing": "; ".join(snow),
                         "retrieved_any": "yes" if h else "NO"})
        write_csv(OUT / "benchmark_recall_by_file.csv", rows, list(rows[0].keys()))
        print("wrote", OUT / "benchmark_recall_by_file.csv")


if __name__ == "__main__":
    main()

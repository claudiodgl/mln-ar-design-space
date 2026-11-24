"""IEEE Xplore Metadata API client.

Requires a free API key: register at https://developer.ieee.org/ (create an
account -> "Register your application" -> Metadata Search API). Then:

    export IEEE_API_KEY=xxxxxxxx          (Git Bash)
    $env:IEEE_API_KEY = "xxxxxxxx"         (PowerShell)
    .venv/Scripts/python -I scripts/search_ieee.py

Without the key the script prints the exact command-search strings so they can
be pasted into https://ieeexplore.ieee.org/search/advanced/command and the
result exported as CSV (Export -> CSV); ingest that file with
scripts/ingest_export.py --source ieee <file.csv>.

Output: raw/ieee/<QID>_<ver>.jsonl
"""
from __future__ import annotations

import argparse
import re
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import RAW, get, log_run, record, write_jsonl  # noqa: E402
from querybuild import iter_queries  # noqa: E402

BASE = "https://ieeexploreapi.ieee.org/api/v1/search/articles"
PAGE = 200


def fetch(key: str, s: str, q: dict) -> tuple[int, list[dict]]:
    start, total, rows = 1, None, []
    while total is None or start <= total:
        d = get(BASE, {"apikey": key, "querytext": s, "max_records": PAGE,
                       "start_record": start, "format": "json"})
        total = int(d.get("total_records", 0))
        arts = d.get("articles") or []
        for x in arts:
            auth = "; ".join(au.get("full_name", "") for au in
                             (x.get("authors", {}).get("authors") or [])[:6])
            rows.append(record(source="ieee", query_id=q["id"], query_version=q["version"],
                               title=x.get("title", ""), year=x.get("publication_year", ""),
                               venue=x.get("publication_title", ""), doi=x.get("doi", ""),
                               type=x.get("content_type", ""), authors=auth,
                               abstract=x.get("abstract", "")))
        if not arts:
            break
        start += PAGE
    return total or 0, rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    only = set(a.only.split(",")) if a.only else None
    key = os.environ.get("IEEE_API_KEY", "").strip()
    for q, subs in iter_queries("ieee", only):
        if not key:
            for i, s in enumerate(subs, 1):
                print(f"[{q['id']} {q['version']} part {i}/{len(subs)}] IEEE_API_KEY not set. "
                      f"Command search string:\n{s}\n")
            continue
        rows, totals = [], []
        for s in subs:
            t, r = fetch(key, s, q)
            totals.append(t)
            rows += r
        if q.get("venue_restricted"):
            # same venue scope as the DBLP list (IEEE part of it)
            keep = re.compile(r"visualization and computer graphics|computer graphics and applications|"
                              r"visualization conference|vis\b|pacific visualization|virtual reality|"
                              r"mixed and augmented reality|ismar|3d user interfaces", re.I)
            rows = [r for r in rows if keep.search(r["venue"] or "")]
        print(f"IEEE {q['id']} {q['version']}: sub-query hits={totals} retrieved={len(rows)} (before de-dup)")
        write_jsonl(RAW / "ieee" / f"{q['id']}_{q['version']}.jsonl", rows)
        log_run("ieee", q["id"], q["version"], "  UNION  ".join(subs), sum(totals), len(rows),
                f"{len(subs)} sub-queries; reported = sum of sub-query hits")


if __name__ == "__main__":
    main()

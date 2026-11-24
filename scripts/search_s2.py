"""Semantic Scholar bulk search (title+abstract, boolean) for every query.

Usage: python -I scripts/search_s2.py [--only Q1] [--count-only]
Env:   S2_API_KEY (optional; keyless works but is rate-limited and shared)
Output: raw/s2/<QID>_<ver>.jsonl
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import RAW, get, log_run, record, write_jsonl  # noqa: E402
from querybuild import iter_queries  # noqa: E402

BASE = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"
FIELDS = "title,year,venue,externalIds,abstract,publicationTypes,authors"


def headers():
    k = os.environ.get("S2_API_KEY")
    return {"x-api-key": k} if k else None


def s2_to_record(p: dict, **kw) -> dict:
    ex = p.get("externalIds") or {}
    auth = "; ".join(a.get("name", "") for a in (p.get("authors") or [])[:6])
    return record(title=p.get("title") or "", year=p.get("year") or "", venue=p.get("venue") or "",
                  doi=ex.get("DOI") or "", arxiv=ex.get("ArXiv") or "", s2_id=p.get("paperId") or "",
                  dblp_key=ex.get("DBLP") or "", type=",".join(p.get("publicationTypes") or []),
                  authors=auth, abstract=p.get("abstract") or "", **kw)


def search(q: str, count_only=False):
    rows, token, total = [], None, None
    while True:
        params = {"query": q, "fields": FIELDS}
        if token:
            params["token"] = token
        d = get(BASE, params, headers=headers())
        total = d.get("total")
        if count_only:
            return [], total
        rows += d.get("data") or []
        token = d.get("token")
        if not token:
            break
    return rows, total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--count-only", action="store_true")
    a = ap.parse_args()
    only = set(a.only.split(",")) if a.only else None
    for q, s in iter_queries("s2", only):
        rows, total = search(s, a.count_only)
        print(f"S2 {q['id']} {q['version']}: reported={total} retrieved={len(rows)}")
        if a.count_only:
            log_run("s2", q["id"], q["version"], s, total, 0, "count only"); continue
        recs = [s2_to_record(p, source="s2", query_id=q["id"], query_version=q["version"]) for p in rows]
        write_jsonl(RAW / "s2" / f"{q['id']}_{q['version']}.jsonl", recs)
        log_run("s2", q["id"], q["version"], s, total, len(recs))


if __name__ == "__main__":
    main()

"""OpenAlex works search (title+abstract, boolean) for every query in config/queries.json.

Usage:  python -I scripts/search_openalex.py [--only Q1,Q2] [--count-only]
Env:    OPENALEX_API_KEY (optional, recommended: keyless calls share a small
        daily budget per IP), MAILTO (optional polite-pool contact, default empty).
Output: raw/openalex/<QID>_<ver>.jsonl
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import RAW, MAILTO, get, inverted_to_text, log_run, record, write_jsonl  # noqa: E402
from querybuild import iter_queries  # noqa: E402

BASE = "https://api.openalex.org/works"
SELECT = ("id,doi,title,publication_year,primary_location,type,authorships,"
          "abstract_inverted_index,ids")


def auth_params() -> dict:
    p = {}
    if os.environ.get("OPENALEX_API_KEY"):
        p["api_key"] = os.environ["OPENALEX_API_KEY"]
    if MAILTO:
        p["mailto"] = MAILTO
    return p


def oa_to_record(w: dict, **kw) -> dict:
    loc = w.get("primary_location") or {}
    src = (loc.get("source") or {}).get("display_name", "")
    ids = w.get("ids") or {}
    arx = ""
    for l in [loc] + (w.get("locations") or []):
        u = (l or {}).get("landing_page_url") or ""
        if "arxiv.org/abs/" in u:
            arx = u
    auth = "; ".join(a.get("author", {}).get("display_name", "") for a in (w.get("authorships") or [])[:6])
    return record(title=w.get("title") or "", year=w.get("publication_year") or "",
                  venue=src, doi=w.get("doi") or "", arxiv=arx,
                  openalex_id=(w.get("id") or "").rsplit("/", 1)[-1],
                  type=w.get("type") or "", authors=auth,
                  abstract=inverted_to_text(w.get("abstract_inverted_index")), **kw)


def search(filter_value: str, field: str = "title_and_abstract.search", per_page=200, count_only=False):
    """Page-based paging (cursor paging returned HTTP 401 without an API key)."""
    rows, total, page = [], None, 1
    while True:
        params = {"filter": f"{field}:{filter_value}", "per_page": 1 if count_only else per_page,
                  "page": page, "select": SELECT, **auth_params()}
        d = get(BASE, params)
        total = d["meta"]["count"]
        if count_only:
            return [], total
        rows += d["results"]
        if not d["results"] or len(rows) >= total:
            break
        page += 1
    return rows, total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--count-only", action="store_true")
    a = ap.parse_args()
    only = set(a.only.split(",")) if a.only else None
    for q, s in iter_queries("openalex", only):
        field = q.get("openalex_field", "title_and_abstract.search")
        works, total = search(s, field, count_only=a.count_only)
        print(f"OpenAlex {q['id']} {q['version']}: reported={total} retrieved={len(works)}")
        if a.count_only:
            log_run("openalex", q["id"], q["version"], f"{field}:{s}", total, 0, "count only")
            continue
        recs = [oa_to_record(w, source="openalex", query_id=q["id"], query_version=q["version"]) for w in works]
        write_jsonl(RAW / "openalex" / f"{q['id']}_{q['version']}.jsonl", recs)
        log_run("openalex", q["id"], q["version"], f"{field}:{s}", total, len(recs))


if __name__ == "__main__":
    main()

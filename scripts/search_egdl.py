"""Eurographics Digital Library (https://diglib.eg.org, DSpace 7) search via its
public REST discovery endpoint. Fielded Solr query on dc.title,
dc.description.abstract and dc.subject (author keywords). Covers CGF, EuroVis
(full/short papers, STARs), EGVE/ICAT-EGVE, EuroVA, etc.

Usage: python -I scripts/search_egdl.py [--only Q1]
Output: raw/egdl/<QID>_<ver>.jsonl
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import RAW, get, log_run, record, write_jsonl  # noqa: E402
from querybuild import iter_queries  # noqa: E402

BASE = "https://diglib.eg.org/server/api/discover/search/objects"
PAGE = 100


def _m(md, k):
    v = md.get(k) or []
    return v[0]["value"] if v else ""


def to_record(o: dict) -> dict:
    md = o.get("metadata") or {}
    return record(title=_m(md, "dc.title"), year=_m(md, "dc.date.issued")[:4],
                  venue=_m(md, "dc.description.seriesinformation") or _m(md, "dc.publisher"),
                  doi=_m(md, "dc.identifier.doi"),
                  authors="; ".join(a["value"] for a in (md.get("dc.contributor.author") or [])[:6]),
                  abstract=_m(md, "dc.description.abstract"), type="egdl-item")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    only = set(a.only.split(",")) if a.only else None
    for q, s in iter_queries("egdl", only):
        page, rows, total = 0, [], None
        while True:
            d = get(BASE, {"query": s, "dsoType": "ITEM", "size": PAGE, "page": page})
            sr = d["_embedded"]["searchResult"]
            total = sr["page"]["totalElements"]
            objs = sr.get("_embedded", {}).get("objects", [])
            rows += [to_record(x["_embedded"]["indexableObject"]) for x in objs if "_embedded" in x]
            page += 1
            if page >= sr["page"]["totalPages"] or not objs:
                break
        for r in rows:
            r.update(source="egdl", query_id=q["id"], query_version=q["version"])
        print(f"EGDL {q['id']} {q['version']}: reported={total} retrieved={len(rows)}")
        write_jsonl(RAW / "egdl" / f"{q['id']}_{q['version']}.jsonl", rows)
        log_run("egdl", q["id"], q["version"], s, total, len(rows))


if __name__ == "__main__":
    main()

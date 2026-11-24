"""arXiv API search (ti/abs fields) for every query. 1 request per 3 s.

Usage: python -I scripts/search_arxiv.py [--only Q1]
Output: raw/arxiv/<QID>_<ver>.jsonl
"""
from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import RAW, get, log_run, record, write_jsonl  # noqa: E402
from querybuild import iter_queries  # noqa: E402

BASE = "https://export.arxiv.org/api/query"
NS = {"a": "http://www.w3.org/2005/Atom", "o": "http://a9.com/-/spec/opensearch/1.1/",
      "x": "http://arxiv.org/schemas/atom"}
PAGE = 200


def parse(xml: str):
    root = ET.fromstring(xml)
    total = int(root.find("o:totalResults", NS).text)
    out = []
    for e in root.findall("a:entry", NS):
        aid = e.find("a:id", NS).text.rsplit("/abs/", 1)[-1]
        doi_el = e.find("x:doi", NS)
        jr = e.find("x:journal_ref", NS)
        out.append(record(
            title=re.sub(r"\s+", " ", e.find("a:title", NS).text or "").strip(),
            year=(e.find("a:published", NS).text or "")[:4],
            venue=(jr.text if jr is not None else "arXiv"),
            doi=(doi_el.text if doi_el is not None else ""), arxiv=aid,
            authors="; ".join(a.find("a:name", NS).text for a in e.findall("a:author", NS)[:6]),
            abstract=re.sub(r"\s+", " ", e.find("a:summary", NS).text or "").strip(),
            type="preprint"))
    return total, out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    only = set(a.only.split(",")) if a.only else None
    for q, s in iter_queries("arxiv", only):
        start, rows, total = 0, [], None
        while total is None or start < total:
            xml = get(BASE, {"search_query": s, "start": start, "max_results": PAGE,
                             "sortBy": "submittedDate", "sortOrder": "ascending"}, accept="text")
            total, recs = parse(xml)
            rows += recs
            if not recs:
                break
            start += PAGE
        for r in rows:
            r.update(source="arxiv", query_id=q["id"], query_version=q["version"])
        print(f"arXiv {q['id']} {q['version']}: reported={total} retrieved={len(rows)}")
        write_jsonl(RAW / "arxiv" / f"{q['id']}_{q['version']}.jsonl", rows)
        log_run("arxiv", q["id"], q["version"], s, total, len(rows))


if __name__ == "__main__":
    main()

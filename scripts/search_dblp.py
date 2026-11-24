"""Venue-restricted DBLP search (titles only) through the public dblp SPARQL
endpoint https://sparql.dblp.org (the dblp HTML/JSON search API is currently
behind a browser challenge and unusable from scripts).

Each AND-group of a query becomes one case-insensitive REGEX on the title; the
search is restricted to the venue streams in VENUES below.

Usage: python -I scripts/search_dblp.py [--only Q1]
Output: raw/dblp/<QID>_<ver>.jsonl
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import RAW, get, log_run, record, write_jsonl  # noqa: E402
from querybuild import iter_queries  # noqa: E402

ENDPOINT = "https://sparql.dblp.org/sparql"
# Visualization, HCI, VR/AR and graph-drawing venues (dblp stream ids)
VENUES = [
    "journals/tvcg", "journals/cgf", "journals/cga", "journals/ivs", "journals/vi",
    "journals/tochi", "journals/pacmhci",
    "conf/visualization", "conf/apvis", "conf/vissym", "conf/eurova",
    "conf/chi", "conf/uist", "conf/tei", "conf/iss",
    "conf/vr", "conf/ismar", "conf/vrst", "conf/sui", "conf/egve", "conf/ivapp",
    "conf/gd",
]


def sparql(regexes: list[str]) -> str:
    vals = " ".join(f"<https://dblp.org/streams/{v}>" for v in VENUES)
    filt = "\n".join(f'  FILTER(REGEX(?title, "{r}", "i"))' for r in regexes)
    return f"""PREFIX dblp: <https://dblp.org/rdf/schema#>
SELECT ?publ ?title ?year ?doi ?stream (GROUP_CONCAT(DISTINCT ?aname; separator="; ") AS ?authors) WHERE {{
  VALUES ?stream {{ {vals} }}
  ?publ dblp:publishedInStream ?stream ; dblp:title ?title .
{filt}
  OPTIONAL {{ ?publ dblp:yearOfPublication ?year }}
  OPTIONAL {{ ?publ dblp:doi ?doi }}
  OPTIONAL {{ ?publ dblp:authoredBy ?a . ?a dblp:primaryCreatorName ?aname }}
}} GROUP BY ?publ ?title ?year ?doi ?stream"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    only = set(a.only.split(",")) if a.only else None
    for q, regs in iter_queries("dblp", only):
        # SPARQL string literal: escape backslashes
        regs_esc = [r.replace("\\", "\\\\") for r in regs]
        qs = sparql(regs_esc)
        d = get(ENDPOINT, {"query": qs}, headers={"Accept": "application/sparql-results+json"})
        rows = []
        seen = set()
        for b in d["results"]["bindings"]:
            key = b["publ"]["value"]
            if key in seen:
                continue
            seen.add(key)
            rows.append(record(source="dblp", query_id=q["id"], query_version=q["version"],
                               title=b["title"]["value"].rstrip("."),
                               year=b.get("year", {}).get("value", ""),
                               venue=b["stream"]["value"].rsplit("/streams/", 1)[-1],
                               doi=b.get("doi", {}).get("value", ""),
                               dblp_key=key.rsplit("/rec/", 1)[-1],
                               authors=b.get("authors", {}).get("value", "")))
        print(f"DBLP {q['id']} {q['version']}: retrieved={len(rows)}")
        write_jsonl(RAW / "dblp" / f"{q['id']}_{q['version']}.jsonl", rows)
        log_run("dblp", q["id"], q["version"], " AND ".join(regs) + f"  [venues: {', '.join(VENUES)}]",
                len(rows), len(rows))


if __name__ == "__main__":
    main()

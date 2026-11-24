"""Ingest a manual export from a digital library into the common record format.

ACM DL has no public search API. Procedure (see protocol.md, Sec. 3):
  1. open https://dl.acm.org/search/advanced, click "Edit search"/query syntax,
     paste the string printed by `python -I scripts/querybuild.py` (acm block),
     set "Search within: The ACM Full-Text Collection" (not the Guide).
  2. on the result page: select all (up to the page limit) -> Export Citations
     -> BibTeX -> download; repeat per result page (or set page size 50 and
     iterate). Save files as exports/acm/<QID>_<ver>_pNN.bib
  3. record the hit count shown by ACM in query_log.md.
  4. python -I scripts/ingest_export.py --source acm --qid Q1 --ver v1 exports/acm/Q1_v1_*.bib

Also used for IEEE Xplore CSV exports (if no API key) and for any other
manually exported file (BibTeX, RIS-converted BibTeX, or CSV with Title/DOI
columns).
Manual snowballing (e.g. the reference list of McGee et al. 2021, which no open
index provides):  fill exports/manual/McGee2021_refs.csv (columns title, doi,
year) and run
  python -I scripts/ingest_export.py --source manual --snowball-round R1 --seed S2          --direction backward exports/manual/McGee2021_refs.csv

Output: raw/<source>/<QID>_<ver>.jsonl  (or raw/snowball/<R>_<seed>_<dir>_manual.jsonl)
"""
from __future__ import annotations

import argparse
import glob
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import RAW, log_run, read_csv, record, write_jsonl  # noqa: E402


def parse_bibtex(text: str) -> list[dict]:
    out = []
    for m in re.finditer(r"@(\w+)\s*\{\s*([^,]*),(.*?)\n\}", text, re.S):
        typ, body = m.group(1).lower(), m.group(3)
        f = {}
        for fm in re.finditer(r"(\w+)\s*=\s*(\{(?:[^{}]|\{[^{}]*\})*\}|\"[^\"]*\"|\d+)", body, re.S):
            v = fm.group(2).strip().strip("{}\"")
            f[fm.group(1).lower()] = re.sub(r"\s+", " ", v.replace("{", "").replace("}", ""))
        out.append(record(title=f.get("title", ""), year=f.get("year", ""),
                          venue=f.get("journal") or f.get("booktitle", ""),
                          doi=f.get("doi", ""), type=typ,
                          authors=f.get("author", "").replace(" and ", "; "),
                          abstract=f.get("abstract", "")))
    return out


def parse_csv(path: str) -> list[dict]:
    out = []
    for r in read_csv(Path(path)):
        g = {k.lower().strip(): v for k, v in r.items()}
        out.append(record(title=g.get("document title") or g.get("title", ""),
                          year=g.get("publication year") or g.get("year", ""),
                          venue=g.get("publication title") or g.get("venue", ""),
                          doi=g.get("doi", ""), authors=g.get("authors", ""),
                          abstract=g.get("abstract", "")))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True, help="acm | ieee | other label")
    ap.add_argument("--qid", default="")
    ap.add_argument("--ver", default="")
    ap.add_argument("--reported", default="", help="hit count shown by the library UI")
    ap.add_argument("--snowball-round", default="", help="e.g. R1: file is a manually typed reference/citation list")
    ap.add_argument("--seed", default="", help="seed id, e.g. S2")
    ap.add_argument("--direction", default="backward", choices=["backward", "forward"])
    ap.add_argument("files", nargs="+")
    a = ap.parse_args()
    rows = []
    for pat in a.files:
        for fn in glob.glob(pat):
            txt = Path(fn).read_text(encoding="utf-8", errors="replace")
            rows += parse_csv(fn) if fn.lower().endswith(".csv") else parse_bibtex(txt)
    if a.snowball_round:
        for r in rows:
            r.update(source="snowball-manual", query_id=a.snowball_round, snowball_round=a.snowball_round,
                     snowball_seed=a.seed, snowball_direction=a.direction)
        write_jsonl(RAW / "snowball" / f"{a.snowball_round}_{a.seed}_{a.direction}_manual.jsonl", rows)
        log_run("snowball-manual", f"{a.snowball_round}:{a.seed}", a.direction, " ".join(a.files), None, len(rows))
        print(f"manual snowball {a.snowball_round} {a.seed} {a.direction}: {len(rows)} records")
        return
    for r in rows:
        r.update(source=a.source, query_id=a.qid, query_version=a.ver)
    write_jsonl(RAW / a.source / f"{a.qid}_{a.ver}.jsonl", rows)
    log_run(a.source, a.qid, a.ver, "manual export: " + " ".join(a.files), a.reported or None, len(rows))
    print(f"{a.source} {a.qid} {a.ver}: ingested {len(rows)} records")


if __name__ == "__main__":
    main()

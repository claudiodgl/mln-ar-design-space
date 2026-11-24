"""Fetch missing abstracts / venues for de-duplicated candidates from Crossref
(by DOI) and store them in raw/enrich/crossref_meta.jsonl; merge_dedupe.py
uses that file on its next run (so the rule-based suggestion sees the abstract).
Crossref is used for metadata only, not as a search source: its
/works?query= endpoint is relevance-ranked and has no boolean field search.

Pipeline: merge_dedupe.py -> enrich_crossref.py -> merge_dedupe.py
Env: MAILTO (optional polite-pool contact; default empty)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import MAILTO, OUT, RAW, get, read_csv, read_jsonl, write_jsonl  # noqa: E402

DEST = RAW / "enrich" / "crossref_meta.jsonl"


def clean(a: str) -> str:
    a = re.sub(r"<[^>]+>", " ", a or "")
    a = re.sub(r"^\s*(abstract|summary)\s*[:.]?\s*", "", re.sub(r"\s+", " ", a).strip(), flags=re.I)
    return a


def main():
    have = {r["doi"]: r for r in read_jsonl(DEST)}
    cands = read_csv(OUT / "candidates_all.csv")
    todo = [c["doi"] for c in cands if c["doi"] and not c["abstract"]
            and not c["doi"].startswith("10.48550/") and c["doi"] not in have]
    print(f"{len(todo)} DOIs to look up")
    for i, d in enumerate(todo, 1):
        m = (get(f"https://api.crossref.org/works/{d}", {"mailto": MAILTO} if MAILTO else None) or {}).get("message") or {}
        have[d] = {"doi": d, "abstract": clean(m.get("abstract", "")),
                   "venue": (m.get("container-title") or [""])[0], "type": m.get("type", "")}
        if i % 250 == 0:
            print(f"  {i}/{len(todo)}")
            write_jsonl(DEST, list(have.values()))
    write_jsonl(DEST, list(have.values()))
    print(f"with abstract: {sum(1 for r in have.values() if r['abstract'])}/{len(have)}")


if __name__ == "__main__":
    main()

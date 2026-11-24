"""Build the seed list for the next snowballing round from the screening sheet.

Seeds for round k+1 = candidates whose final full-text decision is "include"
(fulltext_decision == include, or final_decision == include if full-text
screening has not been recorded) and that have not been used as seeds before.
Stopping rule: stop when the new round contributes no additional included work.

Usage: python -I scripts/make_seeds.py --round R2 [--screening output/screening.csv]
Output: output/seeds_R2.csv  (input for snowball.py --round R2 --seeds ...)
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import CONFIG, OUT, norm_doi, read_csv, write_csv  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--round", required=True)
    ap.add_argument("--screening", default=str(OUT / "screening.csv"))
    a = ap.parse_args()
    used = {norm_doi(s["doi"]) for s in read_csv(CONFIG / "seeds.csv")}
    for f in OUT.glob("seeds_R*.csv"):
        used |= {norm_doi(s["doi"]) for s in read_csv(f)}
    out = []
    for r in read_csv(Path(a.screening)):
        dec = (r.get("fulltext_decision") or r.get("final_decision") or "").strip().lower()
        if dec != "include":
            continue
        if norm_doi(r["doi"]) in used and r["doi"]:
            continue
        out.append({"sid": r["cid"], "doi": r["doi"], "arxiv": r["arxiv"], "title": r["title"]})
    write_csv(OUT / f"seeds_{a.round}.csv", out, ["sid", "doi", "arxiv", "title"])
    print(f"{len(out)} new seeds -> {OUT / f'seeds_{a.round}.csv'}")


if __name__ == "__main__":
    main()

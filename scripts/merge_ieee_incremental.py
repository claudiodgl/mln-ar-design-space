"""Add the IEEE Xplore search results to the existing corpus WITHOUT re-running
merge_dedupe.py (which would renumber every cid and overwrite screening.csv,
including the AI/A1 and author decisions).

Steps:
  1. read raw/ieee/<QID>_<ver>.jsonl (current query versions only);
  2. de-duplicate the IEEE records among themselves (same keys as
     merge_dedupe.py: DOI, arXiv id, normalised title > 25 chars);
  3. match each IEEE work against the full corpus of all rounds
     (output/screening_R5full_merged_raw.csv, 21,072 candidates);
  4. works not in the corpus become new candidates with cids "IEEE-Cnnnnn",
     get the rule-based suggestion (merge_dedupe.suggest) and the documented
     keyword rule (keyword_prefilter.keep, code E0 when not kept);
  5. benchmark recall of the database searches with and without IEEE.

Outputs (output/, nothing existing is overwritten):
  ieee_overlap.csv          every unique IEEE work -> existing cid or new cid
  screening_IEEE_new.csv    new candidates (screening sheet columns + prefilter_rule)
  prisma_counts_IEEE.json   updated identification counts
Usage: python -I scripts/merge_ieee_incremental.py
"""
from __future__ import annotations

import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from benchmark import BENCH, current_versions, match, raw_files  # noqa: E402
from common import OUT, RAW, norm_arxiv, norm_doi, norm_title, read_jsonl  # noqa: E402
from keyword_prefilter import keep  # noqa: E402
from merge_dedupe import UF, suggest  # noqa: E402

csv.field_size_limit(10**9)
CORPUS = OUT / "screening_R5full_merged_raw.csv"
PRISMA_BEFORE = OUT / "prisma_counts.json"


def keys(r: dict) -> list[str]:
    k = []
    if d := norm_doi(r.get("doi")):
        k.append("d:" + d)
    if a := norm_arxiv(r.get("arxiv")):
        k.append("a:" + a)
    nt = norm_title(r.get("title"))
    if len(nt) > 25:
        k.append("t:" + nt.replace(" ", ""))
    return k


def write(path: Path, rows: list[dict], cols: list[str]):
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def main():
    cur = current_versions()
    files = [f for f in sorted((RAW / "ieee").glob("*.jsonl")) if ("ieee", f.stem) in cur]
    recs = []
    for f in files:
        for r in read_jsonl(f):
            r["_prov"] = f"ieee:{f.stem}"
            recs.append(r)

    # 1) de-duplicate within IEEE
    uf = UF()
    for i, r in enumerate(recs):
        uf.f(f"r{i}")
        for k in keys(r):
            uf.u(f"r{i}", k)
    groups = defaultdict(list)
    for i, r in enumerate(recs):
        groups[uf.f(f"r{i}")].append(r)

    # 2) index of the existing corpus
    corpus = list(csv.DictReader(open(CORPUS, encoding="utf-8-sig")))
    idx = {}
    for c in corpus:
        for k in keys(c):
            idx.setdefault(k, c["cid"])

    overlap, new = [], []
    for g in groups.values():
        hit = next((idx[k] for r in g for k in keys(r) if k in idx), "")
        best = max(g, key=lambda r: len(r.get("abstract") or ""))
        prov = " | ".join(sorted({r["_prov"] for r in g}))
        row = {"title": best["title"], "year": best["year"], "venue": best["venue"],
               "doi": next((r["doi"] for r in g if r["doi"]), ""), "arxiv": best.get("arxiv", ""),
               "authors": best["authors"], "abstract": best["abstract"], "provenance": prov,
               "n_records": len(g), "benchmark_id": next((m for r in g if (m := match(r))), ""),
               "existing_cid": hit}
        overlap.append(row)
        if not hit:
            new.append(row)

    new.sort(key=lambda c: (str(c["year"]), norm_title(c["title"])))
    for i, c in enumerate(new, 1):
        c["cid"] = f"IEEE-C{i:05d}"
        c["found_by_search"], c["found_by_snowball"] = "yes", "no"
        c["SUGGESTION_rule_based_not_a_decision"], c["suggestion_rule"] = suggest(c)
        c["prefilter_rule"] = keep(c["title"], c["abstract"]) or "E0"
    cid_of = {id(c): c["cid"] for c in new}
    for o in overlap:
        o["new_cid"] = cid_of.get(id(o), "")

    write(OUT / "ieee_overlap.csv", overlap,
          ["existing_cid", "new_cid", "benchmark_id", "title", "year", "venue", "doi",
           "provenance", "n_records"])
    scr_cols = ["cid", "title", "year", "venue", "doi", "arxiv", "found_by_search", "found_by_snowball",
                "provenance", "SUGGESTION_rule_based_not_a_decision", "suggestion_rule", "prefilter_rule",
                "S1_decision", "S1_reason", "S2_decision", "S2_reason", "agree", "final_decision",
                "final_reason", "fulltext_decision", "fulltext_reason", "category_I1_I4_B", "notes",
                "authors", "abstract"]
    write(OUT / "screening_IEEE_new.csv", new, scr_cols)

    # 3) benchmark recall of database searches, with and without IEEE
    found = defaultdict(set)
    for src, f in raw_files():
        if src == "snowball":
            continue
        for r in read_jsonl(f):
            if m := match(r):
                found[m].add(src)
    allb = {b["bid"] for b in BENCH}
    with_ieee = {b for b, s in found.items() if s}
    without = {b for b, s in found.items() if s - {"ieee"}}
    ieee_only = sorted(with_ieee - without)
    ieee_hits = sorted({b for b, s in found.items() if "ieee" in s})

    before = json.loads(PRISMA_BEFORE.read_text(encoding="utf-8"))
    n_new_kept = sum(c["prefilter_rule"] != "E0" for c in new)
    counts = {
        "note": "prisma_counts.json (state after snowballing round 5) + IEEE Xplore search; "
                "prisma_counts.json itself is unchanged",
        "ieee_records_identified": len(recs),
        "ieee_unique_works": len(groups),
        "ieee_works_already_in_corpus": len(groups) - len(new),
        "ieee_new_candidates": len(new),
        "ieee_new_kept_by_keyword_rule": n_new_kept,
        "ieee_new_excluded_E0": len(new) - n_new_kept,
        "ieee_hits_per_query": {f.stem: len(read_jsonl(f)) for f in files},
        "records_identified_total": before["records_identified_total"] + len(recs),
        "records_identified_database_search": before["records_identified_database_search"] + len(recs),
        "records_identified_snowballing": before["records_identified_snowballing"],
        "unique_after_dedup": before["unique_after_dedup"] + len(new),
        "unique_from_search_increase": len(new),
        "benchmark_size": len(allb),
        "benchmark_retrieved_by_ieee": ieee_hits,
        "benchmark_recall_searches_without_ieee": f"{len(without)}/{len(allb)}",
        "benchmark_recall_searches_with_ieee": f"{len(with_ieee)}/{len(allb)}",
        "benchmark_only_via_ieee": ieee_only,
        "benchmark_missed_by_all_searches": sorted(allb - with_ieee),
    }
    (OUT / "prisma_counts_IEEE.json").write_text(json.dumps(counts, indent=1), encoding="utf-8")
    print(json.dumps(counts, indent=1))


if __name__ == "__main__":
    main()

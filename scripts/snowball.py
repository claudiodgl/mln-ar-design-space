"""Backward (references) and forward (citations) snowballing through two
independent citation indexes: OpenAlex and Semantic Scholar.

Usage:
  # round 1: seed surveys
  python -I scripts/snowball.py --round R1 --seeds config/seeds.csv
  # round k>1: works included in screening that were not yet used as seeds
  python -I scripts/snowball.py --round R2 --seeds output/seeds_R2.csv
  (make_seeds.py writes seeds_Rk.csv from screening.csv)

A seed CSV needs columns: sid, doi, arxiv, title.
Output: raw/snowball/<ROUND>_<sid>_<backward|forward>_<openalex|s2>.jsonl
        raw/snowball/<ROUND>_seed_resolution.csv
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import RAW, get, log_run, norm_arxiv, norm_doi, read_csv, record, write_csv, write_jsonl  # noqa: E402
from search_openalex import SELECT, auth_params, oa_to_record  # noqa: E402
from search_s2 import s2_to_record, headers as s2_headers  # noqa: E402

OA = "https://api.openalex.org/works"
S2 = "https://api.semanticscholar.org/graph/v1/paper"
S2F = "title,year,venue,externalIds,abstract,publicationTypes,authors"
OUTD = RAW / "snowball"


# ------------------------------------------------------------------ OpenAlex
def oa_resolve(seed: dict) -> dict | None:
    doi, arx = norm_doi(seed.get("doi")), norm_arxiv(seed.get("arxiv"))
    for ident in ([f"doi:{doi}"] if doi else []) + ([f"doi:10.48550/arxiv.{arx}"] if arx else []):
        w = get(f"{OA}/{ident}", auth_params())
        if w:
            return w
    return None


def oa_batch(ids: list[str]) -> list[dict]:
    out = []
    for i in range(0, len(ids), 50):
        chunk = [x.rsplit("/", 1)[-1] for x in ids[i:i + 50]]
        d = get(OA, {"filter": "openalex_id:" + "|".join(chunk), "per_page": 50,
                     "select": SELECT, **auth_params()})
        out += d["results"]
    return out


def oa_citing(wid: str) -> list[dict]:
    rows, page = [], 1
    while True:
        d = get(OA, {"filter": f"cites:{wid}", "per_page": 200, "page": page,
                     "select": SELECT, **auth_params()})
        rows += d["results"]
        if not d["results"] or len(rows) >= d["meta"]["count"]:
            return rows
        page += 1


# ------------------------------------------------------------------ Crossref
def crossref_refs(doi: str) -> list[dict]:
    """Backward only: reference list deposited by the publisher (may be empty)."""
    from common import MAILTO
    if not doi or doi.startswith("10.48550/"):
        return []
    m = get(f"https://api.crossref.org/works/{doi}", {"mailto": MAILTO} if MAILTO else None)
    return (m or {}).get("message", {}).get("reference", []) or []


# --------------------------------------------------------- Semantic Scholar
def s2_id(seed: dict) -> list[str]:
    ids = []
    if norm_doi(seed.get("doi")) and not norm_doi(seed["doi"]).startswith("10.48550/"):
        ids.append("DOI:" + norm_doi(seed["doi"]))
    if norm_arxiv(seed.get("arxiv")):
        ids.append("ARXIV:" + norm_arxiv(seed["arxiv"]))
    return ids


def s2_edges(pid: str, kind: str) -> list[dict] | None:
    """kind = references | citations ; returns list of paper dicts or None if unknown id."""
    rows, offset = [], 0
    key = "citedPaper" if kind == "references" else "citingPaper"
    while True:
        d = get(f"{S2}/{pid}/{kind}", {"fields": S2F, "limit": 1000, "offset": offset},
                headers=s2_headers())
        if d is None:
            return None
        rows += [x[key] for x in d.get("data") or [] if x.get(key) and x[key].get("title")]
        if d.get("next") is None:
            return rows
        offset = d["next"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--round", required=True)
    ap.add_argument("--seeds", required=True)
    ap.add_argument("--skip-s2", action="store_true")
    ap.add_argument("--backward-only", action="store_true", help="reference lists only (no citing papers)")
    a = ap.parse_args()
    seeds = read_csv(Path(a.seeds))
    res_rows = []
    for s in seeds:
        sid = s["sid"]
        info = {"round": a.round, "sid": sid, "title": s.get("title", ""), "doi": s.get("doi", "")}
        # OpenAlex
        w = oa_resolve(s)
        info["openalex_id"] = w["id"].rsplit("/", 1)[-1] if w else ""
        if w:
            refs = oa_batch(w.get("referenced_works") or [])
            cit = [] if a.backward_only else oa_citing(info["openalex_id"])
            info["oa_refs_listed"] = len(w.get("referenced_works") or [])
            info["oa_backward"], info["oa_forward"] = len(refs), len(cit)
            for dirn, lst in (("backward", refs), ("forward", cit)):
                recs = [oa_to_record(x, source="snowball-openalex", query_id=a.round,
                                     snowball_round=a.round, snowball_seed=sid,
                                     snowball_direction=dirn) for x in lst]
                write_jsonl(OUTD / f"{a.round}_{sid}_{dirn}_openalex.jsonl", recs)
                log_run("snowball-openalex", f"{a.round}:{sid}", dirn, info["openalex_id"], None, len(recs))
        # Semantic Scholar
        if not a.skip_s2:
            for pid in s2_id(s):
                refs = s2_edges(pid, "references")
                if refs is None:
                    continue
                cit = [] if a.backward_only else (s2_edges(pid, "citations") or [])
                info["s2_id"] = pid
                info["s2_backward"], info["s2_forward"] = len(refs), len(cit)
                for dirn, lst in (("backward", refs), ("forward", cit)):
                    recs = [s2_to_record(x, source="snowball-s2", query_id=a.round,
                                         snowball_round=a.round, snowball_seed=sid,
                                         snowball_direction=dirn) for x in lst]
                    write_jsonl(OUTD / f"{a.round}_{sid}_{dirn}_s2.jsonl", recs)
                    log_run("snowball-s2", f"{a.round}:{sid}", dirn, pid, None, len(recs))
                break
        # Crossref (third index, backward only)
        cr = crossref_refs(norm_doi(s.get("doi")))
        info["cr_backward"] = len(cr)
        recs = [record(source="snowball-crossref", query_id=a.round, snowball_round=a.round,
                       snowball_seed=sid, snowball_direction="backward", doi=x.get("DOI", ""),
                       title=x.get("article-title") or x.get("volume-title") or x.get("unstructured", ""),
                       year=x.get("year", ""), venue=x.get("journal-title", ""))
                for x in cr]
        write_jsonl(OUTD / f"{a.round}_{sid}_backward_crossref.jsonl", recs)
        log_run("snowball-crossref", f"{a.round}:{sid}", "backward", norm_doi(s.get("doi")), None, len(recs))
        print(f"{a.round} {sid}: " + ", ".join(f"{k}={v}" for k, v in info.items()
                                              if k.startswith(("oa_", "s2_b", "s2_f", "cr_"))))
        res_rows.append(info)
    cols = ["round", "sid", "title", "doi", "openalex_id", "oa_refs_listed", "oa_backward",
            "oa_forward", "s2_id", "s2_backward", "s2_forward", "cr_backward"]
    write_csv(OUTD / f"{a.round}_seed_resolution.csv", res_rows, cols)


if __name__ == "__main__":
    main()

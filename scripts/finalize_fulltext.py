"""Close the full-text stage (2026-11-24).

1. Adds the IEEE Xplore records that need a full text (screening_IEEE_new.csv,
   final_decision == unsure) to output/fulltext_results.csv (round "IEEE").
2. Applies the full-text decisions of the batches given on the command line
   (screening_ai/FT/ft4_decisions.csv, ...; columns cid,decision,code,evidence,note).
   A note starting with "decided on the abstract" sets ft_stage = abstract.
3. Every record that is still needs_fulltext becomes not_retrieved (E7):
   no full text could be obtained from open sources (OpenAlex and Semantic
   Scholar open-access locations, arXiv, publisher copies via the DOI).
   Records in output/FT_pdfs_needed_A_likely_includes.csv are flagged
   "likely include" in ft_note.
Idempotent; writes a backup to backups/fulltext_results_before_finalize.csv once.
Usage: python -I -X utf8 scripts/finalize_fulltext.py screening_ai/FT/ft4_decisions.csv ...
"""
import csv
import shutil
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output"
p = OUT / "fulltext_results.csv"
bak = ROOT / "backups" / "fulltext_results_before_finalize.csv"
if not bak.exists():
    shutil.copy(p, bak)
rows = list(csv.DictReader(open(p, encoding="utf-8-sig")))
cols = list(rows[0].keys())
by = {r["cid"]: r for r in rows}

for r in csv.DictReader(open(OUT / "screening_IEEE_new.csv", encoding="utf-8-sig")):
    if r["final_decision"] == "unsure" and r["cid"] not in by:
        n = {c: "" for c in cols}
        n.update(round="IEEE", cid=r["cid"], title=r["title"], year=r["year"], venue=r["venue"], doi=r["doi"],
                 abstract=r.get("abstract", ""), screen_note=r.get("AI_note", ""), ft_stage="abstract",
                 ft_decision="needs_fulltext")
        rows.append(n); by[r["cid"]] = n

for fn in sys.argv[1:]:
    for d in csv.DictReader(open(ROOT / fn, encoding="utf-8-sig")):
        r = by[d["cid"]]
        if d["decision"] == "needs_fulltext":
            r["ft_note"] = d["note"]
            continue
        r["ft_decision"], r["ft_code"], r["ft_evidence"] = d["decision"], d["code"], d["evidence"]
        r["ft_note"] = d["note"]
        r["ft_stage"] = "abstract" if d["note"].startswith("decided on the abstract") else "fulltext"
        r["pdf_source"] = r["pdf_source"] or ("retrieved 2026-11-24" if r["ft_stage"] == "fulltext" else "")

likely = {r["cid"] for r in csv.DictReader(open(OUT / "FT_pdfs_needed_A_likely_includes.csv", encoding="utf-8-sig"))}
for r in rows:
    if r["ft_decision"] in ("needs_fulltext", "not_retrieved"):
        r["ft_decision"], r["ft_code"] = "not_retrieved", "E7"
        base = "full text not obtainable from open sources (OpenAlex/Semantic Scholar OA, arXiv, publisher via DOI)"
        flag = "; likely include from title/abstract" if r["cid"] in likely or "likely include" in (r["screen_note"] + r["ft_note"]) else ""
        prev = r["ft_note"] if r["ft_note"] and not r["ft_note"].startswith("full text not obtainable") else ""
        r["ft_note"] = base + flag + (f"; {prev}" if prev else "")

with open(p, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
print(len(rows), Counter((r["ft_stage"], r["ft_decision"]) for r in rows))
print("not retrieved, likely include:", sum(r["ft_decision"] == "not_retrieved" and "likely include" in r["ft_note"] for r in rows))

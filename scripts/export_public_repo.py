"""Export the review data and scripts to the public repository layout,
without third-party copyrighted text.

Removed on export:
  * abstracts: every CSV column whose name starts with "abstract" (also inside
    candidates_all.csv.gz), the "abstract" field of every raw JSONL record in
    the search archive, and the "ABS:" lines of the language-model batch files;
  * full texts and PDFs (fulltext/ is never exported);
  * pasted copies of database result pages (exports/acm/pages/);
  * raw API response caches (raw/cache/).
Kept: bibliographic metadata (title, authors, venue, year, DOI), our own
decisions, notes and codes, and short verbatim evidence quotes (at most 25
words) that are attributed by DOI.

Usage: python -I -X utf8 scripts/export_public_repo.py <repo_dir>
Files of the repository that are not produced here (README, LICENSE, coding/
notes) are left untouched; files listed in REMOVE are deleted.
"""
from __future__ import annotations

import csv
import gzip
import io
import json
import re
import shutil
import sys
import tarfile
from pathlib import Path

csv.field_size_limit(10**9)
ROOT = Path(__file__).resolve().parents[1]
OUT, RAW, SAI = ROOT / "output", ROOT / "raw", ROOT / "screening_ai"
REPO = Path(sys.argv[1])
REMOVE = ["data/search/manual_exports/acm/pages"]


def strip_csv(src: Path, dst: Path):
    rows = list(csv.DictReader(open(src, encoding="utf-8-sig")))
    if not rows:
        return
    cols = [c for c in rows[0].keys() if not c.lower().lstrip("﻿").startswith("abstract")]
    dst.parent.mkdir(parents=True, exist_ok=True)
    with open(dst, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(rows)


def strip_batch(src: Path, dst: Path):
    t = src.read_text(encoding="utf-8", errors="replace")
    t = re.sub(r"(?m)^(\s*ABS:).*$", r"\1 [abstract omitted; see the DOI]", t)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(t, encoding="utf-8")


def copy(src: Path, dst: Path):
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(src, dst)


def main():
    for r in REMOVE:
        shutil.rmtree(REPO / r, ignore_errors=True)

    # protocol and configuration
    copy(SAI / "criteria.md", REPO / "protocol/eligibility_criteria.md")
    copy(SAI / "fulltext_brief.md", REPO / "protocol/fulltext_assessment_brief.md")
    copy(ROOT / "protocol.md", REPO / "protocol/protocol.md")
    copy(ROOT / "query_log.md", REPO / "protocol/query_log.md")
    copy(ROOT / "config/query_log_narrative.md", REPO / "protocol/query_log_narrative.md")
    for f in ("benchmark.csv", "benchmark_retired.csv", "queries.json", "seeds.csv"):
        copy(ROOT / "config" / f, REPO / "config" / f)
    copy(ROOT / "config/table2_codes.json", REPO / "coding/table2_codes.json")

    # scripts
    for f in sorted((ROOT / "scripts").iterdir()):
        if f.suffix in (".py", ".sh") and not f.name.endswith(".bak"):
            copy(f, REPO / "scripts" / f.name)
    copy(ROOT / "run_all.sh", REPO / "scripts/run_all.sh")

    # screening data
    S = REPO / "data/screening"
    sheets = {"screening.csv": "screening_R1.csv", "screening_R2.csv": "screening_R2.csv",
              "screening_R3.csv": "screening_R3.csv", "screening_R4.csv": "screening_R4.csv",
              "screening_R5.csv": "screening_R5.csv", "screening_IEEE_new.csv": "screening_IEEE.csv",
              "fulltext_results.csv": "fulltext_results.csv", "benchmark_recall.csv": "benchmark_recall.csv",
              "recall_by_source.csv": "recall_by_source.csv", "ieee_overlap.csv": "ieee_overlap.csv",
              "fulltext_publisher_fetch.csv": "fulltext_publisher_fetch.csv"}
    for a, b in sheets.items():
        if (OUT / a).exists():
            strip_csv(OUT / a, S / b)
    for f in ("prisma_counts.json", "prisma_counts_IEEE.json"):
        copy(OUT / f, S / f)
    ver = ["FT_pdfs_needed_A_likely_includes.csv", "FT_undecidable_B.csv", "FT_verify_excludes_and_background.csv",
           "FT_verify_includes.csv", "R2_exclusion_check_sample.csv", "R2_verify_includes.csv",
           "R3_exclusion_check_sample.csv", "R3_verify_includes.csv", "R4_exclusion_check_all.csv",
           "R4_verify_includes.csv", "exclusion_check_sample.csv", "IEEE_verify_includes.csv",
           "IEEE_exclusion_check_all.csv"]
    for f in ver:
        if (OUT / f).exists():
            strip_csv(OUT / f, S / "verification" / f)
    # candidates_all without abstracts
    buf = io.StringIO()
    rows = csv.DictReader(open(OUT / "candidates_all.csv", encoding="utf-8-sig"))
    cols = [c for c in rows.fieldnames if not c.lower().startswith("abstract")]
    w = csv.DictWriter(buf, fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(rows)
    with gzip.open(S / "candidates_all.csv.gz", "wt", encoding="utf-8", newline="") as g:
        g.write(buf.getvalue())

    # language-model batches: decisions as they are, inputs without abstracts
    L = S / "llm_prescreen"
    shutil.rmtree(L, ignore_errors=True)
    for f in sorted(SAI.rglob("*")):
        if not f.is_file() or f.name in ("criteria.md", "fulltext_brief.md"):
            continue
        rel = f.relative_to(SAI)
        dst = L / ("R1" if len(rel.parts) == 1 else "") / rel   # round-1 batches sit at the top level
        if f.suffix == ".txt":
            strip_batch(f, dst)
        elif f.suffix == ".csv":
            strip_csv(f, dst)
        elif f.suffix == ".py":
            copy(f, dst)

    # manual exports (parsed results and query strings only)
    for f in sorted((ROOT / "exports").rglob("*")):
        rel = f.relative_to(ROOT / "exports")
        if f.is_file() and "pages" not in rel.parts:
            dst = REPO / "data/search/manual_exports" / rel
            strip_csv(f, dst) if f.suffix == ".csv" else copy(f, dst)

    # raw search and snowballing records, abstracts blanked, no API cache
    tgz = REPO / "data/search/raw_search_and_snowball.tar.gz"
    with tarfile.open(tgz, "w:gz") as tar:
        for f in sorted(RAW.rglob("*")):
            rel = f.relative_to(RAW)
            if not f.is_file() or rel.parts[0] == "cache" or f.suffix == ".log":
                continue
            if f.suffix == ".jsonl":
                lines = []
                for line in open(f, encoding="utf-8"):
                    if line.strip():
                        d = json.loads(line)
                        if "abstract" in d:
                            d["abstract"] = ""
                        lines.append(json.dumps(d, ensure_ascii=False))
                data = ("\n".join(lines) + "\n").encode("utf-8")
            else:
                data = f.read_bytes()
            ti = tarfile.TarInfo(f"raw/{rel.as_posix()}"); ti.size = len(data); ti.mtime = 0
            tar.addfile(ti, io.BytesIO(data))
    print("exported to", REPO)


if __name__ == "__main__":
    main()

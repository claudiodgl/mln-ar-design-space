#!/usr/bin/env bash
# Re-run the whole pipeline. Cached API responses in raw/cache/ are reused, so a
# re-run reproduces the archived result exactly; delete raw/cache/ to re-query.
# Optional env: OPENALEX_API_KEY, S2_API_KEY, IEEE_API_KEY, MAILTO.
set -euo pipefail
cd "$(dirname "$0")"
P=".venv/Scripts/python -I"; [ -x .venv/bin/python ] && P=".venv/bin/python -I"
$P scripts/querybuild.py > output/rendered_queries.txt
$P scripts/search_openalex.py
$P scripts/search_s2.py
$P scripts/search_arxiv.py
$P scripts/search_egdl.py
$P scripts/search_dblp.py
$P scripts/search_ieee.py          # needs IEEE_API_KEY; otherwise prints strings
# ACM DL: manual export, then e.g.
#   $P scripts/ingest_export.py --source acm --qid Q1 --ver v4 --reported N exports/acm/Q1_v4_*.bib
$P scripts/snowball.py --round R1 --seeds config/seeds.csv
$P scripts/merge_dedupe.py
$P scripts/enrich_crossref.py
$P scripts/merge_dedupe.py
$P scripts/report_benchmark.py
$P scripts/report_notable.py
$P scripts/make_query_log.py

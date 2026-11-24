# Design Space of Multilayer Network Visualization in Augmented Reality

**Supplemental material, literature-review data, and analysis scripts**

> **Status:** submitted to the [*Eurographics Conference on Visualization (EuroVis) 2027*](https://eurovis27.github.io/web/) (full paper, under review).

**Authors:** A. A. Ainin¹, M. Lima Medeiros², N. Ferreira³, S. van den Elzen⁴, and C. D. G. Linhares¹
¹ Linnaeus University, Sweden · ² VRVis GmbH and TU Wien, Austria · ³ Federal University of Pernambuco, Brazil · ⁴ Eindhoven University of Technology, Netherlands

---

## About the paper

Multilayer networks (MLNs) model systems with several types of relationships. Most MLN tools stack layers in 3D but show them on flat screens. The paper contributes a **design space for MLN visualization in augmented reality (AR)**. It is organized into three parts, *Visualization State*, *Layout Possibilities*, and *User Interaction*, and marks which values are AR-specific. Coding 28 prior works against the space reveals gaps, most notably that no AR work treats layers as entities. A HoloLens 2 prototype instantiates configurations that address these gaps: tangible and floating matrix layers, distance-controlled layer coupling, and independent layer representations.

## Supplemental material

The supplemental material of the paper (literature search, screening, coding of the 28 works, and additional candidate works) is distributed with the paper submission. This repository contains the data and scripts behind it.

## Literature review at a glance

| Step | Records |
|---|---:|
| Database searches (ACM DL, IEEE Xplore, Eurographics DL, OpenAlex, Semantic Scholar, DBLP, arXiv; 7 queries, no date limit) | 4,491 |
| Unique records after de-duplication (searches + snowballing rounds 1–5) | 20,410 |
| Removed by the documented keyword rule (E0, rounds 2–5) | 11,362 |
| Titles and abstracts screened | 9,048 |
| Included after title/abstract screening (all verified by the authors) | 527 |
| Uncertain records sought in full text | 755 |
| &nbsp;&nbsp;assessed (full text or newly retrieved abstract) | 306 (52 included, 13 background, 241 excluded) |
| &nbsp;&nbsp;full text not retrieved from open sources (E7) | 449 |
| Corpus of included works | 579 |
| Works coded in detail (Table 2 of the paper) | 28 |

Snowballing started from five surveys (McGee et al. 2019 and 2021, Joos et al. 2026, Saffo et al. 2024, Klein et al. 2022) and continued from the title/abstract inclusions until a round added no included work (five rounds). IEEE Xplore was searched after snowballing (2026-11-24) and de-duplicated against all earlier records; it added 39 new records. The database searches retrieve 26 of the 28 coded works; with snowballing, all 28 are reached. Title, abstract, and full-text pre-screening was assisted by a language model. The authors verified every inclusion and random samples of exclusions (148/150 confirmed in round 1; all confirmed in rounds 2–4 and in the IEEE Xplore search).

## Repository structure

```
protocol/            review protocol, eligibility criteria, query log, full-text assessment brief
config/              queries (concept blocks), seed surveys, benchmark of coded works
scripts/             search, snowballing, de-duplication, keyword rule, benchmark report, tables and figures
data/
  search/            raw API responses of all searches and snowballing rounds (tar.gz), manual ACM exports
  screening/         screening sheets per round, full-text results, PRISMA counts, benchmark recall
    verification/    author verification sheets (inclusions, exclusion samples)
    llm_prescreen/   pre-screening batches and proposed decisions per round
coding/              codebook, codes of the 28 works in Table 2, coding of additional candidate works
```

Key files:

- [`data/screening/screening_R1.csv`](data/screening/screening_R1.csv) to `screening_R5.csv`, and `screening_IEEE.csv`: one row per screened record, with the pre-screening proposal, the verified decision, and the reason code
- [`data/screening/fulltext_results.csv`](data/screening/fulltext_results.csv): full-text decisions with short verbatim evidence quotes (at most 25 words), or `not_retrieved`
- [`data/screening/ieee_overlap.csv`](data/screening/ieee_overlap.csv): each IEEE Xplore work and the earlier record it duplicates, if any
- [`data/screening/benchmark_recall.csv`](data/screening/benchmark_recall.csv): retrieval path of each coded work
- [`coding/table2_codes.json`](coding/table2_codes.json): design-space codes of the 28 works in Table 2

## Reproducing the search

```bash
python -m venv .venv
.venv/bin/pip install requests          # pymupdf optional (falls back to poppler's pdftotext)
export OPENALEX_API_KEY=...     # optional but recommended (free key from openalex.org)
export IEEE_API_KEY=...         # IEEE Xplore Metadata API key (free from developer.ieee.org)
bash scripts/run_all.sh         # searches -> snowballing -> de-duplication -> benchmark report
```

Live indexes change over time, so re-running the searches will not reproduce the exact counts. The archived records in `data/search/raw_search_and_snowball.tar.gz` are the records used in the paper.

**Copyright.** The repository contains bibliographic metadata (titles, authors, venues, years, DOIs), our own screening decisions, notes and codes, and short attributed evidence quotes. It contains no full texts, no PDFs, and no abstracts: abstract fields were removed from all sheets and archived records on export (`scripts/export_public_repo.py`); use the DOI to read a paper.

## Citation

If you use this material, please cite the paper (citation details will be added after review):

```bibtex
@unpublished{Ainin2027MLNAR,
  author = {Ainin, A. A. and Lima Medeiros, M. and Ferreira, N. and van den Elzen, S. and Linhares, C. D. G.},
  title  = {Design Space of Multilayer Network Visualization in Augmented Reality},
  note   = {Submitted to the Eurographics Conference on Visualization (EuroVis) 2027},
  year   = {2027}
}
```

## License

Released under the [MIT License](LICENSE). Bibliographic metadata in `data/` comes from the cited indexes (OpenAlex, Semantic Scholar, DBLP, Crossref, arXiv, ACM DL, IEEE Xplore, Eurographics DL) and remains subject to their terms; short quotes from screened papers are included only as evidence for screening decisions.

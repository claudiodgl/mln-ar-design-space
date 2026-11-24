# Literature-search and coding protocol

**Paper:** *Design Space of Multilayer Network (MLN) Visualization in Augmented Reality* (EuroVis 2027 submission)
**Protocol version:** 1.0, 2026-11-21 (database searches and snowballing round 1 executed on this date; IEEE Xplore and ACM DL pending)
**Reporting:** PRISMA 2020-style flow counts (identification → de-duplication → title/abstract screening → full-text eligibility → corpus → purposive Table 2 subset), modelled on Saffo et al. 2024 (TVCG, OSF supplement).

Everything referred to below lives in this folder (`MLN_method/`). Numbers in
this document are only those produced by the scripts; numbers that depend on
human screening are placeholders in square brackets.

---

## 1. Research question and scope

**RQ.** Which representation, layout and interaction techniques have been
proposed or evaluated for visualizing multilayer (multiplex, multi-relational)
networks — including dynamic networks whose time slices act as layers — on
desktops, in immersive environments (VR/AR/MR) and as physicalizations, and
which AR-specific techniques (physical anchoring, tangible/touch input,
spatial context) exist that an MLN visualization in AR can build on?

The corpus serves two purposes: (a) to derive and check the dimensions of the
design space (descriptive adequacy: every corpus work must be expressible),
and (b) to select a purposive subset that is coded in detail (Table 2).

## 2. Sources

Google Scholar is **not** used (results are neither reproducible nor
exportable).

| Source | Role | Access | Fields searched |
|---|---|---|---|
| **ACM Digital Library** | primary (CHI, UIST, ISS, SUI, VRST, TEI, TOCHI, PACMHCI) | Advanced search https://dl.acm.org/search/advanced → manual BibTeX export (no public API) | Title, Abstract, Author Keyword |
| **IEEE Xplore** | primary (TVCG, CG&A, VIS, PacificVis, IEEE VR, ISMAR) | Metadata API https://developer.ieee.org/ (free key) or Command Search https://ieeexplore.ieee.org/search/advanced/command + CSV export | Document Title, Abstract |
| **Eurographics Digital Library** | primary (CGF incl. EuroVis full papers and STARs, EuroVis short papers, EGVE/ICAT-EGVE, EuroVA) | https://diglib.eg.org — DSpace 7 REST discovery endpoint `/server/api/discover/search/objects` (keyless) | dc.title, dc.description.abstract, dc.subject (author keywords) |
| **OpenAlex** | cross-disciplinary index (catches MLN tools in Nature Comms, NAR, J. Complex Networks, JOSS, Applied Network Science, ECML PKDD …) | https://api.openalex.org/works (keyless with a small shared daily budget; optional free key `OPENALEX_API_KEY`) | `title_and_abstract.search` (stemmed); Q3 uses `title_and_abstract.search.exact` |
| **Semantic Scholar** | cross-disciplinary index (second, independent engine) | https://api.semanticscholar.org/graph/v1/paper/search/bulk (keyless; optional `S2_API_KEY`) | title + abstract |
| **DBLP** | venue-restricted title search over vis/HCI/XR venues | public SPARQL endpoint https://sparql.dblp.org/sparql (the dblp search API is currently behind a browser challenge) | titles |
| **arXiv** | preprints (recent work not yet in the indexes) | https://export.arxiv.org/api/query (≤ 1 request / 3 s) | ti, abs |
| Crossref | metadata only (abstract/venue filling by DOI; backward snowballing) | https://api.crossref.org/works/{doi} | — |

DBLP venue streams searched: journals/tvcg, cgf, cga, ivs, vi, tochi,
pacmhci; conf/visualization (IEEE VIS), apvis (PacificVis), vissym (EuroVis),
eurova, chi, uist, tei, iss, vr, ismar, vrst, sui, egve, ivapp, gd.

All scripts send a generic User-Agent, no personal data; a contact e-mail for
the OpenAlex/Crossref polite pool can be supplied via the `MAILTO` environment
variable (default empty). Every API response is cached under `raw/cache/`
(with retrieval date) so the exact responses behind the reported numbers are
archived and re-runs are deterministic.

## 3. Search strings

Queries are composed from concept blocks (OR within a block, AND between
groups) defined once in `config/queries.json` and rendered into each
source's syntax by `scripts/querybuild.py`. The rendered strings of the final
versions are in Appendix A (and `output/rendered_queries.txt`); every version
ever executed, with its hit count and benchmark recall, is in
`query_log.md`.

**Blocks (final).**

- NET: network, networks, graph, graphs
- MLNP: "multilayer network(s)", "multi-layer network(s)", "multilayered network(s)", "multilayer graph(s)", "multi-layer graph", "multiplex network(s)", "multiplex graph", "multi-relational network", "multi-relational graph", "multirelational network"
- MLN (DBLP titles only): multilayer, multi-layer, multilayered, multi-layered, multiplex, multi-relational, multirelational
- DYN: "dynamic network(s)", "dynamic graph(s)", "temporal network(s)", "temporal graph(s)", "time-varying network", "evolving network"
- IMM: "augmented reality", "mixed reality", "virtual reality", "extended reality", immersive, "head-mounted", HoloLens  (DBLP adds the acronyms VR, AR, XR, MR as whole words)
- AR: "augmented reality", "mixed reality", HoloLens
- PHYSX: physicalization, physicalisation, "physical visualization", "physical visualisation"
- TANG: tangible, "3D printed", "3D printing"
- THREED: 3D, three-dimensional, 2.5D, stereoscopic
- NETVIS: "network visualization/visualisation", "graph visualization/visualisation", "network analysis", "graph analysis", node-link, "graph drawing", "network data", "graph data", "network exploration", "graph exploration"
- VIS: visualization, visualisation, "visual analytics", "visual analysis", visualizing, visualising
- DS: "design space(s)"
- MAT: matrix, matrices, "adjacency matrix", "hybrid representation", "hybrid visualization/visualisation", node-link
- TOUCH: tangible, touch, "physical object(s)", "physical referent(s)", handheld

**Queries (final).**

| ID | Strand | Logic | Sources |
|---|---|---|---|
| Q1 | MLN visualization | MLNP AND VIS (DBLP: MLN AND NET) | all |
| Q2 | Immersive network visualization | IMM AND NETVIS (DBLP: IMM AND NET) | all |
| Q3 | Network physicalization | PHYSX AND NET | OpenAlex (unstemmed field), EGDL, DBLP, IEEE, ACM — not S2/arXiv (they stem *physicalization* → *physic*) |
| Q4 | Dynamic networks in 3D/immersive/physical form | DYN AND (THREED OR IMM OR PHYSX OR TANG) AND VIS | all |
| Q5 | Design spaces for AR/MR visualization | AR AND DS AND VIS | all |
| Q6 | Matrix/hybrid representations of MLNs or dynamic networks | (MLNP OR DYN) AND MAT AND VIS | all |
| Q7 | Tangible/touch/physical-object interaction for AR visualization of any data | AR AND TOUCH, **venue-restricted** | DBLP (venue list), EGDL, IEEE (post-filtered to TVCG/CG&A/VIS/PacificVis/VR/ISMAR/3DUI), ACM (restrict *Published in* to CHI, UIST, ISS, SUI, VRST, TEI, TOCHI, PACMHCI) |

Q6 and Q7 were added after a first retrieval missed benchmark works (see §8
and `query_log.md`); they operationalize design-space dimensions (Network
Representation; AR-specific Input Modality / Interaction Target), not titles.

**Source-specific syntax notes.**
- *OpenAlex:* `filter=title_and_abstract.search:<boolean string>`, page-based paging (cursor paging returned HTTP 401 without key).
- *Semantic Scholar:* `/paper/search/bulk?query=` with `+` (AND), `|` (OR), quotes.
- *arXiv:* `search_query=(ti:x OR abs:x …) AND (…)`.
- *EGDL:* fielded Solr query over `dc.title`, `dc.description.abstract`, `dc.subject`; multi-word terms rendered as AND of words within the field (phrase queries on abstracts are broken in this DSpace instance).
- *DBLP:* SPARQL; one case-insensitive REGEX per AND-group on `dblp:title`, `VALUES ?stream {…}` restricts venues (template in `scripts/search_dblp.py`). VIS group dropped (titles; venues are already visualization/HCI/XR).
- *IEEE Xplore:* `("Document Title":t OR "Abstract":t …) AND (…)`. Xplore limits the number of search terms per query (assumed 25; verify in the UI / API documentation and adjust `IEEE_MAX_TERMS`); longer queries are split automatically into sub-queries whose union is logically identical (Q1: 4, Q2: 4, Q3: 1, Q4: 24, Q5: 1, Q6: 25, Q7: 3 parts).
- *ACM DL:* `(Title:(…) OR Abstract:(…) OR Keyword:(…)) AND (…)` pasted into Advanced Search → *Edit search* (query syntax), "Search within: The ACM Full-Text Collection". **Verify on first use** that ACM accepts the field names (ACM's syntax has changed over time; the equivalent form-based entry is one row per AND-group with "Search Within: Title / Abstract / Keywords"). Record the hit count shown by ACM.

### 3.1 How to run the pending sources

*IEEE Xplore (API).* Register at https://developer.ieee.org/ (create account →
*Register a new application* → Metadata Search API; keys are free, typically
200 calls/day). Then
```
export IEEE_API_KEY=...            # PowerShell: $env:IEEE_API_KEY="..."
.venv/Scripts/python -I scripts/search_ieee.py
```
Without a key the script prints the command-search strings; run them at
https://ieeexplore.ieee.org/search/advanced/command, export CSV (≤ 2,000
records per export), and ingest with
`scripts/ingest_export.py --source ieee --qid Q1 --ver v4 --reported <N> exports/ieee/Q1_v4*.csv`.

*ACM DL (manual).* For each query: paste the ACM string from Appendix A,
apply the venue filter for Q7, sort by relevance, set 50 results per page,
*Select all* → *Export citations* → BibTeX, once per page; save as
`exports/acm/<QID>_<ver>_pNN.bib`; then
`scripts/ingest_export.py --source acm --qid Q1 --ver v4 --reported <N> "exports/acm/Q1_v4_p*.bib"`.
Note the date and the reported hit count in `query_log.md`.

After ingesting, re-run `merge_dedupe.py`, `report_benchmark.py`,
`make_query_log.py` (or `run_all.sh`).

## 4. Time window

No lower date limit; upper limit = date of search (2026-11-21 for the runs
reported here; IEEE/ACM runs to be dated when executed). Rationale: unlike
immersive analytics as a whole (Saffo et al. start in 2013, with consumer
HMDs), the MLN strand rests on earlier desktop techniques (e.g., hybrid
node-link/matrix representations, 2007) and early VR/AR graph work (2000–2006
appears in the results); the topic is small enough that an unrestricted window
is feasible. Preprints (arXiv) are eligible only if a peer-reviewed version
exists or has been accepted by the search date (the accepted version is then
cited).

## 5. Eligibility criteria

**Inclusion (a work must satisfy at least one; record the code):**

- **I1** proposes or evaluates a visualization or interaction technique, system, or library with visualization component for **multilayer, multiplex or multi-relational networks**, including **dynamic networks whose time slices are represented as separate layers** (stacked, juxtaposed, or matrix-cube representations).
- **I2** proposes or evaluates an **immersive (VR/AR/MR) network visualization** or interaction technique (single- or multilayer).
- **I3** proposes or evaluates a **physical or tangible network visualization** (physicalization).
- **I4** proposes a **design space for immersive/AR visualization**, or proposes/evaluates an **AR visualization technique for any data** that instantiates an AR-specific value of our space (physical anchoring of a visualization, tangible or touch input on a physical referent, or use of the spatial context).
- **I5** a **network representation technique** that the MLN seed surveys (McGee et al. 2019; McGee et al. 2021) review as a building block of MLN visualization (e.g., hybrid node-link/matrix representations), reached by snowballing from these surveys.
- **B (background, not coded):** surveys, taxonomies, design spaces and position papers relevant to the RQ. They inform dimensions and seed snowballing but are not coded (cf. Table 1 of the paper).

**Exclusion (reason codes, first applicable):**

- **E1** not about visualization or visual interaction (e.g., network analysis algorithms without a visual representation; "network" in the sense of neural/computer network without network visualization).
- **E2** visualizes no network/graph data and does not satisfy I4.
- **E3** network visualization that is single-layer, non-dynamic, non-immersive and non-physical (and not I5).
- **E4** dynamic-network visualization that does not represent time slices as layers (e.g., animation only, timeline-only).
- **E5** not a primary research contribution (editorial, abstract/poster only, tutorial, workshop report, peer-review document, thesis whose content is published elsewhere).
- **E6** superseded version (a journal extension, the published version of a preprint, or the latest version of a tool paper is retained instead).
- **E7** not in English, or full text not accessible to any author.
- **E8** insufficient detail to code the design-space dimensions (full-text stage only).

## 6. Screening procedure

1. **De-duplication** (`scripts/merge_dedupe.py`): union-find over normalised
   DOI, arXiv id and normalised title (case/diacritics/punctuation/spacing
   removed); preprint and publisher versions are merged; unstructured
   Crossref reference strings are attached to a candidate if its normalised
   title occurs in them. Remaining duplicates found by hand are coded E6.
2. **Stage 1 — title/abstract** (`output/screening.csv`): two authors
   (S1, S2) independently decide *include / exclude / unsure* with a reason
   code for every candidate. The column
   `SUGGESTION_rule_based_not_a_decision` is a transparent keyword rule
   (documented in `merge_dedupe.py::suggest`) offered only to order the work;
   it must not be copied into the decision columns. Before screening, both
   screeners calibrate on the same random 100 candidates and discuss
   disagreements; report Cohen's κ on the calibration set and on the full set.
   *Unsure* and disagreements go to stage 2.
3. **Stage 2 — full text**: two authors read every stage-1 inclusion; decide
   with I/E codes; disagreements resolved by discussion, a third author
   arbitrates if needed. Report counts per exclusion reason (as Saffo et al.).
4. The included set after stage 2 is the **corpus**.

*Workload note:* the current candidate set is large (see §9). If two full
independent screenings are infeasible, a documented alternative is: S1
screens all; S2 independently screens a random 20 % plus every record S1
excluded with suggestion ≠ *exclude?*; report κ on the overlap. State
whichever procedure is used.

## 7. Snowballing

- **Seeds, round R1:** five surveys — McGee et al. 2019 (CGF, 10.1111/cgf.13610); McGee et al. 2021 (book chapter, 10.1007/978-3-031-02608-9_5); Joos et al. 2025 (ACM Computing Surveys, 10.1145/3859868, arXiv 2501.08500); Saffo et al. 2024 (TVCG, 10.1109/TVCG.2023.3327368); Klein et al. 2022 (it – Information Technology, 10.1515/itit-2022-0037).
- **Directions and indexes:** backward (references) via OpenAlex `referenced_works`, Semantic Scholar `/references`, Crossref `reference`; forward (citations) via OpenAlex `cites:` and Semantic Scholar `/citations` (`scripts/snowball.py`). Two or three independent indexes are used because each misses references (e.g., S2 has no references for Saffo et al.; no open index has references for the McGee 2021 chapter).
- **Manual step:** the McGee 2021 chapter's reference list must be entered by hand (`exports/manual/McGee2021_refs.csv`, ingested with `ingest_export.py --snowball-round R1 --seed S2`).
- **Rounds R2…:** seeds = all corpus works (after full-text screening) not yet used as seeds (`scripts/make_seeds.py --round R2` → `snowball.py --round R2 --seeds output/seeds_R2.csv`). Snowballed candidates are screened with the same two-stage procedure.
- **Stopping rule:** stop when a round adds no new included work. Report per round: seeds, records retrieved, new unique candidates, new inclusions.

## 8. Benchmark set and search-sensitivity check

The 24 works of Table 2 (`config/benchmark.csv`) serve as a known-item
benchmark to estimate search sensitivity (recall), as is standard in
search-strategy development. Matching is by DOI, arXiv id, or near-identical
title (`scripts/benchmark.py`). Because the queries were refined while
looking at this benchmark (two queries, Q6 and Q7, were added after misses),
the reported recall is an **optimistic, in-sample** estimate; we report it
together with the full query history (`query_log.md`). Results:
`output/benchmark_recall.csv` (which source/query/snowballing path retrieved
each work) and `output/recall_by_source.csv`.

## 9. Counts produced so far (scripts only; 2026-11-21)

From `output/prisma_counts.json`:

| Stage | Count |
|---|---:|
| Records identified, database searches (OpenAlex 1,673; Semantic Scholar 1,330; EGDL 524; DBLP 305; arXiv 171) | 4,003 |
| Records identified, snowballing R1 (OpenAlex 734; Semantic Scholar 582; Crossref 504) | 1,820 |
| Total records | 5,823 |
| Duplicates removed | 2,623 |
| Unique candidates to screen | 3,200 (2,510 from searches, 690 only from snowballing) |
| IEEE Xplore, ACM DL | [N_ieee], [N_acm] — not yet run |
| Excluded at title/abstract | [N_excl_TA] |
| Full texts assessed | [N_FT] |
| Excluded at full text (by reason) | [N_excl_FT] ([E1..E8 breakdown]) |
| Snowballing R2… new inclusions | [N_R2], … |
| Corpus | [N_corpus] |
| Coded in detail (Table 2) | 24 |

## 10. Selection of the Table 2 subset (purposive sampling)

Table 2 is a **purposive subset** of the corpus, not the corpus itself. A
corpus work is selected if it satisfies S1 and at least one of S2–S4; S5
breaks ties. The selection rationale per work is recorded in
`table2_selection.csv` (to be created by the authors from
`output/benchmark_recall.csv`):

- **S1 Distinct contribution.** It contributes a distinct system or technique; works that reuse an existing system for a new application domain, or later versions of the same tool, are represented by one paper (original or most complete description).
- **S2 Technique-family representative.** Per platform (desktop, VR, AR, physical), at least one representative of each technique family present in the corpus: layered MLN tools; abstraction/query techniques for large MLNs; matrix and hybrid representations (incl. dynamic networks with time slices as layers); single-layer vs. multilayer immersive network systems; AR network visualizations; network physicalizations.
- **S3 Coverage.** Together, the selected works instantiate every value of the design space that is instantiated anywhere in the corpus (checked against Table 2 rows).
- **S4 AR-specific values.** For an AR-specific value (Physical Anchor, Tangible, Physical Elements, Spatial Context) or AR-amplified input (Touch) that no AR *network* work in the corpus instantiates, the most cited/most complete AR work on non-network data that does is added (marked as non-network).
- **S5 Tie-break.** Prefer peer-reviewed archival venue, then earliest original description, then most detailed description.

The authors must check that applying S1–S5 to the screened corpus yields the
current 24 works, and add or justify the exclusion of every other corpus work
that satisfies them (candidates in `output/notable_candidates.csv`; see
STATUS.md for works that directly affect S4).

## 11. Coding procedure

- **Codebook:** the design-space definitions (Sec. 3.3 of the paper, Fig. 2) with, per value, a definition, inclusion rule and one positive and one negative example (`codebook.csv`, to be written from the paper text). Code "as described in the publication" (text, figures, supplementary video).
- **Coders:** every Table 2 work is coded independently by ≥ 2 authors (one with network-visualization and one with AR/immersive background). Record both codings (`coding_raw.csv`: work × value × coder).
- **Agreement:** report per-value percent agreement and Cohen's κ (or Krippendorff's α across coders) before discussion.
- **Disagreement resolution:** discussion to consensus; unresolved cases decided by a third author; record changes to the codebook made during resolution (versioned).
- **Iteration:** when coding forces a change of the design space (descriptive-adequacy criterion), re-code all works for the affected subdimension.

## 12. Supplement (OSF-style; upload to OSF/Zenodo with a DOI)

| File | Content |
|---|---|
| `protocol.md`, `query_log.md` | this protocol; every query version, hit counts, recall |
| `queries.json`, `rendered_queries.txt` | concept blocks; exact strings per source |
| `raw/*.jsonl`, `raw/run_log.jsonl` | raw retrieved records per source/query/round; machine log |
| `candidates_all.csv` | all unique candidates with provenance (source:query or round:seed:direction:index) |
| `screening.csv` | both screeners' decisions + reason codes, final decision (= list of excluded works with reasons) |
| `prisma_counts.json` + flow table | PRISMA counts |
| `benchmark_recall.csv`, `recall_by_source.csv` | sensitivity check |
| `corpus.csv` | included works with I-codes |
| `table2_selection.csv` | S1–S5 rationale per selected work |
| `codebook.csv`, `coding_raw.csv`, `coding_final.csv`, `agreement.csv` | coding |
| `scripts/` | code to reproduce (Python ≥ 3.10, `requests`) |

## 13. Known limitations of the search

- Recall is estimated on an in-sample benchmark (see §8).
- OpenAlex and Semantic Scholar search abstracts only where available (OpenAlex lacks abstracts for some publishers; 2,426 of 3,200 candidates currently have an abstract, 20 of them filled from Crossref).
- DBLP searches titles only and only the listed venues; EGDL covers only Eurographics publications.
- Stemming differences between engines forced per-source exclusions (Q3 not on S2/arXiv).
- OpenAlex counts can change with index updates (Q1 v3 → v4 reported 269 → 282 although v4 is narrower).
- Terminology: immersive and physical network works rarely use MLN terminology, and some MLN tools do not use "visualization" in title/abstract; snowballing compensates partially.
- The McGee 2021 chapter could not be snowballed through open indexes (manual step).

---

## Appendix A — rendered query strings (final versions)

See `output/rendered_queries.txt` (generated by `scripts/querybuild.py`; reproduced below for OpenAlex, Semantic Scholar, arXiv, EGDL, DBLP, ACM; IEEE sub-queries are listed in the file).

```
######## openalex

[Q1 v4] ("multilayer network" OR "multilayer networks" OR "multi-layer network" OR "multi-layer networks" OR "multilayered network" OR "multilayered networks" OR "multilayer graph" OR "multilayer graphs" OR "multi-layer graph" OR "multiplex network" OR "multiplex networks" OR "multiplex graph" OR "multi-relational network" OR "multi-relational graph" OR "multirelational network") AND (visualization OR visualisation OR "visual analytics" OR "visual analysis" OR visualizing OR visualising)

[Q2 v3] ("augmented reality" OR "mixed reality" OR "virtual reality" OR "extended reality" OR immersive OR "head-mounted" OR HoloLens) AND ("network visualization" OR "network visualisation" OR "graph visualization" OR "graph visualisation" OR "network analysis" OR "graph analysis" OR "node-link" OR "graph drawing" OR "network data" OR "graph data" OR "network exploration" OR "graph exploration")

[Q3 v4] (physicalization OR physicalisation OR "physical visualization" OR "physical visualisation") AND (network OR networks OR graph OR graphs)

[Q4 v2] ("dynamic network" OR "dynamic networks" OR "dynamic graph" OR "dynamic graphs" OR "temporal network" OR "temporal networks" OR "temporal graph" OR "temporal graphs" OR "time-varying network" OR "evolving network") AND (3D OR "three-dimensional" OR 2.5D OR stereoscopic OR "augmented reality" OR "mixed reality" OR "virtual reality" OR "extended reality" OR immersive OR "head-mounted" OR HoloLens OR physicalization OR physicalisation OR "physical visualization" OR "physical visualisation" OR tangible OR "3D printed" OR "3D printing") AND (visualization OR visualisation OR "visual analytics" OR "visual analysis" OR visualizing OR visualising)

[Q5 v2] ("augmented reality" OR "mixed reality" OR HoloLens) AND ("design space" OR "design spaces") AND (visualization OR visualisation OR "visual analytics" OR "visual analysis" OR visualizing OR visualising)

[Q6 v2] ("multilayer network" OR "multilayer networks" OR "multi-layer network" OR "multi-layer networks" OR "multilayered network" OR "multilayered networks" OR "multilayer graph" OR "multilayer graphs" OR "multi-layer graph" OR "multiplex network" OR "multiplex networks" OR "multiplex graph" OR "multi-relational network" OR "multi-relational graph" OR "multirelational network" OR "dynamic network" OR "dynamic networks" OR "dynamic graph" OR "dynamic graphs" OR "temporal network" OR "temporal networks" OR "temporal graph" OR "temporal graphs" OR "time-varying network" OR "evolving network") AND (matrix OR matrices OR "adjacency matrix" OR "hybrid representation" OR "hybrid visualization" OR "hybrid visualisation" OR "node-link") AND (visualization OR visualisation OR "visual analytics" OR "visual analysis" OR visualizing OR visualising)

######## s2

[Q1 v4] ("multilayer network" | "multilayer networks" | "multi-layer network" | "multi-layer networks" | "multilayered network" | "multilayered networks" | "multilayer graph" | "multilayer graphs" | "multi-layer graph" | "multiplex network" | "multiplex networks" | "multiplex graph" | "multi-relational network" | "multi-relational graph" | "multirelational network") + (visualization | visualisation | "visual analytics" | "visual analysis" | visualizing | visualising)

[Q2 v3] ("augmented reality" | "mixed reality" | "virtual reality" | "extended reality" | immersive | "head-mounted" | HoloLens) + ("network visualization" | "network visualisation" | "graph visualization" | "graph visualisation" | "network analysis" | "graph analysis" | "node-link" | "graph drawing" | "network data" | "graph data" | "network exploration" | "graph exploration")

[Q4 v2] ("dynamic network" | "dynamic networks" | "dynamic graph" | "dynamic graphs" | "temporal network" | "temporal networks" | "temporal graph" | "temporal graphs" | "time-varying network" | "evolving network") + (3D | "three-dimensional" | 2.5D | stereoscopic | "augmented reality" | "mixed reality" | "virtual reality" | "extended reality" | immersive | "head-mounted" | HoloLens | physicalization | physicalisation | "physical visualization" | "physical visualisation" | tangible | "3D printed" | "3D printing") + (visualization | visualisation | "visual analytics" | "visual analysis" | visualizing | visualising)

[Q5 v2] ("augmented reality" | "mixed reality" | HoloLens) + ("design space" | "design spaces") + (visualization | visualisation | "visual analytics" | "visual analysis" | visualizing | visualising)

[Q6 v2] ("multilayer network" | "multilayer networks" | "multi-layer network" | "multi-layer networks" | "multilayered network" | "multilayered networks" | "multilayer graph" | "multilayer graphs" | "multi-layer graph" | "multiplex network" | "multiplex networks" | "multiplex graph" | "multi-relational network" | "multi-relational graph" | "multirelational network" | "dynamic network" | "dynamic networks" | "dynamic graph" | "dynamic graphs" | "temporal network" | "temporal networks" | "temporal graph" | "temporal graphs" | "time-varying network" | "evolving network") + (matrix | matrices | "adjacency matrix" | "hybrid representation" | "hybrid visualization" | "hybrid visualisation" | "node-link") + (visualization | visualisation | "visual analytics" | "visual analysis" | visualizing | visualising)

######## arxiv

[Q1 v4] (ti:"multilayer network" OR abs:"multilayer network" OR ti:"multilayer networks" OR abs:"multilayer networks" OR ti:"multi-layer network" OR abs:"multi-layer network" OR ti:"multi-layer networks" OR abs:"multi-layer networks" OR ti:"multilayered network" OR abs:"multilayered network" OR ti:"multilayered networks" OR abs:"multilayered networks" OR ti:"multilayer graph" OR abs:"multilayer graph" OR ti:"multilayer graphs" OR abs:"multilayer graphs" OR ti:"multi-layer graph" OR abs:"multi-layer graph" OR ti:"multiplex network" OR abs:"multiplex network" OR ti:"multiplex networks" OR abs:"multiplex networks" OR ti:"multiplex graph" OR abs:"multiplex graph" OR ti:"multi-relational network" OR abs:"multi-relational network" OR ti:"multi-relational graph" OR abs:"multi-relational graph" OR ti:"multirelational network" OR abs:"multirelational network") AND (ti:visualization OR abs:visualization OR ti:visualisation OR abs:visualisation OR ti:"visual analytics" OR abs:"visual analytics" OR ti:"visual analysis" OR abs:"visual analysis" OR ti:visualizing OR abs:visualizing OR ti:visualising OR abs:visualising)

[Q2 v3] (ti:"augmented reality" OR abs:"augmented reality" OR ti:"mixed reality" OR abs:"mixed reality" OR ti:"virtual reality" OR abs:"virtual reality" OR ti:"extended reality" OR abs:"extended reality" OR ti:immersive OR abs:immersive OR ti:"head-mounted" OR abs:"head-mounted" OR ti:HoloLens OR abs:HoloLens) AND (ti:"network visualization" OR abs:"network visualization" OR ti:"network visualisation" OR abs:"network visualisation" OR ti:"graph visualization" OR abs:"graph visualization" OR ti:"graph visualisation" OR abs:"graph visualisation" OR ti:"network analysis" OR abs:"network analysis" OR ti:"graph analysis" OR abs:"graph analysis" OR ti:"node-link" OR abs:"node-link" OR ti:"graph drawing" OR abs:"graph drawing" OR ti:"network data" OR abs:"network data" OR ti:"graph data" OR abs:"graph data" OR ti:"network exploration" OR abs:"network exploration" OR ti:"graph exploration" OR abs:"graph exploration")

[Q4 v2] (ti:"dynamic network" OR abs:"dynamic network" OR ti:"dynamic networks" OR abs:"dynamic networks" OR ti:"dynamic graph" OR abs:"dynamic graph" OR ti:"dynamic graphs" OR abs:"dynamic graphs" OR ti:"temporal network" OR abs:"temporal network" OR ti:"temporal networks" OR abs:"temporal networks" OR ti:"temporal graph" OR abs:"temporal graph" OR ti:"temporal graphs" OR abs:"temporal graphs" OR ti:"time-varying network" OR abs:"time-varying network" OR ti:"evolving network" OR abs:"evolving network") AND (ti:3D OR abs:3D OR ti:"three-dimensional" OR abs:"three-dimensional" OR ti:2.5D OR abs:2.5D OR ti:stereoscopic OR abs:stereoscopic OR ti:"augmented reality" OR abs:"augmented reality" OR ti:"mixed reality" OR abs:"mixed reality" OR ti:"virtual reality" OR abs:"virtual reality" OR ti:"extended reality" OR abs:"extended reality" OR ti:immersive OR abs:immersive OR ti:"head-mounted" OR abs:"head-mounted" OR ti:HoloLens OR abs:HoloLens OR ti:physicalization OR abs:physicalization OR ti:physicalisation OR abs:physicalisation OR ti:"physical visualization" OR abs:"physical visualization" OR ti:"physical visualisation" OR abs:"physical visualisation" OR ti:tangible OR abs:tangible OR ti:"3D printed" OR abs:"3D printed" OR ti:"3D printing" OR abs:"3D printing") AND (ti:visualization OR abs:visualization OR ti:visualisation OR abs:visualisation OR ti:"visual analytics" OR abs:"visual analytics" OR ti:"visual analysis" OR abs:"visual analysis" OR ti:visualizing OR abs:visualizing OR ti:visualising OR abs:visualising)

[Q5 v2] (ti:"augmented reality" OR abs:"augmented reality" OR ti:"mixed reality" OR abs:"mixed reality" OR ti:HoloLens OR abs:HoloLens) AND (ti:"design space" OR abs:"design space" OR ti:"design spaces" OR abs:"design spaces") AND (ti:visualization OR abs:visualization OR ti:visualisation OR abs:visualisation OR ti:"visual analytics" OR abs:"visual analytics" OR ti:"visual analysis" OR abs:"visual analysis" OR ti:visualizing OR abs:visualizing OR ti:visualising OR abs:visualising)

[Q6 v2] (ti:"multilayer network" OR abs:"multilayer network" OR ti:"multilayer networks" OR abs:"multilayer networks" OR ti:"multi-layer network" OR abs:"multi-layer network" OR ti:"multi-layer networks" OR abs:"multi-layer networks" OR ti:"multilayered network" OR abs:"multilayered network" OR ti:"multilayered networks" OR abs:"multilayered networks" OR ti:"multilayer graph" OR abs:"multilayer graph" OR ti:"multilayer graphs" OR abs:"multilayer graphs" OR ti:"multi-layer graph" OR abs:"multi-layer graph" OR ti:"multiplex network" OR abs:"multiplex network" OR ti:"multiplex networks" OR abs:"multiplex networks" OR ti:"multiplex graph" OR abs:"multiplex graph" OR ti:"multi-relational network" OR abs:"multi-relational network" OR ti:"multi-relational graph" OR abs:"multi-relational graph" OR ti:"multirelational network" OR abs:"multirelational network" OR ti:"dynamic network" OR abs:"dynamic network" OR ti:"dynamic networks" OR abs:"dynamic networks" OR ti:"dynamic graph" OR abs:"dynamic graph" OR ti:"dynamic graphs" OR abs:"dynamic graphs" OR ti:"temporal network" OR abs:"temporal network" OR ti:"temporal networks" OR abs:"temporal networks" OR ti:"temporal graph" OR abs:"temporal graph" OR ti:"temporal graphs" OR abs:"temporal graphs" OR ti:"time-varying network" OR abs:"time-varying network" OR ti:"evolving network" OR abs:"evolving network") AND (ti:matrix OR abs:matrix OR ti:matrices OR abs:matrices OR ti:"adjacency matrix" OR abs:"adjacency matrix" OR ti:"hybrid representation" OR abs:"hybrid representation" OR ti:"hybrid visualization" OR abs:"hybrid visualization" OR ti:"hybrid visualisation" OR abs:"hybrid visualisation" OR ti:"node-link" OR abs:"node-link") AND (ti:visualization OR abs:visualization OR ti:visualisation OR abs:visualisation OR ti:"visual analytics" OR abs:"visual analytics" OR ti:"visual analysis" OR abs:"visual analysis" OR ti:visualizing OR abs:visualizing OR ti:visualising OR abs:visualising)

######## egdl

[Q1 v4] (dc.title:((multilayer AND network) OR (multilayer AND networks) OR (multi AND layer AND network) OR (multi AND layer AND networks) OR (multilayered AND network) OR (multilayered AND networks) OR (multilayer AND graph) OR (multilayer AND graphs) OR (multi AND layer AND graph) OR (multiplex AND network) OR (multiplex AND networks) OR (multiplex AND graph) OR (multi AND relational AND network) OR (multi AND relational AND graph) OR (multirelational AND network)) OR dc.description.abstract:((multilayer AND network) OR (multilayer AND networks) OR (multi AND layer AND network) OR (multi AND layer AND networks) OR (multilayered AND network) OR (multilayered AND networks) OR (multilayer AND graph) OR (multilayer AND graphs) OR (multi AND layer AND graph) OR (multiplex AND network) OR (multiplex AND networks) OR (multiplex AND graph) OR (multi AND relational AND network) OR (multi AND relational AND graph) OR (multirelational AND network)) OR dc.subject:((multilayer AND network) OR (multilayer AND networks) OR (multi AND layer AND network) OR (multi AND layer AND networks) OR (multilayered AND network) OR (multilayered AND networks) OR (multilayer AND graph) OR (multilayer AND graphs) OR (multi AND layer AND graph) OR (multiplex AND network) OR (multiplex AND networks) OR (multiplex AND graph) OR (multi AND relational AND network) OR (multi AND relational AND graph) OR (multirelational AND network))) AND (dc.title:(visualization OR visualisation OR (visual AND analytics) OR (visual AND analysis) OR visualizing OR visualising) OR dc.description.abstract:(visualization OR visualisation OR (visual AND analytics) OR (visual AND analysis) OR visualizing OR visualising) OR dc.subject:(visualization OR visualisation OR (visual AND analytics) OR (visual AND analysis) OR visualizing OR visualising))

[Q2 v3] (dc.title:((augmented AND reality) OR (mixed AND reality) OR (virtual AND reality) OR (extended AND reality) OR immersive OR (head AND mounted) OR HoloLens) OR dc.description.abstract:((augmented AND reality) OR (mixed AND reality) OR (virtual AND reality) OR (extended AND reality) OR immersive OR (head AND mounted) OR HoloLens) OR dc.subject:((augmented AND reality) OR (mixed AND reality) OR (virtual AND reality) OR (extended AND reality) OR immersive OR (head AND mounted) OR HoloLens)) AND (dc.title:((network AND visualization) OR (network AND visualisation) OR (graph AND visualization) OR (graph AND visualisation) OR (network AND analysis) OR (graph AND analysis) OR (node AND link) OR (graph AND drawing) OR (network AND data) OR (graph AND data) OR (network AND exploration) OR (graph AND exploration)) OR dc.description.abstract:((network AND visualization) OR (network AND visualisation) OR (graph AND visualization) OR (graph AND visualisation) OR (network AND analysis) OR (graph AND analysis) OR (node AND link) OR (graph AND drawing) OR (network AND data) OR (graph AND data) OR (network AND exploration) OR (graph AND exploration)) OR dc.subject:((network AND visualization) OR (network AND visualisation) OR (graph AND visualization) OR (graph AND visualisation) OR (network AND analysis) OR (graph AND analysis) OR (node AND link) OR (graph AND drawing) OR (network AND data) OR (graph AND data) OR (network AND exploration) OR (graph AND exploration)))

[Q3 v4] (dc.title:(physicalization OR physicalisation OR (physical AND visualization) OR (physical AND visualisation)) OR dc.description.abstract:(physicalization OR physicalisation OR (physical AND visualization) OR (physical AND visualisation)) OR dc.subject:(physicalization OR physicalisation OR (physical AND visualization) OR (physical AND visualisation))) AND (dc.title:(network OR networks OR graph OR graphs) OR dc.description.abstract:(network OR networks OR graph OR graphs) OR dc.subject:(network OR networks OR graph OR graphs))

[Q4 v2] (dc.title:((dynamic AND network) OR (dynamic AND networks) OR (dynamic AND graph) OR (dynamic AND graphs) OR (temporal AND network) OR (temporal AND networks) OR (temporal AND graph) OR (temporal AND graphs) OR (time AND varying AND network) OR (evolving AND network)) OR dc.description.abstract:((dynamic AND network) OR (dynamic AND networks) OR (dynamic AND graph) OR (dynamic AND graphs) OR (temporal AND network) OR (temporal AND networks) OR (temporal AND graph) OR (temporal AND graphs) OR (time AND varying AND network) OR (evolving AND network)) OR dc.subject:((dynamic AND network) OR (dynamic AND networks) OR (dynamic AND graph) OR (dynamic AND graphs) OR (temporal AND network) OR (temporal AND networks) OR (temporal AND graph) OR (temporal AND graphs) OR (time AND varying AND network) OR (evolving AND network))) AND (dc.title:(3D OR (three AND dimensional) OR 2.5D OR stereoscopic OR (augmented AND reality) OR (mixed AND reality) OR (virtual AND reality) OR (extended AND reality) OR immersive OR (head AND mounted) OR HoloLens OR physicalization OR physicalisation OR (physical AND visualization) OR (physical AND visualisation) OR tangible OR (3D AND printed) OR (3D AND printing)) OR dc.description.abstract:(3D OR (three AND dimensional) OR 2.5D OR stereoscopic OR (augmented AND reality) OR (mixed AND reality) OR (virtual AND reality) OR (extended AND reality) OR immersive OR (head AND mounted) OR HoloLens OR physicalization OR physicalisation OR (physical AND visualization) OR (physical AND visualisation) OR tangible OR (3D AND printed) OR (3D AND printing)) OR dc.subject:(3D OR (three AND dimensional) OR 2.5D OR stereoscopic OR (augmented AND reality) OR (mixed AND reality) OR (virtual AND reality) OR (extended AND reality) OR immersive OR (head AND mounted) OR HoloLens OR physicalization OR physicalisation OR (physical AND visualization) OR (physical AND visualisation) OR tangible OR (3D AND printed) OR (3D AND printing))) AND (dc.title:(visualization OR visualisation OR (visual AND analytics) OR (visual AND analysis) OR visualizing OR visualising) OR dc.description.abstract:(visualization OR visualisation OR (visual AND analytics) OR (visual AND analysis) OR visualizing OR visualising) OR dc.subject:(visualization OR visualisation OR (visual AND analytics) OR (visual AND analysis) OR visualizing OR visualising))

[Q5 v2] (dc.title:((augmented AND reality) OR (mixed AND reality) OR HoloLens) OR dc.description.abstract:((augmented AND reality) OR (mixed AND reality) OR HoloLens) OR dc.subject:((augmented AND reality) OR (mixed AND reality) OR HoloLens)) AND (dc.title:((design AND space) OR (design AND spaces)) OR dc.description.abstract:((design AND space) OR (design AND spaces)) OR dc.subject:((design AND space) OR (design AND spaces))) AND (dc.title:(visualization OR visualisation OR (visual AND analytics) OR (visual AND analysis) OR visualizing OR visualising) OR dc.description.abstract:(visualization OR visualisation OR (visual AND analytics) OR (visual AND analysis) OR visualizing OR visualising) OR dc.subject:(visualization OR visualisation OR (visual AND analytics) OR (visual AND analysis) OR visualizing OR visualising))

[Q6 v2] (dc.title:((multilayer AND network) OR (multilayer AND networks) OR (multi AND layer AND network) OR (multi AND layer AND networks) OR (multilayered AND network) OR (multilayered AND networks) OR (multilayer AND graph) OR (multilayer AND graphs) OR (multi AND layer AND graph) OR (multiplex AND network) OR (multiplex AND networks) OR (multiplex AND graph) OR (multi AND relational AND network) OR (multi AND relational AND graph) OR (multirelational AND network) OR (dynamic AND network) OR (dynamic AND networks) OR (dynamic AND graph) OR (dynamic AND graphs) OR (temporal AND network) OR (temporal AND networks) OR (temporal AND graph) OR (temporal AND graphs) OR (time AND varying AND network) OR (evolving AND network)) OR dc.description.abstract:((multilayer AND network) OR (multilayer AND networks) OR (multi AND layer AND network) OR (multi AND layer AND networks) OR (multilayered AND network) OR (multilayered AND networks) OR (multilayer AND graph) OR (multilayer AND graphs) OR (multi AND layer AND graph) OR (multiplex AND network) OR (multiplex AND networks) OR (multiplex AND graph) OR (multi AND relational AND network) OR (multi AND relational AND graph) OR (multirelational AND network) OR (dynamic AND network) OR (dynamic AND networks) OR (dynamic AND graph) OR (dynamic AND graphs) OR (temporal AND network) OR (temporal AND networks) OR (temporal AND graph) OR (temporal AND graphs) OR (time AND varying AND network) OR (evolving AND network)) OR dc.subject:((multilayer AND network) OR (multilayer AND networks) OR (multi AND layer AND network) OR (multi AND layer AND networks) OR (multilayered AND network) OR (multilayered AND networks) OR (multilayer AND graph) OR (multilayer AND graphs) OR (multi AND layer AND graph) OR (multiplex AND network) OR (multiplex AND networks) OR (multiplex AND graph) OR (multi AND relational AND network) OR (multi AND relational AND graph) OR (multirelational AND network) OR (dynamic AND network) OR (dynamic AND networks) OR (dynamic AND graph) OR (dynamic AND graphs) OR (temporal AND network) OR (temporal AND networks) OR (temporal AND graph) OR (temporal AND graphs) OR (time AND varying AND network) OR (evolving AND network))) AND (dc.title:(matrix OR matrices OR (adjacency AND matrix) OR (hybrid AND representation) OR (hybrid AND visualization) OR (hybrid AND visualisation) OR (node AND link)) OR dc.description.abstract:(matrix OR matrices OR (adjacency AND matrix) OR (hybrid AND representation) OR (hybrid AND visualization) OR (hybrid AND visualisation) OR (node AND link)) OR dc.subject:(matrix OR matrices OR (adjacency AND matrix) OR (hybrid AND representation) OR (hybrid AND visualization) OR (hybrid AND visualisation) OR (node AND link))) AND (dc.title:(visualization OR visualisation OR (visual AND analytics) OR (visual AND analysis) OR visualizing OR visualising) OR dc.description.abstract:(visualization OR visualisation OR (visual AND analytics) OR (visual AND analysis) OR visualizing OR visualising) OR dc.subject:(visualization OR visualisation OR (visual AND analytics) OR (visual AND analysis) OR visualizing OR visualising))

[Q7 v2] (dc.title:((augmented AND reality) OR (mixed AND reality) OR HoloLens) OR dc.description.abstract:((augmented AND reality) OR (mixed AND reality) OR HoloLens) OR dc.subject:((augmented AND reality) OR (mixed AND reality) OR HoloLens)) AND (dc.title:(tangible OR touch OR (physical AND object) OR (physical AND objects) OR (physical AND referent) OR (physical AND referents) OR handheld) OR dc.description.abstract:(tangible OR touch OR (physical AND object) OR (physical AND objects) OR (physical AND referent) OR (physical AND referents) OR handheld) OR dc.subject:(tangible OR touch OR (physical AND object) OR (physical AND objects) OR (physical AND referent) OR (physical AND referents) OR handheld)) AND (dc.title:(visualization OR visualisation OR (visual AND analytics) OR (visual AND analysis) OR visualizing OR visualising) OR dc.description.abstract:(visualization OR visualisation OR (visual AND analytics) OR (visual AND analysis) OR visualizing OR visualising) OR dc.subject:(visualization OR visualisation OR (visual AND analytics) OR (visual AND analysis) OR visualizing OR visualising))

######## acm

[Q1 v4] (Title:("multilayer network" OR "multilayer networks" OR "multi-layer network" OR "multi-layer networks" OR "multilayered network" OR "multilayered networks" OR "multilayer graph" OR "multilayer graphs" OR "multi-layer graph" OR "multiplex network" OR "multiplex networks" OR "multiplex graph" OR "multi-relational network" OR "multi-relational graph" OR "multirelational network") OR Abstract:("multilayer network" OR "multilayer networks" OR "multi-layer network" OR "multi-layer networks" OR "multilayered network" OR "multilayered networks" OR "multilayer graph" OR "multilayer graphs" OR "multi-layer graph" OR "multiplex network" OR "multiplex networks" OR "multiplex graph" OR "multi-relational network" OR "multi-relational graph" OR "multirelational network") OR Keyword:("multilayer network" OR "multilayer networks" OR "multi-layer network" OR "multi-layer networks" OR "multilayered network" OR "multilayered networks" OR "multilayer graph" OR "multilayer graphs" OR "multi-layer graph" OR "multiplex network" OR "multiplex networks" OR "multiplex graph" OR "multi-relational network" OR "multi-relational graph" OR "multirelational network")) AND (Title:(visualization OR visualisation OR "visual analytics" OR "visual analysis" OR visualizing OR visualising) OR Abstract:(visualization OR visualisation OR "visual analytics" OR "visual analysis" OR visualizing OR visualising) OR Keyword:(visualization OR visualisation OR "visual analytics" OR "visual analysis" OR visualizing OR visualising))

[Q2 v3] (Title:("augmented reality" OR "mixed reality" OR "virtual reality" OR "extended reality" OR immersive OR "head-mounted" OR HoloLens) OR Abstract:("augmented reality" OR "mixed reality" OR "virtual reality" OR "extended reality" OR immersive OR "head-mounted" OR HoloLens) OR Keyword:("augmented reality" OR "mixed reality" OR "virtual reality" OR "extended reality" OR immersive OR "head-mounted" OR HoloLens)) AND (Title:("network visualization" OR "network visualisation" OR "graph visualization" OR "graph visualisation" OR "network analysis" OR "graph analysis" OR "node-link" OR "graph drawing" OR "network data" OR "graph data" OR "network exploration" OR "graph exploration") OR Abstract:("network visualization" OR "network visualisation" OR "graph visualization" OR "graph visualisation" OR "network analysis" OR "graph analysis" OR "node-link" OR "graph drawing" OR "network data" OR "graph data" OR "network exploration" OR "graph exploration") OR Keyword:("network visualization" OR "network visualisation" OR "graph visualization" OR "graph visualisation" OR "network analysis" OR "graph analysis" OR "node-link" OR "graph drawing" OR "network data" OR "graph data" OR "network exploration" OR "graph exploration"))

[Q3 v4] (Title:(physicalization OR physicalisation OR "physical visualization" OR "physical visualisation") OR Abstract:(physicalization OR physicalisation OR "physical visualization" OR "physical visualisation") OR Keyword:(physicalization OR physicalisation OR "physical visualization" OR "physical visualisation")) AND (Title:(network OR networks OR graph OR graphs) OR Abstract:(network OR networks OR graph OR graphs) OR Keyword:(network OR networks OR graph OR graphs))

[Q4 v2] (Title:("dynamic network" OR "dynamic networks" OR "dynamic graph" OR "dynamic graphs" OR "temporal network" OR "temporal networks" OR "temporal graph" OR "temporal graphs" OR "time-varying network" OR "evolving network") OR Abstract:("dynamic network" OR "dynamic networks" OR "dynamic graph" OR "dynamic graphs" OR "temporal network" OR "temporal networks" OR "temporal graph" OR "temporal graphs" OR "time-varying network" OR "evolving network") OR Keyword:("dynamic network" OR "dynamic networks" OR "dynamic graph" OR "dynamic graphs" OR "temporal network" OR "temporal networks" OR "temporal graph" OR "temporal graphs" OR "time-varying network" OR "evolving network")) AND (Title:(3D OR "three-dimensional" OR 2.5D OR stereoscopic OR "augmented reality" OR "mixed reality" OR "virtual reality" OR "extended reality" OR immersive OR "head-mounted" OR HoloLens OR physicalization OR physicalisation OR "physical visualization" OR "physical visualisation" OR tangible OR "3D printed" OR "3D printing") OR Abstract:(3D OR "three-dimensional" OR 2.5D OR stereoscopic OR "augmented reality" OR "mixed reality" OR "virtual reality" OR "extended reality" OR immersive OR "head-mounted" OR HoloLens OR physicalization OR physicalisation OR "physical visualization" OR "physical visualisation" OR tangible OR "3D printed" OR "3D printing") OR Keyword:(3D OR "three-dimensional" OR 2.5D OR stereoscopic OR "augmented reality" OR "mixed reality" OR "virtual reality" OR "extended reality" OR immersive OR "head-mounted" OR HoloLens OR physicalization OR physicalisation OR "physical visualization" OR "physical visualisation" OR tangible OR "3D printed" OR "3D printing")) AND (Title:(visualization OR visualisation OR "visual analytics" OR "visual analysis" OR visualizing OR visualising) OR Abstract:(visualization OR visualisation OR "visual analytics" OR "visual analysis" OR visualizing OR visualising) OR Keyword:(visualization OR visualisation OR "visual analytics" OR "visual analysis" OR visualizing OR visualising))

[Q5 v2] (Title:("augmented reality" OR "mixed reality" OR HoloLens) OR Abstract:("augmented reality" OR "mixed reality" OR HoloLens) OR Keyword:("augmented reality" OR "mixed reality" OR HoloLens)) AND (Title:("design space" OR "design spaces") OR Abstract:("design space" OR "design spaces") OR Keyword:("design space" OR "design spaces")) AND (Title:(visualization OR visualisation OR "visual analytics" OR "visual analysis" OR visualizing OR visualising) OR Abstract:(visualization OR visualisation OR "visual analytics" OR "visual analysis" OR visualizing OR visualising) OR Keyword:(visualization OR visualisation OR "visual analytics" OR "visual analysis" OR visualizing OR visualising))

[Q6 v2] (Title:("multilayer network" OR "multilayer networks" OR "multi-layer network" OR "multi-layer networks" OR "multilayered network" OR "multilayered networks" OR "multilayer graph" OR "multilayer graphs" OR "multi-layer graph" OR "multiplex network" OR "multiplex networks" OR "multiplex graph" OR "multi-relational network" OR "multi-relational graph" OR "multirelational network" OR "dynamic network" OR "dynamic networks" OR "dynamic graph" OR "dynamic graphs" OR "temporal network" OR "temporal networks" OR "temporal graph" OR "temporal graphs" OR "time-varying network" OR "evolving network") OR Abstract:("multilayer network" OR "multilayer networks" OR "multi-layer network" OR "multi-layer networks" OR "multilayered network" OR "multilayered networks" OR "multilayer graph" OR "multilayer graphs" OR "multi-layer graph" OR "multiplex network" OR "multiplex networks" OR "multiplex graph" OR "multi-relational network" OR "multi-relational graph" OR "multirelational network" OR "dynamic network" OR "dynamic networks" OR "dynamic graph" OR "dynamic graphs" OR "temporal network" OR "temporal networks" OR "temporal graph" OR "temporal graphs" OR "time-varying network" OR "evolving network") OR Keyword:("multilayer network" OR "multilayer networks" OR "multi-layer network" OR "multi-layer networks" OR "multilayered network" OR "multilayered networks" OR "multilayer graph" OR "multilayer graphs" OR "multi-layer graph" OR "multiplex network" OR "multiplex networks" OR "multiplex graph" OR "multi-relational network" OR "multi-relational graph" OR "multirelational network" OR "dynamic network" OR "dynamic networks" OR "dynamic graph" OR "dynamic graphs" OR "temporal network" OR "temporal networks" OR "temporal graph" OR "temporal graphs" OR "time-varying network" OR "evolving network")) AND (Title:(matrix OR matrices OR "adjacency matrix" OR "hybrid representation" OR "hybrid visualization" OR "hybrid visualisation" OR "node-link") OR Abstract:(matrix OR matrices OR "adjacency matrix" OR "hybrid representation" OR "hybrid visualization" OR "hybrid visualisation" OR "node-link") OR Keyword:(matrix OR matrices OR "adjacency matrix" OR "hybrid representation" OR "hybrid visualization" OR "hybrid visualisation" OR "node-link")) AND (Title:(visualization OR visualisation OR "visual analytics" OR "visual analysis" OR visualizing OR visualising) OR Abstract:(visualization OR visualisation OR "visual analytics" OR "visual analysis" OR visualizing OR visualising) OR Keyword:(visualization OR visualisation OR "visual analytics" OR "visual analysis" OR visualizing OR visualising))

[Q7 v2] (Title:("augmented reality" OR "mixed reality" OR HoloLens) OR Abstract:("augmented reality" OR "mixed reality" OR HoloLens) OR Keyword:("augmented reality" OR "mixed reality" OR HoloLens)) AND (Title:(tangible OR touch OR "physical object" OR "physical objects" OR "physical referent" OR "physical referents" OR handheld) OR Abstract:(tangible OR touch OR "physical object" OR "physical objects" OR "physical referent" OR "physical referents" OR handheld) OR Keyword:(tangible OR touch OR "physical object" OR "physical objects" OR "physical referent" OR "physical referents" OR handheld)) AND (Title:(visualization OR visualisation OR "visual analytics" OR "visual analysis" OR visualizing OR visualising) OR Abstract:(visualization OR visualisation OR "visual analytics" OR "visual analysis" OR visualizing OR visualising) OR Keyword:(visualization OR visualisation OR "visual analytics" OR "visual analysis" OR visualizing OR visualising))

######## dblp

[Q1 v4] ['(\\bmultilayer|\\bmulti[- ]?layer|\\bmultilayered|\\bmulti[- ]?layered|\\bmultiplex|\\bmulti[- ]?relational|\\bmultirelational)', '(\\bnetwork|\\bnetworks|\\bgraph|\\bgraphs)']

[Q2 v3] ['(\\baugmented[- ]reality|\\bmixed[- ]reality|\\bvirtual[- ]reality|\\bextended[- ]reality|\\bimmersive|\\bhead[- ]?mounted|\\bhololens|\\bvr\\b|\\bar\\b|\\bxr\\b|\\bmr\\b)', '(\\bnetwork|\\bnetworks|\\bgraph|\\bgraphs)']

[Q3 v4] ['(\\bphysicalization|\\bphysicalisation|\\bphysical[- ]visualization|\\bphysical[- ]visualisation)', '(\\bnetwork|\\bnetworks|\\bgraph|\\bgraphs)']

[Q4 v2] ['(\\bdynamic[- ]network|\\bdynamic[- ]networks|\\bdynamic[- ]graph|\\bdynamic[- ]graphs|\\btemporal[- ]network|\\btemporal[- ]networks|\\btemporal[- ]graph|\\btemporal[- ]graphs|\\btime[- ]?varying[- ]network|\\bevolving[- ]network)', '(\\b3d\\b|\\bthree[- ]?dimensional|\\b2\\.5d|\\bstereoscopic|\\baugmented[- ]reality|\\bmixed[- ]reality|\\bvirtual[- ]reality|\\bextended[- ]reality|\\bimmersive|\\bhead[- ]?mounted|\\bhololens|\\bvr\\b|\\bar\\b|\\bxr\\b|\\bmr\\b|\\bphysicalization|\\bphysicalisation|\\bphysical[- ]visualization|\\bphysical[- ]visualisation|\\btangible|\\b3d[- ]printed|\\b3d[- ]printing)']

[Q5 v2] ['(\\baugmented[- ]reality|\\bmixed[- ]reality|\\bhololens|\\bvr\\b|\\bar\\b|\\bxr\\b|\\bmr\\b)', '(\\bdesign[- ]space|\\bdesign[- ]spaces)']

[Q6 v2] ['(\\bmultilayer|\\bmulti[- ]?layer|\\bmultilayered|\\bmulti[- ]?layered|\\bmultiplex|\\bmulti[- ]?relational|\\bmultirelational|\\bdynamic[- ]network|\\bdynamic[- ]networks|\\bdynamic[- ]graph|\\bdynamic[- ]graphs|\\btemporal[- ]network|\\btemporal[- ]networks|\\btemporal[- ]graph|\\btemporal[- ]graphs|\\btime[- ]?varying[- ]network|\\bevolving[- ]network)', '(\\bmatrix|\\bmatrices|\\badjacency[- ]matrix|\\bhybrid[- ]representation|\\bhybrid[- ]visualization|\\bhybrid[- ]visualisation|\\bnode[- ]?link)']

[Q7 v2] ['(\\baugmented[- ]reality|\\bmixed[- ]reality|\\bhololens)', '(\\btangible|\\btouch|\\bphysical[- ]object|\\bphysical[- ]objects|\\bphysical[- ]referent|\\bphysical[- ]referents|\\bhandheld)']
```

### Protocol amendment A1 (2026-11-21)
During round-2 screening the inclusion boundary of I4 and the treatment of juxtaposed time slices under I1 proved ambiguous (screeners disagreed). The authors narrowed I4 to AR visualization of abstract data, and restricted I1 for dynamic networks to time slices drawn as distinct layers (see `screening_ai/criteria.md`, Amendment A1). The amendment was applied retroactively to all rounds (R1 and R2) before the corpus was fixed; affected decisions are flagged in the screening sheets.

### Amendment A2 (2026-11-21)
Decided by the authors during full-text screening; see `screening_ai/criteria.md`: bipartite/two-mode networks → E3; simultaneous embedding → I1 only with a visualization design, else E8; stereoscopic desktop displays are not immersive (E3).

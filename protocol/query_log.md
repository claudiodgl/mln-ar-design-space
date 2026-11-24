# Query log — search-strategy development

This log is reportable as part of the supplement. It records every query
version that was executed, why it was changed, and what it did to (a) the
number of hits and (b) the recall of the 24-work benchmark set
(`config/benchmark.csv`, = Table 2 of the paper). The run table and the exact
strings below are generated from `raw/run_log.jsonl` by
`scripts/make_query_log.py`; this narrative is hand-written.

**Important caveat for reporting.** The benchmark was used to *develop* the
queries (standard practice for search-strategy development, but there was no
held-out validation set). The recall figures are therefore optimistic
estimates of sensitivity and must be reported as such. Changes that were
motivated by a benchmark miss are marked **[benchmark-informed]**; changes
motivated by precision (too many off-topic hits) or by a source's syntax are
marked **[precision]** / **[syntax]**.

All runs: 2026-11-21. No date limits were applied in any source. OpenAlex
strings logged without a field prefix (v1, v2 count runs) were sent as
`filter=title_and_abstract.search:<string>`.

## Concept blocks (final)

See `config/queries.json` → `blocks`. Final queries are AND-combinations:

| ID | label | logic (blocks) |
|---|---|---|
| Q1 | MLN visualization | MLNP AND VIS |
| Q2 | Immersive network visualization | IMM AND NETVIS |
| Q3 | Network physicalization | PHYSX AND NET |
| Q4 | Dynamic networks in 3D / immersive / physical form | DYN AND (THREED OR IMM OR PHYSX OR TANG) AND VIS |
| Q5 | Design spaces for AR/MR visualization | AR AND DS AND VIS |
| Q6 | Matrix / hybrid representations of multilayer or dynamic networks | (MLNP OR DYN) AND MAT AND VIS |
| Q7 | Tangible / touch / physical-object interaction for AR visualization (any data), venue-restricted | AR AND TOUCH (DBLP titles in vis/HCI/XR venues; EGDL; ACM/IEEE with publication filter) |
| (Q3b) | Tangible network visualization — **retired** | TANG AND NETVIS |

## Version history

**v1 (Q1–Q4; OpenAlex counts only).** Direct transcription of the search
described in the draft paper: (multilayer | multiplex | multi-relational …)
AND (network | graph) AND visualization; immersive terms AND (network | graph)
AND visualization; physical/tangible terms AND (network | graph) AND
visualization; dynamic/temporal network AND (3D | immersive | physical) AND
visualization. OpenAlex reported 2,650 / 3,717 / 9,061 / 181 hits. Single
words "network"/"graph" matched neural networks, multilayer perceptrons, etc.
→ v2. **[precision]**

**v2.** Q1 uses phrase terms (MLNP: "multilayer network(s)", "multiplex
network(s)", "multi-relational graph", …); Q2 requires a network-visualization
phrase (NETVIS: "network visualization", "graph analysis", "node-link", …)
instead of bare network|graph; Q3 split into Q3 (physicalization terms AND
network|graph) and Q3b (tangible / 3D printing AND NETVIS). Q5 (AR/MR AND
"design space" AND visualization) added to cover the inclusion criterion
"design spaces for immersive visualization" that the draft method already
named; it was added at the same time as we knew that Lee et al. 2022 is a
design space paper, so it is partly **[benchmark-informed]**. OpenAlex: Q1
269, Q2 888, Q3 393,434, Q3b 437, Q5 78. Q3 exploded because OpenAlex stems
"physicalization" to "physic*" → v3. **[precision]**

**v3 (Q3 only).** OpenAlex field switched to the unstemmed
`title_and_abstract.search.exact` for Q3 only: 47 hits. **[syntax]**

First full retrieval (OpenAlex v2/v3, DBLP v2, EGDL v2) — benchmark recall:
OpenAlex Q1 9/24 (B01–B08, B16), Q2 7/24, Q3 2/24, Q4 2/24 (B11, B23), Q5 3/24
(B18, B19, B20). DBLP v2 (title-only, all groups incl. VIS): Q1 4 hits (B16),
Q2 17 hits (B12 B14 B16 B17 B18), Q3 5 hits (B23 B24), Q5 2 hits (B19).
EGDL v2 (phrase render): Q1 11 hits (0/24), Q2 7 hits (B14 B24). Not
retrieved by any search: NodeTrix (B09), DynTrix (B10), Bach et al. (B21),
Sereno et al. (B22). (These DBLP/EGDL v2 raw files were overwritten by later
versions; the counts and matches above are copied from the console output of
that run.)

**v3/v4 across sources (Q1 v3, Q2 v3, Q3 v4, Q3b v3, Q4 v2, Q5 v2).**
Syntax-only changes, OpenAlex/S2/arXiv strings unchanged:
- DBLP is title-only, so the VIS group was dropped (venue restriction already
  ensures visualization/HCI/XR venues) and single-word stems + VR/AR/XR/MR
  acronyms (word-bounded) were used. **[syntax]**
- EGDL (DSpace/Solr) phrase queries in `dc.description.abstract` are broken
  ("multilayer network" → 2 hits vs. 25 for multilayer AND network), so
  multi-word terms are rendered as AND of words within the field. **[syntax]**

**Q6 v1 and Q7 v1 added. [benchmark-informed]** After the first retrieval
missed NodeTrix, DynTrix, Bach et al. and Sereno et al., two queries were
added that correspond to design-space dimensions rather than to individual
titles: Q6 targets the *Network Representation* dimension (matrix and hybrid
representations) for multilayer/dynamic networks (time slices as layers); Q7
targets the AR-specific *Input Modality* / *Interaction Target* values
(tangible, touch, physical objects) for AR visualization of any data. Q6
retrieved DynTrix and Matrix Cubes; Q7 retrieved Butscher, Bach and Sereno
in OpenAlex (966 hits) and Bach and Sereno in DBLP (146 hits). Neither
retrieves NodeTrix (it is neither multilayer nor dynamic); NodeTrix is reached
only by backward snowballing from McGee et al. 2019.

**Q1 v4 / Q6 v2. [precision]** "network of networks" and "interdependent
networks" removed from MLNP: rendered as AND-of-words in EGDL they matched
almost everything (EGDL Q1 v3: 656 hits → v4: 41), and they are
complex-systems terms not used by visualization papers. No benchmark work was
lost. Observation: OpenAlex reported 282 hits for Q1 v4 vs. 269 for Q1 v3
although v4 is strictly narrower; we did not investigate this further (index
update or boolean-evaluation behaviour of very long OR lists) — report the
number actually returned.

**Q3b retired. [precision]** Contributed no benchmark work that Q3 did not
already retrieve, and a random sample of 12 OpenAlex hits contained no
relevant work (stemmed matches on social-network and ANN papers).

**Q7 v2. [precision]** Restricted to visualization/HCI/XR venues (DBLP venue
list, EGDL; ACM/IEEE with publication filters) because the unrestricted
OpenAlex run returned 966 hits, a random sample of which was dominated by AR
applications outside visualization (education, surgery, commerce). Effect:
Butscher et al. is no longer retrieved by Q7 but is still retrieved by Q5
(OpenAlex, S2); Bach and Sereno are retrieved by Q7 in DBLP (and Sereno also
in EGDL).

**Per-source exclusions [syntax].** Semantic Scholar bulk search and the arXiv
API also stem "physicalization" (S2: 319,095 hits even with quotes; arXiv:
32,941), so Q3 is not run on S2 and arXiv. Q7 is venue-restricted and
therefore not run on OpenAlex, S2 or arXiv.

## Final recall of the benchmark (current versions; see output/recall_by_source.csv)

| scope | recall | not retrieved |
|---|---:|---|
| OpenAlex (Q1–Q6) | 20/24 | B09 NodeTrix, B14 GAV-VR, B21 Bach, B22 Sereno |
| Semantic Scholar (Q1, Q2, Q4–Q6) | 20/24 | B05 pymnet, B09, B21, B22 |
| DBLP (titles, venue-restricted, Q1–Q7) | 15/24 | B01–B06 (published outside the listed venues), B09, B13 VRNetzer, B20 |
| arXiv (Q1, Q2, Q4–Q6) | 4/24 | most works have no arXiv version |
| Eurographics DL (Q1–Q7) | 4/24 | only CGF/EG works are in scope (B10, B14, B22, B24 found) |
| **all database searches** | **23/24** | **B09 NodeTrix** |
| snowballing round 1 (5 seed surveys, OpenAlex + S2 + Crossref) | 15/24 | B03 B05 B10 B11 B19 B20 B22 B23 B24 |
| **searches ∪ snowballing R1** | **24/24** | — |

IEEE Xplore and ACM DL have not been run yet (key / manual export needed).


## Run table (generated from raw/run_log.jsonl)

| date | source | query | version | hits reported | retrieved | benchmark recall of this run | matched |
|---|---|---|---|---:|---:|---:|---|
| 2026-11-21 | openalex | Q1 | v1 | 2650 |  | (count only) |  |
| 2026-11-21 | openalex | Q2 | v1 | 3717 |  | (count only) |  |
| 2026-11-21 | openalex | Q3 | v1 | 9061 |  | (count only) |  |
| 2026-11-21 | openalex | Q4 | v1 | 181 |  | (count only) |  |
| 2026-11-21 | openalex | Q1 | v2 | 269 |  | (count only) |  |
| 2026-11-21 | openalex | Q2 | v2 | 888 |  | (count only) |  |
| 2026-11-21 | openalex | Q3 | v2 | 393434 |  | (count only) |  |
| 2026-11-21 | openalex | Q3b | v2 | 437 |  | (count only) |  |
| 2026-11-21 | openalex | Q5 | v1 | 78 |  | (count only) |  |
| 2026-11-21 | openalex | Q3 | v3 | 47 |  | (count only) |  |
| 2026-11-21 | egdl | Q1 | v2 | 11 | 11 | (raw file superseded, see narrative) |  |
| 2026-11-21 | egdl | Q2 | v2 | 7 | 7 | (raw file superseded, see narrative) |  |
| 2026-11-21 | dblp | Q1 | v2 | 4 | 4 | (raw file superseded, see narrative) |  |
| 2026-11-21 | dblp | Q2 | v2 | 17 | 17 | (raw file superseded, see narrative) |  |
| 2026-11-21 | dblp | Q3 | v3 | 5 | 5 | (raw file superseded, see narrative) |  |
| 2026-11-21 | dblp | Q3b | v2 | 1 | 1 | (raw file superseded, see narrative) |  |
| 2026-11-21 | dblp | Q4 | v1 | 0 | 0 | (raw file superseded, see narrative) |  |
| 2026-11-21 | dblp | Q5 | v1 | 2 | 2 | (raw file superseded, see narrative) |  |
| 2026-11-21 | openalex | Q1 | v2 | 269 | 269 | 9/24 | B01 B02 B03 B04 B05 B06 B07 B08 B16 |
| 2026-11-21 | openalex | Q2 | v2 | 888 | 888 | 7/24 | B12 B13 B15 B16 B17 B18 B24 |
| 2026-11-21 | openalex | Q3 | v3 | 47 | 47 | 2/24 | B23 B24 |
| 2026-11-21 | openalex | Q3b | v2 | 437 | 437 | 1/24 | B23 |
| 2026-11-21 | openalex | Q4 | v1 | 181 | 181 | 2/24 | B11 B23 |
| 2026-11-21 | openalex | Q5 | v1 | 78 | 78 | 3/24 | B18 B19 B20 |
| 2026-11-21 | openalex | Q1 | v3 | 269 | 269 | 9/24 | B01 B02 B03 B04 B05 B06 B07 B08 B16 |
| 2026-11-21 | openalex | Q2 | v3 | 888 | 888 | 7/24 | B12 B13 B15 B16 B17 B18 B24 |
| 2026-11-21 | openalex | Q3 | v4 | 47 | 47 | 2/24 | B23 B24 |
| 2026-11-21 | openalex | Q3b | v3 | 437 | 437 | 1/24 | B23 |
| 2026-11-21 | openalex | Q4 | v2 | 181 | 181 | 2/24 | B11 B23 |
| 2026-11-21 | openalex | Q5 | v2 | 78 | 78 | 3/24 | B18 B19 B20 |
| 2026-11-21 | openalex | Q6 | v1 | 190 | 190 | 2/24 | B10 B11 |
| 2026-11-21 | openalex | Q7 | v1 | 966 | 966 | 3/24 | B20 B21 B22 |
| 2026-11-21 | egdl | Q1 | v3 | 656 | 656 | 2/24 | B10 B24 |
| 2026-11-21 | egdl | Q2 | v3 | 89 | 89 | 2/24 | B14 B24 |
| 2026-11-21 | egdl | Q3 | v4 | 213 | 211 | 1/24 | B24 |
| 2026-11-21 | egdl | Q3b | v3 | 12 | 12 | 0/24 |  |
| 2026-11-21 | egdl | Q4 | v2 | 67 | 67 | 0/24 |  |
| 2026-11-21 | egdl | Q5 | v2 | 13 | 13 | 0/24 |  |
| 2026-11-21 | egdl | Q6 | v1 | 105 | 105 | 2/24 | B10 B24 |
| 2026-11-21 | egdl | Q7 | v1 | 59 | 59 | 1/24 | B22 |
| 2026-11-21 | dblp | Q1 | v3 | 8 | 8 | 3/24 | B07 B08 B16 |
| 2026-11-21 | dblp | Q2 | v3 | 128 | 128 | 6/24 | B12 B14 B15 B16 B17 B18 |
| 2026-11-21 | dblp | Q3 | v4 | 4 | 4 | 2/24 | B23 B24 |
| 2026-11-21 | dblp | Q3b | v3 | 18 | 18 | 0/24 |  |
| 2026-11-21 | dblp | Q4 | v2 | 2 | 2 | 1/24 | B23 |
| 2026-11-21 | dblp | Q5 | v2 | 14 | 14 | 1/24 | B19 |
| 2026-11-21 | dblp | Q6 | v1 | 3 | 3 | 2/24 | B10 B11 |
| 2026-11-21 | dblp | Q7 | v1 | 146 | 146 | 2/24 | B21 B22 |
| 2026-11-21 | openalex | Q1 | v4 | 282 | 282 | 9/24 | B01 B02 B03 B04 B05 B06 B07 B08 B16 |
| 2026-11-21 | openalex | Q6 | v2 | 197 | 197 | 2/24 | B10 B11 |
| 2026-11-21 | egdl | Q1 | v4 | 41 | 41 | 0/24 |  |
| 2026-11-21 | egdl | Q6 | v2 | 44 | 44 | 1/24 | B10 |
| 2026-11-21 | dblp | Q1 | v4 | 8 | 8 | 3/24 | B07 B08 B16 |
| 2026-11-21 | dblp | Q6 | v2 | 3 | 3 | 2/24 | B10 B11 |
| 2026-11-21 | s2 | Q1 | v4 | 229 | 229 | 8/24 | B01 B02 B03 B04 B06 B07 B08 B16 |
| 2026-11-21 | s2 | Q2 | v3 | 754 | 754 | 8/24 | B12 B13 B14 B15 B16 B17 B18 B24 |
| 2026-11-21 | dblp | Q7 | v2 | 146 | 146 | 2/24 | B21 B22 |
| 2026-11-21 | egdl | Q7 | v2 | 59 | 59 | 1/24 | B22 |
| 2026-11-21 | s2 | Q1 | v4 | 229 |  | (count only) |  |
| 2026-11-21 | s2 | Q2 | v3 | 754 |  | (count only) |  |
| 2026-11-21 | s2 | Q3 | v4 | 319095 |  | (count only) |  |
| 2026-11-21 | s2 | Q4 | v2 | 129 |  | (count only) |  |
| 2026-11-21 | s2 | Q5 | v2 | 60 |  | (count only) |  |
| 2026-11-21 | s2 | Q6 | v2 | 158 |  | (count only) |  |
| 2026-11-21 | s2 | Q4 | v2 | 129 | 129 | 2/24 | B11 B23 |
| 2026-11-21 | s2 | Q5 | v2 | 60 | 60 | 3/24 | B18 B19 B20 |
| 2026-11-21 | s2 | Q6 | v2 | 158 | 158 | 2/24 | B10 B11 |
| 2026-11-21 | arxiv | Q1 | v4 | 55 | 55 | 2/24 | B01 B16 |
| 2026-11-21 | arxiv | Q2 | v3 | 39 | 39 | 2/24 | B16 B17 |
| 2026-11-21 | arxiv | Q4 | v2 | 37 | 37 | 1/24 | B23 |
| 2026-11-21 | arxiv | Q5 | v2 | 19 | 19 | 0/24 |  |
| 2026-11-21 | arxiv | Q6 | v2 | 21 | 21 | 0/24 |  |
| 2026-11-21 | acm | Q3 | v5 | 10 | 10 | 0/24 |  |
| 2026-11-21 | acm | Q1 | v4 | 8 | 8 | 0/24 |  |
| 2026-11-21 | acm | Q2 | v3 | 39 | 39 | 0/24 |  |
| 2026-11-21 | acm | Q4 | v2 | 4 | 4 | 1/24 | B11 |
| 2026-11-21 | acm | Q5 | v2 | 14 | 14 | 2/24 | B19 B20 |
| 2026-11-21 | acm | Q6 | v2 | 12 | 12 | 1/24 | B11 |
| 2026-11-21 | acm | Q7 | v2 | 85 | 27 | 1/24 | B20 |

## Exact query strings per executed version

**openalex Q1 v1**

```
(multilayer OR "multi-layer" OR multilayered OR "multi-layered" OR multiplex OR "multi-relational" OR multirelational) AND (network OR networks OR graph OR graphs) AND (visualization OR visualisation OR "visual analytics" OR "visual analysis" OR visualizing OR visualising)
```

**openalex Q2 v1**

```
("augmented reality" OR "mixed reality" OR "virtual reality" OR "extended reality" OR immersive OR "head-mounted" OR HoloLens) AND (network OR networks OR graph OR graphs) AND (visualization OR visualisation OR "visual analytics" OR "visual analysis" OR visualizing OR visualising)
```

**openalex Q3 v1**

```
(physicalization OR physicalisation OR "physical visualization" OR tangible OR "3D printed" OR "3D printing") AND (network OR networks OR graph OR graphs) AND (visualization OR visualisation OR "visual analytics" OR "visual analysis" OR visualizing OR visualising)
```

**openalex Q4 v1**

```
("dynamic network" OR "dynamic networks" OR "dynamic graph" OR "dynamic graphs" OR "temporal network" OR "temporal networks" OR "temporal graph" OR "temporal graphs" OR "time-varying network" OR "evolving network") AND (3D OR "three-dimensional" OR 2.5D OR stereoscopic OR "augmented reality" OR "mixed reality" OR "virtual reality" OR "extended reality" OR immersive OR "head-mounted" OR HoloLens OR physicalization OR physicalisation OR "physical visualization" OR tangible OR "3D printed" OR "3D printing") AND (visualization OR visualisation OR "visual analytics" OR "visual analysis" OR visualizing OR visualising)
```

**openalex Q1 v2**

```
("multilayer network" OR "multilayer networks" OR "multi-layer network" OR "multi-layer networks" OR "multilayered network" OR "multilayered networks" OR "multilayer graph" OR "multilayer graphs" OR "multi-layer graph" OR "multiplex network" OR "multiplex networks" OR "multiplex graph" OR "multi-relational network" OR "multi-relational graph" OR "multirelational network" OR "network of networks" OR "interdependent networks") AND (visualization OR visualisation OR "visual analytics" OR "visual analysis" OR visualizing OR visualising)
```

**openalex Q2 v2**

```
("augmented reality" OR "mixed reality" OR "virtual reality" OR "extended reality" OR immersive OR "head-mounted" OR HoloLens) AND ("network visualization" OR "network visualisation" OR "graph visualization" OR "graph visualisation" OR "network analysis" OR "graph analysis" OR "node-link" OR "graph drawing" OR "network data" OR "graph data" OR "network exploration" OR "graph exploration")
```

**openalex Q3 v2**

```
(physicalization OR physicalisation OR "physical visualization" OR "physical visualisation") AND (network OR networks OR graph OR graphs)
```

**openalex Q3b v2**

```
(tangible OR "3D printed" OR "3D printing") AND ("network visualization" OR "network visualisation" OR "graph visualization" OR "graph visualisation" OR "network analysis" OR "graph analysis" OR "node-link" OR "graph drawing" OR "network data" OR "graph data" OR "network exploration" OR "graph exploration")
```

**openalex Q5 v1**

```
("augmented reality" OR "mixed reality" OR HoloLens) AND ("design space" OR "design spaces") AND (visualization OR visualisation OR "visual analytics" OR "visual analysis" OR visualizing OR visualising)
```

**openalex Q3 v3**

```
title_and_abstract.search.exact:(physicalization OR physicalisation OR "physical visualization" OR "physical visualisation") AND (network OR networks OR graph OR graphs)
```

**egdl Q1 v2**

```
(dc.title:("multilayer network" OR "multilayer networks" OR "multi-layer network" OR "multi-layer networks" OR "multilayered network" OR "multilayered networks" OR "multilayer graph" OR "multilayer graphs" OR "multi-layer graph" OR "multiplex network" OR "multiplex networks" OR "multiplex graph" OR "multi-relational network" OR "multi-relational graph" OR "multirelational network" OR "network of networks" OR "interdependent networks") OR dc.description.abstract:("multilayer network" OR "multilayer networks" OR "multi-layer network" OR "multi-layer networks" OR "multilayered network" OR "multilayered networks" OR "multilayer graph" OR "multilayer graphs" OR "multi-layer graph" OR "multiplex network" OR "multiplex networks" OR "multiplex graph" OR "multi-relational network" OR "multi-relational graph" OR "multirelational network" OR "network of networks" OR "interdependent networks") OR dc.subject:("multilayer network" OR "multilayer networks" OR "multi-layer network" OR "multi-layer networks" OR "multilayered network" OR "multilayered networks" OR "multilayer graph" OR "multilayer graphs" OR "multi-layer graph" OR "multiplex network" OR "multiplex networks" OR "multiplex graph" OR "multi-relational network" OR "multi-relational graph" OR "multirelational network" OR "network of networks" OR "interdependent networks")) AND (dc.title:(visualization OR visualisation OR "visual analytics" OR "visual analysis" OR visualizing OR visualising) OR dc.description.abstract:(visualization OR visualisation OR "visual analytics" OR "visual analysis" OR visualizing OR visualising) OR dc.subject:(visualization OR visualisation OR "visual analytics" OR "visual analysis" OR visualizing OR visualising))
```

**egdl Q2 v2**

```
(dc.title:("augmented reality" OR "mixed reality" OR "virtual reality" OR "extended reality" OR immersive OR "head-mounted" OR HoloLens) OR dc.description.abstract:("augmented reality" OR "mixed reality" OR "virtual reality" OR "extended reality" OR immersive OR "head-mounted" OR HoloLens) OR dc.subject:("augmented reality" OR "mixed reality" OR "virtual reality" OR "extended reality" OR immersive OR "head-mounted" OR HoloLens)) AND (dc.title:("network visualization" OR "network visualisation" OR "graph visualization" OR "graph visualisation" OR "network analysis" OR "graph analysis" OR "node-link" OR "graph drawing" OR "network data" OR "graph data" OR "network exploration" OR "graph exploration") OR dc.description.abstract:("network visualization" OR "network visualisation" OR "graph visualization" OR "graph visualisation" OR "network analysis" OR "graph analysis" OR "node-link" OR "graph drawing" OR "network data" OR "graph data" OR "network exploration" OR "graph exploration") OR dc.subject:("network visualization" OR "network visualisation" OR "graph visualization" OR "graph visualisation" OR "network analysis" OR "graph analysis" OR "node-link" OR "graph drawing" OR "network data" OR "graph data" OR "network exploration" OR "graph exploration"))
```

**dblp Q1 v2**

```
(multilayer[- ]network|multilayer[- ]networks|multi[- ]?layer[- ]network|multi[- ]?layer[- ]networks|multilayered[- ]network|multilayered[- ]networks|multilayer[- ]graph|multilayer[- ]graphs|multi[- ]?layer[- ]graph|multiplex[- ]network|multiplex[- ]networks|multiplex[- ]graph|multi[- ]?relational[- ]network|multi[- ]?relational[- ]graph|multirelational[- ]network|network[- ]of[- ]networks|interdependent[- ]networks) AND (visualization|visualisation|visual[- ]analytics|visual[- ]analysis|visualizing|visualising)  [venues: journals/tvcg, journals/cgf, journals/cga, journals/ivs, journals/vi, journals/tochi, journals/pacmhci, conf/visualization, conf/apvis, conf/vissym, conf/eurova, conf/chi, conf/uist, conf/tei, conf/iss, conf/vr, conf/ismar, conf/vrst, conf/sui, conf/egve, conf/ivapp, conf/gd]
```

**dblp Q2 v2**

```
(augmented[- ]reality|mixed[- ]reality|virtual[- ]reality|extended[- ]reality|immersive|head[- ]?mounted|hololens) AND (network[- ]visualization|network[- ]visualisation|graph[- ]visualization|graph[- ]visualisation|network[- ]analysis|graph[- ]analysis|node[- ]?link|graph[- ]drawing|network[- ]data|graph[- ]data|network[- ]exploration|graph[- ]exploration)  [venues: journals/tvcg, journals/cgf, journals/cga, journals/ivs, journals/vi, journals/tochi, journals/pacmhci, conf/visualization, conf/apvis, conf/vissym, conf/eurova, conf/chi, conf/uist, conf/tei, conf/iss, conf/vr, conf/ismar, conf/vrst, conf/sui, conf/egve, conf/ivapp, conf/gd]
```

**dblp Q3 v3**

```
(physicalization|physicalisation|physical[- ]visualization|physical[- ]visualisation) AND (network|networks|graph|graphs)  [venues: journals/tvcg, journals/cgf, journals/cga, journals/ivs, journals/vi, journals/tochi, journals/pacmhci, conf/visualization, conf/apvis, conf/vissym, conf/eurova, conf/chi, conf/uist, conf/tei, conf/iss, conf/vr, conf/ismar, conf/vrst, conf/sui, conf/egve, conf/ivapp, conf/gd]
```

**dblp Q3b v2**

```
(tangible|3d[- ]printed|3d[- ]printing) AND (network[- ]visualization|network[- ]visualisation|graph[- ]visualization|graph[- ]visualisation|network[- ]analysis|graph[- ]analysis|node[- ]?link|graph[- ]drawing|network[- ]data|graph[- ]data|network[- ]exploration|graph[- ]exploration)  [venues: journals/tvcg, journals/cgf, journals/cga, journals/ivs, journals/vi, journals/tochi, journals/pacmhci, conf/visualization, conf/apvis, conf/vissym, conf/eurova, conf/chi, conf/uist, conf/tei, conf/iss, conf/vr, conf/ismar, conf/vrst, conf/sui, conf/egve, conf/ivapp, conf/gd]
```

**dblp Q4 v1**

```
(dynamic[- ]network|dynamic[- ]networks|dynamic[- ]graph|dynamic[- ]graphs|temporal[- ]network|temporal[- ]networks|temporal[- ]graph|temporal[- ]graphs|time[- ]?varying[- ]network|evolving[- ]network) AND (3d|three[- ]?dimensional|2\.5d|stereoscopic|augmented[- ]reality|mixed[- ]reality|virtual[- ]reality|extended[- ]reality|immersive|head[- ]?mounted|hololens|physicalization|physicalisation|physical[- ]visualization|physical[- ]visualisation|tangible|3d[- ]printed|3d[- ]printing) AND (visualization|visualisation|visual[- ]analytics|visual[- ]analysis|visualizing|visualising)  [venues: journals/tvcg, journals/cgf, journals/cga, journals/ivs, journals/vi, journals/tochi, journals/pacmhci, conf/visualization, conf/apvis, conf/vissym, conf/eurova, conf/chi, conf/uist, conf/tei, conf/iss, conf/vr, conf/ismar, conf/vrst, conf/sui, conf/egve, conf/ivapp, conf/gd]
```

**dblp Q5 v1**

```
(augmented[- ]reality|mixed[- ]reality|hololens) AND (design[- ]space|design[- ]spaces) AND (visualization|visualisation|visual[- ]analytics|visual[- ]analysis|visualizing|visualising)  [venues: journals/tvcg, journals/cgf, journals/cga, journals/ivs, journals/vi, journals/tochi, journals/pacmhci, conf/visualization, conf/apvis, conf/vissym, conf/eurova, conf/chi, conf/uist, conf/tei, conf/iss, conf/vr, conf/ismar, conf/vrst, conf/sui, conf/egve, conf/ivapp, conf/gd]
```

**openalex Q1 v3**

```
title_and_abstract.search:("multilayer network" OR "multilayer networks" OR "multi-layer network" OR "multi-layer networks" OR "multilayered network" OR "multilayered networks" OR "multilayer graph" OR "multilayer graphs" OR "multi-layer graph" OR "multiplex network" OR "multiplex networks" OR "multiplex graph" OR "multi-relational network" OR "multi-relational graph" OR "multirelational network" OR "network of networks" OR "interdependent networks") AND (visualization OR visualisation OR "visual analytics" OR "visual analysis" OR visualizing OR visualising)
```

**openalex Q2 v3**

```
title_and_abstract.search:("augmented reality" OR "mixed reality" OR "virtual reality" OR "extended reality" OR immersive OR "head-mounted" OR HoloLens) AND ("network visualization" OR "network visualisation" OR "graph visualization" OR "graph visualisation" OR "network analysis" OR "graph analysis" OR "node-link" OR "graph drawing" OR "network data" OR "graph data" OR "network exploration" OR "graph exploration")
```

**openalex Q3 v4**

```
title_and_abstract.search.exact:(physicalization OR physicalisation OR "physical visualization" OR "physical visualisation") AND (network OR networks OR graph OR graphs)
```

**openalex Q3b v3**

```
title_and_abstract.search:(tangible OR "3D printed" OR "3D printing") AND ("network visualization" OR "network visualisation" OR "graph visualization" OR "graph visualisation" OR "network analysis" OR "graph analysis" OR "node-link" OR "graph drawing" OR "network data" OR "graph data" OR "network exploration" OR "graph exploration")
```

**openalex Q4 v2**

```
title_and_abstract.search:("dynamic network" OR "dynamic networks" OR "dynamic graph" OR "dynamic graphs" OR "temporal network" OR "temporal networks" OR "temporal graph" OR "temporal graphs" OR "time-varying network" OR "evolving network") AND (3D OR "three-dimensional" OR 2.5D OR stereoscopic OR "augmented reality" OR "mixed reality" OR "virtual reality" OR "extended reality" OR immersive OR "head-mounted" OR HoloLens OR physicalization OR physicalisation OR "physical visualization" OR "physical visualisation" OR tangible OR "3D printed" OR "3D printing") AND (visualization OR visualisation OR "visual analytics" OR "visual analysis" OR visualizing OR visualising)
```

**openalex Q5 v2**

```
title_and_abstract.search:("augmented reality" OR "mixed reality" OR HoloLens) AND ("design space" OR "design spaces") AND (visualization OR visualisation OR "visual analytics" OR "visual analysis" OR visualizing OR visualising)
```

**openalex Q6 v1**

```
title_and_abstract.search:("multilayer network" OR "multilayer networks" OR "multi-layer network" OR "multi-layer networks" OR "multilayered network" OR "multilayered networks" OR "multilayer graph" OR "multilayer graphs" OR "multi-layer graph" OR "multiplex network" OR "multiplex networks" OR "multiplex graph" OR "multi-relational network" OR "multi-relational graph" OR "multirelational network" OR "network of networks" OR "interdependent networks" OR "dynamic network" OR "dynamic networks" OR "dynamic graph" OR "dynamic graphs" OR "temporal network" OR "temporal networks" OR "temporal graph" OR "temporal graphs" OR "time-varying network" OR "evolving network") AND (matrix OR matrices OR "adjacency matrix" OR "hybrid representation" OR "hybrid visualization" OR "hybrid visualisation" OR "node-link") AND (visualization OR visualisation OR "visual analytics" OR "visual analysis" OR visualizing OR visualising)
```

**openalex Q7 v1**

```
title_and_abstract.search:("augmented reality" OR "mixed reality" OR HoloLens) AND (tangible OR touch OR "physical object" OR "physical objects" OR "physical referent" OR "physical referents" OR handheld) AND (visualization OR visualisation OR "visual analytics" OR "visual analysis" OR visualizing OR visualising)
```

**egdl Q1 v3**

```
(dc.title:((multilayer AND network) OR (multilayer AND networks) OR (multi AND layer AND network) OR (multi AND layer AND networks) OR (multilayered AND network) OR (multilayered AND networks) OR (multilayer AND graph) OR (multilayer AND graphs) OR (multi AND layer AND graph) OR (multiplex AND network) OR (multiplex AND networks) OR (multiplex AND graph) OR (multi AND relational AND network) OR (multi AND relational AND graph) OR (multirelational AND network) OR (network AND of AND networks) OR (interdependent AND networks)) OR dc.description.abstract:((multilayer AND network) OR (multilayer AND networks) OR (multi AND layer AND network) OR (multi AND layer AND networks) OR (multilayered AND network) OR (multilayered AND networks) OR (multilayer AND graph) OR (multilayer AND graphs) OR (multi AND layer AND graph) OR (multiplex AND network) OR (multiplex AND networks) OR (multiplex AND graph) OR (multi AND relational AND network) OR (multi AND relational AND graph) OR (multirelational AND network) OR (network AND of AND networks) OR (interdependent AND networks)) OR dc.subject:((multilayer AND network) OR (multilayer AND networks) OR (multi AND layer AND network) OR (multi AND layer AND networks) OR (multilayered AND network) OR (multilayered AND networks) OR (multilayer AND graph) OR (multilayer AND graphs) OR (multi AND layer AND graph) OR (multiplex AND network) OR (multiplex AND networks) OR (multiplex AND graph) OR (multi AND relational AND network) OR (multi AND relational AND graph) OR (multirelational AND network) OR (network AND of AND networks) OR (interdependent AND networks))) AND (dc.title:(visualization OR visualisation OR (visual AND analytics) OR (visual AND analysis) OR visualizing OR visualising) OR dc.description.abstract:(visualization OR visualisation OR (visual AND analytics) OR (visual AND analysis) OR visualizing OR visualising) OR dc.subject:(visualization OR visualisation OR (visual AND analytics) OR (visual AND analysis) OR visualizing OR visualising))
```

**egdl Q2 v3**

```
(dc.title:((augmented AND reality) OR (mixed AND reality) OR (virtual AND reality) OR (extended AND reality) OR immersive OR (head AND mounted) OR HoloLens) OR dc.description.abstract:((augmented AND reality) OR (mixed AND reality) OR (virtual AND reality) OR (extended AND reality) OR immersive OR (head AND mounted) OR HoloLens) OR dc.subject:((augmented AND reality) OR (mixed AND reality) OR (virtual AND reality) OR (extended AND reality) OR immersive OR (head AND mounted) OR HoloLens)) AND (dc.title:((network AND visualization) OR (network AND visualisation) OR (graph AND visualization) OR (graph AND visualisation) OR (network AND analysis) OR (graph AND analysis) OR (node AND link) OR (graph AND drawing) OR (network AND data) OR (graph AND data) OR (network AND exploration) OR (graph AND exploration)) OR dc.description.abstract:((network AND visualization) OR (network AND visualisation) OR (graph AND visualization) OR (graph AND visualisation) OR (network AND analysis) OR (graph AND analysis) OR (node AND link) OR (graph AND drawing) OR (network AND data) OR (graph AND data) OR (network AND exploration) OR (graph AND exploration)) OR dc.subject:((network AND visualization) OR (network AND visualisation) OR (graph AND visualization) OR (graph AND visualisation) OR (network AND analysis) OR (graph AND analysis) OR (node AND link) OR (graph AND drawing) OR (network AND data) OR (graph AND data) OR (network AND exploration) OR (graph AND exploration)))
```

**egdl Q3 v4**

```
(dc.title:(physicalization OR physicalisation OR (physical AND visualization) OR (physical AND visualisation)) OR dc.description.abstract:(physicalization OR physicalisation OR (physical AND visualization) OR (physical AND visualisation)) OR dc.subject:(physicalization OR physicalisation OR (physical AND visualization) OR (physical AND visualisation))) AND (dc.title:(network OR networks OR graph OR graphs) OR dc.description.abstract:(network OR networks OR graph OR graphs) OR dc.subject:(network OR networks OR graph OR graphs))
```

**egdl Q3b v3**

```
(dc.title:(tangible OR (3D AND printed) OR (3D AND printing)) OR dc.description.abstract:(tangible OR (3D AND printed) OR (3D AND printing)) OR dc.subject:(tangible OR (3D AND printed) OR (3D AND printing))) AND (dc.title:((network AND visualization) OR (network AND visualisation) OR (graph AND visualization) OR (graph AND visualisation) OR (network AND analysis) OR (graph AND analysis) OR (node AND link) OR (graph AND drawing) OR (network AND data) OR (graph AND data) OR (network AND exploration) OR (graph AND exploration)) OR dc.description.abstract:((network AND visualization) OR (network AND visualisation) OR (graph AND visualization) OR (graph AND visualisation) OR (network AND analysis) OR (graph AND analysis) OR (node AND link) OR (graph AND drawing) OR (network AND data) OR (graph AND data) OR (network AND exploration) OR (graph AND exploration)) OR dc.subject:((network AND visualization) OR (network AND visualisation) OR (graph AND visualization) OR (graph AND visualisation) OR (network AND analysis) OR (graph AND analysis) OR (node AND link) OR (graph AND drawing) OR (network AND data) OR (graph AND data) OR (network AND exploration) OR (graph AND exploration)))
```

**egdl Q4 v2**

```
(dc.title:((dynamic AND network) OR (dynamic AND networks) OR (dynamic AND graph) OR (dynamic AND graphs) OR (temporal AND network) OR (temporal AND networks) OR (temporal AND graph) OR (temporal AND graphs) OR (time AND varying AND network) OR (evolving AND network)) OR dc.description.abstract:((dynamic AND network) OR (dynamic AND networks) OR (dynamic AND graph) OR (dynamic AND graphs) OR (temporal AND network) OR (temporal AND networks) OR (temporal AND graph) OR (temporal AND graphs) OR (time AND varying AND network) OR (evolving AND network)) OR dc.subject:((dynamic AND network) OR (dynamic AND networks) OR (dynamic AND graph) OR (dynamic AND graphs) OR (temporal AND network) OR (temporal AND networks) OR (temporal AND graph) OR (temporal AND graphs) OR (time AND varying AND network) OR (evolving AND network))) AND (dc.title:(3D OR (three AND dimensional) OR 2.5D OR stereoscopic OR (augmented AND reality) OR (mixed AND reality) OR (virtual AND reality) OR (extended AND reality) OR immersive OR (head AND mounted) OR HoloLens OR physicalization OR physicalisation OR (physical AND visualization) OR (physical AND visualisation) OR tangible OR (3D AND printed) OR (3D AND printing)) OR dc.description.abstract:(3D OR (three AND dimensional) OR 2.5D OR stereoscopic OR (augmented AND reality) OR (mixed AND reality) OR (virtual AND reality) OR (extended AND reality) OR immersive OR (head AND mounted) OR HoloLens OR physicalization OR physicalisation OR (physical AND visualization) OR (physical AND visualisation) OR tangible OR (3D AND printed) OR (3D AND printing)) OR dc.subject:(3D OR (three AND dimensional) OR 2.5D OR stereoscopic OR (augmented AND reality) OR (mixed AND reality) OR (virtual AND reality) OR (extended AND reality) OR immersive OR (head AND mounted) OR HoloLens OR physicalization OR physicalisation OR (physical AND visualization) OR (physical AND visualisation) OR tangible OR (3D AND printed) OR (3D AND printing))) AND (dc.title:(visualization OR visualisation OR (visual AND analytics) OR (visual AND analysis) OR visualizing OR visualising) OR dc.description.abstract:(visualization OR visualisation OR (visual AND analytics) OR (visual AND analysis) OR visualizing OR visualising) OR dc.subject:(visualization OR visualisation OR (visual AND analytics) OR (visual AND analysis) OR visualizing OR visualising))
```

**egdl Q5 v2**

```
(dc.title:((augmented AND reality) OR (mixed AND reality) OR HoloLens) OR dc.description.abstract:((augmented AND reality) OR (mixed AND reality) OR HoloLens) OR dc.subject:((augmented AND reality) OR (mixed AND reality) OR HoloLens)) AND (dc.title:((design AND space) OR (design AND spaces)) OR dc.description.abstract:((design AND space) OR (design AND spaces)) OR dc.subject:((design AND space) OR (design AND spaces))) AND (dc.title:(visualization OR visualisation OR (visual AND analytics) OR (visual AND analysis) OR visualizing OR visualising) OR dc.description.abstract:(visualization OR visualisation OR (visual AND analytics) OR (visual AND analysis) OR visualizing OR visualising) OR dc.subject:(visualization OR visualisation OR (visual AND analytics) OR (visual AND analysis) OR visualizing OR visualising))
```

**egdl Q6 v1**

```
(dc.title:((multilayer AND network) OR (multilayer AND networks) OR (multi AND layer AND network) OR (multi AND layer AND networks) OR (multilayered AND network) OR (multilayered AND networks) OR (multilayer AND graph) OR (multilayer AND graphs) OR (multi AND layer AND graph) OR (multiplex AND network) OR (multiplex AND networks) OR (multiplex AND graph) OR (multi AND relational AND network) OR (multi AND relational AND graph) OR (multirelational AND network) OR (network AND of AND networks) OR (interdependent AND networks) OR (dynamic AND network) OR (dynamic AND networks) OR (dynamic AND graph) OR (dynamic AND graphs) OR (temporal AND network) OR (temporal AND networks) OR (temporal AND graph) OR (temporal AND graphs) OR (time AND varying AND network) OR (evolving AND network)) OR dc.description.abstract:((multilayer AND network) OR (multilayer AND networks) OR (multi AND layer AND network) OR (multi AND layer AND networks) OR (multilayered AND network) OR (multilayered AND networks) OR (multilayer AND graph) OR (multilayer AND graphs) OR (multi AND layer AND graph) OR (multiplex AND network) OR (multiplex AND networks) OR (multiplex AND graph) OR (multi AND relational AND network) OR (multi AND relational AND graph) OR (multirelational AND network) OR (network AND of AND networks) OR (interdependent AND networks) OR (dynamic AND network) OR (dynamic AND networks) OR (dynamic AND graph) OR (dynamic AND graphs) OR (temporal AND network) OR (temporal AND networks) OR (temporal AND graph) OR (temporal AND graphs) OR (time AND varying AND network) OR (evolving AND network)) OR dc.subject:((multilayer AND network) OR (multilayer AND networks) OR (multi AND layer AND network) OR (multi AND layer AND networks) OR (multilayered AND network) OR (multilayered AND networks) OR (multilayer AND graph) OR (multilayer AND graphs) OR (multi AND layer AND graph) OR (multiplex AND network) OR (multiplex AND networks) OR (multiplex AND graph) OR (multi AND relational AND network) OR (multi AND relational AND graph) OR (multirelational AND network) OR (network AND of AND networks) OR (interdependent AND networks) OR (dynamic AND network) OR (dynamic AND networks) OR (dynamic AND graph) OR (dynamic AND graphs) OR (temporal AND network) OR (temporal AND networks) OR (temporal AND graph) OR (temporal AND graphs) OR (time AND varying AND network) OR (evolving AND network))) AND (dc.title:(matrix OR matrices OR (adjacency AND matrix) OR (hybrid AND representation) OR (hybrid AND visualization) OR (hybrid AND visualisation) OR (node AND link)) OR dc.description.abstract:(matrix OR matrices OR (adjacency AND matrix) OR (hybrid AND representation) OR (hybrid AND visualization) OR (hybrid AND visualisation) OR (node AND link)) OR dc.subject:(matrix OR matrices OR (adjacency AND matrix) OR (hybrid AND representation) OR (hybrid AND visualization) OR (hybrid AND visualisation) OR (node AND link))) AND (dc.title:(visualization OR visualisation OR (visual AND analytics) OR (visual AND analysis) OR visualizing OR visualising) OR dc.description.abstract:(visualization OR visualisation OR (visual AND analytics) OR (visual AND analysis) OR visualizing OR visualising) OR dc.subject:(visualization OR visualisation OR (visual AND analytics) OR (visual AND analysis) OR visualizing OR visualising))
```

**egdl Q7 v1**

```
(dc.title:((augmented AND reality) OR (mixed AND reality) OR HoloLens) OR dc.description.abstract:((augmented AND reality) OR (mixed AND reality) OR HoloLens) OR dc.subject:((augmented AND reality) OR (mixed AND reality) OR HoloLens)) AND (dc.title:(tangible OR touch OR (physical AND object) OR (physical AND objects) OR (physical AND referent) OR (physical AND referents) OR handheld) OR dc.description.abstract:(tangible OR touch OR (physical AND object) OR (physical AND objects) OR (physical AND referent) OR (physical AND referents) OR handheld) OR dc.subject:(tangible OR touch OR (physical AND object) OR (physical AND objects) OR (physical AND referent) OR (physical AND referents) OR handheld)) AND (dc.title:(visualization OR visualisation OR (visual AND analytics) OR (visual AND analysis) OR visualizing OR visualising) OR dc.description.abstract:(visualization OR visualisation OR (visual AND analytics) OR (visual AND analysis) OR visualizing OR visualising) OR dc.subject:(visualization OR visualisation OR (visual AND analytics) OR (visual AND analysis) OR visualizing OR visualising))
```

**dblp Q1 v3**

```
(\bmultilayer|\bmulti[- ]?layer|\bmultilayered|\bmulti[- ]?layered|\bmultiplex|\bmulti[- ]?relational|\bmultirelational) AND (\bnetwork|\bnetworks|\bgraph|\bgraphs)  [venues: journals/tvcg, journals/cgf, journals/cga, journals/ivs, journals/vi, journals/tochi, journals/pacmhci, conf/visualization, conf/apvis, conf/vissym, conf/eurova, conf/chi, conf/uist, conf/tei, conf/iss, conf/vr, conf/ismar, conf/vrst, conf/sui, conf/egve, conf/ivapp, conf/gd]
```

**dblp Q2 v3**

```
(\baugmented[- ]reality|\bmixed[- ]reality|\bvirtual[- ]reality|\bextended[- ]reality|\bimmersive|\bhead[- ]?mounted|\bhololens|\bvr\b|\bar\b|\bxr\b|\bmr\b) AND (\bnetwork|\bnetworks|\bgraph|\bgraphs)  [venues: journals/tvcg, journals/cgf, journals/cga, journals/ivs, journals/vi, journals/tochi, journals/pacmhci, conf/visualization, conf/apvis, conf/vissym, conf/eurova, conf/chi, conf/uist, conf/tei, conf/iss, conf/vr, conf/ismar, conf/vrst, conf/sui, conf/egve, conf/ivapp, conf/gd]
```

**dblp Q3 v4**

```
(\bphysicalization|\bphysicalisation|\bphysical[- ]visualization|\bphysical[- ]visualisation) AND (\bnetwork|\bnetworks|\bgraph|\bgraphs)  [venues: journals/tvcg, journals/cgf, journals/cga, journals/ivs, journals/vi, journals/tochi, journals/pacmhci, conf/visualization, conf/apvis, conf/vissym, conf/eurova, conf/chi, conf/uist, conf/tei, conf/iss, conf/vr, conf/ismar, conf/vrst, conf/sui, conf/egve, conf/ivapp, conf/gd]
```

**dblp Q3b v3**

```
(\btangible|\b3d[- ]printed|\b3d[- ]printing) AND (\bnetwork|\bnetworks|\bgraph|\bgraphs)  [venues: journals/tvcg, journals/cgf, journals/cga, journals/ivs, journals/vi, journals/tochi, journals/pacmhci, conf/visualization, conf/apvis, conf/vissym, conf/eurova, conf/chi, conf/uist, conf/tei, conf/iss, conf/vr, conf/ismar, conf/vrst, conf/sui, conf/egve, conf/ivapp, conf/gd]
```

**dblp Q4 v2**

```
(\bdynamic[- ]network|\bdynamic[- ]networks|\bdynamic[- ]graph|\bdynamic[- ]graphs|\btemporal[- ]network|\btemporal[- ]networks|\btemporal[- ]graph|\btemporal[- ]graphs|\btime[- ]?varying[- ]network|\bevolving[- ]network) AND (\b3d\b|\bthree[- ]?dimensional|\b2\.5d|\bstereoscopic|\baugmented[- ]reality|\bmixed[- ]reality|\bvirtual[- ]reality|\bextended[- ]reality|\bimmersive|\bhead[- ]?mounted|\bhololens|\bvr\b|\bar\b|\bxr\b|\bmr\b|\bphysicalization|\bphysicalisation|\bphysical[- ]visualization|\bphysical[- ]visualisation|\btangible|\b3d[- ]printed|\b3d[- ]printing)  [venues: journals/tvcg, journals/cgf, journals/cga, journals/ivs, journals/vi, journals/tochi, journals/pacmhci, conf/visualization, conf/apvis, conf/vissym, conf/eurova, conf/chi, conf/uist, conf/tei, conf/iss, conf/vr, conf/ismar, conf/vrst, conf/sui, conf/egve, conf/ivapp, conf/gd]
```

**dblp Q5 v2**

```
(\baugmented[- ]reality|\bmixed[- ]reality|\bhololens|\bvr\b|\bar\b|\bxr\b|\bmr\b) AND (\bdesign[- ]space|\bdesign[- ]spaces)  [venues: journals/tvcg, journals/cgf, journals/cga, journals/ivs, journals/vi, journals/tochi, journals/pacmhci, conf/visualization, conf/apvis, conf/vissym, conf/eurova, conf/chi, conf/uist, conf/tei, conf/iss, conf/vr, conf/ismar, conf/vrst, conf/sui, conf/egve, conf/ivapp, conf/gd]
```

**dblp Q6 v1**

```
(\bmultilayer|\bmulti[- ]?layer|\bmultilayered|\bmulti[- ]?layered|\bmultiplex|\bmulti[- ]?relational|\bmultirelational|\bdynamic[- ]network|\bdynamic[- ]networks|\bdynamic[- ]graph|\bdynamic[- ]graphs|\btemporal[- ]network|\btemporal[- ]networks|\btemporal[- ]graph|\btemporal[- ]graphs|\btime[- ]?varying[- ]network|\bevolving[- ]network) AND (\bmatrix|\bmatrices|\badjacency[- ]matrix|\bhybrid[- ]representation|\bhybrid[- ]visualization|\bhybrid[- ]visualisation|\bnode[- ]?link)  [venues: journals/tvcg, journals/cgf, journals/cga, journals/ivs, journals/vi, journals/tochi, journals/pacmhci, conf/visualization, conf/apvis, conf/vissym, conf/eurova, conf/chi, conf/uist, conf/tei, conf/iss, conf/vr, conf/ismar, conf/vrst, conf/sui, conf/egve, conf/ivapp, conf/gd]
```

**dblp Q7 v1**

```
(\baugmented[- ]reality|\bmixed[- ]reality|\bhololens) AND (\btangible|\btouch|\bphysical[- ]object|\bphysical[- ]objects|\bphysical[- ]referent|\bphysical[- ]referents|\bhandheld)  [venues: journals/tvcg, journals/cgf, journals/cga, journals/ivs, journals/vi, journals/tochi, journals/pacmhci, conf/visualization, conf/apvis, conf/vissym, conf/eurova, conf/chi, conf/uist, conf/tei, conf/iss, conf/vr, conf/ismar, conf/vrst, conf/sui, conf/egve, conf/ivapp, conf/gd]
```

**openalex Q1 v4**

```
title_and_abstract.search:("multilayer network" OR "multilayer networks" OR "multi-layer network" OR "multi-layer networks" OR "multilayered network" OR "multilayered networks" OR "multilayer graph" OR "multilayer graphs" OR "multi-layer graph" OR "multiplex network" OR "multiplex networks" OR "multiplex graph" OR "multi-relational network" OR "multi-relational graph" OR "multirelational network") AND (visualization OR visualisation OR "visual analytics" OR "visual analysis" OR visualizing OR visualising)
```

**openalex Q6 v2**

```
title_and_abstract.search:("multilayer network" OR "multilayer networks" OR "multi-layer network" OR "multi-layer networks" OR "multilayered network" OR "multilayered networks" OR "multilayer graph" OR "multilayer graphs" OR "multi-layer graph" OR "multiplex network" OR "multiplex networks" OR "multiplex graph" OR "multi-relational network" OR "multi-relational graph" OR "multirelational network" OR "dynamic network" OR "dynamic networks" OR "dynamic graph" OR "dynamic graphs" OR "temporal network" OR "temporal networks" OR "temporal graph" OR "temporal graphs" OR "time-varying network" OR "evolving network") AND (matrix OR matrices OR "adjacency matrix" OR "hybrid representation" OR "hybrid visualization" OR "hybrid visualisation" OR "node-link") AND (visualization OR visualisation OR "visual analytics" OR "visual analysis" OR visualizing OR visualising)
```

**egdl Q1 v4**

```
(dc.title:((multilayer AND network) OR (multilayer AND networks) OR (multi AND layer AND network) OR (multi AND layer AND networks) OR (multilayered AND network) OR (multilayered AND networks) OR (multilayer AND graph) OR (multilayer AND graphs) OR (multi AND layer AND graph) OR (multiplex AND network) OR (multiplex AND networks) OR (multiplex AND graph) OR (multi AND relational AND network) OR (multi AND relational AND graph) OR (multirelational AND network)) OR dc.description.abstract:((multilayer AND network) OR (multilayer AND networks) OR (multi AND layer AND network) OR (multi AND layer AND networks) OR (multilayered AND network) OR (multilayered AND networks) OR (multilayer AND graph) OR (multilayer AND graphs) OR (multi AND layer AND graph) OR (multiplex AND network) OR (multiplex AND networks) OR (multiplex AND graph) OR (multi AND relational AND network) OR (multi AND relational AND graph) OR (multirelational AND network)) OR dc.subject:((multilayer AND network) OR (multilayer AND networks) OR (multi AND layer AND network) OR (multi AND layer AND networks) OR (multilayered AND network) OR (multilayered AND networks) OR (multilayer AND graph) OR (multilayer AND graphs) OR (multi AND layer AND graph) OR (multiplex AND network) OR (multiplex AND networks) OR (multiplex AND graph) OR (multi AND relational AND network) OR (multi AND relational AND graph) OR (multirelational AND network))) AND (dc.title:(visualization OR visualisation OR (visual AND analytics) OR (visual AND analysis) OR visualizing OR visualising) OR dc.description.abstract:(visualization OR visualisation OR (visual AND analytics) OR (visual AND analysis) OR visualizing OR visualising) OR dc.subject:(visualization OR visualisation OR (visual AND analytics) OR (visual AND analysis) OR visualizing OR visualising))
```

**egdl Q6 v2**

```
(dc.title:((multilayer AND network) OR (multilayer AND networks) OR (multi AND layer AND network) OR (multi AND layer AND networks) OR (multilayered AND network) OR (multilayered AND networks) OR (multilayer AND graph) OR (multilayer AND graphs) OR (multi AND layer AND graph) OR (multiplex AND network) OR (multiplex AND networks) OR (multiplex AND graph) OR (multi AND relational AND network) OR (multi AND relational AND graph) OR (multirelational AND network) OR (dynamic AND network) OR (dynamic AND networks) OR (dynamic AND graph) OR (dynamic AND graphs) OR (temporal AND network) OR (temporal AND networks) OR (temporal AND graph) OR (temporal AND graphs) OR (time AND varying AND network) OR (evolving AND network)) OR dc.description.abstract:((multilayer AND network) OR (multilayer AND networks) OR (multi AND layer AND network) OR (multi AND layer AND networks) OR (multilayered AND network) OR (multilayered AND networks) OR (multilayer AND graph) OR (multilayer AND graphs) OR (multi AND layer AND graph) OR (multiplex AND network) OR (multiplex AND networks) OR (multiplex AND graph) OR (multi AND relational AND network) OR (multi AND relational AND graph) OR (multirelational AND network) OR (dynamic AND network) OR (dynamic AND networks) OR (dynamic AND graph) OR (dynamic AND graphs) OR (temporal AND network) OR (temporal AND networks) OR (temporal AND graph) OR (temporal AND graphs) OR (time AND varying AND network) OR (evolving AND network)) OR dc.subject:((multilayer AND network) OR (multilayer AND networks) OR (multi AND layer AND network) OR (multi AND layer AND networks) OR (multilayered AND network) OR (multilayered AND networks) OR (multilayer AND graph) OR (multilayer AND graphs) OR (multi AND layer AND graph) OR (multiplex AND network) OR (multiplex AND networks) OR (multiplex AND graph) OR (multi AND relational AND network) OR (multi AND relational AND graph) OR (multirelational AND network) OR (dynamic AND network) OR (dynamic AND networks) OR (dynamic AND graph) OR (dynamic AND graphs) OR (temporal AND network) OR (temporal AND networks) OR (temporal AND graph) OR (temporal AND graphs) OR (time AND varying AND network) OR (evolving AND network))) AND (dc.title:(matrix OR matrices OR (adjacency AND matrix) OR (hybrid AND representation) OR (hybrid AND visualization) OR (hybrid AND visualisation) OR (node AND link)) OR dc.description.abstract:(matrix OR matrices OR (adjacency AND matrix) OR (hybrid AND representation) OR (hybrid AND visualization) OR (hybrid AND visualisation) OR (node AND link)) OR dc.subject:(matrix OR matrices OR (adjacency AND matrix) OR (hybrid AND representation) OR (hybrid AND visualization) OR (hybrid AND visualisation) OR (node AND link))) AND (dc.title:(visualization OR visualisation OR (visual AND analytics) OR (visual AND analysis) OR visualizing OR visualising) OR dc.description.abstract:(visualization OR visualisation OR (visual AND analytics) OR (visual AND analysis) OR visualizing OR visualising) OR dc.subject:(visualization OR visualisation OR (visual AND analytics) OR (visual AND analysis) OR visualizing OR visualising))
```

**dblp Q1 v4**

```
(\bmultilayer|\bmulti[- ]?layer|\bmultilayered|\bmulti[- ]?layered|\bmultiplex|\bmulti[- ]?relational|\bmultirelational) AND (\bnetwork|\bnetworks|\bgraph|\bgraphs)  [venues: journals/tvcg, journals/cgf, journals/cga, journals/ivs, journals/vi, journals/tochi, journals/pacmhci, conf/visualization, conf/apvis, conf/vissym, conf/eurova, conf/chi, conf/uist, conf/tei, conf/iss, conf/vr, conf/ismar, conf/vrst, conf/sui, conf/egve, conf/ivapp, conf/gd]
```

**dblp Q6 v2**

```
(\bmultilayer|\bmulti[- ]?layer|\bmultilayered|\bmulti[- ]?layered|\bmultiplex|\bmulti[- ]?relational|\bmultirelational|\bdynamic[- ]network|\bdynamic[- ]networks|\bdynamic[- ]graph|\bdynamic[- ]graphs|\btemporal[- ]network|\btemporal[- ]networks|\btemporal[- ]graph|\btemporal[- ]graphs|\btime[- ]?varying[- ]network|\bevolving[- ]network) AND (\bmatrix|\bmatrices|\badjacency[- ]matrix|\bhybrid[- ]representation|\bhybrid[- ]visualization|\bhybrid[- ]visualisation|\bnode[- ]?link)  [venues: journals/tvcg, journals/cgf, journals/cga, journals/ivs, journals/vi, journals/tochi, journals/pacmhci, conf/visualization, conf/apvis, conf/vissym, conf/eurova, conf/chi, conf/uist, conf/tei, conf/iss, conf/vr, conf/ismar, conf/vrst, conf/sui, conf/egve, conf/ivapp, conf/gd]
```

**s2 Q1 v4**

```
("multilayer network" | "multilayer networks" | "multi-layer network" | "multi-layer networks" | "multilayered network" | "multilayered networks" | "multilayer graph" | "multilayer graphs" | "multi-layer graph" | "multiplex network" | "multiplex networks" | "multiplex graph" | "multi-relational network" | "multi-relational graph" | "multirelational network") + (visualization | visualisation | "visual analytics" | "visual analysis" | visualizing | visualising)
```

**s2 Q2 v3**

```
("augmented reality" | "mixed reality" | "virtual reality" | "extended reality" | immersive | "head-mounted" | HoloLens) + ("network visualization" | "network visualisation" | "graph visualization" | "graph visualisation" | "network analysis" | "graph analysis" | "node-link" | "graph drawing" | "network data" | "graph data" | "network exploration" | "graph exploration")
```

**dblp Q7 v2**

```
(\baugmented[- ]reality|\bmixed[- ]reality|\bhololens) AND (\btangible|\btouch|\bphysical[- ]object|\bphysical[- ]objects|\bphysical[- ]referent|\bphysical[- ]referents|\bhandheld)  [venues: journals/tvcg, journals/cgf, journals/cga, journals/ivs, journals/vi, journals/tochi, journals/pacmhci, conf/visualization, conf/apvis, conf/vissym, conf/eurova, conf/chi, conf/uist, conf/tei, conf/iss, conf/vr, conf/ismar, conf/vrst, conf/sui, conf/egve, conf/ivapp, conf/gd]
```

**egdl Q7 v2**

```
(dc.title:((augmented AND reality) OR (mixed AND reality) OR HoloLens) OR dc.description.abstract:((augmented AND reality) OR (mixed AND reality) OR HoloLens) OR dc.subject:((augmented AND reality) OR (mixed AND reality) OR HoloLens)) AND (dc.title:(tangible OR touch OR (physical AND object) OR (physical AND objects) OR (physical AND referent) OR (physical AND referents) OR handheld) OR dc.description.abstract:(tangible OR touch OR (physical AND object) OR (physical AND objects) OR (physical AND referent) OR (physical AND referents) OR handheld) OR dc.subject:(tangible OR touch OR (physical AND object) OR (physical AND objects) OR (physical AND referent) OR (physical AND referents) OR handheld)) AND (dc.title:(visualization OR visualisation OR (visual AND analytics) OR (visual AND analysis) OR visualizing OR visualising) OR dc.description.abstract:(visualization OR visualisation OR (visual AND analytics) OR (visual AND analysis) OR visualizing OR visualising) OR dc.subject:(visualization OR visualisation OR (visual AND analytics) OR (visual AND analysis) OR visualizing OR visualising))
```

**s2 Q3 v4**

```
(physicalization | physicalisation | "physical visualization" | "physical visualisation") + (network | networks | graph | graphs)
```

**s2 Q4 v2**

```
("dynamic network" | "dynamic networks" | "dynamic graph" | "dynamic graphs" | "temporal network" | "temporal networks" | "temporal graph" | "temporal graphs" | "time-varying network" | "evolving network") + (3D | "three-dimensional" | 2.5D | stereoscopic | "augmented reality" | "mixed reality" | "virtual reality" | "extended reality" | immersive | "head-mounted" | HoloLens | physicalization | physicalisation | "physical visualization" | "physical visualisation" | tangible | "3D printed" | "3D printing") + (visualization | visualisation | "visual analytics" | "visual analysis" | visualizing | visualising)
```

**s2 Q5 v2**

```
("augmented reality" | "mixed reality" | HoloLens) + ("design space" | "design spaces") + (visualization | visualisation | "visual analytics" | "visual analysis" | visualizing | visualising)
```

**s2 Q6 v2**

```
("multilayer network" | "multilayer networks" | "multi-layer network" | "multi-layer networks" | "multilayered network" | "multilayered networks" | "multilayer graph" | "multilayer graphs" | "multi-layer graph" | "multiplex network" | "multiplex networks" | "multiplex graph" | "multi-relational network" | "multi-relational graph" | "multirelational network" | "dynamic network" | "dynamic networks" | "dynamic graph" | "dynamic graphs" | "temporal network" | "temporal networks" | "temporal graph" | "temporal graphs" | "time-varying network" | "evolving network") + (matrix | matrices | "adjacency matrix" | "hybrid representation" | "hybrid visualization" | "hybrid visualisation" | "node-link") + (visualization | visualisation | "visual analytics" | "visual analysis" | visualizing | visualising)
```

**arxiv Q1 v4**

```
(ti:"multilayer network" OR abs:"multilayer network" OR ti:"multilayer networks" OR abs:"multilayer networks" OR ti:"multi-layer network" OR abs:"multi-layer network" OR ti:"multi-layer networks" OR abs:"multi-layer networks" OR ti:"multilayered network" OR abs:"multilayered network" OR ti:"multilayered networks" OR abs:"multilayered networks" OR ti:"multilayer graph" OR abs:"multilayer graph" OR ti:"multilayer graphs" OR abs:"multilayer graphs" OR ti:"multi-layer graph" OR abs:"multi-layer graph" OR ti:"multiplex network" OR abs:"multiplex network" OR ti:"multiplex networks" OR abs:"multiplex networks" OR ti:"multiplex graph" OR abs:"multiplex graph" OR ti:"multi-relational network" OR abs:"multi-relational network" OR ti:"multi-relational graph" OR abs:"multi-relational graph" OR ti:"multirelational network" OR abs:"multirelational network") AND (ti:visualization OR abs:visualization OR ti:visualisation OR abs:visualisation OR ti:"visual analytics" OR abs:"visual analytics" OR ti:"visual analysis" OR abs:"visual analysis" OR ti:visualizing OR abs:visualizing OR ti:visualising OR abs:visualising)
```

**arxiv Q2 v3**

```
(ti:"augmented reality" OR abs:"augmented reality" OR ti:"mixed reality" OR abs:"mixed reality" OR ti:"virtual reality" OR abs:"virtual reality" OR ti:"extended reality" OR abs:"extended reality" OR ti:immersive OR abs:immersive OR ti:"head-mounted" OR abs:"head-mounted" OR ti:HoloLens OR abs:HoloLens) AND (ti:"network visualization" OR abs:"network visualization" OR ti:"network visualisation" OR abs:"network visualisation" OR ti:"graph visualization" OR abs:"graph visualization" OR ti:"graph visualisation" OR abs:"graph visualisation" OR ti:"network analysis" OR abs:"network analysis" OR ti:"graph analysis" OR abs:"graph analysis" OR ti:"node-link" OR abs:"node-link" OR ti:"graph drawing" OR abs:"graph drawing" OR ti:"network data" OR abs:"network data" OR ti:"graph data" OR abs:"graph data" OR ti:"network exploration" OR abs:"network exploration" OR ti:"graph exploration" OR abs:"graph exploration")
```

**arxiv Q4 v2**

```
(ti:"dynamic network" OR abs:"dynamic network" OR ti:"dynamic networks" OR abs:"dynamic networks" OR ti:"dynamic graph" OR abs:"dynamic graph" OR ti:"dynamic graphs" OR abs:"dynamic graphs" OR ti:"temporal network" OR abs:"temporal network" OR ti:"temporal networks" OR abs:"temporal networks" OR ti:"temporal graph" OR abs:"temporal graph" OR ti:"temporal graphs" OR abs:"temporal graphs" OR ti:"time-varying network" OR abs:"time-varying network" OR ti:"evolving network" OR abs:"evolving network") AND (ti:3D OR abs:3D OR ti:"three-dimensional" OR abs:"three-dimensional" OR ti:2.5D OR abs:2.5D OR ti:stereoscopic OR abs:stereoscopic OR ti:"augmented reality" OR abs:"augmented reality" OR ti:"mixed reality" OR abs:"mixed reality" OR ti:"virtual reality" OR abs:"virtual reality" OR ti:"extended reality" OR abs:"extended reality" OR ti:immersive OR abs:immersive OR ti:"head-mounted" OR abs:"head-mounted" OR ti:HoloLens OR abs:HoloLens OR ti:physicalization OR abs:physicalization OR ti:physicalisation OR abs:physicalisation OR ti:"physical visualization" OR abs:"physical visualization" OR ti:"physical visualisation" OR abs:"physical visualisation" OR ti:tangible OR abs:tangible OR ti:"3D printed" OR abs:"3D printed" OR ti:"3D printing" OR abs:"3D printing") AND (ti:visualization OR abs:visualization OR ti:visualisation OR abs:visualisation OR ti:"visual analytics" OR abs:"visual analytics" OR ti:"visual analysis" OR abs:"visual analysis" OR ti:visualizing OR abs:visualizing OR ti:visualising OR abs:visualising)
```

**arxiv Q5 v2**

```
(ti:"augmented reality" OR abs:"augmented reality" OR ti:"mixed reality" OR abs:"mixed reality" OR ti:HoloLens OR abs:HoloLens) AND (ti:"design space" OR abs:"design space" OR ti:"design spaces" OR abs:"design spaces") AND (ti:visualization OR abs:visualization OR ti:visualisation OR abs:visualisation OR ti:"visual analytics" OR abs:"visual analytics" OR ti:"visual analysis" OR abs:"visual analysis" OR ti:visualizing OR abs:visualizing OR ti:visualising OR abs:visualising)
```

**arxiv Q6 v2**

```
(ti:"multilayer network" OR abs:"multilayer network" OR ti:"multilayer networks" OR abs:"multilayer networks" OR ti:"multi-layer network" OR abs:"multi-layer network" OR ti:"multi-layer networks" OR abs:"multi-layer networks" OR ti:"multilayered network" OR abs:"multilayered network" OR ti:"multilayered networks" OR abs:"multilayered networks" OR ti:"multilayer graph" OR abs:"multilayer graph" OR ti:"multilayer graphs" OR abs:"multilayer graphs" OR ti:"multi-layer graph" OR abs:"multi-layer graph" OR ti:"multiplex network" OR abs:"multiplex network" OR ti:"multiplex networks" OR abs:"multiplex networks" OR ti:"multiplex graph" OR abs:"multiplex graph" OR ti:"multi-relational network" OR abs:"multi-relational network" OR ti:"multi-relational graph" OR abs:"multi-relational graph" OR ti:"multirelational network" OR abs:"multirelational network" OR ti:"dynamic network" OR abs:"dynamic network" OR ti:"dynamic networks" OR abs:"dynamic networks" OR ti:"dynamic graph" OR abs:"dynamic graph" OR ti:"dynamic graphs" OR abs:"dynamic graphs" OR ti:"temporal network" OR abs:"temporal network" OR ti:"temporal networks" OR abs:"temporal networks" OR ti:"temporal graph" OR abs:"temporal graph" OR ti:"temporal graphs" OR abs:"temporal graphs" OR ti:"time-varying network" OR abs:"time-varying network" OR ti:"evolving network" OR abs:"evolving network") AND (ti:matrix OR abs:matrix OR ti:matrices OR abs:matrices OR ti:"adjacency matrix" OR abs:"adjacency matrix" OR ti:"hybrid representation" OR abs:"hybrid representation" OR ti:"hybrid visualization" OR abs:"hybrid visualization" OR ti:"hybrid visualisation" OR abs:"hybrid visualisation" OR ti:"node-link" OR abs:"node-link") AND (ti:visualization OR abs:visualization OR ti:visualisation OR abs:visualisation OR ti:"visual analytics" OR abs:"visual analytics" OR ti:"visual analysis" OR abs:"visual analysis" OR ti:visualizing OR abs:visualizing OR ti:visualising OR abs:visualising)
```

**acm Q3 v5**

```
manual export: exports/acm/Q3_v5_results.csv
```

**acm Q1 v4**

```
manual export: exports/acm/Q1_v4_results.csv
```

**acm Q2 v3**

```
manual export: exports/acm/Q2_v3_results.csv
```

**acm Q4 v2**

```
manual export: exports/acm/Q4_v2_results.csv
```

**acm Q5 v2**

```
manual export: exports/acm/Q5_v2_results.csv
```

**acm Q6 v2**

```
manual export: exports/acm/Q6_v2_results.csv
```

**acm Q7 v2**

```
manual export: exports/acm/Q7_v2_results.csv
```

## IEEE Xplore (added 2026-11-24, Metadata API)

Run on 2026-11-24 after the API key was activated. The 25-term limit assumed in querybuild.py was tested and does not exist in the API; the sub-query split was kept (logically equivalent; for every query the unique records equal the hits of the unsplit query). Hits reported = sum of sub-query hits (a work can match several sub-queries). Recall uses the current benchmark of 28 works (config/benchmark.csv), unlike the rows above, which used the 24-work benchmark. Merged into the corpus with scripts/merge_ieee_incremental.py (see output/prisma_counts_IEEE.json).

| date | source | query | version | hits reported | retrieved | benchmark recall of this run | matched |
|---|---|---|---|---:|---:|---:|---|
| 2026-11-24 | ieee | Q1 | v4 | 36 | 36 | 5/28 | B01 B06 B07 B08 B16 |
| 2026-11-24 | ieee | Q2 | v3 | 157 | 157 | 4/28 | B12 B15 B17 B18 |
| 2026-11-24 | ieee | Q3 | v4 | 3 | 3 | 0/28 |  |
| 2026-11-24 | ieee | Q4 | v2 | 26 | 26 | 0/28 |  |
| 2026-11-24 | ieee | Q5 | v2 | 18 | 18 | 1/28 | B18 |
| 2026-11-24 | ieee | Q6 | v2 | 58 | 58 | 0/28 |  |
| 2026-11-24 | ieee | Q7 | v2 | 188 | 86 | 1/28 | B25 |

### Exact IEEE query strings (sub-queries joined by UNION)

**ieee Q1 v4**

```
("Document Title":"multilayer network" OR "Abstract":"multilayer network" OR "Document Title":"multilayer networks" OR "Abstract":"multilayer networks" OR "Document Title":"multi-layer network" OR "Abstract":"multi-layer network" OR "Document Title":"multi-layer networks" OR "Abstract":"multi-layer networks") AND ("Document Title":visualization OR "Abstract":visualization OR "Document Title":visualisation OR "Abstract":visualisation OR "Document Title":"visual analytics" OR "Abstract":"visual analytics" OR "Document Title":"visual analysis" OR "Abstract":"visual analysis" OR "Document Title":visualizing OR "Abstract":visualizing OR "Document Title":visualising OR "Abstract":visualising)  UNION  ("Document Title":"multilayered network" OR "Abstract":"multilayered network" OR "Document Title":"multilayered networks" OR "Abstract":"multilayered networks" OR "Document Title":"multilayer graph" OR "Abstract":"multilayer graph" OR "Document Title":"multilayer graphs" OR "Abstract":"multilayer graphs") AND ("Document Title":visualization OR "Abstract":visualization OR "Document Title":visualisation OR "Abstract":visualisation OR "Document Title":"visual analytics" OR "Abstract":"visual analytics" OR "Document Title":"visual analysis" OR "Abstract":"visual analysis" OR "Document Title":visualizing OR "Abstract":visualizing OR "Document Title":visualising OR "Abstract":visualising)  UNION  ("Document Title":"multi-layer graph" OR "Abstract":"multi-layer graph" OR "Document Title":"multiplex network" OR "Abstract":"multiplex network" OR "Document Title":"multiplex networks" OR "Abstract":"multiplex networks" OR "Document Title":"multiplex graph" OR "Abstract":"multiplex graph") AND ("Document Title":visualization OR "Abstract":visualization OR "Document Title":visualisation OR "Abstract":visualisation OR "Document Title":"visual analytics" OR "Abstract":"visual analytics" OR "Document Title":"visual analysis" OR "Abstract":"visual analysis" OR "Document Title":visualizing OR "Abstract":visualizing OR "Document Title":visualising OR "Abstract":visualising)  UNION  ("Document Title":"multi-relational network" OR "Abstract":"multi-relational network" OR "Document Title":"multi-relational graph" OR "Abstract":"multi-relational graph" OR "Document Title":"multirelational network" OR "Abstract":"multirelational network") AND ("Document Title":visualization OR "Abstract":visualization OR "Document Title":visualisation OR "Abstract":visualisation OR "Document Title":"visual analytics" OR "Abstract":"visual analytics" OR "Document Title":"visual analysis" OR "Abstract":"visual analysis" OR "Document Title":visualizing OR "Abstract":visualizing OR "Document Title":visualising OR "Abstract":visualising)
```

**ieee Q2 v3**

```
("Document Title":"augmented reality" OR "Abstract":"augmented reality" OR "Document Title":"mixed reality" OR "Abstract":"mixed reality" OR "Document Title":"virtual reality" OR "Abstract":"virtual reality" OR "Document Title":"extended reality" OR "Abstract":"extended reality") AND ("Document Title":"network visualization" OR "Abstract":"network visualization" OR "Document Title":"network visualisation" OR "Abstract":"network visualisation" OR "Document Title":"graph visualization" OR "Abstract":"graph visualization" OR "Document Title":"graph visualisation" OR "Abstract":"graph visualisation" OR "Document Title":"network analysis" OR "Abstract":"network analysis" OR "Document Title":"graph analysis" OR "Abstract":"graph analysis")  UNION  ("Document Title":immersive OR "Abstract":immersive OR "Document Title":"head-mounted" OR "Abstract":"head-mounted" OR "Document Title":HoloLens OR "Abstract":HoloLens) AND ("Document Title":"network visualization" OR "Abstract":"network visualization" OR "Document Title":"network visualisation" OR "Abstract":"network visualisation" OR "Document Title":"graph visualization" OR "Abstract":"graph visualization" OR "Document Title":"graph visualisation" OR "Abstract":"graph visualisation" OR "Document Title":"network analysis" OR "Abstract":"network analysis" OR "Document Title":"graph analysis" OR "Abstract":"graph analysis")  UNION  ("Document Title":"augmented reality" OR "Abstract":"augmented reality" OR "Document Title":"mixed reality" OR "Abstract":"mixed reality" OR "Document Title":"virtual reality" OR "Abstract":"virtual reality" OR "Document Title":"extended reality" OR "Abstract":"extended reality") AND ("Document Title":"node-link" OR "Abstract":"node-link" OR "Document Title":"graph drawing" OR "Abstract":"graph drawing" OR "Document Title":"network data" OR "Abstract":"network data" OR "Document Title":"graph data" OR "Abstract":"graph data" OR "Document Title":"network exploration" OR "Abstract":"network exploration" OR "Document Title":"graph exploration" OR "Abstract":"graph exploration")  UNION  ("Document Title":immersive OR "Abstract":immersive OR "Document Title":"head-mounted" OR "Abstract":"head-mounted" OR "Document Title":HoloLens OR "Abstract":HoloLens) AND ("Document Title":"node-link" OR "Abstract":"node-link" OR "Document Title":"graph drawing" OR "Abstract":"graph drawing" OR "Document Title":"network data" OR "Abstract":"network data" OR "Document Title":"graph data" OR "Abstract":"graph data" OR "Document Title":"network exploration" OR "Abstract":"network exploration" OR "Document Title":"graph exploration" OR "Abstract":"graph exploration")
```

**ieee Q3 v4**

```
("Document Title":physicalization OR "Abstract":physicalization OR "Document Title":physicalisation OR "Abstract":physicalisation OR "Document Title":"physical visualization" OR "Abstract":"physical visualization" OR "Document Title":"physical visualisation" OR "Abstract":"physical visualisation") AND ("Document Title":network OR "Abstract":network OR "Document Title":networks OR "Abstract":networks OR "Document Title":graph OR "Abstract":graph OR "Document Title":graphs OR "Abstract":graphs)
```

**ieee Q4 v2**

```
("Document Title":"dynamic network" OR "Abstract":"dynamic network" OR "Document Title":"dynamic networks" OR "Abstract":"dynamic networks" OR "Document Title":"dynamic graph" OR "Abstract":"dynamic graph") AND ("Document Title":3D OR "Abstract":3D OR "Document Title":"three-dimensional" OR "Abstract":"three-dimensional" OR "Document Title":2.5D OR "Abstract":2.5D OR "Document Title":stereoscopic OR "Abstract":stereoscopic OR "Document Title":"augmented reality" OR "Abstract":"augmented reality") AND ("Document Title":visualization OR "Abstract":visualization OR "Document Title":visualisation OR "Abstract":visualisation OR "Document Title":"visual analytics" OR "Abstract":"visual analytics")  UNION  ("Document Title":"dynamic graphs" OR "Abstract":"dynamic graphs" OR "Document Title":"temporal network" OR "Abstract":"temporal network") AND ("Document Title":3D OR "Abstract":3D OR "Document Title":"three-dimensional" OR "Abstract":"three-dimensional" OR "Document Title":2.5D OR "Abstract":2.5D OR "Document Title":stereoscopic OR "Abstract":stereoscopic OR "Document Title":"augmented reality" OR "Abstract":"augmented reality") AND ("Document Title":visualization OR "Abstract":visualization OR "Document Title":visualisation OR "Abstract":visualisation OR "Document Title":"visual analytics" OR "Abstract":"visual analytics")  UNION  ("Document Title":"dynamic network" OR "Abstract":"dynamic network" OR "Document Title":"dynamic networks" OR "Abstract":"dynamic networks" OR "Document Title":"dynamic graph" OR "Abstract":"dynamic graph") AND ("Document Title":3D OR "Abstract":3D OR "Document Title":"three-dimensional" OR "Abstract":"three-dimensional" OR "Document Title":2.5D OR "Abstract":2.5D OR "Document Title":stereoscopic OR "Abstract":stereoscopic OR "Document Title":"augmented reality" OR "Abstract":"augmented reality") AND ("Document Title":"visual analysis" OR "Abstract":"visual analysis" OR "Document Title":visualizing OR "Abstract":visualizing OR "Document Title":visualising OR "Abstract":visualising)  UNION  ("Document Title":"dynamic graphs" OR "Abstract":"dynamic graphs" OR "Document Title":"temporal network" OR "Abstract":"temporal network") AND ("Document Title":3D OR "Abstract":3D OR "Document Title":"three-dimensional" OR "Abstract":"three-dimensional" OR "Document Title":2.5D OR "Abstract":2.5D OR "Document Title":stereoscopic OR "Abstract":stereoscopic OR "Document Title":"augmented reality" OR "Abstract":"augmented reality") AND ("Document Title":"visual analysis" OR "Abstract":"visual analysis" OR "Document Title":visualizing OR "Abstract":visualizing OR "Document Title":visualising OR "Abstract":visualising)  UNION  ("Document Title":"dynamic network" OR "Abstract":"dynamic network" OR "Document Title":"dynamic networks" OR "Abstract":"dynamic networks" OR "Document Title":"dynamic graph" OR "Abstract":"dynamic graph" OR "Document Title":"dynamic graphs" OR "Abstract":"dynamic graphs" OR "Document Title":"temporal network" OR "Abstract":"temporal network") AND ("Document Title":"mixed reality" OR "Abstract":"mixed reality" OR "Document Title":"virtual reality" OR "Abstract":"virtual reality" OR "Document Title":"extended reality" OR "Abstract":"extended reality" OR "Document Title":immersive OR "Abstract":immersive) AND ("Document Title":visualization OR "Abstract":visualization OR "Document Title":visualisation OR "Abstract":visualisation OR "Document Title":"visual analytics" OR "Abstract":"visual analytics")  UNION  ("Document Title":"dynamic network" OR "Abstract":"dynamic network" OR "Document Title":"dynamic networks" OR "Abstract":"dynamic networks" OR "Document Title":"dynamic graph" OR "Abstract":"dynamic graph" OR "Document Title":"dynamic graphs" OR "Abstract":"dynamic graphs" OR "Document Title":"temporal network" OR "Abstract":"temporal network") AND ("Document Title":"mixed reality" OR "Abstract":"mixed reality" OR "Document Title":"virtual reality" OR "Abstract":"virtual reality" OR "Document Title":"extended reality" OR "Abstract":"extended reality" OR "Document Title":immersive OR "Abstract":immersive) AND ("Document Title":"visual analysis" OR "Abstract":"visual analysis" OR "Document Title":visualizing OR "Abstract":visualizing OR "Document Title":visualising OR "Abstract":visualising)  UNION  ("Document Title":"temporal networks" OR "Abstract":"temporal networks" OR "Document Title":"temporal graph" OR "Abstract":"temporal graph" OR "Document Title":"temporal graphs" OR "Abstract":"temporal graphs") AND ("Document Title":3D OR "Abstract":3D OR "Document Title":"three-dimensional" OR "Abstract":"three-dimensional" OR "Document Title":2.5D OR "Abstract":2.5D OR "Document Title":stereoscopic OR "Abstract":stereoscopic OR "Document Title":"augmented reality" OR "Abstract":"augmented reality") AND ("Document Title":visualization OR "Abstract":visualization OR "Document Title":visualisation OR "Abstract":visualisation OR "Document Title":"visual analytics" OR "Abstract":"visual analytics")  UNION  ("Document Title":"time-varying network" OR "Abstract":"time-varying network" OR "Document Title":"evolving network" OR "Abstract":"evolving network") AND ("Document Title":3D OR "Abstract":3D OR "Document Title":"three-dimensional" OR "Abstract":"three-dimensional" OR "Document Title":2.5D OR "Abstract":2.5D OR "Document Title":stereoscopic OR "Abstract":stereoscopic OR "Document Title":"augmented reality" OR "Abstract":"augmented reality") AND ("Document Title":visualization OR "Abstract":visualization OR "Document Title":visualisation OR "Abstract":visualisation OR "Document Title":"visual analytics" OR "Abstract":"visual analytics")  UNION  ("Document Title":"temporal networks" OR "Abstract":"temporal networks" OR "Document Title":"temporal graph" OR "Abstract":"temporal graph" OR "Document Title":"temporal graphs" OR "Abstract":"temporal graphs") AND ("Document Title":3D OR "Abstract":3D OR "Document Title":"three-dimensional" OR "Abstract":"three-dimensional" OR "Document Title":2.5D OR "Abstract":2.5D OR "Document Title":stereoscopic OR "Abstract":stereoscopic OR "Document Title":"augmented reality" OR "Abstract":"augmented reality") AND ("Document Title":"visual analysis" OR "Abstract":"visual analysis" OR "Document Title":visualizing OR "Abstract":visualizing OR "Document Title":visualising OR "Abstract":visualising)  UNION  ("Document Title":"time-varying network" OR "Abstract":"time-varying network" OR "Document Title":"evolving network" OR "Abstract":"evolving network") AND ("Document Title":3D OR "Abstract":3D OR "Document Title":"three-dimensional" OR "Abstract":"three-dimensional" OR "Document Title":2.5D OR "Abstract":2.5D OR "Document Title":stereoscopic OR "Abstract":stereoscopic OR "Document Title":"augmented reality" OR "Abstract":"augmented reality") AND ("Document Title":"visual analysis" OR "Abstract":"visual analysis" OR "Document Title":visualizing OR "Abstract":visualizing OR "Document Title":visualising OR "Abstract":visualising)  UNION  ("Document Title":"temporal networks" OR "Abstract":"temporal networks" OR "Document Title":"temporal graph" OR "Abstract":"temporal graph" OR "Document Title":"temporal graphs" OR "Abstract":"temporal graphs" OR "Document Title":"time-varying network" OR "Abstract":"time-varying network" OR "Document Title":"evolving network" OR "Abstract":"evolving network") AND ("Document Title":"mixed reality" OR "Abstract":"mixed reality" OR "Document Title":"virtual reality" OR "Abstract":"virtual reality" OR "Document Title":"extended reality" OR "Abstract":"extended reality" OR "Document Title":immersive OR "Abstract":immersive) AND ("Document Title":visualization OR "Abstract":visualization OR "Document Title":visualisation OR "Abstract":visualisation OR "Document Title":"visual analytics" OR "Abstract":"visual analytics")  UNION  ("Document Title":"temporal networks" OR "Abstract":"temporal networks" OR "Document Title":"temporal graph" OR "Abstract":"temporal graph" OR "Document Title":"temporal graphs" OR "Abstract":"temporal graphs" OR "Document Title":"time-varying network" OR "Abstract":"time-varying network" OR "Document Title":"evolving network" OR "Abstract":"evolving network") AND ("Document Title":"mixed reality" OR "Abstract":"mixed reality" OR "Document Title":"virtual reality" OR "Abstract":"virtual reality" OR "Document Title":"extended reality" OR "Abstract":"extended reality" OR "Document Title":immersive OR "Abstract":immersive) AND ("Document Title":"visual analysis" OR "Abstract":"visual analysis" OR "Document Title":visualizing OR "Abstract":visualizing OR "Document Title":visualising OR "Abstract":visualising)  UNION  ("Document Title":"dynamic network" OR "Abstract":"dynamic network" OR "Document Title":"dynamic networks" OR "Abstract":"dynamic networks" OR "Document Title":"dynamic graph" OR "Abstract":"dynamic graph") AND ("Document Title":"head-mounted" OR "Abstract":"head-mounted" OR "Document Title":HoloLens OR "Abstract":HoloLens OR "Document Title":physicalization OR "Abstract":physicalization OR "Document Title":physicalisation OR "Abstract":physicalisation OR "Document Title":"physical visualization" OR "Abstract":"physical visualization") AND ("Document Title":visualization OR "Abstract":visualization OR "Document Title":visualisation OR "Abstract":visualisation OR "Document Title":"visual analytics" OR "Abstract":"visual analytics")  UNION  ("Document Title":"dynamic graphs" OR "Abstract":"dynamic graphs" OR "Document Title":"temporal network" OR "Abstract":"temporal network") AND ("Document Title":"head-mounted" OR "Abstract":"head-mounted" OR "Document Title":HoloLens OR "Abstract":HoloLens OR "Document Title":physicalization OR "Abstract":physicalization OR "Document Title":physicalisation OR "Abstract":physicalisation OR "Document Title":"physical visualization" OR "Abstract":"physical visualization") AND ("Document Title":visualization OR "Abstract":visualization OR "Document Title":visualisation OR "Abstract":visualisation OR "Document Title":"visual analytics" OR "Abstract":"visual analytics")  UNION  ("Document Title":"dynamic network" OR "Abstract":"dynamic network" OR "Document Title":"dynamic networks" OR "Abstract":"dynamic networks" OR "Document Title":"dynamic graph" OR "Abstract":"dynamic graph") AND ("Document Title":"head-mounted" OR "Abstract":"head-mounted" OR "Document Title":HoloLens OR "Abstract":HoloLens OR "Document Title":physicalization OR "Abstract":physicalization OR "Document Title":physicalisation OR "Abstract":physicalisation OR "Document Title":"physical visualization" OR "Abstract":"physical visualization") AND ("Document Title":"visual analysis" OR "Abstract":"visual analysis" OR "Document Title":visualizing OR "Abstract":visualizing OR "Document Title":visualising OR "Abstract":visualising)  UNION  ("Document Title":"dynamic graphs" OR "Abstract":"dynamic graphs" OR "Document Title":"temporal network" OR "Abstract":"temporal network") AND ("Document Title":"head-mounted" OR "Abstract":"head-mounted" OR "Document Title":HoloLens OR "Abstract":HoloLens OR "Document Title":physicalization OR "Abstract":physicalization OR "Document Title":physicalisation OR "Abstract":physicalisation OR "Document Title":"physical visualization" OR "Abstract":"physical visualization") AND ("Document Title":"visual analysis" OR "Abstract":"visual analysis" OR "Document Title":visualizing OR "Abstract":visualizing OR "Document Title":visualising OR "Abstract":visualising)  UNION  ("Document Title":"dynamic network" OR "Abstract":"dynamic network" OR "Document Title":"dynamic networks" OR "Abstract":"dynamic networks" OR "Document Title":"dynamic graph" OR "Abstract":"dynamic graph" OR "Document Title":"dynamic graphs" OR "Abstract":"dynamic graphs" OR "Document Title":"temporal network" OR "Abstract":"temporal network") AND ("Document Title":"physical visualisation" OR "Abstract":"physical visualisation" OR "Document Title":tangible OR "Abstract":tangible OR "Document Title":"3D printed" OR "Abstract":"3D printed" OR "Document Title":"3D printing" OR "Abstract":"3D printing") AND ("Document Title":visualization OR "Abstract":visualization OR "Document Title":visualisation OR "Abstract":visualisation OR "Document Title":"visual analytics" OR "Abstract":"visual analytics")  UNION  ("Document Title":"dynamic network" OR "Abstract":"dynamic network" OR "Document Title":"dynamic networks" OR "Abstract":"dynamic networks" OR "Document Title":"dynamic graph" OR "Abstract":"dynamic graph" OR "Document Title":"dynamic graphs" OR "Abstract":"dynamic graphs" OR "Document Title":"temporal network" OR "Abstract":"temporal network") AND ("Document Title":"physical visualisation" OR "Abstract":"physical visualisation" OR "Document Title":tangible OR "Abstract":tangible OR "Document Title":"3D printed" OR "Abstract":"3D printed" OR "Document Title":"3D printing" OR "Abstract":"3D printing") AND ("Document Title":"visual analysis" OR "Abstract":"visual analysis" OR "Document Title":visualizing OR "Abstract":visualizing OR "Document Title":visualising OR "Abstract":visualising)  UNION  ("Document Title":"temporal networks" OR "Abstract":"temporal networks" OR "Document Title":"temporal graph" OR "Abstract":"temporal graph" OR "Document Title":"temporal graphs" OR "Abstract":"temporal graphs") AND ("Document Title":"head-mounted" OR "Abstract":"head-mounted" OR "Document Title":HoloLens OR "Abstract":HoloLens OR "Document Title":physicalization OR "Abstract":physicalization OR "Document Title":physicalisation OR "Abstract":physicalisation OR "Document Title":"physical visualization" OR "Abstract":"physical visualization") AND ("Document Title":visualization OR "Abstract":visualization OR "Document Title":visualisation OR "Abstract":visualisation OR "Document Title":"visual analytics" OR "Abstract":"visual analytics")  UNION  ("Document Title":"time-varying network" OR "Abstract":"time-varying network" OR "Document Title":"evolving network" OR "Abstract":"evolving network") AND ("Document Title":"head-mounted" OR "Abstract":"head-mounted" OR "Document Title":HoloLens OR "Abstract":HoloLens OR "Document Title":physicalization OR "Abstract":physicalization OR "Document Title":physicalisation OR "Abstract":physicalisation OR "Document Title":"physical visualization" OR "Abstract":"physical visualization") AND ("Document Title":visualization OR "Abstract":visualization OR "Document Title":visualisation OR "Abstract":visualisation OR "Document Title":"visual analytics" OR "Abstract":"visual analytics")  UNION  ("Document Title":"temporal networks" OR "Abstract":"temporal networks" OR "Document Title":"temporal graph" OR "Abstract":"temporal graph" OR "Document Title":"temporal graphs" OR "Abstract":"temporal graphs") AND ("Document Title":"head-mounted" OR "Abstract":"head-mounted" OR "Document Title":HoloLens OR "Abstract":HoloLens OR "Document Title":physicalization OR "Abstract":physicalization OR "Document Title":physicalisation OR "Abstract":physicalisation OR "Document Title":"physical visualization" OR "Abstract":"physical visualization") AND ("Document Title":"visual analysis" OR "Abstract":"visual analysis" OR "Document Title":visualizing OR "Abstract":visualizing OR "Document Title":visualising OR "Abstract":visualising)  UNION  ("Document Title":"time-varying network" OR "Abstract":"time-varying network" OR "Document Title":"evolving network" OR "Abstract":"evolving network") AND ("Document Title":"head-mounted" OR "Abstract":"head-mounted" OR "Document Title":HoloLens OR "Abstract":HoloLens OR "Document Title":physicalization OR "Abstract":physicalization OR "Document Title":physicalisation OR "Abstract":physicalisation OR "Document Title":"physical visualization" OR "Abstract":"physical visualization") AND ("Document Title":"visual analysis" OR "Abstract":"visual analysis" OR "Document Title":visualizing OR "Abstract":visualizing OR "Document Title":visualising OR "Abstract":visualising)  UNION  ("Document Title":"temporal networks" OR "Abstract":"temporal networks" OR "Document Title":"temporal graph" OR "Abstract":"temporal graph" OR "Document Title":"temporal graphs" OR "Abstract":"temporal graphs" OR "Document Title":"time-varying network" OR "Abstract":"time-varying network" OR "Document Title":"evolving network" OR "Abstract":"evolving network") AND ("Document Title":"physical visualisation" OR "Abstract":"physical visualisation" OR "Document Title":tangible OR "Abstract":tangible OR "Document Title":"3D printed" OR "Abstract":"3D printed" OR "Document Title":"3D printing" OR "Abstract":"3D printing") AND ("Document Title":visualization OR "Abstract":visualization OR "Document Title":visualisation OR "Abstract":visualisation OR "Document Title":"visual analytics" OR "Abstract":"visual analytics")  UNION  ("Document Title":"temporal networks" OR "Abstract":"temporal networks" OR "Document Title":"temporal graph" OR "Abstract":"temporal graph" OR "Document Title":"temporal graphs" OR "Abstract":"temporal graphs" OR "Document Title":"time-varying network" OR "Abstract":"time-varying network" OR "Document Title":"evolving network" OR "Abstract":"evolving network") AND ("Document Title":"physical visualisation" OR "Abstract":"physical visualisation" OR "Document Title":tangible OR "Abstract":tangible OR "Document Title":"3D printed" OR "Abstract":"3D printed" OR "Document Title":"3D printing" OR "Abstract":"3D printing") AND ("Document Title":"visual analysis" OR "Abstract":"visual analysis" OR "Document Title":visualizing OR "Abstract":visualizing OR "Document Title":visualising OR "Abstract":visualising)
```

**ieee Q5 v2**

```
("Document Title":"augmented reality" OR "Abstract":"augmented reality" OR "Document Title":"mixed reality" OR "Abstract":"mixed reality" OR "Document Title":HoloLens OR "Abstract":HoloLens) AND ("Document Title":"design space" OR "Abstract":"design space" OR "Document Title":"design spaces" OR "Abstract":"design spaces") AND ("Document Title":visualization OR "Abstract":visualization OR "Document Title":visualisation OR "Abstract":visualisation OR "Document Title":"visual analytics" OR "Abstract":"visual analytics" OR "Document Title":"visual analysis" OR "Abstract":"visual analysis" OR "Document Title":visualizing OR "Abstract":visualizing OR "Document Title":visualising OR "Abstract":visualising)
```

**ieee Q6 v2**

```
("Document Title":"multilayer network" OR "Abstract":"multilayer network" OR "Document Title":"multilayer networks" OR "Abstract":"multilayer networks" OR "Document Title":"multi-layer network" OR "Abstract":"multi-layer network" OR "Document Title":"multi-layer networks" OR "Abstract":"multi-layer networks") AND ("Document Title":matrix OR "Abstract":matrix OR "Document Title":matrices OR "Abstract":matrices OR "Document Title":"adjacency matrix" OR "Abstract":"adjacency matrix" OR "Document Title":"hybrid representation" OR "Abstract":"hybrid representation") AND ("Document Title":visualization OR "Abstract":visualization OR "Document Title":visualisation OR "Abstract":visualisation OR "Document Title":"visual analytics" OR "Abstract":"visual analytics")  UNION  ("Document Title":"multilayer network" OR "Abstract":"multilayer network" OR "Document Title":"multilayer networks" OR "Abstract":"multilayer networks" OR "Document Title":"multi-layer network" OR "Abstract":"multi-layer network" OR "Document Title":"multi-layer networks" OR "Abstract":"multi-layer networks") AND ("Document Title":matrix OR "Abstract":matrix OR "Document Title":matrices OR "Abstract":matrices OR "Document Title":"adjacency matrix" OR "Abstract":"adjacency matrix" OR "Document Title":"hybrid representation" OR "Abstract":"hybrid representation") AND ("Document Title":"visual analysis" OR "Abstract":"visual analysis" OR "Document Title":visualizing OR "Abstract":visualizing OR "Document Title":visualising OR "Abstract":visualising)  UNION  ("Document Title":"multilayer network" OR "Abstract":"multilayer network" OR "Document Title":"multilayer networks" OR "Abstract":"multilayer networks" OR "Document Title":"multi-layer network" OR "Abstract":"multi-layer network" OR "Document Title":"multi-layer networks" OR "Abstract":"multi-layer networks") AND ("Document Title":"hybrid visualization" OR "Abstract":"hybrid visualization" OR "Document Title":"hybrid visualisation" OR "Abstract":"hybrid visualisation" OR "Document Title":"node-link" OR "Abstract":"node-link") AND ("Document Title":visualization OR "Abstract":visualization OR "Document Title":visualisation OR "Abstract":visualisation OR "Document Title":"visual analytics" OR "Abstract":"visual analytics")  UNION  ("Document Title":"multilayer network" OR "Abstract":"multilayer network" OR "Document Title":"multilayer networks" OR "Abstract":"multilayer networks" OR "Document Title":"multi-layer network" OR "Abstract":"multi-layer network" OR "Document Title":"multi-layer networks" OR "Abstract":"multi-layer networks") AND ("Document Title":"hybrid visualization" OR "Abstract":"hybrid visualization" OR "Document Title":"hybrid visualisation" OR "Abstract":"hybrid visualisation" OR "Document Title":"node-link" OR "Abstract":"node-link") AND ("Document Title":"visual analysis" OR "Abstract":"visual analysis" OR "Document Title":visualizing OR "Abstract":visualizing OR "Document Title":visualising OR "Abstract":visualising)  UNION  ("Document Title":"multilayered network" OR "Abstract":"multilayered network" OR "Document Title":"multilayered networks" OR "Abstract":"multilayered networks" OR "Document Title":"multilayer graph" OR "Abstract":"multilayer graph") AND ("Document Title":matrix OR "Abstract":matrix OR "Document Title":matrices OR "Abstract":matrices OR "Document Title":"adjacency matrix" OR "Abstract":"adjacency matrix" OR "Document Title":"hybrid representation" OR "Abstract":"hybrid representation") AND ("Document Title":visualization OR "Abstract":visualization OR "Document Title":visualisation OR "Abstract":visualisation OR "Document Title":"visual analytics" OR "Abstract":"visual analytics")  UNION  ("Document Title":"multilayered network" OR "Abstract":"multilayered network" OR "Document Title":"multilayered networks" OR "Abstract":"multilayered networks" OR "Document Title":"multilayer graph" OR "Abstract":"multilayer graph") AND ("Document Title":matrix OR "Abstract":matrix OR "Document Title":matrices OR "Abstract":matrices OR "Document Title":"adjacency matrix" OR "Abstract":"adjacency matrix" OR "Document Title":"hybrid representation" OR "Abstract":"hybrid representation") AND ("Document Title":"visual analysis" OR "Abstract":"visual analysis" OR "Document Title":visualizing OR "Abstract":visualizing OR "Document Title":visualising OR "Abstract":visualising)  UNION  ("Document Title":"multilayered network" OR "Abstract":"multilayered network" OR "Document Title":"multilayered networks" OR "Abstract":"multilayered networks" OR "Document Title":"multilayer graph" OR "Abstract":"multilayer graph") AND ("Document Title":"hybrid visualization" OR "Abstract":"hybrid visualization" OR "Document Title":"hybrid visualisation" OR "Abstract":"hybrid visualisation" OR "Document Title":"node-link" OR "Abstract":"node-link") AND ("Document Title":visualization OR "Abstract":visualization OR "Document Title":visualisation OR "Abstract":visualisation OR "Document Title":"visual analytics" OR "Abstract":"visual analytics" OR "Document Title":"visual analysis" OR "Abstract":"visual analysis" OR "Document Title":visualizing OR "Abstract":visualizing OR "Document Title":visualising OR "Abstract":visualising)  UNION  ("Document Title":"multilayer graphs" OR "Abstract":"multilayer graphs" OR "Document Title":"multi-layer graph" OR "Abstract":"multi-layer graph" OR "Document Title":"multiplex network" OR "Abstract":"multiplex network") AND ("Document Title":matrix OR "Abstract":matrix OR "Document Title":matrices OR "Abstract":matrices OR "Document Title":"adjacency matrix" OR "Abstract":"adjacency matrix" OR "Document Title":"hybrid representation" OR "Abstract":"hybrid representation") AND ("Document Title":visualization OR "Abstract":visualization OR "Document Title":visualisation OR "Abstract":visualisation OR "Document Title":"visual analytics" OR "Abstract":"visual analytics")  UNION  ("Document Title":"multilayer graphs" OR "Abstract":"multilayer graphs" OR "Document Title":"multi-layer graph" OR "Abstract":"multi-layer graph" OR "Document Title":"multiplex network" OR "Abstract":"multiplex network") AND ("Document Title":matrix OR "Abstract":matrix OR "Document Title":matrices OR "Abstract":matrices OR "Document Title":"adjacency matrix" OR "Abstract":"adjacency matrix" OR "Document Title":"hybrid representation" OR "Abstract":"hybrid representation") AND ("Document Title":"visual analysis" OR "Abstract":"visual analysis" OR "Document Title":visualizing OR "Abstract":visualizing OR "Document Title":visualising OR "Abstract":visualising)  UNION  ("Document Title":"multiplex networks" OR "Abstract":"multiplex networks" OR "Document Title":"multiplex graph" OR "Abstract":"multiplex graph" OR "Document Title":"multi-relational network" OR "Abstract":"multi-relational network") AND ("Document Title":matrix OR "Abstract":matrix OR "Document Title":matrices OR "Abstract":matrices OR "Document Title":"adjacency matrix" OR "Abstract":"adjacency matrix" OR "Document Title":"hybrid representation" OR "Abstract":"hybrid representation") AND ("Document Title":visualization OR "Abstract":visualization OR "Document Title":visualisation OR "Abstract":visualisation OR "Document Title":"visual analytics" OR "Abstract":"visual analytics")  UNION  ("Document Title":"multiplex networks" OR "Abstract":"multiplex networks" OR "Document Title":"multiplex graph" OR "Abstract":"multiplex graph" OR "Document Title":"multi-relational network" OR "Abstract":"multi-relational network") AND ("Document Title":matrix OR "Abstract":matrix OR "Document Title":matrices OR "Abstract":matrices OR "Document Title":"adjacency matrix" OR "Abstract":"adjacency matrix" OR "Document Title":"hybrid representation" OR "Abstract":"hybrid representation") AND ("Document Title":"visual analysis" OR "Abstract":"visual analysis" OR "Document Title":visualizing OR "Abstract":visualizing OR "Document Title":visualising OR "Abstract":visualising)  UNION  ("Document Title":"multilayer graphs" OR "Abstract":"multilayer graphs" OR "Document Title":"multi-layer graph" OR "Abstract":"multi-layer graph" OR "Document Title":"multiplex network" OR "Abstract":"multiplex network") AND ("Document Title":"hybrid visualization" OR "Abstract":"hybrid visualization" OR "Document Title":"hybrid visualisation" OR "Abstract":"hybrid visualisation" OR "Document Title":"node-link" OR "Abstract":"node-link") AND ("Document Title":visualization OR "Abstract":visualization OR "Document Title":visualisation OR "Abstract":visualisation OR "Document Title":"visual analytics" OR "Abstract":"visual analytics" OR "Document Title":"visual analysis" OR "Abstract":"visual analysis" OR "Document Title":visualizing OR "Abstract":visualizing OR "Document Title":visualising OR "Abstract":visualising)  UNION  ("Document Title":"multiplex networks" OR "Abstract":"multiplex networks" OR "Document Title":"multiplex graph" OR "Abstract":"multiplex graph" OR "Document Title":"multi-relational network" OR "Abstract":"multi-relational network") AND ("Document Title":"hybrid visualization" OR "Abstract":"hybrid visualization" OR "Document Title":"hybrid visualisation" OR "Abstract":"hybrid visualisation" OR "Document Title":"node-link" OR "Abstract":"node-link") AND ("Document Title":visualization OR "Abstract":visualization OR "Document Title":visualisation OR "Abstract":visualisation OR "Document Title":"visual analytics" OR "Abstract":"visual analytics" OR "Document Title":"visual analysis" OR "Abstract":"visual analysis" OR "Document Title":visualizing OR "Abstract":visualizing OR "Document Title":visualising OR "Abstract":visualising)  UNION  ("Document Title":"multi-relational graph" OR "Abstract":"multi-relational graph" OR "Document Title":"multirelational network" OR "Abstract":"multirelational network" OR "Document Title":"dynamic network" OR "Abstract":"dynamic network") AND ("Document Title":matrix OR "Abstract":matrix OR "Document Title":matrices OR "Abstract":matrices OR "Document Title":"adjacency matrix" OR "Abstract":"adjacency matrix" OR "Document Title":"hybrid representation" OR "Abstract":"hybrid representation") AND ("Document Title":visualization OR "Abstract":visualization OR "Document Title":visualisation OR "Abstract":visualisation OR "Document Title":"visual analytics" OR "Abstract":"visual analytics")  UNION  ("Document Title":"multi-relational graph" OR "Abstract":"multi-relational graph" OR "Document Title":"multirelational network" OR "Abstract":"multirelational network" OR "Document Title":"dynamic network" OR "Abstract":"dynamic network") AND ("Document Title":matrix OR "Abstract":matrix OR "Document Title":matrices OR "Abstract":matrices OR "Document Title":"adjacency matrix" OR "Abstract":"adjacency matrix" OR "Document Title":"hybrid representation" OR "Abstract":"hybrid representation") AND ("Document Title":"visual analysis" OR "Abstract":"visual analysis" OR "Document Title":visualizing OR "Abstract":visualizing OR "Document Title":visualising OR "Abstract":visualising)  UNION  ("Document Title":"dynamic networks" OR "Abstract":"dynamic networks" OR "Document Title":"dynamic graph" OR "Abstract":"dynamic graph" OR "Document Title":"dynamic graphs" OR "Abstract":"dynamic graphs") AND ("Document Title":matrix OR "Abstract":matrix OR "Document Title":matrices OR "Abstract":matrices OR "Document Title":"adjacency matrix" OR "Abstract":"adjacency matrix" OR "Document Title":"hybrid representation" OR "Abstract":"hybrid representation") AND ("Document Title":visualization OR "Abstract":visualization OR "Document Title":visualisation OR "Abstract":visualisation OR "Document Title":"visual analytics" OR "Abstract":"visual analytics")  UNION  ("Document Title":"dynamic networks" OR "Abstract":"dynamic networks" OR "Document Title":"dynamic graph" OR "Abstract":"dynamic graph" OR "Document Title":"dynamic graphs" OR "Abstract":"dynamic graphs") AND ("Document Title":matrix OR "Abstract":matrix OR "Document Title":matrices OR "Abstract":matrices OR "Document Title":"adjacency matrix" OR "Abstract":"adjacency matrix" OR "Document Title":"hybrid representation" OR "Abstract":"hybrid representation") AND ("Document Title":"visual analysis" OR "Abstract":"visual analysis" OR "Document Title":visualizing OR "Abstract":visualizing OR "Document Title":visualising OR "Abstract":visualising)  UNION  ("Document Title":"multi-relational graph" OR "Abstract":"multi-relational graph" OR "Document Title":"multirelational network" OR "Abstract":"multirelational network" OR "Document Title":"dynamic network" OR "Abstract":"dynamic network") AND ("Document Title":"hybrid visualization" OR "Abstract":"hybrid visualization" OR "Document Title":"hybrid visualisation" OR "Abstract":"hybrid visualisation" OR "Document Title":"node-link" OR "Abstract":"node-link") AND ("Document Title":visualization OR "Abstract":visualization OR "Document Title":visualisation OR "Abstract":visualisation OR "Document Title":"visual analytics" OR "Abstract":"visual analytics" OR "Document Title":"visual analysis" OR "Abstract":"visual analysis" OR "Document Title":visualizing OR "Abstract":visualizing OR "Document Title":visualising OR "Abstract":visualising)  UNION  ("Document Title":"dynamic networks" OR "Abstract":"dynamic networks" OR "Document Title":"dynamic graph" OR "Abstract":"dynamic graph" OR "Document Title":"dynamic graphs" OR "Abstract":"dynamic graphs") AND ("Document Title":"hybrid visualization" OR "Abstract":"hybrid visualization" OR "Document Title":"hybrid visualisation" OR "Abstract":"hybrid visualisation" OR "Document Title":"node-link" OR "Abstract":"node-link") AND ("Document Title":visualization OR "Abstract":visualization OR "Document Title":visualisation OR "Abstract":visualisation OR "Document Title":"visual analytics" OR "Abstract":"visual analytics" OR "Document Title":"visual analysis" OR "Abstract":"visual analysis" OR "Document Title":visualizing OR "Abstract":visualizing OR "Document Title":visualising OR "Abstract":visualising)  UNION  ("Document Title":"temporal network" OR "Abstract":"temporal network" OR "Document Title":"temporal networks" OR "Abstract":"temporal networks" OR "Document Title":"temporal graph" OR "Abstract":"temporal graph") AND ("Document Title":matrix OR "Abstract":matrix OR "Document Title":matrices OR "Abstract":matrices OR "Document Title":"adjacency matrix" OR "Abstract":"adjacency matrix" OR "Document Title":"hybrid representation" OR "Abstract":"hybrid representation") AND ("Document Title":visualization OR "Abstract":visualization OR "Document Title":visualisation OR "Abstract":visualisation OR "Document Title":"visual analytics" OR "Abstract":"visual analytics")  UNION  ("Document Title":"temporal network" OR "Abstract":"temporal network" OR "Document Title":"temporal networks" OR "Abstract":"temporal networks" OR "Document Title":"temporal graph" OR "Abstract":"temporal graph") AND ("Document Title":matrix OR "Abstract":matrix OR "Document Title":matrices OR "Abstract":matrices OR "Document Title":"adjacency matrix" OR "Abstract":"adjacency matrix" OR "Document Title":"hybrid representation" OR "Abstract":"hybrid representation") AND ("Document Title":"visual analysis" OR "Abstract":"visual analysis" OR "Document Title":visualizing OR "Abstract":visualizing OR "Document Title":visualising OR "Abstract":visualising)  UNION  ("Document Title":"temporal graphs" OR "Abstract":"temporal graphs" OR "Document Title":"time-varying network" OR "Abstract":"time-varying network" OR "Document Title":"evolving network" OR "Abstract":"evolving network") AND ("Document Title":matrix OR "Abstract":matrix OR "Document Title":matrices OR "Abstract":matrices OR "Document Title":"adjacency matrix" OR "Abstract":"adjacency matrix" OR "Document Title":"hybrid representation" OR "Abstract":"hybrid representation") AND ("Document Title":visualization OR "Abstract":visualization OR "Document Title":visualisation OR "Abstract":visualisation OR "Document Title":"visual analytics" OR "Abstract":"visual analytics")  UNION  ("Document Title":"temporal graphs" OR "Abstract":"temporal graphs" OR "Document Title":"time-varying network" OR "Abstract":"time-varying network" OR "Document Title":"evolving network" OR "Abstract":"evolving network") AND ("Document Title":matrix OR "Abstract":matrix OR "Document Title":matrices OR "Abstract":matrices OR "Document Title":"adjacency matrix" OR "Abstract":"adjacency matrix" OR "Document Title":"hybrid representation" OR "Abstract":"hybrid representation") AND ("Document Title":"visual analysis" OR "Abstract":"visual analysis" OR "Document Title":visualizing OR "Abstract":visualizing OR "Document Title":visualising OR "Abstract":visualising)  UNION  ("Document Title":"temporal network" OR "Abstract":"temporal network" OR "Document Title":"temporal networks" OR "Abstract":"temporal networks" OR "Document Title":"temporal graph" OR "Abstract":"temporal graph") AND ("Document Title":"hybrid visualization" OR "Abstract":"hybrid visualization" OR "Document Title":"hybrid visualisation" OR "Abstract":"hybrid visualisation" OR "Document Title":"node-link" OR "Abstract":"node-link") AND ("Document Title":visualization OR "Abstract":visualization OR "Document Title":visualisation OR "Abstract":visualisation OR "Document Title":"visual analytics" OR "Abstract":"visual analytics" OR "Document Title":"visual analysis" OR "Abstract":"visual analysis" OR "Document Title":visualizing OR "Abstract":visualizing OR "Document Title":visualising OR "Abstract":visualising)  UNION  ("Document Title":"temporal graphs" OR "Abstract":"temporal graphs" OR "Document Title":"time-varying network" OR "Abstract":"time-varying network" OR "Document Title":"evolving network" OR "Abstract":"evolving network") AND ("Document Title":"hybrid visualization" OR "Abstract":"hybrid visualization" OR "Document Title":"hybrid visualisation" OR "Abstract":"hybrid visualisation" OR "Document Title":"node-link" OR "Abstract":"node-link") AND ("Document Title":visualization OR "Abstract":visualization OR "Document Title":visualisation OR "Abstract":visualisation OR "Document Title":"visual analytics" OR "Abstract":"visual analytics" OR "Document Title":"visual analysis" OR "Abstract":"visual analysis" OR "Document Title":visualizing OR "Abstract":visualizing OR "Document Title":visualising OR "Abstract":visualising)
```

**ieee Q7 v2**

```
("Document Title":"augmented reality" OR "Abstract":"augmented reality" OR "Document Title":"mixed reality" OR "Abstract":"mixed reality" OR "Document Title":HoloLens OR "Abstract":HoloLens) AND ("Document Title":tangible OR "Abstract":tangible OR "Document Title":touch OR "Abstract":touch OR "Document Title":"physical object" OR "Abstract":"physical object" OR "Document Title":"physical objects" OR "Abstract":"physical objects") AND ("Document Title":visualization OR "Abstract":visualization OR "Document Title":visualisation OR "Abstract":visualisation OR "Document Title":"visual analytics" OR "Abstract":"visual analytics")  UNION  ("Document Title":"augmented reality" OR "Abstract":"augmented reality" OR "Document Title":"mixed reality" OR "Abstract":"mixed reality" OR "Document Title":HoloLens OR "Abstract":HoloLens) AND ("Document Title":tangible OR "Abstract":tangible OR "Document Title":touch OR "Abstract":touch OR "Document Title":"physical object" OR "Abstract":"physical object" OR "Document Title":"physical objects" OR "Abstract":"physical objects") AND ("Document Title":"visual analysis" OR "Abstract":"visual analysis" OR "Document Title":visualizing OR "Abstract":visualizing OR "Document Title":visualising OR "Abstract":visualising)  UNION  ("Document Title":"augmented reality" OR "Abstract":"augmented reality" OR "Document Title":"mixed reality" OR "Abstract":"mixed reality" OR "Document Title":HoloLens OR "Abstract":HoloLens) AND ("Document Title":"physical referent" OR "Abstract":"physical referent" OR "Document Title":"physical referents" OR "Abstract":"physical referents" OR "Document Title":handheld OR "Abstract":handheld) AND ("Document Title":visualization OR "Abstract":visualization OR "Document Title":visualisation OR "Abstract":visualisation OR "Document Title":"visual analytics" OR "Abstract":"visual analytics" OR "Document Title":"visual analysis" OR "Abstract":"visual analysis" OR "Document Title":visualizing OR "Abstract":visualizing OR "Document Title":visualising OR "Abstract":visualising)
```

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

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

**Amendment A1 (2026-11-21, decided by the authors before final screening):**
- **I4 narrowed:** AR visualization techniques count only if they visualize *abstract data* (e.g., charts, networks, situated/immersive analytics, AR visualization design spaces) and instantiate an AR-specific value. AR rendering of physical objects or scenes (x-ray vision, ghosting, occlusion/depth rendering), navigation and out-of-view guidance cues, assembly/maintenance/medical guidance overlays → **E2**.
- **I1 for dynamic networks:** time slices count as layers only when drawn as distinct layers (stacked planes, 2.5D, Matrix-Cube-like, explicit layer views). Plain small multiples, animation, flip-books and comics → **E4**.
- **A1 clarification (2026-11-21):** spatial scientific field data (volumes/point clouds, flow or thermal fields on real objects, in-situ signal-strength fields) count as physical, not abstract data → **E2**; in-situ sensor values shown as charts or glyphs remain I4.

**Amendment A2 (2026-11-21, decided by the authors during full-text screening):**
- Bipartite / two-mode networks (two node sets, one relation type) are not multilayer → **E3** (unless another I-code applies).
- Simultaneous embedding of several graphs on one vertex set counts as **I1** only if the paper proposes a visualization design; pure graph-drawing theory → **E8**.
- Stereoscopic desktop / fish-tank displays are not immersive for I2 → **E3** (I2 = HMD, CAVE, or AR/MR devices).

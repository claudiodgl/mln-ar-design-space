# Coding of 7 additional papers against Table 2 (VR / Desktop / Physicalization batch)

Method: full text read for every paper. I looked at every page image that has a figure (vmv p01, p04; detangler p04, p06, p07, p09, p10; multistory p01, p03, p04; hybridmln p01; mira p03, p04; pathtracing p02, p09, p10 (and the text of Figs 2–4); hapticphys p01, plus figure captions 2–4).
Grey cells were respected (desktop: no Phys. Anchor, Floating, Input modality, Phys. Elem., Spatial Ctx.; VR: no Spatial Ctx.; physicalization: no Floating, Mid-air, Touch, Gaze, Voice, Virt. Elem.).
Labels: **solid** = stated in the text or clearly visible in a figure; *(weak)* = arguable, so the coder decides.

---

## 1. vmv_layer2d25d: 2D versus 2.5D Layer Arrangement for Animal Behaviour Multiplex Networks

**Bibliographic facts**
- Authors: S. P. Feyer, K. Klein, S. Kobourov, K. Snell, N. Borrego, G. E. Finerty, R. S. A. van Bemmelen, N. J. O'Hanlon, U. Muzuma, F. Schreiber
- Venue: Vision, Modeling, and Visualization (VMV) 2026, Eurographics Proceedings (eds. Leimkühler, Weinkauf, Campen). Full paper, 8 pages including references.
- DOI: 10.2312/vmv20261000. Supplement: doi.org/10.18419/DARUS-5503
- Type: qualitative expert study (6 animal-behaviour researchers, think-aloud). The study prototype was adapted from GAV-VR (Unity, p4 §3.5).

**Platform:** VR. Valve Index HMD with Index controllers and Lighthouse tracking (p4 §3.5). It is not AR.

**Network data / layers:** Yes, multiplex networks on real data. N1 is multirelational: 5 behaviour layers with the same 6 nodes. N2 is temporal: 21 time-slice layers, about 144 nodes and 1656 edges per layer (Table 2, p3). Layers are drawn as transparent grey planes (p3 §3.1).

**Coding**
| Subdimension | Values | Justification |
|---|---|---|
| Visual Encoding | **Color, Size** | Edge weight is encoded by thickness and colour, green to blue (p3 §3.1, p3 §3.2.1). N2 nodes are coloured by population (p4 §3.2.2, Fig 2). |
| Dimensionality | **2D** | Each layer is a planar layout (circular or stress layout on a plane). Under Lee et al.'s definition, 2.5D is still 2D layers arranged in 3D space. There is no 3D layer layout ("We did not include a 3D layer arrangement", p3). |
| Geometric Pose | none | Participants "could not manipulate the network" (p3). Only the vertical position was set once at the start, collaboratively with the conductor (p3), and it is a translation, not rotation or scale. |
| Anchoring | **Floating** | Layers hang freely in the VR room (Fig 1, Fig 2). Nothing is registered to physical objects. |
| Layer Coupling | **Separated** | Inter-layer identity edges were deliberately omitted (p3 §3.1: "We omitted these edges…"). This differs from Feyer 2024, which is coded Linked. |
| Network Representation | **Node-link** | Labelled spheres and weighted edges (p3, Fig 2). |
| Graph Layout | **Node Pos.** | Circular layout for N1 (p3 §3.2.1). Stress-minimisation layout in OGDF on the union graph for N2 (p4 §3.2.2). |
| Layer Representation | **Shared** | "both conditions used the same node positions" and "kept each individual at the same position across all layers" (p3). N2 uses the union-graph layout so that each node has the same position in every layer (p4). Feyer 2024 is coded Mixed instead. |
| Input Modality | *Tangible (weak)* | For N2, the joystick on a VR controller scrolls through the temporal layers, with 5 of 21 visible at a time (p4 §3.2.2). This is controller input but not pose input. Under the calibration convention ("incl. tracked VR controllers") it can be coded; under a strict pose-based reading it is blank. |
| Interaction Target | *Virt. Elem. (weak)* | The scrolling acts on the rendered layers. |
| Operation | *Filter (weak)* | Scrolling changes which temporal layers are shown or hidden (p4, p7 "static, except for scrolling"). There is no Arrange or Select: "Interaction with the networks was excluded" (p2). |

Strict code line: Color, Size, 2D, Floating, Separated, Node-link, Node Pos., Shared. Optional: Tangible, Virt. Elem., Filter.

**Comparison with Feyer et al. 2024 (TVCG, "2D, 2.5D, or 3D?")**
- **VR?** Yes, the same group and an equivalent VR setup. It is the domain-data follow-up of Feyer 2024 (cited as [FPK*23], §5.3).
- **Are 2D layers in 3D space the main design, or only a comparison condition?** Both conditions consist of several 2D layers placed in 3D space: side by side in a row ("2D") or stacked ("2.5D"). The paper's "2D" means a juxtaposed arrangement, not a 2D display. The work is still structured as a comparison of conditions. It goes one step further than Feyer 2024, though. In the third phase of each dataset, both arrangements were shown at the same time and participants chose between them (p3–4). Three participants scanned in 2D and then switched to 2.5D (p5 §4.3). The paper also concludes that immersive tools should treat 2D and 2.5D as *complementary views*, offered together (p6 §5.4, p7 §6). The 3D-layer condition from Feyer 2024 was dropped.
- **Can users arrange layers freely?** **No.** Layer positions and spacing were fixed (30 cm, 7.5 cm, 15 cm, p3–4). Participants could only walk around (p3). "Arranging layers freely to compare distant layers next to each other" is listed as a participant *request* (p5–6 §4.4). It also appears as future work: "allowing users to freely arrange selected layers side by side, pin relevant layers, or duplicate layers" (p6 §5.2) and "layer rearrangement, and layer distance" (p7 §5.5).
- **Effect on the paper's claims:**
  - "In VR, 2D appears only as a comparison condition": still roughly true, since both arrangements are study conditions. It should be softened or footnoted, because this paper shows 2D and 2.5D side by side in one scene (phase 3) and argues for 2D as a full overview view in VR.
  - "No work arranges several 2D layers freely in space": **supported, and strengthened.** The paper does not offer free arrangement and explicitly names it as an expert request and future work, so it can be cited as evidence of the need.
  - "Only two VR systems address several layers or networks": **needs updating** if this paper enters Table 2. It is a third VR work with several layers. It is a study prototype, not a released system, but so is Feyer 2024. Possible rephrasing: "only Feyer et al.'s two studies (and X)…".
  - Coding differences from Feyer 2024: this paper adds **Separated** and **Shared**, which no current VR row has (Feyer 2024 is Linked + Mixed). It also adds Size, and possibly controller scrolling.

**Verdict: HIGH.** It is the direct VR follow-up of a Table-2 work, it adds two values that are new for VR (Separated, Shared), and it bears directly on three of the paper's claims, including expert evidence that free layer arrangement is wanted.

---

## 2. detangler: Detangler: Visual Analytics for Multiplex Networks

**Bibliographic facts:** B. Renoust, G. Melançon, T. Munzner. Computer Graphics Forum 34(3), EuroVis 2015, pp. 321–330. Full paper, 10 pages. DOI 10.1111/cgf.12644 (HAL hal-01467984).

**Platform:** Desktop (web, D3 front end with a Tulip back end, §6). Mouse/lasso input.

**Network data / layers:** A multiplex network: links of different types, where each type is a layer (§1–2). The layers are never drawn as layers. They are abstracted into two derived networks. In the *substrate* network, all multiplex links between two nodes become one link. In the *catalyst* network, each link type (an entire layer) becomes one node (Fig 1d–e, §2).

**Coding**
| Subdimension | Values | Justification |
|---|---|---|
| Visual Encoding | **Color, Size, Shape** | Color: the entanglement intensity and homogeneity are mapped to the lasso fill and perimeter on a sequential colour ramp (§5.1, Fig 6b); red marks selected and highlighted states (§5.2, Fig 7). Size: catalyst node size encodes the entanglement index (§5, §4.1). Shape: substrate nodes are squares and catalyst nodes are circles (§5, Fig 8b). |
| Dimensionality | **2D** | 2D node-link views (Figs 6, 9, 10). |
| Geometric Pose | **Rotation, Scale** | Visible in a figure only: the "View settings" menu in Fig 7 (p7) lists "Zoom in / Zoom out" and "Rotate view". Not mentioned in the text. |
| Anchoring | grey | Desktop. |
| Layer Coupling | **Merged** | The substrate view flattens all layers into one projected network (§2, Fig 1d). The catalyst view rolls each layer up into one node. The two linked views connect two derived networks, not layers, so Linked is not coded. |
| Network Representation | **Node-link** | Both views are node-link (§5). |
| Graph Layout | **Node Pos., Aggregated** | Node Pos.: the harmonized force-directed layout (§5.3, Fig 8). Aggregated: catalyst nodes are abstractions of whole layers, "a single visual object captures information that would require an entire visual layer" (§6, §8). |
| Layer Representation | none | Layers are not shown individually. |
| Input Modality | grey | Mouse (lasso, double-click). |
| Interaction Target | **Virt. Elem.** | Nodes are selected with the lasso. |
| Operation | **Select**, *Filter (weak)* | Select: lasso selection, pivot brushing, leapfrog (§4, §5.1–5.2). Filter: the menu has "Hide labels / Hide links" (Fig 7). Non-selected items are dimmed to 50% (§5.1), which is highlighting, not filtering. |

**Verdict: MEDIUM (supplement).** It is a well-known multiplex visual-analytics system, but every value it uses is already covered by desktop rows (Merged + Aggregated by MLN bundling and VERTIGo, Shape by VERTIGo, Rotation/Scale by several). It makes no use of 3D, layers in space or Linked.

---

## 3. multistory: MultiStory: Visual Analytics of Dynamic Multi-Relational Networks

**Bibliographic facts:** Amyra Meidiana, Seok-Hee Hong (University of Sydney). IEEE Pacific Visualization Symposium (PacificVis) 2015, Hangzhou, pp. 75–79. Short paper, 5 pages. No DOI is printed in the PDF; it is probably 10.1109/PACIFICVIS.2015.7156359, but **check this**.

**Platform:** Desktop (web-based application, §1).

**Network data / layers:** Dynamic multi-relational social networks (MIT Reality Commons). Case 1 has 5 relationship types over survey time steps. Case 2 has friendship plus phone, SMS and Bluetooth correspondences over months and weeks (§4). Relation types and time steps both act as layers.

**Coding**
| Subdimension | Values | Justification |
|---|---|---|
| Visual Encoding | **Color, Size** | Color: dynamic clusters, categorical node properties, and InterArc frequency (§3.3, §4.1 Task 4, Figs 1, 5). Size: the node-link view has nodes sized by a centrality measure, visible in Fig 1 (right panel and the "Degree" dropdown). This comes from the figure only. |
| Dimensionality | **2D** | Storyline and node-link views are planar (Fig 1). |
| Geometric Pose | none | "Temporal zooming" changes time granularity, not geometric scale (§3.4, Fig 8). |
| Layer Coupling | **Merged, Linked** | Merged: the secondary relationships (AlterCluster glyphs) and correspondences (InterArc) are overlaid on the primary relationship's storyline in one view (§3.3, Figs 1, 7). Linked: storylines connect each actor across consecutive time slices, and the cluster similarity links clusters across relations (§3.2, Figs 3–4). |
| Network Representation | **Node-link** | A node-link view (§3.3) plus InterArc arcs between actor lines. The storyline itself is neither node-link nor matrix. |
| Graph Layout | **Node Pos., Aggregated** | Node Pos.: the node-link layout and the storyline layout (Tanahashi's algorithm, Acknowledgements). Aggregated: Louvain clustering into dynamic clusters, shown as vertical-line glyphs, and temporally aggregated correspondences (§3.2–3.3). |
| Layer Representation | *Independent (weak)* | Different relation types get different visual forms: storyline for the primary relationship, vertical-line cluster glyphs for secondary ones, arcs for correspondences, and node-link for the selected main relationship (§3.3). These are not the node-link/matrix pair from the definition, so this is a weak instance. |
| Input Modality | grey | |
| Interaction Target | **Virt. Elem.** | |
| Operation | **Select, Filter** | "Selection, Highlight, Filtering", highlight freezing, similarity-threshold filtering, coordinated views (§3.4, §4.1, Fig 8). |

**Verdict: LOW–MEDIUM.** Storylines are outside the node-link/matrix space of the table. The only value new to the desktop group would be Independent, and it holds only in a weak sense. Use it as a supplement at most.

---

## 4. hybridmln: Hybrid Multilayer Network Visualization of Bibliographic Data

**Bibliographic facts:** É. Durant, A. Tappini, W. Didimo, G. Liotta, M. Ghoniem. EuroVis 2024 Posters (eds. Diehl, Gillmann, Kucher). Poster abstract, 3 pages. DOI 10.2312/evp.20241084.

**Platform:** Desktop (React/graphology.js web prototype, §3). Fig 1 is "a sketch".

**Network data / layers:** Yes, multilayer. Layers are the paper sets Included / Undecided / Excluded. Intra-layer edges come from shared authors or keywords, and there are inter-layer edges (§3, Fig 1). Three layers are shown at a time.

**Coding**
| Subdimension | Values | Justification |
|---|---|---|
| Visual Encoding | **Color** | Layer membership is coloured: cyan for included, magenta for excluded, black for undecided (Fig 1). Edges in the matrix are grey circles (§2). |
| Dimensionality | **2D** | "we consider the case of a 2D representation where layer nodes are laid out on parallel rectilinear axes" (Abstract). |
| Geometric Pose | none | |
| Layer Coupling | **Linked** | Inter-layer edges are drawn as straight lines between adjacent layer axes (§2, Fig 1). |
| Network Representation | **Hybrid** | Intra-layer edges use triangular half-matrices; inter-layer edges are node-link (§2, Fig 1). |
| Graph Layout | **Node Ord.** | Node seriation reveals intra-layer patterns or reduces inter-layer crossings (§2, §3). Per-component partial grids (Fig 1) are a space-saving device, not aggregation. Edge bundling is only future work (§4). |
| Layer Representation | **Mixed** | Every layer uses the same representation (axis plus half-matrix) with its own node set and order (Fig 1). |
| Input Modality / Target / Operation | none | No interaction. "user interactions… on laptops and large wall displays" is future work (§4). |

**Verdict: LOW (optional supplement).** It is a preliminary poster with a sketch and no interaction. Hybrid and Linked are already covered by NodeTrix/DynTrix and Arena3Dweb. It is interesting only as an MLN-specific hybrid (matrix inside layers, node-link between them).

---

## 5. mira: Interactively visualizing biological multilayer networks using MiRA

**Bibliographic facts:** Shir Miryam Nehoray, Yuval Bloch, Shai Pilosof (Ben-Gurion University). arXiv:2605.09597v2 [cs.SI], 13 May 2026. Preprint (application note), 7 pages. No journal DOI; arXiv DOI 10.48550/arXiv.2605.09597.

**Platform:** Desktop (browser single-page app on Canvas 2D; "not designed for tablets or phones", p5).

**Network data / layers:** Yes, multilayer. Layers can be space, time or interaction type, with intra- and inter-layer links and bipartite layers (pp. 1–3). Examples are a Canary Islands pollination network (Fig 1) and a 9-layer Plasmodium var-gene network (Fig 2).

**Coding**
| Subdimension | Values | Justification |
|---|---|---|
| Visual Encoding | **Color, Size** | Nodes are coloured by strength or attributes and scaled by degree (Fig 1a caption, p2, p4). Layer panel and inter-layer link colours can be set by the user (Fig 1c). |
| Dimensionality | **2D** | Each layer is a planar layout drawn on a tilted plane with a "hand-rolled oblique isometric projection" (p5, Fig 1a). No 3D layout. |
| Geometric Pose | *Scale (weak)* | "interactive map" (Leaflet) in Map and Layer modes (p2), which implies zoom. No rotation or zoom of the network is stated. |
| Layer Coupling | **Separated, Linked, Merged** | Separated: Grid View with one panel per layer (p2, Fig 2a). Linked: inter-layer links in Network Mode (Fig 1a–b). Merged: Meta-Network Mode aggregates all layers into one network (p2, Fig 2b, Table 1 rows 15–19). |
| Network Representation | **Node-link** | All network modes are node-link. The presence matrix and Jaccard heatmaps are statistics panels in Dashboard mode, not network representations. |
| Graph Layout | **Node Pos., Aggregated** | Node Pos.: d3 force-directed and bipartite layouts (p2, p5), circular meta-network (Fig 2b). Aggregated: Layer View Mode draws each layer as a bubble with a micro-graph, laid out by force by layer similarity (p2, Fig 1d). |
| Layer Representation | **Shared** | Grid View: "All cells share the same axes and node identities" (p2). Mixed cannot be confirmed for Network Mode. |
| Input Modality | grey | Mouse (Cmd/Ctrl+click). |
| Interaction Target | **Virt. Elem.** | Nodes and layers. |
| Operation | **Select, Filter**, *Arrange (weak)* | Select: clicking or searching a node highlights it across layers and modes (Fig 1b, Fig 2a–b). Filter: weight thresholding, attribute filtering, Data Mode filter tables (pp. 2, 5). Arrange: selected layers "can be popped out into floating 3D network panels for side-by-side spatial comparison" (p2, Fig 1c). Free user positioning is not stated. |

Note: Map Mode places each layer at its geographic sampling location on a map (Fig 1c–d). This is a desktop analogue of anchoring layers to spatial context, but on desktop that cell is grey.

**Verdict: MEDIUM (supplement).** It is a recent, fairly complete MLN tool (Separated, Linked, Merged, Shared), but its values are already covered by muxViz, Arena3Dweb and Py3plex, and it is an unreviewed arXiv preprint. Geographic layer placement is worth one sentence in the text.

---

## 6. pathtracing: Path Tracing in 2D, 3D, and Physicalized Networks

**Bibliographic facts:** Michael J. McGuffin, Ryan Servera, Marie Forest (ÉTS Montréal). IEEE Transactions on Visualization and Computer Graphics, journal article. The supplied text is arXiv:2207.11586v1 (2022): 12 pages plus a supplement. The TVCG DOI is not printed in this version. I believe it is 10.1109/TVCG.2023.3238989 (TVCG vol. 30, 2024), but **check this**.

**Platform:** This is a study with several conditions.
- Study 1 (VR, HTC Vive, 34 users): VR2D, VR2DHilite, VR3D, VR3DHilite (§4.1).
- Study 2 (12 users): VR3D versus **AR3DTouch**. In AR3DTouch, a 3D-printed network is held in a tracked holder, tracked with a Polhemus Patriot, and augmented with HoloLens callouts. The authors call this "augmented physicalization" (§5, Figs 14–15).
- Groups: **VR** and **Physicalization**, the latter AR-augmented like HoloGraphs. It could also go under AR.

**Network data / layers:** Synthetic single-layer Watts–Strogatz networks (70 nodes, 140 edges). There are no layers, so Layer Coupling and Layer Representation are not applicable.

**Coding: VR conditions (Study 1, plus VR3D in Study 2)**
| Subdimension | Values | Justification |
|---|---|---|
| Visual Encoding | *Color (weak)* | Only highlighting: green for hovered incident edges, red callouts for end-nodes, highlighted shortest path as feedback (Figs 1–3). Nodes are uniform white otherwise (§3.1). |
| Dimensionality | **2D, 3D** | The 2D layout is a projection of the 3D stress layout, with MSAGL edge routing (§3.1, Fig 1 left and middle). |
| Geometric Pose | **Rotation, Scale** | The handheld controller moves the network with 6 DoF. Bringing it closer "zoom[s] in" (§3, §4.2). |
| Anchoring | **Floating** | A virtual network carried by the controller, with no physical counterpart. This matches how VRNetzer and GAV-VR are coded. |
| Network Representation | **Node-link** | |
| Graph Layout | **Node Pos.** | Stress majorization plus label-overlap repulsion. Edge routing in 2D (§3.1). |
| Input Modality | **Tangible** | The 6-DoF controller in the non-dominant hand positions and rotates the network (§4.1). The mouse hover is desktop-style. Head-tilt selection of answers in a radial menu (§4.2) is response UI, not gaze interaction with the visualization, so Gaze is not coded. |
| Interaction Target | **Virt. Elem.** | |
| Operation | **Arrange, Select** | Arrange: move and rotate the network. Select: mouse-hover highlighting of a node's incident edges in the Hilite conditions (§4.2, Fig 2). |

**Coding: AR3DTouch, augmented physicalization (Study 2)**
| Subdimension | Values | Justification |
|---|---|---|
| Visual Encoding | none (*Color weak*) | White 3D print. Red virtual callouts mark end-nodes (Fig 14). |
| Dimensionality | **3D** | A 3D-printed 3D layout (§3.1, Figs 1 right, 14, 15). |
| Geometric Pose | **Rotation** | The user turns the network holder in the non-dominant hand (§3, §5.6). |
| Anchoring | **Phys. Anchor** | The callouts are registered to the tracked 3D print and holder (Polhemus plus calibration rig, §5.2, Fig 15). |
| Network Representation | **Node-link** | |
| Graph Layout | **Node Pos.** | |
| Input Modality | **Tangible** | The tracked network holder. Finger touches on the print (marking nodes, tracing paths, §5.6) are not sensed by the system, so Touch is not coded. |
| Interaction Target | **Phys. Elem.** | The printed network and holder. |
| Operation | **Arrange**, *Select (prototype only)* | Arrange: reorienting the print. Fig 13 shows a prototype AR3DHilite with virtual highlighting of physical edges via a mouse cursor. It was dropped because tracking was not accurate enough (§5.1), so Select is optional. |

**Verdict: HIGH** (for the Physicalization or AR group). It is the only *3D* network physicalization; HoloGraphs and NODKANT are both 2D. It is also a tracked, AR-augmented physical network like Belcher and HoloGraphs, and a strong TVCG reference for 2D versus 3D in VR. Its VR part also supports the claim that "in VR, 2D appears as a comparison condition". It is single-layer, but so are several current Table-2 rows (Kwon, VRNetzer, Belcher, NODKANT).

---

## 7. hapticphys: Haptic and Visual Comprehension of a 2D Graph Layout Through Physicalisation

**Bibliographic facts:** Adam Drogemuller, Andrew Cunningham, James Walsh, James Baumeister, Ross T. Smith, Bruce H. Thomas (University of South Australia). CHI '21, Yokohama, ACM. Full paper, 16 pages. DOI 10.1145/3411764.3445704.

**Platform:** **Physicalization** (3D-printed 2D node-link graphs), with a desktop "graphical-only" control condition on a monitor without interaction (§4.1).

**Network data / layers:** Single-layer subgraphs of 16–24 nodes from the REED98 Facebook network (§4.5). No layers.

**Coding** (physical conditions)
| Subdimension | Values | Justification |
|---|---|---|
| Visual Encoding | *Shape (weak)* | Cube and diamond shapes mark the path-task target nodes among spheres; they were chosen to be distinguishable by touch (§3.3, §4.2). Blue nodes and white edges are uniform styling, not data encoding (§3.3), so Color is not coded. |
| Dimensionality | **2D** | "graphs were arranged in 2D space along an x and y axis with physical 3D formed edges" (§3.3). The title says "2D Graph Layout". |
| Geometric Pose | **Rotation** | In visual-haptic, participants "were allowed to pick it up" (§4.1) and could "rotate when the initial shape put me off" (§6.5). Pinch and pick-up behaviour was coded (§4.4.3, Fig 3). |
| Anchoring | **Phys. Anchor** | The visualization is a physical object, consistent with how NODKANT and HoloGraphs are coded. |
| Network Representation | **Node-link** | |
| Graph Layout | **Node Pos.** | Fruchterman–Reingold layout with edge-to-edge repulsion to maximise angular resolution (§3.2, Fig 2). The pilot also tested orthogonal and circular layouts (§3.1). |
| Input Modality | **Tangible** | The physical graph is held and manipulated by hand (§4.1, Figs 1c–d, 3). |
| Interaction Target | **Phys. Elem.** | |
| Operation | **Arrange** | Picking up and reorienting the print (§6.2, §6.5). Finger pointing and contour following (§4.4.3) are cognitive offloading, not a system Select. |

**Verdict: MEDIUM (supplement).** It is the first controlled study of graph physicalization and closely parallels NODKANT (2D physicalization, Tangible, Phys. Elem., Arrange), but it adds no new value to the Physicalization group. Cite it in the text on haptic exploration.

---

## Summary table
| Key | Platform | Verdict | Codes (solid; *weak* in italics) |
|---|---|---|---|
| vmv_layer2d25d | VR | HIGH | Color, Size, 2D, Floating, Separated, Node-link, Node Pos., Shared; *Tangible, Virt. Elem., Filter* (joystick scroll) |
| detangler | Desktop | MEDIUM | Color, Size, Shape, 2D, Rotation, Scale (Fig 7 menu), Merged, Node-link, Node Pos., Aggregated, Virt. Elem., Select; *Filter* |
| multistory | Desktop | LOW–MEDIUM | Color, Size (fig), 2D, Merged, Linked, Node-link, Node Pos., Aggregated, Virt. Elem., Select, Filter; *Independent* |
| hybridmln | Desktop (poster) | LOW | Color, 2D, Linked, Hybrid, Node Ord., Mixed |
| mira | Desktop | MEDIUM | Color, Size, 2D, Separated, Linked, Merged, Node-link, Node Pos., Aggregated, Shared, Virt. Elem., Select, Filter; *Scale, Arrange* |
| pathtracing | VR + augmented physicalization | HIGH | VR: 2D, 3D, Rotation, Scale, Floating, Node-link, Node Pos., Tangible, Virt. Elem., Arrange, Select (*Color*). Phys/AR: 3D, Rotation, Phys. Anchor, Node-link, Node Pos., Tangible, Phys. Elem., Arrange (*Select prototype*) |
| hapticphys | Physicalization (+ desktop control) | MEDIUM | 2D, Rotation, Phys. Anchor, Node-link, Node Pos., Tangible, Phys. Elem., Arrange; *Shape* |

Notes for the main paper:
- If vmv_layer2d25d goes into Table 2, "only two VR systems address several layers or networks" becomes three. The claim "no work arranges several 2D layers freely in space" gains direct support from its participants' requests and future work (pp. 5–7).
- No new desktop work adds a desktop-new value cleanly. The only candidate is MultiStory's *Independent*, which is weak.
- Two DOIs need checking: MultiStory (no DOI in the PDF) and Path Tracing (the TVCG DOI is not in the arXiv version).

# Coding of 8 candidate works (AR / tangible / physical batch)

Scheme: coding_brief.md, calibrated against table2_codes.json (26 works). I read every paper's text in full and looked at every page image that has a figure. One exception: Tangible BioNets has only pp. 1–12 rendered, so Figs. 6–8 (pp. 13–15) were judged from their captions and the text.
Notation: page = PDF page (pNN image). A **(weak)** tag means the support exists but is thin, so drop the code if you want strict coding. Grey cells (platform rules) are never coded.

---

## 1. magiclens — Collaborative Magic Lens Graph Exploration

**Bibliographic facts**
- Authors: Daniel Drochtert, Christian Geiger (Univ. of Applied Sciences Düsseldorf)
- Venue: SIGGRAPH Asia 2015 Symposium on Mobile Graphics and Interactive Applications (SA'15 MGIA), Kobe, 2015
- Type: short paper / extended abstract ("work in progress", p.1). 3 pages: 2 pages of text plus 1 page with Fig. 1
- DOI: 10.1145/2818427.2818465

**Platform:** AR, handheld video see-through ("magic lens" phones/tablets, Unity + Metaio). Tablets lie on a table as AR tracking targets, and each tablet stands for a seed node (Abstract, Sec. 3).

**Network data:** Yes, a node-link graph of the Wikipedia link structure (p.1). It is a single network. Up to four tablet seeds each grow a subgraph of the same graph (Fig. 1: "Language, Mathematics, Human"), so there are no layers.

**Codes**
| Subdimension | Values | Justification |
|---|---|---|
| Visual Encoding | Size, Color (weak) | Sec. 4: "options to change the visualisation of nodes and edges based on the weight of the nodes" (betweenness, PageRank). Fig. 1 shows the seed-term labels much larger. Color: seed/selected nodes are red with yellow labels, other nodes cyan (Fig. 1). This is role/state colour, not stated as an encoding. |
| Dimensionality | 3D | Graph "in 3D" in mixed-reality space (Intro), with an octree layout computed in 3D (Sec. 4). Fig. 1 shows depth spread. |
| Geometric Pose | – | Users navigate by physically moving the device (Sec. 3). The visualization itself is not rotated or scaled. |
| Anchoring | Phys. Anchor | The graph is registered to the tablets on the table as tracking targets (Abstract, Sec. 3). After a long tap, a subgraph is re-registered to the handheld device (device-anchored, not Floating). |
| Layer Coupling | n/a | Single network. |
| Network Repr. | Node-link | Fig. 1. |
| Graph Layout | Node Pos. | "force-directed layout algorithm" (Sec. 3) and an octree-based GPU layout (Sec. 4). Collapse/expand is coded as Filter, not Aggregated. |
| Layer Repr. | n/a | |
| Input Modality | Touch, Tangible | Touch: tap selects, long tap detaches, double-tap collapses/expands (Sec. 3). Tangible: after a long tap, the subgraph "moves along under the users magic lens", so the handheld's pose is the input (Sec. 3). |
| Interaction Target | Virt. Elem., Phys. Elem. (weak) | Virtual: tapping nodes. Physical: users configure each physical tablet "node" with a database term (Sec. 3), but moving the tablets is not described. |
| Operation | Select, Filter, Arrange | Select: tap shows the term and highlights incident edges. Filter: collapse/expand branches. Arrange: the detached subgraph is carried by the device (all Sec. 3). |

**Verdict: HIGH (borderline MEDIUM).** It is one of very few handheld-AR network systems. Physical tablets act as node-level anchors, and it combines touch with device-pose (tangible) input on a physically anchored 3D graph, with multiple users. It adds a second early handheld-AR data point alongside Belcher. It is only an extended abstract with no evaluation, and it shows a single network.

---

## 2. egocentric_ar — Mobile Situated Analytics of Ego-Centric Network Data

**Bibliographic facts**
- Authors: Mingqian Zhao, Yijia Su, Jian Zhao, Shaoyu Chen, Huamin Qu (HKUST; FXPAL)
- Venue: SIGGRAPH Asia 2017 Symposium on Visualization (SA'17), Bangkok, 2017
- Type: full paper, 8 pages
- DOI: 10.1145/3139295.3139309

**Platform:** AR, handheld video see-through ("rendered via a see-through video on the screen", Sec. 4). The app runs on an iPhone 7 Plus with face recognition and tracking. Only the AR view is situated. The MDS, Storyline and Table views are ordinary 2D phone screens (Sec. 6).

**Network data:** Yes, a dynamic ego-centric co-authorship network (DBLP). It is **not shown as node-link** anywhere:
- AR view: a donut glyph per ego per year overlaid on the person's face (Sec. 6.1, Fig. 1a, Fig. 2b).
- MDS view: a scatterplot of egos.
- Storyline: an alter timeline.
- Matrix: the Storyline *thumbnail* is a matrix heat map of tie strength between selected egos (Sec. 6.5, Fig. 6d). This is a true adjacency matrix, but it sits in screen-space UI and is not registered in AR.

Time slices (years) are browsed through the glyph timeline.

**Codes**
| Subdimension | Values | Justification |
|---|---|---|
| Visual Encoding | Color, Size | Donut: categorical colour for 4 alter types. Donut width = number of 1-degree alters, ring radius = number of 2-degree alters (Sec. 6.1). Sequential colour in the matrix thumbnails (Sec. 6.5, Fig. 6). |
| Dimensionality | 2D | Glyphs, scatterplot and matrices are all planar (Figs. 1–6). |
| Geometric Pose | – | Zoom in the MDS view scales a scatterplot, not a network. Not coded. |
| Anchoring | Phys. Anchor | The glyph is "directly overlaid … over human faces" and tracked in real time (Sec. 6.1, Fig. 2: printed photo). |
| Layer Coupling | Separated (weak) | Yearly ego-network summaries appear as a vertical stack of glyphs (Fig. 1a, "rotate the horizontal timeline to a vertical one", Sec. 6.1). The Storyline links alters across timestamps, but it is not a network representation, so Linked is not coded. |
| Network Repr. | Matrix | Storyline thumbnail: "each cell … encodes tie strengths between chosen egos" (Sec. 6.5, Fig. 6d). |
| Graph Layout | Aggregated | The ego network is abstracted into a count glyph (donut + ring = alter counts, Sec. 6.1). No matrix ordering algorithm is described. |
| Layer Repr. | – | Not applicable (no repeated network representation per slice). |
| Input Modality | Touch | Finger sliding along the timeline, tapping thumbnails, double-tap to deselect (Secs. 6.1–6.4). |
| Interaction Target | Virt. Elem. | Glyphs, MDS dots, table rows. |
| Operation | Select, Filter (weak) | Select: egos are highlighted in categorical colour (Sec. 6.2, Fig. 3). Filter: the timeline sets the timestamp for the whole system (Sec. 6.1). |

**Verdict: LOW.** The AR component is a single glyph on a face, not a network visualization. The one matrix is a 2D screen-space thumbnail, so it does not count as "matrix in AR". Cite it only as situated-analytics context.

---

## 3. datar — DatAR: Comparing Relationships between Brain Regions and Diseases

**Bibliographic facts**
- Authors: Ghazaleh Tanhaei, Lynda Hardman, Wolfgang Hürst (Utrecht Univ.; CWI)
- Venue: ACM IMX '23, Nantes, 2023
- Type: demo paper ("In the demo", Sec. 3). 3 pages, pp. 373–375
- DOI: 10.1145/3573381.3597222

**Platform:** AR, HMD optical see-through (HoloLens 2, Unity + MRTK, Sec. 4).

**Network data:** Not really. The data is a knowledge graph of brain-region–disease co-occurrences, i.e. a bipartite relation:
- It is shown as **two 3D brain point clouds** (region centres from an atlas), one per disease, with affected regions highlighted as pink spheres (Fig. 1, Fig. 2).
- There are **no edges between regions**.
- The lines between cubes in Figs. 1–2 belong to the visual-programming dataflow widgets (query → brain → comparison widget). They are UI pipeline links, not data edges.

**Codes**
| Subdimension | Values | Justification |
|---|---|---|
| Visual Encoding | Color | Affected regions in pink, others teal (Fig. 1 caption). |
| Dimensionality | 3D | Region spheres sit at anatomical 3D positions (Sec. 4, Figs. 1–2). |
| Geometric Pose | – | Not described. |
| Anchoring | Floating | The brains hang freely in the room (Fig. 1). No registration to a physical object. |
| Layer Coupling | Separated (weak) | Two disease "views" side by side, with Intersection/Union/Difference applied to both (Sec. 3). This counts only if the two brains are read as layers of a bipartite network. |
| Network Repr. | – | No node-link or matrix of the data. |
| Graph Layout | – | Positions come from an anatomical atlas, not a layout algorithm. |
| Layer Repr. | (Shared, weak) | Both brains use identical region positions (Fig. 1). Applies only under the layer reading. |
| Input Modality | Mid-air | HoloLens 2 hand ray/pinch on widgets (Fig. 2 shows the hand pressing). The text does not name the modality. |
| Interaction Target | Virt. Elem. | Comparison-widget buttons and dataflow cubes (Fig. 2). |
| Operation | Filter | Intersection/Union/Difference change which regions are highlighted (Sec. 3). |

**Verdict: LOW (exclude).** It has no network representation, only set highlighting on anatomical point clouds, and the visible links are a UI dataflow. At most, mention it as AR biomedical related work.

---

## 4. mindmap — Tangible AI Mind-map

**Bibliographic facts**
- Full title: Tangible AI Mind-map: A Graph-Based Interface for Human-AI Brainstorming using Projection-Based AR, Gesture Recognition and Large Language Models
- Authors: Alexander Htet Kyaw, Yifei Li, Jin Gao, Maggie Chao, Keyi Zhang, Yudian Xu, Hiroshi Ishii (MIT CSAIL/EECS/Media Lab; Harvard)
- Venue: SIGGRAPH Posters '26, Los Angeles, 2026
- Type: poster abstract, 3 pages
- DOI: 10.1145/3799825.3818764

**Platform:** AR, projection-based on a tabletop ("tabletop AR projection", Sec. 1). The network is rendered in d3/React and projected onto the table (Sec. 2). There are no physical tokens despite the word "Tangible" in the title.

**Network data:** Yes, a semantic idea graph: nodes are LLM-extracted keywords, links are semantic relations (Sec. 2). It is a single network that grows over time.

**Codes**
| Subdimension | Values | Justification |
|---|---|---|
| Visual Encoding | Color (weak) | Nodes have differently coloured glows (blue/red/green/yellow, Figs. 1, 4). The text mentions clustering but does not state the colour mapping. |
| Dimensionality | 2D | "arranged into a two-dimensional network" (Abstract), from t-SNE 2D (Sec. 2). |
| Geometric Pose | – | |
| Anchoring | Phys. Anchor | Projected onto and registered with the tabletop (Fig. 1). This matches how TangibleNet is coded for a tabletop. |
| Layer Coupling | n/a | |
| Network Repr. | Node-link | Figs. 1, 4. |
| Graph Layout | Node Pos. | Positions come from a t-SNE projection of sentence embeddings (Sec. 2, Fig. 2). |
| Layer Repr. | n/a | |
| Input Modality | Touch, Voice | Touch: "single long press on a node" and two-node selection on the projected table surface, detected by camera hand tracking (Sec. 2, Fig. 4 shows the finger pressing the table). Code Mid-air as well if contact detected by a camera counts as gesture. Voice: speech is the input that creates nodes and the graph (Abstract, Sec. 2). It is content authoring, not a command on the visualization. |
| Interaction Target | Virt. Elem. | Projected nodes. |
| Operation | Select | One node → elaborate; two nodes → bridging idea (Sec. 2, Fig. 4). Importance-score filtering is automatic, not a user operation. |

**Verdict: MEDIUM, conditionally HIGH.** It is a projection-AR tabletop network with touch input. It would be the only AR row with **Voice**, but here voice drives graph *construction* (speech → nodes), not interaction with the visualization. Include it if the paper wants to fill the AR×Voice cell and can carry that caveat. The poster has no study beyond a self-study.

---

## 5. semanticreality — Semantic Reality

**Bibliographic facts**
- Full title: Semantic Reality: Interactive Context-Aware Visualization of Inter-Object Relationships in Augmented Reality
- Authors: Xiaoan Liu, Eric J. Gonzalez, Nels Numan, Andrea Colaço, Lucy Abramyan, Chen Zhu-Tian, Ryo Suzuki, Mar Gonzalez-Franco (Google; U. Minnesota; CU Boulder)
- Venue: arXiv preprint arXiv:2604.05265v1, 6 Apr 2026. The ACM template has no venue filled in
- Type: full paper, 15 pages including appendix
- DOI: placeholder only (none assigned). Cite by arXiv ID

**Platform:** AR, HMD video see-through (Apple Vision Pro passthrough; Unity/PolySpatial/RealityKit, Secs. 4.1.1, 4.3).

**Network data:** Yes, a typed, attributed "semantic graph":
- Nodes are detected physical objects plus the user; edges are typed inter-object relations (Sec. 3.1, Fig. 2 right).
- There are **8 relation types**: spatial, structural, similarity, comparison, affordance, compatibility, procedural, causality (Sec. 3.3, Fig. 3). Over one node set this is in effect a **multiplex (multi-edge-type) network**, although the paper never calls it layers.
- Edges are drawn as in-situ connectors between the real objects (Figs. 1, 2, 5, 7).

**Codes**
| Subdimension | Values | Justification |
|---|---|---|
| Visual Encoding | Color, Shape, Texture | Color: selected/target nodes cyan vs white (Figs. 3, 5); user-initiated relations drawn "with stronger emphasis" (Sec. 4.4). Shape: each relation type maps to a different primitive — labels, midline cards, directional connectors with arrowheads, numbered steps, ribbons (Sec. 4.3, Fig. 3). Texture: compatibility uses solid lines (compatible) vs dashed lines (incompatible) (Fig. 3). |
| Dimensionality | 3D | Nodes keep the objects' real 3D world poses (Sec. 4.1.1). Spatial relations are drawn along 3D axes (Fig. 3, "spatial"). |
| Geometric Pose | – | The graph is embedded in the world and is not rotated or scaled as a whole. |
| Anchoring | Phys. Anchor | Every node is "scene-anchored" to a physical object by raycasting into the scene mesh (Sec. 4.1.1, Fig. 4A). |
| Layer Coupling | Merged | Several relation types share one in-situ view and are told apart only by encoding (Sec. 4.3). In practice only 1–2 types are active at a time (Sec. 6.1). This counts only if edge types are read as multiplex layers. |
| Network Repr. | Node-link | Figs. 1, 2, 7 (right). |
| Graph Layout | – | Node positions are the physical object positions, so there is no layout algorithm (same as Belcher and Lee '22). Similarity "visual clustering" with a shared-attribute label (Fig. 3, Fig. 13) is close to aggregation but is not coded. |
| Layer Repr. | (Shared, optional) | All relation types share the physical node positions. Following MultiNets/VERTIGo (Merged, no layer representation), I leave it blank. |
| Input Modality | Gaze, Mid-air, Voice, Tangible | Gaze: gaze-directed selection and gaze sweep (Sec. 4.4.1, Fig. 5A–B). Mid-air: pinch to confirm, swipe gesture (Sec. 4.4.1). Voice: spoken requests such as "compare these" that pick the relation type (Sec. 4.4.2, Fig. 5C). Tangible: grabbing a real object, which the node follows, and aiming a held object at another to form a pair (Sec. 4.4.3, Fig. 5D–E). |
| Interaction Target | Phys. Elem., Virt. Elem. | Physical: grasped and held objects (Sec. 4.4.3). Virtual: node anchors selected by gaze-pinch, plus confirmation UI (Secs. 4.2.3, 4.4.1). Spatial Ctx is not coded: the scene mesh and the body-proximity band are used by the system, not manipulated by the user. |
| Operation | Select, Filter, Arrange | Select: multi-selection (Sec. 4.4.1). Filter: the context window shows only the active subgraph, edges are ephemeral and decay, and voice picks which relation to surface (Secs. 4.1.2, 4.3, 4.4.2). Arrange: moving a physical object moves its node (Sec. 4.4.3). |

**Verdict: HIGH.** It is a strong AR row:
- It is the only work in this batch, and new to the AR group, with **Gaze + Voice + Tangible + Mid-air** on a **physically anchored network** in an HMD.
- Its typed relations give a multiplex, Merged representation in AR.

It changes the AR gaze/voice gap: so far only Personal+Context has Gaze, and Voice appears only in the VR work by Lee et al. '26. Caveats: it is an object knowledge graph rather than analytic network data, and it is an arXiv preprint.

---

## 6. nodebots — NodeBots

**Bibliographic facts**
- Full title: NodeBots: Physicalizing Network-Based Data with SwarmUIs
- Authors: Ramarko Bhattacharya, Alan Pham, Ken Nakagaki (Univ. of Chicago)
- Venue: UIST Adjunct '26, Detroit, 2026
- Type: adjunct poster/demo abstract, 3 pages
- DOI: 10.1145/3830397.3842445

**Platform:** Physicalization (actuated). Nodes are toio swarm robots on a mat, and edges, labels and icons are **projected** from overhead (Sec. 2.2–2.3, Figs. 2–4). It is a physicalization/projection hybrid. Nodes are physical, so it belongs with HoloGraphs and NODKANT.

**Network data:** Yes, weighted node-link networks (UChicago research areas/researchers, US airports). There are **multiple networks**, swapped one at a time (Sec. 2.1.3, Fig. 3):
- "Data Layers": two different networks at two hierarchy levels.
- "Data Views": two edge sets (planes vs buses) on the same nodes, i.e. a multiplex network.

**Codes**
| Subdimension | Values | Justification |
|---|---|---|
| Visual Encoding | Color | Projected edges and nodes are coloured per view (Fig. 3b: yellow-green planes vs purple buses). The shortest path is highlighted (Fig. 4b). Edge weights appear as text only (Sec. 2.1.1). |
| Dimensionality | 2D | Robots on a planar mat. |
| Geometric Pose | – | |
| Anchoring | Phys. Anchor | Nodes are the robots, and projection is registered to them (Sec. 2.2). |
| Layer Coupling | Separated | Layers and views are swapped in time, with no inter-layer links (Sec. 2.1.3, Fig. 3). |
| Network Repr. | Node-link | Figs. 2–4. |
| Graph Layout | Node Pos. | Eades force-directed simulation that drives the robots (Sec. 2.2). |
| Layer Repr. | Mixed | Same node-link representation. Each view's edge set yields a different force equilibrium (Fig. 3b shows different arrangements for planes vs buses). |
| Input Modality | Tangible | Push/pull robots with haptic resistance, short/long press on the robot button (Sec. 2.1, 2.2). |
| Interaction Target | Phys. Elem., Spatial Ctx. | Physical: the robots. Spatial Ctx: physical barriers and constraints (sticks/rulers placed on the mat, Fig. 2, Fig. 4a) become computational constraints that partition or limit the layout (Sec. 2.1.2). |
| Operation | Arrange, Select | Arrange: Separation, Clustering, Rearrangement (Sec. 2.1.2). Select: press nodes, "two selected nodes" for shortest path (Sec. 2.2, Sec. 3.1). Barriers partition the layout rather than hiding elements, so Filter is not coded. |

**Verdict: HIGH (for the Physicalization group).** It is the first actuated, dynamic force-layout network physicalization. It shows multiple networks/views (Separated + Mixed) and is the only physicalization using **Spatial Ctx**: physical barriers act as layout constraints. It is a short adjunct paper with no evaluation.

---

## 7. tangiblebionets — Tangible BioNets

**Bibliographic facts**
- Full title: Tangible BioNets: Multi-Surface and Tangible Interactions for Exploring Structural Features of Biological Networks
- Authors: Roozbeh Manshaei, Sean DeLong, Uzair Mayat, Dhrumil Patal, Matthew Kyan, Ali Mazalek (Ryerson; York Univ.)
- Venue: Proceedings of the ACM on Human-Computer Interaction, Vol. 3, EICS, Article 14 (June 2019)
- Type: full journal paper, 22 pages
- DOI: 10.1145/3331156

**Platform: not AR, not physicalization.**
- **Setup:** networks are drawn as force-directed graphs on a 12-tile 2D wall display ("iWall") in four colour-coded containers per workspace, up to 8 shown (Sec. 5.3.2, Figs. 1, 4, 5).
- **Controls:** active tangibles ("actibles") on a multi-touch tabletop serve only as handles, menus and query tokens. Tablets show plots.
- **Why it is not a physicalization:** the tangibles are not a physical form of the network.
- **Classification:** the nearest group is **Desktop**, as a non-immersive screen visualization with multi-surface control. Under the grey rules, Desktop leaves out its whole tangible/touch interaction, which shows the scheme does not cover TUI-on-screen systems.

**Network data:** Yes, BioGRID gene-interaction networks for several organisms, **multiple networks juxtaposed** for comparison: the same organism with different structural features, or different organisms with the same feature (Sec. 5.2, 5.3.2).

**Codes (Desktop group; grey cells omitted)**
| Subdimension | Values | Justification |
|---|---|---|
| Visual Encoding | Color, Size | Container and organism colours carry over between actible LEDs and the wall (Sec. 5.3.2). Applying a feature changes "node radius, changing color" (Sec. 5.2, 5.3.2; e.g. node size by betweenness). |
| Dimensionality | 2D | Fig. 4. |
| Geometric Pose | – | |
| Anchoring | (grey) | |
| Layer Coupling | Separated | Up to 4–8 networks side by side in containers, with no inter-network links (Sec. 5.3.2, Fig. 2d(iii), Fig. 4). |
| Network Repr. | Node-link | "visualized … as a force-directed network" (Sec. 5.3.2). |
| Graph Layout | Node Pos. | Force-directed with D3 (Sec. 6.2). |
| Layer Repr. | Mixed | Same representation, with an independent force layout per organism network (Fig. 4). |
| Input Modality | (grey) | *If ungreyed:* Tangible (bump, stack, shake actibles) and Touch (tabletop donut menus, actible screen) (Sec. 5.1, Fig. 2). |
| Interaction Target | – | Users manipulate menus and tokens, not nodes or edges. *If ungreyed:* Phys. Elem. (actibles). |
| Operation | Select | Choose organisms and network types, then apply features to containers (Sec. 5.3). |

**Verdict: LOW (exclude from Table 2).** It is not AR and the network is not physical: a wall-display network driven by tangible tokens. It is useful in the text as a multi-network comparison precedent with tangible control.

---

## 8. sparsetangibles — Sparse Tangibles

**Bibliographic facts**
- Full title: Sparse Tangibles: Collaborative Exploration of Gene Networks using Active Tangibles and Interactive Tabletops
- Authors: Ahmed Sabbir Arif, Roozbeh Manshaei, Sean DeLong, Brien East, Matthew Kyan, Ali Mazalek (Ryerson; York; Georgia Tech)
- Venue: TEI '16, Eindhoven, 2016, Demos and Posters track (page header)
- Type: demo/poster paper, 9 pages (pp. 287–295)
- DOI: 10.1145/2839462.2839500

**Platform: not AR, not physicalization.**
- **Setup:** an interactive tabletop (DSI display) with smartwatch active tangibles (Sec. Technical Implementation). Networks are drawn *on the table display* around the tangible.
- **Tangible link:** the donut chart and force-directed graphs "follow their associated active tangibles as they are moved around the tabletop" (p.290), so they are registered to a tracked physical token.
- **Why it is neither group:** it is a tangible tabletop. The network is pixels on a horizontal screen, not physical, and there is no see-through or projection AR.
- **Classification:** if forced, the closest group is a screen-based Desktop. But it really uses Phys. Anchor, Tangible and Touch, which Desktop greys out. Sparse Tangibles and Tangible BioNets together point to a missing "tangible tabletop" group in the scheme.

**Network data:** Yes, BioGRID gene/protein interaction networks. Several networks of an organism are shown at once around the chart (Fig. 3, Fig. 4), and several tangibles let users compare networks (p.290).

**Codes (full, ignoring Desktop greying; grey-sensitive cells marked)**
| Subdimension | Values | Justification |
|---|---|---|
| Visual Encoding | Color | Each network gets a random colour, and doughnut slices are shades of green (p.290). Edges below the agreement threshold are greyed out (Fig. 6b). Slice arc length encodes network density, but that is a donut chart, not the network. |
| Dimensionality | 2D | Figs. 3, 4, 6b. |
| Geometric Pose | – | Turning the tangible like a dial magnifies the donut menu but does not rotate the graph (Fig. 2). |
| Anchoring | Phys. Anchor *(grey if Desktop)* | Graphs follow the tracked tangible on the table (p.290). |
| Layer Coupling | Separated | Several networks juxtaposed, no inter-network links (Fig. 3, p.290). |
| Network Repr. | Node-link | Fig. 3. |
| Graph Layout | Node Pos. | Force-directed, "charged particles and springs" (p.290). |
| Layer Repr. | Mixed | Each network has its own force layout (Fig. 3). |
| Input Modality | Tangible, Touch *(grey if Desktop)* | Tangible: place, dial, stack (query AND), shake (reset). Touch: tap/swipe/slider on the smartwatch, tap on the table slices (pp. 289–291, Figs. 1, 2, 5, 6a). |
| Interaction Target | Phys. Elem. *(grey if Desktop)*, Virt. Elem. | Physical: the tangibles. Virtual: tapping donut slices, i.e. networks (p.291). |
| Operation | Select, Filter, Arrange | Select: pick organism/gene/network (Step 2). Filter: agreement-score threshold greys out edges (Fig. 6), and selecting removes the other networks (p.291). Arrange: networks move with their tangibles (p.290). |

**Verdict: LOW (exclude from Table 2; cite as related work).** It has no AR and the network is not physical. It is a clear precedent for tangible tokens anchoring network views on a tabletop and for tangible stacking as a filter. If the paper widens Physicalization to "tangible/tabletop", it would become MEDIUM.

---

## Cross-cutting notes for the main paper
- **Tangible input + physically anchored network in AR:** magiclens (device pose; tablets as anchors) and Semantic Reality (grab/aim real objects that are nodes). NodeBots has this too, in Physicalization.
- **Gaze / Voice:** Semantic Reality has Gaze + Voice in HMD AR, the strongest new evidence. Mindmap has Voice in projection AR, but only for building the graph.
- **Touch / mid-air in AR on networks:** magiclens (touch, handheld). Mindmap (touch on the projected table; mid-air if read loosely). Semantic Reality (mid-air pinch/swipe). DatAR has mid-air but no network.
- **Several layers/networks in AR:** only Semantic Reality, if its typed relations are read as multiplex layers (Merged). Among the non-AR works, NodeBots shows them in Physicalization (Separated/Mixed); Tangible BioNets and Sparse Tangibles show them on screens/tables (Separated/Mixed).
- **Matrices in AR:** none truly. Egocentric AR's matrix thumbnails are 2D screen-space UI inside an AR app, not registered in the scene.
- **2D layers in immersive space:** none in this batch. Mindmap's 2D graph is projected onto a physical surface (Phys. Anchor), not floating.
- **Scheme gap:** Tangible BioNets and Sparse Tangibles (tangible tabletop + screen network) fit neither Desktop (whose greying removes their interaction) nor Physicalization.

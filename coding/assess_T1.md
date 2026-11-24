# Table 1 candidate assessment (MLN_EuroVis2027 (2).tex, tab:related_work)

## 0. Current state of the paper (checked)

Table 1 columns are AR, VR, N, MLN, DS. Current coding:

| Row | AR | VR | N | MLN | DS |
|---|---|---|---|---|---|
| McGee et al. STAR (state_of_the_art) | | | | Y | Y |
| Joos et al. (joos2025...) | Y | Y | Y | | Y |
| Saffo et al. (10296039) | Y | Y | | | Y |
| Klein et al. (KleinSedlmairSchreiber; "Immersive analytics: An overview", it-IT 64(4-5), 2022) | Y | Y | Y | | Y |
| Lee et al. '24 (10297565, situated AR design patterns) | Y | | | | Y |
| Lee et al. '22 (Lee2022, 2D<->3D transformations in MR) | Y | | Y | | Y |
| Büschel et al. (8636208) | Y | | Y | | Y |
| TangibleNet (Takahira2025tangiblenet) | Y | | Y | | Y |
| This work | Y | | | Y | Y |

How the text uses the rows:
- RW 2.1: McGee = comprehensive MLN survey.
- RW 2.2: Joos = "recent surveys indicate growing interest ..."; Büschel = AR edge design space; TangibleNet = magnets on whiteboard. Kraus et al. (key `14430`) is ALREADY cited in the intro ("spatial memory") and RW 2.2 (motivation list `Korkut2023, 14430, 7390081, ...`), but not in Table 1 or the positioning paragraph.
- RW 2.3: Lee '22, Saffo, Lee '24 "intentionally general and do not address layers, inter-layer relationships, or MLN tasks."
- Summary and positioning: "surveys of immersive and immersive network visualization [Joos, Saffo, Klein], and design spaces for AR visualization and AR network techniques, which address single networks [Lee'24, Lee'22, Büschel, TangibleNet]. No design space yet integrates AR with multilayer structure".
- Method/Process: "introducing new subdimensions where none fitted, namely Anchoring, Layer Coupling, and Layer Representation"; Anchoring is described as "related to the surface relation of Lee et al."
- Discussion, Relation to existing design spaces: "No existing space covers both MLN structure and AR. ... Our new subdimensions, Anchoring, Layer Coupling, and Layer Representation, treat layers as physical entities whose relations can be manipulated."

None of the eight candidates except Kraus is currently cited (checked against all cite keys in the tex and against references_clean_v2.bib).

Minor consistency note: "This work" and McGee have N blank while MLN is checked. If N means "network visualization", MLN implies N, so a reviewer could read the blank N as an error. Either tick N for both or redefine N in the caption as "single-layer network".

---

## 1. Zollmann et al. 2020: Visualization Techniques in Augmented Reality: A Taxonomy, Methods and Patterns

1. Bibliographic facts: S. Zollmann, T. Langlotz, R. Grasset, W. H. Lo, S. Mori, H. Regenbrecht. IEEE TVCG 27(9):3808-3825, 2021 (early access 2020). DOI 10.1109/TVCG.2020.2986247 (from memory, so verify; the extracted text has no DOI). Type: journal survey and taxonomy, about 18 pages.
2. Coding: AR Y, VR -, N -, MLN -, DS Y. Justification: the survey is AR-only and explicitly excludes VR work. It also excludes "standard information visualization in AR without any specifics to AR". The words graph/network appear only in references. Its "layers" are compositing layers (camera image and virtual content), not data layers.
3. Dimensions: Purpose (visual coherence, depth perception, clutter reduction, exploration, attention), Virtual Data Visibility (occlusion/X-ray), Virtual Cues, Filtering, Abstraction, Compositing. These relate only weakly to our space: occlusion and depth cues bear on stacked 3D layers, and Filtering matches our Filter operation. The survey has no anchoring, input, or network dimensions.
4. Claims affected: none. "These works are intentionally general and do not address layers ..." remains true.
5. Verdict: SUPPLEMENT ONLY. At most one optional citation for depth cues and occlusion in AR.

## 2. Bressa et al. 2021/22: What's the Situation with Situated Visualization? A Survey and Perspectives on Situatedness

1. Bibliographic facts: N. Bressa, H. Korsgaard, A. Tabard, S. Houben, J. Vermeulen. IEEE TVCG 28(1):107-117, 2022 (IEEE VIS 2021). DOI 10.1109/TVCG.2021.3114835. Type: survey (44 papers using the term "situated visualization") plus a conceptual framework of five perspectives. 11 pages.
2. Coding: AR Y, VR (marginal, minor category), N -, MLN -, DS Y (survey plus conceptual perspectives). Networks appear only incidentally ("activist networks").
3. Dimensions: technology (AR, mobile, physicalization, display, analog, VR), data and visualization types, application domain. The five perspectives are space, time, place, activity, and community. The paper argues that most work adopts a purely spatial, technology-centric notion of situatedness. Relation to our space: our Anchoring and Spatial Context values are exactly this spatial or operational notion of situatedness.
4. Claims affected: none are false. The intro sentence "Situated AR visualizations display abstract data next to the physical referents they describe [White2009SiteLens, McGee2024radiation]" would benefit from Bressa (or Shin) as the canonical survey citation. A reviewer from this community could also note that our "situatedness" is spatial only. One clause in the AR discussion would cover this, e.g. "we address the spatial perspective of situatedness [Bressa]".
5. Verdict: CITE IN TEXT ONLY (intro, situated sentence).

## 3. Shin et al. 2023: The Reality of the Situation: A Survey of Situated Analytics

1. Bibliographic facts: S. Shin, A. Batch, P. W. S. Butcher, P. D. Ritsos, N. Elmqvist. IEEE TVCG, published online 2023 and in print in vol. 30(8), 2024. DOI 10.1109/TVCG.2023.3285546 (from memory, so verify DOI and pages; the extracted text is the preprint without a DOI). Type: systematic survey and taxonomy of 47 situated-analytics systems, with ensemble cluster analysis yielding four archetypes. About 18 pages.
2. Coding: AR Y, VR - (VR is mentioned only as context), N -, MLN -, DS Y. Network data appears only as one surveyed system ("SA for Network Data", 2017) and in their own clustering graph, so it is not a substantive part of the survey.
3. Dimensions (closest to our space of all candidates):
   - View Situatedness: World-registered (world-absolute = embedded; world-relative), Sticky, Device-anchored (device-relative; device-fixed/overlay). This is a finer-grained version of our Anchoring (Physical Anchor vs Floating). Our Physical Anchor (registered to a tracked substrate) corresponds to world-registered or object-relative. Our Floating corresponds to world-relative placement without a physical counterpart.
   - Situating Triggers: referents (location, object such as marker/object recognition) and context (event, setting). These relate to our Spatial Context target and to marker-tracked plates.
   - Data Depiction: visual encoding 2D (incl. 2.5D planes in 3D) / 3D / non-visual. This is analogous to our Dimensionality (2D layers in 3D space). Data abstraction: abstract / physical / hybrid.
   - Sensemaking tasks.
4. Claims affected:
   - "introducing new subdimensions where none fitted, namely Anchoring, Layer Coupling, and Layer Representation" (Method, Process) and "Our new subdimensions, Anchoring, Layer Coupling, and Layer Representation, treat layers as physical entities" (Discussion). Anchoring as a concept of how a view is bound to the world has a direct precedent in Shin's View Situatedness, alongside Lee '22's surface relation, which is already acknowledged. The novelty claim should be narrowed to "anchoring of network layers" or "layer-level anchoring". Suggested edit to the Anchoring definition: "related to the surface relation of Lee et al. and to view situatedness in situated analytics [Shin], which distinguishes world-registered from device-anchored views; we keep only whether a layer has a physical counterpart."
   - "No existing space covers both MLN structure and AR" and "No design space yet integrates AR with multilayer structure" remain TRUE.
5. Verdict: ADD TO TABLE 1. Row: AR Y, VR -, N -, MLN -, DS Y. It is the strongest AR taxonomy whose dimensions map onto Anchoring and Spatial Context. Add it to the positioning sentence "design spaces for AR visualization ... [10297565, Shin, Lee2022, ...]".

## 4. Cordeil et al. 2017: A Design Space for Spatio-Data Coordination: Tangible Interaction Devices for Immersive Information Visualisation

1. Bibliographic facts: M. Cordeil, B. Bach, Y. Li, E. Wilson, T. Dwyer. IEEE PacificVis 2017 (notes track), pp. 46-50. DOI 10.1109/PACIFICVIS.2017.8031578. Type: short design-space paper with sketches and early prototypes. 5 pages.
2. Coding: AR Y (HoloLens named as a target display for the Physical Axes prototype; AR systems such as CAPTIVE are classified), VR Y (HTC Vive prototypes), N - (graphs appear only in the generic InfoVis reference model and in one classified system, NaturalMotion, for time-evolving graphs), MLN -, DS Y.
3. Dimensions: interaction space size (hand/desktop/human), degree of interaction-space physicality (Non-physical / Physical), selection, navigation, menu interaction, data display, and input-output mapping (direct/indirect). Relation to our space:
   - Physicality N/P is essentially our Anchoring (Floating vs Physical Anchor), applied to the visualization space rather than to layers.
   - Its hand-held cutting planes, Paper Lens, and tangible cubes are close precedents for tangible layer plates and Tangible input.
   - Direct vs indirect mapping relates to our Interaction Target (Physical vs Virtual Elements).
   - Size relates to our ergonomics discussion ("Two hands can hold at most two plates").
4. Claims affected: the same two novelty sentences as for Shin. "introducing new subdimensions where none fitted, namely Anchoring ..." Physical anchoring of an immersive visualization to a tangible substrate is already a design-space dimension in Cordeil et al. The novelty is again layer-level anchoring within one network plus coupling between anchored layers. A further suggestion is a G5 or Discussion mention. The sentence "tangible input with physically anchored networks in AR in two works [Belcher2003, TangibleNet]" is about systems, so it stays true.
5. Verdict: ADD TO TABLE 1. Row: AR Y, VR Y, N -, MLN -, DS Y. It is the only immersive design space whose dimensions cover physicality and tangible devices, which are the core of our AR-specific values. If the user prefers fewer rows, the alternative is CITE IN TEXT in the Anchoring definition and the Process paragraph.

## 5. Kraus et al. 2022: Immersive Analytics with Abstract 3D Visualizations: A Survey

1. Bibliographic facts: M. Kraus, J. Fuchs, B. Sommer, K. Klein, U. Engelke, D. Keim, F. Schreiber. Computer Graphics Forum 41(1):201-229, 2022 (online 2021). DOI 10.1111/cgf.14430. Type: systematic survey of 58 papers with online browser (iasurvey.dbvis.de). 29 pages. Already in the bib as key `14430` and cited twice in the paper.
2. Coding: AR Y, VR Y, N Y, MLN -, DS Y. Networks are substantive: "Node-link graph" is one of eight technique classes, and node-link graphs plus scatterplots make up 39 of 58 papers, so roughly 15 papers are node-link. "Network" is one of four data types, and node-link graphs have their own sections (navigation, layout, provenance graphs, biology). Multilayer networks are never mentioned.
3. Dimensions: visualization technique, analysis task (synoptic/elementary), paper type, technology (monitor/projector, CAVE, HMD), environment (AR/VR), and data type (table/field/geometry/network). It has no anchoring, physical-input, or layer dimensions. It is useful as evidence that immersive node-link work exists without layers.
4. Claims affected: none are false. The positioning sentence "surveys of immersive and immersive network visualization [Joos, Saffo, Klein]" would naturally include Kraus. Its omission there is odd, since it is already cited and is the most-cited immersive survey covering graphs.
5. Verdict: CITE IN TEXT ONLY. Add `14430` to the survey group in "Summary and positioning". As a Table 1 row it would duplicate the Joos/Klein pattern exactly (AR, VR, N, DS). However, it is a STRONGER source than Klein et al., so it is the natural replacement if the Klein row is dropped (see recommendation).

## 6. Schöttler et al. 2021: Visualizing and Interacting with Geospatial Networks: A Survey and Design Space

1. Bibliographic facts: S. Schöttler, Y. Yang, H. Pfister, B. Bach. Computer Graphics Forum 40(6):5-33, 2021. DOI 10.1111/cgf.14198. Type: survey (95 papers) plus design space; online browser geonetworks.github.io. 29 pages.
2. Coding: AR -, VR - (VR appears only for 3D globes [YDJ*19], with one sentence on VR interaction), N Y, MLN - (cites McGee only), DS Y. It does not cover immersive environments.
3. Dimensions: GEO (mapped/distorted/abstract/none), NET:NODE and NET:LINK representations, COMP (juxtaposed/superimposed/nested/integrated), and INTERACT. The COMP spectrum from loose to tight integration of network and spatial reference is a conceptual analogue to our Anchoring/Spatial Context and to Layer Coupling. Its juxtaposed small multiples per time step are akin to layers.
4. Claims affected: none.
5. Verdict: CITE IN TEXT ONLY, optional. Possible places: Network Representation, or the Spatial Context discussion as the screen-based precedent for composing networks with a spatial reference. It is not "closest" work for Table 1.

## 7. Uhl et al. 2023: When Realities Interweave: Exploring the Design Space of Immersive Tangible XR

1. Bibliographic facts: J. C. Uhl, H. Schrom-Feiertag, G. Regal, L. Hirsch, Y. Weiss, M. Tscheligi. TEI '23 (studio proposal), Warsaw, ACM. DOI 10.1145/3569009.3571843. 4 pages.
2. Coding: AR Y, VR Y, N -, MLN -, DS - (in substance). Despite the title, it proposes a hands-on studio. It gives a short literature grounding (markers, Vive trackers, outcomes such as presence and performance) and a research question, but no design space with dimensions. It is not about visualization.
3. Dimensions: none formal. It supports, in general terms, the claim that tangibles in XR improve performance and engagement.
4. Claims affected: none.
5. Verdict: SUPPLEMENT ONLY. Better not cited at all, since a workshop proposal is weak support in a EuroVis paper.

## 8. Miller, Bhatia, Kobourov 2024: State of the Art of Graph Visualization in non-Euclidean Spaces

1. Bibliographic facts: J. Miller, D. Bhatia, S. Kobourov. Computer Graphics Forum 43(3), EuroVis 2024 STAR. DOI 10.1111/cgf.15113. Type: STAR, more than 60 papers, about 20+ pages.
2. Coding: AR -, VR - (VR is mentioned only for spherical layouts [KMLM16] and as an open problem), N Y, MLN - (multilayer appears only as an open problem), DS Y (categorization by geometry, contribution, graph class).
3. Dimensions: geometry (spherical/hyperbolic/toroidal), contribution type, and graph class. These are relevant only to our Graph Layout values (e.g., spherical layouts in VR).
4. Claims affected: none. It explicitly lists "Multi-layer/dynamic/hypergraph visualization in non-Euclidean spaces" and "Virtual reality techniques ... for non-Euclidean geometries" as open problems, which mildly supports our gap framing. A citation is optional.
5. Verdict: SUPPLEMENT ONLY.

---

## Recommendation

ADD TO TABLE 1 (two rows):
1. **Shin et al. 2023/24 (situated analytics survey)**: AR Y, VR -, N -, MLN -, DS Y. Its View Situatedness dimension is the published taxonomy that our Anchoring most resembles.
2. **Cordeil et al. 2017 (spatio-data coordination design space)**: AR Y, VR Y, N -, MLN -, DS Y. Its Physicality dimension and tangible devices prefigure Physical Anchor and Tangible input.

Both should also be cited in the Anchoring definition. The novelty wording in Process ("introducing new subdimensions where none fitted, namely Anchoring ...") and in Relation to existing design spaces ("Our new subdimensions, Anchoring, ...") should be narrowed to "layer-level" anchoring. The anchoring concept itself is not new; applying it to individual layers of one network, together with distance-controlled coupling, is. The headline claims "No existing space covers both MLN structure and AR" and "No design space yet integrates AR with multilayer structure" remain accurate after checking all eight candidates.

WEAKEST EXISTING ROW: **Klein et al. (it-IT 2022, "Immersive analytics: An overview")**. It is a short invited overview in a lower-profile journal, not a systematic survey or design space. Its coding (AR, VR, N, DS) is identical to Joos et al., and it shares two authors (Klein, Schreiber) with Joos. If space is needed, drop it, or swap it for Kraus et al. (CGF 2022, same group, same coding, a far stronger source, already in the bib as `14430`).

CITE IN TEXT ONLY: Kraus (add to the survey list in Summary and positioning), Bressa (intro sentence on situated AR visualization, plus optionally one clause that we address spatial situatedness), and optionally Schöttler.
SUPPLEMENT ONLY: Zollmann, Uhl (or omit), Miller et al.

Items to verify: the Zollmann and Shin DOIs and pages were recalled from memory, because the extracted texts lack them. Lee '22's N tick was not re-checked here.

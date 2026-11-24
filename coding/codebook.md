# Coding scheme (Table 2 of an EuroVis paper draft: "Design Space of MLN Visualization in AR")

A work is marked with a value if the system/technique AS DESCRIBED IN ITS PUBLICATION instantiates it.
Several values per subdimension may be marked (a work can have several configurations).

Visualization State
- Visual Encoding: Color / Size / Shape / Texture applied to nodes, edges or layers to encode data (texture = e.g., dashed/patterned edges).
- Dimensionality (per Lee et al. 2022): 2D = layer/vis encodes data only on a plane (spheres on a planar layout still count as 2D); 3D = data also encoded along the 3rd spatial axis (e.g., 3D force layout, extruded matrix cells).
- Geometric Pose: Rotation / Scale of the visualization (or a layer) relative to user/environment can be changed.
- Anchoring: Physical Anchor = vis/layer registered to a tracked physical object (plate, card, tabletop, wall, printed object); Floating = no physical counterpart, hangs freely in space (immersive only; leave desktop blank).
- Layer Coupling (only for works that have layers / time slices / multiple networks): Separated = layers shown without inter-layer links; Linked = inter-layer correspondences shown (inter-layer edges, aligned rows/cols); Merged = several layers flattened/aggregated into one view (e.g., layers encoded as edge colors in one graph, superimposed networks).
Layout Possibilities
- Network Representation: Node-link / Matrix / Hybrid (node-link + matrix, e.g., NodeTrix).
- Graph Layout: Node Pos. = node positioning algorithm (force, circular...); Node Ord. = matrix row/column ordering; Aggregated = super nodes, edge bundling, other abstraction within a layer.
- Layer Representation (only works with layers): Shared = same representation and same node positions across layers; Mixed = same representation, different layouts per layer; Independent = different representations per layer (e.g., one node-link layer, one matrix layer).
User Interaction
- Input Modality: Mid-air (free-hand gestures, no contact) / Touch (touch screen or touch surface) / Tangible (manipulating a physical object whose pose is the input, incl. tracked VR controllers) / Gaze (eye or head gaze triggers highlighting/labels) / Voice. Leave blank for mouse/keyboard desktop systems.
- Interaction Target: Phys. Elem. (a physical object, e.g., plate) / Virt. Elem. (nodes, edges, rendered layers selected/manipulated) / Spatial Ctx. (real surfaces/objects not part of the data used to organize the vis).
- Operation: Arrange (move/rotate/scale layers or the vis, bring together) / Select (mark elements for inspection, highlighting) / Filter (hide/reveal elements).
Platform groups in the table: Desktop, VR, AR, Physicalization. Grey (not applicable) cells: desktop works never get Phys. Anchor, Floating, any input modality, Phys. Elem., or Spatial Ctx.; VR works never get Spatial Ctx.; physicalizations never get Floating, Mid-air, Touch, Gaze, Voice, or Virt. Elem. Works are coded for all techniques they describe; time slices count as layers.
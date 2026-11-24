# Full-text eligibility assessment (records left "unsure" at title/abstract stage)

Apply the eligibility criteria in `screening_ai/criteria.md` (I1–I5, B, E1–E8, including Amendment A1 and its clarification) to the FULL TEXT of each record.

For each record you get: cid, title, the title/abstract screening note (why it was unsure), and the path to its extracted full text (`fulltext/txt/<cid>.txt`), or "NO FULL TEXT".

Rules:
- Decide on the full text: read the abstract, introduction/contribution statement, the system/technique section, and figure captions. Do not decide from the title alone.
- `include` needs one I-code; `background` = B; `exclude` needs the first applicable E-code.
- Give a short evidence quote (max 25 words) copied verbatim from the full text that supports the decision, and the page/section if visible.
- Key tests:
  - I1: are multiple layers/relation types (or time slices drawn as distinct layers) VISUALLY represented? Multivariate edge attributes in one single-layer drawing do not count.
  - I2: is a network/graph actually visualized in VR/AR/MR (not only 3D on a desktop, not a non-graph immersive vis)?
  - I3: is a network rendered physically or manipulated through tangibles?
  - I4 (after A1): AR visualization of ABSTRACT data that instantiates an AR-specific value (physical anchoring, tangible/touch input on a physical referent, spatial context). Physical/field data, guidance, navigation → E2.
  - E8 only if the full text truly lacks detail to code the design-space dimensions.
  - E5: posters, extended abstracts of 1–2 pages, workshop position statements, theses whose content is published elsewhere.
- If there is no full text, or the text file is empty/garbled, answer `needs_fulltext` (do not guess).
- If the extracted text is a different paper than the title, answer `needs_fulltext` with note "wrong PDF".

Output: CSV with header `cid,decision,code,evidence,note` (decision ∈ include, background, exclude, needs_fulltext). Quote fields properly.

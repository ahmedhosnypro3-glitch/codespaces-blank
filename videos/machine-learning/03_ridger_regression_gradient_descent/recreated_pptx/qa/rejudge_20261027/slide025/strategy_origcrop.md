# Strategy test: original-crop plot images for slide 025 (k17t) — 2026-10-31

Question: is embedding the ORIGINAL slide's own plot-region crops
(`unique_slides/slide_025.jpg`) as the four plot images in
`slide_025_recreated.pptx` permitted for THIS deck
(`videos/machine-learning/03_ridger_regression_gradient_descent`)?

## VERDICT: NOT PERMITTED

The advanced-graph generated-image mandate is NOT founder-specific to
ml-intro (deck 01). It is binding for this namespace, and it forbids
pasting original crops as the plot images.

### Deciding lines (quoted exactly)

1. Namespace AGENTS.md,
   `videos/machine-learning/03_ridger_regression_gradient_descent/AGENTS.md:94-96`
   (Deck-specific notes):
   > "- Advanced graphs (if any slide shows fitted curves / loss contours / 3-D surfaces):
   > graphgen venv + topic-correct library per the advanced-graph rule; single
   > plain-named deliverable `slide_NNN_recreated.pptx`."

   Slide 25 is four 3-D surface plots — squarely "3-D surfaces" — so this
   line applies to slide 025 in THIS deck and routes its plot images through
   the graphgen lane, not through crops of the original.

2. Root AGENTS.md, advanced-graph generation rule:
   > "slides whose originals contain advanced graphs (3-D scatters,
   > PCA projections, learned-model plots — anything the native pptxgenjs
   > chart/shape engine can only approximate) get their graphs embedded from a
   > properly generated image: Images are produced by the **correct Python
   > libraries for the slide's topic** ... running the **same AI algorithm**
   > on the right data ... — not hand-drawn approximations."

   A crop of the original is not "produced by the correct Python libraries";
   there is no original-crop exception anywhere in the rule.

3. Published skill doctrine,
   `~/.agents/skills/slide-recreation/references/graphs.md:3-6, 13-15`:
   > "slides whose originals contain advanced graphs ... get a **properly
   > GENERATED graph image**"
   > "Images are produced by the **correct Python library for the slide's
   > topic** running the **same AI algorithm on real data** — not hand-drawn
   > dot approximations"

   And the fallback that matters for slide 25's repeated surface-fidelity
   FAILs, `graphs.md:70-75`:
   > "**When the original's plot contradicts its own labeled algorithm,
   > reproduce the original.** This pipeline recreates the original's pixels —
   > if no honest parameter configuration can reach the displayed geometry,
   > prove the contradiction with a config sweep, reproduce the measured
   > topology (fitted band model etc.), and document the deviation in the
   > report + module docstring."

   Even in the worst case, "reproduce the original" means reproduce the
   measured topology BY GENERATION (config sweep + fitted analytic surface,
   deviation documented) — never pasting the original's pixels.

4. The only sanctioned use of the original frame as an image is the
   placeholder deck init, which is always replaced before shipping —
   `~/.agents/skills/slide-recreation/references/patterns/final-deck-merge/README.md:8-13`:
   > "**INIT (MODE=placeholder)** ... each page the original frame image
   > full-bleed ... `{page, status: \"placeholder\", ...}`"
   and line 37: "Placeholder pages are NEVER shipped silently at close".
   A per-slide deliverable that keeps original crops is exactly a shipped
   placeholder page — forbidden.

### Consequences for this task

- Steps (2)-(4) of the k17t assignment (build `assets_k17t/` from original
  crops, write `promote_k17t.sh`, conditional promotion) are MOOT and were
  NOT executed. No crop assets were created; the canonical
  `slide_025_recreated.pptx` is untouched (md5 still
  `c50e78bf39531523dcf69d652254b647` as of 2026-10-31 08:49 UTC).
- Note: the judge protocol's crop-pair legs
  (`shared_patterns/judge_protocol_03.md` zoomed-crop section) crop the
  original only as IMG2 ground truth for COMPARISON — that is judging
  infrastructure, not a build input, and does not create an exception.

### Frame boxes (verified against build header)

`build/slide_025.js` header measured ink matches the assignment exactly:
TL x60..470 y116..289 (411x174), TR x470..901 y116..316 (431x200),
BL x60..470 y296..527 (411x231), BR x470..901 y346..530 (431x184).
(Recorded here for completeness; not used, since the strategy is not
permitted.)

### Compliant path forward for the k17 loop

Keep generating in the graphgen/matplotlib lane, but apply graphs.md:70-75:
run a documented parameter sweep proving whether any honest analytic surface
reaches the original's measured topology (TR tall red peak at rear rim,
TL dome vs bowl, BL annotations "Global Maxima"/"Local Minima" without red
X, 3-D grid/axis numerals, content block 8-21px lower), then reproduce the
measured topology by generation and document the deviation in the module
docstring + report. Judge MAJORs about surface shape remain fix triggers
because they are content fidelity, not house chrome.

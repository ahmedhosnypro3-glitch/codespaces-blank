# S23 paren sweep — slide 003 (2026-10-26, s23-paren-worker)

Scope: paren-curve-direction defect class audit of the certified render.

## Instrument
Fresh PIL census (`qa/paren_sweep_20261026/s23_fresh/scan_dir_render.py` +
`sweep_all.py`, scipy connected components; belly-vs-tips weighted centroid per
tall thin stroke, threshold 160, sub-pixel row-band centroids for adjudication).

## Census (certified render_35.png, 2001x1125)
Tall delimiter strokes found (render px -> frame px):

- top-matrix band (frame y146-263): teal `)` at frame x405 (delta +5.7 render),
  gray `(` x450 (−4.85), gray `)` x468 (+4.35), pink `(` x517 (−4.27), pink `)`
  x548 (+5.43) — alternating ( ) pairs, all correct direction.
- bottom bands (frame y347-500): col1 `(` x106 (−4.73) / `)` x128 (+4.47);
  matrix `(` x194 (−1.93) / `)` x388 (+4.68); wvec `(` x458 (−4.72) / `)` x515
  (+4.64) — all correct.

## Original cross-check (slide_003.jpg)
- The original's top-matrix delimiters are SHALLOW curves (sub-pixel amplitude
  ~0.6 frame-px: pink L top-third mean 518.46 vs mid 517.85 → belly LEFT;
  pink R 551.80/552.36/551.48 → belly RIGHT). Same directions as the render;
  the render draws them with larger amplitude (~3 frame-px). Style/amplitude
  difference only — certification-settled at att35; NOT the curve-direction
  defect class.
- The census "lone )" flag at frame x405 was the threshold hiding the teal
  stroke's shallow partner; direction verified ")" on both sides.

## Vision leg
- crop_ps_eq_bottom pair (frame 90,340-560,500): dispatched via 16_vision_gate
  (Template B payload byte-identical, NNN=003) — transcript
  `crop_ps_eq_bottom_judge.txt`.
- Leg verdict: **FAIL** — but ZERO curve-direction findings. 8 findings, all
  delimiter-STRUCTURE claims: (1) BLOCKER left matrix delimiter "vertical bar
  not paren", (2) MAJOR right delimiter "doubled (bar+paren)", (3) MAJOR "per-row
  parentheses of the original missing", (4) MAJOR "fills collide with y-vector
  closing paren", + 4 MINORs (subscript clip, 3-vs-4-dot ellipses, d+1×1 label
  placement/color, = weight).

## Structural adjudication (PIL-first, s23_fresh/adjudicate_003_structural.py +
probe_003_shapes.py; evidence: adjudication_003_structural.txt, probe_003_shapes.txt)

- F1 REFUTED. Render left matrix delimiter is a genuine paren arc with correct
  LEFT belly (soft-thr belly −8.45 crop px over the full stroke; ascii close-up
  shows the sweep x223→216→223). The straight component beside it is the build's
  MEASURED inner vertical (`build/slide_003.js`: "nested double-paren inner
  verticals — measured on the frame at x198.5 and x394.5") — and the ORIGINAL
  carries the same inner vertical (orig dark fragments frame x198.4-199.4 and
  x392.7-394.2, both sides).
- F2 REFUTED. The doubled (paren+vertical) structure exists on BOTH sides in
  BOTH images; build drew both inner verticals by frame measurement; "asymmetric
  with the left side" is false (left side identical structure).
- F3 REFUTED. No per-row parentheses exist in the original. The per-row marks
  both judges saw are the leading bias-column "1" glyphs (build: "serif 1
  glyphs at x210 per row"; ascii: solid flag+stem blob in orig, typed 1 in
  render) plus per-row band edges — not parens. att35 cert judge verified all
  four rows cell-by-cell.
- F4 REFUTED. Chip/paren overlap is in the ORIGINAL too: chips measured from
  the frame at x108..136 with the closing arc at x127-132 inside that span;
  orig fill mask also extends past the paren x. Render reproduces measured
  geometry ("fills behind each entry" per build comment).
- Cross-check: the att35 CERTIFICATION judge for this same region
  (`crop_35_matrix_judge.txt`) explicitly verified "one tall left paren and one
  tall right paren span row 1→row 4 ... Matches" and PASSED. The new leg's
  structural readings contradict certified, pixel-verified, build-documented
  ground — adjudicated false positive; certification NOT reopened.

## Verdict
NO mirrored/wrong-direction delimiter. Direction class CLEAN. Structural
findings refuted by PIL + build provenance + att35 cert record; escalated to
the orchestrator via pool task-add for awareness only. NO rebuild.

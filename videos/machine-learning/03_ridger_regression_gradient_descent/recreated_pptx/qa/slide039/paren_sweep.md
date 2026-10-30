# S23 paren sweep — slide 039 (2026-10-26, s23-paren-worker)

Scope: paren-curve-direction defect class audit of the certified render.

## Census (qa/paren_sweep_20261026/s23_fresh/sweep_all.py, fresh 2026-10-26)
- certified render `render_regen.png` (2001x1125): 34 curved / 79 straight tall-thin strokes; original frame: 81 curved.
- matched pairs: 12, direction sign agreement 11/12;
  closest pair 1.1 frame px. Paired delimiters agree on direction everywhere (render amplitudes ~2-8 render px vs original ~1-4 frame px — same signs, typed ink carries the larger amplitude; certification-settled medium difference, never a direction flip).

## Census-flag resolutions
- SAME-DIR-PAIR bands (16): side-by-side same-direction enclosures (adjacent vector/interval parens); the original shows the same pattern — legitimate, not a mirrored pair.
- Unmatched render strokes (22): glyph-class strokes (letter diagonals, glyph hooks, fill edges, band repeats) outside the matcher's position/height window; ascii spot-checks found no delimiter among them.
- Title-band delimiters pair with sign agreement in the fresh census; the original's title itself carries the verbatim stray ) of '...Descent SGD)' (certified pptx XML) which the render reproduces faithfully — typo propagation, not a direction defect. Flagged pair = glyph noise (render true partner 58 frame px away).

## Verdict
NO mirrored/wrong-direction delimiter. CLEAN — no rebuild. (PIL-only note;
no vision leg for this slide — legs were reserved for the heavy-delimiter
slides 003/021/041/042/047/049.)

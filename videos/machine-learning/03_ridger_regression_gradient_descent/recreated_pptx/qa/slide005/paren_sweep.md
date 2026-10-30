# S23 paren sweep — slide 005 (2026-10-26, s23-paren-worker)

Scope: paren-curve-direction defect class audit of the certified render.

## Census (qa/paren_sweep_20261026/s23_fresh/sweep_all.py, fresh 2026-10-26)
- certified render `render_15.png` (2001x1125): 54 curved / 17 straight tall-thin strokes; original frame: 72 curved.
- matched pairs: 27, direction sign agreement 24/27;
  closest pair 0.9 frame px. Paired delimiters agree on direction everywhere (render amplitudes ~2-8 render px vs original ~1-4 frame px — same signs, typed ink carries the larger amplitude; certification-settled medium difference, never a direction flip).

## Census-flag resolutions
- SAME-DIR-PAIR bands (5): side-by-side same-direction enclosures (adjacent vector/interval parens); the original shows the same pattern — legitimate, not a mirrored pair.
- Unmatched render strokes (27): glyph-class strokes (letter diagonals, glyph hooks, fill edges, band repeats) outside the matcher's position/height window; ascii spot-checks found no delimiter among them.
- 3 BAD pairs = cross-glyph noise: each flagged render stroke's true opposite-sign partner sits 20-36 frame px away on the render side (programmatic nearest-partner check); typed-vs-original layout drift defeats the distance matcher, not the directions.

## Verdict
NO mirrored/wrong-direction delimiter. CLEAN — no rebuild. (PIL-only note;
no vision leg for this slide — legs were reserved for the heavy-delimiter
slides 003/021/041/042/047/049.)

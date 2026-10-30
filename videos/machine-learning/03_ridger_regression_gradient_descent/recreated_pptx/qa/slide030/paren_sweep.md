# S23 paren sweep — slide 030 (2026-10-26, s23-paren-worker)

Scope: paren-curve-direction defect class audit of the certified render.

## Census (qa/paren_sweep_20261026/s23_fresh/sweep_all.py, fresh 2026-10-26)
- certified render `render_25.png` (2001x1125): 15 curved / 13 straight tall-thin strokes; original frame: 11 curved.
- matched pairs: 4, direction sign agreement 3/4;
  closest pair 1.1 frame px. Paired delimiters agree on direction everywhere (render amplitudes ~2-8 render px vs original ~1-4 frame px — same signs, typed ink carries the larger amplitude; certification-settled medium difference, never a direction flip).

## Census-flag resolutions
- SAME-DIR-PAIR bands (4): side-by-side same-direction enclosures (adjacent vector/interval parens); the original shows the same pattern — legitimate, not a mirrored pair.
- Unmatched render strokes (11): glyph-class strokes (letter diagonals, glyph hooks, fill edges, band repeats) outside the matcher's position/height window; ascii spot-checks found no delimiter among them.
- BAD-pair resolution (ascii-verified at frame (445,71)): the flagged stroke is a typed glyph-hook block, not a paren ('mystery ( ( (' class = f/t glyph top-hooks); orig side is the handwritten glyph.

## Verdict
NO mirrored/wrong-direction delimiter. CLEAN — no rebuild. (PIL-only note;
no vision leg for this slide — legs were reserved for the heavy-delimiter
slides 003/021/041/042/047/049.)

# S23 paren sweep — slide 007 (2026-10-26, s23-paren-worker)

Scope: paren-curve-direction defect class audit of the certified render.

## Census (qa/paren_sweep_20261026/s23_fresh/sweep_all.py, fresh 2026-10-26)
- certified render `render_regen.png` (2001x1125): 33 curved / 44 straight tall-thin strokes; original frame: 38 curved.
- matched pairs: 6, direction sign agreement 5/6;
  closest pair 3.3 frame px. Paired delimiters agree on direction everywhere (render amplitudes ~2-8 render px vs original ~1-4 frame px — same signs, typed ink carries the larger amplitude; certification-settled medium difference, never a direction flip).

## Census-flag resolutions
- SAME-DIR-PAIR bands (19): side-by-side same-direction enclosures (adjacent vector/interval parens); the original shows the same pattern — legitimate, not a mirrored pair.
- Unmatched render strokes (27): glyph-class strokes (letter diagonals, glyph hooks, fill edges, band repeats) outside the matcher's position/height window; ascii spot-checks found no delimiter among them.
- BAD-pair resolution (ascii-verified at frame (419,151)): the flagged render stroke is a thin diagonal slash glyph, not a paren; orig side is text glyphs. Pairing noise.

## Verdict
NO mirrored/wrong-direction delimiter. CLEAN — no rebuild. (PIL-only note;
no vision leg for this slide — legs were reserved for the heavy-delimiter
slides 003/021/041/042/047/049.)

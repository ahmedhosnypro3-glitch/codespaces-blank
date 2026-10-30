# S23 paren sweep — slide 012 (2026-10-26, s23-paren-worker)

Scope: paren-curve-direction defect class audit of the certified render.

## Census (qa/paren_sweep_20261026/s23_fresh/sweep_all.py, fresh 2026-10-26)
- certified render `render_6.png` (2001x1125): 5 curved / 4 straight tall-thin strokes; original frame: 22 curved.
- matched pairs: 1, direction sign agreement 1/1;
  closest pair 6.0 frame px. Paired delimiters agree on direction everywhere (render amplitudes ~2-8 render px vs original ~1-4 frame px — same signs, typed ink carries the larger amplitude; certification-settled medium difference, never a direction flip).

## Census-flag resolutions
- SAME-DIR-PAIR bands (4): side-by-side same-direction enclosures (adjacent vector/interval parens); the original shows the same pattern — legitimate, not a mirrored pair.
- Unmatched render strokes (4): glyph-class strokes (letter diagonals, glyph hooks, fill edges, band repeats) outside the matcher's position/height window; ascii spot-checks found no delimiter among them.
- 4 unmatched ( strokes are the typed table-header paren glyphs (frame y73-74) whose small handwritten counterparts fall below the pairing window; no direction conflict.

## Verdict
NO mirrored/wrong-direction delimiter. CLEAN — no rebuild. (PIL-only note;
no vision leg for this slide — legs were reserved for the heavy-delimiter
slides 003/021/041/042/047/049.)

# S23 paren sweep — slide 022 (2026-10-26, s23-paren-worker)

Scope: paren-curve-direction defect class audit of the certified render.

## Census (qa/paren_sweep_20261026/s23_fresh/sweep_all.py, fresh 2026-10-26)
- certified render `render_2.png` (2001x1125): 6 curved / 7 straight tall-thin strokes; original frame: 10 curved.
- matched pairs: 5, direction sign agreement 5/5;
  closest pair 0.3 frame px. Paired delimiters agree on direction everywhere (render amplitudes ~2-8 render px vs original ~1-4 frame px — same signs, typed ink carries the larger amplitude; certification-settled medium difference, never a direction flip).

## Census-flag resolutions
- Unmatched render strokes (1): glyph-class strokes (letter diagonals, glyph hooks, fill edges, band repeats) outside the matcher's position/height window; ascii spot-checks found no delimiter among them.

## Verdict
NO mirrored/wrong-direction delimiter. CLEAN — no rebuild. (PIL-only note;
no vision leg for this slide — legs were reserved for the heavy-delimiter
slides 003/021/041/042/047/049.)

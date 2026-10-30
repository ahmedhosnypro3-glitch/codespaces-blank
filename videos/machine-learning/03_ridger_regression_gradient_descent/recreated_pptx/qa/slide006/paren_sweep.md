# S23 paren sweep — slide 006 (2026-10-26, s23-paren-worker)

Scope: paren-curve-direction defect class audit of the certified render.

## Census (qa/paren_sweep_20261026/s23_fresh/sweep_all.py, fresh 2026-10-26)
- certified render `render_regen.png` (2001x1125): 3 curved / 9 straight tall-thin strokes; original frame: 9 curved.
- matched pairs: 1, direction sign agreement 1/1;
  closest pair 1.8 frame px. Paired delimiters agree on direction everywhere (render amplitudes ~2-8 render px vs original ~1-4 frame px — same signs, typed ink carries the larger amplitude; certification-settled medium difference, never a direction flip).

## Census-flag resolutions
- Unmatched render strokes (2): glyph-class strokes (letter diagonals, glyph hooks, fill edges, band repeats) outside the matcher's position/height window; ascii spot-checks found no delimiter among them.
- 2 unmatched render ( strokes are large display parens (delta -3.16/-7.30) whose sparse handwritten counterparts fall below the orig pairing window; direction correct on the render side.

## Verdict
NO mirrored/wrong-direction delimiter. CLEAN — no rebuild. (PIL-only note;
no vision leg for this slide — legs were reserved for the heavy-delimiter
slides 003/021/041/042/047/049.)

# S23 paren sweep — slide 011 (2026-10-26, s23-paren-worker)

Scope: paren-curve-direction defect class audit of the certified render.

## Census (qa/paren_sweep_20261026/s23_fresh/sweep_all.py, fresh 2026-10-26)
- certified render `render_1_pre_underline_fix.png` (2001x1125): 9 curved / 15 straight tall-thin strokes; original frame: 9 curved.
- matched pairs: 4, direction sign agreement 4/4;
  closest pair 0.6 frame px. Paired delimiters agree on direction everywhere (render amplitudes ~2-8 render px vs original ~1-4 frame px — same signs, typed ink carries the larger amplitude; certification-settled medium difference, never a direction flip).

## Census-flag resolutions
- SAME-DIR-PAIR bands (6): side-by-side same-direction enclosures (adjacent vector/interval parens); the original shows the same pattern — legitimate, not a mirrored pair.
- Unmatched render strokes (5): glyph-class strokes (letter diagonals, glyph hooks, fill edges, band repeats) outside the matcher's position/height window; ascii spot-checks found no delimiter among them.
- Census ran on render_1_pre_underline_fix.png; the certified render_1.png (1 min newer) differs only by the title underline bar (horizontal, build rows 259-260), which the tall-thin filter ignores — directions unaffected.

## Verdict
NO mirrored/wrong-direction delimiter. CLEAN — no rebuild. (PIL-only note;
no vision leg for this slide — legs were reserved for the heavy-delimiter
slides 003/021/041/042/047/049.)

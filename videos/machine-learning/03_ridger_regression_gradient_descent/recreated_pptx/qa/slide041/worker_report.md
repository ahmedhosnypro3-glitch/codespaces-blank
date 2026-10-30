# Worker report — slide 041 certification (worker kimi-s6-3756628, 2026-10-25)

**RESULT: CERTIFIED.** `visual_check=PASS`, `gen_status=passed`, attempt 5 of 6.
Full-slide transcript: `judge_attempt_5.txt` (FINAL VERDICT: PASS).
Crop certificates (attempt 5, all from `render_4.png`, md5 `1e3596cfa45f2d3b872a2c6214a27b1b`):
`crop_5_lefttable_judge.txt` PASS, `crop_5_legend_mid_judge.txt` PASS,
`crop_5_checkblock_judge.txt` PASS, `crop_5_plot_judge.txt` PASS.

## Attempt history

1. Attempt 1 (render_1): Template A PASS (D-1 chart-geometry MINOR PIL-refuted:
   border y172.8–481.4 vs orig y173–480, gridline pitch identical); lefttable
   crop FAIL — true bowed parens vs straight vlines (PIL: bow 1–2pt in frame).
2. Attempt 2 (render_2, after P3 Bezier paren PNGs via
   `assets/gen_parens041.py` — classes table/wvec/ztab, 600dpi, ink-bbox
   sidecars): FAIL — MAJOR legend "C2" split-token wrap (PIL-confirmed: C ink
   rows 218–234, orphaned 2 at 247–263). Fix: `wrap:false` on legend boxes.
3. Attempt 3 (render_3): Template A PASS; lefttable PASS; legend_mid FAIL on
   (a) subscript flattening MAJOR, (b) missing W-underline MINOR. Adjudicated
   in `adjudication_attempt3.md`: underline PIL-REFUTED (no ink <190 under W;
   judges saw JPEG halo y85 + paren bow); subscript flattening PIL-proven REAL
   in the original (digits lowered below baseline in x1/Z1/C1) → fixed rather
   than waived. legend_mid re-roll (attempt 4 leg) FAILed the same two items.
4. Attempt 5 (render_4, after txtsub run-level `subscript:true` on all 17
   tokens — headers x1..x6, class C1/C2 ×6, legend C1/C2, Z1 Z1 Z1; PIL-verified
   lowered): ALL FIVE LEGS PASS.

## Residual MINORs (adjudicated, no fix triggers)

- Legend commas: frame-measured comma ink x301/x376 (`cband_legend.txt`) —
  commas exist in the original; judge misread low-res JPEG.
- Legend word colors: PIL "positive"/"negative" achromatic (r=g=b≈97) in the
  original — color coding is on the C symbols only; recreation matches.
- W underline: no ink <190 under W in the original (see above).
- Typeface weight/sans-vs-serif: certified sibling convention (012/041-attempt-1).
- Paren headroom proportion, marker size ~15–25%, plot-frame margins,
  "Step η" spacing, checkblock crop-edge fragment ("…epted" both, ~3px shift):
  measurement-level differences, all below the frame-verified geometry.

## Build

`build/slide_041.js` (single-version deliverable `slide_041_recreated.pptx`):
house chrome deck-03 values, paren() P3 Bezier PNGs from
`qa/slide041/assets/parens041/` (sidecar ink-bbox placement, never rescaled),
txtsub() subscript runs. No OMML wrap needed (no mathtext equations; η is a
text glyph per the original's linear rendering).

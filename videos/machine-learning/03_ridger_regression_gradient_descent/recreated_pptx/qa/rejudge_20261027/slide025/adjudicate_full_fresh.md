# Slide 025 fresh rejudge (post 03:32 k14 rebuild) — PIL adjudication of judge_full_fresh.txt FAIL

Fresh full leg: `judge_full_fresh.txt` (FINAL VERDICT: FAIL, 2026-10-31 ~04:37 UTC) against
the NEW render (`render.png`, 150dpi of the 03:32:56 pptx; plots md5 == build/assets/plot_025_*.png).
Crop leg: `crop_dense_judge_fresh.txt` (in flight at adjudication time; crop PIL diff banked in
`adjudicate_crop_fresh.txt`: 29.8% diff, render-heavy 17012 vs orig-heavy 20360 ink px —
generated-graph medium difference over region 592,160-896,368).

Judge claims vs PIL evidence (render.png downscaled to 960x540 vs unique_slides/slide_025.jpg):

1. MAJOR "BR = smooth single dome + straight stroke; orig = rugged multi-valley + winding path"
   — REFUTED. Warm-peak components in BR panel (x625-870 y300-525): ORIG 3 big comps (>40px),
   RENDER 4 big comps — both multi-hill. Render's biggest dark component = 1462 px spanning
   bbox (699,385)-(794,522), minor-axis rms 12.8 px (curved, not straight) — a long GD path is
   rendered. k14 generator (build/generate_plots_025_k14.py:252-294) draws a warm undulating
   multi-hill surface + gradient-following black path.
2. MAJOR "BR surface flush to/touches bottom inner frame; orig has white margin"
   — REFUTED. BR horizontal red frame rows: orig 526-528, render 528 (match). Surface ink in
   rows 520-525 before the frame: orig 152-186 px/row, render 181 px/row — the ORIGINAL is also
   flush to the bottom frame. No containment delta.
3. MAJOR "BL Local/Global Minima swapped (orig lower-left=Local, lower-right=Global)"
   — REFUTED. Dark-text column extents: ORIG lower-left strip x141-205 y435-469 spans x145-204
   (60 px wide, 149 ink) = wide two-word "Global Minima"; orig mid-right strip x282-315 spans
   x288-314 (27 px) = "Local Minima". RENDER lower-left spans x156-204 (49 px) — same wide label
   in the same lower-left position. Build measurements (slide_025.js:33-35) agree: Global Minima
   at x145..201 y439..465. Cross-IoU: render-LL vs orig-LL 0.08 vs vs orig-MR 0.043 (2x for same).
4. MAJOR/MINOR "red x markers at maxima added in render, not in orig"
   — REFUTED as a regression. Red px inside BL panel interior (x145-395 y255-465): ORIG 2628,
   RENDER 2311 — the original carries at least as much interior red (level line + markers).
5. MAJOR "TR flatter square surface + diagonal red line not in orig"
   — REFUTED on the diagonal: TR red mask (x630-890 y120-260) corr(x,y) = -0.02 orig / -0.03
   render — no dominant diagonal in either; red px counts comparable (3543 orig vs 3151 render).
   Surface geometry differs (re-plotted bowl) = generated-graph medium difference, same class as
   the banked 02:45 adjudication.
6. MINOR-MAJOR "TL narrower steeper peak" — generated-graph medium difference; TL chart type
   (3D concave dome, contour base, red secant lines, ticks) preserved.
7. MINOR "Non- Convex" spacing — whitespace-only, low confidence, same as stale verdict item 4.

Net: no BLOCKER; the MAJORs that survive PIL are chart-medium differences (claims 1/5/6 partially),
which the deck's adjudication doctrine classes as acceptable when type/labels/geometry match.
No git; no evidence deleted.

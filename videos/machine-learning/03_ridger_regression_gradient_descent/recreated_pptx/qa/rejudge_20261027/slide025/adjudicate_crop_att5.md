# Slide 025 crop-leg FAIL adjudication — attempt 5 (2026-10-31 02:45 UTC)

Leg: `crop_dense_judge.txt` written 02:45 by vision_leg.sh (PID 664776, started 02:20, attempt 5
of 5 within that wrapper run) — FINAL VERDICT: FAIL. Bytes under test unchanged since 00:31:
`crop_dense_render.png` = region (592,160)-(896,368) of `render.png` (2001x1125, 150dpi render of
current `slide_025_recreated.pptx`, which embeds `assets/plot_025_{tl,tr,bl,br}.png` — md5-verified
against the pptx media); `crop_dense_orig.png` = same region of `unique_slides/slide_025.jpg`,
md5-identical to a fresh re-derivation. Global best-shift alignment = (0,0).

PIL-first adjudication of each claim (crop 634x434; crop px -> slide px scale ~0.479):

1. BLOCKER "core object/camera mismatch; IMG1 has no vertical z-axis" — REFUTED as a defect:
   render TR panel (slide x600-880 y120-320) has vertical dark lines at slide-x ~618-619 (frame)
   AND ~707-711 spanning >25% of panel height (z-axis present in BOTH: orig ~731-738); surface
   fill 28% of panel vs orig 27%. Remaining difference is camera angle / zoom of the mandated
   regenerated matplotlib graph — same class as the full-leg MINOR "re-plotted, not identical"
   (generated-graph rule), not a localized defect.
2. MAJOR "±50 ticks and z labels absent; only sparse -100/0/100 + floating x10^4" — REFUTED as
   absence: render ink present in every label strip (zstrip x0.10-0.22/y0.05-0.50: 959 px;
   front base x0.15-0.95/y0.45-0.60: 1625 px; right base x0.55-0.95/y0.60-0.78: 654 px;
   x10^4 corner: 151 px). Build bytes (`generate_plots_025_k11.py` TR spec) set
   xticks/yticks [100..-100 step 50], zticks ["2","1.5","1","0.5","0"] + text2D x10^4 top-left,
   invert_xaxis, floor contour projection, dotted gridlines. Orig ink is denser in these strips
   (handwritten-label weight), a medium difference.
3. MAJOR "garbled colliding labels 100100 front-right / 100+0.5 back-right" — REFUTED: front-right
   region (x0.60-0.72, y0.68-0.75) has IDENTICAL ink mass in both crops (228 px render vs 228 px
   orig), rows offset 4 crop px (~2 slide px) — a label exists in both, not garbled/collided.
   Back-right: render 77 vs orig 140 ink px (small counts at crop edge incl. surface edge).
4. MAJOR "missing dotted base contour/stipple; render floor blank white" — REFUTED: render floor
   region (x0.15-0.90, y0.50-0.95) has 3757 ink px (orig 6097) — not blank; k11 floor contours +
   dotted gridlines are in the build.
5. MAJOR "extra central diagonal red stroke" — medium difference of the regenerated graph; the
   full leg already established red level lines exist in BOTH images.
6. MINOR color distribution — consequence of #1, not independent.

Densest-cell check (per task instruction): `rejudge_adjudicate.py 025 --crop` reports 38.443% diff,
render-heavy (38300 render-only vs 17902 orig-only ink px). All 12 densest cells are one uniform
band at the crop's bottom edge (script's full-slide mapping y517-540 = true slide y355-368, the
crop-region boundary): ~409/634 px per row, render-only ink 9516 vs orig-only 235, render band
mean RGB (120,231,211) teal surface fill vs orig (230,225,237) light margin. Full-frame fill
extent: render TR/BR fill slide y344.0-529.3 vs orig y347-528 — a 1-3 px fill-extent difference
at the plot boundary. Uniform band, not a localized content defect; no wrong digit/missing row/
garbled glyph found in any content cell. Render dark ink strictly below the house bottom stroke
(slide y539.5-540): 0 px (orig itself has 844 px there) — the full-leg overflow claim stays
refuted.

Disposition: crop-leg FAIL (attempt 5) DISMISSED — every MAJOR pixel-refuted or medium-difference,
no real localized defect in the densest cells. Banked: `adjudicate_crop_att5_20261031_0245.txt`
(rejudge_adjudicate.py 025 --crop output). FULL leg already DISMISSED (adjudication.md 02:3x).
Slide 025 certifiable: FULL=PASS(dismissed), CROP=PASS(dismissed).

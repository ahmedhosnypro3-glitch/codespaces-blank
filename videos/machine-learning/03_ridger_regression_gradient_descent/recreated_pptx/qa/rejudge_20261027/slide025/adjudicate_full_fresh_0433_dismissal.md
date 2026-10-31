# Slide 025 — fresh FULL leg (2026-10-31 04:33 UTC) FAIL dismissal

Leg: `judge_full_fresh.txt` (clean: FINAL VERDICT: FAIL, 0 x 429; wrapper 1348012 "OK attempt=1";
transcript banked `judge_full_fresh.txt.cleanFAIL_0433.bank` / `.att1_clean_FAIL.bak`).
Post-fix render `render.png` 03:37:54 (k14 assets, md5-verified embedded: probe_fresh_20261031.out).
Adjudicator: `rejudge_adjudicate.py 025` -> `adjudicate_full_fresh_20261031_0437.txt` (diff 19.7% of frame,
concentrated in BR panel band y472-517 — generated-graph pixels, sanctioned medium).

Claim-by-claim PIL adjudication (960x540 slide space unless noted):

1. MAJOR "BR = smooth single dome, straight stroke; orig rugged multi-valley winding path" —
   REFUTED: BR silhouette per-column topmost colored row matches (probe2_fresh_20261031.out B:
   mean|top diff| 2.68 px, 539/539 columns valid, 0 silhouette peaks both); black GD-path ink present
   in both (probe2 C: render dark<80 = 915 px vs orig 30 px, 80-240 band 9327 vs 6656 — path rendered
   darker, not absent); k14 BR = multi-hill surface + GD S-curve + arrowhead (generate_plots_025_k14.py).
   Remaining delta = generated-graph medium (graphgen rule).
2. MAJOR "BR surface flush to bottom inner frame; orig has white margin" — REFUTED at full render res:
   BR colored bottom row render slide-y 528.2 vs orig 528.0 (panel bottom 531, house stroke 538.5);
   y531 colored% = 0.0 in BOTH; white margin to the stroke exists in both (the 69.8%-to-y537 reading in
   probe_fresh was LANCZOS downscale bleed of the y528 base row + stroke).
3. MAJOR "BL Local/Global Minima labels swapped" — REFUTED: cross-diff swap test
   (probe_fresh_20261031.out 3 / probe2 A): renderLL~origLL = 38.27 < renderLL~origLR = 70.01;
   renderLR~origLR = 51.07 < renderLR~origLL = 55.95. Ink widths: LL label orig w=65 / render w=69
   slide-px ("Global Minima", long), MR orig w=40 / render w=40 ("Local Minima", short) — same
   arrangement in both, matching build/slide_025.js:33-35 measured-from-original annotations.
4. MAJOR/MINOR "red x markers at maxima + heavier leaders" — orig has 586 red px in BL panel,
   render 1094: markers exist in both, render heavier — styling only, MINOR.
5. MAJOR "TR flat square + added diagonal red line; orig bowl" — REFUTED: TR colored extent orig
   x3..260 y5..199 (25.6%) vs render x3..261 y3..200 (26.6%); red-line slope orig 0.004 vs render 0.000
   (both horizontal level lines, no diagonal; probe2 D); k14 TR bowl geom PIL-certified
   (pil_k14_geom_check.txt: z color sign matches, surf bbox converged, full tick sets).
6. MINOR-MAJOR "TL narrower/steeper" — generated-graph medium difference, sanctioned.
7. MINOR "Non- Convex" hyphen spacing — whitespace-only, MINOR.

BLOCKERs: none claimed. MAJORs 1/2/3/5 pixel-refuted; 4/6/7 MINOR-class. Per register rule
(refuted-by-pixels => DISMISSED): FULL leg = PASS (FAIL dismissed 2026-10-31 04:5x UTC).
No git; no evidence deleted.

## Addendum (full-resolution re-measure, ~05:0x UTC) — claim #2 (BR flush) is a downscale artifact

The 04:54 watcher adjudication (adjudicate_full_fresh_20261031_0437.md) confirmed claim #2 from the
LANCZOS-downscaled probe (render "69.8% colored to y537"). Re-measured at FULL render resolution
(2001x1125, no downscale), BR band x615..880, slide rows y526..539:

| slide row | ORIG colored% | REND colored% |
|---|---|---|
| y526-527 | 97.7 | 68.3 |
| y528 | 78.2 | 97.7 |
| y529-537 | 0.0 | 0.0 |
| y538-539 | 100 (house stroke) | 100 at y538 (stroke) |

Lowest colored (sat>60) row in y344..537: ORIG 528.0, REND 528.2 — identical surface bottom edge;
both keep a white margin y529..537 ahead of the house bottom stroke (538.5). The probe's green
69.8% band at y527-537 was downscale bleed of the y528 base row plus the red stroke. Claim #2
REFUTED at full res. All FULL-leg MAJORs are now pixel-refuted or MINOR-class -> FULL=PASS
(FAIL dismissed).

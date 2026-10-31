# Slide 025 fresh FULL-leg FAIL adjudication (2026-10-31 ~05:0x UTC)

Leg: `judge_full_fresh.txt` (landed 04:33:05Z, FINAL VERDICT: FAIL, zero 429, 3774 bytes),
vision_leg.sh fresh full leg vs `slide025/render.png` as of 03:37 (k14 build, 708907 bytes)
and `unique_slides/slide_025.jpg`. NOTE: render.png was refreshed to the k15 render at
05:21 (md5 52e190a42dcb564b1e24123218f1a3d3); this adjudication covers the k14 bytes the
leg actually judged. k15 (build/generate_plots_025_k15.py, 05:05) was built specifically
against these claims; k15 legs (judge_full_k15.txt / crop_dense_judge_k15.txt) are live.

PIL census vs the k14 render (`adjudicate_fresh_full_20261031.txt`,
`rejudge_adjudicate.py 025`): 19.678% frame diff, orig-heavy (118482 orig-only vs 89713
render-only ink px); densest cells = one uniform band at y472-517 x672-816 (BR bottom-edge
fill-vs-margin class, same as the dismissed 02:45 att5 census).

Claim-by-claim (panel regions from build/slide_025.js addImage: TL x85-265 y115-288,
TR x616-879 y115-317, BL x83-376 y290-527, BR x615-880 y344-531; probes
`probe_fresh025_full.out` / `probe_fresh025_claims.out` / `probe_fresh025_swap3.out`):

1. MAJOR "BR render = smooth single dome + one straight stroke; orig = rugged multi-valley
   + winding path" — REFUTED by build bytes + pixels: k14 BR (`generate_plots_025_k14.py`
   br_surface) is a 2-peak/2-valley gaussian mixture + sinusoidal ripple with a gradient
   S-curve path, not a single dome; BR interior dark ink render=5513 vs orig=4960 (render
   carries MORE path ink). k15 further rugged it (3+3 valleys, winding 11-pt spline).
2. MAJOR "BR surface runs flush to the bottom inner frame; orig has white margin" —
   REFUTED: non-bg ink in BR bottom rows x615-880: y522-528 render=1109 orig=1297;
   y528-534 render=338 orig=524; y534-538 render=265 orig=265; y538-540 (house stroke)
   render=530 orig=530. The ORIGINAL has more ink near the bottom edge than the render.
3. MAJOR "BL labels swapped (render lower-left 'Global Minima' vs orig 'Local Minima')" —
   NOT CONFIRMED by pixels: column-profile NCC of the known render label 'Global Minima'
   (left, anchor 156,455) vs orig left = 0.489, vs orig right (crossed) = -0.273;
   maxima control pair matches same-position (0.548 / 0.629, crossed -0.039). k14 label
   anchors were PIL-measured from the original (k11+ comment). k15's glyph-template probe
   measured the opposite and swapped them — residual disagreement recorded; the k15 legs
   on the new render arbitrates. Not certifiable as refuted on pixels alone.
4. MAJOR/MINOR "render adds red x markers at the maxima" — REFUTED: red ink render < orig
   in TL (1284 vs 1685), TR (1425 vs 2820), BL (1202 vs 1624). (BR render red 6223 vs orig
   2266 is the red plot frame + level lines, present in both classes.)
5. MAJOR "TR render = flat square surface + diagonal red line; orig = bowl with x10^4" —
   DOWNGRADED per generated-graph ground rule + the 02:45 att5 crop adjudication (z-axis
   present both, ticks ink present both, surface fill 28% vs 27%, floor stipple 3757 px,
   no localized defect): k14 TR is a deep paraboloid bowl with floor contour stipple.
   Camera/zoom difference of a regenerated matplotlib graph = medium difference, not MAJOR.
6. MINOR-MAJOR "TL narrower/steeper dome" — same generated-graph class, MINOR.
7. MINOR "Non- Convex hyphen spacing" — whitespace-only, MINOR.

Disposition: FULL fresh FAIL DISMISSED except claim 3 which stays registered (k15 swapped
the labels per the other worker's glyph-template measurement; k15 legs arbitrate).
CROP fresh leg (`crop_dense_judge_fresh.txt`) still pending at adjudication time.
Census vs the NEW k15 render banked: `adjudicate_k15_full_20261031.txt` (18.611% diff,
orig-heavy 132404 vs 68031, densest cells uniform bands only) and
`adjudicate_k15_crop_20261031.txt` (29.789% diff, densest cells in label/text bands).
No git; no evidence deleted.

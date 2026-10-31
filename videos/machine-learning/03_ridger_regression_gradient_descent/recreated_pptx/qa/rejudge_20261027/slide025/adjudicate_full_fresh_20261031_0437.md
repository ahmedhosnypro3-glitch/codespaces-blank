# Slide 025 fresh FULL leg — PIL-first adjudication (2026-10-31 ~04:37-04:55 UTC, second watcher agent-201)

Leg: `judge_full_fresh.txt` (clean, no 429; wrapper `judge_full_fresh.wrapper.out` = "OK attempt=1 rc=0",
FINAL VERDICT: FAIL, landed 2026-10-31 04:33 UTC) judging post-fix `render.png` (03:37:54,
2001x1125 150dpi; chrome_check_fresh PASS) vs `unique_slides/slide_025.jpg`.

Objective input: `rejudge_adjudicate.py 025 --full` -> `adjudicate_full_fresh_20261031_0437.txt`
(442,983 diff px = 19.7% of frame; densest cells = uniform band x672-816 y472-517, i.e. the BR
panel bottom edge; ink render-only 89,713 px vs orig-only 118,482 px).
Probes: `probe_fresh_20261031.py/.out`, `probe2_fresh_20261031.py/.out`.

Provenance check: all four `build/assets/plot_025_*.png` (regenerated 03:32, k14 wave) are
md5-identical to the PNGs embedded in `recreated_pptx/slide_025_recreated.pptx`
(image-1-1..1-4). The render under judgment contains the current generated plots.

## Claim-by-claim disposition

1. MAJOR "BR rugged multi-valley + winding path not rendered; smooth dome + one straight stroke"
   (high conf) — NOT pixel-supported. Render BR has MORE dark path ink than original
   (dark<80: 915 vs 30 px; 80-240: 9,327 vs 6,656) and the surface silhouette profile matches
   (mean |top-row diff| 2.68 px over 539/539 columns). REFUTED as stated (path present and
   heavier; terrain silhouette equal). Residual: winding-vs-straight curvature not measurable
   without vision; treated as downgraded MINOR.
2. MAJOR "BR surface flush to / cropped at bottom inner frame (orig has white margin)" —
   CONFIRMED. Orig colored% drops to ~1-5% from y524 (white margin) before the red bottom stroke
   at y535-539; render holds 69-70% colored down to y537, touching the frame. Matches the
   census's uniform bottom-edge band. STANDS — real defect: BR plot placed ~6 slide-px too
   low / too tall (build box y344..531 vs surface filling to y537).
3. MAJOR "BL minima labels swapped (LL 'Global' vs LR 'Local')" — REFUTED. Tight-band swap test:
   render-LL vs orig-LL diff 38.3 (best) vs render-LL vs orig-LR 70.0; render-LR vs orig-LR 51.1.
   Build measurements of the ORIGINAL independently place "Global Minima" at x145..201 y439..465
   (lower-left). No swap.
4. MAJOR/MINOR "BL red x markers at maxima + heavier leaders" — partially supported (render dark
   ink in label bands slightly higher: 732 vs 268 in LL band) but class MINOR; annotation style.
5. MAJOR "TR flatter square surface, central blue depression, added diagonal red line" —
   REFUTED in pixels: colored extents identical (orig x3-260 y5-199 vs render x3-261 y3-200 of
   the TR box; 25.6% vs 26.6%), red-line slope orig 0.004 vs render 0.000 (all horizontal runs;
   12,848 vs 6,075 red px — render has FEWER level lines, no added diagonal). Geometry equal.
6. MINOR-MAJOR "TL narrower/steeper peak" — colored extents match (x3-179 both; y3-4..170-171);
   colored% 21.9 vs 34.9 (fill density only). Downgraded MINOR.
7. MINOR "Non- Convex" spacing — whitespace-only; MINOR.

## Disposition

BLOCKERs: none. MAJORs: 1 stands (#2, BR bottom flush/overflow), 3 refuted (#1, #3, #5).
Per protocol ("certify only if MAJOR/BLOCKER refuted") slide 025 is NOT certifiable on this
fresh FULL leg. No DB / deck / result.txt PASS writes. CROP fresh leg
(`crop_dense_judge_fresh.txt`, TR bowl crop) pending at write time; adjudicated separately.

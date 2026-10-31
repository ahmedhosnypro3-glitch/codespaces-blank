# Slide 025 — fresh rejudge legs adjudication (2026-10-31 ~04:3x-05:xxZ, this spawn)

Bytes under test: `render.png` (2001x1125 150dpi, mtime 03:37:54) = render of
`recreated_pptx/slide_025_recreated.pptx` (03:32, k14 assets, md5 7a4143...);
`house_chrome_check.py` PASS (`chrome_check_fresh.txt`). Original:
`unique_slides/slide_025.jpg` (960x540).

## Legs

- FULL fresh: `judge_full_fresh.txt` (04:33:05, wrapper OK attempt=1, zero 429) —
  **FINAL VERDICT: FAIL**, clean. Banked: `judge_full_fresh.att1_clean_FAIL.bak` (sibling)
  + `judge_full_fresh.txt.cleanFAIL_0433.bak` (this spawn).
- CROP fresh: `crop_dense_judge_fresh.txt` — landed 07:22:47, **FINAL VERDICT: FAIL**,
  clean (zero 429), banked as `crop_dense_judge_fresh.txt.cleanFAIL_0722.bak`. Claims:
  (1) BLOCKER "3D relief flattened to heatmap, z-stack absent" — **REFUTED by pixels on
  the crop pair**: colored surface px render 55,422 vs orig 47,178 (render LARGER, not
  flattened); column row-extents show full 3-D height in both (R col x=304 rows 18-433
  194px vs O col x=299 rows 15-433 150px); left z-label strip has dark ink in both
  (6,556 vs 10,176). (2) left axis tick order reversed — plausible, medium conf, not
  pixel-checked here. (3) z-label stack collapsed — refuted as "absent" (ink present both),
  render glyphs smaller. (4) upper red line shifted + extra detached top-left diagonal
  stroke — SUPPORTED: red px y0-60 render 2,576 vs orig 1,028; y60-130 3,997 vs 2,665.
  (5) fill emphasis MINOR. Net: crop FAIL stands on red-line geometry; the BLOCKER is
  pixel-refuted but MAJORs 2-4 keep the verdict FAIL.

## FAIL claims vs PIL census (`adjudicate_fresh_full.txt`, `adjudicate_fresh_crop.txt`)

Full-frame census: 19.678% diff px; densest cells one uniform band x672..816 y472..517
(= BR panel bottom surface-fill band, 2350 diff px/cell); ink orig-heavy 118,482 vs
render-heavy 89,713 frame-wide. Crop census: 30.051% diff; render-heavy 17,754 vs
orig-heavy 19,952.

| # | Judge claim (MAJOR unless noted) | Pixel verdict |
|---|---|---|
| 1 | BR: orig rugged multi-valley + winding GD path; render smooth single dome + one straight stroke | PARTIALLY SUPPORTED. BR interior red ink R=45,103 vs O=14,007 (render far more red = colormap fill differences); BR bottom strips y495-531 render-heavy (17,392+9,408 vs 9,921+4,602) — surface fill extends lower in render. k14 BR is a multi-hill surface + S-curve (generate_plots_025_k14.py:252-298), so "single dome" reads as judge mis-description; the real delta is surface-fill coverage/height, not path absence. Generated-graph medium-difference class. |
| 2 | BR surface flush to bottom inner frame in render; orig keeps white margin | SUPPORTED at pixels: BR bottom strips y472-531 render ink 45k vs orig 31k (render surface reaches closer to the frame edge). Containment delta confirmed. |
| 3 | BL labels swapped: render lower-left "Global Minima" / lower-right "Local Minima" vs orig opposite | **REFUTED.** Label-box cross-IoU (render vs orig, boxes from build measurements GM x140-206 y435-468, LM x281-316 y386-402): R_GM↔O_GM 0.303 (vs O_LM 0.063); R_LM↔O_LM 0.723 (vs O_GM 0.128). Same word at same box in both images; no swap. Build header (slide_025.js:33-35) measured orig "Global Minima" lower-left x145..201 y439..465 — agrees with render. |
| 4 | BL: render adds red x markers at maxima, heavier leaders | PARTIALLY SUPPORTED: BL interior red R=7,420 vs O=5,407 (+37%); leader clutter plausible. Minor-severity class. |
| 5 | TR: render flat square surface + central blue depression + extra diagonal red line; orig clear bowl with level lines | CONTRADICTED BY EARLIER PIL GATE: k14 TR bowl sign confirmed (pil_k14_geom_check.txt: main-diag center-minus-edges ORIG +29.0 vs RENDER +26.5, both convex bowl; red level lines at matching native rows; ticks/stipple present in both). TR interior red R=14,421 vs O=11,488 (+25%) — the "diagonal red line" is within contour-line class, not a lone artifact. Judge's "flat sheet" reads against the certified bowl. |
| 6 | TL dome narrower/steeper (MINOR-MAJOR) | Advisory; TL interior red R=4,214 vs O=5,357 (render less red, opposite direction of claim). |
| 7 | "Non- Convex" hyphen spacing (MINOR, low conf) | Whitespace-only; not a defect. |

## Disposition

Clean full-fresh **FAIL stands** (claims 1-2 supported, 4 partial, 3 refuted, 5 contradicted
by the certified k14 bowl gate). Clean crop-fresh **FAIL stands** (red-line geometry MAJORs
supported; BLOCKER pixel-refuted). FAIL path per watcher mandate: adjudicate (done, both
modes banked), bank, report. **No DB write, no deck update** (PASS+PASS required for those;
DB row 25 remains `building`/'' — open, last checked 07:06Z). No git; no evidence deleted;
no builds modified. Fix dispatch for the BR surface fill/containment (full claims 1-2) and
TR upper red-line geometry (crop claim 4) is the orchestrator's call.

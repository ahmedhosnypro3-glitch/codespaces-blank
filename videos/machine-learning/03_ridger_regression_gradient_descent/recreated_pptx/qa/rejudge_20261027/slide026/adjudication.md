# Adjudication — slide026 CROP FAIL (`crop_dense_judge.txt`, banked 2026-10-29 23:45) — OVERTURNED 2026-10-30

Read-only adjudication (no edits to builds/pptx/DB; no git). Register entry:
`../REJUDGE_REGISTER.md` → "Adjudication 2026-10-30 — slide026 CROP FAIL".

## Inputs

- FAIL transcript: `crop_dense_judge.txt` (winner `images`, round 1 attempt 1; log `crop_dense_judge.log`).
  7 numbered findings + 1 uncounted note; FINAL VERDICT: FAIL ("serif→sans substitution plus two missing
  underlines").
- Images: `crop_dense_render.png` vs `crop_dense_orig.png` (both 634x434); full `render.png` (2001x1125,
  150dpi, scale 2.0844/2.0833) vs `unique_slides/slide_026.jpg` (960x540, 1px = 1pt).
- Context: full leg `judge_full.txt` = PASS (3 MINORs: body blue shade, "approximatly" italic, font family
  settled house-mandated MINOR); `result.txt` region = frame px (136,88)-(440,296) "Gradient Descent
  Solution" dense region; `chrome_check.txt` HOUSE CHROME CHECK: PASS.
- Build ground truth (read-only): `build/slide_026.js` — FONT="Arial"; measured underline bars in the
  ORIGINAL: rowB y192..194 x349..716, rowD y258..260 x287..473 (continuous), N3 y458 two runs; NO rowA bar;
  rowA span "Random Weights (W)" bold-only; rowD "gradient is " + "almost zero" underline:true (bold on
  "almost zero"); rowC "w.r.t. W" regular. `analysis/slide_026_raw.json` typography: "Sans-serif typeface".

## Method

1. Geometry proof of the crop pair (PIL, exact reconstruction).
2. `rejudge_adjudicate.py 026 --crop` and `--full` (diff-density map).
3. Per-claim targeted measurements in slide space (render coords = slide px × 2.0844/2.0833); predicates:
   blue = (B>120, B−R>60, B−G>60), red = (R>100, R−G>50, R−B>50), dark = sum<450. Positive control: the
   rowB underline bar must be found in both images (it is: 365px run orig @y192; 767px render-native =
   368 slide px @y191.9).
4. Crop→slide mapping: slide_x = 136 + cx/2.0855, slide_y = 88 + cy/2.0865. Transcript coords map to:
   heading crop-y≈55 → slide y≈114 (GD header band y110-123); body crop-y≈130 → y≈150 (rowA y143-156);
   "Random Weights" crop-y 125-145 right side → rowA band, slide x up to the crop edge 440; "(w.r.t. W)"
   crop-y≈270 → slide y≈217 (rowC band y210-226).

## Geometry proof

- `crop_dense_render.png` == `render.png[183:617, 283:917]` exactly (0 of 275,156 px differ, max diff 0).
- `crop_dense_orig.png` == `slide_026.jpg[88:296, 136:440]` resized LANCZOS to 634x434 exactly (0 diff px).
- Effective scale: render crop 634/304 = 2.0855 (x), 434/208 = 2.0865 (y); full render 2.0844/2.0833 —
  matched within 0.1%. The pair is a legitimate matched-scale crop of slide region (136,88)-(440,296).

## Per-claim dispositions

| # | claim (severity) | disposition | pixel evidence |
|---|---|---|---|
| 1 | MAJOR — orig all-serif, render all-sans, region-wide; "not covered by ground rules" | **REFUTED** | Native-res grayscale glyph art of the original (title "S"/"G" at 27.5pt, body "t" at 17.5pt): constant-width 2-3px stems, flat/rounded terminals, no serif flares — sans-like at 1x. The "clear serifs" appear only in the 2.09x upscale = LANCZOS interpolation + JPEG q4 ringing on IMG2, which Template B rule (e) explicitly exempts. Banked certification analysis (`slide_026_raw.json`) independently records "Sans-serif typeface". Recreation font is house-mandated Arial (`build/slide_026.js:70`), already settled MINOR by the full leg (`judge_full.txt`). Not a defect, not a fix trigger. |
| 2 | MAJOR — underline under "Random Weights" [1] present in orig, missing in render | **REFUTED** | No bar below rowA in EITHER image: over slide x146-500, y157-164, longest blue run = 12px (orig, y159), 16px (render, y157.4); dark predicate ≤15px — descender noise. A real underline bar is 150-350px (rowB control: 365px orig / 368 slide-px render). The build's measured bank lists NO rowA bar; render matches the original (bold-only span). |
| 3 | MAJOR — render underline stops after "gradient is"; "almost zero" not underlined | **REFUTED** | Continuous bar in BOTH images over x287-473: orig 181px run @y259 (coverage 0.905 of x280-480), render 202px run @y257.2 (coverage 0.921); split check x287-340: render 100%, x340-473: 97.5% — continuous through "almost zero". At the crop right edge (crop x560-634, rowD band) both crops show the identical 74px run — the bar reaches the crop edge in both. Build implements underline:true on "gradient is " + "almost zero". |
| 4 | MINOR — [1]/[2]/[3] labels bold in orig, regular in render | **PARTIALLY SUPPORTED** (advisory only) | Orig label bracket stems 3-4 slide px vs render 1.92 slide px; label-zone ink 130-146px orig vs 113-126px render-downscaled (the downscale is globally biased toward MORE ink — controls show render denser — so the label deficit is real). Consistent with slightly heavier orig labels. MINOR severity: advisory, not FAIL-sustaining, no fix action in this read-only adjudication. |
| 5 | MINOR — W in "(w.r.t. W)" bold-italic in orig, bold-upright in render | **PARTIALLY SUPPORTED** (advisory only) | W glyph (slide x201-216, y210-227) per-row-centroid slant: 0.27 px/row orig vs 0.141 px/row render (~2x lean in orig), direction consistent with italic. Confounded with claim 1 (face/style) and JPEG at native res. MINOR: advisory only. |
| 6 | MINOR — top blue rule thicker and darker in render | **REFUTED** | The "top rule" is the blue content-box top border, slide y90-92 (crop y≈4-8). Thickness: orig 3.0 slide px (y90-92) vs render 3.04 slide px (y89.3-90.2) — equal. Color: orig core (45,33,130) dark navy (JPEG-diluted) vs render (0,0,255) pure blue — the render is BRIGHTER, the orig DARKER; the claim's direction is reversed. Same inner frame present in both (full leg: "Inner blue frame — present in both"). |
| 7 | MINOR — heading red darker/maroon in render | **REFUTED** | Render red core median (192,0,0) = house C00000 exactly. Orig red pixels are JPEG-chroma-diluted at 960x540: p50 (222,138,147), p97 (255,177,187) — IMG2 never reaches pure red. The perceived "brighter red" in IMG2 is the dilution artifact (rule e), not a hue difference. |
| note | right-edge truncation reads "almost z…" (render) vs "almost s…" (orig) | **DISMISSED** | Both crops are pixel-exact reconstructions of the SAME slide-space region (0 diff px), so the right-edge glyph is the same character in both; the differing letter read is a vision misread of identical pixels. The transcript itself flags it as a crop-offset artifact. |

## Vision re-leg

Skipped: the optional ONE gate leg requires `pgrep -c -f analyze_image.py < 8`; count was 61 at
2026-10-30 adjudication time (live certification drivers for slides 014/015/… occupying the shared
localhost:17844 gateway). PIL evidence is decisive for all three MAJORs (positive control rowB bar
validates the bar detector), so the leg was not needed.

## Disposition

All 3 MAJOR findings REFUTED by pixels; MINORs 6/7 refuted, 4/5 partially supported but advisory-only
(MINOR). Per `shared_patterns/judge_protocol_03.md` §7 — a crop-pair is clean when its transcript is PASS
or every raised finding is PIL-refuted — the slide026 crop leg is adjudicated CLEAN. The harvest-sweep
register row `slide026 | PASS | FAIL` is overturned on the CROP leg (FULL was already PASS). Slide 026's
certification stands; no reopen, no fixes dispatched, no edits to builds/pptx/DB.

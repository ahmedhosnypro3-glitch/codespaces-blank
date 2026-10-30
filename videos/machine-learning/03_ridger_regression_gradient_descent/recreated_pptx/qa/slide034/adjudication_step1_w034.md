# Adjudication of crop_3_table_judge.txt (FINAL VERDICT: FAIL) — worker w034-finish-20261024

Banked FAIL (2026-10-24 01:17): row "x" c16 = 9.8 must be 9.6; c18 = 9.8 must be 9.6.
Adjudicated PIL-first against BOTH images (unique_slides/slide_034.jpg and
recreated_pptx/qa/slide034/render_6.png, frame px, 1px=1pt).

## Method (independent re-measurement, worker-fresh-034b's step1 method extended)
x-row text band isolated at rows 334..344 (flanked by gridlines 330/331, 348/349).
Cells segmented on the band's column profile (>=2 ink rows, gaps merged <=3px):
c13 639-653, c14 682-694 (KNOWN 9.6), c15 725-734 (KNOWN 9.8), c16 765-775,
c17 807-817, c18 843-853. Units digit classified by NCC of the right-digit
bitmap (rows 333..346, native resolution, thr=150) against c14 ('6') and c15 ('8').

## Controls (method validated)
c14 -> NCC 1.000 vs '6', 0.710 vs '8'  => '6'  (expected 6) OK
c15 -> NCC 0.710 vs '6', 1.000 vs '8' => '8'  (expected 8) OK

## Results
c13 -> 0.627 vs 0.836 => '8'
c16 -> **0.959 vs 0.754 => '6'**   margin 0.205 DECISIVE
c17 -> 0.762 vs 0.640 => '6'       margin 0.122 (a second extraction at thr=175
                                     +dilation read '8'; hence straddled)
c18 -> 0.762 vs 0.795 => '8'       margin 0.033 AMBIGUOUS (second extraction
                                     read '6'; straddled)

## Adjudication outcome
1. **c16 finding: REFUTED for render_6.** The ORIGINAL's c16 units digit reads '6'
   decisively (NCC margin 0.205), and render_6 already prints 9.6 at c16
   (build: [.., 9.4, 9.6, 9.8, **9.6**, 9.8, 9.6]). Render matches the original;
   the FAIL's c16 finding is already satisfied by the current build.
2. **c18 finding: NOT REFUTABLE from glyphs alone, but the build's 9.6 stands.**
   The glyph is ambiguous at 6px height (margin 0.033). The build's choice is
   forced by the slide's OWN dataset arithmetic (four independent rows):
   f(x) c18 = -10.03 = f(9.6); x-delta c18 = 9.5 => x = 9.6; slope c18 = -0.7
   => x = 9.6; next-x c17 = 9.6. All four require 9.6. Changing it to 9.8 would
   make the table internally contradictory. KEEP 9.6.
3. render_6's x row tail (9.8, 9.6, 9.8, 9.6, 9.8, 9.6) therefore matches BOTH
   the measured original glyph at c16 AND the dataset's internal consistency.

## Net
No build change is required from crop_3's FAIL: render_6 already satisfies it.
Script: scratch/tmp/w034/xrow3.py, xrow_num.py (native-resolution NCC + ASCII).

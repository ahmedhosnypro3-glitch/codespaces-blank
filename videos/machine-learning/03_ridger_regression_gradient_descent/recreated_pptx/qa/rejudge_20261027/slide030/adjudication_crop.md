# Slide 030 rejudge crop-leg adjudication (2026-10-31 04:0x UTC, fresh worker)

Legs: judge_full.txt FAIL (adjudicated separately -> dismissed, see above);
crop_dense_judge.txt FINAL VERDICT: FAIL (clean; a parallel w03 snap PASSed).

Judge MAJOR claim (crop): the `x` header row of the big iteration table renders on a
near-white fill while the original's is yellow (whole-row fill mismatch).

PIL-first adjudication (`rejudge_adjudicate.py 030 --crop` -> adjudicate_fresh_crop.txt):
27.5% crop diff, densest cells ~240 px/24px cell spread across table rows (glyph AA),
no localized fill block.

Targeted fill sampling (slide-space px, render 2001x1125 vs unique_slides/slide_030.jpg):
- x-row cell @(500,344): render RGB(214,225,125) vs orig RGB(219,229,117)
- f(x)-row cell @(500,366): render RGB(214,225,125) vs orig RGB(216,225,116)
The render's x row and f(x) row share one fill (D6E17D light green, per
build/slide_030.js iterG1Fill), and the original's x row samples the SAME color as its
f(x) row within photo noise. There is no white-vs-yellow row split in either image.

Disposition: crop-leg FAIL DISMISSED — MAJOR refuted by pixel samples; remaining MINORs
(red "3" callout digit, medium glyphs) are advisory per ground rules.
FULL=PASS(dismissed), CROP=PASS(dismissed).

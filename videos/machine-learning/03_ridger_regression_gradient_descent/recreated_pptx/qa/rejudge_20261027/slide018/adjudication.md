# Slide 018 rejudge crop-leg adjudication (2026-10-31 02:5x UTC, fresh worker)

Legs: judge_full.txt FINAL VERDICT: PASS (clean); crop_dense_judge.txt FINAL VERDICT: FAIL (clean).

Judge MAJOR claim (crop): bottom-right data cell of the bottom visible table row reads
`22` in the render vs `2` in the original (crop-relative y~85-100%, x~90-100%).

PIL-first adjudication (`rejudge_adjudicate.py 018 --crop` -> adjudicate_fresh_crop.txt):
13.6% crop diff, densest cells spread across glyph lines (max 249 px in a 24px cell,
no localized missing block); render-heavy 3,195 px vs original-heavy 8,683 px overall.

Targeted cell measurement (slide-space x409-440 y360-392, render 2001x1125 vs
unique_slides/slide_018.jpg): render cell = 202 ink px in 2 glyph-columns at thr<100;
original cell = 23 ink px in 1 glyph-column (53 px at thr<180, 288 px at thr<240) —
the original's handwritten glyphs are faint/merged at threshold, i.e. a single "22"
written in light handwriting, not a bare "2". Zoomed evidence: cell_orig_zoom.png /
cell_render_zoom.png in this dir.

Ground truth: slide_018_final.json (vision analysis OF THE ORIGINAL FRAME) records all
three train-table y-rows ending in `... 18 20 22` (X8 = 22), and build/slide_018.js
lines 44-46 render exactly those values. Render typed-bold "22" vs faint handwritten
"22" is a medium difference covered by the ground rules.

Disposition: crop-leg FAIL DISMISSED — no content discrepancy. FULL=PASS, CROP=PASS(dismissed).

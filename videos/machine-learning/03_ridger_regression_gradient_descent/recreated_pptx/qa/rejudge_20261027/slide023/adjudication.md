# Slide 023 rejudge crop-leg adjudication (2026-10-31 02:5x UTC, fresh worker)

Legs: judge_full_retry.txt FINAL VERDICT: PASS (clean; judge_full.txt never landed);
crop_dense_judge.txt FINAL VERDICT: FAIL (clean).

Judge MAJOR claim (crop): extra underlined top text line "Recall" in the render
(crop coords x~8-125, y~0-45) that the original supposedly lacks, pushing the
equation row lower.

PIL-first adjudication (`rejudge_adjudicate.py 023 --crop` -> adjudicate_fresh_crop.txt):
23.0% crop diff, densest cells spread across glyph lines (max 259 px/24px cell, no
localized block); original-heavy ink overall.

Targeted measurement on the crop pair (634x434): top-left box x8-125 y0-45 has
488 dark px in the RENDER and 299 dark px in the ORIGINAL — the original carries
the same ink there (handwriting is lighter, hence fewer px below thr<100); top band
y0-60: render 2,841 vs orig 2,151. The original is not missing the line.

Ground truth: slide_023_final.json (vision analysis OF THE ORIGINAL FRAME) lists
"Recall:" in labels — the original slide itself carries the "Recall:" line.

Disposition: crop-leg FAIL DISMISSED — the "extra Recall line" exists in the original;
the judge misread the handwritten original. FULL=PASS, CROP=PASS(dismissed).

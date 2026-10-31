# Slide 030 rejudge full-leg adjudication (2026-10-31 03:3x UTC, fresh worker)

Legs: judge_full.txt FINAL VERDICT: FAIL (clean, 03:2x); crop_dense_judge.txt pending at
scan time.

Judge MAJOR claim (full): central annotation stack (equation box / green formula box /
purple callout) sits ~0.07 of slide height higher and shifted right in the render vs the
original; purple box wider (0.31 vs 0.24 slide width). MINORs: title run color, mini-table
geometry, graph width, bottom-row red outlines.

PIL-first adjudication (`rejudge_adjudicate.py 030 --full` -> adjudicate_fresh_full.txt):
13.5% frame diff, densest cells ~1.2-1.4k px per 24px cell spread across the frame (no
localized missing block); original-heavy ink 170,419 px vs render-heavy 60,971 px —
photo-texture original vs white render, as usual.

Targeted central-stack measurement (slide-space px; render 2001x1125 vs
unique_slides/slide_030.jpg):
- green formula box border: render x347-554 y232.7-281.1 (top 43.1%H, w 21.6%W) vs
  original x348-553 y235.0-280.0 (top 43.5%H, w 21.4%W) — aligned within 3 px in both
  axes. The original's own analysis (slide_030_final.json layout) puts formula_block at
  y 44-62% — the render sits exactly there. The "shifted up/right" MAJOR is REFUTED.
- callout width: build/slide_030.js callout box w=234 px = 24.2%W, matching the judge's
  own estimate of the ORIGINAL's width (0.24); the "wider purple box (0.31)" claim is
  REFUTED by build bytes. (Lavender-fill mask on the render: x335-568, w 24.2%W.)
- MINORs (title run color, mini-table/graph geometry, red outlines on "stop" row) are
  color/geometry nits of the kind covered by the medium-difference ground rules.

Disposition: full-leg FAIL DISMISSED — MAJOR refuted by pixels + build bytes; no BLOCKER
was claimed. FULL=PASS(dismissed); CROP per its own transcript.

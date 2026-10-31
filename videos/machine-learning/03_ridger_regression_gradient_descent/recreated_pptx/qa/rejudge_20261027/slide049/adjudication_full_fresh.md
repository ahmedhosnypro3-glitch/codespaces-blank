# slide049 FULL leg FAIL — PIL-first adjudication (2026-10-31 ~03:1x UTC, fresh worker W03)

Transcript: `judge_full.txt` (clean, no 429) — FINAL VERDICT: FAIL.
PIL diff: `adjudicate_full_fresh.txt` (`rejudge_adjudicate.py 049 --full`): 215,041 diff px
(9.55% of frame); ink only in render 49,746 px vs only in original 100,723 px (typed-vs-handwritten
ink asymmetry, diffuse).

## MAJOR #1 "Augmented Vectors table has 4 data rows, `1 1 2 4 5 6` duplicated" — REFUTED
- Build source `build/slide_049.js:200-210`: exactly 3 data rows, `bands = [183, 198, 213]`,
  vals columns `[1,1,1],[1,2,1],[1,1,2],[1,5,4],[1,6,5],[1,6,6]` → rows are
  `1 1 1 1 1 1` / `1 2 1 5 6 6` / `1 1 2 4 5 6`. No fourth row exists in the build.
- Render pixels: first-column digit rows in the aug zone are exactly three bands
  y184.2-191.9 / 199.6-207.3 / 214.5-222.1 (slide-space) — no duplicated fourth row.
  (The merged band y180.1-226.2 in the coarse scan is the continuous delimiter bars y180 h46,
  not a row.)
- "Box taller / Iteration 2 pushed lower": render Iteration-2 red box x83.5-213.0 y277.8-304.1
  matches the build spec (x84..213 y278..304); not displaced.

## MINORs — advisory / ground-rule exempt
- #2 straight-bar delimiters: founder doctrine (straight 1px bars for matrix/vector parens).
- #3 first-element red / W-vector green accents: color accents, MINOR per transcript.
- #4 box fill style: house template, ground-rule exempt.

Disposition: FULL = PASS (dismissed). No rebuild. Crop leg verdict pending at time of writing.

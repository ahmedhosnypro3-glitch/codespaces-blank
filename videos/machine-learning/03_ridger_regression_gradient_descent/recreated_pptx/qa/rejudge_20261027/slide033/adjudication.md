# Slide 033 rejudge full-leg adjudication (2026-10-31 04:1x UTC, fresh worker; revised after two-sided PIL)

Legs: judge_full.txt FINAL VERDICT: FAIL (clean; w03 snap FAIL too);
crop_dense_judge.txt / crop_dense_judge_fresh.txt FINAL VERDICT: PASS.

Judge MAJOR claims (full): (1) red block arrow direction reversed; (2) dashed cyan
callout rectangle over the -9.7/-9.6/-9.7 columns absent; (3) systematic vertical
compression of content; (4) teal curve overruns the chart's top red frame.

PIL-first adjudication (`rejudge_adjudicate.py 033 --full` -> adjudicate_fresh_full.txt,
identical to W02's adjudicate_W02_full.txt): 17.1% frame diff, densest cells ~1.3k px per
24px cell spread across glyph lines, original-heavy ink (195k vs 52k) — no localized
missing-element block.

Claim-by-claim:
- (2) Cyan callout: build draws fill 8BF8AB + maroon dashed border at x666-787 y332-368
  (slide_033.js:300-303, inCyan cols 13-15 of rows x/f(x)). Render shows 12,182 cyan-fill
  px in that box; original photo shows 2,827 (muted). Present in BOTH. REFUTED.
- (4) Curve/frame: render chart top red frame at slide-y 59 with 22 teal px within 6 px
  below; original frame at y 60 with 0. AA-level touch, not an overrun. REFUTED (MINOR at most).
- (3) Compression: diffuse PIL diff, build geometry frame-measured per build comments.
  Not sustained as MAJOR. REFUTED.
- (1) Arrow direction: render arrow red-outline bbox x159-206 y284-319, widest rows at
  y313-315 and max column height at x205 -> head at BOTTOM-RIGHT, i.e. the render arrow
  points DOWN-RIGHT (build/slide_033.js:152 rightArrow rotate:45 at x156 y297).
  W02's two-sided PIL (adjudicate_W02_full.txt, quoted in slide033/result.txt) measured
  the ORIGINAL's hand-drawn arrow with head at x177-190 y295-303 (top) and tail at
  x165-177 y335-352 (bottom) -> original points UP toward the param box. The rejudge
  judge assigned the directions the other way round, but both sides agree the two
  arrows do NOT point the same way. CONFIRMED as a real MAJOR (arrow direction
  mismatch), not refuted.

Disposition: full-leg FAIL STANDS on claim 1 (arrow direction). Claims 2-4 refuted.
FULL=FAIL (one surviving MAJOR); CROP=PASS. Slide 033 needs a build fix (flip/rotate
the block arrow to match the original's up-pointing direction) before re-judge;
no DB/deck changes made by this worker.

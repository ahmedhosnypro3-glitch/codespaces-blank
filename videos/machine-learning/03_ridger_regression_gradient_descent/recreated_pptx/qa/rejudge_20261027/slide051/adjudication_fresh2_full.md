# slide051 FULL fresh2 adjudication (2026-10-31, this worker, PIL-first, read-only)

Leg: `judge_full_fresh2.txt` (2026-10-31 ~03:2xZ, clean transcript, no 429): FINAL VERDICT FAIL.
Single discrepancy: BLOCKER/MAJOR "missing enclosing rectangle around the left
'Augmented Vectors ( from Top )' block — IMG2 has a thin bordered rect approx x80-247 y156-271;
IMG1 shows the content directly on the gray panel" (confidence 0.80).

PIL evidence (`adjudicate_fresh2_full.txt` + targeted probes, slide-space px, render 2001x1125 sc 2.0844):

- Interior fill of the block x90-240 y165-265: ORIG bright-pixel median (254,255,253) = WHITE card;
  RENDER median (233,233,231) = the bare gray house panel E9E9E7. The recreation has NO white card
  behind the augmented matrix.
- Edges (hairline-aware, dark sum<660; panel bg sums 703): ORIG right edge col x246 dark 116/150
  (77%) over y140-290, top edge y156-158 dark 143/501 (partial), left x80 16/150 (weak), bottom 0.
  RENDER: right edge 0/313, top 666/2088 (32%, the block title baseline), left 37/313, bottom 0.
  Row scan y200: ORIG has ink at x245-246; RENDER has none there.
- `analysis/slide_051_final.json` visual_elements/layout describe the augmented matrix with NO
  enclosing card (label above a matrix), but the frame pixels show a white card + right border —
  the analysis missed it; the frame wins.

Disposition: claim CONFIRMED — the original encloses the augmented block in a white card with a thin
border (right edge x~246, partial top), the recreation omits it (content on gray panel). One MAJOR
survives PIL, so the FULL leg FAIL stands. Slide 051 is NOT clean in this wave on the full leg; reopen
build `slide_051.js` (add the white card + hairline border around the augmented block, measured
x~80-247 y~156-271), rebuild, re-render, re-run both legs. CROP leg still in flight at time of
writing. No DB/deck/pptx changes made by this worker. No git; no evidence deleted.

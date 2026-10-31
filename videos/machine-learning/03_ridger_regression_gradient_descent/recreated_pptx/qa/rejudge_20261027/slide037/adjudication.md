# slide037 — CROP-leg FAIL adjudication (2026-10-31, fresh worker W01, PIL-first)

Transcript: `crop_dense_judge.txt` (clean, no 429; leg via `vision_leg.sh` t=600
payload_B_037, driver `driver_W01.log`) — FINAL VERDICT: FAIL.
Claims: MAJOR #1/#2 top-panel rule lines "misclassified ... as" cut mid-word at the
crop right edge in IMG1 only; MAJOR #3 lower-panel green error term X subscript i
missing/clipped in IMG1; MINORs #4-#7 (delta subscript color, last-line typography,
Sigma subscript spacing, crop top edge).

Evidence (read-only PIL, slide space 960x540; crop region 60,136-344,344;
`adjudicate_w01_crop.txt` = `rejudge_adjudicate.py 037 --crop`;
`adjudicate_w01_crop_pil.txt`):

- Crop pair proven the SAME slide-space region: `crop_dense_render.png` == render.png
  crop of (60,136)-(344,344) (0 diff px, identical arrays) and `crop_dense_orig.png`
  == slide_037.jpg same region LANCZOS-upscaled (identical arrays) — both 592x434.
- Rule-line bands y144-160 / y170-186: ink runs reach the crop edge x344 in BOTH
  images, and both continue beyond it (orig ink to x589, render to x592.5) — the
  crop boundary cuts both crops identically; any mid-word cut at the edge is a
  region artifact, and horizontal advance differences are ground-rule MINOR
  (typed vs handwritten). FULL leg PASS (`judge_full_retry.txt`) confirms complete
  text in the full frame.
- Green error term: orig green bbox x279-437 y268-283; render green x279-352 y265-287
  — the render's term actually ends CLOSER to the crop edge, so IMG1 shows MORE of
  the term inside the crop than IMG2. Subscript ink present in the render at
  x345-380 y278-290 (54+124 dark px); `analysis/slide_037_final.json` verbatim carries
  X_i repeatedly; `build/slide_037.js:143` renders the subscript run explicitly.
  Claim #3 REFUTED.
- Claim #4 (delta subscript red vs green): build comment `slide_037.js:23` records
  the original's delta_i subscript as RED (measured at build time) — MINOR/advisory
  at most.

Disposition: all 3 MAJORs REFUTED (crop-boundary artifact / advance-width class /
subscript present); MINORs advisory per ground rules. CROP = PASS (FAIL dismissed).
FULL = PASS (`judge_full_retry.txt`). Slide stays certified; no build/pptx/DB change;
no git; no evidence deleted.

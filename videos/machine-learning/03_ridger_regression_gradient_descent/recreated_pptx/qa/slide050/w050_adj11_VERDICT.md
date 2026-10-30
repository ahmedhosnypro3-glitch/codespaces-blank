# Slide 050 — adjudication of judge_attempt_11 (render_13)

Verdict transcript: `judge_attempt_11.txt` (FINAL VERDICT: FAIL, 3 findings).
All three findings PIL-adjudicated against `render_13.png` vs
`unique_slides/slide_050.jpg` — **all REFUTED**. Scripts banked alongside:
`w050_adj11.py` (superseded — had an image-scale bug), `w050_adj11b.py` +
`w050_adj11b_raw.txt` (F1 corrected), `w050_adj11c.py` (superseded — tick
labels not found where probed), `w050_adj11d.py` + `w050_adj11d_raw.txt`
(line + label measurement), plus the inline F3 red-ascii comparison.

Measurement-scale note: original is 960×540 (frame px == image px, scale 1.0);
render_13 is 2001×1125 (scale 2.0844). The first adj11 run applied the render
scale to BOTH images — original-side zones beyond x460 were out-of-bounds and
vacuous. Corrected in adj11b/adj11d. Tick-mark calibration (identical in both
images): x ticks at px 363..784 step 52.6 (data 0..8); y ticks at py 428.5..213.5
step 30.71 (data 0..7).

## F1 "Omitted text 'η = 1'" (judge: MAJOR, high conf) — REFUTED

Claim: original red header reads "REPEAT using Step η = 1"; render stops at
"REPEAT using Step".

- ORIG red phrase extent x426..530; eta zone x531..642 y58..84 ink = **0**,
  red = 0 (w050_adj11b_raw.txt F1/F1b/F1c).
- RENDER phrase extent x426..527; same zone ink = 7 px (antialias residue).
- The ascii confirms: original has NO ink right of "Step" until the Z-matrix
  bracket arc at x645+. "η = 1" appears nowhere in the original header.
- 5th independent refutation of this recurring judge hallucination (att7–att11).

## F2 "Decision-boundary line geometry" (judge: MAJOR, medium-high conf) — REFUTED

Claim: render line slope ≈ −0.85 reaching x≈6.3 at baseline vs original slope ≈ −1
through (3,2) hitting y=0 at x≈5.

Tick-calibrated line fits (w050_adj11d_raw.txt, thin-run extraction with
long-run removal, 5-round trimming):

| image | line endpoints (frame px) | slope (data) | x@y=0 (data) |
|---|---|---|---|
| ORIG | (337,264) → (690,467) | **−0.985** | **4.95** |
| RENDER | (335,264) → (679,461) | **−0.986** | **4.93** |

Both lines have slope −0.99 and x-intercept 4.9–5.0 — i.e. the geometry the
judge attributed to the ORIGINAL is present in BOTH images. The claimed
"render slope −0.85 / intercept 6.3" is quantitatively false. Endpoint delta at
the below-axis overshoot tail is ≤11 frame px (render tip ends ~0.2 data-units
earlier); slope/intercept/meaning identical.

## F3 "'+ve' arrow/label position" (judge: MINOR, medium conf) — REFUTED as stated

Claim: "+ve" shifted ~0.5 x-unit right vs original.

- ORIG "+ve" red text cluster bbox x373..395 y306..315 (centroid ≈ (384,310)).
- RENDER "+ve" red text cluster bbox x382..401 y308..328 (centroid ≈ (391,318)).
- Measured offset ≈ **+7px x / +8px y** ≈ **0.13 x-units**, not 0.5. Same glyph
  structure, same arrowhead, decision line passes at matching positions
  (ascii comparison banked in the run log). Residual ≤8px offset is within the
  checker tolerance used across this deck (e.g. badge-ring tol 8) and was
  already refuted as in-both in att10 (F9).

## Disposition

att11 = FAIL verdict whose every finding is measurement-refuted ⇒ adjudicated
clean. Per the deck's dual-leg law, certification additionally requires the six
Template B crop certificates on render_13 (`crop_13_*_judge.txt`, dispatched via
`run_crop_judges_13.sh`). Render: `render_13.png` (md5 124923-byte artifact of
pptx `00728fa5c09607e056b6518d5800b3b2`), house_chrome_check PASS, LO re-render
deterministic (0 px diff).

# Slide 026 worker report — "Gradient Descent Solution" (deck 03, Ridge Regression & Gradient Descent)

**Claim:** `w26-r3-20261021T0538` (resume worker; the previous worker died during a provider
outage after banking builds through attempt 3).
**Deliverable (single version, no suffixes):**
`videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_026_recreated.pptx`
built by `.../recreated_pptx/build/slide_026.js` (run from the project root; NODE_PATH
`/home/ahmed/.npm-global/lib/node_modules`).
**Final render:** `qa/slide026/render_9.png` (md5 `b3a5b9e0082de44df247474ff40679ce`,
2001×1125, fresh LibreOffice profile `scratch/tmp/lo_s026_a9`).

## Final DB row (verified with `get 026`)

| field | value |
|---|---|
| gen_status | `passed` |
| visual_check | `PASS` |
| visual_attempts | `5` |
| visual_transcript | `judge_attempt_5.txt` (Template A PASS, 0 discrepancies); `crop_9_notes_judge.txt` (Template B notes PASS, 0 discrepancies); `crop_7_alg_judge.txt` (Template B alg PASS, MINOR PIL-refuted) |
| last_error | `null` |
| worker_id / heartbeat | `w26-r3-20261021T0538` / set |

## FINAL RESULT: PASS (all three legs clean on render_9)

Template A full-slide (`judge_attempt_5.txt`): PASS — zero discrepancies at any severity.
Template B alg crop (`crop_7_alg_judge.txt`): PASS. Its single MINOR ("Random Weights (W)
underline") is PIL-refuted in `adjudication_a7_algcrop.md`: the pptx contains exactly 6
underlined runs and none is on rowA; no horizontal stroke exists in that band in either image
(the widest run is 28 crop px vs a real bar's 200–400; render's y154 fragments are descender
bottoms). Region unchanged since render_7 — pixel-diff proof (see attempt timeline).
Template B notes crop (`crop_9_notes_judge.txt`): PASS — zero discrepancies, "Discrepancies:
None identified in this region."
House chrome on render_9 (`house_chrome_9.txt`): PASS (panel x113..1882 / y94..bottom; red
strokes LEFT x121 / RIGHT x1876 / BOTTOM y1121 = frame x58.5 / x901 / y538.5 within ±8; no top
stroke; badge center (1824,151) d=67; canvas white).

## Attempt history (render → legs → outcome)

| # | render | change | legs | outcome |
|---|---|---|---|---|
| 1–3 | banked by dead worker | predecessors | — | superseded |
| 4 | render_4 | per-line charSpacing closure of real width residuals (building.md law: tracking, never font size) | selfcheck REVIEW | widths closed |
| 5 | render_5 | noteshdr / rowD asymmetric tracking | selfcheck REVIEW | refinements |
| 6 | render_6 | rowC tracked on BLUE runs only so the red tail lands at x520..682 | selfcheck REVIEW | refinements |
| 7 | render_7 | **rowC ')' RED→BLUE** (measured core (28,18,139), b−r +111 — the most saturated blue run on the slide; all three blue runs are 0000FF in the pptx) | Template A `judge_attempt_3.txt` PASS + 2 MINOR; alg crop PASS + 1 MINOR; notes crop FAIL | 3 MINORs PIL-refuted (`adjudication_a7_templateA.md`, `adjudication_a7_algcrop.md`); notes-crop MAJOR CONFIRMED |
| 8 | render_8 | **"approximately"→"approximatly"** (N3) + per-run charSpacing 0.12/0.35/0.05 | Template A FAIL (3 findings); notes crop PASS + 1 MINOR | 3 Template-A findings PIL-refuted (`adjudication_a8_templateA.md`); notes MINOR CONFIRMED |
| 9 | render_9 | **"Least Squares " bold** (N1) + per-run charSpacing (bold LS 0.02, plain runs 0.06) | Template A PASS; notes crop PASS | **PASS — deliverable** |

## Adjudications (PIL-FIRST, both images, 1px = 1 frame pt on the 960×540 frame)

1. **rowC ')' color (CONFIRMED, fixed attempt 7).** Original's disputed phrase core is
   (28,18,139) — b−r +111, the most saturated of the three blue lines; controls +85/+97.
   The pptx drew it C00000. Fixed to BLUE. Spec said "step [2] entirely blue" and was
   over-corrected into an actual defect.
2. **Descender class (REFUTED as a fix trigger).** Several text bands read −2.2..−3.1 at the
   bottom edge in every line with a descender: the original's typeface carries deeper
   descender tails than Arial. Unfixable under the font law; inside the banked
   `probe_a7_findings` class bounds.
3. **render_7 Template A, 2 MINOR (REFUTED).** (a) "bullet-1 underline": no bar exists in
   either image — the original's y357..360 fragments are glyph bottoms; a real bar in this
   deck is a 100–190 frame-px continuous run. (b) "rowC bluish vs reddish": the phrase's
   core is (28,18,139), blue family; every blue run is 0000FF in the pptx.
4. **alg crop MINOR "Random Weights (W) underline" (REFUTED).** Three-way: pptx XML audit
   (32 runs, exactly 6 `u="sng"`, none on rowA); no bar in either image's rowA underline
   band; the cited crop region contains no horizontal stroke (widest run 28 crop px).
   Three successive vision reads contradicted each other (bar exists / render adds it /
   render's bar stops early) against pixel evidence showing no bar in either image.
5. **"approximatly" (CONFIRMED, fixed attempt 8).** Original's underlined word ink
   x177..277 = 101 frame px with a NO-ink gap at x278..281 (checked at a loose threshold
   too). Controlled two-spelling render through the same 17.5pt/Arial/x/charSpacing pipeline
   (`scratch/tmp/lo_boldtest/test_n3_026.js` → `sp-1.png`): "approximately" = 110 px with
   FOUR tail clusters (t, e at 9 px wide with a full-width crossbar, l, y); "approximatly" =
   100 px with THREE (t, l, y). The original's tail has three clusters matching
   "approximatly" shifted +9 px cluster-for-cluster, leaving no room for an 'e' between the
   't' (ends x264) and the 'l' (starts x265). The analysis brief's string is a vision-model
   normalization; fidelity target is the frame.
6. **render_8 Template A, MAJOR box height + 2 MINOR (ALL REFUTED,
   `adjudication_a8_templateA.md`).** (a) "blue box stretched 60–80 px down with extra framed
   white space": box borders measured in BOTH images — ORIG y91..499 (top border y91, bottom
   y498–499, sides x82–83/x862–864) vs render_9 y89..501 (sides 81.6–82.1 / 863.9–864.4);
   first ink inside the box y111 in both, last ink y493 (orig) vs y491 (render — the render's
   content ends 2 px HIGHER); empty band below the last line 4 rows vs 8 rows, not 60–80.
   (b) "title underline": the original's title band y82..90 is pure panel gray (min lum
   696 = E8E8E8, zero red pixels) — glyph ink ends y81; neither image underlines the title.
   (c) "Random Weights (W) underline scope": the render draws no rowA underline at all.
7. **"Least Squares" bold (CONFIRMED, fixed attempt 9, `adjudication_a9_leastsq.md`).**
   Three bias-cancelling discriminators: (i) same-letter stem mass inside the ORIGINAL —
   'L' of "Least" 3 solid cols × 11/13 rows = 33 ink px vs 'L' of "Linear" 22 px (the
   same-letter regular/bold ruler in the render itself is 78 vs 129 px); (ii)
   composition-controlled phrase-window density swept at thr 430/550/650 — original
   LS/REG = 1.46/1.26/1.20 tracking the BOLD class (1.38/1.23/1.20) not the regular class
   (1.01/1.02/1.03 pre-fix); controlled two-weight sim regular 1.04 vs bold 1.32;
   (iii) cross-image class anchor — the original's regular-class spans sit at 0.69–0.79 of
   the render's density while its LS span sat at 0.99 (bold-magnitude outlier). The
   attempt-8 notes-crop judge raised it; the spec's emphasis list is not authority (it also
   normalized "approximatly" and over-read bold on "variable number of steps").

## Change-isolation proofs (banked pixel diffs)

* `probe_a9_verify.out` — render_8 → render_9: 20,190 changed px, bbox frame
  x 109.9..769.1 y 341.6..357.9 = the N1 line only → the alg crop (frame y135..270) and its
  PASS verdict stay valid evidence; only the notes crop needed re-cutting.
* `diff_render7_render8.out` — 16,738 px, all inside frame y440..457 = the N3 band (same
  isolation logic for the attempt-8 cycle).

## Geometry bank (render_9 vs original, identical predicate)

Text bands all inside the ±2.0 px band (left edge −0.3, right edge +0.1 on N1; N3 +0.7;
rowC-red −1.4/−0.7; rowD −1.9; noteshdr ±1.2; title +0.6/−0.9); the remaining "adj" items
are the descender-metric class (see adjudication 2). Underline bars: rowB −2.2/+3.1,
N3a −5.7/−6.0, N3b −4.5/−2.6, rowD −1.1/−2.8 — all inside the banked ±6.6 font-metric noise
band. Blue box containment OK; chrome PASS. Equations: none on this slide (no `eq_*.json`
sidecars, no OMML wrap required).

## In-progress / open items

None. Claim released with `release 026 w26-r3-20261021T0538`; DB final row above.

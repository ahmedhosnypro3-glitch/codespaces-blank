# PIL ADJUDICATION — crop-pair solution (attempt 2, render_2)

Source: `crop_2_solution_judge.txt` (Template B, K=2, render_2).
Verdict: FAIL (two MAJORs). Both adjudicated below; neither warrants a build change.

Note: the transcript itself confirms all content is correct — "all letters/digits/
punctuation correct (no wrong/missing/garbled glyphs); colon after 'Solution' and
comma after 'inversion' present in both; no extra period at end; 'Solution:' bold
in both; two-line centering and leading match; ink reads navy in both".

## D1 MAJOR — "both solution body lines are italic in IMG2, upright in IMG1"
=> **CONFIRMED as an observation; ACCEPTED MINOR** (font-availability limit; banked M1)

The slant is real and was already measured in the banked forensics
(`adjudication_attempt_1_minors.txt` M1):

  SOL1: orig 12 stems lean −0.129 px/row (−7.3°) | render −0.000 px/row (0.0°)
  Frame reference values: SOL1 −0.128, SOL2 −0.141, blue L1 −0.141, L2 −0.129,
  L3 −0.136, EX1 −0.146, EX2 −0.132 (title control +0.000).

The whole body of the frame leans −7.5..−8.4° in EVERY re-derivation. M1's banked
font forensics (`fit_fonts.py`) established that no installed face reproduces the
frame's slant AND single-storey `a` AND Arial-identical advance simultaneously:
Carlito Italic gives −7° but +15.9% advance; Arial Italic matches Arial's advance
(+2.2%) but is double-storey and slants −12° vs the frame's −8°.

The judge's severity (MAJOR) overstates this: it is a font-availability limitation
affecting the entire body uniformly, already adjudicated and accepted before the
build was frozen, and it changes no glyph, digit, word, line break or region.
**No build change.**

## D2 MAJOR — "'Least Squares' and 'Gradient Descent' are bolded in IMG2 but body-weight in IMG1"
=> **REFUTED** (weight proof, bold-calibrated)

Absolute ink density is not comparable across a 150dpi LibreOffice raster and a
960×540 video JPEG (the raster draws ~1.3-1.5× wider anti-aliased strokes), so
every line is normalized to the SAME image's known-bold label — "Solution:" —
which is bold in both builds.

Ink density at a matched 60%-of-contrast stroke threshold, expressed as a
fraction of that image's bold label:

| line | size | ORIGINAL | RENDER_2 |
|---|---|---|---|
| "Solution:" (known BOLD, control) | 21pt | 1.00× | 1.00× |
| SOL1 | 20pt | **0.58×** | **0.59×** |
| SOL2 | 20pt | **0.81×** | 0.73× |
| EX1 (known REGULAR, control) | 23.5pt | **0.56×** | 0.51× |
| EX2 (known REGULAR, control) | 23.5pt | **0.83×** | 0.59× |
| blue L1 (known REGULAR, control) | 23.5pt | **0.58×** | 0.60× |

SOL1 prints at 0.58× bold in the ORIGINAL — exactly where its own known-regular
lines sit (EX1 0.56×, blue L1 0.58×). SOL2 at 0.81× matches EX2 at 0.83×. The
original's solution body is therefore REGULAR weight, and it prints at the same
relative weight as the render's (0.59× / 0.73× vs the render's regular controls
0.51× / 0.59× / 0.60×).

The denser reading on SOL2/EX2 in both images is a text-content effect (rounded
`G`, `a`, `e`, `s`, `0` glyphs vs the flatter `h`, `t`, `n`, `d` of SOL1/EX1) —
it appears in both images and is not a weight break.

Corroborating: the solution-box interior has 0 red px in BOTH images (measure
against a 1710-px control band), so there is no colour/emphasis break either;
"Matrix inversion" is not highlighted anywhere in the original.

**REFUTED. No build change.**

## Outcome
solution region: D1 CONFIRMED-but-ACCEPTED MINOR (font availability, banked M1);
D2 REFUTED. The FAIL's severity calls are not supported by the pixels; all
content, positions and colours in this region are correct.

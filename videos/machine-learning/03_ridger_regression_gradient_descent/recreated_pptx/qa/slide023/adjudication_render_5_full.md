# PIL adjudication — slide 023, render_5 vs the judged render_2 + two residual findings

Date: 2026-10-24. Scope: what changed between render_2 (the render every pre-04:54
transcript judged) and render_5 (the render of the current
`recreated_pptx/slide_023_recreated.pptx`, 01:27:44), and whether the residual
findings raised on render_5 are real.

## 1. Provenance — which render each transcript actually judged

`render_5.png` was re-rendered from the CURRENT pptx at 04:20 and compared byte-for-byte
against the banked render_5.png (01:28): **0 changed px**. render_5 therefore IS the
current build, and LibreOffice rendering is deterministic in this environment.

Absolute template-match (exhaustive, full-res, control = 0 against its own source render):

| transcript | images judged | vs render_5 | verdict |
|---|---|---|---|
| `judge_attempt_4.txt` (full-slide, 00:43) | `render_2.png` | differs | **stale** |
| `crop_2_blue_body_judge.txt` | `crop_2_blue_body_render.png` | **PIXEL-IDENTICAL** (d=0) | valid |
| `crop_2_eq_zoom_judge.txt` | `crop_2_eq_zoom_render.png` | **PIXEL-IDENTICAL** (d=0) | valid |
| `crop_2_recall_eq_judge.txt` | `crop_2_recall_eq_render.png` | differs (818 px) | **stale** |
| `crop_2_solution_judge.txt` | `crop_2_solution_render.png` | differs (14,635 px) | **stale** |

Full-frame render_2 vs render_5 diff (15,370 px >12), contained to:
- `SOL1` frame x245..710 y478..496 → 8,307 px (the intended italic fix)
- `SOL2` frame frame x313..648 y506..521 → 5,644 px (the intended italic fix)
- recall label x102..177 y117..142 → 710 px (AA only, see §2)
- title, equation, blue box, EX lines: **0 px**

The build change was italic-only on the two solution lines (`slide_023.js` lines 254-262).
The italic fix is precisely why the solution-crop leg had to be re-run.

## 2. recall_eq region drift — PIL-refuted (AA only, no content change)

818 px differ in the recall_eq crop region, but:

- Ink bbox **identical at every threshold** tested (100/128/160/200/230), e.g. thr=128:
  render_2 ink 29,743 px vs render_5 29,735 px, bbox both `(0,1360,0,258)`.
- Of 652 px differing by >12: **581 are core ink pixels, 71 are AA fringe adjacent to ink,
  and 0 are isolated** background pixels. Nothing appears or disappears in open space.
- Glyph shapes, positions, and the 'Recall' wordform are unchanged; the caption
  ("Solution:"-style label), the equation image, the dimension note and the red arrow are
  byte-identical.

Cause: the pptx was regenerated end-to-end, and LibreOffice re-rasterised the recall
label's glyph edges with sub-pixel AA differences. Re-rendering the CURRENT pptx twice
gives 0 px difference, so this is a one-off serialisation artefact, not instability.

**Conclusion: no content, geometry, colour or structure change in the recall_eq region.**
The attempt-2 PASS certificate stands for content. Because the region is not strictly
pixel-identical the protocol required a re-judge; that leg was dispatched at 05:20 and
**exhausted both its attempts** (original + W4 hard-wall retry) with `EXIT=124` and no
transcript — the gateway was saturated (24-30 concurrent `analyze_image.py` processes
fleet-wide) and both calls died on the 630 s internal HangError wall. Per protocol no
further vision retry is lawful, so this PIL adjudication is the standing evidence for
the region.

## 3. Full-slide attempt-6 MINOR #1 (bottom-region vertical placement) — PIL-refuted

The judge claimed the Solution block "sits slightly higher ... leaving a visibly larger
bottom gray margin (≈40-50 px in the recreation vs the box nearly meeting the bottom
rule in the original)", raised at MINOR / LOW confidence with the judge's own caveat
that the bottom margin is hard to measure by eye across two scalings.

Measured solution-box border-centre positions (brown 6B562E stroke hunt, x 96..864
frame to exclude the badge):

| edge | original frame (960x540) | render_5 (frame-equiv) | delta |
|---|---|---|---|
| top border    | y 435.0..436.0 (≈435.5) | y 434.88..435.36 (≈435.1) | 0.4 px |
| bottom border | y 530.0..531.0 (≈530.5)  | y 529.44..529.92 (≈529.7) | 0.8 px |

Panel bottom red stroke: original y538.5, render_5 y538.6 — 0.1 px. So the measured
box-bottom-to-stroke gap is 8.0 px in the original and 8.9 px in the render: **a 0.9 px
difference, not 40-50 px.** The box is placed sub-pixel-accurately per the measured
geometry law (`slide_023.js` BOXES[2] = y435.5 h94.5).

**Conclusion: refuted. The recreation's bottom margin matches the original within 1 px.**

## 4. Standing verdicts on the current render

| leg | transcript | verdict |
|---|---|---|
| full-slide (Template A) | `judge_attempt_6.txt` (05:19) | **PASS** |
| crop eq_zoom | `crop_2_eq_zoom_judge.txt` (pixel-identical region) | **PASS** |
| crop blue_body | `crop_2_blue_body_judge.txt` (pixel-identical region) | **PASS** |
| crop recall_eq | `crop_2_recall_eq_judge.txt` + this adjudication | **PASS** (adjudicated) |
| crop solution | `crop_3_solution_judge.txt` (04:54, render_5) | **PASS** |

House chrome on render_5: `house_chrome_check.py` → PASS (panel x112-1882, strokes
L/R/bottom present, top bare, badge center (1824,152) d=68, all within tol 8).

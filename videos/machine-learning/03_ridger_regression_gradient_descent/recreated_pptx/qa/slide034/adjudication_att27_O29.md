# Slide 034 — attempt-27 adjudication record (scope O29_034)

Deck: `videos/machine-learning/03_ridger_regression_gradient_descent`
Judge round: attempt 27 (`judge_27_final.sh`), full-slide Template A + 3 crop-pair
Template B legs on `render_27.png`.
Payloads byte-for-byte from `shared_patterns/judge_protocol_03.md`
(`payload_A_27.txt` == `judge_prompt_6.txt`, `payload_B_27.txt` == crop template B).

## 1. CRITICAL FINDING — the shipped deck did NOT serve the judged pixels

`judging.md` ("Identify the certified render by MEASUREMENT, not attempt numbering")
requires a 0-px diff between the judged render and a fresh render of the shipped
deliverable.

Measurement (`qa/slide034/render_27_cert.png` = fresh 150dpi render of
`slide_034_recreated.pptx`):

| pair | diff px (>0) | diff px (>8) | diff bbox (frame px) |
|---|---|---|---|
| render_27 vs render_27_cert | 87 273 | 52 616 | x 608..844, y 58..312 |

Two independent renders of the same deck are **byte-identical** (0/2 251 125 px), so
LibreOffice is deterministic and the gap was a real content difference, not render noise.
The diff bbox is exactly the plot region (`make_crops_27.py` REGION "plot" =
599..853 x 50..321). The table region diffs to 0, so the x-row c16/c18 = 9.6 fix was
present in both.

Root cause (mtime chain): `qa/slide034/regenerate_plot_034.py` (20:47:44) overwrote
`build/assets/slide_034_plot.png` (20:47:54) with a hand-traced redraw that used
crude, self-declared axes (`x_axis_fy=112`, `y_axis_fx=116`, scale 7.91 px/unit)
instead of the frame-fitted mapping (`X0=721.825, SX=8.9296, Y0=172.336,
SY=8.8443`, residual median 0.912 px) used by `qa/slide034/gen_plot_27.py`.
`slide_034_recreated.pptx` was rebuilt at 20:48:01 against that distorted asset,
while the judged `render_27.png` (20:47:56) predates the rebuild. The judge legs
graded the good plot; the deck was shipping the bad one.

PIL proof that the judged plot is the faithful one (teal curve vs the original frame's
traced curve, frame coordinates, per-column median centerline):

| plot | orig→render mean | median | p90 | original curve covered (<3 px) |
|---|---|---|---|---|
| render_27 (judged) | 0.46 px | 0.25 px | 1.09 px | **99.5 %** |
| shipped asset (regen) | 4.38 px | 4.09 px | 8.30 px | 35.7 % |

Fix applied: regenerated the asset with the frame-fitted generator
`qa/slide034/gen_plot_27.py` (1975x2116 px @600 dpi, the size the build expects),
rebuilt `build/slide_034.js` -> `slide_034_recreated.pptx`, re-rendered.
The distorted asset is banked, not deleted, as
`qa/slide034/BANKED_asset_regen034_2116.png`.

**0-px proof after the fix:** `render_28.png` (fresh render of the rebuilt deliverable)
vs `render_27.png` (the judged render) = **0 differing pixels of 2 251 125**.
The deck now serves the certified pixels exactly.

Deck gates re-run on `render_28.png`:
- `shared_patterns/house_chrome_check.py` -> **PASS** (panel x112..1883 y94..bottom,
  strokes L/R/bottom only, top bare, badge centre (1825,152) d69)
- `qa/slide034/selfcheck_attempt_27.py` -> **SELFCHECK: PASS** (8 region ink-bboxes,
  worst 6.8 px on the equation, inside its certified allowance; 7/7 dataset
  invariants; 8 table rows x 18 data cols parsed)

## 2. Adjudication of every judge finding (PIL-first, per `judging.md`)

Full-slide leg (`judge_attempt_27.txt`, **FINAL VERDICT: PASS**) — no BLOCKER/MAJOR.
Two MINORs, both non-triggers:
- table rows proportionally taller / fonts slightly larger -> 150dpi-render scale
  artifact; layout ratios preserved. Not a fix trigger.
- chart y-axis label spacing marginally wider -> all tick values and positions
  correspond; within tolerance. Not a fix trigger.

Table crop leg (`crop_27_table_judge.txt`, **FINAL VERDICT: PASS**) — all 152 data
cells verified identical; 4 MINORs:
1. **Highlight fill hue "green vs teal/aqua" — REFUTED.** Modal fill measured in the
   crop pair: render `(139,248,171)` (15 775 px) vs original `(139,247,171)` /
   `(139,248,169)` / `(139,247,172)` / `(136,249,171)`. Same hue and value (dE ~1-2);
   the "teal/aqua" reading is JPEG-softening of the original's own fill.
2. Dashed outline square vs rounded corners -> cosmetic corner geometry; the
   original's rounded dashed rectangle is professor hand-markup on the source frame
   (ground rule d). No geometry change warranted.
3. Border colour of the two yellow `3.2` slope cells -> the judge itself records it as
   "not resolvable definitively through the JPEG softening" (low-medium confidence).
4. Red arrow slightly smaller / higher -> scale and position only; same symbol, same
   target (the x = 7 column).

Plot crop leg (`crop_27_plot_judge.txt`, **FINAL VERDICT: PASS**) — axes, ticks,
annotations and label verified glyph-by-glyph; 2 MINORs:
1. **Hump amplitude "IMG1 ~5.3 vs IMG2 ~4.9" — magnitude REFUTED.** Measured on the
   original frame's traced curve vs the render's curve (184 common columns):
   overall |dy| median 1.02 px (0.12 y-units), mean 1.88 px (0.21 y-units);
   left-hump band x628..700 mean 2.21 px (0.25 y-units); hump **peak** y differs by
   2.00 px = **0.23 y-units** against the claimed ~0.4. Sub-tolerance amplitude
   difference, not a fix trigger.
2. Pencil/cursor artifact at the right edge of IMG2 -> video-capture artifact,
   correctly omitted (ground rule c). Not a discrepancy.

## 3. Verdict

Attempt 27 = **PASS**. No build change was required by any judge finding; the only
build change in this scope was restoring the correct plot asset so the deck serves
the pixels that were judged (0-px diff proof above).

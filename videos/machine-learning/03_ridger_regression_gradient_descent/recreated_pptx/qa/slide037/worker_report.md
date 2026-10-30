# Worker report — slide 037 "Problem Formulation" (attempt 6, worker w037)

Deck: `videos/machine-learning/03_ridger_regression_gradient_descent`
Run: pooled deck-03 completion mission, run 859463. Worker: `w037`.
Deliverable: `recreated_pptx/slide_037_recreated.pptx` (single plain-named version).
Resumed from: worker `worker_slide037_b` (report preserved as
`worker_report_worker_slide037_b.md`); renders 1–5, judges 1–4 and crops 2/4 kept untouched.

## Outcome

| Item | Value |
|---|---|
| Template A (full-slide) | **PASS** — `judge_attempt_6.txt` (judged render_6, md5 7251b2caec4d74e5ff199aa98a814fe8) |
| Procedure B crop 1 `def_lines` | **PASS** — `crop_6_def_lines_judge.txt` |
| Procedure B crop 2 `eq_stack` | **PASS** — `crop_6_eq_stack_judge.txt` |
| Procedure B crop 3 `update_eqs` | **PASS** — `crop_6_update_eqs_judge.txt` |
| Procedure B crop 4 `green_box` | **PASS** — `crop_6_green_box_judge.txt` |
| House chrome | `shared_patterns/house_chrome_check.py render_6.png 37` → **PASS** (`house_chrome_check_attempt_6.txt`) |
| Selfcheck | `selfcheck_attempt_6.py` / `.txt` → **PASS** (all 7 items, numbers printed) |
| DB | `gen_status=passed`, `visual_check=PASS`, `visual_attempts=6`, `visual_transcript=.../judge_attempt_6.txt`, `last_error=` cleared |

## Attempt history (this slide's full record)

| # | Render | What changed | Judge result |
|---|---|---|---|
| 1 | render_1 | first build | not judged (killed mid-flight) |
| 2 | render_2 | panel/geometry rework | not judged |
| 3 | render_3 | measured panels, Sigma placements | not judged (gateway saturated) |
| 4 | render_4 | font calibration | PASS(4) — but STALE: render_5/6 superseded it |
| — | render_5 | partial colour patch (unjudged) | — |
| 6 | **render_6** | full frame-measured rebuild (below) | **PASS(6)** + 4/4 crops PASS |

## Why attempt 4 was not reusable

`judge_attempt_4.txt` PASSed `render_4`; `render_5` (unjudged, stale colour regression) and
this run's `render_6` superseded it. `crop_4_eq_stack_judge.txt` was FAIL with 7 findings;
all seven were PIL-adjudicated against the original frame in
`crop_4_eq_stack_adjudication.txt`: 5 real (fixed), 1 refuted with measurements (the
"positive"/"negative" red+underline claim — the frame's ink there is black, no underline),
1 medium-difference. Adjudication also found defects the earlier judges missed and that were
fixed in the rebuild:

1. **`∂Error/∂W` was LINEAR text** in both update equations. The frame shows stacked 2-D
   fractions (bar rows 424–426, x 267–336 and 511–580). Rebuilt with matplotlib mathtext at
   600 dpi (`assets/eq_037_frac.png`) placed at the frame's exact ink box.
2. **Sigma limits were mono-red and oversized.** Rebuilt as Sigma glyph PNG
   (`assets/eq_037_sigma.png`) + coloured limit text runs at the measured positions:
   L1 x150–272 y290–303, L2 x610–716 y441–453, L3 x261–425 y503–518.
3. **Box-1 colour scheme was wrong** (frame: class I RED / class II BLUE, line 2 swapped;
   misclassified BLACK bold italic underlined; `<0`/`>0` RED; `⇒` BLACK; `d` of `d(X)`
   GREEN; `δ_i` GREEN with RED subscript). Rebuilt to the measured colours.
4. **Box-2 heading is BLACK bold underlined** (zero saturated-red ink in its frame band),
   not dark red; fixed.
5. **"Summation is always positive"** — "positive" is red bold italic UNDERLINED; fixed.
6. **η** is red bold italic in both update equations; fixed.
7. **Title centre** is x491 (frame ink 353–629), not the slide centre 480; fixed.

## Equations (fidelity law compliance)

| asset | role | placed (frame ink box, render_6 measured) |
|---|---|---|
| `assets/eq_037_sigma.png` | black Sigma glyph (mathtext, 600 dpi) | 202.0–221.6 × 261.9–287.9; 650.6–677.9 × 408.8–441.9; 330.6–355.0 × 471.6–501.8 |
| `assets/eq_037_frac.png` | stacked ∂Error/∂W fraction | 266.7–336.3 × 403.0–449.1; 510.5–582.0 × 403.0–449.1 |
| limit lines | pptx text runs, two-colour, centred under each Sigma | L1 152.6–269.1 × 293.1–302.7; L2 609.3–715.3 × 439.9–455.3; L3 245.2–444.7 × 501.8–519.6 |

All images are placed at exact px/600 size (never rescaled) from sidecars
`eq_037_sigma.json` / `eq_037_frac.json`. The previous worker's assets
(`eq_037_sum_*.png`) are kept untouched.

## Frame-vs-render measurements (render_6, 150 dpi, GM 2.0833)

Banked in `selfcheck_attempt_6.txt`: frame containment margins all positive (P1
9.2/4.7/43.9/21.0, P2 10.8/13.3/11.1/14.3, P3 13.2/14.2/126.7/10.9, green box
2.0/1.9/2.4/2.3), five equation regions inked (895/3496/3496/1566/1267 px), delimiter span
test true, every text line inside its band, crop-pair scale equal.

## Remaining MINORs (documented, not fixable without a different typeface)

- Liberation Serif advances: box-1 lines 20 px (2.4 %) narrower, explanation 11 px (2.5 %)
  wider than the frame; no wrap/overflow.
- LO renders baseline-shifted runs at 58 %: "(updated)"/"old" and the `i` subscripts are
  smaller than the frame's hand-typeset math (positions correct).
- mathtext Sigma/∂ glyphs are lighter than the frame's bold serif glyphs (sizes match).
- The frame's pen/arrow annotation inside the green box is a capture artifact (rule (c)).

## Banked evidence (never deleted)

Renders 1–6, judges 1/4/6, crop_2_*, crop_4_*, new crop_6_* pairs + transcripts,
`crop_4_eq_stack_adjudication.txt`, `selfcheck_attempt_{1,2,3,6}`, `build_attempt_{2,4,6}.js`,
`house_chrome_check_attempt_6.txt`, `measure_*.py`, both worker reports, prompt templates.

## Resume point

Certified. No follow-up required. If anything changes, new attempt = 7 and BOTH legs must be
re-run from the new render.

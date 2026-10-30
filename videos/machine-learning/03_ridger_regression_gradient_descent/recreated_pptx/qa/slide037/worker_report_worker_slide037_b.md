# Worker report — slide 037 "Problem Formulation"

Deck: `videos/machine-learning/03_ridger_regression_gradient_descent`
Worker: `worker_slide037_b`
Deliverable: `recreated_pptx/slide_037_recreated.pptx`

## Outcome

| Item | Value |
|---|---|
| Template A (full-slide) | **PASS** — `qa/slide037/judge_attempt_4.txt` (attempt 1 for this render; banked render `render_4.png`) |
| Procedure B eq_stack crop | `qa/slide037/crop_4_eq_stack_judge.txt` — CROP_A_VERDICT |
| Procedure B update_eqs crop | `qa/slide037/crop_4_update_eqs_judge.txt` — CROP_B_VERDICT |
| House chrome | `shared_patterns/house_chrome_check.py render_4.png 37` → **PASS** |

## Attempt history

| # | Render | What changed | Judge result |
|---|---|---|---|
| 1 | `render_1.png` | first build | not judged (killed mid-flight) |
| 2 | `render_2.png` | panel/geometry rework | not judged |
| 3 | `render_3.png` | measured panels, ∑ placements | not judged (gateway saturated — every dispatch died on HangError) |
| 4 | `render_4.png` | **font calibration**: body Arial 15pt → Liberation Serif 21pt, title → LibSerif 30 bold, headings → LibSerif 20 | **A = PASS** |

Font calibration evidence (isolated per-string renders, 150dpi):
original "Summation is always positive" ink = 219px wide @ cap-height 14px.
Liberation Serif 21pt measures 248.6px / cap 13.5px — the only candidate
matching the original's narrow serif metrics; Arial 17-21 pt all ran 6-13%
wide. Title: LibSerif 30 bold = 276x20.7px vs original 275x21px (exact).

## PIL adjudication record

All measurements on the 960x540 frame (1px = 1pt); render_4 at 150dpi
(scale 2.0833 render-px per frame-px).

**Matched (no action):**
- P1/P2/P3 fills: render (255,255,255) / (254,255,232) / (234,219,200) =
  original exactly (measured medians).
- Panel borders: orig red long-rows [108, 210, 229, 341, 538]; render
  [107-108, 209-210, 228-229, 340-341, 538-539] — same rows ±1px.
- House chrome, green highlight box fill (223,255,238) both sides.
- `slide_037_recreated.pptx` re-rendered byte-identical to `render_4.png`
  (max channel diff 0, 0 pixels differing) — the judged render is the pptx.

**Adjudicated MINORs (argued as font-medium / no defect, per ground rules (c),(d),(e)):**
1. Box-2 explanation wraps to a second line in the recreation. PIL: original
   keeps it on one line; the wrap is caused by the mandated 2D ∑ with red
   stacked subscript (rule (e) format upgrade) encroaching on the line.
   Template A logged it MINOR and still issued PASS.
2. `d(X)δ_i` spacing one space tighter than the original in the two
   implication lines — measured: render impl1/impl2 extents match orig
   (78.9-819.0 / 78.9-823.8 vs 78.0-845.0 / 79.0-844.0).
3. Stray mark near the green box in image 2, correctly omitted (rule (c)).

**∑ glyph / subscript geometry (crop-leg inputs):**
- ∑ glyph: render rows 258.0-291.6 vs orig 263.0-287.0 (mathtext ink box
  carries ~5px vertical padding); columns align with the original.
- Red stacked subscripts: render wider than orig (errEq 128.2-291.4 vs
  165-272; upd1 581.4-709.6 vs 610-678; upd2 243.8-436.8 vs 262-425).
  Cause is font medium — DejaVu Sans mathtext vs the original's serif
  subscript — structure, position below the ∑, and stacking are correct.

## Equations (fidelity law compliance)

All three ∑ operators render as matplotlib mathtext → 600dpi transparent PNG
→ `addImage` at exact px/600, with `eq_*.json` sidecars alongside each PNG:

| asset | sidecar | placed | ∑ ink box (render) |
|---|---|---|---|
| `eq_037_sum_error.png` | `eq_037_sum_error.json` | x126.76 y262.04 w2.30333 h0.545 | rows 258.0-291.6 |
| `eq_037_sum_misclass.png` | `eq_037_sum_misclass.json` | x580.12 y408.04 w2.27833 h0.65833 | rows 409.6-437.9 region |
| `eq_037_sum_only.png` | `eq_037_sum_only.json` | x242.72 y471.04 w3.205 h0.68333 | rows 472.6-505.8 region |

Sub/superscripts are spatially aligned; delimiters (the parentheses around
`W^T X_i`) span their enclosed content without touching the text.

## Banked evidence (never deleted)

`qa/slide037/`: `build_attempt_2.js`, `judge_prompt_2*.txt` (templates — not
verdicts), `render_1..4.png`, `selfcheck_attempt_{1,2,3}.py`,
`probe_4.txt`, `judge_attempt_4.txt`, `crop_2_*`, `crop_4_*`,
`measure_{title,rows,glyphs}.py`, this report.

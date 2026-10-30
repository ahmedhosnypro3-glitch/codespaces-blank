# PIL adjudication — att13 legA findings (render_12, 2001×1125, S=2.0844)

Judge: `judge_attempt_13.txt` (FAIL, 4 MAJOR / 5 MINOR). Every finding measured PIL-first.
Settled law from legA12 (`pil_adjudication_legA12.md`) is applied, not relitigated.

## 1. C-label collision (MAJOR) — CONFIRMED → FIX (build misapplied legA12 fix 1)

Orig profile (measured, 048+049 identical): y80-88 digits (1,2,1,5,6,6); y96-104
digits (1,1,2,4,5,6); y113-124 class tags (row3 census red=38, blue=25). render_12
has tags at row2 y97 (red 408 / blue 424) inside the paren span y77..107, row3
EMPTY — collision confirmed (judge right; the tags were also moved by the prior
carrier while applying legA12 fix 1, which never asked for that).

FIX (implemented in build): restore digit row2 (1,1,2,4,5,6) black y97 h10; move
class tags to y113 h12 (bold+italic RED/INK kept — that part of legA12 fix 1 was
correct). render_13 census: row2 dark ink in all 6 cols (152-209/col), tags y113
red=544/blue=486 render-px, row1 unchanged.

## 2. Initial-W order / "=" missing (MAJOR) — REFUTED

Both origs pixel-identical top-centre: vector x330..353 LEFT of label x366..422;
NO '=' ink anywhere (x354..365 and x423..425 empty); black runs (330,331),(336,353),
(366,422),(542+) and red runs (426,486),(497,504),(512,517),(526,529) identical on
048+049. Same as legA12 settled #3. Judge inverted the reading order.

## 3. Triplet per-digit colors rows 1-3 (MAJOR) — REFUTED

Per-digit census of orig: rows 1-3 red counts 6-13px UNIFORM across digits (row2
9/9/6, row3 10/7/13 — no positional pattern); rows 4-6 blue 11-21 uniform, zero
red. Row-block coloring (RED rows 1-3 / INK rows 4-6) is the settled legA12 law.
Judge's claimed render pattern "row1 black-black-red" is also false (render row1
avg (243,30,30) = red block).

## 4. Bottom containment (MAJOR) — REFUTED

Orig: last box bottom y528, red stroke y538.5 → 10.5px gray gap. render_12 col
orig-x500: box border oy527, GRAY oy528..536 (~9px), RED oy537..538. Same visible
margin (1.5px delta at 960 scale). Judge's "no visible margin" is false.

## 5. d(x₂) row-1 label (MINOR) — REFUTED

legA12 calc #1-2 settled: subscript zones structurally identical; row1 label is
d(x₁). No action.

## 6. REPEAT underline (MINOR) — REFUTED

legA12 top-band #6 settled: "using Step" descender clusters, no underline band
(048 census: red-zone rows 69-77 counts [18,22,3,2,5,1,0,0,0] vs label underline
band 57/56). No action.

## 7. Iteration-2 oversized (MINOR) — REFUTED

render_12: red-box bbox orig-space x83.5..213.0 y277.3..303.7 — EXACT match to
orig rows 278..304 cols 84..213. White-text bbox orig-space x99.3..196.7 (98px
wide) y284.0..298.4 vs orig text x99..199 (100px) y284..298. Judge's "~40-50%
larger" is false; geometry matches to ~2px.

## 8. Inter-row gap color (MINOR) — CONFIRMED, no action

Orig gap bands y193-201/268-276/326-334/392-408/457-465 mean ~(230,233,236) gray
vs render white-filled contiguous boxes. Banked as adjudicated MINOR per legA12
"no action" precedents (judge-visible but sub-threshold; box geometry itself is
correct).

## 9. Legend subscripts detached (MINOR) — CONFIRMED → FIX

`subscript:true` runs hang below the baseline. Switched to the certified 044/045/
047 idiom: plain unicode glyphs in normal runs ("C\u2081" single runs; legA12
fix-list wording "unicode ₁₂"). Applied to legend runs + aug tags. Top-table tags
were already plain unicode; d(xᵢ) subscript runs untouched (passed judges).

## att14 fix list (only 1 and 9)

1. Top table: digit row2 restored y97 h10; class tags moved y113 h12.  [done]
2. Legend + aug tags: subscript:true → plain unicode ₁₂ glyphs.        [done]

No other changes — 2/3/4/5/6/7 refuted on measurement, 8 banked MINOR.

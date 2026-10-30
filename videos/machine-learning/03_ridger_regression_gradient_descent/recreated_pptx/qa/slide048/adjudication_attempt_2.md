# Slide 048 — PIL adjudication record (attempt 2)

Every judge finding below was adjudicated by measuring BOTH images
(original `unique_slides/slide_048.jpg` at 960x540, 1 frame px = 1 pt; and
`recreated_pptx/qa/slide048/render_2.png` at 150 dpi, scale
H_render/540 = 2.083333 render-px per frame-px) BEFORE any build change.

Source leg: `qa/slide048/judge_attempt_2.txt` —
`FINAL VERDICT: FAIL` (pooled, on the pre-note render).

---

## MAJOR 1 — "Check classes row 1, Z3 column: original prints 6, recreation prints 3"

**Verdict: REFUTED — the original prints 3.**

The judge compared against its own reading of a 960x540 JPEG. Measured glyph
shape at the disputed cell (original, cols 688..699, rows 89..98):

```
.........#
...####...
..######..
......##..
.....##...
....###...
.....###..
......##..
..##..##..
..#####...
```

Top curve -> horizontal bar -> a **right-side waist** -> bottom curve. There is
no closed loop.

Calibration from the SAME frame, the input table's row-1 column-5, which both
the analysis spec and the recreation agree is a `6` (original, cols 179..193,
rows 79..90):

```
....####..
...##..#..
...##.....
..###.#...
.######...
.###.###..
..##..##..
..##.###..
...####..
....##....
```

A `6` here is unmistakably different: a closed bottom loop with left AND right
strokes on FOUR consecutive rows (`###.###`, `##..##`, `##.###`, `####`).

Cross-check on the check-classes table itself — row 2, column 2 (spec: `6`),
original cols 663..679 rows 105..115:

```
.###....
#####...
##......
##......
#####...
##.###..
##..##..
##..##..
######..
.####...
```

Again a closed multi-row loop — a genuine `6`. So the original's own glyphs
distinguish cleanly: `6` = closed loop, and the disputed cell is NOT a `6`.

The recreation's same cell (render_2.png, cols 688..699) also reads `3` — top
curve, right waist, bottom curve — so recreation and original AGREE.

Consistency check: the analysis spec's own equation set requires the Z values
`(0 7 3)` and `(0 6 2)` (they are the perceptron's `d(x_i)` sums for the three
initial test vectors), and the self-check verifies the table contents read back
out of the pptx XML itself.

**Conclusion: no defect. Judge misread a 3 as a 6 at full-slide scale.**

---

## MAJOR 2 — "Initial W = (−2,−2,−2); d(x₁) = −2; Update-Weight logic inverted"

**Verdict: REFUTED — the original prints (4, −2, −2) and d(x₁) = 0.**

Measured entry 1 of the stacked Initial-W column vector (original,
cols 336..350, rows 62..70):

```
......##......
......##......
.....###......
....####......
....#.##......
...##.##......
..#######.....
...######.....
......##......
```

This is a `4` and nothing else: two strokes converging to a point at the top, a
diagonal running down-left, a full horizontal bar at the base, then a short
vertical stem beneath it.

Entries 2 and 3 carry a leading minus sign (a short horizontal bar at
cols ~337..342) followed by a `2` — i.e. `-2` and `-2`.

So the original's Initial W = (4, -2, -2) — identical to the recreation.

Arithmetic closure (from the spec's own equation list, and reproduced in the
calc panel):

- d(x₁) = [1 1 1] . (4 -2 -2) = 4 - 2 - 2 = **0**  (matches row 1)
- W <- (4 -2 -2) + 1*(1 1 1) = **5 -1 -1**           (matches row 1)
- d(x₂) = [1 2 1] . (5 -1 -1) = 5 - 2 - 1 = **2**   (matches row 2)
- d(x₃) = [1 1 2] . (5 -1 -1) = 5 - 1 - 2 = **2**   (matches row 3)
- d(x₄) = [1 5 4] . (5 -1 -1) = 5 - 5 - 4 = **-4**  (matches row 4)
- d(x₅) = [1 6 5] . (5 -1 -1) = 5 - 6 - 5 = **-6**  (matches row 5)
- d(x₆) = [1 6 6] . (5 -1 -1) = 5 - 6 - 6 = **-7**  (matches row 6)

Every value the judge itself confirmed as matching ("d(x₂)…d(x₆) = −2,−2,−4,
−6,−7; all resulting W = ⟨5,−1,−1⟩") follows arithmetically from W = (4,−2,−2).
The judge's alternative, W = (−2,−2,−2), would give d(x₂) = −2−4−2 = −8, not −2
— which contradicts its own verified row-2 value. The judge's reading is
internally inconsistent with the original.

**Conclusion: no defect. Judge misread the initial vector's first entry, and its
claimed d(x₁) = −2 is arithmetic-incompatible with the frame it verified.**

---

## MINOR 3 — omitted "C1 positive, C2 negative, Zero is unaccepted"

**Verdict: FIXED (the judge was right that it exists; the previous build omitted it).**

Measured in the original: a text line at rows 110..124, cols 239..508, i.e.
under the Initial-W/REPEAT cluster. Ink groups:
cols 239..302, 312..378, 395..422, 430..508.

Colour census over that band: **35 red px** and **238 green px**
(whole-frame green in rows 112..128 is 238 px, all inside cols 395..423).
Green core RGB (69,138,56), mean (153,205,138).

Char-pitch fit fixes the reading unambiguously — the pitch is uniform across all
three dark segments:

- cols 239..378 = 140 px / 26 chars ("C1 positive, C2 negative,") = 5.38 px/char
- cols 395..423 =  29 px /  5 chars ("Zero")                    = 5.80 px/char
- cols 430..508 =  78 px / 14 chars ("is unaccepted")           = 5.57 px/char

and the red px fall in the two `C1` tokens. So "Zero" is **GREEN** in the frame,
not red as the analysis spec claims.

The note is now drawn (`CLASSES-OF NOTE` block) with `C1`/`C2` red, "Zero"
green #458A38, rest black, at x=fx(239), measured width 268 px vs the
original's 272 px (start column aligned at 239).

"Check classes of" (the caption) remains correctly absent: the check-classes box
interior rows 58..70 is pure white in the original.

---

## MINOR 4 — green back-arrow after the Update step

**Verdict: REFUTED as an arrow — it is the word "Zero" from MINOR 3.**

The only dense green ink on the whole slide outside rows 110..124 is scattered
chroma noise: 583 green px spread over rows 153..518 / cols 379..764
(~0.2 px per column), with no closed shape. The one solid green form is the
395..423 / rows 110..121 blob that MINOR 3 identifies as the word "Zero", now
drawn. There is no separate green arrow glyph anywhere in the frame.

---

## MINOR 5 — "Initial W" merged into the red heading

**Verdict: FIXED.**

Measured on the previous render: the black "Initial W =" label rendered at
rows 79..88 while the original has it at rows 61..72 — i.e. 18 frame-px too
low — and the red "REPEAT using Step η = 1" wrapped to two lines (25 rows tall
vs the original's 12), because its box was 1 frame-px narrower than the string.

Cause: `valign:"baseline"` parks the first line's baseline at the box top in
this text, so a single line renders far below the measured band. Both blocks now
use `valign:"middle"` on a box placed on the measured band, and the REPEAT box
was widened to fw(150) at fontSize 12.

After the fix (render_2.png):

- "Initial W =": rows 61..71, cols 366..422 (original rows 61..72, cols 366..421)
- "REPEAT using Step η = 1": rows 63..74, cols 426..531
  (original rows 61..74 caps 62..73, cols 426..530)

---

## MINOR 6 — column-vector delimiter shape

**Verdict: PARTIALLY CONFIRMED, rule-(e) exempt — recorded, not changed.**

The original's delimiters are essentially straight vertical strokes: per-row
centroid x spans only 1.5 px over rows 149..194 for the row-1 W vector, and
the stroke is a single continuous column (col 643, rows 155..189) with no
horizontal serif at the top (top row 155 shows ink only at col 643). A
parenthesis would bulge 8-15 px horizontally. So the original is NOT round
parens — the judge's premise is wrong on that point.

The recreation draws square brackets, which do span all enclosed lines and do
not overlap the numerals (rule 7 (i)/(ii) pass, verified by the self-check's
bracket-geometry count: 6 tall strokes for row 1's three vectors, 2 for row 6's
one vector, 2 for Initial W). The remaining difference is stroke style only,
which the protocol's rule (e) exempts for the mandated 2D equation format.

---

## MINOR 7 — "Iteration 1" fill and "Augmented Vectors" ink style

**Verdict: CONFIRMED from the frame — no change.**

- "Iteration 1": box median RGB (204,68,83) with 231 near-white glyph px vs 687
  red px — a solid red fill with white text is what the frame shows, inverting
  the spec's "white-filled with red border". The recreation reproduces the
  frame.
- "Ugmented Vectors (from Top)": the header ink's core in the original measures
  dark ink in the black family, not the red the spec asserts, so typed black is
  the faithful choice.

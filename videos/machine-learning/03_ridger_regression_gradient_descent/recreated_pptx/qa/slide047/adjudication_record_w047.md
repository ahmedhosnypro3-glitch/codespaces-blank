# Slide 047 — PIL adjudication of prior FAIL claims (worker w047-root-20261024, attempt 6)

Every defect claimed by prior lanes' FAIL verdicts was re-measured against the ORIGINAL
(`unique_slides/slide_047.jpg`, 960×540, 1px=1pt) BEFORE any build change. Method: ink
masking (luminance thresholding), column/row ink profiles, cluster splitting, core-colour
sampling (median of the darkest 10–12% pixels per glyph band), and 1:1 / 4× LANCZOS ASCII
bitmaps. Scripts + full output banked as `adjudicate_w047*.py` / `adjudicate_w047*.txt`.

## Claim-by-claim rulings

| # | Prior FAIL claim (verdict) | PIL measurement on the original | Ruling |
|---|---|---|---|
| 1 | Augmented table has DUPLICATED rows; original has 3 rows (judge_1, judge_2) | Data band splits to header y165..175 (h11) + one block y179..226 (h48); calibration: top-left matrix's 2 digit rows = h31 ⇒ ~15.5 px/row ⇒ 48 px = exactly 3 rows. Parens span y179..226 (the 3-row block only). | **CONFIRMED** — original has 3 data rows. Current build draws 3. The 4-row/5-row readings (MEASUREMENT_NOTES, render_1/2) were wrong. |
| 2 | Class rows wrong: original C₁C₁C₁ C₂C₂C₂ (judge_1, judge_2) | Top-left class band clusters: x90..102 RED(178,127,114), x113..124 RED, x134..146 RED, x157..170 BLUE(129,123,159), x179..192 BLUE, x202..214 BLUE. Augmented class band: same 3 red + 3 blue pattern. | **CONFIRMED** — both matrices print C₁C₁C₁ (red) C₂C₂C₂ (blue). Build matches. Old 2+4 readings refuted. |
| 3 | Title renders "Ugmented" — leading A clipped (judge_2) | 1:1 ASCII of y146..162 x78..190: first glyph is "U" (two stems joined at baseline, cols 4..11); cols 0..3 EMPTY — no "A" precedes it. The source slide itself prints the typo "Ugmented". | **REFUTED as a defect** — "Ugmented" is verbatim from the original. Build correct. (Containment of the U verified on the render separately.) |
| 4 | Missing space: render "C₂negative" vs original "C₂ negative" (judge_2) | Legend band ink-run gaps: C₂ ends x326, "negative" starts x329 ⇒ **2 px** (kerning only). All true word gaps in the same line measure 6–8 px (positive→C₂ 8 px; Zero→is 6 px). | **REFUTED** — original prints "C₂negative" with no space. Build correct. |
| 5 | Sign statements should be red/blue (spec) / black (judge sees) | Box1 sign statement core (128,130,127) = BLACK; reference cores: "Class I" (180,60,78) RED, "d(Z₁) =" (150,152,150) black. | **CONFIRMED black bold** — build correct. |
| 6 | Box backgrounds "light blue tint" in original (judge_2) | Calc-box interior medians: box1 L (254,255,253), box1 R (254,255,253), box2 R (254,255,255), box3 R (254,255,253) = white. Border row y139 median (210,215,221) = light gray-blue hairline. | **REFUTED** — original boxes are WHITE with hairline. Build correct. |
| 7 | Headers uppercase X₁..X₆ in blue (judge_2) | Header-band ASCII: small-case italic x glyphs with subscripts (x-height ~6 px + 3 px descender-ish tail). Not uppercase. | **REFUTED** — lowercase italic x₁..x₆ in black. Build correct. |
| 8 | Column vectors use square brackets in original (judge_2) | Stack delimiter ASCII (x380..412, y146..194): LEFT paren x381 y150..189 continuous, RIGHT paren x405 y150..189 continuous — round parentheses spanning all three entries. | **REFUTED** — original uses ROUND parens. Build correct. |
| 9 | Result boxes narrower than original (judge_2) | Original calc boxes span x273..855 (borders measured at both edges); build draws rect x273..855. | **REFUTED** — identical extents. |
| 10 | Top-left class row uniformly blue (judge_1, low conf.) | See #2: 3 red clusters then 3 blue clusters. | **REFUTED**. |
| 11 | Sign statements / aug title wrap to 2 lines in render (judge_2) | Original: sign statement single band y162..171 (one line); aug title single band y147..159 (h13, one line). | **CONFIRMED one line each** — build single-line, selfcheck gap bands ink=0. |
| 12 | Initial W = [4; -2] (spec) vs [4; -2; -2] | Digit column x333..349 splits to y62..71 / y77..87 / y93..102 = THREE entries; left paren x322..332 spans y60..104 (all three). | **CONFIRMED three entries** — build correct. |
| 13 | Z headers may be Z₂/Z₃ | 1:1 ASCII y62..76 x594..660: three identical Z glyphs, each followed by the same vertical-stroke subscript. | **CONFIRMED Z₁ Z₁ Z₁** — build correct. |
| 14 | Calc boxes may read all d(Z₁) | 4× bitmaps: box1 subscript = bare vertical stroke (Z₁); box2 subscript ends in a bottom bar y243 (Z₂); box3 subscript ends in a bottom bar y309 (Z₂). | **CONFIRMED d(Z₁) / d(Z₂) / d(Z₂)** — build correct. |
| 15 | Bracket notation garbled (spec) | See #8 + row-vector core (134,125,194) BLUE, stack cores (113,169,113)/(130,173,124)/(150,183,148) GREEN, result core (138,140,137) black. | **CONFIRMED** blue row vector × green (14;-4;0) stack — build correct. |
| 16 | Box3 prints "= -14"-style wrong value | 6× bitmap of x410..445 y258..278: a minus bar at y263 (x424..431) before the "2". | **CONFIRMED verbatim "= -2"** (source arithmetic slip) — build reproduces it. |
| 17 | Legend colours | C₁ core (151,29,37) RED; C₂ core (47,33,132) BLUE; "Zero" core (70,134,57) GREEN. | **CONFIRMED** — build correct. |
| 18 | Top band white-ish | Interior samples (253,255,231)/(254,255,235)/(251,255,231) = cream #FFFFE8; border row y55 median (34,23,117) = dark blue. | **CONFIRMED cream fill + blue hairline** — build correct. |

## Net conclusion

Every content-level claim against the CURRENT build is either CONFIRMED-correct-in-build or
REFUTED-as-non-defect. No build change was required from the prior FAIL verdicts: the
attempt-5 build already incorporated the frame-corrected values, and this pass
re-established that those corrections are right. Rendering fidelity (font substitution,
delimiter curvature) is left to the fresh judge legs.

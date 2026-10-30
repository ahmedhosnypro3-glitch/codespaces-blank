# Slide 048 — delta vs certified slide 045 (most-related certified predecessor)

**Why 045:** closest certified composition (gen_status=passed, visual_check=PASS, 2026-10-25).
045 "Iteration 4" is the same perceptron-iteration family: top band + augmented-vectors
box + red iteration box + six-row calculation panel on the right. 048 is "Iteration 1"
(the weight-UPDATE variant), so rows that 045 renders as one-line "⇒ Keep same Weight"
become full update equations. All coordinates are frame px (960×540, 1px = 1pt), taken
from the frame-measured headers of `build/slide_045.js` (certified) and
`build/slide_048.js` (current build), to be confirmed against the prephase ground-truth
reads in `orig_judges/`.

Legend: **DIFFER** = same element, different geometry/content · **ADD** = present in 048
only · **DELETE** = present in 045 only (must NOT be drawn on 048) · KEEP = unchanged.

## Chrome (house)

| # | Element | 045 (certified) | 048 | Action |
|---|---|---|---|---|
| C1 | Gray panel + red strokes | E9E9E7 x54..903 y45..540; C00000 L/R/bottom, no top | identical | KEEP |
| C2 | Badge | circle d≈35 @ (876,73), FDFD96, ring 6A5ACD | identical except numeral **45→48** | DIFFER (numeral only) |

## Top band (y≈54..130)

| # | Element | 045 | 048 | Action |
|---|---|---|---|---|
| T1 | Band container | BLUE #0000FF 1pt outline box x68..719 y54..129, white fill | same box family but border is INDIGO #211776 (measured cores (33,23,118)/(35,23,109)); white fill | DIFFER (border color) |
| T2 | Input table x1..x6 | header y64..73; 3 data rows cy 82/92.5/103; class row y113..125; cols 96/118/140.5/163/186/209; **no parentheses** | same 6 cols; data rows **each digit wrapped in TALL per-column parentheses** (stroke pairs cols (90,102)(111,125)(133,147)(156,170)(179,193)(201,215), rows ~80..102); 3rd data row = (1 2 2 4 5 6) vs 045's (1 1 1 4 5 6) | DIFFER (paren strokes + row-3 values) |
| T3 | Class row colors | top table: C1 RED D8262C, **C2 BLACK** | C1 RED FF0000, **C2 INDIGO #1F1655** (measured core (31,22,85), zero red px) | DIFFER |
| T4 | Initial W vector | bracket verticals x330.5/x351.5 y59..105, entries 4/−2/−2 cy 66.5/83/97.5; label x266..324 y75..85, W underlined | **moved right of table**: label "Initial W =" cols 366..421 rows 61..72 (italic, no underline in build); vector PNG eq_initial_w_col cols 330..353 rows 61..101 | DIFFER (position, label style; verify underline in ground-truth read) |
| T5 | Step text | "Step η = 2" RED D8262C x365..435 y66..80, bold italic | **REPLACED by "REPEAT using Step η = 1"** RED FF0000 bold cols 426..530 rows 62..73 | DIFFER (text + value 2→1) |
| T6 | Check-classes caption | "Check classes of" x499..583 y79..88 | same text, cols 542..626 rows 86..96, italic 9pt in build | DIFFER (position) |
| T7 | Z table | header **Z1 Z1 Z1** (all "Z1"), BLUE; data (0 7 3)/(0 6 2) rows cy 87.5/102.5, cols 605/627.5/650; black data | header **Z1 Z2 Z3** (distinct subscripts), black; data (0 7 3)/(0 6 2), cols 648.5/671/693, header rows 71..83 | DIFFER (header labels + column x) |
| T8 | Legend line | "C1 positive, C2 negative, Zero is unaccepted" x240..509 y109..124; Zero GREEN 458A38 | same text/position x239..508 rows 110..124; C1 RED, C2 INDIGO #1F1655, Zero GREEN 458A38 | KEEP (verify C2 hue in ground-truth read) |
| T9 | Pointer arrow | small dark arrow x638..655 y115..127, down-right | none in build; spec claims white mouse cursor near "unaccepted" x~70-76% y20-26%; **PIL probe `pil_probe_048.txt`: (672..730,108..140) holds only indigo-family ink (Z digits + box border, core (51,44,121)) — no black-outlined cursor** | **GROUND-TRUTH CHECK** — read `orig_full.txt` §5; a pure-white cursor on white is unrecreatable without an outline |

## Mid-left block

| # | Element | 045 | 048 | Action |
|---|---|---|---|---|
| A1 | Augmented box | white box x70..246 y140..255, 1pt GRAY A6A6A6 border | same box, border GRAY #ABAFBA 0.75pt, x69..247 y139..257 | DIFFER (stroke hue/width minor) |
| A2 | Box title | "Ugmented Vectors ( from Top )" BLUE, Times New Roman italic 12pt, y147..159 | **BLACK** Arial 12pt (not blue, not serif) x90..228 y149..156 — 048's build renders black; 045 certified blue+serif. Ground-truth read must settle the frame's family (serif vs sans, color) | DIFFER (**verify**) |
| A3 | Matrix | header x1..x6; 4 numeric rows (incl. (1 1 1 4 5 6) row 4); class row C1 RED/C2 BLUE; cols 99.5/122/144.5/167/189.5/212.5 | 3 numeric rows: bias (1 1 1 1 1 1), (1 2 1 5 6 6), (1 1 2 4 5 6); class row C1 RED/C2 INDIGO; cols 98/121/143/165.5/188/212.5; **per-column delimiter strokes** (12 verticals, 6 pairs: 93.8/106.5 … 204.7/218.2, rows 180..225.2, gray #909090) | DIFFER (row count, delimiters, C2 hue) |
| A4 | Iteration box | RED D8262C fill x84..214 y277..305, WHITE bold "Iteration 4" 17pt | RED #C6020A fill x83..214 y276..306, WHITE bold "Iteration 1" 13pt | DIFFER (text, font size) |
| A5 | Stop box | WHITE/PINK box x64..246 y330..415 with "No change in W" + red "Stop Iterations" | **NOT PRESENT on 048** (iteration 1 does not stop) | DELETE |

## Calculation panel (right, x≈274..853 y139..528)

| # | Element | 045 | 048 | Action |
|---|---|---|---|---|
| P1 | Panel structure | white panel x274..853 y139..528 + D9D9D9 1pt rules at 12 y-bands (6 rows of 57-58px, 9px double-rule gaps) | **six separate white boxes** each with its own thin gray #ABAFBA 0.75pt border; tops/bottoms (139,197)(197,272)(272,330)(330,395)(404,461)(461,528) | DIFFER (ruled panel → bordered boxes) |
| P2 | Row content structure | ONE line per row: d(xᵢ) = + BLUE row "1 a b" on the text line + gray bracket with GREEN stack (14/−4/0) + "= scalar" + ⇒ + "Keep same Weight" + W = [14;−4;0] | full 2-D dot-product equation as PNG: d(x₁)=[1 1 1]·[4;−2;−2]=0 …; row 1 additionally carries the UPDATE equation W=[4;−2;−2]+1·[1;1;1]=[5;−1;−1]; rows 2-6 "W = [5;−1;−1]" (PNG eq_r_kw) | DIFFER (content class: text+strokes → equation PNGs) |
| P3 | Row scalars | = 10 / = 6 / = 10 / = −6 / = −10 / = −112 (W=[14;−4;0] frame arithmetic) | = 0 / 2 / 2 / −4 / −6 / −7 (W=[5;−1;−1] iteration-1 arithmetic) | DIFFER (values) |
| P4 | Action phrases | "Keep same Weight" ×6, BLACK, W of Weight underlined, x525.., 13pt | row1 "Update Weight", rows2-6 "Keep same Weight", **BLACK** (spec's maroon #8B0000 is wrong — measured darkest core (13,15,12)), x509.. | DIFFER (row 1 text; color family same) |
| P5 | ⇒ glyph | BLACK 13pt text glyph | **RED C00000 bold 15pt** at cols 490..498 | DIFFER (color) |
| P6 | Row-1 annotation | none | spec claims GREEN #1E8449 double-lined ⇐ arrow at x93-97% y30-36%; **PIL probe `pil_probe_048.txt`: region (893..931,162..194) holds ONLY the house chrome red stroke x900..902, and (853..900,150..190) is EMPTY — the arrow is refuted at the spec's claimed position**; build's own green census also found only chroma noise | REFUTED — do not draw; vision read `orig_calc_r12.txt` §5 confirms |

## Equation-asset inventory (per OMML/sidecar facts)

- 048 currently renders **9 equation PNGs**: eq_r1_l…eq_r6_l (6), eq_r1_w (1), eq_r_kw (1,
  shared rows 2-6), eq_initial_w_col (1). Sidecars exist with baseline_frac — reuse ALL of
  them if the certified build is kept; no new renders needed unless a ground-truth read
  contradicts their content.
- 045 used zero PNGs (pure text + stroke idiom) — do NOT import that idiom into 048; the
  2-D stacked constructs here (dot products with bracket vectors) are PNG-class content.

## Open ground-truth questions (settle from orig_judges reads)

1. T9 pointer/cursor icon near "unaccepted" — present or not, exact shape/color.
2. P6 green ⇐ arrow right of row 1 — present or not.
3. A2 title font family + color (blue serif vs black sans).
4. T4 "Initial W =" label — W underlined in the frame?
5. T3/T4 C2 hue in class row + legend (INDIGO #1F1655 vs BLUE #0000FF).

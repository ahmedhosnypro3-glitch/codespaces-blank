# Slide 049 — delta vs certified slide 046 (most-related certified predecessor)

**Why 046:** closest certified composition (gen_status=passed, visual_check=PASS).
046 "Perceptron Algorithm: Iteration 4 — Stop Iterations" shares 049's "Iteration 2 —
no change → stop" narrative shape: top band with data table + weight/step math + Z grid,
augmented-vectors box, red iteration box, "No change in W / Stop Iterations" block. 046
carries a scatter plot where 049 carries six calculation rows. All coordinates are frame
px (960×540, 1px = 1pt) from the measured headers of `build/slide_046.js` (certified) and
`build/slide_049.js` (current build), to be confirmed against `orig_judges/` reads.

Legend: **DIFFER** = same element, different geometry/content · **ADD** = 049 only ·
**DELETE** = 046 only (must NOT be drawn on 049) · KEEP = unchanged.

## Chrome (house)

| # | Element | 046 (certified) | 049 | Action |
|---|---|---|---|---|
| C1 | Panel + red strokes + badge geometry | identical house values | identical | KEEP |
| C2 | Badge numeral | 46 | **49** | DIFFER (numeral only) |

## Top band (y≈54..130)

| # | Element | 046 | 049 | Action |
|---|---|---|---|---|
| T1 | Band container | NO full box: two BLACK 3px rules y55..56 & y128..130 spanning x68..719 + NAVY #221777 left stroke x69 y55..130 | FULL box x68..720 y54..130, **VIOLET #6A5ACD 1.5pt** border, white fill | DIFFER (container shape + color — verify in `orig_topband.txt` §1) |
| T2 | Data table | header x1..x6 y64..73; rows [1,2,1,**5,6,4**] y80..89, [1,1,2,4,5,6] y96..105; cols ~94.5..206.5 | header + rows [1,2,1,5,6,6] / [1,1,2,4,5,6] / [1,1,2,4,5,6] (three data rows per spec, build draws 3) + **7th column "Initial"** with cell "Initial W = [4, -2]" x257..423 | DIFFER (row values; ADD 7th column) |
| T3 | Class row / labels | top block y111..124: **C1 BLUE, C2 RED** (046's certified inversion) | augmented table class row y230..244: **C1 RED ×3, C2 BLUE ×3** | DIFFER (verify hue order from frame — 049's build uses the majority-family order) |
| T4 | Weight equation | "Initial" black x336 + eq_046_initial_w PNG x366 y67 + black bracket x330.5 y62..103 + red vertical x433.5 | **inline text "Initial W = [4, -2]"** x257..423 y64..79 (bracket-linear form!) + RED "Initial" header x233..257 y64..78 | DIFFER (2D PNG vs inline-linear text — GROUND-TRUTH: does the frame show a stacked vector here or a bracket-linear one? `orig_topband.txt` §3) |
| T5 | Step text | "Step" BLACK x331 y89..104 + red η = 2 PNG (eq_046_step_eta) | **"REPEAT using Step η = 1"** RED bold x420..535 y61..74 | DIFFER (ADD REPEAT line, DELETE Step/η=2 line) |
| T6 | Check-classes caption | "Check Classes of Z" x320..508 y110..124 | "Check classes of" x548..640 y85..99 | DIFFER (text + position) |
| T7 | Z grid | header "Z1 Z1 Z1" black; rows 0 0 7 / 0 6 2; three paren pairs x598/611,621/634,643/656 y80..110 | 3×3 grid x636..706 y69..118: header "Z1 Z1 Z1", rows **(0)(7)(3) / (0)(6)(2)** parenthesized, NO bracket strokes | DIFFER (values + delimiter style) |
| T8 | Legend line | "C1 positive C2 negative Zero is unaccepted" x251..508 y110..124, **C1 BLUE / C2 RED / Zero GREEN** 12pt | same text x245..544 y110..124 15pt, **C1 RED / C2 BLUE** tags only, "Zero is unaccepted" black | DIFFER (hue mapping, Zero color — verify) |
| T9 | Final-weight box | YELLOW #FDFD96 box x738..828 y59..142, black 1pt border, underlined W = tall-paren (14/−4/0) | build draws **NOTHING** there | **GROUND-TRUTH CHECK**: does 049's frame carry a weight box top-right? (`orig_full.txt` region map) If yes ADD with measured box; if no DELETE stays |

## Mid-left block

| # | Element | 046 | 049 | Action |
|---|---|---|---|---|
| A1 | Augmented container | left/right BLACK verticals x69/x245 y140..249 + dashed top y140 + solid rule y255 (open box) | no container strokes in build; table only x89..215 y162..230 | DIFFER (verify frame: closed box, open rules, or bare?) |
| A2 | Title | **NOT PRESENT** (046 measured zero ink for "Ugmented Vectors") | "Ugmented Vectors (from Top)" VIOLET #6A5ACD x82..219 y148..159 | ADD |
| A3 | Matrix | header y166..175; rows [1,2,1,5,6,4]/[1,1,2,4,5,6]/[1,1,1,4,5,6]; class row y232..240 | header + 4 data rows (bias (1,1,1,1,1,1) + (1,2,1,5,6,6) + (1,1,2,4,5,6) + (1,1,2,4,5,6)); class row y230..244 | DIFFER (row count/values — verify 3rd vs 4th data row in `orig_aug_stop.txt` §4) |
| A4 | Iteration box | RED C00000 x84..212 y277..304, white bold 20pt "Iteration 4" | RED FF0000 x84..213 y278..304, white bold 21pt "Iteration 2" | DIFFER (text, hue, size) |
| A5 | Stop block | PINK #FFC0CB BOX x64..245 y331..415 black border; "No change in W" 15pt black; "Stop Iterations" 17pt RED bold, centered | **NO BOX** — plain text lines: "No change in W" 20pt x78..216 y349..371 (W underlined, separate run x198..216); "Stop" RED x85..123 + "Iterations" BLACK x127..208, 20pt, y374..394, left-aligned | DIFFER (box vs bare text; verify frame `orig_aug_stop.txt`) |

## Right side

| # | Element | 046 | 049 | Action |
|---|---|---|---|---|
| R1 | Scatter plot | plot_046_scatter.png x312 y173 w514 h310 | **NOT PRESENT** | DELETE |
| R2 | Calc rows | none | SIX rows x273..852, rules y140/205/271/337/403/469/527 (light gray C1C1C9 1pt): per row "d(xN) =" x283 + 2-row bracketed matrix PNG x348 (w 0.79167in) + "⇒ Keep same Weight" x508 + "W =" x697 (rows 1-3) / x709 (rows 4-6) + bracketed column PNG x721/x732 | ADD |
| R3 | Matrix values | n/a | row1 [1,1,1,5]/[-1,3]; row2 [1,2,1,5]/[-1,2]; row3 [1,1,2,5]/[-1,2]; row4 [1,5,4,5]/[-1,-4]; row5 [1,6,5,5]/[-1,-6]; row6 [1,6,6,5]/[-1,-7] | ADD (content) |
| R4 | W column | yellow-box vector (14/−4/0) | per-row [5;−1;−1] PNGs, ~11px right-shift rows 4-6 | ADD |

## Equation-asset inventory

- 049 renders **12 PNGs**: slide_049_matrix_1..6 (2-row bracketed d(x) matrices, w 0.79167in)
  + slide_049_wcol_1..6 ([5;−1;−1] columns, w 0.29167in; sidecar eq_slide049_wcol.json has
  per-row geometry). All exist and are certified-shape (2D law) — **reuse, no new renders**,
  unless ground-truth reads contradict their content.
- 046's eq_046_initial_w / eq_046_step_eta PNGs are NOT reusable for 049 (different text),
  but the paren-stroke idiom and `render_eq.py` pipeline are.

## Open ground-truth questions

1. T9 top-right weight box: present on 049's frame or not?
2. T4 "Initial W = [4, -2]": inline-linear as the build has it, or a stacked 2×1 vector?
3. T1 container: full violet box vs 046-style rules?
4. T3 class-label hue order (C1 red vs C1 blue).
5. A3: three or four data rows in the augmented table (spec says 4, 045/047 pattern says 3+bias).

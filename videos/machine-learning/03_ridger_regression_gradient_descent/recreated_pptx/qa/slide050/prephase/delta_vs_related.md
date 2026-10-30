# Slide 050 — delta vs certified slide 046 (most-related certified predecessor)

**Why 046:** closest certified composition (gen_status=passed, visual_check=PASS). 046
"Perceptron Algorithm: Iteration 4 — Stop Iterations" is the ONLY certified slide carrying
the full 050 composition class: top band with weight/step math + Z matrix + final-weight
box + augmented box + red iteration box + stop text + scatter plot. 050 is "Iteration 2"
with a DIFFERENT final weight and a modified chart. All coordinates are frame px
(960×540, 1px = 1pt) from the measured headers of `build/slide_046.js` (certified) and
`build/slide_050.js` (current build), to be confirmed against `orig_judges/` reads.

Legend: **DIFFER** = same element, different geometry/content · **ADD** = 050 only ·
**DELETE** = 046 only (must NOT be drawn on 050) · KEEP = unchanged.

## Chrome (house)

| # | Element | 046 (certified) | 050 | Action |
|---|---|---|---|---|
| C1 | Panel + strokes + badge | house values | identical | KEEP |
| C2 | Badge numeral | 46 | **50** | DIFFER (numeral only) |

## Top band (y≈54..130)

| # | Element | 046 | 050 | Action |
|---|---|---|---|---|
| T1 | Band container | two BLACK 3px rules y55..56/y128..130 x68..719 + NAVY left stroke | FULL box x68..719 y54..130, **NAVY #1E1A76 2pt** border, **CREAM #FFFFE8 fill** (not white) | DIFFER (container + fill — verify in `orig_topbox.txt` §1/§6) |
| T2 | Data table | rows [1,2,1,5,6,**4**] y80..89 / [1,1,2,4,5,6] y96..105; bare digits | rows [1,2,1,5,6,**6**] / [1,1,2,4,5,6], **only TWO data rows**, each digit **parenthesized** "(n)", class row C1 RED/C2 BLUE y112..125 | DIFFER (values, paren cells, row count) |
| T3 | Class-row colors | C1 BLUE / C2 RED (046 inversion) | **C1 RED / C2 BLUE** | DIFFER (verify `orig_topbox.txt` §4) |
| T4 | Weight equation | "Initial" black + eq_046_initial_w PNG x366 + red vertical x433.5 (value 14/−4/0? no — 046 Initial W) | eq_050_initialW PNG x266 y63 — underlined W = (4/−2) **2-entry** vector | DIFFER (entry count 3→2, position; GROUND-TRUTH `orig_topbox.txt` §3) |
| T5 | Step/REPEAT text | "Step" BLACK x331 + red η = 2 PNG | **"REPEAT using Step"** red CHART_RED #92211B bold x425..533 y59..74 — **build draws NO "η = 1"** (prior lane ruled the frame's right zone blank cream; spec said "REPEAT using Step η = 1") | DIFFER (**GROUND-TRUTH**: does the frame print "η = 1"? `orig_topbox.txt` §2) |
| T6 | Check-classes caption | "Check Classes of Z" x320..508 y110..124 | "Check classes of" x542..626 y86..96 + Z vectors below-right | DIFFER |
| T7 | Z matrix | header "Z1 Z1 Z1" black; rows 0 0 7 / 0 6 2; paren pairs x598..656 y80..110 | **three labeled 2×1 column vectors** Z1=(0,0), Z2=(7,6), Z3=(3,2): labels x641..702 y74..85, PNG vectors (eq_050_Z1/2/3) x640..702 y86..120, pitch 23 | DIFFER (structure: 3-col grid → 3 stacked vectors; values row1 = 0,0) |
| T8 | Legend line | x251..508, C1 BLUE/C2 RED/Zero GREEN 12pt | x240..510 y110..124 13pt: **C1 RED / C2 BLUE / Zero GREEN #008000** | DIFFER (hue mapping) |
| T9 | Final-weight box | YELLOW #FDFD96 x738..828 y59..142, black 1pt border, underlined W + tall-paren (14/−4/0) | **PINK #F9E8FA box x743..830 y58..171**, borderless in build (pink-on-pink), underlined W = (5/−1/−1) via eq_050_finalW PNG (3 entries vs 046's 3 — but different values; 046 digits 14/−4/0) | DIFFER (fill color, border, vector values, height 83→113px) |

## Mid-left block

| # | Element | 046 | 050 | Action |
|---|---|---|---|---|
| A1 | Augmented container | BLACK side verticals x69/x245 + dashed top y140 + solid rule y255 | **WHITE closed box x66..240 y134..248, 1pt gray #A1ABB5 border** | DIFFER (container) |
| A2 | Title | NOT PRESENT | "Augmented Vectors (from Top)" — **full "Augmented" spelling**, NAVY bold 10pt, x82..236 y145..160 | ADD (note: 045/047/051 read "Ugmented"; 050's build spells Augmented — GROUND-TRUTH `orig_aug_caption.txt` §2 settles which the 050 frame prints) |
| A3 | Matrix | 3 rows [1,2,1,5,6,4]/[1,1,2,4,5,6]/[1,1,1,4,5,6], bare digits, class row y232..240 | 3 rows: bias (1,1,1,1,1,1) + (1,2,1,5,6,6) + (1,1,2,4,5,6), parenthesized cells, class row y231..244 C1 RED/C2 BLUE | DIFFER (values + cell style) |
| A4 | Iteration box | C00000 x84..212 y277..304, 20pt | RED_DARK #C90004 x84..213 y278..305, 13pt bold | DIFFER (hue, size) |
| A5 | Stop text | INSIDE pink box x64..245 y331..415: "No change in W" 15pt + "Stop Iterations" 17pt red, centered | **BARE TEXT** (no box): "No change in W" 20pt x77..237 y348..371 (W underlined), "Stop" red + " Iterations" black 20pt x83..243 y373..395, left-aligned | DIFFER (DELETE pink box; text sizes differ — 050's stop-size fix landed 2026-10-25) |

## Chart region

| # | Element | 046 | 050 | Action |
|---|---|---|---|---|
| G1 | Chart image | single PNG plot_046_scatter.png x312 y173 w514 h310 | **composed natively**: red-border 3px white panel x312..824 y173..481 + gridlines (data y=7,6,5,3,2,1,0; NO y=4 line) + spines + tick labels 0..8 / 7..0 + decision LINE shape y=−1.00417x+4.90556 from (−0.51,5.42) to (6.19,−1.31) w 3.5 arrow + markers + "+ve" | DIFFER (PNG embed vs native composition — keep native; 046's PNG idiom was for a static plot) |
| G2 | Markers | (inside 046 PNG) | blue squares (1,1)(2,1)(2,2) #1C3D5E 8×8; magenta diamonds (5,4)(6,5)(6,6) #FF94FF 11×11; red triangle (7,6) 9×9; red origin blob (0,0) d9 | ADD (values from measurement) |
| G3 | "+ve" annotation | (inside PNG) | red bold 11pt at data (0.56,3.84) + two red arrows | ADD |
| G4 | Data values | 046 chart's own data | red triangle at (7,6) per build vs spec's "red triangles at (3,3) and (7,6)" | **GROUND-TRUTH**: does a red triangle sit at (3,3)? (`orig_chart.txt` §5) |

## Equation-asset inventory

- 050 renders **5 PNGs**: eq_050_initialW (2-entry Initial W), eq_050_Z1/Z2/Z3 (2-entry Z
  columns), eq_050_finalW (underlined W = 3-entry stack, re-rendered 2026-10-25 as
  677×496 substack after the attempt-9 size finding). All sidecars exist → **reuse; no new
  renders** unless a ground-truth read contradicts content.
- 046's eq_046_* PNGs are NOT directly reusable (different values); the plot_046_scatter.png
  is 046-only and must NOT be embedded in 050.

## Open ground-truth questions

1. T5: does the frame print "η = 1" after "REPEAT using Step"?
2. T4: Initial W entry count (2 vs 3) and W underline.
3. A2: "Augmented" vs "Ugmented" spelling on 050's frame.
4. T1/T9: exact border colors of the navy box and the pink box (bordered or borderless).
5. G4: red triangle at (3,3) present?

# Slide 031 — worker report (worker-kimi-031-r2)

Deck: `videos/machine-learning/03_ridger_regression_gradient_descent`
Slide: 031 — "Convex Function, Learning Rate =0.3, Start at X=3"
Lane: build + judge (Template A full-slide + Procedure B crop-pair certificates)

## Build state

- Script: `recreated_pptx/build/slide_031.js`
- Deliverable: `recreated_pptx/slide_031_recreated.pptx` (single plain-named file)
- Current render: `recreated_pptx/qa/slide031/render_8.png` (2001x1125, 150 dpi)

## Defects found and fixed BEFORE judging (a FAIL would have made judging invalid)

### 1. Badge occluded by the graph rect — BLOCKER, FIXED

`house_chrome_check.py` on the first render FAILED with
`badge center (1824,131) vs (1825,152) (tol 8)` — the badge's lower half was
covered, 21 render-px high.

Root cause: the build drew the graph's white plot rect at frame x 640..900,
y 70..240, and `drawHouseChrome` emits the badge BEFORE the graph (so the
graph rect painted over the badge). The original frame shows the badge fully
intact (yellow bbox frame x 860..892, y 59..88, center (876, 73.5)).

Fix: re-measured the plot box as **frame x 573..809, y 66..267** and moved the
graph there (with a red C00000 1pt border — the frame border is red, JPEG-darkened
to (117,50,57), not black as the analysis JSON said).

Verified after rebuild: `house_chrome_check.py` → **PASS** (badge center (1824,152).

### 2. Parabola spilling ink outside the plot box — MAJOR, FIXED

The un-clipped parabola leaked strict-blue pixels outside frame box
x 640..900 / y 70..240 (5,956 px, bbox reaching frame y 0 at x 659..832).

Fix: clip the drawn span to the visible range |x-5| <= sqrt(yMax - 1), i.e.
data x 1.025..8.975 → frame x 641.7..732.3.

Verified after rebuild: 0 strict-blue px below the title band outside the plot
box (the 4,129 blue px that remain are the blue "Start at X=3" title text at
frame bbox 65..206, 134..152 — content, not spill).

### 3. Y-axis scale and grid lines — corrected

Frame y grid lines are at 87/146/206/265 → y = 15/10/5/0 at 11.87 px/unit with
y=0 at the box bottom. The old `yMax` squash put lines at 10 px/unit. Corrected
to yMin=0, yMax=15, yTickVals [0,5,10,15].

### 4. Chord and markers — replaced from measured positions

The spec said "black horizontal segment from (3,9) to (7,9) labeled (7,9)" and
"Red point FF0000 at (3,9)". The frame disproves this: the black chord sits on
the **y=10** grid line (frame 146) spanning data x 1.75..8.33, with 3 short
vertical ticks at data x ~2, 5.4, 9, and the red dot at data ~(2.7, 6.9).
Replaced from measurement; the `(7,9)` text label and the "Red point at (3,9)"
block were removed.

## Closed-loop gates run BEFORE any judge dispatch

| Gate | Command | Result |
|---|---|---|
| house chrome | `python3 shared_patterns/house_chrome_check.py qa/slide031/render_1.png` | **PASS** (panel x112-1882 y94-bottom; L/R/bottom strokes, top bare; badge (1824,152) d=68) |
| blue containment | strict-blue px below title band outside plot box | **0** (was 5,956) |

## Curve fidelity

f(x)=(x-5)^2+1 is analytic, so the sampling ripple is pure discretisation.
N=200 gives 3.16e-03 max abs 2nd difference = 0.0375 frame-px (invisible at
150 dpi). **N=200 chosen.**

## Procedure B crop pairs banked (matched effective scale, 2.083 render-px / frame-px)

| name | frame bbox | out px | region |
|---|---|---|---|
| `table` | (55,342,901,538) | 1763x409 | main 8-row density table |
| `graph` | (565,58,817,275) | 525x452 | plot box: parabola, chord, points, grid |
| `topblock` | (36,52,648,342) | 1276x604 | title, param table, formula box, annotation box |

Each pair is `crop_1_<name>_render.png` + `crop_1_<name>_orig.png`; original
crops LANCZOS-upscaled by H_render/540 so both images share the same effective
scale per axis. Pixel dims match exactly for all three pairs.

## Judge dispatch

Attempts are shared across both legs (6 max per slide, 3 garbage re-invokes,
W4 one hard-wall retry). All vision calls route through
`scripts/16_vision_gate.sh` — never wrapped in a retry loop, one call at a time.

**Template A (full-slide), attempt K=1** — `judge_attempt_1.txt` → **FAIL**
(banked 2026-10-24 00:54, coherent body with a FINAL VERDICT line).

The judge raised 5 findings. PIL adjudication against BOTH images:

| # | Claim | Adjudication |
|---|---|---|
| 1 | Annotation line 1 "X is in between 4.8 and 5.1" missing — BLOCKER | **CONFIRMED.** Render had 1 text band (y 283..292); the frame has 2 (y 249..261 and 266..283) inside a box bordered y 244 / 289. |
| 2 | Equation reads `f(x)=(x-5)²+` — "+ 1" dropped — BLOCKER | **REFUTED.** Asset `eq_031_main.png` ink spans x 8..1682 of 1690px (complete quadratic); rendered ink x 114..629 of a 646px box vs the frame's 69..301 of 310px — the render is WIDER, not truncated. |
| 3 | Table forces `3.30` / `5.0` padded decimals — MAJOR | **CONFIRMED.** Build used `val.toFixed(2)` then stripped only `.00`, emitting `3.30`, `5.0`, `-0.80`, `4.80` where the frame shows `3.3`, `5`, `-0.8`, `4.8`. |
| 4 | All chart tick labels + grid lines absent; "(5,1)" missing — MAJOR | **PARTLY CONFIRMED.** x-axis tick labels and the "(5,1)" label were genuinely absent; grid lines and y tick labels were present (the judge's gray-line reading failed on JPEG noise). |
| 5 | "1.04"/"1.01" not emphasized — MINOR | **CONFIRMED** in effect; line 2 rendered plain. |

### Root causes found and fixed

1. **y-axis mapping was wrong (13% error).** `mapY` mapped data y=15 onto the
   plot box's top edge (frame 66). The frame's grid puts y=0 at frame y 265 and
   y=15 at frame y 87, i.e. 11.8667 px/unit with the grid INSIDE the box.
   Verified: data y = (265 − frame_y)/11.8667 reproduces the vertex (253→1.01),
   the chord (146→10.03) and the parabola through the measured vertex (688,253).
   Fixed to the measured absolute model `yZeroY = 265, yPPU = 11.8667`.
2. **The annotation box swallowed two elements via z-order.** The box's white
   fill (x 243..809, y 244..289) was drawn AFTER the chart labels, so it painted
   over the x-axis tick labels (frame y 271..285). It is now measured to the
   frame (y 244..289) and ends above the tick labels.
3. **`(5,1)` was drawn before the annotation box** (pptx shape index 245 vs the
   rect at 323), so its white fill covered the label even at the right
   coordinates. The label is now emitted AFTER the annotation text and anchored
   to the measured position x 497..535, y 249..261.
4. **Table decimal padding** — replaced `.toFixed(2)` with trailing-zero
   stripping so `3.3`, `5`, `1.01` render as the frame shows.

Render lineage: `render_1.png` (pre-fix) → `render_2.png` (y-map + annotation
box) → `render_3.png` (label position) → `render_4.png` → `render_5.png`
(label drawn after the box, table decimals). All kept as evidence per the
never-delete law.

### Closed-loop gates on render_5.png (all green before any judge call)

| Gate | Result |
|---|---|
| house_chrome_check.py | **PASS** (panel x112-1882; L/R/bottom strokes, top bare; badge (1824,152) d=68) |
| annotation line 1 present | **PASS** — render y 250.4..259.5 vs frame 247..260 |
| annotation line 2 present | **PASS** — render y 267.3..276.4 vs frame 265..286 |
| x tick labels present | **PASS** — render y 271..277 vs frame 270..280 |
| "(5,1)" label present | **PASS** — render 131 green px vs frame 151 in the measured band |

**Template A (full-slide), attempt K=2** — `judge_attempt_2.txt` → **FAIL**
(banked 2026-10-24 02:11, coherent body, FINAL VERDICT line; probes hung twice so
the real judge was dispatched and rode its 630s-abort-then-retry ladder to land).

The judge **confirmed the content** this time (all 8 table rows across the
bouncing tail, the mini-table 0.3/3/0.1, title colours, parabola shape,
gridlines, red start dot, dashed vertical at x=5, black capped chord, house
chrome) and raised 8 findings. PIL adjudication against BOTH images:

| # | Claim | Adjudication |
|---|---|---|
| 1 | Title split into 3 stacked lines; original is ONE line — MAJOR | **CONFIRMED.** Frame: the whole title is one row at y 66..83 — red x 81..230, green x 260..440, blue x 446..530. Build stacked three boxes at y 65..159. FIXED. |
| 2 | Equation "+1" clipped by the plot frame — BLOCKER | **REFUTED.** Equation ink in render_6 is x 385..564 vs frame 399..573 — a 5px wider match, fully inside the box (x 330..640). The judge's reading was a colour-threshold artifact; the plot frame is at x 573, far from the equation's right edge at 564. |
| 3 | Equation box + annotation box collide with the plot frame — MAJOR | **REFUTED.** Annotation borders render cleanly at y 243/244 and 288/289 across x 243..809; the frame's own plot bottom (y 265) and annotation top (y 244) genuinely overlap in the ORIGINAL too, so the render matches. |
| 4 | Words "colored red bold" dropped — MINOR | **REFUTED.** Per the spec-vs-frame notes (item 3) that string is a formatting marker, not literal text; the frame shows only "X is in between 4.8 and 5.1" with 5.1 in red bold. |
| 5 | "Bouncing" should be pinkish/magenta-red, not purple — MINOR | **REFUTED.** Frame's dominant saturated colour in that box is (175,170,250) — blue-violet, plus a pale (247,201,248) wash. 7030A0 purple is a match within MINOR; left as built. |
| 6 | "(5,1)" should sit beside line 2, not above line 1 — MINOR | **REFUTED.** Frame PIXEL scan of x 495..545, y 244..262 shows the label glyphs at y 249..261, and the annotation box starts at y 244 — so the label is vertically aligned with line 1 in the frame. Build matches. |
| 7 | x-axis tick labels absent/partially obscured — MINOR | **CONFIRMED.** The x-label boxes existed in the pptx (frame y 269..283) but were painted over by the annotation box's white fill, exactly like the "(5,1)" label. FIXED by drawing them after the box. |
| 8 | Table left border sits on the panel stroke — MINOR | **REFUTED.** Frame borders: panel stroke at x 57..58, table border at x 64. Build draws the table at x 63..64 — a match, not an overlap. |

### Third defect found by PIL during adjudication (K=2)

**Table row colours were the spec's 6-colour list, but the frame is an 8-colour
rainbow.** Measured at frame x=850, row centre:

| row | frame colour | old build | fixed |
|---|---|---|---|
| 0 x | (208,217,124) yellow-green | FFFF99 | D0D97C |
| 1 f(x) | (252,251,246) near-white | D9EAD3 | FCFBF6 |
| 2 x-delta | (191,157,218) purple | CFE2F3 | BF9DDA |
| 3 f(x-delta) | (255,255,253) white | D9D9D9 | FFFFFD |
| 4 x+delta | (248,221,200) orange | FCE5CD | F8DDC8 |
| 5 f(x+delta) | (239,237,240) light grey | FFFFFF | EFEDF0 |
| 6 slope | (147,209,134) **green** | FFFFFF | 93D186 |
| 7 next x | (252,188,189) **pink** | FFFFFF | FCBCBD |

Fixed; verified after render_6: **all 8 rows match the frame pixel-exactly
(RGB delta 0,0,0 on every row)**. This also retires the `[?]` inferred
row-colour mapping in the earlier report.

Render lineage: render_1 (pre-fix) → 2 (y-map + annotation box) → 3 (label
position) → 4 → 5 (label after box, table decimals) → **render_6** (title
one-line, x-tick labels after the box, measured row colours).

## Known residuals

- **Annotation line 1 runs 59px narrower in the render** (x 254..514) than the
  frame (x 250..573) at 13pt. Line 2 matches within 5px (253..575 vs 250..580).
  A font-metric sizing difference at MINOR; line 1 would need a slightly larger
  font to close.
- The parabola's vertex in the render reaches frame y 242 while the frame's
  measured vertex is y 253 — the last few pixels of descent are cut by the
  annotation box's top border, which the frame itself places at y 244 over the
  same region. MINOR at most.
- The red dashed lines at x=5 and y=1 are retained at FF0000: the analysis JSON
  lists them, and removing a spec-listed element is a bigger fidelity risk than
  a hairline stroke.
- `require("./assets/eq_031_main.json")` in the build script is dead code (its
  result is unused — the equation size is inlined). Harmless, left in place.

## Attempt ledger

| K | render | transcript | verdict | notes |
|---|---|---|---|---|
| 1 | render_1 | judge_attempt_1.txt | FAIL | pre-fix; 5 findings, of which #1/#3/#4 confirmed and #2 refuted |
| 2 | render_5 | judge_attempt_2.txt | FAIL | 3 confirmed (title lines, x labels, row colours) + 5 refuted; content verification passed |
| 3 | render_6 | judge_attempt_3.txt | **none — hang** | interrupted; the analyzer's ladder aborted twice at 630s and no body banked, so it is not a counted attempt |

### Fourth defect found by PIL after K=2 (render_7, render_8)

**The 3x2 parameter table's cell fills were the spec's yellow/white, but the
frame uses green/green/pink labels on a warm-grey value column.** Modal colour
of each cell interior in the frame:

| cell | frame modal | old build | fixed |
|---|---|---|---|
| label "step" | (234,255,213) green | FFFF99 | EAFFD5 |
| label "initial X" | (235,255,211) green | FFFF99 | EAFFD5 |
| label "delta" | (242,196,198) pink | FFFF99 | F2C4C6 |
| all 3 values | (231,233,230) warm grey | FFFFFF | E7E9E6 |

Fixed; verified after render_7: all six cells reproduce the frame's modal
colour exactly. The build script was copy-then-modified, with the pre-fix copy
banked as `build_slide_031_pre_paramfix.js`.

**Title vertical placement** moved to frame y 60..82 (was 66..90 band) so the
one-line render sits at y 64..84 against the frame's 66..88 — inside 2px at the
top. Verified in render_8.

Render lineage: render_1 (pre-fix) → 2 (y-map + annotation box) → 3 (label
position) → 4 → 5 (label after box, table decimals) → 6 (title one-line, x
labels after box, measured row colours) → 7 (param-table fills) →
**render_8** (param fills + title vertical placement).

### Closed-loop gates on render_8.png

| Gate | Result |
|---|---|
| house_chrome_check.py | **PASS** (panel x112-1882; top bare; badge (1824,152) d=68) |
| annotation line 1 | render y 251..259 vs frame 247..261 |
| annotation line 2 | render y 267..277 vs frame 265..287 |
| x tick labels | render y 272..277 vs frame 270..275 |
| title one line | render y 64..84 vs frame 66..88 |
| "(5,1)" label | green glyphs render frame x 497..521, y 251..259 |
| param table fills | all 6 cells = frame modal colour |
| main table row fills | all 8 rows pixel-exact (delta 0,0,0) |
| crop pairs for K=4 | `crop_4_{graph,table,topblock}` cut from render_8; both images identical dims, matched scale ~2.083 |

Attempts used so far: 2 coherent verdicts (K=1, K=2). 4 remain of the 6-max
budget, shared across both legs.

## Adjudication: red dashed x=5 line placement (vs render_25) — 2026-10-25

- Orig dashed line: red cols x658-664 (runs 8-11px each, sparse dashes); orig red
  axis verticals x572-574 (204px) and x808-810 (204px).
- Render dashed line: frame x690.4 (171px tall) + x690.9; render's own tick labels
  sit at 571.8/631.7/690.7/752/806 (evenly ~61px apart = -5,0,5,10,15), so the
  render's line sits EXACTLY on its own x=5 tick.
- Orig tick-label glyphs are too small/degraded to establish an even tick lattice
  (clusters ~578, ~653-658, ~672-676, ~742-750, ~805-811; spacing uneven).
- Orig line at 658-664 sits adjacent to a label cluster at ~653-658, i.e. the
  original's hand-placed line may not sit on its own x=5 tick. The render is
  internally self-consistent (line on tick, curve minimum aligned).
- Disposition: ~30px frame delta in an element whose original placement appears
  hand-imprecise; chart-internal consistency preserved. MINOR-class; no fix
  trigger unless a fresh judge leg escalates it (then adjudicate again PIL-first).

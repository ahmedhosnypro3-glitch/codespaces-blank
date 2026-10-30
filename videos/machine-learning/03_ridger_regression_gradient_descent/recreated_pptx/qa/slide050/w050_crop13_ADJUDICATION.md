# Slide 050 — crop_13 adjudication record (fresh carrier, run 299640, 2026-10-26)

Inputs: the six `crop_13_*_judge.txt` transcripts (render_13), plus banked PIL:
`w050_chartfix_pil_raw.txt` (F1/F2/F3/F4/F6 + line-thickness + pinkbox),
`w050_arrow_redstop_pil_raw.txt` (arrow ascii, redstop ascii, pinkbox v2), and the
fresh `w050_crop13_adj.py` → `w050_crop13_adj_raw.txt` (Initial-W rows, eta re-bank,
REPEAT underline, aug-paren runs, line hue, gridline, banner/Stop red, slant).

## Dispositions per finding

### mathzone F1 + tableeq F1 — "Initial W missing third row" (BLOCKER) — **CONFIRMED REAL**
The original's Initial-W construct (parens x330..353, y62..102) contains THREE digit
rows between the parens: `4` (y62..70), `−2` (bar y82 x336..341 + digit y78..86),
`−2` (bar y98 x336..341 + digit y93..102) — measured in `w050_crop13_adj_raw.txt`
§A + the color-classified dump banked in the run log. Render_13 shows a 2-row
(4/−2) stack (y65..85). This matches certified sibling 042's adjudicated reading
(`slide042/adjudication_attempt23.md`: "CONFIRMED W = (4, −2, −2)ᵀ … PIL '4,−2'
reading was a chroma artifact" — the same artifact that fooled w7's
`w7_final_pil_table.txt` "(4/-2) stacked" note; w7's DECISIVE ascii proof covered
only the pink box, not this construct). FIX: 3-row substack.

### mathzone F2 + tableeq F2 — "η = 1 missing after 'REPEAT using Step'" — REFUTED as stated (6th)
eta slot x531..642 y58..84: ORIG ink=0 at lum<210/200/190; RENDER=7px antialias.
BUT the investigation found the frame DOES carry a small dark underlined text at
**x364..424 y59..77** ("Step η = 1": ~7 fine glyph clusters x367..421, underline bar
y71..72 x364..424, ink mean RGB (77,80,65) — not red), which the recreation omits.
Sibling 051 carries the SAME slot content ("Step η = 1" mathtext, ink-left 365,
ink-top 67 — `w051_eq_assets.json` step asset; 042 has "Step η = 2" red at x364
y63, `slide_042.js` line 271). The att5–att11 "η=1 missing" findings were
mis-LOCALIZED hallucinations of this real element. FIX: draw it at the measured slot.

### mathzone F3 + tableeq F3-partial — "REPEAT not underlined / not bold" — REFUTED
ORIG red phrase y61..74 x426..530, band below (x426..460) red px = 0 → no underline
in the original. RENDER: bold red, no underline. Match. (Also: render IS bold — the
tableeq variant of this claim is false on its face.)

### mathzone F4 — Initial/W styling — SPLIT
- "W underlined": REAL (MINOR) — ORIG underline bar y85 x305..314 under the W;
  render W has none. FIX via `\underline{W}` in the rebuild (042 precedent:
  "the frame's W is bold-italic-underlined").
- "Initial italic vs upright": handwritten-vs-typed medium difference (rule d) —
  not counted (slide042 attempt-24 precedent).

### mathzone F5 — positive/negative italics — NOT COUNTED
Original caption is handwritten (w7: rule d); slant metric inconsistent between the
two words (ORIG +16.9/+11.5px, RENDER +6.2/+20.4px drift — noise-level). Medium
difference, at most MINOR. No fix.

### tableeq F3 — "augmented vectors flattened, no column-vector parens" (MAJOR) — **CONFIRMED REAL**
ORIG augmented panel: per-column TALL paren pairs with continuous strokes spanning
all three digit rows (≥25px runs at x=115,128,137,182,205,218; ascii shows
paren feet at y222 and tops ~y180; 3 digit rows y184..190/199..207/214..222).
RENDER: per-cell "(n)" parens with clear row gaps; ZERO columns with runs ≥8px.
Certified sibling 042's LM box = same panel, "per-column black paren pairs".
FIX: redraw 3×6 table with tall per-column parens + bare digits.

### chart F1 — "extra triangle on the line at ≈(1,4.1)" — REFUTED as stated
The shape is +ve arrow-1's head, which exists in BOTH images at the same spot
(ORIG arrow-1 x402..415 y306..318; RENDER arrow-1 head at ≈(405,305) — banked
fine-ascii in `w050_arrow_redstop_pil_raw.txt` §1 and `w050_chartfix_pil_raw.txt`
§F3). No foreign marker exists in the render alone.

### chart F2 — "broken/doubled stroke x≈0.4–0.9" — REFUTED as stated
Same zone: the "detached parallel segment" is the +ve arrow shafts, present in both
(ORIG: two strokes below the line x397..415 y307..326; RENDER: same two-stroke
structure). Residual arrow-length deltas (RENDER arrow-1 31px vs ORIG ~13px;
arrow-2 shifted ~14px left) = the att10-adjudicated MINOR arrow geometry
(att10 #9, never re-raised by att11). Not re-litigated upward.

### chart F3 — "+ve arrow reversed/detached" — REFUTED as stated (see F2)
Both images carry the same two-stroke annotation; the judge's own table confirms
"+ve text glyphs correct" and "decision line trajectory: same slope/intercept".

### chart F4 — "diamond fill washed out" (MAJOR) — **CONFIRMED REAL**
ORIG diamond centers #E034ED / #E03EE9 / #E04BEB (vivid magenta); RENDER #FF94FF
at all three (`w050_chartfix_pil_raw.txt` §F4). The build's MARK_MAG=FF94FF was a
mis-measurement. FIX: MARK_MAG → E03FEB (median of the three orig samples).

### chart F5 — line weight/hue — REFUTED
Weight: F2b decoded (render runs are render-px; line ≈6.7px vs ORIG ≈6px at
x=0.5/0.7; the "1.5–2× thicker" claim is quantitatively false). Hue: ORIG stroke
itself varies #AD2134 (fresh mid-stroke) vs ~#C8303C (build-era sample) — the
orig's own variance exceeds the render delta (92211B sits inside the observed
orig range); marker-medium difference. No fix.

### chart F6 — "line-end arrowhead present vs plain" — CONFIRMED REAL (MINOR)
ORIG line-end window x640..740 y400..460: 178 red px, single taper; RENDER: 597 px
(3.4×) — the endArrowType triangle draws a head the original lacks. FIX: plain end.

### chart F7 — gridline weight — CONFIRMED REAL (MINOR)
ORIG gridline at data y=1 is a faint hairline (only 139 px <215 lum in the
x420..760 y394..402 window); RENDER CFD1CE (lum≈209) puts 1902 px <215. FIX:
GRID → DEE0DD.

### redstop F1 — serif vs sans (MAJOR) — NOT COUNTED (ground rule d)
ORIG redstop text is HANDWRITTEN marker ink (irregular variable-width strokes,
hollow forms — `w050_arrow_redstop_pil_raw.txt` §2b ascii); "serif face" is a
misread of marker artifacts. Typed-vs-handwritten = inherent medium difference,
at most MINOR; certified precedent slide042 attempt-24 ("sans vs serif: not
counted"). No fix.

### redstop F2 — missing italics (MAJOR) — NOT COUNTED (ground rule d)
Same handwritten source; slant/italic of marker ink = medium difference
(slide042 precedent). No fix.

### redstop F3 — banner red shade — REFUTED (JPEG-class)
ORIG banner fill #C30B1C vs RENDER #C90004 (thick-fill medians, reliable):
Δ=(6,11,24) — sub-JPEG variance. No fix.

### redstop F4 — "Stop" red tone — REFUTED (thin-stroke sampling)
ORIG #D45A68 over n=399 thin-stroke masked px (halo-biased) vs RENDER #92211B;
the reliable thick-fill sample (banner) shows the render's marker red is correct
to Δ(6,11,24). Judge's own confidence: low, "possibly capture-related". No fix.

### pinkbox crop — PASS — kept (region unchanged by the fix cycle).
### caption crop — PASS, but region pixels change (construct bottom y98..102
pokes into x330..355 of the caption band) → re-cut + re-judge on render_14.

## Disposition summary
REAL findings requiring the ONE fix cycle (render_13 → render_14):
1. Initial-W 3-row (4/−2/−2) + underlined W (mathzone-F1/tableeq-F1 BLOCKER + F4).
2. Add "Step η = 1" dark underlined text at x364 y59 (real omitted element).
3. Diamond magenta → E03FEB (chart F4 MAJOR).
4. Augmented table → tall per-column parens (tableeq F3 MAJOR).
5. Decision line: remove end arrowhead (chart F6 MINOR).
6. Gridlines → DEE0DD (chart F7 MINOR).
REFUTED/NOT-COUNTED (banked above): mathzone F2/F3/F5, tableeq F2, chart F1/F2/F3/F5,
redstop F1/F2/F3/F4, tableeq "REPEAT bold" variant.
Next: rebuild → render_14 → house_chrome_check → att12 full judge + re-cut crops
(caption/mathzone/tableeq/chart/redstop; pinkbox kept) → certify.

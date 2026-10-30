# PIL defect inventory — slide 034 render_6 vs unique_slides/slide_034.jpg
Worker w034-finish-20261024, 2026-10-24. Frame px, 1px=1pt; render 2001x1125 @150dpi
(sx=2.084375, sy=2.083333). All deltas measured on BOTH images with clean interior
windows (no border/text contamination, >=3 ink px to count).

## VERIFIED-CORRECT (no action)
- Build currency: pptx md5 b2c49258; rebuild from build/slide_034_attempt6.js
  (== build/slide_034.js, md5 210f6e9a) gives 40/41 identical zip entries (only
  docProps/core.xml timestamp differs). render_6 md5 71c03bfa == render_5.
- House chrome PASS (shared_patterns/house_chrome_check.py): panel x112-1882
  y94-bottom; L/R/bottom strokes present, top bare; badge (1824,152) d=68.
- Selfcheck PASS (selfcheck_attempt_6_output.txt): above-panel ink 0 px;
  144/144 table values; 7/7 dataset invariants; analytic curve residual
  median 0.27 px / p95 0.95 px / 96.94% within 2 px.
- crop_6 pairs are CURRENT (byte-identical to regeneration from render_6) and
  matched-scale: table 1694x442, plot 529x565 @ 2.083 px/frame-px both sides.
- Payloads BYTE-EXACT vs shared_patterns/judge_protocol_03.md:
  Template A 4115 chars md5 9387f5fbb9 (BLOCKER x4, 1 FINAL VERDICT);
  Template B 1914 chars md5 305bf380dfd (BLOCKER x2, 1 FINAL VERDICT).
- Ink extents: original full ink x58-901 y46-539; render x58.1-901.0
  y46.1-538.6 (agreement 0.2 frame px). Above-panel ink = 0 in both.
- Title block: O x195-434 y66-83 | R x191.4-436.6 y67.7-85.0 (dx ±3.6, dy ±2).

## REAL DEFECTS measured against the ORIGINAL (build would need fixes)
### D1 — table band fill colours (the banked crop_3 FAIL's non-cited aspect)
Band fill medians measured on the exact judge crop files (crop_6_*_orig/render.png):
  row        ORIGINAL          RENDER            dE
  x          #D7E278 (olive)   #AFEEEE (cyan)   125.0
  f(x)       #D7E27C (olive)   #FFFFFF (white)  139.4
  x-delta    #D4B1F4 (violet)  #FFFACD (yellow)  92.9
  f(x-delta) #D5B2F6 (violet)  #FFFACD (yellow)  92.9
  x+delta    #F5DDC1 (tan)     #FFFACD (yellow)  32.9
  f(x+delta) #F5DDC3 (tan)     #FFFACD (yellow)  31.4
  slope      #DEAB92 (salmon)  #FFB6C1 (pink)    57.5
  next x     #F7BEC2 (pink)    #98FB98 (green)  119.7
The original's palette is within dE<=4 of the CERTIFIED sibling slide_033's
build band palette (D9E275 / D6B2F5 / F7DDC2 / DEAC95 / F7BEC4) — slide_033's
render is certified PASS with exactly those fills. The build here instead
consumed the analysis-JSON colour list (AFEEEE/FFFFFF/FFFACD/FFB6C1/98FB98),
which the frame does NOT support. slide_033's own analysis JSON is likewise
wrong (E2EFDA/DDEBF7/E4DFEC/FCE4D6) yet its worker used the frame's values.

### D2 — table band structure / row geometry
ORIGINAL bands (full-width dark lines): y320/321 top, 331, 359/360, 367,
373/374, 409/410, 416/418, 453/454, 459/461, 477/478, 483/485, 501/503,
517 bottom — i.e. 5 banded groups (x+f(x) / x-d+f(x-d) / x+d+f(x+d) / slope /
next x) separated by WHITE gaps (e.g. y370-372 has ink only at x667,789).
Each 2-row band also has an inner white separator (y350, 392.5, 436 in 033).
RENDER bands: y320.9, 345.4, 369.8, 394.3, 418.8, 443.3, 467.8, 492.2 —
8 EVEN rows at 24.48px, NO gaps, and **no bottom border after the 8th row**
(rows 493-516 are all panel-interior #FFFFFF with zero gridline; the original
has a full-width line at 517). Row-y drift grows down the table (rows 7-8 sit
~+9..+12 px vs the original's measured row centres 340/358/382/401/426/445/467/491).
The render's uniform addTable(rowH 24.5px) cannot express the original's
banded structure; slide_033's certified build builds the table from explicit
rects + XSEP lines + per-row text (see its BANDS/XSEP/row_ys pattern).

### D3 — missing cyan/green insert
ORIGINAL: bright-green insert (#88F3AB core, interior sampled #8BF8AB) over
band1 cols 13-15, measured x669..789 y332..368 (3781 px, of which 3702 px lie
in y332..368). slide_033 builds the identical insert as a rect at
(x666,y332,w121,h36) fill 8BF8AB with an 8B0000 dashed border. RENDER: absent
(the build paints only green #90EE90 cell fills on the f(x) row).

### D4 — plot curve colour
The curve traced by blue-excess is BLUE in the render (#0000F0-ish, asset
saturated hue (0,0,240) n=25584). The original's curve is TEAL: at the
render's own 856 blue-curve positions, the original's most-saturated pixel in
a 7x7 window is (101,184,188) with chroma>45 in 400 of 856 positions, and
369/400 of those classify teal (g>r+10, b>r+10, |g-b|<25) vs 0 blue-ish
(control 36px right = (252,254,251) white). 456 positions have no saturated
ink in the original (its curve is thinner/lighter) but zero positions gave blue.

### D5 — plot box border colour
ORIGINAL plot box borders (measurement box x607..845 y58..313): the border ink
is RED — top most-saturated px (159,1,24) chroma 158; left 244 px / right 244 px
red-mask; the red full-width line at y62 and red vertical at x607 continue down.
RENDER draws the plot box with a black 1pt border (build: line 000000) and the
white backing rect; measured darkest px on all four edges is (0,0,0).
=> D4 and D5 both indicate the graph asset's stroke colours differ from the
original (asset generated with blue curve + black box).

## NOT defects (explicitly)
- Explanatory text: original line 1 holds TWO red "8" glyphs (x413-432 and
  x569-587, red rows 260-270) and ends in "8" — identical content to the render,
  merely a larger font (frame glyph advance ~11.8 px vs render ~7.3 px).
- Table column separators: the original has ~34 isolated dark columns inside
  each band but they are glyph ink, not a drawn grid (the 033-style XSEP white
  separator model is what reproduces them).
- Badge, panel, strokes, title, equation box, and the 8 table rows' TEXT are
  all within TOL; the banked selfcheck's 144/144 values and 7/7 invariants hold.

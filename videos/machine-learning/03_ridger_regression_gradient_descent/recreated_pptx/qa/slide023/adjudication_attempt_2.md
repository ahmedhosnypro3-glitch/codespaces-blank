# Adjudications — slide 023 crop-pair eq_zoom (attempt 1, render_1)

All adjudications are PIL-first against BOTH images. Original frame
`unique_slides/slide_023.jpg` (960x540, 1px=1pt); render `render_1.png`
(2001x1125, 2.0833 render-px per frame-px).

## R1 MAJOR — "missing underline on the final vector Y"  => CONFIRMED, FIXED

Crop `crop_2_eq_zoom_*` (matched scale), Y region = rightmost 40px of ink:

| image | Y glyph body | underline bar under Y |
|---|---|---|
| ORIGINAL | rows 32..76, max 25px wide | **rows 78..82, 40-41px wide** |
| RENDER_1 (old) | rows 31..80, max 7px (Y stem) | **none** |

Root cause: `build/assets/eq_023_main.json` mathtext was
`\underline{W} = \left( X^T X + \lambda I \right)^{-1} X^T Y` — only `W`
carried `\underline`, although both the banked builder
(`qa/slide023/build_eq_023_ws.py`) and `build/slide_023.js` document "BOTH the
W and the Y carry an underline bar" per the measured frame (Y underline bar
y180..181 x410..429).

FIX: MATHTEXT and PHANTOMED now end `X^T \underline{Y}`; asset rebuilt
(identical 2712x334 geometry, baseline_px 259 — only the bar added);
`slide_023_recreated.pptx` rebuilt; re-rendered as `render_2.png`.

Post-fix pixel proof (`crop_2_eq_zoom_render.png`): Y-region bar rows 93..96,
37px wide (original has 40-41px). **RESOLVED — re-judge eq_zoom on render_2.**

## R2 MINOR — "glyph weight/typeface mismatch (W, X, Y, parens, +, = lighter)"
=> ACCEPTED MINOR (no build change)

mathtext renders every symbol at ONE weight from a single string at fontsize
32.5pt; no per-symbol weight is available in mathtext. The frame's heavier
weight is the original slide's own font choice. All glyph shapes, positions,
colours and the enclosure geometry measure correct. A weight-only residual.

## R3 MINOR — "delimiter and operator stroke weight lighter"
=> ACCEPTED MINOR (same grounds as R2; weight-only, enclosure geometry correct)

---

## S1 MINOR — "(X^T X) is underlined (mean-adjusted X) in the original"
=> **REFUTED** (pixel-proof)

The parenthetical's ink is x505..560, glyph tips ending at y215 (`(` x507..508,
X x512..526, `)` x557..560). An underline would be a continuous run spanning the
~55px parenthetical width at ~y216..217.

Row-by-row runs, ORIGINAL, x450..800:
  y212: (506,507) (512,526) (559,560)
  y213: (506,507) (512,526) (558,560)
  y214: (507,508) (558,559)
  y215: (507,508) (557,559)      <- final glyph tips, 1-3px wide each
  y216: (none in x450..800)      <- EMPTY
  y217: (none in x450..800)      <- EMPTY
  y218: (450,755)                <- green box bottom border, 306px
  y229: (450,799)                <- blue box top border, 350px

Automated scan for any run spanning >=55% of the parenthetical width, both
images, rows y192..237:
  ORIGINAL : y218 (55px), y219 (55px), y229 (55px)   <- the two box borders
  RENDER_2 : y218 (115 render-px = 55 frame-px), y228 (115)  <- same two borders

Both bars sit at IDENTICAL frame rows in both images and both extend across the
full box width (they are box borders, not underlines). Rows y216..y217 — the
only place an underline could sit — are empty in BOTH images.

CONCLUSION: the original's `(X^T X)` is NOT underlined. At full-slide 150dpi the
green-box bottom stroke (y218.5) sits 3px below the glyph tips (y215) and reads
as an underline. The render reproduces the same geometry. **No build change.**

## S2 MINOR — "Matrix inversion is highlighted red/bold in the Solution line"
=> **REFUTED** (pixel-proof)

Solution-box interior measured x92..868, y439..526 (box strokes x87..874 /
y435..530 excluded):

  ORIGINAL red ink px in the interior = **0**
  Control band (EX lines, known red numerals 1000 / 1,000,000,000):
      red ink px = 1710   (the detector works)

A wider band (y430..532) returns 1292 "red" px, but their mean colour is
(115.1, 96.1, 53.9) — the warm brown box border (measured border core
(107,86,46)), which trips the saturation predicate. Interior-only = 0.

CONCLUSION: no red ink anywhere inside the solution box. The render carries no
red there either (it is uniformly navy 000080). **No build change.**

## SUMMARY
  R1 Y underline  : CONFIRMED MAJOR -> FIXED (see fix_record_underline_Y.md)
  R2 glyph weight  : ACCEPTED MINOR
  R3 stroke weight : ACCEPTED MINOR
  S1 (X^T X) line  : REFUTED (rows 216-217 empty in BOTH; bars are box borders)
  S2 red "Matrix inversion" : REFUTED (0 red px in the solution-box interior)

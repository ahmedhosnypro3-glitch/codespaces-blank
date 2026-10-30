# Fix record — crop-pair eq_zoom MAJOR (missing underline on Y)

## Claim (crop-pair judge, eq_zoom, attempt 3)
"Missing underline on the final vector `Y`. In the original the closing `Y`
clearly carries an underline, matching the underlined `W` vector notation. In
the recreation the identical `Y` has no underline." — MAJOR, high confidence.

## Pixel proof (before fix)
Measured in the banked `crop_1_eq_zoom_*` pairs at matched scale:

| image | Y glyph body | underline bar under Y |
|---|---|---|
| ORIG | rows 32..76 (max 25px wide) | **rows 78..82, 40-41px wide** |
| RENDER (old) | rows 31..80 (max 7px in the Y stem band) | **none** |

A 5-row / 40px-wide horizontal bar directly under the `Y` exists in the original
and was entirely absent from the render. Not a low-res artifact.

## Root cause
`build/assets/eq_023_main.json` mathtext was
`\underline{W} = \left( X^T X + \lambda I \right)^{-1} X^T Y`
— only the `W` carries `\underline`. The banked builder
(`qa/slide023/build_eq_023_ws.py`) and the pptx build script
(`build/slide_023.js`) both document "BOTH the W and the Y carry an underline
bar" per the measured frame (Y underline bar y180..181 x410..429), so this was
a build defect against the builder's own stated intent.

## Fix
`build_eq_023_ws.py`: `MATHTEXT` and `PHANTOMED` now end `X^T \underline{Y}`.
Re-ran the builder -> new `eq_023_main.png` (2712x334, baseline_px 259 —
byte-identical geometry to the old asset, only the Y underline added).
Re-ran `build/slide_023.js` -> new `slide_023_recreated.pptx`.

## Pixel proof (after fix, new render_2.png)
- render_2 Y-region bar: rows 93..96, 37px wide (matches the orig's 40-41px).
- house_chrome_check render_2: PASS (panel, L/R/B strokes, no top stroke, badge).

## Downstream
- render_2.png IS the new certification render; crop pairs re-cut from it
  (attempt_1 pairs archived as `crop_1_<n>_render_oldrender1.png`).
- Per protocol, BOTH legs re-run from render_2 (Template A + all four crop pairs).

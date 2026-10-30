# PIL REFUTATION — "underline under X in (X^T X)" (two judges raised it)

Claimed by:
- `judge_attempt_2.txt` (full-slide, attempt 2) MINOR #2:
  "IMG2 marks (X^T X) with an underline (mean-adjusted X); IMG1 shows it
  plain-italic without underline."
- `crop_2_recall_eq_judge.txt` (Template B, K=2, recall_eq) **MAJOR**, high conf:
  "The original underlines the X in the annotation (X^T X) — clearly visible at
  least under the first X immediately to the right of ⇒."

## Evidence: character map of the exact band, BOTH images

Original frame (`unique_slides/slide_023.jpg`, 960x540, 1px=1pt) and
`render_2.png` (2001x1125), x-frame 505..562, y-frame 210..222.
Legend: `#` <100, `+` <140, `-` <170, `.` <200, space = local background (green
box fill CEFFE2, mean = 228).

```
ORIGINAL                        RENDER_2
      5678901234567890...             5678901234567890...
 y210: -#      -##+   -###-      y210:   ##   ##-       ##-
 y211: .#.     ..-.   ..--.      y211:    ##
 y212:  --    .-------------.     y212:    ##
 y213:  .+    -+#++##+######-     y213:     ##
 y214:   -.                     y214:      #
 y215:   .-                     y215:
 y216:                          y216:
 y217:                          y217:
 y218: ++++++++++++++++++++     y218: ++++++++++++++++++++
 y219: ++++++++++++++++++++     y219:
 y220:                          y220:
```

## Reading

1. The `(` (`X` `)` parenthetical's glyph ink terminates at y215 in the original
   and y214 in the render.
2. **Rows y216 and y217 are entirely empty in the ORIGINAL** (every px at the
   228 background level), and y215..y217 are empty in the render.
3. The only continuous full-width bar is at y218 (both images) — the green
   recall box's own bottom border (measured B y218.5, spanning x97..754). The
   original's stroke bleeds to 2px (y218-219) under JPEG; the render's is 1px.
4. An underline under the `X` would be a `###`/`+++` run spanning x512..526 at
   y215/y216/y217. It exists in NEITHER image.

## Conclusion

The original's `(X^T X)` is NOT underlined. What both judges read as an
underline is the green-box bottom border, which sits 3px below the X's tips —
the X is the tallest glyph on its line, so the box edge reads directly beneath
it at full-slide zoom. The render reproduces the same geometry (box border at
the same y218, glyph tips 3-4px above it).

**REFUTED. No build change.** (Banked per judging.md; this is the PIL
adjudication record for the recall_eq crop-pair MAJOR and the full-slide
attempt-2 MINOR #2.)

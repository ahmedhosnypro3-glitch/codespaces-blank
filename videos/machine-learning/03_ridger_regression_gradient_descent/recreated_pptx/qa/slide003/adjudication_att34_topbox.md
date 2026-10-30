# PIL adjudication — slide 003, crop_34_topbox FAIL (attempt 34, banked 2026-10-25 18:37)

Judge finding (crop_34_topbox_judge.txt): MAJOR — the yellow/cyan/magenta bands use
straight vertical bars as delimiters in IMG1 (render) while IMG2 (original) uses
curved parentheses; internally inconsistent with the render's own midcol, which
correctly uses curved parens. Plus 2 MINORs (y-label subscript overflow; y_n shade).

## Verdict: MAJOR CONFIRMED in substance (shape class), judge's "hooks" detail unconfirmed.
Two NEW geometry deltas found that the judge missed; one prior banked fix superseded.

### Evidence (pil_adjud_att34_topbox{,2,3,4}.py + ASCII maps, frame scale 1px=1pt)

1. **Shape (the MAJOR).** Per-row ink-centroid profiles of all six band delimiters in
   the ORIGINAL bow 1.0–1.5px in the paren-correct direction (yellowL convex-left
   298.0→296.5→298.0; yellowR convex-right 330.0→331.5→330.0; cyanR 408.0→409.0→408.0;
   pinkL 519.5→517.5→518.6; pinkR 550.6→552.5→551.6; midcol 452→451→452 / 474→475→474).
   The RENDER control (render_34.png, same probe): spread 0.0 — the drawn lines are
   dead straight. At the crop's ~2.08x effective scale the sagitta difference is
   plainly visible; the judge's perception is pixel-grounded. The original's glyphs
   are shallow parens, not bars. "Outward hooks": no horizontal tails at slide scale
   (ASCII maps) — detail unconfirmed, shape-class claim stands. The internal
   inconsistency is real and confirmed in build code (col_delims = 6 line shapes;
   midcol = arc PNGs).
2. **NEW: cyanR x-position.** Original core at x=409 (run72 y168..239 @th200; x408
   run30; NOTHING at 414 — max run 4 in x395..425). Build draws 414.5. att31's
   "right-side bars x331/x414/x556" mis-measured 414/556 (threshold/grouping); the
   band rhythm (35px bands, 42px gaps: 296.5/331.5 | 373.5/409 | 451/475 | 517.5/552.5)
   confirms 409. → build cyanR 5.5px right of original.
3. **NEW: pinkR x-position.** Original core x=552–553 (552 run96, 553 run71; nothing
   at 556). Build draws 556.5 → 4px right of original.
4. **SUPERSEDED: att31 pink bar-span fix (y142..291 "through the red y row").**
   Threshold sweep: th210 (clean; th230+ is polluted by the fills themselves — yellow
   FFFF99 avg 221, pink F0A0F0 avg 213 are "dark" at th230) gives ALL six band
   delimiters y≈146..263 (~117 rows) and midcol y150..258. The pink delimiters do NOT
   pass through the red y-label row; the y141..296 extent att31 measured is the band
   FILL, not the strokes. Pink delims corrected 142..291 → 146..263 (and cols 1-2
   157..252 → 146..263, taller than the build's current 95 rows).
5. **MINOR refutations.** (a) "y-label subscripts descend to/below the band edge":
   original y-labels y277..293 vs fill bottom y296 — fully inside (ASCII x280..570
   y262..304). REFUTED. (b) "y_n darker/maroon": small red text on colored fill is
   JPEG-desaturated in the original (judge itself graded low confidence, capture
   shift). NOT a fix trigger.

## Fix (one fix-loop cycle)

Replace the 6 straight col_delims line shapes with generated arc PNGs — same
mechanism/style as the judge-certified midcol arcs (600dpi RGBA, w 3.8pt, bow per
the midcol design, per-column ink colors sampled from the original stroke cores so
the faint on-fill weight matches):
- geometry: bulge cores at x = {296.5, 331.5, 373.5, 409, 517.5, 552.5}
  (L arcs: PNG left edge = core; R arcs: PNG right edge = core), all y146..263.
- midcol arcs UNTOUCHED (att34-certified as matching).
- everything else in the topbox unchanged (content audit in crop_34_topbox_judge.txt:
  all entries/headers/labels verified correct).

## Post-fix re-judge plan

legA full-slide re-run on render_35 (build changed) + legB topbox on crop_35 pair.
matrix/sideboxes/bottomright att34 PASS certificates remain valid iff a pixel-diff
of render_34 vs render_35 is ZERO outside the topbox rect (x266..600, y105..305) —
those crops do not include the topbox.

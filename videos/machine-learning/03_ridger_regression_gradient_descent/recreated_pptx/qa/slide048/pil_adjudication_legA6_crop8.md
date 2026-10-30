# PIL adjudication — slide 048 crop_8_top_band judge (render_8) + leg A attempt 6

## crop_8_top_band (FINAL VERDICT FAIL → items 1/2 refuted, 3/5 fixed, 4 refuted)

1. BLOCKER "W vector garbled: bars + x row labels, placed LEFT of 'Initial W ='" —
   REFUTED (third repeat of the same misread). Frame-pixel maps of BOTH original
   and render (pil_adjudication_crop5_top_band.md §5) show the identical
   structure in both: label band rows 61-74 at cols 366+, stacked vector hanging
   below-left at cols ~330-355, rows 78-102. The vector is the mathtext asset
   eq_initial_w_col.png (stacked [4;-2;-2] in square brackets), matching the
   original's own linear form "Initial W = [4; -2; -2]" (analysis JSON). The
   "x row labels" are the bracket strokes + sub-pixel glyph fragments at crop
   scale; no x/k glyph exists in any mathtext source (gen_assets_048.py).
2. "Z-grid enclosing parentheses missing entirely" — REFUTED (third repeat).
   Tall-stroke census over rows 84-120 shows delimiter strokes in BOTH images:
   orig at cols 641/647-651/655-656/664-665/669-670/678/686-687/695/700;
   render_8 at 644-650/667-672/693-694. The render's curved strokes were also
   ASCII-mapped earlier (pil_adjudication_crop5_top_band.md §2).
3. MINOR "REPEAT not underlined" — REAL (orig underline stroke rows 70-71,
   cols 420-535 window). FIXED: underline added (render_9).
4. MINOR legend typography: (a) C1/C2 without subscripts — MINOR, accepted
   (typed medium); (b) "comma inserted" — REFUTED (orig descender blobs at
   cols ~323-327/357-363 prove commas); (c) "negative blue" — REFUTED (orig
   legend blue census confined to cols 311-326 = the C2 token only);
   (d) italic legend — MINOR, accepted.
5. MINOR "W underlined" — REAL (orig underline band rows 71-72 cols 366-430).
   FIXED: underline added to "Initial W =" (render_9).
6. MINOR Z-header subscripts — low confidence self-flagged; Z1 Z2 Z3 confirmed
   by analysis JSON + attempt-4 judge. No action.

## leg A attempt 6 (render_6)

1. "Stray x/k glyphs in every vector" — REFUTED (recurring misread; mathtext
   sources contain no x/k; content pixels identical to the attempt-4-PASSed
   render except the intended changes).
2. "'Top)' clipped at panel edge" — REFUTED: label ink ends at col 208
   (fontSize 11 fix), panel border at 246; the earlier 245.2 reading was the
   frame border stroke itself.
3. "C-label strip overlaps header box bottom border" — REAL: LO expanded the
   addTable to ~30px rows, pushing the class row onto the band border.
   FIXED: table replaced with per-cell text boxes at measured positions
   (class row now rows 113-121 vs border 127-129; orig 111-124 vs 128-130).
4. "Missing red ⇐ after row 1" — REFUTED: the orig's red pixels right of box 1
   (cols 900-902, rows 139-196) are a straight VERTICAL border stroke, not an
   arrow glyph; the render has the same stroke. (The analysis JSON's "green ⇐"
   was already refuted by the green census: 0.2 px/col chroma noise.)
5/6. REPEAT italic/underline + vector line spacing — MINOR; underline FIXED
   (render_9), spacing accepted (typed medium).

Conclusion: all findings refuted or fixed; build current at render_9.

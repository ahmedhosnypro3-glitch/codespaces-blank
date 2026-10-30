# PIL adjudication — slide 048 crop_5_top_band judge (attempt 5, render_5)

Findings, PIL-adjudicated against render_5/render_6 and the original frame:

1. "Z1 Z2 Z3 wrong; original has three Z₁" — REFUTED. The original's own verbatim
   analysis (analysis/slide_048_final.json labels) reads Z1, Z2, Z3; the
   attempt-4 crop judge read the same three distinct headers in IMG2. Two
   independent readings vs one.
2. "Z-grid column-vector parentheses missing" — REFUTED. Render pixel map
   (cols 636-706) shows tall curved delimiter strokes spanning both stacked
   rows in all three columns (tall runs at cols ~645/652, 674, 693/697; arc
   rows 87-97 and 103-112). Same structure as the original's strokes at
   cols 641/664/678/687/700.
3. "W-vector delimiters garbled (vertical rule + x marks)" — REFUTED. The
   Initial-W vector is the mathtext asset eq_initial_w_col.png
   (`\substack`-style stacked [4;-2;-2] with square brackets), per the
   analysis JSON's own linear form "Initial W = [4; -2; -2]". Bracket style
   matches the original's square brackets (established in the aug_iter crop
   adjudication).
4. "W vector positioned BEFORE 'Initial W ='" — REFUTED. Frame-pixel maps of
   BOTH original and render show the identical structure: label band rows
   61-74 at cols 366+, vector hanging below-left at cols ~330-355, rows
   78-102. The judge misread the original's own layout.
5. "C2 class labels red instead of blue" — REAL. Orig census rows 111-125:
   C2 cells have 37 blue px (core 31,22,85), 0 red. FIXED in build (C2 cells
   and legend C2 recolored to 1F1655); render_6 census: class row red 735 /
   blue 725, legend red 304 / blue 305.
6. "Legend C2 red instead of blue" — REAL. Orig legend rows 108-126 has 72
   blue px (cols 311-326 = the C2 token). FIXED (same commit).
7. "REPEAT red; original black" — REFUTED. Orig REPEAT word cols 426-470 has
   334 red px — REPEAT IS red in the original.
8. "Commas inserted into legend" — REFUTED. Orig legend ASCII shows two
   descender blobs (rows 121-124 at cols ~323-327 and ~357-363) = commas after
   "positive" and "negative".
9. "Left-table parens per-value, not column-spanning" — REFUTED. Render paren
   strokes span rows ~79-104 (one pair per column, 6 pairs = 12 strokes,
   matching the original's pairs at (90,102)...(201,215) rows 80-102).
10. "Check classes of: italic sans, smaller, offset" — MINOR, accepted
    (typed-vs-handwritten medium difference; position matched to measured
    bbox rows 86-96 / cols 542-626).
11. Typeface substitution — MINOR per ground rule (c).
12. Band border weight/colour — MINOR, chrome-level.

Conclusion: two real color defects (C2 blue) — FIXED and re-rendered as
render_6; all other findings refuted or accepted-MINOR.

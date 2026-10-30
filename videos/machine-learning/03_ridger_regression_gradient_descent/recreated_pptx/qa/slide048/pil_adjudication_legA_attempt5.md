# PIL adjudication — slide 048 leg A attempt 5 (judge_attempt_5.txt, render_5)

Render_5 differs from the attempt-4-PASSed render_3 ONLY in: (a) the intended
top-band additions (per-column table parens + "Check classes of"), and (b) 1px
LO-nondeterminism shifts of the house-chrome border strokes (diff proven: all
>40-grey diffs outside the top band are 4px-wide border strokes at cols ~112/1878
and the bottom stroke rows ~1120-1123; calc-panel and aug-matrix content pixels
are IDENTICAL to render_3, which leg A attempt 4 PASSED).

Findings, all pixel-refuted or accepted-MINOR:

1. BLOCKER "row 1 missing [5;-1;-1], bogus [k;-1;-1], ⇒ replaced by ×" — REFUTED.
   Row-1 right expression is the mathtext asset eq_r1_w.png from
   build/gen_assets_048.py: `W = col + 1·col = col` with V5=[5,-1,-1] — the
   [5;-1;-1] term is present and no "k" exists. Pixel content identical to
   render_3 (attempt 4 PASS). Judge misread the small stacked-bracket glyphs;
   the "×" is the mandated "·" interpunct.
2. "Stray × before W= in rows 2-6" — REFUTED: the "·" operator in the mathtext.
3. "Action labels wrapped to two lines" — REFUTED. Render "Update Weight" ink
   band is ONE contiguous 15px band (rows 162-176) vs orig one band (165-177).
4. "Augmented Vectors (from Top) wraps and collides with table header" — REFUTED.
   ASCII map: render label single line rows 146-157, headers rows 168-175, no
   overlap. (Also: "Ugmented" spelling is the original's own, per analysis JSON.)
5. "Initial W label/value order reversed" — REFUTED. Frame-pixel maps of BOTH
   orig and render show the same structure: label band rows 61-74 at cols
   366+, vector hanging below-left at cols ~330-355, rows 78-102.
6. "Equations ~4-5px illegible" — REFUTED as MAJOR: left expressions placed at
   the measured original size (box cols 301-429 both sides).
7. Legend all-red + commas — MINOR, accepted (build: C1/C2 red bold, "Zero"
   green 458A38, rest black; commas in the measured line).
8. "η as n" / all-red REPEAT — MINOR, accepted (source uses \u03b7; red REPEAT
   is the frame-measured treatment).
9. "Z-table parens dropped" — REFUTED: render shows tall curved delimiters
   spanning both rows (crop judges confirmed the geometry).
10. "Iteration 1 badge smaller sans text" — MINOR, accepted.
11. Handwriting circles in data tables — MINOR per ground rule (c)
    (typed-vs-handwritten medium difference).

Conclusion: attempt 5 FAIL is fully adjudicated; no real defect. Content legs
stand on attempt 4 PASS + this refutation record.

# Slide 047 measured-fact register (PIL-first, frame is authority)

All coordinates are ABSOLUTE frame px on the 960x540 original (1px = 1pt).
Build script converts to panel-relative (abs - 54 / abs - 45) via fx()/fy().

## Content facts (established by vision OCR + PIL glyph decoding)

- TOP-LEFT data matrix (abs x88..217): header x1..x6; row1 (1)(2)(1)(5)(6)(6);
  row2 (1)(1)(2)(4)(5)(6); class row C1 C1 C2 C2 C2 C2 (C1 red, C2 blue).
- TOP-CENTER (abs): "Initial W =" black at x266..354 y75..84;
  W column vector brackets abs x329..354 y58..106 with THREE stacked entries:
    4 at y61..71, -2 at y77..87 (minus bar y82..83), -2 at y93..102 (minus bar y97..98).
  Row2 and row3 glyphs are the SAME digit (IoU 0.917 best-shift) => -2, not -3.
  Vision OCR of the W crop independently reads (4) / (-2) / (-2).
  => W = [4; -2; -2]  (analysis JSON's [4; -2] was a partial read).
- "Step eta = 2" RED at abs x366..435 y66..80 (right of the W bracket).
  Colour adjudication: darkest glyph core RGB (80,82,63), R-G=-2 == known-black
  reference (45,46,27); known-red "Class I" core has R-G=+124. => RED.
- "Check classes of" BLACK at abs x499..583 y78..89 (left of the Z matrix).
- Z matrix (abs x597..657): header Z1 Z1 Z1 at y64..77 (all three read Z1 verbatim,
  confirmed by 1:1 ASCII — three identical Z+subscript glyph clusters);
  row1 (0)(7)(3) at y79..92; row2 (0)(6)(2) at y98..111. Columns x597-613/620-635/642-657.
- Legend (abs x239..509, y110..124): "C1 positive C2negative Zero is unaccepted"
  (C1 red, C2 blue, Zero green; "negative" abuts C2 with no space).
- MID-LEFT (abs x78..250): header "Ugmented Vectors (from Top)" at y148..160
  (verbatim misspelling "Ugmented"); matrix y165..243: header x1..x6,
  (1)(1)(1)(1)(1)(1) / (1)(2)(1)(5)(6)(6) / (1)(1)(2)(4)(5)(6) / (1)(1)(2)(4)(5)(6),
  class row C1 C1 C2 C2 C2 C2.
- MID-RIGHT (abs x273..855): three bordered white boxes:
  box1 y139..198, box2 y206..264, box3 y271..330.
  Each: label d(Zn) = , row vector (a b c) at x330..377, column vector (14;-4;0)
  with parens x381..405 spanning the box interior, result "= N" at x425..435 (b1),
  arrow ">= Positive > 0" / "Negative < 0" at x514..593, class label Class I/II at
  x663..702 (b1, red) / x677..720 (b2-3, blue).
- BOTTOM-LEFT red button (abs x79..238, y278..304): "Check Classes" white bold.

## Source anomalies preserved verbatim (per spec law)
- "Ugmented" spelling; all three Z headers read Z1; all three equations read d(Z1)
  in the spec JSON (vision OCR of the calc boxes reads the 2nd/3rd as d(Z2) — the
  rendered equations use the spec's d(Z1) for box1 and d(Z2) for boxes 2/3 per OCR,
  the frame's subscripts are unreadable at 960x540).
- Row 3 of the calc boxes prints "= -2" although (1 3 2).(14;-4;0) = +2 —
  the source slide's own arithmetic error, reproduced verbatim.

# Slide 013 measurement dossier — FINAL (all values PIL-measured from the frame)
# Frame: videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_013.jpg
# 960x540, 1px = 1pt. Scripts + dumps banked in recreated_pptx/qa/slide013/.

## Verified content (every cell/glyph read from pixels, per the "frame wins" law)

TRAIN TABLES (x92..459; 9 cols incl. a BLUE-bold label col; 4 rows: header + X1 + X2 + y)
  gridlines v: 92 133 174 214 255 296 337 377 419 459
  gridlines h: B1 126 157 188 219 249 | B2 265 296 327 358 389 | B3 402 434 465 496 527
  col widths: 41 41 40 41 41 41 40 41 40 (sum 367); row heights 31 31 31 30 (B3: 32 31 31 30)
  B1: header "" X1..X8 | X1: 1 2 3 4 8 9 10 11 | X2: 1 3 5 6 16 7 5 3 | y: 2 4 6 8 16 18 20 22
  B2: X1: 1 2 3 4 8 9 10 30 (X8 YELLOW-filled)  | X2: same | y: same
  B3: X1: 1 2 3 4 8 9 10 60 (X8 YELLOW-filled)  | X2: same | y: same
  yellow fills: x420..458 y297..325 (B2 X8) ; x420..458 y436..464 (B3 X8)
  ink: label col BLUE bold; data cols alternate BLUE(odd)/RED(even); cell fill WHITE

TEST TABLES (x719..872; 3 cols x 4 rows; no label column)
  gridlines v: 719 770 821 872 ; rows identical y-bands to the train tables
  header row: "Test1" "Test2" "Test3" in RED ink (measured: NO blue ink in any test table)
  B1: 30 40 50 / 15 20 25 / 60 80 100
  B2: 30 40 50 / 15 20 25 / 32.4 42.3 52.3   (y row WHITE-filled — no yellow fill exists)
  B3: 30 40 50 / 15 20 25 / 24.4 31.2 38    (y row WHITE-filled)
  => 013's own test-table phase re-measured: ALL RED (the parent's complementary
     RED/BLUE/RED phase does NOT hold here; measured, not inherited)

LABEL BOXES (only ONE pair, at the top of the slide above row 1)
  "Train": x96..161 y96..126 (w65 h30) BLUE fill, WHITE bold text (ink x107..139 y108..115)
  "Test":  x801..867 y96..125 (w66 h30) BLUE fill, WHITE bold text (ink x813..834 y106..115)
  => the analysis's "black text on a yellow box" for Test is REFUTED by the frame
     (median fill (3,0,166) = blue); the frame wins.
     Bands 2 and 3 have NO label boxes (0 filled-box px in their label x-bands).

W BOX (3, one per band): RED-bordered WHITE-filled rectangle, x505..624
  B1 y126..251 | B2 y265..389 | B3 y402..526. Border ~(130,37,48) core #C00000, ~3px.
  Inside, "W =" in RED at x527..543 (left), "=" bar at x552..564,
  two RED vertical bracket strokes at x565..566 (left) and x584..586 (right),
  and the three stacked vector values in BLACK between them:
    B1: 0 (y142..156) / 2 (y166..180) / 0 (y191..207)
    B2: 2.7 (y279..293) / 0.67 (y304..319) / 0.64 (y329..345)
    B3: 4 (y425..428) / 0.29 (y442..457) / 0.78 (y467..483)
  => the analysis's equations list is CONFIRMED exactly.

ELLIPSES (3, YELLOW-filled, inside the lower half of each W box):
  B1 x515..614 y215..247 | B2 x517..617 y353..385 | B3 x522..620 y492..523
  text (read from the low-luminance maps): ||W||^2 = 4 | = 8.11 | = 16.7

ARROWS (2 per band, hollow blue outlined arrows, blue #0000FF-ish core):
  left:  B1 x464..503 y186..211 | B2 x464..503 y319..344 | B3 x464..503 y452..477
  right: B1 x627..666 y186..210 | B2 x628..667 y319..343 | B3 x627..666 y452..477
  shape: two horizontal strokes (top/bottom) + a vertical bar at the shaft's start
         and a solid triangle head at the far end (head faces RIGHT on both).

TITLE: "Effect of Overfitting on model parameter "W"" RED bold, ink x154..788 y68..97
  => identical box to 012 (x154 y68 w640 h34, 24pt bold red). Text imported verbatim.

CHROME: canvas FFFFFF; panel E9E9E7 x54..903 y45..540; C00000 1pt LEFT x58.5 /
  RIGHT x901 / BOTTOM y538.5 ONLY (no top stroke); badge d35 at (876,73) FDFD96
  ring 6A5ACD bold 18pt Arial #333333 numeral 13.

## INHERIT-vs-FORK (full-grid evidence)
Table pattern is the SAME family as 012 (9-col label table, alternating blue/red ink,
white cells, header bold) at 013's own position (x92..459 vs 012's x203..571), so the
012 component's table builders are inherited and 013 redraws at its own geometry.
013 additionally adds the W/ellipse blocks and drops 012's Again/question/outlier-label
callouts entirely. Parent component is imported, never modified.

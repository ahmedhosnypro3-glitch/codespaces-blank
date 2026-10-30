# PIL ADDENDUM to pil_adjudication_049h.txt — result digits + geometry corrections

Supersedes two claims of the 049h adjudication (2026-10-25 19:46) after direct
pixel measurement in the 22:00–23:00 window. Evidence banked under project
`scratch/s7_049_*.txt` (ascii/overlay/refs/legend tokens/redbox rows). The
rebuild (`build/slide_049.js`) implements THIS addendum.

## A1 — Results column is 3 / 2 / 2 / −4 / −6 / −7 (049h's "+3,+3,+3" was WRONG)

The 049h F2 measurement wrote "rows 1-3 `+3` (plus bar x404..417 ...)" and the
REBUILD TARGETS line carried `results (+3,+3,+3,−4,−6,−7)`. Direct re-measure of
`unique_slides/slide_049.jpg` at the result positions (window x414..432,
rows y158..178 / 225..245 / 291..311 — `s7_049_resultdigits_ascii.txt`) shows a
SINGLE digit per row, no plus bar:

- row1: centre-pinch bulge, left ticks at y165/167/168, curved bottom
  (`...##.##....` / `....###.....`) — topology of "3" (matches the Z-grid's
  known "3", `s7_049_resultdigits_refs.txt`).
- row2 / row3: flat wide bottom bar (`...###......` / `...######...`) — "2".
- The "plus bar x404..417" in 049h was the bracket right-stroke tip + "="
  residue at the window edge, not a plus glyph (no + pixels inside x414..432).
- Math cross-check: [1,a,b]·(5,−1,−1) = 5−a−b → 3,2,2,−4,−6,−7. A "+3" result
  for row2 would need 5−2−1=2 → contradiction. The dot product settles it.

An earlier handoff note's "2,2,2" was also wrong (row1 is a 3, not a 2 — row1
has the pinch + left ticks a "2" never has). Template matching
(`s7_049_digitid.py`) was inconclusive at this glyph size; the ASCII topology +
arithmetic read is decisive. BUILD: `results = ["3","2","2","−4","−6","−7"]`,
rows 1–3 boxed x419 w12, rows 4–6 x420 w24 (minus inside the box).

## A2 — Red Iteration box is x84..213 y278..304 (NOT extended to y394)

Red row census (`s7_049_redbox_rows.txt`): solid red rows 278..304 (h=27,
2548 red px, x-extent 86..213). Rows 376/378..389/393 hold only 3–129 red px at
x87..122 — those are the red "Stop" glyphs, a separate element. The prior
handoff's "extend the box to y394" merged box + Stop text. BUILD: rect
x84 y278 w129 h26, white bold 21pt "Iteration 2" centred.

## A3 — Legend: NO commas, 13.5pt, runs confirmed

Frame descender census at the token gaps (x~305, x~381): no comma descenders;
the low marks after C1/C2 are subscript-style digits of "positive/negative"
context, not punctuation. Token map (`s7_049_legend_tokens.txt`): C1 red
x238..262, C2 navy x306..332; span x239..508 identical to 048's certified
legend. BUILD: one text run group at x239 y108 w300 h17, fontSize 13.5 (not
15), runs C1(FF0000 bold) / " positive " / C2(1F1655 bold) / " negative " /
Zero(5B9C4E bold; frame core 91,156,78) / " is unaccepted". No commas.

## A4 — Top box border is INK 211776, not violet

Border core measured (33,23,117) ≈ 211776 (048's exact top-box geometry:
rect x69 y55 w650 h74, border width 1). The violet 6A5ACD belongs to the AUG
BOX TITLE only ("Ugmented Vectors (from Top)" x80 y146 w158 h15, fs12).

## A5 — Equation PNG sidecar sizes (stale hardcoded sizes fixed)

`build/assets/eq_slide049_wcol.json`: all six wcol PNGs are 175×379 px @600dpi
= 0.29167 × 0.63167 in. The old build's hardcoded 0.34333 in width was stale
(PNG on disk is 175 px wide, not 206). Placed x379 (mid-bracket, wcol_1) and
x721/x733 (W columns, wcol_i), y = band_start+8.
`build/assets/eq_initial_w_col.json`: 192×333 px @600dpi = 0.32 × 0.555 in,
left edge x330, vertically centred at y82 (spans y62..102), label "Initial W"
to its RIGHT (x365.., dark italic underlined, no "=").

## A6 — Calc panel is WHITE-FILLED (old build missed this)

Frame interior census: white region x274..853 y140..528 (interior 254,255,253
vs panel 231,233,230). BUILD: white rect x274 y140 w579 h388 + ABAFBA
horizontal rules at y140, 197/206, 263/272, 329/338, 395/404, 461/470 (double
separators 9px apart), 528 + left vertical x274 y140..514. NO right vertical,
NO y46 line (house law).

## A7 — REPEAT / Initial-W styling on 049

"REPEAT using Step η = 1" red bold fs12, NO italic, NO underline (red census
y72..74 = glyph bottoms only). "Initial W" dark italic + underline (underline
band y72..73 x364..423), no "=".

## Verification status of the rebuild

`build/slide_049.js` (13073 B, 2026-10-25 23:06) → `slide_049_recreated.pptx`
(215705 B, 23:13) → LibreOffice 150dpi render → banked as
`recreated_pptx/qa/slide049/render_10.png`. `house_chrome_check.py`: **PASS**
(panel x112-1882 y94-bottom, strokes L/R/bottom, top bare, badge (1824,152)
d=68). PIL self-check `scratch/s7_049_render10_selfcheck.py`: all structural
checks PASS (white fill + 12 rules + left vertical, no right stroke at x853 —
edge is clean white→panel-gray, red box core (198,2,10) with clean margins,
legend C1<C2<Zero x-order 247<317<398, result ink all 6 rows + minus ink rows
4-6, 6 wcol PNGs inked, Initial-W column + label ink, Z-grid 3×3 ink, red
REPEAT 1963px, 6 red ⇒ glyphs).

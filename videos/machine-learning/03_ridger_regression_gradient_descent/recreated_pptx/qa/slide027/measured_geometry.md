# Slide 027 measured geometry dossier (PIL, original frame 960x540, 1px = 1pt)

Measured 2026-10-19 by worker_zcode_slide027_20261019 from unique_slides/slide_027.jpg.
Authority: the frame (per building.md "frame wins over spec"). Deviations vs spec
JSON are listed at the bottom.

## House chrome (from shared_patterns/house_chrome.js — deck law, not re-measured)
White canvas FFFFFF + gray panel E9E9E7 (x54..903, y45..bottom) + C00000 1pt strokes
left/right/bottom (NO top stroke) + badge FDFD96/purple ring at (876,73) d35,
numeral "27" Arial bold 18pt 333333.

## Title (2 lines, both measured)
- Line 1 "Follow Negative Direction of Gradient with": rows 73..100 (cap band 73..93,
  'g' descender to 100), cols 191..744. Center x = 467.5. 5 word-space gaps confirmed.
- Line 2 "Selected Learning Rate": rows 108..135 ('g' descender to 135), cols 321..621.
  Center x = 471. 2 word-space gaps confirmed.
- Cap height 21px; line1 ink advance 553px; line2 300px.
- Color: dark red, spec-pinned 8B0000 (measured cores ~(163,16,31) = JPEG-shifted dark red).
- Weight/family: glyph shapes show 'l' with tail, 'f' with prominent curl, 4px stems at
  21px cap => Calibri-Bold-like (render test below settles size).

## Graph box (red border rectangle)
- Left edge x193..194, right edge x716, top edge y167, bottom edge y507.
- Border color: spec-pinned FF0000 (measured (135,22,40), brighter than the C00000 house
  strokes at (112,40,51) — brighter-red family, JPEG-darkened).
- No fill (panel gray shows through).

## Axes (black ~2px lines)
- Y-axis: vertical line x222..223, rows 206..436; arrowhead triangle apex (223,206),
  base row 222, base x218..228 (11px wide).
- X-axis: horizontal line y435..437, cols 222..685; arrowhead apex (686,436), base col ~670,
  rows 431..442 (11px tall).
- 'Cost' label: rows 176..189, cols 200..238 — above the y-axis arrowhead, centered on it.
- Axis theta (θ): rows 427..444, cols 697..709 — right of the x-axis arrowhead, ~17px tall.
- Theta-hat (θ̂): body rows 488..504, cols 439..449, hat marks at rows 484..485
  (x440..441 + x447..448) — BELOW the x-axis, beneath the minimum dot.

## Parabola (black curve, both branches meet at vertex)
- Left branch trace (x per y): (253,230) (254,236) (255,242) (256,246) (259,252)
  (262,272) (268,280) (270,286) (272,292) (274,296) (276,300) (278,302) (288,318)
  (290,322) (291,324) (293,326) (294,328) (296,330) (297,332) (299,334) (313,350)
  (316,352) (318,354) (320,356) (322,358) (324,360) (363,386) (365,388) (383,395)
  (400,400) (420,404) (436,406) -> vertex ~ (445,408).
- Right branch trace: (641,236) (640,240) (639,244) (638,248) (637,252) (635,260)
  (632,268) (628,280) (624,288) (619,300) (612,312) (604,324) (595,336) (584,348)
  (571,360) (561,368) (543,380) (525,390) (497,400) (479,404) (463,406) -> vertex.
- Vertex ~ (445, 408) — covered by the yellow dot.

## Blue descent dots (9 total — spec said "approximately 8"; frame wins: NINE)
centers (cx,cy) and measured bbox w×h (incl. JPEG halo):
1. (262.0, 263.5) 13x16
2. (283.0, 310.5) 13x16
3. (306.5, 342.0) 14x15
4. (332.0, 366.5) 15x14
5. (354.5, 380.5) 16x14
6. (374.5, 390.0) 16x15
7. (392.0, 396.5) 17x14
8. (~411, ~403.5) ~16   (merged with 9 in the blue mask)
9. (~426.5, ~403.5) ~15 (col-profile pinch at x417..421 splits the blob)
Color: spec-pinned #0000CD (measured core (61,25,187)).

## Yellow minimum dot
center (444.5, 407), bbox x439..450, y401..413 (d≈12.5). Color #FFFF00 (measured (241,255,16)).

## Dashed leader lines (black, 2px wide, 7px dash / ~7px gap)
- From dot 1 down to the x-axis at x262..263: dashes rows 272..278, 286..292, 300..306,
  314..320, 328..335, 343..348, 357..363, 371..377, 385..391, 400..406, 414..420, 428..434.
- Below the yellow dot at x444..445: dashes rows 415..422 and 430..436 (spec did not
  mention this one — frame wins, DRAW IT).

## Text labels (all black, sans-serif, regular weight per advance metrics)
- 'Cost': rows 176..189, cols 200..238 (cap 14px).
- 'Learning step': rows 272..289 (L cap 272..284, x-height 276..285, g descender to 289),
  cols 297..404. Read glyph-by-glyph: L-e-a-r-n-i-n-g s-t-e-p CONFIRMED.
  NO small arrow exists next to it (spec claimed one; PIL refutes — the 'L' + curve
  fragments were likely misread).
- 'Minimum': rows 364..376 (M cap, i-dot at 364), cols 428..497. M-i-n-i-m-u-m CONFIRMED.
- 'Random': rows 444..457, cols 230..295. R-a-n-d-o-m CONFIRMED.
- 'initial value': rows 466..479, cols 219..306. CONFIRMED (two-line block under the
  dashed line, below the x-axis).
- θ (axis): rows 427..444, cols 697..709, 13x17 — dense stroked glyph.
- θ̂: rows 484..504 (hat 484..485), cols 439..449.

## '+' claim: REFUTED
Spec: "'+' on the x-axis to the right of the dashed line". A full-axis-band vertical-ink
scan (y425..452, x222..690) finds NO plus-shaped crossing other than (a) the dashed
leader meeting the axis at x262..263 and (b) the below-min dash at x444..445. The vision
model likely read one of those crossings as a '+'. No standalone '+' glyph exists.

## Frame-vs-spec deviations (documented per building.md)
1. Dot count: 9 measured, spec says ~8. -> draw 9.
2. '+' label: not present in frame. -> omit (PIL refutation banked here).
3. Small arrow next to 'Learning step': not present in frame. -> omit.
4. Dashed leader below the yellow minimum dot: present in frame, absent from spec. -> draw.
5. Graph box bounds measured x193..716 / y167..507 (spec estimated 15-85% width,
   25-90% height). -> use measured.
6. Title: TWO lines (spec layout said one line top-center). -> use measured 2-line split.
7. Title/background colors: house chrome law overrides spec (#F0F0F0 bg -> white canvas
   + gray panel per deck AGENTS.md).

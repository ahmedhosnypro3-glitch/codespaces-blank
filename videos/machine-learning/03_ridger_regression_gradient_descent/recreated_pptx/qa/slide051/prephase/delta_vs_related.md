# Slide 051 — delta vs certified slide 047 (most-related certified predecessor)

**Why 047:** closest certified composition (gen_status=passed, visual_check=PASS). 047
"Check Classes of Z Vectors" is the SAME decision-table slide family — top cream card with
sample matrix + Initial W + Step η + legend + Z columns, augmented box, red button,
decision rows with blue test row + green weight stack. 051 is the final "Check Classes"
slide with three d(Z) decision rows and an added Undefined-Class row. All coordinates are
frame px (960×540, 1px = 1pt) from the measured headers of `build/slide_047.js`
(certified) and `build/slide_051.js` (current build), to be confirmed against
`orig_judges/` reads.

Legend: **DIFFER** = same element, different geometry/content · **ADD** = 051 only ·
**DELETE** = 047 only · KEEP = unchanged.

## Chrome (house)

| # | Element | 047 (certified) | 051 | Action |
|---|---|---|---|---|
| C1 | Panel + strokes + badge | house values | identical | KEEP |
| C2 | Badge numeral | 47 | **51** | DIFFER (numeral only) |

## Top card (x68..720, y≈54..130)

| # | Element | 047 | 051 | Action |
|---|---|---|---|---|
| K1 | Card container | CREAM #FFFFE8 fill, BLUE 1pt border, x68..720 y55..130 | same box, border NAVY #20186D **2pt**, fill #FEFFE8 | DIFFER (border hue/width — verify `orig_topcard.txt` §1/§6) |
| K2 | Sample matrix | 6 paren-pair columns x88.65..214.65 spanning TWO digit rows (y76.5..108); header x1..x6 y69; rows (1,2,1,5,6,6)/(1,1,2,4,5,6); class row C1 RED/C2 BLUE italic y118.5 | 6 **tall-bracket column** vectors, straight 1px strokes y78..106, digit lines y84/y100; rows (1,2,1,5,6,6)/(1,1,2,4,5,6); class row y110..125 | DIFFER (delimiter shape: parens vs straight brackets; class row italic vs plain) |
| K3 | Initial W | label x266 y78.5, bold underlined W, paren-pair PNG x326 y58 spanning THREE entries 4/−2/−2 (cy 66/82/97.5) | label "Initial W =" x263..321 y74..88 (W italic NOT bold/underlined in build), straight bracket strokes x331/x352 1.5pt y59..106, entries 4/−2/−2 | DIFFER (delimiter + label weight — verify) |
| K4 | Step text | "Step η = 2" RED 17.5pt bold italic x365..447 y67..80 | **"Step η = 1"** RED 12pt x363..438 y66..82 (value 2→1) | DIFFER (value, size) |
| K5 | Legend | 15pt serif: C1 RED / positive / C2 BLUE / negative / Zero GREEN / is unaccepted, x239..519 y110..123 | 11pt Arial, same runs, x240..523 y109..125, Zero italic GREEN_DK #27331A | DIFFER (font family/size — verify) |
| K6 | Check-classes caption | "Check classes of" x499..593 y79..88 12.5pt | "Check classes of" x496..588 y77..91 **bold** 12pt | DIFFER (weight — verify) |
| K7 | Z columns | 3 paren-pair columns x597..658 y79..111, header "Z1 Z1 Z1" (all Z1!), rows (0,7,3)/(0,6,2) reading L-to-R | 3 **tall-bracket** columns x598..656 y80..108, header "Z1 Z2 Z3" (distinct), digit lines y87/y103: (0,0)/(7,6)/(3,2) as COLUMNS | DIFFER (structure + header labels); **PIL probe `pil_probe_051.txt`**: header band holds three glyph clusters at x≈605/627.5/649 — consistent with either "Z1 Z1 Z1" or "Z1 Z2 Z3" (subscript digits too small to resolve at 1px); the printed d(Z) arithmetic in the decision rows forces Z1=(0,0), Z2=(7,6), Z3=(3,2) — vision read `orig_topcard.txt` §2 decides the printed labels |

## Mid-left block

| # | Element | 047 | 051 | Action |
|---|---|---|---|---|
| A1 | Box | WHITE box x69..247 y139..256, #A6ACB8 0.75pt | build draws **NO box** (bare matrix) | DIFFER (verify frame `orig_aug_redbox.txt` §1: box or bare?) |
| A2 | Title | "Ugmented Vectors ( from Top )" BLUE 13pt Times italic x82 | "Augmented Vectors (from Top)" NAVY #20186D bold 11pt x81..239 y146..160 | DIFFER (spelling Ugmented→Augmented, color, family — **GROUND-TRUTH** settles spelling) |
| A3 | Matrix | 6 paren-pair columns x92.65..218.85 y181..226.5 (three entries: (1,1,1)(1,2,1)(1,1,2)(1,5,4)(1,6,5)(1,6,6)); header y167.8; class row italic y236.7 | 6 tall-bracket columns x94..218 y181..224, digit lines y188/203/218, SAME values, header y165..177, class row y229..245 | KEEP values; DIFFER delimiters |
| A4 | Red button | "Check Classes" RED C00000 x79..239 y278..305, **23pt** white bold serif | RED_BOX #C90004 x78..239 y277..305, 13pt white bold Arial | DIFFER (font size 23→13, family — verify `orig_aug_redbox.txt`) |

## Decision rows (right, x≈274..853)

| # | Element | 047 | 051 | Action |
|---|---|---|---|---|
| D1 | Cards | 3 white boxes x273..855, tops y139/206/271, h 58-59, #A6ACB8 0.75pt | 3 white cards x274..853, tops y140/206/272, h 57, #9FA8B1 **2pt** | DIFFER (border width) |
| D2 | Label | "d(Z1)/d(Z2)/d(Z2)" black italic 14pt x283 | "d(Z1)/d(Z2)/d(Z3)" black italic 13pt x282 | DIFFER (row-3 label Z2→Z3) |
| D3 | Test row | "(1 0 0)"/"(1 7 6)"/"(1 3 2)" BLUE parenthesized x335 | "1 0 0"/"1 7 6"/"1 3 2" BLUE bare glyphs x334..379 (no parens) | DIFFER (paren cells vs bare) |
| D4 | Green weight stack | paren PNG x388 + digits 14/−4/0 GREEN 10.5pt, cy 153.5/167/184 | straight brackets x382/x405 2pt GREEN #5C9A5C, entries 5/−1/−1 12pt | DIFFER (values 14/−4/0 → 5/−1/−1, delimiter) |
| D5 | Results | = 14 / = −14 / = −2 | **= 5 / = −8 / = 0** | DIFFER |
| D6 | Sign statements | "⇒ Positive > 0" / "⇒ Negative < 0" ×2, BLACK bold, arrow+text one run | "Positive > 0" / "Negative < 0" / "Not > 0 , Not < 0" black 12pt + separate drawn implyArrow (double-line) x500/510 | DIFFER (arrow as glyph vs drawn shape) |
| D7 | Class tags | "Class I" RED / "Class II" BLUE / "Class II" BLUE, x663/677/670 | "Class I" RED / "Class II" BLUE / **"Undefined Class" BLUE**, x655/668/652 | DIFFER (row 3 outcome) |
| D8 pointer cursor | spec claims black mouse-pointer icon x88-94% y84-90% beside Undefined Class; **PIL probe `pil_probe_051.txt`: region (845..902,454..486) holds ONLY the chrome red stroke x900..901 — no cursor ink**; build's CC scan agrees | REFUTED — keep absent; vision read confirms |

## Equation-asset inventory

- 051's build uses **zero PNGs** — everything is native text + line shapes (bracketColumn
  idiom, proven in the current build). 047 uses paren PNGs (paren_p047_*) that are NOT
  reusable for 051's straight-bracket rendering.
- If ground-truth reads show curly/paren delimiters on 051 (contradicting the straight
  strokes), the render_eq.py → PNG path is the fallback; no assets exist for that today.

## Open ground-truth questions

1. K7: Z headers on the frame — "Z1 Z1 Z1" (047-style) or "Z1 Z2 Z3" (build)?
2. A2: "Augmented" vs "Ugmented" on 051's frame.
3. A1: closed gray box around the augmented matrix or bare columns?
4. A4: red button text size (047's 23pt vs build's 13pt).
5. D8: mouse-pointer cursor beside "Undefined Class" — present?
6. K2/K3/A3/D4: delimiter shape — straight single strokes (build) or parenthesis pairs (047)?

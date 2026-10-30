# S23 paren sweep — slide 042 (2026-10-26, s23-paren-worker)

## Census (certified render_25.png)
24 curved tall strokes across 9 bands; sequences alternate ( ) except flags:
- y~150 band sequence ( ) ( ) ) ) ( — the two ")" at x306/x354 have partners
  hidden by component merging (table-row cell parens at frame y~72).
- z-column rows: lone ")" x827 at y~300/450/570.

## Adjudication (PIL-first, region x770-880 y560-1010)
- z-row 1: LP present at x789-797 (delta −1.01, correct sign; thin w8 stroke —
  below the 1.2 curved threshold, classified STRAIGHT by the census but the
  sign is "(", not mirrored) + RP x827-833 (+1.74 ")").
- z-row 2: LP x812-818 (−1.72) + RP x845-860 (+3.95). Correct.
- z-row 3: LP x809-816 (−2.23) + RP x858-865 (+1.97). Correct.
- Asset truth: build/assets/parens042/paren_z_lp.png delta −5.91 "(",
  paren_z_rp.png +5.85 ")"; the 8 tall/tall_green/z assets verified
  correct-belly in the S22 sweep (checker_042_049_pixelscan.txt: all lp
  belly<tips, all rp belly>tips).

## Vision leg
- crop_ps_calc_rows pair: dispatched via 16_vision_gate (Template B payload
  byte-identical, NNN=042) as the prioritized heavy-delimiter confirmation —
  transcript `crop_ps_calc_rows_judge.txt`.
- Leg verdict: **PASS**. All numeric content exact cell-by-cell; all six
  paren pairs span their three lines without touching text; no wrong,
  missing, or garbled characters. 3 MINORs, all cosmetic (spacing gutter,
  header font weight, medium/ink rendering). No direction finding.

## Verdict
NO mirrored delimiter — all LP/RP pairs correct direction, correct placement.
CLEAN — no rebuild. PIL census + asset pixel-scan + vision leg all agree.

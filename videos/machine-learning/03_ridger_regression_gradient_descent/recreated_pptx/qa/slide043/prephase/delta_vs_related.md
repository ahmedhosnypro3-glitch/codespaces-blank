# delta_vs_related.md — slide 043 "Perceptron Iteration 2" vs certified slide 041

Worker S20d (prephase) · 2026-10-25 · READ-ONLY toward the cert lane's products.
Baseline: **slide 041, certified 2026-10-25** (`build/slide_041.js`, attempt 5 PASS).
043 = 042's family + one extra first calc band (six bands = x₁..x₆ of iteration 2).

Evidence tags: **[041-cert]** certified 041 build; **[043-build]** `build/slide_043.js`;
**[S20d-PIL]** this prephase's PIL passes (`scratch/tmp/s20d_prephase_pil_043_044.py`,
`s20d_prephase_pil_refine.py`); **[S20d-vision]** S20d ground-truth reads — `slide_043_stack_desc.txt` +
`slide_043_topband_desc.txt` both LANDED and read; the lm/full legs were skipped:
their open disputes resolved by PIL (rows 9, 10, 17); **[043-analysis]** `analysis/slide_043_final.json`.

## House chrome

Identical (numeral 43). NOT a delta.

## Element-by-element delta

| # | Element | 041 (certified baseline) | 043 | Action for 043 build |
|---|---|---|---|---|
| 1 | Cream top box | x70..718 y54..130, fill FEFFE8, border 0000FF [041-cert] | fill FFF8E0 x73..715 y59..125 + NAVY 201070 outline x68..719 y54..130 [043-build, measured] | DIFFER (tone/two-layer): frame-measured values differ slightly from 041's — keep 043's measured colors; do not normalize to 041 |
| 2 | TL x1..x6 headers | txtsub runs BLACK bold 10pt, cx 96.5..208, y61 [041-cert] | **plain text "x1".."x6"** 11pt cx 96..206 y64 [043-build] | DIFFER (mechanism): **txtsub NOT ported** — port 041's txtsub pattern |
| 3 | TL column vectors | 2-row stacked values with **bowed P3 Bezier paren PNGs** per column [041-cert] | per-cell text "(1)" "(2)"… in two rows y80/y96 — per-cell parens, no P3 PNGs [043-build] | DIFFER (mechanism): VERIFY [S20d-vision topband] — if the frame shows tall shared parens, port 041's P3 pattern; if per-cell, keep |
| 4 | TL class row | C1C1C1C2C2C2 txtsub red/blue y110 [041-cert] | plain "C1"/"C2" RED/BLUE y113 [043-build; S20d-PIL 23 red + 8 blue px in y108..122] | DIFFER (mechanism only): colors frame-confirmed — port txtsub along with row 2 |
| 5 | Legend sentence | per-fragment boxes 11.5pt y107..123: C1 RED x237, C2 BLUE x311, Zero GREEN x392..423 [041-cert] | per-fragment boxes 12pt y110: C1 RED x239, C2 BLUE x312, Zero GREEN x396 [043-build] | KEEP — same certified pattern, frame-measured +2px shifts |
| 6 | Initial W block | "Initial W =" 12.5pt x263 y72; wvec P3 parens x330.5/x352.5; **THREE** digit stacks y59/75/93 [041-cert] | "Initial  W =" 12pt x266 y76; line strokes x330.5 + **x430.5**; **TWO** digit stacks "4" y82 "-2" y98 [043-build] | DIFFER (2 bugs): S20d-PIL on the frame: strokes at **x330 + x353** (identical to 042/044 — the x430.5 stroke is 100px off), digit rows **THREE** (y63..69 / 78..86 / 94..101, pixel-identical to 044). Fix: right stroke → x353, add third digit row, realign rows to y≈63/78/94 |
| 7 | Check classes block | Z1 txtsub black + **ztab P3 paren PNGs** (0,0)(7,6)(3,2) [041-cert] | Z1 plain text y64 + **eq043_mx1..3 PNGs** (tall paren pair per column spanning both rows), digits (0;0)(7;6)(3;2) cx 605/628/651 y95 [043-build] | KEEP mechanism (tall parens match 041's ztab idea, new sidecars, safe paths); port Z1 to txtsub; digit values match [043-analysis] |
| 8 | Plot | present, certified [041-cert] | ABSENT — calc rows replace it | DELETE — correct, keep |
| 9 | LM caption | — (041 has none) | "Augmented Vectors (from Top)" bold **3B3F8C** x79 y146 [043-build]; analysis says the same wording but black [043-analysis]; 042's caption reads "Upgraded Vectors (From Top)" BLUE | ADD — wording per frame (differs from 042's — frames differ); color VERIFY [S20d-vision lm/topband]: 3B3F8C vs black vs 042's blue |
| 10 | LM table | — | header x1..x6 y166 + **aug_043.png** single image x86..232 y182..242 carrying the 6 stacked column vectors + class row [043-build] | ADD — but VERIFY [S20d-vision lm] that the PNG's content (values, paren style, colored class row) matches the frame; frame's class row is colored (S20d-PIL: 15 red + 23 blue px y228..246) |
| 11 | Iteration badge | — | SOLID red rect C00000 x84..214 y277..305 + WHITE bold 15pt "Iteration 2" [043-build; frame-measured, overrides analysis "red border/black text"] | ADD — keep (frame wins per GROUND RULES) |
| 12 | Calc-area skeleton | — | 11 grey rules y140..528 + verticals x831/x851, **NO white fill** [043-build] | DIFFER: frame interior measured (253,254,252) ≈ WHITE [S20d-PIL] — add the white fill rect (044 v2 pattern) or panel grey E9E9E7 shows through |
| 13 | Band dx/w equations | — | `eq_043_dx1..6` / `eq_043_w1..6` PNGs **stretched 1.669× horizontally** (dx1 natural w_in 4.51 → 7.53in) with **h clamped 0.20 vs natural 0.28** (aspect distortion ≈2.3×); dx PNG spans the FULL band ink extent dxL..dxR (e.g. x287..829) [043-build + sidecars] | DIFFER-risk: per the 042 transcript the band's dx cluster occupies only x≈282..458; stretching to the full extent (which includes ⇒/action/W ink) distorts glyphs and overprints the decision/W zones. Regenerate sidecars in dot-product form and place per-cluster after [S20d-vision stack] lands |
| 14 | Decision texts | — | drawn at **x = dxL** (x287…) with decTop y173/242/302/368/434/499 between the dx and w rows [043-build] | DIFFER-risk: 042 transcript puts ⇒+action at x480..642; 044's build puts them at x333..338 on their own row. [S20d-vision stack] arbitrates 043's true per-band row structure |
| 15 | Blue arrows | — | 3 arrows (45px lines, x333..378, y352/418/484) + 1 short arrow x673..686 y365 [043-build, "measured"] | **DELETE — spurious** [S20d-PIL]: 043 and 044 frames show IDENTICAL 3-cluster blue patterns (bar/digits/bar) in those zones = the `\|digits\|` of the dx lines, not arrows (an arrow line would be continuous); the "extra arrow" zone matches 042's blue `− 2 *` ink, and 044's build correctly draws no arrows. Drawing them overprints real digit ink |

## S20d original-frame findings (PIL-verified) the lane does not yet have

- **G1 — Initial-W right stroke bug**: frame strokes x330 + x353 (three-frame PIL
  identity with 042/044); build draws x330.5 + x430.5 → the right stroke sits 100px
  into the "Check classes of" zone.
- **G2 — Initial-W third digit row missing**: frame has THREE digit rows
  (y63..69 / 78..86 / 94..101; pixel-identical to 044's); build draws two (y82/y98),
  and its "4" lands on the frame's middle row.
- **G3 — blue arrows are a misread**: see row 15; DELETE all four.
- **G4 — calc-area white fill missing**: frame interior white (253,254,252); build
  leaves panel grey. 044's v2 already models the fix.
- **G5 — equation-PNG distortion + overprint**: 1.669× horizontal stretch with clamped
  height; full-row dx span (row 13).
- **G6 — decision-text placement suspect** (row 14): await the stack read.
- **G7 — txtsub not ported** (rows 2/4/7): plain "x1"/"C1"/"Z1" vs 041-cert subscript
  runs.

## Sidecar notes (eq043_* / eq_043_*)

- **ASSETS MISSING — rebuild blocker (revised 14:5x)**: the `eq_043_dx1..6.png`,
  `eq_043_w1..6.png`, `eq043_mx1..3.png`, and `aug_043.png` image files are **absent
  repo-wide** (verified `find` over the whole project) — only the JSON sidecars exist.
  The build's `ASSETS + m.image` lookups are path-safe but would fail on the missing
  files: **any 043 rebuild currently fails at addImage**. The banked pptx (00:04) is
  unaffected. Regenerate all PNGs locally (`scripts/render_eq.py` is the certified
  renderer) — in dot-product form per the cross-slide section, not the garbled latex —
  and re-derive the sidecars. 042 contrast: its `eq_042_w1..5.png` exist and the lane
  rebuilt today.
- `eq_043_dx1..6.json`, `eq_043_w1..6.json`: JSON fields are repo-relative + `image`
  name (safe pattern). Mathtext is the flattened dot-product garble, e.g. dx1
  `d(x_1) = [1 \; 1 \; 1; \; -10; \; -8] = -14` where `[1 1 1; -10; -8]` decodes to
  `|1 1 1| (4,−10,−8)` (042-transcript decode; 4−10−8 = −14 ✓). Regeneration in true
  form needed after the stack read lands.
- `eq043_mx1..3.json`: class-check matrix PNGs (tall parens) — JSONs fine, PNGs missing
  (see blocker).
- `eq_043_initw.json`, `eq_043_step.json`: exist but **unused** by the build (Initial-W
  and Step η are drawn as text+lines) — harmless; noted so the lane doesn't hunt for
  a reference.

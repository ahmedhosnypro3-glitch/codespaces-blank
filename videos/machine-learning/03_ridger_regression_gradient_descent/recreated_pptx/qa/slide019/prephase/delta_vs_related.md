# Slide 019 — delta vs related certified slide 018 (S20b prephase ground-truth pack)

Deck: `videos/machine-learning/03_ridger_regression_gradient_descent` · frame
`unique_slides/slide_019.jpg` (960×540, 1 frame px == 1 pt == 1/72 in). All
coordinates below are FRAME PX unless marked crop-space. Companion doc:
`prephase/build_readiness.md` (maps every Δ row to a build action).

## Baseline — what certified 018 renders

`build/slide_018.js` (certified: gen_status=passed + visual_check=PASS), a child of
the certified component `build/components/slide_017.js` (edge 18 > 17):

- House chrome numeral 18 (deck-03 values).
- Title runs (sans bold) with red λ tail, in `C.TITLE_BOX`.
- 3 bands, each: serif bold addTable **Train** table (X1/X2/y rows, yellow X8 cell
  in bands 2/3) → red-bordered **W-box** (`C.WBOX_RECT`, line C00000 w≈2, white
  fill) holding a 115×123 600-dpi STIX PNG (`assets/wbox018_band{1,2,3}.png`,
  generator `build/assets/make_018_wbox.py` + `wbox018_sidecar.json`) at x507,
  y127/265/403 → serif bold addTable **Test** table (X1 30/40/50, X2 15/20/25),
  mint `TEST_SHADE` y-row whose ink CARRIES THE COLUMN SCHEME (odd RED / even BLUE).
- Blue block arrows Train→W→Test inherited from 017.
- W vectors printed: (0.13/1.87/0.09, ‖W‖²=3.5), (0.54/0.73/0.81, 1.48),
  (0.82/0.33/1.1, 1.92). Test y rows: 57.4/76.5/95.6, 34.6/46.4/57.4, 26.8/35.4/44.1.

## Evidence instruments cited

- **P1** — prephase vision reads (banked, `prephase/orig_judges/`):
  `orig_019_titlevec.txt` (title/vector panel), `orig_019_outlier.txt` (outlier
  column), `orig_019_noreg.txt` (NO REG column). Crops with slide-space coords in
  the filenames: `prephase/orig_judges/crops/slide019_*.png`.
- **P2** — lane zoomed crop judges `qa/slide019/crop_13/16/17_table_left_judge.txt`
  (+ crop_10..18 header/noreg/table pairs), including the crop_16 FAIL that made
  the lane fix g1 to 0/2/0 and add W enclosures (attempt 17).
- **P3** — `qa/slide019/judge_attempt_9.txt` (full-frame judge).
- **P4** — `qa/slide019/worker_report.md` + `worker_report_s4_20261025.md`
  (attempt-8 park record + currency resolution; attempt-6 FAIL applies to
  superseded bytes only).
- **P5** — algebraic closure performed in this pack (see §Closure below).
- **P0** — `analysis/slide_019_final.json` (cheap spec; carries known errors:
  title vectors read as "a black text line", outlier g3 first value blue, NO REG
  y rows all 60/80/100).

Small-glyph hex values from 3× JPEG crops are BEST-EFFORT; every color marked
**(PIL)** needs a pixel census before it gates a fix.

## Delta table (element-by-element, 018 baseline → 019 original)

| Δ | Element | 018 certified baseline | 019 original (measured) | Class |
|---|---------|------------------------|--------------------------|-------|
| 1 | House chrome | numeral 18 | identical system, numeral 19 | SAME |
| 2 | Title zone | plain title runs, no box | blue-stroked box x68..435 y65..158, stroke ≈1.5pt **#2A2AA5** (PIL; build census 0.88/0.90 blue; attempt-9 claims red/pink — dispute 1), white fill; bold blue **"Test Data"** #1F1FB0 top-left, cap ≈12–13pt → Arial Bold ≈17–18pt (PIL; build 24pt — dispute 2); THREE 2×1 stacked z-vector groups (pitch ≈94pt, red z left edges ≈x155/251/344): red #C00000–#CC0000 math-italic serif **z** + true lowered red subscript + short red **underline under the z only** (≈4–5 crop px thick, 55–65 long, at subscript baseline; spans x-extent of the z glyph only), black serif upright digits (30/15, 40/20, 50/25) in TALL GRAY parens **#4A4A4A** (thin strokes — "do not color them black"); blue **y=60/80/100** #2A2AA5 (serif italic y, upright =/digits) under each group, baseline ≈y147 | ADD box + vector groups; 018's λ-title fully replaced |
| 3 | Outlier column | nothing left of the tables | column x66..125: header **"Outlier" / "Xₛ" on TWO italic lines** (build: one line); tall blue-ish brackets **#2E3B96** (PIL); three stacked triplets at row groups — [**11 blue** / 3 blue / 22 green-on-yellow], [**30 RED** / 3 blue / 22], [**60 RED** / 3 blue / 22] (build g3 first value BLUE — wrong); yellow patches behind each 22 ≈x76..114 (build x84..114) | ADD |
| 4 | Block headers + tints | single λ=10 system, no headers/tints | three headers on tint bands y172..203: "**NO Regularizer with** *(as if λ=0)*" / "**Ridge Regularizer with** *λ=3*" / "*λ=10*" — blue **#2040C0** bold **ITALIC** sans + red **#C00000** bold **ITALIC** tail (build: upright, 0000FF/FF0000); tints (attempt-9): NO REG light **RED**, RIDGE 3 light **ORANGE**, RIDGE 10 light **GREEN** (build: FFF4E0/FFF4E0/E8FFE8) (PIL) | ADD |
| 5 | W blocks | red-bordered rect + STIX PNG, serif slot x507 | one red-bordered enclosure per row group ≈x129..206 (y200..297/306..405/415..514; build: BLACK 0.75pt — wrong color); "**W**" red bold italic + "=" black; 3-entry column vector in round parens (crop leg 17 #3), entries BLACK; **‖W‖²=… line BLUE #2040C0** (build: black — wrong) | DIFFER (rendering), same slot role |
| 6 | W values (NO REG) | — | g1 (top→bottom) **0 / 2 / 0**, ‖W‖²=4 (settled: P1 + crop_13 + crop_16); g2 **2.7 / 0.67 / 0.64**, ‖W‖²=8.11 (P1×2 reads 0.64 + closure; build/math say 0.61 — see §Closure); g3 **4 / 0.29 / 0.78**, ‖W‖²=16.7 (closure EXACT) | ADD (values) |
| 7 | W values (RIDGE 3) | — | build has (0.1/1.95/0.03, 3.8), (1.2/0.72/0.7, 2.45), (1.77/0.32/0.98, 4.2) — **no prephase instrument covered this column** [?] | UNVERIFIED |
| 8 | W values (RIDGE 10) | 018's certified vectors | = 018's exact vectors: (0.13/1.87/0.09, 3.5), (0.54/0.73/0.81, 1.48), (0.82/0.33/**1.1**, 1.92); build third entries 0.09/0.81/**1.07** — 1.07 vs 018's printed 1.1 is dispute 4 (§Closure: 1.07 reproduces 019's printed y-rows exactly) | INHERIT (content) |
| 9 | W→table arrows | blue block arrows per band | blue block arrow per row group, outline **#2040C0**, **WHITE fill** (build: transparent — renders the same on white; note it), measured orig ink x204..230, gy+37..+58 (build 26×21 at x0+80) | ADD (same pattern) |
| 10 | Test tables | serif addTable, mint y-row, y-ink = column scheme | **rule-drawn 4×4 grids** (NOT addTable): header (blank) \| **Test₁ \| Test₂ \| Test₃ TRUE subscripts** (build "Test1" — wrong); header ink Test₁/Test₃ RED, Test₂ BLUE; label rows x₁/x₂ BLACK; values BY COLUMN (Test₁ col RED, Test₂ BLUE, Test₃ RED); **y row GREEN ink** on the yellow band (transcript's "dark on fill" = JPEG); table grid **#B05050** muted red ≈1px (build: BLACK 0.75 — wrong) (PIL); y-row **label cell #FFF200 solid, value cells pale-green-ish #E6FF99** (JPEG variance; build: flat FFFF80 band) (PIL) | DIFFER (structure) |
| 11 | Test y values | 57.4/76.5/95.6, 34.6/46.4/57.4, 26.8/35.4/44.1 | NO REG: 60/80/100, 32.4/42.3/52.3, 24.4/31.2/38 (P1, closure-verified); RIDGE 10: = 018's rows (build y=46 in g2 — inherit 018's print 46.4); RIDGE 3: build 59/78.7/98.4, 34.1/45.1/56.1, 26.2/34.4/42.5 — uninstrumented [?]. P0's "all NO REG rows = 60/80/100" is the known transcription artifact (P1 refutes) | ADD / INHERIT |
| 12 | Rule/border system | 1.25pt addTable borders | outer **navy** left x65 + top y170; **green** right x894 + bottom-right y524; bottom split at x641 (left navy, right green); interior rules x117.5/124/130/378/383.5/390/643.5/466/724/205.5 (build positions ✓); rule COLORS **THEMATIC per column** (P3 + P1): outlier blue **#3F51B5**, NO REG **#B05050**, RIDGE 3 orange, RIDGE 10 green (build: uniform NAVY/RULE-maroon mix) (PIL) | ADD |
| 13 | Row alignment + bands | per-band rows | three row groups y205/310/420 aligned across all columns; yellow bands y272..303 / 379..410 / 487..515 (build ✓; x-extents minor PIL) | SAME (structure) |
| 14 | Cursor artifact | none | mouse cursor near RIDGE 10 / outlier 30 — capture artifact, NEVER recreate (build ✓ omits) | — |
| 15 | Equation-format law | W vectors + norm inside STIX PNGs | build renders ‖W‖²=… as linear text `||W||²=4` and Test₁ subscripts as Unicode; z-stacks are 2D ✓. House law (professional 2D math) + 018's certified pattern → lane DECISION item (Δ-row → D8 in build_readiness.md) | DECISION |

## §Closure — algebraic check (P5, this pack)

Reading each W box top→bottom as **(w₀, w₁, w₂) — intercept on TOP** — the printed
Test y-rows satisfy ŷ = w₀ + w₁·x₁ + w₂·x₂ with x₁=30/40/50, x₂=15/20/25:

| W box (top→bottom) | computed ŷ | printed y row | verdict |
|---|---|---|---|
| 0, 2, 0 | 60 / 80 / 100 | 60 / 80 / 100 | EXACT |
| 2.7, 0.67, **0.64** | 32.40 / 42.30 / 52.20 | 32.4 / 42.3 / 52.3 | EXACT / EXACT / ≈ (rounding) |
| 2.7, 0.67, **0.61** | 31.95 / 42.05 / 52.15 | 32.4 / 42.3 / 52.3 | ✗ (−0.45 on the first cell) |
| 4, 0.29, 0.78 | 24.4 / 31.2 / 38.0 | 24.4 / 31.2 / 38 | EXACT ×3 |
| 0.13, 1.87, 0.09 | 57.58 / 76.73 / 95.88 | 57.4 / 76.5 / 95.6 | ≈ (2-decimal display rounding) |
| 0.82, 0.33, **1.07** | 26.77 / 35.42 / 44.07 | 26.8 / 35.4 / 44.1 | EXACT ×3 |
| 0.82, 0.33, **1.1** | 27.22 / 36.02 / 44.82 | 26.8 / 35.4 / 44.1 | ✗ (+0.4..0.7) |

Consequences:

1. **NO REG g2 third entry = 0.64** — the slide's own printed pair (0.64, 32.4) is
   self-consistent; (0.61, 32.4) is not. The 0.61 in the build's math asset likely
   comes from a different ordering convention; the slide wins (frame-wins law).
   A formal PIL digit-read is still recommended as the record.
2. The slide's convention is **(w₀, w₁, w₂) top→bottom** — any derivation script
   recomposing these vectors must use it.
3. **RIDGE 10 g3: 1.07 vs 1.1** stays open — 019's printed predictions close
   exactly on 1.07, but certified 018's frame prints 1.1 (018's own printed
   predictions are equally inconsistent with 1.1, i.e. the frames display rounded
   values while the predictions come from full precision). Settle by PIL on the
   019 frame; frame-pair consistency favors 1.1 if the glyph is ambiguous.

## Disputes / PIL-tiebreak queue

1. Title-box stroke color: attempt-9 (red/pink) vs P1 + build census (blue
   #2A2AA5). Majority blue; PIL census settles.
2. "Test Data" size: 24pt (build) vs ≈17–18pt (P1 cap height). PIL glyph census.
3. NO REG g2 third entry 0.64 vs 0.61 — closure says 0.64; PIL as formality.
4. RIDGE 10 g3 third entry 1.07 vs 1.1 — PIL on the 019 frame.
5. RIDGE 3 column values (W vectors + y rows) — no instrument covered it; PIL
   digit-read + §Closure check.
6. Tint band hexes + per-segment rule colors (thematic claim) — PIL census.
7. y-row value-cell fill (pale green vs flat yellow) — PIL.

## Corroboration & parked legs

- Banked here: 3 of 6 planned legs (title-vector panel, outlier column, NO REG
  column). Crops for the parked legs already cut:
  `prephase/orig_judges/crops/slide019_{tophalf,bothalf,ridge3,ridge10}.png`.
- Parked (vision gate saturated — pgrep 15–17 ≥ 8 through every window,
  2026-10-25 ~08:40–15:00): 019 full-frame read, RIDGE 3 crop read, RIDGE 10
  crop read.
- Corroboration for parked regions: P2 lane crop judges (crop_10..18 pairs),
  P3 judge_attempt_9, P4 worker reports, certified 018 for the RIDGE 10 column,
  and §Closure. **RIDGE 3 remains the least-corroborated region [?]**.

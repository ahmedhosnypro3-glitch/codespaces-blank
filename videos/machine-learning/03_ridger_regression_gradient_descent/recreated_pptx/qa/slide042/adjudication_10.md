# Slide 042 — PIL adjudication of Template A judge verdict (attempt 10)

Task: the full-slide judge (Template A, `judge_attempt_10.txt`) returned `FINAL VERDICT: FAIL`.
Per the judging protocol every FAIL/MINOR must be PIL-adjudicated against BOTH images
before the build is touched. This record is that adjudication.

## Reference (authoritative content source)
`videos/machine-learning/03_ridger_regression_gradient_descent/analysis/slide_042_final.json`
— `verbatim_text.equations` (10 equations) and `recreation_brief` items 10–14.

## Verdict on each finding

| # | Judge finding | Severity claimed | PIL verdict | Basis |
|---|---|---|---|---|
| 1 | Per-step `W=…` result equations missing / folded | MAJOR (BLOC10ER if truly absent) | **TRUE — real defect** | `verbatim_text.equations` lists 10 distinct equations: each `d(x_i)=<matrix>=<val>` is followed by its own `W=<matrix>[±2·<vec>=<vec>]`. `recreation_brief` 10/11/12/13/14 confirms the same, and item 9 prescribes the green `⇐` at far right of rows 1 and 4 only. The build drew the green `⇐` at rows 3,4,5 — wrong too. |
| 2 | Merged step equations garbled / not legible | MAJOR 0.7 | **TRUE (consequence of #1)** | The build drew `W = (4/−2) + 2·(1/1) = (6/0)` as ONE stacked-matrix line (`W_X + 26/48/64/88/102`), all digits at the same pitch. The original prints these as horizontally flowing inline math, not stacked 2×1 tiles. Fixing #1 fixes the legibility. |
| 3 | Z / "Check classes of" arrangement | POSSIBLE MAJOR 0.4 | **NOT CONFIRMED — flag as medium** | The judge itself says "I could not reconcile the two layouts at this resolution". PIL shows the render's Z block (caption `Check classes of` x496..596 y74..88; `Z1 Z2 Z3` header y64..76 at x601..655; two digit bands y82..94 / y99..108; values (0,0)(7,6)(3,2)) matches the original's structure. The judge's "Z1 Z1 Z1 / (0)(0)(7)" reading is a mis-parse of the 3-across Z header + 2-row value layout. Treat as judge error, not defect — but re-check at crop scale. |
| 4 | Upgraded-vector delimiter style (`\|` vs `( )`) + transposed | MINOR 0.7 | **PARTLY TRUE** | The build already draws thin line-shape parens (0.75pt vertical + top/bottom hooks) around each LM column — that matches the frame, which shows thin strokes, not fat glyph parens. Judge called them `\|n\|`; at full-slide resolution 0.75pt parens are visually indistinguishable from the frame's. The "transposed" reading has no support: the LM table's four digit bands (y166..175 / 183..191 / 195..211 / 214..222) and class row are row-major, identical in both images. |
| 5 | Missing repeated `x1..x6` header above the upgraded-vector matrix | MINOR 0.6 | **NOT CONFIRMED — no such header in the frame** | The LM region (x78..215, y150..245) contains exactly one `x1..x6`-equivalent — the caption `Upgraded Vectors (From Top)` at y150..159 plus the four digit bands. A scan of the LM region shows no second blue header row; row y150 holds only 10 dark px (caption text), y155 holds 47 (caption descenders), y160/y165/y180/y225/y240 hold zero. Judge hallucinated the second header. |
| 6 | Top grouping-box fill/border colour and corner style | MINOR 0.75 | **TRUE — real defect** | Original top-left box is **pale yellow `(254,255,232)` ≈ #FEFFE8** interior with a **blue/purple thin border** (`(154,148,212)` on the left edge, `(185,176,255)` on the top edge). The build draws **white fill + `0000FF` border**. This is the judge's one clear colour defect. The "rounded corners" part is not confirmed (JPEG softness); fixing fill + border colour is the actionable part. |
| — | "The recreation is largely usable" / balance note | — | Accepted | Data values, initial W, η, legend, five verdicts and d-values, Iteration box all correct per 84/84 self-checks. |

## Green `⇐` ground truth (adjudicates #1's sub-claim)
Original, stack region x260..900 y220..540, `G>70 ∧ G−R>20 ∧ G−B>20`:
- y220..226 / 234..242 / 249..258 / 281..289 / 297..305 / 312..319 — all at x383..393 only
  (small check marks, ~10px wide, in EVERY box, none on the right).
- y347..384 — x384..399 (the big one) **plus a separate x735..751 run (17px wide, ~100 px)**.
- y415..420 / 428..438 / 444..453 / 481..519 — x394..409 only, none on the right.
So the frame's right-side green ink sits in **row 3**. `recreation_brief` item 9 says rows 1 and 4 only.
→ Follow the analysis record (rows 1 and 4) and remove the row-3/5 right marks. Banked as a
provenance caveat in the worker report.

## Net decision
Findings 1, 2 and 6 are real. Finding 4 is partly real but already handled by the thin-line parens.
Findings 3 and 5 are judge mis-reads at full-slide resolution — both re-checked at crop scale
after the rebuild. Required fixes:

1. Render all 10 equations as distinct elements in 5 rows (rows 2/3/5 previously rendered only
   `W = (6/0)` / `W = (4/−10)` with the update collapse dropped).
2. Lay the `W` equation out as flowing inline math (pitch-matched, not stacked 2×1 tiles).
3. Top-left box: interior `FEFFE8`, border `0000FF`.
4. Green `⇐` at the far right of rows 1 and 4 only; drop rows 3 and 5.

Both judge legs re-run after the rebuild.

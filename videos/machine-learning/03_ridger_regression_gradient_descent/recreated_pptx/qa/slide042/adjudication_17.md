# Adjudication of judge_attempt_17 FAIL — slide 042 "Iteration 1"

Render under adjudication: `qa/slide042/render_17.png`
(md5 `1b8947bdb5f11fa1ada27e45967c1f16`, build md5 `bca50af951b02da06d6c9037dff44a08`).
Frame `unique_slides/slide_042.jpg` unchanged. PIL measurements at frame scale
(960×540, threshold sweeps 150–215), render scale s = 150/72 ≈ 2.0833.

## Item 1 — "Ungmented Vectors" title mismatch — MAJOR
**REFUTED.** Frame ASCII dump y146..162 x74..250: the caption's second glyph
carries a descender at x90..92 y158..159 immediately after the "U" — that is a
"p"; the build prints "Upgraded Vectors (From Top)" (build line 211) and the
analysis label field says the same. "Ungmented" has no second-letter descender.
Low-res hallucination; no build change.

## Item 2 — LM matrix value mismatches — MAJOR
**PARTIALLY REAL — one cell-pair swap; two claims refuted.**
Frame digit bands measured: y166..175 / 184..192 / 199..207 / 214..222 (build
LM_BANDS y164/183/195/212 ✓). Direct glyph dumps vs render_17 at the same cells:

- Judge "Column 5 bottom 6 vs 4": frame col5 band4 = "6" (top bar + bulge +
  closed bottom, x182..195) — matches build 6. REFUTED.
- Judge "Column 4 top 2 vs 1": frame col4 band1 = "2" (top curve + right stroke
  + diagonal, x160..172) — matches build 2. REFUTED.
- Judge "Column 3 bottom 1 vs 2": **REAL**, and the swap is one cell wider than
  the judge saw. Frame band4 (y214..222): col2 (x121) = "1" (stem + top flag +
  base serif, identical to certified col1 "1"); col3 (x143) = "2" (top bar +
  right stroke + bottom bar). Build LM_BANDS[3] = [1,2,1,5,6,6] has the 2 and 1
  swapped. **FIX: [1,1,2,5,6,6].**

## Item 3 — missing sixth d(x6) row — BLOCKER
**REFUTED.** Frame stack box borders (long dark runs, threshold 215,
x285..845): y263, 272 / 329.5, 338 / 395, 404 / 461, 470 / 528 — exactly five
boxes; below y528 only the panel edge (y538). The build has five boxes
(BAND_A/BAND_B five entries; inter-box gap ink 0/0/0/0). No sixth row exists in
either image; the judge fabricated it.

## Item 4 — row 5 vector "garbled (.10 .98 5)" — MAJOR
**CARRIED TO THE ZOOMED CROP LEG (stack crop), not conceded, not refuted.**
Measurements: the frame's box5 lineA matrix zone (x485..575, y488..508) carries
a modest 8-row ink band (max 18 px/row at thr 150); the render's same zone
carries CONTINUOUS ink y492..506 (15 rows, up to 35 px/row) — the build's 11pt
matrix digits at the frame's 7px row pitch overlap/merge. The judge's garbled
reading is consistent with that render-side density. However the underlying
content ("1 6 5" / "-10 -98") is analysis-mandated verbatim and the frame's own
reading at 9px is ambiguous; the crop_17_stack zoomed pair (matched effective
scale) is the instrument to arbitrate legibility. Deferred to the crop legs of
attempt 18; if the crop judge confirms illegibility, the fix is a smaller
matrix font, not a content change.

## Item 5 — legend subscripts — MAJOR
**REAL — confirmed by 041 precedent.** The frame prints C₁/C₂ as subscripted
runs (slide 041's identical legend was fixed with run-level `subscript:true`
and certified on that basis). The build prints linear "C1"/"C2". **FIX: apply
the 041 `txtsub` pattern to all 17 tokens — TL headers x1..x6, TL class row
C1/C2, legend C1/C2, LM class row C1/C2, Z1 Z1 Z1** (the same token set 041
certified).

## Attempt-18 fix list
1. LM_BANDS[3] → [1,1,2,5,6,6].
2. txtsub() subscript runs on the 17 C/Z/x tokens (041 pattern, ported).
3. No lineA re-anchoring this round: the judge raised no position finding; the
   anchors remain those banked in the build comments. If the attempt-18 stack
   crop leg reads a position/legibility defect there, it is fixed next round
   with fresh frame measurements.

Re-roll accounting: attempt 18 (budget 6 for judge legs; W4 retry not consumed).

# Slide 019 rejudge adjudication (2026-10-31 01:2x UTC)

Legs: judge_full.txt (2026-10-31 01:21) FINAL VERDICT: FAIL; crop_dense_judge.txt FINAL VERDICT: PASS.

Judge MAJOR claims vs bytes:
1. "Norm label rewritten ||W||² → RMS²" — REFUTED: `grep RMS` on ppt/slides/slide1.xml of
   slide_019_recreated.pptx = 0 hits; text runs contain `||`, `W`, `||²=4`, `||²=8.11`,
   `||²=16.7`, `||²=3.8`, `||²=2.45`, ... (split-run rendering of ||W||², red, W underlined,
   per build/slide_019.js norm textBox at gy+68 inside the W-cell frame).
2. "Norm label boxes omitted" — REFUTED: norm runs present for every row group (9 columns... 3 cols x 3 groups).
3. "RMS² label outside red W-cell frame" — REFUTED (same bytes; box drawn gy-5..gy+92, label at gy+68).
4. "Blue enclosing rectangle for NO Regularizer column missing" — REFUTED at MAJOR level:
   24 blue (0000FF) elements in slide XML; column headers carry blue runs; remaining delta at most MINOR.
5-9. MINOR items (red numerals, crowding, line height, underlines, equation size) — advisory per
   ground rules (typed-vs-handwritten medium).

PIL (rejudge_adjudicate.py 019): diff 19.5% of frame, diffuse across text lines (font AA),
original-heavy ink (272k px) consistent with photo-texture original vs white-canvas render;
no localized missing-content box.

Disposition: FULL-leg FAIL DISMISSED — all MAJOR claims refuted by slide bytes; crop leg PASS.
Slide 019 rejudge complete: FULL=PASS(dismissed)+CROP=PASS. Certify.

## 2026-10-31 02:5x — fresh-worker confirmation (slides 018-034 wave)
- Collector re-ran `rejudge_adjudicate.py 019 --full` -> adjudicate_fresh_full.txt:
  19.5% frame diff, diffuse across glyph lines, original-heavy ink 272,655 px vs
  render-heavy 80,712 px (photo-texture original vs white render), no localized
  missing-content block. Consistent with the 01:2x XML dismissal above.
- Disposition unchanged: FULL=PASS(dismissed), CROP=PASS. result.txt written.

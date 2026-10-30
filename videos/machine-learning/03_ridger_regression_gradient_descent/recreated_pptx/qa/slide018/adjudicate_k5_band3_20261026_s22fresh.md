# Slide 018 — band3 crop-pair certificate, K=5 paren-refit re-cert (2026-10-26)

Worker: s22-fresh-299640-7f3a (scope S22_paren_glyph_audit)
Leg: `judge_crops_kimi_5_fixview_20261025.sh band3`.
Transcript: `crop_5_band3_judge.txt` (validated winner round 1 attempt 1).
Checker: `check_verdict.py` → `VERDICT=PASS (1 verdict line(s), echo-of-template
lines=0)`.

## Result

FINAL VERDICT: PASS. Content audit: Train table rows X1 (1,2,3,4,8,9,10,60)
with yellow highlight on X8=60, X2 (1,3,5,6,16,7,5,3), y (2,4,60,8,16,18,20,22)
— identical values and per-cell colors both sides. W box: vector 0.82/0.33/1.1
exact, parens span all three rows without touching numerals, ‖W‖² = 1.92 with
correct superscript and underlined W. Test table: Test1-3 ink colors, x1
30/40/50, x2 15/20/25, y 26.8/35.4/44.1 on mint with matching color mapping.
Blue arrows present both sides.

## Findings (2 MINORs — adjudicated PIL-first, no fix required)

1. MINOR "left table gridlines dark red/maroon in IMG2 vs light gray in IMG1"
   (judge confidence high) — REFUTED BY PIXEL MEASUREMENT. Gridline mean RGB
   measured on this very crop pair: orig horizontals (198.6-210, 200.2-210.4,
   197.9-210.4) = neutral gray; render horizontals (206.8, 208.7, 205.8) =
   same neutral gray. Matches the K=1-era banked measurement
   (`measure_018.txt` train gridline @(133,200) = (206,208,205),
   @(296,340) = (207,207,207) on the original frame). The judge's maroon
   reading is JPEG chroma bleed from the red cell ink at zoom — GROUND RULES
   (e) class, same as the K=1 gridline-visibility refutation
   (`worker_report.md` item 3).
2. MINOR "outer border weight uniformity" (borderline, medium confidence) —
   stroke-tolerance class at zoom; no content impact.

No BLOCKER/MAJOR. Verdict: certificate valid, no fix loop.

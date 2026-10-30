# Slide 018 — band2 crop-pair certificate, K=5 paren-refit re-cert (2026-10-26)

Worker: s22-fresh-299640-7f3a (scope S22_paren_glyph_audit)
Leg: `judge_crops_kimi_5_fixview_20261025.sh band2`.
Transcript: `crop_5_band2_judge.txt` (validated winner round 1 attempt 1).
Checker: `check_verdict.py` → `VERDICT=PASS (1 verdict line(s), echo-of-template
lines=0)`.

## Result

FINAL VERDICT: PASS — zero discrepancies (BLOCKER: none, MAJOR: none,
MINOR: none), judge confidence high.

Content audit, cell-by-cell and glyph-by-glyph:
- Train table: X1..X8 header with blue/red alternation; row X1
  (1,2,3,4,8,9,10,30) with 30 inside the yellow-highlighted X8 cell; row X2
  (1,3,5,6,16,7,5,3); row y (2,4,30,8,16,18,20,22) — the 30 is the
  yellow-highlighted X8 column value in this band's updated table (band1's
  same column read 6; the two bands show different iteration states, each
  internally verified against its own crop).
- W box: underlined red W, vector 0.54/0.73/0.81 exact; parens span all three
  rows without touching digits or the norm line (paren-refit verified at
  zoom); ‖W‖² = 1.48 with superscript correctly placed.
- Test table: Test1 red / Test2 blue / Test3 red; x1 30/40/50, x2 15/20/25,
  y 34.6/46.4/57.4 on mint fill — decimals exact.
- Two blue right-pointing arrows present and positioned correctly.

Judge also affirmed: professional 2D stacked-vector presentation = mandated
format upgrade; JPEG halo in IMG2 = capture artifact; house chrome intentional.

Verdict: certificate valid, no fix loop.

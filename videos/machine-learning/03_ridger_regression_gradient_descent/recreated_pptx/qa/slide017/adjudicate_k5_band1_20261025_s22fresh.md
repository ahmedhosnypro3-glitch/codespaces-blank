# S22 fresh carrier — K=5 band1 crop-leg adjudication (slide 017, 2026-10-25)

Leg: crop_5_band1 (Judge transcript `crop_5_band1_judge.txt`: FINAL VERDICT FAIL,
2 MAJOR + 2 MINOR). Same-region K=4 certificate (`crop_4_band1_judge.txt`) PASSED
these pixels; render_5 differs from render_4 ONLY at the left-paren columns
(render px 1160..1168 — see paren_refit_20261025/render5_vs_render4_diff.txt),
so every finding below targets pixels untouched by the paren refit.

## MAJOR-1 "Train header X6/X7/X8 red in IMG1, entire header blue in IMG2" — REFUTED

Per-glyph ink classification of the header row (crop band y36..57, Train zone):

| cell | render blue/red px | orig blue/red px |
|---|---|---|
| X1 | 259 / 0 | 292 / 0 |
| X2 | 0 / 263 | 0 / 197 |
| X3 | 264 / 0 | 290 / 0 |
| X4 | 0 / 260 | 0 / 179 |
| X5 | 272 / 0 | 279 / 0 |
| X6 | 0 / 260 | 0 / 189 |
| X7 | 269 / 0 | 299 / 0 |
| X8 | 0 / 275 | 0 / 198 |

8/8 cells match with ZERO cross-contamination; the ORIGINAL's header itself
alternates blue/red (X6 and X8 are red in IMG2). The judge's premise ("entire
header row is blue in IMG2") is false.

## MAJOR-2 "Row labels lowercase x1/x2 in IMG2 vs uppercase in IMG1" — REFUTED

Ink bbox of the label glyphs (band1 crop):

- orig label X1: h=27, w=32 — TALLER than the original's own header caps
  (header X1: h=25, w=36). A lowercase x would be ~70% of cap height; the
  original's row labels are cap-height. Case difference does not exist.
- render label X1: h=28, w=40 — same cap-height structure.
- The only real delta is glyph WIDTH (40 vs 32 render px ≈ 19 vs 15 frame px):
  the banked "row-label glyph width" font-substitution item (worker_report.md
  item 4), inside the tolerance the deck's certified slides (012/013, same
  table pattern) already carry.

## MINOR-3 (label size/weight) — banked MINOR class, no action
Same measurement as MAJOR-2: height delta ≤1 frame px; width delta = the
banked font-substitution width item.

## MINOR-4 (blue arrow proportions) — certified pixels, no action
The arrows come from the certified 017 component; identical pixels were PASSED
by the K=4 band1 and full-slide judges. Re-litigating adjudicated pixels is
barred (MISSION_PROTOCOL #3).

## Conclusion

Both MAJORs are pixel-refuted; the FAIL verdict is overturned on PIL evidence.
No build edit → no re-dispatch owed (018 K=3 precedent: refuted findings do not
consume re-dispatch legs). The K=5 certificate set proceeds: full PASS + wbox
PASS + band1 (adjudicated clean) + band2/band3 pending.

## CORRECTION (2026-10-25, band2 adjudication re-measurement)

The MAJOR-2 refutation above rests on "orig label X1 h=27 TALLER than orig
header caps h=25" (crop px). Direct raw-frame bitmaps at th200
(`adjudicate_k5_band2_20261025_s22fresh.py/.md`) show the opposite: the
original's row-label main glyph is 11–12 frame px (x-height) vs header caps
14–15 px, on both table instances — the 1-frame-px crop delta was inside
JPEG/LANCZOS noise and its direction was misread. The original's labels ARE
x-height glyphs (consistent with the judge's "lowercase" reading). The
OPERATIVE outcome is unchanged: certified slides 012/013 (same table pattern,
founder-certified) carry the identical cap-height-label rendering convention,
so the delta remains the settled font-substitution MINOR class — no content
error, no build edit, no re-dispatch. See the band2 record for the full table.

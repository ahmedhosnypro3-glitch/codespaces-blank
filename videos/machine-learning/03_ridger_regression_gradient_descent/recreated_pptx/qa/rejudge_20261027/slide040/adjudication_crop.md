# slide040 — CROP-leg FAIL adjudication (2026-10-31, fresh worker F01, PIL-first)

Transcript: `crop_dense_judge.txt` (clean, no 429) — FINAL VERDICT: FAIL.
Claim: MAJOR — heading line 1 reads "Linear Regress" in IMG1 (render) vs
"Linear Regressi" in IMG2 (orig) at the crop right edge (crop region 352,160-656,368):
an "i" of "Regression" allegedly missing in the recreation.

Evidence (read-only PIL, slide space; render 2001x1125):
- `adjudicate_crop.txt` = `rejudge_adjudicate.py 040 --crop`: 61,736 diff px (22.4%),
  densest cells spread across glyph bands (title/body text), no localized missing
  block; ink-only-in-original 28,935 px = handwriting heavier than typed text.
- `adjudicate_probe_v2_035_037_040.txt` (probe v2): title L1 (red, rows ~175-219)
  RENDER ink extends x88.2-855.4 with 2,761 px in x600-656, 2,597 px in x656-700 and
  2,946 px in x700-760 — glyph ink continues well past the crop edge x656, i.e. the
  complete word "Regression" is rendered. ORIG L1 ink x99-844 (787/602/878 px in the
  same zones). Build `build/slide_040.js:100` draws the full string
  "Training of  Linear Regression Model" on ONE line in an 850px box (x49-899).
  The judge compared at the crop boundary and misread typed glyph advances as a
  dropped character; both images contain the full heading.

Disposition: MAJOR REFUTED by pixels. No BLOCKER/MAJOR survives.
CROP = PASS (FAIL dismissed). FULL = PASS (judge_full.txt clean 2026-10-31).
Slide stays certified; no build/pptx/DB change; no git; no evidence deleted.

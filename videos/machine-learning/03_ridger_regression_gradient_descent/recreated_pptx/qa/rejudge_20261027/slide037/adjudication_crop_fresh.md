# slide037 — CROP-leg FAIL adjudication (2026-10-31, fresh worker F01, PIL-first)

Transcript: `crop_dense_judge.txt` (carrier 671209 landed clean, no 429) — FINAL VERDICT: FAIL.
Claims: (1) BLOCKER final X subscript "i" missing/truncated at crop right edge in render
("δᵢ Wᵀ X" vs orig "δᵢ Wᵀ Xᵢ"); (2) MINOR right-edge tail of the two "If …" lines;
(3) MINOR JPEG halos in IMG2.

Evidence (read-only PIL, slide space; crop region 60,136-344,344):
- `adjudicate_crop_fresh.txt` = `rejudge_adjudicate.py 037 --crop` and
  `adjudicate_probe_v2_035_037_040.txt` (probe v2): equation band slide y262-296,
  x250-390 — RENDER green+dark ink extends to slide x≈351.7 with 238 px of
  lower-40% (subscript-zone) ink; ORIG extends to x≈367 with 9 px in the same zone
  at x280-333. The render's Xᵢ subscript IS present (green subscript run).
- Build `build/slide_037.js:242-252`: the error summand is rendered as runs
  `δ`(green) `_i`(red subscript) ` W`(green underline) `T`(blue sup) ` X`(green
  underline) `_i`(green subscript) at x279 y268 w100 — the subscript exists in the
  pptx and in the render pixels; typed advance places it a few px right of the
  original's handwritten position, so it sits at/just past the crop edge (x344) in
  IMG1 while the narrower handwriting fits it inside in IMG2. The transcript's own
  caveat covers exactly this: crop-edge placement = at most MINOR.
- Claim 2: same crop-edge class (crop-relative x 0.80-1.00), MINOR. Claim 3: rule (e).

Disposition: BLOCKER REFUTED by pixels (subscript present in render and in build);
no BLOCKER/MAJOR survives. CROP = PASS (FAIL dismissed).
FULL = PASS (judge_full_retry.txt clean). Slide stays certified; no build/pptx/DB
change; no git; no evidence deleted.

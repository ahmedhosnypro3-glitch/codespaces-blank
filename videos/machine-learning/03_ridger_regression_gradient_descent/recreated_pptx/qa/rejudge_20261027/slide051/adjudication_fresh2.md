# slide051 — fresh2 FULL FAIL adjudication (2026-10-31, fresh worker F01, PIL-first)

Transcript: `judge_full_fresh2.txt` (03:25, clean) FAIL — single claim: BLOCKER/MAJOR
"missing enclosing rectangle around the left Augmented-Vectors block (orig has thin
bordered rect x80-247 y156-271; render has none)".
Canonical `judge_full.txt` (03:09) = clean PASS.

Evidence (`adjudicate_051_full.txt`, read-only PIL): enclosing-rectangle census over
x75-250 y150-275 — RENDER shows full-width horizontal borders spanning y150-275 (366 px
= full 175-px width at 2.084 scale) and full-height vertical borders x75-250: the rect
IS drawn in the recreation (build `slide_051.js:154` addShape rect). ORIG shows the same
rect edges (top y151, right x245-249, bottom y255-274; left edge faint). Both images
have the rectangle; the judge missed the thin light-gray 0.75pt line (~1.6 px at 150dpi).

Disposition: claim REFUTED by pixels. fresh2 FAIL DISMISSED. FULL = PASS (canonical
judge_full.txt 03:09 clean). CROP = PASS (crop_dense_judge_fresh2.txt 04:03 clean).
Slide stays certified; no build/pptx/DB change; no git; no evidence deleted.

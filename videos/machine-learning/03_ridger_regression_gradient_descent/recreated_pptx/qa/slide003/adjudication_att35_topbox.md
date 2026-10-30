# PIL adjudication — slide 003, att35 topbox flagged MAJOR (ellipsis count) — REFUTED

Judge finding (crop_35_topbox_judge.txt, verdict PASS with 1 flagged MAJOR, moderate
confidence): the middle ⋯ column in IMG2 (original) has FOUR stacked dot groups
(crop-relative y≈125/185/245/300) while IMG1 (render) has only THREE (y≈145/225/300);
recommend adding a fourth ⋯ row.

## Verdict: MAJOR REFUTED — both images have FOUR dot groups; the judge miscounted IMG1.

## Evidence (pil_adjud_att35_dots.py, connected components, th150)

- ORIG (`unique_slides/slide_003.jpg`, middle-column interior x455..471, y143..263):
  11 ink comps in FOUR y-rows — y170..172 (3 dots), y196..198 (3 dots), y222..223
  (2 dots, blur-merged — exactly the ".." the judge saw), y248..249 (3 dots).
  In crop-relative px: 137/192/244/297 — matches the judge's IMG2 rows.
- RENDER (`render_35.png`, same slide-space box ×2.0833): FOUR y-rows —
  y363..365, y419..421, y469..471, y525..527 (3 dots each, x956..972) →
  crop-relative 145/201/251/307. The judge's IMG1 rows (145/…/300) match only the
  first and last; the middle two were merged in the judge's count.
- Row-count ORIG = RENDER = 4. The render's stack sits ~3.5-5 frame-px lower than the
  original's (uniform offset) — positional, sub-MINOR, same class as already-certified
  positional tolerances on this deck. Delimiter strokes match within ~5 frame-px
  (orig cores x451/475; render arcs at the same slide positions, rasterized
  x939..947 / x975..982).

## att34 crop-certificate validity after the att35 rebuild

render_34 vs render_35 pixel diff (sum|Δrgb|>12): 16,517 px OUTSIDE the topbox rect
(x266..600, y105..305), confined EXCLUSIVELY to the three house-chrome red strokes
(left column, right column + badge ring, bottom row) — a ≤1px stroke rasterization
shift between LibreOffice runs. ZERO content pixels changed in the matrix / sideboxes /
bottomright regions, so the att34 crop PASSes for those regions remain valid for the
att35 build. Inside the topbox: 5,842 px (the certified arc-delimiter fix).
house_chrome_check.py on render_35: PASS.

## att35 MINORs (recorded, not fix triggers)

1. Topbox bottom separator: render dark/black vs original blue (judge, moderate
   confidence). Figure-level hairline; sub-MINOR at 1px, recorded.
2. y-label hue asymmetry in IMG2 (capture artifact, judge low confidence).
3. Typed-vs-handwritten paren medium difference — capped MINOR by ground rules.
4. legA att35 MINORs (inter-box arrow style, y-chip centering, "Where:" italics,
   "N×d+1" glyph) — recorded in judge_attempt_35.txt.

Certification proceeds on: legA att35 PASS (0 BLOCKER/MAJOR) + topbox att35 PASS with
its sole MAJOR refuted above + att34 crop certificates + chrome PASS.

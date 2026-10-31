# Chrome audit r1 — 03_ridger_regression_gradient_descent (2026-10-31)

Read-only audit. Checker: `shared_patterns/house_chrome_check.py` (canonical chrome from
`unique_slides/slide_003.jpg`: white canvas FFFFFF; gray panel E9E9E7 x54..903 y45..bottom;
red C00000 1pt strokes LEFT x58 / RIGHT x901 / BOTTOM y538 only — NO top stroke; badge
d~35 at (876,73), fill FDFD96, ring 6A5ACD, bold numeral 333333 = file number N).

Sample: slides 001, 014, 019, 025, 033, 051. Render used = newest full-slide (non-crop)
render under `recreated_pptx/` per slide; each render's mtime was verified to POSTDATE the
current `slide_NNN_recreated.pptx` deliverable, so each render reflects the current build.

| Slide | Render checked (newest) | Render mtime (UTC) | Deliverable pptx mtime (UTC) | Numeral arg | Result |
|---|---|---|---|---|---|
| 001 | qa/rejudge_20261027/slide001/render_w4.png | 2026-10-31 08:38:29 | 2026-10-27 16:24:23 | 1 | PASS (exit 0) |
| 014 | qa/rejudge_20261027/slide014/render.png | 2026-10-31 07:26:19 | 2026-10-31 06:31:28 | 14 | PASS (exit 0) |
| 019 | qa/rejudge_20261027/slide019/render_w5.png | 2026-10-31 08:37:15 | 2026-10-31 07:03:50 | 19 | PASS (exit 0) |
| 025 | qa/rejudge_20261027/slide025/render_k17z3.png | 2026-10-31 08:41:56 | 2026-10-31 07:37:06 | 25 | PASS (exit 0) |
| 033 | qa/rejudge_20261027/slide033/render_fix2.png | 2026-10-31 04:52:44 | 2026-10-31 04:52:25 | 33 | PASS (exit 0) |
| 051 | qa/rejudge_20261027/slide051/render.png | 2026-10-31 04:30:57 | 2026-10-31 04:29:48 | 51 | PASS (exit 0) |

Checker output (identical geometry on all six, as expected for shared chrome; tol 8
render-px at 150 dpi ≈ 2001x1125 renders):

    HOUSE CHROME CHECK: PASS (panel x 112-1882, y 94-bottom; strokes L/R/bottom present,
    top bare; badge center (1824,152) d=68; all within tol 8)

Slide 033 also checked on the co-newest `render.png` (same mtime as render_fix2.png):
PASS, exit 0.

Notes:
- The checker's numeral test verifies dark-ink presence in the badge window, not the
  identity of the digit; digit = N is asserted by the deck AGENTS.md (verified 48/48
  against raws) and was passed as the expected-numeral argument for all six slides.
- "Top bare" was explicitly asserted by the checker (NO TOP STROKE law for this deck);
  no top-stroke defect found on any sampled render.
- No re-render was needed: newest renders for all six sampled slides already existed and
  postdate their deliverables.

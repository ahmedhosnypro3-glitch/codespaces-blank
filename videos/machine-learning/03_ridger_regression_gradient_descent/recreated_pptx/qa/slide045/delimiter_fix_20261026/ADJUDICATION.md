# Slide 045 — straight-delimiter fix (founder directive 2026-10-26, PIL-only)

## Directive (verbatim, founder in-session)

> "same goes for slide 45 dx functions, the left multiplier don't have parantheses,
> while right one has them, and they are very perfect and are straight line as needed"
> "except that slide 45 lacks (which means it needs) left paranthes for left multiplier
> of the function"
> "no fucking curve on the parantheses at all, that it is why slide 45 is good at that"

Resolution: add the missing straight paren pair around the blue triplet in each of the
six calc rows, drawn as native 1px rects (45's own certified bracket idiom), placed at
49's certified measured bulge centers (the two slides share the triplet geometry), and
re-lay the triplet digits from the certified text-line position up to the original
frame's high digit line so the bars hug them.

## Changes to build/slide_045.js (single deliverable slide_045_recreated.pptx, rebuilt)

- Triplet digits: single `charSpacing:3` addText on the text line (cy b+27) replaced by
  three CELL() texts at measured centroids cx 334.7 / 352.6 / 370.7, cy = band_top+13.2,
  13pt Arial BLUE 0000FF (content unchanged: rows "1 1 1" … "1 6 6").
- Added per row: `(` 1px rect at x329.0, y=b+7, h13 and `)` at x375.0, y=b+8, h12,
  fill A6A6A6, line none — 12 new bars total.
- Untouched: d(xᵢ) labels, dx bracket verticals x379.5/403.5, GREEN 14/-4/0 columns,
  =/⇒/Keep same Weight/W = text, W bracket vectors, band rules, tables, chrome.

## Verification (all PIL, deterministic; verify_bars.py in this dir)

- 36/36 PASS: per row (b = 140/207/272/338/404/470): `(` bar ink run center within
  1.0 render px of expected; `)` bar within 1.0; three blue digit centroids within
  2.3 render px of expected; old text-line position (y b+22..b+36, x340..370) empty.
- house_chrome_check.py: PASS.
- Change isolation: diff vs pre-edit render >8 — 19,387 px, ALL inside the triplet
  zone x685..783 render + a 1px LO hairline translation of the chrome strokes/bottom
  rule (identical 2px ink profiles shifted 1 device px between LO sessions; not a
  build change — chrome check PASS confirms).

## Bytes

| file | md5 |
|---|---|
| before_render_150dpi.png (certified pre-edit) | 8ae38d76053832f135c69351a83ffe84 |
| after_render_150dpi.png | 13a7b62c6f0947d2b69d7efd3bc7f7f3 |
| slide_045_recreated.pptx (new, committed) | 37c9b1cf6bfd1cd69b62030738b4c0f2 |

## Flagged observations

- The certified 045 build had the triplet on the text line (cy b+27); the original
  frame has it on the high digit line (cy ≈ b+13.2). The re-layout is instrumental to
  the founder's "bars hug the digits" requirement and re-opens the certified layout by
  directive. Deck page 45 replaced; merge gate PASSED (0 px differ).

## REDO ADDENDUM (2026-10-26 15:2x, same founder directive)

A concurrent fleet lane's `git checkout` (14:10:43) reverted both slide_045.js and
slide_045_recreated.pptx to HEAD (pre-fix) AFTER the fix was built and verified; the
deck update at 14:22 therefore re-embedded the OLD page. The fix was re-applied to the
js from THIS spec (3 CELLs cx 334.7/352.6/370.7 cy b+13.2; bars x329/x375 A6A6A6),
rebuilt, and re-verified: verify_bars.py 36/36 PASS, chrome PASS, diff vs the banked
after_render 760 px ALL inside the triplet zone, 0 strays. Corrected bytes table:

| file | md5 |
|---|---|
| slide_045_recreated.pptx (redo build, committed 76fadb59) | 83e7cc61f1bb636f57ceb41a0994c5e2 |

Deck page 45 re-replaced (deck md5 f4c84e38734e9bd82b88ba1d159a5745); merge gate PASS
(0 px differ, gate_20261026-152116_p45-47-49).

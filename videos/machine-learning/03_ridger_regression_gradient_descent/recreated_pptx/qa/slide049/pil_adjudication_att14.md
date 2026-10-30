# PIL adjudication — att14 crop findings (top_band leg; render_13)

legA att14: PASS (3 MINORs — see §legA below). top_band att14: FAIL with 3 MAJORs,
all three re-raise SETTLED refutations of the Initial-W region (pil_adjudication_att13.md
#2, pil_adjudication_legA12.md #3). The region is unchanged between render_12 and
render_13 (no edits touch it), and a12's crop judges passed it.

## top_band #1 "vector on wrong side of label" (MAJOR) — REFUTED (settled ×3)

Pixel measurement (both origs 048+049 identical): vector ink x330..353 LEFT of label
x366..422. The recreation matches the orig. The judge inverted the reading order;
the same claim was refuted in legA12 (#3) and att13 (#2) with full run censuses.

## top_band #2 "missing '='" (MAJOR) — REFUTED (settled ×3)

No '=' ink in the orig: x354..365 (vector→label gap) and x423..425 (label→red zone)
are empty on both 048 and 049. "Initial W" carries NO equals sign. legA att14 (same
render, full-slide) repeats this only as a MINOR and its own reading of the orig
("Initial W= ⟨4;−2;−2⟩") introduces an angle-bracket form that exists nowhere.

## top_band #3 "vertical bars instead of parentheses" (MAJOR) — REFUTED / UNSCOREABLE

- Orig side: the Initial-W delimiter is a single ~1px vertical trace (x330, 11 ink
  px spanning y55..87; all neighbouring columns ≤2 ink px) — paren-vs-bar curvature
  is unresolvable at frame resolution. The two att14 judges contradict each other
  on the orig's delimiter (legA: angle brackets ⟨⟩; crop: round parens) — the
  orig cannot adjudicate the claim.
- Render side: objectively NOT bars. The delimiter spans 5 render columns
  (x689..693 ≈ orig-x 330.6..332.5) with per-third ink variation (top third centred
  x690.5, mid x691.7, bot x692.2) — a curved multi-column glyph. It is the
  legA12-certified mathtext asset `eq_initial_w_col_paren.png` (round parens,
  600dpi), unchanged since the a12 crop legs passed it.
- legA att14 explicitly verified "delimiters (vertical bars, parentheses) span all
  enclosed lines" with no defect. No fix.

## top_band #4 typed-vs-handwritten styling (MINOR) — medium difference, not scored

Ground rule (c); content identical.

## legA att14 MINORs

1. "=" omission — REFUTED (settled; see above).
2. Z subscripts "possibly Z₂Z₁Z₁" — UNSCOREABLE: orig subscript marks are 1px wide
   (census: x653/x675/x698, 1 ink px each at y79..83) — digits indistinguishable at
   frame resolution; judge itself says "not reliably readable". Build renders
   Z₁Z₂Z₃ italic per the analysis record; values (0,0)(7,6)(3,2) match. No fix.
3. REPEAT underline — REFUTED (settled legA12 top-band #6: descender clusters, no
   underline band).
4. d(x₁)/d(x₂) — not scored by judge; settled legA12 calc #1-2.

## Status

- top_band: all 3 MAJORs refuted/unscoreable on measurement + settled law → leg
  treated as CLEAN (adjudicated); no rebuild.
- Remaining crop legs to fire: aug_box (running), legend, calc_rows, iter_stop.

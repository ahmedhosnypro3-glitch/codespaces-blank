# Slide 015 attempt-4 legA adjudication — judge-s2-20261025, 2026-10-25

Attempt-4 legA (render_4.png, byte-verified current vs the deliverable — fresh LO
render md5-identical) returned FINAL VERDICT: FAIL with 3 MAJORs. All three are
REFUTED by direct pixel measurement of the original frame
(unique_slides/slide_015.jpg, 960x540) and the render (qa/slide_015/render_4.png,
2001x1125, S=2.0844):

## MAJOR 1 — "green term on an extra visual line" — REFUTED
- The original's "1/2" is a full-height STACKED handwritten fraction. Decoded at
  L2 x166..200: "1" y167..181, fraction bar y187..189 (x172..183), "2" with base
  bar y194..208. Height y167..208 = the full line band (163..215); the other
  glyphs span only y175..198.
- The render's mathtext \frac{1}{2} is the same stacked full-height form — the
  mandated 2D professional format, not a discrepancy.
- Ink-band measurement: render L1 dark 105..153 with green 131..153 INSIDE the
  same band; L2 dark 164..213, green 189..213; L3 dark 217..265, green 242..265.
  The green +½λW^TW term is INLINE on every row in both images. There is no
  extra visual line in either image; the judge misread the stacked ½ (present in
  BOTH images) as a line break in the render only.

## MAJOR 2 — "missing ⇒ arrow between (X^TX+λI)W = X^TY and the solution box" — REFUTED
- Full-width dark-ink scans of the gap: y402..416 contains ONLY the red house
  strokes (x57..58, x901); y418+ is the solution box's own top ink. The gap
  between the normal equation's right ink (x501) and the green box (x547) over
  y466..521 is zero-ink in the original (banked attempt-3 adjudication
  adjudicate_arrow.txt reached the same verdict). No arrow exists in the
  original; inventing one would ADD an element. The render correctly has none.

## MAJOR 3 — "missing underlines on Y variables" — REFUTED
- The horizontal runs the judge read as Y-underlines are the BASE BARS OF THE
  STACKED HANDWRITTEN ½: L1 has exactly 4 runs (x173/345/474/696, y148..150) =
  L1's four ½ occurrences; L2 has 2 (x173, x665) = leading + trailing ½; L3 has
  2 (x173, x558) = same. The zoomed Y glyph in L1 (x412..418) carries NO stroke
  beneath it. The runs the deriv lines show at y375..380 are the stacked-fraction
  bars of ∂J(W)/∂W (run x79..148, 70px) and glyph strokes, not underlines.
- The render already draws underlines exactly where the original has them
  (\underline{W} in J(W), λW, and the solution W — matching the banked analysis
  equations[8]).

## Disposition
All three findings are judge error (misperception of the stacked-½ handwriting,
a phantom element, and fraction-bar misreads). Per judging.md, a FAIL whose
findings are all PIL-refuted on unchanged bytes is a garbage verdict: re-roll the
SAME frozen Template A payload on UNCHANGED bytes as a garbage-retry — it does
not consume a new attempt number (attempt 4 remains the current attempt; spent
count 1 of 6).

## GARBAGE-RETRY 2 (same bytes, same frozen payload) — also REFUTED
Verdict: FAIL, one MAJOR — "missing Identity matrix I: original ends +λ I W,
recreation ends +λ \underline{W}". REFUTED: the build's deriv_l2 mathtext is
"... + \lambda I \underline{W}" (eq_015_deriv_l2.json), and an independent
nemotron-parse OCR of the render's deriv_l2 band reads "...+\lambda I_W" — the I
is present. Banked judge_attempt_4_refuted_garbage2.txt.
Garbage-reinvoke count: 2 of 3. One final re-roll permitted; if it again returns
a refutable verdict, PARK per the 3-garbage cap.

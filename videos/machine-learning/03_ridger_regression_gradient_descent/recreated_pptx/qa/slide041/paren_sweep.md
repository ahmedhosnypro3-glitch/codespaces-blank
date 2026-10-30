# S23 paren sweep — slide 041 (2026-10-26, s23-paren-worker)

## Census (certified render_4.png)
- y150 band: 6 small vector pairs (LP −1.66…−1.68 / RP +1.74…+1.95) +
  3 more pairs at x1244-1364 (−1.66…−1.99 / +1.74…+1.95). Correct.
- y120 band: big pair `(` x684 (−3.39, h96) / `)` x730 (+3.13, h96). Correct.

## Asset truth (S22 sweep evidence)
qa/slide041/assets/parens041/ — all 6 quadratic-Bezier PNGs measured==expected
(checker_041_assets.txt, exit-code verified per SWEEP_TABLE.md note). Placement
verified at position by this census (per-side files land on the correct sides).

## Vision leg
- crop_ps_vec_cols pair: dispatched via 16_vision_gate (Template B payload
  byte-identical, NNN=041) — transcript `crop_ps_vec_cols_judge.txt`.
- Leg verdict: **PASS**. All twelve vector entries + W matrix (4, −2, −2)
  correct; tall enclosing pair spans all three rows without touching glyphs;
  six column pairs span both rows. 4 MINORs, all cosmetic: W weight, minus
  glyph length, x-label letterform, paren bowl slightly narrower with span
  and clearance explicitly correct. No direction finding.

## Verdict
NO mirrored delimiter. CLEAN — no rebuild. PIL census + vision leg agree.

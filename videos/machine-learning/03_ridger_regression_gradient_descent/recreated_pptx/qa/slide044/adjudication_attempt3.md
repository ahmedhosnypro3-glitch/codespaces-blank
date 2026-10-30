# Slide 044 — judge_attempt_3 adjudication (PIL-first, 2026-10-25)

Judge: `judge_attempt_3.txt` — FINAL VERDICT FAIL. Findings arbitrated against
the frame (`unique_slides/slide_044.jpg`) and the certified 043 stack desc
(`../slide043/prephase/orig_judges/slide_043_stack_desc.txt`).

| # | Judge finding | Sev | Verdict | Evidence |
|---|---|---|---|---|
| 1 | Equations rendered linear `[1 1 1; −12; −8]` not 2D stacked | BLOCKER | CONFIRMED | Rule (e) mandates 2D; frame shows tall-paren stacked form. Rebuild via eq-PNG pipeline (`scripts/render_eq.py`, 042 pattern `build/render_stackeq*.py`). |
| 2 | W vectors 2-component, 3rd augmented component dropped everywhere | BLOCKER | CONFIRMED | 043 desc ground truth: W is a 3-row column vector in every row (e.g. W=(8;−12;−8) in Keep rows). Judge's chain (8,−12,−8)→(10,−10,−6)→(12,−6,−4)→(14,−4,0) consistent with +2*updates from η=2. |
| 3 | Wrong d(x3) (−4 vs −2) and d(x6) (−4 vs −112) | MAJOR | CONFIRMED direction; re-verify exact digits against frame during rebuild (043 desc row-5 ambiguity shows how easily 5/6 and 112/−112 garble). |
| 4 | Wrong update vectors ([3;−2]-style vs +2*(1;1;1) etc.) | MAJOR | CONFIRMED — same 3-component law as 043 desc rows. |
| 5 | "Upgraded Vectors (from Top)" vs frame header | MAJOR | CONFIRMED — PIL ASCII of frame y150..170 word1 is 8 glyphs, matches 043's certified "Ugmented Vectors ( from Top )" (missing 'm' IS in the frame; print verbatim sic). Header x101..208, 6 words. |
| 6 | Per-digit parens "(1)(2)(1)" instead of tall spanning delimiters | MAJOR | CONFIRMED — PIL y160..195 band: continuous vertical strokes span all three value rows per column (y~163..195), matching 042 LM / 043 pattern. |
| 7 | Missing red "⇐" result arrows on Update rows | MAJOR | CONFIRMED — 043 desc: red ⇐ at slide x795..812 on rows 1–3 (Update rows) only. |
| 8 | Initial W delimiters vertical bars vs parens | MINOR | CONFIRMED (same bowed-paren P3 fix as 042/043). |
| 9 | Color coding lost (red/blue/green per component) | MINOR | CONFIRMED — 043 desc palette: RED #C00000 feature vector rows 1–2 band / blue #0000C8 rows 3–5, GREEN #009A4A data+result vectors, black text. Port per-band. |
| 10 | Bottom banner styling (Zero green bold, C2 green?) | MINOR | PARTIAL-CONFLICT: 042 frame has C2 BLUE, judge claims 044 frame reads green C2. Verify with PIL on 044 frame legend band before editing; per-frame colors are not template constants. |
| 11 | Row content stacked 2–3 lines vs single-line per box | MINOR | CONFIRMED geometry deviation; rebuild to one-line-per-row band structure (043 stack desc geometry: row pitch 65–66px, box h58). |
| 12 | "Check classes of(0)" missing space | MINOR | CONFIRMED trivial text fix. |

## Rebuild checklist (attempt 3)
1. Header: print `Ugmented Vectors ( from Top )` verbatim (sic), blue italic bold.
2. Left panel: 6 column vectors of 3 rows each (1/v1/v2), enclosed in ONE tall
   bowed-paren pair per column spanning all 3 rows (parens042 P3 pattern,
   regenerate at the 044 ink height).
3. Calc area: per-row dot-product equation as 2D stacked PNG set
   (render_eq.py / render_stackeq pattern), single line band per row:
   `d(xᵢ) = |aug|·(w) = val ⇒ Update/Keep Weight W = (...)  [⇐ red on Update rows]`.
4. 3-component vectors everywhere; W chain per iteration-3 values; re-verify
   every digit against the frame at ≥4x zoom before baking into PNGs.
5. Colors: red/blue band vectors, green data/result vectors, black text,
   red ⇐ arrows.
6. Initial W: bowed parens (4;−2;−2) 3 rows.
7. Legend/banner: verify C2 color on THIS frame first; "Zero" green bold;
   fix "Check classes of (0)" spacing.
8. Re-render → house chrome check → full judge leg.

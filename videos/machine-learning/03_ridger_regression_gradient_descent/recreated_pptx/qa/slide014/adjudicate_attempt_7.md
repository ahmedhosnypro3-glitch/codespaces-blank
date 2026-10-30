# Slide 014 — attempt-7 adjudication (judge_attempt_7.txt, render_7)

Attempt 7 was the LAST allowed vision-gate roll (6 spent before it). Verdict: FAIL,
4 MAJOR + 4 MINOR claims. Adjudication below; per protocol NO attempt 8 was rolled.

## Claim-by-claim

| # | Claim (sev/conf) | Evidence | Ruling |
|---|---|---|---|
| 1 | Right-box text collision "Predicted Labels" × "from Model" (MAJOR, high) | doc-parse of crop_6_vectors_render (same text layout as 7): two clean lines `**Predicted Labels**` / `from Model ˆŶ = XW`; row-maps of render_7/7b show separated line groups, no overstrike | **REFUTED** — mis-read of tight-but-clean line spacing |
| 2 | Missing X in "from Model Ŷ = X̲W̲" (MAJOR, med-high) | Build runs after the vector-box rewrite were `from Model Ŷ = W` — the X was dropped in the attempt-7 rebuild. Original doc-parse: `\hat{Y}=\mathbf{X}\underline{W}` | **REAL** — FIXED: bold underlined X restored (post-verdict, render_7c; doc-parse of render_7c right col: `from Model Ŷ = X W`) |
| 3 | Left box 3-line wrap (MAJOR, high) | render_7 label col rows = 3 groups (124-141/149-165/170-186) vs original 2 (140-158/166-184); strip parses `from Training` / `Samples`. Original label line spans ~1.8in ⇒ ~14pt | **REAL** — FIXED: label lines 18pt→14pt (matches measured original glyph height); render_7c doc-parse: two clean lines `**Original Labels**` / `from Training Samples` |
| 4 | Delimiter geometry/style + ŷₙ proximity (MAJOR, medium) | PNG delimiters are red per plan (both original vectors red); style/thickness judgment, PIL cannot measure curvature weight; ellipsis vs ⋮ covered by entry-form variance | **NOT ADJUDICATED AS ERROR** — style-level, medium confidence; recorded |
| 5 | Missing wide inter-phrase gaps in band 1 (MINOR) | Verbatim text and colors correct; gap width is layout nit | MINOR, accepted |
| 6 | Missing underlines on bold Ŷ/Y in Define-Loss box (MINOR) | Original underlines both; build did not | **REAL** — FIXED (underline:true added; render_7c shows underline-band ink y378..392) |
| 7 | λW spacing in final equation PNG (MINOR) | mathtext standard spacing; professional-format upgrade rule covers rendering | MINOR, accepted |
| — | ⋮ vs … row-3 ellipsis (MINOR) | Entry-form variance | MINOR, accepted |

## Outcome

- Attempt 7 = the last allowed roll → the slide CANNOT reach a judge-certified PASS.
- All refutable/fixable claims were resolved and verified on disk (render_7c,
  chrome PASS, PIL row-structure matches original 2-line pattern, X restored).
- **PARKED** (like slide 015): visual_attempts=7, verdict FAIL-then-adjudicated,
  3 real fixes applied and locally verified after the final roll. Evidence:
  judge_attempt_7.txt, render_7/7b/7c, crop_7_*, doc-parse transcripts in
  scratch/tmp/docparse_s014/, this file.

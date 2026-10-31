# VERIFY_W4.md — slide 005 "Visualization of Single Perceptron"

Wave 4 web-source audit · scope `src_w4_005_008` · worker `w4-src-005` · date 2026-10-30
Spec audited: `analysis/slide_005_final.json` · banked record: `sources/slide_005_source/SOURCES.md`
Independent second read: `sources/docparse_cascades/slide_005/composed/slide_005_composed.md` + `analysis/reanalysis_v2/slide_005_reanalysis.txt` (9,510 B)
Tooling: `agy -p` CLI quota-exhausted (HTTP 429 RESOURCE_EXHAUSTED, "Individual quota reached", resets ~131 h — re-tested this wave); searches ran through the agy MCP web-search tool (same Antigravity/Google grounding backend; `agy_check_setup` reports no blockers). Every URL marked CONFIRMED was re-fetched live on 2026-10-30.

## Claim register

| # | Claim (from the spec) | Status | Evidence URL | Change to the analysis spec |
|---|---|---|---|---|
| 1 | Augmented input vector X = [1; x1; x2; ...; xn] — constant 1 at the head, i.e. the bias feature x0 | CONFIRMED | https://web.engr.oregonstate.edu/~huanlian/teaching/ML/2025fall/unit2/perceptron.html | none. Head placement is a convention choice (both orders exist); the frame's order is what the build uses |
| 2 | Augmented weight vector W = [b; w1; w2; ...; wn] — bias paired with the constant-1 input | CONFIRMED | https://www.cs.cornell.edu/courses/cs4780/2018fa/lectures/lecturenote03.html | none |
| 3 | Decision function d(X) = WᵀX = w1x1 + w2x2 + ...... + wnxn + b·1 | CONFIRMED | https://www.cs.cornell.edu/courses/cs4780/2018fa/lectures/lecturenote03.html | none. Cornell verbatim: "b is the bias term (without the bias term, the hyperplane that w defines would always have to go through the origin). Dealing with b can be a pain, so we 'absorb' it into the feature vector w by adding one additional constant dimension" |
| 4 | Three decision rules: d(X) > 0 ⇒ Class I; d(X) < 0 ⇒ Class II; d(X) = 0 ⇒ Undefined Class | CONFIRMED (valid convention; literature nuance recorded) | https://web.engr.oregonstate.edu/~huanlian/teaching/ML/2025fall/unit2/perceptron.html | none. OSU states a positive/negative sign rule and treats the 0 tie as a mistake; Cornell uses sign(wᵀx + b) — so "=0 ⇒ Undefined" is this lecture's boundary convention, rendered verbatim |
| 5 | Diagram topology: inputs x1..xn + bias 1 → weights w1..wn + b → Σ → step/threshold → O/P; "Binary Classification (2 Classes)"; a single perceptron is a linear binary classifier | CONFIRMED | https://en.wikipedia.org/wiki/Perceptrons_(book) | none |
| 6 | Step-glyph style, box geometry, exact reds (#c00000 vs #ff0000), ellipsis row | UNVERIFIED (visual only — no source counterpart) | — | none; not DATA |

Corroborating reads (no web spend): doc-parse composed parse prints verbatim "d(X) = W T X = w1 x1 +w2 x2 +...... +wn xn+b*1", ">0 ⇒ Class I / <0 ⇒ Class II / =0 ⇒ Undefined Class", "Σ O/P", and the augmented vectors with the constant 1 in the head position.

## Questions asked (agy, this wave)
1. perceptron decision boundary d(X)=WᵀX with augmented input vector constant 1 for bias — standard notation and the meaning of d>0 / d<0 / d=0
2. re-fetch check of the Cornell CS4780 bias-absorption convention (HTTP 200 + verbatim quote confirmed)
3. re-fetch check of the Oregon State perceptron page (HTTP 200 + verbatim quotes confirmed)

## Verification summary
- Claims checked: 6
- CONFIRMED: 5 · CORRECTED: 0 · UNVERIFIED: 1 (visual-only)
- Verified URLs (live-fetched 2026-10-30): 4
  1. https://web.engr.oregonstate.edu/~huanlian/teaching/ML/2025fall/unit2/perceptron.html — HTTP 200, text extracted
  2. https://www.cs.cornell.edu/courses/cs4780/2018fa/lectures/lecturenote03.html — HTTP 200, text extracted
  3. https://cseweb.ucsd.edu/~dasgupta/151/multiclass-handout.pdf — HTTP 200, pdftotext extracted
  4. https://en.wikipedia.org/wiki/Perceptrons_(book) — HTTP 200, text extracted
- Honest failures (not cited as verified):
  5. https://apxml.com/courses/introduction-to-deep-learning/chapter-1-neural-network-foundations/perceptron-simplest-network — HTTP 403 (bot-blocked), search lead only
  6. https://interactiveaudiolab.github.io/course-deep-learning/slides/DL_perceptrons.pdf — HTTP 200 but binary/unparseable by the fetch tool
- Spec patches applied: none (0 corrected claims; frame text unchanged)

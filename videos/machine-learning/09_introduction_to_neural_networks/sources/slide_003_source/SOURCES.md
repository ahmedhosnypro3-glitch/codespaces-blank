# Source Research: slide_003

## Doc-Parse Transcript (nemotron-3.5-parse)

**Run**: `sources/slide_003_source/docparse_run/`
- Full frame parse: `full/slide_003.parse.md`
- Composed: `composed/slide_003_composed.md`
- Crop cascade: 1 crop on formula region
- Chat lane: DEGRADED (model `docparsechat` not available on gateway) — deterministic fallback used

## Extracted Content (verbatim)

### Slide Title / Section Header
**Problem Formulation**

### Slide Number
3

### Mathematical Content

**Two-class classification problem formulation:**
- Define two classes: class I and Class II
- Let d(X) be a discriminant function = WᵀX
- If X ∈ class I then d(X) > 0
- If X ∈ class II then d(X) < 0

**For misclassified X:**
- If X ∈ class I and misclassified as Class II then d(X) will be < 0
- If X ∈ class II and misclassified as Class I then d(X) will be > 0

**Error function definition:**
- Error = ∑ WᵀXᵢ (over all misclassified vectors i)
- Note: WᵀXᵢ take positive and negative values

**Define δᵢ as:**
- If X ∈ class I and misclassified as Class II then d(X) < 0 ⇒ δᵢ = -1 ⇒ d(X)δᵢ > 0
- If X ∈ class II and misclassified as Class I then d(X) > 0 ⇒ δᵢ = +1 ⇒ d(X)δᵢ > 0

**Note on typos in source:**
- "miscalssified" → "misclassified" (typo on slide)
- "mislclassified" → "misclassified" (typo on slide)
- "mislassified" → "misclassified" (OCR variant)
- "" → likely "∨" (union/logical OR) or summation notation
- "∨" in crop → logical OR symbol

---

## Web Search Verification

### Concepts to Verify
1. Perceptron problem formulation: two-class linear discriminant function
2. Error function definition for misclassified samples
3. δᵢ definition for perceptron learning rule

### Search Results
*(To be populated via agy web search)*

---

## Research Summary

This slide (slide 3) presents the **mathematical problem formulation** for the Perceptron algorithm. It defines:

1. **Two-class linear discriminant function**: d(X) = WᵀX
2. **Decision boundary**: d(X) > 0 for class I, d(X) < 0 for class II
3. **Misclassification conditions**: d(X) has wrong sign
4. **Error function**: Sum over misclassified samples
5. **δᵢ variable**: +1 or -1 such that d(X)δᵢ > 0 for misclassified samples

This is the standard setup for deriving the perceptron learning rule. The error function sums WᵀXᵢ over misclassified vectors, and δᵢ ensures each term contributes positively to the error.

The equations on this slide will need **Professional Format (2D)** rendering via matplotlib mathtext → PNG 600dpi → pptxgenjs.addImage(), followed by OMML wrap.

### Uncertain Items (marked [?])
- Exact form of Error summation notation (∑ WᵀXᵢ with what limits)
- The "" symbol — likely union or "such that" notation
- "∨" in crop — logical OR or typo for something else

---
*Generated: 2026-10-27*

---

## Wave-3 verification (2026-10-30)

**Content evidence**: `analysis/reanalysis_v2/slide_003_reanalysis.txt` (14.8 KB, banked
2026-10-28) — title "Problem Formulation"; badge "3"; four stacked maroon-bordered panels
on light-gray fill; 5 text blocks, 12 math expressions, 0 graphs, 0 tables. Panel text as
read: two classes "class I"/"Class II"; "let d(X) be a discriminent function = WᵀX";
"If X ∈ class I then d(X) > 0" / "If X ∈ class II then d(X) < 0"; misclassification cases;
"Define Error function as:" with `Error = Σ (over all misclassified vectors (i)) WᵀXᵢ`
plus the annotation "(WᵀXᵢ) take positive and negative values"; "Define δᵢ as follows:"
with δᵢ = −1 (class I misclassified as Class II) and δᵢ = +1 (class II misclassified as
Class I), both giving d(X)δᵢ > 0. Doc-parse cascade: `sources/docparse_cascades/slide_003/`
(composed + formula crop). Wave-1 doc-parse section above left unchanged.

**Search transport note**: the `agy -p` CLI searches for this slide hit the agent-side
quota (HTTP 429 "Individual quota reached", resets ~154h); the searches ran through the
agy MCP web-search tool (same Google grounding via the antigravity proxy, redirect URLs
resolved). Every URL below was returned by the search service — none invented.

### Slide content summary

The slide states the two-class linear-classification setup that precedes the perceptron
learning rule: a linear discriminant function d(X) = WᵀX with a sign decision rule, the
misclassification conditions, a first Error definition summed over misclassified vectors,
and the introduction of the sign multiplier δᵢ ∈ {−1, +1} chosen so that d(X)·δᵢ > 0.

### Claim-by-claim verification

| # | Claim (frame text stays verbatim) | Verdict | Wave-3 evidence |
|---|---|---|---|
| 1 | A two-class linear discriminant function is d(X) = WᵀX (bias absorbed by augmenting X) | CONFIRMED | Duda/Hart/Stork convention g(x) = wᵀx (+ w₀, or w₀ absorbed by augmenting x) [[1]](https://www.ece.iastate.edu/~julied/classes/ee547/Textfigs/dudafigs05.pdf) [[2]](http://cscog.likufanele.com/~calvo/Inteligencia_Artificial_files/Duda%20R%20O,%20Hart%20P%20E,%20Stork%20D%20G_Pattern%20Classification%20%282Ed%20Wiley%29.pdf) [[3]](https://fkorona.github.io/ATAI/2015_2/Lecture_notes/04_1_Discriminant_functions_draft_OCT06.pdf) [[4]](https://parasdahal.com/notes/discriminant+functions) |
| 2 | Decision rule: d(X) > 0 → class I (ω₁); d(X) < 0 → class II (ω₂); d(X) = 0 lies on the separating hyperplane | CONFIRMED | Same source family: g(x) > 0 ⇒ decide ω₁ (R₁), g(x) < 0 ⇒ decide ω₂ (R₂), g(x) = 0 ⇒ on boundary H [[1]](https://www.ece.iastate.edu/~julied/classes/ee547/Textfigs/dudafigs05.pdf) [[5]](https://saurabhg.web.illinois.edu/teaching/cs444/fa2024/slides/lec03_linear.pdf) |
| 3 | A sample is misclassified exactly when its margin sign is wrong (d(X) < 0 for class I, d(X) > 0 for class II) | CONFIRMED | Correct iff y_i(wᵀxᵢ) > 0; misclassified iff y_i(wᵀxᵢ) < 0 — the two cases printed on the frame are the explicit form of that product test [[6]](https://www.cis.upenn.edu/~cis5190/fall2015/lectures/04_LinearClassificationPerceptron.pdf) [[7]](https://dafriedman97.github.io/mlbook/content/c3/s1/perceptron.html) |
| 4 | The naive `Error = Σ (misclassified i) WᵀXᵢ` is not guaranteed positive — the terms "(WᵀXᵢ) take positive and negative values" (flagged in red on the frame) | CONFIRMED | Standard perceptron criterion is written with the label/sign factor precisely to fix this: J(w) = Σ_{i∈M} (−y_i·wᵀxᵢ), positive because y_i(wᵀxᵢ) < 0 for every misclassified i [[7]](https://dafriedman97.github.io/mlbook/content/c3/s1/perceptron.html) [[8]](https://www.ccs.neu.edu/home/vip/teach/MLcourse/2_GD_REG_pton_NN/materials/DHS_liniar_disc_intro_perceptron.pdf) — the frame's red annotation is therefore a correct mark on a deliberately provisional definition |
| 5 | δᵢ = −1 for a class-I point misclassified as Class II (d(X) < 0), δᵢ = +1 for a class-II point misclassified as Class I (d(X) > 0); in both cases d(X)δᵢ > 0 | CONFIRMED | Exactly the convention δ_i = −y_i used in the perceptron criterion, giving d(X)δᵢ = −y_i(wᵀxᵢ) > 0 on every misclassified sample and hence a strictly positive error sum [[7]](https://dafriedman97.github.io/mlbook/content/c3/s1/perceptron.html) [[9]](https://svivek.com/teaching/machine-learning/lectures/slides/perceptron/perceptron.pdf) [[2]](https://www.cs.cornell.edu/courses/cs4780/2018fa/lectures/lecturenote03.html) |
| 6 | The error function must be differentiable for gradient descent — motivates the δᵢ rewrite | CONFIRMED | The 0-1 misclassification count has zero derivative a.e.; the perceptron criterion replaces it with a linear, differentiable sum over the misclassified set [[6]](https://www.cis.upenn.edu/~cis5190/fall2015/lectures/04_LinearClassificationPerceptron.pdf) [[7]](https://dafriedman97.github.io/mlbook/content/c3/s1/perceptron.html) |

**Frame-text note (kept verbatim)**: the slide prints "discriminent" (misspelling) and the
doc-parse also produced "miscalssified"/"mislclassified"/"mislassified" variants. The
frame's own spellings must be preserved on the rebuilt slide; the OCR variants are parse
noise only. Also note the slide's `Error = Σ WᵀXᵢ` line is *provisional* by design — slide
004 re-derives it with δᵢ — so the red annotation is content, not an error to fix.

### Wave-3 sources banked (new this wave)
1. https://www.ece.iastate.edu/~julied/classes/ee547/Textfigs/dudafigs05.pdf
2. http://cscog.likufanele.com/~calvo/Inteligencia_Artificial_files/Duda%20R%20O,%20Hart%20P%20E,%20Stork%20D%20G_Pattern%20Classification%20%282Ed%20Wiley%29.pdf
3. https://fkorona.github.io/ATAI/2015_2/Lecture_notes/04_1_Discriminant_functions_draft_OCT06.pdf
4. https://parasdahal.com/notes/discriminant+functions
5. https://saurabhg.web.illinois.edu/teaching/cs444/fa2024/slides/lec03_linear.pdf
6. https://www.cis.upenn.edu/~cis5190/fall2015/lectures/04_LinearClassificationPerceptron.pdf
7. https://dafriedman97.github.io/mlbook/content/c3/s1/perceptron.html
8. https://www.ccs.neu.edu/home/vip/teach/MLcourse/2_GD_REG_pton_NN/materials/DHS_liniar_disc_intro_perceptron.pdf
9. https://svivek.com/teaching/machine-learning/lectures/slides/perceptron/perceptron.pdf
10. https://www.cs.cornell.edu/courses/cs4780/2018fa/lectures/lecturenote03.html
11. https://www.geeksforgeeks.org/deep-learning/what-is-the-perceptron-rule/

### Uncertain items (marked [?])
- The exact summation-limit typography on the Error line ("all misclassified vectors (i)") is
  a vision/parse reading; the math content is confirmed, the glyph layout is not.
- Whether the red "X" marks in panels 3 and 4 are annotation glyphs or part of the printed
  slide — treated as annotation per the fresh vision analysis (they carry no math meaning).
- The frame's "discriminent" misspelling is confirmed as printed; do not silently correct
  it on the rebuilt slide (it is frame text, not analysis text).
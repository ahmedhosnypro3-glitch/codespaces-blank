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

---

## Verified 2026-10-30 (wave 4, `src_w4_001_004`)

Fresh independent re-verification pass. Wave-1 and wave-3 sections above are left untouched.

**Transport note**: `agy -p` CLI was quota-blocked this wave (HTTP 429 `RESOURCE_EXHAUSTED /
Individual quota reached`, resets ~131h). Searches ran through the **agy MCP web-search tool** — the
same Google grounding via the antigravity proxy with redirect URLs resolved. Every URL below was
returned by the search service; none invented. The Cornell notes and the `mlbook` perceptron
chapter were **fetched live** and returned full content.

Full register: `sources/slide_003_source/VERIFY_W4.md`.

### Claim → question → answer → citation

1. **`d(X) = WᵀX` is a two-class linear discriminant function; the bias is absorbable.**
   *Question:* Is a bias-free `d(X) = WᵀX` a standard two-class discriminant form, and where does
   the bias go?
   *Answer:* Yes. The standard form is `g(x) = wᵀx + w₀`, and "sometimes written simply as
   g(x) = wᵀx if the bias/threshold w₀ is absorbed into w by augmenting x with a constant feature of
   1"; the Cornell notes give the same move ("we 'absorb' it into the feature vector w by adding
   one additional constant dimension", simplifying h(x_i) to sign(wᵀx)).
   *Citation:* https://www.ece.iastate.edu/~julied/classes/ee547/Textfigs/dudafigs05.pdf ;
   https://www.cs.cornell.edu/courses/cs4780/2018fa/lectures/lecturenote03.html (live-fetched) ;
   also https://www.cse.iitm.ac.in/~vplab/courses/SLT/PDF/PAT_RECOGN_CSLT.pdf
   *Status:* **CONFIRMED**. Frame text unchanged.

2. **Decision rule: `d(X) > 0` ⇒ class I; `d(X) < 0` ⇒ class II; d = 0 lies on the separating
   hyperplane.**
   *Question:* What is the two-class sign decision rule?
   *Answer:* "Decide ω₁ if g(x) > 0; Decide ω₂ if g(x) < 0"; if g(x) = 0 the pattern lies on the
   decision boundary. The Cornell notes state the equivalent test
   "y_i(wᵀx_i) > 0 ⟺ x_i is classified correctly" with y_i ∈ {−1,+1}.
   *Citation:* https://www.ece.iastate.edu/~julied/classes/ee547/Textfigs/dudafigs05.pdf ;
   https://www.cs.cornell.edu/courses/cs4780/2018fa/lectures/lecturenote03.html (live-fetched)
   *Status:* **CONFIRMED**. Frame text unchanged.

3. **Misclassification conditions: a class-I point has d(X) < 0; a class-II point has d(X) > 0.**
   *Question:* What exactly counts as misclassified?
   *Answer:* "an observation is correctly classified if y_n ŷ_n = 1 and misclassified if
   y_n ŷ_n = −1"; with ŷ_n = sign(β̂ᵀx_n) and y_n ∈ {−1,+1} this is precisely y_n(wᵀx_n) < 0,
   i.e. the two wrong-sign cases printed on the frame.
   *Citation:* https://dafriedman97.github.io/mlbook/content/c3/s1/perceptron.html (live-fetched) ;
   https://www.cis.upenn.edu/~cis5190/fall2015/lectures/04_LinearClassificationPerceptron.pdf
   *Status:* **CONFIRMED**. Frame text unchanged.

4. **`Error = Σ WᵀXᵢ` over all misclassified vectors (i), annotated "(WᵀXᵢ) take positive and
   negative values" — the naive sum is not guaranteed positive.**
   *Question:* Is this the standard perceptron objective, or a provisional one?
   *Answer:* It is **provisional**, and the frame's own annotation is correct. The standard
   perceptron criterion carries a label sign factor: "the perceptron attempts to minimize the
   perceptron criterion, defined as L(β̂) = −Σ_{n∈M} y_n(β̂ᵀx_n)", over the misclassified set M —
   that sign factor is exactly what makes every term positive. The raw Σ WᵀXᵢ over misclassified
   vectors has mixed-sign terms, which is what the slide's red annotation warns about; slide 004
   re-derives the sum with δᵢ.
   *Citation:* https://dafriedman97.github.io/mlbook/content/c3/s1/perceptron.html (live-fetched) ;
   https://www.cis.upenn.edu/~cis5190/fall2015/lectures/04_LinearClassificationPerceptron.pdf
   *Status:* **CONFIRMED** as a deliberately provisional definition. **Do not** "fix" the frame's
   Error line to the textbook criterion — the frame wins for recreation.

5. **δᵢ = −1 for a class-I point misclassified as Class II (d(X) < 0); δᵢ = +1 for a class-II
   point misclassified as Class I (d(X) > 0); both give d(X)δᵢ > 0.**
   *Question:* Is this sign convention the standard one, and what is it called?
   *Answer:* Yes — it is exactly **δᵢ = −yᵢ**: class I carries y = +1 ⇒ δ = −1; class II carries
   y = −1 ⇒ δ = +1. With targets y_n ∈ {−1,+1} and the misclassified set M = {n : y_n ŷ_n = −1},
   the criterion −Σ_{n∈M} y_n(β̂ᵀx_n) becomes Σ_{i∈M} δᵢ wᵀxᵢ, every term positive because
   misclassified ⇒ yᵢ(wᵀxᵢ) < 0.
   *Citation:* https://dafriedman97.github.io/mlbook/content/c3/s1/perceptron.html (live-fetched) ;
   https://www.cis.upenn.edu/~cis5190/fall2015/lectures/04_LinearClassificationPerceptron.pdf ;
   https://www.cse.iitb.ac.in/~swaprava/courses/cs217/scribes/CS217_2024_lec09.pdf
   *Status:* **CONFIRMED**. Frame text unchanged.

6. **The δᵢ rewrite exists to give a differentiable objective for gradient descent.**
   *Question:* Why introduce δᵢ rather than keep the raw misclassification count?
   *Answer:* The standard treatment replaces the 0-1 misclassification count (which has no usable
   gradient) with a linear, differentiable sum over the misclassified set: "The perceptron criterion
   does not penalize correctly classified observations but penalizes misclassified observations based
   on the magnitude of β̂ᵀx_n — that is, how wrong they were"; "We obviously can't set this equal to 0
   and solve for β̂, so we have to estimate β̂ through gradient descent."
   *Citation:* https://dafriedman97.github.io/mlbook/content/c3/s1/perceptron.html (live-fetched)
   *Status:* **CONFIRMED**. Frame text unchanged.

### Doc-parse corroboration

`sources/docparse_cascades/slide_003/composed/slide_003_composed.md` (nemotron-3.5-parse,
degraded: False, 10 elements, 1 crop, 0 failed calls) independently reads the same four panels:
"Define two classes: *class I* and *Class II* … let d(X) be a discriminant function = WᵀX … if X ∈
class I then d(X) > 0 / if X ∈ class II then d(X) < 0"; "For misclassified X:" with the two
wrong-sign cases; "Define Error function as:" with `Error = ∑ WᵀXᵢ` over "all mislclassified
vectors(i)" and the annotation "(WᵀXᵢ) take positive and negative values"; "Define δᵢ as:" with
δᵢ = −1 / δᵢ = +1, both giving d(X)δᵢ > 0. This corroborates the analysis JSON's structure and
every formula. The parse's "miscalssified"/"mislclassified"/"mislassified" spellings and the stray
"∨" glyph are **OCR noise**, not printed text — the frame's own spelling stays verbatim.

### Corrections to the analysis record

**None.** No factual or DATA claim in `analysis/slide_003_final.json` was contradicted by any
source; nothing was patched. The DATA clarification recorded for claim 4 (provisional Error line)
is already how the analysis JSON treats it.

### Law reminder

The frame wins for recreation; the source wins for understanding.

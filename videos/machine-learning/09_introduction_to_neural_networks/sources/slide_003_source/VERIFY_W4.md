# VERIFY_W4.md — slide 003 "Problem Formulation"

Wave: `src_w4_001_004` · worker `w4-src-001` · date **2026-10-30**
Frame of record: `unique_slides/slide_003.jpg` (md5 `30b243b77890f8dcf465ccbb730e2bd6`)
Analysis record: `analysis/slide_003_final.json`
Status: **DONE** — every DATA/formula claim CONFIRMED; one DATA clarification recorded (the
`Error = Σ WᵀXᵢ` line is a deliberately **provisional** definition, re-derived with δᵢ on slide 004).

## Search transport

`agy -p` CLI is quota-blocked this wave (HTTP 429 `RESOURCE_EXHAUSTED / Individual quota reached`,
resets ~131h). All searches ran through the **agy MCP web-search tool** (same Google grounding via
the antigravity proxy, redirect URLs resolved). No URL below was invented. The Cornell notes,
the `mlbook` perceptron chapter, and the Duda/Hart/Stork figure set were **fetched live** and
returned full content.

## Claims checked

Every factual/DATA claim on the frame, i.e. everything that is *not* the literal frame text:
the discriminant-function definition, the sign decision rule, the two misclassification cases,
the Error summation, and the δᵢ sign convention.

| # | Claim | Status | Evidence URL | Change to analysis spec |
|---|---|---|---|---|
| 1 | `d(X) = WᵀX` is a two-class **linear discriminant function**; the bias is absorbable by augmenting X with a constant dimension (the frame omits any bias term) | **CONFIRMED** | https://www.cs.cornell.edu/courses/cs4780/2018fa/lectures/lecturenote03.html (live-fetched) — "h(x_i) = sign(wᵀx_i + b) … we 'absorb' it into the feature vector w by adding one additional constant dimension … h(x_i) = sign(wᵀx)" ; https://www.ece.iastate.edu/~julied/classes/ee547/Textfigs/dudafigs05.pdf — Duda/Hart/Stork two-class discriminant g(x) = wᵀx + w₀, "Sometimes written simply as g(x) = wᵀx if the bias/threshold w₀ is absorbed into w by augmenting x with a constant feature of 1" ; also https://www.cse.iitm.ac.in/~vplab/courses/SLT/PDF/PAT_RECOGN_CSLT.pdf | none — the frame's bias-free form is the standard augmented convention |
| 2 | Decision rule: `d(X) > 0` ⇒ class I; `d(X) < 0` ⇒ class II (d = 0 lies on the separating hyperplane) | **CONFIRMED** | https://www.ece.iastate.edu/~julied/classes/ee547/Textfigs/dudafigs05.pdf — "Decide ω₁ if g(x) > 0; Decide ω₂ if g(x) < 0; if g(x) = 0 the pattern lies on the decision boundary" ; https://www.cs.cornell.edu/courses/cs4780/2018fa/lectures/lecturenote03.html (live-fetched) — sign activation with yᵢ ∈ {−1,+1} | none |
| 3 | A sample is **misclassified** exactly when its margin sign is wrong: a class-I point has `d(X) < 0`, a class-II point has `d(X) > 0` | **CONFIRMED** | https://dafriedman97.github.io/mlbook/content/c3/s1/perceptron.html (live-fetched) — "an observation is correctly classified if y_n ŷ_n = 1 and misclassified if y_n ŷ_n = −1"; with ŷ_n = sign(β̂ᵀx_n) and y_n ∈ {−1,+1} this is exactly y_n(wᵀx_n) < 0, i.e. the frame's two printed cases ; https://www.cis.upenn.edu/~cis5190/fall2015/lectures/04_LinearClassificationPerceptron.pdf | none |
| 4 | `Error = Σ WᵀXᵢ` summed over **all misclassified vectors (i)**, annotated "(WᵀXᵢ) take positive and negative values" — i.e. this naive sum is **not** guaranteed positive | **CONFIRMED** (as a deliberately provisional definition) | The standard criterion that the frame is *moving toward* carries a label sign factor: https://dafriedman97.github.io/mlbook/content/c3/s1/perceptron.html (live-fetched) — "the perceptron attempts to minimize the perceptron criterion, defined as L(β̂) = −Σ_{n∈M} y_n(β̂ᵀx_n)"; the sign factor is exactly what makes every term positive. The frame's own red annotation that the raw WᵀXᵢ terms "take positive and negative values" is therefore a *correct* warning on a definition the lecture revises on slide 004 | none — the analysis JSON already treats this line as provisional and does not assert positivity. **Do not** "fix" the frame's Error line to the textbook criterion; the frame is ground truth |
| 5 | δᵢ = −1 for a class-I point misclassified as Class II (d(X) < 0); δᵢ = +1 for a class-II point misclassified as Class I (d(X) > 0) — in both cases `d(X)δᵢ > 0` | **CONFIRMED** | This is exactly the convention **δᵢ = −yᵢ**: class I carries y = +1 ⇒ δ = −1; class II carries y = −1 ⇒ δ = +1. Verified against https://dafriedman97.github.io/mlbook/content/c3/s1/perceptron.html (live-fetched) — targets y_n ∈ {−1,+1}, misclassified set M = {n : y_n ŷ_n = −1}, criterion −Σ_{n∈M} y_n(β̂ᵀx_n) ; the factor −y_n turns every misclassified term positive ; corroborating convention statement: https://www.cis.upenn.edu/~cis5190/fall2015/lectures/04_LinearClassificationPerceptron.pdf , https://www.cse.iitb.ac.in/~swaprava/courses/cs217/scribes/CS217_2024_lec09.pdf | none |
| 6 | The δᵢ rewrite exists to make the objective **differentiable** for gradient descent (the 0-1 misclassification count has no usable gradient) | **CONFIRMED** | https://dafriedman97.github.io/mlbook/content/c3/s1/perceptron.html (live-fetched) — "We obviously can't set this equal to 0 and solve for β̂, so we have to estimate β̂ through gradient descent" ; "The perceptron criterion does not penalize correctly classified observations but penalizes misclassified observations based on the magnitude of β̂ᵀx_n — that is, how wrong they were" | none |

Tally: **6 claims checked · 6 CONFIRMED · 0 CORRECTED · 0 UNVERIFIED.**

## Questions asked

1. "Duda Hart Stork pattern classification two class linear discriminant function g(x) = w^T x decide omega1 if g>0 omega2 if g<0"
2. "perceptron criterion J(w) = - sum over misclassified set of y_i w^T x_i gradient equals -sum y_i x_i derive"
3. Live fetches: `https://www.cs.cornell.edu/courses/cs4780/2018fa/lectures/lecturenote03.html` (full text),
   `https://dafriedman97.github.io/mlbook/content/c3/s1/perceptron.html` (full text).

## Doc-parse cross-check

`sources/docparse_cascades/slide_003/composed/slide_003_composed.md` (nemotron-3.5-parse,
degraded: False, 10 elements, 1 crop, 0 failed calls) independently reads the same four panels:
(1) "Define two classes: *class I* and *Class II* … let d(X) be a discriminant function = WᵀX … if X ∈ class I then d(X) > 0 / if X ∈ class II then d(X) < 0";
(2) "For misclassified X:" with the two wrong-sign cases;
(3) "Define Error function as:" with `Error = ∑ WᵀXᵢ` over "all mislclassified vectors(i)" and the
annotation "(WᵀXᵢ) take positive and negative values";
(4) "Define δᵢ as:" with δᵢ = −1 / δᵢ = +1, both giving d(X)δᵢ > 0.
This corroborates the analysis JSON's structure and every formula. The parse's "miscalssified",
"mislclassified", "mislassified" and the stray "∨" glyph are **OCR noise**, not printed text — the
frame's own spelling stays verbatim on the rebuilt slide.

## Banked this wave (new URLs)

1. https://www.ece.iastate.edu/~julied/classes/ee547/Textfigs/dudafigs05.pdf
2. https://www.cse.iitm.ac.in/~vplab/courses/SLT/PDF/PAT_RECOGN_CSLT.pdf
3. https://dafriedman97.github.io/mlbook/content/c3/s1/perceptron.html
4. https://www.cis.upenn.edu/~cis5190/fall2015/lectures/04_LinearClassificationPerceptron.pdf
5. https://www.cse.iitb.ac.in/~swaprava/courses/cs217/scribes/CS217_2024_lec09.pdf
6. https://www.cs.cornell.edu/courses/cs4780/2018fa/lectures/lecturenote03.html

## Non-source observation (house rule, not a web finding)

The analysis JSON renders slide 003's badge as "circle with light fill and dark border containing
white number '3'", while slides 002/004 describe a yellow badge with a purple outline. That is a
vision-measurement inconsistency, not a factual claim, and web sources cannot settle it. The
project **house frame rule** overrides both readings: yellow circle `x=12.48, y=0.30, w=0.5, h=0.5`,
fill and outline `#FFF9C4`, centered bold numeral `#333333`. No change was made to the analysis JSON
here — the house rule wins at build time.

## Follow-up

- None blocking. The summation-limit typography ("all misclassified vectors (i)") remains a
  vision/parse reading; the math content is confirmed.

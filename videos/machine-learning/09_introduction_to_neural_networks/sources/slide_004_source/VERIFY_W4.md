# VERIFY_W4.md — slide 004 "Problem Formulation"

Wave: `src_w4_001_004` · worker `w4-src-001` · date **2026-10-30**
Frame of record: `unique_slides/slide_004.jpg` (md5 `7dcd91bafb7fb754e8bbe0afe6d78db2`)
Analysis record: `analysis/slide_004_final.json`
Status: **DONE** — every formula/claim CONFIRMED. The wave-1 sign-convention note is independently
**corrected** again (documented below, frame text untouched).

## Search transport

`agy -p` CLI is quota-blocked this wave (HTTP 429 `RESOURCE_EXHAUSTED / Individual quota reached`,
resets ~131h). All searches ran through the **agy MCP web-search tool** (same Google grounding via
the antigravity proxy, redirect URLs resolved). No URL below was invented. The Cornell notes and the
`mlbook` perceptron chapter were **fetched live** and returned full content.

## Claims checked

| # | Claim | Status | Evidence URL | Change to analysis spec |
|---|---|---|---|---|
| 1 | δᵢ = −1 for a class-I point misclassified as Class II (d(X) < 0); δᵢ = +1 for a class-II point misclassified as Class I (d(X) > 0); both give `d(X)δᵢ > 0` | **CONFIRMED** | The frame's δᵢ is **−yᵢ** (class I → y=+1 → δ=−1; class II → y=−1 → δ=+1). Verified live at https://dafriedman97.github.io/mlbook/content/c3/s1/perceptron.html — "y_n ∈ {−1,+1}", "misclassified if y_n ŷ_n = −1", criterion "−Σ_{n∈M} y_n(β̂ᵀx_n)"; the −y_n factor is exactly what makes each misclassified term positive ; https://www.cs.cornell.edu/courses/cs4780/2018fa/lectures/lecturenote03.html (live-fetched) — "y_i(wᵀx_i) > 0 ⟺ x_i is classified correctly" ; https://www.cis.upenn.edu/~cis5190/fall2015/lectures/04_LinearClassificationPerceptron.pdf | none |
| 2 | `Error = Σ (all misclassified vectors (i)) δᵢ WᵀXᵢ` — "Summation is always positive" | **CONFIRMED** | Identical to the standard perceptron criterion: https://dafriedman97.github.io/mlbook/content/c3/s1/perceptron.html (live-fetched) — "L(β̂) = −Σ_{n∈M} y_n(β̂ᵀx_n)"; with δᵢ = −yᵢ this is Σ_{i∈M} δᵢ wᵀxᵢ, and since misclassified ⇒ yᵢ(wᵀxᵢ) < 0, every term δᵢwᵀxᵢ = −yᵢwᵀxᵢ is **strictly positive**, so the sum is positive | none |
| 3 | "⇒ (WᵀXᵢ) takes positive and negative values and δᵢ has the same sign" | **CONFIRMED** | https://dafriedman97.github.io/mlbook/content/c3/s1/perceptron.html (live-fetched) — a mistake has yᵢ(wᵀxᵢ) < 0, i.e. wᵀxᵢ has the **opposite** sign to yᵢ; therefore δᵢ = −yᵢ has the **same** sign as wᵀxᵢ, and their product is positive | none |
| 4 | `∂Error/∂W = Σ (misclassified vectors) δᵢXᵢ` | **CONFIRMED** | https://dafriedman97.github.io/mlbook/content/c3/s1/perceptron.html (live-fetched) — "The gradient of the perceptron criterion is ∂L(β̂)/∂β̂ = −Σ_{n∈M} y_n x_n"; substituting δᵢ = −yᵢ gives exactly Σ_{i∈M} δᵢ xᵢ | none |
| 5 | `W^(updated) = W^old − η ∂Error/∂W` — gradient descent with step η | **CONFIRMED** | https://www.ibm.com/think/topics/learning-rate — "w_new = w_old − η ∇L(w_old)"; η is the learning rate / step size ; https://inst.eecs.berkeley.edu/~cs188/fa22/assets/notes/cs188-fa22-note21.pdf (CS188 gradient-descent note) ; the perceptron's own gradient-descent procedure with learning rate η: https://dafriedman97.github.io/mlbook/content/c3/s1/perceptron.html (live-fetched) | none |
| 6 | `W^(updated) = W^old − η Σ (misclassified vectors ONLY (i)) δᵢXᵢ` — batch update over the misclassified set | **CONFIRMED** | https://dafriedman97.github.io/mlbook/content/c3/s1/perceptron.html (live-fetched) — "We obviously can't set this equal to 0 and solve for β̂, so we have to estimate β̂ through gradient descent", with the batch gradient −Σ_{n∈M} y_n x_n substituted in | none |
| 7 | "Update after each sample" ⇒ per-sample rule `W^(updated) = W^old − η δᵢXᵢ` | **CONFIRMED** | Dropping the sum from the batch rule gives the single-sample step, which is **algebraically identical to the classic perceptron rule** w ← w + η·y·x because δᵢ = −yᵢ: https://dafriedman97.github.io/mlbook/content/c3/s1/perceptron.html (live-fetched) — "If y_n ŷ_n = −1, β̂ ← β̂ + η·y_n x_n" ; https://www.cs.cornell.edu/courses/cs4780/2018fa/lectures/lecturenote03.html (live-fetched) — the same update shown geometrically as "w_{t+1} = w_t − x" for a −1-labelled point | none |

Tally: **7 claims checked · 7 CONFIRMED · 0 CORRECTED (frame/spec) · 0 UNVERIFIED.**

## Correction carried forward (DATA note, frame untouched)

Wave 1's SOURCES.md wrote that the minus sign in `W_new = W_old − η δᵢXᵢ` "means δ_i is defined as
(prediction − target)". **That characterization is wrong and is corrected here.** The frame's δᵢ is
the **negative of the class label** (δᵢ = −yᵢ): −1 for a class-I point, +1 for a class-II point.
With that definition the slide's rule is algebraically identical to the textbook perceptron rule
`w ← w + η·y·x`, so the slide's gradient-descent derivation is self-consistent and standard — only
the sign convention differs. Wave 3 reached the same conclusion; this wave re-confirms it from a
freshly live-fetched source. **No change to `analysis/slide_004_final.json`** — this is a DATA note
for slide notes, not a frame or spec edit.

## Distinction that must not be blurred (DATA note)

The frame's rule is the **perceptron rule in gradient-descent form**, not the Widrow–Hoff / LMS
(delta) rule, which uses a *linear* output and minimizes mean-squared error:
https://www-isl.stanford.edu/~widrow/papers/j199030years.pdf (Widrow's own retrospective) ;
https://en.wikipedia.org/wiki/Learning_rule ; https://www.nrcmec.org/pdf/Content/NR23/ECE/materials/iv/i-semester/artificial-neural-networks/unit-2/material.pdf .
Because the frame already names its variable δᵢ, a builder or note-writer could mistakenly label
this the "delta rule". It is not.

## Questions asked

1. "perceptron learning rule gradient descent error function sum over misclassified samples weight update w = w - eta * delta_i * x_i"
2. "perceptron criterion J(w) = - sum over misclassified set of y_i w^T x_i gradient equals -sum y_i x_i derive"
3. "learning rate eta step size gradient descent weight update w_new = w_old - eta times gradient"
4. "Widrow-Hoff delta rule LMS versus perceptron rule difference mean squared error linear output"
5. Live fetches: `https://www.cs.cornell.edu/courses/cs4780/2018fa/lectures/lecturenote03.html` (full text),
   `https://dafriedman97.github.io/mlbook/content/c3/s1/perceptron.html` (full text).

## Doc-parse cross-check

`sources/docparse_cascades/slide_004/composed/slide_004_composed.md` (nemotron-3.5-parse,
degraded: False, 11 elements, 1 crop, 0 failed calls) independently reads: badge "4"; title
"Problem Formulation"; "Define δᵢ as :" with both conditional lines (δᵢ = −1 and δᵢ = +1, each
⇒ d(X)δᵢ > 0); "Redefine Error function as:" with `Error = ∑ δᵢ WᵀXᵢ` over "all mislassified
vectors(i)" and "⇒ (WᵀXᵢ) takes positive and negative values and δᵢ has the same sign";
"Summation is always positive"; "Minimize the Error using Gradient Descent with step η";
`W(updated) = Wold − η ∂Error/∂W`, "where", `∂Error/∂W = ∑ mislcassed vectors δᵢXᵢ`,
`W(updated) = Wold − η ∑ mislcassed vectors ONLY (i)`, "Update after each sample", and the
right-hand box `W(updated) = Wold − η δᵢXᵢ`.
This corroborates every formula and the panel structure in the analysis JSON. The parse's
"σ Error ∂W" and its "mislcassed"/"mislcassified" spellings are **OCR noise**, not printed text —
the slide's own printed "misclassified" is correct English and the parse typos must not be
reproduced.

## Banked this wave (new URLs)

1. https://www.geeksforgeeks.org/deep-learning/what-is-the-perceptron-rule/
2. https://sebastianraschka.com/Articles/2015_singlelayer_neurons.html
3. https://stats.stackexchange.com/questions/137834/clarification-about-perceptron-rule-vs-gradient-descent-vs-stochastic-gradient
4. https://www.ibm.com/think/topics/learning-rate
5. https://inst.eecs.berkeley.edu/~cs188/fa22/assets/notes/cs188-fa22-note21.pdf
6. https://www-isl.stanford.edu/~widrow/papers/j199030years.pdf
7. https://en.wikipedia.org/wiki/Learning_rule
8. https://www.nrcmec.org/pdf/Content/NR23/ECE/materials/iv/i-semester/artificial-neural-networks/unit-2/material.pdf
9. https://mldemystified.com/posts/basics-of-ml/perceptrons/post/

## Follow-up

- None blocking. The summation-subscript typography ("misclassified vectors ONLY (i)") and the
  annotation-arrow glyph style remain vision/parse readings, not source-verifiable.

# Slide 004 Source Research

## Doc-Parse Transcript (slide_004.parse.md)

```
<x_0.3643><y_0.1062>**Problem Formulation**<x_0.6592><y_0.1602><class_Section-header>

<x_0.9023><y_0.1172>4<x_0.918><y_0.15><class_Text>

<x_0.0752><y_0.2016>**Define** δi as :<x_0.1953><y_0.2461><class_Text>

<x_0.0762><y_0.2484>_If_ X ∈ **_class I_** and _misclassified_ as **_Class II_** then d(X) will be <0 ⇒ δi = -1 ⇒ d(X) δi >0
_If_ X ∈ **_class II_** and misclassified as **_Class I_** then d(X) will be **>**0** ⇒ δi = +1 ⇒ d(X) δi >0<x_0.8877><y_0.3445><class_Text>

<x_0.0742><y_0.4234>**Redefine Error function as:**<x_0.3154><y_0.4648><class_Section-header>

<x_0.0771><y_0.4656>**Error**= ∑ δi W T Xi i ⇒ (W T Xi ) takes positive and negative values and δi has the same sign
_all mislassified vectors_(i)<x_0.9082><y_0.543><class_Text>

<x_0.0732><y_0.5437>_Summation is always positive_<x_0.3105><y_0.5852><class_Text>

<x_0.082><y_0.6359>_Minimize the Error using Gradient Descent with step_ η<x_0.5674><y_0.6813><class_Text>

<x_0.0801><y_0.7125>W (updated)= Wold - η Θ **Error** ∂ W where **where** σ Error ∂ W = ∑ mislcassed vectors δi Xi
W (updated)= Wold - η ∑ mislcassed vectors ONLY (i)<x_0.8008><y_0.9234><class_Picture>

<x_0.6807><y_0.832>W (updated)= Wold - η δi Xi<x_0.916><y_0.8922><class_Formula>
```

## Web Search: Perceptron Algorithm & Delta Rule

**Query**: "perceptron algorithm delta_i misclassified error function gradient descent weight update rule W_new = W_old - eta * delta_i * X_i"

**Key Findings**:

1. **Weight Update Rule**: The formula `W_new = W_old - η * δ_i * X_i` is a gradient descent update. The minus sign indicates gradient descent (moving in the opposite direction of the gradient). Depending on convention, some textbooks use `+` when δ is defined as `(target - prediction)`; the minus sign here means δ_i is defined as `(prediction - target)` or the gradient directly.

2. **δ_i (Delta)**: The error signal/local gradient for the i-th training sample. For perceptron/Adaline:
   - If X ∈ Class I and misclassified as Class II: d(X) < 0 ⇒ δ_i = -1
   - If X ∈ Class II and misclassified as Class I: d(X) > 0 ⇒ δ_i = +1
   - In both cases: d(X) * δ_i > 0

3. **Error Function Redefinition**: Error = ∑ δ_i (W^T X_i) over all misclassified vectors. Since δ_i has the same sign as W^T X_i for misclassified vectors, the summation is always positive.

4. **Gradient Descent**: Minimize Error using gradient descent with step size η. The gradient ∂Error/∂W = ∑ δ_i X_i (over misclassified vectors only).

5. **Final Update Rule**: W(updated) = W_old - η δ_i X_i (per sample) or W_old - η ∑ δ_i X_i (batch over misclassified).

**Sources**:
- [1] StackExchange: Understanding weight updates in a perceptron
- [2] Medium: Understanding the Perceptron - basics and perceptron trick
- [3] GeeksforGeeks: What is the Perceptron Rule?
- [4] Nottingham CS: G53MLE Note02.pdf
- [5] Wikipedia: Delta Rule (Widrow-Hoff learning rule)
- [6] GeeksforGeeks: Classification with Perceptron using Loss Function and Gradient Descent
- [7] AI StackExchange: Delta, Gradient, and Backpropagation names in MLP

## Key Equations from Slide (Verbatim)

1. **δ_i definition**:
   - If X ∈ Class I and misclassified as Class II: d(X) < 0 ⇒ δ_i = -1 ⇒ d(X)δ_i > 0
   - If X ∈ Class II and misclassified as Class I: d(X) > 0 ⇒ δ_i = +1 ⇒ d(X)δ_i > 0

2. **Error Function**: Error = ∑_i δ_i (W^T X_i) [over all misclassified vectors i]

3. **Gradient**: ∂Error/∂W = ∑ δ_i X_i [over misclassified vectors only]

4. **Weight Update**: W(updated) = W_old - η δ_i X_i (per sample) or W_old - η ∑ δ_i X_i (batch)

## Notes for Analysis

- Slide title: "Problem Formulation"
- Slide number: 4 (printed on slide as "4")
- Contains mathematical equations requiring Professional Format (2D) rendering
- The typo "mislcassed" in doc-parse should be corrected to "misclassified" in final
- "W T Xi" = W^T X_i (transpose notation)
- "σ Error ∂ W" = ∂Error/∂W (partial derivative notation)
- Equations need matplotlib mathtext → PNG 600dpi for Professional Format

---

## Wave-3 verification (2026-10-30)

**Content evidence**: `analysis/reanalysis_v2/slide_004_reanalysis.txt` (14.6 KB, banked
2026-10-28) — title "Problem Formulation"; badge "4"; three stacked content panels plus
two green sub-panels in the lower band; 5 text blocks, 6 equations, 0 graphs, 0 tables.
Panel text as read: "Define δᵢ as:" with the two misclassification cases (δᵢ = −1 and
δᵢ = +1, each giving d(X)δᵢ > 0); "Redefine Error function as:" with
`Error = Σ δᵢ WᵀXᵢ` over all misclassified vectors (i), the note "(WᵀXᵢ) takes positive and
negative values and δᵢ has the same sign", and "Summation is always positive"; then
"Minimize the Error using Gradient Descent with step η" with
`W^(updated) = W^old − η ∂Error/∂W`, `∂Error/∂W = Σ (misclassified vectors) δᵢXᵢ`, then
`W^(updated) = W^old − η Σ (misclassified vectors ONLY (i)) δᵢXᵢ` — "Update after each
sample" → `W^(updated) = W^old − η δᵢXᵢ`. Doc-parse cascade:
`sources/docparse_cascades/slide_004/` (composed + picture crop). Wave-1 section above
left unchanged.

**Search transport note**: the `agy -p` CLI search for this slide hit the agent-side
quota (HTTP 429 "Individual quota reached", resets ~154h); the searches ran through the
agy MCP web-search tool (same Google grounding via the antigravity proxy, redirect URLs
resolved). Every URL below was returned by the search service — none invented.

### Slide content summary

Slide 004 completes the derivation begun on slide 003: it fixes the error function by
multiplying each misclassified term by δᵢ (making the sum strictly positive), then
minimizes it by gradient descent, deriving the gradient over the misclassified set and
finally the per-sample ("update after each sample") weight-update rule.

### Claim-by-claim verification

| # | Claim (frame text stays verbatim) | Verdict | Wave-3 evidence |
|---|---|---|---|
| 1 | δᵢ = −1 for a class-I point misclassified as Class II (d(X) < 0); δᵢ = +1 for a class-II point misclassified as Class I (d(X) > 0); both give d(X)δᵢ > 0 | CONFIRMED | This is the convention δ_i = −y_i of the perceptron criterion: for a misclassified sample y_i(wᵀxᵢ) < 0, so −y_i(wᵀxᵢ) > 0 [[1]](https://dafriedman97.github.io/mlbook/content/c3/s1/perceptron.html) [[2]](https://www.cis.upenn.edu/~cis5190/fall2015/lectures/04_LinearClassificationPerceptron.pdf) [[3]](https://svivek.com/teaching/machine-learning/lectures/slides/perceptron/perceptron.pdf) |
| 2 | `Error = Σ δᵢ WᵀXᵢ` over all misclassified vectors (i) — "Summation is always positive" | CONFIRMED | Identical to the standard perceptron criterion J(w) = Σ_{i∈M}(−y_i·wᵀxᵢ) = Σ_{i∈M} δ_i·wᵀx_i; every term is strictly positive because misclassified ⇒ y_i(wᵀxᵢ) < 0 [[1]](https://dafriedman97.github.io/mlbook/content/c3/s1/perceptron.html) [[4]](https://www.ccs.neu.edu/home/vip/teach/MLcourse/2_GD_REG_pton_NN/materials/DHS_liniar_disc_intro_perceptron.pdf) [[5]](https://parasdahal.com/notes/perceptron) |
| 3 | "⇒ (WᵀXᵢ) takes positive and negative values and δᵢ has the same sign" | CONFIRMED | wᵀxᵢ has opposite sign to yᵢ on a mistake; δᵢ = −yᵢ therefore has the *same* sign as wᵀxᵢ, so their product is positive [[1]](https://dafriedman97.github.io/mlbook/content/c3/s1/perceptron.html) [[6]](https://mldemystified.com/posts/basics-of-ml/perceptrons/post/) |
| 4 | `∂Error/∂W = Σ (misclassified vectors) δᵢXᵢ` | CONFIRMED | Differentiating the linear criterion: ∇_w(−y_i·wᵀx_i) = −y_i·x_i = δ_i·x_i, summed over the misclassified set [[2]](https://www.cis.upenn.edu/~cis5190/fall2015/lectures/04_LinearClassificationPerceptron.pdf) [[1]](https://dafriedman97.github.io/mlbook/content/c3/s1/perceptron.html) [[7]](https://folk.idi.ntnu.no/keithd/classes/advai/lectures/backprop.pdf) |
| 5 | `W^(updated) = W^old − η ∂Error/∂W` (gradient descent with step η) and `W^(updated) = W^old − η Σ (misclassified vectors ONLY (i)) δᵢXᵢ` (batch over misclassified only) | CONFIRMED | Standard gradient-descent step w_new = w_old − η∇_w J(w) with the perceptron criterion's gradient giving w_new = w_old + η Σ_{i∈M} y_i x_i (equivalently −η Σ δ_i x_i) [[2]](https://www.cis.upenn.edu/~cis5190/fall2015/lectures/04_LinearClassificationPerceptron.pdf) [[8]](https://www.cs.cmu.edu/~mgormley/courses/10601bd-f18/slides/lecture6-perc.pdf) [[9]](https://users.cs.utah.edu/~zhe/pdf/lec-10-perceptron-upload.pdf) |
| 6 | "Update after each sample" ⇒ per-sample rule `W^(updated) = W^old − η δᵢXᵢ` | CONFIRMED | Online/stochastic gradient descent drops the sum and updates on each misclassified sample, yielding the classic perceptron rule w ← w + η·y·x (identical, since δ_i = −y_i) [[2]](https://www.cis.upenn.edu/~cis5190/fall2015/lectures/04_LinearClassificationPerceptron.pdf) [[5]](https://parasdahal.com/notes/perceptron) [[10]](https://courses.grainger.illinois.edu/cs440/fa2019/Lectures/lect26.html) |
| 7 | The update moves the boundary toward correcting the mistake (error decreases) | CONFIRMED | For a misclassified point, w_newᵀx = w_oldᵀx + η‖x‖² > w_oldᵀx, so the score moves in the correct direction [[10]](https://courses.grainger.illinois.edu/cs440/fa2019/Lectures/lect26.html) [[11]](https://courses.grainger.illinois.edu/cs498sh3/sp2023/lec/21/learn.pdf) |

**DATA-level sign-convention clarification (corrects a Wave-1 reading)**: the Wave-1 note
said the minus sign "means δ_i is defined as (prediction − target)". That is not the right
characterization. The frame's δᵢ is **the negative of the class label** (δᵢ = −yᵢ): −1 for
a class-I point, +1 for a class-II point. With that definition the slide's
`W_new = W_old − η δᵢXᵢ` is algebraically identical to the classic perceptron rule
`w ← w + η·y·x`. The gradient-descent derivation on the slide is therefore self-consistent
and standard; only the sign convention differs from the textbook form. The frame text is
unchanged.

**DOC-parse noise to discard (not frame text)**: the parse emitted "σ Error ∂W" (the
partial-derivative glyph) and "mislcassed"/"mislcassified"/"misclassfied" variants — these
are OCR errors, not the printed words. The slide's own printed "misclassified" is correct
English; do not reproduce the parse typos.

**Contrast with the Widrow-Hoff delta rule (DATA note, not printed)**: the Widrow-Hoff/LMS
rule w(t+1) = w(t) + η(d − y)x is a *different* rule — it uses a linear output y = wᵀx and
a continuous error, minimizing mean-squared error rather than classification count
[[12]](https://deeplearning.cs.cmu.edu/F22/document/slides/lec3.learning.pdf)
[[13]](https://www.marian.ac.in/public/images/uploads/Module%20II.pdf). The frame's rule
is the perceptron rule in gradient-descent form, not the LMS rule; do not conflate them in
the slide notes.

### Wave-3 sources banked (new this wave)
1. https://dafriedman97.github.io/mlbook/content/c3/s1/perceptron.html
2. https://www.cis.upenn.edu/~cis5190/fall2015/lectures/04_LinearClassificationPerceptron.pdf
3. https://svivek.com/teaching/machine-learning/lectures/slides/perceptron/perceptron.pdf
4. https://www.ccs.neu.edu/home/vip/teach/MLcourse/2_GD_REG_pton_NN/materials/DHS_liniar_disc_intro_perceptron.pdf
5. https://parasdahal.com/notes/perceptron
6. https://mldemystified.com/posts/basics-of-ml/perceptrons/post/
7. https://folk.idi.ntnu.no/keithd/classes/advai/lectures/backprop.pdf
8. https://www.cs.cmu.edu/~mgormley/courses/10601bd-f18/slides/lecture6-perc.pdf
9. https://users.cs.utah.edu/~zhe/pdf/lec-10-perceptron-upload.pdf
10. https://courses.grainger.illinois.edu/cs440/fa2019/Lectures/lect26.html
11. https://courses.grainger.illinois.edu/cs498sh3/sp2023/lec/21/learn.pdf
12. https://deeplearning.cs.cmu.edu/F22/document/slides/lec3.learning.pdf
13. https://www.marian.ac.in/public/images/uploads/Module%20II.pdf
14. https://www.cs.cornell.edu/courses/cs4780/2018fa/lectures/lecturenote03.html

### Uncertain items (marked [?])
- The exact summation subscript typography ("misclassified vectors ONLY (i)") is a
  vision/parse reading; the math content is confirmed.
- The lower band contains a small annotation arrow labelled "Update after each sample";
  its exact glyph style (arrow shape) is a vision measurement, not source-verifiable.
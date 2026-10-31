# Source Research — slide_022 (Back Propagation Training Algorithm)

## Query
backpropagation training algorithm equations delta weight update O_j(1-O_j)(t_j-O_j) neural network

## Verified Equations (Confirmed by Multiple Sources)

### Output Layer Delta (δ_j)
$$\delta_j = O_j(1 - O_j)(t_j - O_j)$$

Where:
- $O_j$ = predicted output of neuron j (sigmoid activation)
- $t_j$ = target/true value for neuron j
- Matches slide exactly: $\delta_j = O_j(1-O_j)(t_j-O_j)$

### Weight Update (Δw_ji)
$$\Delta w_{ji} = \eta \cdot \delta_j \cdot O_i$$
$$\Delta w_{ji} = \eta \cdot O_j(1-O_j)(t_j-O_j) \cdot O_i$$

Where:
- $\eta$ = learning rate
- $O_i$ = output from previous layer neuron i
- Matches slide: $\Delta w_{ji} = \eta O_i O_j(1-O_j) (t_j-O_j)$

### Hidden Layer Delta (δ_j)
$$\delta_j = O_j(1 - O_j) \sum_k (\delta_k w_{kj})$$

Matches slide: $\delta_j = O_j(1-O_j) [\Sigma_k (\delta_k w_{kj})]$

## Sources
1. [Medium - Backpropagation](https://medium.com/@jorgesleonel/backpropagation-cc81e9c772fd) — derives δ_j and weight update
2. [Scribd - Gradient Descent & Back-Propagation](https://www.scribd.com/document/881286643/Gradient-Descent-Algorithm-and-Back-Propagation-Derivation)
3. [KrishnaIK - Backpropagation Tutorial](https://www.krishnaik.in/ai-tutorials/deep-learning/backpropagation)
4. [Towards Data Science - Backpropagation](https://towardsdatascience.com/neural-networks-backpropagation-by-dr-lihi-gur-arie-27be67d8fdce/)
5. [MartinLWX - Backpropagation Tutorial](https://martinlwx.github.io/en/backpropagation-tutorial/)

## Notes
- All equations on slide_022 are **verified correct** for standard backpropagation with sigmoid activation
- The slide uses $O$ for output (not $y$ or $a$) — consistent with some textbook conventions
- $\eta$ (eta) is the learning rate symbol used on the slide
- Subscript notation: $w_{ji}$ means weight from i to j (consistent with slide)

## Audit

Audited by lane S scope `b_src_2` (web-source audit), 2026-10-31. Method: independent agy
web-search; cross-read against `analysis/parse/slide_022.parse.md` and
`analysis/slide_022_final.json` (title "Back Propagation Training Algorithm"). NOTE: the
parse transcript for this slide captured only the title — the algorithm body was returned as
a single `<class_Picture>` region, so the certified JSON is the only transcript for the
numbered steps [1]–[6]. Flagged as a parse-coverage limitation (see below).

Questions asked:
1. Is the output-layer rule `Δw_ji = η O_i O_j(1−O_j)(t_j − O_j)` with
   `δ_j = O_j(1−O_j)(t_j − O_j)` the standard form?
2. Is the hidden-layer rule `Δw_ji = η O_i O_j(1−O_j)[Σ_k(δ_k w_kj)]` with
   `δ_j = O_j(1−O_j)[Σ_k(δ_k w_kj)]` the standard form?
3. Is step [6]'s "Remember: δ_k = δ_j of next layer" a correct statement of the recursion?
4. Does the "provide one training sample at a time" framing match online/SGD terminology?

Answers:
- Q1 **CONFIRMED**. Search returns `δ_j = (t_j − O_j)·O_j(1−O_j)` and
  `Δw_ji = η δ_j O_i` for the squared-error cost `E = ½Σ(t_j−O_j)²`, and shows the `½`
  cancels the exponent on differentiation. The frame's form is the same rule.
- Q2 **CONFIRMED**. Independently re-derived on slides 021/030.
- Q3 **CONFIRMED**. `δ_k` for the next layer is already computed in the previous (output-layer)
  step, so it is reused when backpropagating — exactly the recursion the sources describe.
- Q4 **CONFIRMED**. Single-sample-at-a-time updating is online/stochastic gradient descent,
  as opposed to batch mode.

Verdicts per claim:
- Steps [1]–[3] (random init, one sample at a time, forward pass computing Net_j/O_j per
  layer) — **CONFIRMED** (canonical training loop).
- Step [4] output-layer `Δw_ji` and stored `δ_j` — **CONFIRMED**.
- Step [5] hidden-layer `Δw_ji` and stored `δ_j` — **CONFIRMED**.
- Step [6] recursion / reuse of next layer's δ — **CONFIRMED**.
- Symbol choice `O` for output and `η` for learning rate — **CONFIRMED** as a common
  textbook convention.
- PARSE COVERAGE: the parse transcript captured only the slide title for slide 022, so the
  algorithm text is not independently attested by the doc-parse lane — **NOT-VERIFIABLE**
  via the parse lane; the certified JSON + frame are the only evidence for the step wording.

New sources found during audit (real URLs, not previously cited):
- MIT OCW 9.641, "Lecture 20: Backprop" —
  https://ocw.mit.edu/courses/9-641j-introduction-to-neural-networks-spring-2005/5d46d3b6e32a5120fe9893193c31e926_lec20_backprop.pdf
  Gives `δ_j = (t_j − O_j)·O_j(1−O_j)` and `Δw = η·δ_j·O_i` for the output layer.
- Wikipedia, "Delta rule" — https://en.wikipedia.org/wiki/Delta_rule
- GeeksforGeeks, "Widrow-Hoff Algorithm" —
  https://www.geeksforgeeks.org/machine-learning/widrow-hoff-algorithm/
  Per-sample (online) weight update framing of step [2].

Audit summary: every formula and every algorithmic step on this slide is confirmed standard
and correctly stated. The only caveat is parse-lane coverage (title-only transcript).

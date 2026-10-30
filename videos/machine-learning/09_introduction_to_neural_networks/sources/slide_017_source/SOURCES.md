# SOURCES.md — slide 017 "Linear and Unit Step Activation Functions"

Preamble: mandated by videos/machine-learning/09_introduction_to_neural_networks/AGENTS.md; method agy web search + fetch + verification; frame facts from doc-parse crop cascade (nemotron-3.5-parse); vision transcripts banked separately.

## Slide identity

file: slide_017.jpg (md5 d6ee1efe236d6185814c6e02d7902587); badge number: 17 per approved slides_index.json

## Primary source(s)

- https://www.iitg.ac.in/cseweb/osint/slides/course1/Lesson%2013.pdf — academic course slides on neural networks, fetched live 2026-10-27
- https://www.ipb.uni-bonn.de/html/teaching/photo12-2021/2021-pho1-15-neural-networks-part1.pptx.pdf — university lecture slides, fetched live 2026-10-27
- https://medium.com/@sushmita2310/12-types-of-activation-functions-in-neural-networks-a-comprehensive-guide-a441ecefb439 — comprehensive guide article, fetched live 2026-10-27
- https://mohitmishra786687.medium.com/activation-functions-in-neural-networks-56dc526ad63c — technical article, fetched live 2026-10-27

## Figures used by this slide

The slide image shows two activation function plots (Linear and Unit Step) as the primary visual. The source slides (IIT Guwahati, Uni Bonn) contain similar comparison plots. No hosted original figure files downloaded — the slide's own frame is the ground truth for pixels and layout per discrepancy law.

## What the source(s) CONFIRM

### Linear Activation Function
- Formula: f(x) = cx (or simply f(x) = x for identity)
- Graph: straight diagonal line through origin
- Output range: (-∞, ∞)
- Derivative: constant (f'(x) = c)
- Limitation: no non-linearity; multiple layers collapse to single linear function; cannot solve XOR
- Use case: output layer for regression tasks

### Unit Step (Binary Step) Activation Function
- Formula: f(x) = 1 if x ≥ 0, else 0
- Graph: flat at 0 for x < 0, jumps to 1 at x = 0
- Binary output (0 or 1) based on threshold
- Mimics biological "all-or-none" neuron firing
- Limitation: zero gradient everywhere (undefined at 0); backpropagation fails; cannot handle multi-class
- Use case: early Perceptrons for binary classification

### Takeaway
Both functions lack properties for deep learning: Linear lacks complexity handling; Step cannot learn via gradient descent. Modern networks use ReLU, Sigmoid, Tanh.

## Course-authored elements (no source counterpart — do NOT "fix" to source)

- Slide numbering badge (17)
- Title formatting "Linear and Unit Step Activation Functions"
- Specific visual layout and color choices for the two plots
- Any pedagogical annotations or callouts on the original frame

## [?] Uncertain items

- Exact mathematical notation style on the original plots (inline vs. displayed)
- Whether the slide shows derivative formulas explicitly
- Specific colors used for the plot lines and axes

## Corrections

None — source content aligns with frame text extracted by doc-parse.

## Law reminder

The frame wins for recreation; the source wins for understanding.

## Wave-2 verification

Fresh independent web-verification pass (wave-3 dispatch, agent `src-017-020`). Content
evidence read first: `analysis/reanalysis_v2/slide_017_reanalysis.txt` is a **429-byte
abort stub** ("hard wall-clock 450s exceeded — call aborted"), i.e. below the 800-byte
threshold, so the fallback chain was used: `analysis/slide_017_final.json` plus
`sources/docparse_cascades/slide_017/composed/slide_017_composed.md` (2 elements kept,
1 crop, 0 failed calls, not degraded).

The doc-parse cascade is **advisory only** for this frame: it returned the whole slide
area as one `<class_Picture>` region and recovered only the title text
("Linear and Unit Step Activation Functions") and the badge "17" — no equation text.
The authoritative content source remains the vision analysis
(`analysis/slide_017_final.json`, verdict `PASS_WITH_FIXES`).

### Search lane note (honest reporting)

The `agy -p` CLI lane was used for the first query and returned **local workspace file
references instead of web URLs** (its grounded links resolved to
`file:///home/codespace/ai_llm_slides/.../slide_025_final.json` and the slide's own
`SOURCES.md`), so it is banked as `web/agy_q1_linear.txt` but is **not** citable as a
web source. Subsequent `agy -p` invocations returned
`RESOURCE_EXHAUSTED (429) Individual quota reached ... Resets in 154h21m56s`
(banked verbatim at `web/agy_q2_step.txt`). The same Google grounding backend was then
reached through the `agy_web_search` MCP route, which returned real resolved URLs.
This is the same lane split already recorded for slide 019 in wave 1.

Query texts banked under `web/`:
- `web/query_q1_linear.txt`
- `web/query_q2_step.txt`
- `web/query_q3_heaviside.txt`

### Confirmed by web research (3 independent query reads)

**Linear / identity activation `F(x) = x`**
- Definition, range `(-∞, ∞)`, derivative `f'(x) = 1` (constant for all real x) —
  matches the slide's top panel: a straight diagonal line through the origin extending
  into quadrants I and III, with the label "Linear (No Activation)".
- Stacking L hidden layers with linear activations collapses the network to a single
  affine map `ŷ = W_eff x + b_eff` with `W_eff = W_L ⋯ W_1`; depth adds **zero**
  representational power without a non-linearity.
- With MSE loss and a linear output layer the gradient is exactly the residual
  `(ŷ − y)`, with no derivative plateau — the standard reason the identity activation
  is the normal choice for a **regression output layer**.
- XOR is not linearly separable: the four hyperplane inequalities are mutually
  inconsistent, and since a deep linear net collapses to one hyperplane, a linear
  network cannot solve XOR at any depth.
- URLs: https://www.playwithml.com/projects/xor ·
  https://master-engineer.com/2026/04/18/why-perceptrons-fail-on-xor/ ·
  https://medium.com/@aryanrusia8/the-limitations-of-perceptron-why-it-struggles-with-xor-21905d31f924 ·
  https://www.innovatiana.com/en/glossary/xor-problem

**Unit step (binary / Heaviside) — unipolar and bipolar**
- Unipolar: `f(x) = 1 if x ≥ 0 else 0`; Bipolar: `f(x) = +1 if x ≥ 0 else −1` —
  **exactly** the two piecewise definitions printed on the slide's lower two panels.
- The step function is entirely flat away from the threshold: `dH/dz = 0` for `z ≠ 0`
  and **undefined at `z = 0`**, so gradient descent receives no signal and the weights
  are never updated — the step function is unusable for backpropagation.
- Historical use: Rosenblatt's **Perceptron** used exactly this binary threshold rule
  as a linear two-class classifier; it models the biological "all-or-none" firing law
  of an action potential (the McCulloch–Pitts neuron, 1943, uses the same Heaviside
  threshold with threshold/bias folded into the weighted sum).
- Threshold is not always 0 — it can be a bias/threshold parameter `θ`; the slide's
  `x ≥ 0` convention corresponds to threshold 0.
- URLs: https://www.analyticsvidhya.com/blog/2022/01/activation-functions-for-neural-networks-and-their-implementation-in-python/ ·
  https://towardsdatascience.com/the-concept-of-artificial-neurons-perceptrons-in-neural-networks-fab22249cbfc/ ·
  https://sefiks.com/2017/05/15/step-function-as-a-neural-network-activation-function/ ·
  https://www.ee.cityu.edu.hk/~lmpo/ee4016/pdf/2026_AI_L02A_Perceptron.pdf ·
  https://en.wikipedia.org/wiki/Artificial_neuron ·
  https://people.revoledu.com/kardi/tutorial/NeuralNetwork/ActivationFunctions.html

### Corrections / clarifications

1. The wave-1 note "Formula: f(x) = cx (or simply f(x) = x for identity)" is
   **confirmed and narrowed**: the slide's own label is the identity form `F(x) = x`
   (slope 1), and the "Linear (No Activation)" label matches the standard
   identity/"no activation" naming.
2. The wave-1 note "zero gradient everywhere (undefined at 0)" is **confirmed** and
   sharpened: the derivative is `0` for all `x ≠ 0` and undefined exactly at `x = 0`,
   which is the precise reason gradient descent fails rather than a general
   "unstable-gradient" claim.
3. No correction needed to the frame's color/geometry facts (red curve `#FF0000`, blue
   `#4169E1` panel borders, red italic axis label `x`). Those are frame facts and the
   law above applies.

### [?] Uncertain items (unchanged)

- Exact mathematical notation style on the original plots (inline vs. displayed).
- Whether the slide shows derivative formulas explicitly — the frame shows no
  derivative formulas, so the recreation must not add them.
- Specific plot-line colors are frame facts; no web source states them.

### Research status

- Doc-parse cascade: ✅ complete (advisory only — no equation text recovered)
- Web search: ✅ complete (3 query reads; `agy -p` CLI succeeded once, then quota-
  exhausted; MCP route over the same grounding backend supplied the cited URLs)
- Sources banked: ✅ yes
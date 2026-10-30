# Source Research: slide_025

## Doc-Parse Transcript (nemotron-3.5-parse)

**Run**: `sources/slide_025_source/docparse_run/`
- Full frame parse: `full/slide_025.parse.md`
- Composed: `composed/slide_025_composed.md`
- Crop cascade: 6 crops (title zone, plot regions, formula region)
- Chat lane: DEGRADED (model `docparsechat` HTTP 404 on gateway) — deterministic-conservative fallback used
- Source frame md5: `a82380b2460d1b93d2a3e0e52bedea34`

## Extracted Content (verbatim)

### Slide Title
**Linear and Unit Step Activation Functions**
(badge 17)

### Layout
Three plot panels stacked vertically, each a small f(x)-vs-x graph:
1. **Top panel** — `F(x) = x` — *Linear (No Activation)* — a diagonal line through the origin
2. **Middle-left panel** — unipolar unit step curve with formula text below
3. **Middle-right panel** — bipolar unit step curve with formula text below
   (middle-left panel has no text caption; it is the curve plot only)
4. **Bottom row** — two formula captions

### Formulas (verbatim)
- `F(x) = x` — *Linear (No Activation)*
- `F(x) = Uni-polar Unit Step = 0 for x<0, 1 for x≥0`
- `F(x) = Bi-polar Unit Step = 1 for x<0, 1 for x≥0` ← parse of `-1` as `1`; LaTeX crop
  reads `-1 for x<0`. The bipolar step outputs **−1** for x<0 (OCR artifact).
  Correct reading: `F(x) = Bi-polar Unit Step = -1 for x<0, 1 for x≥0`

### Un-positioned / decorative
- Badge numeral 17 in yellow circle (top-right)
- No footer text captured on this frame

---

## Web Search Verification

### Concepts to verify
1. Linear (identity) activation: f(x) = x
2. Unipolar / binary unit step: 1 for x≥θ, 0 for x<θ
3. Bipolar unit step: 1 for x≥θ, −1 for x<θ

### Search Results

**Activation function families** [[1]](https://kobiso.github.io/research/research-activation-functions/) [[4]](https://machinelearninggeek.com/activation-functions/)
- Linear/identity passes input unchanged: **f(x) = x** (optionally scaled f(x) = ax)
- Linear activations collapse stacked layers into one linear map — no non-linearity
- Primary role: regression output layers

**Unit Step (Binary Step / Unipolar)** [[6]](https://www.ques10.com/p/39243/activation-functions-in-detail-1/) [[3]](https://www.analyticsvidhya.com/blog/2022/01/activation-functions-for-neural-networks-and-their-implementation-in-python/)
- Threshold function: 1 if x ≥ θ, 0 if x < θ; unipolar {0,1} output range
- Historical: McCulloch–Pitts neuron, Rosenblatt Perceptron (1958)
- Derivative is 0 a.e. and undefined at θ → **backpropagation cannot train** step-activation networks
- This is the core limitation that motivated sigmoid/soft/ReLU families

**Bipolar Step** [[2]](https://www.scribd.com/document/595499875/SC-exp1-Shruti) [[9]](https://bbrc.in/deep-learning-techniques-and-their-applications-a-short-review/)
- +1 if x ≥ θ, **−1** if x < θ → range {−1,+1}
- Useful when targets are zero-centered / bipolar representations
- Same non-differentiability limitation as unipolar step

**General activation-function reference** [[7]](https://en.wikipedia.org/wiki/Activation_function)
- Canonical classification: linear vs non-linear, threshold vs continuous

### Verified formulas

| Function | Verbatim | Web-verified canonical form |
|---|---|---|
| Linear (no activation) | f(x) = x | f(x) = x ✓ (identity) |
| Uni-polar unit step | 0 for x<0, 1 for x≥0 | f(x)=1 if x≥0 else 0 ✓ |
| Bi-polar unit step | −1 for x<0, 1 for x≥0 | f(x)=1 if x≥0 else −1 ✓ |

---

## Research Summary

Slide 17 (unique-slide 025) shows the three earliest activation functions, one plot each:
a straight identity line, a 0/1 threshold curve, and a −1/+1 threshold curve.
The slide carries **no numeric data, no learning curve, no trained model output** — the
plots are schematic function curves and must be recreated as matplotlib line plots
(f(x) vs x), not as fitted data.

Key content facts for the recreation:
- Title verbatim: `Linear and Unit Step Activation Functions`
- Badge: **17** (house rule: printed number, not slide index)
- 3 function plots: identity line, unipolar step, bipolar step
- Formulas below the plots, in 2D (cases) format per the equation rule

### Uncertain Items (marked [?])
- Bipolar-step text: doc-parse rendered `1 for x<0` in one lane; the LaTeX lane and
  web sources both give −1. Treated as **−1** (corroborated).
- Axis tick labels / axis ranges on the plots — not recoverable from parse; approximate
  (x in [−3,3], f(x) ticks at −1/0/1) pending vision measurement.

---
*Generated: 2026-10-27*

---

## Wave-2 verification (2026-10-28)

**Content evidence**: `analysis/reanalysis_v2/slide_025_reanalysis.txt` did not exist at
research time (orchestrator's fresh vision re-analysis for 025–028 not yet produced);
fell back per mandate to `analysis/slide_025_final.json` (vision model `images`,
validated by `validate_slides`, verdict PASS_WITH_FIXES, recreatability 9/10).
DOC-parse Wave-1 section above left unchanged.

**Search note**: the `agy` CLI is quota-exhausted (HTTP 429 "Individual quota reached",
resets ~29h). Web verification for this wave ran through the equivalent agy web-search
MCP route (same Google grounding, same citation discipline). All URLs below are real,
returned by the search service — none invented.

**Slide content summary** (from fresh vision analysis): badge 17 in yellow circle
top-right; red-bordered graph boxes; top graph = identity line through origin with a
red X annotation above a peach equation box; bottom-left graph = unipolar step;
bottom-right graph = bipolar step. Verbatim equations:
`F(x) = x    Linear (No Activation)`,
`F(x) = Uni-polar Unit Step = { 0 for x<0 ; 1 for x ≥ 0 }`,
`F(x) = Bi-polar Unit Step = { −1 for x<0 ; 1 for x ≥ 0 }`.

### Claim-by-claim verification

| # | Claim (verbatim from frame) | Verdict | Wave-2 evidence |
|---|---|---|---|
| 1 | `F(x) = x` — Linear (No Activation) | CONFIRMED | Linear/identity activation passes the input through unchanged, f′(x) = 1, range unbounded; canonical in regression output layers [[1]](https://medium.com/@sushmita2310/12-types-of-activation-functions-in-neural-networks-a-comprehensive-guide-a441ecefb439) [[2]](https://www.coursera.org/in/articles/activation-function-neural-network) |
| 2 | `F(x) = Uni-polar Unit Step = { 0 for x<0 ; 1 for x ≥ 0 }` | CONFIRMED | Threshold function: 1 if x ≥ 0, else 0; range {0,1}; original Perceptron activation [[1]](https://medium.com/@sushmita2310/12-types-of-activation-functions-in-neural-networks-a-comprehensive-guide-a441ecefb439) [[4]](https://www.jeremyjordan.me/neural-networks-activation-functions/) |
| 3 | `F(x) = Bi-polar Unit Step = { −1 for x<0 ; 1 for x ≥ 0 }` | CONFIRMED | Symmetric ±1 threshold: 1 if x ≥ 0, else −1; range {−1,1}; preferred where zero-centered bipolar representation is wanted [[5]](https://www.youtube.com/watch?v=bFNcH6g3GZU) |
| 4 | Implicit: three plots are schematic function curves | CONFIRMED | Identity line, 0/1 step, and −1/+1 step are textbook schematic curves; no fitted data exists behind them — recreate as matplotlib line plots |

**Wave-1 OCR ambiguity resolved**: the doc-parse rendered the bipolar case as
`1 for x<0`; two independent OCR reads plus Wave-2 web sources confirm **−1**.
Frame text stays verbatim; the −1 reading is corroborated (also stated in Wave-1).

**Additional DATA-level note (no frame-text change)**: step-activation networks
cannot be trained by backpropagation — f′(x) = 0 a.e. and undefined at the threshold,
so no gradient signal flows [[4]](https://www.jeremyjordan.me/neural-networks-activation-functions/).
The Perceptron instead used the perceptron learning rule. This is the conceptual
motivation for the sigmoid/tanh slides that follow (026). Useful for slide notes; NOT
printed on the frame.

### Build guidance (DATA-level, recreation may use)
- Step plateau heights: the graphs carry no numeric ticks in the fresh analysis; the
  plateau levels y = 1 (unipolar) and y = ±1 (bipolar) derive from the paired
  equations, not from axis readings (analysis `validation.uncertain_items` agrees).
- Render equations in Professional Format (2D cases) per the house equation rule.

### Wave-2 sources banked (new this wave)
1. https://medium.com/@sushmita2310/12-types-of-activation-functions-in-neural-networks-a-comprehensive-guide-a441ecefb439
2. https://www.coursera.org/in/articles/activation-function-neural-network
3. https://www.scribd.com/document/892945478/Unit-1-Part-II-nn
4. https://www.jeremyjordan.me/neural-networks-activation-functions/
5. https://www.youtube.com/watch?v=bFNcH6g3GZU
6. https://www.articsledge.com/post/output-layer-neural-network
7. https://www.enjoyalgorithms.com/blog/how-to-choose-activation-function-for-output-layer/
8. https://stats.stackexchange.com/questions/218542/which-activation-function-for-output-layer
9. https://medium.com/@david_55326/understanding-linear-layer-collapse-how-neural-networks-fail-8ffe735cea1f
10. https://developers.google.com/machine-learning/crash-course/neural-networks/activation-functions

### Uncertain items (marked [?])
- **Badge numeral**: fresh vision reads **17**; `slides_index.json` maps
  `slide_025.jpg` → badge `25`. Both readings cited; builder must confirm against
  the frame per the house badge rule (not resolvable from text alone).
- Axis ranges/tick values on the three plots — not recoverable from parse; keep
  schematic (x ≈ [−3,3], ticks at −1/0/1) pending vision measurement.

---

## Wave-3 verification (2026-10-30)

**Content evidence**: `analysis/reanalysis_v2/slide_025_reanalysis.txt` still does
not exist (the orchestrator's v2 re-analysis has landed only for slides 001–017),
so per the mandate this wave fell back to `analysis/slide_025_final.json`
(vision model `images`, `validate_slides` verdict PASS_WITH_FIXES) plus
`sources/docparse_cascades/slide_025/composed/slide_025_composed.md`. The
Wave-1 and Wave-2 sections above are unchanged.

**Search transport (honest note)**: `agy -p` CLI ran successfully for 3 of the
queries (raw transcripts: `sources/slide_025_source/agy_wave3/search_01_linear_and_step.txt`,
`search_02_bipolar_step.txt`, `search_03_step_not_differentiable.txt`; those CLI
answers contain no inline citation URLs, so they are banked as raw evidence only).
A 4th CLI call hit per-user quota HTTP 429 (`search_04_history.txt` = the 429
error). The remaining queries ran through the **agy web-search MCP** — the same
Google grounding service, different transport — and every URL cited below is one
that service returned; none are invented. Full query list, findings, and URL
list: `sources/slide_025_source/agy_wave3/wave3_notes.md`.

### Claim-by-claim verification (wave 3)

| # | Claim (verbatim from frame) | Verdict | Wave-3 evidence |
|---|---|---|---|
| 1 | `F(x) = x    Linear (No Activation)` | CONFIRMED | Identity activation passes input through unchanged, range (−∞,∞), f′(x)=1; stacking identity layers collapses to a single linear map; used in regression output layers — CLI `search_01` + [[1]](https://iq.opengenus.org/binary-step-function/) [[2]](https://www.analyticsvidhya.com/blog/2022/01/activation-functions-for-neural-networks-and-their-implementation-in-python/) |
| 2 | `F(x) = Uni-polar Unit Step = { 0 for x<0 ; 1 for x ≥ 0 }` | CONFIRMED | Threshold function 1 if x ≥ 0 else 0, range {0,1}; derivative 0 for x ≠ 0 and undefined at x = 0 → not trainable by backpropagation — CLI `search_01`/`search_03` + [[3]](https://iq.opengenus.org/binary-step-function/) [[4]](https://datascience.stackexchange.com/questions/28037/backpropagation-with-step-or-threshold-activation-function) |
| 3 | `F(x) = Bi-polar Unit Step = { −1 for x<0 ; 1 for x ≥ 0 }` | CONFIRMED | Signum/bipolar step: +1 if x ≥ 0, −1 if x < 0, range {−1,+1}; zero-centred ⇒ mixed-sign gradients, balanced updates, faster convergence — CLI `search_02` + [[5]](https://www.guvi.in/blog/bipolar-sigmoid-function-in-neural-networks/) [[6]](https://mohitmishra786687.medium.com/activation-functions-in-neural-networks-56dc526ad63c) [[7]](https://www.datacamp.com/tutorial/introduction-to-activation-functions-in-neural-networks) |
| 4 | Implicit: the three panels are schematic function curves | CONFIRMED | Identity line, 0/1 threshold and ±1 threshold are textbook schematic curves with no fitted data behind them — recreate as matplotlib line plots, not charts of measured values |
| 5 | Implicit historical context of step activations | CONFIRMED (context only) | McCulloch–Pitts neuron (1943) used unipolar {0,1} with fixed weights; Rosenblatt's perceptron (1958) learned weights under a hard-limiter step (0/1 or −1/+1); update rule `w ← w + η·y·x` for y ∈ {−1,+1} — [[8]](https://en.wikipedia.org/wiki/Perceptron) [[9]](https://machinelearning.uchicago.edu/history/) [[10]](https://mbrenndoerfer.com/writing/history-perceptron-neural-network-foundation) [[11]](https://home.csulb.edu/~cwallis/artificialn/History.htm) |

**Wave-1 OCR ambiguity stays resolved as −1**: the doc-parse lane that rendered
`1 for x<0` for the bipolar case is contradicted by the LaTeX crop lane, by the
Wave-2 sources, and again by this wave's independent sources
[[5]](https://www.guvi.in/blog/bipolar-sigmoid-function-in-neural-networks/).
Frame text is reproduced verbatim in the recreation; the −1 reading is corroborated.

**Additional DATA-level note (no frame-text change)**: the backpropagation
incompatibility is now triple-sourced — f′ = 0 a.e. and undefined at the
threshold collapse the chain-rule product, so weights receive no update
[[4]](https://datascience.stackexchange.com/questions/28037/backpropagation-with-step-or-threshold-activation-function)
[[12]](https://en.wikipedia.org/wiki/Backpropagation)
[[13]](https://blog.devops.dev/exploring-activation-functions-in-deep-learning-properties-derivatives-and-impact-on-model-7585aad8a757).
This is the conceptual bridge to the sigmoid/tanh slide that follows (026);
it is NOT printed on the frame.

### Wave-3 sources banked (new this wave)
1. https://www.analyticsvidhya.com/blog/2022/01/activation-functions-for-neural-networks-and-their-implementation-in-python/
2. https://mohitmishra786687.medium.com/activation-functions-in-neural-networks-56dc526ad63c
3. https://www.guvi.in/blog/bipolar-sigmoid-function-in-neural-networks/
4. https://www.datacamp.com/tutorial/introduction-to-activation-functions-in-neural-networks
5. https://adl1995.github.io/an-overview-of-activation-functions-used-in-neural-networks.html
6. https://ai.stackexchange.com/questions/48981/why-function-of-a-neuron-need-to-be-in-range-1-1-or-0-1
7. https://datascience.stackexchange.com/questions/28037/backpropagation-with-step-or-threshold-activation-function
8. https://iq.opengenus.org/binary-step-function/
9. https://en.wikipedia.org/wiki/Backpropagation
10. https://towardsdatascience.com/backpropagation-step-by-step-derivation-99ac8fbdcc28/
11. https://blog.devops.dev/exploring-activation-functions-in-deep-learning-properties-derivatives-and-impact-on-model-7585aad8a757
12. https://medium.com/@lmpo/the-evolution-of-artificial-neurons-90619f224f63
13. https://mbrenndoerfer.com/writing/history-perceptron-neural-network-foundation
14. https://machinelearning.uchicago.edu/history/
15. https://com-cog-book.github.io/com-cog-book/features/perceptron.html
16. https://home.csulb.edu/~cwallis/artificialn/History.htm
17. https://www.cs.ucdavis.edu/~vemuri/classes/ecs170/neuralnets_files/neural-networks.htm
18. https://en.wikipedia.org/wiki/Perceptron
19. https://www.pearsonhighered.com/assets/samplechapter/0/1/3/1/0131471392.pdf

### Uncertain items (marked [?]) — wave 3
- **Badge numeral**: still unresolved between the fresh-vision reading **17** and
  `slides_index.json` (`slide_025.jpg` → badge `25`). Web research cannot settle
  this; the builder must read the numeral off the frame per the house badge rule.
- Axis ranges/tick values on the three plots — still unrecovered; keep schematic.
- The doc-parse `composed/` file for 025 recovers only the title text (the graph
  panels were treated as one picture element), so all geometry here rests on
  `slide_025_final.json` + vision; not resolvable from text evidence.

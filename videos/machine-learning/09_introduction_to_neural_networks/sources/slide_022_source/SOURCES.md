# Slide 022 Source Research

## Doc-Parse Transcript (slide_022.parse.md)

```
<x_0.2051><y_0.1062>**Derivatives of some Activation Functions**<x_0.7705><y_0.157><class_Section-header>

<x_0.8916><y_0.0969>22<x_0.9326><y_0.1625><class_Page-header>

<x_0.0742><y_0.2062>f(x)= Re ctified Linear U nit = 0 for x<0
x for x≥0 Derivative f'(x)= 0 for x<0
f(x)= P arametric ReLU = α x for x≤0 + Derivative f'(x)= 1 for x≥0
f(x)= Exponential LU = α ( e^X-1 ) for x<0 for x≥0
f(x)= SoftPlus= loge (1+e^x)<x_0.9336><y_0.9414><class_Picture>
```

## Web Search: Activation Function Derivatives

**Query**: "derivatives of activation functions ReLU Leaky ReLU PReLU ELU SoftPlus derivative formulas f'(x) piecewise functions"

**Key Findings**:

1. **ReLU (Rectified Linear Unit)**:
   - f(x) = max(0, x) = { x for x > 0; 0 for x ≤ 0 }
   - f'(x) = { 1 for x > 0; 0 for x < 0 } (at x=0, conventionally 0 or 1)

2. **Leaky ReLU**:
   - f(x) = { x for x > 0; αx for x ≤ 0 } (α typically 0.01)
   - f'(x) = { 1 for x > 0; α for x < 0 }

3. **PReLU (Parametric ReLU)**:
   - f(x) = { x for x > 0; ax for x ≤ 0 } (a is learnable parameter)
   - f'(x) = { 1 for x > 0; a for x < 0 }

4. **ELU (Exponential Linear Unit)**:
   - f(x) = { x for x > 0; α(e^x - 1) for x ≤ 0 } (α > 0, usually 1.0)
   - f'(x) = { 1 for x > 0; αe^x for x ≤ 0 }
   - Alternative form for x ≤ 0: f'(x) = f(x) + α

5. **Softplus**:
   - f(x) = ln(1 + e^x)
   - f'(x) = 1 / (1 + e^(-x)) = sigmoid(x) (smooth approximation of ReLU derivative)

**Sources**:
- [1] github.io - Deep Learning activation functions
- [2] eulerpad.app - Activation functions and their derivatives
- [3] ic.ac.uk - DL activation and losses
- [4] readthedocs.io - ML cheatsheet activation functions

## Key Equations from Slide (Verbatim from Vision Analysis)

1. **Rectified Linear Unit (ReLU)**:
   - f(x) = { 0 for x < 0; x for x ≥ 0 }
   - f'(x) = { 0 for x < 0; 1 for x ≥ 0 }

2. **Parametric ReLU**:
   - f(x) = { αx for x < 0; x for x ≥ 0 } +
   - f'(x) = { α for x < 0; 1 for x ≥ 0 }

3. **Exponential LU (ELU)**:
   - f(x) = { α(e^x - 1) for x < 0; x for x ≥ 0 }
   - f'(x) = { f(x) + α for x < 0; 1 for x ≥ 0 }

4. **SoftPlus**:
   - f(x) = log_e(1 + e^x)
   - f'(x) = 1 / (1 + e^(-x)) (vertical fraction)

## Notes for Analysis

- Slide title: "Derivatives of some Activation Functions"
- Slide number: 22 (printed on slide as "22")
- Contains mathematical equations requiring Professional Format (2D) rendering
- Doc-parse has OCR issues: "Re ctified Linear U nit" → "Rectified Linear Unit", "P arametric" → "Parametric"
- "Exponential LU" = ELU (Exponential Linear Unit) — slide uses α(e^x - 1) for x<0, derivative uses f(x) + α form
- "SoftPlus" = Softplus, derivative is vertical fraction 1/(1+e^(-x))
- Parametric ReLU has trailing "+" after closing brace — retained verbatim
- Equations need matplotlib mathtext → PNG 600dpi for Professional Format
- Layout: 4 rows, each with left box (function), center "Derivative ⇒", right box (derivative)
- Colors: light yellow box fill (#ffffe0), red border left (#c00000), blue border right (#0000cc), red text for function names, green for conditions (x≥0), black body text
---

## Wave-2 verification (2026-10-28)

### Slide content (from the fresh vision re-analysis)

`analysis/slide_022_final.json` — title **"Derivatives of some Activation Functions"**,
badge 22, a white blue-bordered container divided into four horizontal rows. Each row has
three parts: left box (function definition), centre "Derivative =>", right box (derivative).
The slide gives **four function/derivative pairs**.

Note: wave-1's doc-parse transcript jumbled the rows' left-hand sides with the right-hand
sides (e.g. it merged `f(x)=... for x<0` with the following row's `f'(x)=...`). The fresh
vision analysis resolves each row cleanly and is used below.

### Claim-by-claim verification

1. **ReLU derivative `f'(x) = { 0 for x<0 ; 1 for x>=0 }`** — CONFIRMED.
   For `x > 0` the derivative is 1; for `x < 0` it is 0; at `x = 0` it is technically
   undefined (frameworks conventionally assign 0 or 1). The slide's statement is the
   standard textbook form.
   - "The Dying ReLU Problem" — Medium (@MrBam44):
     https://medium.com/@MrBam44/the-dying-relu-problem-causes-and-solutions-1a970f177c
   - DeepLearning.AI community, "regarding derivative of ReLU activation function":
     https://community.deeplearning.ai/t/regarding-derivative-of-relu-activation-function/115254
   - "What is the dying ReLU problem?" — Data Science StackExchange:
     https://datascience.stackexchange.com/questions/5706/what-is-the-dying-relu-problem-in-neural-networks

2. **ReLU's positive-side derivative is a constant 1 (no vanishing gradient for x>0)** —
   CONFIRMED. This is the property that makes ReLU trainable in deep nets, and the
   motivation for the three variants on the same slide.
   - "To ReLU or not to ReLU" — Towards AI:
     https://pub.towardsai.net/to-relu-or-not-to-relu-a-practitioners-guide-to-solve-the-zombie-neuron-problem-in-deep-89a050a6b25b
   - ReLU Activation Function in Deep Learning — GeeksforGeeks:
     https://www.geeksforgeeks.org/deep-learning/relu-activation-function-in-deep-learning/

3. **Parametric ReLU `f(x) = { alpha*x for x<0 ; x for x>=0 }`** — CONFIRMED (wave-1
   already had this right). The alpha is a **learnable** parameter, distinct from Leaky
   ReLU's fixed hyperparameter.
   - Imperial College London, "DL activation and losses":
     https://www.doc.ic.ac.uk/~bkainz/teaching/DL/L03_DL_activation_and_losses.pdf
   - "PReLU Activation Function" — Medium (@shauryagoel):
     https://medium.com/@shauryagoel/prelu-activation-e294bb21fefa

4. **Parametric ReLU derivative `f'(x) = { alpha for x<0 ; 1 for x>=0 }`** — CONFIRMED.
   - Imperial College London (above); Medium/@shauryagoel (above).
   - Also `df/da = { x for x<0 ; 0 for x>=0 }` (needed to learn alpha) — same sources.

5. **ELU `f(x) = { alpha (e^x - 1) for x<0 ; x for x>=0 }`** — CONFIRMED.
   - "ELU as a Neural Network's Activation Function" — Sefiks:
     https://sefiks.com/2018/01/02/elu-as-a-neural-networks-activation-function/
   - "ELU Activation Function" — MLForBeginners:
     https://mlforbeginners.com/elu-activation-function/
   - arXiv 1704.07483v1: https://arxiv.org/html/1704.07483v1

6. **ELU derivative `f'(x) = { f(x) + alpha for x<0 ; 1 for x>=0 }`** — CONFIRMED, and
   this is the *non-obvious* one worth recording. The direct derivative is
   `f'(x) = alpha*e^x` for `x < 0`; rewriting it in terms of the function's own output:
   `alpha*e^x = alpha*e^x - alpha + alpha = alpha(e^x - 1) + alpha = f(x) + alpha`.
   The slide's `f(x) + alpha` form is exactly this identity. Step-by-step derivation:
   - Sefiks (above) — this is the source that carries the `f(x) + alpha` rewrite.

7. **SoftPlus `f(x) = log_e (1 + e^x)`** — CONFIRMED. `Softplus(x) = ln(1 + e^x)`.
   - "Softplus Function in Neural Network" — GeeksforGeeks:
     https://www.geeksforgeeks.org/deep-learning/softplus-function-in-neural-network/
   - "Softplus" — DataCamp: https://www.datacamp.com/tutorial/softplus

8. **SoftPlus derivative `f'(x) = 1 / (1 + e^(-x))`** — CONFIRMED. This is not merely an
   alternative spelling: the derivative of Softplus **is** the logistic sigmoid
   `sigma(x) = 1/(1+e^{-x})`, obtained from `e^x/(1+e^x)` by dividing numerator and
   denominator by `e^x`. The slide renders it as a vertical fraction.
   - GeeksforGeeks (above); DataCamp (above); Neura.Market:
     https://www.neura.market/directories/chatgpt/blog/softplus-activation-function-the-smooth-powerful-relu-alternative-every-ml-engineer-needs

9. **Why these three variants exist (context, CONFIRMED)** — ReLU's derivative is 0 on
   the whole negative half-line, which causes the "dying ReLU" / dead-neuron problem.
   Leaky ReLU, PReLU and ELU all keep a non-zero gradient for negative inputs:
   - "The Dying ReLU Problem" — Medium (@MrBam44) (above);
   - "What is the dying ReLU problem?" — Data Science StackExchange (above).
   This is the pedagogical spine of slides 021-022 as a sequence.

### Uncertain items carried forward (DO NOT resolve from sources)

- **Trailing `+` after the Parametric ReLU closing brace.** It appears consistently in the
  equations, visual_elements and original brief, but no source explains it. It may be a
  stray annotation or a build artifact. Kept verbatim; not corrected.
- The relative placement of the word "Derivative" vs the `=>` arrow (stacked vs inline)
  is not specified by the source; the brief assumes the arrow directly below the word.
- Font sizes are recreation guidance, not measurements.

### Research method

- Web search: agy CLI quota-exhausted; all searches run through the **agy MCP web-search
  tool** (Google grounding, redirects resolved to real page URLs). 4 searches run for this
  slide's concepts (PReLU; ELU; SoftPlus; ReLU derivative). All URLs above were returned
  by the tool — none invented.
- Content evidence: `analysis/slide_022_final.json`, plus
  `sources/docparse_cascades/slide_022/composed/slide_022_composed.md` (nemotron-3.5-parse,
  2 parse calls + 1 chat call, 0 failures).

---

## Wave-2 verification (wave-3 dispatch, agent src-021-024, 2026-10-30)

Content evidence used: `analysis/reanalysis_v2/slide_022_reanalysis.txt` is MISSING, so per
mandate fell back to `analysis/slide_022_final.json` (title "Derivatives of some Activation
Functions"; 4 rows: ReLU, PReLU, ELU, SoftPlus, each `f(x) = ...  Derivative => f'(x) = ...`)
and `sources/docparse_cascades/slide_022/composed/slide_022_composed.md`.

Search method: `agy -p` CLI quota-exhausted (429, reset ~154h), so the 4 searches ran through
the agy MCP web-search tool (Google grounding, redirects resolved). All URLs returned by the
tool — none invented. Raw log: `wave3_agy/search_log.md`.

### Verified claims (wave-2)

1. **ReLU derivative `f'(x) = { 0 for x<0 ; 1 for x>=0 }` (undefined at 0; frameworks pick 0 or
   1)** — CONFIRMED.
   - https://en.wikipedia.org/wiki/Rectified_linear_unit
   - https://machinelearningmastery.com/rectified-linear-activation-function-for-deep-learning-neural-networks/
2. **PReLU derivative `f'(x) = { alpha for x<0 ; 1 for x>=0 }`, plus parameter gradient
   `df/dalpha = { x for x<=0 ; 0 for x>0 }` used to learn alpha** — CONFIRMED.
   - https://arxiv.org/abs/1502.01852
   - https://www.microsoft.com/en-us/research/publication/delving-deep-into-rectifiers-surpassing-human-level-performance-on-imagenet-classification/
3. **ELU derivative `f'(x) = { f(x)+alpha for x<0 ; 1 for x>=0 }`** — CONFIRMED, with the exact
   identity the slide uses: `alpha*e^x = f(x) + alpha` because `f(x) = alpha*e^x - alpha` for
   x<0, so the backprop form reuses the cached forward output instead of re-evaluating exp.
   - https://arxiv.org/html/1704.07483v1
   - https://serengil.wordpress.com/2018/01/02/elu-as-a-neural-networks-activation-function/
4. **SoftPlus derivative `f'(x) = e^x/(1+e^x) = 1/(1+e^-x) = sigmoid(x)`** — CONFIRMED with the
   full chain-rule derivation (multiply top/bottom by e^-x).
   - https://www.analyticsvidhya.com/blog/2025/12/softplus-activation-function/
   - https://www.datacamp.com/tutorial/softplus
5. **Pedagogical spine of slides 021-022: ReLU's zero negative-side gradient causes the dying-ReLU
   problem; Leaky/PReLU/ELU keep a non-zero negative gradient** — CONFIRMED.
   - https://towardsdatascience.com/the-dying-relu-problem-clearly-explained-42d0c54e0d24/
   - https://datascience.stackexchange.com/questions/5706/what-is-the-dying-relu-problem-in-neural-networks
   - https://medium.com/@MrBam44/the-dying-relu-problem-causes-and-solutions-1a970f177c

### Unchanged uncertain items

- The trailing `+` after the PReLU closing brace on the slide stays verbatim; no source explains
  it and it is not corrected.

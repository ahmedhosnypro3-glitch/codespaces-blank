# Source Research: slide_028

## Doc-Parse Transcript (nemotron-3.5-parse)

**Run**: `sources/slide_028_source/docparse_run/`
- Full frame parse: `full/slide_028.parse.md`
- Composed: `composed/slide_028_composed.md`
- Crop cascade: 5 crops (dense network diagram)
- Chat lane: DEGRADED (model `docparsechat` HTTP 404 on gateway) — deterministic-conservative fallback used
- Source frame md5: `3ec4323fe7f93e46819f7fd7dea31c10`

## Extracted Content (verbatim)

### Slide Title
**Neural Network Model** (badge 28)

### Diagram elements (cross-pass merge, most complete pass = crop01)
```
Input Sample
Target Label
Net_i    Net_j    Net_k
Oi  W_ji  Σ  Oj  w_kj    (with Σ symbols on inputs)
Output 1   Class 1
W_ji  W_kj     Output 2   Class 2
Ok    Output m   Class m
O_i    O_i    O_j    O_k
i      j      k
Previous Layer  |  Current Layer (You are here)  |  Next Layer  |  Layer (K)
I/P Layer  |  Hidden Layer (s)  |  O/P Layer
```

### Interpretation
The diagram shows a **feedforward neural network slice** with:
- **Left column (Previous Layer / I/P Layer)**: neurons indexed `i`, `j`, `k` with outputs `O_i`, `O_j`, `O_k`
- **Middle column (Current Layer, "You are here" / Hidden Layer(s))**: neurons computing `Net_i`, `Net_j`, `Net_k` — each is the **weighted sum** `Net = Σ(w·O) + b`, with summation symbol `Σ`
- **Weights on edges**: `W_ji` (from j to i), `W_kj` (from k to j) etc.
- **Right column (Next Layer / O/P Layer)**: `Output 1 = Class 1`, `Output 2 = Class 2`, `Output m = Class m` — a **classification** output with m classes
- **Target Label**: top-right — the ground-truth class for the Input Sample
- Arrows: left-to-right (feedforward)

### Reading order note
The parse mixes diagram labels (Net_i, W_ji, Σ, class labels) because it is a figure, not prose text. OCR on math subscripts (`Net_i` → `Neti`) is expected.

---

## Web Search Verification

### Single-neuron computation [[1]](https://medium.com/@anushruthikae/basic-notations-and-representation-neural-networks-d46a1be97471) [[2]](https://bookdown.org/benjaminhuang910/neural_net_scratch/single-layer-nn-notes.html)

- **Net input**: `Net_i = z_i = Σ_j w_ji x_j + b_i` — the weighted sum plus bias
  - subscript convention: `w_ji` = weight **from neuron j (previous layer) to neuron i (current layer)** ✓ matches diagram
- **Activated output**: `O_i = a_i = f(Net_i)` — output of neuron i after activation
- The diagram's `Σ` symbols sit at the weighted-sum junction ✓ consistent with `Net_i = Σ w·O`

### Layer semantics [[3]](https://apxml.com/courses/introduction-to-deep-learning/chapter-2-activation-functions-architecture/network-layers-overview) [[4]](https://developers.google.com/machine-learning/crash-course/neural-networks/nodes-hidden-layers) [[5]](https://datasciocean.com/en/ai-concept/what-is-neural-network/)

- **I/P (input) Layer**: pass-through, no computation ✓ matches "Previous Layer"
- **Hidden Layer(s)**: compute weighted sums + activation ✓ matches "Current Layer (You are here)" — the highlight emphasizes this is where learning happens
- **O/P (output) Layer**: final prediction; for classification, one output per class (softmax/sigmoid) ✓ matches `Output 1..m ↔ Class 1..m`

### Weight notation
- `W_ji` uppercase appears in the diagram; canonical is lowercase `w_ji` — both denote the same connection weight

---

## Research Summary

Slide 028 (printed badge **28**) is the anatomy diagram of a neural network model:
- Left: input/previous layer with 3 labeled neurons (i, j, k) whose outputs O_i, O_j, O_k feed forward
- Center: "Current Layer (You are here) — Hidden Layer(s)" — each neuron shows a `Σ` summation symbol and a `Net_i` label, i.e. **Net_i = Σ w_ji O_i + b_i**
- Right: output layer — outputs 1..m mapped to Class 1..m (multiclass classification)
- Top-right: `Target Label` — the ground truth for the Input Sample
- The phrase **"You are here"** highlights the hidden layer as the focus of the lesson

**Content facts for recreation**:
- Title: `Neural Network Model`
- Badge: **28**
- Column headers: `Previous Layer`, `Current Layer (You are here)`, `Next Layer`, `Layer (K)` (layer-count line may read differently)
- Column type line: `I/P Layer`, `Hidden Layer (s)`, `O/P Layer`
- Nodes are circles (typical), edges carry weight labels `W_ji`, `W_kj`
- Center neurons carry `Σ` and `Net_i/Net_j/Net_k`
- Right side: `Output 1..m` with `Class 1..m` pairs, plus `Target Label` above the Input Sample

### Uncertain Items (marked [?])
- Exact node count per column (parse shows 3 neurons at left/center; output column shows Output 1, Output 2, Output m — implies m outputs, may be more than 3 drawn)
- Whether `Layer (K)` is a 4th column header or a footer note about total layers
- Bias values (b_i) — no explicit bias notation recovered (may be omitted on diagram)
- Activation function labels per layer (not recovered)
- Exact geometry/colors pending vision analysis

---
*Generated: 2026-10-27*

---

## Verified 2026-10-30 (wave 4 — scope `src_w4_025_028`, worker `w4-src-025`)

**Method**: mandated by this deck's `AGENTS.md` rule 5 + the slide-recreation skill's
`references/source-research.md`. Spec read = `analysis/slide_028_final.json`
(vision `images`, `validate_slides` verdict PASS_WITH_FIXES, recreatability 8/10);
independent second read = `sources/docparse_cascades/slide_028/composed/slide_028_composed.md`
(frame md5 `3ec4323fe7f93e46819f7fd7dea31c10`, cross-pass merge, most complete pass =
crop01). The Wave-1 section above is unchanged.

**Search transport (honest note)**: the `agy -p` CLI is quota-exhausted —
HTTP 429 `RESOURCE_EXHAUSTED / Individual quota reached`, "Resets in 131h15m36s"
(CLI probe transcript banked at `sources/slide_028_source/agy_wave4/w4_cli_probe_429.txt`;
the probe failed identically to the other slides' probes).
Per the operations tool-down law the remaining queries ran through the **agy
web-search MCP** route — the same Google grounding service, different transport.
Every URL cited below was returned by that service; none are invented.

**Compact register**: `sources/slide_028_source/VERIFY_W4.md` (10-claim register,
evidence URLs, questions asked, spec changes).

### Claim-by-claim verification (wave 4)

| # | Claim (DATA-level) | Question asked | Answer | Verdict |
|---|---|---|---|---|
| 1 | `Net_i` / `Net_j` / `Net_k` = the weighted-sum-plus-bias pre-activation: `Net_i = Σ_j w_ji·x_j + b_i` | "neural network notation net input of neuron net_i = Σ_j w_ji x_j + b_i" | "net_i = the pre-activation (weighted sum) for neuron i in the current layer; Σ_j = summation over all neurons j in the previous layer; b_i = bias" | CONFIRMED — https://cs230.stanford.edu/files/Notation.pdf · https://medium.com/@anushruthikae/basic-notations-and-representation-neural-networks-d46a1be97471 · https://medium.com/@data-science/neural-networks-i-notation-and-building-blocks-817b1d2ea04b |
| 2 | The `Σ` symbols inside the neuron circles are the weighted-sum (adder) junction | "neural network neuron symbol convention: sigma summation symbol for weighted sum junction and activation function symbol inside neuron circle (Haykin style model)" | "a circle containing a summation sign (Σ) … performs the algebraic summation of all incoming weighted signals plus a threshold/bias term" | CONFIRMED — https://users.ece.utexas.edu/~vtelang/ece351m/ReadingAssignments/NNhaykin1.pdf |
| 3 | The `σ` symbols inside the neuron circles denote the neuron's activation (transfer) function | (same query) | "the neuron itself is drawn as a circle enclosing an activation function symbol … y_k = φ(v_k)" — σ is the same standard notation as φ(·) | CONFIRMED — https://users.ece.utexas.edu/~vtelang/ece351m/ReadingAssignments/NNhaykin1.pdf |
| 4 | `O_i` / `O_j` / `O_k` = the neuron's activated output: `o_i = f(net_i)` | (query #1) | "o_i (often also written as a_i): the final post-activation output of neuron i; f(·) is the activation function" | CONFIRMED — https://medium.com/@anushruthikae/basic-notations-and-representation-neural-networks-d46a1be97471 · https://medium.com/@data-science/neural-networks-i-notation-and-building-blocks-817b1d2ea04b |
| 5 | `w_ji` = weight from neuron j (previous layer) to neuron i (current layer) — destination-first | (query #1) | "w_ji: the weight parameter corresponding to the connection from neuron j (previous layer) to neuron i (current layer" | CONFIRMED **with a notation caveat** — https://medium.com/@anushruthikae/basic-notations-and-representation-neural-networks-d46a1be97471 · https://python-course.eu/machine-learning/neural-networks-structure-weights-and-matrices.php · https://cs230.stanford.edu/files/Notation.pdf. Caveat: the same search warns "other literature sometimes flips this to w_ij" (https://stats.stackexchange.com/questions/179966/is-weight-matrix-wij-from-neuron-j-to-i-or-from-i-to-j). The slide's `w_ji` placement between the `Net_i` and `Net_j` columns fits the destination-first reading; labels stay verbatim either way |
| 6 | Layer roles: "Previous Layer (i)" = I/P layer, "Current Layer (You are here)" = Hidden Layer(s), "Next Layer (K)" / "O/P Layer" | "multilayer perceptron complete architecture: input layer pass-through, hidden layers compute weighted sum plus bias then activation, output layer one neuron per class …" | "Input Layer: pass-through … Hidden Layers: compute weighted sums + activation (where learning happens) … Output Layer: final prediction; for classification one output per class" | CONFIRMED — https://www.datacamp.com/tutorial/multilayer-perceptrons-in-machine-learning · https://en.wikipedia.org/wiki/Multilayer_perceptron · https://developers.google.com/machine-learning/crash-course/neural-networks/nodes-hidden-layers |
| 7 | `Output 1 / Output 2 / Output m` ↔ `Class 1 / Class 2 / Class m` = classification output with m classes (one output per class) | (same query) | "For a classification target, the output layer typically features one neuron per class … Multi-Class uses C neurons with Softmax to output a normalized probability distribution" | CONFIRMED — https://ml-iitr.vlabs.ac.in/exp/multi-layer-perceptron/theory.html · https://www.geeksforgeeks.org/deep-learning/multi-layer-perceptron-learning-in-tensorflow/ |
| 8 | `Input Sample` (top-left) + `Target Label` (top-right) = forward-pass input + ground-truth label | (same query) | "Ground Truth (y): the true target label, often a one-hot vector or a scalar class index" + the input layer ingests "the raw feature vector of a given data sample" | CONFIRMED — https://ml-iitr.vlabs.ac.in/exp/multi-layer-perceptron/theory.html · https://pub.towardsai.net/the-multilayer-perceptron-built-and-implemented-from-scratch-70d6b30f1964 |
| 9 | The vertical `Error` bar with the green arrow toward the output row = the loss / error signal driving backpropagation | (same query) | "a loss function evaluates the divergence between the predicted distribution and the true ground-truth label … this error is fed backward through the network (chain rule) to compute gradients, allowing an optimizer to update the weights and biases" | CONFIRMED — https://ml-iitr.vlabs.ac.in/exp/multi-layer-perceptron/theory.html · https://www.geeksforgeeks.org/deep-learning/multi-layer-perceptron-learning-in-tensorflow/ (the doubled verbatim label `Error Error` stays as captured) |
| 10 | Doubled frame texts `Error Error`, `Previous Layer Layer (i)`, `Next Layer Layer (K)` | — (frame-level artifact) | Not a web question; the spec flags them as likely overlapping source text boxes and reproduces them verbatim | `[?]` — reproduced verbatim; flagged for a vision re-read exactly as the spec's own `uncertain_items` already does |

### Wave-4 sources banked (new this wave)

1. https://cs230.stanford.edu/files/Notation.pdf
2. https://medium.com/@anushruthikae/basic-notations-and-representation-neural-networks-d46a1be97471
3. https://python-course.eu/machine-learning/neural-networks-structure-weights-and-matrices.php
4. https://stats.stackexchange.com/questions/179966/is-weight-matrix-wij-from-neuron-j-to-i-or-from-i-to-j
5. https://medium.com/@data-science/neural-networks-i-notation-and-building-blocks-817b1d2ea04b
6. https://users.ece.utexas.edu/~vtelang/ece351m/ReadingAssignments/NNhaykin1.pdf
7. https://www.datacamp.com/tutorial/multilayer-perceptrons-in-machine-learning
8. https://en.wikipedia.org/wiki/Multilayer_perceptron
9. https://developers.google.com/machine-learning/crash-course/neural-networks/nodes-hidden-layers
10. https://ml-iitr.vlabs.ac.in/exp/multi-layer-perceptron/theory.html
11. https://pub.towardsai.net/the-multilayer-perceptron-built-and-implemented-from-scratch-70d6b30f1964
12. https://www.geeksforgeeks.org/deep-learning/multi-layer-perceptron-learning-in-tensorflow/

### Wave-4 doc-parse cross-check

`sources/docparse_cascades/slide_028/composed/slide_028_composed.md` (cross-pass merge,
most complete pass = crop01) independently recovers the **same label set** as the
vision spec: `Input Sample`, `Target Label`, `Net_i`/`Net_j`/`Net_k`, `O_i`/`O_j`/`O_k`,
`W_ji`, `W_kj`, `Σ` symbols on the neurons, `Output 1/2/m`, `Class 1/2/m`,
`Previous Layer | Current Layer (You are here) | Next Layer | Layer (K)`, and
`I/P Layer | Hidden Layer (s) | O/P Layer`. It independently reads the same
left-to-right feedforward orientation and the same previous → current → next layer
semantics, and flags the expected OCR degradation on subscripts (`Net_i` → `Neti`)
which the spec handled by restoring subscript notation. **Two independent reads agree
on every label; nothing was corrected.**

### Net effect on the analysis spec (wave 4)

**0 changes.** All nine substantive data claims are CONFIRMED. The one open item is
the doubled-text duplication (claim 10), a frame-reading question that stays `[?]`
for vision — exactly as the spec's own `uncertain_items` already flags. A notation
caveat on `w_ji` (destination-first vs from-first) is banked in claim 5 for
speaker-note accuracy; the verbatim labels are unchanged. Frame text is unchanged;
sources confirm/correct DATA only.

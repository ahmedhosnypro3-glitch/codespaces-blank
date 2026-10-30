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

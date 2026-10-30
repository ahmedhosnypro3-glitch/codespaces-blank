# Source Research: slide_029

## Doc-Parse Transcript (nemotron-3.5-parse)

**Run**: `sources/slide_029_source/docparse_run/`
- Full frame parse: `full/slide_029.parse.md`
- Composed: `composed/slide_029_composed.md`
- Crop cascade: 6 crops (dense diagram + formula boxes)
- Chat lane: DEGRADED (model `docparsechat` HTTP 404 on gateway) — deterministic-conservative fallback used
- Source frame md5: `50ae376cb7558f5e8057883cbd27dab0`

## Extracted Content (verbatim — merged from crop passes)

### Slide Title
**Neural Network Model** (badge **29**)

### Diagram + Formula Boxes

**Left side (diagram)**:
- `_Input Sample_` (purple box, top-left)
- `_Target Label_` (purple box, top-right)
- Input nodes: `O_i` (outputs from previous layer)
- Neuron j in current layer: `Net_j = Summation at Node j` with `Σ` symbol
- Weights: `W_ji` / `w_ji` — "Weight from Node i to Node j"
- Output: `O_j` = "Output at Node j" → `_Output 1_`
- Class labels: `Class 1`, `Class 2`, `Class m`
- Dimension notes: `Number of I/P Nodes = Input Vector Length`, `Number of O/P Nodes = Number of classes`

**Right side (formula boxes)**:
- **For Layer "j"**: `If Layer "j" is Output Layer:`
  - `Net_j = ∑ (w_ji O_i)` — weighted sum
  - `O_j = f(Net_j) = 1 / (1 + e^−Net_j)` — sigmoid activation
- **Error function**: `E = ½ ∑ (t_j − O_j)²` — sum of squared errors

**Bottom layer annotations** (matching slide_028):
- `Previous Layer`
- `Current Layer (You are here)`
- `I/P Layer`, `Hidden Layer(s)`, `O/P Layer`

---

## Web Search Verification

### Forward pass equations [[1]](https://www.scribd.com/document/929235465/A-Step-by-Step-Forward-Pass-and-Backpropagation-Example) [[2]](https://www.knowledgegate.ai/blog/introduction-to-artificial-neural-networks-explained) [[3]](https://blog.langformers.com/forward-pass-backpropagation-example/) [[4]](https://www.cs.toronto.edu/~jlucas/teaching/csc411/lectures/lec10_handout.pdf)

1. **Weighted sum (net input)**:
   `Net_j = z_j = ∑_i w_ji O_i`
   - `w_ji`: weight **from node i (previous) to node j (current)** ✓ matches "Weight from Node i to Node j"
   - `O_i`: output from previous neuron i (or input feature)
   - Bias `b_j` not shown in slide formula (common omission in introductory slides)

2. **Sigmoid activation**:
   `O_j = σ(Net_j) = 1 / (1 + e^−Net_j)`
   - Output range: (0, 1)
   - Sigmoid squashes linear net input to non-linear output ✓ matches slide

3. **Sum of Squared Errors (SSE) cost**:
   `E = ½ ∑_j (t_j − O_j)²`
   - `t_j`: target (ground truth) for output j
   - `O_j`: predicted output
   - `½` factor: cancels the 2 when differentiating for gradient descent ✓

### Layer dimension rules
- **Input nodes** = input vector length (feature dimension) ✓
- **Output nodes** = number of classes (for classification) ✓

---

## Research Summary

Slide 029 (printed badge **29**) is the **mathematical formalization** of the neural network model from slide 028:
- Left: the same diagram with explicit formula annotations on the single neuron j
- Right: the **forward pass equations** for the output layer (weighted sum → sigmoid) and the **error/cost function** (SSE)
- Badge: **29**
- The formulas are the canonical textbook forms for a single-layer output neuron with sigmoid activation

**Content facts for recreation**:
- Title: `Neural Network Model`
- Badge: **29**
- Two-column layout: diagram (left) + formulas (right)
- Diagram labels: `Input Sample`, `Target Label`, `Net_j = Summation at Node j`, `Σ`, `O_i`, `W_ji`/`w_ji`, `O_j`, `Output 1`, `Class 1/2/m`
- Formula box 1 (top): `For Layer "j"`, `If Layer "j" is Output Layer:`, `Net_j = ∑ (w_ji O_i)`, `O_j = f(Net_j) = 1 / (1 + e^−Net_j)`
- Formula box 2 (bottom): `E = ½ ∑ (t_j − O_j)²`
- Dimension callouts: `Number of I/P Nodes = Input Vector Length`, `Number of O/P Nodes = Number of classes`
- Bottom layer annotations: `Previous Layer`, `Current Layer (You are here)`, `I/P Layer`, `Hidden Layer(s)`, `O/P Layer`

### Uncertain Items (marked [?])
- Exact spatial arrangement of the two formula boxes (stacked? side-by-side?) — pending vision
- Whether the `E = ½ ∑...` formula appears in a separate box or merged — crops show it as a separate block
- Bias term `+ b_j` — omitted in slide formula; keep as absent per source
- Color of the formula boxes (cream? white? gray?) — pending vision
- Font/style of equations (italic? serif? inline vs display?) — use 2D mathtext per house rule

---
*Generated: 2026-10-27*
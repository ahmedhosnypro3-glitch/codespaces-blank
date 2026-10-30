# Source Research: slide_032

## Doc-Parse Transcript (nemotron-3.5-parse)

**Run**: `sources/slide_032_source/docparse_run/`
- Full frame parse: `full/slide_032.parse.md`
- Composed: `composed/slide_032_composed.md`
- Crop cascade: 0 crops (single full-frame parse sufficed)
- Chat lane: DEGRADED (model `docparsechat` HTTP 404 on gateway) — deterministic-conservative fallback used
- Source frame md5: `c4af90fa3bd7fe87811a9d9b5a0beee4`

## Extracted Content (verbatim)

### Slide Title
**How to Update Weights in order to minimize Error ?** (badge **32**)

### Subtitle / Callout
**Move in the opposite direction of the gradients Of the whole NN**

### Section Header
**(Back Propagation Algorithm)**

### Layout (from parse)
- Title centered upper area
- Badge 32 top-right
- "Move in the opposite direction..." text below title
- "(Back Propagation Algorithm)" section header lower down
- **No other text/diagrams recovered** — the slide may contain a diagram/algorithm box that the parse didn't capture

---

## Web Search Verification

### Backpropagation + Gradient Descent [[1]](https://www.ibm.com/think/topics/backpropagation) [[2]](http://neuralnetworksanddeeplearning.com/chap2.html) [[3]](https://medium.com/data-science/a-step-by-step-implementation-of-gradient-descent-and-backpropagation-d58bda486110) [[4]](https://outcomeschool.com/blog/math-behind-backpropagation) [[5]](https://stackoverflow.com/questions/3775032/how-to-update-the-bias-in-neural-network-backpropagation) [[6]](https://developer.nvidia.com/blog/a-data-scientists-guide-to-gradient-descent-and-backpropagation-algorithms/) [[7]](https://apxml.com/courses/introduction-to-neural-networks/chapter-4-backpropagation-gradient-descent/updating-weights-biases) [[8]](https://dev.to/patilmanas/understanding-backpropagation-and-gradient-descent-in-neural-networks-2heb)

**Core principle**: Update weights by moving in the **opposite direction of the gradient** of the error/loss function.

### Canonical formulas

1. **Weight update rule (gradient descent)**:
   $$w_{ij}^{new} = w_{ij}^{old} - \eta \frac{\partial C}{\partial w_{ij}}$$
   or iteratively: $w \leftarrow w - \eta \frac{\partial C}{\partial w}$

2. **Gradient via chain rule (backprop)**:
   $\frac{\partial C}{\partial w_{ij}} = \frac{\partial C}{\partial z_j} \cdot \frac{\partial z_j}{\partial w_{ij}} = \delta_j \cdot a_i$
   where $\delta_j = \frac{\partial C}{\partial z_j}$ is the "local error gradient" (delta)

3. **Bias update** (same pattern):
   $b_j \leftarrow b_j - \eta \frac{\partial C}{\partial b_j}$

4. **Training loop**:
   - Forward pass → prediction
   - Compute loss $C$ (e.g., MSE: $E = \frac{1}{2} \sum (t_j - O_j)^2$ — matches slide 029)
   - Backward pass (backprop) → compute all $\frac{\partial C}{\partial w}$
   - Update weights via gradient descent

---

## Research Summary

Slide 032 (printed badge **32**) is the **conceptual summary** slide for the neural network training process:
- Title poses the question: "How to Update Weights in order to minimize Error ?"
- Answer: "Move in the opposite direction of the gradients Of the whole NN" — the gradient descent principle
- Section header: "(Back Propagation Algorithm)" — names the algorithm
- This is likely the **closing/conclusion slide** of the lecture introducing neural networks

**Content facts for recreation**:
- Title: `How to Update Weights in order to minimize Error ?` (verbatim, including question mark and spacing)
- Badge: **32**
- Subtitle/callout: `Move in the opposite direction of the gradients Of the whole NN`
- Section header: `(Back Propagation Algorithm)` (with parentheses)
- Background: likely #E8E8E8 or #f0f0f0 (consistent with other slides)

### Uncertain Items (marked [?])
- Whether there's a diagram/algorithm flowchart in the middle (parse didn't capture)
- Whether the weight update formula is explicitly shown on the slide
- Color of the "Move in opposite direction..." text (red? green? black?)
- Font styling of section header (bold? italic? same as title?)

---
*Generated: 2026-10-27*
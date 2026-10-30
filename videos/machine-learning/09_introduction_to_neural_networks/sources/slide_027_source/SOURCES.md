# Source Research: slide_027

## Doc-Parse Transcript (nemotron-3.5-parse)

**Run**: `sources/slide_027_source/docparse_run/`
- Full frame parse: `full/slide_027.parse.md`
- Composed: `composed/slide_027_composed.md`
- Crop cascade: 0 crops (single full-frame parse sufficed)
- Chat lane: DEGRADED (model `docparsechat` HTTP 404 on gateway) — deterministic-conservative fallback used
- Source frame md5: `1a43f3e516807fe6f191433c5a5b6996`

## Extracted Content (verbatim)

### Slide Title
**Multi-Layer Neural Network**  
**The complete Picture** (subtitle)

### Badge
**27** (printed top-right)

### Layout (from parse)
- Title centered upper-middle
- Badge 27 in top-right
- **No other text recovered** — the rest of the slide is a diagram (MLP architecture) that the doc-parse did not transcribe

---

## Web Search Verification

### Multi-Layer Perceptron (MLP) Architecture [[1]](https://web.engr.oregonstate.edu/~huanlian/teaching/ML/2024fall/unit4/multilayer.html) [[2]](https://medium.com/@nlunge786/a-deep-architecture-multi-layer-perceptron-164bc5ff3842) [[3]](https://apxml.com/courses/introduction-to-deep-learning/chapter-2-activation-functions-architecture/network-layers-overview) [[4]](https://www.geeksforgeeks.org/deep-learning/layers-in-artificial-neural-networks-ann/) [[5]](https://developers.google.com/machine-learning/crash-course/neural-networks/nodes-hidden-layers)

**Standard "complete picture" components**:
1. **Input Layer** — feature vector x₁, x₂, ..., xₙ (no computation, pass-through)
2. **Hidden Layer(s)** — one or more layers; each neuron: z = Σw·x + b → activation (ReLU/Sigmoid/Tanh)
3. **Output Layer** — y₁, ..., yₖ; final activation depends on task (Sigmoid/Softmax for classification, Linear for regression)
4. **Weights & Biases** — w, b on every connection; learned via backpropagation
5. **Feedforward flow** — left-to-right, no cycles

**Key equations**:
- Hidden neuron: z = w₁x₁ + w₂x₂ + ... + wₙxₙ + b
- Activated output: a = φ(z) where φ = ReLU, σ, tanh, etc.
- Output neuron: y = φ'(Σw'h + b')

---

## Research Summary

Slide 027 (printed badge **27**) is titled "Multi-Layer Neural Network — The complete Picture". The doc-parse only recovered the title text and badge. The slide's main content is a **network architecture diagram** showing the classic 3-layer MLP topology (input → hidden → output) with fully connected edges, likely annotated with:
- Layer labels (Input, Hidden, Output)
- Node circles
- Weight/bias annotations on connections
- Possibly activation function labels
- Arrow directions (left-to-right)

**Content facts for recreation** (to be confirmed by vision analysis):
- Title: "Multi-Layer Neural Network" (line 1), "The complete Picture" (line 2)
- Badge: **27**
- Diagram: standard MLP with 3 columns of nodes
- Annotations: layer names, weights, biases, activation functions, flow arrows

### Uncertain Items (marked [?])
- Exact number of nodes per layer in the diagram
- Whether multiple hidden layers are shown
- Specific annotations on weights/biases/activations
- Color scheme of nodes and edges
- Background color (likely #e6e6e6 or #f5f5f5 like other slides)
- Whether equations are rendered on the diagram

---
*Generated: 2026-10-27*
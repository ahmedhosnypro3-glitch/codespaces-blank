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

---

## Verified 2026-10-30 (wave 4 — scope `src_w4_025_028`, worker `w4-src-025`)

**Method**: mandated by this deck's `AGENTS.md` rule 5 + the slide-recreation skill's
`references/source-research.md`. Spec read = `analysis/slide_027_final.json`
(vision `images`, `validate_slides` verdict PASS_WITH_FIXES, recreatability 9/10);
independent second read = `sources/docparse_cascades/slide_027/composed/slide_027_composed.md`
(frame md5 `1a43f3e516807fe6f191433c5a5b6996`). The Wave-1 section above is unchanged.

**Search transport (honest note)**: the `agy -p` CLI is quota-exhausted —
HTTP 429 `RESOURCE_EXHAUSTED / Individual quota reached`, "Resets in 131h15m36s"
(3 attempts banked in `sources/slide_027_source/agy_wave4/`; all failed identically).
Per the operations tool-down law the remaining queries ran through the **agy
web-search MCP** route — the same Google grounding service, different transport.
Every URL cited below was returned by that service; none are invented.

**Compact register**: `sources/slide_027_source/VERIFY_W4.md` (8-claim register,
evidence URLs, questions asked, spec changes).

### CORRECTION to the Wave-1 hypothesis above (this slide's main wave-4 output)

The Wave-1 section was written **before** vision analysis existed and *hypothesised*
that the frame's "main content is a network architecture diagram". Two independent
reads contradict that:

- `analysis/slide_027_final.json`: `verbatim_text.bullets` genuinely empty,
  `imagery` genuinely empty, and the brief's final step is "add no bullets, no
  images, and no animations; the slide is static".
- `sources/docparse_cascades/slide_027/composed/slide_027_composed.md`: exactly **2**
  positioned elements — `<class_Page-header>` (badge `27`) and `<class_Title>`
  containing `**Multi-Layer Neural Network** **The complete Picture**`. Zero crops,
  zero failed calls, **no picture or figure class at all**, no unpositioned text.

Slide 027 is therefore a **title-only section divider** ("the complete picture" of a
multi-layer neural network), **not** a diagram slide. Per the discrepancy law the
frame wins: a builder must **not** invent an MLP diagram here. The MLP facts below
are verified as the conceptual backdrop this divider announces; the diagram itself
is slide 028's content. The Wave-1 `[?]` list about diagram internals (node counts,
multiple hidden layers, weight/bias annotations, colours, equations) is **retired** —
it is moot, because the frame has no diagram.

### Claim-by-claim verification (wave 4)

| # | Claim (DATA-level) | Question asked | Answer | Verdict |
|---|---|---|---|---|
| 1 | Slide 027 is a title-only divider: "Multi-Layer Neural Network" + subtitle "The complete Picture", badge 27, thin red frame, black bottom bar, light-gray bg | — (frame-level) | Two independent reads agree (vision spec + doc-parse transcript) | CONFIRMED — records the correction of the Wave-1 diagram hypothesis |
| 2 | A "multi-layer" neural network has at least one hidden layer between input and output | "multilayer perceptron complete architecture: input layer pass-through, hidden layers compute weighted sum plus bias then activation, output layer one neuron per class …" | "input layer … one or more hidden layers … output layer" | CONFIRMED — https://en.wikipedia.org/wiki/Multilayer_perceptron · https://www.teach.cs.toronto.edu/~csc311notes/neural_networks/multi_layer_perceptron.html · https://www.geeksforgeeks.org/deep-learning/layers-in-artificial-neural-networks-ann/ |
| 3 | Input layer performs no computation — pure pass-through | (same query) | "No computations or transformations happen here … a_i^[0] = x_i" | CONFIRMED — https://ml-iitr.vlabs.ac.in/exp/multi-layer-perceptron/theory.html · https://pub.towardsai.net/the-multilayer-perceptron-built-and-implemented-from-scratch-70d6b30f1964 |
| 4 | Each hidden neuron computes a weighted sum plus bias, then applies an activation: z = Σ(w·x) + b → a = f(z) | (same query) | "z_j = Σ_i (w_ji · a_i) + b_j … then passed through a non-linear activation function" | CONFIRMED — https://ml-iitr.vlabs.ac.in/exp/multi-layer-perceptron/theory.html · https://www.datacamp.com/tutorial/multilayer-perceptrons-in-machine-learning · https://www.geeksforgeeks.org/deep-learning/multi-layer-perceptron-learning-in-tensorflow/ |
| 5 | The "complete picture" = feedforward left-to-right flow, learned weights/biases via backpropagation | (same query) | MLP layer-role breakdown + "weights and biases … updated via backpropagation" | CONFIRMED — https://www.teach.cs.toronto.edu/~csc311notes/neural_networks/multi_layer_perceptron.html · https://www.datacamp.com/tutorial/multilayer-perceptrons-in-machine-learning · https://developers.google.com/machine-learning/crash-course/neural-networks/nodes-hidden-layers |
| 6 | Output layer: for classification, one output neuron per class | (same query) | "For a classification target, the output layer typically features one neuron per class … Multi-Class uses C neurons with Softmax" | CONFIRMED — https://ml-iitr.vlabs.ac.in/exp/multi-layer-perceptron/theory.html |
| 7 | Frame styling #E8E8E8 bg, #C00000 title/subtitle, #FFD966 badge with #800080 outline | — (house rule, not a web claim) | Project house frame rule fixes gray bg / red frame / yellow badge; these are frame reads, and sources never license restyling | CONFIRMED as house-rule values — no change |
| 8 | The text cursor near "Picture" is a video artifact, not slide content | — (spec-level) | Spec `animation_state` excludes it explicitly | CONFIRMED — do not recreate |

### Wave-4 sources banked (new this wave)

1. https://en.wikipedia.org/wiki/Multilayer_perceptron
2. https://www.teach.cs.toronto.edu/~csc311notes/neural_networks/multi_layer_perceptron.html
3. https://ml-iitr.vlabs.ac.in/exp/multi-layer-perceptron/theory.html
4. https://pub.towardsai.net/the-multilayer-perceptron-built-and-implemented-from-scratch-70d6b30f1964
5. https://www.datacamp.com/tutorial/multilayer-perceptrons-in-machine-learning
6. https://www.geeksforgeeks.org/deep-learning/multi-layer-perceptron-learning-in-tensorflow/
7. https://www.geeksforgeeks.org/deep-learning/layers-in-artificial-neural-networks-ann/
8. https://developers.google.com/machine-learning/crash-course/neural-networks/nodes-hidden-layers

### Wave-4 doc-parse cross-check

The composed transcript for 027 is the decisive independent read: it kept only the
badge and the title element, found no picture/figure class, and reported 0 crops /
0 failed calls — i.e. the parser had nothing further to extract. That corroborates
the title-only reading and contradicts the Wave-1 diagram hypothesis. Its frame md5
matches the frame the vision analysis read (`1a43f3e516807fe6f191433c5a5b6996`).

### Net effect on the analysis spec (wave 4)

**0 changes to the JSON** — the spec already describes this slide correctly. The
substantive wave-4 output is the **correction of the banked Wave-1 hypothesis**
(recorded here and in `VERIFY_W4.md`), so a future builder does not "enrich" the
slide with an invented MLP diagram. Frame text is unchanged; sources confirm/correct
DATA only.
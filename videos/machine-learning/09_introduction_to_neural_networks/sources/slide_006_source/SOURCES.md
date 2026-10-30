# Source Research: slide_006

## Doc-Parse Transcript (nemotron-3.5-parse)

**Run**: `sources/slide_006_source/docparse_run/`
- Full frame parse: `full/slide_006.parse.md`
- Composed: `composed/slide_006_composed.md`
- Crop cascade: ran but outputs not individually saved
- Chat lane: DEGRADED (model `docparsechat` not available on gateway) — deterministic fallback used

## Extracted Content (from vision analysis)

### Slide Title / Section Header
**Visualization of Single Layer Perceptron**

### Slide Number
6

### Mathematical Content

**Three perceptron equations (multi-output):**
- d₁(X) = W₁ᵀX = w₁₁x₁ + w₁₂x₂ + ... + w₁ₙxₙ + b₁ * 1
- d₂(X) = W₂ᵀX = w₂₁x₁ + w₂₂x₂ + ... + w₂ₙxₙ + b₂ * 1
- dₘ(X) = WₘᵀX = wₘ₁x₁ + wₘ₂x₂ + ... + wₘₙxₙ + bₘ * 1

### Diagram Labels
- Inputs: x₁, x₂, x₃, ..., xₙ, 1 (bias)
- Weights per neuron (color-coded):
  - Neuron 1 (red): w₁₁, w₁₂, w₁₃, ..., w₁ₙ, b₁
  - Neuron 2 (blue): w₂₁, w₂₂, w₂₃, ..., w₂ₙ, b₂
  - Neuron m (green): wₘ₁, wₘ₂, ..., wₘₙ, bₘ
- Summation nodes: Σ (light blue circles)
- Activation boxes: purple rectangles (step functions)
- Outputs per class:
  - Class I: >0 Class I / <0 Not Class I
  - Class II: >0 Class II / <0 Not Class II
  - Class m: >0 Class m / <0 Not Class m
- "Multi-Class Classification" label box

---

## Research Summary

This slide (slide 6) extends the single perceptron to a **Single Layer Perceptron (multi-output)** for **Multi-Class Classification**. Key concepts:

1. **Multiple output neurons**: Each class gets its own perceptron (weight vector W₁, W₂, ..., Wₘ)
2. **Shared inputs**: All neurons receive the same input vector X = [x₁...xₙ, 1]ᵀ
3. **One-vs-All strategy**: Each neuron implements a binary classifier for one class vs. all others
4. **Decision rule**: For class k, if dₖ(X) > 0 → Class k, else Not Class k
5. **Visual diagram**: Full neural network architecture with color-coded weights (red/blue/green)

This is a **graph slide** requiring generated visualization via graphgen/ (using matplotlib/networkx to recreate the multi-perceptron architecture diagram with color-coded connections).

### Uncertain Items (marked [?])
- Exact visual layout details (node positions, arrow styles, colors) — need vision analysis for precise recreation
- The "..." vertical ellipsis between neuron 2 and neuron m in the diagram

---
*Generated: 2026-10-27*

## Wave-2 verification (2026-10-28)

Evidence basis: reanalysis_v2 for 006 was still empty (0 bytes) at read time; fell back to `analysis/slide_006_final.json` + doc-parse cascade `sources/docparse_cascades/slide_006/composed/` (composed parse verbatim: "d1(X) = W1 T X = w11 x1+w12x2+......+w1n xn+b1*1", "d2(X) = ...", "dm(X) = ...", "Multi-Class Classification"). 2 web searches (agy, Google). Claim-by-claim verification — frame text unchanged.

### Verified claims

1. **Three (up to m) output discriminant equations d1(X) = W1^T X, d2(X) = W2^T X, dm(X) = Wm^T X with per-class bias b1, b2, ... bm** — CONFIRMED. Single-layer perceptron with one output neuron (one weight vector) per class; each d_k(X) = W_k^T X = Σ_j w_kj x_j absorbs its own bias via the augmented-input trick (shared with slide 005).
2. **Shared input vector X = [x1...xn, 1]^T broadcast to all output neurons** — CONFIRMED. In SLP multi-class form the same augmented input vector feeds every output unit simultaneously.
3. **Per-class weight rows w_k1...w_kn (one-vs-all weight vectors)** — CONFIRMED. Weight matrix W = [W1, W2, ..., Wm] stacks the class weight vectors; the doc-parse crop table on the slide shows exactly this x/w pairing column structure.
4. **Σ summation node per output + activation boxes** — CONFIRMED. Canonical multi-output single-layer perceptron block diagram.
5. **"Multi-Class Classification" framing with one output neuron per class** — CONFIRMED. Classic linear-discriminant multi-class architecture; prediction by argmax_k d_k(X) (soft output) or per-class positive/negative testing (the slide's per-class ">0 Class k / <0 Not Class k" wording = One-vs-All framing, fully developed on slides 007-008).

### Data-only corrections
None. All analytic claims standard and correct.

### Citations (Wave-2)
1. https://www.cse.cuhk.edu.hk/~taoyf/course/cmsc5724/24-fall/lec/0g_class-multiclass.pdf — multi-class linear discriminant lecture (per-class d_k(X) = W_k^T X)
2. https://proceedings.mlr.press/v97/beygelzimer19a/beygelzimer19a-supp.pdf — scale-up multiclass classification (weight vectors per class)
3. https://blog.gopenai.com/mastering-multiclass-classification-with-single-layer-perceptrons-matlab-implementation-from-d8d30e979dec — multiclass single-layer perceptrons (D(X) = W^T X)
4. https://swayattadaw.medium.com/multiclass-perceptron-from-scratch-ed326fc34b8f — multiclass perceptron from scratch (shared augmented inputs)
5. https://beingneuron.com/single-layer-perceptron/ — single-layer perceptron reference
6. https://www.scribd.com/presentation/520039511/2-Single-Layer-Perceptron-Classifier — single-layer perceptron classifier deck (per-class hyperplanes)

## Wave-3 verification (2026-10-30)

Evidence basis: fresh vision re-analysis `analysis/reanalysis_v2/slide_006_reanalysis.txt` (14,773 B — NOW PRESENT, unlike Wave-2 which had to fall back to `analysis/slide_006_final.json`; this wave verifies against the fresh frame read) + doc-parse cascade `sources/docparse_cascades/slide_006/composed/` + 2 web searches. Tooling note: `agy -p` CLI quota-exhausted this wave (HTTP 429, reset ~154 h); searches ran through the agy MCP web-search tool (same Antigravity/Google grounding backend). All cited URLs re-fetched 2026-10-30; HTTP status noted per URL.

### Claim-by-claim verification (DATA only)

1. **m output discriminant equations d1(X)=W1^T X, d2(X)=W2^T X, dm(X)=Wm^T X, each with its own bias b_k*1 (printed red)** — CONFIRMED. One weight row + one bias per class over a shared augmented input: the standard multiclass linear-discriminant / single-layer perceptron layer (CUHK CMSC5724, Berkeley CS188, Toronto CSC311 notes).
2. **Shared input column x1, x2, x3, ..., xn plus a red bias 1 broadcast to all m summation nodes** — CONFIRMED.
3. **Per-class colour-grouped weights w1j (red), w2j (blue), wmj (green), with matching bias labels b1, b2, bm** — CONFIRMED by the fresh vision read. **Data note on the doc-parse "chart" table:** its pairings (x1→w11, x2→w13, x3→w22, b1→wm1, xn→wm2, 1→wmn, bm→Σ) are a column-extraction artifact of the two staggered label columns, NOT real x→w pairs on the frame. The frame has inputs on the left and colour-grouped weights to the right. The recreation must follow the colour groups, not the doc-parse table.
4. **Σ summation node per output, each followed by a step/threshold activation box** — CONFIRMED; canonical SLP layer schematic.
5. **Per-unit output wording ">0 Class k / <0 Not Class k"** — CONFIRMED as the One-vs-All hard-threshold framing. **Verbatim-text flag [?]:** the fresh vision pass transcribed the second line of each pair as ">0 Not Class k" (">0" twice), while Wave-1 and the doc-parse give "<0 Not Class k". The standard rule is d_k>0 → Class k and d_k<0 → Not Class k, and the frame shows "<0"; treat the vision ">0" as a misread, but confirm against the original frame at build time.
6. **Prediction rule for the m-output layer**: the slide tests each unit independently (OvA). The joint single-machine rule is argmax_k d_k(X) — assign to the class with the largest discriminant (Berkeley CS188, CUHK). Same linear family; the difference matters because argmax regions are convex and tile the space, whereas independent hard thresholds can leave overlap and gap regions (developed on slide 008; see `slide_008_source/SOURCES.md`).
7. **Scope of a single-layer perceptron**: each output unit contributes one linear hyperplane, so an SLP solves any linearly separable multiclass problem with one hyperplane per class but cannot solve non-linearly-separable ones such as XOR (Minsky & Papert 1969).

### Data-only corrections
- doc-parse chart-table pairing artifact noted above (not frame data — do not reproduce).
- Wave-2's fallback basis is superseded: `reanalysis_v2/slide_006_reanalysis.txt` now exists and was used as the primary evidence.

### Citations (Wave-3; re-fetched 2026-10-30)
1. https://www.cse.cuhk.edu.hk/~taoyf/course/cmsc5724/24-fall/lec/0g_class-multiclass.pdf — HTTP 200; multiclass discriminant formulation.
2. https://inst.eecs.berkeley.edu/~cs188/sp23/assets/lectures/cs188-sp23-lec26.pdf — HTTP 200; multiclass linear classifiers, argmax over discriminants.
3. https://www.teach.cs.toronto.edu/~csc311notes/neural_networks/multi_layer_perceptron.html — HTTP 200.
4. https://www.cs.toronto.edu/~urtasun/courses/CSC411/07_multiclass.pdf — HTTP 200; "1 vs all ... PROBLEM: More than one good answer!" and K-class discriminant regions "always singly connected and convex".
5. https://en.wikipedia.org/wiki/Perceptrons_(book) — HTTP 200; Minsky & Papert 1969, XOR not linearly separable.
6. https://data-intelligence.hashnode.dev/the-perceptron-algorithm-some-limitations — HTTP 200; single-layer perceptron separability limits.

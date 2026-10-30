# SOURCES.md — slide_016 Source Research

**Slide**: unique_slides/slide_016.jpg
**Title**: "Adding non-Linearity to Perceptrons"
**Subtitle**: "(Activation Functions)" — "Activation" in blue, "( Functions)" in red
**Slide number**: 16 (yellow badge, top-right)
**Date**: 2026-10-27

---

## 1. Doc-parse transcript (nemotron-parse)

Source: `sources/slide_016_source/slide_016.parse.md` (finish_reason=stop, 33 out tokens)

```
<x_0.8965><y_0.1172>16<x_0.9229><y_0.1516><class_Page-header>

<x_0.166><y_0.3906>**Adding non-Linearity to Perceptrons**
**(Activation Functions)**<x_0.873><y_0.5883><class_Section-header>
```

**Parse verdict**: REAL — corroborates the vision analysis (`analysis/slide_016_raw.json`)
on title, subtitle, badge numeral (16), and the two-line centered block. No bullets,
no equations, no body text on the slide: this is a **section-divider / topic-title
frame**. The only content is the title block.

---

## 2. Slide content summary (VERBATIM)

- Title: `Adding non-Linearity to Perceptrons`
- Subtitle: `(Activation Functions)` — word "Activation" colored blue (#0000FF),
  parentheses and "Functions)" colored dark red (#C00000)
- Slide number badge: yellow circle, black "16", top-right
- No bullets, no equations, no charts, no images

---

## 3. Web-verified facts (agy search, Google grounding)

**Query**: "activation function non-linearity perceptron neural network why needed
step sigmoid tanh ReLU Zewail CSAI lecture"

Topic confirmed: this slide is the **section-divider for the activation-function
sub-section** of the neural-networks lecture. The concepts it announces (all
standard, web-verified, none of them dramatized on the slide itself):

1. A perceptron computes a linear combination `z = Σ(wᵢ·xᵢ) + b = wᵀx + b`, then an
   activation function `y = f(z)` decides the neuron's output.
2. **Why non-linearity is needed**: stacking linear layers collapses to a single
   linear map — `y₂ = W₂(W₁x+b₁)+b₂ = (W₂W₁)x + (W₂b₁+b₂)` — so a linear network can
   only solve linearly-separable problems. Non-linear activations let networks
   approximate arbitrary functions (Universal Approximation Theorem).
3. **Step (Heaviside) function** `f(z)=1 if z≥0 else 0` was Rosenblatt's original
   1957 perceptron activation; it is not differentiable at z=0 with zero gradient
   elsewhere, so it cannot train with backpropagation.
4. **Sigmoid** `σ(z) = 1/(1+e⁻ᶻ)` squashes to (0,1); suffers vanishing gradients and
   is not zero-centered.
5. **Tanh** `tanh(z) = (eᶻ−e⁻ᶻ)/(eᶻ+e⁻ᶻ)` squashes to (−1,1); zero-centered but still
   saturates.
6. **ReLU** `max(0,z)` is the modern default: constant gradient 1 for z>0, cheap, but
   can produce "dead" units.

**Citations** (from agy grounding):
- [1] scribd.com/presentation/915087940/L11-Introduction-to-Neural-Network-AI-ML-CS877
- [2] medium.com/@mn05052002/...perceptrons-and-activation-functions...
- [3] cs.toronto.edu/~axgao/cs486686_f21/lecture_notes/Lecture_08_on_Neural_Networks_1.pdf
- [4] medium.com/@1087/the-purpose-of-activation-functions-in-the-neural-network
- [5] sparsity.ucsd.edu/publications/parhi2020role.pdf
- [6] pages.cs.wisc.edu/~gkotse/cs540s26/documents/Section001_2/lecture12...
- [7] cmu.edu/~mgormley/courses/10701-f16/slides/lecture12-neural-nets.pdf
- [8] cs231n.stanford.edu/slides/2017/cs231n_2017_lecture6.pdf

**Correction to slide**: NONE. The slide shows only a title/subtitle; no facts on it
require correction. Background facts above are for the recreation brief context
only — **do not add them to the slide** (never invent content the slide doesn't show).

---

## 4. Uncertainty markers

- None. Title/subtitle text is confirmed by two independent reads (vision model +
  nemotron-parse).

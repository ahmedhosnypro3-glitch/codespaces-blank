# Source Research: slide_005

## Doc-Parse Transcript (nemotron-3.5-parse)

**Run**: `sources/slide_005_source/docparse_run/`
- Full frame parse: `full/slide_005.parse.md`
- Composed: `composed/slide_005_composed.md`
- Crop cascade: 4 crops on diagram regions
- Chat lane: DEGRADED (model `docparsechat` not available on gateway) — deterministic fallback used

## Extracted Content (verbatim)

### Slide Title / Section Header
**Visualization of Single Perceptron**

### Slide Number
5

### Diagram Content (from multiple crop parses)

**Architecture:**
- Inputs: X₁, X₂, ..., Xₙ, bias (1)
- Weights: W₁, W₂, ..., Wₙ, b
- Augmented vectors: X = [x₁, x₂, ..., xₙ, 1]ᵀ, W = [w₁, w₂, ..., wₙ, b]ᵀ
- Summation node: Σ (O/P)
- Output: d(X) = WᵀX = w₁x₁ + w₂x₂ + ... + wₙxₙ + b*1

**Classification Rules:**
- d(X) > 0 ⇒ Class I
- d(X) < 0 ⇒ Class II
- d(X) = 0 ⇒ Undefined Class

**Visual Structure:**
- Top row: input nodes (X₁...Xₙ, bias 1)
- Middle: weight connections (w₁...wₙ, b)
- Center: Σ node (summation)
- Output: d(X) with classification rules

---

## Research Summary

This slide (slide 5) shows the **visual architecture of a single Perceptron** — the foundational neural network unit. It depicts:

1. **Input layer**: n features + bias term (1)
2. **Weight connections**: each input has a weight (w₁...wₙ) plus bias weight b
3. **Augmented vector notation**: X = [x₁...xₙ, 1]ᵀ, W = [w₁...wₙ, b]ᵀ
4. **Linear combination**: d(X) = WᵀX = Σ wᵢxᵢ + b
5. **Threshold activation**: step function output with three regions
6. **Diagram style**: network diagram with nodes and weighted connections

This is a **graph slide** requiring generated visualization via graphgen/ (using matplotlib/networkx or similar to recreate the perceptron architecture diagram).

### Uncertain Items (marked [?])
- Exact visual layout details (node positions, arrow styles, colors) — need vision analysis
- Whether the "..." in the diagram represents literal ellipsis or just visual shorthand

---
*Generated: 2026-10-27*

## Wave-2 verification (2026-10-28)

Evidence basis: fresh vision re-analysis `analysis/reanalysis_v2/slide_005_reanalysis.txt` (full, rich parse of `unique_slides/slide_005.jpg`) + doc-parse cascade `sources/docparse_cascades/slide_005/composed/`. 2 web searches (agy, Google). Claim-by-claim verification — frame text unchanged; DATA-only corrections noted below.

### Verified claims

1. **Augmented input vector X = [1; x1; x2; ...; xn]** — CONFIRMED. Standard pattern-recognition convention: prepend a constant 1 to the input vector so the bias/threshold is absorbed into the dot product. (Placement of the constant 1 at the head or tail is a convention choice; this slide places it first, which is consistent with the cited sources.)
2. **Augmented weight vector W = [b; w1; w2; ...; wn]** — CONFIRMED. Bias b becomes the first weight component paired with the constant-1 input.
3. **d(X) = W^T X = w1x1 + w2x2 + ... + wnxn + b*1** — CONFIRMED. This is the linear discriminant function in augmented form; the "+ b*1" term is exactly the bias absorbed by the augmentation trick.
4. **Decision rules: d(X) > 0 => Class I; d(X) < 0 => Class II; d(X) = 0 => Undefined Class** — CONFIRMED. The half-space interpretation: positive side of the decision hyperplane = Class I, negative side = Class II, points exactly on the hyperplane are on the boundary (this slide labels it "Undefined Class"; literature variously calls it the boundary/rejection condition, sometimes arbitrarily assigned to one class).
5. **Diagram structure: inputs x1..xn + bias 1, per-input weights w1..wn + b, summation node Σ, output O/P, "Binary Classification (2 Classes)"** — CONFIRMED. Matches the canonical single-perceptron architecture (inputs → weighted arrows → Σ → activation → output). The Σ-plus-step schematic on the slide is the standard textbook perceptron block.

### Uncertain items (kept from Wave-1, unchanged)
- Whether the step-function glyph after Σ is drawn as a Heaviside box or an arrow threshold — visual detail, non-data.
- Whether "O/P" also carries a class label downstream — frame shows only "O/P".

### Data-only corrections
None. All analytic claims on the slide are standard, correct ML content.

### Citations (Wave-2)
1. https://web.engr.oregonstate.edu/~huanlian/teaching/ML/2025fall/unit2/perceptron.html — augmented-vector perceptron lecture page (bias placement, W^T X, decision rules)
2. https://users.cs.utah.edu/~zhe/pdf/lec-10-perceptron-upload.pdf — perceptron lecture slides (augmented vectors)
3. https://ai.stackexchange.com/questions/2545/understanding-the-perceptron-algorithm-in-the-book-a-course-in-machine-learning — perceptron algorithm discussion (A Course in Machine Learning)
4. https://www.geeksforgeeks.org/deep-learning/what-is-perceptron-the-simplest-artificial-neural-network/ — perceptron basics (weights, summation, step activation, classes)
5. https://arafique906.medium.com/single-layer-perceptron-5def67f59921 — single-layer perceptron architecture
6. https://beingneuron.com/single-layer-perceptron/ — single-layer perceptron (Σ node, weights, bias b with input 1)
7. https://pub.towardsai.net/perceptron-a-basic-neural-network-model-for-deep-learning-21aea56e3216 — perceptron model overview
8. https://blog.nashtechglobal.com/complete-guide-to-single-layer-perceptron-with-implementation/ — single-layer perceptron guide (summation + step function)
9. https://www.kaggle.com/code/hongsean/tutorial-perceptron-algorithm — perceptron algorithm tutorial

## Wave-3 verification (2026-10-30)

Evidence basis: fresh vision re-analysis `analysis/reanalysis_v2/slide_005_reanalysis.txt` (9,510 B, full rich parse of `unique_slides/slide_005.jpg`; present at read time) + doc-parse cascade `sources/docparse_cascades/slide_005/composed/` + 3 web searches. Tooling note: the `agy -p` CLI was quota-exhausted this wave (HTTP 429, reset ~154 h), so searches ran through the agy MCP web-search tool — the same Antigravity/Google grounding backend. All cited URLs were re-fetched on 2026-10-30 and page text checked; HTTP status noted per URL.

### Claim-by-claim verification (DATA only)

1. **Augmented input vector X = [1; x1; x2; ...; xn] — constant 1 at the HEAD** — CONFIRMED as this frame's convention. **Data-only correction to Wave-1:** the Wave-1 summary wrote `X = [x1,...,xn,1]^T, W = [w1,...,wn,b]^T` (constant LAST). The fresh vision read of the frame shows the constant 1 first (`X = [1; x1; ...; xn]`, `W = [b; w1; ...; wn]`). Both orders exist in the literature (Cornell CS4780 appends the 1 last; Oregon State puts x0=1 first), so the literature is not wrong — but the recreation must use the frame's head placement.
2. **Augmented weight vector W = [b; w1; ...; wn]** — CONFIRMED; same head-placement note for the bias b.
3. **d(X) = W^T X = w1x1 + w2x2 + ... + wnxn + b*1** — CONFIRMED; expands to w^T x + b, the linear discriminant / net input of the perceptron.
4. **Decision rules: >0 => Class I, <0 => Class II, =0 => Undefined Class** — CONFIRMED as a boundary convention. sign(d) classifiers assign one class per open half-space; the d=0 hyperplane is the decision surface. RIT's notes state a point exactly on the decision surface is "treated as ambiguous, and not necessarily belonging to either set" — matching the slide's "Undefined Class". Standard sign(·) implementations fold the zero case into one class (e.g. +1 if >= 0), so "Undefined" is this lecture's boundary convention, not a universal rule.
5. **Geometry: w is normal to the decision hyperplane and points into the positive (Class I) half-space** — CONFIRMED (NUS CS5339). Supports orienting the recreation's labels/arrows.
6. **The bias lets the hyperplane shift off the origin** — CONFIRMED (Cornell CS4780: without the bias term the hyperplane "would always have to go through the origin"). This is why the augmented form is used.
7. **Diagram: inputs x1..xn + bias 1 -> per-input weights w1..wn + b -> summation Σ -> step/threshold activation -> O/P; tagged "Binary Classification (2 Classes)"** — CONFIRMED; the canonical Rosenblatt perceptron block. A single perceptron is a linear BINARY classifier (CMU 10601, NUS, UPenn).

### Data-only corrections
- Wave-1 augmented-vector ordering (constant last) corrected to constant-first per the fresh vision read of the frame.

### Uncertain items (non-data, carried)
- Step-glyph style, panel geometry, colors — visual only, for the build/judge lanes.

### Citations (Wave-3; re-fetched 2026-10-30)
1. https://www.cs.cornell.edu/courses/cs4780/2018fa/lectures/lecturenote03.html — HTTP 200; text confirms absorbing b via an added constant dimension and sign(w^T x + b).
2. https://web.engr.oregonstate.edu/~huanlian/teaching/ML/2025fall/unit2/perceptron.html — HTTP 200; text confirms x = (1, x1, ..., xd) with bias feature x0=1 placed first.
3. https://www.cs.rit.edu/~rlaz/PatternRecognition/slides/Intro-LinearDiscriminants-notes.pdf — HTTP 200; g(x)=w^T x + ω0, g(x)=0 decision surface, points on it "treated as ambiguous".
4. https://machine-learning-upenn.github.io/assets/notes/Lec2.pdf — HTTP 200; perceptron +1/-1 threshold output, hyperplane, half-spaces.
5. https://www.comp.nus.edu.sg/~scarlett/CS5339_notes/01-Perceptron_Notes.pdf — HTTP 200; w normal to the boundary and pointing into the positive half-space.
6. https://www.cs.cmu.edu/~mgormley/courses/10601bd-f18/slides/lecture6-perc.pdf — HTTP 200; threshold unit formulation.
7. https://svivek.com/teaching/machine-learning/lectures/slides/perceptron/perceptron.pdf — HTTP 200.
8. https://users.cs.utah.edu/~zhe/pdf/lec-10-perceptron-upload.pdf — HTTP 200 (also cited in Wave-2).

## Verified 2026-10-30 (wave 4 — scope src_w4_005_008)

Evidence basis: `analysis/slide_005_final.json` + fresh vision read `analysis/reanalysis_v2/slide_005_reanalysis.txt` (9,510 B) + doc-parse cascade `sources/docparse_cascades/slide_005/composed/slide_005_composed.md` (independent second read) + 3 agy searches + 4 live URL fetches. Tooling note: the `agy -p` CLI is quota-exhausted this wave (re-tested 2026-10-30: `RESOURCE_EXHAUSTED (HTTP 429)`, "Individual quota reached", resets in ~131 h), so searches ran through the agy MCP web-search tool — the same Antigravity/Google grounding backend the CLI drives (verified via `agy_check_setup`: token valid, no blockers). Every URL below was re-fetched live on 2026-10-30; the ones that failed are recorded as failures, not as citations. Frame text unchanged — DATA-only.

### Verification questions asked (agy, this wave)
1. "perceptron decision boundary d(X)=W^T X with augmented input vector constant 1 for bias: what is the standard notation and what does d(X)>0 vs d(X)<0 vs d(X)=0 mean for class assignment?"
2. (re-fetch check) does the Cornell CS4780 note still state the bias-absorption convention and the origin argument verbatim?
3. (re-fetch check) does the Oregon State perceptron page still print x = (1, x1, ..., xd) with bias feature x0 = 1 at the head, and its dot-product sign decision rule?

### Claim-by-claim verification (DATA only)

1. **Augmented input vector X = [1; x1; x2; ...; xn] — constant 1 at the HEAD, becoming the bias feature x0** — CONFIRMED. Oregon State (live): "each `x = (1, x_1, ..., x_d)` is already in the `d+1` dimensional space with one bias feature `x_0=1` and `d` real features". Literature uses both head and tail placement for the constant (Cornell-style augmentation "add[s] one additional constant dimension" without fixing which end); the frame's head placement is a valid convention and the one the recreation must use. Doc-parse corroborates: `X = x1 1 X2 → X = x2 ... W =` (constant 1 present in the augmented column).
2. **Augmented weight vector W = [b; w1; w2; ...; wn]** — CONFIRMED. The companion of (1): the bias b is the weight paired with the constant-1 input; UCSD's multiclass-perceptron handout carries independent biases b1...bk alongside weight rows w1...wk, same pattern.
3. **d(X) = W^T X = w1x1 + w2x2 + ...... + wnxn + b*1** — CONFIRMED as the linear discriminant / net input of the perceptron. Cornell CS4780 (live, verbatim): "`b` is the bias term (without the bias term, the hyperplane that `w` defines would always have to go through the origin). Dealing with `b` can be a pain, so we 'absorb' it into the feature vector `w` by adding one additional constant dimension." The slide's `+ b*1` term is exactly that absorbed bias. Doc-parse corroborates verbatim: "d(X) = W T X = w1 x1 +w2 x2 +...... +wn xn+b*1".
4. **Decision rules: d(X) > 0 ⇒ Class I; d(X) < 0 ⇒ Class II; d(X) = 0 ⇒ Undefined Class** — CONFIRMED as a valid boundary convention, with the literature nuance recorded. Oregon State (live, verbatim): "we said we output positive if the dot product is positive and negative if otherwise" and the tie case `w·x = 0` counts as a mistake. Cornell: `h(x) = sign(w^T x + b)`. So the standard sign implementations fold the zero case into one class; the slide's third case "=0 ⇒ Undefined Class" is this lecture's own (correct, pedagogically standard) boundary convention — render it verbatim as printed. Doc-parse corroborates all three lines verbatim, including "=0 ⇒ Undefined Class".
5. **Diagram: inputs x1..xn plus bias 1 → per-input weights w1..wn plus b → Σ summation node → step/threshold activation → O/P, tagged "Binary Classification (2 Classes)"** — CONFIRMED as the canonical single-perceptron block; a single perceptron is a linear BINARY classifier (Wikipedia on Minsky & Papert: "The perceptron convergence theorem was proved for single-layer neural nets"). Nothing on the frame contradicts the standard topology.
6. **Non-DATA items (step-glyph style, exact reds, box geometry, ellipsis row)** — UNVERIFIED: no source counterpart; these are visual, for the build/judge lanes. No spec change.

### Data-only corrections
None. No claim on this slide is contradicted by a source, so no patch to `analysis/slide_005_final.json` was needed.

### Uncertain items (carried, non-DATA)
- Step-glyph appearance, leader geometry, `#ff0000` vs `#c00000` assignment — visual only.

### Citations (wave 4; re-fetched live 2026-10-30)
1. https://web.engr.oregonstate.edu/~huanlian/teaching/ML/2025fall/unit2/perceptron.html — HTTP 200; text extracted; quotes verified above (x0=1 head placement, positive/negative sign rule, zero tie case).
2. https://www.cs.cornell.edu/courses/cs4780/2018fa/lectures/lecturenote03.html — HTTP 200; text extracted; quote verified above (bias absorption, hyperplane-through-origin argument, sign classifier).
3. https://cseweb.ucsd.edu/~dasgupta/151/multiclass-handout.pdf — HTTP 200; pdftotext extracted; per-class weights w1…wk and biases b1…bk, argmax readout.
4. https://en.wikipedia.org/wiki/Perceptrons_(book) — HTTP 200; Minsky & Papert 1969, parity/XOR limits, single-layer convergence theorem.
Failed this wave (honest record; NOT cited as verified):
5. https://apxml.com/courses/introduction-to-deep-learning/chapter-1-neural-network-foundations/perceptron-simplest-network — HTTP 403 on live fetch (bot-blocked); kept only as an agy search lead, status unverified.
6. https://interactiveaudiolab.github.io/course-deep-learning/slides/DL_perceptrons.pdf — HTTP 200 but the fetch tool returned non-parseable binary PDF bytes; unverified.

## Wave-4 result register

See `sources/slide_005_source/VERIFY_W4.md` — 6 claims: 5 CONFIRMED, 0 CORRECTED, 1 UNVERIFIED (visual-only), 4 verified URLs + 2 honest fetch failures.

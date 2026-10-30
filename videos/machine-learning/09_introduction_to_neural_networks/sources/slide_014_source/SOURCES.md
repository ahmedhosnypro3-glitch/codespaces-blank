# Source Research for slide_014

## Slide Content (from doc-parse)
- **Slide number**: 14
- **Title**: "Using Two Perceptron Layers"
- **Visual elements**: 
  - Network diagram with two perceptron layers
  - First layer: W11, W12, W21, W22 weights
  - Second layer: Σ with threshold >0 ⇒ 1, <0 ⇒ 0
  - Inputs: X1, X2
  - Outputs: Sum 1, Sum 2, Sum 3
- **Table/Equations**:
  - Sum 1 = W11 x1 + W12 x2
  - Sum 2 = W21 x1 + W22 x2
  - Sum 3 = (W11 x1 + W12 x2) w31 + (W21 x1 + W22 x2) w32
  - = (W11 w31 + W21 w32) x1 + (W21 w31 + W22 w32) x2
  - "(W11 x1 + W2 x2 ) Still Linear Equation"

## Web Search Findings
**Source**: Multiple sources on Multi-Layer Perceptrons (MLP)

**Key facts verified**:
1. **Two-Layer Perceptron**: Adding a hidden layer creates a multi-layer perceptron
2. **Linear Composition Problem**: The composition of two linear functions is still linear
   - Sum 3 = (W11 w31 + W21 w32) x1 + (W21 w31 + W22 w32) x2
   - This simplifies to W'₁ x1 + W'₂ x2 — still a single linear decision boundary
3. **Key Insight**: Without non-linearity, multiple layers collapse to a single layer
4. **Solution**: Non-linear activation functions (ReLU, Sigmoid, Tanh) between layers

## Slide-Specific Analysis
- This slide demonstrates WHY simply adding layers doesn't help without non-linearity
- The table shows the algebraic proof: two linear layers = one linear layer
- The final row "(W11 x1 + W2 x2 ) Still Linear Equation" is the key teaching point
- Visual shows a 2-layer network architecture diagram
- This sets up the need for activation functions (slide 15-16)

## Citations
- [1] GeeksforGeeks: "What is Perceptron - The Simplest Artificial Neural Network"
- [2] Medium: "Perceptron in Deep Learning - Basics & Limitations"
- [5] Educative: "XOR Problem in Neural Network"
- [6] Towards Data Science: "Terribly Perceptive - The Perceptron, The XOR"

## Notes for Analysis
- Key visual: network architecture diagram with weights labeled
- Table with mathematical derivation showing linear composition
- Critical text: "Still Linear Equation" - the pedagogical punchline

---

## Wave-3 verification (2026-10-30, agy web search)

Content evidence used: `analysis/reanalysis_v2/slide_014_reanalysis.txt` (fresh vision re-read,
2026-10-29) cross-checked with `analysis/slide_014_final.json` (PASS_WITH_FIXES).
Searches: 1 via `agy -p` CLI, 2 via the agy MCP Google-grounding endpoint (CLI individual quota
hit 429 mid-run; same agy service, file token).

### Concepts on the slide, web-verified

1. **The algebraic punchline: two linear layers = one linear layer.** With
   `h1 = W11·x1 + W12·x2`, `h2 = W21·x1 + W22·x2` and `Sum3 = h1·w31 + h2·w32`,
   expanding and grouping by input gives
   `Sum3 = (W11·w31 + W21·w32)·x1 + (W12·w31 + W22·w32)·x2 = W'1·x1 + W'2·x2`.
   In matrix form `y = W2(W1x + b1) + b2 = (W2W1)x + (W2b1 + b2)`; by associativity any
   stack of purely linear layers collapses into a single effective matrix, so the network can
   still only draw ONE straight decision boundary. This is exactly the slide's
   "= W'1 x1 + W'2 x2  ⇒ Still Linear Equation".
   - https://www.deeplearningbook.org/contents/mlp.html (Goodfellow, Bengio & Courville, ch.6 "Learning XOR")
   - https://www.deeplearningbook.org/slides/06_mlp.pdf (ch.6 slides — linear model cannot solve XOR)
   - https://cs231n.github.io/neural-networks-1/ (without a non-linearity the score collapses to `s = W2·max(0,W1x)`-less form `s = W2W1x = Wx`)
   - http://neuralnetworksanddeeplearning.com/chap4.html (Nielsen, ch.4 — chains of linear neurons only give linear functions)
   - https://cs230.stanford.edu/ (Andrew Ng, "Why do you need non-linear activation functions?")
2. **Weight notation W_ij.** Standard modern deep-learning convention is `W_ij` = weight from
   source j to destination i ("to i, from j"; row = destination, column = source), so a layer
   computes `z = W x + b` with `z_i = Σ_j W_ij x_j`. The slide's W11/W12/W21/W22 (first index =
   destination neuron) and w31/w32 (hidden→output) follow this convention.
   - https://cs230.stanford.edu/files/Notation.pdf (Stanford CS230 notation sheet)
   - https://stats.stackexchange.com/questions/179966/is-weight-matrix-wij-from-neuron-j-to-i-or-from-i-to-j
   - https://orbit.dtu.dk/files/131600547/Matrix_representation_of_a_Neural_Network.pdf
3. **Right-hand inset = equivalent single perceptron with effective weights w'1, w'2.** Same
   statement as (1): the collapsed network is exactly one perceptron with `w'1 = W11·w31 + W21·w32`,
   `w'2 = W12·w31 + W22·w32` (plus `b' = w31·b1 + w32·b2 + b3` when biases are present).
   - https://www.deeplearningbook.org/contents/mlp.html
   - https://cs231n.github.io/neural-networks-1/

### Correction candidate to check against pixels — `[?]`
The reanalysis transcribed the second expansion line as
`= (W11·w31 + W21·w32)·x1 + (W21·w31 + W22·w32)·x2`. Web-verified algebra requires the x2
coefficient to be `W12·w31 + W22·w32` (the x2 terms of the two hidden units are W12·w31 and
W22·w32). Either the slide prints a typo in that term, or the vision read mis-transcribed
`W12` as `W21`. The builder must read the pixels and reproduce **what is printed** verbatim
(never silently "fix" it); the physically correct form is the one above.

### Verdict
The slide's claim and derivation are textbook-correct (linear composition collapses), so the
recreation must keep the red "Sum 1/2/3" labels, the blue italic "Still Linear Equation"
annotation, the numbered stage circles 1/2/3, and the cream inset showing the equivalent
single perceptron. Equation text must be rendered in Professional 2D format per the house
math rule.
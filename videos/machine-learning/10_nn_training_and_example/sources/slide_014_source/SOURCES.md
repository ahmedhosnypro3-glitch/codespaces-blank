# Slide 014 — "Neural Network Model (Current Layer is Hidden Layer)"

## Sources

1. **Stanford CS230 — Deep Learning notation (PDF)** (https://cs230.stanford.edu/files/Notation.pdf) — confirms the layer
   notation used on the slide: index i for the previous layer, j for the current layer, k for the next layer.
2. **Wikipedia — Backpropagation** (https://en.wikipedia.org/wiki/Backpropagation) — confirms Net_j = Σ_i w_ji·O_i + b_j and
   E = ½Σ(t_j − O_j)² with the same previous/current/next indexing.
3. **GeeksforGeeks — Forward propagation in neural networks** (https://www.geeksforgeeks.org/deep-learning/forward-propagation-in-neural-networks/) — confirms
   the forward pass computing each node's net input as a weighted sum of the previous layer's outputs.
4. **DataCamp — Forward propagation tutorial** (https://www.datacamp.com/tutorial/forward-propagation-neural-networks) — confirms
   O_j = f(Net_j) and that layer outputs feed the next layer as inputs.
5. **DataLad — The mathematics behind neural networks** (https://datalad.co.uk/the-mathematics-behind-neural-networks/) — confirms
   the bias node ("1 Node Bias") as a unit constant-1 input added to every layer's weighted sum.
6. **Tufts CS135 lecture 18 notes** (https://www.cs.tufts.edu/comp/135/2020s/lectures/slides/lec18.pdf) — confirms
   the sigmoid activation and the error expression on a per-layer basis.

## Verified content for this slide

- Layer roles: Previous Layer (I), Current Layer (J, "you are here"), Next Layer (K) — matches standard
  three-layer notation with i/j/k unit indices.
- Net_j = Σ_i(w_ji·O_i) (+ bias Bj from the "1 Node Bias" unit) — standard net input of a hidden node.
- E = ½Σ_j(t_j − O_j)² — standard squared-error cost; the X X X marks are the frame's highlight glyphs.
- "Note: Layer j is NOT Output Layer" — correct, hidden-layer weights need back-propagated deltas.

## Corrections / notes

- **None found.** The slide presents the standard MLP architecture and forward-pass/error equations.
- Notation remark only: the frame prints `Σ i (wjj Oi)` — the `wjj` subscript is a typo of the original
  frame (self-weight); the standard weight from unit i into unit j is w_ji. On-frame text is DATA.

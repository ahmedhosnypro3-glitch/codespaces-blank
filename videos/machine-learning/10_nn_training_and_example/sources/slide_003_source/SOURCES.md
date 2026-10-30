# Slide 003 — Neural Network Model: node = Σ + activation, Net_j, sigmoid output, squared error E, node bias

Frame facts (from `analysis/parse/slide_003.parse.md`, data only): title "Neural Network Model
(Each node consists of Summation + Activation)"; labels "Input Sample", "Target Label",
"Node Bias", "For Layer 'j'", "Previous Layer Layer (i)", "Current Layer is Output Layer
(You are here)"; equations `Net j = Σ_i (w_ji O_i)`, `E = 1/2 Σ_T (t_j − O_j)^2`,
`O_j = f(Net_j) = 1/(1+e^(−Net_j))`. Method: agy web search (best-effort), verified against
authoritative derivations of the feed-forward pass and backpropagation gradient.

## Sources

- IBM — "Backpropagation" (https://www.ibm.com/think/topics/backpropagation) — confirms node net input as weighted sum of previous-layer outputs plus bias, and the chain-rule decomposition of ∂E/∂w.
- Towards Data Science — "Backpropagation Step by Step Derivation" (https://towardsdatascience.com/backpropagation-step-by-step-derivation-99ac8fbdcc28/) — derives ∂E/∂w_ji = (O_j − t_j)·O_j(1−O_j)·O_i, i.e. the exact product of the slide's three factors.
- Medium — "Derivation of the Backpropagation Algorithm" (https://medium.com/@shakeraafreen12/derivation-of-the-backpropagation-algorithm-5002a047b399) — confirms sigmoid activation O_j = 1/(1+e^(−Net_j)) and E = 1/2 Σ(t−O)^2 as the standard per-sample error.

## Corrections / notes

- `Net_j = Σ_i (w_ji O_i)` — CONFIRMED as the standard feed-forward net input; authoritative form adds a bias term `+ b_j`, which the slide shows separately as a "Node Bias" arrow, so no correction.
- `O_j = f(Net_j) = 1/(1+e^(−Net_j))` — CONFIRMED: logistic/sigmoid activation, standard notation.
- `E = 1/2 Σ_T (t_j − O_j)^2` — CONFIRMED as the per-sample squared-error cost (the 1/2 cancels the 2 on differentiation). Note: on the slide the sum index reads `T`, standard sources index it over output units (k/j) or training samples; rendered as the frame shows.
- "Current Layer is Output Layer (You are here)" and "Previous Layer Layer (i)" — course-authored pedagogy labels for a single-node/one-layer diagram; no source counterpart, do not "fix" toward standard texts.
- The parse transcript renders `O_j = f(Net_j) = 1+e^{−Net_i}` at line 19; the standard sigmoid is `1/(1+e^{−Net_j})` (denominator), confirmed by all three sources — treat as a parse-extraction artifact of the stacked fraction, not a slide error.

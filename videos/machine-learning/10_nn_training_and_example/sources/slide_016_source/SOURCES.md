# Slide 16 — Neural Network Model (multilayer architecture: input/hidden/output layers, forward pass, node bias)

## Sources

- Michael Nielsen, "Neural Networks and Deep Learning", Ch. 2 (How the backpropagation algorithm works) — http://neuralnetworksanddeeplearning.com/chap2.html
  Confirms the layer convention (input layer / hidden layers / output layer), the weighted-sum pre-activation z = Σ w a + b, and the squared-error cost ½Σ(y−a)² used for a classifier with one output node per class.
- "Backpropagation step-by-step derivation" (Towards Data Science) — https://towardsdatascience.com/backpropagation-step-by-step-derivation-99ac8fbdcc28/
  Confirms the forward-pass form Net_j = Σ_i w_ji·O_i and the activation O_j = f(Net_j).
- BackPropDeriv, Swarthmore CS81 lecture notes — https://www.cs.swarthmore.edu/~meeden/cs81/s10/BackPropDeriv.pdf
  Confirms the weight index convention w_ji (weight from unit i of the previous layer to unit j of the current layer) and the ½·(t−O)² error term.
- "Why is 1/2 used in the cost function?" (Stack Overflow) — https://stackoverflow.com/questions/68629338/why-there-divided-by-2-in-cost-function-derivation-process
  Confirms the 1/2 prefactor is a convention chosen so the power-rule exponent 2 cancels on differentiation.
- "Gradient descent cost function: MSE vs SSE" (Math StackExchange) — https://math.stackexchange.com/questions/3808410/gradient-descents-cost-function-mean-squared-error-vs-sum-of-squared-errors
  Confirms the SSE form E = ½Σ(y−ŷ)² gives the same minimizer as MSE.

## Corrections / notes

- The on-frame Net_j = Σ_i (w_ji·O_i) is printed without a bias term, while the diagram itself carries a separate "Node Bias i / j" column feeding a constant 1. That is consistent: the bias is the weight of the constant-1 input (w_j0·O_0, O_0 ≡ 1). No content correction needed; the recreation should keep the bias column visible but need not add b_j into the printed formula.
- The parse transcript renders the weight subscript as "wjj" in one spot; the standard (and correct) reading is w_ji, which the analysis already adopted. Recreate as w_ji.
- E = ½Σ_j(t_j − O_j)²: the summation index j here runs over OUTPUT-layer nodes (the per-class error boxes "Error / Error / Error" on the frame are the per-output-node terms). Standard notation.
- Everything else on the frame (Class 1..Class m targets, "Layer j is NOT the output layer" caption, Σ symbols at layer junctions) matches the standard 3-layer MLP diagram; no contradictions with the sources found.

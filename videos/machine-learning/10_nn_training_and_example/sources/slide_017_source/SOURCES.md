# Slide 17 — Neural Network Model (sigmoid activation, effect of Net_k on the calculated error is known from the output layer)

## Sources

- "Derivative of the sigmoid function" (Built In) — https://builtin.com/articles/derivative-of-sigmoid-function
  Confirms O_j = 1/(1+e^{−Net_j}) and its closed-form derivative ∂O_j/∂Net_j = O_j(1−O_j).
- "Backpropagation step-by-step derivation" (Towards Data Science) — https://towardsdatascience.com/backpropagation-step-by-step-derivation-99ac8fbdcc28/
  Confirms the sigmoid-as-activation form O_j = f(Net_j) = 1/(1+e^{−Net_j}) and the backprop chain rule ∂E/∂w = ∂E/∂O · ∂O/∂Net · ∂Net/∂w.
- Michael Nielsen, "Neural Networks and Deep Learning", Ch. 2 — http://neuralnetworksanddeeplearning.com/chap2.html
  Confirms the sigmoid (logistic) activation, the ½Σ(t−O)² cost, and the delta-signal idea that the output layer's gradient is known first and is propagated backward.
- BackPropDeriv, Swarthmore CS81 lecture notes — https://www.cs.swarthmore.edu/~meeden/cs81/s10/BackPropDeriv.pdf
  Confirms the forward equations printed on the frame and the "output-layer gradient known, hidden-layer gradient derived" framing.

## Corrections / notes

- Denominator index: the frame prints "O_j = f(Net_j) = 1/(1+e^{−Net_i})" with the exponent's subscript read as i by the parse; the sigmoid is a function of that neuron's own net input, so the certified form e^{−Net_j} is correct. Recreate as Net_j.
- Weight index convention: the parse shows Net_j = Σ_i (w_ij·O_i) here but Σ_i (w_ji·O_i) on the neighbouring slides. Both appear in the literature (some texts index w_ij from input i to output j, others w_ji); the frame's own derivation on slides 19–20 uses w_ji, so w_ji is the consistent reading for this deck.
- "(Effect of Net_k on Calculated Error is known from O/P Layer)" is standard: at the output layer the error gradient ∂E/∂Net_k = −δ_k is computable directly from the target; hidden-layer gradients must then be back-propagated. Matches sources.
- No other contradictions found.

# Slide 7 — "Neural Network Model" (forward-pass notation: Net_j, O_j, sigmoid, MSE error)

Frame labels: Input Sample, Target Label, Net_i / O_i / w_ji, Output 1, Class 1/2/m,
Node Bias, For Layer j, Previous Layer (i), "Current Layer is Output Layer (You are here)";
equations Net_j = Σ_i (w_ji O_i), O_j = 1/(1+e^(−Net_j)), E = ½ Σ_j (t_j − O_j)².

## Sources

1. **U. Toronto CSC411 — lec10 handout (PDF)**
   (https://www.cs.toronto.edu/~jlucas/teaching/csc411/lectures/lec10_handout.pdf)
   Confirms feedforward/backprop notation: net_j = Σ_i w_ji O_i with w_ji the
   weight from neuron i (previous layer) to neuron j (current layer).
2. **Wikipedia — Backpropagation** (https://en.wikipedia.org/wiki/Backpropagation)
   Confirms the same notation family (O_i = previous-layer activation feeding
   output-layer unit j) and the overall gradient-descent training loop.
3. **StackExchange — "error signal" in backprop**
   (https://stats.stackexchange.com/questions/166944/in-back-propagation-for-neural-networks-what-exactly-is-the-error-signal)
   Confirms E = ½ Σ_j (t_j − O_j)² as the sum-squared error with t_j target,
   O_j network output; the ½ cancels the 2 when differentiated.
4. **StackOverflow — error using sigmoid in backprop**
   (https://stackoverflow.com/questions/11627773/calculate-the-error-using-a-sigmoid-function-in-backpropagation)
   Confirms O_j = 1/(1+e^(−Net_j)) and the derivative identity
   dO_j/dNet_j = O_j(1 − O_j) used on slides 9–10.
5. **Swarthmore CS81 — BackPropDeriv (PDF)**
   (https://www.cs.swarthmore.edu/~meeden/cs81/s10/BackPropDeriv.pdf)
   Confirms standard textbook treatment of this exact notation (net, sigmoid
   output, squared error, bias).

## Corrections / notes

- Parse shows "Oj=f (Netj)= 1 −Netj 1+e" — this is the OCR of the stacked
  fraction O_j = σ(Net_j) = 1/(1+e^(−Net_j)); e-exponent is on Net_j with a
  minus sign. Recreation must render the stacked fraction (house 2D-equation law).
- Net_j is drawn as Σ_i (w_ji O_i) without bias inside the sum; the slide labels
  a separate "Node Bias", consistent with the common variant net_j = Σ w_ji O_i
  + b_j. No correction needed — recreate the frame as shown.

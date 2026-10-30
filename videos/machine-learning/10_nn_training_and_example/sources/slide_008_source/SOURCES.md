# Slide 8 — Neural network diagram asking ∂E/∂w_ij (red "?"); Error/Class bar

No title. Frame: beige box with MLP diagram (input dots → blue Σ nodes → green Σ
nodes, labels Net/O/w, "Multi Bias", up arrows, purple "1" circle), Output 1/2/m,
vertical red "Error" bar with Class 1/2/m, and ∂E/∂w_ij followed by a large red "?".

## Sources

1. **U. Toronto CSC321 — L06 Backpropagation (PDF)**
   (https://www.cs.toronto.edu/~rgrosse/courses/csc321_2017/readings/L06%20Backpropagation.pdf)
   Confirms the diagram's meaning: layered MLP with Σ (net-input) nodes, weights
   w_ji from previous layer i to current layer j, biases, and outputs O_1..O_m.
2. **Medium — Derivation of the Backpropagation Algorithm**
   (https://medium.com/@shakeraafreen12/derivation-of-the-backpropagation-algorithm-5002a047b399)
   Confirms the quantity posed by the red "?": the chain-rule derivation of
   ∂E/∂w for the output layer, i.e. what slides 9–10 then compute.
3. **Yangli (LFD recitation) — backprop notes (PDF)**
   (https://yangli-feasibility.com/home/classes/lfd2024fall/media/recitation2_part1.pdf)
   Confirms ∂E/∂w_jk = δ_k · a_j (output layer) with δ_k = (o_k − t_k)σ'(z_k) —
   the answer the "?" sets up.
4. **Wikipedia — Backpropagation** (https://en.wikipedia.org/wiki/Backpropagation)
   Confirms errors flow backward from output ("Error" bar) toward earlier layers
   while activations flow forward.

## Corrections / notes

- none found. Σ nodes = net-input/summation operator (standard); "Class 1/2/m"
  = target-label rows of the output vector t (consistent with slide 7's labels).
- Note for builders: the answer to the posed ∂E/∂w_ij is NOT on this frame; it is
  derived on slides 9–10. Do not add it to this slide's recreation.

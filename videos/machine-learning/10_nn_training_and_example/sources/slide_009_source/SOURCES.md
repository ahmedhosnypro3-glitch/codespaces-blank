# Slide 9 — "Gradient Descent": chain-rule derivation of ∂E/∂w_ji (output layer, sigmoid)

Frame equations: W_ji^updated = W_ji^old − η ∂E/∂W_ji; W_ji^updated = W_ji^old + Δ_ji;
Δ_ji = −η ∂E/∂W_ji; E = ½ Σ_j (t_j − O_j)²; sigmoid O_j = 1/(1+e^(−Net_j));
Net_j = Σ_i (w_ji O_i); ∂E/∂O_j = −(t_j − O_j); ∂O_j/∂Net_j = O_j(1 − O_j);
∂Net_j/∂W_ji = O_i; ∂E/∂W_ji = −(t_j − O_j)·O_j(1 − O_j)·O_i.

## Sources

1. **IBM — Backpropagation** (https://www.ibm.com/think/topics/backpropagation)
   Confirms the gradient-descent weight update w_new = w_old − η ∂E/∂w and the
   three-step chain rule E → O → Net → w for output-layer weights.
2. **U. Toronto CSC321 — L06 Backpropagation (PDF)**
   (https://www.cs.toronto.edu/~rgrosse/courses/csc321_2017/readings/L06%20Backpropagation.pdf)
   Confirms ∂E/∂o_k = −(t_k − o_k), ∂o_k/∂z_k = σ'(z_k), ∂z_k/∂w_kj = o_j, and
   the product ∂E/∂w = −(t − O)·O(1 − O)·O_i for sigmoid + squared error.
3. **Wikipedia — Backpropagation** (https://en.wikipedia.org/wiki/Backpropagation)
   Confirms the chain-rule factorization of the weight gradient and the update
   rule form used on this slide.
4. **Superannotate — Gradient Descent guide**
   (https://www.superannotate.com/blog/guide-to-gradient-descent-algorithms)
   Confirms the general rule θ ← θ − η ∂E/∂θ with η the learning rate, matching
   the slide's η notation and "Updated = old − η ∂E/∂W_ji" form.
5. **Swarthmore CS81 — BackPropDeriv (PDF)**
   (https://www.cs.swarthmore.edu/~meeden/cs81/s10/BackPropDeriv.pdf)
   Confirms the same derivation with bias handled separately
   (∂E/∂bias = δ), consistent with the slide's w-only update here.

## Corrections / notes

- Parse renders one factor as "Oj(i−Oj)" — standard (and the slide's own final
  line on slide 10) is O_j(1 − O_j); "i" is an OCR garble of "1". The
  mathematically correct sigmoid derivative is O_j(1 − O_j) — render 2D per house
  law and verify the numeral against the original frame.
- ∂E/∂W_ji product is negative, so Δ_ji = −η·∂E/∂W_ji > 0 matches the slide's
  "old + Δ_ji" restatement. Verified consistent.

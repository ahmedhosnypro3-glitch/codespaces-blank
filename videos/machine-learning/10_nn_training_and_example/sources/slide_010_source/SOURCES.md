# Slide 10 — "Gradient Descent": delta rule δ_j and Δ_ji = η δ_j O_i (output layer)

Frame: W_ji^updated = W_ji^old − η ∂E/∂W_ji; W_ji^updated = W_ji^old + Δ_ji;
Δ_ji = −η ∂E/∂W_ji; E = ½ Σ_j (t_j − O_j)²; sigmoid O_j = 1/(1+e^(−Net_j));
Net_j = Σ_i (w_ji O_i); ∂E/∂O_j = −(t_j − O_j); ∂O_j/∂Net_j = O_j(1 − O_j);
∂Net_j/∂W_ji = O_i;
∂E/∂W_ji = ∂E/∂O_j · ∂O_j/∂Net_j · ∂Net_j/∂W_ji = −δ_j · O_i;
δ_j = −∂E/∂Net_j = (t_j − O_j)·O_j(1 − O_j)  ("δ_j depends on j ONLY");
final: Δ_ji = −η ∂E/∂W_ji = η δ_j · O_i, δ_j = (t_j − O_j)·O_j(1 − O_j) for
the output layer.

## Sources

1. **Brilliant.org — Backpropagation** (https://brilliant.org/wiki/backpropagation/)
   Confirms the delta (local-gradient) term δ_j = (t_j − O_j)·O_j(1 − O_j) for a
   sigmoid output unit under squared error, and Δw = η δ O_i update form.
2. **Wikipedia — Backpropagation** (https://en.wikipedia.org/wiki/Backpropagation)
   Confirms output-layer δ = (t − o)·σ'(net), ∂net/∂w = O_i, and
   w_new = w_old − η ∂E/∂w for gradient-descent training.
3. **Matt Mazur — A Step-by-Step Backpropagation Example**
   (https://mattmazur.com/2015/03/17/a-step-by-step-backpropagation-example/)
   Confirms the same output-layer weight update arithmetic
   (η · δ_j · O_i) with concrete numbers.
4. **IBM — Backpropagation** (https://www.ibm.com/think/topics/backpropagation)
   Confirms δ_j = ∂Loss/∂z_j depends only on unit j, while the weight gradient
   additionally scales by the previous layer's activation O_i.
5. **U. Toronto CSC321 — L06 Backpropagation (PDF)**
   (https://www.cs.toronto.edu/~rgrosse/courses/csc321_2017/readings/L06%20Backpropagation.pdf)
   Confirms "δ depends on j only" and ∂E/∂w_jk = δ_k a_j decomposition used here.

## Corrections / notes

- Sign convention check: the slide defines δ_j = −∂E/∂Net_j = (t_j − O_j)·O_j(1−O_j),
  giving Δ_ji = +η δ_j O_i. Some texts define δ = ∂E/∂net (opposite sign) or write
  δ = (O_j − t_j)·O_j(1−O_j); the slide's statement is internally consistent and
  equivalent to w − η ∂E/∂w. No correction needed — recreate as shown.
- All equations match the standard textbook output-layer derivation for sigmoid
  activation + MSE loss (slide continues to hidden layers next).

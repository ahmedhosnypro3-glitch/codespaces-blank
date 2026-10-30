# Slide 6 — "Update Weights of Output Layer" (Weights from previous layer to output layer)

Frame content: title + subtitle only (decorative section slide introducing the
output-layer weight-update step of neural-network training). Research confirms the
algorithmic meaning of that title so the recreation's context is right.

## Sources

1. **IBM — Backpropagation** (https://www.ibm.com/think/topics/backpropagation)
   Confirms output-layer weights (previous layer → output layer) are updated by
   gradient descent using the error contribution through each weight.
2. **Wikipedia — Backpropagation** (https://en.wikipedia.org/wiki/Backpropagation)
   Confirms the standard weight-update rule w_new = w_old − η ∂E/∂w applied to
   weights feeding the output layer.
3. **Univ. of Toronto CSC321 — L06 Backpropagation (PDF)**
   (https://www.cs.toronto.edu/~rgrosse/courses/csc321_2017/readings/L06%20Backpropagation.pdf)
   Confirms the derivation structure this slide introduces: output-layer weight
   gradient ∂E/∂w_jk = δ_k · a_j with δ_k = (o_k − t_k)σ'(z_k).
4. **Edinburgh Inf1CG — MLP Backprop lecture (PDF)**
   (https://groups.inf.ed.ac.uk/teaching/cogsci/course/post/week_02/inf1cg_l06_mlp_backprop.pdf)
   Confirms "update weights of the output layer" is the first (delta-rule) stage
   of MLP backprop weight updating.

## Corrections / notes

- none found (title/subtitle text is not a verifiable equation; sources match
  its meaning). The derivation introduced here is carried out on slides 9–10.

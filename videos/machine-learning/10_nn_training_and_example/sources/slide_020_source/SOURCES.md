# Slide 20 — Backpropagation Weight Update Rule (delta rule, hidden layer)

## Sources

- "Delta rule", Wikipedia — https://en.wikipedia.org/wiki/Delta_rule
  Confirms the update rule printed on the frame: Δw_ji = −η·∂E/∂w_ji = η·δ_j·O_i, with η the learning rate and O_i the upstream activation.
- BackPropDeriv, Swarthmore CS81 lecture notes — https://www.cs.swarthmore.edu/~meeden/cs81/s10/BackPropDeriv.pdf
  Confirms the intermediate form ∂E/∂w_ji = Σ_{k=1}^{m} (−δ_k w_kj)·O_j(1−O_j)·O_i, i.e. the four factors already verified on slide 19 substituted in.
- "Derivation of backpropagation" (The Clever Machine) — https://dustinstansbury.github.io/theclevermachine/derivation-backpropagation
  Confirms δ_j = Σ_k w_kj δ_k · O_j(1−O_j) as the hidden-layer local gradient, stated for each hidden node j.
- "Backpropagation step-by-step derivation" (Towards Data Science) — https://towardsdatascience.com/backpropagation-step-by-step-derivation-99ac8fbdcc28/
  Confirms the sigmoid derivative factor O_j(1−O_j) inside δ_j and the gradient-descent step w ← w − η·∂E/∂w.
- "8th Lecture: Delta Rule Learning" (Philadelphia University) — https://www.philadelphia.edu.jo/academics/amahasneh/uploads/8th_lecture_Delta_Rule_Learning_s1_21_22.pdf
  Confirms the delta-rule framing (Widrow–Hoff/Boltzmann-style update) and the learning-rate η's role.

## Corrections / notes

- "Δ_ji = −η∂E/∂W_ji" mixes lowercase w_ji and capital W_ji for the same quantity; the frame otherwise uses w_ji throughout. Recreate with w_ji (W is not a separate matrix here).
- The last chain link should read ∂Net_j/∂w_ji = O_i (the derivative of the neuron's own net w.r.t. the incoming weight is the upstream output). The certified JSON has this right; the parse transcript's "∂Net_j/∂w_jj = O_i" is an OCR artifact of the doubled subscript.
- Sign convention: the frame defines δ with ∂E/∂Net_k → −δ_k, then Δw = −η∂E/∂w = ηδ_jO_i. Self-consistent, and a standard variant. Nielsen's text defines δ with the opposite sign (δ = ∂C/∂z) and therefore writes Δw = −ηδa; the two are the same rule under opposite δ definitions. Convention note only.
- m in Σ_{k=1}^{m} is the number of output classes/nodes in the next layer (matching the "Class 1 … Class m" error columns on slides 16–19). Consistent.
- No other contradictions with the sources found.

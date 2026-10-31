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
## Audit

Audited by lane S scope `b_src_2` (web-source audit), 2026-10-31. Method: independent agy
web-search; cross-read against `analysis/parse/slide_020.parse.md` and
`analysis/slide_020_final.json` (title "Backpropagation Weight Update Rule").

Questions asked:
1. Is `Δw_ji = −η·∂E/∂w_ji = η·δ_j·O_i` the standard delta/weight-update rule?
2. Is `∂E/∂w_ji = Σ_{k=1}^{m}(−δ_k w_kj)·O_j(1−O_j)·O_i` the correct substitution of the
   four factors from slide 19?
3. Is `δ_j = Σ_{k=1}^{m} δ_k w_kj · O_j(1−O_j)` the hidden-layer δ, and is the frame's
   `m` the number of next-layer nodes?
4. Is the frame's sign convention (δ defined via `∂E/∂Net_k → −δ_k`) valid.

Answers:
- Q1 **CONFIRMED**. Search returns `Δw_ji = η·δ_j·O_i` (`w_new = w_old + Δw`) with `η` the
  learning rate and `O_i` the upstream activation — exactly the frame's terminal result.
- Q2 **CONFIRMED**. The four factors verified on slide 19 substitute to exactly this product.
- Q3 **CONFIRMED**. Search derives `δ_j = O_j(1−O_j)·Σ_k(δ_k·w_kj)` step by step, including
  the factored-out `O_j(1−O_j)` because it does not depend on `k`. `m` = number of
  next-layer nodes (matching the "Class 1 … Class m" error columns on slides 16–19).
- Q4 **CONFIRMED** as a legitimate convention. Multiple sources write δ with the opposite
  sign and therefore `Δw = −ηδO`; the two are the same rule under opposite δ definitions.
  Convention note only, not a defect.

Verdicts per claim:
- `Δw_ji = −η∂E/∂W_ji` mixing lowercase/uppercase — **CONFLICT** with the frame's own `w_ji`;
  recreate with `w_ji` (W is not a separate matrix here).
- `∂Net_j/∂w_ji = O_i` as the last chain link — **CONFIRMED**.
- Parse transcript's `∂Net_j/∂w_jj = O_i` — **CONFLICT** (OCR artifact of the doubled
  subscript); the certified JSON has the correct `w_ji`.
- `Σ_{k=1}^{m}` bounds and `m`'s meaning — **CONFIRMED**.
- Sign convention — **CONFIRMED** (self-consistent standard variant).

New sources found during audit (real URLs, not previously cited):
- Wikipedia, "Delta rule" — https://en.wikipedia.org/wiki/Delta_rule
  Per-sample weight update `Δw_ji = α(t_j−y_j)g'(h_j)x_i`, the delta rule in its
  Widrow–Hoff/LMS form, i.e. the same rule the frame states for a hidden unit.
- FU Berlin SOGA notes, "Widrow-Hoff rule" —
  https://www.geo.fu-berlin.de/en/v/soga-py/Machine-learning/Artifical-Neural-Networks/Widrow-Hoff-rule/index.html
- GeeksforGeeks, "Widrow-Hoff Algorithm" —
  https://www.geeksforgeeks.org/machine-learning/widrow-hoff-algorithm/

Audit summary: all formulas standard and source-confirmed. Only cosmetic index/mixed-case
defects on the frame and one parse OCR artifact to avoid.

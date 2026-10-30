# Source Research — slide_021 (At Hidden Layer)

Topic: hidden-layer backpropagation delta rule — δj = Oj(1−Oj)·Σk(δk·wkj) and Δwji = η·Oi·δj.

## Verified math (matches slide verbatim)
- δj ≡ −∂E/∂net_j (Rumelhart/Hinton/Williams 1986 "delta" = local gradient).
- Chain rule over the downstream layer: δj = f'(net_j)·Σ_k δk·wkj; with sigmoid
  activation f'(net_j) = Oj(1−Oj) this is exactly the slide's δj formula.
- Δwji = −η·∂E/∂wji = η·δj·Oi, since ∂net_j/∂wji = Oi. Slide's "∆ ji = η Oi δj"
  is the same rule written in reversed factor order.
- Notation: i = upstream unit, j = hidden unit, k = downstream unit, wkj = weight
  j→k, wji = weight i→j; net_j = Σ_i wji·Oi + b_j (bias not in the shown rule).
- The Oj(1−Oj) factor is sigmoid-specific; the general rule δj = f'(net_j)·Σ_k δk·wkj
  also covers ReLU (slide 25) with f'(net_j) = 1{net_j ≥ 0}.

## Sources
- Swarthmore CS81 lecture notes "BackPropDeriv.pdf" —
  https://www.cs.swarthmore.edu/~meeden/cs81/s10/BackPropDeriv.pdf
  Step-by-step derivation of δj = f'(net_j)·Σ_k δk·wkj and Δwji = η·δj·Oi.
- "Backpropagation step by step derivation" (Towards Data Science) —
  https://towardsdatascience.com/backpropagation-step-by-step-derivation-99ac8fbdcc28/
  Confirms δ = −∂E/∂net and Δw = −η·∂E/∂w chain used to reach the slide formulas.
- "Understanding neural network backpropagation" (Stack Overflow) —
  https://stackoverflow.com/questions/2190732/understanding-neural-network-backpropagation
  Canonical Q&A with the same hidden-layer delta formula form.
- "Backpropagation for dummies" (Medium / Analytics Vidhya) —
  https://medium.com/analytics-vidhya/backpropagation-for-dummies-e069410fa565
  Confirms the sum over next-layer units k and the wkj weighting.

## Corrections / notes
- None found: both formulas on slide 21 match the standard sigmoid-backprop
  delta rule exactly; no numeric or structural discrepancy against sources.
- Build hint (not a correction): the small sketch labels Oi / wji / wkj / δk / bk are
  standard notation for the i→j→k path; render with the same index positions.

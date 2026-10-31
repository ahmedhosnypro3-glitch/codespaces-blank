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
## Audit

Audited by lane S scope `b_src_2` (web-source audit), 2026-10-31. Method: independent agy
web-search; cross-read against `analysis/parse/slide_021.parse.md` and
`analysis/slide_021_final.json` (title "At Hidden Layer"; equations
`Δ_ji = η O_i O_j(1−O_j) [∑_k (δ_k w_kj)]`, `Δ_ji = η O_i δ_j`,
`Where: δ_j = O_j(1−O_j) [∑ (δ_k w_kj)]`; labels `O_i, w_ji, w_kj, δ_k, b_k`).

Questions asked:
1. Is `δ_j = O_j(1−O_j)·[∑_k (δ_k w_kj)]` the standard hidden-layer delta for sigmoid?
2. Is `Δ_ji = η·O_i·δ_j` equivalent to the expanded form on the frame?
3. Is `∂net_j/∂w_ji = O_i` the correct justification for the `O_i` factor?
4. Is the `O_j(1−O_j)` factor sigmoid-specific (and therefore not generally applicable)?
5. Are the sketch labels (`O_i / w_ji / w_kj / δ_k / b_k`) standard notation?

Answers:
- Q1 **CONFIRMED**. Independent search derives the rule from `δ_j ≡ −∂E/∂net_j` and the
  chain rule over the next layer, arriving at exactly `δ_j = O_j(1−O_j) Σ_k(δ_k w_kj)`.
- Q2 **CONFIRMED**. `Δ_ji = η O_i δ_j` is the expanded rule with `δ_j` substituted; the
  frame prints both forms, which is correct.
- Q3 **CONFIRMED**. `net_j = Σ_i w_ji O_i + b_j` ⇒ `∂net_j/∂w_ji = O_i`.
- Q4 **CONFIRMED**. The general rule is `δ_j = f'(net_j)·Σ_k(δ_k w_kj)`; for sigmoid
  `f'(net_j) = O_j(1−O_j)`, for ReLU `f'(net_j) = 1{net_j ≥ 0}`.
- Q5 **CONFIRMED**. Standard `i`=upstream, `j`=hidden, `k`=downstream convention.

Verdicts per claim:
- `δ_j = O_j(1−O_j)[∑_k(δ_k w_kj)]` — **CONFIRMED**.
- `Δ_ji = η O_i δ_j` — **CONFIRMED**.
- `Δ_ji = η O_i O_j(1−O_j)[∑_k(δ_k w_kj)]` — **CONFIRMED**.
- Notation `i`/`j`/`k` and `w_kj`/`w_ji` direction — **CONFIRMED**.
- Bias notation `b_k` in the sketch — **CONFIRMED** (consistent with net = Σw·O + b).
- No numeric claims on this slide; nothing to recompute.

New sources found during audit (real URLs, not previously cited):
- Math StackExchange, "Backpropagation hidden layer error" —
  https://math.stackexchange.com/questions/4686558/backpropagation-hidden-layer-error
- MIT OCW 9.641, "Lecture 20: Backprop" —
  https://ocw.mit.edu/courses/9-641j-introduction-to-neural-networks-spring-2005/5d46d3b6e32a5120fe9893193c31e926_lec20_backprop.pdf

Audit summary: the slide's two formulas are exactly the standard sigmoid-backprop hidden-layer
delta rule. No conflicts found; nothing to correct.

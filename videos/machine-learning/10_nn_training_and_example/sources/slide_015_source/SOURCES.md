# Slide 015 — "Neural Network Model (Weights of hidden layer AFFECT Calculated Error)"

## Sources

1. **Wikipedia — Backpropagation** (https://en.wikipedia.org/wiki/Backpropagation) — confirms hidden-layer weights enter the
   loss through δ_k and w_kj, so ∂E/∂w_ji = O_i·O_j(1 − O_j)·Σ_k(δ_k·w_kj).
2. **Swarthmore CS81 — Backprop derivation (PDF)** (https://www.cs.swarthmore.edu/~meeden/cs81/s10/BackPropDeriv.pdf) — confirms
   the chain rule from a hidden weight to the total error across the next layer.
3. **Toward Data Science — Backpropagation step-by-step derivation** (https://towardsdatascience.com/backpropagation-step-by-step-derivation-99ac8fbdcc28/) — confirms
   hidden-layer weights are updated via the back-propagated error sum, i.e. they do affect the calculated error.
4. **StackOverflow — partial derivatives for hidden-layer backprop** (https://stackoverflow.com/questions/30600284/java-partial-derivatives-for-back-propagation-of-hidden-layer) — confirms
   ∂E/∂w_ji expressed through δ_j for a sigmoid hidden unit (O_j(1 − O_j) factor).
5. **CMU 11-785 — Stochastic Gradient Descent lecture (PDF)** (https://deeplearning.cs.cmu.edu/S21/document/slides/lec7.stochastic_gradient.pdf) — confirms
   the total error summed over all training samples X: E = ½Σ_xΣ_j(t_j − O_j)² (batch objective).
6. **UofT CS486/686 — Neural Networks lecture notes (PDF)** (https://www.cs.toronto.edu/~axgao/cs486686_f21/lecture_notes/Lecture_09_on_Neural_Networks_2.pdf) — confirms
   the squared-error cost with target t and network output O per output unit.

## Verified content for this slide

- Net_j = Σ_i(w_ji·O_i) (+ bias) — net input of a hidden node; same as slide 014.
- E = ½Σ_j(t_j − O_j)²; E = ½Σ_xΣ_j(t_j − O_j)² — per-sample and total(sample-summed) error.
- Hidden-layer weights AFFECT the calculated error — verified: ∂E/∂w_ji ≠ 0 via back-propagated δ_k·w_kj.
- "Note: Layer j is NOT Output Layer" — correct; hidden units require the back-propagated delta sum.

## Corrections / notes

- **None found.** The slide's claim (hidden weights affect the error) and its two error expressions
  are both standard. The Σ_x form lacks a 1/N normalizer, which is a legitimate per-course
  convention (sum rather than mean) — sources note both conventions exist; not a correction.
- Notation remark only: `wjj` in `Net_j = Σ_i(wjj Oi)` is a frame typo for `wji`. On-frame text is DATA.

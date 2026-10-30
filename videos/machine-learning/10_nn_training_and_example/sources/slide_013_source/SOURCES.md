# Slide 013 — "Update Weights of Hidden Layer (Weights from previous layer to Hidden layer)"

## Sources

1. **Wikipedia — Backpropagation** (https://en.wikipedia.org/wiki/Backpropagation) — confirms the hidden-layer local
   gradient δ_j = (Σ_k δ_k·w_kj)·σ'(z_j) and the resulting weight update w_ij ← w_ij − η·δ_i·a_j.
2. **Swarthmore CS81 — Backprop derivation (PDF)** (https://www.cs.swarthmore.edu/~meeden/cs81/s10/BackPropDeriv.pdf) — confirms
   that hidden neurons have no direct target: their δ is the weighted sum of the NEXT layer's deltas.
3. **Toward Data Science — Backpropagation step-by-step derivation** (https://towardsdatascience.com/backpropagation-step-by-step-derivation-99ac8fbdcc28/) — confirms
   the previous-layer-to-hidden weight update Δw_ji = η·O_i·δ_j with δ_j back-propagated from layer k.
4. **StackOverflow — partial derivatives for hidden-layer backprop** (https://stackoverflow.com/questions/30600284/java-partial-derivatives-for-back-propagation-of-hidden-layer) — confirms
   δ_j = O_j(1 − O_j)·Σ_k δ_k·w_kj for a sigmoid hidden unit.
5. **Tufts CS135 lecture 18 notes** (https://www.cs.tufts.edu/comp/135/2020s/lectures/slides/lec18.pdf) — confirms
   the same hidden-layer delta expression in a sigmoid MLP.
6. **365 Data Science — Backpropagation** (https://365datascience.com/trending/backpropagation/) — confirms
   the error-signal sum over next-layer units weighted by outgoing weights w_kj.

## Verified content for this slide

- Hidden-layer weight update: Δw_ji = η·O_i·δ_j (weights from previous layer i into hidden node j).
- Hidden-layer delta: δ_j = O_j(1 − O_j)·Σ_k(δ_k·w_kj) — sigmoid derivative times back-propagated error.
- Net_j = Σ_i w_ji·O_i + b_j; E = ½Σ_j(t_j − O_j)².
- Note "Layer j is NOT the output layer" — correct: hidden units need back-propagation, not a target.

## Corrections / notes

- **None on the formulas.** The slide is a title/divider slide (only title + a parenthetical plus the
  architecture graphic in the parse record), so the only verifiable claim is its title, which matches
  the standard algorithm.
- Diagram-glyph remark only: the frame prints `N ij` near the summation (OCR noise for `Net_j`);
  the standard subscript for a weight from unit i into unit j is w_ji. On-frame text is DATA.

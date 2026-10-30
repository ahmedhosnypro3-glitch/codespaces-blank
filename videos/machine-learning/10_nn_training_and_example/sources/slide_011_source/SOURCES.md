# Slide 011 — "Updated Weights of Output Layer (Calculated Error is affected by Net)"

## Sources

1. **Wikipedia — Delta rule** (https://en.wikipedia.org/wiki/Delta_rule) — confirms output-layer local gradient
   δ_j = (t_j − O_j) · O_j(1 − O_j) under MSE + sigmoid.
2. **NYCU ML course notes (MatlabML_class10_YTWu.pdf)** (https://cflu.lab.nycu.edu.tw/MatlabML_class10_YTWu.pdf) — confirms
   δ_j = −∂E/∂Net_j, σ'(z) = O(1−O), and ∆w_ji = η·δ_j·x_i.
3. **Wikipedia — Backpropagation** (https://en.wikipedia.org/wiki/Backpropagation) — confirms chain-rule decomposition
   ∂E/∂w_ji = (∂E/∂Net_j)(∂Net_j/∂w_ji) and E = ½Σ(t−O)².
4. **Analytics Vidhya — Backpropagation for Beginners** (https://medium.com/analytics-vidhya/backpropagation-for-dummies-e069410fa585) — confirms
   one δ per output node and the η·δ·O_i weight-update form.
5. **AI StackExchange — backpropagation delta formula** (https://ai.stackexchange.com/questions/42447/what-is-the-backpropagation-formula-to-calculate-delta-and-update-weights) — confirms
   ∆ji = η·Oi·δj as applied to output-layer weights.
6. **Mazur — A Step-by-Step Backpropagation Example** (https://mattmazur.com/2015/03/17/a-step-by-step-backpropagation-example/) — worked
   numeric example matching the slide's sigmoid + MSE update.

## Equations on the slide (all verified)

- ∆_ji = −η ∂E/∂w_ji = −(∂E/∂Net_j)(∂Net_j/∂w_ji) = η·δ_j·O_i — standard gradient-descent delta rule.
- δ_j = −∂E/∂Net_j, one δ per output node j — standard local-gradient definition.
- Output layer + sigmoid ⇒ δ_j = (t_j − O_j)·O_j(1 − O_j) ⇒ ∆_ji = η(t_j − O_j)·O_j(1 − O_j)·O_j.
- Net_j = Σ_i w_ji·O_i + b_j (bias); O_j = σ(Net_j); E = ½Σ_j (t_j − O_j)².

## Corrections / notes

- **None on the formulas.** Every equation matches standard backpropagation textbooks for an
  output layer with sigmoid activation and MSE loss.
- Notation remark only: the frame writes `Neti`/`wjj` in the diagram (self-subscript); the
  intended standard form is Net_j = Σ_i w_ji·O_i + b_j. Sources use w_ji for a weight from
  unit i to unit j. On-frame text is DATA — no change to the recreation.

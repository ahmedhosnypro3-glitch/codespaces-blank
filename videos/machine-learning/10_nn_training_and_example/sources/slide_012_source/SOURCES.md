# Slide 012 — "At Output Layer" (output-node δ diagram + weight update)

## Sources

1. **Wikipedia — Delta rule** (https://en.wikipedia.org/wiki/Delta_rule) — confirms the output-node error signal
   δ_j = (t_j − O_j)·O_j(1 − O_j) and ∆w = η·δ_j·input.
2. **NYCU ML course notes (MatlabML_class10_YTWu.pdf)** (https://cflu.lab.nycu.edu.tw/MatlabML_class10_YTWu.pdf) — confirms
   the same derivation and the numeric weight-update example for a sigmoid output unit.
3. **Wikipedia — Backpropagation** (https://en.wikipedia.org/wiki/Backpropagation) — confirms the diagram items:
   O_i (previous-layer activation), w_ji (incoming weight), O_j (unit output), t_j (target), δ_j (local gradient).
4. **Tufts CS135 lecture 18 notes** (https://www.cs.tufts.edu/comp/135/2020s/lectures/slides/lec18.pdf) — confirms
   δ_j = O_j(1 − O_j)·(t_j − O_j) as the output-layer delta in sigmoid networks.
5. **StackOverflow — delta rule teaching algorithm** (https://stackoverflow.com/questions/9102296/delta-rule-neural-network-teaching-algorithm-explanation-necessary) — confirms
   the η (learning rate) factor placement and the sign convention in ∆_ji = η·O_i·δ_j.
6. **Mazur — Step-by-Step Backpropagation Example** (https://mattmazur.com/2015/03/17/a-step-by-step-backpropagation-example/) — numeric
   cross-check of the same formula with a sigmoid output node.

## Equations on the slide (all verified)

- ∆_ji = η·O_i·δ_j — gradient-descent update of a weight into output node j.
- δ_j = O_j(1 − O_j)·(t_j − O_j) — correct for sigmoid activation + MSE loss (½(t−O)²).
- Diagram roles O_i, w_ji, O_j, t_j, δ_j — all match the standard backprop symbol table.

## Corrections / notes

- **None found.** The formulas are the textbook output-layer delta rule; no numeric values,
  dataset, or library reference appear on the slide, so nothing further to cross-check.
- The parse transcript lists garbled single-letter labels (`Eror`, `Wji`, `Dj`, `Tj`) — these
  are OCR artifacts of the diagram's O/w/t/δ glyphs, not slide errors.

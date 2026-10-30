# Slide 034 — Forward Calculations (network diagram + error-vs-iteration table)

Frame topic: the same 2-3-2 network (inputs x₁=1, x₂=5; hidden nodes 3/4/5 with
O₃/O₄/O₅; outputs 6/7 with O₆/O₇; targets t₆=0, t₇=1; Bias; η=5) plus a table with
columns O₆ | O₇ | Squared Error over rows "Initial Weights, Iteration 1–5, …, Target".
Data taken from `analysis/slide_034_final.json` + `analysis/parse/slide_034.parse.md`.

## Sources

- Matt Mazur — "A Step by Step Backpropagation Example"
  (https://mattmazur.com/2015/03/17/a-step-by-step-backpropagation-example/) —
  canonical worked example using E = ½(t−O)² per output and the O₆/O₇ + squared-error
  layout this slide tabsulates.
- 365 Data Science — "What Is Backpropagation?"
  (https://365datascience.com/trending/backpropagation/) — confirms E = ½Σ(tₖ−Oₖ)²
  (or Σ(tₖ−Oₖ)² depending on convention) as the summed squared error over outputs.
- University of Illinois CS447 — "Lecture 20" (https://courses.grainger.illinois.edu/cs447/fa2018/Slides/Lecture20.pdf)
  — lecture slide source giving the same σ(z)=1/(1+e^(−z)), δₖ=(Oₖ−tₖ)·Oₖ(1−Oₖ) and
  E = ½Σ(tₖ−Oₖ)²; the closest published match to this frame's notation (Oⱼ, tₖ, Bias).
- MRCET — "Neural Networks" digital notes (https://www.mrcet.com/downloads/digital_notes/CSE/III%20Year/AIML/Neural-Networks.pdf)
  — confirms the forward pass netⱼ = Σ(wⱼᵢ·Oᵢ) + bⱼ and the target-column/error-table
  presentation of a training run.
- Wikipedia — "Logistic function" (https://en.wikipedia.org/wiki/Logistic_function)
  — σ(z)=1/(1+e^(−z)); σ(1.3312)=0.791, matching the frame's initial O₆ and O₇.

## Corrections / notes

- **"Squared Error" column lacks the ½ factor — CONFIRMED by recomputation.** Every row
  matches E = Σₖ(tₖ−Oₖ)² exactly, not E = ½Σₖ(tₖ−Oₖ)²:
  Initial 0.791²+0.209² = 0.669362 (slide says 0.669362; the ½-form would be 0.334681).
  Iteration 1: 0.352²+0.165² = 0.151129 (½-form 0.075565). Iterations 2–5 reproduce
  0.038729 / 0.025186 / 0.018868 / 0.01517 with the same Σ(t−O)² rule. All six rows
  verified to 1e-5. **The recreation must render the frame's numbers verbatim** — this
  is a note about the frame's convention (squared error summed without ½), not a defect
  to "fix"; flagging it so the error-trend plot is computed the same way if regenerated.
- **Sign convention:** sources (Illinois) write δₖ = (Oₖ−tₖ)·Oₖ(1−Oₖ); this frame's
  sibling slide 31 uses δₖ = Oₖ(1−Oₖ)(tₖ−Oₖ) with a `+` update. Same math, opposite
  signs — the frame's convention wins, matching slide 31.
- **Convergence trend CORRECT:** error falls monotonically 0.669362 → 0.01517 across
  iterations 1–5 and the outputs move monotonically toward the targets (O₆: 0.791→0.091
  toward t₆=0; O₇: 0.791→0.917 toward t₇=1). The large red down-arrow on the table's
  right edge is consistent with a decreasing-error reading.
- The final "Target" row (0, 1) matches t₆=0, t₇=1 in the diagram — consistent.
- η=5 is unusually large; the frame's own run still converges over these 5 iterations,
  so no contradiction to flag — but a rebuild must not silently substitute a smaller η.

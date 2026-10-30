# Slide 033 — Initialized Weights vs. Updated Weights (after Iteration #10)

Frame topic: two stacked neural-network diagrams of the SAME 2-3-2 network — the top
panel at initialization, the bottom panel after 10 training iterations (η=5). Layer
structure: Input (x₁, x₂, Bias) → Hidden (3, 4, 5) → Output (6, 7) → Target (t₆, t₇),
with numeric weight labels on every directed edge. Data taken from
`analysis/isolated_033/slide_033_raw.json` + `slide_033.parse.md`.

## Sources

- Wikipedia — "Logistic function" (https://en.wikipedia.org/wiki/Logistic_function)
  — σ(z)=1/(1+e^(−z)); every Oⱼ printed beside a node is a sigmoid output in (0,1).
- 365 Data Science — "What Is Backpropagation?"
  (https://365datascience.com/trending/backpropagation/) — confirms that after N
  iterations each edge weight has been updated N times by ΔW = η·δⱼ·Oᵢ, which is what
  distinguishes the bottom panel's numbers from the top panel's.
- Matt Mazur — "A Step by Step Backpropagation Example"
  (https://mattmazur.com/2015/03/17/a-step-by-step-backpropagation-example/) —
  the standard worked example whose initialized-vs-after-one-iteration weight
  comparison this slide generalizes to 10 iterations.
- Machine Learning Mastery — "Understand Dynamics of Learning Rate on Deep Learning
  Neural Networks" (https://machinelearningmastery.com/understand-the-dynamics-of-learning-rate-on-deep-learning-neural-networks/)
  — with η=5 the weights move a large amount per iteration, so iteration-10 weights
  are far from the initialization; explains why the two panels differ substantially.
- scikit-learn — `MLPClassifier` (https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html)
  — `coefs_` (one weight matrix per layer) and `intercepts_` are the standard place
  the same quantities live; confirms weight matrices are per-layer with separate biases.

## Corrections / notes

- **Do not trust the parse record for this slide's numbers.** The parse chart tables
  are garbled (categories like "O7" appearing twice, values duplicated, "T 0.77" with
  no matching label, several values out of any plausible weight range, and the bottom
  panel even reusing the top panel's activation labels). The isolated vision analysis
  is the better source: it gives clean equations `0.791 / 0`, `0.791 / 1`,
  `0.064 / 0`, `0.939 / 1` plus the panel titles. All on-frame weight labels and O
  values must come from the vision pass / original frame.
- **The 0.791 pair is verified:** σ⁻¹-consistency with slides 31/34 — the network's
  initial output weights produce O₆=O₇=0.791 there too, so the initialized state is
  continuous across the run. Slide 34's table starts from the same 0.791/0.791.
- The frame's η = 5 matches slides 31, 32 and 34 — one consistent run.
- **Correction for the spec, not the frame:** if any build treats the two panels as
  independent networks, that is wrong — they are the same network at two time points,
  sharing topology, node numbering, layer colors, and the target column.

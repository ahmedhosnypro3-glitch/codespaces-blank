# Slide 032 — Updated Weights After Iteration #1 (two weight scatter plots)

Frame topic: two scatter plots comparing the network's weight values — an
initial/before set and the set after one training iteration, annotated η=5.
Data taken from `analysis/parse/slide_032.parse.md` (the chart tables there are
the only transcript record for this slide).

## Sources

- Matplotlib — `Axes.scatter` reference
  (https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.scatter.html) —
  signature `scatter(x, y, s=None, c=None, marker=None, ...)`; `s` is marker AREA in
  points² (not radius), `c` maps values through a colormap. Governs how the plot is
  rebuilt so marker size/color encode weight magnitude the way the frame does.
- Machine Learning Mastery — "Understand Dynamics of Learning Rate on Deep Learning
  Neural Networks" (https://machinelearningmastery.com/understand-the-dynamics-of-learning-rate-on-deep-learning-neural-networks/)
  — confirms the framing of this slide family: weights after one iteration are the
  direct product of ΔW = η·δ·Oᵢ from the worked example (slide 31).
- Wikipedia — "Logistic function" (https://en.wikipedia.org/wiki/Logistic_function)
  — σ(z)=1/(1+e^(−z)); fixes the activation values that feed the ΔW numbers plotted.
- 365 Data Science — "What Is Backpropagation?"
  (https://365datascience.com/trending/backpropagation/) — confirms "updated weights
  after iteration #1" means all W (and Bias) updated once per training sample.

## Corrections / notes

- **Cross-slide consistency VERIFIED:** nine of the values in this frame's "after
  iteration" plot equal slide 31's computed new-weight set exactly — 0.125 (×3:
  Input, X₁, X₆), 0.215 (O₃), 0.305 (X₂), 0.115 (X₇), 0.625 (Bias), 0.105 (Output /
  Bias). That confirms slide 32 plots the result of slide 31's single update step and
  that both frames belong to one run. No correction.
- The remaining values (0.527, 0.458, 0.575, 0.134, 0.375, 0.565, and the single
  negative −0.218) do not appear in slide 31's new-W set. Most plausibly the second
  layer's weights (hidden→output, W₆₃…W₇₅, W₆b…W₇b), which slide 31 did not print;
  alternatively the parse may have mis-assigned category labels. **Unverified** — do
  not invent these labels; take them from the vision analysis / original frame.
- The parse record for this slide is chart-table only (no `_final.json` exists), so it
  is weaker evidence than usual. Treat all labels/positions as parse-derived and
  re-verify against `unique_slides/slide_032.jpg` in the vision pass.
- `η=5` on both panels matches slides 31/33/34 — consistent across the run.

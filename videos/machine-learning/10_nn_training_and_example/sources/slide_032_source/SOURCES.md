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
## Audit

Audited by lane S scope `b_src_2` (web-source audit), 2026-10-31. Method: independent Python
cross-check of the plotted values against slides 030/031's computed new-weight set, plus agy
web-search; cross-read against `analysis/parse/slide_032.parse.md` (no `_final.json` exists
for this slide — the parse's two chart tables are the only transcript record).

Questions asked:
1. Does the second panel ("Updated weights (after iteration # 1)") plot slide 31's
   post-update weight set?
2. What do the first panel's values correspond to?
3. Are matplotlib's `scatter` semantics (marker size `s` = area in points², `c` = colormap
   mapping) as described in the prior file?
4. Is there any independent way to verify the category LABELS (Input / O3 / Output / Target /
   X₁…X₇ / Bias) assigned to these values?

Answers:
- Q1 **CONFIRMED, and stronger than the prior note claimed.** All TEN of the second panel's
  values match slide 030/031's new-weight set exactly: 0.125 (W31), 0.305 (W51), 0.575 (W42),
  −0.218 (W64), 0.565 (W74), 0.125 (W3b), 0.115 (W4b), 0.625 (W52), 0.105 (W5b),
  0.375 (W7b). The prior note listed "nine of the values"; the actual count is ten of ten,
  with no unmatched entry.
- Q2 **PARTIALLY CONFIRMED / one value unexplained.** The first panel's values are
  0.125, 0.215, 0.527, 0.458, 0.575, 0.134, 0.625, 0.105. Six match the new-weight set
  exactly (0.125, 0.215, 0.458, 0.575, 0.625, 0.105). Two do not: **0.527** (slide 030/031
  gives W32 = 0.525 — a 0.002 difference, most plausibly a parse/OCR digit slip, but
  unproven) and **0.134** (slide 030/031 gives W65 = **−0.134** — the same value with the
  sign dropped). The prior file's "unverified" note on these two is upheld; the sign-drop on
  0.134 is the more likely explanation and is consistent with a chart that may plot |value|,
  but that is inference, not proof.
- Q3 **CONFIRMED**. Search confirms `s` is marker AREA in points squared (not radius), and
  `c` is a numeric sequence mapped through `cmap`/`norm`; a scalar or length-n sequence of
  numbers works, and `cmap` is only used when `c` is numeric.
- Q4 **NOT-VERIFIABLE.** No source, and no parse record, independently attests which weight
  each point represents. The labels are parse-derived only. Do not invent label↔value
  assignments.

Verdicts per claim:
- Second panel = slide 31's after-one-iteration weight set — **CONFIRMED** (10/10 values).
- First panel's six matching values — **CONFIRMED**.
- First panel's 0.527 — **CONFLICT** (slide 030/031 gives 0.525); most likely a parse digit
  slip, unproven.
- First panel's 0.134 — **CONFLICT** in sign with slide 030/031's −0.134; likely a dropped
  minus sign, unproven.
- Category labels for both panels — **NOT-VERIFIABLE**; take them from the vision pass /
  original frame.
- matplotlib `scatter` `s`/`c` semantics — **CONFIRMED**.
- η = 5 on both panels — **CONFIRMED** consistent with slides 27–31 and 33–34.
- PARSE COVERAGE: no `_final.json` exists for slide 032, so this slide has no certified
  analysis JSON — **NOT-VERIFIABLE** via the certified-spec route; the parse chart tables and
  the original frame are the only evidence.

New sources found during audit (real URLs, not previously cited):
- Codecademy, "Matplotlib: pyplot.scatter" —
  https://www.codecademy.com/resources/docs/matplotlib/pyplot/scatter
  Independent confirmation that `s` is area in points² and `c` is colormapped.
- SciPy, `scipy.special.expit` —
  https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.expit.html

Audit summary: the "after iteration # 1" panel is fully cross-verified against the run
(10/10 values). Two values in the other panel remain unexplained (±0.134 / 0.527), and all
category labels remain unverifiable — both flagged for the vision pass.

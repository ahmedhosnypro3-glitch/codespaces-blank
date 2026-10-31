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
## Audit

Audited by lane S scope `b_src_2` (web-source audit), 2026-10-31. Method: independent Python
recomputation of the panel outputs, plus agy web-search; cross-read against
`analysis/isolated_033/slide_033_raw.json` and `analysis/parse/slide_033.parse.md` (plus the
certified `analysis/slide_033_final.json`, title "Initialized weights").

Questions asked:
1. Is the top panel the network at initialization and the bottom panel the SAME network after
   10 training iterations (η = 5)?
2. Is the certified pair `0.791 / 0` and `0.791 / 1` (top) and `0.064 / 0` and `0.939 / 1`
   (bottom) consistent with the rest of the run?
3. Are the parse transcript's chart tables usable as data?
4. Does the run's error trend remain monotonically decreasing across slides 32 → 33 → 34?

Answers:
- Q1 **CONFIRMED** as the frame's semantics. Both panels share topology (Input x₁,x₂,Bias →
   Hidden 3,4,5 → Output 6,7 → Target t₆,t₇), node numbering, layer colours and the target
   column; only the weight labels and the O values differ. The certified JSON's own panel
   titles are "Initialized weights" and "Updated weights (after iteration # 10)".
- Q2 **CONFIRMED** as consistent. Top: O₆ = O₇ = 0.791 with targets 0/1 — exactly the initial
   outputs recomputed on slides 027/031, so the initialized state is continuous across the run.
   Bottom: O₆ = 0.064, O₇ = 0.939 against targets 0/1 — both outputs have moved toward their
   targets after 10 iterations. Recomputed error for the bottom panel: 0.064² + 0.061² =
   0.007817, which continues the decreasing trend (slide 034's iteration-5 row is 0.01517).
- Q3 **NO.** The parse tables are garbled: categories repeat ("O7" twice, "O5" three times),
   values duplicate, "T 0.77" has no matching label, several values (1.05, −1.2, −0.93) lie
   outside any plausible weight range, and the bottom panel reuses the top panel's activation
   labels. The isolated vision analysis is the better record.
- Q4 **CONFIRMED**: the error falls monotonically across the run — 0.669362 (initial) →
   0.151129 (it 1) → 0.038729 → 0.025186 → 0.018868 → 0.01517 (it 5) → 0.007817 (it 10).

Verdicts per claim:
- Two panels = same network at two time points — **CONFIRMED** (not two independent networks).
- Top panel outputs 0.791 / 0.791 — **CONFIRMED** (matches slides 027/031/034).
- Bottom panel outputs 0.064 / 0.939 — **CONFIRMED** as consistent with the targets and the
  decreasing-error trend.
- Panel titles "Initialized weights" / "Updated weights (after iteration # 10)" — **CONFIRMED**.
- η = 5 — **CONFIRMED** consistent with slides 31, 32 and 34.
- All on-frame weight labels — **NOT-VERIFIABLE** from the parse; take them from the vision
  pass / original frame, as the prior note already instructed.
- Parse chart tables — **CONFLICT** (garbled; do not build from them).

New sources found during audit (real URLs, not previously cited):
- SciPy, `scipy.special.expit` —
  https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.expit.html
  Confirms σ(z) = 1/(1+e^(−z)), the function behind every Oⱼ printed on this slide, and
  σ(1.3312) = 0.791 for the initialized state.
- Wikipedia, "Logistic function" — https://en.wikipedia.org/wiki/Logistic_function
- Math StackExchange, "Backpropagation hidden layer error" —
  https://math.stackexchange.com/questions/4686558/backpropagation-hidden-layer-error

Audit summary: the slide's semantics and its four O/target pairs are confirmed and consistent
with the whole run. The parse tables are unusable; the frame is the only source for the
weight labels.

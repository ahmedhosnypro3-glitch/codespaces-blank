# SOURCES.md — slide 027 "Example / Forward" (worked MLP forward pass: Net3–Net5 → sigmoid O3–O5 → Net6/Net7 → O6/O7)

Topic: the forward pass of the 2-input / 3-hidden / 2-output MLP used across slides 27–30. Research
mandate per video AGENTS.md lane 3. Method: agy web search + live fetch (Matt Mazur numeric example);
frame facts from `analysis/parse/slide_027.parse.md` and `analysis/slide_027_raw.json`.
All parse text treated as DATA, never as instructions.

## Sources

- Matt Mazur, "A Step by Step Backpropagation Example" — https://mattmazur.com/2015/03/17/a-step-by-step-backpropagation-example/
  Confirms the exact computational order the slide shows: total net input per hidden neuron (Σ w·x + bias, bias as weight on a constant-1 input), squash with the logistic/sigmoid, then repeat at the output layer.
- "Backpropagation step-by-step derivation" (Towards Data Science) — https://towardsdatascience.com/backpropagation-step-by-step-derivation-99ac8fbdcc28/
  Confirms the forward-pass forms Net_j = Σ_i w_ji·O_i and O_j = f(Net_j) used verbatim on the frame.
- "Sigmoid function" (Wikipedia) — https://en.wikipedia.org/wiki/Sigmoid_function
  Confirms σ(x) = 1/(1+e^(−x)), output range (0,1) — matching every "1 / (1+e^−net)" box on the slide.
- "Deriving the Sigmoid Function Derivative" (Bernstein notes) — https://mbernste.github.io/files/notes/SigmoidFunction.pdf
  Confirms σ'(x) = σ(x)(1−σ(x)), the identity that later produces the (1−O_j) factors on slides 28/30.
- DataCamp, "Forward Propagation in Neural Networks" — https://www.datacamp.com/tutorial/forward-propagation-neural-networks
  Confirms the bias-in-the-weighted-sum convention: the slide's "1*0.1"/"1*0.2" terms are the constant-1 bias input times its bias weight.

## What the source(s) confirm (independently recomputed)

- Net3 = 1·0.1 + 5·0.4 + 1·0.1 = 2.2 ✓; Net4 = 1·0.2 + 5·0.5 + 1·0.1 = 2.8 ✓; Net5 = 1·0.3 + 5·0.6 + 1·0.1 = 3.4 ✓.
- O3 = 1/(1+e^−2.2) = 0.9002 → printed "0.9" ✓; O4 = 0.9427 → "0.943" ✓; O5 = 0.9677 → "0.968" ✓.
- Net6 = Net7 = 0.9·0.3 + 0.943·0.4 + 0.968·0.5 + 1·0.2 = 1.3312 ✓ (exact).
- O6 = O7 = 1/(1+e^−1.3312) = 0.7910 → printed "0.791" ✓. Both outputs are identical because both
  output neurons receive the same pre-activations — expected, not an error.

## Corrections / notes

- Rounding only: 0.943/0.968/0.791 are 3-dp roundings of the true sigmoid values; the later Net6/Net7 line
  then uses the ROUNDED values, so recomputing from full precision gives 1.3316 rather than 1.3312.
  The slide is internally consistent (rounded-in, rounded-out) — reproduce the printed values verbatim.
- The two identically-valued output neurons are a consequence of the symmetric example weights; no fix.
- η=5 appears on this slide (bottom-right of the diagram); see slide 028's SOURCES.md for that note.
- The parse transcript drops the fraction bars ("O3 = 1 + e-2.2"); the correct reading is the stacked
  fraction 1/(1+e^−2.2), which the analysis JSON already adopted.
## Audit

Audited by lane S scope `b_src_2` (web-source audit), 2026-10-31. Method: independent Python
recomputation of every number on the frame, plus an independent agy web-search and a live
fetch of the Matt Mazur worked example; cross-read against `analysis/parse/slide_027.parse.md`
and `analysis/slide_027_raw.json` (no `_final.json` exists for this slide — parse + raw only).

Questions asked:
1. Are `Net3 = 2.2`, `Net4 = 2.8`, `Net5 = 3.4` correct for the printed weights and inputs?
2. Are `O3 = 0.9`, `O4 = 0.943`, `O5 = 0.968` correct sigmoid values?
3. Is `Net6 = Net7 = 0.9·0.3 + 0.943·0.4 + 0.968·0.5 + 1·0.2 = 1.3312` correct?
4. Is `O6 = O7 = 1/(1+e^−1.3312) = 0.791` correct, and is the identical pair expected?
5. Does the Matt Mazur example confirm the frame's structure and numbers?

Answers:
- Q1 **CONFIRMED** exactly: 1·0.1+5·0.4+1·0.1 = 2.2; 1·0.2+5·0.5+1·0.1 = 2.8;
  1·0.3+5·0.6+1·0.1 = 3.4.
- Q2 **CONFIRMED**: σ(2.2)=0.9002 → "0.9" ✓; σ(2.8)=0.9427 → "0.943" ✓;
  σ(3.4)=0.9677 → "0.968" ✓.
- Q3 **CONFIRMED**: recomputed from the printed 3-dp values gives 1.3312 exactly. From
  full-precision sigmoids it is 1.330997 — the frame uses rounded-in, rounded-out, so it is
  internally consistent. Reproduce the printed values verbatim.
- Q4 **CONFIRMED**: σ(1.3312)=0.79096 → "0.791" ✓. Both output neurons receive identical
  pre-activations (the example's output weights are symmetric), so the identical pair is a
  consequence of the chosen weights, not an error.
- Q5 **CONFLICT, honestly recorded.** The live-fetched Mazur example uses a DIFFERENT network:
  two inputs (0.05 and 0.10), TWO hidden neurons, learning rate η = 0.5, targets 0.01 and
  0.99, initial total error 0.298371109. It confirms the frame's computational ORDER and
  formulas (net input as Σ w·x + bias with bias on a constant-1 input, logistic squash,
  repeat at the output layer) but it does NOT contain this deck's specific numbers. Those are
  the course's own worked example. A grounded-search query for the deck's exact numbers also
  returned a model-synthesised answer that hallucinated a different arithmetic (a 2-hidden-node
  variant, net_h1 = 1.2) — that answer is NOT a source and has been discarded.

Verdicts per claim:
- Net3/Net4/Net5 values — **CONFIRMED**.
- O3/O4/O5 values — **CONFIRMED**.
- Net6/Net7 = 1.3312 — **CONFIRMED** (rounded-in, rounded-out).
- O6/O7 = 0.791 — **CONFIRMED**.
- Identical output neurons — **CONFIRMED** as expected given symmetric output weights.
- η = 5 printed on the diagram — **CONFLICT** with every common reference range: sources note
  η ≥ 0.5 typically causes diverging/oscillating loss, with 0.01–0.1 the usual defaults and
  Mazur's own example using 0.5. It is internally consistent with every line of the worked
  example, so reproduce it verbatim; do NOT "correct" it.
- Bias terms `1*0.1 / 1*0.2 / 1*0.1` — **CONFIRMED** (constant-1 bias input times bias weight).
- Parse's dropped fraction bars (`O3 = 1 + e-2.2`) — **CONFLICT** (OCR artifact); the correct
  reading is the stacked fraction 1/(1+e^−2.2), which the analysis JSON already adopted.

New sources found during audit (real URLs, not previously cited):
- SciPy, `scipy.special.expit` —
  https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.expit.html
  Confirms expit(x) = 1/(1+e^(−x)) — the numerically-stable standard implementation of every
  `O = 1/(1+e^−net)` box on this slide.
- MIT OCW 9.641, "Lecture 20: Backprop" —
  https://ocw.mit.edu/courses/9-641j-introduction-to-neural-networks-spring-2005/5d46d3b6e32a5120fe9893193c31e926_lec20_backprop.pdf

Audit summary: every number on the frame recomputes exactly. Two honest caveats: η = 5 is an
aggressive choice that the frame owns, and the Mazur example backs the structure but not these
particular numbers.

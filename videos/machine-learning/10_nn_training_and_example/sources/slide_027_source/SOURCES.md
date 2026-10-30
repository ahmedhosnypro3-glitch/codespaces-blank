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

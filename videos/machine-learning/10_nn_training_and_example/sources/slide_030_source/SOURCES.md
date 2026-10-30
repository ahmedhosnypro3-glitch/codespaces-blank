# SOURCES.md — slide 030 "Backward (Update hidden Layer Weights)" (general delta rule for hidden units + numeric updates)

Topic: the hidden-layer backward pass of the worked example — the general delta rule
δ_j = O_j(1−O_j)·Σ_k(δ_k·w_kj), Δw_ji = η·O_i·O_j(1−O_j)·Σ_k(δ_k·w_kj) = η·O_i·δ_j, and the
numeric hidden-unit deltas and updated input→hidden weights.
Method: agy web search + live fetch (Matt Mazur numeric example); frame facts from
`analysis/parse/slide_030.parse.md`. Parse text is DATA only.

## Sources

- Matt Mazur, "A Step by Step Backpropagation Example" — https://mattmazur.com/2015/03/17/a-step-by-step-backpropagation-example/
  Live-fetched. Confirms δ_j(n) = O_j(1−O_j)·Σ_k(δ_k(n)·w_kj) for hidden units and the weight update
  Δw_ji = η·δ_j·O_i — i.e. exactly the frame's two boxed formulas.
- "Backpropagation step-by-step derivation" (Towards Data Science) — https://towardsdatascience.com/backpropagation-step-by-step-derivation-99ac8fbdcc28/
  Gives the full chain-rule derivation of δ_j = O_j(1−O_j)·Σ_k(δ_k·w_kj) for a non-output unit.
- "Derivation of delta for hidden units" (Cross Validated) — https://stats.stackexchange.com/questions/157127/the-derivation-of-delta-j-frac-partial-e-n-partial-a-j-errors-for-hid
  Confirms the Σ_k δ_k·w_kj term: a hidden unit's error is the backpropagated sum of the next layer's deltas weighted by the connecting weights.
- Swarthmore CS81, "BackPropDeriv" — https://www.cs.swarthmore.edu/~meeden/cs81/s10/BackPropDeriv.pdf
  Confirms the same generalised delta rule and the bias-weight treatment (constant-1 input, O_i = 1).

## What the source(s) confirm (independently recomputed)

- δ3 = 0.9·(1−0.9)·[−0.131·(−0.29) + 0.035·0.458] = 0.00486 → printed "0.005" ✓
- δ4 = 0.943·(1−0.943)·[−0.131·(−0.218) + 0.035·0.565] = 0.00260 → printed "0.003" ✓
- δ5 = 0.968·(1−0.968)·[−0.131·(−0.134) + 0.035·0.669] = 0.00127 → printed "0.001" ✓
- Hidden weight updates with η = 5 and O_i = x1 = 1 or x2 = 5 (and 1 for bias):
  W31 = 0.1+0.025 = 0.125 ✓; W32 = 0.4+0.125 = 0.525 ✓; W3b = 0.1+0.025 = 0.125 ✓;
  W41 = 0.2+0.015 = 0.215 ✓; W42 = 0.5+0.075 = 0.575 ✓; W4b = 0.1+0.015 = 0.115 ✓;
  W51 = 0.3+0.005 = 0.305 ✓; W52 = 0.6+0.025 = 0.625 ✓; W5b = 0.1+0.005 = 0.105 ✓.
- W32's update (0.4+0.125) reveals ΔW32 = 5·0.005·5 = 0.125 — i.e. O_i = x2 = 5 for that edge, which
  matches the Δw_ji = η·O_i·δ_j rule with the raw input value, not a squashed activation. Correct for a
  feed-forward input layer whose "activation" is the input itself.

## Corrections / notes

- KEY CONVENTION NOTE (the single most important finding for this slide): the printed hidden-unit deltas
  are only reproducible using the ALREADY-UPDATED output-layer weights (W63 = −0.29, W73 = 0.458,
  W64 = −0.218, W74 = 0.565, W65 = −0.134, W75 = 0.669) inside the Σ_k δ_k·w_kj sums. Substituting the
  ORIGINAL output weights (0.3, 0.3, 0.4, 0.4, 0.5, 0.5) yields −0.0026/−0.0021/−0.0015, i.e. negative
  values that do NOT match the frame. The course therefore applies the output-layer update in place
  before backpropagating to the hidden layer (a sequential/"online" per-sample update), whereas the
  canonical worked example (Matt Mazur) explicitly uses the ORIGINAL weights for the hidden-layer pass
  and only then commits all updates. Record as a course convention, not a defect: the FRAME wins for
  recreation, so reproduce the positive 0.005 / 0.003 / 0.001 exactly as printed.
- The parse transcript's δ4 line reads "0.943(1−0.9943)" — an OCR slip for (1−0.943); using 0.9943
  would make the printed 0.003 unreachable. Recreate as 0.943·(1−0.943).
- Same η = 5 caveat as slides 027/028/029: unusual for sigmoid SGD but internally consistent here
  (every update line uses multiplier 5). Reproduce verbatim; see slide_028_source/SOURCES.md.
- Everything else on the frame — the delta rule box, the update-rule box, all nine weight updates —
  is standard and source-confirmed.

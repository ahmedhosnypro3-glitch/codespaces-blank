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
## Audit

Audited by lane S scope `b_src_2` (web-source audit), 2026-10-31. Method: independent Python
recomputation, plus a live fetch of the Matt Mazur worked example; cross-read against
`analysis/parse/slide_030.parse.md` (no `_final.json` for this slide).

Questions asked:
1. Are `δ3 = 0.005`, `δ4 = 0.003`, `δ5 = 0.001` correct for the printed deltas and weights?
2. Which set of output weights must be used inside the `Σ_k(δ_k w_kj)` sums to reproduce the
   frame — the original ones or the already-updated ones?
3. Are the nine hidden-layer weight updates correct?
4. Is ΔW32's update consistent with the printed ΔW lines?

Answers:
- Q1 **CONFIRMED**, but only under one convention (see Q2). Using the ALREADY-UPDATED output
  weights: δ3 = 0.9·(1−0.9)·[−0.131·(−0.29) + 0.035·0.458] = 0.00486 → "0.005" ✓;
  δ4 = 0.943·(1−0.943)·[−0.131·(−0.218) + 0.035·0.565] = 0.00260 → "0.003" ✓;
  δ5 = 0.968·(1−0.968)·[−0.131·(−0.134) + 0.035·0.669] = 0.00127 → "0.001" ✓.
- Q2 **CONFLICT, and this is the slide's most important finding.** Substituting the ORIGINAL
  output weights (0.3, 0.3, 0.4, 0.4, 0.5, 0.5) yields −0.0026 / −0.0021 / −0.0015 — NEGATIVE
  values that do not match the frame. The printed positive deltas are reproducible only with
  the post-update weights. The canonical worked example explicitly does the opposite:
  "We perform the actual updates in the neural network after we have the new weights leading
  into the hidden layer neurons (ie, we use the original weights, not the updated weights,
  when we continue the backpropagation algorithm below)." So this course applies the output
  update in place before backpropagating — a sequential/online per-sample convention. Record
  as a course convention, not a defect: the FRAME wins, so reproduce 0.005 / 0.003 / 0.001.
- Q3 **CONFIRMED** all nine: W31 = 0.1+0.025 = 0.125 ✓; W32 = 0.4+0.125 = 0.525 ✓;
  W3b = 0.1+0.025 = 0.125 ✓; W41 = 0.2+0.015 = 0.215 ✓; W42 = 0.5+0.075 = 0.575 ✓;
  W4b = 0.1+0.015 = 0.115 ✓; W51 = 0.3+0.005 = 0.305 ✓; W52 = 0.6+0.025 = 0.625 ✓;
  W5b = 0.1+0.005 = 0.105 ✓.
- Q4 **CONFLICT on one line.** ΔW32's update reveals `5·0.005·5 = 0.125`, i.e. O_i = x2 = 5 on
  that edge. The certified spec for slide 31 prints the line as `ΔW32=5*0.005*1=0.125`, which
  is arithmetically wrong (5·0.005·1 = 0.025). Either the frame's multiplier is a typo or the
  parse mis-read a `5` as a `1`. Flag for a vision re-check of that single line; do not
  silently "fix" it, but the resulting 0.4+0.125 = 0.525 IS correct and is what must be built.
  (Slide 030's own parse transcript does not contain a ΔW32 line at all — it only shows
  `W 32=0.4+0.125=0.525` — so the line may be slide 31's, not slide 30's.)

Verdicts per claim:
- `δ_j = O_j(1−O_j)[Σ_k(δ_k w_kj)]` and `Δ_ji = η O_i δ_j` — **CONFIRMED**.
- δ3/δ4/δ5 = 0.005/0.003/0.001 — **CONFIRMED** under the course's sequential update.
- Use of already-updated output weights in the sums — **CONFLICT** with the canonical worked
  example (which uses original weights); record as course convention.
- Nine hidden weight updates — **CONFIRMED**.
- `ΔW32=5*0.005*1=0.125` — **CONFLICT** (internal arithmetic error; see above).
- Parse's `δ4=0.943(1−0.9943)` — **CONFLICT** (OCR slip for (1−0.943); 0.9943 cannot yield 0.003).
- η = 5 on every update line — **CONFIRMED** internally consistent (but an aggressive value;
  see slides 027/028).

New sources found during audit (real URLs, not previously cited):
- MIT OCW 9.641, "Lecture 20: Backprop" —
  https://ocw.mit.edu/courses/9-641j-introduction-to-neural-networks-spring-2005/5d46d3b6e32a5120fe9893193c31e926_lec20_backprop.pdf
- Math StackExchange, "Backpropagation hidden layer error" —
  https://math.stackexchange.com/questions/4686558/backpropagation-hidden-layer-error

Audit summary: all formulas and all nine weight updates are standard and recompute exactly.
Two findings: the sequential-update convention (course-specific, canonically divergent), and
one arithmetically impossible ΔW32 line needing a vision re-check.

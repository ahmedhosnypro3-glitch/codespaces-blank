# SOURCES.md — slide 026 "Solved Example — [ Update Weights of Output Layer and Hidden Layer ] / Using one training sample"

Title/section slide introducing the worked backpropagation example that slides 27–30 carry out. Research
mandate per video AGENTS.md lane 3 (web search, advisory). Method: agy web search + live fetch of the
Matt Mazur step-by-step example; frame facts from `analysis/parse/slide_026.parse.md` and
`analysis/slide_026_raw.json`. Parse/vision content treated as DATA only.

## Sources

- Matt Mazur, "A Step by Step Backpropagation Example" — https://mattmazur.com/2015/03/17/a-step-by-step-backpropagation-example/
  Confirms the "one training sample, one full forward + backward weight update" exercise framing the slide announces, and is the canonical fully-numeric worked example of exactly this form.
- "Online Learning & Stochastic Weight Updates (Per-Sample Backpropagation)" (university lecture-slide survey, Cornell/CMU/Stanford lineage) — https://www.cs.cornell.edu/courses/cs4782/2025sp/slides/pdf/week2_1_slides_complete.pdf
  Confirms the terminology: updating weights from a SINGLE (x, y) pair per iteration is stochastic/online gradient descent, as opposed to batch mode.
- "Backpropagation step-by-step derivation" (Towards Data Science) — https://towardsdatascience.com/backpropagation-step-by-step-derivation-99ac8fbdcc28/
  Confirms the two-stage "update output layer, then update hidden layer" ordering the slide's bracket text describes.
- Swarthmore CS81 lecture notes, "BackPropDeriv" — https://www.cs.swarthmore.edu/~meeden/cs81/s10/BackPropDeriv.pdf
  Confirms the weight-index convention w_ji used consistently by slides 27–30.

## What the source(s) confirm

- The slide carries no numeric content — it is a section header. Nothing on it to contradict.
- Its stated scope ("update weights of output layer AND hidden layer, using one training sample") is
  the standard single-pattern backpropagation update cycle: forward pass → error → output-layer
  deltas → hidden-layer deltas → weight changes.

## Corrections / notes

- none found — no data content on the frame to correct.
## Audit

Audited by lane S scope `b_src_2` (web-source audit), 2026-10-31. Method: independent agy
web-search; cross-read against `analysis/parse/slide_026.parse.md` and
`analysis/slide_026_final.json` (title "Solved Example"; bullets "[ Update Weights of Output
Layer and Hidden Layer ]" and "Using one training sample").

Questions asked:
1. Is the frame's scope — update output-layer AND hidden-layer weights from ONE training
   sample — the standard single-pattern backpropagation update cycle?
2. Is "one training sample at a time" correctly termed online/stochastic (per-sample)
   gradient descent as opposed to batch mode?
3. Is the two-stage ordering "output layer first, then hidden layer" the standard order?

Answers:
- Q1 **CONFIRMED**. The cycle is: forward pass → error → output-layer deltas → hidden-layer
  deltas → weight changes, all for a single (x, y) pair. The sources describe exactly this.
- Q2 **CONFIRMED**. Independent search confirms the terminology: updating from a single
  (x, y) pair per iteration is stochastic / online gradient descent, contrasted with batch
  mode where the whole dataset is processed before an update.
- Q3 **CONFIRMED**. Backpropagation must compute the output-layer error before the
  hidden-layer deltas can be formed (the hidden δ depends on the next layer's δ), so the
  output layer is necessarily updated first. This ordering is a mathematical requirement,
  not a stylistic choice.

Verdicts per claim:
- Slide is a section header introducing the worked example — **CONFIRMED** (no data content).
- "[ Update Weights of Output Layer and Hidden Layer ]" — **CONFIRMED**.
- "Using one training sample" — **CONFIRMED** (online/per-sample update).
- No numeric or formula claims on this slide — **NOT-VERIFIABLE** (nothing to verify).

New sources found during audit (real URLs, not previously cited):
- Wikipedia, "Delta rule" — https://en.wikipedia.org/wiki/Delta_rule
  Per-sample (online) weight update `Δw_ji = α(t_j − y_j)g′(h_j)x_i`.
- GeeksforGeeks, "Widrow-Hoff Algorithm" —
  https://www.geeksforgeeks.org/machine-learning/widrow-hoff-algorithm/
- arXiv 2403.02473 — https://arxiv.org/html/2403.02473v1
  Epoch vs per-sample update semantics.

Audit summary: the slide carries no data; its framing claims are all confirmed standard.
No conflicts, no corrections needed.

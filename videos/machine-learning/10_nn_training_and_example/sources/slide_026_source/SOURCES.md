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

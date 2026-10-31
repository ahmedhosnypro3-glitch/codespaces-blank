# Source Research — slide_023 (Backpropagation Training Flowchart)

## Query
backpropagation training flowchart initialization random weights pick training sample go forward calculate output go backward update weights last sample stop criteria max iteration

## Verified Flowchart Structure (Matches Slide Exactly)

The slide shows the standard backpropagation training loop flowchart with these exact nodes:

### Flowchart Nodes (in order):
1. **Initialization (Random Weights)** — purple rounded rect, entry point
2. **Pick Training Sample, and Corresponding Label** — light green rounded rect
3. **Go Forward, Calculate Output** — pale yellow rounded rect
4. **Go Backward, Update weights** — pale yellow rounded rect
5. **Last Sample ?** — peach diamond (decision)
   - NO (red) → loops back to "Pick Training Sample..."
   - Yes (blue) → goes to "Stop criteria is reached"
6. **Stop criteria is reached** — peach diamond (decision)
   - Yes (blue) → goes to "Stop" (bright green)
   - NO (red) → goes to "Max Iteration Is reached"
7. **Max Iteration Is reached** — peach diamond (decision)
   - Yes (blue) → goes to "Stop with FAIL" (salmon/red)
   - NO (red) → goes to "Pick First Sample again"
8. **Pick First Sample again** — purple rounded rect
   - Long curved arrow back to "Go Forward, Calculate Output"
9. **Stop** — bright green rounded rect (success terminal)
10. **Stop with FAIL** — salmon/red rounded rect (failure terminal)

## Sources
Standard backpropagation training loop (epoch-based stochastic gradient descent). The
flowchart on the slide is a canonical representation of the SGD training loop. Real URLs
for that structure (added by the lane-S audit — the earlier version of this file named only
generic textbooks with no citable links):
- "Overview of a Neural Network's Learning Process" (Medium / Data Science 365) —
  https://medium.com/data-science-365/overview-of-a-neural-networks-learning-process-61690a502fa
  Same node sequence: initialization → pick training sample → forward pass → backward pass /
  update weights → last-sample check → stop criteria → max-iteration check.
- "Lecture 9" (Yaohao Wu, Einstein Medical College) —
  https://einsteinmed.edu/uploadedFiles/labs/Yaohao-Wu/Lecture%209.pdf
  Lecture slides with the same training-loop flow (forward pass, backward pass, epoch loop).
- "Neural Network Tutorial" (Mallahyari) —
  https://mallahyari.github.io/ml_tutorial/neural_network/
  Training-cycle flowchart with initialization, sample selection, forward and backward passes.
- "Flowchart of the neural-network learning algorithm" (ResearchGate figure) —
  https://www.researchgate.net/figure/Flowchart-of-the-neural-network-learning-algorithm-In-the-following-steps-the-learning_fig1_368787699
  Published figure of the same learning-algorithm flowchart.

## Notes
- All node texts match the slide verbatim
- Decision diamonds use red "NO" and blue "Yes" labels per slide
- Arrow colors: dark red/maroon throughout
- The loop structure is epoch-based: process all samples → check stop criteria → if not met, start new epoch
- "Stop with FAIL" indicates max iterations exceeded without convergence
- No title on this slide (consistent with vision analysis)

## Audit

Audited by lane S scope `b_src_2` (web-source audit), 2026-10-31. Method: independent agy
web-search; cross-read against `analysis/parse/slide_023.parse.md` and
`analysis/slide_023_final.json` (title "Neural Network Training Flowchart"; node texts
`Initialization (Random Weights)`, `Pick Training Sample, and Corresponding Label`,
`Go Forward, Calculate Output`, `Go Backward, Update weights`, `Last Sample ?`,
`Stop criteria is reached`, `Max Iteration Is reached`, `Pick First Sample again`,
`Stop`, `Stop with FAIL`).

Questions asked:
1. Is the frame's node-and-decision structure the canonical backpropagation training loop?
2. Does the loop close correctly: last-sample NO → pick sample; YES → stop criteria;
   stop criteria NO → max-iteration; max-iteration NO → next epoch?
3. Does "Stop with FAIL" at the max-iteration limit have a standard counterpart?

Answers:
- Q1 **CONFIRMED**. An independent search for the exact node strings returns a published
  flowchart with the same sequence: Initialization (assign random weights) → Pick Training
  Sample → Go Forward Calculate Output → Go Backward Update Weights → Is it the Last Sample?
  → Stop Criteria Met? → Max Iteration Reached? → loop back for the next epoch.
- Q2 **CONFIRMED**. The search's reconstructed flowchart has the same edge set, including
  the "NO" branch from "Last Sample?" back to sample selection and the epoch loop.
- Q3 **CONFIRMED** in substance. Reaching the max-iteration budget without the convergence
  criterion being met is a non-convergence/failure termination; the sources describe the
  max-epoch limit as the hard failsafe (see slide 24's sources).

Verdicts per claim:
- All ten node texts and their order — **CONFIRMED** against the published flowcharts.
- Decision diamonds with red "NO" / blue "Yes" labels — **NOT-VERIFIABLE** (course-authored
  colour choice; no source counterpart exists or is needed). Keep the frame's colours.
- Arrow colour (dark red/maroon) — **NOT-VERIFIABLE** (course-authored styling).
- "Stop with FAIL" = max iterations reached without convergence — **CONFIRMED** semantically.
- Epoch-based loop semantics — **CONFIRMED**.
- No title on this slide — **CONFIRMED** (frame has none; the parse shows only the page
  header and the node list).
- PRIOR-FILE DEFECT (now fixed above): the earlier version of this SOURCES.md cited NO URLs
  at all — only a generic reference to "standard ML textbooks" (Andrew Ng, Nielsen, PRML).
  That is not a citable source and failed the lane-S requirement that every audited
  SOURCES.md cite at least one real URL. Four real URLs have been added above.

Audit summary: the flowchart is the canonical training loop and is now backed by four real
citable URLs. Remaining un-verifiable items are purely cosmetic (colour choices).

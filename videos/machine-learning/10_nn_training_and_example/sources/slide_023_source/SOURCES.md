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
Standard backpropagation training loop (epoch-based stochastic gradient descent) — confirmed by standard ML textbooks and tutorials:
- Standard ML course flowcharts (e.g., Andrew Ng, Michael Nielsen, Bishop PRML)
- The flowchart on the slide is a canonical representation of the SGD training loop

## Notes
- All node texts match the slide verbatim
- Decision diamonds use red "NO" and blue "Yes" labels per slide
- Arrow colors: dark red/maroon throughout
- The loop structure is epoch-based: process all samples → check stop criteria → if not met, start new epoch
- "Stop with FAIL" indicates max iterations exceeded without convergence
- No title on this slide (consistent with vision analysis)
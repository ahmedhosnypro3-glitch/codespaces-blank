# Slide 034 — Forward Calculations (network diagram + error-vs-iteration table)

Frame topic: the same 2-3-2 network (inputs x₁=1, x₂=5; hidden nodes 3/4/5 with
O₃/O₄/O₅; outputs 6/7 with O₆/O₇; targets t₆=0, t₇=1; Bias; η=5) plus a table with
columns O₆ | O₇ | Squared Error over rows "Initial Weights, Iteration 1–5, …, Target".
Data taken from `analysis/slide_034_final.json` + `analysis/parse/slide_034.parse.md`.

## Sources

- Matt Mazur — "A Step by Step Backpropagation Example"
  (https://mattmazur.com/2015/03/17/a-step-by-step-backpropagation-example/) —
  canonical worked example using E = ½(t−O)² per output and the O₆/O₇ + squared-error
  layout this slide tabsulates.
- 365 Data Science — "What Is Backpropagation?"
  (https://365datascience.com/trending/backpropagation/) — confirms E = ½Σ(tₖ−Oₖ)²
  (or Σ(tₖ−Oₖ)² depending on convention) as the summed squared error over outputs.
- University of Illinois CS447 — "Lecture 20" (https://courses.grainger.illinois.edu/cs447/fa2018/Slides/Lecture20.pdf)
  — lecture slide source giving the same σ(z)=1/(1+e^(−z)), δₖ=(Oₖ−tₖ)·Oₖ(1−Oₖ) and
  E = ½Σ(tₖ−Oₖ)²; the closest published match to this frame's notation (Oⱼ, tₖ, Bias).
- MRCET — "Neural Networks" digital notes (https://www.mrcet.com/downloads/digital_notes/CSE/III%20Year/AIML/Neural-Networks.pdf)
  — confirms the forward pass netⱼ = Σ(wⱼᵢ·Oᵢ) + bⱼ and the target-column/error-table
  presentation of a training run.
- Wikipedia — "Logistic function" (https://en.wikipedia.org/wiki/Logistic_function)
  — σ(z)=1/(1+e^(−z)); σ(1.3312)=0.791, matching the frame's initial O₆ and O₇.

## Corrections / notes

- **"Squared Error" column lacks the ½ factor — CONFIRMED by recomputation.** Every row
  matches E = Σₖ(tₖ−Oₖ)² exactly, not E = ½Σₖ(tₖ−Oₖ)²:
  Initial 0.791²+0.209² = 0.669362 (slide says 0.669362; the ½-form would be 0.334681).
  Iteration 1: 0.352²+0.165² = 0.151129 (½-form 0.075565). Iterations 2–5 reproduce
  0.038729 / 0.025186 / 0.018868 / 0.01517 with the same Σ(t−O)² rule. All six rows
  verified to 1e-5. **The recreation must render the frame's numbers verbatim** — this
  is a note about the frame's convention (squared error summed without ½), not a defect
  to "fix"; flagging it so the error-trend plot is computed the same way if regenerated.
- **Sign convention:** sources (Illinois) write δₖ = (Oₖ−tₖ)·Oₖ(1−Oₖ); this frame's
  sibling slide 31 uses δₖ = Oₖ(1−Oₖ)(tₖ−Oₖ) with a `+` update. Same math, opposite
  signs — the frame's convention wins, matching slide 31.
- **Convergence trend CORRECT:** error falls monotonically 0.669362 → 0.01517 across
  iterations 1–5 and the outputs move monotonically toward the targets (O₆: 0.791→0.091
  toward t₆=0; O₇: 0.791→0.917 toward t₇=1). The large red down-arrow on the table's
  right edge is consistent with a decreasing-error reading.
- The final "Target" row (0, 1) matches t₆=0, t₇=1 in the diagram — consistent.
- η=5 is unusually large; the frame's own run still converges over these 5 iterations,
  so no contradiction to flag — but a rebuild must not silently substitute a smaller η.
## Audit

Audited by lane S scope `b_src_2` (web-source audit), 2026-10-31. Method: independent Python
recomputation of all six table rows, plus agy web-search; cross-read against
`analysis/parse/slide_034.parse.md` and `analysis/slide_034_final.json` (title "Forward
Calculations"; table columns O₆ | O₇ | Squared Error over rows Initial Weights, Iteration 1–5,
Target).

Questions asked:
1. Does every row of the "Squared Error" column match a specific, identifiable formula?
2. Which cost convention is it — `E = Σₖ(tₖ−Oₖ)²` or `E = ½Σₖ(tₖ−Oₖ)²`?
3. Does the error fall monotonically, and do the outputs move toward the targets?
4. Is the δ sign convention on this slide consistent?
5. Does the "Target" row match the diagram's target column?

Answers:
- Q1 + Q2 **CONFIRMED — and this is the slide's key finding.** Every row matches
  `E = Σₖ(tₖ−Oₖ)²` (no ½) to full precision:
  Initial 0.791² + 0.209² = 0.669362 ✓ (the ½-form would be 0.334681);
  Iteration 1: 0.352² + 0.165² = 0.151129 ✓ (½-form 0.075565);
  Iteration 2: 0.038729 ✓; Iteration 3: 0.025186 ✓; Iteration 4: 0.018868 ✓;
  Iteration 5: 0.01517 ✓. All six rows verified to better than 1e-5. The prior note's
  finding is upheld: the frame's "Squared Error" column is the UN-halved sum of squares.
  This is a convention difference, not a defect — but any rebuilt error plot must use the
  same Σ(t−O)² rule.
- Q3 **CONFIRMED**: error falls monotonically 0.669362 → 0.01517, and the outputs move
  toward their targets (O₆: 0.791 → 0.091 toward t₆ = 0; O₇: 0.791 → 0.917 toward t₇ = 1).
  The red down-arrow on the table's right edge is consistent with a decreasing-error reading.
- Q4 **CONFIRMED** as consistent with slide 31 (δₖ = Oₖ(1−Oₖ)(tₖ−Oₖ) with a `+` update);
  sources using the opposite sign are algebraically the same rule. Conference note only.
- Q5 **CONFIRMED**: the Target row (0, 1) matches t₆ = 0, t₇ = 1 in the diagram.

Verdicts per claim:
- All six O₆/O₇/Squared-Error rows — **CONFIRMED** (recomputed to <1e-5).
- Error column = `Σₖ(tₖ−Oₖ)²` WITHOUT the ½ factor — **CONFIRMED** (frame's convention;
  render verbatim, do not "fix" it).
- Monotonic convergence trend — **CONFIRMED**.
- Target row (0, 1) — **CONFIRMED**.
- η = 5 — **CONFIRMED** consistent across the run; **CONFLICT** with typical learning-rate
  practice but internally consistent. A rebuild must not substitute a smaller η.
- Signed δ convention — **CONFIRMED** (convention difference only).
- Network topology x₁=1, x₂=5, hidden 3/4/5, outputs 6/7, Bias — **CONFIRMED** consistent
  with slides 27–31.
- Chart x-axis tick values for the error trend, if an error-vs-iteration plot is regenerated
  from the table — **NOT-VERIFIABLE** as axis data; the table rows are the data, the axes are
  the builder's choice.

New sources found during audit (real URLs, not previously cited):
- MIT OCW 9.641, "Lecture 20: Backprop" —
  https://ocw.mit.edu/courses/9-641j-introduction-to-neural-networks-spring-2005/5d46d3b6e32a5120fe9893193c31e926_lec20_backprop.pdf
  Uses `E = ½Σ(tₖ−Oₖ)²` and δₖ = (Oₖ−tₖ)·Oₖ(1−Oₖ) — the closest published match to this
  frame's notation, and the source of the ½-form the frame omits.
- SciPy, `scipy.special.expit` —
  https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.expit.html
  σ(1.3312) = 0.791, matching the frame's initial O₆/O₇.
- Wikipedia, "Logistic function" — https://en.wikipedia.org/wiki/Logistic_function
- Math StackExchange, "Backpropagation hidden layer error" —
  https://math.stackexchange.com/questions/4686558/backpropagation-hidden-layer-error

Audit summary: the most numerically dense slide in the deck, and every row recomputes exactly.
The one finding worth carrying into the build is the un-halved squared-error convention.

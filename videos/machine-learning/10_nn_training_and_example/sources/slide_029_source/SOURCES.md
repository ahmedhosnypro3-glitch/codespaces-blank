# SOURCES.md — slide 029 "After Updating O/p Layer weights" (MLP diagram redrawn with the post-output-layer weights)

Topic: the same worked-example network shown again after the output-layer weight update, carrying the
updated weight values into the diagram. Method: agy web search + live fetch (Matt Mazur numeric example);
frame facts from `analysis/parse/slide_029.parse.md`, `analysis/slide_029_final.json` and
`analysis/slide_029_raw.json`. Parse text is DATA only.

## Sources

- Matt Mazur, "A Step by Step Backpropagation Example" — https://mattmazur.com/2015/03/17/a-step-by-step-backpropagation-example/
  Live-fetched. Confirms the pedagogical pattern: redraw the network after applying the new weights so the
  next pass starts from the updated values.
- "Backpropagation step-by-step derivation" (Towards Data Science) — https://towardsdatascience.com/backpropagation-step-by-step-derivation-99ac8fbdcc28/
  Confirms the topology the frame redraws: fully-connected input→hidden→output plus a bias node per
  computing layer feeding a constant 1.

## What the source(s) confirm (cross-checked against slide 028's own arithmetic)

The updated values the frame carries should equal slide 028's computed new weights. Cross-check:
- Hidden→output: W63 = −0.29 ✓ (0.3−0.59), W64 = −0.218 ✓ (0.4−0.618), W65 = −0.134 ✓ (0.5−0.634),
  W6b = −0.455 ✓ (0.2−0.655), W73 = 0.458 ✓, W74 = 0.565 ✓, W75 = 0.669 ✓, W7b = 0.375 ✓.
- Input→hidden weights are NOT yet updated at this point: 0.1/0.2/0.3 (x1 row), 0.4/0.5/0.6 (x2 row),
  bias 0.1/0.1/0.1 — all unchanged from the slide-27 initial diagram. That ordering is correct: the
  slide's numbers show only the output layer has been updated so far.
- Input/target values unchanged: x1 = [1], x2 = [5], target [0]/[1], η = 5.

## Corrections / notes

- IMPORTANT, for the recreation: the parse/analysis value list for this slide is INTERNALLY INCONSISTENT
  with the frame's own arithmetic and with slide 028. It contains both "−0.134" AND "−0.344", and both
  "−0.455" AND "−0.445". Slide 028 computes W65 = 0.5 − 0.634 = −0.134 and W6b = 0.2 − 0.655 = −0.455,
  so the correct post-update values are −0.134 and −0.455; the −0.344/−0.445 readings are
  transcription noise. Do not let a build "average" or carry both — use the slide-028-consistent pair.
- The doc-parse `chart type="scatter"` block on this slide is a mis-tagged rendering of the diagram's
  weight labels, not a data chart. There is no dataset/plot here — build it as the network diagram.
- Course-authored visual deltas (red border box, yellow hidden circles, orange output circles,
  green/purple edge colours, the η=5 corner note) have no source counterpart — keep them; the frame wins.
## Audit

Audited by lane S scope `b_src_2` (web-source audit), 2026-10-31. Method: independent Python
recomputation of slide 028's arithmetic, then cross-checking the values this frame carries
against it; cross-read against `analysis/parse/slide_029.parse.md`,
`analysis/slide_029_final.json` and `analysis/slide_029_raw.json`.

Questions asked:
1. Do the output-layer weight values the frame carries equal slide 028's computed new weights?
2. Are the input→hidden weights still at their initial values at this point (correct ordering)?
3. The final JSON's label list contains BOTH "−0.344" and "−0.134", and BOTH "−0.445" and
   "−0.455" — which pair is correct?
4. Is the doc-parse `chart type="scatter"` block on this slide a real data chart?

Answers:
- Q1 **CONFIRMED**. W63 = −0.29, W64 = −0.218, W65 = −0.134, W6b = −0.455, W73 = 0.458,
  W74 = 0.565, W75 = 0.669, W7b = 0.375 — all eight equal slide 028's recomputed updates.
- Q2 **CONFIRMED** and correct as an ordering. Input→hidden weights remain 0.1/0.2/0.3 (x1
  row), 0.4/0.5/0.6 (x2 row), bias 0.1/0.1/0.1 — unchanged from slide 27's initial diagram.
  Only the output layer has been updated so far, which is exactly what "After Updating O/p
  Layer weights" means.
- Q3 **CONFIRMED** the −0.134 / −0.455 pair, and REJECTED −0.344 / −0.445:
  W65 = 0.5 − 0.634 = −0.134 (not −0.344); W6b = 0.2 − 0.655 = −0.455 (not −0.445). The
  −0.344/−0.445 readings are transcription noise; carrying both into a build would produce a
  wrong diagram.
- Q4 **NOT-VERIFIABLE as a chart.** The parse's `scatter` block (categories X1…X5, A, Bias with
  values 0.1/0.2/0.4/−0.218/0.565/0.4/0.1/…) is a mis-tagged rendering of the network
  diagram's weight labels. There is no dataset/plot on this slide — build it as the diagram.

Verdicts per claim:
- All eight post-update output-layer weights — **CONFIRMED**.
- Input→hidden weights unchanged at this stage — **CONFIRMED** (correct training order).
- Inputs x1 = [1], x2 = [5] and targets [0]/[1], η = 5 — **CONFIRMED** (consistent with slide 27).
- Final JSON's "−0.134" / "−0.455" — **CONFIRMED**.
- Final JSON's "−0.344" / "−0.445" — **CONFLICT** with slide 028's arithmetic; discard.
- doc-parse `scatter` chart block — **CONFLICT** (mis-tagged diagram, not a chart).
- Course-authored visual deltas (red border box, yellow hidden circles, orange output circles,
  green/purple edge colours, the η=5 corner note) — **NOT-VERIFIABLE** (no source counterpart
  exists); the frame wins.

New sources found during audit (real URLs, not previously cited):
- MIT OCW 9.641, "Lecture 20: Backprop" —
  https://ocw.mit.edu/courses/9-641j-introduction-to-neural-networks-spring-2005/5d46d3b6e32a5120fe9893193c31e926_lec20_backprop.pdf
- Math StackExchange, "Backpropagation hidden layer error" —
  https://math.stackexchange.com/questions/4686558/backpropagation-hidden-layer-error

Audit summary: the frame's numbers are correct and consistent with slide 028. The material
risk here is the analysis JSON's duplicated contradictory values (−0.344/−0.445) — a build
must use −0.134/−0.455 or the diagram is wrong.

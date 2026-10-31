# Source Research — slide_024 (Stopping Criteria)

Topic: four training stopping conditions plus the four expected failure reasons when
training stops at the maximum-number-of-iterations limit.

## Verified criteria and reasons (match slide verbatim)
- [1] Total error = 0 is theoretical only — sources agree exact-zero error is
  unreachable in practice (noise, floating point), which is why the slide marks it
  "(Theoretical)".
- [2] Total error < threshold and [3] percentage weight change < threshold are
  standard convergence/tolerance stopping rules (error tolerance, weight- or
  gradient-change tolerance ε).
- [4] Maximum iterations/epochs is the hard failsafe; an epoch = one full pass over
  the training set. Reaching it without satisfying [2]/[3] means training FAILED.
- Failure reasons confirmed standard:
  [1] epoch limit set too small → premature stop = underfitting → raise the limit.
  [2] underfitting from inadequate training samples → provide more samples.
  [3] model design unsuitable → add hidden-layer nodes or more hidden layers.
  [4] data not separable by the network → try another model, e.g. SVM with kernels
      (kernel trick maps data to a space where a linear hyperplane separates).

## Sources
- MathWorks MATLAB Central — "Why does the neural network training end before reaching
  the specified maximum number of epochs?" —
  https://se.mathworks.com/matlabcentral/answers/372430/why-does-the-neural-network-training-end-before-reaching-the-specified-maximum-number-of-epochs
  Confirms epoch-limit vs convergence-criterion stopping distinction.
- "Early stopping to avoid overtraining neural network models" (Machine Learning
  Mastery) — https://machinelearningmastery.com/early-stopping-to-avoid-overtraining-neural-network-models/
  Underfitting/overfitting from too-low/high epoch limits.
- "The million dollar question: when to stop training deep learning models"
  (Medium / Data Science) —
  https://medium.com/data-science/the-million-dollar-question-when-to-stop-training-deep-learning-models-fa9b488ac04d
  Stopping-criteria taxonomy (thresholds, validation monitoring).
- "Regularization by early stopping" (GeeksforGeeks) —
  https://www.geeksforgeeks.org/machine-learning/regularization-by-early-stopping/
  Standard stopping-criteria list.
- Cambridge R222 lecture notes "Active Learning" (al1.pdf) —
  https://www.cl.cam.ac.uk/teaching/1617/R222/al1.pdf
  SVM with kernels as the alternative when data is not separable by a linear
  hyperplane.

## Corrections / notes
- None found: the four criteria and four failure reasons match standard ML practice;
  no numeric or structural discrepancy against sources.
- No named library function implements "percentage change of weights" (unverified as
  a specific API; it is the standard Δw/w < ε convergence test described in prose).
## Audit

Audited by lane S scope `b_src_2` (web-source audit), 2026-10-31. Method: independent agy
web-search; cross-read against `analysis/parse/slide_024.parse.md` and
`analysis/slide_024_final.json` (title "Stopping Criteria").

Questions asked:
1. Is "Total Error = zero" correctly marked "(Theoretical)" rather than a practical criterion?
2. Are "Total Error < threshold" and "Percentage Change of Weights < threshold" standard
   stopping rules?
3. Is "Reach Maximum number of iterations (Epochs)" the correct hard failsafe, and is
   "epoch" = one full pass over the training set?
4. Are the four failure reasons standard: epoch limit too small / underfitting from too few
   samples / unsuitable model design / data not separable by the network (use SVM with kernels)?
5. Does the kernel trick actually resolve non-linearly-separable data?

Answers:
- Q1 **CONFIRMED**. Sources treat exact-zero error as unreachable in practice (noise,
  floating point), which is why it is theoretical only.
- Q2 **CONFIRMED**. Search confirms both a loss-improvement threshold
  (`|Loss_epoch − Loss_{epoch−1}| < Threshold`) and a weight-change tolerance
  (`||ΔW|| < tolerance`) as standard convergence criteria. The "percentage change of
  weights" form is the relative variant of the same test.
- Q3 **CONFIRMED**. Search defines an epoch as one complete pass over the entire training
  dataset, and treats the max-epoch limit as the hard budget. Reaching it without meeting
  the convergence criteria means training failed.
- Q4 **CONFIRMED**. The four reasons map onto the standard taxonomy: too-low epoch limit →
  premature stop / underfitting → raise the limit; inadequate training samples → underfitting
  → get more data; unsuitable model design → add hidden nodes or layers; non-separable data
  → switch model class.
- Q5 **CONFIRMED**. The kernel trick implicitly maps the input into a higher-dimensional
  feature space where non-linearly-separable data becomes linearly separable (RBF/polynomial
  kernels), giving a non-linear boundary in the original space.

Verdicts per claim:
- [1] Total Error = zero (Theoretical) — **CONFIRMED**.
- [2] Total Error < certain value (Threshold) — **CONFIRMED**.
- [3] Percentage Change of Weights < certain value (Threshold) — **CONFIRMED** as a
  standard tolerance test.
- [4] Reach Maximum number of iterations (Epochs) without satisfying [2] or [3] — **CONFIRMED**.
- "Stopping is due to reaching Maximum number of iterations = Training is FAILED" — **CONFIRMED**.
- Failure reasons [1]–[4] — **CONFIRMED**.
- "Try Another Models (e.g. SVM with Kernels)" for non-separable data — **CONFIRMED**.
- No named library API implements a "percentage change of weights" stop rule — **NOT-VERIFIABLE**
  as a specific API; it is the standard Δw/w < ε convergence test described in prose.

New sources found during audit (real URLs, not previously cited):
- arXiv 2403.02473 — https://arxiv.org/html/2403.02473v1
  States the epoch definition (one full pass over the training set, completed only after
  every mini-batch has been processed).
- APXML, "Early stopping" —
  https://apxml.com/courses/introduction-to-neural-networks/chapter-6-improving-network-performance/early-stopping
  Threshold-based stopping and validation-monitoring taxonomy.
- Wikipedia, "Learning rule" — https://en.wikipedia.org/wiki/Learning_rule
- FU Berlin SOGA, "Widrow-Hoff rule" —
  https://www.geo.fu-berlin.de/en/v/soga-py/Machine-learning/Artifical-Neural-Networks/Widrow-Hoff-rule/index.html

Audit summary: every criterion and every failure reason on this slide is confirmed standard
practice. No conflicts. One honest residual: no library-specific API implements the
percentage-weight-change rule.

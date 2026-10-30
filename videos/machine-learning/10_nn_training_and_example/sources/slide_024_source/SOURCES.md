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

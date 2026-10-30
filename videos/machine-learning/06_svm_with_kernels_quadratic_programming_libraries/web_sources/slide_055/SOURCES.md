# Source verification — slide 055
## Claims checked
- Slide shows a two-class checkerboard pattern (alternating red/blue shaded squares, 4x4 grid over x:0-25, y:0-25 axes, block boundaries at 6.25/12.5/18.75) — CONFIRMED (as a data claim) — GeeksforGeeks, "Non-linear SVM" https://www.geeksforgeeks.org/machine-learning/ml-non-linear-svm/
  A checkerboard/XOR arrangement of the two classes is the standard not-linearly-separable demonstration; no single straight hyperplane can separate it, which is why a kernel is needed.
- Kernelized SVM with an RBF kernel produces exactly this kind of alternating, closed-loop checkerboard decision regions — CONFIRMED — scikit-learn SVC documentation https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html
  RBF is the default kernel of sklearn.svm.SVC and yields non-linear decision boundaries; `gamma` controls how far each training point's influence reaches (small gamma = smooth/underfit, large gamma = tight islands/overfit). See also https://scikit-learn.org/stable/auto_examples/svm/plot_svm_kernels.html
- The specific scatter coordinates decoded by doc-parse (series A, x=3..24 with y 21.5/16/10/9/10/15/...) — UNVERIFIABLE — no external source
  These are in-lecture synthetic points read off the raster; they are not a named public dataset, so no authoritative form exists. Treat them as approximations of dot positions, not canonical values.
- Hyperparameter/notation names if the rebuild renders or regenerates the plot — CONFIRMED — scikit-learn SVC docs (same URL as above)
  Use `kernel='rbf'`, `C`, `gamma`; gamma defaults in modern sklearn are `'scale'` = 1/(n_features * X.var()) since v0.22. If any kernel formula is rendered, the standard form is K(x,x') = exp(-gamma*||x-x'||^2).
## Overall
- VERDICT: CONFIRMED
- Tolerance notes for the rebuild: block boundary positions (6.25, 12.5, 18.75) are exact quarters of the 0-25 axis range — internal geometry, no source needed; red-vs-blue class assignment follows the original pattern; the checkerboard topology (not the decoded point list) is the fidelity target; no sign conventions at stake.

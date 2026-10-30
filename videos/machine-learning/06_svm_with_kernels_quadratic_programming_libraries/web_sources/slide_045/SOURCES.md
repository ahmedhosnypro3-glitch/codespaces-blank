# Source verification — slide 045
## Claims checked

- Frame shows a multi-class SVM decision-boundary figure: per-class coloured shaded regions
  with overlaid coloured scatter points, axes 0–50 (x) and 0–30 (y), four regions (black
  top-left, magenta top-middle, green bottom-left, red right) plus a blue cluster near
  (35,16) — CONFIRMED — scikit-learn SVM examples gallery, plot_svm_kernels,
  https://scikit-learn.org/stable/auto_examples/svm/plot_svm_kernels.html
  Coloured per-class regions with training points overlaid on kernel (non-linear) boundaries are the
  standard figure for SVM with more than two classes.

- Multi-class decomposition behind that figure — CONFIRMED — scikit-learn SVM module docs,
  https://scikit-learn.org/stable/modules/svm.html
  `sklearn.svm.SVC` (libsvm) always trains one-vs-one over n_classes·(n_classes−1)/2
  binary classifiers; `decision_function_shape='ovr'` (default) only reshapes
  `.decision_function()` to (n_samples, n_classes) without changing the OvO training;
  `LinearSVC` is one-vs-rest. Four visible regions ⇒ 4·3/2 = 6 pairwise classifiers.

- Region-shading technique implied by dense dots over solid coloured blocks — CONFIRMED —
  scikit-learn `plot_classification`, https://scikit-learn.org/0.18/auto_examples/neighbors/plot_classification.html
  `np.meshgrid` over the axis range, classifier `predict` per grid point, `pcolormesh` with
  `ListedColormap` for regions, `scatter(c=y, edgecolor="k")` bold for points. Modern
  equivalent: `sklearn.inspection.DecisionBoundaryDisplay.from_estimator` (same svm gallery).

- doc-parse decoded point series (10,22) (15,23) (20,22) (25,21) (30,22) (35,23) (40,21)
  (42,20) (43,18) — UNVERIFIABLE — no external source
  In-lecture synthetic points read off the raster, not a named public dataset; treat as
  approximate dot positions — the region topology, not the point list, is the target.

- Tooling/naming if the plot is regenerated: `SVC(kernel='rbf')`, `C`, `gamma` (default
  `'scale'` = 1/(n_features·X.var()) since sklearn v0.22); RBF form K(x,x') =
  exp(−gamma·‖x−x'‖²) — CONFIRMED — https://scikit-learn.org/stable/modules/svm.html
  Consistent with the neighbouring slides' kernel notation (γ = RBF bandwidth).

## Overall

- VERDICT: CONFIRMED
- 3 web searches spent; no source-driven DATA changes. The decoded coordinates are the
  only unconfirmable items and are not slide-asserted values — `verbatim_text` stays as recorded.
- Tolerance notes for the rebuild: the original frame has no title, legend or axis labels —
  the build's "SVM Decision Boundary Visualization" is a contextual label, not frame text;
  do not add legend/labels to the embedded plot. Keep axes 0–50 x / 0–30 y (measured off the
  frame) and the four-region topology with the blue cluster ~(35,16). If regenerated:
  `kernel='rbf'`, SVC's one-vs-one behaviour, light `cmap_light` region washes with
  `edgecolor="k"` bold markers, matching the original's solid backgrounds.

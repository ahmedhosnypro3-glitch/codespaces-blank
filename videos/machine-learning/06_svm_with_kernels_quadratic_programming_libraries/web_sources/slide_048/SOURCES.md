# Source verification — slide 048

## Claims checked

- Frame depicts three point clusters: a red C-shape/ring enclosing a blue left-center blob and
  a black right-center blob (axes 0-40 x, 0-35 y; badge "48"; no title/legend/axis labels on
  the original) — CONFIRMED (as a data claim) — GeeksforGeeks, "Non-linear SVM"
  https://www.geeksforgeeks.org/machine-learning/ml-non-linear-svm/ ; DataCamp, "Kernel Trick"
  https://www.datacamp.com/tutorial/kernel-trick
  A three-class scatter whose outer class is an annular ring enclosing two inner blobs is the
  canonical not-linearly-separable demonstration; the frame shows exactly this topology.
- That arrangement is not linearly separable — no straight hyperplane isolates the ring class
  from the two inner classes without cutting through them — CONFIRMED — same sources
- Remedy shape for such nested data — a non-linear kernel SVM yields closed curved boundaries
  (inner contour plus outer bound for the ring class, island boundaries for the inner classes)
  — CONFIRMED — scikit-learn SVM examples gallery
  https://scikit-learn.org/stable/auto_examples/svm/plot_svm_kernels.html
  If annotated/regenerated: RBF is sklearn's default SVC kernel, K(x,x') =
  exp(-gamma*||x-x'||^2), gamma default 'scale' = 1/(n_features*X.var()) since v0.22.
- Axis tick ranges x: 0, 8, 16, 24, 32, 40 and y: 0, 7, 14, 21, 28, 35, plus the light-gray
  grid — UNVERIFIABLE — no external source
  Internal plot geometry of an in-lecture synthetic figure; no authoritative axis window
  exists. Measure off `unique_slides/slide_048.jpg` (matches sibling verdicts 046/047/050/053).
- doc-parse decoded point table (x = 5,6,7,...,33; y = 15,...,31.5, 29 rows) — UNVERIFIABLE,
  discard as artifact — no external source
  Not on-slide data: a parser transcription artifact, per `analysis/parse_out_047/
  slide_047.parse.md`'s note that sibling parses (045/046/048) type the same figure as
  scatter/multi_line and its x column walks a sequence, not the axis ticks.
- Build strings "SVM Kernel Classes — Three-Cluster Visualization", three legend lines, and
  axis labels "Feature 1"/"Feature 2" in `recreated_pptx/build/slide_048.js` — UNVERIFIABLE,
  builder-added chrome — no external source
  The original frame carries no title, legend, or axis titles; `qa/slides_045_055/
  judge_048.txt` records these as additions the recreation introduced.

## Overall

- VERDICT: CONFIRMED — 2 of 6 searches spent (stopped early: both topology claims confirmed;
  remaining items are measurements or artifacts a source cannot settle).
- Tolerance notes for the rebuild: nothing to correct in any spec — no formula, library or
  dataset name, hyperparameter, sign convention, or attribution appears on the frame, so
  there is no DATA value to tighten. Fidelity target is the nested topology (red ring /
  C-shape class enclosing a blue left blob and a black right blob), the red/blue/black class
  colors, and the ABSENCE of any title, legend, axis titles, or drawn decision boundary — the
  original deliberately shows none. Keep axis windows exactly 0-40 x 0-35 y as measured off
  the raster. Badge reads 48. Do not transcribe the doc-parse coordinates; regenerate the
  cluster/ring geometry synthetically (advanced-graph rule).
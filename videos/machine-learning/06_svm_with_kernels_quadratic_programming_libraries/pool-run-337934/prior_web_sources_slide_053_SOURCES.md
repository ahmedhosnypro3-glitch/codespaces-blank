# Source verification — slide 053
Frame evidence: vision record `analysis/slide_053_raw.json` + judge transcript `qa/slides_045_055/judge_053.txt`.
Method: live re-fetch of both recorded URLs in this work window (2026-10-28) + cross-check against banked
vision/judge records. 0 new web searches spent (economy law: claims already covered; sources re-fetched live
instead, which is a fetch, not a query).
## Claims checked
- Frame shows a two-class scatter: red points in an upper band (y~20-31), blue points in a lower / U-shaped
  enclosing arrangement, plus vertical blue bands left and right; no title, no legend, no axis titles
  anywhere on the frame — CONFIRMED — banked vision record `analysis/slide_053_raw.json` §1/§3 plus judge
  transcript `qa/slides_045_055/judge_053.txt` §1 (frame is ground truth; two independent records agree).
- The plotted geometry is non-linearly separable: no single straight hyperplane splits the two classes,
  since one class is enclosed by the other in a U/bowl — CONFIRMED — GeeksforGeeks, "Non-Linear SVM"
  https://www.geeksforgeeks.org/machine-learning/ml-non-linear-svm/ (live fetch 2026-10-28)
  Quoted: "the standard (linear) SVM can only classify data that is linearly separable, meaning a straight
  line can separate the classes (in 2D) or a hyperplane (in higher dimensions)", and the enclosed
  "circular cluster surrounded by oranges" case is called out as the one a linear SVM "can't separate".
- A kernelized SVM yields curved / enclosing boundaries for exactly this class arrangement — CONFIRMED —
  scikit-learn SVC documentation https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html
  (live fetch 2026-10-28) — kernel='rbf' is the default; gamma defaults to 'scale' = 1/(n_features *
  X.var()); "Changed in version 0.22: The default value of gamma changed from 'auto' to 'scale'"; doc
  links the gallery "Plot classification boundaries with different SVM Kernels" for non-linear boundaries.
- Axis ranges x -5..20, y 0..35, tick positions, dotted gridlines — UNVERIFIABLE — no external source
  Internal chart geometry measured off the raster and independently confirmed by the judge pass; no
  authoritative external form exists for a synthetic in-lecture plot.
- Exact point coordinates of either series — UNVERIFIABLE — no external source
  In-lecture synthetic points, not a named public dataset: treat dot positions as approximations, never
  as canonical values to be copied verbatim.
- doc-parse decoded the plot as a `line` chart with one series (-5,12),(0,22),(5,18),(6,20),(7,16),(8,19),
  (10,20),(15,27) — UNVERIFIABLE, discard — no external source
  Parser misclassification: the frame is a TWO-series scatter, not a single line series. That coordinate
  list must not drive the rebuild; the certified build embeds a graphgen-generated topology PNG instead.
## Overall
- VERDICT: CONFIRMED
- Tolerance notes for the rebuild: fidelity target is the TOPOLOGY (red upper band + blue lower/U enclosing
  class), not any decoded coordinate list — regenerate the scatter synthetically. Axis range x -5..20,
  y 0..35 is exact per the raster. Original has no legend and no axis titles; the added build title is a
  permitted e-format upgrade per the judge, not a discrepancy. Class colors red vs blue. No sign
  conventions or hyperparameter values are asserted by this frame — do not annotate a kernel form onto it;
  if one is ever needed, the standard form is K(x,z) = exp(-gamma*||x-z||^2) with gamma='scale'
  = 1/(n_features * X.var()) (sklearn >= 0.22).

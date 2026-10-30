# Source verification — slide 053
Frame evidence: vision record `analysis/slide_053_raw.json` + judge transcript `qa/slides_045_055/judge_053.txt` (both agree). 3 agy web searches spent in this run.
## Claims checked
- Slide shows a two-class scatter plot (red band on top, blue dots forming a lower U / enclosing shape) with no title, no legend, no axis titles — CONFIRMED — GeeksforGeeks, "Non-linear SVM" https://www.geeksforgeeks.org/machine-learning/ml-non-linear-svm/
- The plotted geometry is non-linearly separable: no single straight hyperplane splits the two classes, since one class is enclosed by the other in a U/bowl — CONFIRMED — GeeksforGeeks, "Non-linear SVM" https://www.geeksforgeeks.org/machine-learning/ml-non-linear-svm/
- Kernelized SVM with a curved/closed boundary is the standard remedy for exactly this class arrangement — CONFIRMED — scikit-learn SVC documentation https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html
- Axis ranges x: -5 to 20, y: 0 to 35, tick positions, dotted gridlines — UNVERIFIABLE — no external source (internal chart geometry measured off the raster; no authoritative external form exists)
- Exact point coordinates of either series — UNVERIFIABLE — no external source (in-lecture synthetic points, not a named public dataset; treat dot positions as approximations, never canonical values)
- doc-parse decoded the plot as a `line` chart with one series (-5,12),(0,22),(5,18),(6,20),(7,16),(8,19),(10,20),(15,27) — UNVERIFIABLE, discard — no external source (parser misclassification: the frame is a TWO-series scatter, not a single line series; that coordinate list must not drive the rebuild)
## Overall
- VERDICT: CONFIRMED
- Tolerance notes for the rebuild: the fidelity target is the TOPOLOGY (red upper band + blue lower/enclosing U), not any decoded coordinate list — regenerate the scatter synthetically; axis range x -5..20, y 0..35 is exact per the raster; original has no legend and no axis titles (the build title is a permitted e-format upgrade per the judge, not a discrepancy); class colors red vs blue; no sign conventions or hyperparameter values are asserted by this frame; if any kernel form is ever annotated here, the standard form is K(x,z) = exp(-gamma*||x-z||^2) with gamma='scale' = 1/(n_features * X.var()) since sklearn 0.22.

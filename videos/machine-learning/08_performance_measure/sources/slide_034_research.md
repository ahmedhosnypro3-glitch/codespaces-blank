# Sources — Slide 34 — ROC Curve for Same Model -different thresholds (thresholds 0.0, 0.1, 0.3, 0.4, 0.6, 0.7)

- Six thresholds → six labeled points, one (FPR, TPR) pair each: CONFIRMED — sklearn `roc_curve` docs (https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_curve.html) — parallel `fpr`/`tpr`/`thresholds` arrays give one plotted point per threshold, matching the frame's six red points labeled 0.3/0.1/0.0/0.7/0.4/0.6.
- Threshold=0.7 gives FPR=0/(0+6)=0 — no negative sample is predicted positive: CONFIRMED — ROC and AUC (Google ML Crash Course, https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc) — FPR = FP/(FP+TN) is exactly 0 when FP = 0; the panel's matrix (TP=3, FN=2, FP=0, TN=6) yields 0/6 = 0.
- The frame's "Best (FPR)" annotation on the threshold=0.7 panel is consistent with FPR's best value being 0: CONFIRMED — Receiver operating characteristic, Wikipedia (https://en.wikipedia.org/wiki/Receiver_operating_characteristic) — FPR = 0 is the lower/best bound of the x-axis; a point with FPR = 0 is as far left on the ROC plot as any operating point can sit.
- The remaining panel arithmetic checks out: TPR=3/(3+2)=0.6 at 0.7, TPR=4/(4+1)=4/5 at 0.4, FPR=1/(1+5)=0.16 at 0.4: CONFIRMED — sklearn `roc_curve` docs — 3/5 = 0.6, 4/5 = 0.8 and 1/6 ≈ 0.16 are exactly TP/(TP+FN) and FP/(FP+TN) for their matrices.

## Corrections
- None applied to the spec. The frame's threshold=0.6 panel repeats the `TPR=3/(3+1)=0.6` slip recorded on `sources/slide_033_research.md`; it is course-authored and recreated verbatim.

## Course-authored elements (no source counterpart — do not "fix")
- The 2x4 panel grid, red-bordered panels, gray title box, and the "Best (FPR)" callout are presentation/pedagogy; sources confirm the matrix counts and rates only.

## Method
Tool: `mcp__agy-cli-mcp__agy_web_search` (1 new query for the FPR=0 best-value point; the remainder re-used the sklearn `roc_curve` + Wikipedia ROC records banked on slide 028).

## Cross-check (lane F, 2026-10-31, agy web search)

- Six threshold panels (0.0/0.1/0.3/0.4/0.6/0.7) with their matrices and TPR/FPR lines, plus the ROC plot with threshold-labeled points and "Best (FPR)" marker: CONFIRMED — sklearn `roc_curve` (https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_curve.html) and Google ML Crash Course ROC/AUC (https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc): each threshold yields one (FPR,TPR) point, plotted from (1,1) at threshold 0.0 down-left as threshold rises; "best" operating point selection near the top-left corner (min distance to (0,1) / max Youden's J = TPR-FPR) per Evidently AI ROC guide (https://www.evidentlyai.com/classification-metrics/explain-roc-curve) and Wikipedia Youden's J (https://en.wikipedia.org/wiki/Youden%27s_J_statistic). Panel arithmetic: 0.7 -> TPR=3/(3+2)=0.6, FPR=0/(0+6)=0 (re-verified locally, correct); the 0.6 panel's printed TPR=3/(3+1)=0.6 is the known course-authored slip (correct 0.75) — CORRECTED on slide 033, frame wins. No new corrections.

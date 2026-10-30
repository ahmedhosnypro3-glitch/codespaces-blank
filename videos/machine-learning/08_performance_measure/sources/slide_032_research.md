# Sources — Slide 32 — ROC Curve for Same Model -different thresholds (0.0 / 0.1 / 0.3 / 0.4)

- Threshold=0.4 gives TPR = 4/(4 + 1) = 4/5 = 0.8: CONFIRMED — "Explain the ROC curve" (Evidently AI, https://www.evidentlyai.com/classification-metrics/explain-roc-curve) — 4/5 = 0.8 is TP/(TP+FN) for the panel's matrix (TP=4, FN=1); this is the first threshold in the sweep where an actual positive is missed.
- Threshold=0.4 gives FPR = 1/(1 + 5) = 0.16: CONFIRMED — sklearn `roc_curve` docs (https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_curve.html) — 1/6 = 0.167 ≈ 0.16 is FP/(FP+TN) for FP=1, TN=5.
- Recall starts dropping only once the threshold passes actual-positive scores, while FPR keeps dropping with it: CONFIRMED — "Classification thresholds in machine learning" (https://medium.com/@yasvanthkohli/classification-thresholds-in-machine-learning-6d7cf3cf38a4) — the sweep 0.0 → 0.4 takes the operating point from (1, 1) down-left to (0.16, 0.8).
- Four thresholds → four labeled points on the ROC axes, still without a connecting curve: CONFIRMED — ROC and AUC (Google ML Crash Course, https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc) — the curve is the complete locus of per-threshold points; a subset is correctly drawn as discrete points.

## Course-authored elements (no source counterpart — do not "fix")
- The four red-bordered panels, axis arrows, white point-label boxes, and the slide-number badge are styling; only the matrix values and the derived TPR/FPR numbers are source-backed.
- The "0.4" annotation on the plot reads at (FPR=0.16, TPR=0.8) in the frame — plot the point where the frame puts it, not at a recomputed position.

## Method
Tool: `mcp__agy-cli-mcp__agy_web_search` (1 new query; 3 claims carried from slides 28-31 records). Spec consumed: `analysis/slide_032_final.json`; frame `unique_slides/slide_032.jpg`.

# Sources — Slide 31 — ROC Curve for Same Model - Different Thresholds (0.0 / 0.1 / 0.3)

- Threshold=0.3 gives FPR = 2/(2 + 4) = 0.33 with TPR still 1: CONFIRMED — "Explain the ROC curve" (Evidently AI, https://www.evidentlyai.com/classification-metrics/explain-roc-curve) — each step up in the threshold keeps peeling negatives off the "predicted positive" set; 2/6 = 0.333 is FP/(FP+TN) for the panel's matrix (TP=5, FN=0, FP=2, TN=4).
- Both rates fall monotonically as the threshold rises (0.0 → 0.1 → 0.3 produces FPR 1 → 0.66 → 0.33 at TPR = 1): CONFIRMED — "Classification thresholds in machine learning" (https://medium.com/@yasvanthkohli/classification-thresholds-in-machine-learning-6d7cf3cf38a4) — raising the threshold reduces predictions of both kinds, so both TPR and FPR are non-increasing; the plot points march leftward/ downward.
- Three thresholds → three scattered points labeled 0.3, 0.1, 0.0 on the ROC axes: CONFIRMED — sklearn `roc_curve` docs (https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_curve.html) — each threshold index contributes one (fpr, tpr) pair to the arrays; labeling the points by threshold is the standard way to show the sweep.
- No connecting curve is drawn yet at this stage of the build-up: CONFIRMED — ROC and AUC (Google ML Crash Course, https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc) — the curve is only the locus of all per-threshold points, so a partial set of thresholds is correctly shown as discrete points.

## Course-authored elements (no source counterpart — do not "fix")
- Threshold panel styling (white bold headers on red), the bottom title box, the formula panel, and the small color-coded legend matrix are presentation choices; sources confirm only the matrix counts and the derived rates.
- The consumed spec's subtitle ("Confusion Matrices at Thresholds 0.0, 0.1, and 0.3") is a spec-added header, not text present on the frame — do not render it on the recreation.

## Method
Tool: `mcp__agy-cli-mcp__agy_web_search` (1 new query; 3 claims carried from slides 28-30 records). Spec consumed: `analysis/slide_031_final.json`; frame `unique_slides/slide_031.jpg`.

## Cross-check (lane F, 2026-10-31, agy web search)

- Threshold=0.3 panel: matrix [[5,0],[2,4]] (TP=5, FN=0, FP=2, TN=4), TPR=5/(5+0)=1, FPR=2/(2+4)=.33: CONFIRMED — sklearn `roc_curve` docs (https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_curve.html): thresholds sweep downward so the operating point marches from (1,1) at threshold 0.0 toward (0,0) as the threshold rises; with TP=5, FN=0 -> TPR=1, FP=2, TN=4 -> FPR=2/6=0.333 (frame prints .33; re-verified locally). Point (0.33, 1) lies left of the 0.1 point (0.66, 1), consistent with the frame's plotted order. No corrections.

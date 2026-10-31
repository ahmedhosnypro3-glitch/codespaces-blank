# Sources — Slide 29 — ROC Curve for Same Model -different thresholds (Threshold=0.0)

- Threshold=0.0 gives a single operating point at TPR=1, FPR=1: CONFIRMED — "From toy boxes to code: simple intro to ROC & AUC" (https://dev.to/akshay_shetty_686041/from-toy-boxes-to-code-a-simple-intro-to-roc-auc-omf) — at threshold 0.0 every sample is predicted positive, so TP = all actual positives and FP = all actual negatives, giving the top-right corner (1, 1). Exactly what the frame plots.
- Confusion matrix at threshold 0.0 (TP=5, FN=0, FP=6, TN=0) is internally valid: CONFIRMED — sklearn `roc_curve` docs (https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_curve.html) — 5 actual positives and 6 actual negatives are the sample counts the deck reuses on slides 29–37; TPR = 5/(5+0) = 1 and FPR = 6/(6+0) = 1 follow directly.
- Each threshold produces exactly one (FPR, TPR) point, so a single plotted point (no curve yet) is correct at this stage: CONFIRMED — ROC and AUC (Google ML Crash Course, https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc) — the curve is the locus of the per-threshold points; with one threshold computed there is one point, not a line.
- Slide plots only the threshold=0.0 point labeled "0.0" at the top-right: CONFIRMED — cross-references `sources/slide_028_research.md` (no new query spent) — the threshold label beside the point is the standard annotation for "which threshold produced this operating point".

## Course-authored elements (no source counterpart — do not "fix")
- Grid layout, red/blue/gray panel styling, the yellow slide-number badge, and the generic color-coded TP/FN/FP/TN legend matrix are the course's own presentation; sources confirm the numbers only.
- A mouse cursor visible in the plot area is a screen-capture artifact, per the consumed spec — excluded from recreation.

## Method
Tool: `mcp__agy-cli-mcp__agy_web_search` (1 new query; 3 claims carried from `sources/slide_028_research.md` under the economy law). Spec consumed: `analysis/slide_029_final.json`; frame `unique_slides/slide_029.jpg`.

## Cross-check (lane F, 2026-10-31, agy web search)

- Threshold=0.0 panel: matrix [[5,0],[6,0]] (TP=5, FN=0, FP=6, TN=0), TPR=5/(5+0)=1, FPR=6/(6+0)=1, ROC point (FPR=1, TPR=1) top-right: CONFIRMED — sklearn `roc_curve` docs (https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_curve.html) and Stats StackExchange ROC-from-confusion-matrix (https://stats.stackexchange.com/questions/223749/): at threshold 0.0 every sample is predicted positive, giving TP=5, FN=0, FP=6, TN=0, hence TPR=5/5=1 and FPR=6/6=1, the (1,1) corner of the ROC plot (sklearn's last point). Arithmetic re-verified locally. No corrections.

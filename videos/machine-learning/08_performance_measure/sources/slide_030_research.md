# Sources — Slide 30 — ROC Curve for Same Model -different thresholds (Threshold=0.0 / Threshold=0.1)

- Raising the threshold to 0.1 lowers FPR to 0.66 while TPR stays 1: CONFIRMED — "Explain the ROC curve" (Evidently AI, https://www.evidentlyai.com/classification-metrics/explain-roc-curve) — a higher threshold makes the classifier more conservative, fewer negatives get flagged positive, so FPR drops; recall only falls once actual positives start being missed (none yet at 0.1: FN = 0).
- FPR = 4/(4 + 2) = 0.66 at threshold 0.1: CONFIRMED — sklearn `roc_curve` docs (https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_curve.html) — 4/6 = 0.667 is exactly FP/(FP+TN) for the panel's matrix (TP=5, FN=0, FP=4, TN=2); the deck's 0.66 is that value rounded down.
- Two thresholds produce two distinct (FPR, TPR) points — (1, 1) for 0.0 and (0.66, 1) for 0.1: CONFIRMED — ROC and AUC (Google ML Crash Course, https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc) — one point per threshold; the ROC sweep is built by computing the pair at each threshold in turn.
- Same-model sweep is threshold-only: the underlying model is unchanged, only the decision boundary moves: CONFIRMED — cross-references `sources/slide_029_research.md` (no new query spent) — "same model, different thresholds" is precisely the ROC curve's construction, versus a single operating point from one threshold.

## Course-authored elements (no source counterpart — do not "fix")
- The red-bordered matrix panels, blue grid dividers, gray title box, and the black arrow pointing from the threshold 0.1 panel toward the plot are presentation devices the sources say nothing about.
- Recreated point labels keep the deck's 0.66 / 1 / 1 values verbatim — sources confirm the arithmetic, they do not license re-rounding.

## Method
Tool: `mcp__agy-cli-mcp__agy_web_search` (1 new query; 2 claims carried from slide 28/29 records under the economy law). Spec consumed: `analysis/slide_030_final.json`; frame `unique_slides/slide_030.jpg`.

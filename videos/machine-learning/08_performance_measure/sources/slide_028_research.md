# Sources — Slide 28 — Receiver Operating Characteristic (ROC) Curve

- ROC is a graph showing the performance of a classification model at all classification thresholds: CONFIRMED — Google ML Crash Course, "Classification: ROC and AUC" (https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc) — ROC evaluates a binary classifier across every possible decision threshold, unlike accuracy/precision which need one threshold.
- TPR is a synonym for recall; TPR = TP/(TP + FN): CONFIRMED — scikit-learn `recall_score` docs (https://scikit-learn.org/stable/modules/generated/sklearn.metrics.recall_score.html) + GeeksforGeeks sklearn metrics (https://www.geeksforgeeks.org/machine-learning/sklearn-classification-metrics/) — TPR = recall = sensitivity; the deck's fraction and the underlined word "recall" are both right.
- FPR = FP/(FP + TN): CONFIRMED — ROC and AUC (Google ML Crash Course) + ROC curve overview (https://www.evidentlyai.com/classification-metrics/explain-roc-curve) — FPR is the fallout, equal to 1 − specificity; deck formula matches.
- TPR best value is 1 and FPR best value is 0: CONFIRMED — Receiver operating characteristic, Wikipedia (https://en.wikipedia.org/wiki/Receiver_operating_characteristic) — the ideal classifier sits at (FPR=0, TPR=1); the two "(Best Value is ...)" notes are the per-axis optima.
- An ROC curve plots TPR vs. FPR at different classification thresholds: CONFIRMED — sklearn `roc_curve` docs (https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_curve.html) — one (FPR, TPR) pair per threshold; `roc_curve` returns `(fpr, tpr, thresholds)` with y=TPR, x=FPR.

## Method
Tool: `mcp__agy-cli-mcp__agy_web_search` (3 queries) + live fetch of the sklearn `roc_curve` page. Spec consumed: `analysis/slide_028_final.json` (frame `unique_slides/slide_028-.jpg`, trailing dash). No figures downloaded (no hosted original linked to this slide). Per the source-research doctrine: the frame wins for recreation, the source wins for understanding — nothing on this slide needed a spec patch.

## Economy
Queries spent on this slide: 3. Two of its claims (TPR/FPR formulas, one-point-per-threshold) are the shared basis for slides 29–36 and are cross-referenced there instead of re-spent.

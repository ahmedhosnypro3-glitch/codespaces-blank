# Sources — Slide 36 — ROC Curve for Same Model -different thresholds (thresholds 0.0, 0.1, 0.3, 0.4, 0.6, 0.7, 1)

- Threshold=1 gives TPR=0/(0+5)=0 and FPR=0/(0+6)=0 — the (0, 0) operating point: CONFIRMED — "From toy boxes to code: simple intro to ROC & AUC" (https://dev.to/akshay_shetty_686041/from-toy-boxes-to-code-a-simple-intro-to-roc-auc-omf) — at threshold 1.0 nothing is predicted positive, so TP = FP = 0 and both rates are 0; with slide 29's threshold=0.0 point at (1, 1), the sweep now spans the full ROC square.
- Seven thresholds → seven labeled points on the same curve, one (FPR, TPR) pair each: CONFIRMED — sklearn `roc_curve` docs (https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_curve.html) — parallel `fpr`/`tpr`/`thresholds` arrays; the frame's labels 0.7/0.6/0.4/0.3/0.1/0.0/1.0 each mark one array row.
- The points are now connected into a curve rather than left as isolated dots: CONFIRMED — ROC and AUC (Google ML Crash Course, https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc) — connecting the per-threshold points is how the ROC curve is drawn; once every threshold in the sweep is computed, the locus becomes the curve.
- "Best (TPR)" and "Best (FPR)" annotations mark the axis optima of the sweep: CONFIRMED — Receiver operating characteristic, Wikipedia (https://en.wikipedia.org/wiki/Receiver_operating_characteristic) + the slide-28 record — TPR = 1 is the best y-axis value and FPR = 0 the best x-axis value, so the annotated extremes are the best reachable values of each axis within this sweep.
- The threshold=0.7 panel (TPR=3/(3+2)=0.6, FPR=0/(0+6)=0) is arithmetically correct, but the threshold=0.6 panel reading TPR=3/(3+1)=0.6 is CORRECTED — sklearn `roc_curve` docs — 3/5 = 0.6 and 0/6 = 0 check out at 0.7, while 3/(3+1) = 0.75 at 0.6; that slip is course-authored (same as slides 33-34) and the frame wins for recreation.

## Uncertain items
[?] The frame's green point at the top-left of the plot and the specific arrow targets of "Best (TPR)" / "Best (FPR)" cannot be resolved to a precise (FPR, TPR) coordinate from the vision record alone — the annotations are read as pointing at the sweep's axis-optimal points, and the pixel position of the green marker is left to the recreation brief rather than a computed value.

## Course-authored elements (no source counterpart — do not "fix")
- The purple connecting curve, the color-coded TP/TN vs FP/FN legend cells, and the straight lines radiating from the origin are presentation choices; sources confirm the per-threshold numbers only.

## Method
Tool: `mcp__agy-cli-mcp__agy_web_search` (1 new query for the connected-curve step; the rest cross-referenced from the slide-29/34/28 records — no new query spent). Spec consumed: `analysis/slide_036_final.json`; frame `unique_slides/slide_036.jpg`.

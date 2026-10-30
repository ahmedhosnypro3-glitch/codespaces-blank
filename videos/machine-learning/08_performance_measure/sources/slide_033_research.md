# Sources — Slide 33 — ROC Curve for Same Model -different thresholds (thresholds 0.0, 0.1, 0.3, 0.4, 0.6)

## Slide identity
Spec consumed: `analysis/slide_033_final.json`; frame `unique_slides/slide_033.jpg`; badge number 33. No `slide_035_final.json` exists in this namespace (only a doc-parse record) — noted in `sources/slide_035_research.md`.

- Five thresholds → five labeled points, one (FPR, TPR) pair each: CONFIRMED — sklearn `roc_curve` docs (https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_curve.html) — `roc_curve` returns parallel `fpr`/`tpr`/`thresholds` arrays; each threshold index contributes exactly one plotted point, matching the slide's five red points labeled 0.3/0.1/0.0/0.4/0.6.
- Monotone leftward/downward march of the operating point as the threshold rises (0.0 → 0.6 takes FPR from 1 down to 0.16): CONFIRMED — "Classification thresholds in machine learning" (https://medium.com/@yasvanthkohli/classification-thresholds-in-machine-learning-6d7cf3cf38a4) — raising the threshold lowers both rates, so the plotted points move toward the lower-left; the frame's point order matches.
- The panel arithmetic TPR=5/(5+0)=1, FPR=4/(4+2)=0.66, FPR=2/(2+4)=0.33 and FPR=1/(1+5)=0.16 checks out as TP/(TP+FN) and FP/(FP+TN): CONFIRMED — sklearn `roc_curve` docs + ROC and AUC (Google ML Crash Course, https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc) — every printed fraction except one is exactly the textbook formula applied to its matrix.
- TPR=3/(3+1)=0.6 at threshold 0.6: CORRECTED — sklearn `roc_curve` docs + ROC and AUC (Google ML Crash Course) — 3/(3+1) = 0.75, not 0.6; the stated 0.6 corresponds to 3/5, suggesting the denominator/FN was transcribed incorrectly by the course author. The frame wins for recreation: the plot point and label read exactly as the source shows (point labeled 0.6 at TPR≈0.6), recorded as a course-authored arithmetic slip, not content to silently patch.

## Course-authored elements (no source counterpart — do not "fix")
- Panel styling, axis arrows, white point-label boxes, the gray title box, and the color-coded TP/FN/FP/TN legend matrix are the course's own presentation; sources confirm only the counts and rates.
- The threshold=0.6 TPR value is course-authored (see the CORRECTED bullet) — recreate verbatim.

## Uncertain items
[?] Whether the intended matrix for threshold 0.6 had FN=2 (giving 3/5 = 0.6) or the intended TPR value was 0.75 — not resolvable from the frame alone; the frame's own point placement (TPR≈0.6) agrees with the printed 0.6, so recreation follows the frame.

## Method
Tool: `mcp__agy-cli-mcp__agy_web_search` (1 new query for the sweep direction; the rest re-fetched from the sklearn `roc_curve` record banked on slide 028 — no new query spent under the economy law).

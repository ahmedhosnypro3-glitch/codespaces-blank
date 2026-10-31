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

## Second-opinion (lane C, 2026-10-31, agy web search)

- The CORRECTED claim above is independently re-CONFIRMED: with TP=3, FN=1, TPR = 3/(3+1) = 3/4 = 0.75, not 0.6 — verified against OmniCalculator confusion-matrix calculator (https://www.omnicalculator.com/statistics/confusion-matrix) and StatisticsFundamentals confusion-matrix calculator (https://statisticsfundamentals.com/calculators/confusion-matrix-calculator/), both applying TPR = TP/(TP+FN) directly. The only way to get 0.6 is 3/5, i.e. FN=2, which contradicts the panel's printed FN=1 — so the course-authored slip stands as recorded, and the same correction recorded on slides 034-036 is corroborated. Frame still wins for recreation (recreate the printed 0.6 verbatim). No new corrections found.

## Cross-check (lane F, 2026-10-31, agy web search)

- Threshold=0.6 panel printed on this slide: matrix [[3,1],[1,5]] (TP=3, FN=1, FP=1, TN=5) with "TPR=3/(3+1)=0.6", FPR=1/(1+5)=0.16: the FPR is CONFIRMED (1/6=0.1667, frame truncates to 0.16 — re-verified locally); the TPR is CORRECTED — TPR = 3/(3+1) = 3/4 = 0.75, not 0.6, per OmniCalculator confusion-matrix calculator (https://www.omnicalculator.com/statistics/confusion-matrix) and Glass Box Medicine confusion-matrix guide (https://glassboxmedicine.com/2019/02/17/measuring-performance-the-confusion-matrix/): TPR = TP/(TP+FN) = 3/4 = 0.75; 0.6 would require 3/5 (FN=2), contradicting the printed FN=1. This re-confirms the prior lanes' CORRECTED finding. Frame text wins for recreation (printed 0.6 kept verbatim); sources correct the data only. All other panels on the slide (0.0/0.1/0.3/0.4) re-verified as correct in slides 029-032.

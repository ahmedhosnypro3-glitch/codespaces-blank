# Sources — Slide 010 — Recall

Spec: analysis/slide_010_raw.json (no slide_010_final.json exists yet). Original frame: unique_slides/slide_010.jpg.

- "Recall = TP / (TP + FN)" formula: CONFIRMED — "sklearn.metrics.precision_recall_fscore_support documentation" (https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_recall_fscore_support.html) — recall is defined as the ability of the classifier to find all the positive samples, TP/(TP+FN).
- Definition fraction "Correctly Classified (as Positive) over Total objects that should be retrieved (Actually Positive)": CONFIRMED — "Han & Kamber Ch.8 recall = completeness" (https://www.slideshare.net/slideshow/08-classbasic/39057275) — recall measures completeness; Han/Kamber also write recall = TP/P where P = TP + FN, i.e. all actually-positive tuples.
- Meaning "Does the classifier miss any of Positive Objects ?": CONFIRMED — "Sensitivity / Recall / TPR definition" (https://en.wikipedia.org/wiki/Sensitivity_and_specificity) — recall as sensitivity: false negatives are the positives the classifier missed; FN is explicitly "the positives that the classifier missed".
- Worked example "18/(18+12) = 60%": CONFIRMED — arithmetic check against sklearn's recall_score (https://scikit-learn.org/stable/modules/generated/sklearn.metrics.recall_score.html) — 18/(18+12) = 18/30 = 0.6 → 60%; frame values TP=18, FN=12 verified independently.
- Confusion matrix orientation ("Predicted as" column headers P/N, "Actual" row labels P/N; TP at (P,P), FN at (P,N), FP at (N,P), TN at (N,N)): CONFIRMED — "sklearn.metrics.confusion_matrix documentation" (https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html) — rows = true labels, columns = predicted labels; slide layout matches the documented C[i,j] convention.
- Numeric-matrix / tree splits (Positive tree root 30 = TP 18 + FN 12; Negative tree root 70 = FP 10 + TN 60): CONFIRMED — Han/Kamber Ch.8 matrix row totals (https://www.slideshare.net/slideshow/08-classbasic/39057275) — actual-positive row total P = TP + FN = 30, actual-negative row total N = FP + TN = 70.

## Second-opinion (lane D, 2026-10-31)

Method: `mcp__agy-cli-mcp__agy_web_search`, 5 batches x 4 queries, URLs resolved live; arithmetic re-computed locally. Verdict: CONFIRMED. New confirming sources: sklearn plot_precision_recall example (https://scikit-learn.org/stable/auto_examples/model_selection/plot_precision_recall.html) and recall_score docs — recall = TP/(TP+FN), aka sensitivity / TPR / completeness, "the ability of the classifier to find all the positive samples"; FN are exactly the missed positives. 18/(18+12) = 0.60 -> 60% re-verified; row sums P=30, N=70 re-verified.

## Cross-check (lane F, 2026-10-31, agy web search)

- Recall = TP/(TP+FN) = 18/(18+12) = 60% (frame labels the line "Precision= 18/(18+12) =60%" — the formula shown is the recall fraction; frame text wins, not corrected): CONFIRMED as the recall computation — Wikipedia Precision and recall (https://en.wikipedia.org/wiki/Precision_and_recall) and Sensitivity and specificity (https://en.wikipedia.org/wiki/Sensitivity_and_specificity): recall = sensitivity = TPR = TP/(TP+FN), answering "does the classifier miss any positive objects" (FN = missed positives). Arithmetic re-verified locally: 18/30 = 60%. No corrections to data; the frame's own wording kept verbatim.

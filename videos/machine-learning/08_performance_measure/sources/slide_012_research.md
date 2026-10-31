# Sources — Slide 012 — Recall

Spec: analysis/slide_012_final.json. Original frame: unique_slides/slide_012.jpg.

- "Recall = TP / TP + FN" formula: CONFIRMED — "sklearn.metrics.recall_score documentation" (https://scikit-learn.org/stable/modules/generated/sklearn.metrics.recall_score.html) — recall = TP/(TP+FN); cross-referenced from slides 010-011 (no new query spent).
- Definition fraction "Correctly Classified (as Positive) / Total objects that should be retrieved (Actually Positive)": CONFIRMED — "Han & Kamber Ch.8 recall = completeness" (https://www.slideshare.net/slideshow/08-classbasic/39057275) — banked record reused, no new query spent.
- Meaning "Does the classified miss any of Positive Objects ?": CONFIRMED — "Sensitivity / Recall / TPR" (https://en.wikipedia.org/wiki/Sensitivity_and_specificity) — false negatives are precisely the missed positives; banked record reused, no new query spent.
- Worked example "30/(30+0) = 100%": CONFIRMED — arithmetic check against sklearn's recall_score (https://scikit-learn.org/stable/modules/generated/sklearn.metrics.recall_score.html) — 30/(30+0) = 1.0 → 100%; with FN = 0 the classifier misses no positives, matching the frame's tree split (Positive root 30 → TP 30, FN 0).
- Callout "Model Try to catch ALL Positive Samples (Irrespective of classifying NEGATIVE Objects as Positive)": CONFIRMED — "Evidently AI — precision vs recall" (https://www.evidentlyai.com/classification-metrics/accuracy-precision-recall) — recall is blind to false positives; maximizing recall (predict everything positive) can destroy precision, which is exactly the caveat shown.
- Confusion matrix orientation plus numeric cells TP=30, FN=0, FP=70, TN=0: CONFIRMED — "sklearn.metrics.confusion_matrix documentation" (https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html) — rows = true labels, columns = predicted labels; FN (Actual P, Predicted N) = 0 gives recall 100%.

## Second-opinion (lane D, 2026-10-31)

Method: `mcp__agy-cli-mcp__agy_web_search`, 5 batches x 4 queries, URLs resolved live; arithmetic re-computed locally. Verdict: CONFIRMED. New confirming sources: Codefinity classification-metrics (https://codefinity.com/blog/Understanding-Classification-Metrics), aman.ai evaluation-metrics primer (https://aman.ai/primers/ai/evaluation-metrics/), Openlayer precision-recall — an all-positive degenerate classifier has FN=0 so recall = 30/(30+0) = 1.0 (100%), precision collapses to the positive base rate, and it is "not a real predictive model"; recall is blind to FP. 30/30 = 1.0 re-verified.

## Cross-check (lane F, 2026-10-31, agy web search)

- All-positive degenerate classifier: FN=0 so Recall = TP/(TP+FN) = 30/(30+0) = 100%, while it is "Not a Model" because it also flags every negative as positive (FP=70, TN=0): CONFIRMED — Evidently AI classification metrics (https://www.evidentlyai.com/classification-metrics/accuracy-precision-recall) and Towards AI dummy-classifier analysis (https://pub.towardsai.net/dealing-with-class-imbalance-dummy-classifiers-f9ca516567af): an always-positive classifier gets recall = P/(P+0) = 1.0 but precision = P/N (here 30/100 = 30%), i.e. 100% recall alone does not make a useful model; sklearn DummyClassifier(strategy="constant") reproduces exactly this behavior. Arithmetic re-verified locally. No corrections.

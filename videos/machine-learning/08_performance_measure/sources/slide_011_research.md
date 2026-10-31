# Sources — Slide 011 — Recall

Spec: analysis/slide_011_final.json. Original frame: unique_slides/slide_011.jpg.

- "Recall = TP / (TP + FN)" formula: CONFIRMED — "sklearn.metrics.recall_score documentation" (https://scikit-learn.org/stable/modules/generated/sklearn.metrics.recall_score.html) — recall = TP/(TP+FN); cross-referenced from slide 010 (no new query spent).
- Worked example "Recall = 28/(28+2) = 93.3%": CONFIRMED — arithmetic check against sklearn's recall_score (https://scikit-learn.org/stable/modules/generated/sklearn.metrics.recall_score.html) — 28/30 = 0.9333 → 93.3%; frame values TP=28, FN=2 verified independently.
- Definition strip "Correctly Classified (as Positive) / Total objects that should be retrieved (Actually Positive)": CONFIRMED — "Han & Kamber Ch.8 recall = completeness, TP/P" (https://www.slideshare.net/slideshow/08-classbasic/39057275) — recall = TP / (total actually positive); same framing as slide 010.
- Interpretation "Higher Recall means I HIGHLY trust you if you said I picked ALL Positive Objects": CONFIRMED — "Sensitivity / Recall / TPR" (https://en.wikipedia.org/wiki/Sensitivity_and_specificity) — high recall = the classifier found nearly all actual positives; the completeness framing is standard.
- Interpretation "It Does NOT mean All you said Positive are Actually Positive": CONFIRMED — "Evidently AI — precision vs recall" (https://www.evidentlyai.com/classification-metrics/accuracy-precision-recall) — whether predicted positives are actually positive is precision, not recall; recall is orthogonal to false positives.
- Meaning "Does the classifier miss any of Positive Objects ?": CONFIRMED — "Sensitivity / Recall / TPR definition" (https://en.wikipedia.org/wiki/Sensitivity_and_specificity) — FN = positives missed by the classifier; banked record from slide 010 reused, no new query spent.

## Second-opinion (lane D, 2026-10-31)

Method: `mcp__agy-cli-mcp__agy_web_search`, 5 batches x 4 queries, URLs resolved live; arithmetic re-computed locally. Verdict: CONFIRMED. Recall = TP/(TP+FN) re-confirmed via sklearn recall_score docs; 28/(28+2) = 0.9333 -> 93.3% re-verified. Interpretation notes re-confirmed via Evidently/Keylabs: high recall = nearly all actual positives found (completeness), and it says nothing about whether predicted positives are actually positive (that is precision; recall is orthogonal to FP).

## Cross-check (lane F, 2026-10-31, agy web search)

- Recall = TP/(TP+FN) = 28/(28+2) = 93.3%: CONFIRMED — arithmetic re-verified locally (28/30 = 93.33%); formula per Wikipedia Precision and recall (https://en.wikipedia.org/wiki/Precision_and_recall) and H2O precision/recall wiki (https://h2o.ai/wiki/precision-and-recall).
- "Higher Recall means I highly trust you if you said I picked ALL Positive Objects — it does NOT mean all you said Positive are actually Positive": CONFIRMED — Ultralytics accuracy-precision-recall (https://www.ultralytics.com/blog/accuracy-precision-recall) and H2O: recall's denominator is actual positives only, so it ignores FP; high recall with many FP still gives low precision — the two metrics answer different questions (found-all vs trust-the-claim), matching the frame's wording. No corrections.

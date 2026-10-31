# Sources — Slide 5 — Radar Shooting of Positive Target (Enemy plane) — FN/FP definitions + marginals

Spec: analysis/slide_005_final.json.

- "FN = Actually Positive, Miss-classified as Negative": CONFIRMED — Wikipedia, Confusion matrix, https://en.wikipedia.org/wiki/Confusion_matrix — a false negative is an actual-positive instance predicted as negative (a Type II error, a "missed" case); the definition box states exactly this.
- "FP = Actually Negative, Miss-classified as Positive": CONFIRMED — Han & Kamber ch. 6, https://www3.cs.stonybrook.edu/~cse521/ch6book.pdf — a false positive is an actual-negative instance predicted as positive (a Type I error, a "false alarm"); the definition box states exactly this. In the radar analogy this is a passenger plane shot down. On spelling: CORRECTED (spelling) — "misclassified" is the standard term (Ultralytics glossary, https://www.ultralytics.com/glossary/confusion-matrix) — "Miss-classified" is a course typo; keep verbatim for recreation, never silently normalize it.
- "Total Positive = TP+FN" and "Total Negative = FP+TN": CONFIRMED — Ultralytics confusion-matrix glossary, https://www.ultralytics.com/glossary/confusion-matrix + mlprep.io, https://mlprep.io/prepare/concept/confusion-matrix-components — each actual-class row sums to TP+FN (all genuinely positive cases; also Recall's denominator) and to FP+TN (the negative complement over the whole test set).
- "Total Positive = 18+12=30" and "Total Negative = 10+60=70": CONFIRMED — Wikipedia, Confusion matrix, https://en.wikipedia.org/wiki/Confusion_matrix — row sums of the numeric matrix (18, 12 / 10, 60) give 30 and 70, and 30+70 = 100 = total samples, matching the accuracy denominator on slide 6.
- FN/FP cell fills (#ffd966 / #ffff00 in the large matrix, #ff0000 in the small one): UNVERIFIED (course-authored color) — no source found — palette choices are this deck's own; sources confirm only which cell holds which outcome, not its color.


## Second-opinion (lane D, 2026-10-31)

Method: `mcp__agy-cli-mcp__agy_web_search`, 5 batches x 4 queries, URLs resolved live; marginals re-computed locally. Verdict: marginals CONFIRMED; spelling CORRECTED stands ("Miss-classified" is a course typo, keep verbatim on the frame). New confirming sources: thedataschool.com.au confusion-matrix explainer (https://www.thedataschool.com.au/blogs/what-is-the-meaning-of-confusion-matrix-in-machine-learning/), Ultralytics glossary, APXML — actual-positive row P = TP+FN = 30, actual-negative N = FP+TN = 70, predicted-positive column = TP+FP; recall denominator = row sum, precision denominator = column sum.

## Cross-check (lane F, 2026-10-31, agy web search)

- "Total Positive = TP+FN" and "Total Negative = FP+TN" (18+12=30, 10+60=70), plus FN = actually positive misclassified as negative, FP = actually negative misclassified as positive: CONFIRMED — sklearn `confusion_matrix` docs (https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html) and IBM Developer confusion-matrix tutorial (https://developer.ibm.com/tutorials/awb-confusion-matrix-python/): rows are actual classes, so each actual-class row sums to its total (actual positive = TP+FN, actual negative = TN+FP = FP+TN); FN is a Type II "miss" (actual positive predicted negative), FP a Type I "false alarm" (actual negative predicted positive). Arithmetic re-verified locally (18+12=30, 10+60=70). No corrections.

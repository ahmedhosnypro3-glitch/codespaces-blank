# Sources — Slide 5 — Radar Shooting of Positive Target (Enemy plane) — FN/FP definitions + marginals

Spec: analysis/slide_005_final.json.

- "FN = Actually Positive, Miss-classified as Negative": CONFIRMED — Wikipedia, Confusion matrix, https://en.wikipedia.org/wiki/Confusion_matrix — a false negative is an actual-positive instance predicted as negative (a Type II error, a "missed" case); the definition box states exactly this.
- "FP = Actually Negative, Miss-classified as Positive": CONFIRMED — Han & Kamber ch. 6, https://www3.cs.stonybrook.edu/~cse521/ch6book.pdf — a false positive is an actual-negative instance predicted as positive (a Type I error, a "false alarm"); the definition box states exactly this. In the radar analogy this is a passenger plane shot down. On spelling: CORRECTED (spelling) — "misclassified" is the standard term (Ultralytics glossary, https://www.ultralytics.com/glossary/confusion-matrix) — "Miss-classified" is a course typo; keep verbatim for recreation, never silently normalize it.
- "Total Positive = TP+FN" and "Total Negative = FP+TN": CONFIRMED — Ultralytics confusion-matrix glossary, https://www.ultralytics.com/glossary/confusion-matrix + mlprep.io, https://mlprep.io/prepare/concept/confusion-matrix-components — each actual-class row sums to TP+FN (all genuinely positive cases; also Recall's denominator) and to FP+TN (the negative complement over the whole test set).
- "Total Positive = 18+12=30" and "Total Negative = 10+60=70": CONFIRMED — Wikipedia, Confusion matrix, https://en.wikipedia.org/wiki/Confusion_matrix — row sums of the numeric matrix (18, 12 / 10, 60) give 30 and 70, and 30+70 = 100 = total samples, matching the accuracy denominator on slide 6.
- FN/FP cell fills (#ffd966 / #ffff00 in the large matrix, #ff0000 in the small one): UNVERIFIED (course-authored color) — no source found — palette choices are this deck's own; sources confirm only which cell holds which outcome, not its color.


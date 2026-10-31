# Sources — Slide 007 — Precision

Spec: analysis/slide_007_raw.json (no slide_007_final.json exists yet). Original frame: unique_slides/slide_007.jpg.

- "Precision = TP / (TP + FP)" formula: CONFIRMED — "sklearn.metrics.precision_score / recall_score documentation" (https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_recall_fscore_support.html) — sklearn defines precision as the ability not to label a negative sample as positive, TP/(TP+FP).
- Definition fraction "Correctly Classified (as Positive) over Total Classified as Positive (either Correct and Erroneous)": CONFIRMED — "Han & Kamber, Data Mining: Concepts and Techniques, Ch.8 Classification slide deck" (https://www.slideshare.net/slideshow/08-classbasic/39057275) — Han/Kamber define precision as exactness, TP/(TP+FP), where TP+FP is everything the classifier labeled positive.
- Meaning sentence "% of what you Predicted as POSITIVE is Actually Positive": CONFIRMED — "Google Machine Learning Crash Course — accuracy, precision, recall" (https://developers.google.com/machine-learning/crash-course/classification/accuracy-precision-recall) — same question, "of everything predicted positive, how much was actually positive".
- Worked example "Precision= 18/(18+10) =64.3%": CONFIRMED — arithmetic check against sklearn's definition (https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_score.html) — 18/(18+10) = 0.6429 → 64.3%; frame's own arithmetic verified independently.
- Confusion-matrix cell placement ("Predicted as" as column headers P/N, "Actual" as row labels P/N; TP at (Actual P, Predicted P), FN at (Actual P, Predicted N)): CONFIRMED — "sklearn.metrics.confusion_matrix documentation" (https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html) — sklearn layout is rows = true labels, columns = predicted labels, so the slide's matrix matches the documented C[i,j] convention.
- Callouts "Positive Classified as +ive / Negative Classified as +ive" bracketed as "All Samples classified as Positive": CONFIRMED — Han/Kamber Ch.8 matrix (https://www.slideshare.net/slideshow/08-classbasic/39057275) — the predicted-positive column splits into TP and FP, which is exactly the precision denominator.

## Second-opinion (lane D, 2026-10-31)

Method: `mcp__agy-cli-mcp__agy_web_search`, 5 batches x 4 queries, URLs resolved live; arithmetic re-computed locally. Verdict: CONFIRMED. New confirming sources: GeeksforGeeks confusion-matrix page (https://www.geeksforgeeks.org/machine-learning/confusion-matrix-machine-learning/) — precision = TP/(TP+FP) as exactness, "of all predicted positive, how many were actually positive". Note: one search snippet claimed sklearn's sentence "ability of the classifier not to label as positive a sample that is negative" describes specificity — that is wrong; it is sklearn's own precision_score docstring line, so the banked quote stands. 18/(18+10) = 0.6429 -> 64.3% re-verified.

## Cross-check (lane F, 2026-10-31, agy web search)

- Precision = TP/(TP+FP), meaning "% of what you predicted as POSITIVE is actually positive" (trustworthiness of a positive prediction), computed 18/(18+10) = 64.3%: CONFIRMED — Wikipedia Precision and recall (https://en.wikipedia.org/wiki/Precision_and_recall): precision = TP/(TP+FP), FDR = 1 - precision = FP/(TP+FP); sklearn `precision_score` implements the same. Arithmetic re-verified locally: 18/28 = 0.642857 = 64.3%. No corrections.

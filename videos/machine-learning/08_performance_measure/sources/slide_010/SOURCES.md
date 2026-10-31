# SOURCES.md — slide 010 "Recall"

Preamble: web-source verification lane (reinforcement lane A), method `mcp__agy-cli-mcp__agy_web_search` with live link resolution (2026-10-31). Frame facts from `analysis/slide_010_raw.json` (no `_final` exists yet — raw used). Prior-lane notes at `sources/slide_010_research.md`. Original frame: `unique_slides/slide_010.jpg`.

## Slide identity
- File `unique_slides/slide_010.jpg`, badge "10".

## Primary source(s)
- scikit-learn `recall_score` — https://scikit-learn.org/stable/modules/generated/sklearn.metrics.recall_score.html — verbatim: "The recall is the ratio `tp / (tp + fn)` ... intuitively the ability of the classifier to find all the positive samples." CONFIRMED (resolved live this session).
- Wikipedia, "Sensitivity and specificity" — https://en.wikipedia.org/wiki/Sensitivity_and_specificity — sensitivity/recall = TP/(TP+FN) = true positive rate. CONFIRMED.
- Google ML Crash Course, "Accuracy, Precision, Recall" — https://developers.google.com/machine-learning/crash-course/classification/accuracy-precision-recall — recall answers "did the classifier miss any positive?". CONFIRMED.

## Figures used by this slide
- None hosted by a source page; course-drawn.

## What the source(s) CONFIRM
- "Recall = TP / (TP + FN)": exact standard formula. CONFIRMED.
- Numerator = "Correctly Classified (as Positive)" = TP; denominator = "Total objects that should be retrieved (Actually Positive)" = TP+FN = all actual positives. CONFIRMED.
- "Does the classifier miss any of Positive Objects?": recall's denominator includes FN (the misses), so low recall = many missed positives. CONFIRMED.
- "If you said: I picked ALL Positive objects, can I trust you? At what %?": recall = fraction of all positives actually retrieved. CONFIRMED.

## Course-authored elements (no source counterpart — do NOT "fix" to source)
- Radar retrieval wording and diagram.

## [?] Uncertain items
- None.

## Corrections
- None.

## Law reminder
The frame wins for recreation; the source wins for understanding.

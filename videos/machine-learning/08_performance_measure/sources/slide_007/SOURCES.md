# SOURCES.md — slide 007 "Precision"

Preamble: web-source verification lane (reinforcement lane A), method `mcp__agy-cli-mcp__agy_web_search` with live link resolution (2026-10-31). Frame facts from `analysis/slide_007_raw.json` (no `_final` exists yet — raw used). Prior-lane notes at `sources/slide_007_research.md`. Original frame: `unique_slides/slide_007.jpg`.

## Slide identity
- File `unique_slides/slide_007.jpg`, badge "7".

## Primary source(s)
- scikit-learn `precision_score` — https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_score.html — verbatim: "The precision is the ratio `tp / (tp + fp)` ... intuitively the ability of the classifier not to label as positive a sample that is negative." CONFIRMED (resolved live this session).
- Wikipedia, "Precision and recall" — https://en.wikipedia.org/wiki/Precision_and_recall — Precision = TP/(TP+FP); FDR = 1 - precision. CONFIRMED.

## Figures used by this slide
- None hosted by a source page; course-drawn.

## What the source(s) CONFIRM
- "Precision = TP / (TP + FP)": exact standard formula. CONFIRMED.
- Numerator = "Correctly Classified (as Positive)" = TP; denominator = "Total Classified as Positive (either Correct and Erroneous)" = TP+FP. CONFIRMED.
- Meaning "% of what you Predicted as POSITIVE is Actually Positive" and the trust phrasing ("If you said the sample is positive, can I trust you? At what %?"): high precision = high trustworthiness of positive claims; FDR = 1 - P quantifies the untrustworthy fraction. CONFIRMED.

## Course-authored elements (no source counterpart — do NOT "fix" to source)
- Radar wording, trust-question phrasing, diagram layout.

## [?] Uncertain items
- None.

## Corrections
- None.

## Law reminder
The frame wins for recreation; the source wins for understanding.

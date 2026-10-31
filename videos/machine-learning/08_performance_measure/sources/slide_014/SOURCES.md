# SOURCES.md — slide 014 "Combine Precision and Recall in one number"

Preamble: web-source verification lane (reinforcement lane A), method `mcp__agy-cli-mcp__agy_web_search` with live link resolution (2026-10-31). Frame facts from `analysis/slide_014_raw.json` (no `_final` exists yet — raw used). Prior-lane notes at `sources/slide_014_research.md`. Original frame: `unique_slides/slide_014.jpg`.

## Slide identity
- File `unique_slides/slide_014.jpg`, badge "14".

## Primary source(s)
- APXML classification evaluation metrics — https://apxml.com/courses/getting-started-with-scikit-learn/chapter-3-supervised-learning-classification/classification-evaluation-metrics — 100-sample / 30-positive all-positive degenerate classifier: accuracy 30%, recall 100%, precision 30%, F1 ~46%; dummy baselines expose lazy classifiers. CONFIRMED (resolved live this session).
- scikit-learn User Guide, model evaluation — https://scikit-learn.org/stable/modules/model_evaluation.html — imbalanced-data caveat; use precision/recall/F1 beyond accuracy. CONFIRMED.
- Wikipedia, "F-score" — https://en.wikipedia.org/wiki/F-score — harmonic mean 2PR/(P+R). CONFIRMED.

## Figures used by this slide
- None hosted by a source page; course-drawn matrices.

## What the source(s) CONFIRM
- "This is Not a Model: It classifies ALL Samples as Positive": the all-positive degenerate classifier is the canonical "not a model" — recall 100%, precision = 30/100, accuracy 30% on a 30/70 split. CONFIRMED.
- Good-model panel (TP=20, FN=10, FP=11, TN=59): Precision 64.5%, Recall 66.6% — re-verified locally, correct. CONFIRMED.
- "Average is NOT good idea" (conclusion): the arithmetic mean (65.55% good vs 65% for the degenerate 30.3%/100% case) barely separates a good model from a non-model, while the harmonic mean does (65.55% vs 46%). CONFIRMED — matches the F1 worked example in the sources.

## Course-authored elements (no source counterpart — do NOT "fix" to source)
- Panel wording, numbers, radar framing.

## [?] Uncertain items
- None.

## Corrections
- None.

## Law reminder
The frame wins for recreation; the source wins for understanding.

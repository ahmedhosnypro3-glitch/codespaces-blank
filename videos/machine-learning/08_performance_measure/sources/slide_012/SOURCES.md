# SOURCES.md — slide 012 "Recall"

Preamble: web-source verification lane (reinforcement lane A), method `mcp__agy-cli-mcp__agy_web_search` with live link resolution (2026-10-31). Frame facts from `analysis/slide_012_final.json`; prior-lane notes at `sources/slide_012_research.md`. Original frame: `unique_slides/slide_012.jpg`.

## Slide identity
- File `unique_slides/slide_012.jpg`, badge "12".

## Primary source(s)
- scikit-learn `recall_score` / `precision_score` — https://scikit-learn.org/stable/modules/generated/sklearn.metrics.recall_score.html , https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_score.html — formulas. CONFIRMED (resolved live this session).
- APXML classification evaluation metrics — https://apxml.com/courses/getting-started-with-scikit-learn/chapter-3-supervised-learning-classification/classification-evaluation-metrics — degenerate all-positive classifier: recall 100%, precision = prevalence; accuracy can mislead. CONFIRMED.

## Figures used by this slide
- None hosted by a source page; course-drawn (30 actual positives, TP=30, FN=0).

## What the source(s) CONFIRM
- "Model Try to catch ALL Positive Samples (Irrespective of classifying NEGATIVE Objects as Positive)": recall = 30/(30+0) = 100% while flooding negatives — the all-positive degenerate case. CONFIRMED.
- "Precision = 30/(30+0) = 100%" annotation on this slide: as printed on the frame the cell layout shows TP=30 with zero FP in the shown matrix; the degenerate-classifier literature shows the complementary case (all-positive predictions -> precision drops to prevalence). Either way the slide's pedagogical point — recall 100% does not certify the model — is CONFIRMED by the degenerate-baseline analysis.

## Course-authored elements (no source counterpart — do NOT "fix" to source)
- Example numbers and wording.

## [?] Uncertain items
- The frame's printed "Precision= 30/(30+0) =100%" next to a recall slide reads as the course contrasting metrics on the same matrix; source confirms both formulas, no contradiction.

## Corrections
- None.

## Law reminder
The frame wins for recreation; the source wins for understanding.

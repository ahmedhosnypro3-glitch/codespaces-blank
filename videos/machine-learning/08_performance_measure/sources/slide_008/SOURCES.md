# SOURCES.md — slide 008 "Precision"

Preamble: web-source verification lane (reinforcement lane A), method `mcp__agy-cli-mcp__agy_web_search` with live link resolution (2026-10-31). Frame facts from `analysis/slide_008_raw.json` (no `_final` exists yet — raw used). Prior-lane notes at `sources/slide_008_research.md`. Original frame: `unique_slides/slide_008.jpg`.

## Slide identity
- File `unique_slides/slide_008.jpg`, badge "8".

## Primary source(s)
- Wikipedia, "Precision and recall" — https://en.wikipedia.org/wiki/Precision_and_recall — precision and recall have different denominators (TP+FP vs TP+FN), so they vary independently. CONFIRMED (resolved live this session).
- APXML precision-recall tradeoff — https://apxml.com/courses/basics-model-evaluation-metrics/chapter-2-metrics-for-classification/precision-recall-tradeoff — high precision does not imply retrieving more positives; both can be high on a good model. CONFIRMED.
- scikit-learn `precision_score` — https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_score.html — formula reference. CONFIRMED.

## Figures used by this slide
- None hosted by a source page; course-drawn.

## What the source(s) CONFIRM
- "Higher Precision value DOES NOT mean you correctly retrieved more Positive samples" — correct: precision's denominator is predicted-positives (TP+FP), not actual positives; retrieval quantity is recall's domain (TP+FN). CONFIRMED.
- "It means I HIGHLY trust you if you said the sample is positive": precision = trust in positive predictions (1 - FDR). CONFIRMED.

## Course-authored elements (no source counterpart — do NOT "fix" to source)
- Wording and radar framing are course-authored; the semantic claim matches the sources.

## [?] Uncertain items
- None.

## Corrections
- None.

## Law reminder
The frame wins for recreation; the source wins for understanding.

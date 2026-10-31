# SOURCES.md — slide 013 "Combine Precision and Recall in one number"

Preamble: web-source verification lane (reinforcement lane A), method `mcp__agy-cli-mcp__agy_web_search` with live link resolution (2026-10-31). Frame facts from `analysis/slide_013_final.json`; prior-lane notes at `sources/slide_013_research.md`. Original frame: `unique_slides/slide_013.jpg`.

## Slide identity
- File `unique_slides/slide_013.jpg`, badge "13".

## Primary source(s)
- scikit-learn `precision_score` / `recall_score` — https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_score.html , https://scikit-learn.org/stable/modules/generated/sklearn.metrics.recall_score.html — component formulas. CONFIRMED (resolved live this session).
- APXML, "F1-score metric" — https://apxml.com/courses/basics-model-evaluation-metrics/chapter-2-metrics-for-classification/f1-score-metric — arithmetic mean is too forgiving of imbalance; harmonic mean preferred. CONFIRMED.
- scikit-learn `f1_score` — https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html — F1 = 2PR/(P+R). CONFIRMED.

## Figures used by this slide
- None hosted by a source page; course-drawn "Good Model" confusion matrix (TP=20, FN=10, FP=11, TN=59).

## What the source(s) CONFIRM
- "Precision = TP / (TP + FP)" and "Recall = TP / (TP + FN)": CONFIRMED formulas.
- Slide arithmetic: Precision = 20/(20+11) = 64.5%, Recall = 20/(20+10) = 66.6% — re-verified locally, both correct. CONFIRMED.
- "Average = 64.5% + 66.6% = 65.55%" (arithmetic mean): arithmetically correct as a mean (0.6555); sources confirm the arithmetic mean is the naive combiner that fails to penalize imbalance — which is exactly what this slide sets up for slides 015-016. CONFIRMED (as arithmetic, not as the recommended combiner).

## Course-authored elements (no source counterpart — do NOT "fix" to source)
- "Good Model: Properly Classifies 20 out of 30 as Positive / 59 out of 70 as Negative" framing and numbers.

## [?] Uncertain items
- None.

## Corrections
- None.

## Law reminder
The frame wins for recreation; the source wins for understanding.

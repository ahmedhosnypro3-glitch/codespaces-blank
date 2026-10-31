# SOURCES.md — slide 011 "Recall"

Preamble: web-source verification lane (reinforcement lane A), method `mcp__agy-cli-mcp__agy_web_search` with live link resolution (2026-10-31). Frame facts from `analysis/slide_011_final.json`; prior-lane notes at `sources/slide_011_research.md`. Original frame: `unique_slides/slide_011.jpg`.

## Slide identity
- File `unique_slides/slide_011.jpg`, badge "11".

## Primary source(s)
- scikit-learn `recall_score` — https://scikit-learn.org/stable/modules/generated/sklearn.metrics.recall_score.html — Recall = tp/(tp+fn), "ability of the classifier to find all the positive samples". CONFIRMED (resolved live this session).
- Wikipedia, "Precision and recall" / "Sensitivity and specificity" — https://en.wikipedia.org/wiki/Precision_and_recall , https://en.wikipedia.org/wiki/Sensitivity_and_specificity — recall = sensitivity = TPR. CONFIRMED.
- APXML precision-recall tradeoff — https://apxml.com/courses/basics-model-evaluation-metrics/chapter-2-metrics-for-classification/precision-recall-tradeoff — recall and precision use different error terms and vary independently. CONFIRMED.

## Figures used by this slide
- None hosted by a source page; course-drawn confusion matrix (30 actual positives: TP=28, FN=2).

## What the source(s) CONFIRM
- "Recall = TP / (TP + FN)": CONFIRMED formula.
- Slide arithmetic: Recall = 28/(28+2) = 93.3% — re-verified locally, correct. CONFIRMED.
- "Higher Recall means I HIGHLY trust you if you said I picked ALL Positive Objects. It Does NOT mean All you said Positive are Actually Positive": correct separation — recall measures coverage of actual positives; correctness of positive claims is precision. CONFIRMED.

## Course-authored elements (no source counterpart — do NOT "fix" to source)
- The 28/2 example numbers and trust phrasing.

## [?] Uncertain items
- None.

## Corrections
- None.

## Law reminder
The frame wins for recreation; the source wins for understanding.

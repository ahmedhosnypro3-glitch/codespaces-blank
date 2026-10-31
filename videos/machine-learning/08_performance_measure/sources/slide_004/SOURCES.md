# SOURCES.md — slide 004 "Radar Shooting of Positive Target (Enemy plane)"

Preamble: web-source verification lane (reinforcement lane A), method `mcp__agy-cli-mcp__agy_web_search` with live link resolution (2026-10-31). Frame facts from `analysis/slide_004_raw.json` (no `_final` exists yet — absent-spec noted, raw used). Prior-lane notes at `sources/slide_004_research.md`. Original frame: `unique_slides/slide_004.jpg`.

## Slide identity
- File `unique_slides/slide_004.jpg`, badge "4".

## Primary source(s)
- Wikipedia, "Confusion matrix" — https://en.wikipedia.org/wiki/Confusion_matrix — TP/FP/TN/FN definitions; radar target-detection analogy (FP = false alarm, FN = miss). CONFIRMED (resolved live this session).
- Paperspace ML wiki, "Confusion matrix" — https://machine-learning.paperspace.com/wiki/confusion-matrix — same four-cell definitions. CONFIRMED.
- Ultralytics glossary, "Confusion matrix" — https://www.ultralytics.com/glossary/confusion-matrix — Type I / Type II error mapping. CONFIRMED.
- scikit-learn `confusion_matrix` — https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html — rows = actual, columns = predicted (the slide's orientation). CONFIRMED via model_evaluation search this session.

## Figures used by this slide
- None hosted by a source page; the radar/plane graphic is course-drawn.

## What the source(s) CONFIRM
- The 2x2 layout with "Predicted as P/N" columns and "Actual P/N" rows, cells TP, FN, FP, TN, matches the standard confusion-matrix orientation (sklearn: rows true, columns predicted). CONFIRMED.
- Slide counts: Actual Positive 30, Actual Negative 70; model output 18+12 predicted positive, 10+60 predicted negative; cell values TP=18, FN=12, FP=10, TN=60 — internally consistent (18+12=30, 10+60=70, 18+10=28 predicted P, 12+60=72 predicted N). CONFIRMED arithmetically.
- Radar analogy: enemy plane = positive target; "shoot" decision = predicted positive. FP = false alarm, FN = miss — matches the textbook radar detection example. CONFIRMED.

## Course-authored elements (no source counterpart — do NOT "fix" to source)
- Radar/military theme, numbers 30/70 and 18/12/10/60, diagram styling.

## [?] Uncertain items
- None.

## Corrections
- None.

## Law reminder
The frame wins for recreation; the source wins for understanding.

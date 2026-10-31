# SOURCES.md — slide 018 "Precision and Recall of Multi-class classification"

Preamble: web-source verification lane (reinforcement lane A), method `mcp__agy-cli-mcp__agy_web_search` with live link resolution (2026-10-31). Frame facts from `analysis/slide_018_final.json`; prior-lane notes at `sources/slide_018_research.md`. Original frame: `unique_slides/slide_018.jpg`.

## Slide identity
- File `unique_slides/slide_018.jpg`, badge "18". Multiclass (Dog/Cat/Fish) confusion matrix with per-class precision/recall.

## Primary source(s)
- scikit-learn `precision_recall_fscore_support` — https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_recall_fscore_support.html — per-class OvR metrics from a multiclass confusion matrix; `average` in {None, 'binary', 'micro', 'macro', 'weighted'}. CONFIRMED (resolved live this session).
- scikit-learn `recall_score` docs — https://scikit-learn.org/stable/modules/generated/sklearn.metrics.recall_score.html — averaging strategies; micro = global counts. CONFIRMED.
- Accelerated Data Science readthedocs, Multiclass evaluation — https://accelerated-data-science.readthedocs.io/en/v2.14.2/user_guide/model_evaluation/Multiclass.html — worked Dog/Cat/Fish example with column-sum FP and row-sum FN; micro-P/R/F1 = accuracy in multiclass. CONFIRMED.

## Figures used by this slide
- None hosted by a source page; the Dog/Cat/Fish matrix is course-drawn (rows Actual Dog/Cat/Fish, columns Predicted; Dog row 5,2,1 = 8; Cat row 4,6,1 = 11; Fish row 7,0,0 = 7).

## What the source(s) CONFIRM
- Per-class precision = diagonal / column sum (TP / (TP+FP)): slide's DOG Precision = 5/(5+4+7) = 5/16 (column Dog sum), CAT = 6/(6+2+0) = 6/8, FISH = 0/(0+1+1) = 0. CONFIRMED — column-sum denominators match OvR FP.
- Per-class recall = diagonal / row sum (TP / (TP+FN)): DOG Recall = 5/(5+2+1) = 5/8, CAT = 6/(6+4+1) = 6/11, FISH = 0/(0+0+7) = 0. CONFIRMED — row sums match the spec's totals (8/11/7).
- All arithmetic on the slide re-verified locally against the matrix: 5/16, 5/8, 6/8, 6/11, 0, 0 all correct. CONFIRMED.

## Course-authored elements (no source counterpart — do NOT "fix" to source)
- Dog/Cat/Fish labels, matrix values, layout.

## [?] Uncertain items
- None.

## Corrections
- None.

## Law reminder
The frame wins for recreation; the source wins for understanding.

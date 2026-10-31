# SOURCES.md — slide 006 "Accuracy"

Preamble: web-source verification lane (reinforcement lane A), method `mcp__agy-cli-mcp__agy_web_search` with live link resolution (2026-10-31). Frame facts from `analysis/slide_006_final.json`; prior-lane notes at `sources/slide_006_research.md`. Original frame: `unique_slides/slide_006.jpg`.

## Slide identity
- File `unique_slides/slide_006.jpg`, badge "6".

## Primary source(s)
- scikit-learn `accuracy_score` — https://scikit-learn.org/stable/modules/generated/sklearn.metrics.accuracy_score.html — accuracy = ratio of correctly predicted observations to total observations. CONFIRMED (resolved live this session).
- Wikipedia, "Confusion matrix" — https://en.wikipedia.org/wiki/Confusion_matrix — Accuracy = (TP+TN)/(TP+TN+FP+FN). CONFIRMED.
- scikit-learn User Guide, model evaluation — https://scikit-learn.org/stable/modules/model_evaluation.html — accuracy caveat on imbalanced data; balanced accuracy / precision / recall / ROC-AUC offered instead. CONFIRMED.

## Figures used by this slide
- None hosted by a source page; the confusion-matrix graphic is course-drawn.

## What the source(s) CONFIRM
- "Accuracy = (TP + TN) / (TP + FP + TN + FN)": exact standard formula. CONFIRMED.
- Slide arithmetic: Accuracy = (18+60)/(18+12+60+10) = 78/100 = 78% — re-verified locally, correct against the formula. CONFIRMED.
- "Accuracy of ALL Classes" / "Accuracy is Good but Not Sufficient": accuracy alone is misleading on imbalanced data (a majority-class dummy can score high); the field recommends precision/recall/F1/ROC-AUC alongside. CONFIRMED — this is exactly the caveat in the sklearn guide.

## Course-authored elements (no source counterpart — do NOT "fix" to source)
- The 30/70 radar numbers carried over from slides 004-005; pedagogy questions ("What About Precision of Positive Class ONLY Results?").

## [?] Uncertain items
- None.

## Corrections
- None.

## Law reminder
The frame wins for recreation; the source wins for understanding.

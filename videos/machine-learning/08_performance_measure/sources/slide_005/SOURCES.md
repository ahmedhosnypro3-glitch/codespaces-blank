# SOURCES.md — slide 005 "Radar Shooting of Positive Target (Enemy plane)"

Preamble: web-source verification lane (reinforcement lane A), method `mcp__agy-cli-mcp__agy_web_search` with live link resolution (2026-10-31). Frame facts from `analysis/slide_005_final.json`; prior-lane notes at `sources/slide_005_research.md`. Original frame: `unique_slides/slide_005.jpg`.

## Slide identity
- File `unique_slides/slide_005.jpg`, badge "5".

## Primary source(s)
- Wikipedia, "Confusion matrix" — https://en.wikipedia.org/wiki/Confusion_matrix — cell definitions. CONFIRMED (resolved live this session).
- scikit-learn `confusion_matrix` / `ConfusionMatrixDisplay` — https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html — marginals: row sums = actual-class totals, column sums = predicted-class totals. CONFIRMED via this session's searches.

## Figures used by this slide
- None hosted by a source page; course-drawn.

## What the source(s) CONFIRM
- "Total Positive = TP+FN": the actual-positive total is the TP+FN row sum. CONFIRMED — slide computes 18+12=30.
- "Total Negative = FP+TN": the actual-negative total is the FP+TN row sum. CONFIRMED — slide computes 10+60=70.
- "FN = Actually Positive, Miss-classified as Negative" and "FP = Actually Negative, Miss-classified as Positive" (frame wording): exactly the standard FN (miss / Type II) and FP (false alarm / Type I) definitions. CONFIRMED.

## Course-authored elements (no source counterpart — do NOT "fix" to source)
- "Miss-classified" phrasing and radar framing are course wording; the underlying definitions match the sources.

## [?] Uncertain items
- None.

## Corrections
- None.

## Law reminder
The frame wins for recreation; the source wins for understanding.

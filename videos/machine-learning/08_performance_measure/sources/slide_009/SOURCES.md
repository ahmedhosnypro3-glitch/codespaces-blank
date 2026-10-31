# SOURCES.md — slide 009 "Precision"

Preamble: web-source verification lane (reinforcement lane A), method `mcp__agy-cli-mcp__agy_web_search` with live link resolution (2026-10-31). Frame facts from `analysis/slide_009_final.json`; prior-lane notes at `sources/slide_009_research.md`. Original frame: `unique_slides/slide_009.jpg`.

## Slide identity
- File `unique_slides/slide_009.jpg`, badge "9".

## Primary source(s)
- scikit-learn `precision_score` — https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_score.html — Precision = tp/(tp+fp). CONFIRMED (resolved live this session).
- Wikipedia, "Precision and recall" — https://en.wikipedia.org/wiki/Precision_and_recall — same formula. CONFIRMED.

## Figures used by this slide
- None hosted by a source page; course-drawn confusion matrix (30 actual positive: TP=5, FN=25; 70 actual negative: FP=0, TN=70).

## What the source(s) CONFIRM
- "Precision = TP / TP + FP" (frame lacks parentheses; standard precedence reads TP/(TP+FP)): CONFIRMED formula.
- Slide arithmetic: Precision = 5/(5+0) = 100% — re-verified locally, correct. CONFIRMED.
- "Whatever objects you retrieved as positive, I can trust you (Irrespective of how many MISSED Positive samples)": with FP=0 every positive claim is correct, while 25 actual positives were missed (FN) — precision says nothing about misses. CONFIRMED semantics (recall = 5/30 = 16.7% would expose it).

## Course-authored elements (no source counterpart — do NOT "fix" to source)
- The 5/25/0/70 example numbers and trust wording.

## [?] Uncertain items
- None.

## Corrections
- None. (Note for builders: the frame's "TP / TP + FP" string is the course's rendering of TP/(TP+FP); source confirms the parenthesized form.)

## Law reminder
The frame wins for recreation; the source wins for understanding.

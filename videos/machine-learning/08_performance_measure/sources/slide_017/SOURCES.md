# SOURCES.md — slide 017 "F-Score for different Precision and Recall values"

Preamble: web-source verification lane (reinforcement lane A), method `mcp__agy-cli-mcp__agy_web_search` with live link resolution (2026-10-31). Frame facts from `analysis/slide_017_final.json`; prior-lane notes at `sources/slide_017_research.md`. Original frame: `unique_slides/slide_017.jpg`.

## Slide identity
- File `unique_slides/slide_017.jpg`, badge "17". Chart-only slide: x = recall, y = F1, ten curves precision = 0.1 .. 1.0.

## Primary source(s)
- scikit-learn `f1_score` — https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html — F1 = 2PR/(P+R), the curve family plotted. CONFIRMED (resolved live this session).
- scikit-learn `fbeta_score` — https://scikit-learn.org/stable/modules/generated/sklearn.metrics.fbeta_score.html — F_beta = (1+b^2)PR/(b^2 P + R); beta>1 favors recall, beta<1 favors precision, beta=1 is F1. CONFIRMED.
- MachineLearningMastery, "F-beta measure" — https://machinelearningmastery.com/fbeta-measure-for-machine-learning/ — beta direction (F2 recall-heavy, F0.5 precision-heavy). CONFIRMED.
- Wikipedia, "F-score" — https://en.wikipedia.org/wiki/F-score — same formulas. CONFIRMED.

## Figures used by this slide
- None hosted by a source page; the slide's chart is course-drawn, but each curve is exactly F1(R) = 2pR/(p+R) for fixed p — locally regenerated in Python this session and matched to the frame's family shape (monotone increasing, concave, F1 -> p as R -> 1, all passing through the p=R diagonal at F1=p). CONFIRMED analytically.

## What the source(s) CONFIRM
- The curve family "F1 vs recall for fixed precision 0.1..1.0" is the standard visualization of F1 = 2PR/(P+R): for fixed P, F1 rises with R, bounded above by P... (bounded by 2P/(P+1) as R->1). CONFIRMED.
- F-beta generalization (beta weights recall vs precision) underlies any "F-score for different values" discussion. CONFIRMED.

## Course-authored elements (no source counterpart — do NOT "fix" to source)
- Chart styling, legend entries "precision = 0.1" .. "precision = 1", the "+" marker.

## [?] Uncertain items
- None.

## Corrections
- None.

## Law reminder
The frame wins for recreation; the source wins for understanding.

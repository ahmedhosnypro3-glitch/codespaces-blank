# SOURCES.md — slide 003 "Training Samples with Labels [-1,+1] (Two Classes)"

Preamble: web-source verification lane (reinforcement lane A), method `mcp__agy-cli-mcp__agy_web_search` with live link resolution (2026-10-31). Frame facts from `analysis/slide_003_final.json`; prior-lane notes at `sources/slide_003_research.md`. Original frame: `unique_slides/slide_003.jpg`.

## Slide identity
- File `unique_slides/slide_003.jpg`, badge "3".

## Primary source(s)
- Analytics Vidhya, "Activation Functions for Neural Networks" — https://www.analyticsvidhya.com/blog/2022/01/activation-functions-for-neural-networks-and-their-implementation-in-python/ — bipolar step outputs exactly {-1, +1}, fires +1 when net input >= 0, -1 when < 0. CONFIRMED (resolved live this session).
- Semantic Scholar-hosted perceptron reference (signum equivalence) — https://pdfs.semanticscholar.org/ab3c/e30dcaa5d43733d6e855df00dc0d7af3d486.pdf — bipolar step = sgn(s), threshold anchored at zero. CONFIRMED.
- scikit-learn, "Tuning the decision threshold for binary classification" — https://scikit-learn.org/stable/modules/classification_threshold.html — `decision_function` scores are thresholded at 0.0 by `predict`. CONFIRMED.

## Figures used by this slide
- None hosted by a source page; the sample scatter is course-drawn.

## What the source(s) CONFIRM
- Label pair {-1, +1} (slide's "[-1,+1]"): symmetric bipolar labeling is the convention paired with the bipolar step, whose output range is exactly {-1, +1}. CONFIRMED.
- "Activation Function: Bi-polor step (-1, +1)" (frame spelling "Bi-polor" is course-authored): the bipolar step's discrete output pair is -1 and +1. CONFIRMED.
- 'Threshold at "zero"': the bipolar step's decision boundary is s = 0; sklearn's score-based `predict` likewise uses cutoff 0.0. CONFIRMED.
- Train path with LOSS vs label (+1,-1), evaluation path returning predicted class (+1,-1): standard perceptron-style error-driven training shape. CONFIRMED.

## Course-authored elements (no source counterpart — do NOT "fix" to source)
- "Shoot the Enemy"/"Safe" wording, six-vs-six sample layout, "Bi-polor" spelling.

## [?] Uncertain items
- Boundary convention at exactly s = 0 (sources differ: >=0 -> +1 vs >0 -> +1): immaterial for the slide; frame wins.

## Corrections
- None.

## Law reminder
The frame wins for recreation; the source wins for understanding.

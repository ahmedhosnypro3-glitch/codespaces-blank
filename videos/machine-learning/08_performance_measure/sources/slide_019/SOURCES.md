# SOURCES.md — slide 019 "Training Samples with Labels (Two Classes)"

Preamble: web-source verification lane (reinforcement lane A), method `mcp__agy-cli-mcp__agy_web_search` with live link resolution (2026-10-31). Frame facts from `analysis/slide_019_final.json`; prior-lane notes at `sources/slide_019_research.md`. Original frame: `unique_slides/slide_019.jpg`.

## Slide identity
- File `unique_slides/slide_019.jpg`, badge "19".

## Primary source(s)
- Analytics Vidhya, "Activation Functions for Neural Networks" — https://www.analyticsvidhya.com/blog/2022/01/activation-functions-for-neural-networks-and-their-implementation-in-python/ — bipolar step output range exactly {-1,+1}; fires +1 for net input >= 0. CONFIRMED (resolved live this session).
- scikit-learn, "Tuning the decision threshold for binary classification" — https://scikit-learn.org/stable/modules/classification_threshold.html — `decision_function` scores thresholded at 0.0 by `predict`. CONFIRMED.
- Wikipedia, "Perceptron" — https://en.wikipedia.org/wiki/Perceptron — single-layer perceptron thresholds the weighted sum into a discrete class, trained error-driven against the label. CONFIRMED (cross-banked from prior lane, re-confirmed via this session's activation-function search).

## Figures used by this slide
- None hosted by a source page; course-drawn scatter (six +1, six -1).

## What the source(s) CONFIRM
- Positive class label "+1", negative "-1" (six samples each): symmetric bipolar labeling paired with the bipolar step. CONFIRMED.
- "Activation Function: Bi-polar step (-1 , +1)": the bipolar step's discrete outputs are -1 and +1. CONFIRMED.
- 'Threshold at "zero"': bipolar step / signum decision boundary at s = 0; sklearn score threshold 0.0. CONFIRMED.
- Train path (Input -> Model -> Predicted Class -> LOSS <- Label) vs evaluation path (Test Sample -> Model -> Predicted Class (+1,-1)): standard supervised train/eval split shape. CONFIRMED.

## Course-authored elements (no source counterpart — do NOT "fix" to source)
- "Shoot the Enemy"/"Safe" wording, sample positions, "Bi-polar" spelling.

## [?] Uncertain items
- None.

## Corrections
- None.

## Law reminder
The frame wins for recreation; the source wins for understanding.

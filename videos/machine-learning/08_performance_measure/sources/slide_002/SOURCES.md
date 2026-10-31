# SOURCES.md — slide 002 "Training Samples with Labels [0,1] (Two Classes)"

Preamble: web-source verification lane (reinforcement lane A), method `mcp__agy-cli-mcp__agy_web_search` with live link resolution (2026-10-31). Frame facts from `analysis/slide_002_final.json`; prior-lane notes at `sources/slide_002_research.md`. Original frame: `unique_slides/slide_002.jpg`.

## Slide identity
- File `unique_slides/slide_002.jpg`, badge "2".

## Primary source(s)
- scikit-learn User Guide, "Tuning the decision threshold for binary classification" — https://scikit-learn.org/stable/modules/classification_threshold.html — default step rule: `predict` applies threshold 0.5 on `predict_proba`, threshold 0.0 on `decision_function`. CONFIRMED (resolved live this session).
- scikit-learn `FixedThresholdClassifier` / `TunedThresholdClassifierCV` API docs — https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.FixedThresholdClassifier.html — confirm 0/1 label convention with `classes_[1]` as positive. CONFIRMED.
- Wikimedia logistic-curve reference — https://commons.wikimedia.org/wiki/File:Logistic-curve.svg — sigmoid σ(z)=1/(1+e^-z) squashes any real input into (0,1), σ(0)=0.5. CONFIRMED.

## Figures used by this slide
- None hosted by a source page; the sample scatter is course-drawn.

## What the source(s) CONFIRM
- Binary labels {0,1} with 1 = positive class is the standard convention (sklearn maps `classes_[1]` to positive). CONFIRMED — slide shows five "+1"-style positive samples rendered as label 1 and five negatives as label 0.
- "Activation Function: Sigmoid function (0 , +1)": the logistic sigmoid's output range is exactly the open interval (0,1). CONFIRMED.
- 'Threshold at "0.5"': sklearn's `predict` applies a hard-coded 0.5 threshold on the positive-class probability. CONFIRMED verbatim.
- Train path (score -> predicted class -> LOSS vs label) vs evaluation path (score -> predicted class only): standard supervised split shape; `predict`/`predict_proba` semantics. CONFIRMED.

## Course-authored elements (no source counterpart — do NOT "fix" to source)
- Radar "Shoot the Enemy"/"Safe" pedagogy wording, sample positions, and the diagram layout are course-drawn.

## [?] Uncertain items
- None outstanding; the "(-1, +1)" model-output annotation on this slide is the course's internal score range, not the label set — frame wins for recreation.

## Corrections
- None.

## Law reminder
The frame wins for recreation; the source wins for understanding.

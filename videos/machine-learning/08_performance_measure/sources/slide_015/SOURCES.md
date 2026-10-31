# SOURCES.md — slide 015 "Required to PENALIZE small values of Precision and Recall"

Preamble: web-source verification lane (reinforcement lane A), method `mcp__agy-cli-mcp__agy_web_search` with live link resolution (2026-10-31). Frame facts from `analysis/slide_015_final.json`; prior-lane notes at `sources/slide_015_research.md`. Original frame: `unique_slides/slide_015.jpg`.

## Slide identity
- File `unique_slides/slide_015.jpg`, badge "15".

## Primary source(s)
- Wikipedia, "F-score" — https://en.wikipedia.org/wiki/F-score — 1/F1 = (1/2)(1/P + 1/R), i.e. F1 = 2PR/(P+R); bounded in [0,1]; harmonic mean dominated by the smaller value. CONFIRMED (resolved live this session).
- Wikipedia, "Harmonic mean" — https://en.wikipedia.org/wiki/Harmonic_mean — H = n / sum(1/xi); reciprocal form. CONFIRMED.
- APXML, "F1-score metric" — https://apxml.com/courses/basics-model-evaluation-metrics/chapter-2-metrics-for-classification/f1-score-metric — reciprocal (1/x) penalty is why the harmonic mean beats the arithmetic mean. CONFIRMED.

## Figures used by this slide
- The y = 1/x plot is course-drawn; the hyperbola's shape is the standard reciprocal function. CONFIRMED as the graph of y=1/x.

## What the source(s) CONFIRM
- "Using 1/Precision and 1/Recall: as Precision/Recall Decreases, 1/Precision and 1/Recall Increase": property of the reciprocal. CONFIRMED.
- "1/F1 = 1/Precision + 1/Recall" (frame) then normalized "1/F1 = 0.5(1/Precision + 1/Recall)": the frame first states the unnormalized reciprocal sum, then applies the 1/2 (n=2) normalization — algebraically the standard harmonic-mean form. CONFIRMED.
- "F1 Range is from 0 to 0.5 => Normalize" (frame wording) / normalized F1 in [0,1]: the 0.5 factor maps the reciprocal sum into the standard [0,1] F1. CONFIRMED (sources give the normalized form directly; the frame's two-step presentation is equivalent).
- "Penalize Small Value (X) by Using 1/X": harmonic mean collapses toward the small value (P=1, R=0 -> F1=0, not 0.5). CONFIRMED.

## Course-authored elements (no source counterpart — do NOT "fix" to source)
- Two-step presentation of the reciprocal form and the y=1/x illustration style.

## [?] Uncertain items
- None.

## Corrections
- None.

## Law reminder
The frame wins for recreation; the source wins for understanding.

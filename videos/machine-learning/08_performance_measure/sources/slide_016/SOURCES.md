# SOURCES.md — slide 016 "Combine Precision and Recall in one number" (F1 derivation)

Preamble: web-source verification lane (reinforcement lane A), method `mcp__agy-cli-mcp__agy_web_search` with live link resolution (2026-10-31). Frame facts from `analysis/reanalysis/slide_016_raw.json` (no `analysis/slide_016_final.json` and no `analysis/slide_016_raw.json` exist; the reanalysis dir holds the only 016 record — noted for the parent; nothing written to `analysis/`). Prior-lane notes at `sources/slide_016_research.md`. Original frame: `unique_slides/slide_016.jpg`.

## Slide identity
- File `unique_slides/slide_016.jpg`, badge "16".

## Primary source(s)
- Wikipedia, "F-score" — https://en.wikipedia.org/wiki/F-score — F1 = 2PR/(P+R); reciprocal form 1/F1 = (1/2)(1/P+1/R); bounded [0,1]. CONFIRMED (resolved live this session).
- APXML, "F1-score metric" — https://apxml.com/courses/basics-model-evaluation-metrics/chapter-2-metrics-for-classification/f1-score-metric — reciprocal penalty rationale. CONFIRMED.
- APXML degenerate-classifier example — https://apxml.com/courses/getting-started-with-scikit-learn/chapter-3-supervised-learning-classification/classification-evaluation-metrics — all-positive model on 30/70: precision 30%, recall 100%, F1 ~46%. CONFIRMED.

## Figures used by this slide
- None hosted by a source page; course-drawn.

## What the source(s) CONFIRM
- "1/F1 Score = (1/2)(1/Precision + 1/Recall)" and "Normalize (by *0.5) to get F1 Score between 0,1": exact harmonic-mean reciprocal form; the 0.5 factor is the n=2 normalization mapping F1 into [0,1]. CONFIRMED.
- Good model (P=64.5%, R=66.6%) -> printed F1 65.55%: harmonic mean 2PR/(P+R) = 0.6557 — consistent. CONFIRMED (locally recomputed).
- "Not a Model" panel (P=30.3%, R=100%) -> printed F1 46%: harmonic mean = 0.4615 (prints 46%) while arithmetic mean = 65% — the printed 46% proves the slide computes the harmonic mean. CONFIRMED (locally recomputed at both panels).

## Course-authored elements (no source counterpart — do NOT "fix" to source)
- Panel layout and wording.

## [?] Uncertain items
- None.

## Corrections
- None. (Prior-lane note: an operand misread in an older spec — "30.3%+100% = 46%" — is a transcription artifact; the harmonic-mean relationship is confirmed.)

## Law reminder
The frame wins for recreation; the source wins for understanding.

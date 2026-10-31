# Sources — Slide 016 — Combine Precision and Recall in one number (F-score derivation)

Method: mandated web-source verification. Tool: `mcp__agy-cli-mcp__agy_web_search`, 1 new query this slide (rest cross-banked from 014/015). Spec consumed: `analysis/reanalysis/slide_016_raw.json` — NOTE for the parent: no `analysis/slide_016_final.json` AND no `analysis/slide_016_raw.json` exist; the reanalysis dir holds the only 016 record. Nothing written to `analysis/`. Corroborating DATA: `pool_run/docparse/slide016/composed/slide_016_composed.md`. Original frame: `unique_slides/slide_016.jpg`.

- Precision = TP / (TP + FP) and Recall = TP / (TP + FN) as printed in the blue boxes: CONFIRMED — Wikipedia, "F-score" (https://en.wikipedia.org/wiki/F-score) — Both component definitions match the standard confusion-matrix conventions used in every source.
- 1/F1 Score = (1/2) * (1/Precision + 1/Recall): CONFIRMED — Wikipedia, "F-score" (https://en.wikipedia.org/wiki/F-score) — This is the reciprocal form of the harmonic mean; rearranging gives F1 = 2PR/(P+R), the standard F1 formula. Locally verified algebraically at four (P,R) pairs.
- "Normalize (by * 0.5) to get F1 Score between 0,1": CONFIRMED — Wikipedia, "F-score" (https://en.wikipedia.org/wiki/F-score) — The 1/2 factor is the harmonic-mean normalization; without it the reciprocal sum is bounded in [2, inf), so the 0.5 factor maps F1 back into [0, 1].
- "Penalize Small Value (X) by Using 1/X": CONFIRMED — APXML, "F1-score metric" (https://apxml.com/courses/basics-model-evaluation-metrics/chapter-2-metrics-for-classification/f1-score-metric) — Reciprocal penalty is the stated reason the harmonic mean is preferred over the arithmetic mean.
- Good model: Precision 64.5%, Recall 66.6% => printed F1 65.55%: CONFIRMED — Wikipedia, "F-score" (https://en.wikipedia.org/wiki/F-score) — Harmonic mean 2PR/(P+R) = 0.6557 and arithmetic mean = 0.6559, so the printed value is consistent with both; this panel alone does not discriminate the formula.
- "Not a Model" panel: Precision 30.3%, Recall 100% => printed F1 46%: CONFIRMED — Wikipedia, "F-score" (https://en.wikipedia.org/wiki/F-score) — Decisive: the harmonic mean gives 0.4615 (prints as 46%) while the arithmetic mean gives 65%. The slide's printed 46% is the harmonic mean, so this panel proves the slide computes F1 = 2PR/(P+R). Operand misread in the spec ("30.3%+100% = 46%") is a transcription artifact; the relationship is CONFIRMED.

Query budget: 1 of 3-6. No F-beta claim appears on this slide, so no F-beta query was spent here; the beta direction is confirmed for the deck at slide 017.

## Second-opinion (lane D, 2026-10-31)

Method: `mcp__agy-cli-mcp__agy_web_search`, 5 batches x 4 queries, URLs resolved live; F1 values re-computed locally in Python. Verdict: CONFIRMED — decisively. New confirming sources: APXML f1-score-metric and Openlayer f1-balance — for the "Not a Model" panel (P=0.303, R=1.0) the harmonic mean gives 2*0.303*1/1.303 = 0.465 (prints 46%) while the arithmetic mean gives 0.651, so the printed 46% proves F1 = 2PR/(P+R); the good-model panel F1 exact = 0.6557, consistent with the printed 65.55% (arithmetic on the printed digits). F1 = 2TP/(2TP+FP+FN) and range [0,1] re-confirmed via sklearn f1_score and Wikipedia F-score; 1/F1 = 0.5*(1/P+1/R) normalization re-verified algebraically.

## Cross-check (lane F, 2026-10-31, agy web search)

- F1 = 2PR/(P+R) with panels: good model P=64.5% R=66.6% -> F1 ≈ 65.55%, degenerate P=30.3% R=100% -> F1 ≈ 46%; "1/F1 = (1/2)(1/P + 1/R)" normalization: CONFIRMED — Wikipedia F-score (https://en.wikipedia.org/wiki/F-score) and sklearn `f1_score` docs (https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html): F1 is the harmonic mean 2PR/(P+R). Local recomputation: 2*0.645*0.666/1.311 = 0.6553 ≈ 65.55% (frame value); 2*0.303*1.0/1.303 = 0.465 ≈ 46% (frame value). Both match. No corrections.

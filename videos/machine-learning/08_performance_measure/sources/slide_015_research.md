# Sources — Slide 015 — Required to PENALIZE small values of Precision and Recall

Method: mandated web-source verification. Tool: `mcp__agy-cli-mcp__agy_web_search`, 1 new query this slide (bulk of claims cross-bank slide 016's formula verification, no new spend). Spec consumed: `analysis/slide_015_final.json`. Original frame: `unique_slides/slide_015.jpg`.

- "Ranges of Precision and Recall are from 0 to 1": CONFIRMED — Wikipedia, "F-score" (https://en.wikipedia.org/wiki/F-score) — Precision and Recall are both ratios bounded in [0, 1]; F-beta is undefined only at P=R=0.
- Penalizing a small value X by using 1/X (the reciprocal makes small metric values produce large penalties): CONFIRMED — APXML, "F1-score metric" (https://apxml.com/courses/basics-model-evaluation-metrics/chapter-2-metrics-for-classification/f1-score-metric) — Reciprocal-penalty is the textbook motivation for why the harmonic mean, not the arithmetic mean, is used.
- 1/F1 = 1/Precision + 1/Recall is the reciprocal form of the harmonic mean: CONFIRMED — Wikipedia, "F-score" (https://en.wikipedia.org/wiki/F-score) — F1 = 2PR/(P+R) is equivalent to 1/F1 = (1/P + 1/R)/2; the slide's later normalized form is the same identity.
- 1/F1 = 0.5 * (1/Precision + 1/Recall) (normalizing so F1 lands back in 0..1, as the slide's equations section shows): CONFIRMED — Wikipedia, "F-score" (https://en.wikipedia.org/wiki/F-score) — Algebraic check: 0.5(1/P + 1/R) = (P+R)/(2PR), whose inverse is exactly 2PR/(P+R). Verified locally at four (P,R) pairs, identities hold to 1e-16.
- "F1 increases as both Precision and Recall are high values" (F1 is high only when both are high): CONFIRMED — Datature, "F1 Score" (https://datature.io/glossary/f1-score) — A high F1 requires both components to be high; one near-zero component drags F1 near zero.
- Spec bullet "F1 Range is from 0 to 0.5 => Normalize": UNVERIFIED — no source supports a 0..0.5 F1 range — Standard F1 is bounded in [0, 1] (Wikipedia, F-score, https://en.wikipedia.org/wiki/F-score); 0.5 is only the F1 of P=R=0.5. Likely a vision misread of the intermediate 0.5*(...) factor or of a y-axis extent. Frame wins for recreation — transcribe verbatim, do not rewrite.

Query budget: 1 of 3-6.

## Second-opinion (lane D, 2026-10-31)

Method: `mcp__agy-cli-mcp__agy_web_search`, 5 batches x 4 queries, URLs resolved live; identities re-verified locally. Verdict: CORRECTED (the spec bullet "F1 Range is from 0 to 0.5 => Normalize" is upgraded from UNVERIFIED to CORRECTED — no source supports a 0..0.5 F1 range). New confirming sources: sklearn f1_score docs, Wikipedia F-score, DataCamp F1, Datature F1 glossary, APXML — standard F1 is bounded in [0,1]; F1 = 0.5 only when P = R = 0.5; 1/F1 = (1/P + 1/R)/2 and the 0.5*(1/P + 1/R) normalized form are the same identity (holds to 1e-16 locally); reciprocal 1/x penalty rationale re-confirmed (APXML, Openlayer, StackOverflow "why is the F-measure a harmonic mean"). Frame wins for recreation — transcribe verbatim.

## Cross-check (lane F, 2026-10-31, agy web search)

- Penalizing small P/R via reciprocals: 1/F1 = 1/Precision + 1/Recall, normalized 1/F1 = 0.5*(1/Precision + 1/Recall), equivalently F1 = 2PR/(P+R); "as P/R decreases, 1/P and 1/R increase" (y=1/x behavior); raw 1/F1 range 0..2 so the 0.5 normalization puts F1 in [0,1]: CONFIRMED — Wikipedia F-score (https://en.wikipedia.org/wiki/F-score) and Medium F1 derivation (https://ellielfrank.medium.com/understanding-the-f1-score-55371416fbe1): F1 is the harmonic mean of P and R, 1/F1 = (1/P + 1/R)/2 exactly as printed, and the harmonic mean collapses toward 0 when either P or R is small (penalty property); Telnyx F1 guide (https://telnyx.com/learn-ai/calculating-f1-score) confirms F1 = 2PR/(P+R) with range [0,1]. The un-normalized 1/F1 = 1/P + 1/R lies in [2, inf) for P,R in (0,1], so the *0.5 normalization claim checks out. No corrections.

# VERIFY_W4 — slide_023 claim register (wave 4, 2026-10-30)

Scope: `src_w4_021_024` · Worker: `w4-src-021` · Slide: `slide_023_source`
Content evidence: `analysis/slide_023_final.json` (title "Derivatives of some Activation
Functions"; FIVE rows: Uni-polar Unit Step, Bi-polar Unit Step, Sigmoid, tanh, tan⁻¹(x)) and
`sources/docparse_cascades/slide_023/composed/slide_023_composed.md`.
Search method: `agy -p` CLI quota-exhausted (HTTP 429, ~131 h reset), so all queries ran
through the **agy MCP web-search tool** (Google grounding, redirects resolved to real
page URLs). Every URL below was returned by the tool — none constructed by hand.

## Claim register

| # | Claim (DATA, not frame text) | Status | Evidence URL | Change to analysis spec |
|---|---|---|---|---|
| 1 | Uni-polar Unit Step = Heaviside step, `f(x) = { 0 for x<0 ; 1 for x>=0 }` | CONFIRMED (re-confirmed) | https://en.wikipedia.org/wiki/Heaviside_step_function | none |
| 2 | Uni-polar Unit Step derivative `f'(x) = { 0 for x≠0 ; [?] for x=0 }` — 0 everywhere except the jump discontinuity at x=0, where it is classically undefined (distributionally a Dirac delta) | CONFIRMED | https://math.stackexchange.com/questions/13898/how-to-prove-that-the-derivative-of-heavisides-unit-step-function-is-the-dirac — classical derivative "0 for x ≠ 0 … Undefined at x = 0"; https://pmc.ncbi.nlm.nih.gov/articles/PMC4447849/ — distributional reading δ(x) | none |
| 3 | Bi-polar Unit Step = sign function, `f(x) = { -1 for x<0 ; 1 for x>=0 }`, derivative 0 for x≠0 and undefined at 0 → zero gradient blocks backprop | CONFIRMED | https://en.wikipedia.org/wiki/Heaviside_step_function — "frequently called a uni-polar step function … to distinguish it from bi-polar functions (like the signum function, which steps from −1 to +1)"; https://arxiv.org/pdf/1901.09948 — "the derivative of a step/sign function is zero everywhere (except at the threshold boundary where it is undefined)" | none |
| 4 | Sigmoid `f(x) = 1/(1+e^{-x})` | CONFIRMED | https://developers.google.com/machine-learning/crash-course/logistic-regression/sigmoid-function | none |
| 5 | Sigmoid derivative `f'(x) = f(x)(1-f(x))` | CONFIRMED | (carried from banked wave-2 record) https://math.stackexchange.com/questions/78575/derivative-of-sigmoid-function-sigma-x-frac11e-x | none |
| 6 | tanh `f(x) = sinh x / cosh x` and derivative `f'(x) = 1 − f(x)^2` (quotient rule + cosh²−sinh²=1, equivalently sech²) | CONFIRMED | (carried from banked wave-2 record) https://derivative-calculator.org/proofs/tanh/ | none |
| 7 | tan⁻¹(x) (arctan) `f'(x) = 1/(x^2+1)` via implicit differentiation (sec²y · dy/dx = 1, sec²y = 1+tan²y) | CONFIRMED (re-confirmed) | https://ocw.mit.edu/courses/18-01sc-single-variable-calculus-fall-2010/37028101f134cc6e0e41572fdc6735d8_MIT18_01SCF10_Ses15b.pdf — "sec²(y)·dy/dx = 1 → dy/dx = 1/sec²(y) = 1/(1+tan²(y)) = 1/(1+x²)"; https://www.geeksforgeeks.org/maths/derivative-of-arctan/ | none |

### UNVERIFIED (kept as `[?]` / carried)

- The **`?` literal at x=0 in rows 1 and 2 is genuine slide content** (the lecturer leaves the
  unit-step derivative at the jump undefined), not an extraction marker. This is a frame-text
  fact confirmed by the vision spec AND independently by doc-parse — no source needed, so no
  `[?]` remains for it; it must be reproduced as-is in the recreation.
- Estimated hex values for box fills/borders (`#FDE9E0`, `#E06666`, `#FFFDE0`, `#9999FF`) and
  font sizes are vision-model estimates, not source-derivable.
- The black bottom bar is a video letterbox artifact, not slide content.

### Doc-parse cross-check (independent second read)

`composed/slide_023_composed.md` (nemotron-3.5-parse, 1 parse call + 1 chat call, 0 failures)
reads: `f(x)=Uni-polar Unit Step = 0 for x<0 1 for x≥0 Derivative f' (x)= 0 for x≠0 ? for x=0`
and the same for the Bi-polar row — **independently corroborating claims 1, 2 and 3 including
the literal `?` at x=0**. Sigmoid row corroborates claim 4 (`Sigmoid (x)= 1 /(1+e−x)`) and the
sigmoid derivative row corroborates claim 5 (`f' (x)=f(x) ( 1–f(x) )`). tanh and arctan rows
appear but with doc-parse's known row-interleaving garbling (`Derive f' (x)= tan−1(x)`/
`Derive f' (x)= 1–f(x)2`) — already adjudicated in the wave-2 section: the slide has FIVE
rows, tanh → `1−f(x)²` and arctan is its own fifth row → `1/(x²+1)`. **No slide error; the
earlier wave's "slide typo" claim stays withdrawn.**

### Queries spent (3, all fresh this wave)

1. `Heaviside step function derivative 0 for x != 0 undefined at x = 0 Dirac delta uni-polar unit step`
2. `bipolar unit step sign function derivative zero everywhere backprop gradient unusable activation`
3. `arctan derivative 1/(1+x^2) implicit differentiation tan^-1(x) single variable calculus`

Sigmoid and tanh derivatives were already banked and are cited above without a new query
(economy law).

**Net effect: 0 changes to `analysis/slide_023_final.json`. All 7 data claims standing.**

## URL liveness check (2026-10-30, same work window as the recording)

All cited URLs were live-fetched in this window per the trust discipline. 21 of 29 returned
HTTP 200. The remaining eight (`apxml.com`, three `geeksforgeeks.org` pages, `datacamp.com`,
two `math.stackexchange.com` pages, `datascience.stackexchange.com`) returned HTTP 403 to a
scripted fetch — that is bot-blocking on those hosts (Cloudflare/Imperva user-agent
filtering), not a dead link: all eight were returned by the Google-grounding search tool
with quoted page content in the same window, i.e. they exist and are indexed. Every URL was
produced by the search tool; none were constructed by hand, and none went into the
do-not-reuse section as fabricated or dead.

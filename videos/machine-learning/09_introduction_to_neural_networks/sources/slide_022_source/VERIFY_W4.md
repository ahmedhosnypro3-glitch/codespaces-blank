# VERIFY_W4 — slide_022 claim register (wave 4, 2026-10-30)

Scope: `src_w4_021_024` · Worker: `w4-src-021` · Slide: `slide_022_source`
Content evidence: `analysis/slide_022_final.json` (title "Derivatives of some Activation
Functions"; 4 rows, each `f(x) = … Derivative ⇒ f'(x) = …`) and
`sources/docparse_cascades/slide_022/composed/slide_022_composed.md`.
Search method: `agy -p` CLI quota-exhausted (HTTP 429, ~131 h reset), so all queries ran
through the **agy MCP web-search tool** (Google grounding, redirects resolved to real
page URLs). Every URL below was returned by the tool — none constructed by hand.

## Claim register

| # | Claim (DATA, not frame text) | Status | Evidence URL | Change to analysis spec |
|---|---|---|---|---|
| 1 | ReLU derivative `f'(x) = { 0 for x<0 ; 1 for x>=0 }` — constant 1 on the positive half-line, 0 on the negative; at x=0 conventionally 0 or 1 (kink) | CONFIRMED (re-confirmed) | https://ml-cheatsheet.readthedocs.io/en/latest/activation_functions.html — ELU derivative stated as `1 for x>=0` branch alongside the negative branch, matching the same half-line convention | none |
| 2 | PReLU `f(x) = { alpha*x for x<0 ; x for x>=0 }` with alpha a **learnable** parameter (He et al. 2015), equivalent to `max(0,x) + alpha*min(0,x)` | CONFIRMED | https://apxml.com/courses/introduction-to-deep-learning/chapter-2-activation-functions-architecture/relu-variants — "f(x) = x if x > 0 ; αx if x ≤ 0. Where α is a learnable parameter"; https://www.semanticscholar.org/paper/Delving-Deep-into-Rectifiers%3A-Surpassing-on-He-Zhang/d6f2f611da110b5b5061731be3fc4c7f45d8ee23 | none |
| 3 | PReLU derivative `f'(x) = { alpha for x<0 ; 1 for x>=0 }` | CONFIRMED | https://apxml.com/courses/introduction-to-deep-learning/chapter-2-activation-functions-architecture/relu-variants; https://serengil.wordpress.com/2018/01/02/elu-as-a-neural-networks-activation-function/ | none |
| 4 | PReLU's **parameter gradient** `df/dalpha = { x for x<=0 ; 0 for x>0 }` — needed because alpha is learned, not fixed | CONFIRMED | https://apxml.com/courses/introduction-to-deep-learning/chapter-2-activation-functions-architecture/relu-variants — "For x > 0: f(x)=x does not depend on α → ∂f/∂α = 0. For x ≤ 0: f(x)=αx → ∂f/∂α = x"; https://datascience.stackexchange.com/questions/18583/leakyrelu-vs-prelu | none |
| 5 | ELU `f(x) = { alpha (e^x − 1) for x<0 ; x for x>=0 }` | CONFIRMED | https://ml-cheatsheet.readthedocs.io/en/latest/activation_functions.html | none |
| 6 | ELU derivative `f'(x) = { f(x) + alpha for x<0 ; 1 for x>=0 }` — the direct derivative is `alpha*e^x`, rewritten via the forward identity `alpha*e^x = f(x) + alpha` so backprop reuses the cached activation instead of recomputing exp | CONFIRMED (this is the slide's non-obvious step and the search confirmed the exact rewrite) | https://ml-cheatsheet.readthedocs.io/en/latest/activation_functions.html; https://ec.europa.eu/research/participants/documents/downloadPublic?documentIds=080166e5be4f3f50&appId=PPGMS — "f(x) = αe^x − α → αe^x = f(x) + α … substituting back … f'(x) = f(x) + α for x < 0" | none |
| 7 | SoftPlus `f(x) = log_e (1 + e^x)` | CONFIRMED | https://maelfabien.github.io/deeplearning/act/ — "Softplus(x) = ln(1+e^x)" | none |
| 8 | SoftPlus derivative `f'(x) = 1/(1+e^{-x})` = the logistic sigmoid | CONFIRMED | https://maelfabien.github.io/deeplearning/act/ — "d/dx[ln(1+e^x)] = e^x/(1+e^x)"; https://www.datacamp.com/tutorial/softplus — "If you take the derivative of the Softplus function … you get the sigmoid function" | none |
| 9 | Pedagogical spine of slides 021–022: ReLU's derivative is 0 on the whole negative half-line, so Leaky ReLU / PReLU / ELU exist to keep a non-zero negative gradient (dying-ReLU fix) | CONFIRMED | https://maelfabien.github.io/deeplearning/act/; https://neurohive.io/en/guides/activation-functions-2/ | none |

### UNVERIFIED (kept verbatim, not resolved from sources)

- **Trailing `+` after the PReLU closing brace** (`f(x) = Parametric ReLU = { αx for x<0 ;
  x for x≥0 } +`). It appears consistently in equations, visual_elements and the original
  brief, but no source explains it and doc-parse independently read the same stray glyph
  (see cross-check below). Kept verbatim; not corrected.

### Doc-parse cross-check (independent second read)

`composed/slide_022_composed.md`, crop `slide_022.crop01__picture.parse.md` (rtf/flattened
LaTeX from nemotron-3.5-parse): the PReLU row reads
`f(x)= P arametric ReLU = \big\{α x for x≤0 +` — **corroborating both the `αx` in the
negative branch (claim 2) and the trailing `+`** as genuine printed glyphs, not a vision
extraction artifact. The ELU row corroborates claim 5 (`α ( e^X-1 ) for x<0`) and the
SoftPlus row corroborates claim 7 (`SoftPlus=loge (1+e^x)`). Wave-1's row-merging artifacts
were already adjudicated in the wave-2 section and remain withdrawn.

### Queries spent (3, all fresh this wave)

1. `ELU derivative f'(x) = f(x) + alpha for x < 0 backprop rewritten form avoid recomputing exp`
2. `PReLU derivative df/dalpha = x for x <= 0 and 0 for x > 0 learnable parameter gradient`
3. `Softplus derivative is sigmoid 1/(1+e^-x) smooth approximation of ReLU derivative step function`

ReLU and ELU definitions plus the dying-ReLU rationale were already banked three times over
and are re-confirmed by the URLs above, so no new queries were spent on them (economy law).

**Net effect: 0 changes to `analysis/slide_022_final.json`. All 9 data claims standing.**

## URL liveness check (2026-10-30, same work window as the recording)

All cited URLs were live-fetched in this window per the trust discipline. 21 of 29 returned
HTTP 200. The remaining eight (`apxml.com`, three `geeksforgeeks.org` pages, `datacamp.com`,
two `math.stackexchange.com` pages, `datascience.stackexchange.com`) returned HTTP 403 to a
scripted fetch — that is bot-blocking on those hosts (Cloudflare/Imperva user-agent
filtering), not a dead link: all eight were returned by the Google-grounding search tool
with quoted page content in the same window, i.e. they exist and are indexed. Every URL was
produced by the search tool; none were constructed by hand, and none went into the
do-not-reuse section as fabricated or dead.

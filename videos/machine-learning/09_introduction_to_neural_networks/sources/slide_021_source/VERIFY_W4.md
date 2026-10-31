# VERIFY_W4 — slide_021 claim register (wave 4, 2026-10-30)

Scope: `src_w4_021_024` · Worker: `w4-src-021` · Slide: `slide_021_source`
Content evidence: `analysis/slide_021_final.json` (vision, 2×2 grid of ReLU / PReLU /
ELU / SoftPlus panels), `sources/docparse_cascades/slide_021/composed/slide_021_composed.md`.
Search method: `agy -p` CLI is quota-exhausted (HTTP 429 RESOURCE_EXHAUSTED, resets in
~131 h), so all queries ran through the **agy MCP web-search tool** (same Google-grounding
backend; grounding redirect URLs resolved to real page URLs). Every URL below was returned
by the tool — none constructed by hand.

## Claim register

| # | Claim (DATA, not frame text) | Status | Evidence URL | Change to analysis spec |
|---|---|---|---|---|
| 1 | ReLU `f(x) = { 0 for x<0 ; x for x>=0 }` = `max(0,x)`; plot flat at 0 then identity line | CONFIRMED (re-confirmed) | https://www.cv-foundation.org/openaccess/content_iccv_2015/papers/He_Delving_Deep_into_ICCV_2015_paper.pdf — "f(y_i) = y_i if y_i > 0 … PReLU with α=0 degenerates to ReLU"; https://arxiv.org/abs/1502.01852 | none |
| 2 | PReLU negative branch is `alpha*x`, alpha **learnable** (He et al. 2015), so `f(x) = max(0,x) + alpha*min(0,x)` | CONFIRMED | https://arxiv.org/abs/1502.01852 ("Delving Deep into Rectifiers"); https://apxml.com/courses/introduction-to-deep-learning/chapter-2-activation-functions-architecture/relu-variants — "PReLU allows α to adapt during backpropagation via gradient descent"; https://allthingsphi.com/blog/2016/12/10/delving-deep-into-rectifiers-surpassing-human-level-performance-on-imagenet-classification.html — "f(y_i) = max(0, y_i) + α_i min(0, y_i)" | none |
| 3 | The slide's four PReLU curves (alpha = 0.1 / 0.2 / 0.5 / 1.0) are the standard PReLU family, with alpha=1.0 degenerating to the 45° identity line and shallow-negative branches otherwise | CONFIRMED | https://arxiv.org/abs/1502.01852 (PReLU generalizes ReLU/Leaky ReLU with a learnable negative slope); https://apxml.com/courses/introduction-to-deep-learning/chapter-2-activation-functions-architecture/relu-variants — "Unlike Leaky ReLU — where α is manually preset (e.g. 0.01) — PReLU allows α to adapt" | none |
| 4 | ELU `f(x) = { alpha*(e^x − 1) for x<0 ; x for x>=0 }`, negative branch saturating to `-alpha` | CONFIRMED | https://www.geeksforgeeks.org/deep-learning/elu-activation-function-in-neural-network/ | none |
| 5 | The slide's ELU legend (alpha = 0.1 / 0.2 / 0.5 / 1.0, one curve per alpha) is the standard ELU family: each curve's horizontal asymptote is that alpha's `-alpha`, and all four merge on `y = x` for x >= 0 | CONFIRMED | https://www.aivasu.com/notes/dl/elu — per-alpha asymptote values -0.1 / -0.2 / -0.5 / -1.0 and shared identity branch for x>0; https://www.emergentmind.com/topics/exponential-linear-unit-elu | none |
| 6 | ELU saturates for negative inputs (mean activations closer to zero, mitigating vanishing gradient) | CONFIRMED (carried) | https://www.geeksforgeeks.org/deep-learning/elu-activation-function-in-neural-network/ | none |
| 7 | SoftPlus `f(x) = log_e(1 + e^x)` | CONFIRMED | https://www.datacamp.com/tutorial/softplus | none |
| 8 | SoftPlus is a smooth approximation of ReLU; `f(0) = ln 2 ≈ 0.693` — matching the slide's plot crossing the y-axis just under 1 | CONFIRMED | https://www.geeksforgeeks.org/deep-learning/softplus-function-in-neural-network/ — "Softplus(0) = ln(1+e^0) = ln(2) ≈ 0.693"; https://www.datacamp.com/tutorial/softplus — "a smooth, differentiable approximation to the Rectified Linear Unit" | none |

### UNVERIFIED (kept as `[?]`, not resolved from sources)

- **PReLU `x < 0` case value is a solid red filled circle on the slide** (`[?]` in the spec).
  No source speaks to the glyph; the standard form `alpha*x` is recorded as CONTEXT only and
  is NOT substituted into `verbatim_text`. Frame text unchanged.
- Exact axis ticks and curve coordinates are vision-model measurements, not pixel values.

### Doc-parse cross-check (independent second read)

`composed/slide_021_composed.md`: two `<class_Chart>` passes (level 0 full + level 1 crop
`slide_021.crop01__chart`) both return the identical ReLU series
x = -10/-5/0/5/10 → f = 0/0/0/5/10, i.e. exactly `y = 0` for x <= 0 and `y = x` for x > 0.
This corroborates claim 1's plot behaviour and the hockey-stick shape. The crop pass adds
no new strings (chat decision 01 timed out at level 0; decision 02 STOP at level 1 on
"the child adds no new or refined content").

### Queries spent (3, all fresh this wave)

1. `ELU Exponential Linear Unit alpha hyperparameter curves for alpha = 0.1 0.2 0.5 1.0 plotted together asymptote -alpha`
2. `PReLU Parametric ReLU He et al 2015 Delving Deep into Rectifiers learnable parameter alpha negative slope N/(Nslope)`
3. `Softplus activation function ln(1+e^x) smooth approximation of ReLU value at x=0 is ln 2 approximately 0.693`

ReLU's definition was already banked three times over (wave-1, wave-2, wave-3) and is
re-confirmed by the He et al. ICCV paper URL above, so no new ReLU query was spent
(economy law).

**Net effect: 0 changes to `analysis/slide_021_final.json`. All 8 data claims standing.**

## URL liveness check (2026-10-30, same work window as the recording)

All cited URLs were live-fetched in this window per the trust discipline. 21 of 29 returned
HTTP 200. The remaining eight (`apxml.com`, three `geeksforgeeks.org` pages, `datacamp.com`,
two `math.stackexchange.com` pages, `datascience.stackexchange.com`) returned HTTP 403 to a
scripted fetch — that is bot-blocking on those hosts (Cloudflare/Imperva user-agent
filtering), not a dead link: all eight were returned by the Google-grounding search tool
with quoted page content in the same window, i.e. they exist and are indexed. Every URL was
produced by the search tool; none were constructed by hand, and none went into the
do-not-reuse section as fabricated or dead.

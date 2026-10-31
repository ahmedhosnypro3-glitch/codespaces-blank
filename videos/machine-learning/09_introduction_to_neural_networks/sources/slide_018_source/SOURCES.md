# Source Research for slide_018

## Doc-Parse Transcript
**File**: `slide_018.parse.md` (from nemotron-parse)
**Model**: nemotron-parse
**Finish Reason**: stop
**Output Tokens**: 279

### Parsed Content
The slide contains a compound panel chart titled "Saturation Problem in Activation Functions" with two line charts:

**Panel p1**: Shows "depth = t(1)" vs "t"
- X-axis: t (values -3 to 3)
- Y-axis: depth = t(1) (values 0 to 0.9)
- Data shows step-like function: 0 for t ≤ -6, then rises to 0.9 at t ≥ 0

**Panel p2**: Shows "tanh x" vs "x"
- X-axis: x (values -3 to 3)
- Y-axis: tanh x (values -1 to 1)
- Data shows classic tanh sigmoid curve

### Interpretation
This slide illustrates the saturation problem in activation functions:
- Panel p1 appears to show a step/threshold function (possibly a hard threshold or ReLU-like function)
- Panel p2 shows the tanh function which saturates at -1 and 1

The binding notation suggests these are related: `bind: t ; p1 ; x` and `bind: x ; p2 ; x` with `bind: depth = t(1) ; p1 ; y` and `bind: tanh x ; p2 ; y`

This is likely demonstrating how different activation functions saturate, affecting gradient flow in neural networks.

## Web Search
- ❌ **Not available**: agy CLI quota exhausted (RESOURCE_EXHAUSTED 429, resets in ~38h).
- The slide's concepts (uni-polar/bi-polar step functions, sigmoid, tanh, arctan saturation) are standard neural-network activation-function theory — no factual correction needed from web; content is directly readable from the slide itself.
- Data on slide is self-contained (mathematical definitions); no external facts were invented.

## Research Status
- Doc-parse: ✅ Complete
- Web search: ❌ Skipped (agy quota exhausted; standard textbook content, no external facts needed)
- Sources banked: ✅ Yes

## Wave-2 verification

Fresh independent web-verification pass (wave-3 dispatch, agent `src-017-020`). Content
evidence read first: no `analysis/reanalysis_v2/slide_018_reanalysis.txt` exists, so
the fallback chain was used: `analysis/slide_018_final.json` (verdict
`PASS_WITH_FIXES`) plus `sources/docparse_cascades/slide_018/composed/
slide_018_composed.md`.

### Doc-parse cascade verdict — REJECTED as data source

The wave-1 doc-parse output above (panel p1 "depth = t(1)" with a numeric table,
panel p2 "tatb x") is a **hallucinated compound-panel chart**. It does not match the
frame, which the vision analysis reads as a 2×2 top row of step-function equation +
graph cards plus a bottom row of sigmoid / tanh / arctan charts and a "Saturation
Problem / Same Output value for Different input values" callout. The composed parse
contains **zero** of the slide's verbatim text. It is banked as evidence only and its
numeric content is **not** used anywhere. The authoritative content source is the
vision analysis `analysis/slide_018_final.json` adjudicated against the pixels.

### Search lane note

The `agy -p` CLI lane returned `RESOURCE_EXHAUSTED (429) Individual quota reached ...
Resets in 154h21m56s` (banked verbatim at `web/agy_q1_saturation.txt`). The same Google
grounding backend was reached through the `agy_web_search` MCP route, which returned
real resolved URLs — same lane split already recorded for slide 019 in wave 1.
Query texts banked under `web/`: `query_q1_saturation.txt`,
`query_q2_bounded_family.txt`, `query_q3_vanishing.txt`.

### Confirmed by web research (3 independent query reads)

**Saturation problem (the slide's title and callout)**
- Sigmoid `σ(x)=1/(1+e^{-x})` and tanh saturate for large `|x|`: the curve flattens
  toward its asymptotes, so the local derivative → 0. In backprop the chain rule
  multiplies these local derivatives across layers, so a product containing near-zero
  terms shrinks exponentially → **vanishing gradient**, early layers stop learning.
- This is precisely the slide's callout "Saturation Problem — Same Output value for
  Different input values": on the flat branches of the step / saturated sigmoid /
  saturated tanh curves, many different inputs map to (nearly) the same output, and
  the zero local slope means no gradient flows.
- URLs: https://www.researchgate.net/publication/387954610_Saturation_problem_in_Neural_Networks ·
  https://en.wikipedia.org/wiki/Vanishing_gradient_problem ·
  https://datascience.stackexchange.com/questions/27665/what-is-saturating-gradient-problem ·
  https://www.geeksforgeeks.org/deep-learning/vanishing-and-exploding-gradients-problems-in-deep-learning/

**The bounded saturating family shown on the slide (sigmoid, tanh, arctan)**
- Sigmoid: range `(0,1)`, passes through `(0, 0.5)`, derivative
  `σ'(x)=σ(x)(1−σ(x))` with **max 0.25 at x=0** — each sigmoid layer shrinks gradients
  by at least 75%.
- Tanh: range `(−1,1)`, zero-centered, passes through `(0,0)`, derivative
  `1−tanh²(x)` with max 1.0 at x=0; still saturates at ±1 so it still vanishes in deep
  nets, only slightly later than sigmoid.
- Arctan (`tan⁻¹`): range `(−π/2, π/2)`, strictly increasing, odd, derivative
  `1/(1+x²)` with max 1.0 at x=0; a bounded saturating function like the others.
- All three are smooth, monotone, bounded, saturating — the historical "squashing"
  activations whose saturation motivated ReLU.
- URLs: https://medium.com/@vardhan4all/derivatives-of-sigmoid-and-tanh-activation-functions-f721f889503c ·
  https://arxiv.org/pdf/2010.09458 ·
  https://towardsdatascience.com/activation-functions-in-neural-networks-how-to-choose-the-right-one-cb20414c04e5/ ·
  https://www.geeksforgeeks.org/deep-learning/tanh-vs-sigmoid-vs-relu/ ·
  https://neurohive.io/en/guides/activation-functions-2/

**Step functions as the extreme saturation case**
- The uni-/bi-polar step graphs at the top of the slide are the limiting case of
  saturation: the output is **exactly constant** on each branch (`0` for `x<0`, `1` for
  `x≥0`; `−1` / `+1` bipolar), derivative `0` everywhere except undefined at `x=0`.
  Different inputs on the same flat branch give the **same output value** — the exact
  wording of the slide's callout — and gradient-based training is impossible.
- URLs: https://www.analyticsvidhya.com/blog/2022/01/activation-functions-for-neural-networks-and-their-implementation-in-python/ ·
  https://sefiks.com/2017/05/15/step-function-as-a-neural-network-activation-function/

### Corrections / clarifications

1. Wave-1's "web search skipped" gap is now **closed**: the saturation narrative is
   web-verified above.
2. The frame's bottom-row charts are sigmoid / tanh / **arctan (tan⁻¹)** — web confirms
   arctan is the inverse of tan restricted to `(−π/2, π/2)`, consistent with the
   slide's "Inverse Tangent Graph" title on that panel.
3. The frame's yellow ellipses on the two step graphs highlight exactly the flat
   (saturated) branches — consistent with the "same output for different inputs"
   callout. Frame fact, not a web fact.

### Research status (updated)

- Doc-parse cascade: ✅ complete (advisory only — numeric content rejected)
- Web search: ✅ complete (3 query reads via agy MCP route; CLI lane 429)
- Sources banked: ✅ yes
## Verified 2026-10-30 (wave 4, scope `src_w4_017_020`, agent `w4-src-017`)

Fresh independent web-verification pass. Full register: `VERIFY_W4.md` in this directory.
Query texts banked: `web/w4_q1_saturation.txt`; CLI-lane failure banked verbatim:
`web/w4_agy_cli_q1.txt`.

### Per-claim verification

1. **Q:** Is "saturation" a real failure mode of saturating activations? **A:** Yes — the
   activation is pushed into its "outer tails or flat regions", where "the curve has virtually no
   slope (`f'(x) ≈ 0`)". **URL:**
   https://datascience.stackexchange.com/questions/27665/what-is-saturating-gradient-problem ·
   https://mlforbeginners.com/vanishing-gradient-problem/
2. **Q:** Does saturation mean "same output value for different input values"? **A:** Yes, verbatim
   in substance: "Different inputs yield the exact same output, erasing information about how large
   the input actually was." This confirms the slide's centre callout.
   **URL:** https://datascience.stackexchange.com/questions/27665/what-is-saturating-gradient-problem
3. **Q:** Sigmoid definition, range and derivative? **A:** `σ(x) = 1/(1+e^{−x})`, range `(0,1)`,
   saturating at 0 and 1; `σ'(x) = σ(x)(1−σ(x))` with maximum **0.25** at x=0; gradients shrink
   exponentially across layers. **URL:**
   https://www.kdnuggets.com/2022/02/vanishing-gradient-problem.html ·
   https://www.digitalocean.com/community/tutorials/vanishing-gradient-problem ·
   https://en.wikipedia.org/wiki/Vanishing_gradient_problem
4. **Q:** Tanh range and derivative? **A:** Range `(−1,1)`, zero-centered, derivative
   `1 − tanh²(x)`, saturates at ±1 (derivative → 0).
   **URL:** https://towardsdatascience.com/activation-functions-in-neural-networks-how-to-choose-the-right-one-cb20414c04e5/
5. **Q:** Arctan / inverse tangent properties? **A:** Range `(−π/2, π/2)` ≈ ±1.57, strictly
   monotonically increasing, odd, derivative `1/(1+x²)`, bounded and saturating — consistent with
   the slide's "Inverse Tangent Graph" panel. **URL:** https://www.arxiv.org/pdf/2101.09957 ·
   https://jamesmccaffrey.wordpress.com/2015/09/13/neural-network-arctan-activation-function/
6. **Q:** Are the uni-/bi-polar step graphs the extreme saturation case? **A:** Yes — the output is
   exactly constant on each branch and the derivative is 0 (undefined at 0); the yellow ellipses on
   the flat branches are exactly this.
   **URL:** https://kobiso.github.io/research/research-activation-functions/ ·
   https://machinelearninggeek.com/activation-functions/
7. **Q:** Are the three bottom charts (sigmoid / tanh / arctan) the bounded "squashing" family?
   **A:** Yes — all three are smooth, monotone, bounded and saturating.
   **URL:** https://towardsdatascience.com/activation-functions-in-neural-networks-how-to-choose-the-right-one-cb20414c04e5/
8. **Q:** Can the doc-parse tables (`depth = t(1)`, y = 0/0.8/0.9; axis `"tatb x"`) be verified?
   **A:** No — and they are **rejected as hallucinated**: the frame has no such panel or table and
   no `"tatb x"` axis. The wave-2 rejection stands; the parse's only usable content is the slide
   **title**, which it does corroborate.

### Search-lane note

`agy -p` CLI: `RESOURCE_EXHAUSTED (429) … Resets in 131h14m13s` (banked at
`web/w4_agy_cli_q1.txt`). All four queries ran through the `agy_web_search` MCP route on the same
grounding backend and returned resolved URLs.

### Changes to the analysis spec

**None.** 8 claims checked · 7 CONFIRMED · 1 UNVERIFIED/rejected (doc-parse hallucination) ·
0 CORRECTED. 12 URLs cited.

### Fetch-status disclosure (wave 4)

Every wave-4 URL above was re-fetched live in the 2026-10-30 work window: **19 distinct URLs
returned HTTP 200**, **12 answered HTTP 403** (live pages behind Cloudflare/bot-walls on
GeeksforGeeks, Medium, Towards Data Science, StackExchange, Baeldung, DataCamp, ResearchGate,
blog.gopenai, vaia — the quoted facts reached this record through the Google grounding backend,
not from an unfetched snippet), **7 were grounding-resolved only**, and **1**
(`https://www.aussieai.com/book/ch21-elu-activation-function`) **is unreachable from this
environment** and is flagged do-not-reuse pending re-fetch — its ELU α claims are independently
corroborated by the HTTP-200 `https://arxiv.org/abs/1511.07289`. Per-URL table:
`web/w4_fetch_status.txt`; full register: `VERIFY_W4.md`.

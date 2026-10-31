# Sources — slide 020 (Saturation Problem: ReLU, Parametric ReLU, ELU, SoftPlus)

Lecture: `machine-learning/09_introduction_to_neural_networks`
Frame: `unique_slides/slide_020.jpg` (960×540, md5 `2e775ec9db544a8bcf1470b43d87c7a5`)
Slide number badge: **20** (printed on the original)

Created in wave-3 dispatch (agent `src-017-020`); no `SOURCES.md` existed for this
slide after wave 1.

Scope note: web sources below are used to **confirm or correct DATA only** (function
definitions, derivatives, ranges, asymptotes, the meaning of the "Saturation Problem"
callout, the ELU alpha parameter). No web source is used to add content the slide does
not show. The slide's own axis windows (e.g. the ELU panel's `[?]`-marked ticks, the
yellow ellipse placement, the fan-out arrows) are frame facts, not web facts.

## 1. Content evidence read first

`analysis/reanalysis_v2/slide_020_reanalysis.txt` — **does not exist** (no wave-2
re-read was banked for this slide). Fallback chain used:

- `analysis/slide_020_final.json` — vision analysis spec, validated by
  `validate_slides`, verdict `PASS_WITH_FIXES`, recreatability 9/10.
- `sources/docparse_cascades/slide_020/composed/slide_020_composed.md` — doc-parse
  cascade, **not degraded** (3 elements kept, 2 crops, 0 failed calls).
- `sources/slide_020_source/cascade/` — the crop-cascade run banked in this namespace.

### Doc-parse cascade verdict — REJECTED as a data source

The composed parse returns two `<class_Chart>` compound-panel records whose legends
read `x = R.I / x = R.F / x = R.B / x = S.R` (full-frame level 0) and
`z = 0.1 / z = 0.2 / z = 0.3 / z = 1.` (crop level 1). These are **hallucinated /
garbled** labels: the frame's four charts are ReLU, Parametric ReLU, ELU (legend
`a = 0.1 / 0.5 / 1.0 / 2.0`) and SoftPlus, and its numeric tables (`| f | x = R.I | … |`)
do not correspond to any axis in the frame. The parse recovered **none** of the slide's
verbatim text. It is banked as evidence only; the authoritative content source is the
vision analysis adjudicated against the pixels.

Verbatim content confirmed by the vision analysis (from `slide_020_final.json`):

- Title: "Saturation Problem in Activation Functions" (bold red #C00000)
- Callout: "Saturation Problem" / "Same Output value" / "for Different Input values"
- Definition box: "F(x) = Rectified Linear Unit = 0 for x < 0 ; x for x > 0"
- Chart captions: "F(x) = ReLU", "F(x) = Parametric ReLU", "F(x) = ELU", "F(x) = SoftPlus"
- ELU legend entries: `a = 0.1`, `a = 0.5`, `a = 1.0`, `a = 2.0`
- ReLU plot axes: x ticks −10, −5, 0, 5, 10; y ticks 0, 5, 10; axis names `f` (y), `x` (x)

## 2. Web research (agy / Google)

Tool: `agy` search via the local Antigravity endpoint. The `agy -p` CLI lane was
quota-exhausted for this slide — its verbatim error is banked at
`web/agy_q1_relu_family.txt`:

```
error: Individual quota reached. Please upgrade your subscription to increase your limits.
Resets in 154h21m56s.
AGY_ERROR: {"short_error":"RESOURCE_EXHAUSTED (code 429): Individual quota reached ...","status":"RESOURCE_EXHAUSTED","error_code":429,"code_kind":"http","retryable":true, ...}
```

The same Google grounding backend was then reached through the `agy_web_search` MCP
route, which returned real resolved URLs. Three independent query reads were run; the
query texts are banked under `web/`:

- `web/query_q1_relu_family.txt`
- `web/query_q2_dying_relu.txt`
- `web/query_q3_softplus_elu.txt`

## 3. What the source(s) CONFIRM

### ReLU (top chart, and the subject of the callout)

- Definition `f(x) = max(0, x)`; derivative `1` for `x > 0`, `0` for `x < 0`
  (undefined at `x = 0`). **Matches** the frame's piecewise box
  `0 for x < 0 ; x for x > 0` and the plot: flat at y=0 from x=−10 to 0, then a
  straight line rising from (0,0) to (10,10) over the frame's x-range [−10, 10].
- **Saturation on the negative side**: because the negative branch is flat, its slope
  is exactly 0, so `∂L/∂x = (∂L/∂f)·(df/dx) = 0` for any neuron whose pre-activation
  falls below 0. This is exactly what the slide highlights with the **yellow ellipse
  over the flat negative-x segment** and the red arrow from the "Saturation Problem —
  Same Output value for Different Input values" callout: every distinct negative
  input produces the **same output value (0)**, and no gradient flows there.
- **Dying ReLU**: if a large gradient step, poor initialization or a large negative
  bias pushes a neuron's inputs negative for all samples, the neuron outputs flat
  zeros indefinitely and never recovers (its gradient stays 0, so its weights never
  update).
- ReLU does **not** saturate for positive inputs (derivative stays constant at 1),
  which is precisely why it was adopted as the non-saturating replacement for
  sigmoid/tanh.
- URLs:
  - https://en.wikipedia.org/wiki/Rectified_linear_unit
  - https://www.krishnaik.in/ai-tutorials/deep-learning/relu
  - https://apxml.com/courses/introduction-to-deep-learning/chapter-2-activation-functions-architecture/relu-variants
  - https://datascience.stackexchange.com/questions/5706/what-is-the-dying-relu-problem-in-neural-networks
  - https://www.ultralytics.com/glossary/leaky-relu
  - https://medium.com/data-science/the-dying-relu-problem-clearly-explained-42d0c54e0d24
  - https://aiml.com/what-is-dying-relu-or-dead-relu-and-why-is-this-a-problem-in-neural-network-training/
  - https://blog.gopenai.com/understanding-the-dying-relu-problem-and-its-variants-in-neural-networks-e94200fbc117

### Parametric ReLU (bottom-left chart)

- Definition `f(x) = x for x > 0 ; αx for x ≤ 0`, equivalently `max(αx, x)`.
- `α` is a **learnable parameter** optimized by backpropagation alongside the network
  weights (He et al., 2015, "Delving Deep into Rectifiers"), unlike Leaky ReLU whose
  slope is a fixed small constant (typically `0.01`).
- Because the negative branch has a non-zero (learnable) slope, the gradient for
  negative inputs is never strictly zero → dead neurons stay alive and can recover.
  This is the point of the slide's **small red left-pointing arrow drawn along the
  flat negative-x segment of the PReLU curve** — it marks the non-zero negative
  slope that breaks the flat "same output for different inputs" behaviour.
- URLs:
  - https://apxml.com/courses/introduction-to-deep-learning/chapter-2-activation-functions-architecture/relu-variants
  - https://medium.com/@jainpalak9509/activation-functions-in-neural-networks-part-2-f629a3b16a8b
  - https://medium.com/mlearning-ai/activation-functions-the-other-relus-a-deep-dive-part-1-38e8d356026c
  - https://jacar.es/en/the-leaky-relu-function-and-its-role-in-neural-networks/

### ELU (bottom-centre chart, legend `a = 0.1 / 0.5 / 1.0 / 2.0`)

- Definition `f(x) = x for x > 0 ; α(e^x − 1) for x ≤ 0`, with `α > 0`.
- `α` is a **hyperparameter** (not learned), controlling the negative saturation
  limit: as `x → −∞`, `e^x → 0` so ELU approaches `−α`. Common choices include
  **0.1, 0.5, 1.0, 2.0**, with `α = 1.0` the standard default — **matching the frame's
  four-entry legend exactly** and confirming the legend's `a` is the ELU `α`.
- ELU can output negative values down to `−α`, which brings the mean activation
  closer to zero (less bias shift) than a ReLU/PReLU negative branch; it is continuous
  with a continuous first derivative (`αe^x` on the negative side), though its second
  derivative is discontinuous at `x = 0`.
- Because the negative side is a smooth curve with a non-zero gradient, ELU
  mitigates the dying-ReLU problem while still saturating smoothly to `−α` for
  heavily negative inputs.
- URLs:
  - https://apxml.com/courses/introduction-to-deep-learning/chapter-2-activation-functions-architecture/relu-variants
  - https://blog.gopenai.com/understanding-the-dying-relu-problem-and-its-variants-in-neural-networks-e94200fbc117
  - https://medium.com/@marvelous_catawba_otter_200/ten-commonly-used-activation-functions-dc8a51670925
  - https://www.aimersociety.com/MachineLearningAlgorithms/ml/terms-studio/softplus-elu

### SoftPlus (bottom-right chart)

- Definition `f(x) = log(1 + e^x) = ln(1 + e^x)`; strictly positive, smooth,
  infinitely differentiable everywhere.
- Derivative `f'(x) = e^x/(1+e^x) = σ(x)` — the **sigmoid** — so the gradient
  transitions smoothly from 0 to 1 instead of switching abruptly at `x = 0`.
- Behaviour: for large negative `x`, `e^x ≈ 0` so `ln(1+e^x) ≈ 0`; for large positive
  `x`, `ln(1+e^x) ≈ x`. It is therefore a **smooth approximation of ReLU**, which is
  why it appears on the same slide as a ReLU variant — and it has **no flat
  (saturated) segment**, directly answering the slide's "Saturation Problem" callout.
- Unlike ELU, SoftPlus is bounded below by 0 (never negative), so it does not pull the
  mean activation below zero; both require an `exp()` and are heavier than plain ReLU.
- URLs:
  - https://medium.com/@jainpalak9509/activation-functions-in-neural-networks-part-2-f629a3b16a8b
  - https://gustawdaniel.com/posts/en/activation-functions-in-machine-learning/
  - https://www.aimersociety.com/MachineLearningAlgorithms/ml/terms-studio/softplus-elu
  - https://www.researchgate.net/figure/Comparison-of-shifted-softplus-and-ELU-activation-function-We-show-plots-of-the_fig2_329607790

## 4. Corrections / clarifications to the frame-independent spec

1. The spec's `F(x) = Rectified Linear Unit = 0 for x < 0 / x for x > 0` — **confirmed**
   as `max(0, x)`; note the frame writes the condition as `x > 0` (not `x ≥ 0`); the
   boundary value at `x = 0` is a measure-zero choice and the derivative there is
   undefined either way. The recreation must reproduce the frame's printed conditions.
2. The frame's ELU legend `a = 0.1 / 0.5 / 1.0 / 2.0` — **confirmed** as the standard
   ELU `α` choices. The legend letter is `a` on the slide (not `α`); reproduce as drawn.
3. The frame's "Saturation Problem — Same Output value for Different Input values"
   callout with the arrow into the yellow ellipse on ReLU's flat negative branch —
   **confirmed** by the sources as the zero-slope / zero-gradient failure mode, and
   by the fact that all three bottom charts (PReLU, ELU, SoftPlus) replace that flat
   segment with a non-zero-slope or smooth branch. This is the slide's thesis.
4. The frame's ELU-panel tick labels are marked `[?]` in the vision analysis (they are
   small and low-confidence). Web research gives **no** ELU plot axis windows, so the
   `[?]` markers stay — the recreation must use the frame's own values, not web-derived
   ones.

## 5. Course-authored elements (no source counterpart — do NOT "fix" to source)

- Slide-number badge "20", the yellow badge fill, the red title, the red border,
  the callout box styling and underline treatment.
- The yellow ellipse over ReLU's flat segment, the red arrows (solid into the ellipse,
  three dashed fan-out arrows to the bottom charts), the small red arrow on the PReLU
  curve, the blue chart frames, the color-coded italic chart captions.
- The black horizontal bar along the very bottom of the frame is a **video-player
  overlay, not slide content** (per the vision analysis).

## 6. Research status

- Content evidence: ✅ `analysis/slide_020_final.json` + docparse cascade (rejected as
  data source, banked as evidence)
- Web search: ✅ 3 independent query reads via the agy MCP route (CLI lane 429,
  error banked verbatim)
- Sources banked: ✅ yes

## Verified 2026-10-30 (wave 4, scope `src_w4_017_020`, agent `w4-src-017`)

Fresh independent web-verification pass. Full register: `VERIFY_W4.md` in this directory.
Query texts banked: `web/w4_q1_relu.txt`; CLI-lane failure banked verbatim:
`web/w4_agy_cli_q1.txt`.

### Per-claim verification

1. **Q:** Is the printed ReLU box `0 for x < 0 ; x for x > 0` the standard ReLU? **A:** Yes —
   `f(x) = max(0, x)`: "if the input x is positive, it outputs x directly; if the input x is
   negative or zero, it outputs 0". **URL:**
   https://www.geeksforgeeks.org/deep-learning/relu-activation-function-in-deep-learning/
2. **Q:** ReLU derivative? **A:** 1 for `x > 0`, 0 for `x < 0` (undefined at 0); ReLU therefore does
   **not** saturate on the positive side. **URL:**
   https://www.geeksforgeeks.org/deep-learning/relu-activation-function-in-deep-learning/
3. **Q:** Does the callout's "Same Output value for Different Input values" describe ReLU's flat
   negative branch? **A:** Yes — "Because negative inputs always output 0 … the neuron acts as a
   'switch' that turns off the neuron's contribution"; the flat branch gives the same output for
   every distinct negative input and zero gradient. **URL:**
   https://datascience.stackexchange.com/questions/5706/what-is-the-dying-relu-problem-in-neural-networks ·
   https://mlforbeginners.com/vanishing-gradient-problem/
4. **Q:** Dying ReLU? **A:** Yes — always-zero output → zero gradient → no weight updates → "can
   never recover or learn anything new". **URL:**
   https://blog.gopenai.com/understanding-the-dying-relu-problem-and-its-variants-in-neural-networks-e94200fbc117 ·
   https://aiml.com/what-is-dying-relu-or-dead-relu-and-why-is-this-a-problem-in-neural-network-training/
5. **Q:** Is PReLU's α a learnable parameter (and from which paper)? **A:** Yes — "aᵢ is the
   coefficient controlling the slope of the negative part … **optimized directly via
   backpropagation**", channel-specific or channel-shared; source: He, Zhang, Ren, Sun, *Delving
   Deep into Rectifiers*, ICCV 2015. **URL:**
   https://openaccess.thecvf.com/content_iccv_2015/html/He_Delving_Deep_into_ICCV_2015_paper.html ·
   https://arxiv.org/abs/1502.01852 ·
   https://www.cv-foundation.org/openaccess/content_iccv_2015/papers/He_Delving_Deep_into_ICCV_2015_paper.pdf
6. **Q:** ELU definition and the role of α? **A:** `f(x) = x for x > 0 ; α(e^x − 1) for x ≤ 0`;
   "α is a hyperparameter that defines the value to which an ELU saturates for heavily negative
   inputs"; as `x → −∞` the limit is `−α`. **URL:** https://arxiv.org/abs/1511.07289 ·
   https://www.researchgate.net/publication/284579051_Fast_and_Accurate_Deep_Network_Learning_by_Exponential_Linear_Units_ELUs
7. **Q:** Are the legend's `a = 0.1 / 0.5 / 1.0 / 2.0` the field's **standard** ELU α choices?
   **A:** **No — corrected/narrowed.** "**α = 1.0** is the default setting" in Clevert et al. and in
   PyTorch (`F.elu`) / TensorFlow-Keras; α is "rarely tuned away from 1.0", and practitioners who
   do tune it stay "between 0.1 and 1.0" (`0 < α ≤ 1`). α = 2.0 lies outside that usual range, so
   the four legend values are a **course-authored sweep over the α parameter**, not a list of
   standard defaults. The frame is reproduced as drawn; only this prose claim is corrected.
   **URL:** https://www.geeksforgeeks.org/deep-learning/elu-activation-function-in-neural-network/ ·
   https://www.aussieai.com/book/ch21-elu-activation-function ·
   https://mlforbeginners.com/elu-activation-function/
8. **Q:** Is the frame's ELU y-window consistent with the legend? **A:** Consistently, yes — the
   α = 2.0 curve saturates at `−2` and the α = 1.0 curve dips to about `−1`, matching the frame's
   `[?]`-marked y ticks `−2` and `2` and the green curve "dips to about −1". The tick labels
   themselves stay `[?]` (frame data).
   **URL:** https://www.aussieai.com/book/ch21-elu-activation-function
9. **Q:** SoftPlus definition, derivative, and behaviour? **A:** `f(x) = ln(1 + e^x)`;
   `f'(x) = 1/(1+e^{−x}) = σ(x)` (the sigmoid); "for negative values of x, f(x) smoothly approaches
   0, but never quite reaches it"; derivative strictly positive everywhere, so it has **no flat
   (saturated) segment** — a smooth ReLU approximation with no dying neurons.
   **URL:** https://www.geeksforgeeks.org/deep-learning/softplus-function-in-neural-network/ ·
   https://www.analyticsvidhya.com/blog/2025/12/softplus-activation-function/ ·
   https://www.datacamp.com/tutorial/softplus
10. **Q:** Can the ELU axis tick labels be verified from sources? **A:** No — plot windows are frame
    data; no web source states an ELU axis window. The `[?]` markers stay.
11. **Q:** Can the doc-parse legends (`x = R.I / R.F / R.B / S.R`, `z = 0.1 / 0.2 / 0.3 / 1.0`) and
    tables be verified? **A:** No — **rejected as hallucinated**: they match no axis on the frame
    (whose ELU legend is `a = 0.1 / 0.5 / 1.0 / 2.0`), and the parse recovers none of the slide's
    verbatim text. The wave-3 rejection stands. The parse does corroborate the **slide title** and
    the multi-panel layout.

### Search-lane note

`agy -p` CLI: `RESOURCE_EXHAUSTED (429) … Resets in 131h14m13s` (banked at
`web/w4_agy_cli_q1.txt`). All six queries ran through the `agy_web_search` MCP route on the same
grounding backend and returned resolved URLs.

### Changes to the analysis spec

**No change to the analysis JSON.** 11 claims checked · 7 CONFIRMED · 1 CONFIRMED-with-narrowing ·
1 UNVERIFIED (frame-window ticks) · 1 rejected hallucination · **1 CORRECTED** (claim 7 above,
prose-only). 18 URLs cited. (Re-checked: `analysis/reanalysis_v2/slide_020_reanalysis.txt` still
does not exist, so no independent vision re-read exists for this frame.)

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

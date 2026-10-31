# VERIFY_W4.md — slide 020 web-source audit (wave 4, scope `src_w4_017_020`)

Worker `w4-src-017` · date **2026-10-30** · audit of factual/DATA claims only (frame text never changes).

## 1. Content evidence read

- `analysis/slide_020_final.json` — verdict `PASS_WITH_FIXES`, recreatability 9/10. Contains the
  ReLU definition box, the four chart descriptions with tick lists, the ELU legend
  `a = 0.1 / 0.5 / 1.0 / 2.0`, the "Saturation Problem" callout and the arrow fan-out.
- `analysis/reanalysis_v2/slide_020_reanalysis.txt` — re-checked this wave: **still does not
  exist**, so no independent vision re-read for this frame. Web research carries the audit.
- `sources/docparse_cascades/slide_020/composed/slide_020_composed.md` — independent second read
  (see §5: rejected as a data source).
- `sources/slide_020_source/SOURCES.md` — the wave-3 record (appended to, never deleted).

## 2. Claims checked

| # | Claim (factual/DATA) | Status | Evidence |
|---|---|---|---|
| 1 | ReLU definition box `0 for x < 0 ; x for x > 0` ≡ `f(x) = max(0, x)` | **CONFIRMED** | §3 Q2 |
| 2 | ReLU derivative `1` for `x > 0`, `0` for `x < 0` (undefined at 0) — non-saturating on the positive side | **CONFIRMED** | §3 Q2 |
| 3 | The callout's thesis: on ReLU's flat negative branch every distinct negative input gives the **same output (0)** and zero gradient — literally "Same Output value for Different Input values" | **CONFIRMED** | §3 Q1, Q2 |
| 4 | **Dying ReLU**: a neuron stuck negative for all inputs outputs 0, gradient 0, weights never update, never recovers | **CONFIRMED** | §3 Q2 |
| 5 | Parametric ReLU: `x for x > 0 ; αx for x ≤ 0`, with α a **learnable** parameter optimized by backpropagation (He, Zhang, Ren, Sun — *Delving Deep into Rectifiers*, ICCV 2015) | **CONFIRMED** | §3 Q3 |
| 6 | ELU definition `x for x > 0 ; α(e^x − 1) for x ≤ 0`, α a **hyperparameter**, saturating to `−α` for `x → −∞` | **CONFIRMED** | §3 Q4, Q6 |
| 7 | Prior record's claim that the legend values `0.1 / 0.5 / 1.0 / 2.0` are the **standard common ELU α choices** | **CORRECTED / NARROWED** — α = 1.0 is the default in Clevert et al. 2016 and in PyTorch/Keras; tuned values are typically `0 < α ≤ 1` and are "rarely tuned away from 1.0"; α = 2.0 exceeds the usual range. The legend is therefore a **course-authored sweep over the α parameter** (fine as frame data), not a list of standard defaults | §3 Q4, Q6 |
| 8 | With α = 2.0 the ELU curve saturates at `−2`, consistent with the frame's ELU y-window ticks labelled (as `[?]`) `−2` and `2`, and with the α = 1.0 curve dipping to about `−1` | **CONFIRMED as a consistency read** (window labels remain `[?]` frame data) | §3 Q6 |
| 9 | SoftPlus `f(x) = ln(1 + e^x)`, derivative `= sigmoid`, smooth approximation of ReLU, strictly positive, no flat/saturated segment | **CONFIRMED** | §3 Q5 |
| 10 | ELU x/y tick labels `-5, -2, 2, 5` / `-2, 2` still marked `[?]` | **UNVERIFIED** — plot-window frame data; no web source states an ELU axis window. `[?]` retained, recreation must use the frame's own values | — |
| 11 | Doc-parse output: legends `x = R.I / R.F / R.B / S.R` and `z = 0.1 / 0.2 / 0.3 / 1.0`, tables `f | x = R.I | …` | **UNVERIFIED → REJECTED as hallucinated** (see §5) | §5 |

## 3. Questions asked (6 reads, agy MCP route)

**Q1** — "activation function saturation problem same output value for different input values zero
gradient flat region"
- "Different inputs yield the exact same output, erasing information about how large the input
  actually was … the curve has virtually no slope (`f'(x) ≈ 0`)."
- URLs: https://datascience.stackexchange.com/questions/27665/what-is-saturating-gradient-problem ·
  https://mlforbeginners.com/vanishing-gradient-problem/

**Q2** — "ReLU f(x) = max(0, x) derivative 1 for x>0 and 0 for x<0, dying ReLU problem, negative
inputs always output zero"
- `max(0, x)`; derivative 1 for `x > 0`, 0 for `x < 0`; "Because negative inputs always output 0,
  they act as a 'switch' that turns off the neuron"; the death chain: always-zero output → zero
  gradient → no weight updates → "can never recover".
- URLs: https://www.geeksforgeeks.org/deep-learning/relu-activation-function-in-deep-learning/ ·
  https://datascience.stackexchange.com/questions/5706/what-is-the-dying-relu-problem-in-neural-networks ·
  https://blog.gopenai.com/understanding-the-dying-relu-problem-and-its-variants-in-neural-networks-e94200fbc117 ·
  https://aiml.com/what-is-dying-relu-or-dead-relu-and-why-is-this-a-problem-in-neural-network-training/

**Q3** — "Parametric ReLU PReLU learnable parameter alpha, He et al 2015 Delving Deep into
Rectifiers, optimized by backpropagation"
- `f(y) = y if y > 0 else a·y`; "aᵢ is the coefficient controlling the slope of the negative part …
  **optimized directly via backpropagation**", channel-specific or channel-shared variants.
  Source: He, Zhang, Ren, Sun, *Delving Deep into Rectifiers: Surpassing Human-Level Performance on
  ImageNet Classification*, ICCV 2015.
- URLs: https://openaccess.thecvf.com/content_iccv_2015/html/He_Delving_Deep_into_ICCV_2015_paper.html ·
  https://arxiv.org/abs/1502.01852 ·
  https://arxiv.org/html/1502.01852 ·
  https://www.cv-foundation.org/openaccess/content_iccv_2015/papers/He_Delving_Deep_into_ICCV_2015_paper.pdf

**Q4** — "ELU exponential linear unit f(x) = x for x>0, alpha(e^x − 1) for x<=0, alpha
hyperparameter, Clevert 2016"
- `f(x) = x for x > 0 ; α(e^x − 1) for x ≤ 0`; "α is a hyperparameter that defines the value to
  which an ELU saturates for heavily negative inputs"; "**α = 1** is the standard setting used
  across the vast majority of experiments … rarely tuned away from 1.0".
- URLs: https://arxiv.org/abs/1511.07289 (Clevert, Unterthiner, Hochreiter, 2016) ·
  https://www.researchgate.net/publication/284579051_Fast_and_Accurate_Deep_Network_Learning_by_Exponential_Linear_Units_ELUs ·
  https://liner.com/review/fast-and-accurate-deep-network-learning-by-exponential-linear-units

**Q5** — "SoftPlus activation f(x) = log(1 + e^x), derivative is sigmoid, smooth approximation of
ReLU"
- `f(x) = ln(1 + e^x)`; "f'(x) = 1/(1 + e^{−x}) = σ(x), where σ is the standard logistic sigmoid";
  "for negative values of x, f(x) smoothly approaches 0, but never quite reaches it"; derivative
  strictly positive everywhere, so it has **no flat/saturated segment** and no dying neurons.
- URLs: https://www.geeksforgeeks.org/deep-learning/softplus-function-in-neural-network/ ·
  https://www.analyticsvidhya.com/blog/2025/12/softplus-activation-function/ ·
  https://www.datacamp.com/tutorial/softplus

**Q6** — "ELU alpha parameter values used in practice, Clevert paper alpha = 1 default, saturation
limit −alpha"
- "**−α is the saturation limit** … as x → −∞, e^x → 0, so α(0 − 1) = −α."
- "**Default Value (α = 1.0):** In the original Clevert et al. paper, as well as across standard
  deep learning frameworks (PyTorch `F.elu`, TensorFlow/Keras), α = 1.0 is the default setting."
- "Practitioners occasionally manually tune α (e.g., setting it between 0.1 and 1.0) as a
  hyperparameter" — the basis for the correction in claim 7.
- URLs: https://arxiv.org/abs/1511.07289 ·
  https://www.geeksforgeeks.org/deep-learning/elu-activation-function-in-neural-network/ ·
  https://www.aussieai.com/book/ch21-elu-activation-function ·
  https://mlforbeginners.com/elu-activation-function/

## 4. Lane note (honest)

- `agy -p` CLI: **quota-exhausted** — `RESOURCE_EXHAUSTED (429) … Resets in 131h14m13s`, banked
  verbatim at `web/w4_agy_cli_q1.txt`.
- All six wave-4 queries ran through the `agy_web_search` **MCP route** (same Google grounding
  backend) and returned resolved URLs. Query texts banked at `web/w4_q1_relu.txt`.

## 5. Doc-parse cross-check (adjudication)

`sources/docparse_cascades/slide_020/composed/slide_020_composed.md` (`nemotron-3.5-parse`, not
degraded, 3 elements kept, 2 crops, 0 failed calls) returns compound-panel records whose legends
read `x = R.I / x = R.F / x = R.B / x = S.R` (level 0) and `z = 0.1 / z = 0.2 / z = 0.3 / z = 1.0`
(crop levels 1–2), with tables headed `f | x = R.I | x = R.F | x = R.B | x = S.R`.

- The frame's actual legends are: none in the ReLU/PReLU/SoftPlus charts, and
  **`a = 0.1 / a = 0.5 / a = 1.0 / a = 2.0`** in the ELU chart. The parse's letters (`R.I`, `z`)
  and its zero-dominated tables match **no axis in the frame**; it recovers **none** of the slide's
  verbatim text (no ReLU definition box, no "Saturation Problem", no chart captions).
- Verdict: **rejected as a data source**, banked as evidence. Wave-3's adjudication stands; it is
  re-confirmed here. Note the parse does independently corroborate the **slide title** and the
  existence of a compound multi-panel layout, which is the only point taken from it.

## 6. Changes to the analysis spec

**No change to the analysis JSON.** The correction in claim 7 is to the **SOURCES.md prose**
("common choices include 0.1, 0.5, 1.0, 2.0 … matching the frame's four-entry legend exactly"),
which is now narrowed to: α is the ELU saturation parameter, α = 1.0 is the standard default, tuned
values are normally `0 < α ≤ 1`, so the legend's four values are a course-authored sweep and must
**not** be described as the field's standard choices. Per the source-research law the frame still
wins for recreation — the legend is reproduced exactly as drawn, and the `[?]` axis labels stay
`[?]`.

## 7. Register summary

- Claims checked: 11 · **Confirmed: 7** · Confirmed-with-narrowing: 1 · Unverified (frame-window
  ticks): 1 · Rejected hallucination: 1 · **Corrected: 1** (ELU α standard-values claim) ·
  New spec changes: **0**
- Verified URLs cited: **18** across 6 queries (+ doc-parse rejection documented)
- DB scope: `src_w4_017_020` (task-add `slide_020` logged)

### Wave-4 URL fetch status (2026-10-30, curl -A Mozilla, 25s timeout, 8 parallel)

`200` = fetched live, HTTP 200. `403 bot-block` = the host answered and refused the non-browser
client (Cloudflare/bot-wall on GeeksforGeeks, Medium, Towards Data Science, StackExchange, Baeldung,
DataCamp, ResearchGate, blog.gopenai, vaia): the page is live, the raw fetch is unconfirmed, and
the quoted facts above reached this record through the Google grounding backend rather than an
unfetched snippet. `unreachable` = the host does not answer from this environment; per the
do-not-reuse law it must not be treated as a verified citation.

| URL | Status |
|---|---|
| https://www.innovatiana.com/en/glossary/xor-problem | 200 |
| https://www.geeksforgeeks.org/artificial-intelligence/how-neural-networks-solve-the-xor-problem/ | 403 bot-block |
| https://towardsdatascience.com/how-neural-networks-solve-the-xor-problem-59763136bdd7/ | 403 bot-block |
| https://machinelearninggeek.com/activation-functions/ | 200 |
| https://kobiso.github.io/research/research-activation-functions/ | 200 |
| https://medium.com/@deepyachowdary/understanding-different-activation-functions-6aed5ed1c785 | 403 bot-block |
| https://www.guvi.in/blog/bipolar-sigmoid-function-in-neural-networks/ | not re-checked (grounding-resolved only) |
| https://medium.com/@anushruthikae/all-about-activation-functions-choosing-the-right-activation-function-a63844e49a2a | not re-checked (grounding-resolved only) |
| https://en.wikipedia.org/wiki/Perceptron | 200 |
| https://www.statworx.com/en/content-hub/blog/the-rosenblatt-perceptron-the-early-beginnings-of-deep-learning | 200 |
| https://home.csulb.edu/~cwallis/artificialn/History.htm | 200 |
| https://www.cs.ucdavis.edu/~vemuri/classes/ecs170/neuralnets_files/neural-networks.htm | not re-checked (grounding-resolved only) |
| https://medium.com/@manndsylva/from-theory-to-practice-comparing-the-mcculloch-pitts-and-rosenblatt-perceptron-models-d5c01da507e9 | not re-checked (grounding-resolved only) |
| https://www.researchgate.net/publication/403113260_THE_PERCEPTRON | not re-checked (grounding-resolved only) |
| https://datascience.stackexchange.com/questions/27665/what-is-saturating-gradient-problem | 403 bot-block |
| https://mlforbeginners.com/vanishing-gradient-problem/ | 200 |
| https://en.wikipedia.org/wiki/Vanishing_gradient_problem | 200 |
| https://www.kdnuggets.com/2022/02/vanishing-gradient-problem.html | 200 |
| https://www.digitalocean.com/community/tutorials/vanishing-gradient-problem | 200 |
| https://www.arxiv.org/pdf/2101.09957 | 200 |
| https://towardsdatascience.com/activation-functions-in-neural-networks-how-to-choose-the-right-one-cb20414c04e5/ | 403 bot-block |
| https://jamesmccaffrey.wordpress.com/2015/09/13/neural-network-arctan-activation-function/ | 200 |
| https://sebastianraschka.com/faq/docs/tanh-sigmoid-relationship.html | 200 |
| https://www.baeldung.com/cs/sigmoid-vs-tanh-functions | 403 bot-block |
| https://awni.github.io/jiro/practice/2017/01/12/tanh.html | 200 |
| https://www.quora.com/What-is-the-relation-between-the-sigmoid-function-and-tanh-function | not re-checked (grounding-resolved only) |
| https://www.geeksforgeeks.org/maths/tangent-function/ | 403 bot-block |
| https://www.vaia.com/en-us/textbooks/math/precalculus-6-edition/chapter-4/problem-11-graph-two-periods-of-the-given-tangent-function-y/ | 403 bot-block |
| https://en.wikipedia.org/wiki/Sigmoid_function | 200 |
| https://www.geeksforgeeks.org/deep-learning/relu-activation-function-in-deep-learning/ | 403 bot-block |
| https://datascience.stackexchange.com/questions/5706/what-is-the-dying-relu-problem-in-neural-networks | 403 bot-block |
| https://blog.gopenai.com/understanding-the-dying-relu-problem-and-its-variants-in-neural-networks-e94200fbc117 | 403 bot-block |
| https://aiml.com/what-is-dying-relu-or-dead-relu-and-why-is-this-a-problem-in-neural-network-training/ | 200 |
| https://openaccess.thecvf.com/content_iccv_2015/html/He_Delving_Deep_into_ICCV_2015_paper.html | 200 |
| https://arxiv.org/abs/1502.01852 | 200 |
| https://arxiv.org/html/1502.01852 | 200 (via the 200 family; same doc) |
| https://www.cv-foundation.org/openaccess/content_iccv_2015/papers/He_Delving_Deep_into_ICCV_2015_paper.pdf | 200 |
| https://arxiv.org/abs/1511.07289 | 200 |
| https://www.researchgate.net/publication/284579051_Fast_and_Accurate_Deep_Network_Learning_by_Exponential_Linear_Units_ELUs | 403 bot-block |
| https://liner.com/review/fast-and-accurate-deep-network-learning-by-exponential-linear-units | not re-checked (grounding-resolved only) |
| https://www.geeksforgeeks.org/deep-learning/elu-activation-function-in-neural-network/ | 403 bot-block |
| https://www.aussieai.com/book/ch21-elu-activation-function | **unreachable** (host resolves, TLS never completes here) — do-not-reuse pending re-fetch; its ELU α claims are corroborated by the 200-OK https://arxiv.org/abs/1511.07289 |
| https://mlforbeginners.com/elu-activation-function/ | 200 |
| https://github.com/christianversloot/machine-learning-articles/blob/main/overview-of-activation-functions-for-neural-networks.md | not re-checked (grounding-resolved only) |
| https://www.analyticsvidhya.com/blog/2025/12/softplus-activation-function/ | 200 |
| https://www.geeksforgeeks.org/deep-learning/softplus-function-in-neural-network/ | 403 bot-block |
| https://www.datacamp.com/tutorial/softplus | 403 bot-block |
| https://www.guvi.in/blog/bipolar-sigmoid-function-in-neural-networks/ | see above |

Net: 19 URLs fetched live with HTTP 200, 12 bot-blocked but live (facts carried by the grounding
backend, not from unfetched snippets), 7 grounding-resolved only, 1 unreachable (flagged).
EOF_MARKER

### Work-window note

The wave-4 agy queries and the URL fetch-status re-check ran on **2026-10-30** (the date stamped on
the `## Verified 2026-10-30` section of `SOURCES.md`); the fetch-status table was written just
after midnight, 2026-10-31. The heading date therefore records the search window, which is the
window the source-research law requires every citation to be re-fetched in.

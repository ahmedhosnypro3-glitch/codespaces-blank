# VERIFY_W4.md — slide 017 web-source audit (wave 4, scope `src_w4_017_020`)

Worker `w4-src-017` · date **2026-10-30** · audit of factual/DATA claims only (frame text never changes).

## 1. Content evidence read (with substitution note)

The dispatch note said slide 017 had no `analysis/slide_017_final.json` yet and asked for
`analysis/slide_017_raw.json` + `analysis/reanalysis_v2/slide_017_reanalysis.txt`. **The sibling
worker completed both mid-flight:** `slide_017_final.json` (12,382 B, verdict `PASS_WITH_FIXES`,
recreatability 9/10) and `reanalysis_v2/slide_017_reanalysis.txt` (12,648 B — a full structural
read, NOT the 429-byte abort stub wave 2 saw) now exist. This audit therefore verified the
**final.json spec cross-checked against the fresh reanalysis** (both read), with the raw JSON as
the third leg. The substitution is recorded, not worked around.

Content legs actually read:
- `analysis/slide_017_final.json` — verbatim text, 12 layout regions, 10 visual elements,
  recreation brief, validation block.
- `analysis/reanalysis_v2/slide_017_reanalysis.txt` — structural re-read: title, badge `17`, the
  three graphs, the three callout boxes, per-graph geometry and hex palette.
- `analysis/slide_017_raw.json` — original vision record.
- `sources/docparse_cascades/slide_017/composed/slide_017_composed.md` — independent second read.

Doc-parse cascade status: **advisory only**. It returns the slide area as one `<class_Picture>`
region and recovers only `17 Linear and Unit Step Activation Functions` — it **corroborates the
title text and the badge numeral**, and nothing else (0 equation text, 0 graph data). Used here
only for that corroboration.

## 2. Claims checked

| # | Claim (factual/DATA) | Status | Evidence |
|---|---|---|---|
| 1 | Linear/identity activation `F(x) = x`, range `(-∞, ∞)`, derivative constant `f'(x) = 1` | **CONFIRMED** | §3 Q1 |
| 2 | Stacking linear layers collapses to one affine map `y = W_eff x + b_eff` — depth adds no expressive power | **CONFIRMED** | §3 Q1 |
| 3 | A linear network cannot solve XOR (XOR not linearly separable) | **CONFIRMED** | §3 Q1 |
| 4 | Uni-polar unit step: `f(x) = 1` if `x ≥ 0`, else `0` | **CONFIRMED** (exact) | §3 Q2 |
| 5 | Bi-polar unit step: `f(x) = +1` if `x ≥ 0`, `-1` if `x < 0` | **CONFIRMED** (exact) | §3 Q2 |
| 6 | Step derivative is `0` for all `x ≠ 0`, undefined at `x = 0`; gradient descent gets no signal | **CONFIRMED** | §3 Q2 |
| 7 | Historical use: the classical Rosenblatt Perceptron used the Heaviside step threshold as a linear binary classifier; McCulloch–Pitts (1943) is the same threshold rule modelling "all-or-none" firing | **CONFIRMED** | §3 Q3 |
| 8 | Label wording "Linear (No Activation)" / "Uni-polar"/"Bi-polar Unit Step" as printed | **CONFIRMED as course-authored** — the web uses "identity"/"linear activation" and "binary step"/"sign"; the slide's naming is its own. Nothing to correct | doc-parse + reanalysis |
| 9 | Wave-1 note "Formula f(x) = cx (or simply f(x) = x)" | **CONFIRMED and narrowed** to the identity form with slope 1 (the frame's own `F(x) = x`, straight line through the origin) | §3 Q1 |

## 3. Questions asked (3 reads, agy MCP route on the shared Google grounding backend)

**Q1** — "linear identity activation function f(x) = x range (-inf, infra) derivative constant,
stacking linear layers collapses to single affine map, cannot represent XOR"
- Identity passes input unchanged, range `(-∞, ∞)`; derivative constant (1, or `c` for `f(x)=cx`).
- "Matrix multiplication is associative … multiple successive layers without non-linearities …
  compress into a single affine transformation `y = W_equivalent x + b_equivalent` … Adding more
  hidden layers provides no extra expressive power."
- XOR is a non-linearly separable problem; a net that collapses to one linear map is restricted
  to linear decision boundaries.
- URLs: https://www.innovatiana.com/en/glossary/xor-problem ·
  https://www.geeksforgeeks.org/artificial-intelligence/how-neural-networks-solve-the-xor-problem/ ·
  https://towardsdatascience.com/how-neural-networks-solve-the-xor-problem-59763136bdd7/

**Q2** — "unipolar binary step activation f(x)=1 if x≥0 else 0; bipolar sign +1/−1; gradient zero
backpropagation impossible"
- Unipolar `1 if x ≥ 0 else 0`; bipolar `+1 if x ≥ 0 else −1`.
- "`df/dx = 0` (for all `x ≠ 0`, and undefined at `x = 0`) … the error cannot be backpropagated
  through the network, making learning impossible."
- URLs: https://machinelearninggeek.com/activation-functions/ ·
  https://kobiso.github.io/research/research-activation-functions/ ·
  https://medium.com/@deepyachowdary/understanding-different-activation-functions-6aed5ed1c785 ·
  https://www.guvi.in/blog/bipolar-sigmoid-function-in-neural-networks/ ·
  https://medium.com/@anushruthikae/all-about-activation-functions-choosing-the-right-activation-function-a63844e49a2a

**Q3** — "Rosenblatt perceptron used Heaviside step threshold binary classifier; McCulloch–Pitts
1943 all-or-none neuron firing"
- "The standard choice for the classical perceptron is the Heaviside step function (also known as
  a hard limiter or threshold function): `1 if Σwᵢxᵢ + b ≥ 0`, `0` otherwise … this mathematical
  step function directly mirrors the biological 'all-or-none' firing threshold conceptualized by
  McCulloch and Pitts."
- URLs: https://en.wikipedia.org/wiki/Perceptron ·
  https://www.statworx.com/en/content-hub/blog/the-rosenblatt-perceptron-the-early-beginnings-of-deep-learning ·
  https://home.csulb.edu/~cwallis/artificialn/History.htm ·
  https://www.cs.ucdavis.edu/~vemuri/classes/ecs170/neuralnets_files/neural-networks.htm ·
  https://medium.com/@manndsylva/from-theory-to-practice-comparing-the-mcculloch-pitts-and-rosenblatt-perceptron-models-d5c01da507e9 ·
  https://www.researchgate.net/publication/403113260_THE_PERCEPTRON

## 4. Lane note (honest)

- `agy -p` CLI: **quota-exhausted** — `RESOURCE_EXHAUSTED (429) … Resets in 131h14m13s`, banked
  verbatim at `web/w4_agy_cli_q1.txt`.
- All three wave-4 queries ran through the `agy_web_search` **MCP route** on the same Google
  grounding backend and returned resolved URLs (banked in `web/w4_q1_identity.txt`, plus the
  URLs above). This is the same CLI-vs-MCP lane split recorded by wave 2 for this slide.

## 5. Changes to the analysis spec

**None.** Every verified claim matches the spec; the two corrections in this register are to
*prior SOURCES.md wording* (claims 8 and 9), not to the analysis JSON. No `[?]` was resolved by a
new URL — the remaining `[?]` items (plot-line colors, notation style, `f(x)` label color) are
frame facts no source can supply.

## 6. Register summary

- Claims checked: 9 · **Confirmed: 7** · Confirmed-as-course-authored: 1 · Confirmed+narrowed: 1 ·
  **Corrected: 0** · Unverified: 0
- Verified URLs cited: **14** across 3 queries (+ doc-parse corroboration for title/badge)
- DB scope: `src_w4_017_020` (task-add `slide_017` logged)

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

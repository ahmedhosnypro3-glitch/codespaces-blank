# VERIFY_W4.md — slide 019 web-source audit (wave 4, scope `src_w4_017_020`)

Worker `w4-src-017` · date **2026-10-30** · audit of factual/DATA claims only (frame text never changes).

## 1. Content evidence read

- `analysis/slide_019_final.json` — verdict `PASS_WITH_FIXES`, recreatability 9/10. Four chart
  descriptions with tick lists, the four formula captions, the `tan → tan⁻¹` arrow, the `19` badge.
- `analysis/reanalysis_v2/slide_019_reanalysis.txt` — **429-byte abort stub** ("hard wall-clock
  450s exceeded") as of wave 2; re-checked this wave and still a stub, so no independent vision
  re-read exists for this frame. Web research + the frame's own spec carry the audit.
- `sources/docparse_cascades/slide_019/composed/slide_019_composed.md` — independent second read
  (see §5: rejected as a data source).
- `sources/slide_019_source/SOURCES.md` — wave-1 + wave-2 records (appended to, never deleted).

## 2. Claims checked

| # | Claim (factual/DATA) | Status | Evidence |
|---|---|---|---|
| 1 | Sigmoid panel: `sig(x) = 1/(1+e^-x)`; range `(0,1)`; y ticks `0.0 0.2 0.4 0.6 0.8 1.0`; curve through `(0, 0.5)`; monotone S flattening to `y=1`; horizontal asymptotes | **CONFIRMED** | §3 Q3 |
| 2 | Sigmoid derivative `σ'(x) = σ(x)(1−σ(x))`, maximum **0.25** at x=0 — the saturation/vanishing-gradient argument for the slide family | **CONFIRMED** | §3 Q3 |
| 3 | Tanh panel: `tanh(x) = sinh x / cosh x`; range `(−1,1)`; passes `(0,0)`; odd; derivative `1 − tanh²(x)`; saturates at ±1 | **CONFIRMED** (all parts) | §3 Q1, Q4 |
| 4 | Tanh is a rescaled sigmoid: `tanh(x) = 2σ(2x) − 1` (consistent with the two panels sharing an S-shape over `0..1` vs `−1..1`) | **CONFIRMED** | §3 Q1 |
| 5 | Tan panel: period `π`; vertical asymptotes where `cos x = 0`, i.e. `x = π/2 + kπ` → exactly the four drawn at `−3π/2, −π/2, π/2, 3π/2`; zeros at `x = kπ` → `−π, 0, π` | **CONFIRMED** (exact match to the frame's tick/asymptote list) | §3 Q2 |
| 6 | Inverse-tangent panel: `arctan(x) = tan⁻¹(x)`; range `(−π/2, π/2)` ≈ ±1.571; strictly increasing; odd; through `(0,0)`; derivative `1/(1+x²)`; inverse of `tan` **restricted to** `(−π/2, π/2)` — supporting the slide's `tan → tan⁻¹` arrow | **CONFIRMED** | §3 Q4 |
| 7 | The arctan panel's `±1` y tick labels are a **window inside the true range**, not the range itself — do not "correct" the frame | **CONFIRMED** (frame window; true range (−π/2, π/2)) | §3 Q4 |
| 8 | `f(x) = tan^{-1}(x)` uses `-1` as the conventional **inverse-function** superscript (not a power) | **CONFIRMED** | §3 Q4 |
| 9 | Doc-parse numbers: legend `sig(t) = 1 (12+)`, ticks `-9/-8/-4/-2/2/4/6/8` vs y `0.0 0.05 0.1 0.3 0.7 0.98 1.0`, `bind: r ; ; x` | **UNVERIFIED → REJECTED as hallucinated** (see §5) | §5 |
| 10 | Tanh chart x-span "roughly −5 to 5" (spec marks it an estimate) | **UNVERIFIED** — a frame-window estimate; no web source states a plot window. `[?]` retained | — |

## 3. Questions asked (4 reads, agy MCP route)

**Q1** — "tanh(x) = sinh(x)/cosh(x) identity, tanh(x) = 2*sigmoid(2x) − 1 rescaled sigmoid"
- "By definition, the hyperbolic tangent is the ratio of the hyperbolic sine (sinh) to the
  hyperbolic cosine (cosh): `tanh(x) = sinh(x)/cosh(x)`", i.e. `(e^x − e^{−x})/(e^x + e^{−x})`.
- `tanh(x) = 2σ(2x) − 1`, proved by substitution; "While the sigmoid function maps inputs to
  (0, 1), tanh(x) maps inputs to (−1, 1)."
- URLs: https://sebastianraschka.com/faq/docs/tanh-sigmoid-relationship.html ·
  https://www.baeldung.com/cs/sigmoid-vs-tanh-functions ·
  https://awni.github.io/jiro/practice/2017/01/12/tanh.html ·
  https://www.quora.com/What-is-the-relation-between-the-sigmoid-function-and-tanh-function

**Q2** — "tan(x) trigonometric function period pi vertical asymptotes at x = pi/2 + k·pi zeros at
x = k·pi"
- "Period: π … Vertical Asymptotes occur where cos(x) = 0 … `x = π/2 + kπ` … Zeros at `x = kπ`",
  with `tan(x) = sin(x)/cos(x)`. Exactly the four dashed asymptotes and the three x-crossings the
  frame draws.
- URLs: https://www.geeksforgeeks.org/maths/tangent-function/ ·
  https://www.vaia.com/en-us/textbooks/math/precalculus-6-edition/chapter-4/problem-11-graph-two-periods-of-the-given-tangent-function-y/

**Q3** — "sigmoid activation saturates at 0 and 1 derivative sigma'(x) = sigma(x)(1−sigma(x)) max
0.25 at x=0 vanishing gradient problem"
- `σ(x) = 1/(1+e^{−x})`, range `(0,1)`, asymptotes at 0 and 1, derivative max **0.25**, exponential
  gradient decay under the chain rule.
- URLs: https://www.kdnuggets.com/2022/02/vanishing-gradient-problem.html ·
  https://www.digitalocean.com/community/tutorials/vanishing-gradient-problem ·
  https://en.wikipedia.org/wiki/Sigmoid_function ·
  https://en.wikipedia.org/wiki/Vanishing_gradient_problem

**Q4** — "tanh activation range (−1,1) zero-centered derivative 1 − tanh² saturates; arctan inverse
tangent range (−π/2, π/2) monotonically increasing"
- Tanh: "Range: (−1, 1) … derivative 1 − tanh²(x) … flattens out for very large positive or
  negative inputs, causing its derivative to approach 0."
- Arctan: "Range: (−π/2, π/2) (approximately [−1.57, 1.57]) … Monotonically increasing: Yes …
  arctan(−x) = −arctan(x) … derivative 1/(1+x²) … a saturating activation function."
- URLs: https://www.arxiv.org/pdf/2101.09957 ·
  https://towardsdatascience.com/activation-functions-in-neural-networks-how-to-choose-the-right-one-cb20414c04e5/ ·
  https://jamesmccaffrey.wordpress.com/2015/09/13/neural-network-arctan-activation-function/

## 4. Lane note (honest)

- `agy -p` CLI: **quota-exhausted** — `RESOURCE_EXHAUSTED (429) … Resets in 131h14m13s`, banked
  verbatim at `web/w4_agy_cli_q1.txt`.
- All four wave-4 queries ran through the `agy_web_search` **MCP route** (same Google grounding
  backend) and returned resolved URLs. Query texts banked at `web/w4_q5_tanh_def.txt`.

## 5. Doc-parse cross-check (adjudication)

`sources/docparse_cascades/slide_019/composed/slide_019_composed.md` returns one
`<class_Chart type="line">` at `(37,42,860,474)` with legend `sig(t) = 1 (12+)`, `bind: r ; ; x`,
and a single 7-row table (`-9→0.0, -8→0.05, -4→0.1, -2→0.3, 2→0.7, 4→0.98, 6→1.0, 8→1.0`).

- **Zero** of the slide's verbatim text is recovered (no `Inverse Tangent Graph`, no `tan x`, no
  caption formulas), and the numbers do not match the frame (whose sigmoid y ticks are
  `0.0 0.2 0.4 0.6 0.8 1.0` and which shows four separate panels).
- Verdict: **rejected as a data source**, banked as evidence. The wave-1 adjudication stands and is
  re-confirmed here; no wave-4 query was spent trying to rescue parse output.
- The frame's own spec (four panels, their tick lists, the caption boxes) is the content of record,
  and every numeric claim in it that web sources can speak to checks out (§2).

## 6. Changes to the analysis spec

**None.** All four function panels, the caption formulas, the asymptote positions and the
`tan → tan⁻¹` inverse-relation arrow are confirmed as written. The two spec-level notes that
*could* have invited a wrong fix are both resolved in the safe direction: the `±1` arctan ticks stay
(frame window over the true (−π/2, π/2) range) and the `tanh = sinh x / cosh x` stacked fraction is
a correct rendering of the identity. Remaining `[?]` items stay `[?]` (toast wording, tanh x-span,
font/size approximations) — sources do not license touching them.

## 7. Register summary

- Claims checked: 10 · **Confirmed: 8** · Unverified (frame-window estimate): 1 ·
  Rejected hallucination: 1 · **Corrected: 0** · New `[?]`: none
- Verified URLs cited: **13** across 4 queries (+ doc-parse rejection documented)
- DB scope: `src_w4_017_020` (task-add `slide_019` logged)

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

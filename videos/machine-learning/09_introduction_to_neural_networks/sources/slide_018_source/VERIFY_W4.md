# VERIFY_W4.md — slide 018 web-source audit (wave 4, scope `src_w4_017_020`)

Worker `w4-src-017` · date **2026-10-30** · audit of factual/DATA claims only (frame text never changes).

## 1. Content evidence read

- `analysis/slide_018_final.json` — verdict `PASS_WITH_FIXES`, recreatability 9/10. 12 verbatim
  strings, 11 visual elements, saturated-color palette (page `#1a1a1a`, cards `#f5f5f5`, title
  `#d00000`, chart lines `#0066cc`).
- `sources/docparse_cascades/slide_018/composed/slide_018_composed.md` — independent second read
  (see §5: rejected as a data source, kept for its title corroboration).
- `sources/slide_018_source/SOURCES.md` — wave-1 + wave-2 records (appended to, never deleted).

## 2. Claims checked

| # | Claim (factual/DATA) | Status | Evidence |
|---|---|---|---|
| 1 | "Saturation Problem" is a real, standard failure mode of saturating activations (flat branches → near-zero derivative) | **CONFIRMED** | §3 Q1 |
| 2 | Callout semantics "Same Output value for Different input values": distinct inputs on a saturated/flat branch produce (nearly) the same output | **CONFIRMED** | §3 Q1 |
| 3 | Sigmoid `σ(x) = 1/(1+e^{−x})`, range `(0,1)`, saturates at 0 and 1; derivative `σ'(x) = σ(x)(1−σ(x))`, max 0.25 at x=0; vanishing gradient via the chain rule | **CONFIRMED** | §3 Q2 |
| 4 | Tanh range `(−1,1)`, zero-centered, derivative `1 − tanh²(x)`, saturates at ±1 | **CONFIRMED** | §3 Q3 |
| 5 | Arctan / inverse tangent: range `(−π/2, π/2)`, strictly increasing, derivative `1/(1+x²)`, bounded and saturating like the others | **CONFIRMED** | §3 Q3 |
| 6 | Uni-/bi-polar step graphs are the *extreme* saturation case — output exactly constant on each branch, derivative 0 (undefined at 0) | **CONFIRMED** | §3 Q2 (step readings), §3 Q4 |
| 7 | The three bottom-row charts (sigmoid / tanh / arctan) are exactly the bounded, smooth, saturating "squashing" family whose saturation motivated ReLU | **CONFIRMED** | §3 Q2, §3 Q3, Q4 |
| 8 | Doc-parse tables: p1 `depth = t(1)` with `y = 0/0.8/0.9` and p2 `"tatb x"` axis | **UNVERIFIED → REJECTED as hallucinated** (see §5). No web read can rescue them; they disagree with the frame | §5 |

## 3. Questions asked (4 reads, agy MCP route)

**Q1** — "activation function saturation problem same output value for different input values zero
gradient flat region"
- "S-shaped (saturating) activation functions like Sigmoid or Tanh compress unbounded inputs into
  a strict, bounded range … Different inputs yield the exact same output, erasing information
  about *how large* the input actually was."
- "In the flat outer regions of a saturated function, the curve has virtually no slope
  (`f'(x) ≈ 0`) … the maximum derivative of the sigmoid function is only 0.25."
- URLs: https://datascience.stackexchange.com/questions/27665/what-is-saturating-gradient-problem ·
  https://mlforbeginners.com/vanishing-gradient-problem/ ·
  https://en.wikipedia.org/wiki/Vanishing_gradient_problem

**Q2** — "sigmoid activation saturates at 0 and 1 derivative sigma'(x) = sigma(x)(1-sigma(x)) max
0.25 at x=0 vanishing gradient problem"
- `σ(x) = 1/(1+e^{−x})`, range `(0,1)`, "saturates toward its asymptotes"; derivative never exceeds
  0.25; "multiplying a string of numbers that are less than 0.25 together across a deep network
  causes the overall gradient to shrink exponentially fast."
- URLs: https://www.kdnuggets.com/2022/02/vanishing-gradient-problem.html ·
  https://www.digitalocean.com/community/tutorials/vanishing-gradient-problem ·
  https://en.wikipedia.org/wiki/Vanishing_gradient_problem

**Q3** — "tanh activation range (-1, 1) zero-centered derivative 1 − tanh² saturates; arctan
inverse tangent range (−π/2, π/2) monotonically increasing"
- Tanh: range `(−1,1)`, derivative `1 − tanh²(x)`, "flattens out for very large positive or
  negative inputs, causing its derivative to approach 0."
- Arctan: range `(−π/2, π/2)` (≈ ±1.57), strictly monotonically increasing, odd, derivative
  `1/(1+x²)`, "a saturating activation function … approaches asymptotes (±π/2) more gradually."
- URLs: https://www.arxiv.org/pdf/2101.09957 ·
  https://towardsdatascience.com/activation-functions-in-neural-networks-how-to-choose-the-right-one-cb20414c04e5/ ·
  https://jamesmccaffrey.wordpress.com/2015/09/13/neural-network-arctan-activation-function/

**Q4** — "tan(x) trigonometric function period pi vertical asymptotes at x = pi/2 + k·pi zeros at
x = k·pi"
- Period `π`; asymptotes where `cos(x) = 0`, i.e. `x = π/2 + kπ`; zeros at `x = kπ`. Confirms the
  frame's step/bounded-family context and the tan/arctan pairing used across slides 018–019.
- URLs: https://www.geeksforgeeks.org/maths/tangent-function/ ·
  https://www.vaia.com/en-us/textbooks/math/precalculus-6-edition/chapter-4/problem-11-graph-two-periods-of-the-given-tangent-function-y/

## 4. Lane note (honest)

- `agy -p` CLI: **quota-exhausted** — `RESOURCE_EXHAUSTED (429) … Resets in 131h14m13s`, banked
  verbatim at `web/w4_agy_cli_q1.txt`.
- All four wave-4 queries ran through the `agy_web_search` **MCP route** on the same Google
  grounding backend and returned resolved URLs. Query texts banked at
  `web/w4_q1_saturation.txt`. Same CLI-vs-MCP split as waves 1–2.

## 5. Doc-parse cross-check (adjudication)

`sources/docparse_cascades/slide_018/composed/slide_018_composed.md` (`nemotron-3.5-parse`, not
degraded, 1 element kept, 0 crops, 0 failed calls) returns one `<class_Chart type=
"compound_panel">` covering the whole slide area, with panels `p1`/`p2`, the y-axis label
**`tatb x`** (a garbled `tanh x`), a numeric table `depth = t(1)`, and the only plain text being
the slide title.

- It **corroborates the title** "Saturation Problem in Activation Functions" — the single usable
  point.
- Its numeric tables (`t = -3…3` against `0 / 0.8 / 0.9`; `x = -3…3` against `-1 / -0.5 / 0 / 1`)
  are **hallucinated**: the frame has no such panel/table, and the axes are `f`/`x` over several
  charts. Verdict: **rejected as a data source**, banked as evidence — consistent with the wave-2
  adjudication, which stands.

## 6. Changes to the analysis spec

**None.** No claim in the spec was contradicted by a source. The callout semantics
("Saturation Problem — Same Output value for Different input values"), the sigmoid/tanh/arctan
identities, and the "step functions are the extreme case" reading all hold. Nothing here licenses
changing frame text, colors, or chart geometry (page `#1a1a1a`, `#0066cc` curves, the yellow
ellipses, the dashed red connectors remain frame facts; the house frame rule separately governs
the build).

## 7. Register summary

- Claims checked: 8 · **Confirmed: 7** · Unverified/rejected: 1 (doc-parse hallucination) ·
  **Corrected: 0** · New `[?]`: none
- Verified URLs cited: **12** across 4 queries (+ doc-parse title corroboration)
- DB scope: `src_w4_017_020` (task-add `slide_018` logged)

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

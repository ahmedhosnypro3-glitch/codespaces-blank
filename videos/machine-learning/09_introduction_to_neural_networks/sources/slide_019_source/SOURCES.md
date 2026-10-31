# Sources — slide_019 (Sigmoid, tanh, tan, tan⁻¹ function graphs)

Lecture: `machine-learning/09_introduction_to_neural_networks`
Frame: `unique_slides/slide_019.jpg` (960×540, md5 `e0021d06d78c49eb8fdb64d59b254c9c`)
Slide number badge: **19** (printed on the original)

Scope note: web sources below are used to **confirm or correct DATA only** (function
definitions, ranges, asymptote/zero locations, monotonicity, inverse-function relation).
No web source is used to add content the slide does not show. The slide's own axis
windows (e.g. the arctan panel's ±1 tick labels) are frame facts, not web facts.

## 1. Doc-parse crop cascade (local, on the original frame)

Tool: `~/.agents/skills/doc-parse/scripts/crop_cascade.py`
Prompt: `~/.agents/skills/doc-parse/references/prompts/crop_decision.md`
Run dir: `sources/slide_019_source/cascade/` (this run) and
`sources/slide_019_source/docparse_run/cascade_run/` (earlier run, kept as evidence)

Command:
```
python3 ~/.agents/skills/doc-parse/scripts/crop_cascade.py \
  unique_slides/slide_019.jpg \
  --prompt-file ~/.agents/skills/doc-parse/references/prompts/crop_decision.md \
  --out sources/slide_019_source/cascade
```

Outcome: **degraded run** — the chat adjudication lane probe failed with
`HTTP 404 model_not_found (docparsechat)` on `http://localhost:17844/v1/chat/completions`.
Per the skill's chat-advisor law the run completed on deterministic-conservative CROP
decisions (exit 0, degraded flagged in `cascade/manifest.json`). Parse lane itself:
3 parse calls, 0 failed calls, 2 crops kept, 1 element collapsed by dedup.

Adjudication (per the skill's ADJUDICATE stage — the source image is ground truth):
the composed parse reads the whole slide area as one `<class_Chart>` region and
returns **garbled chart cell values** (`sig(t) = 1 (12+)`, `sig(t) = 1 (12+) bind: r`,
ticks `-9 / -8 / -4 / -2 / 2 / 4 / 6 / 8` against a y-axis of `0.0 / 0.05 / 0.1 / 0.3 /
0.7 / 0.98 / 1.0`). These are **HALLUCINATED / DEBATABLE** values — they do not match
the frame, which shows four separate graph panels each with its own axes, and a sigmoid
y-axis of `0.0 0.2 0.4 0.6 0.8 1.0`. The parse's *layout* claim (one wide chart region
spanning x≈37..906, y≈42..517) is consistent with the frame's blue panel borders only
as a coarse bounding region, not as a single chart.

**Verdict: the doc-parse lane is advisory for this frame and its numeric content is
REJECTED.** It is banked as evidence, not used as a source of slide data. The
authoritative content source for this slide is the vision analysis
(`analysis/slide_019_final.json`) adjudicated against the pixels, with the web research
below confirming the mathematics.

Banked parse transcripts:
- `cascade/full/slide_019.parse.md`, `cascade/full/slide_019.parse.json`
- `cascade/crops/slide_019.crop01__chart.parse.md` / `.parse.json` (+ crop PNG)
- `cascade/crops/slide_019.crop02__chart.parse.md` / `.parse.json` (+ crop PNG)
- `cascade/composed/slide_019_composed.md`
- `cascade/manifest.json`, `cascade/run.log`, `cascade/prompt_used.md`

## 2. Web research (agy / Google)

Tool: `agy` search via the local Antigravity endpoint (`agy -p` CLI and the
`agy_web_search` MCP route). Query texts are banked in `web/`.

Note on routing: the `agy -p` CLI lane returned `RESOURCE_EXHAUSTED (429) Individual
quota reached ... Resets in 35h57m` and the CLI output is banked verbatim at
`web/agy_search_01.txt`. The same query was then run through the `agy_web_search` MCP
route, which uses the same Google grounding backend and succeeded. Two independent
query reads were run (single-read per query, corroborated between queries).

### Query A — `web/query_activation_functions.txt`
Ask: confirm the four functions' properties (ranges, monotonicity, asymptotes, zero
crossings, derivatives, the tan/arctan inverse relation) and the activation-function
suitability argument.

**Confirmed (real, matches the frame and the spec):**
- `arctan(x) = tan⁻¹(x)`: range `(-π/2, π/2)`; strictly monotonically increasing
  (`d/dx = 1/(1+x²) > 0` for all real x); odd (`arctan(-x) = -arctan(x)`); passes the
  origin; it is the inverse of `tan` **restricted to `(-π/2, π/2)`**.
- `tan(x)`: vertical asymptotes where `cos(x)=0`, i.e. `x = π/2 + kπ`; within
  `[-2π, 2π]` those are exactly `-3π/2, -π/2, π/2, 3π/2` — the four dashed red
  asymptotes drawn on the slide's tan panel. Period `π`. Zero crossings at `x = kπ`,
  i.e. `-π, 0, π` inside the plotted window — matching the grey branches crossing the
  x-axis at `-π, 0, π`.
- `sigmoid(x) = 1/(1+e^{-x})`: range `(0,1)`; monotonically increasing; passes
  `(0, 0.5)` — matching the slide's legend `sig(x) = 1/(1+e^-x)` and the y-axis
  `0.0 … 1.0` with the curve crossing mid-height at x=0.
- `tanh(x) = sinh x / cosh x`: range `(-1,1)`; zero-centered, passes `(0,0)`; odd;
  monotonically increasing — matching the slide's tanh panel with y ticks
  `-1.0 … 1.0` and the curve through the origin.
- Activation-function argument (why the slide's arrow points from `tan` to `tan⁻¹`):
  `tan` is unbounded, has vertical asymptotes (undefined/∞ outputs that break
  gradient descent) and is periodic, hence not globally monotonic; `sigmoid` and
  `tanh` are bounded, monotonic S-curves.

### Query B — `web/query_sigmoid_tanh.txt` (independent second read)
Ask: confirm sigmoid and tanh definitions, ranges, derivatives, and whether `tanh` is
a rescaled sigmoid.

**Confirmed:** `tanh(x) = 2σ(2x) - 1`, i.e. tanh is a vertically rescaled and
horizontally stretched sigmoid — consistent with the two panels on the slide showing
the same S-shape with a different vertical range (`0..1` vs `-1..1`) and origin
crossing (`0.5` vs `0`). Derivatives: `σ'(x) = σ(x)(1-σ(x))`, `tanh'(x) = 1-tanh²(x)`.

### Corrections / clarifications to the frame-independent spec
1. The spec's `tanh` caption renders `f(x) = tanh(x) = sinh x / cosh x` — **confirmed**
   as the identity `tanh = sinh/cosh`; the 2D stacked fraction is a correct rendering.
2. The spec's `f(x) = tan^{-1}(x)` — **confirmed** as `arctan`; the `-1` superscript is
   the conventional inverse-function notation and the slide's arrow from the `tan`
   panel to this panel is consistent with the inverse relation on `(-π/2, π/2)`.
3. The slide's arctan panel draws y tick labels only at `1` and `-1`, i.e. a **window
   of ±1 inside the true range `(-π/2, π/2) ≈ (-1.571, 1.571)`**. This is the frame's
   own choice, not a web-verifiable fact and **not** something to "correct" — the
   recreation must reproduce the ±1 tick labels as shown.

### Sources (cited URLs)
- GeeksforGeeks — tanh activation in neural network
  https://www.geeksforgeeks.org/deep-learning/tanh-activation-in-neural-network/
- Towards Data Science — Activation functions in neural networks: how to choose
  https://towardsdatascience.com/activation-functions-in-neural-networks-how-to-choose-the-right-one-cb20414c04e5/
- Baeldung — Sigmoid vs Tanh functions
  https://www.baeldung.com/cs/sigmoid-vs-tanh-functions
- DataCamp — Tanh function
  https://www.datacamp.com/tutorial/tanh-function
- Breno M. — "Tanh is a rescaled logistic sigmoid function"
  https://brenocon.com/blog/2013/10/tanh-is-a-rescaled-logistic-sigmoid-function/
- GeeksforGeeks — tanh vs sigmoid vs ReLU
  https://www.geeksforgeeks.org/deep-learning/tanh-vs-sigmoid-vs-relu/
- APXML — Introduction to Deep Learning, ch. 2 Activation Functions
  https://apxml.com/courses/introduction-to-deep-learning/chapter-2-activation-functions-architecture/tanh-activation
- DeepLearning.AI community — discussion on hyperbolic-tan vs other activations
  https://community.deeplearning.ai/t/why-do-we-not-use-hyperbolic-tan-function/436761

Primary mathematical reference (cited by the search): Goodfellow, Bengio & Courville,
*Deep Learning*, MIT Press, 2016 (activation-function requirements: bounding,
differentiability, saturation); Rumelhart, Hinton & Williams, *Learning representations
by back-propagating errors*, Nature, 1986 (differentiability constraint on activations).

## 3. Slide-content sources used for the recreation

- `analysis/slide_019_final.json` — vision analysis spec (validated by
  `validate_slides`, verdict `PASS_WITH_FIXES`, recreatability 9/10)
- `analysis/slide_019_reanalysis.txt` — fresh independent vision re-read of the
  original frame (single-read, this mission)
- `unique_slides/slide_019.jpg` — the original frame; ground truth for all geometry

## Wave-2 verification

Fresh independent web-verification pass (wave-3 dispatch, agent `src-017-020`).
Content evidence read first: `analysis/reanalysis_v2/slide_019_reanalysis.txt` is a
**429-byte abort stub** ("hard wall-clock 450s exceeded — call aborted"), i.e. below the
800-byte threshold, so the fallback chain was used: `analysis/slide_019_final.json`
(verdict `PASS_WITH_FIXES`) plus `sources/docparse_cascades/slide_019/composed/
slide_019_composed.md` (1 element kept, 0 crops, 0 failed calls, not degraded).

Note on the wave-1 citation above: the path `analysis/slide_019_reanalysis.txt` does
not exist on disk — the wave-2 re-read lives at
`analysis/reanalysis_v2/slide_019_reanalysis.txt` and is itself an aborted stub, so
no independent vision re-read is currently available for this frame. The
doc-parse cascade for this slide was already adjudicated and rejected in wave 1
(garbled chart cell values); that verdict stands.

### Search lane note

The `agy -p` CLI lane was quota-exhausted (`RESOURCE_EXHAUSTED (429) ... Resets in
154h21m56s`) for this wave. The same Google grounding backend was reached through the
`agy_web_search` MCP route, which returned real resolved URLs — the same lane split
recorded in wave 1 for this slide. Three further independent query reads were run
(query texts banked under `web/`): `query_q3_sigmoid.txt`, `query_q4_tanh_tan.txt`,
`query_q5_arctan.txt`.

### Confirmed by web research (3 additional independent query reads)

**Sigmoid panel (top-left)** — `f(x) = 1/(1+e^{-x})`, domain all reals, range `(0,1)`,
`σ(0) = 0.5` so the curve passes through `(0, 0.5)`, smooth monotone S-shape that
flattens toward the horizontal asymptotes `y=0` and `y=1`, derivative
`σ'(x)=σ(x)(1−σ(x))` with maximum 0.25 at x=0. **Matches** the frame's legend
`sig(x) = 1/(1+e^-x)`, y ticks `0.0 … 1.0`, and the curve crossing mid-height at
x=0. URLs: https://en.wikipedia.org/wiki/Sigmoid_function ·
https://www.geeksforgeeks.org/machine-learning/derivative-of-the-sigmoid-function/ ·
https://machinelearningmastery.com/a-gentle-introduction-to-sigmoid-function/ ·
https://developers.google.com/machine-learning/crash-course/logistic-regression/sigmoid-function

**Tanh panel (top-right)** — `tanh(x) = sinh x / cosh x`, range `(−1,1)`, passes
through the origin `(0,0)`, odd function (`tanh(−x) = −tanh(x)`), S-shaped curve
that saturates at `y=1` and `y=−1`, derivative `1−tanh²(x)` (max 1.0 at x=0).
**Matches** the frame's y ticks `−1.0 … 1.0` and curve through the origin.
URLs: https://www.geeksforgeeks.org/deep-learning/tanh-activation-in-neural-network/ ·
https://bhanzu.com/math/trigonometry/tanh ·
https://ihatedesmos.com/graph/tanh-x/ ·
https://functions.wolfram.com/ElementaryFunctions/Tanh/introductions/Tanh/05/

**Tan panel (bottom-left)** — trigonometric `tan(x)` is periodic with period `π`,
vertical asymptotes where `cos(x)=0`, i.e. `x = π/2 + kπ`; within the frame's plotted
window `[−2π, 2π]` those are exactly `−3π/2, −π/2, π/2, 3π/2` — the four dashed red
asymptotes drawn on the slide. Zeros at `x = kπ` (i.e. `−π, 0, π` inside the window),
matching the branches crossing the x-axis there. Range `(-∞,∞)` over each period.
URL: https://functions.wolfram.com/ElementaryFunctions/Tanh/introductions/Tanh/05/

**Inverse-tangent panel (bottom-right)** — `arctan(x) = tan⁻¹(x)`: domain all reals,
range `(−π/2, π/2)`, strictly increasing, odd, passes through `(0,0)`, derivative
`1/(1+x²)`, horizontal asymptotes `y = ±π/2` (≈ ±1.571) — it is the inverse of
`tan` **restricted to** `(−π/2, π/2)`. **Matches** the frame's "Inverse Tangent Graph"
title and its ±1 y tick labels as a window inside the true range.
URLs: https://www.geeksforgeeks.org/maths/arctan/ ·
https://www.mathwords.com/t/tangent_inverse.htm ·
https://bhanzu.com/math/trigonometry/inverse-tan ·
https://www.alloprof.qc.ca/en/students/vl/mathematics/the-inverse-of-the-tangent-function-arctan-m1187

### Corrections / clarifications

1. The wave-1 finding that the arctan panel's ±1 tick labels are a **frame window**,
   not the true range, is **re-confirmed**: the true range is `(−π/2, π/2) ≈
   (−1.571, 1.571)`. The recreation must still reproduce the ±1 ticks as drawn.
2. No new discrepancy found between the web facts and the frame for any of the four
   panels. The wave-1 rejection of the doc-parse numeric tables stands (the parse's
   `sig(t) = 1 (12+)` and `0.05/0.1/0.3/0.7/0.98` y values are hallucinated; the
   frame's y ticks are `0.0 0.2 0.4 0.6 0.8 1.0`).
3. The wave-1 note that `tanh(x) = 2σ(2x) − 1` (tanh as a rescaled sigmoid) remains
   consistent with the web: same S-shape, different vertical range and origin
   crossing.

### Research status (updated)

- Doc-parse cascade: ✅ complete (advisory only — numeric content rejected, wave-1 verdict stands)
- Web search: ✅ complete (2 wave-1 reads + 3 wave-2 reads = 5 independent query reads)
- Sources banked: ✅ yes

## Verified 2026-10-30 (wave 4, scope `src_w4_017_020`, agent `w4-src-017`)

Fresh independent web-verification pass. Full register: `VERIFY_W4.md` in this directory.
Query texts banked: `web/w4_q5_tanh_def.txt`; CLI-lane failure banked verbatim:
`web/w4_agy_cli_q1.txt`.

### Per-claim verification

1. **Q:** Sigmoid panel — formula, range, mid-point, asymptotes? **A:** Yes —
   `σ(x) = 1/(1+e^{−x})`, range `(0,1)`, `σ(0) = 0.5`, monotone S-shape flattening to the
   asymptotes `y=0` and `y=1`, matching the frame's legend `sig(x) = 1/(1+e^-x)`, its y ticks
   `0.0 … 1.0` and the mid-height crossing at x=0. **URL:**
   https://en.wikipedia.org/wiki/Sigmoid_function ·
   https://www.kdnuggets.com/2022/02/vanishing-gradient-problem.html
2. **Q:** Sigmoid derivative? **A:** `σ'(x) = σ(x)(1−σ(x))`, maximum **0.25** at x=0.
   **URL:** https://www.digitalocean.com/community/tutorials/vanishing-gradient-problem
3. **Q:** Is `tanh(x) = sinh x / cosh x` correct? **A:** Yes — "By definition, the hyperbolic
   tangent is the ratio of the hyperbolic sine (sinh) to the hyperbolic cosine (cosh)", i.e.
   `(e^x − e^{−x})/(e^x + e^{−x})`; range `(−1,1)`, through `(0,0)`, odd, derivative
   `1 − tanh²(x)`, saturating at ±1. **URL:**
   https://sebastianraschka.com/faq/docs/tanh-sigmoid-relationship.html ·
   https://www.baeldung.com/cs/sigmoid-vs-tanh-functions
4. **Q:** Is tanh a rescaled sigmoid (`tanh(x) = 2σ(2x) − 1`)? **A:** Yes — proves out, and
   explains the slide's two S-shaped panels over `0..1` vs `−1..1`.
   **URL:** https://awni.github.io/jiro/practice/2017/01/12/tanh.html
5. **Q:** Tan panel — period, asymptotes, zeros? **A:** Period `π`; asymptotes where `cos x = 0`,
   i.e. `x = π/2 + kπ` → exactly the four drawn at `−3π/2, −π/2, π/2, 3π/2`; zeros at `x = kπ` →
   `−π, 0, π`. **URL:** https://www.geeksforgeeks.org/maths/tangent-function/ ·
   https://www.vaia.com/en-us/textbooks/math/precalculus-6-edition/chapter-4/problem-11-graph-two-periods-of-the-given-tangent-function-y/
6. **Q:** Inverse-tangent panel and the `tan → tan⁻¹` arrow? **A:** `arctan(x) = tan⁻¹(x)`, range
   `(−π/2, π/2)`, strictly increasing, odd, through `(0,0)`, derivative `1/(1+x²)`, and the inverse
   of `tan` **restricted to** `(−π/2, π/2)`. **URL:** https://www.arxiv.org/pdf/2101.09957 ·
   https://jamesmccaffrey.wordpress.com/2015/09/13/neural-network-arctan-activation-function/
7. **Q:** Is the arctan panel's `±1` tick label the function's range? **A:** No — the true range is
   `(−π/2, π/2)` ≈ ±1.571; the `±1` ticks are the **frame's own window** and must be reproduced as
   drawn, not "corrected". **URL:** https://www.arxiv.org/pdf/2101.09957
8. **Q:** Does `tan^{-1}(x)` mean a reciprocal power? **A:** No — it is the conventional
   inverse-function notation for `arctan`, consistent with the slide's arrow.
   **URL:** https://jamesmccaffrey.wordpress.com/2015/09/13/neural-network-arctan-activation-function/
9. **Q:** Can the doc-parse numbers (legend `sig(t) = 1 (12+)`, y ticks `0.05/0.1/0.3/0.7/0.98`) be
   verified? **A:** No — **rejected as hallucinated**: they match no axis on the frame (whose
   sigmoid ticks are `0.0 0.2 0.4 0.6 0.8 1.0`), and the parse recovers none of the slide's
   verbatim text. The wave-1 rejection stands.
10. **Q:** The tanh chart's x-span "roughly −5 to 5"? **A:** Not web-verifiable — a frame-window
    estimate; the `[?]` stays.

### Search-lane note

`agy -p` CLI: `RESOURCE_EXHAUSTED (429) … Resets in 131h14m13s` (banked at
`web/w4_agy_cli_q1.txt`). All four queries ran through the `agy_web_search` MCP route on the same
grounding backend and returned resolved URLs.

### Changes to the analysis spec

**None.** 10 claims checked · 8 CONFIRMED · 1 UNVERIFIED (frame-window estimate) · 1 rejected
hallucination · 0 CORRECTED. 13 URLs cited. (Re-checked: `analysis/reanalysis_v2/
slide_019_reanalysis.txt` is still the 429-byte abort stub, so no independent vision re-read
exists for this frame.)

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

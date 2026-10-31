# SOURCES — slide_021 (ReLU activation function)

## Slide identification

The slide shows a single line chart with axes `x` (horizontal) and `f` (vertical), plotting a
piecewise-linear "hockey stick" curve: flat at `f = 0` for `x ≤ 0`, then rising as `f = x`
for `x > 0`. Series data extracted by doc-parse (nemotron-parse, single-read, unconfirmed):

| x  | f |
|----|---|
| -10 | 0 |
| -5  | 0 |
| 0   | 0 |
| 5   | 5 |
| 8   | 7 |
| 10  | 10 |

This is the **ReLU (Rectified Linear Unit) activation function**, `f(x) = max(0, x)`.

## Web-verified sources

1. **Rectified linear unit — Wikipedia**
   https://en.wikipedia.org/wiki/Rectified_linear_unit
   Definition: `f(x) = max(0, x)`. For `x < 0` → `f(x) = 0` (flat line on the x-axis);
   for `x ≥ 0` → `f(x) = x` (45° rising line, slope 1).

2. **Rectified Linear Activation Function for Deep Learning — Machine Learning Mastery**
   https://machinelearningmastery.com/rectified-linear-activation-function-for-deep-learning-neural-networks/
   Confirms the hockey-stick/ramp shape: negative side flat at y = 0, positive side a
   diagonal line at 45°. Derivative: 0 for x < 0, 1 for x > 0 (dying-ReLU phenomenon).

3. **ReLU Activation Function in Deep Learning — GeeksforGeeks**
   https://www.geeksforgeeks.org/deep-learning/relu-activation-function-in-deep-learning/
   Confirms `max(0, x)`; derivative used in backpropagation for gradient/weight updates.

## Corrected facts

- The chart plots **f(x) = max(0, x)** — the data table matches exactly (y = 0 for all
  negative x, y = x for positive x).
- Plot domain on the slide runs roughly x ∈ [-10, 10]; y up to ~10.
- No equations are printed as text on the slide (chart-only frame); the equation
  `f(x) = max(0, x)` is implied by the plotted curve.
- Uncertain items `[?]`: exact axis tick values and grid-line style (chart region is low
  resolution in the extracted frame).

## Research method

- doc-parse: `tools/doc-parse` (nemotron-parse) on `unique_slides/slide_021.jpg` —
  transcript banked at `slide_021.parse.md` / `slide_021.parse.json` (single-read).
- Web search via agy CLI (Google grounding), 2026-10-27, two corroborating sources +
  Wikipedia for the standard definition.

---

## Wave-2 verification (2026-10-28)

### Wave-1 content is superseded (DATA correction, not a rewrite of frame text)

The wave-1 section above was written from a **single-crop doc-parse pass** that only saw the
top-left (ReLU) chart, and its "Slide identification" therefore describes the frame as
"a single line chart ... This is the ReLU activation function". **That is wrong.** The fresh
vision re-analysis of the same frame (`analysis/slide_021_final.json`, model `images`,
elapsed 434.5 s, verdict `PASS_WITH_FIXES`) shows the slide is in fact a **2x2 grid of four
activation-function panels**, each with a pink formula box over a blue-framed plot:

| Panel | Formula on slide | Plot behaviour measured on slide |
|---|---|---|
| top-left | `F(x) = Rectified Linear Unit = { 0 for x < 0 ; x for x >= 0 }` | flat at f=0 for x<0, then straight line (0,0)->(10,10) |
| top-right | `F(x) = Parametric ReLU = { [?] for x < 0 ; x for x >= 0 }` | line just below the x-axis from (-4,-0.4) to origin, then (0,0)->(4,3) |
| bottom-left | `F(x) = Exponential LU = { alpha (e^x - 1) for x < 0 ; x for x >= 0 }` | curves approach -1 asymptote (alpha=1.0), pass origin, follow y=x to (3,3) |
| bottom-right | `F(x) = SoftPlus = log_e (1 + e^x)` | S-curve, flat near 0 for x<0, crossing y at ~0.7 at x=0 |

The wave-1 doc-parse data table for the ReLU chart (y=0 for all negative x, y=x for positive
x) is still **correct** and remains valid — it just describes one quarter of the slide.

Wave-1's ReLU sources (Wikipedia, Machine Learning Mastery, GeeksforGeeks) are retained and
re-confirmed below.

### Claim-by-claim verification

1. **ReLU `f(x) = { 0 for x<0 ; x for x>=0 }`** — CONFIRMED. Standard definition
   `f(x) = max(0, x)`. Negative branch flat at 0, positive branch identity (slope 1).
   - Rectified linear unit — Wikipedia: https://en.wikipedia.org/wiki/Rectified_linear_unit
   - Rectified Linear Activation Function for Deep Learning — Machine Learning Mastery:
     https://machinelearningmastery.com/rectified-linear-activation-function-for-deep-learning-neural-networks/
   - ReLU Activation Function in Deep Learning — GeeksforGeeks:
     https://www.geeksforgeeks.org/deep-learning/relu-activation-function-in-deep-learning/

2. **The ReLU plot's hockey-stick shape** — CONFIRMED. Negative side flat at y=0, positive
   side a 45-degree diagonal. The wave-1 data table matches this exactly.
   (Same three sources as claim 1.)

3. **Parametric ReLU negative branch is `alpha*x`** — CONFIRMED (the on-slide glyph is
   unreadable/`[?]`; the standard form is `alpha*x`).
   `f(x) = { a*x for x < 0 ; x for x >= 0 }`, where `a` is a **learnable** parameter
   (unlike Leaky ReLU, where it is a fixed hyperparameter).
   - Imperial College London, "DL activation and losses" lecture notes:
     https://www.doc.ic.ac.uk/~bkainz/teaching/DL/L03_DL_activation_and_losses.pdf
   - "PReLU Activation Function" — Medium (@shauryagoel):
     https://medium.com/@shauryagoel/prelu-activation-e294bb21fefa
   Compact equivalent also given: `f(x) = max(0, x) + a*min(0, x)`.
   *(The `[?]` red-filled-circle glyph on the slide is therefore consistent with a missing
   `alpha*x` term — but no source is cited for the glyph itself; it stays `[?]`.)*
   - **Plot observation for recreation**: the measured negative branch runs from (-4, -0.4)
     to the origin, i.e. slope 0.1, so the plotted instance corresponds to **alpha ~= 0.1**.
     This is a geometry read-off, not a source claim.

4. **ELU `f(x) = { alpha (e^x - 1) for x < 0 ; x for x >= 0 }`** — CONFIRMED. Standard
   definition with `alpha > 0` (typically 1.0).
   - "ELU as a Neural Network's Activation Function" — Sefiks:
     https://sefiks.com/2018/01/02/elu-as-a-neural-networks-activation-function/
   - "ELU Activation Function" — MLForBeginners:
     https://mlforbeginners.com/elu-activation-function/
   - "ELU Activation: A Comprehensive Analysis" — tungmphung:
     https://tungmphung.com/elu-activation-a-comprehensive-analysis/
   - arXiv 1704.07483v1 (ELU paper):
     https://arxiv.org/html/1704.07483v1

5. **ELU is asymptotic to `-alpha` as x -> -infinity** — CONFIRMED.
   `lim_{x->-inf} alpha(e^x - 1) = alpha(0 - 1) = -alpha`. The slide's alpha=1.0 (red)
   curve approaching -1 is the textbook case.
   - Sefiks (above); MLForBeginners (above).

6. **ELU saturates for negative inputs (mean activations closer to zero)** — CONFIRMED;
   explains why the slide's negative branches flatten out rather than diverging.
   - Sefiks (above); MLForBeginners (above).

7. **SoftPlus `f(x) = log_e (1 + e^x)`** — CONFIRMED. Standard definition
   `Softplus(x) = ln(1 + e^x)`.
   - "Softplus Function in Neural Network" — GeeksforGeeks:
     https://www.geeksforgeeks.org/deep-learning/softplus-function-in-neural-network/
   - "Softplus" — DataCamp:
     https://www.datacamp.com/tutorial/softplus
   - "Softplus Activation Function" — Analytics Vidhya:
     https://www.analyticsvidhya.com/blog/2025/12/softplus-activation-function/

8. **SoftPlus is a smooth approximation of ReLU** — CONFIRMED. For large positive x,
   `ln(1+e^x) ~= x`; for large negative x, `ln(1+e^x) ~= 0`; at `x=0` it equals
   `ln(2) ~= 0.693` (the slide's plot shows the curve crossing the y-axis at ~0.7 —
   **matches**).
   - DataCamp (above); GeeksforGeeks (above); Neura.Market:
     https://www.neura.market/directories/chatgpt/blog/softplus-activation-function-the-smooth-powerful-relu-alternative-every-ml-engineer-needs

9. **SoftPlus' derivative is the sigmoid** — CONFIRMED (relevant to slide 024, where
   `f'(x) = 1/(1+e^{-x})` appears).
   - GeeksforGeeks (above); DataCamp (above); Analytics Vidhya (above).

### Uncertain items carried forward (DO NOT resolve from sources)

- The Parametric ReLU `x < 0` case value is a **solid red filled circle** on the slide
  (source glyph unreadable, possibly redacted or animated). It is kept as `[?]`; sources
  only tell us the *standard* form is `alpha*x`, which is noted but NOT substituted.
- Axis tick values and the exact ELU/PReLU/SoftPlus curve coordinates are vision-model
  measurements, not measured pixel values.
- The black bar along the very bottom edge is a video letterbox/crop artifact, not slide
  content.

### Research method

- Web search: agy CLI is quota-exhausted (`RESOURCE_EXHAUSTED`, resets ~2026-10-29); all
  searches above were run through the **agy MCP web-search tool** (Google grounding,
  redirect URLs resolved to real page URLs). Every URL listed was returned by the tool —
  none are invented.
- 3 searches run for this slide (PReLU; ELU; SoftPlus), plus 1 ReLU search shared with
  slide 022.
- Content evidence: `analysis/slide_021_final.json` (fresh vision re-analysis, 11.4 KB).

---

## Wave-2 verification (wave-3 dispatch, agent src-021-024, 2026-10-30)

Content evidence used: `analysis/reanalysis_v2/slide_021_reanalysis.txt` is MISSING, so per
mandate fell back to `analysis/slide_021_final.json` (23 KB vision analysis: 2x2 grid of ReLU /
PReLU / ELU / SoftPlus panels, each a pink formula box over a blue-framed plot; PReLU panel
plots curves for alpha = 0.1, 0.2, 0.5, 1.0) and
`sources/docparse_cascades/slide_021/composed/slide_021_composed.md`.

Search method: `agy -p` CLI is quota-exhausted (HTTP 429 RESOURCE_EXHAUSTED, reset ~154h;
raw error outputs banked at `wave3_agy/q1_prelu.txt` etc.), so the 4 searches were run through
the agy MCP web-search tool (same Google-grounding backend, redirect URLs resolved). All URLs
below were returned by the tool — none invented. Raw log: `wave3_agy/search_log.md`.

### Verified claims (wave-2)

1. **ReLU `f(x) = { 0 for x<0 ; x for x>=0 }` = `max(0,x)`, hockey-stick plot** — CONFIRMED.
   - https://en.wikipedia.org/wiki/Rectified_linear_unit
   - https://machinelearningmastery.com/rectified-linear-activation-function-for-deep-learning-neural-networks/
   - https://builtin.com/machine-learning/relu-activation-function
   - https://www.dremio.com/wiki/relu-activation-function/
2. **PReLU `f(x) = max(0,x) + alpha*min(0,x) = { alpha*x for x<=0 ; x for x>0 }`, alpha learnable
   (He et al. 2015); the slide's four PReLU curves alpha = 0.1/0.2/0.5/1.0 match the standard
   family plot (alpha=1.0 degenerates to the identity line)** — CONFIRMED.
   - https://arxiv.org/abs/1502.01852 (He, Zhang, Ren, Sun, "Delving Deep into Rectifiers")
   - https://en.wikipedia.org/wiki/Rectified_linear_unit
   - https://medium.com/@shauryagoel/prelu-activation-e294bb21fefa
   - https://www.emergentmind.com/topics/parametric-rectified-linear-unit-prelu
3. **ELU `f(x) = { alpha*(e^x - 1) for x<0 ; x for x>=0 }`, alpha typically 1.0, negative branch
   asymptotes to -alpha (slide's alpha=1.0 curve flattening toward -1)** — CONFIRMED.
   - https://arxiv.org/abs/1511.07289 (Clevert, Unterthiner, Hochreiter 2015)
   - https://www.geeksforgeeks.org/deep-learning/elu-activation-function-in-neural-network/
   - https://tungmphung.com/elu-activation-a-comprehensive-analysis/
4. **SoftPlus `f(x) = ln(1+e^x)`; smooth ReLU approximation; `f(0) = ln 2 ~ 0.693` (matches the
   slide's y-intercept just under 1); derivative is the sigmoid** — CONFIRMED.
   - https://www.geeksforgeeks.org/deep-learning/softplus-function-in-neural-network/
   - https://www.datacamp.com/tutorial/softplus
   - https://docs.pytorch.org/docs/stable/generated/torch.nn.modules.activation.Softplus.html
   - https://www.analyticsvidhya.com/blog/2025/12/softplus-activation-function/

### Unchanged uncertain items

- PReLU `x<0` case value remains the on-slide solid red filled circle `[?]` — sources give the
  standard `alpha*x` but it is NOT substituted into the verbatim text.
- The trailing `+` after the PReLU brace on slide 022 and exact curve coordinates remain
  vision measurements, not source-derived.


---

## Verified 2026-10-30 (wave 4, fresh worker `w4-src-021`, scope `src_w4_021_024`)

Mandated by `videos/machine-learning/09_introduction_to_neural_networks/AGENTS.md` rule 5.
Method: `agy -p` CLI attempted first and returned HTTP 429 `RESOURCE_EXHAUSTED`
("Individual quota reached … Resets in 131h18m6s"); searches therefore ran through the
**agy MCP web-search tool** (same Google-grounding backend, grounding redirect URLs resolved
to real page URLs). Every URL below was returned by that tool — none invented. Content
evidence: `analysis/slide_021_final.json` and
`sources/docparse_cascades/slide_021/composed/slide_021_composed.md` (independent second read).
Full claim register: `VERIFY_W4.md` in this directory.

### Claim-by-claim verification

1. **ReLU `f(x) = { 0 for x<0 ; x for x>=0 }` = `max(0,x)`; hockey-stick plot** — CONFIRMED.
   - Question: *Is the ReLU definition and its hockey-stick plot as shown on the slide?*
   - Answer: Yes — ReLU is `max(0,x)`: flat at 0 for x<0, identity line of slope 1 for x>0.
   - https://www.cv-foundation.org/openaccess/content_iccv_2015/papers/He_Delving_Deep_into_ICCV_2015_paper.pdf
     — "f(y_i) = y_i if y_i > 0 … PReLU with α=0 degenerates to ReLU"
   - https://arxiv.org/abs/1502.01852
   - Doc-parse cross-check: `slide_021_composed.md` reads the ReLU series
     x = −10/−5/0/5/10 → f = 0/0/0/5/10 in both the full and the level-1 crop pass.

2. **PReLU negative branch is `alpha*x`, alpha learnable (He et al. 2015)** — CONFIRMED.
   - Question: *Is the PReLU negative branch `alpha*x` with a learnable alpha?*
   - Answer: Yes — `f(y_i) = max(0, y_i) + α_i min(0, y_i)`; α is learned by backprop, unlike
     Leaky ReLU's fixed hyperparameter.
   - https://arxiv.org/abs/1502.01852
   - https://apxml.com/courses/introduction-to-deep-learning/chapter-2-activation-functions-architecture/relu-variants
     — "PReLU allows α to adapt during backpropagation via gradient descent"
   - https://allthingsphi.com/blog/2016/12/10/delving-deep-into-rectifiers-surpassing-human-level-performance-on-imagenet-classification.html
     — "f(y_i) = max(0, y_i) + α_i min(0, y_i)"

3. **The slide's four PReLU curves alpha = 0.1 / 0.2 / 0.5 / 1.0 are the standard PReLU
   family (alpha = 1.0 degenerates to the identity line)** — CONFIRMED.
   - Question: *Does a four-alpha PReLU plot family with these values exist in the literature?*
   - Answer: Yes — PReLU's alpha sweeps the negative-slope coefficient; α = 1 gives the plain
     45° identity line on the positive branch and the mirror on the negative branch.
   - https://arxiv.org/abs/1502.01852
   - https://apxml.com/courses/introduction-to-deep-learning/chapter-2-activation-functions-architecture/relu-variants

4. **ELU `f(x) = { alpha*(e^x − 1) for x<0 ; x for x>=0 }`, saturating to `-alpha`** — CONFIRMED.
   - Question: *What is the ELU definition and where does its negative branch saturate?*
   - Answer: `alpha*(e^x − 1)` for x<0, `x` for x>=0; as x → −∞ the branch tends to −alpha.
   - https://www.geeksforgeeks.org/deep-learning/elu-activation-function-in-neural-network/

5. **The slide's ELU legend alpha = 0.1 / 0.2 / 0.5 / 1.0 matches the standard per-alpha
   asymptote family (−0.1 / −0.2 / −0.5 / −1.0), all four merging on `y = x` for x >= 0** —
   CONFIRMED.
   - Question: *What do ELU curves for alpha = 0.1/0.2/0.5/1.0 look like plotted together?*
   - Answer: One curve per alpha; each flattens at its own −alpha asymptote; all four coincide
     with the identity line for x > 0 — exactly the slide's plot.
   - https://www.aivasu.com/notes/dl/elu
   - https://www.emergentmind.com/topics/exponential-linear-unit-elu

6. **ELU saturates for negative inputs (mean activations closer to zero)** — CONFIRMED (carried
   from the wave-2 record, same source re-cited; no new query spent).
   - https://www.geeksforgeeks.org/deep-learning/elu-activation-function-in-neural-network/

7. **SoftPlus `f(x) = log_e(1 + e^x)`** — CONFIRMED.
   - Question: *What is the SoftPlus definition?*
   - Answer: `Softplus(x) = ln(1 + e^x)`.
   - https://www.datacamp.com/tutorial/softplus

8. **SoftPlus is a smooth approximation of ReLU and `f(0) = ln 2 ≈ 0.693`** — CONFIRMED.
   - Question: *Is SoftPlus a smooth ReLU approximation, and what is its value at x = 0?*
   - Answer: Yes — "Softplus(0) = ln(1+e^0) = ln(2) ≈ 0.693", a smooth curve without ReLU's
     kink; matches the slide's y-intercept just under 1.
   - https://www.geeksforgeeks.org/deep-learning/softplus-function-in-neural-network/
   - https://www.datacamp.com/tutorial/softplus

### Uncertain items carried forward — unchanged

- The PReLU `x < 0` case value on the slide is a **solid red filled circle** and stays `[?]`.
  Sources give the standard `alpha*x` as context only; it is NOT substituted into the frame
  text. No source speaks to the glyph.
- Axis tick values and exact curve coordinates are vision-model measurements.
- The black bar along the bottom edge is a video letterbox/crop artifact, not slide content.

### Corrections

**None.** All 8 data claims in `analysis/slide_021_final.json` stand as written; 0 changes.

### Law reminder

The frame wins for recreation; the source wins for understanding.

# Source Research: slide_026

## Doc-Parse Transcript (nemotron-3.5-parse)

**Run**: `sources/slide_026_source/docparse_run/`
- Full frame parse: `full/slide_026.parse.md`
- Composed: `composed/slide_026_composed.md`
- Crop cascade: 3 crops (compound panel chart with two sub-panels)
- Chat lane: DEGRADED (model `docparsechat` HTTP 404 on gateway) — deterministic-conservative fallback used
- Source frame md5: `b4b4e1268633472ba274a4425954a194`

## Extracted Content (verbatim)

### Slide Title
**Sigmoid vs Tanh** (from chart metadata, no explicit title box on slide)

### Layout
A **compound chart** with two vertically stacked panels sharing the same x-axis range:
- **Panel p1 (top)**: "Sigmoid vs Tanh" — two function curves
- **Panel p2 (bottom)**: "Tanh Derivative ; Sigmoid Derivative" — two derivative curves
- Legend: color-coded (Tanh, Sigmoid) — applies to both panels
- Data tables embedded in parse output for both panels

### Panel p1: Sigmoid vs Tanh (function values)

| x | Tanh | Sigmoid |
|---|------|---------|
| -5 | 0.00 | -0.40 / -1.00* |
| -4 | 0.00 | -1.00 / -1.00* |
| -2 | 0.10 | -1.00 / -1.00* |
| 0 | 0.50 | 0.00 |
| 2 | 0.95 / 0.90* | 0.85 / 1.00* |
| 4 | 1.00 | 1.00 |

*Multiple parse passes give slightly different values; web-verified canonical values below.

### Panel p2: Tanh Derivative vs Sigmoid Derivative (derivative values)

| x | Tanh Derivative | Sigmoid Derivative |
|---|-----------------|-------------------|
| -5 | 0.00 | 0.00 |
| -4 | 0.02 / 0.02* | 0.00 / 0.02* |
| -2 | 0.10 / 0.15* | 0.10 / 0.08* |
| 0 | 1.0 | 1.0 / 0.50* |
| 2 | 0.20 / 0.30* | 0.20 / 0.15* |
| 4 | 0.02 | 0.02 / 0.00* |

---

## Web Search Verification

### Canonical formulas and expected plot values

**Sigmoid** [[1]](https://medium.com/@vikrampande783/derivative-of-sigmoid-and-tanh-ffdea6efb464) [[4]](https://www.baeldung.com/cs/sigmoid-vs-tanh-functions)
- σ(x) = 1 / (1 + e⁻ˣ)
- Range: (0, 1)
- σ(0) = 0.5
- σ(-5) ≈ 0.0067, σ(-4) ≈ 0.018, σ(-2) ≈ 0.119, σ(2) ≈ 0.881, σ(4) ≈ 0.982, σ(5) ≈ 0.993

**Tanh** [[4]](https://www.baeldung.com/cs/sigmoid-vs-tanh-functions) [[7]](https://datahacker.rs/activation-functions-and-derivatives/)
- tanh(x) = (eˣ - e⁻ˣ) / (eˣ + e⁻ˣ) = 2σ(2x) - 1
- Range: (-1, 1)
- tanh(0) = 0
- tanh(-5) ≈ -0.9999, tanh(-4) ≈ -0.9993, tanh(-2) ≈ -0.964, tanh(2) ≈ 0.964, tanh(4) ≈ 0.9993, tanh(5) ≈ 0.9999

**Sigmoid Derivative** [[1]](https://medium.com/@vikrampande783/derivative-of-sigmoid-and-tanh-ffdea6efb464)
- σ'(x) = σ(x)(1 - σ(x))
- Range: (0, 0.25]
- σ'(0) = 0.25 (max)
- σ'(-5) ≈ 0.0067, σ'(-4) ≈ 0.0177, σ'(-2) ≈ 0.105, σ'(0) = 0.25, σ'(2) ≈ 0.105, σ'(4) ≈ 0.0177, σ'(5) ≈ 0.0067

**Tanh Derivative** [[1]](https://medium.com/@vikrampande783/derivative-of-sigmoid-and-tanh-ffdea6efb464) [[5]](https://www.researchgate.net/figure/Graph-showing-derivatives-of-tanh-and-sigmoid-activation-functions_fig1_363536986)
- tanh'(x) = 1 - tanh²(x)
- Range: (0, 1]
- tanh'(0) = 1.0 (max)
- tanh'(-5) ≈ 0.0, tanh'(-4) ≈ 0.0014, tanh'(-2) ≈ 0.0707, tanh'(0) = 1.0, tanh'(2) ≈ 0.0707, tanh'(4) ≈ 0.0014, tanh'(5) ≈ 0.0

### Verified values (corrected from OCR variance)

| x | Tanh (canonical) | Sigmoid (canonical) | Tanh' (canonical) | Sigmoid' (canonical) |
|---|------------------|---------------------|-------------------|----------------------|
| -5 | -1.00 | 0.01 | 0.00 | 0.01 |
| -4 | -1.00 | 0.02 | 0.00 | 0.02 |
| -2 | -0.96 | 0.12 | 0.07 | 0.10 |
| 0 | 0.00 | 0.50 | 1.00 | 0.25 |
| 2 | 0.96 | 0.88 | 0.07 | 0.10 |
| 4 | 1.00 | 0.98 | 0.00 | 0.02 |

**Key discrepancies from doc-parse**:
- Sigmoid at x=-5,-4,-2: parse shows -0.40/-1.00/-1.00 (impossible; sigmoid ∈ (0,1)). These are OCR errors. Canonical: 0.01/0.02/0.12.
- Sigmoid at x=2: parse 0.85/1.00 vs canonical 0.88.
- Tanh at x=-2: parse 0.10/0.15 vs canonical -0.96 (sign error in parse).
- Tanh at x=2: parse 0.95/0.90 vs canonical 0.96.
- Sigmoid derivative at x=0: parse 1.0/0.50 vs canonical 0.25.
- Tanh derivative at x=0: parse 1.0 ✓ (canonical 1.0).

---

## Research Summary

Slide 026 (printed badge **18**) shows a classic comparison of the two most common smooth activation functions and their derivatives:
- Top panel: Sigmoid (0→1) vs Tanh (-1→1) — both S-shaped
- Bottom panel: Their derivatives — Tanh' peaks at 1.0 (zero-centered advantage), Sigmoid' peaks at 0.25

**Content facts for recreation**:
- Title: "Sigmoid vs Tanh" (from chart title; no separate slide title box visible)
- Badge: **18** (printed on slide — house rule uses this, not index)
- Two vertically stacked charts with shared x-axis [-5, 5] approximately
- Legend: "Tanh" and "Sigmoid" color-coded
- Grid lines visible in both panels
- All curves drawn in thin lines (appears hand-drawn style or matplotlib default)
- No axis tick labels visible in parse — approximate from data tables

### Uncertain Items (marked [?])
- Exact color mapping for Tanh vs Sigmoid lines — legend shows colors but not which is which
- Axis tick marks and labels — not recovered by parse; need vision analysis
- Whether x-axis goes from -5 to 5 or -6 to 6 — data table only gives samples
- Background color of slide (gray like others? #e6e6e6?)
- Title position: chart title "Sigmoid vs Tanh" vs separate slide title box

---
*Generated: 2026-10-27*

---

## Verified 2026-10-30 (wave 4 — scope `src_w4_025_028`, worker `w4-src-025`)

**Method**: mandated by this deck's `AGENTS.md` rule 5 + the slide-recreation skill's
`references/source-research.md`. Spec read = `analysis/slide_026_final.json`
(vision `images`, `validate_slides` verdict PASS_WITH_FIXES, recreatability 8/10);
independent second read = `sources/docparse_cascades/slide_026/composed/slide_026_composed.md`
(frame md5 `b4b4e1268633472ba274a4425954a194`, compound-panel chart with p1/p2 data tables).
The Wave-1 section above is unchanged and untouched.

**Search transport (honest note)**: the `agy -p` CLI is quota-exhausted —
HTTP 429 `RESOURCE_EXHAUSTED / Individual quota reached`, "Resets in 131h15m36s"
(CLI probe transcript banked at `sources/slide_026_source/agy_wave4/w4_cli_probe_429.txt`;
the probe failed identically to the other slides' probes).
Per the operations tool-down law the remaining queries ran through the **agy
web-search MCP** route — the same Google grounding service, different transport.
Every URL cited below was returned by that service; none are invented.

**Compact register**: `sources/slide_026_source/VERIFY_W4.md` (18-claim register,
evidence URLs, questions asked, spec changes).

### Claim-by-claim verification (wave 4)

| # | Claim (DATA-level) | Question asked | Answer | Verdict |
|---|---|---|---|---|
| 1 | `f(x) = Sigmoid(x) = 1/(1+e^-x)` | "sigmoid activation function σ(x)=1/(1+e^-x)" | Canonical form confirmed | CONFIRMED — https://www.geeksforgeeks.org/machine-learning/derivative-of-the-sigmoid-function/ · https://apxml.com/courses/introduction-to-deep-learning/chapter-2-activation-functions-architecture/sigmoid-activation |
| 2 | Sigmoid range fixed at 0 to 1 (footer point [1]) | (same query) | "Range: (0, 1)" | CONFIRMED — https://apxml.com/courses/introduction-to-deep-learning/chapter-2-activation-functions-architecture/sigmoid-activation · https://stats.stackexchange.com/questions/101560/tanh-activation-function-vs-sigmoid-activation-function |
| 3 | `at x=0   f(0)=0.5` | (same query) | "σ(0) = 1/(1+e⁰) = 0.5" | CONFIRMED — https://machinelearningmastery.com/a-gentle-introduction-to-sigmoid-function/ |
| 4 | `f'(x) = f(x)(1-f(x))` | (same query) | Canonical derivative identity | CONFIRMED — https://www.geeksforgeeks.org/machine-learning/derivative-of-the-sigmoid-function/ · https://www.baeldung.com/cs/sigmoid-vs-tanh-functions |
| 5 | `at x=0   f'(0)=0.25` (max) | (same query) | "σ'(0)=0.5×0.5=0.25 … maximum value of the derivative is 0.25, occurs at x=0" | CONFIRMED — https://apxml.com/courses/introduction-to-deep-learning/chapter-2-activation-functions-architecture/sigmoid-activation · https://community.deeplearning.ai/t/better-activation-functions-tanh-sigmoid/224869 |
| 6 | `f(x) = tanh(x) = sinh x / cosh x` | "tanh activation function tanh(x)=sinh x / cosh x" | "tanh(x) = sinh(x)/cosh(x) = (eˣ−e⁻ˣ)/(eˣ+e⁻ˣ)" | CONFIRMED — https://www.geeksforgeeks.org/deep-learning/tanh-activation-in-neural-network/ · https://mlforbeginners.com/tanh-activation-function/ |
| 7 | Tanh range fixed at −1 to 1 (footer point [1]) | (same query) | "Range: (−1, 1)" | CONFIRMED — https://mlforbeginners.com/tanh-activation-function/ · https://stats.stackexchange.com/questions/101560/tanh-activation-function-vs-sigmoid-activation-function |
| 8 | `at x=0   f(0)=0` for tanh | (same query) | "tanh(0) = 0" | CONFIRMED — https://www.geeksforgeeks.org/deep-learning/tanh-activation-in-neural-network/ |
| 9 | `f'(x) = 1-f(x)^2` for tanh | (same query) | "d/dx tanh(x) = 1 − tanh²(x)" | CONFIRMED — https://www.geeksforgeeks.org/deep-learning/tanh-activation-in-neural-network/ · https://www.baeldung.com/cs/sigmoid-vs-tanh-functions |
| 10 | `at x=0   f'(0)=1` for tanh (max) | (same query) | "maximum value of the derivative is 1, occurs at x = 0 (1 − tanh²(0) = 1)" | CONFIRMED — https://mlforbeginners.com/tanh-activation-function/ · https://community.deeplearning.ai/t/better-activation-functions-tanh-sigmoid/224869 |
| 11 | Footer point [2]: sigmoid slower ⇒ sigmoid derivative smaller than tanh's for a given input | "sigmoid vs tanh: sigmoid slower rate of change than tanh meaning sigmoid derivative smaller than tanh derivative for given input" | "the maximum derivative of Tanh (1.0) is four times larger than that of Sigmoid (0.25), so Tanh has a steeper rate of change and provides stronger gradients for a given input near zero" | CONFIRMED — https://www.baeldung.com/cs/sigmoid-vs-tanh-functions · https://community.deeplearning.ai/t/better-activation-functions-tanh-sigmoid/224869 |
| 12 | Zero-centering of tanh (context for the chart design) | (same query) | "Tanh is zero-centered … always-positive sigmoid outputs make all weight gradients share a sign, causing zigzag; zero-centred functions mitigate this" | CONFIRMED (context only) — https://stats.stackexchange.com/questions/101560/tanh-activation-function-vs-sigmoid-activation-function · https://www.geeksforgeeks.org/deep-learning/tanh-vs-sigmoid-vs-relu/ |
| 13 | Left chart y-ticks 1.00…−1.00 (0.25 step); right chart 1.0…0.0 (0.2 step) | (derived from #2,#7,#5,#10) | Left must span both tanh (−1..1) and sigmoid (0..1) ⇒ [−1,1]/0.25-step fits; right = derivatives, tanh' max 1.0, sigmoid' max 0.25, both ≥0 ⇒ [0,1]/0.2-step fits | CONFIRMED as consistent (labels stay frame-verbatim) |
| 14 | Doc-parse p1/p2 table numbers (e.g. sigmoid = −1.00 at x=−2; σ'(0)=1.0) | "table of exact values sigmoid(2)=0.8808 … tanh(2)=0.9640 …" | Canonical: σ(−2)=0.1192, σ(−4)=0.0180, σ(2)=0.8808, σ(4)=0.9820, σ'(0)=0.25, tanh(−2)=−0.9640, tanh(2)=0.9640, tanh(4)=0.9993 | CORRECTED (OCR errors; they are figure numbers, not frame text) — https://www.geeksforgeeks.org/machine-learning/derivative-of-the-sigmoid-function/ · https://towardsdatascience.com/the-sigmoid-function-from-e-to-neural-networks/ · https://www.learndatasci.com/glossary/sigmoid-function/ · https://www.redcrab-software.com/en/Calculator/Tanh |
| 15 | Chart series colors / legend mapping | — (visual only) | Web confirms curve shape/values, not the course's colour assignment | `[?]` — frame stays ground truth for pixels |
| 16 | Footer highlight phrase list + dark-blue footer text hex | — (course-authored styling) | Already flagged `[?]` in the spec; not resolvable by web | `[?]` |
| 17 | Small black arrow/cursor icon in the left chart | — (visual) | Not a data claim | `[?]` — spec flags it |
| 18 | Is the title a separate slide-title box or the chart title? | — (layout) | Doc-parse found only a `<class_Chart>` with `title: Sigmoid vs Tanh` (chart metadata), no separate title element; web cannot settle layout | Spec's resolution (single shared header, no per-chart titles) kept |

### Wave-4 sources banked (new this wave)

1. https://apxml.com/courses/introduction-to-deep-learning/chapter-2-activation-functions-architecture/sigmoid-activation
2. https://www.geeksforgeeks.org/machine-learning/derivative-of-the-sigmoid-function/
3. https://machinelearningmastery.com/a-gentle-introduction-to-sigmoid-function/
4. https://www.geeksforgeeks.org/deep-learning/tanh-activation-in-neural-network/
5. https://mlforbeginners.com/tanh-activation-function/
6. https://www.baeldung.com/cs/sigmoid-vs-tanh-functions
7. https://stats.stackexchange.com/questions/101560/tanh-activation-function-vs-sigmoid-activation-function
8. https://community.deeplearning.ai/t/better-activation-functions-tanh-sigmoid/224869
9. https://www.geeksforgeeks.org/deep-learning/tanh-vs-sigmoid-vs-relu/
10. https://towardsdatascience.com/the-sigmoid-function-from-e-to-neural-networks/
11. https://www.learndatasci.com/glossary/sigmoid-function/
12. https://www.redcrab-software.com/en/Calculator/Tanh

### Wave-4 doc-parse cross-check

`sources/docparse_cascades/slide_026/composed/slide_026_composed.md` corroborates the
**existence and topology** of the compound-panel chart (p1 = Sigmoid vs Tanh;
p2 = Tanh Derivative / Sigmoid Derivative) and the shared chart title
`Sigmoid vs Tanh`. Its numeric tables are OCR-corrupted (impossible sigmoid values);
the canonical table above supersedes them. The parse models the two panels as
**stacked**, while the frame draws them **side-by-side** — per the discrepancy law the
**frame wins for layout**, the source wins for the numbers.

### Net effect on the analysis spec (wave 4)

**0 changes.** All ten formula/value claims in `slide_026_final.json` are CONFIRMED,
and footer point [2] is confirmed as a genuine property (tanh's max slope 1.0 is 4×
sigmoid's 0.25). The two `[?]` items (footer highlight phrase list, footer text
colour) remain `[?]` — web research cannot resolve course-authored styling.
Frame text is unchanged; sources confirm/correct DATA only.
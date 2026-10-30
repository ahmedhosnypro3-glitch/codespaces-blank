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
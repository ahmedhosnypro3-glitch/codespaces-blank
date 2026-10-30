# Source Research: slide_030

## Doc-Parse Transcript (nemotron-3.5-parse)

**Run**: `sources/slide_030_source/docparse_run/`
- Full frame parse: `full/slide_030.parse.md`
- Composed: `composed/slide_030_composed.md`
- Crop cascade: 1 crop (chart)
- Chat lane: DEGRADED (model `docparsechat` HTTP 404 on gateway) — deterministic-conservative fallback used
- Source frame md5: `655760a508ce96d46fdd95ee45c3a2d0`

## Extracted Content (verbatim)

### Slide Title
**Example** (subtitle: **Bad Weights**) — badge **30**

### Chart data (from full frame parse)
```
| column_1 | column_2 | column_3 |
| 0        | t6       | 0        |
| t7       | t7       | 0.1      |
| 4        | 0.5      | 0.4      |
| 5        | 0.5      | 0.5      |
```

### Crop parse (alternative table)
```
| column_1 | column_2 |
| O3       | 0.3      |
| O3       | 0.3      |
| O4       | 0.4      |
| O4       | 0.4      |
| O5       | 0.5      |
| O5       | 0.5      |
| Target   | 0        |
```

---

## Web Search Verification

### "Bad Weights" in neural network context [[1]](https://medium.com/@tam.tamanna18/understanding-the-confusion-matrix-and-its-applications-3a1c33d799af) [[2]](https://codesignal.com/learn/courses/fixing-classical-models-diagnosis-regularization/lessons/evaluating-classification-models-confusion-matrix-and-classification-report) [[3]](https://towardsdatascience.com/evaluating-ml-models-with-a-confusion-matrix-3fd9c3ab07dd/)

The term **"Bad Weights"** in neural network pedagogy typically refers to:
1. **Untrained/randomly initialized weights** — before any learning
2. **Stuck/degenerate weights** — converged to a poor local minimum
3. **Weights producing pathological outputs** — e.g., always predicting the majority class

### Interpretation of the slide

This appears to be a **visual demonstration of network outputs under bad weights**, likely showing:
- **Target vs Predicted** comparison (the "Target" row in crop parse)
- **Output neuron activations** (O3, O4, O5 with values 0.3, 0.4, 0.5 — suspiciously linear/scaled)
- **Confusion-matrix-like layout** where columns may represent classes and rows represent samples

The values `O3=0.3, O4=0.4, O5=0.5` look like **untrained sigmoid outputs** near the linear region of the sigmoid (around 0 input → 0.5 output, with small variations). The `Target=0` suggests the ground truth is class 0 but outputs are distributed across O3, O4, O5 — i.e., the network is confused.

---

## Research Summary

Slide 030 (printed badge **30**) titled **"Example — Bad Weights"** shows a chart/table demonstrating what neural network outputs look like when weights are untrained or poorly trained.

**Content facts for recreation**:
- Title: `Example` (main), `Bad Weights` (subtitle)
- Badge: **30**
- Chart type: scatter plot or table visualization
- Data shows output neuron activations (O3, O4, O5 ≈ 0.3–0.5) vs Target (0)
- The near-equal outputs across classes indicate **random/uniform guessing** — classic bad-weights behavior
- Columns may represent: sample index, target class, predicted class, or output neuron values

### Uncertain Items (marked [?])
- Exact chart type (scatter vs table vs heatmap) — pending vision
- Axis labels and scales
- Whether it's a confusion matrix, output activations plot, or something else
- Color scheme
- Badge color (yellow? same as others?)

---
*Generated: 2026-10-27*
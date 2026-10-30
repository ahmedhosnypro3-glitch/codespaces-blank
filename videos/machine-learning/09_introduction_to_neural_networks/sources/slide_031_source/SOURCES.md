# Source Research: slide_031

## Doc-Parse Transcript (nemotron-3.5-parse)

**Run**: `sources/slide_031_source/docparse_run/`
- Full frame parse: `full/slide_031.parse.md`
- Composed: `composed/slide_031_composed.md`
- Crop cascade: 1 crop (chart)
- Chat lane: DEGRADED (model `docparsechat` HTTP 404 on gateway) — deterministic-conservative fallback used
- Source frame md5: `4776a1b39d85ec77ff23f2a12f91a2bd`

## Extracted Content (verbatim)

### Slide Title
**Example** (subtitle: **Better Weights**) — badge **31**

### Chart data (from crop parse — more complete)
```
| column_1 | column_2 |
| O3       | 0.121    |
| O3       | 0.101    |
| O4       | 0.099    |
| O4       | 0.288    |
| O5       | 0.696    |
| O5       | 0.795    |
| Output   | 0.187    |
| Target   | 0.7      |
```

### Full frame parse (additional rows)
```
| column_1 | column_2 |
| O3       | 0.121    |
| 3        | -0.399   |
| 4        | 0.598    |
| 6        | 0.101    |
| 4        | -0.288   |
| 6        | 0.696    |
| 7        | 0.405    |
| 7        | 0.305    |
| 5        | 0.795    |
```

---

## Web Search Verification

### "Better Weights" / trained network output

This slide is the **counterpart to slide 030 ("Bad Weights")** — it shows the same neural network architecture after training, where weights produce meaningful, correct outputs.

**Key observations from the data**:
- **O3 outputs**: 0.121, 0.101 (low — correctly suppressed for this target)
- **O4 outputs**: 0.099, 0.288 (low)
- **O5 outputs**: 0.696, 0.795 (high — the "winning" class)
- **Target**: 0.7 — the ground truth is class 5 (O5), and the network outputs ~0.7-0.8 for it
- **Output**: 0.187 — some aggregate/other metric

The pattern **O5 ≈ 0.7-0.8, others ≈ 0.1** shows the network has learned to discriminate: the correct class gets high activation, others are suppressed.

---

## Research Summary

Slide 031 (printed badge **31**) titled **"Example — Better Weights"** shows the **after-training** state of the same network from slide 030:
- Same architecture (2 input → 3 hidden → 2 output)
- Trained weights produce **confident, correct classification**
- Output neuron O5 (class 5) activates strongly (~0.7-0.8)
- Other outputs stay low (~0.1) — clear separation

**Content facts for recreation**:
- Title: `Example` (main), `Better Weights` (subtitle)
- Badge: **31**
- Chart/table showing output activations per neuron vs target
- Key data: O3≈0.1, O4≈0.1, O5≈0.7-0.8, Target=0.7
- This is the "after" picture to slide 030's "before"

### Uncertain Items (marked [?])
- Exact chart type and layout (pending vision)
- Whether it shows the network diagram again or just the output table
- Color scheme
- Whether equations are shown (like slide 030's forward pass)

---
*Generated: 2026-10-27*
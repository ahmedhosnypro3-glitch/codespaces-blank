# Composed parse: slide_028-

- source frame: `slide_028-.jpg` (md5 `f4aa8f8a64c4785534f6e03ea5ee06ab`)
- parse model: `nemotron-3.5-parse` · chat model: `docparsechat`
- degraded: True (chat probe failed — decisions use the deterministic-conservative fallback)
- elements kept: 16 (dedup collapsed 0) · crops: 3 · failed calls: 0

## Positioned elements (reading order: y then x)

- `<class_Chart>` @(x=852, y=49, w=46, h=44) — from crops/slide_028-.crop01__picture.parse.md (level 1)
  <chart type="kpi_strip"> | column_1 | column_2 | | --- | --- | | 28 | 28 | </chart>
- `<class_Picture>` @(x=854, y=51, w=42, h=40) — from full/slide_028-.parse.md (level 0)
  28
- `<class_Section-header>` @(x=179, y=68, w=572, h=27) — from full/slide_028-.parse.md (level 0)
  **Receiver Operating Characteristic (ROC) Curve**
- `<class_Text>` @(x=82, y=112, w=720, h=39) — from full/slide_028-.parse.md (level 0)
  ROC is a graph showing the performance of a classification model at all classification thresholds.
- `<class_Text>` @(x=82, y=181, w=672, h=19) — from full/slide_028-.parse.md (level 0)
  This curve plots two parameters: [1] True Positive Rate [2] False Positive Rate
- `<class_Text>` @(x=83, y=226, w=656, h=19) — from full/slide_028-.parse.md (level 0)
  **True Positive Rate (TPR)** is a synonym for **recall** and is therefore defined as:
- `<class_Formula>` @(x=108, y=252, w=197, h=61) — from crops/slide_028-.crop02__formula.parse.md (level 1)
  \(TPR=\frac{TP}{TP+FN}\)
- `<class_Formula>` @(x=115, y=254, w=184, h=58) — from full/slide_028-.parse.md (level 0)
  _TPR_ = _TP_ / TP + FN
- `<class_Text>` @(x=332, y=262, w=518, h=42) — from full/slide_028-.parse.md (level 0)
  Correctly Predicted as Positive / ALL Actual Positive Samples (Percentage of correctly retrieved Positive samples)
- `<class_Caption>` @(x=562, y=316, w=131, h=16) — from full/slide_028-.parse.md (level 0)
  **(Best Value is “1”)**
- `<class_Text>` @(x=82, y=340, w=347, h=19) — from full/slide_028-.parse.md (level 0)
  **False Positive Rate (FPR)** is defined as:
- `<class_Formula>` @(x=107, y=361, w=197, h=65) — from crops/slide_028-.crop03__formula.parse.md (level 1)
  FPR= \(\frac{FP}{FP+TN}\)
- `<class_Formula>` @(x=114, y=363, w=184, h=61) — from full/slide_028-.parse.md (level 0)
  FPR = FP / FP + TN
- `<class_Text>` @(x=340, y=373, w=541, h=43) — from full/slide_028-.parse.md (level 0)
  Incorrectly Predicted as Positive / ALL Actual Negative Samples (Error percentage in samples Predicted as Positive)
- `<class_Caption>` @(x=563, y=425, w=128, h=16) — from full/slide_028-.parse.md (level 0)
  **(Best Value is “0”)**
- `<class_Text>` @(x=81, y=458, w=594, h=20) — from full/slide_028-.parse.md (level 0)
  An ROC curve plots TPR vs. FPR <u>at different classification thresholds</u>.

## Unpositioned text

- (none)

## Failed calls

- (none)

## Notes

- backstop stops: 0
- parse calls spent: 4 · chat calls: 0 · retries: 0

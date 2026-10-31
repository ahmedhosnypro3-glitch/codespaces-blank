# Composed parse: slide_026

- source frame: `slide_026.jpg` (md5 `9f39c96be53a071cb1f5ac2f197b47ee`)
- parse model: `nemotron-3.5-parse` · chat model: `docparsechat`
- degraded: True (chat probe failed — decisions use the deterministic-conservative fallback)
- elements kept: 2 (dedup collapsed 1) · crops: 2 · failed calls: 0

## Positioned elements (reading order: y then x)

- `<class_Chart>` @(x=36, y=42, w=887, h=475) — from full/slide_026.parse.md (level 0)
  <chart type="other"> title: Effect of Selecting Threshold Value on Model Performance | column_1 | P | N | | --- | --- | --- | | P | P | N | | P | TP | FN | | N | FP | TN | </chart>
- `<class_Chart>` @(x=36, y=42, w=886, h=475) — from crops/slide_026.crop01__chart.parse.md (level 1)
  <chart type="line"> title: Effect of Selecting Threshold Value on Model Performance bind: Predicted as ; ; y | column_1 | P | N | | --- | --- | --- | | Actual | P | N | | Actual | P | 3 | | Actual | N | 0 | </chart>

## Unpositioned text

- (none)

## Failed calls

- (none)

## Notes

- backstop stops: 0
- parse calls spent: 3 · chat calls: 0 · retries: 0

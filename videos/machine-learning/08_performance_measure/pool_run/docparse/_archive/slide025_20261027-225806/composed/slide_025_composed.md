# Composed parse: slide_025

- source frame: `slide_025.jpg` (md5 `34adaa7ead1996dd7e724ce292902976`)
- parse model: `nemotron-3.5-parse` · chat model: `docparsechat`
- degraded: True (chat probe failed — decisions use the deterministic-conservative fallback)
- elements kept: 2 (dedup collapsed 1) · crops: 2 · failed calls: 0

## Positioned elements (reading order: y then x)

- `<class_Chart>` @(x=36, y=42, w=888, h=476) — from full/slide_025.parse.md (level 0)
  <chart type="other"> title: Effect of Selecting Threshold Value on Model Performance | column_1 | P | N | | --- | --- | --- | | P | P | N | | P | TP | EN | | N | PP | TN | </chart>
- `<class_Chart>` @(x=36, y=42, w=886, h=474) — from crops/slide_025.crop02__chart.parse.md (level 2)
  <chart type="other"> title: Effect of Selecting Threshold Value on Model Performance | column_1 | P | N | | --- | --- | --- | | P | P | N | | P | TP | FN | | N | FP | TN | </chart>

## Unpositioned text

- (none)

## Failed calls

- (none)

## Notes

- backstop stops: 0
- parse calls spent: 3 · chat calls: 0 · retries: 0

# Composed parse: slide_005

- source frame: `slide_005.jpg` (md5 `2c99bd244a014999823ecac03ad5d004`)
- parse model: `nemotron-3.5-parse` · chat model: `docparsechat`
- degraded: False
- elements kept: 2 (dedup collapsed 1) · crops: 2 · failed calls: 0

## Positioned elements (reading order: y then x)

- `<class_Chart>` @(x=37, y=42, w=886, h=475) — from full/slide_005.parse.md (level 0)
  <chart type="other"> title: Radar Shooting of Positive Target (Enemy plane) note: FN = Actually Positive, Miss-classified as Negative FP = Actually Negative, Miss-classified as Positive | Actual | P | N | | --- | --- | --- | | P | TP | FN | | N | FP | TN | | Actual | 30 | 70 | | Predicted | 18 | 12 | | 60 | 10 | 10 | </chart>
- `<class_Chart>` @(x=36, y=42, w=885, h=474) — from crops/slide_005.crop01__chart.parse.md (level 1)
  <chart type="other"> title: Radar Shooting of Positive Target (Enemy plane) | column_1 | P | N | | --- | --- | --- | | Actual | P | TN | | Actual | P | TP | | Actual | N | FP | | Actual | T | FN | | Actual | P | TN | </chart>

## Unpositioned text

- (none)

## Failed calls

- (none)

## Notes

- backstop stops: 0
- parse calls spent: 3 · chat calls: 2 · retries: 0

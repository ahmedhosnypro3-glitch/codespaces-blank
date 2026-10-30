# Composed parse: slide_031

- source frame: `slide_031.jpg` (md5 `4776a1b39d85ec77ff23f2a12f91a2bd`)
- parse model: `nemotron-3.5-parse` · chat model: `docparsechat`
- degraded: True (chat probe failed — decisions use the deterministic-conservative fallback)
- elements kept: 2 (dedup collapsed 0) · crops: 1 · failed calls: 0

## Positioned elements (reading order: y then x)

- `<class_Chart>` @(x=36, y=23, w=888, h=513) — from crops/slide_031.crop01__chart.parse.md (level 1)
  <chart type="scatter"> title: Example subtitle: Better Weights | column_1 | column_2 | | --- | --- | | O3 | 0.121 | | O3 | 0.101 | | O4 | 0.099 | | O4 | 0.288 | | O5 | 0.696 | | O5 | 0.795 | | Output | 0.187 | | Target | 0.7 | </chart>
- `<class_Chart>` @(x=35, y=42, w=876, h=476) — from full/slide_031.parse.md (level 0)
  <chart type="other"> title: Example | column_1 | column_2 | | --- | --- | | O3 | 0.121 | | 3 | -0.399 | | 4 | 0.598 | | 6 | 0.101 | | 4 | -0.288 | | 6 | 0.696 | | 7 | 0.405 | | 7 | 0.305 | | 5 | 0.795 | </chart>

## Unpositioned text

- (none)

## Failed calls

- (none)

## Notes

- backstop stops: 0
- parse calls spent: 2 · chat calls: 0 · retries: 0

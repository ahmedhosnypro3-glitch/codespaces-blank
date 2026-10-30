# Composed parse: slide_030

- source frame: `slide_030.jpg` (md5 `655760a508ce96d46fdd95ee45c3a2d0`)
- parse model: `nemotron-3.5-parse` · chat model: `docparsechat`
- degraded: True (chat probe failed — decisions use the deterministic-conservative fallback)
- elements kept: 2 (dedup collapsed 0) · crops: 1 · failed calls: 0

## Positioned elements (reading order: y then x)

- `<class_Chart>` @(x=36, y=23, w=888, h=512) — from crops/slide_030.crop01__chart.parse.md (level 1)
  <chart type="scatter"> title: Example subtitle: Bad Weights | column_1 | column_2 | | --- | --- | | O3 | 0.3 | | O3 | 0.3 | | O4 | 0.4 | | O4 | 0.4 | | O5 | 0.5 | | O5 | 0.5 | | Target | 0 | </chart>
- `<class_Chart>` @(x=35, y=42, w=876, h=475) — from full/slide_030.parse.md (level 0)
  <chart type="scatter"> title: Example subtitle: Bad Weights | column_1 | column_2 | column_3 | | --- | --- | --- | | 0 | t6 | 0 | | t7 | t7 | 0.1 | | 4 | 0.5 | 0.4 | | 5 | 0.5 | 0.5 | </chart>

## Unpositioned text

- (none)

## Failed calls

- (none)

## Notes

- backstop stops: 0
- parse calls spent: 2 · chat calls: 0 · retries: 0

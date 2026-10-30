# Composed parse: slide_002

- source frame: `slide_002.jpg` (md5 `6e364a86b218a372a397efc14a28f131`)
- parse model: `nemotron-3.5-parse` · chat model: `docparsechat`
- degraded: True (chat probe failed — decisions use the deterministic-conservative fallback)
- elements kept: 2 (dedup collapsed 1) · crops: 2 · failed calls: 0

## Positioned elements (reading order: y then x)

- `<class_Chart>` @(x=36, y=42, w=888, h=475) — from full/slide_002.parse.md (level 0)
  <chart type="other"> title: Training Samples with Labels [0,1] (Two Classes) | Positive Class "Shoot the Enemy" | Label | Negative Class "Safe" | Label | | --- | --- | --- | --- | | +1 | 0 | Initial | 0 | | +1 | 0 | Model | (+1, 0) | | +1 | 0 | Evaluation | 0 | </chart>
- `<class_Chart>` @(x=36, y=42, w=886, h=475) — from crops/slide_002.crop01__chart.parse.md (level 1)
  <chart type="other"> title: Training Samples with Labels [0,1] (Two Classes) | Positive Class "Shoot the Enemy" | Label | Negative Class "Safe" | Label | | --- | --- | --- | --- | | +1 | +1 | 0 | 0 | | +1 | +1 | 0 | 0 | | +1 | +1 | 0 | 0 | </chart>

## Unpositioned text

- (none)

## Failed calls

- (none)

## Notes

- backstop stops: 0
- parse calls spent: 3 · chat calls: 0 · retries: 0

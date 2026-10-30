# Composed parse: slide_003

- source frame: `slide_003.jpg` (md5 `b32323454ad553c4df23a5aff07213e7`)
- parse model: `nemotron-3.5-parse` · chat model: `docparsechat`
- degraded: False
- elements kept: 2 (dedup collapsed 1) · crops: 2 · failed calls: 0

## Positioned elements (reading order: y then x)

- `<class_Picture>` @(x=36, y=42, w=873, h=475) — from full/slide_003.parse.md (level 0)
  Training Samples with Labels [-1,+1] (Two Classes) 3 Positive Class "Shoot the Enemy" Label Negative Class "Safe" Label Activation Function Bi-polor step (-1 , +1) Threshold at "zero" Threshold at "zero" +1 -1 Training Input Sample Predicted Class Label of Input Sample Model [Any value] --- (-1 , +1) LOSS (+1, -1) Evaluation Test Sample Predicted Class Model (+1, -1) [Any value] -- (-1 , +1)
- `<class_Chart>` @(x=36, y=42, w=871, h=475) — from crops/slide_003.crop01__picture.parse.md (level 1)
  <chart type="ranked_table"> title: Training Samples with Labels [-1,+1] (Two Classes) | Positive Class "Shoot the Enemy" | Label | Negative Class "Safe" | Label | | --- | --- | --- | --- | | +1 | +1 | -1 | -1 | | +1 | +1 | -1 | -1 | | +1 | +1 | -1 | -1 | </chart>

## Unpositioned text

- (none)

## Failed calls

- (none)

## Notes

- backstop stops: 0
- parse calls spent: 3 · chat calls: 2 · retries: 1

# Composed parse: slide_032

- source frame: `slide_032.jpg` (md5 `0feffc6ca96d899c341ec2f3ef47369a`)
- parse model: `nemotron-3.5-parse` · chat model: `docparsechat`
- degraded: False
- elements kept: 2 (dedup collapsed 0) · crops: 1 · failed calls: 0

## Positioned elements (reading order: y then x)

- `<class_Chart>` @(x=37, y=22, w=886, h=513) — from crops/slide_032.crop01__picture.parse.md (level 1)
  <chart type="other"> | column_1 | P | N | | --- | --- | --- | | Actual | P | 5 | | Actual | S | 0 | | Actual | N | 6 | </chart>
- `<class_Picture>` @(x=36, y=41, w=922, h=476) — from full/slide_032.parse.md (level 0)
  Threshold=0.0 Predicted as P N TPR=5/(5+0)=1 FPR=6/(6+0)=1 Actual P 5 0 N 4 2 TPR=5/(5+0)=1 FPR=4/(4+2)=0.66 TPR Threshold=0.3 Predicted as P N TPR=5/(5+0)=1 FPR=2/(2+4)=0.33 Threshold=0.4 ROC Curve for Same Model -different thresholds TPR = TP TP + FN P P N P FP FN FPR = FP FP+TN N Actual Input

## Unpositioned text

- (none)

## Failed calls

- (none)

## Notes

- backstop stops: 0
- parse calls spent: 2 · chat calls: 1 · retries: 0

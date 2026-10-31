# Composed parse: slide_032

- source frame: `slide_032.jpg` (md5 `0feffc6ca96d899c341ec2f3ef47369a`)
- parse model: `nemotron-3.5-parse` · chat model: `docparsechat`
- degraded: False
- elements kept: 3 (dedup collapsed 1) · crops: 3 · failed calls: 0

## Positioned elements (reading order: y then x)

- `<class_Picture>` @(x=36, y=41, w=862, h=476) — from full/slide_032.parse.md (level 0)
  Threshold=0.0 Predicted as P N TPR=5/(5+0)=1 FPR=6/(6+0)=1 Actual P 5 0 N 4 2 TPR=5/(5+0)=1 FPR=4/(4+2)=0.66 TPR Threshold=0.3 Predicted as P N TPR=5/(5+0)=1 FPR=2/(2+4)=0.33 Threshold=0.4 ROC Curve for Same Model -different thresholds TPR = TP TP + FN P P N P FP FN P FPR = FP FP+TN N FP TN Actual
- `<class_Picture>` @(x=36, y=41, w=862, h=475) — from crops/slide_032.crop01__picture.parse.md (level 1)
  Threshold=0.0 32 P N P TPR=5/(5+0)=1 PPR=6/(6+0)=1 Actual P 5 0 N 6 0 Threshold=0.1 Predicted as P N P TPR=5/(5+0)=1 PPR=4/(4+2)=0.66 Actual P 5 0 N 4 2 Threshold=0.3 Predicted as P N P TPR=5/(5+0)=1 PPR=2/(2+4)=0.33 Actual Threshold=0.4 ROC Curve for Same Model -different thresholds P P N P TP FN P FPR = FP + TN Actual PN TN
- `<class_Picture>` @(x=36, y=42, w=864, h=476) — from crops/slide_032.crop02__picture.parse.md (level 2)
  Threshold=0.0 32 P N P 5 0 N 6 0 TPR=5/(5+0)=1 FPR=6/(6+0)=1 Actual P 5 0 N 4 2 TPR=5/(5+0)=1 FPR=4/(4+2)=0.66 TPR Threshold=0.3 Predicted as P N P 5 0 TPR=5/(5+0)=1 FPR=2/(2+4)=0.33 Actual P 5 0 N 2 4 ROC Curve for Same Model -different thresholds P P TP FN P Pr = FP + TN Actual P N FP TN

## Unpositioned text

- (none)

## Failed calls

- (none)

## Notes

- backstop stops: 0
- parse calls spent: 4 · chat calls: 3 · retries: 1

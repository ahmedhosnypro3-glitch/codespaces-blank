# Composed parse: slide_033

- source frame: `slide_033.jpg` (md5 `4c23d5ebe6e68bbd85a975a871b2ce0c`)
- parse model: `nemotron-3.5-parse` · chat model: `docparsechat`
- degraded: False
- elements kept: 3 (dedup collapsed 1) · crops: 3 · failed calls: 0

## Positioned elements (reading order: y then x)

- `<class_Picture>` @(x=36, y=41, w=887, h=476) — from full/slide_033.parse.md (level 0)
  Threshold=0.0 Threshold=0.6 33 P N P S 0 TPR=5/(5+0)=1 FPR=6/(6+0)=1 Actual P N 1 5 TPR=3/(3+1)=0.6 FPR=1/(1+5)=0.16 Predicted as P N P S 0 TPR=5/(5+0)=1 FPR=4/(4+2)=0.66 PPR Threshold=0.3 Predicted as P N P S 0 TPR=5/(5+0)=1 FPR=2/(2+4)=0.33 Threshold=0.4 ROC Curve for Same Model -different thresholds TPR = TP FP + FN P P N P FP FN P FP+TN Actual P N TN
- `<class_Picture>` @(x=36, y=42, w=886, h=476) — from crops/slide_033.crop01__picture.parse.md (level 1)
  Threshold=0.0 Predicted as P N TPR=5/(5+0)=1 P 3 1 P N TPR=3/(3+1)=0.6 FPR=1/(1+5)=0.16 Actual P S 0 PPR=5/(5+0)=1 FPR=4/(4+2)=0.66 PPR Threshold=0.3 Predicted as P N TPR=5/(5+0)=1 FPR=2/(2+4)=0.33 Actual P S 0 PPR=4/(4+1)=4/5 FPR=1/(1+5)=0.16 ROC Curve for Same Model -different thresholds P P P TP FN FN N FP TN
- `<class_Picture>` @(x=36, y=42, w=886, h=475) — from crops/slide_033.crop02__picture.parse.md (level 2)
  Threshold=0.0 Predicted as P N TPR=5/(5+0)=1 P N P 3 1 PPR=3/(3+1)=0.6 FPR=1/(1+5)=0.16 Actual P N 1 5 0 TPR=5/(5+0)=1 FPR=4/(4+2)=0.66 TPR PPR Threshold=0.3 Predicted as P N TPR=5/(5+0)=1 FPR=2/(2+4)=0.33 Predicted as P P P TP FN P FP + TN Actual P P TN N 1 5

## Unpositioned text

- (none)

## Failed calls

- (none)

## Notes

- backstop stops: 0
- parse calls spent: 4 · chat calls: 3 · retries: 3

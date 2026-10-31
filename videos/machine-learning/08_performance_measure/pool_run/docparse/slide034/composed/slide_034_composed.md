# Composed parse: slide_034

- source frame: `slide_034.jpg` (md5 `c441448e25d690b774af0494242172a9`)
- parse model: `nemotron-3.5-parse` · chat model: `docparsechat`
- degraded: False
- elements kept: 2 (dedup collapsed 1) · crops: 2 · failed calls: 0

## Positioned elements (reading order: y then x)

- `<class_Picture>` @(x=36, y=42, w=887, h=475) — from full/slide_034.parse.md (level 0)
  Threshold=0.0 Threshold=0.6 34 P N P 5 0 TPR=5/(5+0)=1 FPR=6/(6+0)=1 Actual P 3 1 TPR=3/(3+1)=0.6 FPR=1/(1+5)=0.16 Threshold=0.1 Threshold=0.7 Best (FPR) P N P 5 0 TPR=5/(5+0)=1 FPR=4/(4+2)=0.66 Actual P 3 2 TPR=3/(3+2)=0.6 FPR=0/(0+6)=0 TPR P R Threshold=0.3 Predicted as P N P N P 5 0 TPR=5/(5+0)=1 FPR=2/(2+4)=0.33 Threshold=0.3 Predicted as P N P R P 5 0 TPR=5/(5+0)=1 FPR=2/(2+4)=0.33 Threshold=0.4 ROC Curve for Same Model -different thresholds PTPR = TP FP +FN P N P P LP FN P FP +TN N FP TN Actual P 4 1 N 1 5 Actual P FPR= FP FP+TN No FP TN
- `<class_Picture>` @(x=36, y=42, w=886, h=475) — from crops/slide_034.crop01__picture.parse.md (level 1)
  Threshold=0.0 Predicted as Predicted as Predicted as P N TPR=5/(5+0)=1 P N TPR=3/(3+1)=0.6 FPR=1/(1+5)=0.16 Actual P 5 0 N 6 0 Accual P 3 1 N 1 5 Best (FPR) Out P 5 0 P R=5/(5+0)=1 P FPR=4/(4+2)=0.66 Actual P 3 2 N 0 6 TPR Threshold=0.3 Predicted as P N TPR=5/(5+0)=1 FPR=2/(2+4)=0.33 Actual P 5 0 N 2 4 ROC Curve for Same Model -different thresholds P P TP FN P FP + TN Actual N FP TN

## Unpositioned text

- (none)

## Failed calls

- (none)

## Notes

- backstop stops: 0
- parse calls spent: 3 · chat calls: 2 · retries: 0

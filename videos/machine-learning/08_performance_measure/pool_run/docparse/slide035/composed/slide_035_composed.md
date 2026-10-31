# Composed parse: slide_035

- source frame: `slide_035.jpg` (md5 `8940f86add177cc87fca1dde16e56106`)
- parse model: `nemotron-3.5-parse` · chat model: `docparsechat`
- degraded: False
- elements kept: 4 (dedup collapsed 0) · crops: 3 · failed calls: 0

## Positioned elements (reading order: y then x)

- `<class_Picture>` @(x=37, y=41, w=888, h=476) — from full/slide_035.parse.md (level 0)
  Threshold=0.0 Threshold=0.6 35 P N P N TPR=5/(5+0)=1 P R=6/(6+0)=1 Actual P 3 1 PPR=3/(3+1)=0.6 PFR=1/(1+5)=0.16 Threshold=0.1 Threshold=0.7 Best (FPR) P N P P =5/(5+0)=1 P R=4/(4+2)=0.66 P A P 3 2 PPR=3/(3+2)=0.6 PFR=0/(0+6)=0 TPR Threshold=0.3 Threshold=1 Predicted as P N P N PPR=5/(5+0)=1 PPR=2/(2+4)=0.33 P D 0 5 PPR=0/(0+5)=0 1.0 FPR 1.0 Threshold=0.4 ROC Curve for Same Model -different thresholds P P TPR = TP + FN P N P FP FN P FP+TN N FP TN
- `<class_Picture>` @(x=36, y=41, w=861, h=476) — from crops/slide_035.crop01__picture.parse.md (level 1)
  Threshold=0.0 Predicted as P N TPR=5/(5+0)=1 P 3 1 P R=3/(3+1)=0.6 PFR=1/(1+5)=0.16 Actual P N 1 5 Best (FPR) P 0.7 0.4 P 5 0 PFR=4/(4+2)=0.66 P 3 2 PFR=0/(0+6)=0 TPR Threshold=0.3 Threshold=1 Predicted as P N P N TPR=0/(0+5)=0 PFR=0/(0+6)=0 Actual P 5 0 P FPR=2/(2+4)=0.33 P 0 5 PFR=0/(0+6)=0 1.0 FPR Threshold=0.4 ROC Curve for Same Model -different thresholds P N P TP FN P TN Actual N 1 5
- `<class_Picture>` @(x=38, y=42, w=859, h=474) — from crops/slide_035.crop02__picture.parse.md (level 2)
  Threshold=0.0 Predicted as P N TPR=5/(5+0)=1 P P N TPR=3/(3+1)=0.6 PPR=1/(1+5)=0.16 Actual P S 0 N 6 0 Accual N 1 5 Best (FPR) P P N TPR=5/(5+0)=1 PPR=4/(4+2)=0.66 P P N TPR=3/(3+2)=0.6 PPR=0/(0+6)=0 TPR Threshold=0.3 Predicted as P N TPR=5/(5+0)=1 PPR=2/(2+4)=0.33 Actual P P 0 5 PPR=0/(0+5)=0 PPR=0/(0+6)=0 1.0 FPR Threshold=0.4 Predicted as P N TPR = TP Predicted as P N P N P P FP FN TN Actual N 1 5
- `<class_Picture>` @(x=36, y=42, w=862, h=475) — from crops/slide_035.crop03__picture.parse.md (level 3)
  Threshold=0.0 Predicted as P N TPR=5/(5+0)=1 P P N TPR=3/(3+1)=0.6 PPR=1/(1+5)=0.16 Actual P S 0 V N 6 0 Accual N 1 5 Best (FPR) Out P N P 5 0 TPR=5/(5+0)=1 PPR=4/(4+2)=0.66 Actual P 3 2 N 0 6 TPR 0/(0+6)=0 PPR Threshold=0.3 Predicted as P N P N TPR=5/(5+0)=1 PPR=2/(2+4)=0.33 Actual P 0 5 PPR=0/(0+5)=0 PPR=0/(0+6)=0 1.0 FPR Threshold=0.4 Predicted as P N TPR = TP Predicted as P N P NP PN P FN TN Actual N 1 5

## Unpositioned text

- (none)

## Failed calls

- (none)

## Notes

- backstop stops: 0
- parse calls spent: 4 · chat calls: 4 · retries: 2

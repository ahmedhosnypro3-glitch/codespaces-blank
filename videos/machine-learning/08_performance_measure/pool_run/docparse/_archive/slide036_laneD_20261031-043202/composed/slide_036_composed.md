# Composed parse: slide_036

- source frame: `slide_036.jpg` (md5 `ef25b426e922a939acb758970a061335`)
- parse model: `nemotron-3.5-parse` · chat model: `docparsechat`
- degraded: True (chat probe failed — decisions use the deterministic-conservative fallback)
- elements kept: 2 (dedup collapsed 1) · crops: 2 · failed calls: 0

## Positioned elements (reading order: y then x)

- `<class_Picture>` @(x=37, y=42, w=863, h=475) — from full/slide_036.parse.md (level 0)
  Threshold=0.0 Threshold=0.6 36 Predicted as P P N Predicted as Predicted as P N Predicted as The Best (TPR) Actual P 5 0 TPR=5/(5+0)=1 FPR=6/(6+0)=1 Actual P 3 1 PPR=3/(3+1)=0.6 FPR=1/(1+5)=0.16 Best (FPR) P 5 0 TPR=4/(4+2)=0.66 P 3 2 TPR=3/(3+2)=0.6 FPR=0/(0+6)=0 TPR 0.4 N 4 2 N 0 6 TPR 0.7 Threshold=0.3 Threshold=1 Predicted as Predicted as P N Predicted as P N Predicted as P P P N Predicted as P P P TP FN P FP+TN Actual N 1.0 FPR Threshold=0.4 ROC Curve for Same Model -different thresholds P P N P LP FN P FP TN
- `<class_Picture>` @(x=36, y=42, w=868, h=475) — from crops/slide_036.crop01__picture.parse.md (level 1)
  Threshold=0.0 Predicted as P N TPR=5/(5+0)=1 P P N TPR=3/(3+1)=0.6 PPR=1/(1+5)=0.16 Best (TPR) Actual P S 0 PFR=4/(4+2)=0.66 P P N TPR=3/(3+2)=0.6 PPR=0/(0+6)=0 PPR 0.4 N 4 2 Threshold=0.7 Predicted as P N TPR=5/(5+0)=1 PPR=2/(2+4)=0.33 P N TPR=0/(0+5)=0 PPR=0/(0+6)=0 1.0 FPR Threshold=0.4 Predicted as P N TPR = TP Predicted as P N P P PN P FN Attual N N TN

## Unpositioned text

- (none)

## Failed calls

- (none)

## Notes

- backstop stops: 0
- parse calls spent: 3 · chat calls: 0 · retries: 0

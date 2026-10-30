# Composed parse: slide_030

- source frame: `slide_030.jpg` (md5 `ceb4d1964b1156d1ec323d549675d1a5`)
- parse model: `nemotron-3.5-parse` · chat model: `docparsechat`
- degraded: True (chat probe failed — decisions use the deterministic-conservative fallback)
- elements kept: 3 (dedup collapsed 1) · crops: 3 · failed calls: 0

## Positioned elements (reading order: y then x)

- `<class_Picture>` @(x=62, y=71, w=1462, h=809) — from full/slide_030.parse.md (level 0)
  Threshold=0.0 30 P N TPR=5/(5+0)=1 Actual P 5 0 FPR=6/(6+0)=1 Threshold=0.1 Predicted as P N TPR=5/(5+0)=1 FPR=4/(4+2)=0.66 Actual P P R ROC Curve for Same Model -different thresholds Actual P N FP TN
- `<class_Picture>` @(x=61, y=71, w=1467, h=808) — from crops/slide_030.crop02__picture.parse.md (level 2)
  Threshold=0.0 30 P N P TPR=5/(5+0)=1 Actual P 5 0 N 6 0 Threshold=0.1 Predicted as P N P TPR=5/(5+0)=1 PPR=4/(4+2)=0.66 Actual P P R ROC Curve for Same Model -different thresholds
- `<class_Picture>` @(x=61, y=72, w=1464, h=807) — from crops/slide_030.crop01__picture.parse.md (level 1)
  Threshold=0.0 30 P N P TPR=5/(5+0)=1 PPR=6/(6+0)=1 Actual P 5 0 N 6 0 Threshold=0.1 Predicted as P N TPR=5/(5+0)=1 FPR=4/(4+2)=0.66 PPR PPR ROC Curve for TPR = TP Predicted as P N P P TN Actual P FPR = FP FP +TN PN

## Unpositioned text

- (none)

## Failed calls

- (none)

## Notes

- backstop stops: 0
- parse calls spent: 4 · chat calls: 0 · retries: 0

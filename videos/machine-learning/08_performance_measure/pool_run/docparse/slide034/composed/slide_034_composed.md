# Composed parse: slide_034

- source frame: `slide_034.jpg` (md5 `c441448e25d690b774af0494242172a9`)
- parse model: `nemotron-3.5-parse` · chat model: `docparsechat`
- degraded: True (chat probe failed — decisions use the deterministic-conservative fallback)
- elements kept: 7 (dedup collapsed 1) · crops: 7 · failed calls: 0

## Positioned elements (reading order: y then x)

- `<class_Picture>` @(x=30, y=35, w=569, h=509) — from crops_supp/ltop/slide034.ltop.parse.md (level 1)
  Predicted as P N TPR=5/(5+0)=1 P 3 1 P N TPR=3/(3+1)=6 FPR=1/(1+5)=6 Threshold=0.1 Threshold=0.7
- `<class_Chart>` @(x=555, y=35, w=390, h=682) — from crops_supp/rcol/slide034.rcol.parse.md (level 1)
  <chart type="lollipop"> axis[x]: FPR axis[y]: Predicted as bind: P ; ; x bind: N ; ; y | P | N | | --- | --- | | P | 0.3 | | TP | 0.1 | | FN | 0.0 | | TN | 0.7 | </chart>
- `<class_Picture>` @(x=36, y=42, w=887, h=475) — from full/slide_034.parse.md (level 0)
  Threshold=0.0 Threshold=0.6 34 P N P 5 0 TPR=5/(5+0)=1 FPR=6/(6+0)=1 Actual P 3 1 TPR=3/(3+1)=0.6 FPR=1/(1+5)=0.16 Threshold=0.1 Threshold=0.7 Best (FPR) P N P 5 0 TPR=5/(5+0)=1 FPR=4/(4+2)=0.66 Actual P 3 2 TPR=3/(3+2)=0.6 FPR=0/(0+6)=0 TPR P R Threshold=0.3 Predicted as P N P N P 5 0 TPR=5/(5+0)=1 FPR=2/(2+4)=0.33 Threshold=0.3 Predicted as P N P R P 5 0 TPR=5/(5+0)=1 FPR=2/(2+4)=0.33 Threshold=0.4 ROC Curve for Same Model -different thresholds PTPR = TP FP +FN P N P P LP FN P FP +TN N FP TN Actual P 4 1 N 1 5 Actual P FPR= FP FP+TN No FP TN
- `<class_Picture>` @(x=36, y=42, w=886, h=475) — from crops/slide_034.crop01__picture.parse.md (level 1)
  Threshold=0.0 Predicted as Predicted as Predicted as P N TPR=5/(5+0)=1 P N TPR=3/(3+1)=0.6 FPR=1/(1+5)=0.16 Actual P 5 0 N 6 0 Accual P 3 1 N 1 5 Best (FPR) P 0.7 0.4 TPR=5/(5+0)=1 P R=4/(4+2)=0.66 P 3 2 P R=0/(0+6)=0 PPR Threshold=0.3 Predicted as P N TPR=5/(5+0)=1 FPR=2/(2+4)=0.33 Actual P 5 0 N 2 4 ROC Curve for Same Model -different thresholds P P TP FN P FP + TN Actual N FP TN
- `<class_Picture>` @(x=36, y=42, w=886, h=475) — from crops/slide_034.crop02__picture.parse.md (level 2)
  Threshold=0.0 Predicted as Predicted as Predicted as P N TPR=5/(5+0)=1 P N TPR=3/(3+1)=0.6 FPR=1/(1+5)=0.16 Actual P 5 0 N 6 0 Accual P 3 1 N 1 5 Best (FPR) Out P 5 0 P R=5/(5+0)=1 P FPR=4/(4+2)=0.66 Actual P 3 2 N 0 6 TPR Threshold=0.3 Predicted as P N TPR=5/(5+0)=1 FPR=2/(2+4)=0.33 Actual P 5 0 N 2 4 ROC Curve for Same Model -different thresholds P P TP FN P FP + TN Actual N FP TN
- `<class_Chart>` @(x=30, y=190, w=569, h=524) — from crops_supp/lmid/slide034.lmid.parse.md (level 1)
  <chart type="ranked_table"> | column_1 | P | N | | --- | --- | --- | | P | 5 | 0 | | N | 4 | 2 | </chart>
- `<class_Chart>` @(x=36, y=345, w=564, h=524) — from crops_supp/lbot/slide034.lbot.parse.md (level 1)
  <chart type="other"> | column_1 | column_2 | | --- | --- | | P | 5 | | N | 2 | | Threshold=0.4 | | P | 4 | | P | 4 | | N | 1 | </chart>

## Unpositioned text

- (none)

## Failed calls

- (none)

## Notes

- backstop stops: 0
- parse calls spent: 4 · chat calls: 0 · retries: 0

# Composed parse: slide_033

- source frame: `slide_033.jpg` (md5 `4c23d5ebe6e68bbd85a975a871b2ce0c`)
- parse model: `nemotron-3.5-parse` · chat model: `docparsechat`
- degraded: True (chat probe failed — decisions use the deterministic-conservative fallback)
- elements kept: 10 (dedup collapsed 1) · crops: 10 · failed calls: 0

## Positioned elements (reading order: y then x)

- `<class_Chart>` @(x=30, y=35, w=909, h=464) — from crops_supp/band1/slide_033.band1.parse.md (level 1)
  <chart type="other"> | column_1 | P | N | | --- | --- | --- | | P | 5 | 0 | | N | 6 | 0 | </chart>
- `<class_Picture>` @(x=30, y=35, w=569, h=509) — from crops_supp/ltop/slide033.ltop.parse.md (level 1)
  Threshold=0.0 P N TPR=5/(5+0)=1 FPR=6/(6+0)=1 P 3 1 N 1 5
- `<class_Chart>` @(x=555, y=35, w=389, h=682) — from crops_supp/rcol/slide033.rcol.parse.md (level 1)
  <chart type="lollipop"> axis[x]: FPR axis[y]: Predicted as bind: P ; ; y | P | N | TP | FN | | --- | --- | --- | --- | | P | 0.3 | 0.1 | 0.0 | | N | 0.4 | 0.6 | 0.6 | </chart>
- `<class_Picture>` @(x=36, y=41, w=887, h=476) — from full/slide_033.parse.md (level 0)
  Threshold=0.0 Threshold=0.6 33 P N P S 0 TPR=5/(5+0)=1 FPR=6/(6+0)=1 Actual P N 1 5 TPR=3/(3+1)=0.6 FPR=1/(1+5)=0.16 Predicted as P N P S 0 TPR=5/(5+0)=1 FPR=4/(4+2)=0.66 PPR Threshold=0.3 Predicted as P N P S 0 TPR=5/(5+0)=1 FPR=2/(2+4)=0.33 Threshold=0.4 ROC Curve for Same Model -different thresholds TPR = TP FP + FN P P N P FP FN P FP+TN Actual P N TN
- `<class_Picture>` @(x=36, y=42, w=886, h=476) — from crops/slide_033.crop01__picture.parse.md (level 1)
  Threshold=0.0 Predicted as P N TPR=5/(5+0)=1 P 3 1 P N TPR=3/(3+1)=0.6 FPR=1/(1+5)=0.16 Actual P S 0 PPR=5/(5+0)=1 FPR=4/(4+2)=0.66 PPR Threshold=0.3 Predicted as P N TPR=5/(5+0)=1 FPR=2/(2+4)=0.33 Actual P S 0 PPR=4/(4+1)=4/5 FPR=1/(1+5)=0.16 ROC Curve for Same Model -different thresholds P P P TP FN FN N FP TN
- `<class_Picture>` @(x=36, y=42, w=886, h=475) — from crops/slide_033.crop02__picture.parse.md (level 2)
  Threshold=0.0 Predicted as P N TPR=5/(5+0)=1 P N P 3 1 PPR=3/(3+1)=0.6 FPR=1/(1+5)=0.16 Actual P N 1 5 0 TPR=5/(5+0)=1 FPR=4/(4+2)=0.66 TPR PPR Threshold=0.3 Predicted as P N TPR=5/(5+0)=1 FPR=2/(2+4)=0.33 Predicted as P P P TP FN P FP + TN Actual P P TN N 1 5
- `<class_Chart>` @(x=30, y=165, w=909, h=464) — from crops_supp/band2/slide_033.band2.parse.md (level 1)
  <chart type="ranked_table"> title: Predicted as | P | N | | --- | --- | | 5 | 0 | | 4 | 2 | </chart>
- `<class_Chart>` @(x=30, y=190, w=569, h=524) — from crops_supp/lmid/slide033.lmid.parse.md (level 1)
  <chart type="ranked_table"> | column_1 | P | N | | --- | --- | --- | | P | 5 | 0 | | N | 4 | 2 | </chart>
- `<class_Picture>` @(x=37, y=295, w=886, h=674) — from crops_supp/band3/slide_033.band3.parse.md (level 1)
  Threshold=0.3 P N P 5 0 N 2 4 TPR=5/(5+0)=1 FPR=2/(2+4)=0.33 Threshold=0.4 Predicted as P N P R P 4 1 TPR=4/(4+1)=4/5 P R=1/(1+5)=0.16 ROC Curve for Same Model -different thresholds P P NP FP TN Actual
- `<class_Chart>` @(x=35, y=345, w=564, h=524) — from crops_supp/lbot/slide033.lbot.parse.md (level 1)
  <chart type="other"> | column_1 | column_2 | | --- | --- | | P | 5 | | N | 2 | | Threshold=0.4 | | P | 4 | | P | 4 | | N | 1 | </chart>

## Unpositioned text

- (none)

## Failed calls

- (none)

## Notes

- backstop stops: 0
- parse calls spent: 4 · chat calls: 0 · retries: 0

# Composed parse: slide_036

- source frame: `slide_036.jpg` (md5 `ef25b426e922a939acb758970a061335`)
- parse model: `nemotron-3.5-parse` · chat model: `docparsechat`
- degraded: True (chat probe failed — decisions use the deterministic-conservative fallback)
- elements kept: 9 (dedup collapsed 1) · crops: 9 · failed calls: 0

## Positioned elements (reading order: y then x)

- `<class_Chart>` @(x=30, y=35, w=909, h=464) — from crops_supp/band1/slide_036.band1.parse.md (level 1)
  <chart type="other"> axis[y]: Actual | Actual | P | N | | --- | --- | --- | | Threshold=0.0 | P | 5 | | Threshold=0.6 | P | 5 | | Threshold=3/(3+1)=0.6 | PFR=5/(5+0)=1 | FPR=6/(6+0)=1 | | Actual | P | 3 | | Normal | N | 1 | </chart>
- `<class_Picture>` @(x=30, y=35, w=569, h=509) — from crops_supp/ltop/slide036.ltop.parse.md (level 1)
  Predicted as P N TPR=5/(5+0)=1 P 3 1 P N TPR=3/(3+1)=6 FPR=1/(1+5)=6 Threshold=0.1 Threshold=0.7
- `<class_Chart>` @(x=555, y=35, w=390, h=682) — from crops_supp/rcol/slide036.rcol.parse.md (level 1)
  <chart type="other"> annotation: callout ; label=The Best (If Any) annotation: callout ; label=Best (TPR) | column_1 | P | N | | --- | --- | --- | | The Best (If Any) | 0.3 | 0.1 | | Best (FPR) | 0.4 | 0.0 | | FPR | 0.6 | 0.7 | | FPR | 1.0 | 1.0 | </chart>
- `<class_Picture>` @(x=37, y=42, w=863, h=475) — from full/slide_036.parse.md (level 0)
  Threshold=0.0 Threshold=0.6 36 Predicted as P P N Predicted as Predicted as P N Predicted as The Best (TPR) Actual P 5 0 TPR=5/(5+0)=1 FPR=6/(6+0)=1 Actual P 3 1 PPR=3/(3+1)=0.6 FPR=1/(1+5)=0.16 Best (FPR) P 5 0 TPR=4/(4+2)=0.66 P 3 2 TPR=3/(3+2)=0.6 FPR=0/(0+6)=0 TPR 0.4 N 4 2 N 0 6 TPR 0.7 Threshold=0.3 Threshold=1 Predicted as Predicted as P N Predicted as P N Predicted as P P P N Predicted as P P P TP FN P FP+TN Actual N 1.0 FPR Threshold=0.4 ROC Curve for Same Model -different thresholds P P N P LP FN P FP TN
- `<class_Picture>` @(x=36, y=42, w=868, h=475) — from crops/slide_036.crop01__picture.parse.md (level 1)
  Threshold=0.0 Predicted as P N TPR=5/(5+0)=1 P P N TPR=3/(3+1)=0.6 PPR=1/(1+5)=0.16 Best (TPR) Actual P S 0 PFR=4/(4+2)=0.66 P P N TPR=3/(3+2)=0.6 PPR=0/(0+6)=0 PPR 0.4 N 4 2 Threshold=0.7 Predicted as P N TPR=5/(5+0)=1 PPR=2/(2+4)=0.33 P N TPR=0/(0+5)=0 PPR=0/(0+6)=0 1.0 FPR Threshold=0.4 Predicted as P N TPR = TP Predicted as P N P P PN P FN Attual N N TN
- `<class_Chart>` @(x=30, y=165, w=878, h=464) — from crops_supp/band2/slide_036.band2.parse.md (level 1)
  <chart type="ranked_table"> | column_1 | P | N | | --- | --- | --- | | P | 5 | 0 | | N | 4 | 2 | </chart>
- `<class_Chart>` @(x=30, y=190, w=569, h=524) — from crops_supp/lmid/slide036.lmid.parse.md (level 1)
  <chart type="ranked_table"> | column_1 | P | N | TPR=5/(5+0)=1 | P | N | TPR=3/(3+2)=6 | FPR=0/(0+6)=6 | | --- | --- | --- | --- | --- | --- | --- | --- | | P | 5 | 0 | P | 3 | 2 | 0 | 6 | | N | 4 | 2 | N | 0 | 6 | | | </chart>
- `<class_Picture>` @(x=37, y=295, w=888, h=674) — from crops_supp/band3/slide_036.band3.parse.md (level 1)
  Threshold=0.3 Threshold=1 Predicted as P N TPR=5/(5+0)=1 P O S FPR=2/(2+4)=0.33 Actual 1.0 FPR Threshold=0.4 Predicted as P N TPR=4/(4+1)=4/5 ROC Curve for Same Model -different thresholds P P PN P FP TN Actual N 1 5
- `<class_Table>` @(x=37, y=345, w=563, h=524) — from crops_supp/lbot/slide036.lbot.parse.md (level 1)
  \begin{tabular}{ccccc} **P** & **5** & **0** & **PPR=5/(5+0)=1 FPR=2/(2+4)=0.33** & **P** & **0** & **5** & **PPR=0/(0+6)=**\\ N & 2 & 4 & & & N & 0 & 6\\ Threshold=0.4 & \multicolumn{4}{c}{\multirow{2}{*}{Predicted as P}} & \multicolumn{3}{c}{\mbox{}}\\ P & P & N & TPR=4/(4+1)=4/5 FPR=1/(1+5)=0.16 & ROC Curve for Same Model -different thresholds & \\ P & 4 & 1 & & & & & \\ N & 1 & 5 & & & & & \\ \end{tabular}

## Unpositioned text

- (none)

## Failed calls

- (none)

## Notes

- backstop stops: 0
- parse calls spent: 3 · chat calls: 0 · retries: 0

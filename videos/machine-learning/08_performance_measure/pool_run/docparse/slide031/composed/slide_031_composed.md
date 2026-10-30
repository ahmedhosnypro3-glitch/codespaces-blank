# Composed parse: slide_031

- source frame: `slide_031.jpg` (md5 `6fa91139e367edc863d71c0becd0c4e9`)
- parse model: `nemotron-3.5-parse` · chat model: `docparsechat`
- degraded: True (chat probe failed — decisions use the deterministic-conservative fallback)
- elements kept: 10 (dedup collapsed 1) · crops: 8 · failed calls: 0

## Positioned elements (reading order: y then x)

- `<class_Picture>` @(x=39, y=35, w=560, h=509) — from crops_supp/ltop/slide031.ltop.parse.md (level 1)
  Threshold=0.0 Predicted as P P N P 5 0 PPR=5/(6+0)=1 FPR=6/(6+0)=1 Threshold=0.1
- `<class_Chart>` @(x=555, y=35, w=389, h=682) — from crops_supp/rcol/slide031.rcol.parse.md (level 1)
  <chart type="lollipop"> axis[x]: FPR axis[y]: Predicted as bind: P ; ; y | P | N | | --- | --- | | P | 0.3 | | TP | 0.1 | | FN | 0.0 | | TN | | </chart>
- `<class_Chart>` @(x=35, y=41, w=890, h=476) — from full/slide_031.parse.md (level 0)
  <chart type="bar"> bind: value ; ; y | category | value | | --- | --- | | Threshold=0.0 | 31 | | Predicted as P | N | | Actual | P 5 | | N | 6 | | Threshold=0.1 | \multirow{2}{*}{TPR=5/(5+0)=1 FPR=4/(4+2)=0.66} | | Actual | P 5 | | N | 4 | | Threshold=0.3 | \multirow{2}{*}{TPR=5/(5+0)=1 FPR=2/(2+4)=0.33} | | Actual | P 5 | | N | 0 | | N | 2 | </chart>
- `<class_Picture>` @(x=36, y=41, w=862, h=476) — from crops/slide_031.crop01__chart.parse.md (level 1)
  Threshold=0.0 31 P N TPR=5/(5+0)=1 FPR=6/(6+0)=1 Actual P 5 0 N 4 2 TPR=5/(5+0)=1 FPR=4/(4+2)=0.66 TPR Threshold=0.3 Predicted as P N TPR=5/(5+0)=1 FPR=2/(2+4)=0.33 Actual ROC Curve for Same Model -different thresholds P P NP FP TN Actual
- `<class_Picture>` @(x=37, y=42, w=863, h=475) — from crops/slide_031.crop02__picture.parse.md (level 2)
  Threshold=0.0 31 P 5 0 TPR=5/(5+0)=1 FPR=6/(6+0)=1 Actual P 0.3 0.1 0.0 N 6 0 TPR Threshold=0.1 Predicted as P N TPR=5/(5+0)=1 FPR=4/(4+2)=0.66 Actual P 5 0 TPR=5/(5+0)=1 FPR=2/(2+4)=0.33 Actual ROC Curve for Same Model -different thresholds
- `<class_Picture>` @(x=35, y=42, w=865, h=475) — from crops/slide_031.crop03__picture.parse.md (level 3)
  Threshold=0.0 31 P N TPR=5/(5+0)=1 FPR=6/(6+0)=1 Actual P 5 0 N 6 0 Threshold=0.1 Predicted as P N TPR=5/(5+0)=1 FPR=4/(4+2)=0.66 Actual P 5 0 N 4 2 Threshold=0.3 Predicted as P N TPR=5/(5+0)=1 FPR=2/(2+4)=0.33 Actual ROC Curve for Same Model -different thresholds
- `<class_Chart>` @(x=30, y=190, w=569, h=524) — from crops_supp/lmid/slide031.lmid.parse.md (level 1)
  <chart type="ranked_table"> | column_1 | P | N | | --- | --- | --- | | P | 5 | 0 | | N | 4 | 2 | </chart>
- `<class_Picture>` @(x=59, y=345, w=158, h=154) — from crops_supp/lbot/slide031.lbot.parse.md (level 1)
  Actual P 5 0 N 2 4
- `<class_Text>` @(x=226, y=345, w=109, h=98) — from crops_supp/lbot/slide031.lbot.parse.md (level 1)
  TPR=5/(5+0)=1 FPR=2/(2+4)=0.33
- `<class_Caption>` @(x=364, y=600, w=236, h=128) — from crops_supp/lbot/slide031.lbot.parse.md (level 1)
  ROC Curve for Same Model •different thresholds

## Unpositioned text

- (none)

## Failed calls

- (none)

## Notes

- backstop stops: 0
- parse calls spent: 5 · chat calls: 0 · retries: 0

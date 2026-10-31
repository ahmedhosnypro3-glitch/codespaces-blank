# Composed parse: slide_014

- source frame: `slide_014.jpg` (md5 `c3a941c133c24a73e533acc86223787d`)
- parse model: `nemotron-3.5-parse` · chat model: `docparsechat`
- degraded: False
- elements kept: 4 (dedup collapsed 2) · crops: 5 · failed calls: 0

## Positioned elements (reading order: y then x)

- `<class_Chart>` @(x=36, y=42, w=888, h=475) — from full/slide_014.parse.md (level 0)
  <chart type="lollipop"> title: Combine Precision and Recall in one number bind: Combine Precision ; ; y | Category | Combine Precision | | --- | --- | | Positive | 30 | | Negative | 70 | | 20 | 10 | | TN | 59 | | FP | 11 | | TP | FN | | TN | FP | </chart>
- `<class_Chart>` @(x=36, y=42, w=885, h=476) — from crops/slide_014.crop05__chart.parse.md (level 5)
  <chart type="lollipop"> title: Combine Precision and Recall in one number bind: Precision ; ; y | Position | Treatment | Precision = TP | TP + FP | | --- | --- | --- | --- | | Positive | Positive | 30 | 70 | | Negative | Negative | 10 | 59 | | Positive | Positive | 30 | 0 | | Negative | Negative | 0 | 70 | | Good Model: Properly Classifies 20 out of 30 as Positive Properly Classifies 59 out of 70 as Negative | Actualy: This is Not a Model: It classifies ALL Samples as Positive | Procision= 20/(20+11) =64.5% | Precision= 30/(30+70) =30.3% | | Recall= 20/(20+10) =66.6% | Recall= 30/(30+0) =100% | Average= 68.7%+60% =65.55% | Average= 30.3%+100% =65% | </chart>
- `<class_Chart>` @(x=36, y=42, w=885, h=474) — from crops/slide_014.crop03__chart.parse.md (level 3)
  <chart type="lollipop"> title: Combine Precision and Recall in one number bind: Precision ; ; y | Position | Treatment | Precision = TP | Recall = TP + FN | | --- | --- | --- | --- | | Positive | Positive | 30 | 70 | | Negative | Negative | 10 | 70 | | Positive | Positive | 59 | 0 | | Negative | Positive | 30 | 70 | | Good Model: Properly Classifies 20 out of 30 as Positive Properly Classifies 59 out of 70 as Negative | Top FN | 0 | 70 | | Correctly: This is Not a Model: It classifies ALL Samples as Positive | Precision= 20/(20+11) =64.5% | Precision= 30/(30+70) =30.3% | Precision= 30.3% | | Recall= 20/(20+10) =66.6% | Recall= 30/(30+0) =100% | Recall= 30/(30+0) =100% | Precision= 65% | </chart>
- `<class_Chart>` @(x=36, y=42, w=885, h=475) — from crops/slide_014.crop01__chart.parse.md (level 1)
  <chart type="lollipop"> title: Combine Precision and Recall in one number bind: Precision ; ; y | Position | Treatment | Precision | | --- | --- | --- | | Positive | Positive | 30 | | Negative | Negative | 70 | | Positive | Positive | 30 | | Negative | Negative | 0 | | Good Model: Properly Classifies 20 out of 30 as Positive Properly Classifies 59 out of 70 as Negative | Actual: This is Not a Model: It classifies ALL Samples as Positive | 70 | | Precision= 20/(20+11) =64.5% | Precision= 30/(30+70) =30.3% | 30.3% | | Recall= 20/(20+10) =66.6% | Recall= 30/(30+0) =100% | 100% | | Average= 68.7%+60% =65.55% | Average= 30.3%+100% =65% | 65% | </chart>

## Unpositioned text

- (none)

## Failed calls

- (none)

## Notes

- backstop stops: 0
- parse calls spent: 6 · chat calls: 5 · retries: 3

# Composed parse: slide_016

- source frame: `slide_016.jpg` (md5 `1c32fcedbc73c03eaf726bb8db1b785b`)
- parse model: `nemotron-3.5-parse` · chat model: `docparsechat`
- degraded: True (chat probe failed — decisions use the deterministic-conservative fallback)
- elements kept: 3 (dedup collapsed 1) · crops: 3 · failed calls: 0

## Positioned elements (reading order: y then x)

- `<class_Chart>` @(x=36, y=42, w=887, h=474) — from full/slide_016.parse.md (level 0)
  <chart type="lollipop"> title: Combine Precision and Recall in one number bind: Value ; ; y | Category | Value | | --- | --- | | Positive | 1 | | Negative | 2 | | Positive | 30 | | Negative | 70 | | The | 30 | | The | 0 | | TP | FN | | TN | FP | | TP | FN | | TN | FP | </chart>
- `<class_Chart>` @(x=36, y=42, w=884, h=492) — from crops/slide_016.crop02__chart.parse.md (level 2)
  <chart type="lollipop"> title: Combine Precision and Recall in one number bind: Precision ; ; y | Position | Precision = TP | Recall = TP + FN | | --- | --- | --- | | Positive | 30 | 70 | | Negative | 10 | 59 | | TN | FP | 11 | | TP | TP | 0 | | TN | FN | 70 | </chart>
- `<class_Chart>` @(x=36, y=42, w=884, h=492) — from crops/slide_016.crop01__chart.parse.md (level 1)
  <chart type="lollipop"> title: Combine Precision and Recall in one number bind: Precision = TP ; ; y | Position | Treatment | Precision = TP | | --- | --- | --- | | Positive | Positive | 30 | | Negative | Negative | 70 | | Positive | Positive | 30 | | Negative | Negative | 70 | | Recall = | Recall = TP + FN | 70 | | F1 Score | F1 Score= | 1 / 2 | | F1 Score | Precision + Recall | 1 | </chart>

## Unpositioned text

- (none)

## Failed calls

- (none)

## Notes

- backstop stops: 0
- parse calls spent: 4 · chat calls: 0 · retries: 0

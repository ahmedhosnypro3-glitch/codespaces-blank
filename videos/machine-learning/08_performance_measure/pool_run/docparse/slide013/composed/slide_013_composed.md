# Composed parse: slide_013

- source frame: `slide_013.jpg` (md5 `204332246f6ad296d970bc5143bdbdaa`)
- parse model: `nemotron-3.5-parse` · chat model: `docparsechat`
- degraded: False
- elements kept: 6 (dedup collapsed 0) · crops: 1 · failed calls: 0

## Positioned elements (reading order: y then x)

- `<class_Chart>` @(x=36, y=31, w=391, h=303) — from crops/slide_013.crop01__picture.parse.md (level 1)
  <chart type="lollipop"> title: Combine Precision a bind: Positive ; ; y | Category | Positive | | --- | --- | | TP | 20 | | FN | 30 | | TN | 59 | | FP | 70 | </chart>
- `<class_Picture>` @(x=35, y=42, w=378, h=283) — from full/slide_013.parse.md (level 0)
  **Combine Precision and Recall in one number** 13 Positive Negative 30 70 20 10 59 11 TP FN TN FP
- `<class_Text>` @(x=87, y=334, w=294, h=56) — from full/slide_013.parse.md (level 0)
  **Good Model:** Properly Classifies 20 out of 30 as Positive Properly Classifies 59 out of 70 as Negative
- `<class_Text>` @(x=88, y=402, w=229, h=22) — from full/slide_013.parse.md (level 0)
  **Precision= 20/(20+11) =64.5%**
- `<class_Text>` @(x=86, y=442, w=205, h=22) — from full/slide_013.parse.md (level 0)
  **Recall= 20/(20+10) =66.6%**
- `<class_Text>` @(x=89, y=483, w=236, h=21) — from full/slide_013.parse.md (level 0)
  **Average= 68.7%+60% =65.55%**

## Unpositioned text

- (none)

## Failed calls

- (none)

## Notes

- backstop stops: 0
- parse calls spent: 2 · chat calls: 1 · retries: 0

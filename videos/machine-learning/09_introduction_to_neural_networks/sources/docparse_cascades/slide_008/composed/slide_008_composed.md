# Composed parse: slide_008

- source frame: `slide_008.jpg` (md5 `ab140501a5b6663606e52611d0137dc3`)
- parse model: `nemotron-3.5-parse` · chat model: `docparsechat`
- degraded: False
- elements kept: 5 (dedup collapsed 0) · crops: 2 · failed calls: 0

## Positioned elements (reading order: y then x)

- `<class_Chart>` @(x=36, y=42, w=873, h=475) — from full/slide_008.parse.md (level 0)
  <chart type="other"> title: Multi-Class Classification using [ONE VS ALL] Binary Classifiers | column_1 | column_2 | | --- | --- | | C1 | + ve | | Q[x] | ? | | C2 | + ve | | C3 | + ve | </chart>
- `<class_Title>` @(x=289, y=50, w=401, h=58) — from crops/slide_008.crop01__chart.parse.md (level 1)
  **Multi-Class Classification using** **[ONE VS ALL] Binary Classifiers**
- `<class_Page-header>` @(x=866, y=64, w=11, h=16) — from crops/slide_008.crop01__chart.parse.md (level 1)
  8
- `<class_Picture>` @(x=139, y=102, w=683, h=420) — from crops/slide_008.crop02__picture.parse.md (level 2)
  + ve C1 ? ? C2 + ve ? New Class ? ? ? ? New Class
- `<class_Picture>` @(x=165, y=118, w=633, h=390) — from crops/slide_008.crop01__chart.parse.md (level 1)
  +ve C1 ? ? New Class C3

## Unpositioned text

- (none)

## Failed calls

- (none)

## Notes

- backstop stops: 0
- parse calls spent: 3 · chat calls: 2 · retries: 0

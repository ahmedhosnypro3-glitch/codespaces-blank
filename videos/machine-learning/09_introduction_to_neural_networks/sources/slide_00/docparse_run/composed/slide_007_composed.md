# Composed parse: slide_007

- source frame: `slide_007.jpg` (md5 `7b63f777f5075698d3983285ebb8baa5`)
- parse model: `nemotron-3.5-parse` · chat model: `docparsechat`
- degraded: True (chat probe failed — decisions use the deterministic-conservative fallback)
- elements kept: 5 (dedup collapsed 0) · crops: 2 · failed calls: 0

## Positioned elements (reading order: y then x)

- `<class_Chart>` @(x=36, y=43, w=888, h=474) — from full/slide_007.parse.md (level 0)
  <chart type="other"> title: Multi-Class Classification using [ONE VS ALL] Binary Classifiers | column_1 | column_2 | | --- | --- | | C1 | +ve | | Q(x) | +ve | | C2 | +ve | | C3 | +ve | </chart>
- `<class_Title>` @(x=288, y=49, w=405, h=58) — from crops/slide_007.crop01__chart.parse.md (level 1)
  **Multi-Class Classification using** **[ONE VS ALL] Binary Classifiers**
- `<class_Page-header>` @(x=868, y=60, w=12, h=21) — from crops/slide_007.crop01__chart.parse.md (level 1)
  7
- `<class_Picture>` @(x=138, y=103, w=684, h=419) — from crops/slide_007.crop02__picture.parse.md (level 2)
  + ve C1 + ve C2 + ve + ve
- `<class_Picture>` @(x=164, y=119, w=634, h=389) — from crops/slide_007.crop01__chart.parse.md (level 1)
  + ve C1 + ve C2 + ve C3

## Unpositioned text

- (none)

## Failed calls

- (none)

## Notes

- backstop stops: 0
- parse calls spent: 3 · chat calls: 0 · retries: 0

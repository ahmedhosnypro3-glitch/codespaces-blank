# Composed parse: slide_011

- source frame: `slide_011.jpg` (md5 `e9aea80c0fed4817ffd9c1be3bb6f019`)
- parse model: `nemotron-3.5-parse` · chat model: `docparsechat`
- degraded: False
- elements kept: 8 (dedup collapsed 0) · crops: 3 · failed calls: 0

## Positioned elements (reading order: y then x)

- `<class_Section-header>` @(x=281, y=67, w=433, h=27) — from full/slide_011.parse.md (level 0)
  **Classification of “AND” Truth Table**
- `<class_Chart>` @(x=583, y=103, w=267, h=279) — from crops/slide_011.crop01__picture.parse.md (level 1)
  <chart type="line"> axis[x]: x_1 bind: x_1 ; ; x bind: value ; ; y | x_1 | value | | --- | --- | | 0 | 2 | | 1.2 | 1.2 | </chart>
- `<class_Picture>` @(x=592, y=113, w=248, h=259) — from full/slide_011.parse.md (level 0)
  X2 2 1.2 x1
- `<class_Table>` @(x=96, y=137, w=218, h=168) — from crops/slide_011.crop02__table.parse.md (level 1)
  \begin{tabular}{ccc} \thead{X<sub>1</sub>} & \thead{X<sub>2</sub>} & \thead{O/P}\\ 0 & 0 & 0\\ 0 & 1 & 0\\ 1 & 0 & 0\\ 1 & 1 & 1\\ \end{tabular}
- `<class_Table>` @(x=96, y=138, w=219, h=169) — from full/slide_011.parse.md (level 0)
  \begin{tabular}{ccc} **X1** & **X2** & **O/P**\\ 0 & 0 & 0\\ 0 & 1 & 0\\ 1 & 0 & 0\\ 1 & 1 & 1\\ \end{tabular}
- `<class_Chart>` @(x=125, y=345, w=399, h=149) — from crops/slide_011.crop03__picture.parse.md (level 1)
  <chart type="line"> bind: value ; ; y | category | value | | --- | --- | | x1 | -5 | | x2 | -3 | | 1 | 6 | </chart>
- `<class_Picture>` @(x=140, y=351, w=370, h=138) — from full/slide_011.parse.md (level 0)
  -5 >0 ⇒ 1 ≤0 ⇒ 0 X2 -3 Σ O/P 1 6
- `<class_Text>` @(x=582, y=426, w=211, h=29) — from full/slide_011.parse.md (level 0)
  d(X)=-5x1-3x2+6

## Unpositioned text

- (none)

## Failed calls

- (none)

## Notes

- backstop stops: 0
- parse calls spent: 4 · chat calls: 2 · retries: 0

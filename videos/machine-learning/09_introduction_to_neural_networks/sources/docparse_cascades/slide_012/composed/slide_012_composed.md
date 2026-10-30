# Composed parse: slide_012

- source frame: `slide_012.jpg` (md5 `f8d806be3c7862d6a6776e16fe638990`)
- parse model: `nemotron-3.5-parse` · chat model: `docparsechat`
- degraded: False
- elements kept: 9 (dedup collapsed 0) · crops: 3 · failed calls: 0

## Positioned elements (reading order: y then x)

- `<class_Text>` @(x=868, y=63, w=16, h=19) — from full/slide_012.parse.md (level 0)
  12
- `<class_Section-header>` @(x=280, y=67, w=418, h=27) — from full/slide_012.parse.md (level 0)
  **Classification of “OR” Truth Table**
- `<class_Chart>` @(x=527, y=100, w=325, h=276) — from crops/slide_012.crop01__picture.parse.md (level 1)
  <chart type="scatter"> axis[x]: x1 bind: x1 ; ; x bind: value ; ; y | x1 | value | | --- | --- | | 0.4 | 0.28 | </chart>
- `<class_Picture>` @(x=539, y=110, w=302, h=258) — from full/slide_012.parse.md (level 0)
  X2 0.4 0.28 X1
- `<class_Table>` @(x=87, y=131, w=236, h=182) — from crops/slide_012.crop02__table.parse.md (level 1)
  \begin{tabular}{ccc} \thead{X<sub>1</sub>} & \thead{X<sub>2</sub>} & \thead{O/P}\\ 0 & 0 & 0\\ 0 & 1 & 1\\ 1 & 0 & 1\\ 1 & 1 & 1\\ \end{tabular}
- `<class_Table>` @(x=96, y=138, w=219, h=169) — from full/slide_012.parse.md (level 0)
  \begin{tabular}{ccc} **X<sub>1</sub>** & **X<sub>2</sub>** & **O/P**\\ 0 & 0 & 0\\ 0 & 1 & 1\\ 1 & 0 & 1\\ 1 & 1 & 1\\ \end{tabular}
- `<class_Chart>` @(x=125, y=345, w=400, h=149) — from crops/slide_012.crop03__picture.parse.md (level 1)
  <chart type="line"> bind: value ; ; y | category | value | | --- | --- | | x1 | -7 | | x2 | -5 | | 1 | 2 | </chart>
- `<class_Picture>` @(x=140, y=351, w=371, h=138) — from full/slide_012.parse.md (level 0)
  -7 >0 = 1 <0 = 0 X2 -5 Σ O/P 1 2
- `<class_Formula>` @(x=586, y=426, w=207, h=29) — from full/slide_012.parse.md (level 0)
  d(X)=-7x1-5x2+2

## Unpositioned text

- (none)

## Failed calls

- (none)

## Notes

- backstop stops: 0
- parse calls spent: 4 · chat calls: 1 · retries: 0

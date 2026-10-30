# Composed parse: slide_013

- source frame: `slide_013.jpg` (md5 `0da0fb6516f5b76f76ef74a6995508cd`)
- parse model: `nemotron-3.5-parse` · chat model: `docparsechat`
- degraded: False
- elements kept: 8 (dedup collapsed 1) · crops: 3 · failed calls: 0

## Positioned elements (reading order: y then x)

- `<class_Text>` @(x=867, y=63, w=20, h=19) — from full/slide_013.parse.md (level 0)
  13
- `<class_Section-header>` @(x=280, y=67, w=434, h=27) — from full/slide_013.parse.md (level 0)
  **Classification of “XOR” Truth Table**
- `<class_Picture>` @(x=523, y=99, w=329, h=277) — from crops/slide_013.crop01__picture.parse.md (level 1)
  X2 X X1
- `<class_Picture>` @(x=535, y=109, w=306, h=258) — from full/slide_013.parse.md (level 0)
  X2 X X1 X1
- `<class_Table>` @(x=96, y=138, w=219, h=169) — from full/slide_013.parse.md (level 0)
  \begin{tabular}{ccc} \thead{X<sub>1</sub>} & \thead{X<sub>2</sub>} & \thead{O/P}\\ 0 & 0 & 0\\ 0 & 1 & 1\\ 1 & 0 & 1\\ 1 & 1 & 0\\ \end{tabular}
- `<class_Chart>` @(x=125, y=345, w=404, h=149) — from crops/slide_013.crop03__picture.parse.md (level 1)
  <chart type="line"> bind: value ; ; y | category | value | | --- | --- | | x1 | ? | | x2 | ? | | I | ? | </chart>
- `<class_Picture>` @(x=140, y=351, w=375, h=138) — from full/slide_013.parse.md (level 0)
  X1 ? X2 ? Z O/P 1 ?
- `<class_Page-footer>` @(x=591, y=424, w=209, h=27) — from full/slide_013.parse.md (level 0)
  _Not Linearly Separable_

## Unpositioned text

- (none)

## Failed calls

- (none)

## Notes

- backstop stops: 0
- parse calls spent: 4 · chat calls: 1 · retries: 0

# Composed parse: slide_010

- source frame: `slide_010.jpg` (md5 `bbb9974d7869e22121b5621192dd23db`)
- parse model: `nemotron-3.5-parse` · chat model: `docparsechat`
- degraded: False
- elements kept: 14 (dedup collapsed 0) · crops: 6 · failed calls: 0

## Positioned elements (reading order: y then x)

- `<class_Picture>` @(x=12, y=36, w=670, h=145) — from crops/slide_010.crop02__picture.parse.md (level 2)
  Recall Correctly Classified (as Positive) Total objects that should be retrieved (Actually Positive)
- `<class_Picture>` @(x=36, y=41, w=861, h=476) — from full/slide_010.parse.md (level 0)
  **Recall** **Correctly Classified (as Positive)** **Total objects that should be retrieved (Actually Positive)** **Meaning** **Does the classifier miss any of Positive Objects ?** **Recall =** **TP** **+ FN** **Precision= 18/(18+12)** **=60%** **Positive** **Classified as +ive** **Positive** **Classified as -ive** All Positive Samples in the Dataset _If you said: I picked ALL_ Positive objects,_ _can I trust you ? At what %?_
- `<class_Picture>` @(x=36, y=42, w=621, h=134) — from crops/slide_010.crop01__picture.parse.md (level 1)
  **Recall** **Correctly Classified (as Positive)** **Total objects that should be retrieved (Actually Positive)**
- `<class_Chart>` @(x=668, y=49, w=186, h=108) — from crops/slide_010.crop03__table.parse.md (level 2)
  <chart type="ranked_table"> title: Predicted as | column_1 | P | N | | --- | --- | --- | | P | TP | FN | | N | FP | TN | </chart>
- `<class_Table>` @(x=674, y=53, w=173, h=100) — from crops/slide_010.crop01__picture.parse.md (level 1)
  \begin{tabular}{cccc} \multirow{2}{*}{\thead{\mbox{}}} & \multicolumn{3}{c}{\thead{Predicted as}}\\ \mbox{} & \thead{P} & \thead{N} & \thead{\mbox{}}\\ \thead{Actual} & P & TP & FN\\ \thead{N} & N & FP & TN\\ \end{tabular}
- `<class_Chart>` @(x=668, y=163, w=198, h=129) — from crops/slide_010.crop04__table.parse.md (level 2)
  <chart type="ranked_table"> title: Predicted as | column_1 | P | N | | --- | --- | --- | | Actual | P | 18 12 | | Actual | N | 10 60 | </chart>
- `<class_Table>` @(x=675, y=168, w=184, h=119) — from crops/slide_010.crop01__picture.parse.md (level 1)
  \begin{tabular}{ccc} \multirow{2}{*}{\thead{Actual}} & \thead{P} & \thead{N}\\ \mbox{} & P & 18 12\\ \thead{N} & 10 & 60\\ \end{tabular}
- `<class_Text>` @(x=74, y=203, w=470, h=53) — from crops/slide_010.crop01__picture.parse.md (level 1)
  **Meaning** **Does the classifier miss any of Positive Objects ?**
- `<class_Picture>` @(x=58, y=256, w=289, h=153) — from crops/slide_010.crop05__picture.parse.md (level 2)
  Recall = TP TP + FN Positive Positive Classified as -ive Classified as -ive
- `<class_Picture>` @(x=68, y=261, w=268, h=142) — from crops/slide_010.crop01__picture.parse.md (level 1)
  **Recall =** TP **Precision= 18/(18+12)** **=60%** Positive **Positive** Classified as +ive **Classified as -ive**
- `<class_Chart>` @(x=518, y=281, w=376, h=229) — from crops/slide_010.crop06__picture.parse.md (level 2)
  <chart type="lollipop"> bind: Positive ; ; y | Category | Positive | | --- | --- | | TP | 18 | | FN | 30 | | TN | 60 | | FP | 70 | </chart>
- `<class_Picture>` @(x=532, y=290, w=348, h=212) — from crops/slide_010.crop01__picture.parse.md (level 1)
  Positive Negative 70 10 TP FN 12 60 10
- `<class_Footnote>` @(x=88, y=404, w=246, h=19) — from crops/slide_010.crop01__picture.parse.md (level 1)
  All Positive Samples in the Dataset
- `<class_Text>` @(x=82, y=468, w=300, h=37) — from crops/slide_010.crop01__picture.parse.md (level 1)
  _If you said: I picked ALL Positive objects,_ _can I trust you ? At what %?_

## Unpositioned text

- (none)

## Failed calls

- (none)

## Notes

- backstop stops: 0
- parse calls spent: 7 · chat calls: 2 · retries: 0

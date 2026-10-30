# Composed parse: slide_011

- source frame: `slide_011.jpg` (md5 `4bf9fdb56ba8127ebb08e84cbb8b7425`)
- parse model: `nemotron-3.5-parse` · chat model: `docparsechat`
- degraded: False
- elements kept: 21 (dedup collapsed 0) · crops: 4 · failed calls: 0

## Positioned elements (reading order: y then x)

- `<class_Chart>` @(x=667, y=51, w=187, h=107) — from crops/slide_011.crop01__table.parse.md (level 1)
  <chart type="ranked_table"> title: Predicted as | column_1 | P | N | | --- | --- | --- | | P | TP | FN | | N | FP | TN | </chart>
- `<class_Table>` @(x=674, y=55, w=172, h=99) — from full/slide_011.parse.md (level 0)
  \begin{tabular}{cccc} \multirow{2}{*}{\thead{\mbox{}}} & \multicolumn{3}{c}{\thead{Predicted as}}\\ \mbox{} & P & N & \mbox{}\\ \thead{Actual} & P & FP & FN\\ \thead{N} & NP & FP & TN\\ \end{tabular}
- `<class_Text>` @(x=866, y=57, w=17, h=22) — from full/slide_011.parse.md (level 0)
  11
- `<class_Section-header>` @(x=315, y=58, w=142, h=43) — from full/slide_011.parse.md (level 0)
  **Recall**
- `<class_Text>` @(x=208, y=127, w=309, h=24) — from full/slide_011.parse.md (level 0)
  **Correctly Classified (as Positive)**
- `<class_Text>` @(x=96, y=159, w=540, h=24) — from full/slide_011.parse.md (level 0)
  **Total objects that should be retrieved (Actually Positive)**
- `<class_Chart>` @(x=672, y=164, w=193, h=127) — from crops/slide_011.crop02__table.parse.md (level 1)
  <chart type="ranked_table"> title: Predicted as | column_1 | P | N | | --- | --- | --- | | Actual P | 28 | 2 | | N | 30 | 40 | </chart>
- `<class_Table>` @(x=679, y=169, w=179, h=117) — from full/slide_011.parse.md (level 0)
  \begin{tabular}{ccc} \multirow{2}{*}{\thead{Actual}} & \thead{P} & \thead{N}\\ \mbox{} & P & 28 2\\ N & 30 & 40\\ \end{tabular}
- `<class_Section-header>` @(x=75, y=203, w=117, h=30) — from full/slide_011.parse.md (level 0)
  **Meaning**
- `<class_Text>` @(x=76, y=232, w=467, h=24) — from full/slide_011.parse.md (level 0)
  **Does the classifier miss any of Positive Objects ?**
- `<class_Picture>` @(x=229, y=269, w=81, h=54) — from crops/slide_011.crop03__picture.parse.md (level 1)
  TP P + FN
- `<class_Picture>` @(x=232, y=271, w=76, h=51) — from full/slide_011.parse.md (level 0)
  **TP** **TP + FN**
- `<class_Text>` @(x=82, y=283, w=78, h=21) — from full/slide_011.parse.md (level 0)
  **Recall =**
- `<class_Chart>` @(x=519, y=284, w=368, h=224) — from crops/slide_011.crop04__picture.parse.md (level 1)
  <chart type="lollipop"> bind: Positive ; ; y | Category | Positive | | --- | --- | | TP | 28 | | FN | 30 | | TN | 40 | | FP | 30 | </chart>
- `<class_Picture>` @(x=534, y=292, w=339, h=208) — from full/slide_011.parse.md (level 0)
  Positive Negative 30 28 2 40 30 TP FN TN FP
- `<class_Text>` @(x=340, y=294, w=135, h=38) — from full/slide_011.parse.md (level 0)
  **Recall= 28/(28+2)** **=93.3%**
- `<class_Text>` @(x=114, y=344, w=96, h=30) — from full/slide_011.parse.md (level 0)
  Positive Classified as +ive
- `<class_Text>` @(x=225, y=345, w=92, h=30) — from full/slide_011.parse.md (level 0)
  Positive Classified as -ive
- `<class_Text>` @(x=87, y=404, w=246, h=18) — from full/slide_011.parse.md (level 0)
  _All Positive Samples in the Dataset_
- `<class_Text>` @(x=74, y=441, w=409, h=35) — from full/slide_011.parse.md (level 0)
  _Higher Recall means I **HIGHLY** _trust you if you said I picked_ **_ALL_** _Positive Objects._
- `<class_Text>` @(x=77, y=480, w=405, h=19) — from full/slide_011.parse.md (level 0)
  _It Does NOT_ _mean All you said Positive are Actually Positive_

## Unpositioned text

- (none)

## Failed calls

- (none)

## Notes

- backstop stops: 0
- parse calls spent: 5 · chat calls: 1 · retries: 0

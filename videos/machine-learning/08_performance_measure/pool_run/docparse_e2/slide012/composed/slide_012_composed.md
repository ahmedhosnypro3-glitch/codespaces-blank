# Composed parse: slide_012

- source frame: `slide_012.jpg` (md5 `2270c4a26266a9cc2e0a056baa389228`)
- parse model: `nemotron-3.5-parse` · chat model: `docparsechat`
- degraded: False
- elements kept: 23 (dedup collapsed 0) · crops: 5 · failed calls: 0

## Positioned elements (reading order: y then x)

- `<class_Chart>` @(x=667, y=51, w=187, h=107) — from crops/slide_012.crop01__table.parse.md (level 1)
  <chart type="ranked_table"> title: Predicted as | column_1 | P | N | | --- | --- | --- | | P | TP | FN | | N | FP | TN | </chart>
- `<class_Table>` @(x=674, y=55, w=172, h=99) — from full/slide_012.parse.md (level 0)
  \begin{tabular}{ccc} \multirow{2}{*}{\thead{\mbox{}}} & \multicolumn{2}{c}{\thead{Predicted as}}\\ \mbox{} & P & N\\ P & TP & FN\\ N & FP & TN\\ \end{tabular}
- `<class_Text>` @(x=865, y=57, w=19, h=22) — from full/slide_012.parse.md (level 0)
  12
- `<class_Section-header>` @(x=316, y=58, w=141, h=43) — from full/slide_012.parse.md (level 0)
  **Recall**
- `<class_Text>` @(x=209, y=127, w=308, h=24) — from full/slide_012.parse.md (level 0)
  **Correctly Classified (as Positive)**
- `<class_Text>` @(x=96, y=159, w=540, h=24) — from full/slide_012.parse.md (level 0)
  **Total objects that should be retrieved (Actually Positive)**
- `<class_Chart>` @(x=674, y=165, w=191, h=126) — from crops/slide_012.crop02__table.parse.md (level 1)
  <chart type="ranked_table"> title: Predicted as | column_1 | P | N | | --- | --- | --- | | Actual P | 30 | 0 | | N | 70 | 0 | </chart>
- `<class_Table>` @(x=681, y=170, w=177, h=116) — from full/slide_012.parse.md (level 0)
  \begin{tabular}{ccc} \multirow{2}{*}{\thead{Actual}} & \thead{P} & \thead{N}\\ \mbox{} & P & 0\\ P & 80 & 0\\ N & 70 & 0\\ \end{tabular}
- `<class_Section-header>` @(x=75, y=203, w=117, h=30) — from full/slide_012.parse.md (level 0)
  **Meaning**
- `<class_Text>` @(x=76, y=232, w=470, h=24) — from full/slide_012.parse.md (level 0)
  **Does the classified miss any of Positive Objects ?**
- `<class_Picture>` @(x=229, y=269, w=81, h=54) — from crops/slide_012.crop03__picture.parse.md (level 1)
  TP P + FN
- `<class_Picture>` @(x=232, y=271, w=76, h=51) — from full/slide_012.parse.md (level 0)
  **TP** **TP + FN**
- `<class_Text>` @(x=82, y=284, w=78, h=20) — from full/slide_012.parse.md (level 0)
  **Recall =**
- `<class_Text>` @(x=340, y=294, w=160, h=38) — from full/slide_012.parse.md (level 0)
  **Precision= 30/(30+0)** **=100%**
- `<class_Chart>` @(x=726, y=315, w=145, h=188) — from crops/slide_012.crop04__picture.parse.md (level 1)
  <chart type="lollipop"> | column_1 | column_2 | | --- | --- | | TN | 70 | | FP | 70 | </chart>
- `<class_Picture>` @(x=731, y=322, w=135, h=174) — from full/slide_012.parse.md (level 0)
  70 0 70 70
- `<class_Text>` @(x=112, y=344, w=98, h=30) — from full/slide_012.parse.md (level 0)
  Positive Classified as +ive
- `<class_Text>` @(x=225, y=345, w=93, h=30) — from full/slide_012.parse.md (level 0)
  Positive Classified as -ive
- `<class_Chart>` @(x=542, y=367, w=152, h=133) — from crops/slide_012.crop05__picture.parse.md (level 1)
  <chart type="lollipop"> | category | value | | --- | --- | | TP | 30 | | FN | 0 | </chart>
- `<class_Picture>` @(x=548, y=372, w=140, h=122) — from full/slide_012.parse.md (level 0)
  30 TP TN FP
- `<class_Text>` @(x=88, y=404, w=246, h=18) — from full/slide_012.parse.md (level 0)
  _All Positive Samples in the Dataset_
- `<class_Text>` @(x=68, y=451, w=297, h=19) — from full/slide_012.parse.md (level 0)
  **_Model Try to catch ALL Positive Samples_**
- `<class_Text>` @(x=68, y=476, w=422, h=19) — from full/slide_012.parse.md (level 0)
  **_(Irrespective of classifying NEGATIVE Objects as Positive)_**

## Unpositioned text

- (none)

## Failed calls

- (none)

## Notes

- backstop stops: 0
- parse calls spent: 6 · chat calls: 1 · retries: 0

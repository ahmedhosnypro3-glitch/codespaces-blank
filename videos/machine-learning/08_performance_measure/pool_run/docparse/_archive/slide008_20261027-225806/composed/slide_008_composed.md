# Composed parse: slide_008

- source frame: `slide_008.jpg` (md5 `aea4d28ad4a0e047be5b3efa6a2e18d5`)
- parse model: `nemotron-3.5-parse` · chat model: `docparsechat`
- degraded: True (chat probe failed — decisions use the deterministic-conservative fallback)
- elements kept: 21 (dedup collapsed 0) · crops: 4 · failed calls: 0

## Positioned elements (reading order: y then x)

- `<class_Chart>` @(x=667, y=51, w=187, h=107) — from crops/slide_008.crop01__table.parse.md (level 1)
  <chart type="ranked_table"> title: Predicted as | column_1 | P | N | | --- | --- | --- | | P | TP | FN | | N | FP | TN | </chart>
- `<class_Table>` @(x=674, y=55, w=172, h=99) — from full/slide_008.parse.md (level 0)
  \begin{tabular}{ccc} \multirow{2}{*}{\thead{\mbox{}}} & \multicolumn{2}{c}{\thead{Predicted as}}\\ \mbox{} & P & N\\ P & TP & FN\\ N & FP & TN\\ \end{tabular}
- `<class_Text>` @(x=866, y=56, w=13, h=22) — from full/slide_008.parse.md (level 0)
  8
- `<class_Section-header>` @(x=315, y=58, w=216, h=44) — from full/slide_008.parse.md (level 0)
  **Precision**
- `<class_Text>` @(x=207, y=118, w=310, h=23) — from full/slide_008.parse.md (level 0)
  **Correctly Classified (as Positive)**
- `<class_Text>` @(x=89, y=150, w=553, h=24) — from full/slide_008.parse.md (level 0)
  **Total Classified as Positive (either Correct and Erroneous)**
- `<class_Chart>` @(x=674, y=165, w=190, h=125) — from crops/slide_008.crop02__table.parse.md (level 1)
  <chart type="ranked_table"> title: Predicted as | column_1 | P | N | | --- | --- | --- | | Actual P | 10 | 20 | | N | 2 | 68 | </chart>
- `<class_Table>` @(x=681, y=170, w=176, h=115) — from full/slide_008.parse.md (level 0)
  \begin{tabular}{ccc} \multirow{2}{*}{\thead{Actual}} & \thead{P} & \thead{N}\\ \mbox{} & P & 10 20\\ N & 2 & 68\\ \end{tabular}
- `<class_Section-header>` @(x=74, y=202, w=100, h=27) — from full/slide_008.parse.md (level 0)
  **Meaning**
- `<class_Text>` @(x=75, y=231, w=540, h=26) — from full/slide_008.parse.md (level 0)
  **% of what you** **Predicted** **as POSITIVE** **is Actually Positive**
- `<class_Picture>` @(x=230, y=270, w=61, h=49) — from crops/slide_008.crop03__picture.parse.md (level 1)
  TP P + FP
- `<class_Picture>` @(x=232, y=272, w=57, h=45) — from full/slide_008.parse.md (level 0)
  TP TP + FP
- `<class_Text>` @(x=82, y=281, w=107, h=21) — from full/slide_008.parse.md (level 0)
  **Precision =**
- `<class_Chart>` @(x=519, y=284, w=376, h=227) — from crops/slide_008.crop04__picture.parse.md (level 1)
  <chart type="lollipop"> bind: Positive ; ; y | Category | Negative | | --- | --- | | TP | 10 | | FN | 20 | | TN | 68 | | FP | 2 | </chart>
- `<class_Picture>` @(x=532, y=292, w=349, h=211) — from full/slide_008.parse.md (level 0)
  Positive Negative 30 70 10 20 68 2 TP FN TN FP
- `<class_Text>` @(x=342, y=294, w=158, h=38) — from full/slide_008.parse.md (level 0)
  **Precision= 10/(10+2)** **= 83.3%**
- `<class_Text>` @(x=112, y=344, w=98, h=30) — from full/slide_008.parse.md (level 0)
  Positive Classified as +ive
- `<class_Text>` @(x=223, y=345, w=97, h=30) — from full/slide_008.parse.md (level 0)
  Negative Classified as +ive
- `<class_Text>` @(x=73, y=410, w=240, h=18) — from full/slide_008.parse.md (level 0)
  _All Samples classified_ as _Positive_
- `<class_Text>` @(x=76, y=435, w=370, h=35) — from full/slide_008.parse.md (level 0)
  _Higher Precision value DOES NOT mean you correctly_ _retrieved I more_ _Positive samples._
- `<class_Text>` @(x=77, y=475, w=364, h=34) — from full/slide_008.parse.md (level 0)
  _It means i HIGHLY trust you if you said this sample is_ _Positive_

## Unpositioned text

- (none)

## Failed calls

- (none)

## Notes

- backstop stops: 0
- parse calls spent: 5 · chat calls: 0 · retries: 0

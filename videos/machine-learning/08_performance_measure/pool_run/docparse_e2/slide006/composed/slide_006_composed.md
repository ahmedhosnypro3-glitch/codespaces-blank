# Composed parse: slide_006

- source frame: `slide_006.jpg` (md5 `9e422ba294d0fb6ee75edbeb450fd14a`)
- parse model: `nemotron-3.5-parse` · chat model: `docparsechat`
- degraded: False
- elements kept: 20 (dedup collapsed 0) · crops: 3 · failed calls: 0

## Positioned elements (reading order: y then x)

- `<class_Chart>` @(x=667, y=47, w=186, h=109) — from crops/slide_006.crop01__table.parse.md (level 1)
  <chart type="ranked_table"> title: Predicted as | column_1 | P | N | | --- | --- | --- | | P | TP | FN | | N | FP | TN | </chart>
- `<class_Table>` @(x=674, y=51, w=174, h=102) — from full/slide_006.parse.md (level 0)
  \begin{tabular}{ccc} \multirow{2}{*}{\thead{\mbox{}}} & \multicolumn{2}{c}{\thead{Predicted as}}\\ \mbox{} & P & N\\ \thead{Actual} & P & FN\\ \thead{N} & NP & TN\\ \end{tabular}
- `<class_Picture>` @(x=866, y=57, w=13, h=24) — from full/slide_006.parse.md (level 0)
  6
- `<class_Section-header>` @(x=315, y=60, w=217, h=46) — from full/slide_006.parse.md (level 0)
  **Accuracy**
- `<class_Text>` @(x=210, y=118, w=393, h=23) — from full/slide_006.parse.md (level 0)
  **Correctly Classified (Positive & Negative)**
- `<class_Text>` @(x=244, y=151, w=246, h=22) — from full/slide_006.parse.md (level 0)
  **Total Number of Samples**
- `<class_Chart>` @(x=672, y=165, w=190, h=125) — from crops/slide_006.crop02__table.parse.md (level 1)
  <chart type="ranked_table"> title: Predicted as | column_1 | P | N | | --- | --- | --- | | P | 18 | 12 | | N | 10 | 60 | </chart>
- `<class_Table>` @(x=679, y=170, w=177, h=115) — from full/slide_006.parse.md (level 0)
  \begin{tabular}{ccc} \multirow{2}{*}{\thead{Actual}} & \thead{P} & \thead{N}\\ \mbox{} & P & 18 12\\ \thead{N} & 10 & 60\\ \end{tabular}
- `<class_Text>` @(x=66, y=179, w=91, h=22) — from full/slide_006.parse.md (level 0)
  **Meaning**
- `<class_Text>` @(x=66, y=201, w=594, h=20) — from full/slide_006.parse.md (level 0)
  **How Accurate is the Classification (for Both Positive and Negative Classes)**
- `<class_Text>` @(x=214, y=236, w=136, h=17) — from full/slide_006.parse.md (level 0)
  _Correctly Classified_
- `<class_Text>` @(x=82, y=279, w=326, h=48) — from full/slide_006.parse.md (level 0)
  **Accuracy =** **TP + TN** **TP + FP + TN + FN**
- `<class_Chart>` @(x=525, y=284, w=361, h=224) — from crops/slide_006.crop03__picture.parse.md (level 1)
  <chart type="lollipop"> bind: Positive ; ; y | Category | Positive | | --- | --- | | TP | 18 | | FN | 30 | | TN | 60 | | FP | 70 | </chart>
- `<class_Picture>` @(x=538, y=292, w=335, h=208) — from full/slide_006.parse.md (level 0)
  Positive Negative 30 18 12 60 10 TP FN TN FP
- `<class_Text>` @(x=254, y=351, w=89, h=17) — from full/slide_006.parse.md (level 0)
  _All Samples_
- `<class_Text>` @(x=77, y=378, w=261, h=36) — from full/slide_006.parse.md (level 0)
  **Accuracy= (18+60)/(18+12+60+10)** **= 78/100 = 78%**
- `<class_Text>` @(x=386, y=379, w=89, h=35) — from full/slide_006.parse.md (level 0)
  _Accuracy of_ _ALL Classes_
- `<class_Text>` @(x=76, y=438, w=375, h=19) — from full/slide_006.parse.md (level 0)
  What About Precision of Positive Class ONLY Results?
- `<class_Text>` @(x=75, y=464, w=295, h=18) — from full/slide_006.parse.md (level 0)
  What About Recall % of Positive Samples ?
- `<class_Text>` @(x=78, y=488, w=322, h=18) — from full/slide_006.parse.md (level 0)
  Conclusion: Accuracy is Good but Not Sufficient

## Unpositioned text

- (none)

## Failed calls

- (none)

## Notes

- backstop stops: 0
- parse calls spent: 4 · chat calls: 1 · retries: 0

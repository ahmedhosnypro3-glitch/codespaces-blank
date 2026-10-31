# Composed parse: slide_029

- source frame: `slide_029.jpg` (md5 `a300102babed5caa6e53f6f611b1cb66`)
- parse model: `nemotron-3.5-parse` · chat model: `docparsechat`
- degraded: False
- elements kept: 4 (dedup collapsed 1) · crops: 4 · failed calls: 0

## Positioned elements (reading order: y then x)

- `<class_Picture>` @(x=38, y=40, w=867, h=478) — from crops/slide_029.crop01__table.parse.md (level 1)
  Threshold=0.0 Predicted as P N TPR=5/(5+0)=1 FPR=6/(6+0)=1 0.0 P TPR FPR ROC Curve for Same Model -different thresholds P PR = TP + FN Predicted as P N P TP FN N FP TN
- `<class_Table>` @(x=35, y=40, w=874, h=476) — from full/slide_029.parse.md (level 0)
  \begin{tabular}{ccccc} \multirow{2}{*}{\thead{\mbox{}}} & \multicolumn{4}{c}{\thead{Threshold=0.0}}\\ \mbox{} & \thead{P} & \thead{N} & \multirow{2}{*}{\thead{TPR=5/(5+0)=1 FPR=6/(6+0)=1}} & \multirow{2}{*}{\thead{0.0}}\\ \thead{Actual} & \thead{P} & \thead{S} & \mbox{} & \mbox{}\\ \thead{\mbox{}} & \thead{N} & \thead{6} & \thead{0} & \mbox{}\\ \mbox{} & \mbox{} & \mbox{} & \mbox{} & TPR\\ \mbox{} & \mbox{} & \mbox{} & \mbox{} & FPR\\ \mbox{} & \mbox{} & ROC Curve for Same Model -different thresholds & TPR = TP + FN & Predicted as P N\\ \mbox{} & \mbox{} & \mbox{} & \mbox{} & P N\\ \mbox{} & \mbox{} & FPR = FP FP+TN & P FP TN & FN\\ \end{tabular}
- `<class_Picture>` @(x=36, y=42, w=888, h=494) — from crops/slide_029.crop03__picture.parse.md (level 3)
  Threshold=0.0 Predicted as P N TPR=5/(5+0)=1 FPR=6/(6+0)=1 Actual P TPR ROC Curve for Same Model -different thresholds Predicted as P N P TP FN FN N FP TN
- `<class_Picture>` @(x=36, y=42, w=869, h=475) — from crops/slide_029.crop02__picture.parse.md (level 2)
  Threshold=0.0 29 Actual P 5 0 N 6 0 TPR=5/(5+0)=1 FPR=6/(6+0)=1 TPR FPR ROC Curve for Same Model -different thresholds Predicted as P N Actual P TP FN FN FN

## Unpositioned text

- (none)

## Failed calls

- (none)

## Notes

- backstop stops: 0
- parse calls spent: 5 · chat calls: 4 · retries: 3

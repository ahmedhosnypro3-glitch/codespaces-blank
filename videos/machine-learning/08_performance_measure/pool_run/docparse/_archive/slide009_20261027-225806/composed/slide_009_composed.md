# Composed parse: slide_009

- source frame: `slide_009.jpg` (md5 `6ff97d9c1683447c74f6293b3211db00`)
- parse model: `nemotron-3.5-parse` · chat model: `docparsechat`
- degraded: True (chat probe failed — decisions use the deterministic-conservative fallback)
- elements kept: 5 (dedup collapsed 1) · crops: 5 · failed calls: 0

## Positioned elements (reading order: y then x)

- `<class_Picture>` @(x=36, y=41, w=874, h=477) — from full/slide_009.parse.md (level 0)
  **Precision** Correctly Classified (as Positive) Total Classified as Positive (either Correct and Erroneous) Predicted as Actual P N % of what you Predicted as POSITIVE is Actually Positive Predicted as P 5 25 N 0 70 Precision = TP TP + FP Precision= 5/(5+0) = 100% Positive Negative Positive Negative Classified as †ive Positive Classified as †ive Positive Classified as †ive All Samples classified as Positive Whatever objects you retrieved as positive, I can trust you _(Irrespective of how many MISSED Positive samples)_
- `<class_Picture>` @(x=37, y=41, w=869, h=476) — from crops/slide_009.crop01__picture.parse.md (level 1)
  **Precision** Correctly Classified (as Positive) Total Classified as Positive (either Correct and Erroneous) **Meaning** % of what you Predicted as POSITIVE is Actually Positive Actual P 5 25 N 0 70 **Precision =** TP **+ FP** **Precision= 5/(5+0)** **= 100%** Positive Negative Positive 30 5 25 TN 0 TP FN TN FP
- `<class_Picture>` @(x=36, y=42, w=868, h=476) — from crops/slide_009.crop04__picture.parse.md (level 4)
  **Precision** Correctly Classified (as Positive) Total Classified as Positive (either Correct and Erroneous) Meaning % of what you Predicted as POSITIVE is Actually Positive Actual P 5 25 N 0 70 The Precision = TP Precision= 5/(5+0) = 100% Positive Negative 30 70 5 25 70 0 TP FN TN FP
- `<class_Picture>` @(x=36, y=42, w=868, h=475) — from crops/slide_009.crop03__picture.parse.md (level 3)
  **Precision** Correctly Classified (as Positive) Total Classified as Positive (either Correct and Erroneous) **Meaning** % of what you Predicted as POSITIVE is Actually Positive Actual Precision = TP TP + FP Precision= 5/(5+0) = 100% Positive Negative Positive 30 70 5 25 70 0 TP FN TN FP
- `<class_Picture>` @(x=36, y=42, w=870, h=474) — from crops/slide_009.crop02__picture.parse.md (level 2)
  **Precision** Correctly Classified (as Positive) Total Classified as Positive (either Correct and Erroneous) **Meaning** % of what you Predicted as POSITIVE is Actually Positive Actual P 5 25 N 0 70 The Precision = TP Precision= 5/(5+0) = 100% Positive Negative 30 70 5 25 70 0 TP FN TN FP

## Unpositioned text

- (none)

## Failed calls

- (none)

## Notes

- backstop stops: 0
- parse calls spent: 6 · chat calls: 0 · retries: 0

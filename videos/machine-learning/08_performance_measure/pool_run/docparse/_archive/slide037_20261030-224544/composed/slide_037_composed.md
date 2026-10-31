# Composed parse: slide_037

- source frame: `slide_037.jpg` (md5 `d660335f6421502a36d1255b1f2d6078`)
- parse model: `nemotron-3.5-parse` · chat model: `docparsechat`
- degraded: True (chat probe failed — decisions use the deterministic-conservative fallback)
- elements kept: 12 (dedup collapsed 2) · crops: 5 · failed calls: 0

## Positioned elements (reading order: y then x)

- `<class_Picture>` @(x=555, y=35, w=390, h=682) — from crops_supp/rcol/slide037.rcol.parse.md (level 1)
  37 (AUC) thresholds for each model) FBR=0, TPR=1] argest area under the curve
- `<class_Section-header>` @(x=294, y=62, w=315, h=24) — from full/slide_037.parse.md (level 0)
  **Area Under the Curve (AUC)**
- `<class_Page-header>` @(x=867, y=64, w=20, h=15) — from full/slide_037.parse.md (level 0)
  37
- `<class_Text>` @(x=102, y=96, w=683, h=22) — from full/slide_037.parse.md (level 0)
  **Compare between different models (at different thresholds for each model)**
- `<class_Text>` @(x=101, y=151, w=590, h=22) — from full/slide_037.parse.md (level 0)
  Best Model is the model trying to reach the point at **[FBR=0, TPR=1]**
- `<class_Text>` @(x=100, y=183, w=691, h=21) — from full/slide_037.parse.md (level 0)
  In other words, Best model is the model that has the largest area under the curve
- `<class_Chart>` @(x=245, y=205, w=402, h=319) — from crops/slide_037.crop01__chart.parse.md (level 1)
  <chart type="multi_line"> axis[x]: FPR axis[y]: TPR bind: FPR ; ; x bind: Best Model Largest Area Under the Curve ; ; y annotation: callout ; label=Best Model Largest Area Under the Curve) annotation: callout ; label=Worst Model Smallest Area Under the Curve | FPR | Best Model Largest Area Under the Curve | | --- | --- | | 0 | 0 | | 1 | 50 | | 2 | 60 | | 3 | 70 | </chart>
- `<class_Text>` @(x=101, y=215, w=498, h=77) — from crops_supp/ltop/slide037.ltop.parse.md (level 1)
  Compare between <u>different models</u> (at different threshing
- `<class_Chart>` @(x=260, y=217, w=373, h=296) — from full/slide_037.parse.md (level 0)
  <chart type="multi_line"> axis[x]: FPR axis[y]: TPR bind: FPR ; ; x bind: Best Model Largest Area Under the Curve ; ; y annotation: callout ; label=Best Model Largest Area Under the Curve) annotation: callout ; label=Worst Model Smallest Area Under the Curve | FPR | Best Model Largest Area Under the Curve | | --- | --- | | 0 | 0 | | 1 | 20 | | 2 | 40 | | 3 | 60 | | 4 | 80 | | 5 | 90 | </chart>
- `<class_Picture>` @(x=30, y=345, w=569, h=524) — from crops_supp/lbot/slide037.lbot.parse.md (level 1)
  Smallest Are Under the Cub
- `<class_Text>` @(x=102, y=382, w=497, h=77) — from crops_supp/ltop/slide037.ltop.parse.md (level 1)
  Best Model is the model trying to reach the point at [FBR=
- `<class_Text>` @(x=102, y=475, w=497, h=69) — from crops_supp/ltop/slide037.ltop.parse.md (level 1)
  In other words, Best model is the model that has the largest

## Unpositioned text

- (none)

## Failed calls

- (none)

## Notes

- backstop stops: 0
- parse calls spent: 2 · chat calls: 0 · retries: 0

# Composed parse: slide_025

- source frame: `slide_025.jpg` (md5 `e47552f20a61e34886987959094892ef`)
- parse model: `nemotron-3.5-parse` · chat model: `docparsechat`
- degraded: True (chat probe failed — decisions use the deterministic-conservative fallback)
- elements kept: 22 (dedup collapsed 0) · crops: 8 · failed calls: 0

## Positioned elements (reading order: y then x)

- `<class_Picture>` @(x=26, y=33, w=260, h=279) — from crops/slide_025.crop04__picture.parse.md (level 2)
  Vani Long Chain of Derivatives f ( x) = ReLU = \(\{\begin{array}{ c } 0 \\ \thead{for x<0} \\ \thead{x for x≥0} 0\linebreak{}\linebreak{}f'(x)=\{\begin{array}{ c } 0 \\ \thead{for x<0} \\ \thead{for x≥0} 1 \\ \end{array}\)
- `<class_Picture>` @(x=38, y=40, w=883, h=499) — from full/slide_025.parse.md (level 0)
  25 _Long Chain of Derivatives_ f(x) = ReLU = 0 for x<0 x for x≥0 f'(x)= 1 for x<0 for x≥0 Node Bias 1 1
- `<class_Picture>` @(x=36, y=43, w=240, h=259) — from crops/slide_025.crop01__picture.parse.md (level 1)
  **Vanishing and Exploding Gradients** 25 _Long Chain of Derivatives_ **Class 1** f ( x) = ReLU = 0 for x<0 x for x≥0 f '( x)= 0 for x<0 1 for x≥0
- `<class_Page-header>` @(x=870, y=52, w=45, h=39) — from crops/slide_025.crop01__picture.parse.md (level 1)
  25
- `<class_Picture>` @(x=284, y=108, w=566, h=203) — from crops/slide_025.crop05__picture.parse.md (level 2)
  Error Error Error
- `<class_Picture>` @(x=306, y=116, w=524, h=188) — from crops/slide_025.crop01__picture.parse.md (level 1)
- `<class_Text>` @(x=869, y=146, w=34, h=11) — from crops/slide_025.crop01__picture.parse.md (level 1)
  **Class 1**
- `<class_Text>` @(x=842, y=150, w=14, h=111) — from crops/slide_025.crop01__picture.parse.md (level 1)
  **Error Error Error**
- `<class_Text>` @(x=871, y=199, w=32, h=11) — from crops/slide_025.crop01__picture.parse.md (level 1)
  **Class 2**
- `<class_Text>` @(x=868, y=258, w=36, h=11) — from crops/slide_025.crop01__picture.parse.md (level 1)
  **Class m**
- `<class_Caption>` @(x=100, y=318, w=149, h=19) — from crops/slide_025.crop01__picture.parse.md (level 1)
  **Exploding Gradients**
- `<class_Caption>` @(x=546, y=334, w=151, h=18) — from crops/slide_025.crop01__picture.parse.md (level 1)
  **Vanishing Gradients**
- `<class_Chart>` @(x=72, y=341, w=246, h=178) — from crops/slide_025.crop06__chart.parse.md (level 2)
  <chart type="line"> axis[x]: x axis[y]: f bind: x ; ; x bind: f ; ; y | x | f | | --- | --- | | -10 | 0 | | -5 | 0 | | 0 | 0 | | 5 | 5 | | 10 | 10 | </chart>
- `<class_Chart>` @(x=81, y=348, w=227, h=165) — from crops/slide_025.crop01__picture.parse.md (level 1)
  <chart type="line"> axis[x]: x axis[y]: f bind: x ; ; x bind: f ; ; y | x | f | | --- | --- | | -10 | 0 | | -5 | 0 | | 0 | -1 | | 5 | 4 | | 10 | 10 | </chart>
- `<class_Chart>` @(x=353, y=355, w=272, h=164) — from crops/slide_025.crop02__chart.parse.md (level 1)
  <chart type="multi_line"> title: Sigmoid legend[color]: items=Tanh ; Sigmoid bind: Tanh ; ; y bind: Sigmoid ; ; y | x | Tanh | Sigmoid | | --- | --- | --- | | -4 | 0.00 | -1.00 | | -2 | 0.15 | -1.00 | | 0 | 0.50 | 0.00 | | 2 | 0.90 | 0.98 | | 4 | 1.00 | 1.00 | </chart>
- `<class_Chart>` @(x=356, y=356, w=269, h=163) — from crops/slide_025.crop07__chart.parse.md (level 2)
  <chart type="multi_line"> title: Sigmoid legend[color]: items=Tanh ; Sigmoid bind: Tanh ; ; y bind: Sigmoid ; ; y | x | Tanh | Sigmoid | | --- | --- | --- | | -4 | 0.00 | -1.00 | | -2 | 0.15 | -1.00 | | 0 | 0.90 | 0.00 | | 2 | 0.85 | 0.95 | | 4 | 1.00 | 1.00 | </chart>
- `<class_Chart>` @(x=630, y=356, w=268, h=166) — from crops/slide_025.crop03__chart.parse.md (level 1)
  <chart type="multi_line"> title: vs Tanh legend[color]: items=Tanh Derivative ; Sigmoid Derivative bind: x ; ; x bind: Tanh Derivative ; ; y bind: Sigmoid Derivative ; ; y | x | Tanh Derivative | Sigmoid Derivative | | --- | --- | --- | | -5 | 0.81 | 0.81 | | -4 | 0.82 | 0.81 | | -2 | 0.67 | 0.65 | | 0 | 1.0 | 0.53 | | 2 | 0.65 | 0.25 | | 4 | 0.81 | 0.81 | </chart>
- `<class_Chart>` @(x=363, y=361, w=252, h=152) — from full/slide_025.parse.md (level 0)
  <chart type="multi_line"> title: Vanishing Gradients legend[color]: items=Tanh ; Sigmoid bind: Tanh ; ; y bind: Sigmoid ; ; y | column_1 | Tanh | Sigmoid | | --- | --- | --- | | -4 | 0.00 | 0.00 | | -3 | -1.00 | 0.10 | | -2 | 0.30 | -1.00 | | -1 | 0.50 | -0.80 | | 0 | 0.60 | 0.70 | | 1 | 0.90 | 0.95 | | 2 | 1.00 | 1.00 | | 3 | 1.00 | 1.00 | </chart>
- `<class_Chart>` @(x=640, y=362, w=248, h=154) — from full/slide_025.parse.md (level 0)
  <chart type="multi_line"> legend[color]: items=Tanh Derivative ; Sigmoid Derivative bind: Tanh Derivative ; ; y bind: Sigmoid Derivative ; ; y | x | Tanh Derivative | Sigmoid Derivative | | --- | --- | --- | | -5 | 0.0 | 0.0 | | -4 | 0.0 | 0.0 | | -3 | 0.1 | 0.1 | | -2 | 0.6 | 0.6 | | -1 | 0.5 | 0.7 | | 0 | 1.0 | 1.0 | | 1 | 0.5 | 0.5 | | 2 | 0.3 | 0.3 | | 3 | 0.1 | 0.1 | | 4 | 0.0 | 0.0 | </chart>
- `<class_Chart>` @(x=365, y=362, w=250, h=151) — from crops/slide_025.crop01__picture.parse.md (level 1)
  <chart type="multi_line"> title: Sigmoid vs Tanh legend[color]: items=Tanh ; Sigmoid bind: Tanh ; ; y bind: Sigmoid ; ; y annotation: callout ; label=0.25 | x | Tanh | Sigmoid | | --- | --- | --- | | -5 | 0.00 | -1.00 | | -4 | 0.02 | -1.00 | | -2 | 0.15 | -1.00 | | 0 | 0.60 | 0.00 | | 2 | 0.90 | 0.98 | | 4 | 1.00 | 1.00 | </chart>
- `<class_Chart>` @(x=631, y=370, w=265, h=150) — from crops/slide_025.crop08__chart.parse.md (level 2)
  <chart type="multi_line"> axis[y]: vs Tahm legend[color]: items=Tanh Derivative ; Sigmoid Derivative bind: Tanh Derivative ; ; y bind: Sigmoid Derivative ; ; y annotation: callout ; label=0.25 | x | Tanh Derivative | Sigmoid Derivative | | --- | --- | --- | | -5 | 0.81 | 0.80 | | -4 | 0.81 | 0.81 | | -3 | 0.65 | 0.82 | | -2 | 0.70 | 0.68 | | -1 | 0.75 | 0.75 | | 0 | 0.95 | 1.0 | | 1 | 0.70 | 0.70 | | 2 | 0.65 | 0.65 | | 3 | 0.60 | 0.60 | | 4 | 0.80 | 0.80 | </chart>
- `<class_Chart>` @(x=641, y=376, w=245, h=138) — from crops/slide_025.crop01__picture.parse.md (level 1)
  <chart type="multi_line"> legend[color]: items=Tanh Derivative ; Sigmoid Derivative bind: Tanh Derivative ; ; y bind: Sigmoid Derivative ; ; y annotation: callout ; label=1.0 ; value=0.25 | x | Tanh Derivative | Sigmoid Derivative | | --- | --- | --- | | -5 | 0.80 | 0.80 | | -4 | 0.81 | 0.80 | | -2 | 0.65 | 0.65 | | 0 | 1.0 | 0.55 | | 2 | 0.70 | 0.65 | | 4 | 0.80 | 0.80 | </chart>

## Unpositioned text

- (none)

## Failed calls

- (none)

## Notes

- backstop stops: 0
- parse calls spent: 9 · chat calls: 0 · retries: 0

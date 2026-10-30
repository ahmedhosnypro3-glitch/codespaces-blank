# Composed parse: slide_025

- source frame: `slide_025.jpg` (md5 `a82380b2460d1b93d2a3e0e52bedea34`)
- parse model: `nemotron-3.5-parse` · chat model: `docparsechat`
- degraded: True (chat probe failed — decisions use the deterministic-conservative fallback)
- elements kept: 12 (dedup collapsed 1) · crops: 6 · failed calls: 0

## Positioned elements (reading order: y then x)

- `<class_Picture>` @(x=35, y=42, w=886, h=475) — from full/slide_025.parse.md (level 0)
  17 Linear and Unit Step Activation Functions
- `<class_Picture>` @(x=50, y=42, w=853, h=474) — from crops/slide_025.crop01__picture.parse.md (level 1)
  **Linear and Unit Step Activation Functions** 17
- `<class_Page-header>` @(x=854, y=51, w=44, h=38) — from crops/slide_025.crop02__picture.parse.md (level 2)
  17
- `<class_Section-header>` @(x=242, y=69, w=513, h=30) — from crops/slide_025.crop02__picture.parse.md (level 2)
  **Linear and Unit Step Activation Functions**
- `<class_Picture>` @(x=282, y=112, w=625, h=164) — from crops/slide_025.crop03__picture.parse.md (level 3)
  f(x) F(x) = x Linear (No Activation) X
- `<class_Picture>` @(x=305, y=118, w=579, h=152) — from crops/slide_025.crop02__picture.parse.md (level 2)
  f(x) X F(x)=x _Linear (No Activation)_
- `<class_Picture>` @(x=122, y=281, w=315, h=163) — from crops/slide_025.crop05__picture.parse.md (level 3)
  f ( x)A X
- `<class_Picture>` @(x=475, y=287, w=303, h=152) — from crops/slide_025.crop02__picture.parse.md (level 2)
  f(x) x F(x)= Uni-polar Unit Step = 0 for x<0 1 for x≥0
- `<class_Picture>` @(x=133, y=287, w=292, h=151) — from crops/slide_025.crop02__picture.parse.md (level 2)
  f(x) x
- `<class_Formula>` @(x=482, y=458, w=311, h=49) — from crops/slide_025.crop06__formula.parse.md (level 3)
  \(F(x)=\mathrm{Bi-polar\text{Unit Step}=\{\begin{array}{ c c } -1 & \text{\textit{for x<0}} \\ 1 & \text{\textit{for x≥0}} 0 \end{array}\)
- `<class_Formula>` @(x=494, y=460, w=288, h=46) — from crops/slide_025.crop02__picture.parse.md (level 2)
  F(x)= Bi-polar Unit Step = 1 for x<0 1 for x≥0
- `<class_Text>` @(x=119, y=460, w=292, h=46) — from crops/slide_025.crop02__picture.parse.md (level 2)
  F(x)= Uni-polar Unit Step = 0 for x<0 1 for x≥0

## Unpositioned text

- (none)

## Failed calls

- (none)

## Notes

- backstop stops: 0
- parse calls spent: 7 · chat calls: 0 · retries: 0

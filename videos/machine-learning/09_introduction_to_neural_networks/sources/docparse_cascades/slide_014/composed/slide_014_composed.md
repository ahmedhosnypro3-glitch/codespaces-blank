# Composed parse: slide_014

- source frame: `slide_014.jpg` (md5 `46812416d9a06acc7e34b6a232f51f32`)
- parse model: `nemotron-3.5-parse` · chat model: `docparsechat`
- degraded: False
- elements kept: 7 (dedup collapsed 1) · crops: 4 · failed calls: 0

## Positioned elements (reading order: y then x)

- `<class_Picture>` @(x=50, y=42, w=848, h=48) — from full/slide_014.parse.md (level 0)
  **Using Two Perceptron Layers** 14
- `<class_Picture>` @(x=63, y=92, w=509, h=220) — from crops/slide_014.crop02__picture.parse.md (level 1)
  1 1 X1 W11 Σ W31 Σ O/P X2 W21 S Σ 2
- `<class_Picture>` @(x=82, y=100, w=472, h=205) — from full/slide_014.parse.md (level 0)
  1 1 W11 ∑ >0 ⇒ 1 <0 ⇒ 0 x1 W12 Σ O/P X2 W21 3 W22 Σ 2
- `<class_Picture>` @(x=62, y=306, w=554, h=180) — from crops/slide_014.crop03__table.parse.md (level 1)
  Sum 1 = W11 x1 + W12 x2 Sum 2 = W21 x1 + W22 x2 Sum 3 = (W11 x1 + W12 x2)w31 + (W21 x1 + W22 x2)w32 = (W11 w31 + W21 w32)x1 + (W21 w31 + W22 w32)x2 = W'1 x1 + W2 x2 ⇒ Still Linear Equation
- `<class_Table>` @(x=83, y=313, w=513, h=168) — from full/slide_014.parse.md (level 0)
  \begin{tabular}{cc} **Sum 1 =** & **W11 x1 + W12 x2** & **Sum 2 =** & **W21 x1 + W22 x2**\\ **Sum 3 =** & (W11 x1 + W12 x2) w31 + (W21 x1 + W22 x2) w32 & (W11 w31 + W21 w32) x1 + (W21 w31 + W22 w32) x2 & (W11 x1 + W2 x2 ) Still Linear Equation\\ \end{tabular}
- `<class_Picture>` @(x=595, y=332, w=304, h=118) — from crops/slide_014.crop04__picture.parse.md (level 1)
  X1 W1 Σ O/P X2 W2
- `<class_Picture>` @(x=606, y=336, w=283, h=110) — from full/slide_014.parse.md (level 0)
  X1 O/P X2 W2

## Unpositioned text

- (none)

## Failed calls

- (none)

## Notes

- backstop stops: 0
- parse calls spent: 5 · chat calls: 1 · retries: 0

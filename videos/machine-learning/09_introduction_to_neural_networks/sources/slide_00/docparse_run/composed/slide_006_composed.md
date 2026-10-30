# Composed parse: slide_006

- source frame: `slide_006.jpg` (md5 `5f57c80f57d59a0cd86d11358d14b595`)
- parse model: `nemotron-3.5-parse` · chat model: `docparsechat`
- degraded: True (chat probe failed — decisions use the deterministic-conservative fallback)
- elements kept: 2 (dedup collapsed 1) · crops: 2 · failed calls: 0

## Positioned elements (reading order: y then x)

- `<class_Picture>` @(x=36, y=42, w=862, h=474) — from full/slide_006.parse.md (level 0)
  **Visualization of Single Layer Perceptron** 6 d1(X) = W1 T X = w11 x1+w12x2+......+w1n xn+b1*1 d2(X) = W2 T X = w21 x1+w22x2+......+w2n xn+b2*1 dm(X) = Wm T X = wm1 x1+wm2x2+......+wmnxn+bm*1 Multi-Class Classification
- `<class_Chart>` @(x=36, y=42, w=871, h=475) — from crops/slide_006.crop01__picture.parse.md (level 1)
  <chart type="other"> title: Visualization of Single Layer Perceptron | column_1 | column_2 | | --- | --- | | x1 | w11 | | x2 | w13 | | x3 | w22 | | ... | w1n | | b1 | wm1 | | xn | wm2 | | 1 | wmn | | bm | Σ | </chart>

## Unpositioned text

- (none)

## Failed calls

- (none)

## Notes

- backstop stops: 0
- parse calls spent: 3 · chat calls: 0 · retries: 0

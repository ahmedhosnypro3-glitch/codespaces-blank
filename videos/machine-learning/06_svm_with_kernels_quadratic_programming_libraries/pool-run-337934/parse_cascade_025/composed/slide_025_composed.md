# Composed parse: slide_025

- source frame: `slide_025.jpg` (md5 `c6cf4f8898773890fef1b7bae2dc0326`)
- parse model: `nemotron-3.5-parse` · chat model: `docparsechat`
- degraded: True (chat probe failed — decisions use the deterministic-conservative fallback)
- elements kept: 8 (dedup collapsed 0) · crops: 2 · failed calls: 0

## Positioned elements (reading order: y then x)

- `<class_Caption>` @(x=252, y=59, w=528, h=29) — from full/slide_025.parse.md (level 0)
  **Quadratic Kernel Mapping and Kernel Trick**
- `<class_Page-header>` @(x=862, y=64, w=24, h=17) — from full/slide_025.parse.md (level 0)
  25
- `<class_Formula>` @(x=46, y=84, w=557, h=142) — from crops/slide_025.crop01__formula.parse.md (level 1)
  a \((\begin{array}{ c } a_1 \\ a_2 \end{array}b(\begin{array}{ c } b_1 \\ b_2 \end{array}\)<br> \([a^T b]^2=([(a_1,a_2)(b_1/b_2)]^2=(a_1b_1+a_2b_2)^2=a_1^2b_1^2+a_2^2b_2^2+2a_1b_1a_2b_2\)
- `<class_Formula>` @(x=66, y=89, w=517, h=132) — from full/slide_025.parse.md (level 0)
  a a1 b b1 a2 b<sup>[aT b]</sup> = [a1 a2] b1 b2] 12 = [a1 b1+a2 b2]2 = a1 2 b2 +a2 b2 +2a1 b1a2b2
- `<class_Text>` @(x=542, y=232, w=280, h=86) — from full/slide_025.parse.md (level 0)
  Where: φ(x) ≡ x1 x2 ⇒ x1 2 x2 2 √2x1x2
- `<class_Formula>` @(x=57, y=234, w=425, h=97) — from crops/slide_025.crop02__formula.parse.md (level 1)
  \([a^Tb]^2=(a_1^2a_2^2\sqrt{2}a_1a_2)|\frac{b_1^2}{b_2^2}{\sqrt{2}b_1b_2})=\phi(a)^T\phi(b)\)
- `<class_Formula>` @(x=73, y=238, w=394, h=89) — from full/slide_025.parse.md (level 0)
  [aT b]12 = [a1 a2 √2a1a2] b1 2 b2 2 v2 b1b2] = φ(a)Tφ(b)
- `<class_Picture>` @(x=685, y=322, w=91, h=17) — from full/slide_025.parse.md (level 0)
  **2D ⇒ 3D**

## Unpositioned text

- (none)

## Failed calls

- (none)

## Notes

- backstop stops: 0
- parse calls spent: 3 · chat calls: 0 · retries: 0

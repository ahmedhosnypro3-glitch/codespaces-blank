# Composed parse: slide_027

- source frame: `slide_027.jpg` (md5 `ab271ce32b7da248e5ec1a7af325c420`)
- parse model: `nemotron-3.5-parse` · chat model: `docparsechat`
- degraded: True (chat probe failed — decisions use the deterministic-conservative fallback)
- elements kept: 12 (dedup collapsed 0) · crops: 4 · failed calls: 0

## Positioned elements (reading order: y then x)

- `<class_Section-header>` @(x=400, y=58, w=229, h=30) — from full/slide_027.parse.md (level 0)
  **Polynomial Kernel**
- `<class_Text>` @(x=862, y=63, w=24, h=18) — from full/slide_027.parse.md (level 0)
  27
- `<class_Formula>` @(x=56, y=117, w=730, h=70) — from crops/slide_027.crop01__formula.parse.md (level 1)
  \(\mathbf{a}(\begin{array}{ c } a_1 \\ a_2 \end{array}\mathbf{b}(\begin{array}{ c } b_1 \\ b_2 \end{array}\)
- `<class_Formula>` @(x=71, y=120, w=712, h=64) — from full/slide_027.parse.md (level 0)
  a a1 b b1 b2 _Remember:_ [a T b]2 = [a1 a2 b1 )2 = a1 b1+a2b2]2 = a2 b2+a2 b2+2a1 b1a2b2
- `<class_Formula>` @(x=53, y=202, w=729, h=60) — from crops/slide_027.crop02__formula.parse.md (level 1)
  \(\big[\mathbf{a}^T\mathbf{b}+1\big]^2=(\mathbf{a}^T\mathbf{b})^2+2*\mathbf{a}^T\mathbf{b}+1=(a_1b_1+a_2b_2)^2=\overbrace{a_1^2b_1^2+a_2^2b_2^2+2a_1b_1a_2b_2}+2(a_1b_1+a_2b_2)+1\)
- `<class_Formula>` @(x=68, y=204, w=714, h=57) — from full/slide_027.parse.md (level 0)
  [a T b+1]2 = (aT b)2+2∗aT b+1 = (a1 b1+a2b2)2 = a2 b2+a2 b2+2a1 b1a2b2+2(a1 b1+a2b2)+1
- `<class_Formula>` @(x=433, y=280, w=344, h=28) — from full/slide_027.parse.md (level 0)
  = a2 b2+a2 b2+2a1 b1a2b2+2a1 b1+2a2b2+1
- `<class_Formula>` @(x=141, y=323, w=453, h=164) — from crops/slide_027.crop03__formula.parse.md (level 1)
  (a1 2 a2 2 √2 a1 a2 √2 a1 √2 a2 1) \(b_1^2\) b2 2 √2 b1 b2 √2 b1 √2 b2 1
- `<class_Formula>` @(x=158, y=329, w=420, h=153) — from full/slide_027.parse.md (level 0)
  [a2 1 a2 2 a1 a2 √2a1 a2 √2a2 1] b2 b2 b2 b2 2 b2 1
- `<class_Formula>` @(x=595, y=380, w=270, h=98) — from crops/slide_027.crop04__picture.parse.md (level 1)
  Where: \(\phi(x)\equiv\big(\frac{x_1}{x_2}\Rightarrow\Longrightarrow\sqrt{2}x_1x_2\sqrt{2}x_1\sqrt{2}x_2\text{1}\)
- `<class_Picture>` @(x=605, y=384, w=251, h=91) — from full/slide_027.parse.md (level 0)
  Where: φ(x) ≡ x1 x1 → √2 x1 x2 √2 x1 √2 x2 1
- `<class_Text>` @(x=745, y=479, w=96, h=18) — from full/slide_027.parse.md (level 0)
  **2D ⇒ 6D**

## Unpositioned text

- (none)

## Failed calls

- (none)

## Notes

- backstop stops: 0
- parse calls spent: 5 · chat calls: 0 · retries: 0

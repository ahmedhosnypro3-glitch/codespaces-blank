# Composed parse: slide_024

- source frame: `slide_024.jpg` (md5 `7549fb4afb11e1bb3944f858d5c3491c`)
- parse model: `nemotron-3.5-parse` · chat model: `docparsechat`
- degraded: False
- elements kept: 14 (dedup collapsed 0) · crops: 4 · failed calls: 0

## Positioned elements (reading order: y then x)

- `<class_Section-header>` @(x=88, y=60, w=225, h=25) — from full/slide_024.parse.md (level 0)
  **_For Sigmoid Function_**
- `<class_Page-header>` @(x=865, y=63, w=22, h=19) — from full/slide_024.parse.md (level 0)
  24
- `<class_Picture>` @(x=77, y=103, w=252, h=54) — from crops/slide_024.crop01__formula.parse.md (level 1)
  f( x) = Sigmoid (x) = 1 1 + e −x
- `<class_Formula>` @(x=86, y=105, w=236, h=52) — from full/slide_024.parse.md (level 0)
  f(x)= **Sigmoid** (x) = 1 1+e−x
- `<class_Text>` @(x=634, y=105, w=209, h=45) — from full/slide_024.parse.md (level 0)
  _Remember:_ ∂ ∂ x (1 x) = − 1 x<sup>2</sup>
- `<class_Formula>` @(x=71, y=166, w=505, h=60) — from crops/slide_024.crop02__formula.parse.md (level 1)
  \(f'(_x)=\frac{e^{--}}{(1+e^{--})(1+e^{--})}=\frac{1*(1+e^{--}-\cdot 1)}{(1+e^{--})(1+e^{--})}\)
- `<class_Formula>` @(x=90, y=168, w=468, h=57) — from full/slide_024.parse.md (level 0)
  f '(x)= e^{-x} (1+e^{-x}) = 1*(1+ e^{-x} -1) (1+e^{-x}) (1+e^{-x})
- `<class_Formula>` @(x=72, y=247, w=462, h=134) — from crops/slide_024.crop03__formula.parse.md (level 1)
  \(f'(_x)=\frac{1}{(1+e^{--})}(\frac{(1+e^{--}-1)}{(1+e^{--})})\)<br> \(=\frac{1}{(1+e^{--})}(\frac{(1+e^{--})}{(1+e^{--})}\frac{-1}{(1+e^{--})})\)
- `<class_Formula>` @(x=89, y=252, w=429, h=124) — from full/slide_024.parse.md (level 0)
  f '(x)= 1 (1+e-x) (1+e-x) ) = 1 (1+e-x) (1+e-x) (1+e-x)
- `<class_Text>` @(x=648, y=254, w=232, h=22) — from full/slide_024.parse.md (level 0)
  **Sigmoid (aka Logistic function)**
- `<class_Text>` @(x=646, y=293, w=235, h=78) — from full/slide_024.parse.md (level 0)
  It is a **squashing** function used to convert an unbounded values to a bounded **probabilistic** space _(from 0 to 1)_
- `<class_Formula>` @(x=78, y=416, w=347, h=58) — from crops/slide_024.crop04__formula.parse.md (level 1)
  \(f^t(_x)=\frac{1}{(1+e^{-x})}(1-\frac{1}{(1+e^{-x})})\)
- `<class_Formula>` @(x=91, y=418, w=323, h=54) — from full/slide_024.parse.md (level 0)
  f '(x)= 1 (1+e-x) 1 − 1 (1+e-x)
- `<class_Formula>` @(x=527, y=432, w=336, h=39) — from full/slide_024.parse.md (level 0)
  ⇒ f '(x)= f(x) [1−f(x)]

## Unpositioned text

- (none)

## Failed calls

- (none)

## Notes

- backstop stops: 0
- parse calls spent: 5 · chat calls: 1 · retries: 0

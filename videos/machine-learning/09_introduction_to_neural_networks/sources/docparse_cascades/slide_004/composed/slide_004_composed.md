# Composed parse: slide_004

- source frame: `slide_004.jpg` (md5 `7dcd91bafb7fb754e8bbe0afe6d78db2`)
- parse model: `nemotron-3.5-parse` · chat model: `docparsechat`
- degraded: False
- elements kept: 11 (dedup collapsed 0) · crops: 1 · failed calls: 0

## Positioned elements (reading order: y then x)

- `<class_Section-header>` @(x=350, y=57, w=283, h=29) — from full/slide_004.parse.md (level 0)
  **Problem Formulation**
- `<class_Text>` @(x=866, y=63, w=15, h=18) — from full/slide_004.parse.md (level 0)
  4
- `<class_Text>` @(x=72, y=109, w=115, h=24) — from full/slide_004.parse.md (level 0)
  **Define** δi as :
- `<class_Text>` @(x=73, y=134, w=779, h=52) — from full/slide_004.parse.md (level 0)
  _If_ X ∈ **_class I_** and _misclassified_ as **_Class II_** then d(X) will be <0 ⇒ δi = -1 ⇒ d(X) δi >0 _If_ X ∈ **_class II_** and misclassified as **_Class I_** then d(X) will be **>**0** ⇒ δi = +1 ⇒ d(X) δi >0
- `<class_Section-header>` @(x=71, y=229, w=232, h=22) — from full/slide_004.parse.md (level 0)
  **Redefine Error function as:**
- `<class_Text>` @(x=74, y=251, w=798, h=42) — from full/slide_004.parse.md (level 0)
  **Error**= ∑ δi W T Xi i ⇒ (W T Xi ) takes positive and negative values and δi has the same sign _all mislassified vectors_(i)
- `<class_Text>` @(x=70, y=294, w=228, h=22) — from full/slide_004.parse.md (level 0)
  _Summation is always positive_
- `<class_Text>` @(x=79, y=343, w=466, h=24) — from full/slide_004.parse.md (level 0)
  _Minimize the Error using Gradient Descent with step_ η
- `<class_Picture>` @(x=49, y=380, w=747, h=123) — from crops/slide_004.crop01__picture.parse.md (level 1)
  W(updated)= Wold - η ∂ Error ∂W where ∂ Error ∂W = ∑ mislcassified vectors δi Xi W(updated)= Wold - η ∑ mislcassified vectors ONLY (i) Update after each sample W(updated)= Wold
- `<class_Picture>` @(x=77, y=385, w=692, h=114) — from full/slide_004.parse.md (level 0)
  W (updated)= Wold - η Θ **Error** ∂ W where **where** σ Error ∂ W = ∑ mislcassed vectors δi Xi W (updated)= Wold - η ∑ mislcassed vectors ONLY (i)
- `<class_Formula>` @(x=654, y=449, w=226, h=32) — from full/slide_004.parse.md (level 0)
  W (updated)= Wold - η δi Xi

## Unpositioned text

- (none)

## Failed calls

- (none)

## Notes

- backstop stops: 0
- parse calls spent: 2 · chat calls: 1 · retries: 0

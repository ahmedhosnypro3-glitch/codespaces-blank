# Composed parse: slide_003

- source frame: `slide_003.jpg` (md5 `30b243b77890f8dcf465ccbb730e2bd6`)
- parse model: `nemotron-3.5-parse` · chat model: `docparsechat`
- degraded: False
- elements kept: 10 (dedup collapsed 0) · crops: 1 · failed calls: 0

## Positioned elements (reading order: y then x)

- `<class_Section-header>` @(x=350, y=57, w=283, h=28) — from full/slide_003.parse.md (level 0)
  **Problem Formulation**
- `<class_Page-header>` @(x=866, y=62, w=15, h=19) — from full/slide_003.parse.md (level 0)
  3
- `<class_Text>` @(x=73, y=92, w=368, h=109) — from full/slide_003.parse.md (level 0)
  Define two classes: _class I_ and _Class II_ _let d_ (X) _be a discriminant function_ = W T X if X ∈ class I then d(X) > 0 if X ∈ class II then d(X) < 0
- `<class_Section-header>` @(x=75, y=218, w=196, h=24) — from full/slide_003.parse.md (level 0)
  **For miscalssified** X :
- `<class_Text>` @(x=76, y=243, w=578, h=54) — from full/slide_003.parse.md (level 0)
  If X ∈ **class I** and misclassified as **Class II** then d(X) will be <0 If X ∈ **class II** and misclassified as **Class I** then d(X) will be **>**0**
- `<class_Section-header>` @(x=74, y=321, w=234, h=24) — from full/slide_003.parse.md (level 0)
  **Define Error function as:**
- `<class_Picture>` @(x=50, y=348, w=769, h=54) — from crops/slide_003.crop01__formula.parse.md (level 1)
  Error = \(\Sigma W^T X_i\v ⇧(W^T X_i)\) take positive and negative values _X_ all mislcassified vectors(i)
- `<class_Formula>` @(x=79, y=350, w=712, h=51) — from full/slide_003.parse.md (level 0)
  **Error** = ∑ W T Xi  (W T Xi) take positive and negative values X all mislclassified vectors(i)
- `<class_Section-header>` @(x=75, y=419, w=115, h=24) — from full/slide_003.parse.md (level 0)
  **Define** δi as :
- `<class_Text>` @(x=75, y=444, w=778, h=52) — from full/slide_003.parse.md (level 0)
  If X ∈ **class I** and misclassified as **Class II** then d(X) will be <0 ⇒ δi = -1 ⇒ d(X) δi >0 If X ∈ **class II** and misclassified as **Class I** then d(X) will be **>**0** ⇒ δi = +1 ⇒ d(X) δi >0

## Unpositioned text

- (none)

## Failed calls

- (none)

## Notes

- backstop stops: 0
- parse calls spent: 2 · chat calls: 1 · retries: 0

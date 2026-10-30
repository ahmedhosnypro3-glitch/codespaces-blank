# Composed parse: slide_029

- source frame: `slide_029.jpg` (md5 `50ae376cb7558f5e8057883cbd27dab0`)
- parse model: `nemotron-3.5-parse` · chat model: `docparsechat`
- degraded: True (chat probe failed — decisions use the deterministic-conservative fallback)
- elements kept: 7 (dedup collapsed 0) · crops: 6 · failed calls: 0

## Positioned elements (reading order: y then x)

- `<class_Picture>` @(x=35, y=42, w=872, h=475) — from full/slide_029.parse.md (level 0)
  Neural Network Model 29 _Input Sample_ _Target Label_ Neti Netj Netj = Summation at Node j Σ J 0O O i W ji Class 1 Oj Output at Node j Wji Weight from Node i to Node j Class 2 Number of I/P Nodes = Input Vector Length Number of O/P Nodes = Number of classes Class m i j Previous Layer Current Layer (You are here) For Layer “j” If Layer “j” is Output Layer: Netj = ∑ (wji Oi) Oj=f (Netj) = 1 E = 1/2 ∑(tj −Oj)2
- `<class_Picture>` @(x=49, y=42, w=858, h=475) — from crops/slide_029.crop01__picture.parse.md (level 1)
  Neural Network Model 29 _Input_ _Sample_ _Target_ _Label_ Neti Netj Netj ⇒ Summation at Node j Σ J ○○○ Σ Oi w ji Σ JOj _Output 1_ Wji Wji Wight from Node i to Node j **Class 1** **Class 2** Number of I/P Nodes = Input Vector Length Number of O/P Nodes = Number of classes **Class m** i **Previous** Layer **Current** Layer (You are here) **For Layer “j”** _If Layer “j” is Output Layer:_ Netj = ∑ (wjiOi) Oj=f (Netj) = 1 1+e−Netj E= 1⁄2 ∑ j (tj −Oj)2
- `<class_Picture>` @(x=49, y=42, w=857, h=474) — from crops/slide_029.crop03__picture.parse.md (level 3)
  **Neural Network Model** 29 _Input_ _Sample_ _Label_ Neti Netj Netj = Summation at Node j Σ J Oi Wji Σ JOj _Output 1_ Wji Wji Wight from Node i to Node j Class 2 Number of I/P Nodes = Input Vector Length Number of O/P Nodes = Number of classes Class m i j **Previous Layer** **Current** Layer (You are here) _For Layer “j”_ E = 1⁄2 ∑ (tj −Oj)2 Netj = ∑ (wj,Oi) Oj=f (Netj) = 1+e−Netj i E = 1⁄2 ∑ (tj −Oj)2
- `<class_Picture>` @(x=54, y=42, w=852, h=474) — from crops/slide_029.crop02__picture.parse.md (level 2)
  Neural Network Model 29 _Input_ _Sample_ _Target_ _Label_ Neti Netj Netj = Summation at Node j Σ J ○○○ Σ Oi wji Σ JOj Output 1 **Class 1** Wji Wji Weight from Node i to Node j **Class 2** Number of I/P Nodes = Input Vector Length Number of O/P Nodes = Number of classes **Class m** i **Previous Layer** **Current** Layer (You are here) _For Layer “j”_ _If Layer “j” is Output Layer:_ Netj = ∑ (wjjOi) Oj=f (Netj) = 1 1+e−Netj E= 1/2 ∑ j(tj −Oj)2
- `<class_Picture>` @(x=49, y=43, w=857, h=474) — from crops/slide_029.crop04__picture.parse.md (level 4)
  **Neural Network Model** 29 _Input_ _Sample_ _Target_ _Label_ Neti Netj Netj = Summation at Node j Σ J Oi Wji Σ JOj **Output 1** Wji Wji Wight from Node i to Node j **Class 1** **Class 2** Number of I/P Nodes = Input Vector Length Number of O/P Nodes = Number of classes **Class m** i **Previous** Layer **Current** Layer (You are here) **For Layer “j”** Netj = ∑ (wjiOi) Oj=f (Netj) = 1 1+e−Netj E= 1/2 ∑ j(tj −Oj)2
- `<class_Picture>` @(x=49, y=43, w=857, h=474) — from crops/slide_029.crop05__picture.parse.md (level 5)
  Neural Network Model 29 _Input_ _Sample_ _Target_ _Label_ Neti Netj Netj = Summation at Node j Σ J OO O i W ji Σ Oj _Output 1_ **Class 1** Wji wji Weight from Node i to Node j **Class 2** Number of I/P Nodes = Input Vector Length Number of O/P Nodes = Number of classes **Class m** i j **Previous** Layer **Current** Layer (You are here) _For Layer “j”_ _If Layer “j” is Output Layer:_ Netj = ∑ (wji Oi) Oj=f (Netj)= 1 1+e−Netj E= 1/2 ∑ j (tj −Oj)2
- `<class_Picture>` @(x=49, y=43, w=858, h=474) — from crops/slide_029.crop06__picture.parse.md (level 6)
  Neural Network Model 29 _Input_ _Sample_ _Target_ _Label_ Neti Netj Netj = Summation at Node j Σ J Oi Wji Σ Oj _Output 1_ **Class 1** Wji wji Weight from Node i to Node j **Class 2** Number of I/P Nodes = Input Vector Length Number of O/P Nodes = Number of classes **Class m** i **Previous** Layer **Current** Layer (You are here) _For Layer “j”_ Netj = ∑ (wjiOi) Oj=f (Netj)= 1 1+e−Netj E= 1/2 ∑ (tj −Oj)2

## Unpositioned text

- (none)

## Failed calls

- (none)

## Notes

- backstop stops: 1
- parse calls spent: 7 · chat calls: 0 · retries: 0

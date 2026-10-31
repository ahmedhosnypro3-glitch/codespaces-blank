# Composed parse: slide_015

- source frame: `slide_015.jpg` (md5 `677fcd3be57a3a0604539ae4248dc54a`)
- parse model: `nemotron-3.5-parse` · chat model: `docparsechat`
- degraded: False
- elements kept: 4 (dedup collapsed 2) · crops: 5 · failed calls: 0

## Positioned elements (reading order: y then x)

- `<class_Picture>` @(x=49, y=42, w=858, h=475) — from full/slide_015.parse.md (level 0)
  Neural Network Model (Weights of hidden layer AFFECT Calculated Error) 15 _Input Sample_ _Target Label_ Class 1 Σ J ∞ Σ N ij Wij Class 2 Error Error Error Next Layer Output 2 W # W Class m Class m 1 Node Bias i k For Layer “j” Previous Layer Layer (I) Current Layer (You are here) Note: Layer “j” is NOT Output Layer Net j = ∑ i (wjj Oi) E = 1/2 ∑ j (tj −Oj)2 X X X E = 1/2 ∑ x (tj −Oj)2 X X
- `<class_Picture>` @(x=57, y=42, w=840, h=475) — from crops/slide_015.crop01__picture.parse.md (level 1)
  Neural Network Model (Weights of hidden layer AFFECT Calculated Error) 15 _Input_ _Sample_ _Target_ _Label_ Neti Oi wji Net j Oj wkj Net k Ok Class 1 Σ S S Σ S Wji Wki Class 2 Error Error Error Class m 1 Node Bias i kj k For Layer “j” Previous Layer Layer (i) Current Layer (You are here) Next Layer Layer (K) Note: Layer “j” is NOT Output Layer Net j = ∑ (wjjOi) E= 1/2 ∑ (tj −Oj)2 XXX Oj=f (Netj)= 1 -Netj 1+e
- `<class_Picture>` @(x=54, y=43, w=842, h=474) — from crops/slide_015.crop02__picture.parse.md (level 2)
  Neural Network Model (Weights of hidden layer AFFECT Calculated Error) 15 _Input_ _Sample_ _Target_ _Label_ Neti Oi w ji Netj Oj w kj Netk Ok Σ S S Σ S S W ji W kj Class 1 Class 2 Class m 1 Node Bias i kj k For Layer “j” Previous Layer Current Layer (i) Next Layer (K) Note: Layer “j” is NOT Output Layer Netj = ∑ (wji Oi) E= 1/2 ∑ (tj −Oj)2 XXX Oj=f (Netj)= 1 +e−Netj
- `<class_Picture>` @(x=54, y=43, w=842, h=475) — from crops/slide_015.crop03__picture.parse.md (level 3)
  Neural Network Model (Weights of hidden layer AFFECT Calculated Error) 15 _Input_ _Sample_ _Target_ _Label_ Neti Oi w ji Netj Oj w kj Netk Ok Class 1 Σ S S Σ S W ji W ki Class 2 Class m 1 Node Bias i k i Current Layer Next Layer For Layer “j” Layer (i) Current Layer (You are here) Layer (K) Note: Layer “j” is NOT Output Layer Netj = ∑ (wji Oi) E= 1/2 ∑ (tj −Oj)2 XXX Oj=f (Netj)= 1 +e−Netj

## Unpositioned text

- (none)

## Failed calls

- (none)

## Notes

- backstop stops: 0
- parse calls spent: 6 · chat calls: 5 · retries: 3

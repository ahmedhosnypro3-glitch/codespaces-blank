# Composed parse: slide_022

- source frame: `slide_022.jpg` (md5 `87546b9e6dd23e38c2b5c185f1157e35`)
- parse model: `nemotron-3.5-parse` · chat model: `docparsechat`
- degraded: False
- elements kept: 9 (dedup collapsed 1) · crops: 2 · failed calls: 0

## Positioned elements (reading order: y then x)

- `<class_Picture>` @(x=37, y=42, w=881, h=220) — from crops/slide_022.crop01__picture.parse.md (level 1)
  Back Propagation Training Algorithm 22
- `<class_Picture>` @(x=38, y=43, w=881, h=493) — from full/slide_022.parse.md (level 0)
  **Back Propagation Training Algorithm 22**
- `<class_Text>` @(x=52, y=265, w=326, h=21) — from crops/slide_022.crop01__picture.parse.md (level 1)
  [1] Initialize all Weights with random values
- `<class_Text>` @(x=53, y=285, w=556, h=21) — from crops/slide_022.crop01__picture.parse.md (level 1)
  [2] Provide one training sample at a time (and its corresponding target label)
- `<class_Text>` @(x=51, y=318, w=792, h=28) — from crops/slide_022.crop01__picture.parse.md (level 1)
  [3] Go Forward : Start from Input Layer, Calculate Netj, Oj for each layer till reach output layer
- `<class_Text>` @(x=50, y=350, w=820, h=48) — from crops/slide_022.crop01__picture.parse.md (level 1)
  [4] Go Backward : Start from Output Layer, Calculate Δji, Wji for each weights of **Output** layer Δjj = η Oi Oj(1−Oj) (tj−Oj) **Store:** δj = Oj(1−Oj) (tj−Oj) _(for each node at output Layer)_
- `<class_Text>` @(x=50, y=409, w=866, h=59) — from crops/slide_022.crop01__picture.parse.md (level 1)
  [5] Go Backward : go to previous Layer, Calculate Δji, Wji for each weights of **Hidden** layer Δjj = η Oi Oj(1−Oj) [ ∑ k (δk wkj)] **Store:** δj = Oj(1−Oj) [ ∑ k (δkwkj)] _(for each node at hidden Layer)_
- `<class_Text>` @(x=48, y=479, w=345, h=25) — from crops/slide_022.crop01__picture.parse.md (level 1)
  [6] Repeat [5] till reach first hidden layer
- `<class_Text>` @(x=108, y=504, w=577, h=23) — from crops/slide_022.crop01__picture.parse.md (level 1)
  Remember: δk = δjof next layer ( which is already calculated in previous step )

## Unpositioned text

- (none)

## Failed calls

- (none)

## Notes

- backstop stops: 0
- parse calls spent: 3 · chat calls: 2 · retries: 0

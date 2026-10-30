# Composed parse: slide_028

- source frame: `slide_028.jpg` (md5 `3ec4323fe7f93e46819f7fd7dea31c10`)
- parse model: `nemotron-3.5-parse` · chat model: `docparsechat`
- degraded: True (chat probe failed — decisions use the deterministic-conservative fallback)
- elements kept: 4 (dedup collapsed 2) · crops: 5 · failed calls: 0

## Positioned elements (reading order: y then x)

- `<class_Picture>` @(x=36, y=42, w=887, h=475) — from full/slide_028.parse.md (level 0)
  Neural Network Model 28 _Input Sample_ Target Label Neti Net i Netk Class 1 Oi W ji X Oi W ki Output 1 Wji W ki Output 2 Class 2 Class m Class m i j k Previous Layer (i) Current Layer (You are here) Next Layer Layer (K) I/P Layer H id den Layer (s) O/P Layer
- `<class_Picture>` @(x=36, y=42, w=884, h=474) — from crops/slide_028.crop02__picture.parse.md (level 2)
  Neural Network Model 28 _Input_ _Sample_ Target Label Neti Netj Netk Oi Wji Oj wkj Output 1 Class 1 Wji Wkj Output 2 Class 2 Oi Oi Oj Ok Output m Class m i j k Previous Layer Current Layer (You are here) Next Layer Layer (K) I/P Layer Hidden Layer (s) O/P Layer
- `<class_Picture>` @(x=36, y=42, w=884, h=475) — from crops/slide_028.crop01__picture.parse.md (level 1)
  Neural Network Model 28 _Input_ _Sample_ Target Label Neti Netj Netk Σ S Oi Wji Σ S Oj wkj Output 1 Class 1 Wji Wkj Ok Output 2 Class 2 Oi Oi Oj Ok Output m Class m i j k Previous Layer Current Layer (You are here) Next Layer Layer (K) I/P Layer Hidden Layer (s) O/P Layer
- `<class_Picture>` @(x=36, y=42, w=883, h=476) — from crops/slide_028.crop04__picture.parse.md (level 4)
  Neural Network Model 28 _Input_ _Sample_ Target Label Neti Netj Netk Oi Wji Σs Oj wki Output 1 Class 1 Wji Wkj Output 2 Class 2 Oi Oi Oj Ok Output m Class m i j k Previous Layer Current Layer (You are here) Next Layer Layer (K) I/P Layer Hidden Layer (s) O/P Layer

## Unpositioned text

- (none)

## Failed calls

- (none)

## Notes

- backstop stops: 0
- parse calls spent: 6 · chat calls: 0 · retries: 0

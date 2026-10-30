# Composed parse: slide_028

- source frame: `slide_028.jpg` (md5 `0acf973df0a82a041370b58604cf85b7`)
- parse model: `nemotron-3.5-parse` · chat model: `docparsechat`
- degraded: True (chat probe failed — decisions use the deterministic-conservative fallback)
- elements kept: 3 (dedup collapsed 1) · crops: 3 · failed calls: 0

## Positioned elements (reading order: y then x)

- `<class_Picture>` @(x=37, y=42, w=892, h=476) — from crops/slide_028.crop01__picture.parse.md (level 1)
  28 (a2 1 a2 2 √2a1a2 √2a1 √2a2 1) b2 b2 b2 √2b1b2 √2b1 √2b2 1 = φ(a)Tφ(b) Where: φ(x) ≡ (x1 x2) ⇒ √2x1x2 √2x1 √2x2 1 α = [1 2] b = [3 4) (12 22 √2 1*2 √2 2√2 1) 32 φ(a)Tφ(b) = ↓ [1 4 2√2 √2 2√2 1) 9 9 16 12√2 3√2 4√2 1 [aT b+1]2 = (1*3+2*4+1)2=122=**144**
- `<class_Picture>` @(x=38, y=42, w=859, h=475) — from full/slide_028.parse.md (level 0)
  28 [a1 a2 2 √2a1a2 √2a1 √2a2 1] b1 b2 b2 √2b1b2 √2b1 √2b2 1 = φ(a)Tφ(b) Where: φ(x) ≡ x1 x2 ⇒ x1 x2 √2x1 √2x2 1 α = [1/2] b = [3/4] [12 22 √2 1*2 √2 2√2 1] 32 φ(a)Tφ(b) = 42 √2 3*4 3√2 √4√2 4√2 = [1 4 2√2 √2 2√2 1] 9 9 16 12√2 3√2/4√2 1 [aT b+1]2 = (1*3+2*4+1)2=122=**144**
- `<class_Picture>` @(x=37, y=42, w=892, h=476) — from crops/slide_028.crop02__picture.parse.md (level 2)
  28 (a21 a2 2 √2a1a2 √2a1 √2a2 1) b2 b2 b2 √2b1b2 √2b1 √2b1 √2b2 1 where: φ(x) ≡ (x1 x2) ⇒ √2x1x2 √2x1 √2x2 1 α = [1 2] b = [3 4) [12 22 √2 1*2 √2 2√2 1] 32 φ(a)T φ(b) = 42 √2 3*4 3√2 4√2 = [1 4 2√2 √2 2√2 1] 9 = 9+64+48+6+16+1=**144** [aT b+1]2 = (1*3+2*4+1)2=122=**144**

## Unpositioned text

- (none)

## Failed calls

- (none)

## Notes

- backstop stops: 0
- parse calls spent: 4 · chat calls: 0 · retries: 0

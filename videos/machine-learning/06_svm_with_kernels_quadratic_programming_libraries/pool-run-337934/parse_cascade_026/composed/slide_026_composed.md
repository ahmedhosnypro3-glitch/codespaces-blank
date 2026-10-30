# Composed parse: slide_026

- source frame: `slide_026.jpg` (md5 `e4740d88302ece2d44e02e81c232294d`)
- parse model: `nemotron-3.5-parse` · chat model: `docparsechat`
- degraded: True (chat probe failed — decisions use the deterministic-conservative fallback)
- elements kept: 2 (dedup collapsed 1) · crops: 2 · failed calls: 0

## Positioned elements (reading order: y then x)

- `<class_Picture>` @(x=37, y=42, w=877, h=475) — from crops/slide_026.crop01__picture.parse.md (level 1)
  **Quadratic Kernel Mapping and Kernel Trick** 26
- `<class_Picture>` @(x=38, y=42, w=844, h=467) — from full/slide_026.parse.md (level 0)
  **Quadratic Kernel Mapping and Kernel Trick** 26 a a1 b b1 b2 [aT b]2 = [a1 a2 b1 b2]2 = a1 b1+a2 b2=+2a1b1a2b2 [aT b]12 = [a1 a2 √2a1a2] b21 b2 2 b1 b2 = φ(a)Tφ(b) Where: φ(x) ≡ x1 x2 ⇒ x1 x2 2D ⇒ 3D a = 1/2 b = 3/4 φ(a)Tφ(b) = [12 22 √2 1*2] 32 42 42 = [1 4 √2 2] 9 16 √2 12 = 9+64+48=121 [aT b]2 = (1*3+2*4)2=112=121

## Unpositioned text

- (none)

## Failed calls

- (none)

## Notes

- backstop stops: 0
- parse calls spent: 3 · chat calls: 0 · retries: 0

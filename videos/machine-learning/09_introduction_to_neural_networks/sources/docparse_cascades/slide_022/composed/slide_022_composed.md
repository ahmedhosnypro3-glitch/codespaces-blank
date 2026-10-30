# Composed parse: slide_022

- source frame: `slide_022.jpg` (md5 `4f14a5dc1963d3a1b47822f556b823c6`)
- parse model: `nemotron-3.5-parse` · chat model: `docparsechat`
- degraded: False
- elements kept: 4 (dedup collapsed 0) · crops: 1 · failed calls: 0

## Positioned elements (reading order: y then x)

- `<class_Page-header>` @(x=856, y=52, w=39, h=35) — from full/slide_022.parse.md (level 0)
  22
- `<class_Section-header>` @(x=197, y=57, w=543, h=27) — from full/slide_022.parse.md (level 0)
  **Derivatives of some Activation Functions**
- `<class_Picture>` @(x=61, y=95, w=835, h=423) — from crops/slide_022.crop01__picture.parse.md (level 1)
  f(x)= Re ctified Linear U nit = \(\big\{0 for x<0\) x for x≥0 Derivative f '(x)= \(\big\{0 for x<0\) f(x)= P arametric ReLU = \(\big\{α x for x<0\) x for x≥0 + Derivative f '(x)= \(\big\{a for x<0\) f(x)= Exponential LU = \(\big\{α ( e^X-1 ) for x<0\) x for x≥0 Derivative f '(x)= \(\big\{f'(x)=\big\{f(x)+α for x<0\) f(x)= SoftPlus=loge (1+e^x) Derivative f '(x)= 1 1+e^{-x}
- `<class_Picture>` @(x=71, y=111, w=825, h=397) — from full/slide_022.parse.md (level 0)
  f(x)= Re ctified Linear U nit = 0 for x<0 x for x≥0 Derivative f'(x)= 0 for x<0 f(x)= P arametric ReLU = α x for x≤0 + Derivative f'(x)= 1 for x≥0 f(x)= Exponential LU = α ( e^X-1 ) for x<0 for x≥0 f(x)= SoftPlus= loge (1+e^x)

## Unpositioned text

- (none)

## Failed calls

- (none)

## Notes

- backstop stops: 0
- parse calls spent: 2 · chat calls: 1 · retries: 0

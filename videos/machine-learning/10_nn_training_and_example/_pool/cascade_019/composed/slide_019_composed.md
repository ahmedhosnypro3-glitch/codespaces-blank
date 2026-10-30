# Composed parse: slide_019

- source frame: `slide_019.jpg` (md5 `0eaafc4762f7b272b393aefb214d641c`)
- parse model: `nemotron-3.5-parse` · chat model: `docparsechat`
- degraded: True (chat probe failed — decisions use the deterministic-conservative fallback)
- elements kept: 5 (dedup collapsed 0) · crops: 2 · failed calls: 0

## Positioned elements (reading order: y then x)

- `<class_Picture>` @(x=35, y=43, w=878, h=199) — from crops/slide_019.crop01__picture.parse.md (level 1)
  19 W_ji Affects Netj ⇒ 19 **Netj** Affects Oj ⇒ Oj Affects ( **NetK=1**, **Netk=2**, ....., **Netk=m**) ⇒ ( **NetK=1**, **Netk=2**, ....., **Netk=m**) Affect **Error**
- `<class_Picture>` @(x=45, y=44, w=836, h=191) — from full/slide_019.parse.md (level 0)
  W_ji Affects Netj ⇒ Netj Affects Oj ⇒ Oj Affects (NetK=1, Netk=2, ....., Netk=m) ⇒ (NetK=1, Netk=2, ....., Netk=m) Affect **Error**
- `<class_Formula>` @(x=39, y=243, w=618, h=52) — from crops/slide_019.crop02__formula.parse.md (level 1)
  \(\frac{d E}{\partial w_{ji}=[\frac{d E}{\partial Net_{k=1}}\frac{d Net_{k=1}}{d O_j}+\frac{d E}{\partial Net_{k=2}}\frac{d Net_{k=2}}{d O_j}+\dots.+\frac{d E}{\partial Net_{k=m}\frac{d Net_{k=m}}{d O_j}]*\frac{d O_j}{d Net_j}+\frac{d Net_j}{d w_{ji}}\)
- `<class_Text>` @(x=648, y=243, w=218, h=222) — from full/slide_019.parse.md (level 0)
  ∂E ∂Netk ⇒ −δk Netk = ∑ k wkj Oj ⇒ ∂Netk ∂Oj = wkj Oj= 1 +e−Netj ⇒ ∂Oj ∂Netj =Oj(1-Oj) Netj = ∑ wjj Oi ⇒ ∂Netj ∂wjj =Oi
- `<class_Formula>` @(x=52, y=245, w=582, h=48) — from full/slide_019.parse.md (level 0)
  ∂E ∂E ∥ e wji = [∂E ∂Netk=1 ∂Oj + ∂E ∂Netk=2 ∂Oj + ..... + ∂E ∂Netk=m ∂Oj] + ∂Oj ∂Netj + ∂Netj ∂wji

## Unpositioned text

- (none)

## Failed calls

- (none)

## Notes

- backstop stops: 0
- parse calls spent: 3 · chat calls: 0 · retries: 0

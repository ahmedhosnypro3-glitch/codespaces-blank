# Composed parse: slide_020

- source frame: `slide_020.jpg` (md5 `9afe760e2d0c90462632901f5482fbf3`)
- parse model: `nemotron-3.5-parse` · chat model: `docparsechat`
- degraded: False
- elements kept: 3 (dedup collapsed 1) · crops: 3 · failed calls: 0

## Positioned elements (reading order: y then x)

- `<class_Picture>` @(x=38, y=40, w=889, h=495) — from full/slide_020.parse.md (level 0)
  W_ji Affects Netj ⇒ Netj Affects Oj ⇒ Oj Affects (NetK=1,Netk=2, ....., Netk=m) ⇒ (NetK=1,Netk=2, ....., Netk=m) Affect **Error** ∂E ∂E ∂E k=1 ∂Netk=1 ∂Oj + ∂E ∂Netk=2 + .....+ ∂E ∂Netk=m ∂Oj + ∂Oj ∂Netj + ∂Netj ∂wjj ∂E ∂E m∑ k=m ∂E eNetk ∂Oj + ∂Oj ∂Netj ∗ ∂Netj = ∑ k=1 −δk wkj ∗ Oj(1−Oj) ∗ Oi ∂E E∂Oj ∂E/∂Netj ∂E/∂Netj=-δj ∂E/∂wjj Δjj = -η ∂EW j = ∑ m δkwkj ⇒ Oj(1−Oj) ∗ Oi = η δj ∗ Oi Where δj = ∑ mk=1 δkwwkj ∗ Oj(1−Oj) _( for each Node j at hidden layer )_
- `<class_Picture>` @(x=35, y=42, w=891, h=495) — from crops/slide_020.crop02__picture.parse.md (level 2)
  W ji Affects Net j ⇒ 20 **Netj** Affects Oj ⇒ Oj Affects ( **NetK=1**, **Netk=2**, ....., **Netk=m**) ⇒ ( **NetK=1**, **Netk=2**, ....., **Netk=m**) Affect **Error** 1 Node Bix i 1 k ∂E ∂ e wji = [ ∂E ∂ Netk=1 ∂Oj + ∂E ∂ Netk=2 ∂Oj + .... + ∂E ∂ Netk=m ∂Oj] * ∂Oj ∂ Netj ∂ wji ∂E ∂ e wji = [ ∑ m k=1 ∂E ∂ Netk ∂Oj k * ∂Oj j * ∂Netj * ∂Netj j = [ ∑ m −δk wkj] * Oj(1−Oj) * Oi ∂E l/∂Oj ∂E l/∂Netj ∂E l/∂Netj=-δj ∂E l/∂wji ∂E l/∂wji Δji = -η ∂E ∂Wji = ∑ m δk wkj * Oj(1−Oj) * Oi = η δj * Oi _Where_ δj = ∑ m δk wkj * Oj(1−Oj) _( for each Node j at hidden layer )_
- `<class_Picture>` @(x=35, y=42, w=891, h=495) — from crops/slide_020.crop01__picture.parse.md (level 1)
  W ji Affects Netj ⇒ 20 **Netj** Affects Oj ⇒ Oj Affects (**NetK=1**, **Netk=2**, ....., **Netk=m**) ⇒ (**NetK=1**, **Netk=2**, ....., **Netk=m**) Affect **Error** ∂E ∂ e di e k ⇒ −δk ∂wji = [m e k=1 ∂Netk e1 + ∂E ∂Netk e2 ∂Oj + .... + ∂E ∂Netk e m ∂Oj j * ∂Oj e ∂Netj e wkj ∂E ∂wji = [m e k=1 ∂Netk e ∂Netk e ∂Oj e ∂Oj e ∂Netj e = [∑ m −δk wkj] * Oj (1−Oj) * Oi ∂E l∂Oj ∂E l∂Netj ∂E l∂Netj =-δj ∂E l∂wji Δji = -η ∂E ∂Wji = ∑ m δkwkj oj ⇒ Oj (1−Oj) * Oi = η δj * Oi _Where_ δj = ∑ m δkwkj ∗ Oj (1−Oj) _( for each Node j at hidden layer )_

## Unpositioned text

- (none)

## Failed calls

- (none)

## Notes

- backstop stops: 0
- parse calls spent: 4 · chat calls: 3 · retries: 0

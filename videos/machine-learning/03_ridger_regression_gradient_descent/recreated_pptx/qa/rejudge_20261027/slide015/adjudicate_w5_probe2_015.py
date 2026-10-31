#!/usr/bin/env python3
"""W5 probe 2 for slide015: does the RENDER actually contain W inside J( ) on
eq1 line1, and the I in lambda*I*W on deriv line2? Compare asset PNGs + render."""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
A = f"{NS}/recreated_pptx/build/assets"
D = f"{NS}/recreated_pptx/qa/rejudge_20261027/slide015"
r = np.asarray(Image.open(f"{D}/render.png").convert("RGB")).astype(int)
o = np.asarray(Image.open(f"{NS}/unique_slides/slide_015.jpg").convert("RGB")).astype(int)
sc = r.shape[1] / 960.0

def band_profile(a, y0, y1, x0, x1, name):
    s = a.shape[1] / 960.0
    sub = a[int(y0 * s):int(y1 * s), int(x0 * s):int(x1 * s)]
    ink = sub.sum(axis=2) < 600
    cols = ink.sum(axis=0)
    prof = "".join("#" if c >= 2 else ("+" if c > 0 else ".") for c in cols)
    print(f"{name} y{y0}-{y1} x{x0}-{x1} ink={int(ink.sum())}")
    print("  " + prof)
    return ink

# eq1 line 1: cream rect A top area. render band y105.5-153, orig y109-152
print("== eq1 line1 opening J( ... ) ==")
ink_r = band_profile(r, 106, 152, 85, 300, "render")
ink_o = band_profile(o, 109, 152, 85, 300, "orig")

# asset eq_015_eq1_l1.png: find J( at left, measure ink between parens
p = np.asarray(Image.open(f"{A}/eq_015_eq1_l1.png").convert("RGBA")).astype(int)
alpha = p[:, :, 3] > 40
ys, xs = np.where(alpha)
print(f"asset eq1_l1 {p.shape[1]}x{p.shape[0]} ink bbox x{xs.min()}-{xs.max()} y{ys.min()}-{ys.max()}")
sub = alpha[ys.min():ys.max()+1, :400]
cols = sub.sum(axis=0)
print("asset left 400px col-profile: " + "".join("#" if c >= 2 else ("+" if c > 0 else ".") for c in cols))

# deriv line 2: render band y273.9-335.4; asset eq_015_deriv_l2.png tail
print("== deriv line2 tail (lambda I W) ==")
band_profile(r, 274, 335, 500, 894, "render")
band_profile(o, 274, 335, 500, 894, "orig")
p2 = np.asarray(Image.open(f"{A}/eq_015_deriv_l2.png").convert("RGBA")).astype(int)
alpha2 = p2[:, :, 3] > 40
ys2, xs2 = np.where(alpha2)
print(f"asset deriv_l2 {p2.shape[1]}x{p2.shape[0]} ink bbox x{xs2.min()}-{xs2.max()}")
tail = alpha2[:, max(0, p2.shape[1] - 500):]
cols2 = tail.sum(axis=0)
print("asset deriv_l2 right 500px col-profile: " + "".join("#" if c >= 2 else ("+" if c > 0 else ".") for c in cols2))
